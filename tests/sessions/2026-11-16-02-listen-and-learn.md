# Session 2026-11-16-02: "Listen, look and listen and learn" interview

## Source
- Media: `ScreenRecording_11-13-2026 11-11-09_1.mp4` (screen recording of a YouTube meme clip from a *Raffy Tulfo in Action* segment, 49 s)
- Scene (from video frames): the host interviews a young man indoors at night. The man covers his face, then speaks to the camera. On-screen title: *"Listen and look and listen and learn"*.
- Transcriber: `transcribe.py`, model `small`, language `tl`, default flags (VAD off).

## Raw ASR
```
[00:01 -> 00:19] Say something to the viewers at Samakababayan natin because the last time that she was here, so many netizens were bashing you, they were condemning you, what you've done to her. They believed her statement. Now would you like to say something? Make a message to our viewers.
[00:19 -> 00:23] Mga kababayan ko. Hindi po ako narito.
[00:23 -> 00:25] You can say in English kasi par may tindihan din ni ano.
[00:25 -> 00:29] All my fellow Filipinos.
[00:29 -> 00:33] Now this is my side. Listen, look and listen and learn.
```
Nothing was transcribed after 00:33, although the clip runs to 00:49. Follow-up checks:
- Audio levels (`silencedetect`): there is sound until about 00:39.5, then about 10 s of silence (the paused player in the screen recording).
- Re-transcribing 00:33–00:40 alone (`tl` and `auto`) returns only the tail "…and learn.", so the remaining sound is probably non-speech (laughter or reaction).
- A `medium` model run failed because the Hugging Face download kept dropping. Retry it later on a stable connection.

## Skill Output

### Cleaned Transcript
| Time | Raw | Cleaned (best guess) | Confidence |
|---|---|---|---|
| 00:01 | Say something to the viewers at Samakababayan natin because … Make a message to our viewers. | **Host:** Say something to the viewers *at sa mga kababayan natin*, because the last time that she was here, so many netizens were bashing you, they were condemning you, what you've done to her. They believed her statement. Now, would you like to say something? Make a message to our viewers. | high (English); medium (*at sa mga kababayan natin*) |
| 00:19 | Mga kababayan ko. Hindi po ako narito. | **Man:** Mga kababayan ko, hindi po ako narito… | medium (may be cut off: *narito para…*?) |
| 00:23 | You can say in English kasi par may tindihan din ni ano. | **Host:** You can say it in English, *kasi para maintindihan din ni ano*. | medium–high |
| 00:25 | All my fellow Filipinos. | **Man:** All my fellow Filipinos… | high |
| 00:29 | Now this is my side. Listen, look and listen and learn. | **Man:** Now this is my side. Listen, look… and listen and learn. | high (the on-screen title says *"Listen and look…"*) |
| 00:33–00:49 | (nothing) | ? possibly laughter or crowd reaction | unknown |

### Corrections Made
- *at Samakababayan natin* → *at sa mga kababayan natin*: *sa mga* fused with the noun. This is the "fused particles" pattern.
- *par may tindihan* → *para maintindihan*: the infix verb *ma-intindihan* was split, and *para* lost its last vowel into the split. This is a split-affix error on a Tagalog root, not on an English one.
- *ni ano*: kept as is. *Ano* here is a placeholder ("what's-his/her-name"), not "what". It refers to the woman who complained earlier.
- *say in English* → *say it in English*: added the missing object for readability. This is a light edit; the speaker may really have said it without *it*.

### Intent / Analysis
This is a Taglish public-service interview. The host speaks mostly English and asks the man to answer the netizens who bashed him after the woman's earlier statement. The man starts formally in Tagalog (*Mga kababayan ko, hindi po ako narito…*). The host cuts in and tells him to use English so the woman (*ni ano*) also understands. The man switches to a stiff, formal English (*All my fellow Filipinos… Now this is my side. Listen, look and listen and learn.*). The meme is the contrast: an earnest, broken-formal English speech in a tense moment. The host's *ano* means the woman probably doesn't understand Tagalog well, but this is **not confirmed**.

### Dubbing Output
Not requested.

## Review
- Reviewer verdict: accurate. The reviewer confirmed the full cleaned transcript as correct.
- Flags:
  - [x] Line 00:01: is it *at sa mga kababayan natin*?
  - [x] Line 00:19: is it *Hindi po ako narito…*, and is anything cut off after it?
  - [x] Line 00:23: is it *kasi para maintindihan din ni ano*?
  - [x] Line 00:29: is it *Listen, look and listen and learn* or *Listen and look and listen and learn*?
  - [x] 00:33–00:49: is there speech that Whisper missed?

## Fixes
- None needed. All flags were confirmed as transcribed.
