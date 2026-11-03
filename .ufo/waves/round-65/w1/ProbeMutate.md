# ProbeMutate — seat report (kengaku r65 w1)

Lane root base: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. All `…/` paths below are
relative to it. Scratch root `/fast/scratch/hyaku/kengaku-r65/ProbeMutate` was created for this
seat and removed after the evidence was copied here.

## What was tested

Mutation test of the R65-C1 instrument as built by seat ProbeBuild:
`…/.ufo/waves/round-65/w1/ProbeBuild/round65_c1_sqlite_probe.py`
sha256 `f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb`, against the real receipt
`…/.ufo/waves/round-65/w1/ProbeBuild/sqlite-gcov-probe.txt`
sha256 `25c7cab7da00c44b32ab2a939ca9b1626dc0539e870ce9759654bea1535b3ba0`.
Ten single-point mutants, each a fresh copy in scratch; the seat-dir original was never modified.

## Verdict

**10/10 mutants caught; no surviving mutant.** Baseline first (pristine) was green, so no mutant
result is a baseline failure:
- `--check-receipt` on the receipt of record → rc 0, `CHECK ok cases=5`, `PREDICATE R65-C1 pass`;
- full battery → rc 0, `CASE G1=P/P/P G2=F/F/F G3=P/P/F G4=P/P/F G5=P/P/F`, `PREDICATE R65-C1 pass`;
- that fresh receipt re-checked → rc 0.

| mut | single point changed | observed | verdict |
|---|---|---|---|
| M1 | `FROZEN_LEGS["G1"]` leg-3 P→F + `predict_legs` coverage branch (derivation agrees) | battery rc 1 `CASE G1 observed=P/P/P expected=P/P/F`; checker on real receipt rc 1 `CHECK fail G1 expected P/P/P != P/P/F` | caught |
| M2 | `/dev/null` mask bind dropped for G1–G4 | battery rc 1 `CASE G2 observed=P/P/F expected=F/F/F`; real receipt still rc 0 | caught |
| M3 | `FROZEN_FRAGMENTS` G2 leg-2 entry deleted | forged G2 fragment → pristine rc 1 `fragment G2 leg2 'ok' lacks 'sqlite3 not found in PATH'`, mutant rc 0 | caught |
| M4 | `AMALG_SHA256` := 64×`a` | battery rc 2 `SETUP amalgamation-sha-mismatch … != aaaa…`, no receipt; checker rc 1 | caught |
| M5 | `FROZEN_LEGS["G4"]` leg-3 F→P, derivation untouched | battery rc 2 `SETUP prediction-drift G4 derived=P/P/F frozen=P/P/P`, no receipt | caught |
| M6 | per-case LEG-row cross-check disabled | forged LEG G2 1 F→P → pristine rc 1 `G2 leg-verdicts PFF != FFF`, mutant rc 0 | caught |
| M7 | stored-predicate agreement disabled | forged `PREDICATE … fail` → pristine rc 1 `stored-predicate fail disagrees with derived pass`, mutant rc 0 | caught |
| M8 | per-case no-bind clause disabled | forged receipt without `NOBIND G3` → pristine rc 1 `G3 no-bind-observation-missing`, mutant rc 0 | caught |
| M9 | `GRADER_SHA256` := 64×`a` | battery rc 2 `SETUP grader-sha-mismatch b165… != aaaa…`, no receipt; checker rc 1 | caught |
| M10 | LEG-line half of the fragment clause disabled | forged `LEG G2 2 … frag=ok` → pristine rc 1 `G2 leg-2 fragment does not carry the frozen fragment`, mutant rc 0 | caught |

## Findings worth carrying into the closure

1. **The two fragment halves are independently load-bearing.** M3 removes both halves of the G2
   entry and M10 removes only the LEG-line half; each time the forged receipt the pristine rejects
   is accepted (rc 0). Neither half is redundant with the other or with the stored-predicate line.
2. **`--check-receipt` cannot see a mask drop; the battery can.** M2's mutant receipt is internally
   contradictory (`SHAPE … masked=G2:yes` while `ENV G2 which_sqlite3=/usr/bin/sqlite3`) and the
   pristine checker still returns rc 0 on the receipt of record. This measures the instrument's
   named text-only limitation: the masking discipline is witnessed by the live per-case vector
   (`CASE G2 observed=P/P/F expected=F/F/F`), not by the receipt re-derivation.
3. **The r59 M-1 derivation guard fires before any compile.** M5 (frozen edited, derivation not)
   aborts rc 2 `SETUP prediction-drift` and writes no receipt, so a drifted freeze cannot grade.
4. **Both SHA anchors refuse before grading.** M4 and M9 each abort rc 2 with a `SETUP` line and no
   receipt, and each also makes the receipt of record fail its checker.
5. **Residual coverage (named, not claimed):** `TOOLCHAIN` field presence, per-case `BUILD`/`RUN`
   line presence, the `masked`/`build` field checks in `CASE`, the G4 fragment entry (M3 targets G2
   only), and the `VECTOR`-line presence check were not mutated. No claim is made about them beyond
   the pristine battery exercising their accept direction.

## Evidence (written here, observed bytes)

`…/.ufo/waves/round-65/w1/ProbeMutate/`
- `mutations.md` — per-mutant `MUT … → observed … — caught`, ends `MUTATIONS: 10/10 caught`
- `evidence/00-restoration-verification.txt` — probe sha before/after, `cmp` on probe and receipt
- `evidence/01-baseline-check-real.txt`, `02-baseline-battery.txt`, `02-baseline-battery-receipt.txt`,
  `03-baseline-check-battery.txt`
- `evidence/10-diffs.txt` — single-point diff of every mutant against the pristine bytes
- `evidence/11-text-detectors.txt` — 21 checker invocations with rc, pristine and mutant, on the
  receipt of record and on five forged fixtures
- `evidence/20-M{1,2,4,5,9}-*-battery.txt`, `evidence/21-M{1,2}-receipt.txt`
- `evidence/mutants/` — the ten mutant sources; `evidence/forged/` — fixtures + generator

## Restoration

After all mutants: seat-dir original probe sha256 still
`f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb`, mtime `2026-11-03 17:11:18`,
`cmp` against the pre-run scratch copy identical; receipt of record `cmp`-identical to the pre-run
copy (sha256 `25c7cab7da00c44b32ab2a939ca9b1626dc0539e870ce9759654bea1535b3ba0`). Scratch dir removed
after copying.

## Bounds

No port bound, no server started (only `ss -ltnH`/`-ltnpH` reads inside the probe); no `git`/`jj`
mutation; no pacman; no tool installed or upgraded this seat (python 3.14.8, bwrap 0.13.1,
gcc/gcov 16.2.1 were already present — nothing to record under the tooling clause); no network
call; no file outside this seat dir and its scratch dir was written.
