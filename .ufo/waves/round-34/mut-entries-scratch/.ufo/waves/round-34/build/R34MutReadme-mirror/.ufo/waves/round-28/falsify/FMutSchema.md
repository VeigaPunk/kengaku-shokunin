# FMutSchema — duplicate-task finding suppression mutation

Seat: `KengakuR28.FMutSchema`. Author-side falsification only.

VERDICT: PASS

This verdict applies **only to completion of the assigned, one-mutant empirical probe**: the duplicate-task-ID finding-suppression mutant was **KILLED** by the stock selftest and independently by the hand-expected witness, with clean pristine/restored controls and exact byte restoration. It is not a whole-instrument assurance, candidate source-support approval, score change, or admission decision.

## Axes and boundaries

- **Legacy novelty → canonical coverage/constructs7:** challenge one concrete behavior in the newly measured C1 task-spec audit rather than claim methodological novelty.
- **Calibration8:** distinguish a named finding mismatch from generic nonzero exits; record the actual baseline, mutant, and restored outputs and the limited conclusion. Scores held.

Read `plans/round-28-claims.md`, including Amendment 1, and `corpus/lessons/round-28.md`. The relevant declared contracts are claims lines17/21: task-ID/duplicate inventory and hand-expected duplicate-ID controls. All executable inputs came from isolated copies of the lane-owned instrument and its required stock-selftest fixtures. No upstream source was imported/executed; the stock selftest parses the copied scorer source as AST. No benchmark site, browser, REA MCP, other runtime, host service, package installer, Git index, or lane state was used or changed.

The canonical candidate path `corpus/knowledge/webarena-task-spec-audit.md` is outside this probe. This seat does not provide its complete Q10 source/number reread, endorse it, or admit it. Production code, pinned inputs, candidate bytes, corpus and sibling work were not edited. Writes were confined to this report and `.ufo/waves/round-28/scratch/FMutSchema/`.

## One plausible defect

**Mutant:** remove the `("duplicate_task_id", duplicate_ids)` entry from the population finding-emission tuple in scratch `lane/plans/benchmark_spec_audit.py:153`.

Original:

```python
    for key, values in (("duplicate_task_id", duplicate_ids), ("missing_task_id", missing_ids), ("unexpected_task_id", unexpected_ids)):
```

Mutated:

```python
    for key, values in (("missing_task_id", missing_ids), ("unexpected_task_id", unexpected_ids)):
```

This is one expression deletion at the behavior-bearing emission point. It plausibly models dropping a validation entry during a population-check refactor. It leaves duplicate collection, the `duplicate_task_ids` result field, population-size/missing/unexpected findings, every fixture, and the selftest untouched. The retained mutant bytes match precisely this one deletion; see `restoration.json`.

**Expected stock detector:** `selftest`'s `duplicate_and_missing_ids` probe at lines243/226–230 requires the exact finding-ID set `{duplicate_task_id, missing_task_id}`, not merely a nonzero result. Omitting only the duplicate finding must fail that assertion.

## Independent expected witness

Authored `duplicate-witness.json` before applying the mutation. It is not the stock `miniature * 2` fixture: three distinct valid string-match task objects have IDs `[0, 1, 1]`, different intents/answers, and `expected_population=2`.

Independent arithmetic:

- The expected IDs `{0,1}` are fully present: no missing or unexpected IDs.
- ID1 occurs twice: `duplicate_task_ids=[1]` and finding `{"id":"duplicate_task_id","task_ids":[1]}` are required.
- Three objects exceed population2: `{"id":"population_size","actual":3,"expected":2}` is also required.
- `task_count=3`, `distinct_task_ids=2`.

`witness.py` imports only the assigned **scratch lane-owned** audit module and compares its structured result projection against these literal expectations. The witness intentionally preserves the independent population-size error. Consequently, an exit-only audit check would not establish that duplicate reporting survived; this witness specifically requires the duplicate finding even when another error remains.

## Commands and finite execution

Working directory:

```text
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/FMutSchema
```

The same detector was run once per state; the phase argument changes only the evidence destination:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/FMutSchema/temp python3 -B detector.py pristine
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/FMutSchema/temp python3 -B detector.py mutated
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/FMutSchema/temp python3 -B detector.py restored
```

Within each immutable state, two independent commands ran concurrently, each with a30-second bound:

```text
/usr/bin/python3 -B <scratch>/lane/plans/benchmark_spec_audit.py --root <scratch>/lane --selftest
/usr/bin/python3 -B <scratch>/witness.py
```

Here `<scratch>` is the absolute working directory above. Capture JSON retains the full literal argument lists, stdout, stderr, return codes and hashes. Those command lists and detector/witness/specification hashes are identical across all three phases. No timeout or unrelated setup failure occurred. No general build/lint/full acceptance suite or additional production CLI census was run.

## Actual output and verdict

| State | Stock selftest exit/output | Independent witness exit/output | Combined detector exit |
|---|---|---|---:|
| Pristine | 0; `SELFTEST clean cases=21 ...` | 0; `matched: true`; exact duplicate and population-size findings | 0 |
| Mutated | 1; named `duplicate_and_missing_ids` assertion below | 1; `matched: false`; only the population-size finding remains | 1 |
| Restored | 0; same complete21-case output as pristine | 0; `matched: true`; identical stdout to pristine | 0 |

The mutant's stock assertion is exactly:

```text
AssertionError: ('duplicate_and_missing_ids', {'missing_task_id'}, ['duplicate_task_id', 'missing_task_id'])
```

Thus stock failure occurs at the assigned duplicate-ID expectation, after earlier stock cases including `unknown_evaluator`, not from syntax, fixtures, snapshot corruption, import, or setup trouble.

The independent mutant's actual finding list is exactly:

```json
[{"actual": 3, "expected": 2, "id": "population_size"}]
```

The only expected finding absent from that projection is:

```json
{"id": "duplicate_task_id", "task_ids": [1]}
```

The mutant still returns `duplicate_task_ids=[1]`, `missing_task_ids=[]`, `unexpected_task_ids=[]`, `task_count=3`, `distinct_task_ids=2`. Both detectors therefore kill the **specific suppressed finding**, even though other duplicate-related information and other error reporting remain. This is not credit for an unrelated generic red exit.

**Mutation verdict: KILLED.** Pristine and restored detectors are green; the mutant is red for its stable expected finding mismatch. No survivor or inconclusive outcome occurred in this single assigned probe. Unknown-evaluator suppression was not separately mutated; no mutation-coverage claim for that branch is made.

## Before/after hashes and exact restoration

SHA-256 of `plans/benchmark_spec_audit.py` in each state:

| Bytes | SHA-256 |
|---|---|
| Production / saved pristine / scratch pristine | `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8` |
| Scratch mutant / retained mutant specimen | `68191cdd86d2ab9e39c1b3e8ef9de7970a2a418b4eb65ee88166b6ddeb0c130a` |
| Scratch restored | `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8` |

After the expected failed detector, the one original tuple entry was restored before the final detector. `restoration.json` records actual byte comparisons, not hashes alone:

- `restored_bytes_equal_backup: true`
- `restored_bytes_equal_production: true`
- `mutant_bytes_equal_expected_one_expression_deletion: true`
- `pristine_equals_restored_outputs: true`
- `same_commands_all_phases: true`
- `same_detector_and_witness_all_phases: true`
- `production_all_eight_input_hashes_unchanged: true`
- `scratch_seven_fixture_hashes_equal_production_all_phases: true`
- `scratch_inputs_unchanged_during_each_probe: true`
- `no_timeouts: true`
- No `__pycache__` directories or remaining private temporary entries.

The eight tracked production inputs are the instrument plus the seven copied fixture files: scorer-contract expectation, manifest, selected IDs, LICENSE, raw task JSON, evaluator source, and helper source. Their exact before/after digest maps are in every phase capture; this is a bounded input-preservation claim, not a whole-repository comparison during concurrent author work.

## Durable evidence

All paths below are under `.ufo/waves/round-28/scratch/FMutSchema/`:

- `duplicate-witness.json` — independent hand-derived fixture and expected projection.
- `witness.py`, `detector.py` — exact assigned detector and finite capture runner.
- `benchmark_spec_audit.pristine.py` — saved original bytes.
- `benchmark_spec_audit.mutant.py` — retained mutant specimen; not used as the restored active instrument.
- `lane/plans/benchmark_spec_audit.py` — restored exact active scratch bytes.
- `pristine/capture.json`, `mutated/capture.json`, `restored/capture.json` — complete command/output/exit/hash receipts.
- Each phase also retains `stock-selftest.stdout`, `stock-selftest.stderr`, `stock-selftest.exit.txt`, `independent-witness.stdout`, `independent-witness.stderr`, and `independent-witness.exit.txt`.
- `restoration.json` — cross-state comparison of captured evidence and exact restored/specimen bytes; it does not rerun the detectors.

Existing runtime: Python3.14.8 at `/usr/bin/python3`. Tool installs/updates: **none**.

No production repair is proposed or applied. L1 owns any integration or broader interpretation. This report establishes only that the delivered stock selftest rejects this particular duplicate-finding omission, with independently grounded red-before/green-restored evidence.
