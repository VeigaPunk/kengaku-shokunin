# R1C1BeforeRepro — R55-C1 before-state independent reproduction

Seat: R1C1BeforeRepro (falsifier of the freeze's before receipt). Date: 2026-10-30.

## Verdict

**REPRODUCED.** A fresh clean shared clone at the frozen base tip
`798f5e9ef30ef39291295565209b65a17343c00e` running `python3 plans/round52_c2_registry.py --lane <clone>`
prints output byte-equal to the committed `.ufo/waves/round-55/claims/c1-before.txt` modulo the
clone path on the `COMMAND` line, with exit 1 and the exact frozen headline numbers:

- `ADVERTISED total=79` ✓
- `REGISTERED total=77 rows=79` ✓
- `MISSING 2` = exactly `{plans/round54_c1_anchor.py, plans/round54_c2_entrytruth.py}` ✓
- `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0` ✓
- `PREDICATE R52-C2 fail` ✓
- exit 1 ✓

## What I ran

1. `mkdir -p /fast/scratch/hyaku/kengaku-r55/R1C1BeforeRepro` — exit 0.
2. `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin clone` — exit 0.
   - Initial HEAD was master tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
     (claims file commit; local lane has advanced past the frozen base — expected).
   - `git rev-parse --show-toplevel` asserted = `/fast/scratch/hyaku/kengaku-r55/R1C1BeforeRepro/clone`
     before any in-clone git mutation (host guard).
3. `git checkout 798f5e9ef30ef39291295565209b65a17343c00e` (inside my scratch clone only; no lane git mutation)
   — exit 0; `git rev-parse HEAD` → `798f5e9ef30ef39291295565209b65a17343c00e`;
   `git status --porcelain` empty (clean tree at base).
4. From the lane (read-only invocation against my clone):
   `python3 plans/round52_c2_registry.py --lane /fast/scratch/hyaku/kengaku-r55/R1C1BeforeRepro/clone`
   — exit **1**, output captured to `c1-before-repro.txt`.
5. `diff <committed c1-before.txt> <stamped reproduction>` — the only differing line is line 2
   (`COMMAND … --lane /fast/scratch/hyaku/kengaku-r55/c1before/clone` vs
   `… /R1C1BeforeRepro/clone`); `DIFF_EXIT=1` solely due to that path
   (see `receipt-diff.txt`). All other lines byte-equal.

Full captured output:

```
ADVERTISED total=79
REGISTERED total=77 rows=79
MISSING 2
  MISSING plans/round54_c1_anchor.py
  MISSING plans/round54_c2_entrytruth.py
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 fail
EXIT=1
```

## Scan-completeness check (advertised-universe)

The counter (`plans/round52_c2_registry.py`, base revision) defines its advertised universe as
command-form mentions (`CMD = r"python3 (plans/…|corpus/evidence/…|grader\.py)"`) found only in
`self_assessment_files()`: `SCORECARD.md`, `SKILL.md`, `LOG.md`, `corpus/README.md`, plus every
existing `corpus/knowledge/*.md` (62 files scanned at base). I re-derived the universe
independently with the same regex over those 62 files → 79 advertised scripts, matching
`ADVERTISED total=79`.

- Picked script 1: `plans/round54_c1_anchor.py` — advertised in `SCORECARD.md` → in scanned set ✓
- Picked script 2: `plans/round52_c2_registry.py` — advertised in `SCORECARD.md`, `SKILL.md` → in scanned set ✓
- Corroborating: `plans/round54_c2_entrytruth.py` ← `SCORECARD.md`; `plans/round53_c2_tipstate.py` ←
  `LOG.md`, `SCORECARD.md`, `SKILL.md`.
- Exhaustive: for **all 79** advertised scripts, every advertiser file is inside the scanned set —
  zero advertisers outside it (see `scan-advertisers.json`). Distribution: SKILL.md 77, SCORECARD.md 71,
  LOG.md 17, knowledge 22, corpus/README.md 2.

A whole-repo sweep (excluding `.git`) shows command-form mentions of existing scripts in `.ufo/`
historical wave receipts and in `plans/round-54-claims.md` / `plans/*.py` themselves, but those are
not lane self-assessment files; the counter's scope is deliberately bounded to the five
self-assessment surfaces (comment at plans/round52_c2_registry.py lines 24–27). Critically, the
round-54 regression vector — advertising in `LOG.md` without registry rows — lies inside the
scanned set, which is exactly how the counter surfaces it (MISSING 2). No scan gap found.

## Files written

- `.ufo/waves/round-55/w1/R1C1BeforeRepro/c1-before-repro.txt` — stamped reproduction output (byte-equal to committed receipt modulo clone path).
- `.ufo/waves/round-55/w1/R1C1BeforeRepro/receipt-diff.txt` — `diff` vs committed receipt, `DIFF_EXIT=1` with the single clone-path line.
- `.ufo/waves/round-55/w1/R1C1BeforeRepro/scan-advertisers.json` — per-script advertiser files within the scanned set (all 79).
- `.ufo/waves/round-55/w1/R1C1BeforeRepro/report.md` — this report.
- `.ufo/waves/round-55/w1/R1C1BeforeRepro.md` — scoped findings (per the Report trailer).

## Defects found

None. The frozen before receipt is an honest, reproducible statement of the base state; the
counter's advertised-universe scan is complete over the frozen self-assessment surface.

## Dead ends / notes

- None. No tools installed; no lane writes; no subagents spawned; no git mutation outside my
  scratch clone (checkout inside the clone only, after asserting its toplevel).
- Scratch dir `/fast/scratch/hyaku/kengaku-r55/R1C1BeforeRepro/` deleted after receipts were copied out.
