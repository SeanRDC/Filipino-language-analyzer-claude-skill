#!/usr/bin/env python3
"""Transcribe a Tagalog/Taglish video or audio file into raw ASR text.

Produces the *raw* transcript that the filipino-asr-analyzer skill then cleans.
Accepts a local media file or a URL (YouTube and other sites supported by yt-dlp).

Usage:
    python transcribe.py <file-or-url> [--model small] [--language tl] [--out transcript.txt]
    python transcribe.py <file> --start 1:20 --end 1:50 --slow 0.75   # zoom on a hard stretch
    python transcribe.py <file> --device cpu --window 30              # second opinion on the CPU
    python transcribe.py <file> --windows 0:50-1:15,6:15-6:40 --speeds 1,0.75  # many windows, one model load

Devices (--device auto picks the first available):
    cuda  NVIDIA GPU, faster-whisper, beam search
    gpu   Intel Arc GPU via OpenVINO (pip install openvino-genai), greedy, 30 s windows
    cpu   faster-whisper int8, beam search, half the cores by default
On the CPU the process runs at low priority unless --priority normal.

Requirements:
    pip install faster-whisper   (plus openvino-genai for Intel GPUs)
    yt-dlp on PATH (only needed for URLs)
    ffmpeg on PATH (recommended)
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def fmt_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def download_audio(url: str, workdir: Path) -> Path:
    exe = shutil.which("yt-dlp")
    if not exe:
        sys.exit("error: yt-dlp is not on PATH; install it or pass a local file instead of a URL")
    cmd = [exe, "-f", "bestaudio/best", "--no-playlist", "-o", str(workdir / "audio.%(ext)s"), url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"error: yt-dlp failed:\n{result.stderr.strip()[-2000:]}")
    files = sorted(workdir.glob("audio.*"))
    if not files:
        sys.exit("error: yt-dlp finished but no audio file was produced")
    return files[0]


def parse_time(value: str) -> float:
    """Accept seconds ('83.5'), mm:ss ('1:23') or hh:mm:ss."""
    secs = 0.0
    for part in value.split(":"):
        secs = secs * 60 + float(part)
    return secs


def parse_ranges(value: str) -> list[tuple[float, float]]:
    """'0:50-1:15,6:15-6:40' -> [(50.0, 75.0), (375.0, 400.0)]."""
    ranges = []
    for item in value.split(","):
        start, sep, end = item.strip().partition("-")
        if not sep:
            raise argparse.ArgumentTypeError(f"window '{item}' needs start-end, e.g. 0:50-1:15")
        a, b = parse_time(start), parse_time(end)
        if b <= a:
            raise argparse.ArgumentTypeError(f"window '{item}' ends before it starts")
        ranges.append((a, b))
    return ranges


def parse_speeds(value: str) -> list[float]:
    speeds = [float(v) for v in value.split(",")]
    if not all(0.5 <= v <= 1.0 for v in speeds):
        raise argparse.ArgumentTypeError("speeds must be between 0.5 and 1.0")
    return speeds


def load_audio(media: Path, start: float | None = None, end: float | None = None,
               slow: float = 1.0):
    """Decode to 16 kHz mono float32 with ffmpeg, optionally cut to a window and slowed down.

    Bypasses faster-whisper's PyAV decoder, which breaks with some PyAV releases
    (e.g. PyAV 19 removed the `metadata_errors` argument faster-whisper 1.2.x passes).
    Returns the file path unchanged if ffmpeg is unavailable.
    """
    exe = shutil.which("ffmpeg")
    if not exe:
        if start is not None or end is not None or slow != 1.0:
            sys.exit("error: --start/--end/--slow need ffmpeg on PATH")
        return str(media)
    import numpy as np

    cmd = [exe, "-nostdin", "-loglevel", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if end is not None:
        cmd += ["-to", str(end)]
    cmd += ["-i", str(media)]
    if slow != 1.0:
        cmd += ["-af", f"atempo={slow}"]  # pitch-preserving time stretch
    cmd += ["-f", "s16le", "-ac", "1", "-ar", "16000", "-"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        sys.exit(f"error: ffmpeg could not decode {media}:\n{result.stderr.decode(errors='replace')[-2000:]}")
    return np.frombuffer(result.stdout, np.int16).astype(np.float32) / 32768.0


SR = 16000


def lower_priority(level: str) -> None:
    """Run below normal priority so a long transcription doesn't hog the machine.

    Only scheduling changes; the transcript is identical.
    """
    if level != "low":
        return
    try:
        if sys.platform == "win32":
            import ctypes
            BELOW_NORMAL_PRIORITY_CLASS = 0x4000
            k32 = ctypes.windll.kernel32
            k32.SetPriorityClass(k32.GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS)
        else:
            os.nice(10)
    except Exception:
        pass  # best effort


def openvino_devices() -> list[str]:
    try:
        import openvino as ov
        return list(ov.Core().available_devices)
    except Exception:
        return []


def pick_device(requested: str) -> str:
    """auto: NVIDIA GPU (CUDA) > Intel GPU (OpenVINO) > CPU."""
    if requested != "auto":
        if requested in ("gpu", "npu") and requested.upper() not in openvino_devices():
            sys.exit(f"error: no OpenVINO {requested.upper()} found (pip install openvino-genai; "
                     "needs an Intel GPU/NPU with current drivers)")
        return requested
    try:
        import ctranslate2
        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda"
    except ImportError:
        pass
    if "GPU" in openvino_devices():
        try:
            import openvino_genai  # noqa: F401
            return "gpu"
        except ImportError:
            pass
    return "cpu"


def faster_whisper_decoder(model_name: str, device: str, language, threads: int, vad: bool,
                           skip_quiet: bool):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("error: faster-whisper is not installed; run: pip install faster-whisper")
    model = WhisperModel(model_name, device=device,
                         compute_type="float16" if device == "cuda" else "int8",
                         cpu_threads=threads if device == "cpu" else 0)

    def decode(audio):
        # Tuned on session 2026-11-16-01: with VAD + conditioning on previous text, Whisper
        # looped on earlier lines ("Suntalo!" x3) and skipped short cues. Turning both off
        # recovered them; word timestamps give tighter segment boundaries for dubbing.
        # Session 2026-11-16-04: Whisper scored the first 30 s window as no-speech (0.72 > 0.6)
        # and dropped ~20 lines of real dialogue, so the no-speech skip is off unless asked for.
        segments, _ = model.transcribe(
            audio,
            language=language,
            beam_size=5,
            vad_filter=vad,
            condition_on_previous_text=False,
            word_timestamps=True,
            no_speech_threshold=0.6 if skip_quiet else None,
        )
        for s in segments:
            yield s.start, s.end, s.text.strip()

    return decode


def openvino_model_path(model_name: str) -> str:
    """Pre-converted fp16 Whisper from the OpenVINO org on Hugging Face (same weights as Whisper)."""
    from huggingface_hub import snapshot_download
    repo = f"OpenVINO/whisper-{model_name}-fp16-ov"
    try:
        return snapshot_download(repo, local_files_only=True)
    except Exception:
        pass
    last = None
    for _ in range(10):  # the Hub connection drops intermittently on some networks
        try:
            return snapshot_download(repo)
        except Exception as exc:
            last = exc
            time.sleep(2)
    sys.exit(f"error: could not download {repo}: {last}")


def openvino_decoder(model_name: str, device: str, language):
    try:
        import openvino_genai
    except ImportError:
        sys.exit("error: openvino-genai is not installed; run: pip install openvino-genai")
    pipe = openvino_genai.WhisperPipeline(openvino_model_path(model_name), device)
    cfg = pipe.get_generation_config()
    if language:
        cfg.language = f"<|{language}|>"
    cfg.task = "transcribe"
    cfg.return_timestamps = True
    cfg.num_beams = 1  # beam search is not implemented for Whisper on the Intel GPU

    def decode(audio):
        result = pipe.generate(audio.tolist(), cfg)
        for c in result.chunks or []:
            if c.text.strip():
                yield c.start_ts, c.end_ts, c.text.strip()

    return decode


def looks_looping(cues) -> bool:
    """True when a window's cues look like a decoding loop rather than speech.

    Greedy GPU decoding loops over music beds and shouting ("I'm sorry" x14 over an action
    scene, blind test 2026-11-18): one text repeated three or more times and making up at
    least half the cues, or cue times that run backwards.
    """
    if any(b < a for a, b, _ in cues):
        return True
    texts = [re.sub(r"\W+", " ", t).strip().lower() for _, _, t in cues]
    texts = [t for t in texts if t]
    if len(texts) < 3:
        return False
    top = max(texts.count(t) for t in set(texts))
    return top >= 3 and top * 2 >= len(texts)


def hidden_gaps(cues, min_len: float = 8.0, max_rate: float = 0.75):
    """Find stretches where speech may be hidden even though a cue covers them.

    large-v3-turbo can stretch one short line over 10-25 s of music and swallow the real
    speech around it, or write "..." cue after cue over a TV insert (blind test round 3,
    2026-11-19). The gap list misses both because every second has a cue. Normal speech here
    runs 2-3 words per second.

    Returns (hollow, wordless): hollow = [(start, end, words)] for cues of min_len seconds or
    more with fewer than max_rate words per second; wordless = merged (start, end) runs of
    cues that hold no words at all.
    """
    hollow, wordless = [], []
    for start, end, text in cues:
        words = len(re.findall(r"[^\W\d_]+", text))
        if not words:
            if wordless and start - wordless[-1][1] <= 1.0:
                wordless[-1] = (wordless[-1][0], max(wordless[-1][1], end))
            else:
                wordless.append((start, end))
        elif end - start >= min_len and words / (end - start) < max_rate:
            hollow.append((start, end, words))
    return hollow, wordless


NON_LATIN = re.compile(r"[Ͱ-ϿЀ-ӿ֐-ۿ฀-๿぀-ヿ一-鿿가-힯]")


def transcribe_windows(decode, audio, window: float, overlap: float = 5.0, fallback=None,
                       report=None):
    """Decode in overlapping windows, keeping each cue from the window where it sits centrally.

    Whisper sees every stretch away from a window edge, so lines cut by an edge in one
    window are whole in the next. Cue times are relative to the start of `audio`.
    `fallback()` returns a second decoder; a window whose cues loop is decoded again with it,
    and its start time is appended to `report`.
    """
    total = len(audio) / SR
    step = max(window - overlap, 1.0)
    starts, s = [], 0.0
    while True:
        starts.append(s)
        if s + window >= total:
            break
        s += step
    out = []
    for i, s in enumerate(starts):
        e = min(s + window, total)
        keep_from = 0.0 if i == 0 else s + overlap / 2
        keep_to = total if i == len(starts) - 1 else e - overlap / 2
        chunk = audio[int(s * SR):int(e * SR)]
        cues = list(decode(chunk))
        if fallback is not None and looks_looping(cues):
            cues = list(fallback()(chunk))
            if report is not None:
                report.append(s)
        for a, b, text in cues:
            mid = s + (a + b) / 2
            if keep_from <= mid < keep_to:
                out.append((s + a, s + b, text))
    return out


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # keep Tagalog diacritics intact on Windows consoles

    p = argparse.ArgumentParser(description="Raw Tagalog/Taglish transcription (faster-whisper on CPU/CUDA, OpenVINO on Intel GPU/NPU).")
    p.add_argument("source", help="local audio/video file or URL")
    p.add_argument("--model", default="auto",
                   help="Whisper model: auto (default), tiny, base, small, medium, large-v3-turbo, "
                        "large-v3. auto = large-v3-turbo on a GPU, small on CPU-only machines. "
                        "Do not use *.en models; they are English-only.")
    p.add_argument("--fallback-model", default="small",
                   help="model for the CPU loop guard on gpu/npu (default: small, light on the CPU)")
    p.add_argument("--language", default="tl",
                   help="language code (default: tl). Use 'auto' to let Whisper detect it.")
    p.add_argument("--out", type=Path, help="also write the transcript to this file")
    p.add_argument("--no-timestamps", action="store_true", help="omit [mm:ss] timestamps")
    p.add_argument("--vad", action="store_true",
                   help="enable voice-activity filtering (faster on long, quiet media, but drops short "
                        "interjections and commands like 'Ay!' or 'Attention!')")
    p.add_argument("--skip-quiet", action="store_true",
                   help="let Whisper drop 30-second windows it judges to be silence (its stock "
                        "behavior). Off by default: on noisy Tagalog speech it threw away whole "
                        "windows of real dialogue")
    p.add_argument("--start", type=parse_time,
                   help="transcribe from this time (seconds or mm:ss). Re-run gaps and hard stretches "
                        "on their own: Whisper often drops lines right after a speaker or language switch")
    p.add_argument("--end", type=parse_time, help="transcribe up to this time (seconds or mm:ss)")
    p.add_argument("--slow", type=float, default=1.0,
                   help="play the audio at this speed before transcribing, 0.5-1.0 (e.g. 0.75). Helps "
                        "with rapid-fire lines; timestamps are mapped back to the original timing")
    p.add_argument("--windows", type=parse_ranges,
                   help="several windows in one call, e.g. '0:50-1:15,6:15-6:40'. The model loads "
                        "once, so this is much faster than one call per window")
    p.add_argument("--speeds", type=parse_speeds,
                   help="run every window at each of these speeds, e.g. '1,0.75' (default: --slow)")
    p.add_argument("--gap", type=float, default=2.0,
                   help="report silences between cues longer than this many seconds (default 2; 0 = off)")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "gpu", "npu"],
                   help="auto (default): NVIDIA GPU, else Intel GPU via OpenVINO, else CPU. 'gpu'/'npu' "
                        "use OpenVINO (Intel Arc / AI Boost); 'cpu' uses faster-whisper with beam search")
    p.add_argument("--window", type=float, default=0.0,
                   help="decode in overlapping windows of this many seconds (e.g. 30) instead of one "
                        "long pass; this is the zoom pass from SKILL.md 0b. Always 30 on gpu/npu")
    p.add_argument("--threads", type=int, default=max(1, (os.cpu_count() or 2) // 2),
                   help="CPU threads for --device cpu (default: half the cores; same transcript, "
                        "less heat and fan noise)")
    p.add_argument("--priority", default="low", choices=["low", "normal"],
                   help="process priority (default: low, so other apps stay responsive)")
    p.add_argument("--no-loop-fallback", action="store_true",
                   help="on gpu/npu, do not re-decode looping 30 s windows on the CPU (beam search)")
    args = p.parse_args()

    if not 0.5 <= args.slow <= 1.0:
        sys.exit("error: --slow must be between 0.5 and 1.0")
    if args.windows and (args.start is not None or args.end is not None):
        sys.exit("error: use either --windows or --start/--end, not both")

    if args.model.endswith(".en"):
        sys.exit("error: English-only models (*.en) cannot transcribe Tagalog; use e.g. --model small")

    lower_priority(args.priority)
    device = pick_device(args.device)
    if args.model == "auto":
        # Blind test 2026-11-19 (10 captioned drama clips, raw word accuracy on the held-out set):
        # small 54%, medium 66%, large-v3-turbo 75%, at ~10-25 s per clip on an Intel Arc iGPU.
        # On a CPU, turbo is slow and loud, so weak or GPU-less machines stay on small.
        args.model = "small" if device == "cpu" else "large-v3-turbo"

    with tempfile.TemporaryDirectory() as tmp:
        if args.source.startswith(("http://", "https://")):
            print(f"Downloading audio: {args.source}", file=sys.stderr)
            media = download_audio(args.source, Path(tmp))
        else:
            media = Path(args.source)
            if not media.is_file():
                sys.exit(f"error: file not found: {media}")

        print(f"Loading model '{args.model}' on {device}...", file=sys.stderr)
        language = None if args.language == "auto" else args.language
        fallback = None
        if device in ("gpu", "npu"):
            decode = openvino_decoder(args.model, device.upper(), language)
            window = args.window or 30.0  # its long-form mode dropped the last 10 s of a clip
            decoder_note = f"openvino {device.upper()} fp16, greedy"
            if not args.no_loop_fallback:
                cpu = []  # load the CPU model only if a window actually loops

                def fallback():
                    if not cpu:
                        print(f"Loop detected: re-decoding on cpu ({args.fallback_model}, beam 5)...",
                              file=sys.stderr)
                        cpu.append(faster_whisper_decoder(args.fallback_model, "cpu", language, args.threads,
                                                          args.vad, args.skip_quiet))
                    return cpu[0]
                decoder_note += ", looping windows re-decoded on cpu"
        else:
            decode = faster_whisper_decoder(args.model, device, language, args.threads, args.vad,
                                            args.skip_quiet)
            window = args.window
            decoder_note = (f"faster-whisper {device}, beam 5"
                            + (f", {args.threads} threads" if device == "cpu" else ""))

        out: list[str] = []

        def run_range(start_at, end_at, slow):
            audio = load_audio(media, start_at, end_at, slow)
            if isinstance(audio, str):
                sys.exit("error: ffmpeg is required on PATH")
            offset = start_at or 0.0
            total = len(audio) / SR

            def real(t: float) -> float:  # map a time in the (cut, slowed) audio back to the source
                return offset + t * slow

            redone = []
            segments = (transcribe_windows(decode, audio, window, fallback=fallback, report=redone)
                        if window else decode(audio))

            lines = [] if out else [
                f"# source: {args.source}",
                f"# model: {args.model} | language: {args.language} | decoder: {decoder_note}"
                + (f" | windows: {window:g}s" if window else "")
                + f" | duration: {fmt_time(total * slow)}",
            ]
            if start_at is not None or end_at is not None or slow != 1.0:
                lines.append(f"# window: {fmt_time(offset)} -> "
                             f"{fmt_time(end_at) if end_at is not None else 'end'} | slow: {slow}")
            lines.append("")
            for line in lines:
                print(line, flush=True)
            # Session 2026-11-17-04: all three runs skipped 00:22-00:30 (dialogue right after the
            # narrator) and the start of the next line. Report every gap so it gets re-run alone.
            gaps = []
            odd = []
            cues = []
            prev_end = offset
            for seg_start, seg_end, text in segments:  # may be a generator: decoding happens here
                start, end = real(seg_start), real(seg_end)
                cues.append((start, end, text))
                if args.gap and start - prev_end >= args.gap:
                    gaps.append((prev_end, start))
                prev_end = max(prev_end, end)
                if NON_LATIN.search(text):
                    odd.append((start, text))
                line = text if args.no_timestamps else f"[{fmt_time(start)} -> {fmt_time(end)}] {text}"
                lines.append(line)
                print(line, flush=True)
            if args.gap and real(total) - prev_end >= args.gap:  # speech lost at the very end
                gaps.append((prev_end, real(total)))
            if gaps:
                lines += ["", f"# gaps of {args.gap:g}s+ with no cue: check each (silencedetect) or re-run "
                              "it alone with --start/--end (several at once: --windows)"]
                lines += [f"# gap {fmt_time(a)} -> {fmt_time(b)} ({b - a:.0f}s)" for a, b in gaps]
                for line in lines[-len(gaps) - 1:]:
                    print(line, file=sys.stderr)

            notes = []
            if redone:  # blind test 2026-11-18: greedy GPU decoding looped in 9 of 10 drama clips
                notes.append("# loop guard: windows re-decoded on cpu at "
                             + ", ".join(fmt_time(real(t)) for t in redone))
            if odd:  # the CPU decoder sometimes emits Greek/Cyrillic letters in Tagalog
                notes.append("# non-Latin script in a cue (likely hallucination): "
                             + ", ".join(fmt_time(t) for t, _ in odd))
            hollow, wordless = hidden_gaps(cues)
            if hollow:
                notes.append("# hollow cues (long cue, few words: speech may be hidden; re-run as a "
                             "window): " + ", ".join(f"{fmt_time(a)} -> {fmt_time(b)} ({n} words in "
                                                     f"{b - a:.0f}s)" for a, b, n in hollow))
            if wordless:
                notes.append("# wordless cues ('...' or symbols only: treat as gaps): "
                             + ", ".join(f"{fmt_time(a)} -> {fmt_time(b)}" for a, b in wordless))
            if notes:
                lines += [""] + notes
                for line in notes:
                    print(line, file=sys.stderr)

            if out:
                out.append("")
            out.extend(lines)

        # --windows: many ranges in one call, so the model loads once (round 3 spent most of
        # 20 minutes reloading turbo for 113 separate window runs).
        for start_at, end_at in (args.windows or [(args.start, args.end)]):
            for slow in (args.speeds or [args.slow]):
                run_range(start_at, end_at, slow)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"Saved: {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
