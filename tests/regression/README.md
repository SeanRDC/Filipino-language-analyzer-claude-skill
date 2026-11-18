# Regression Scores

How accurate the skill is, measured the same way every time.

- `score.py` lines up a cleaned transcript table (`| mm:ss | line | conf |`) with a reference word by word. It reports exact lines, lines the reviewer had fixed, and word accuracy. Before comparing, it ignores case, punctuation, hyphens and spelling variants (*sa 'kin* = *sakin*, *noon* = *nung*, *niya* = *nya*).
- `2026-11-17-04-reference.md` is the movie-confrontation clip's old cleaned transcript with Sean's per-line fixes merged in. Lines marked `*` are ones Sean fixed. **Caveat:** the unmarked lines are the old skill output that Sean accepted, so any rewording of them counts as an error, even when it may be right.
- **Blind runs** are done by a fresh agent that sees only the audio, the raw Whisper runs and a copy of the skill. That copy has this clip's verified rows removed. The agent never sees the corrections. (SKILL.md still quotes a few of this clip's lines as examples, so the test is not perfectly blind.)

## Results: movie confrontations (15:50, session 2026-11-17-04)

Command: `HYPSKIP=22-30 python -I tests/regression/score.py tests/regression/2026-11-17-04-reference.md <cleaned.md> L115,L116`. 00:22–00:30 has no reviewed reference yet, and L115–L116 are scored inside the L117 block.

| Run | Skill version | Lines exact (137) | Lines Sean fixed, now exact (53) | Word accuracy, all lines | Word accuracy, lines Sean fixed |
|---|---|---|---|---|---|
| Original run, as reviewed | `22ff417` | 83 (61%) | 1 | 91.4% | 78.1% |
| Blind re-run | `342d909` | 64 (47%) | 18 | 89.3% | 83.3% |

What the blind re-run showed:
- **Better on hard lines:** 18 of the 53 lines Sean had to fix now come out exactly right, against 1 before. It also recovered five lines at 00:22–00:30 that every full run dropped.
- **Drift on easy lines:** 38 lines Sean had accepted came out with 1–2 small differences. Some are real regressions: it kept raw slips that are real words (*nambababae*, *nasasaktan*, *conversation scenes*), dropped a real English line (*It's up to you!*), and re-decoded lines every run agreed on (*ang* ↔ *'yung*, *tinatanaw* → *tinatahak*). Others may be right where the old line was wrong, and only a listen can settle them (*'wag ipagkait sa'yo* vs. *'wag mo nang ikaila*; *Poy* (Popoy) vs. *Boy*).
- Fixes: `e317d11` (limits of raw-first), `4ff7030` (window hygiene), `a7c8a3f` (leaks vs. real English), `dfbcc0f` (rule conflicts).
