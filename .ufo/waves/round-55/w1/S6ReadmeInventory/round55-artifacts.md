## Round-55 supporting artifacts (2026-10-30)

| Path | Covers |
|---|---|
| `../plans/round-55-claims.md` | The three claims frozen before data at `80afa613` on base `798f5e9e` — R55-C1 operability 8→9 (registry closure, counter `../plans/round52_c2_registry.py`), R55-C2 calibration 9→10 (entry-argv structural binding), R55-C3 coverage attempt (13th TB2 grader `chess-best-move`, L0-capped) — each with its predicate, counter, kill rule and do-nothing control |
| `../plans/round55_c2_controls.py` | The frozen C2 fixture builder for the two laundering cases (`--case abbreviated-selftest\|uv-decoy-script`, `--against r54\|r55`, `--selftest`), reproducing the round-54 attack routes on one-row scratch git fixtures |
| `../.ufo/waves/round-55/claims/c1-before.txt` | C1 before-run of `../plans/round52_c2_registry.py` at base: `MISSING 2` (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`), `PREDICATE R52-C2 fail`, exit 1 |
| `../.ufo/waves/round-55/claims/c2-before-abbreviated-selftest.txt` | C2 red-before: the `--selft` argparse-prefix fixture passes the unchanged r54 counter (`PREDICATE R54-C2 pass`, exit 0) while the registry-declared entry exits 1 |
| `../.ufo/waves/round-55/claims/c2-before-uv-decoy-script.txt` | C2 red-before: the `uv run … -cprint('wrapper green')` wrapper decoy passes the unchanged r54 counter (exit 0) while the true entry is never executed and exits 1 |
| `../.ufo/waves/round-55/claims/c3-before.txt` | C3 absence receipts at base: the probe receipt absent (`test -e` exit 1), `thirteenth` absent from `PROVINCE.md`, `chess-best-move` with 0 matches in `README.md` and `SOURCES.md` |
| `../.ufo/waves/round-55/claims/census-before.txt` | Pre-wave census receipt over `SOURCES.md`: 15 per-row `W04` duplicate-url notes ending with the `kengaku ok` line |
| `../plans/round55_c2_entryargv.py` — **PENDING-L1** | The new C2 binding counter (`--lane/--source/--work/--jobs/--timeout/--dry/--selftest`): L1 ledger↔registry argv token identity (`ARGV-DEFECT`), L2 interpreter identity refusing `uv`-style wrappers and inline `-c` programs (`WRAPPER-DEFECT`), L3 no argparse flag-prefix abbreviation (`ABBREV-DEFECT`), L4 per-row hermetic ground truth |
| `../plans/round55_c3_chess_probe.py` — **PENDING-L1** | The C3 offline grader probe: a frozen table of 12 synthetic `move.txt` cases, each with a prediction written before the first run, executed against the pinned `chess-best-move` grader (sha256 `a540714e…`, TB2 pin `2fd12b88`) in per-case bwrap sandboxes |
| `evidence/round55/chess-best-move-probe.txt` — **PENDING-L1** | The probe receipt committing the observed per-case verdicts; predicate `cases=12 observed_pass=P observed_fail=F mismatches=0` |
| `knowledge/tb2-chess-best-move-grader.md` — **PENDING-L1** | The knowledge entry for the 13th read TB2 grader: order-insensitive full-multiset equality over whitespace-split tokens (`sorted(move) == sorted(["g2g4", "e2e4"])`), a graded-artefact class new to the lane (r45's password-recovery was line-split membership) |

Rows tagged **PENDING-L1** name artifacts round 55 intends to land; none is committed at the freeze
commit `80afa613` (the probe script exists only as an untracked worktree file). The L1 splices this
section into `corpus/README.md` at landing and drops the tag from each row whose artifact landed; a
kept tag means that artifact did not land.
