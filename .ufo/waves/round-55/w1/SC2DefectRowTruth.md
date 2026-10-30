# SC2DefectRowTruth — round-55 wave-1 seat report (trailer)

Axis: calibration. Scope: independent truth for ledger row `round35-c1-coverage`
(double-run beside E4). Deliverable: `.ufo/waves/round-55/w1/SC2DefectRowTruth/round35-truth.md`;
full seat report: `.ufo/waves/round-55/w1/SC2DefectRowTruth/report.md`.

## Measured truth (clean shared clone @ tip `80afa613`, exit 1, stderr empty)

```
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=58 index rows=58 (want 42/42)
V5 ok
V6 ok
checks=6 defects=1
PREDICATE C1 fail
```

4/4 runs byte-identical (sha256 `69d71d195336bdbed46c4260e71ee46b51f986a7baf392ea60f2c9cb9d8d337d`).

## Delta vs the ledger's declared fragment

- Declared (`plans/round54-entrytruth.json`, row `round35-c1-coverage`):
  `V4 DEFECT knowledge files=57 index rows=57 (want 42/42)`
- Observed now: `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)`
- **Delta = the two integers 57 → 58** (knowledge-file count, README index-row count).
  Everything else (prefix, field names, `(want 42/42)`, exit 1, red state, all other V-lines)
  is unchanged.

## Cause

Commit `9a0746be` added `corpus/knowledge/external-anchor-freeze.md` + one README index row
(57→58) and re-derived three *other* ledger rows' evidence but not this one. The declared
fragment was verbatim-correct at the declaration tip `6e0a1915` (re-verified by running the
entry there) and went stale at `9a0746be`.

## Consequence for R55-C2 (calibration)

Red-row evidence is matched as a **substring** of the entry's stdout
(`plans/round54_c2_entrytruth.py:338`). The declared 57-fragment is NOT a substring of the
current stdout (empirically `False`; the 58-fragment is `True`) → this row yields
`EVIDENCE-MISSING round35-c1-coverage`, breaking the frozen after-predicate
`evidence_missing=0` unless the ledger is corrected (data) before the after-run — exactly the
correction R55-C2 (a) mandates.

**Landing rule for the L1:** the fragment is tree-dependent, not a constant. Re-derive it at
the measured-after revision:
`V4 DEFECT knowledge files=<N> index rows=<N> (want 42/42)` with `N = git ls-files
'corpus/knowledge/*.md' | wc -l` there. `[INFERENCE]` R55-C3's one new knowledge entry + one
README index row → `N = 59`; not measured (the corpus entry had not landed).

## Files written

- `.ufo/waves/round-55/w1/SC2DefectRowTruth/round35-truth.md`
- `.ufo/waves/round-55/w1/SC2DefectRowTruth/report.md`
- `.ufo/waves/round-55/w1/SC2DefectRowTruth.md` (this file)

No lane-tracked file touched; no mutating git/jj; no subagents; no tool installs.

## Observed corroboration (unchanged r54 counter, tip clone, exit 1)

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb clean=yes lane_rev_equal=yes
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=1
TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=61 observed_red=17
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
```

`round35-c1-coverage` is the ledger's **only** `evidence_missing` row (1 of 78). The static
legs are clean (`argv_defect=0 bad_decl=0 missing=0 extra=0`) → the defect is purely the stale
evidence datum, fixable by a one-line data correction. `LAUNDERED round52-c2` and the
`declared_red=16 / observed_red=17` skew are other rounds' surfaces (R55-C1's registry
regression), not my row — reported, untouched.

## Measurement hazard (observed)

`v4()` counts knowledge files with `git ls-files` (**tracked only**) but README index rows
from the **working tree**. A read-only snapshot of the live in-flight lane printed
`V4 DEFECT knowledge files=58 index rows=59 (want 42/42)` (the round-55 README index row for
`knowledge/tb2-chess-best-move-grader.md` is already in the README; the entry file has not
landed). That snapshot also showed `V6 DEFECT census exit 1` — the live-lane branch of `v6()`
validating an in-flight `corpus/SOURCES.md`; on a clean clone `V6 ok`. **The L1 must re-derive
and commit the fragment at a clean, committed landing revision**, never on a dirty in-flight
tree, or the row stays `EVIDENCE-MISSING` with an asymmetric count baked in.

## Honest gaps

- The `N = 59` landing-revision value is a **prediction**, not a measurement: no round-55
  corpus entry had landed in the tree I measured, so the L1 must re-run the entry at the
  landing revision and commit the observed line.
- The r54 counter corroboration needed a *fresh* `--work` directory after the first attempt
  was killed at the 300 s default deadline (it buffers output to the end; the killed run left
  `work54/w0/src` behind, and the retry aborted with
  `fatal: destination path … already exists`). The successful retry (fresh `--work`,
  `--jobs 6`) completed in 239 s.
