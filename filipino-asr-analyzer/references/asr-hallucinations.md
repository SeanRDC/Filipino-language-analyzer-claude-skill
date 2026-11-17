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
| Kaya, … kaya? | *Kuya, … kuya?* | the address term *kuya* (also *ate*) misheard as *kaya* | 2026-11-16-04 |
| nag-drog ako / droga ka ba | *nagdodroga ka ba* | progressive reduplication *nag-do-droga* collapsed, and *ka ba* misheard as *ako* | 2026-11-16-04 |
| Paano nga sabi? / Paano mo na sabi | *Paano mo nasabi(ng)…?* | *mo* dropped, *nasabi* split, linker *-ng* lost | 2026-11-16-04 |
| Interactes na nga ako | *Ida-drug test nga ako* | Taglish future *i-da-* + English *drug test* (the reduplication lands on the English word) bent into a fake English word | 2026-11-16-04 |
| Lelan, paano kong kaya nag-drog ako | *Tinatanong ko nga, eh, nagdodroga ka ba?* | a repeated question that came out almost unrecognizable | 2026-11-16-04 |
| kaya vika ko | *kaibigan ko* | decoded with the English-mode gloss *"I'm just a friend"* | 2026-11-16-04 |
| Walang bayat | *Walang bayad* | final *d* → *t* | 2026-11-16-04 |
| kupit | *gupit* | g→k devoicing (like *suntalo* → *sundalo*) | 2026-11-16-04 |
| great ka ba / Ganit ka ba | *Galit ka ba?* | *l* misheard; English mode bends the word into *great* | 2026-11-16-04 |
| Mersfade | *burst fade* | English haircut term outside Whisper's Tagalog vocabulary; English mode gave *Mercedes-Benz* | 2026-11-16-05 |
| Bicap | *V-cut* | Filipino v→b pronunciation ("bi-cut"); English mode gave *B-Cup* | 2026-11-16-05 |
| ba rin tayo? | *pa rin 'to, 'ya?* | b/p confusion; clipped *'ya* (*kuya*) fused with *'to* | 2026-11-16-05 |
| kasi nga lang | *kaso nga lang* | *kaso* ("but") misheard as *kasi* ("because") | 2026-11-16-05 |
| Pag-antayan kasi sa mukha ano | *Maganda 'yan kesa sa mukha kang ano…* | the opening was lost; the fan caption also misheard *kang* as *ANG* | 2026-11-16-05 |
| so mo papay dito kaya naman tika sa kawale | *So pagpapainit na tayo ng mantika sa kawali* | reduplicated *pa-pa-init* collapsed (*papay*); *ng mantika* split as *naman tika*; *-i* → *-e* | 2026-11-16-06 |
| magliluto / kawale / naingit | *magluluto* / *kawali* / *mainit* | vowel swaps and *ma-* → *na-* | 2026-11-16-06 |
| English plan | *leche flan* | Filipino dish name (Spanish-derived) bent into English words | 2026-11-17-01 |
| lang yan natin ang | *lagyan natin ng* | *lag-yan* heard as *lang yan*; the marker follows the verb (*lagyan … ng*) | 2026-11-17-01 |

## Shouted Commands and Interjections

- **English commands become fake Tagalog.** A shouted English word in a Tagalog clip (*Attention!*, *Salute!*, *Go!*) is often split into short, odd cues that look like Tagalog or English. In a soldier, school or drill scene, check those fragments against drill commands first: *Attention!*, *Harap sa kaliwa/kanan… Harap!*, *Tikas pahinga!*, *Saludo!*.
- **Reaction interjections collapse.** Short phrases like *Ah, kaya pala*, *Ay, grabe*, *Ayan, ang ganda* lose their consonants and merge (*Ayos ay ala*, *Yanang ganda*). Rebuild them from the vowel pattern and the scene, not from the letters.
- **Translation instead of transcription.** Even with `language=tl`, Whisper sometimes writes an English **translation** of a Tagalog line (*"What is CBDC?"* for *"Ano 'yung CBD?"*). Suspect this when a short English line sits inside a Tagalog exchange, especially a question or reply, and the speaker otherwise talks in Tagalog. If on-screen captions exist, check against them. Otherwise rebuild the likely Tagalog form and mark it low confidence.
- **Acronym drift.** Whisper changes an acronym into a better-known one (*CBD* → *CBDC*). Check acronyms against the scene (drugs, banking, school) before accepting them.
- **Dropped short words around English terms.** Short Tagalog words (*ka*, *siya*, *eh*, *po*, the linker *-ng*) vanish next to English words and acronyms (*"CBD siya, eh"* → *"CBDC."*). If a line is just a bare English term, the Tagalog around it was probably lost. Flag it for review instead of treating it as complete.
- **Clip edges are cut.** Memes, duets and screen recordings often start or end mid-word. A leading fragment (*uto* ← *[lu]to*/*[i]to*) or a trailing extra syllable (*kutsahar* ← *kutsara*) is an edit artifact. Mark it as cut (*"…to sa ating…"*) instead of inventing a whole word from it.
- **Short cues may be out of order.** When interjections are under one second long and talk overlaps, Whisper's timestamps can swap their order. Do not treat the cue order as certain.

## Structural Patterns

- **Collapsed reduplication (future and progressive aspect):** Tagalog repeats the first syllable of the root for the future (*hu-hulihin*, *ba-barilin*, and on English words too: *i-da-drug test*), the ongoing tense after *nag-/mag-/um-* (*nag-do-droga*, *nag-a-update*, *ka-kain*), and causatives with *pa-* (*pag-pa-pa-init*, *magpapainit*). ASR often merges the repeated syllable into one, sometimes with a changed consonant (*Bulihin* ← *Huhulihin*, *nag-drog* ← *nagdodroga*). If a verb root looks oddly short or starts with a strange consonant, try putting the reduplicated syllable back.
- **Address terms:** *kuya*, *ate*, *boss*, *sir*, *pare* often open or close a question (*"Kuya, … ka ba, kuya?"*). Whisper turns *kuya* into *kaya*. A *kaya* at the start or end of a question is usually *kuya*. The term is also clipped to *'ya* (*kuya*) or *'te* (*ate*) and fused with the word before it (*"'to, 'ya?"* → *tayo*).
- **Filipino accent on English loanwords (v→b, f→p, z→s):** many speakers say English *v* as *b* and *f* as *p*, and Whisper spells what it hears. *Bicap* is *V-cut* (said "bi-cut"), and *Mersfade* is *burst fade*. When a garbled word has *b/p/s* in it and the topic is English-heavy (haircuts, gadgets, food, basketball), try the English word with *v/f/z*.
- **The *mukha kang ___* construction:** *mukha kang* ("you look like a"), *mukhang* ("looks like") and *parang* set up comparisons and roasts (*"mukha kang ano… mukhang talong"*). Whisper and captions both drop the *k* in *kang*. If a line reads *mukha ang/ano*, check for *mukha kang*.
- **Domain jargon:** names of haircuts (*burst fade*, *V-cut*, *taper*, *undercut*), brands and game terms are mostly English and outside Whisper's Tagalog vocabulary. Guess the domain from the scene first, then match against its jargon.
- **Filipino dish names:** Whisper bends them into English or other words (*English plan* ← *leche flan*). In any cooking or food scene, test garbled nouns against common dishes: *leche flan, adobo, sinigang, tinola, kare-kare, kaldereta, menudo, afritada, pancit, lumpia, sisig, lechon, halo-halo, turon, puto, kutsinta, bibingka, ensaymada, champorado, arroz caldo*.
- **The verb decides the marker (focus agreement):** *lagyan natin **ng** asukal* vs. *ilagay natin **ang** asukal*; *bilhan mo **ng*** vs. *bilhin mo **ang***. Pick the verb that matches the syllables first, then make the marker agree with it. A mismatch (*ilagay … ng*, *lagyan … ang*) means one of the two was misheard.
- **Prefer the closest sound match over the most dramatic reading:** Choose the candidate that needs the fewest sound changes. *Bulihin* → *Huhulihin* keeps *-ulihin* intact, while *Babarilin* would change most of the word. Do not let the scene's theme (e.g., soldier → "shoot") pull you toward a more violent or sensational verb.
- **Split affixes:** "nag drive", "i send", "mag pa deliver" → *nag-drive*, *i-send*, *magpa-deliver*. Reattach the affix to the English root with a hyphen.
- **English nouns made into Tagalog verbs:** Taglish turns English nouns into verbs with *nag-/mag-* plus a repeated first syllable (*nag-na-napkin*, *nagfe-Facebook*, *magla-laptop*). Whisper mangles the English part (*nagnanapten*). Strip the affix and the repeated syllable, then match what's left to an English noun that fits the topic.
- **Stop consonants swap (k/t/p, g/d/b), mostly at the end of a syllable:** *napten* → *napkin*, *bayat* → *bayad*, *kupit* → *gupit*. When a word is one consonant away from a topic word, take the topic word.
- **Particle and noun fused across a word boundary:** *ng mantika* → *naman tika*, *sa mga kababayan* → *Samakababayan*, *ipakita at* → *ipakitat*, *itinuro sa atin* → *tinuturusahati*. Whisper re-splits a run of syllables at the wrong place, sometimes producing a real but wrong word (*naman*). If a common particle sits right before a fragment, try moving the boundary.
- **Fused particles:** "kana", "nalang", "dinaman" → *ka na*, *na lang*, *din naman*. Split them back into separate words.
- **ng / nang confusion:** ASR spells both as "ng" or "nang". Use *ng* before nouns (object/possessor marker) and *nang* for "when", "so that", manner, or repetition (*tumakbo nang mabilis*, *kain nang kain*).
- **Vowel swaps (i↔e, u↔o):** Tagalog speakers blur *i/e* and *u/o*, especially at the end of a word, and Whisper spells exactly what it hears (*kawale* → *kawali*, *magliluto* → *magluluto*, *lalake* → *lalaki*). Restore the standard spelling unless the word is a real *e/o* word (*babae*, *ano*, *sino*) or a deliberate dialect or regional spelling.
- **n↔m and extra consonants on adjectives:** *naingit na* → *mainit na*. A *ma-* adjective that comes out as *na-* plus a stray consonant is usually the plain *ma-* word.
- **Dropped glottal stops and stress:** Text without diacritics loses the difference between *bása*/*basâ*, *búkas*/*bukás*, *báka*/*baká*. Decide from context.
- **Language mislabel:** *hindi* (no/not) can come out capitalized as the language "Hindi".
