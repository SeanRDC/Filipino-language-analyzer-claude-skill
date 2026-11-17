# Session 2026-11-17-01: "Tatlong basong kutsara" kid cooking duet

## Source
- `ScreenRecording_11-14-2026 13-47-18_1.mp4`, a TikTok duet screen recording (11 s). A boy in a kitchen holds a plastic cup over a pot. Description: *"Tatlong basong kutsara pa nga 😂"*; search: *"tatlong basong kutsara kid now"*.
- Recipe: 2× `tl` (they differ only in *yun*/*yan*) + `en` gloss + frames.

## Raw ASR (`tl`)
```
[00:00 -> 00:02] uto sa ating English plan o yun lang
[00:02 -> 00:07] ngayon lang yun natin ang tatlong basong kutsahar
```
`en` gloss: *"This is for our English plan, that's all. / Now, let's make 3 cups of Kucharar."*

## Cleaned Transcript
| Time | Cleaned (best guess) | Confidence |
|---|---|---|
| 00:00 | …to sa ating ___, 'yun lang. (*English plan* is unresolved; it may be an ingredient or dish name) | low |
| 00:02 | Ngayon, ilagay na natin ang tatlong basong kutsara. | medium-high (*tatlong basong kutsara* is confirmed by the description and search) |

Analysis: another kid cooking-show imitation. The joke is the measurement mix-up *"tatlong basong kutsara"* ("three glasses of spoon"), kept verbatim.

## Skill Fixes Made (self-found)
- Gotcha: never "correct" the speaker's own mistake; the odd phrase is often the joke (SKILL.md).
- Clip edges: leading and trailing fragments are edit cuts (`asr-hallucinations.md`).

## Review
- Reviewer verdict: both lines needed correction
- [x] 00:00: **"…to sa ating leche flan, 'yun lang."** *English plan* = *leche flan*, a Filipino dish name bent into English.
- [x] 00:02: **"Ngayon, lagyan natin ng tatlong basong kutsara."** The skill wrote *ilagay na natin ang*. The raw *lang yan* was closer to *lagyan*, and the marker *ng* follows *lagyan*.

## Fixes From Review
- `asr-hallucinations.md`: 2 verified rows, a Filipino dish-name list, and the focus-agreement rule (the verb decides *ng*/*ang*).
- SKILL.md restructured: a hard-audio routine in Step 0b and an ordered 8-step reconstruction in Step 1. The description now triggers on noisy audio/video.
