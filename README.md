# Filipino ASR Analyzer — Claude Skill

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that cleans, interprets, and localizes noisy Tagalog/Filipino speech transcripts. It's built for dubbing and natural-sounding playback.

> **Status:** 🚧 Early initialization. The first draft of `SKILL.md` exists, but it hasn't been tested yet.

## What It Does

English-biased speech recognition (ASR) tends to mangle Tagalog and Taglish. This skill teaches Claude to:

1. **Reconstruct transcripts.** Undo phonetic hallucinations ("add toe" → *dito*), reattach Taglish affixes (*nag-drive*, *i-send*), and recover stress or glottal-stop distinctions from context (*bása* vs. *basâ*).
2. **Analyze meaning.** Pull out the speaker's intent and map slang such as *charot*, *lodi* and *omsim*.
3. **Localize for dubbing.** Write conversational Manila Taglish whose cadence and syllable count fit the source audio timing.

## Structure

```
.
├── README.md
└── filipino-asr-analyzer/
    └── SKILL.md          # Skill entry point (frontmatter + instructions)
```

## Installation

_Coming soon._

## Usage

_Coming soon._

## Roadmap

- [x] Project initialization
- [x] Draft `SKILL.md`
- [ ] Reference files (ASR hallucination patterns, slang glossary, contractions)
- [ ] Example transcripts with expected output
- [ ] Testing and evaluation
- [ ] First release

## Authors

- **Sean** ([@SeanRDC](https://github.com/SeanRDC)): project lead
- **Claude** (Anthropic): co-author

## License

_To be decided._
