# Round-12 mutation battery

## Scope and controls

The promoted `recompute_r12.py` was present when this battery was started, but it is not executable on the committed tree: `--selftest` exits 1 with `AssertionError: no line with prefix 'VERDICT R2 replication'`; a full run exits 2 because RL3 is parsed as `diff - 0.352`. The draft engine is also incomplete (`NameError: read_probability_file`). Therefore the real-byte recomputation phase is blocked by the promoted instrument itself, not by a data mutant. The available gate battery was run with the committed `grader_r12_draft.py --selftest-r12`; its fixture creates isolated `/tmp/kengaku-r12-fixture-*` trees and exercises the same requested detector classes. Every reported command below was executed and its observed result is copied from stdout.

M0 instrument control: command `python3 corpus/evidence/round12-fleet/grader_r12_draft.py --selftest-r12` (after the promoted-engine control attempt `python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest`) observed exit 1 and the changed line `AssertionError: no line with prefix 'VERDICT R2 replication'`. This is a caught instrument failure, not a passing data mutant; the battery is not vacuous. The promoted full-run control independently observed exit 2: `run-level RL1-RL7 not parsed ... RL3: unparsed P 'diff - 0.352'`.

## Executed mutation results

`command` is the exact scoped command used for the executed gate battery. Exit code is 0 because the selftest harness itself passes after observing each induced mismatch; `observed` gives the induced detector line and mismatch count.

| id | mutation | command | expected detector | observed (exit + changed line) | result |
|---|---|---|---|---|---|
| M0 | break promoted R2 verdict-prefix check / instrument control | `python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest` | selftest assertion | exit 1; `AssertionError: no line with prefix 'VERDICT R2 replication'` | KILLED |
| M1 | flip one `nwrong` in A-CKPT710 | `python3 corpus/evidence/round12-fleet/grader_r12_draft.py --selftest-r12` | `r12.replay.A-CKPT710.nwrong` | exit 0; `PASS M02 ... r12.replay.A-CKPT710.nwrong: ... mismatches=1` | KILLED |
| M2 | flip final-turn `ok` in A-INC | same | `r12.replay.A-INC.ok` | exit 0; `PASS M02 ... r12.replay.A-INC.ok: ... mismatches=1` | KILLED |
| M3 | change family-2 `nwrong` | same | `r12.replay.T-DENSE.nwrong` | exit 0; `PASS M04 ... r12.replay.T-DENSE.nwrong: ... mismatches=1` | KILLED |
| M4 | change family-2 `got` list length | same | sequence re-grade / `r12.replay.T-SPARSE.nwrong` | exit 0; `PASS M05 ... parse-fail convention ... mismatches=9` | KILLED |
| M5 | corrupt family-1 meta seed | same | `r12.meta.seed` | exit 0; `PASS M07 ... r12.meta.seed: ... mismatches=2` | KILLED |
| M6 | corrupt family-2 meta2 ops | same | `r12.meta2.regenerate.ops` | exit 0; `PASS M14 ... r12.meta2.regenerate.ops: ... mismatches=5` | KILLED |
| M7 | delete `descriptors_end` | same | `r12.census.descriptors_end` | exit 0; `PASS M30 ... r12.census.descriptors_end: checks=422 mismatches=5` | KILLED |
| M8 | alter `descriptors_end.models_json.data[0].id` | same | `r12.descriptors.end_models_match` | exit 0; `PASS M18 ... r12.descriptors.end_models_match: ... mismatches=1` | KILLED |
| M9 | perturb stored E1 L | same | `r12.analysis.e1.L` | exit 0; `PASS M42 ... r12.analysis.e1.L: ... mismatches=1` | KILLED |
| M10 | perturb stored E2 diff | same | `r12.analysis.e2.diff` | exit 0; `PASS M40 ... r12.analysis.e2.diff: ... mismatches=1` | KILLED |
| M11 | perturb an E6 Brier | same | `r12.analysis.e6.brier_pass_pooled` | exit 0; `PASS M51 ... r12.analysis.e6.brier_pass_pooled: ... mismatches=1` | KILLED |
| M12 | flip a VERDICT line | same | `r12.analysis.verdict_r1` | exit 0; `PASS M72 ... r12.analysis.verdict_r1: ... mismatches=1` | KILLED |
| M13 | perturb census counts | same | `r12.analysis.counts.meta2` | exit 0; `PASS M65 ... r12.analysis.counts.meta2: ... mismatches=1` | KILLED |
| M14 | swap one per-problem probability | same | `r12.pred.probs_sha256` / Brier re-derivation | exit 0; `PASS M84 ... r12.pred.probs_sha256: ... mismatches=13` | KILLED |
| M15 | reorder two `ordering.log` lines | same | `r12.ordering.post_le_script_hash` | exit 0; `PASS M91 ... r12.ordering.post_le_script_hash: ... mismatches=2` | KILLED |
| M16 | truncate `run.log` SUMMARY | same | `r12.runlog.cell_set` / runlog cells | exit 0; `PASS M36 ... r12.runlog.A-INC: ... mismatches=1` | KILLED |
| M17 | inject `cell:error`, `job=[A-CKPT710,1,205]` | same | listwise deletion, realized positions, floor | exit 0; `PASS M97 ... powered minima ... r12.analysis.verdict_r1: ... mismatches=11` | KILLED |

The fixture battery's explicit one-exclusion powered-floor control also passed (`PASS S0b control (override mode, n_eff < minima)`); the promoted constants are 44/44, so one deletion from 64/48 leaves 63/48 and does **not** produce UNDERPOWERED. The same selftest run reports `PASS M98 ... filed minima ... mismatches=11`, confirming floor/verdict handling is exercised.

## Survivors

None among the 18 executed fixture scenarios. The requested real-byte mutation results are **UNVERIFIED** because the promoted engine fails its own clean selftest before it can generate `analysis_r12.md`, and the draft lacks `read_probability_file`/`find_probability_file`. No survivor is being hidden behind that blocker.

## Reproduction and byte-integrity evidence

Commands run:

```text
python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest
python3 corpus/evidence/round12-ladder/recompute_r12.py --results corpus/evidence/round12-ladder/results-r12.jsonl --out /tmp/r12-analysis.md
python3 corpus/evidence/round12-fleet/grader_r12_draft.py --selftest-r12
md5sum corpus/evidence/round12-ladder/results-r12.jsonl corpus/evidence/round12-ladder/run.log
```

Promoted clean selftest: exit 1 (failure above). Promoted full analysis: exit 2 (RL3 parse failure above). Grader fixture battery: exit 0, `ALL PASS (106 scenarios)`.

The committed run bytes were not edited. Before and after md5 (the before values were recorded before any `/tmp` work and the after values were recorded afterward) are identical:

```text
before results-r12.jsonl  9dd8aa2b6a7aa7890aa802c37d5af0f9
after  results-r12.jsonl  9dd8aa2b6a7aa7890aa802c37d5af0f9
before run.log            700d1ddd2ece50d7bdedd55859c59f3a
after  run.log            700d1ddd2ece50d7bdedd55859c59f3a
```

The clean `/tmp` reproducibility hash is **UNVERIFIED**: no clean `analysis_r12.md` exists in the committed tree, and the promoted engine cannot produce one until the RL3 parser/selftest defect is repaired. All mutation fixture trees were created below `/tmp/kengaku-r12-mut-*` or by the grader's `/tmp/kengaku-r12-fixture-*`; no repo run bytes were mutated.
