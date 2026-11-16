---
name: filipino-asr-analyzer
description: Cleans, interprets, and localizes noisy Tagalog/Filipino audio transcripts. Use when the user feeds messy ASR text, Taglish, or asks to prepare/analyze conversational Filipino for dubbing and fluent playback.
---
# Filipino ASR Analyzer & Dubbing Engine

## Summary
Enhances the agent's fluency in Tagalog by correcting phonetic hallucinations from English-biased ASR, interpreting Taglish code-switching, and ensuring output cadence is natural enough for voice dubbing.

## When to Use
*   The user provides an ASR transcript containing mangled Tagalog or Taglish.
*   The user needs an English prompt translated into conversational, spoken Filipino for dubbing.
*   The user asks to clean, analyze, or respond to informal Filipino text.

## Register Policy
Lean on **modern conversational Tagalog** (Manila-style Taglish) by default. Deep Tagalog (*malalim na Tagalog*: literary, formal, poetic, or purist) must still be recognized and correctly interpreted when it appears in the input. Convert it to modern equivalents unless the user asks to keep the formal register. See [references/register.md](references/register.md).

## References
*   [references/asr-hallucinations.md](references/asr-hallucinations.md): common English-ASR mishearings of Tagalog and structural fixes (Step 1).
*   [references/slang-glossary.md](references/slang-glossary.md): modern slang and reversed words (Step 2).
*   [references/register.md](references/register.md): deep → modern equivalents and spoken contractions (Steps 2–3).

## Steps

### 0. Get the Raw Transcript (only when given audio/video)
If the user provides a media file or a video URL instead of text, transcribe it first with the bundled script (run from this skill's directory):

```bash
python scripts/transcribe.py <file-or-url> --out <transcript.txt>
```

*   Defaults: multilingual `small` model, language `tl`. Use `--model medium` or `large-v3` for higher accuracy (slower on CPU), or `--language auto` for heavily English-mixed audio.
*   Never use English-only `*.en` models; they cannot transcribe Tagalog.
*   Keep the raw output untouched and show it alongside your cleaned version, so the user can see every correction.
*   Requirements: `pip install -r scripts/requirements.txt`, plus `ffmpeg` on PATH.

### 1. Reconstruct the Transcript (ASR Cleanup)
*   **Identify Phonetic Hallucinations:** English-biased ASRs often map Tagalog syllables to English words (e.g., ASR output "plannel" usually means *plano*, "add toe" usually means *dito*). Sound the phrase out phonetically to deduce the original Tagalog intent.
*   **Fix Prefix/Suffix Code-Switching:** Correct fractured Taglish conjugations. Reattach prefixes to English root words using hyphens (e.g., *nag-drive*, *papa-deliver*, *i-send*).
*   **Restore Stress and Glottal Stops:** ASR output drops diacritics, so use sentence context to tell apart words that differ only in stress or a final glottal stop (e.g., *bása* [read] vs. *basâ* [wet], *búkas* [tomorrow] vs. *bukás* [open]).

### 2. Semantic Analysis
*   Extract the core intent of the cleaned prompt.
*   Map informal slang or regionalisms (e.g., *charot*, *lodi*, *omsim*) to their semantic equivalents before formulating a response.

### 3. Localization & Dubbing Output (If generating spoken response)
*   **Match Cadence:** Literal translations sound overly formal and robotic in Tagalog. Translate the *intent*, not the literal words.
*   **Use Conversational Taglish:** Where natural to a native speaker in an everyday setting, keep standard English loanwords rather than forcing purist coinages (e.g., use "airplane" or *eroplano* instead of *salipawpaw*).
*   **Syllable Pacing:** If the output is for dubbing, keep sentence length and syllable count as close to the source audio timing as possible. Use contractions (e.g., *'yung* instead of *iyong*, *sa'yo* instead of *sa iyo*) to speed up the sentence.

## Gotchas
*   Never output rigid, textbook Filipino (formal or academic register) unless explicitly requested. Manila-style conversational Taglish is the default for natural dubbing.
*   Do not "correct" grammatically accepted Taglish (like *nag-a-update*) into pure English or pure Tagalog.
*   Watch out for false friends: Spanish loanwords in Tagalog often have slightly different meanings than in modern Spanish.
