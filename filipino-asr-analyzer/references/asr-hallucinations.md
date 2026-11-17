# ASR Hallucination Patterns

English-biased speech recognition often "hears" Tagalog syllables as English words or fragments. Use this table as a pattern guide, not a lookup dictionary: always confirm a fix against the surrounding context.

> These are illustrative patterns. Add real mishearings from your own transcripts as you find them.

## Word-Level Mishearings

| ASR output (typical) | Likely Tagalog | Meaning |
|---|---|---|
| add toe / a toe | *dito* | here |
| manga / mung a | *mga* (pronounced "ma-nga") | plural marker |
| sea yeah / sha | *siya* | he/she |
| nah man / numb on | *naman* | (softener / "on the other hand") |
| con a / kana | *ka na* | you (already) |
| pa ray / pah ray | *pare* | buddy, dude |
| a no / ah no | *ano* | what |
| goose toe | *gusto* | want / like |
| tie yo / tie oh | *tayo* | we (inclusive) |
| peace oh | *piso* | peso |
| Marion / mare on | *meron* (*mayroon*) | there is / have |
| punt a | *punta* | go (to a place) |
| sun a / sauna | *sana* | hopefully / I wish |
| bah ka / backa | *baka* | maybe (or *báka*, cow, by context) |

## Verified From Test Sessions (Whisper, `language=tl`)

These are real mishearings. A native speaker confirmed what was actually said. In Tagalog mode, Whisper makes the opposite mistake to an English ASR: it bends **English** words and fast interjections into Tagalog-looking syllables.

| ASR output | Actually said | Context | Session |
|---|---|---|---|
| Ayos ay ala! | *Ah, kaya pala!* | "Oh, so that's why!", a reaction interjection | 2026-11-16-01 |
| Sarate! / Shoot! | *Attention!* (shouted *"Ten-SHUN!"*) | English drill command broken into fragments | 2026-11-16-01 |
| Bulihin ko | *Huhulihin ko* | "I will catch/arrest". The future-tense reduplication *hu-* merged and its *h* was misheard as *b* | 2026-11-16-01 |
| at Samakababayan natin | *at sa mga kababayan natin* | *sa mga* fused onto the noun | 2026-11-16-02 |
| par may tindihan | *para maintindihan* | verb split at *ma-*; *para* lost its final vowel into the split | 2026-11-16-02 |
| Gumamit ngayon? | *Gumamit ka ngayon?* | the pronoun *ka* was dropped between two words | 2026-11-16-03 |
| Wala naman siya amat eh | *Wala naman siyang amats, eh* | slang *amats* ("high"); the linker *-ng* and the final *-s* were dropped | 2026-11-16-03 |
| CBDC. | *CBD siya, eh.* | acronym changed into a better-known one, and the Tagalog words after it were dropped | 2026-11-16-03 |
| What is CBDC? | *Ano 'yung CBD?* | **translated**: Whisper output English for a Tagalog line, even in `tl` mode | 2026-11-16-03 |

## Shouted Commands and Interjections

- **English commands become fake Tagalog.** A shouted English word in a Tagalog clip (*Attention!*, *Salute!*, *Go!*) is often split into short, odd cues that look like Tagalog or English. In a soldier, school or drill scene, check those fragments against drill commands first: *Attention!*, *Harap sa kaliwa/kanan… Harap!*, *Tikas pahinga!*, *Saludo!*.
- **Reaction interjections collapse.** Short phrases like *Ah, kaya pala*, *Ay, grabe*, *Ayan, ang ganda* lose their consonants and merge (*Ayos ay ala*, *Yanang ganda*). Rebuild them from the vowel pattern and the scene, not from the letters.
- **Translation instead of transcription.** Even with `language=tl`, Whisper sometimes writes an English **translation** of a Tagalog line (*"What is CBDC?"* for *"Ano 'yung CBD?"*). Suspect this when a short English line sits inside a Tagalog exchange, especially a question or reply, and the speaker otherwise talks in Tagalog. If on-screen captions exist, check against them. Otherwise rebuild the likely Tagalog form and mark it low confidence.
- **Acronym drift.** Whisper changes an acronym into a better-known one (*CBD* → *CBDC*). Check acronyms against the scene (drugs, banking, school) before accepting them.
- **Dropped short words around English terms.** Short Tagalog words (*ka*, *siya*, *eh*, *po*, the linker *-ng*) vanish next to English words and acronyms (*"CBD siya, eh"* → *"CBDC."*). If a line is just a bare English term, the Tagalog around it was probably lost. Flag it for review instead of treating it as complete.
- **Short cues may be out of order.** When interjections are under one second long and talk overlaps, Whisper's timestamps can swap their order. Do not treat the cue order as certain.

## Structural Patterns

- **Collapsed reduplication (future/contemplative aspect):** Tagalog marks the future by repeating the first syllable (*hu-hulihin*, *ba-barilin*, *ka-kain*). ASR often merges the repeated syllable into one, sometimes with a changed consonant (*Bulihin* ← *Huhulihin*). If a verb root looks oddly short or starts with a strange consonant, try putting the reduplicated syllable back.
- **Prefer the closest sound match over the most dramatic reading:** Choose the candidate that needs the fewest sound changes. *Bulihin* → *Huhulihin* keeps *-ulihin* intact, while *Babarilin* would change most of the word. Do not let the scene's theme (e.g., soldier → "shoot") pull you toward a more violent or sensational verb.

- **Split affixes:** "nag drive", "i send", "mag pa deliver" → *nag-drive*, *i-send*, *magpa-deliver*. Reattach the affix to the English root with a hyphen.
- **Fused particles:** "kana", "nalang", "dinaman" → *ka na*, *na lang*, *din naman*. Split them back into separate words.
- **ng / nang confusion:** ASR spells both as "ng" or "nang". Use *ng* before nouns (object/possessor marker) and *nang* for "when", "so that", manner, or repetition (*tumakbo nang mabilis*, *kain nang kain*).
- **Dropped glottal stops and stress:** Text without diacritics loses the difference between *bása*/*basâ*, *búkas*/*bukás*, *báka*/*baká*. Decide from context.
- **Language mislabel:** *hindi* (no/not) can come out capitalized as the language "Hindi".
