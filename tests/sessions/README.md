# Test Sessions

A log of every test run of the skill against real Tagalog/Taglish media. Each session records what went in, what the skill produced, what the human reviewer flagged, and which commits fixed it.

Raw media (video/audio) stays local in `test files/`, which is git-ignored. Only the text record is committed.

## File Naming

`YYYY-MM-DD-NN-short-slug.md`, e.g. `2026-11-16-01-vlog-intro.md`

## Template

```markdown
# Session YYYY-MM-DD-NN: <short title>

## Source
- Media: <filename or link> (<type: vlog / teleserye / news / old film / …>, <duration>)
- Transcriber: transcribe.py, model <small>, language <tl>

## Raw ASR
<untouched transcript output>

## Skill Output
### Cleaned Transcript
### Corrections Made
### Intent / Analysis
### Dubbing Output (if requested)

## Review
- Reviewer verdict: <accurate / partly accurate / inaccurate>
- Flags:
  - [ ] <what was wrong → what it should be>

## Fixes
- <commit hash>: <what changed in SKILL.md / references>
```
