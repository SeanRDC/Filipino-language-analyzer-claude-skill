# Filipino ASR Analyzer — Claude Skill

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that cleans, interprets, and localizes noisy Tagalog/Filipino speech transcripts. It's built for dubbing and natural-sounding playback.

> **Status:** 🚧 Early development. SKILL.md, references and examples are drafted; the skill has not been evaluated yet.

## What It Does

English-biased speech recognition (ASR) tends to mangle Tagalog and Taglish. This skill teaches Claude to:

1. **Reconstruct transcripts.** Undo phonetic hallucinations ("add toe" → *dito*), reattach Taglish affixes (*nag-drive*, *i-send*), and recover stress or glottal-stop distinctions from context (*bása* vs. *basâ*).
2. **Analyze meaning.** Pull out the speaker's intent and map slang such as *charot*, *lodi* and *omsim*.
3. **Localize for dubbing.** Write conversational Manila Taglish whose cadence and syllable count fit the source audio timing.

## Structure

```
.
├── README.md
├── LICENSE
└── filipino-asr-analyzer/
    ├── SKILL.md                      # Skill entry point (frontmatter + instructions)
    ├── references/
    │   ├── asr-hallucinations.md     # English-ASR mishearings of Tagalog
    │   ├── slang-glossary.md         # Modern slang and reversed words
    │   └── register.md               # Deep → modern Tagalog, contractions
    ├── scripts/
    │   ├── transcribe.py             # Video/audio → raw ASR (faster-whisper + yt-dlp)
    │   └── requirements.txt
    └── examples/
        └── sample-01.md              # Before/after analyses
tests/
└── sessions/                         # Logged test runs: raw ASR, output, review, fixes
```

## Transcribing Media

The skill can start from audio or video, not only text:

```bash
pip install -r filipino-asr-analyzer/scripts/requirements.txt   # also needs ffmpeg on PATH
python filipino-asr-analyzer/scripts/transcribe.py "https://youtu.be/..." --out transcript.txt
python filipino-asr-analyzer/scripts/transcribe.py clip.mp4 --model medium
```

Whisper does the listening, and the skill is the second pass that fixes its Tagalog mistakes.

## Register

The skill leans on **modern conversational Tagalog** (Manila-style Taglish). It still recognizes **deep Tagalog** (*malalim na Tagalog*) and converts it to modern equivalents, unless you ask it to keep the formal register.

## Installation

**Claude Code:** copy the skill folder into your personal skills directory:

```bash
cp -r filipino-asr-analyzer ~/.claude/skills/
```

**Claude.ai:** zip the `filipino-asr-analyzer/` folder and upload it under **Settings → Capabilities → Skills**.

## Usage

Paste a raw transcript or ask for a dubbing line. Claude loads the skill automatically when the request matches:

```
Clean up this ASR transcript: "pa ray add toe con a nah ba? goose toe co sana mag drive tie yo mamaya"
```

```
Translate this into natural Taglish for dubbing: "Dude, are you here yet?"
```

See [`examples/sample-01.md`](filipino-asr-analyzer/examples/sample-01.md) for expected output.

## Roadmap

- [x] Project initialization
- [x] Draft `SKILL.md`
- [x] Reference files (ASR hallucination patterns, slang glossary, register and contractions)
- [x] Example transcripts with expected output
- [ ] Testing and evaluation
- [ ] First release

## Authors

- **Sean** ([@SeanRDC](https://github.com/SeanRDC)): project lead
- **Claude** (Anthropic): co-author

## License

[MIT](LICENSE)
