# ProbeMutate — mutation test of the R65-C1 instrument (round 65, w1)

Subject: `kengaku-shokunin/.ufo/waves/round-65/w1/ProbeBuild/round65_c1_sqlite_probe.py`
sha256 `f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb` (recorded before any
mutant; re-hashed after: `evidence/00-restoration-verification.txt`).
Receipt of record: `…/ProbeBuild/sqlite-gcov-probe.txt`
sha256 `25c7cab7da00c44b32ab2a939ca9b1626dc0539e870ce9759654bea1535b3ba0` (pre-run copy `cmp`-identical
after the battery, same file).

All paths below are cited lane-root-based; lane root =
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Every mutant is a fresh copy under
`/fast/scratch/hyaku/kengaku-r65/ProbeMutate/mutants/`; the seat-dir original was never written.

Baseline before any mutant (so a killed mutant is not a baseline failure):
`--check-receipt` on the receipt of record → rc 0 `CHECK ok cases=5` / `PREDICATE R65-C1 pass`
(`evidence/01-baseline-check-real.txt`); full battery → rc 0 with the five frozen vectors and
`PREDICATE R65-C1 pass` (`evidence/02-baseline-battery.txt`); that fresh receipt re-checked → rc 0
(`evidence/03-baseline-check-battery.txt`).

Detector per mutant: `--check-receipt` on the receipt of record, a full battery re-run where the
mutation is run-behavioural, and (for checker mutations) a forged receipt whose only difference is
the clause under test. Single-point diffs: `evidence/10-diffs.txt`; all runs:
`evidence/11-text-detectors.txt` + `evidence/20-*-battery.txt`.

MUT M1 vector-flip `FROZEN_LEGS["G1"]` leg-3 `P`→`F` **and** the `predict_legs()` coverage branch
flipped in step (derivation agrees — zero `SETUP` lines, `PREDICTION G1=P/P/F`) → battery rc 1:
`CASE G1 observed=P/P/P expected=P/P/F` + `PREDICATE R65-C1 fail`, receipt written
(`evidence/21-M1-receipt.txt`); `--check-receipt` on the receipt of record rc 1
`CHECK fail G1 expected P/P/P != P/P/F` — caught.

MUT M2 mask-drop `/dev/null` bind suppressed for G1–G4 (`if case.masked and case.name == "G5"`) →
battery rc 1: `CASE G2 observed=P/P/F expected=F/F/F` (`VECTOR G2=P/P/F`) + `PREDICATE R65-C1 fail`;
the mutant receipt still prints `SHAPE … masked=G2:yes` while `ENV G2 which_sqlite3=/usr/bin/sqlite3`
— caught by the battery. `--check-receipt` on the receipt of record rc 0 (text-only limitation).

MUT M3 fragment-weaken `FROZEN_FRAGMENTS` loses the `("G2", 2)` entry → forged receipt with the G2
leg-2 fragment replaced by `ok` on both the `FRAGMENT` and `LEG` lines: pristine rc 1
`CHECK fail fragment G2 leg2 'ok' lacks 'sqlite3 not found in PATH'`; mutant rc 0 `CHECK ok cases=5`
— caught; no other clause holds the line (both halves live in the removed loop).

MUT M4 sha-swap `AMALG_SHA256` := 64×`a` → battery rc 2
`SETUP amalgamation-sha-mismatch 0a9c… != aaaa…`, no receipt written; `--check-receipt` on the
receipt of record rc 1 `CHECK fail amalgamation-sha 0a9c… != aaaa…` — caught.

MUT M5 derive-drift `FROZEN_LEGS["G4"]` leg-3 `F`→`P` with `predict_legs()` untouched → battery rc 2
`SETUP prediction-drift G4 derived=P/P/F frozen=P/P/P`, no receipt written — caught by the r59 M-1
derivation guard; `--check-receipt` on the receipt of record rc 1 `CHECK fail G4 expected P/P/F != P/P/P`.

MUT M6 legrow-weaken the per-case LEG-row cross-check disabled (`row != frozen…` behind `if False`) →
forged receipt with `LEG G2 1 … F` flipped to `P` (VECTOR/CASE lines frozen): pristine rc 1
`CHECK fail G2 leg-verdicts PFF != FFF`; mutant rc 0 — caught.

MUT M7 predicate-line-weaken the stored-predicate agreement disabled → forged receipt whose only
change is `PREDICATE R65-C1 fail`: pristine rc 1
`CHECK fail stored-predicate fail disagrees with derived pass`; mutant rc 0 — caught.

MUT M8 nobind-weaken the per-case no-bind clause disabled → forged receipt with the `NOBIND G3` line
dropped: pristine rc 1 `CHECK fail G3 no-bind-observation-missing`; mutant rc 0 — caught.

MUT M9 grader-sha-swap `GRADER_SHA256` := 64×`a` → battery rc 2
`SETUP grader-sha-mismatch b165… != aaaa…`, no receipt written; `--check-receipt` on the receipt of
record rc 1 `CHECK fail grader-sha b165… != aaaa…` — caught.

MUT M10 legfrag-half only the LEG-line half of the fragment clause disabled (`leg_frags` check behind
`if False`, `FRAGMENT`-line half kept) → forged receipt with `LEG G2 2 … frag=ok` and the `FRAGMENT`
line intact: pristine rc 1 `CHECK fail G2 leg-2 fragment does not carry the frozen fragment`;
mutant rc 0 — caught; the two halves are independently load-bearing.

Calibration notes (observed, not inferred):
- For M3/M6/M7/M8/M10 the receipt of record is accepted (rc 0) by the pristine probe and by the
  mutant alike: the reject direction is invisible in the real receipt bytes and only the forged
  fixture separates the clause. Each removed clause was therefore load-bearing, and the receipt of
  record alone exercises only the accept direction of `--check-receipt` (the instrument's named
  text-only limitation, measured rather than assumed).
- M2's mutant receipt is internally contradictory (`masked=yes` claimed, host binary named in
  `ENV G2`); the text-only checker cannot see it and only the live battery vector does. The battery
  is the load-bearing detector for the masking discipline, not `--check-receipt`.
- Untested clauses (residual, named, not claimed): `TOOLCHAIN` field presence, per-case `BUILD`/`RUN`
  line presence, `masked`/`build` field checks in `CASE`, the G4 fragment entry (M3 removed G2 only),
  and the `VECTOR`-line presence check.

MUTATIONS: 10/10 caught
