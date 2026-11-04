# Draft — four `## Gate/probe registry` rows for the round-68 instruments

Target: `SKILL.md`, section `## Gate/probe registry` (heading at `:587`), rows appended after
`round64-trio-sweep` (`:689`). Owner `kengaku`. Closes R69-C2 **E1** (`plans/round69_c2_routed_defects.py`
`:141-167`), which requires per row: 8 cells, the entry file path present in cell 2 and the file existing,
`` `0` `` and `` `1` `` both in cell 3, and a non-empty self-test cell (cell 4).

Every fact below is copied from the instrument source at the frozen base; the line cites are in the
grounding table. No flag is invented: the flag sets are the `add_argument` calls verbatim.

## Rows (paste-ready; one physical line each, 8 cells)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `round68_c1_pypi_finish` | probe | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt` (lane root; flags implemented: `--lane --work --receipt --evidence-dir --check-receipt --selftest --green-receipt --render-table`; the battery form `--lane . --work <scratch> --receipt <path> --evidence-dir <dir>` runs the four frozen cases in bwrap; `--render-table` prints the case table and `FROZEN-VECTOR`/`DERIVED-VECTOR` without running) | `0` pass (`CHECK ok cases=4 vector=P/F/F/F`, `CHECK stored-predicate=pass derived=pass`, `PREDICATE R68-C1 pass`) · `1` fail (any clause or vector defect, `CHECK defect <name>`, `PREDICATE R68-C1 fail`) · `2` setup (`SETUP receipt-missing`, `grader-sha-mismatch`, `bwrap-absent`, `work-dir-required`, `lane-required`) | `--selftest --work <dir> --green-receipt <receipt>` → `SELFTEST red_refused=5/5 green_ok=1 ok=True` | grader sha `82c63517…` (round-52 pypi-server capture), base-probe sha `2ebaf54e…` (`plans/round63_c1_pypi_probe.py`), TB2 pin `2fd12b88`, frozen vector `P/F/F/F`, receipt `corpus/evidence/round68/pypi/receipt.txt`, per-case stderr captures `corpus/evidence/round68/pypi/stderr/` | writes the `--work`/`--evidence-dir` paths and the receipt; bwrap sandbox, no network beyond 127.0.0.1:8080 | kengaku |
| `round68_c2_correction_gate` | gate | `python3 plans/round68_c2_correction_gate.py` (lane root; flags implemented: `--root --selftest --work`) | `0` pass (`E1..E5 ok`, `DEFECTS n=0`, `PREDICATE R68-C2 pass`) · `1` fail (any `E<n> defect` line) · `2` setup (`SETUP work-dir-required`) | `--selftest --work <dir>` → `SELFTEST defects-in-fake=5 want=5 all-fail=True` | inputs re-hashed in-gate: `plans/round-67-claims.md`, `corpus/evidence/round68/r67-probe-selftest.txt`, `plans/round67_c1_pipeline_probe.py` sha `03793f4f…`, wrongly-cited sha `32bacf1d…`, `corpus/evidence/round67/pipe/a1-mutants.txt`, `SKILL.md` | read-only; fixtures under `--work` | kengaku |
| `round68_report_contract` | gate | `python3 plans/round68_report_contract.py <report.md> --shonen SHONEN.md` (lane root; flags implemented: `--lane --shonen --selftest --work`; `--shonen` defaults to `<lane>/SHONEN.md`) | `0` pass (`DEFECTS n=0`, `PREDICATE R68-A2 pass`) · `1` fail (one `S<n>` defect per missing or malformed required section, S1–S6) · `2` setup (`SETUP could-not-evaluate …`: missing, non-regular, oversized or unreadable input) | `--selftest --work <dir>` → `SELFTEST n=14 red-refused=13 green-ok=1` | the six required `##` headings, the `## Trend verdicts` verdict words, and the four-box SHONEN set (`EXPECTED_BOXES = 4`) read from `SHONEN.md` | read-only over the report and `SHONEN.md`; fixtures under `--work` | kengaku |
| `round68_capability_table` | gate | `python3 plans/round68_capability_table.py --lane .` (lane root; flags implemented: `--lane --scorecard --selftest --work`) | `0` pass (`MISMATCH n=0`, `PREDICATE R68-A3 pass`) · `1` fail (T1 a declared capability has no row, T2 the first-working-round cell does not name the declaring round, T3 the evidence path is absent, T4 a duplicate capability name) · `2` setup (`SETUP could-not-evaluate …`) | `--selftest --work <dir>` → `SELFTEST n=5 red-refused=4 green-ok=1` | `SCORECARD.md` `## Capabilities` table against `DECLARED` (four capabilities, first-working rounds 64–67) | read-only | kengaku |

## Grounding (cell → source)

| row | cell | source |
|---|---|---|
| c1 | entry / flags | `plans/round68_c1_pypi_finish.py:503-511` (`--lane --work --receipt --evidence-dir --check-receipt --selftest --green-receipt --render-table`) |
| c1 | verdict map | `:396-404` (`CHECK ok cases=4 vector=…`, `CHECK stored-predicate=… derived=…`, `PREDICATE R68-C1 pass`), `:240` `SETUP receipt-missing`, `:110` `SETUP grader-sha-mismatch`, `:547` `SETUP bwrap-absent`, `:533/538/541` `SETUP work-dir-required`, `:544` `SETUP lane-required` |
| c1 | self-test | `:491-495` — `SELFTEST red_refused={…}/{len(fixtures)} green_ok={…} ok={ok}`, fixtures `r1-all-p`…`r5-stderr-sha` (five red) + one green receipt |
| c1 | pinned values | `:34` `BASE_PROBE_SHA256 = 2ebaf54e…`, `:35` `GRADER_SHA256 = 82c63517…`, `:36` `TB2_PIN = 2fd12b88…`, `:37` `FROZEN_VECTOR = ("P","F","F","F")`, `:42` `STDERR_DIR`, `:43` `RECEIPT_PATH` |
| c1 | write scope | `:99-101` battery writes under `--work`; `:105` `stderr_dst.mkdir`; `:222-225` receipt write; `:145-149` `m.require_port_free` before every server start (port 8080 only) |
| c2 | entry / flags | `plans/round68_c2_correction_gate.py:223-226` (`--root --selftest --work`) |
| c2 | verdict map | `:165-171` (`DEFECTS n=…`, `PREDICATE R68-C2 pass` on rc 0, `… fail` on rc 1), `:227-230` `SETUP work-dir-required` rc 2 |
| c2 | self-test | `:213-215` — `SELFTEST defects-in-fake={failed} want=5 all-fail={…}` |
| c2 | pinned values | `:36` `R67_PROBE_SHA = 03793f4f…`, `:37` `WRONG_SHA = 32bacf1d…`, `:38` `ERRATUM_HEADING`, `:39` `CLAIMS`, `:40` `TALLY`, `:41` `R67_PROBE`, `:43` `A1_MUTANTS`; the fake-lane selftest strips the erratum section, the pipeline registry row and the sqlite row's `--strict` (`:186-204`) |
| c2 | write scope | `:196-207` writes only the `--work` fake lane; `check()` opens lane files read-only |
| report_contract | entry / flags | `plans/round68_report_contract.py:241-246` (`report` positional, `--lane --shonen --selftest --work`); `--shonen` default resolved to `<lane>/SHONEN.md` at `:176` |
| report_contract | verdict map | docstring `:29` (`Exit 0 = pass; 1 = defects; 2 = could-not-evaluate (missing input).`); `SETUP could-not-evaluate` raised on the input guards |
| report_contract | self-test | `:234` — `SELFTEST n={total} red-refused={refused} green-ok={green_ok}`, 14 fixtures (`r1`…`r14`), 13 refused, 1 green |
| report_contract | pinned values | docstring `:8-14` S1–S6; `:42` `EXPECTED_BOXES = 4`; `:40-48` `HEADINGS` |
| capability_table | entry / flags | `plans/round68_capability_table.py:156-160` (`--lane --scorecard --selftest --work`) |
| capability_table | verdict map | docstring `:24` (`Exit 0 = pass; 1 = mismatches; 2 = could-not-evaluate.`), mismatch classes T1–T4 `:12-16` |
| capability_table | self-test | `:150` — `SELFTEST n={len(fixtures)} red-refused={refused} green-ok={green_ok}`, fixtures s1–s5 |
| capability_table | pinned values | `:36-42` `DECLARED` — `offline-network-service-grader-probe` 64, `offline-db-state-grader-probe` 65, `offline-torch-tensor-parallel-grader-probe` 66, `offline-torch-pipeline-parallel-grader-probe` 67 |

## Deltas from the rows already in the working tree

Observed at drafting time (uncommitted ` M SKILL.md` at HEAD `b288e8e0`): the four rows exist and already
pass E1 (`rows=4/4 missing=[] thin=[]`). This draft is the conformance copy; it differs from the working-tree
text only by adding grounded detail:

- c1: adds the TB2 pin `2fd12b88`, the frozen vector `P/F/F/F`, the `--render-table` flag, the
  `stderr/` capture directory, `CHECK stored-predicate=…`, and the `lane-required` setup token.
- c2: adds the wrongly-cited sha `32bacf1d…`, the `ERRATUM_HEADING`/`TALLY` pins, and the `SELFTEST ` prefix
  on the self-test spelling (the instrument prints `SELFTEST defects-in-fake=…`).
- report_contract: adds `--lane`/`--shonen` to the flag list and names `EXPECTED_BOXES = 4`.
- capability_table: names the T1–T4 mismatch classes and the four `DECLARED` capabilities with their rounds.

## One ungrounded item

The round-69 claims doc's C1 kill rule names `SETUP receipt-exists` and `SETUP port-8080-occupied` as
paths of the C1 instrument. Neither string is emitted by `plans/round68_c1_pypi_finish.py`
(`grep -c` → 0 for `receipt-exists`; `port-8080-occupied` exists only in the base probe
`plans/round63_c1_pypi_probe.py:280`, raised as `SetupError`, and the wrapper's `run_battery` has no
`except SetupError`). They are therefore **not** listed in the c1 verdict-map cell, because the row must
describe what the instrument prints. This is a C1 finding, not a registry fact; see the seat report.
