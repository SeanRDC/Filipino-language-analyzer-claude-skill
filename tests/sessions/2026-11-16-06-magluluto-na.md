# Session 2026-11-16-06: "Ngayon tayo ay magluluto na" kid cooking meme

## Source
- `ScreenRecording_11-14-2026 13-40-31_1.mp4`, a TikTok screen recording (21 s). A boy in an apron cooks at a home stove and narrates like a cooking show. The search bar suggestion reads *"magluluto na original video"*, and the re-uploader's overlay reads *"mga taong mahilig sa yosi"* (framing, not speech).
- Recipe: 2× `tl` (identical) + `en` gloss + frames.

## Raw ASR (`tl`)
```
[00:00 -> 00:02] ngayon tayo ay magliluto na
[00:04 -> 00:07] so mo papay dito kaya naman tika sa kawale
[00:09 -> 00:13] pag naingit na ang kawale ilagay na natin ang mixture
[00:18 -> 00:20] ngayon tayo ay
```
`en` gloss: *"Now, let's cook… / So, we can add oil to the kawale. / When the kawale is hot, we'll add the mixture. / Now, let's…"*

## Cleaned Transcript
| Time | Cleaned (best guess) | Confidence |
|---|---|---|
| 00:00 | Ngayon tayo ay magluluto na. | high (the search suggestion confirms *magluluto*) |
| 00:04 | Susunod, ilalagay dito 'yung mantika sa kawali. | low-medium (*mantika* and *sa kawali* are solid; the opening words are not) |
| 00:09 | Pag mainit na ang kawali, ilagay na natin ang mixture. | high |
| 00:18 | Ngayon tayo ay… | high (cut off) |

## Skill Fixes Made (self-found)
- Vowel swaps i↔e / u↔o (*kawale*, *magliluto*) and *naingit* → *mainit* (`asr-hallucinations.md`).
- Register policy: transcripts stay verbatim; performative formality (*"tayo ay magluluto"*) is kept in dubbing (SKILL.md).
- Platform search suggestions and hashtags count as evidence; re-uploader overlay titles are not dialogue (SKILL.md Step 0).

## Review
- Reviewer verdict: accurate except 00:04
- [x] 00:04: actually **"So pagpapainit na tayo ng mantika sa kawali."** The skill wrote *"Susunod, ilalagay dito 'yung mantika…"*. It dropped the correct *So*, took the verb *ilalagay* from the English gloss (*"add oil"*) instead of the syllables (*papay* = *pa-pa-init*), and ignored that the next line (*"Pag mainit na…"*) implies a heating step.
- [x] Other lines confirmed.

## Fixes From Review
- `asr-hallucinations.md`: 2 verified rows; reduplication extended to *pa-* causatives; new pattern for particles and nouns fused across a word boundary (*ng mantika* → *naman tika*).
- SKILL.md Step 1 reconstruction: procedural order, take words from the syllables and not the gloss, keep English discourse markers.
