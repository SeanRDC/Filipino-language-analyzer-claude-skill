# Session 2026-11-16-01: Pinoy meme clip, "sundalo" interview

## Source
- Media: `ScreenRecording_11-13-2026 12-40-51_1.mp4` (screen recording of a YouTube "Best Legendary Pinoy Memes (Compilation)" video, 18 s)
- Scene (from video frames): two hosts with microphones interviewing a schoolboy outdoors; crowd noise.
- Transcriber: `transcribe.py`, model `small`, language `tl`, CPU int8. Runtime 6m15s, almost all of it the first-time model download.

## Raw ASR
```
[00:00 -> 00:02] Wala kusun mo maging paglaki mo!
[00:02 -> 00:03] Suntalo!
[00:03 -> 00:04] Ay!
[00:04 -> 00:05] Suntalo!
[00:05 -> 00:06] Suntalo!
[00:06 -> 00:07] Sa kalawang!
[00:07 -> 00:13] Wala kusun mo maging suntalo!
[00:13 -> 00:14] Wala kusun mo maging suntalo!
[00:14 -> 00:16] Bulihin ko ang mga baklap!
```

## Skill Output

### Cleaned Transcript
| Time | Raw | Cleaned (best guess) | Confidence |
|---|---|---|---|
| 00:00 | Wala kusun mo maging paglaki mo! | **Host:** Ano'ng gusto mong maging paglaki mo? | medium (*gusto mong maging paglaki mo*: high; *Ano'ng*: medium) |
| 00:02 | Suntalo! | **Boy:** Sundalo! | high |
| 00:03 | Ay! | **Host:** Ay! | high |
| 00:04–00:05 | Suntalo! ×2 | Sundalo! Sundalo! | high |
| 00:06 | Sa kalawang! | ? *Sa kalaban!* / *Sa'n ka lalaban?* | low |
| 00:07–00:14 | Wala kusun mo maging suntalo! ×2 | **Host:** (Bakit) gusto mong maging sundalo? | medium |
| 00:14 | Bulihin ko ang mga baklap! | **Boy:** Babarilin ko ang mga bakla! | low–medium |

### Corrections Made
- *suntalo* → *sundalo*: **d→t devoicing**, a typical Whisper error on child speech.
- *kusun mo* → *gusto mong*: **g→k devoicing**, plus the dropped linker *-ng*.
- *Wala* → *Ano'ng*: the opening question word was misheard. The sentence shape *__ gusto mong maging paglaki mo?* is the classic "what do you want to be when you grow up" question.
- *Bulihin* → *Babarilin*: *b-r-l-n* consonant skeleton; "shoot" fits the soldier theme.
- *baklap* → *bakla*: trailing consonant hallucinated. The hosts appear to be gay/drag comedians, which fits a meme punchline. **Not confirmed.**

### Intent / Analysis
A comedic interview. The hosts ask a boy what he wants to be when he grows up. He answers "a soldier" (*sundalo*). His follow-up line, possibly "I'll shoot the *bakla*", said to gay hosts, is likely the meme punchline. The register is casual Manila Tagalog with no slang.

### Dubbing Output
Not requested.

## Run 2 (after d95e9dd: VAD off, no previous-text conditioning)

Same file, model `small`, language `tl`, default flags.

### Raw ASR
```
[00:00 -> 00:01] Ang gusto mo maging paglary mo?
[00:02 -> 00:03] Suntalo!
[00:03 -> 00:03] Ay!
[00:03 -> 00:04] Ayos ay ala!
[00:04 -> 00:05] Sarate!
[00:05 -> 00:05] Shoot!
[00:07 -> 00:08] Anang sa kalawang!
[00:08 -> 00:09] Ayo!
[00:11 -> 00:12] Yanang ganda!
[00:12 -> 00:14] Bakit gusto mo maging suntalo?
[00:14 -> 00:15] Bulihin ko ang mga bakla!
```
The repetition loop is gone. 11 cues instead of 9, and no duplicated lines.

### Cleaned Transcript
| Time | Raw | Cleaned (best guess) | Confidence |
|---|---|---|---|
| 00:00 | Ang gusto mo maging paglary mo? | **Host:** Ano'ng gusto mong maging paglaki mo? | high (run 1 and run 2 agree) |
| 00:02 | Suntalo! | **Boy:** Sundalo! | high |
| 00:03 | Ay! | **Host:** Ay! | high |
| 00:03 | Ayos ay ala! | ? *Ay, kaya pala!* | low |
| 00:04 | Sarate! | ? *Salute!* (drill command) | low |
| 00:05 | Shoot! | ? unclear; may be part of the drill or crowd noise | low |
| 00:07 | Anang sa kalawang! | **Host:** Harap sa kaliwa! (drill: "left face") | medium |
| 00:08 | Ayo! | **Host:** Harap! (the execution word of the command) | medium |
| 00:11 | Yanang ganda! | **Host:** Ayan, ang ganda! | medium |
| 00:12 | Bakit gusto mo maging suntalo? | **Host:** Bakit gusto mong maging sundalo? | high |
| 00:14 | Bulihin ko ang mga bakla! | **Boy:** Huhulihin ko ang mga bakla! | confirmed by reviewer (skill guessed *Babarilin*, wrong) |

### Corrections Made
- *paglary* → *paglaki*: the *-ki* syllable was misheard as *-ry*.
- *Anang sa kalawang* / *Ayo* → *Harap sa kaliwa… Harap!*: this is the Filipino military drill command (preparatory word + execution word). It reframes the 00:06 line from run 1 (*Sa kalawang*), which was not *kalaban*.
- *Yanang ganda* → *Ayan, ang ganda*: dropped initial *A-* and merged words.

### Intent / Analysis (revised)
The hosts ask the boy what he wants to be. He says "a soldier", so they make him perform drill commands (salute, left face) and praise him (*Ayan, ang ganda!*). Then they ask why he wants to be a soldier, and his answer is the punchline: "I'll catch the *bakla*!" (*Huhulihin ko ang mga bakla*), said to hosts who appear to be gay comedians. The reviewer confirmed this line.

## Review
- Reviewer verdict: _pending_
- Flags:
  - [ ] Line 00:00, is it *Ano'ng gusto mong maging paglaki mo?*
  - [x] Lines 00:03–00:05 (*Ayos ay ala / Sarate / Shoot*): the host says **"Attention!"**, then **"Ah, kaya pala"**. My guess of *Ay, kaya pala* was close; *Salute* was wrong. The reviewer noted that the audio is barely audible here, which is the kind of input this skill exists to handle.
  - [ ] Lines 00:07–00:08, is it the drill command *Harap sa kaliwa… Harap!*?
  - [ ] Line 00:12, the host question: is it *Bakit gusto mong maging sundalo?*
  - [x] Line 00:14: the boy says **"Huhulihin ko ang mga bakla!"** ("I'll catch/arrest the *bakla*"), not *Babarilin* ("shoot"). The skill guessed from the soldier theme instead of the sound. *-ulihin* was already in the raw output, and the future-tense reduplication *hu-* had collapsed into *B-*.

## Fixes
- d95e9dd: transcriber stops the repetition loop and keeps short cues.
- _next commit_: added verified mishearings (*Ayos ay ala* → *Ah, kaya pala*; *Sarate/Shoot* → *Attention*) and the shouted-command guidance to `asr-hallucinations.md` and SKILL.md Step 1.
- _next commit_: added *Bulihin* → *Huhulihin*, the collapsed-reduplication pattern, and the "closest sound match, not theme" rule (`asr-hallucinations.md` and SKILL.md Gotchas).
