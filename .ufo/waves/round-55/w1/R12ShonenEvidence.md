# R12ShonenEvidence — scoped findings (SHONEN box evidence)

Four SHONEN.md boxes, non-author evidence only. All commands executed
2026-10-30 from the lane root; no lane writes outside this seat's dir.
Per-box detail + raw run bytes: `.ufo/waves/round-55/w1/R12ShonenEvidence/`
(`boxes.md`, `grader-selftest.out`, `controls-selftest.out`, `case-abbrev.out`).

## Box-by-box

1. **SKILL.md decision tables/error patterns/checklists with cited sources — SUPPORTED.**
   Sampled citations resolve: file cite `corpus/evidence/round8-horizon/run.log:81-83`
   (lines read `A-INC: 7/10 / A-MONO: 0/10 / A-CKPT: 1/10`, matching anti-pattern 16's
   text); file cite `corpus/evidence/round9-fleet/harness-mutation.md` (17,372 bytes,
   present); command cite `python3 grader.py --selftest` executed → exit 0,
   `[selftest] ALL PASS`.
2. **End-to-end domain task executed and logged — SUPPORTED.** LOG.md's latest landed
   entry (Round 54 + measured close) names frozen commands with receipts; all four
   integrate receipts exist and match the entry: `c1-after.txt` (`SETUP header.bin
   absent`, `PREDICATE R54-C1 fail`, `EXIT 1`); `c2-after.txt` (`executed=78`,
   `laundered=1`, declared 62/16 vs observed 61/17, `redeclared=4`, `PREDICATE
   R54-C2 fail`); `round52-c2-regression.txt` (`ADVERTISED 79 / REGISTERED 77 /
   MISSING 2`, exit 1); `census-end.txt` (`ROWS 193`, `A164/B24/C5`,
   `mined172/queued8/rejected13`).
3. **Instructions executable without oral context — SUPPORTED.** Executed cold from
   written bytes: `python3 plans/round55_c2_controls.py --selftest` → exit 0,
   `SELFTEST cases=4 failures=0` (TMPDIR redirected to seat scratch). Corroborating
   cold run `--case abbreviated-selftest --against r54` → exit 0, `ROUTE laundering
   demonstrated (r54 rc=0, true entry exit=1)` — reproduces the frozen R55-C2
   before-red shape non-author.
4. **No cross-domain bleed / PROVINCE accurate — SUPPORTED.** Core spot 3 re-run:
   `grader.py` sha256 == row pin `90c87c88…ae941f`; the row's 12-dir probe-artifact
   loop prints nothing missing; `corpus/SOURCES.md` present (live 195 rows vs dated
   round-51 "171" and r54 census-end 193 — dated-snapshot drift, not bleed).

## Defects

None blocking. Observation: PROVINCE Core count cells are dated snapshots;
live re-derivation will show growth (171→193→195). Recorded, not a bleed.

## Checks not run

Full 733-check `python3 grader.py` replay (box 1 already has an executed
command citation via `--selftest`; full replay duplicates peer no-harm scope).
SKILL.md's remaining ~40 cited paths (seat spec: 2 samples).
