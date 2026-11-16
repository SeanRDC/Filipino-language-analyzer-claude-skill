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

## Structural Patterns

- **Split affixes:** "nag drive", "i send", "mag pa deliver" → *nag-drive*, *i-send*, *magpa-deliver*. Reattach the affix to the English root with a hyphen.
- **Fused particles:** "kana", "nalang", "dinaman" → *ka na*, *na lang*, *din naman*. Split them back into separate words.
- **ng / nang confusion:** ASR spells both as "ng" or "nang". Use *ng* before nouns (object/possessor marker) and *nang* for "when", "so that", manner, or repetition (*tumakbo nang mabilis*, *kain nang kain*).
- **Dropped glottal stops and stress:** Text without diacritics loses the difference between *bása*/*basâ*, *búkas*/*bukás*, *báka*/*baká*. Decide from context.
- **Language mislabel:** *hindi* (no/not) can come out capitalized as the language "Hindi".
