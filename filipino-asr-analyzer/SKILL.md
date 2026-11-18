---
name: filipino-asr-analyzer
description: Transcribes, cleans, interprets, and localizes noisy Tagalog/Filipino speech, and recognizes Bisaya/Cebuano. Use when the user gives Tagalog, Taglish or Bisaya audio/video (including noisy, near-inaudible meme, TikTok, livestream, or news clips) or messy ASR text, or asks to analyze conversational Filipino or prepare it for dubbing and fluent playback.
---
# Filipino ASR Analyzer & Dubbing Engine

## Summary
Enhances the agent's fluency in Tagalog by recovering speech from hard audio, correcting phonetic hallucinations from ASR, interpreting Taglish code-switching, and ensuring output cadence is natural enough for voice dubbing.

## When to Use
*   The user provides audio or video with Tagalog/Taglish speech, however noisy.
*   The user provides an ASR transcript containing mangled Tagalog or Taglish.
*   The user needs an English prompt translated into conversational, spoken Filipino for dubbing.
*   The user asks to clean, analyze, or respond to informal Filipino text.

## Register Policy
Lean on **modern conversational Tagalog** (Manila-style Taglish) by default. Deep Tagalog (*malalim na Tagalog*: literary, formal, poetic, or purist) must still be recognized and correctly interpreted when it appears in the input. Convert it to modern equivalents unless the user asks to keep the formal register. See [references/register.md](references/register.md).

*   **Transcripts are always verbatim.** Register conversion applies only to the interpretation and dubbing steps, never to the cleaned transcript.
*   **Keep performative formality.** When a speaker puts on a formal register for effect (a kid imitating a cooking show's *"Ngayon tayo ay magluluto na"*, a mock news anchor, a pageant answer, a teacher voice), the formality *is* the meaning or the joke. Keep it in dubbing, and note it in the analysis.

## References
*   [references/asr-hallucinations.md](references/asr-hallucinations.md): verified Whisper mishearings of Tagalog, plus sound and structure patterns (Step 1).
*   [references/slang-glossary.md](references/slang-glossary.md): modern slang, reversed words and euphemisms (Steps 1–2).
*   [references/register.md](references/register.md): deep → modern equivalents and spoken contractions (Steps 2–3).
*   [references/bisaya-cebuano.md](references/bisaya-cebuano.md): spotting Cebuano, common words, false friends with Tagalog (Step 0b).

## Steps

### 0. Get the Raw Transcript and Gather Evidence (only when given audio/video)

**0a. Transcribe** with the bundled script (run from this skill's directory):

```bash
python scripts/transcribe.py <file-or-url> --out <transcript.txt>
```

*   Defaults: multilingual `small` model, language `tl`, VAD off, and Whisper's "this is silence" filter off. On noisy Tagalog speech, that filter threw away whole 30-second windows of real dialogue. Pass `--skip-quiet` only for long recordings with genuinely silent stretches. Use `--model medium` or `large-v3` for higher accuracy (slower on CPU).
*   Never use English-only `*.en` models. **Do not add an `initial_prompt`.** In testing, a Taglish prompt leaked its own words into the transcript or made Whisper drop whole lines.
*   Keep the raw output untouched and show it alongside your cleaned version, so the user can see every correction.
*   The script ends with a list of **gaps** (2 s+ with no cue). `--start`/`--end` (seconds or `mm:ss`) transcribe one window, and `--slow 0.75` stretches the audio first; timestamps stay in source time. See 0b, steps 1 and 3.
*   Requirements: `pip install -r scripts/requirements.txt`, plus `ffmpeg` on PATH.

**0b. Hard-audio routine.** When the audio is noisy, fast, overlapping or barely audible, or the transcript has gaps or gibberish, gather all of this before cleaning:

0. **Identify the language first.** Not every Filipino clip is Tagalog. Check hashtags (*#bisaya*, *#bisdak*, *#ilocano*), captions and marker words (Cebuano: *kaayo*, *karon*, *unsa*, *dili*, *naa*, *gyud*). Whisper has no option for most Philippine languages, so `tl` is the closest setting, but its output will be spelled like Tagalog. Transcribe in the **speaker's** language, never "Tagalogized", and watch for words that look the same but mean different things in the two languages (Cebuano *kaayo* "very" ≠ Tagalog *kayo* "you"). For Cebuano, see [references/bisaya-cebuano.md](references/bisaya-cebuano.md). For other languages, say so, and flag the transcript for a native speaker.
1. **Check every gap.** Go through the script's gap list (and any early ending) and test whether each stretch is really silent: `ffmpeg -i <media> -af silencedetect=n=-35dB:d=1 -f null -`. Sound with no transcript means missed speech, not silence. **Re-run each gap on its own** with `--start`/`--end`, padded by a second or two on each side. A full-file pass often drops the first lines after a switch of speaker or language (narrator → film clip), and repeating the full run drops them again: all three full runs skipped four lines in a row that a 15-second window recovered.
2. **Run it 2–3 times.** Gibberish, or words from an unrelated language (e.g., German *darauf* in a Tagalog clip), means Whisper fell back to random sampling, so each run differs. Line the runs up and trust only the words that recur. On long recordings, the runs often match word for word on clean stretches and split apart only where the audio is really hard (overlapping shouting, sobbing). Spend your effort and your low-confidence tags there.
3. **Zoom in on hard stretches.** Re-run fast, shouted or overlapping stretches as short windows (5–30 s), once at normal speed and once with `--slow 0.75`. Line the window runs up with the full runs just as in step 2. Windows bring back dropped openers and particles (*Ke, isa…*, *Okay! Ikaw na!*), rapid-fire lists, and whole shouted sentences that a full run reduced to *Ay, tama na!* Re-run whenever:
    *   a cue covers far more time than its words could fill (a short line on a long cue means speech was lost);
    *   a line starts abruptly with no opener in heated or fast talk;
    *   the runs disagree, or speakers overlap.
4. **Make one English pass** (`--language en`). Whisper *translates* instead of transcribing, and that English gloss tells you what a garbled line is about (*"I'm just a friend"* → *kaibigan ko*; *"every month"* → *buwan-buwan*). Use it for meaning only; its wording is never what was said, and it can even flip the meaning (*muntik nang magpakamatay*, "almost killed himself", came out as *"why Mark died"*). When the sound and the gloss disagree, trust the sound. The English pass also silently skips long emotional Tagalog stretches, so a gap in it is not silence. On sparse or quiet audio the English pass can invent stock lines (*"Thank you so much for watching, see you in the next video"*, *"Please subscribe"*); discard them. **Exception:** for stretches spoken *in English* (move names, titles, English phrases), the English pass is a real transcription and beats both the `tl` spelling and your sense of what "should" be said (*window of eagle* → *wind of eagle*, not the more logical *wing*).
5. **Read the screen.** Pull frames (`ffmpeg -i <video> -vf fps=1 frames/%03d.jpg`, or crop and tile the caption band) and collect:
    *   **Broadcast subtitles** (TV news): close to ground truth. They expose translation leaks and acronym errors.
    *   **Fan captions** (TikTok/Reels/Shorts): evidence, not truth. They are split across frames and unpunctuated, so stitch them into sentences. Captioners mishear too (*"SA MUKHA ANG"* was *sa mukha kang*). When a caption breaks Tagalog grammar, trust the grammatical reading.
    *   **Post description, hashtags and the platform's search suggestion:** they often quote the key line (*"Burst fade parin to ya?"*, *"magluluto na original video"*, *"tatlong basong kutsara"*).
    *   **Livestream comments:** the speaker is answering them, which tells you who *kayo/n'yo* is and what was asked. Never transcribe comments as speech.
    *   **Scene:** setting, roles and props (police station, kitchen, interview with microphones) narrow the vocabulary.
    *   Captions in parentheses (*"(korean cough)"*, *"(laughs)"*) describe sounds; write them as `[sound: …]`, not as speech.
    *   Overlay titles added by re-uploaders (*"mga taong mahilig sa yosi"*) are meme framing, not dialogue.
    *   **Audio only?** Say so in the output. Without the screen you lose captions and who is speaking, so leave lines unlabeled unless the voices are clearly distinct.
6. **Identify the source.** Compilations, reaction videos and reuploads of famous films or teleseryes often name the title (narrator, file name, description). Remembered lines from a well-known scene are useful evidence for medium confidence, but they are never ground truth: memory of a quote is often slightly off, so the audio decides. A remembered line may only **choose between** readings that already fit the raw syllables. It must never replace them. Character names are the most useful thing a known source gives you, nicknames included (*Basha* is called *Bash*, which Whisper wrote as *Mas* / *Mat* / *Ma*).
7. **Separate the speakers.** In fights and overlapping talk, Whisper merges two voices into one line, and the quieter voice is lost or glued on (*"Sinungaling ka pa!"* with *"Tama na!"* from the other actor underneath). Split a line into turns when:
    *   the voice changes (pitch, male/female) partway through;
    *   the second half answers or contradicts the first (*"…And you will never be Celine."* / *"Celine is dead. Hindi na siya babalik."*);
    *   the pronouns flip (*ako*↔*ikaw*);
    *   one speaker pleads (*Tama na! Awat na!*) under another's shouting.

    Label the turns *A:* / *B:* (or with names, once known). For each overlap, give both lines with their own confidence tags.

### 1. Reconstruct the Transcript (ASR Cleanup)
Work through the evidence in this order. The patterns behind each step, with verified examples, are in [references/asr-hallucinations.md](references/asr-hallucinations.md).

1.  **Anchor on the hard evidence.** Lines confirmed by subtitles, descriptions or captions are fixed points. Rebuild the rest around them.
2.  **Decode by sound, word by word.** Sound each fragment out and apply the sound patterns: vowel swaps (*kawale* → *kawali*), stop swaps (*napten* → *napkin*), v→b and f→p in English loanwords (*Bicap* → *V-cut*), collapsed reduplication (*nag-drog* → *nagdodroga*), words split at the wrong boundary (*naman tika* → *ng mantika*), address terms (*kaya* → *kuya*), and English nouns turned into verbs (*nagnanapten* → *nagnanapkin*). Pick the candidate with the fewest sound changes.
3.  **Catch Whisper's English-side errors.** In `tl` mode, Whisper bends shouted English and interjections into Tagalog-looking nonsense (*Sarate! Shoot!* ← *Attention!*). It also outputs English *translations* of Tagalog lines (*"What is CBDC?"* ← *"Ano 'yung CBD?"*), drifts acronyms (*CBD* → *CBDC*), and drops the small Tagalog words around English terms. Flag a bare English line inside a Tagalog exchange as a possible leak.
4.  **Match the domain vocabulary.** Guess the domain from the scene (food, haircuts, drugs, school, games), then test garbled nouns against its words. Whisper turns Filipino dish names (*English plan* ← *leche flan*) and English jargon (*Mersfade* ← *burst fade*) into nonsense.
5.  **Use the conversation's structure.**
    *   **The speaker's own repeated phrases:** a clear *"Paano mo nasabing mabilisan?"* later decodes *"Paano nga sabi?"* earlier.
    *   **The interview turn pattern:** question → dodge → the question repeated → answer.
    *   **Rhetorical frames.** Emotional monologues repeat one frame (*May kulang ba sa 'kin? May mali ba sa 'kin?*, *Sana maisip mo rin…* ×4, *Ako na 'yung tama, ako na 'yung mali…*). Decode the clearest instance, then use it as the template for the garbled ones. The same phrase can also come back in another scene: a clear *Bakit 'di mo kayang aminin?* decodes an earlier *bakit niyo ay mo mga menin*.
    *   **Procedural order** in tutorials and recipes: *"Pag mainit na ang kawali…"* means the step before was heating (*pagpapainit … ng mantika*).
6.  **Check the grammar fits.** The verb decides the marker (*lagyan … ng*, *ilagay … ang*), and linkers attach where they belong (*nasabing*, *siyang*). A mismatch means a word was misheard.
7.  **Preserve what was heard.**
    *   Never delete a small word Whisper actually caught (*na*, *nga*, *pa*, *eh*, *po*, *lang*), and keep English discourse markers (*so*, *okay*, *actually*).
    *   Reattach split affixes with hyphens (*nag-drive*, *i-send*).
    *   Restore stress and glottal stops from context (*bása*/*basâ*, *búkas*/*bukás*).
    *   Cleanup repairs what was misheard; it does not tidy up the speaker's grammar.
8.  **Never abandon a stretch.** Write the full best-guess sentence with a confidence tag (high / medium / low). A specific guess helps the reviewer more than "[unclear]". Mark edit cuts at clip edges as cut (*"…to sa ating…"*) instead of inventing words.

### 2. Semantic Analysis
*   Extract the core intent of the cleaned transcript, including who says what and why it is funny or notable.
*   Map informal slang, euphemisms or regionalisms (e.g., *charot*, *lodi*, *omsim*, *amats*, *dinadatnan*) to their semantic equivalents before formulating a response.

### 3. Localization & Dubbing Output (If generating spoken response)
*   **Ask which language to dub into** when the source isn't Tagalog (e.g., keep Bisaya or convert to Tagalog). Don't assume.
*   **Match Cadence:** Literal translations sound overly formal and robotic in Tagalog. Translate the *intent*, not the literal words.
*   **Use Conversational Taglish:** Where natural to a native speaker in an everyday setting, keep standard English loanwords rather than forcing purist coinages (e.g., use "airplane" or *eroplano* instead of *salipawpaw*).
*   **Syllable Pacing:** If the output is for dubbing, keep sentence length and syllable count as close to the source audio timing as possible. Use contractions (e.g., *'yung* instead of *iyong*, *sa'yo* instead of *sa iyo*) to speed up the sentence.

## Gotchas
*   Never output rigid, textbook Filipino (formal or academic register) unless explicitly requested. Manila-style conversational Taglish is the default for natural dubbing.
*   Do not "correct" grammatically accepted Taglish (like *nag-a-update*) into pure English or pure Tagalog.
*   **Never "correct" the speaker's own mistake.** A phrase that makes no sense (*"tatlong basong kutsara"*, "three glasses of spoon") may be exactly what was said, and is often the joke the meme exists for. If the post description, captions or search suggestion quote the odd phrase, it was really said, so keep it verbatim and explain it in the analysis. The same goes for invented names in parodies (*wind of eagle*, *isnik dragon*): absurd is on purpose, so don't "improve" them into what makes sense. Fix only what the ASR misheard.
*   **Sound beats story.** When ASR output is ambiguous, pick the reconstruction closest in sound, not the one that best fits the scene or makes the strongest punchline. Theme-driven guessing turned *Bulihin* into "shoot" (*babarilin*) when it was really "catch" (*huhulihin*), and the English gloss *"add oil"* turned *papay* into *ilalagay* when it was *pagpapainit*.
*   Watch out for false friends: Spanish loanwords in Tagalog often have slightly different meanings than in modern Spanish.
