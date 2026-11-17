# Session 2026-11-16-04: Detainee interview, "Paano mo nasabing mabilisan?"

## Source
- Media: `ScreenRecording_11-13-2026 12-43-18_1.mp4` (screen recording of a YouTube "Best Legendary Pinoy Memes (Compilation)" video, 34 s)
- Scene (from video frames): a bald young man in a white shirt stands in front of a police height chart, with a police officer beside him. Someone off camera interviews him. The audio is noisy and the speech is fast.
- Transcriber: `transcribe.py`, model `small`, language `tl`.

## Raw ASR

### Run 1 (old defaults: Whisper's no-speech skip on)
```
[00:30 -> 00:31] So berantagal, paano mo na sabi yung mabilisan?
[00:31 -> 00:32] Oka oka eh, great ka ba?
```
**Only 2 lines out of about 32 s of speech.** `--language auto` gave the same result.

### Diagnosis
- `silencedetect`: sound runs from 00:01 to 00:33, so this is not a silence gap.
- `--language en` gave 9 lines. They are an English **translation** (e.g., *"You don't have to pay for it, I'm just a friend."*), which proves there was speech in the first window.
- Segment stats: the first 30 s window had `no_speech_prob = 0.72`. That is above Whisper's 0.6 cutoff, so the whole window was dropped.
- **Fix:** `transcribe.py` now turns the no-speech skip off by default (`--skip-quiet` restores it). Re-running sessions 01–03 gave identical output, and session 02's 10 s silent tail produced no made-up lines.

### Run 2 (new default)
```
[00:02 -> 00:03] Hidang in solitary zone
[00:03 -> 00:04] uli round or drug darauf?
[00:04 -> 00:05] Kaya wala zama
[00:05 -> 00:07] Pwala ka na yung contributes
[00:07 -> 00:09] Disa yun nag-sinag-sigurado
[00:11 -> 00:13] Kuya anong style ba yung
[00:13 -> 00:14] Buhigh
[00:14 -> 00:17] Gusto ko ibig PUS
[00:17 -> 00:21] hindi selfish mat hamimah reiterate
[00:21 -> 00:22] Walang bayat ba yan yung kaibigan ko yan?
[00:23 -> 00:25] Kaibigan mo. So mabilisan kupit yan.
[00:26 -> 00:27] Paano mo na sabi mabilisan?
[00:27 -> 00:28] Kasi yun no, di ba?
[00:29 -> 00:31] Nakatulog na nga ako sa sobrang tagal, paano mo na sabi mabilisan?
[00:31 -> 00:32] Okay, okay, great ka ba?
```

### Run 3 (diagnostic: same settings, separate sampling)
```
[00:02-00:03] So, sir, sir, sir, sir. / Sir, sir, sir, sir, sir, sir.
[00:03-00:04] Kaya nag-drog ako, kaya?
[00:05-00:05] Paano nga sabi?
[00:06-00:07] Lelan, paano kong kaya nag-drog ako?
[00:07-00:09] Interactes na nga ako para masigurado nyo.
[00:09-00:10] Kaya. / Lelan, terskawa.
[00:11-00:16] Kaya, kaya anong style ba yung buhuk na gusto mo sa aang nag-gusto?
[00:16-00:18] Gusto ko, Kalko, kaso na hindi marunong yung nag-ugupit.
[00:18-00:20] Hindi marunong? Makalabilayad mo.
[00:21-00:22] Walaan ba yung kaya vika ko yun?
[00:22-00:23] Kaya vika mo.
[00:24-00:25] So, mabilisan, kupit yan.
[00:26-00:27] Paano mo na sabi mabilisan?
[00:27-00:28] Kasi, eh, no, di pa.
[00:29-00:30] Nagkatulog nang ako sa sobrang tagal.
[00:30-00:31] Paano mo na sabi ang mabilisan?
[00:31-00:32] Oka, oka eh. / Ganit ka ba?
```
Runs 2 and 3 differ heavily in 00:02–00:20. This is the sign of a random-sampling fallback, and only words that recur across runs are trusted. The German *darauf* in run 2 is a clear hallucination marker.

## Skill Output

### Cleaned Transcript (merged from runs 2–3, the English gloss and run 1)
| Time | Cleaned (best guess) | Confidence |
|---|---|---|
| 00:02–00:05 | ? [unclear, mentions drugs: *droga* / *nag-drugs*] | low |
| 00:05–00:09 | ? … *para masigurado n'yo* ("so you'll be sure"); possibly *nag-drug test na nga ako* | low |
| 00:11 | **Interviewer:** Kuya, anong style ba 'yung buhok na gusto mo? | medium-high |
| 00:14 | **Man:** Gusto ko kalbo, kaso hindi marunong 'yung naggupit. | medium (*kalbo* uncertain) |
| 00:18 | **Interviewer:** Hindi marunong? Magkano binayad mo? | low-medium |
| 00:21 | **Man:** Walang bayad 'yan, 'yung kaibigan ko 'yan. | medium-high (the English gloss agrees) |
| 00:23 | **Interviewer:** Kaibigan mo? So mabilisan, gupit 'yan? | medium-high |
| 00:26 | **Man:** Paano mo nasabing mabilisan? | high |
| 00:27 | **Man:** Kasi, ano, 'di ba… | low |
| 00:29 | **Man:** Nakatulog na nga ako sa sobrang tagal. Paano mo nasabing mabilisan? | high (all runs) |
| 00:31 | **Interviewer:** Okay, okay. Galit ka ba? | medium (*great* / *gared* / *ganit* → *galit*) |

### Corrections Made
- *kaya vika ko* → *kaibigan ko*: rebuilt with the English gloss (*"I'm just a friend"*).
- *bayat* / *Walaan ba* → *walang bayad*: the gloss (*"You don't have to pay for it"*) agrees.
- *kupit* → *gupit*: g→k devoicing, the same pattern as *suntalo* → *sundalo* in session 01.
- *great* / *gared* / *ganit* → *galit*: *l* was misheard, and English mode bent the word into *great*.
- *na sabi* → *nasabing*: the past-tense *na-* got separated, and the linker *-ng* was dropped.
- *buhuk* / *Buhigh* → *buhok*.

### Intent / Analysis
This is comic Q&A at a police station. The interviewer asks the man what hairstyle he wanted. He says (possibly) bald, but the barber didn't know how to cut. The barber was a friend, so it was free. When the interviewer assumes it was a quick cut (*mabilisan*), the man pushes back: "How could you say it was quick? I fell asleep, it took so long!" The interviewer backs off: "Okay, okay. Are you angry?" The opening 9 s seem to involve drugs or a drug test, but the audio is too unclear. Register: casual, fast Manila Tagalog.

### Dubbing Output
Not requested.

## Review
- Reviewer verdict: almost perfect from 00:11 on; **00:02–00:09 missed** (the skill gave up and wrote "unclear")
- What was actually said at 00:02–00:10:
  - **Interviewer:** Kuya, nagdodroga ka ba, kuya?
  - **Man:** Paano mo nasabi?
  - **Interviewer:** Tinatanong ko nga, eh. Nagdodroga ka ba?
  - **Man:** Ida-drug test nga ako para masigurado n'yo.
  - **Interviewer 2:** Kuya…?
  - (00:11 on: as cleaned above, confirmed)
- Flags:
  - [x] 00:02–00:09: see above. **There are two interviewers.**
  - [x] 00:11–00:31: confirmed (*Kuya*, *kalbo*, *Magkano binayad mo?*, *kaibigan*, *gupit*, *Galit ka ba?*).

## Why the Skill Missed 00:02–00:09
The evidence was there across runs 2–3, but the skill did not put it together:
| Run fragment | Actually said |
|---|---|
| *Kaya nag-drog ako, kaya?* | *Kuya, nagdodroga ka ba, kuya?* |
| *Paano nga sabi?* | *Paano mo nasabi?* (the man repeats this exact phrase at 00:26 and 00:30) |
| *Lelan, paano kong kaya nag-drog ako?* | *Tinatanong ko nga, eh. Nagdodroga ka ba?* |
| *Interactes na nga ako para masigurado nyo* | *Ida-drug test nga ako para masigurado n'yo* |
| *Lelan, terskawa* / *Kaya* | *Kuya…?* (second interviewer) |

Root causes:
1. The first window was noisy (no-speech score 0.72), so Whisper fell back to random sampling and each run scrambled it differently.
2. The skill treated low confidence as "give up" instead of rebuilding from the fragments that recur across runs.
3. The skill did not use the man's own repeated phrase (*Paano mo nasabi…*) or the interview pattern (question → dodge → repeated question → answer).
4. Pattern gaps: *kuya* → *kaya*, progressive reduplication collapse (*nagdodroga* → *nag-drog*), and Taglish *ida-drug test* (future reduplication of *i-* + English *drug test*) bent into a fake English word (*Interactes*).

## Fixes
- _pending commit_: `transcribe.py` turns off Whisper's no-speech skip by default (`--skip-quiet` restores it). SKILL.md Step 0 adds the guidance on the skip, on re-running garbled windows and on the English gloss.
- _pending commit_: `asr-hallucinations.md` gets 10 verified rows from session 04, the reduplication rule extended to the progressive, and the address-term (*kuya* → *kaya*) pattern. SKILL.md Step 1 gets "Reconstruct Garbled Stretches, Don't Abandon Them" (recurring fragments, the speaker's repeated phrases, the interview turn pattern, always a best-guess sentence).
