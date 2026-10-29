# C2ExecRowsH — tip-state of 8 registry rows (R53-C2, wave 1)

Seat is blind-neutral (C2 only; no C1 files read). Deliverable: `.ufo/waves/round-53/w1/C2ExecRowsH/ledger-part.json` (exactly the 8 rows). Helper `runner.py` + `cands1.json` kept beside it.

## Method
`C=/fast/scratch/hyaku/kengaku-r53/C2ExecRowsH`; one `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $C/c-<row>/lane` per row (8 parallel); each clone's `git rev-parse --show-toplevel` printed its own dir for the first clone (`$C/lane`) before anything ran. **The clone HEAD was `1373b6c` (lane master: base `536925b` + `a34838f` claims + `1373b6c` wave-1 spec), not the bare base tip** — `git diff --stat 536925b HEAD` touches only the round-53 files (26 files, counters/pin tree/shards), none of the 8 rows' inputs. Each argv ran twice (`reset --hard` + `clean -fdx` between), cwd = clone, `TMPDIR` under `$C`, timeout 900 s, no shell. Command: `python3 runner.py cands1.json`. Both exit codes agreed for all 8 rows (no flaky row). Scratch removed at exit.

## Per row (argv / exit x2 / seconds x2 / state)
| row | argv (cwd lane root) | exit | s | state / kind |
|---|---|---|---|---|
| constraints-probe | `python3 plans/constraints_probe.py --lane .` | 0,0 | 23.9, 25.2 | green / entry — `cases=25 observed_pass=6 observed_fail=19 mismatches=2` |
| gate-timing | `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit 536925b5320fa64298030b4ee76a58fc4b82723f` | 0,0 | 0.1, 0.2 | green / entry — `admissions=1 passed=1 failed=0`; REV = base tip full sha (cell placeholder REV; ancestor of every landing tip) |
| package-gate | `python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json --require-clean-tree` | 1,1 | 0.2, 0.2 | **red** / entry |
| round31-defects | `python3 plans/round31_defects.py --lane .` | 0,0 | 0.6, 0.3 | green / entry — `checks=10 defects=0` |
| round38-c1-mutants | `python3 plans/round38_c1_verify.py --lane .` | 1,1 | 176.9, 143.8 | **red** / entry |
| round42-c1-mutants | `python3 plans/round42_c1_verify.py --lane .` | 0,0 | 16.0, 15.5 | green / entry — `MUTANTS total=14 killed=14`, `PREDICATE C1 pass` |
| round46-c2 | `python3 plans/round46_c2_verify.py --lane .` | 0,0 | 0.6, 1.7 | green / entry — `checks=4 defects=0`, `PREDICATE C2 pass` |
| scratch-root-guard | `python3 plans/scratch_guard.py --selftest` | 0,0 | 0.1, 0.1 | green / **selftest** — `SELFTEST ok=36/36`; the entry cell needs a `<root>` holding a round sentinel, the lane holds none and the r42 sentinel is deleted |

No help-kind rows. Ledger `seconds` = the slower of the two runs.

## Red rows
- **package-gate** (exit 1, tip-dependent). Cause: check P8 — `corpus/knowledge/fixture-honest-geometry.md` (added 822f3b7) has no `corpus/README.md` index row (verified by set difference: 56 files vs 55 index rows). P1–P7, P9 ok. Evidence: `P8 DEFECT index_rows=55 knowledge_files=56 bad=1`. The L1 must re-measure after any commit that touches `corpus/README.md` or `corpus/knowledge/*.md` (the round-53 knowledge entry adds one file and one index row — stays red unless the fixture file gets an index row or is removed; one extra balanced pair does not turn it green).
- **round38-c1-mutants** (exit 1, tip-independent as a whole). Two causes: (1) mutant N21 (D5, "silence") SURVIVES by design — its direction is unreachable; identical `killed=21 survived=1` in `.ufo/waves/round-38/integrate/measure-final.txt:114` and `measure-tip2.txt:114` (so it never passed; round-39 relabelled it M01 "mirror"); (2) at this tip 51 of 86 battery fixtures read `WRONG` because the same P8 defect adds `P8` to every observed defect set (`BATTERY fixtures=86 wrong=51`). Cause (2) is tip-dependent (README/knowledge), cause (1) is not, so the row stays red whatever the round commits. Evidence: `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`.

## Cells that disagree with observation
- `round38-c1-mutants` exit cell: "`0` predicate holds: … `MUTANTS total=22 killed=22 survived=0` … `PREDICATE C1 pass`" — observed `killed=21 survived=1`, `PREDICATE C1 fail`, exit 1 (never held; round-38's own receipt shows the same).
- `package-gate` exit cell `0` accept — the self-test cell is `round36_c1_verify.py`, not this argv; on the tip tree the gate rejects (P8). Not a contradiction of the cell, but no row cell states the tip result.
- `scratch-root-guard` entry cell `check <root>`: unrunnable in-lane (no sentinel); self-test cell matches observation (`SELFTEST ok=36/36`).
- `round46-c2` cell is consistent with observation including the `--selftest`-absent note (not re-probed).
- constraints-probe, gate-timing, round31-defects, round42-c1-mutants: cells match.

Tooling: none installed. No tool inconsistencies observed.
