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


def load_audio(media: Path):
    """Decode to 16 kHz mono float32 with ffmpeg.

    Bypasses faster-whisper's PyAV decoder, which breaks with some PyAV releases
    (e.g. PyAV 19 removed the `metadata_errors` argument faster-whisper 1.2.x passes).
    Returns the file path unchanged if ffmpeg is unavailable.
    """
    exe = shutil.which("ffmpeg")
    if not exe:
        return str(media)
    import numpy as np

    cmd = [exe, "-nostdin", "-loglevel", "error", "-i", str(media),
           "-f", "s16le", "-ac", "1", "-ar", "16000", "-"]
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
    args = p.parse_args()

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
        audio = load_audio(media)
        # Tuned on session 2026-11-16-01: with VAD + conditioning on previous text, Whisper
        # looped on earlier lines ("Suntalo!" x3) and skipped short cues. Turning both off
        # recovered them; word timestamps give tighter segment boundaries for dubbing.
        segments, info = model.transcribe(
            audio,
            language=language,
            beam_size=5,
            vad_filter=args.vad,
            condition_on_previous_text=False,
            word_timestamps=True,
        )

        lines = [
            f"# source: {args.source}",
            f"# model: {args.model} | language: {info.language} ({info.language_probability:.2f}) "
            f"| duration: {fmt_time(info.duration)}",
            "",
        ]
        for seg in segments:  # generator: transcription happens while iterating
            text = seg.text.strip()
            line = text if args.no_timestamps else f"[{fmt_time(seg.start)} -> {fmt_time(seg.end)}] {text}"
            lines.append(line)
            print(line, flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Saved: {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
