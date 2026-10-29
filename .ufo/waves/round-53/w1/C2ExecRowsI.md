# C2ExecRowsI — wave-1 report (R53-C2, rows: coverage-census, git-leak-probe, password-recovery-probe, round33-c1-literals, round38-c2, round42-c2, round46-c3, sources-adopt)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsI/ledger-part.json` (8 entries; keys: argv, exit, state, kind, [reason, evidence], tip_dependent, seconds, argv_source).

## Method
- `C=$(mktemp -d -p /fast/scratch/hyaku/kengaku-r53/C2ExecRowsI); git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$C/lane"`; `rev-parse --show-toplevel` printed `$C/lane`.
- NOTE: the clone is of the lane's current HEAD `1373b6c` (wave-1 dispatch commit), not literally `536925b`. `git diff --stat 536925b HEAD` is additions only (26 files: the a34838f counters/pins/shards plus the 1373b6c spec files); no SKILL/SOURCES/SCORECARD/LOG/README byte changed. Registry cells, scripts and corpus counts are those of the base tip.
- Each argv ran from `cwd="$C/lane"`, no shell, `TMPDIR` = a per-run dir under `$C`, 900 s timeout, twice, with `git reset --hard` + `git clean -fdx` before each run (same as the counter's Worker). Runner: scratch `run.py` (deleted with the scratch dir). Clone stayed clean (`git status --short` empty).
- Both runs agreed on exit code for all 8 rows; for the red rows the stdout+stderr was also byte-equal (round38-c2, round42-c2, round46-c3 checked with `cmp`). No flaky row.

## Per row (argv · exit · seconds run1/run2 · state · kind)
| row | argv | exit | s | state | kind |
|---|---|---|---|---|---|
| coverage-census | `python3 corpus/evidence/round13-coverage/coverage_census.py` | 0 | 0.1/0.1 | green | entry |
| git-leak-probe | `python3 plans/git_leak_probe.py --lane .` | 0 | 9.3/9.9 | green | entry |
| password-recovery-probe | `python3 plans/password_recovery_probe.py --lane .` | 0 | 2.9/4.1 | green | entry |
| round33-c1-literals | `python3 plans/round33_c1_verify.py --lane .` | 0 | 0.1/0.1 | green | entry |
| round38-c2 | `python3 plans/round38_c2_verify.py --lane .` | 1 | 3.4/3.1 | red | entry |
| round42-c2 | `python3 plans/round42_c2_verify.py --lane .` | 1 | 92.2/76.8 | red | entry |
| round46-c3 | `python3 plans/round46_c3_verify.py --lane .` | 1 | 3.7/4.2 | red | entry |
| sources-adopt | `python3 plans/sources_adopt.py --selftest` | 0 | 0.0/0.0 | green | selftest |

Arg sources: every `--lane .` is the entry cell verbatim; coverage-census omits the optional `--revision REV` (working-tree census, no input needed); no `--work`/`--scratch` passed. sources-adopt: the entry needs `--package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`, a path outside the lane, so the row's own self-test cell was used (`SELFTEST cases=17 failed=0`). No help-kind rows from this seat.

Green observations: coverage-census prints JSON census (knowledge files=56 indexed=55, etc.) and exits 0 (cell: 0 even with gaps); git-leak-probe summary `cases=25 observed_pass=13 observed_fail=12 mismatches=0`; password-recovery-probe `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`; round33-c1-literals `checks=8 defects=0`.

## Red rows — cause and tip dependence
- **round38-c2** (exit 1): `V2 DEFECT spec=frozen gate=frozen gate_exit=1`; embedded gate `P8 DEFECT index_rows=55 knowledge_files=56` (`corpus/knowledge/fixture-honest-geometry.md`, landed round 50, is in no `corpus/README.md` index row). All other legs ok; `checks=7 defects=1`, `PREDICATE C2 fail`. **Tip-dependent**: L1 must re-measure after this round touches `corpus/README.md` or adds/indexes a `corpus/knowledge/*.md` entry. If the index is repaired (or the count otherwise equalised), the row would turn green (exit 0) and the declared `red` entry would then mismatch.
- **round42-c2** (exit 1): same P8 cause; `checks=9 defects=1` (V2 only; V8 `order_exit=0 result=PASS`, V9 ok). ~77–92 s (it re-runs the fibsqrt probe). **Tip-dependent**, same files as above. Cell claims for this row at fda71ae (defects=5) are stale vs. observed defects=1.
- **round46-c3** (exit 1): `checks=13 defects=3`: V2 (same P8), V7 `rows=5 tags=7` (entry `## Requirement map` lacks `both-print` and `toolchain` rows), V8 `order_exit=1` (`order_check.py` reports `ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c … probe-executed-before-receipt` — a git-history fact). **Tip-independent** as a row state (V7/V8 depend on committed round-46 entry and history); only the V2 leg is tip-dependent. Evidence fragment chosen is the V8 line so it survives a P8 repair.

## Registry cells disagreeing with observation (quoted <= 25 words)
- round38-c2: cell exit `0` "`checks=7 defects=0` then `PREDICATE C2 pass`" — observed exit 1, `checks=7 defects=1` (P8).
- round42-c2: cell "at tip `fda71ae` ... `checks=9 defects=5` (V2 V3 V4 V7 V9)" — observed `checks=9 defects=1` (V2 only).
- round46-c3: cell's `0` pass state is not reached; its own measured text ("`checks=13 defects=3`", V2/V7/V8) AGREES with observation, so no disagreement beyond the pass path.
- Others (coverage-census, git-leak-probe, password-recovery-probe, round33-c1-literals, sources-adopt): no disagreement found; row cells state exit 0 / `checks=8 defects=0` / `cases=17`-style outputs and observation matches. round33's `--selftest` (`cases=11`) was not executed.

## Tools
None installed. `tool:` anomalies: none. Scratch `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsI/` removed before yield.
