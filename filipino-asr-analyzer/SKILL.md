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

## Steps

### 1. Reconstruct the Transcript (ASR Cleanup)
*   **Identify Phonetic Hallucinations:** English-biased ASRs often map Tagalog syllables to English words (e.g., ASR output "plannel" usually means *plano*, "add toe" usually means *dito*). Sound the phrase out phonetically to deduce the original Tagalog intent.
*   **Fix Prefix/Suffix Code-Switching:** Correct fractured Taglish conjugations. Reattach prefixes to English root words using hyphens (e.g., *nag-drive*, *papa-deliver*, *i-send*).
*   **Restore Stress and Glottal Stops:** ASR output drops diacritics, so use sentence context to tell apart words that differ only in stress or a final glottal stop (e.g., *bása* [read] vs. *basâ* [wet], *pitó* [seven] vs. *pitô* [whistle]).
