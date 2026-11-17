# Session 2026-11-17-02: "Isnik dragon" martial-arts demo meme

## Source
- `ScreenRecording_11-14-2026 13-48-42_1.mp4`, a TikTok screen recording (41 s). A man demonstrates made-up fighting moves outdoors at night while an off-camera narrator introduces each one, documentary style. Description: *"isnik dragon #pinoymeme #meme #urbanlegend"*.
- Routine: 2× `tl` (identical) + `en` gloss + frames.

## Raw ASR (`tl`)
```
[00:00 -> 00:11] Ito ang tinatawag na snake dragon, kung saan ang isang paanya ay isalang ang nakatukod at nakagagad ang kanyang mga...
[00:12 -> 00:14] atto naman ang window of eagle.
[00:15 -> 00:15] Eagle yan?
[00:16 -> 00:17] Yan eagle, yan.
[00:18 -> 00:20] Yan, tinuturusahati ni Kapitan B.
[00:21 -> 00:22] Atto ng hammer punch.
[00:24 -> 00:25] Karate black.
[00:26 -> 00:27] Black karate kaya?
[00:30 -> 00:31] kumpuhasil
[00:32 -> 00:32] kumpuhasil
[00:33 -> 00:35] iron punch
[00:36 -> 00:38] ilan pa lang yan sa mga dapat ipakitat
[00:38 -> 00:39] dapat niyong abangan
[00:40 -> 00:40] kay kapitan
```
`en` gloss highlights: *"wind of eagle"*, *"That's what Captain B taught us"*, *"This is a hammer punch"*.

## Cleaned Transcript
| Time | Cleaned (best guess) | Confidence |
|---|---|---|
| 00:00 | **Narrator:** Ito ang tinatawag na *snake dragon* (said *isnik dragon*), kung saan ang isang paa niya ay isa lang ang nakatukod, at nakaangat ang kanyang mga… | medium (*isa lang ang*, *nakaangat* uncertain) |
| 00:12 | **Narrator:** Heto naman ang *wing of eagle*. → reviewer: ***wind of eagle*** | wrong |
| 00:15 | **?:** Eagle 'yan? | high |
| 00:16 | **Narrator:** Ayan, eagle 'yan. | medium-high |
| 00:18 | **Narrator:** 'Yan, itinuro sa atin ni Kapitan B. | medium (gloss agrees; *B* may be a cut name) |
| 00:21 | **Narrator:** Heto 'yung *hammer punch*. | medium-high |
| 00:24 | **?:** Karate black. | medium |
| 00:26 | **?:** Black karate, kaya? | low-medium |
| 00:30 | **Narrator:** *Kung Fu Hustle.* *Kung Fu Hustle.* | medium-high (said *kumpuhasil*) |
| 00:33 | **Narrator:** *Iron punch.* | high |
| 00:36 | **Narrator:** Ilan pa lang 'yan sa mga dapat ipakita at dapat n'yong abangan kay Kapitan… | high |

Analysis: a parody of a martial-arts showcase. A narrator in mock-documentary formal Tagalog (*"Ito ang tinatawag na… kung saan…"*, performative formality) introduces absurd move names in accented English (*isnik dragon*, *Kung Fu Hustle*, *iron punch*) while the man strikes poses. The humor is the deadpan presentation.

## Skill Fixes Made (self-found)
- Extra *i-* before s-clusters (*isnik* = snake), nasal assimilation in English names (*kumpuhasil* = Kung Fu Hustle), demonstratives at line starts (*atto* = *heto*), and more boundary-fusion examples (*ipakitat*, *tinuturusahati*) (`asr-hallucinations.md`).

## Review
- Reviewer verdict: accurate except 00:12
- [x] 00:12: **wind of eagle**. The `en` gloss had it right; the skill swapped it for the more logical *wing*.
- [ ] 00:00: the full snake-dragon description (not corrected by the reviewer)
- [ ] 00:18: *itinuro sa atin ni Kapitan B*? Who is Kapitan B?
- [ ] 00:24–00:27: *Karate black / Black karate, kaya?* Who says it?
- [ ] 00:30: *Kung Fu Hustle*?

## Fix From Review
- SKILL.md Step 0b.3: for English-spoken stretches the `en` pass is a real transcription and wins. Gotcha: invented parody names are absurd on purpose. Verified row added.
