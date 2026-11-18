#!/usr/bin/env python3
"""Transcribe a Tagalog/Taglish video or audio file into raw ASR text.

Produces the *raw* transcript that the filipino-asr-analyzer skill then cleans.
Accepts a local media file or a URL (YouTube and other sites supported by yt-dlp).

Usage:
    python transcribe.py <file-or-url> [--model small] [--language tl] [--out transcript.txt]

Requirements:
    pip install faster-whisper
    yt-dlp on PATH (only needed for URLs)
    ffmpeg on PATH (recommended)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
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


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # keep Tagalog diacritics intact on Windows consoles

    p = argparse.ArgumentParser(description="Raw Tagalog/Taglish transcription with faster-whisper.")
    p.add_argument("source", help="local audio/video file or URL")
    p.add_argument("--model", default="small",
                   help="Whisper model: tiny, base, small, medium, large-v3 (default: small). "
                        "Do not use *.en models; they are English-only.")
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
    p.add_argument("--gap", type=float, default=2.0,
                   help="report silences between cues longer than this many seconds (default 2; 0 = off)")
    args = p.parse_args()

    if not 0.5 <= args.slow <= 1.0:
        sys.exit("error: --slow must be between 0.5 and 1.0")

    if args.model.endswith(".en"):
        sys.exit("error: English-only models (*.en) cannot transcribe Tagalog; use e.g. --model small")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("error: faster-whisper is not installed; run: pip install faster-whisper")

    with tempfile.TemporaryDirectory() as tmp:
        if args.source.startswith(("http://", "https://")):
            print(f"Downloading audio: {args.source}", file=sys.stderr)
            media = download_audio(args.source, Path(tmp))
        else:
            media = Path(args.source)
            if not media.is_file():
                sys.exit(f"error: file not found: {media}")

        print(f"Loading model '{args.model}' (first run downloads it)...", file=sys.stderr)
        import ctranslate2

        on_gpu = ctranslate2.get_cuda_device_count() > 0
        model = WhisperModel(args.model, device="cuda" if on_gpu else "cpu",
                             compute_type="float16" if on_gpu else "int8")

        language = None if args.language == "auto" else args.language
        audio = load_audio(media, args.start, args.end, args.slow)
        offset = args.start or 0.0

        def real(t: float) -> float:  # map a time in the (cut, slowed) audio back to the source
            return offset + t * args.slow

        # Tuned on session 2026-11-16-01: with VAD + conditioning on previous text, Whisper
        # looped on earlier lines ("Suntalo!" x3) and skipped short cues. Turning both off
        # recovered them; word timestamps give tighter segment boundaries for dubbing.
        # Session 2026-11-16-04: Whisper scored the first 30 s window as no-speech (0.72 > 0.6)
        # and dropped ~20 lines of real dialogue, so the no-speech skip is off unless asked for.
        segments, info = model.transcribe(
            audio,
            language=language,
            beam_size=5,
            vad_filter=args.vad,
            condition_on_previous_text=False,
            word_timestamps=True,
            no_speech_threshold=0.6 if args.skip_quiet else None,
        )

        lines = [
            f"# source: {args.source}",
            f"# model: {args.model} | language: {info.language} ({info.language_probability:.2f}) "
            f"| duration: {fmt_time(info.duration * args.slow)}",
        ]
        if args.start is not None or args.end is not None or args.slow != 1.0:
            lines.append(f"# window: {fmt_time(offset)} -> "
                         f"{fmt_time(args.end) if args.end is not None else 'end'} | slow: {args.slow}")
        lines.append("")
        for line in lines:
            print(line, flush=True)
        # Session 2026-11-17-04: all three runs skipped 00:22-00:30 (dialogue right after the
        # narrator) and the start of the next line. Report every gap so it gets re-run alone.
        gaps = []
        prev_end = offset
        for seg in segments:  # generator: transcription happens while iterating
            start, end = real(seg.start), real(seg.end)
            if args.gap and start - prev_end >= args.gap:
                gaps.append((prev_end, start))
            prev_end = max(prev_end, end)
            text = seg.text.strip()
            line = text if args.no_timestamps else f"[{fmt_time(start)} -> {fmt_time(end)}] {text}"
            lines.append(line)
            print(line, flush=True)
        if gaps:
            lines += ["", f"# gaps of {args.gap:g}s+ with no cue: check each (silencedetect) or re-run "
                          "it alone with --start/--end"]
            lines += [f"# gap {fmt_time(a)} -> {fmt_time(b)} ({b - a:.0f}s)" for a, b in gaps]
            for line in lines[-len(gaps) - 1:]:
                print(line, file=sys.stderr)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Saved: {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
