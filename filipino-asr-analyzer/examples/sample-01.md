# Example Analyses

## Example 1: ASR Cleanup (Taglish)

**Raw ASR input**
```
pa ray add toe con a nah ba? goose toe co sana mag drive tie yo mamaya
```

**Cleaned transcript**
> Pare, dito ka na ba? Gusto ko sana mag-drive tayo mamaya.

**Fixes applied**
- *pa ray* → *pare*, *add toe* → *dito*, *goose toe* → *gusto*, *tie yo* → *tayo* (phonetic hallucinations)
- *con a nah* → *ka na* (fused particles split)
- *mag drive* → *mag-drive* (affix reattached with a hyphen)

**Intent:** The speaker is asking whether their friend has arrived and suggesting they drive somewhere together later.

---

## Example 2: Deep Tagalog → Modern

**Input**
> Nais kong batid mo na ikaw ay aking iniibig.

**Modern output**
> Gusto kong malaman mo na mahal kita.

**Notes:** *nais* → *gusto*, *batid* → *malaman*, *iniibig* → *mahal*. The inverted *ay* construction becomes predicate-first word order.

---

## Example 3: English → Dubbing Line

**Source (English, ~2 seconds)**
> "Dude, are you here yet? I was thinking we could drive around later."

**Dub (conversational Taglish)**
> Pare, nandito ka na? Mag-drive tayo mamaya, gusto mo?

**Notes:** It translates the intent rather than word for word. It keeps the English loanword *drive* and uses a short tag question so the syllable count fits the source timing.
