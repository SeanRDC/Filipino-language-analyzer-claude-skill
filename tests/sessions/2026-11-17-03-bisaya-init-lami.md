# Session 2026-11-17-03: Bisaya eating meme ("Init!! … Lami kaayo!")

## Source
- `ScreenRecording_11-14-2026 13-50-41_1.mp4`, a TikTok screen recording (24 s). A shirtless young man eats hot soup and rice and talks to the camera. Captions burned in; hashtags *#urbanlegend #philippines #bisaya#memes*; search: *"lami kayo ok kayo now"*.
- **Language: Cebuano (Bisaya), not Tagalog.** This is the first non-Tagalog clip.
- Routine: 2× `tl` (identical) + `en` pass + frames and captions at 1 fps.

## Raw ASR
`tl`:
```
[00:01 -> 00:02] Ah, init.
[00:08 -> 00:10] Natokan ko.
[00:11 -> 00:12] Lamme kayo.
[00:13 -> 00:15] Ok kayo.
[00:18 -> 00:19] Nangahain ako ko, Ban.
[00:20 -> 00:22] Kay, break din kayo.
```
`en` (hallucinated a stock outro and nothing else):
```
[00:00 -> 00:19] This is the end of the video, thank you so much for watching, see you in the next video.
```

## Cleaned Transcript (Cebuano, with English)
| Time | Cleaned | English | Confidence |
|---|---|---|---|
| 00:02 | Init!! | Hot!! | high (caption) |
| 00:06 | [sound: cough] (caption: *korean cough*) | | high |
| 00:09 | Natuk-an ko! | I choked! | high (caption) |
| 00:12 | Lami kaayo! | So delicious! | high (caption *Lami Ka'yo*, search) |
| 00:13 | OK kaayo! | Really OK! | high |
| 00:15 | [sound: giggle] (caption: *korean giggle*) | | high |
| 00:18 | Nangahoy na akong kauban! | My companion went to gather firewood! | high (caption) |
| 00:21 | (Kay) birthday niya karon! | (Because) it's his birthday today! | high (caption); *Kay* from audio only, medium |

Analysis: deadpan mukbang-style meme in Cebuano. He burns his mouth, chokes, then declares the food delicious, and the non-sequitur about his companion gathering firewood for a birthday lands as the joke.

## Skill Fixes Made (self-found)
- New `references/bisaya-cebuano.md`: how to spot Cebuano, common words, false friends (*kaayo/kayo*, *kay*, *libog*, *langgam*), verified rows.
- SKILL.md Step 0b.0 "Identify the language first"; sound-description captions become `[sound: …]`; English-pass stock-outro hallucinations are discarded; Step 3 asks which language to dub into; description triggers on Bisaya.

## Review
- Reviewer verdict: _pending_
- [ ] Is the Cebuano right (*natuk-an*, *nangahoy na akong kauban*, *kay birthday niya karon*)?
- [ ] Does he say *Kay* at 00:20?
