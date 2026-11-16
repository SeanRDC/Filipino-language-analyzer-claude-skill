# Filipino Language Analyzer — Claude Skill

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for analyzing Filipino (Tagalog) text.

> **Status:** 🚧 Early initialization. The skill is not functional yet.

## Goal

Give Claude a focused, repeatable way to break down Filipino text. The analysis covers:

- **Morphology:** root words (*salitang-ugat*) and affixes (*panlapi*): prefixes, infixes, suffixes, and circumfixes.
- **Verb focus and aspect:** actor/object focus (*pokus*) and aspect (*aspekto*: perfective, imperfective, contemplative).
- **Parts of speech:** tagging of *pangngalan*, *pandiwa*, *pang-uri*, *pang-abay*, and others.
- **Particles and markers:** *ang/ng/sa*, *si/ni/kay*, enclitics like *na, pa, din/rin, lang*.
- **Code-switching:** detection of Taglish (Tagalog–English mixing).
- **Plain-language explanations:** results that learners can read, not only linguists.

## Planned Structure

```
.
├── README.md
└── filipino-language-analyzer/
    ├── SKILL.md          # Skill entry point (frontmatter + instructions)
    ├── references/       # Grammar notes, affix tables, particle lists
    ├── scripts/          # Helper scripts used by the skill
    └── examples/         # Sample inputs and expected analyses
```

## Installation

_Coming soon._ Instructions will be added after the first working version of the skill.

## Usage

_Coming soon._

## Roadmap

- [ ] Project initialization
- [ ] Draft `SKILL.md`
- [ ] Affix and particle reference files
- [ ] Example analyses
- [ ] Testing and evaluation
- [ ] First release

## Authors

- **Sean** ([@SeanRDC](https://github.com/SeanRDC)): project lead
- **Claude** (Anthropic): co-author

## License

_To be decided._
