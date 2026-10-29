# C2ExecRowsG — tip-state of 8 registry rows (round 53, wave 1)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsG/ledger-part.json` (8 rows, schema as briefed; `.out` files beside it are the raw observed output of run 1 then `=====RUN2=====` run 2, kept for evidence; round46-c1 and config-projection output omitted: long, with scratch paths).

## Method
- Clean shared clone of the lane at HEAD `1373b6c` (descendant of base tip `536925b`/`a34838f`; the diff adds only round-53 spec files, SKILL.md/corpus unchanged vs base): `git clone -q --shared <lane> $C/lane`; `rev-parse --show-toplevel` asserted equal to `$C/lane` per row (one clone per row, 5 rows in parallel). Source `git status --porcelain` empty after both runs of every row.
- Each argv run twice from the clone root, `TMPDIR` a per-run dir, 900 s timeout, `git reset --hard` + `clean -fdx` between runs. Driver: `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsG/run.py` (scratch, removed).
- Exit codes agreed on both runs for every row (no flaky row). All 8 rows are `entry`-kind; 0 help-kind, 0 selftest-kind.

## Per row
| row | argv (after `python3`) | exit (run1/run2) | seconds (r1/r2) | state |
|---|---|---|---|---|
| config-projection | `plans/config_projection.py --summary` | 0/0 | 0.4/0.4 | green |
| gate-flip-check | `plans/gate_flip_check.py --lesson corpus/lessons/round-52.md` | 1/1 | 0.1/0.1 | red |
| order-check | `plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt` | 0/0 | 0.2/0.2 | green |
| round31-c1-literals | `plans/round31_c1_verify.py --lane .` | 0/0 | 0.1/0.1 | green |
| round37-c2 | `plans/round37_c2_verify.py --lane .` | 1/1 | 58.2/54.0 | red |
| round41-c2 | `plans/round41_c2_verify.py --lane .` | 1/1 | 27.9/24.3 | red |
| round46-c1 | `plans/round46_c1_verify.py --lane .` | 0/0 | 27.9/19.3 | green |
| routed-findings | `plans/routed_open.py --lane .` | 0/0 | 0.2/0.3 | green |

Arg sources: all are the row's own entry cell, verbatim, except gate-flip-check, whose `<lesson.md>` placeholder I filled with `corpus/lessons/round-52.md` (newest committed lesson; no `--entry`, so only the flip leg runs). `--work`/`--scratch` never passed. A `--selftest` variant of gate-flip-check was also run (exit 0, `SELFTEST ok` lines, 2.3 s) but not chosen: the entry form works and is the stronger truth.

## Red rows
- **gate-flip-check** (tip-independent): the committed round-52 lesson has three conditional Gate refusals (S191, S192, S193) with no later `Flip check (round N)` line; evidence `FLIPS total=3 unresolved=3`. Only changes if someone edits `corpus/lessons/round-52.md` (append-only, so not expected).
- **round37-c2** and **round41-c2** (tip-dependent): both die only on V2, because the nested `pkg_gate.py` check P8 prints `index_rows=55 knowledge_files=56`. `corpus/knowledge/` holds 56 `.md` files, `corpus/README.md` has 55 backticked `| \`knowledge/...\`` index rows; `fixture-honest-geometry.md` (round-50, `822f3b7`) is cited only by a bullet (README line 664), no table row. Every other leg is `ok` (round37: V1,V3–V7 ok, P10 probe rerun byte-equal; round41: V1,V3–V8 ok). Evidence `gate: P8 DEFECT index_rows=55 knowledge_files=56` (present in both outputs). **L1 must re-measure after any change to `corpus/README.md` or `corpus/knowledge/*.md`** (the round-53 knowledge entry plus its index row keeps the 1-row gap unless the `fixture-honest-geometry` row is also added; adding that row alone turns both rows green and the ledger must then be redeclared exit 0).

`routed-findings` is marked tip-dependent (green) only because it reads `corpus/routed-findings.jsonl`; the counts printed (75/31/1/41/2) would shift if this round edits that file. No other row depends on files this round changes.

## Registry cells that disagree with observation
- `round37-c2`, exit cell: "`0` `checks=7 defects=0` then `PREDICATE C2 pass`" — observed exit 1, `checks=7 defects=1`, `PREDICATE C2 fail` (V2 DEFECT gate_exit=1, P8).
- `round41-c2`, exit cell: "`0` `checks=8 defects=0` then `PREDICATE C2 pass`" — observed exit 1, `checks=8 defects=1` (V2).
- Consistent with observation: config-projection (exit 0, `TOTAL findings=0 exit=0`), order-check (`ORDER RESULT PASS`), round31-c1-literals (`checks=6 defects=0`), round46-c1 (`PINS total=65`, `HONEST fixtures=104`, `PREDICATE C1 pass`), routed-findings (`ROWS total=75 open=31 blocked=1 closed=41 refused=2`, `routed_open=32 oldest_round=39`), gate-flip-check (red on a lesson, exit 1; `--selftest` ok).

## Notes
- Tool installs: none. tool inconsistencies: none observed.
- Blindness: did not read any classifier or label file.
- Scratch `/fast/scratch/hyaku/kengaku-r53/C2ExecRowsG` removed at exit.
