# Session 2026-11-16-07: "Di nga nagnanapkin" livestream meme

## Source
- `ScreenRecording_11-14-2026 13-41-21_1.mp4`, a TikTok screen recording of an old livestream clip (32 s). The streamer answers viewer comments. Description: *"di nga nagnanapkin #nostalgic #pinoymemes"*; search suggestion: *"tomboy napkins"*.
- Recipe: 2× `tl` (identical) + `en` gloss + frames.

## Raw ASR (`tl`)
```
[00:00 -> 00:02] Ano? Ang kulit nyo talaga, ano?
[00:04 -> 00:06] Sabi nandikon nagnanapten eh!
[00:11 -> 00:14] Nga ako kasi kong gumagamit ng napten 100%
[00:16 -> 00:18] Simula batap ako
[00:18 -> 00:19] Anggang lumake
[00:20 -> 00:22] Hindi na ako gumagamit na on
[00:23 -> 00:24] Kasi hindi naman ko
[00:25 -> 00:27] Bonbon na dinadat na ne
[00:30 -> 00:32] Ang kulit nyo talaga
```
`en` gloss: *"I told you I didn't use napkin / I don't use napkin 100% / I'm still a kid until I grow up / I'm not using it anymore / because I don't / use it every month"*

## Cleaned Transcript
| Time | Cleaned (best guess) | Confidence |
|---|---|---|
| 00:00 | Ano? Ang kulit n'yo talaga, ano? | high |
| 00:04 | Sabi nang 'di ako nagnanapkin, eh! | medium (alt: *Sabi nga, 'di ako…*) |
| 00:11 | 'Di nga ako… kasi 'di ako gumagamit ng napkin, 100%. | low-medium |
| 00:16 | Simula bata pa ako | high |
| 00:18 | hanggang lumaki… | high |
| 00:20 | Hindi na ako gumagamit n'on. | high |
| 00:23 | Kasi hindi naman ako… | medium |
| 00:25 | …buwan-buwan dinadatnan, eh. → reviewer: **…buwan-buwan na dinadatnan, eh.** | medium |
| 00:30 | Ang kulit n'yo talaga. | high |

Analysis: the streamer is answering persistent commenters (*ang kulit n'yo*). The humor is the insistence, delivered deadpan, that they have never used napkins "since I was a kid until I grew up", because they "don't get a period every month". Casual Tagalog, with the euphemism *dinadatnan*.

## Skill Fixes Made (self-found)
- English nouns made into Tagalog verbs (*nagnanapten* → *nagnanapkin*) and stop-consonant swaps (`asr-hallucinations.md`).
- Livestreams: read the on-screen comments to resolve *kayo/n'yo*, and never transcribe them (SKILL.md Step 0).
- Euphemisms section: *datnan*, *may dalaw*, *regla*/*mens* (`slang-glossary.md`).

## Review
- Reviewer verdict: accurate except one dropped word
- [x] 00:25: actually **"…buwan-buwan na dinadatnan, eh."** Whisper had the *na* (*Bonbon na dinadat*); the skill deleted it as optional.
- [x] Other lines confirmed.

## Fix From Review
- SKILL.md Step 1 reconstruction, sub-step 7: never delete a small word Whisper actually heard (*na, nga, pa, eh, po, lang*).
