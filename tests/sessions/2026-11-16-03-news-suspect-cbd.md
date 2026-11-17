# Session 2026-11-16-03: News clip, suspect interview ("CBD", "I am God")

## Source
- Media: `ScreenRecording_11-13-2026 12-41-54_1.mp4` (screen recording of a TV news segment, 25 s)
- Scene (from video frames): an off-camera reporter interviews a suspect at night, with traffic enforcers behind him. The on-screen headline is about a man causing a scene and being found with drugs in his vehicle. Around 00:23 the clip cuts to an unrelated *Halalan 2016* press clip.
- Ground truth available: the broadcast has **burned-in subtitles for the reporter's questions** (*"Gumamit ka ngayon?"*, *"Ano 'yung CBD?"*). The suspect's lines have no subtitles.
- Transcriber: `transcribe.py`, model `small`, language `tl`, default flags.

## Raw ASR
```
[00:01 -> 00:02] Gumamit ngayon?
[00:04 -> 00:05] Wala naman siya amat eh.
[00:05 -> 00:06] CBDC.
[00:06 -> 00:07] What is CBDC?
[00:07 -> 00:08] Research mo.
[00:09 -> 00:09] Gumagamit?
[00:10 -> 00:12] Hindi ako tumitigil gumamit.
[00:12 -> 00:13] Gumagamit ako araw-araw.
[00:13 -> 00:15] Pag-gising ko hanggang matulog ako.
[00:15 -> 00:17] The law of God sa Bible.
[00:18 -> 00:19] You cannot touch me.
[00:20 -> 00:20] I am God.
[00:21 -> 00:22] I am Jesus Christ.
[00:22 -> 00:23] Suntukan na lang.
```

## Skill Output

### Cleaned Transcript
| Time | Raw | Cleaned (best guess) | Confidence |
|---|---|---|---|
| 00:01 | Gumamit ngayon? | **Reporter:** Gumamit ka ngayon? | high (matches the subtitle) |
| 00:04 | Wala naman siya amat eh. | **Suspect:** Wala naman siyang amats, eh. | medium |
| 00:05 | CBDC. | **Suspect:** CBD siya, eh. | reviewer-corrected (skill had *CBD.* only) |
| 00:06 | What is CBDC? | **Reporter:** Ano 'yung CBD? | high (matches the subtitle) |
| 00:07 | Research mo. | **Suspect:** Research mo. | high |
| 00:09 | Gumagamit? | **Reporter:** Gumagamit ka? | medium (*ka* may have been dropped, as at 00:01) |
| 00:10 | Hindi ako tumitigil gumamit. | **Suspect:** Hindi ako tumitigil gumamit. | high |
| 00:12 | Gumagamit ako araw-araw. | **Suspect:** Gumagamit ako araw-araw. | high |
| 00:13 | Pag-gising ko hanggang matulog ako. | **Suspect:** Paggising ko hanggang matulog ako. | high |
| 00:15 | The law of God sa Bible. | **Suspect:** The law of God sa Bible… | medium (may be part of a longer line) |
| 00:18 | You cannot touch me. | **Suspect:** You cannot touch me. | high |
| 00:20 | I am God. | **Suspect:** I am God. | high |
| 00:21 | I am Jesus Christ. | **Suspect:** I am Jesus Christ. | high |
| 00:22 | Suntukan na lang. | ? **(cut to the 2016 clip)** Suntukan na lang. | medium (unclear whether the suspect says it or the clip it cuts to) |

### Corrections Made
- **Whisper translated instead of transcribing.** At 00:06 the reporter says *"Ano 'yung CBD?"* (confirmed by the subtitle), but Whisper output English, *"What is CBDC?"*. Even in `tl` mode, Whisper can output an English **translation** of a Tagalog line. This is a new pattern.
- *CBDC* → *CBD*: Whisper added a letter and turned *CBD* (cannabidiol) into *CBDC*, a better-known term in its training data (central bank digital currency). The drug context and the subtitle both say *CBD*.
- *Gumamit ngayon* → *Gumamit ka ngayon*: the short pronoun *ka* was dropped between two words.
- *siya amat* → *siyang amats*: *amats* is slang for being high (*tama* with its syllables swapped). The linker *-ng* and the final *-s* were dropped.
- *Pag-gising* → *Paggising*: *pag-* takes a hyphen only before a vowel (*pag-asa*), not before a consonant.

### Intent / Analysis
A suspect is interviewed after an arrest. He says what he uses is CBD and that "it doesn't get you high" (*wala naman siyang amats*). When the reporter asks what CBD is, he answers dismissively, "Research mo" ("Look it up"). He then says he uses it every day, from waking up until he sleeps. His statements escalate into grandiose religious claims in English (*"The law of God… You cannot touch me. I am God. I am Jesus Christ."*). The meme edit then cuts to a 2016 election clip, *"Suntukan na lang"* ("Let's just settle it with a fistfight"), as a punchline. Register: casual Taglish with drug slang (*amats*).

### Dubbing Output
Not requested.

## Review
- Reviewer verdict: mostly accurate (1 line incomplete, now fixed)
- Flags:
  - [x] 00:05: the suspect says **"CBD siya, eh."** Whisper dropped *siya, eh* and changed *CBD* to *CBDC*. The skill fixed the acronym but missed the dropped words.
  - [x] 00:04 *Wala naman siyang amats, eh*: confirmed.
  - [x] 00:09 *Gumagamit ka?*: confirmed.
  - [x] 00:15 *The law of God sa Bible*: confirmed.
  - [x] 00:22 *Suntukan na lang*: confirmed.
  - [x] Nothing else missing.

## Experiment: Taglish `initial_prompt` (ruled out)
Tested on sessions 01–03 to see whether a prompt stops the translation leak at 00:06.
- A prompt with sample Taglish phrases fixed 00:06 (*Ano yung CBDC*), but its own words leaked into other lines (*yung*, *Ano*, *Aho*). It also invalidated session 01, since the prompt contained *kaya pala*.
- A neutral prompt (*"Transcript ng usapan sa Tagalog at Taglish…"*) **dropped the whole CBD exchange** (00:05–00:07) and garbled session 01 lines.
- Decision: keep the defaults (no prompt) and fix leaks in the skill's Step 1 instead.

## Fixes
- _pending commit_: `asr-hallucinations.md` gets verified rows from sessions 02–03, plus the translation-leak, acronym-drift and dropped-short-words patterns. `slang-glossary.md` gets *amats*. SKILL.md Step 0 gets on-screen text as ground truth, no `initial_prompt`, and the gap check; Step 1 gets the translation-leak bullet.
