# FContractTaskSchema — task-shape contract falsification (author-side, round28)

Seat: KengakuR28.FContractTaskSchema (critic, leaf). Author-side evidence only, not outside non-author evidence.
Scope: malformed task shapes in `plans/benchmark_spec_audit.py` — non-object task, invalid/bool ID,
missing/null sites/intent/eval, missing/mistyped flags. The question is whether each one produces a stable
non-clean result rather than a crash or a silent exclusion.

## Pinned identities (re-read 2026-10-21)

| artifact | SHA256 |
|---|---|
| candidate draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` (canonical target `corpus/knowledge/webarena-task-spec-audit.md`, not admitted) | 77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8 |
| `plans/benchmark_spec_audit.py` | f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8 |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` (upstream dce04686) | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |

Production files were only read. No `benchmark_spec_audit` bytecode was written under `plans/__pycache__`
(checked afterwards). No upstream code was imported or executed. The upstream `evaluators.py` was only grepped
as data for field accessors (lines 137, 161, 213, 215, 258, 361). No installs or updates; I used the existing
Python 3.14.8. Scratch: `.ufo/waves/round-28/scratch/FContractTaskSchema/`.

## 1. Independent census of the pinned input (derived before any production import)

`census.py` uses `object_pairs_hook` duplicate-key detection and rejects NaN/Infinity via `parse_constant`.
It does not import production or oracle code. Output is in `census.out.json`:

- The top level is a list of 812 objects.
- `task_id` is an `int` in all 812 tasks, and the sorted IDs are exactly 0–811.
- There are 0 duplicate JSON keys anywhere and no non-standard constants.
- sites are OK in 812 tasks, intent is a non-blank string in 812, eval is a dict in 812, and eval_types is a
  non-empty string list in 812.
- `require_login` is bool `True` in all 812 tasks and `require_reset` is bool `False` in all 812.

**Result:** every task-shape failure branch is latent on the pinned bytes. The candidate's
"812/812, IDs 0–811, schema findings 0" is reproduced. A re-pinned scratch control printed
`TOTAL task_count=812 distinct_task_ids=812 site_eval_strata=27 selected_count=16 program_html_targets=651
findings=0 exit=0`, byte-identical to the TOTAL line of `corpus/evidence/round28-calibration/audit-summary.txt`.

Side observation (data only): task 723 has an extra top-level `string_note` beside `eval.string_note`. The scorer
reads only `configs["eval"]["string_note"]` (evaluators.py:161), so this is not a defect.

## 2. Function-level probes: 43 hand-expected cases (`probe.py`, `probe.out.txt`)

Result: `crashes 0 id_mismatch 0 record_mismatch 0 cases 43`. For every probe, the set of finding IDs equals the
hand-derived set:

- **Non-object task** (int, null, list): `task_not_object` + `missing_task_id`.
- **Invalid task ID** (`true`, `false`, `"0"`, `0.0`, `null`, absent): `task_id_invalid` + `missing_task_id`.
  Negative IDs or 812 give `unexpected_task_id`.
- **Sites, intent, eval_types** (missing, null, empty or blank, scalar, bool member): `sites_invalid`,
  `intent_invalid` or `eval_types_invalid` respectively.
- **Eval** (missing, null, list): `eval_not_object` + `eval_types_invalid`.
- **Flags** (missing, null, `"true"`, `1`, `0`, `"False"`): `flag_invalid` with the flag name.
- **Empty object `{}`**: all seven task-level IDs plus `missing_task_id`.

Every malformed dict task keeps a per-task record with `schema_status: FAILED`.

## 3. CLI-level probes on re-pinned scratch roots (`cli_probe.py`, `cli_probe.out.txt`)

The stock CLI cannot reach schema findings on any non-pinned bytes: `MANIFEST_SHA256` is a code constant, so
changed bytes produce `snapshot_tampered`/`manifest_tampered` with exit 2. To reach the exit-1 path, I copied the
fixture and script into scratch, re-hashed the manifest, and replaced only the constant. That gate is a
deliberate design tradeoff for a fixed pinned audit, not a defect.

| case (one change to the full 812 population) | `--json` / `--summary` exit | findings | per-task records |
|---|---|---|---|
| re-pinned control | 0 / 0 | none | 812 |
| task0 → `0` (non-object) | 1 / 1 | task_not_object, missing_task_id | **811** |
| task0 id `true` | 1 / 1 | task_id_invalid, missing_task_id | 812 |
| task0 id missing | 1 / 1 | task_id_invalid, missing_task_id | 812 |
| task0 sites null | 1 / 1 | sites_invalid | 812 |
| task0 intent missing | 1 / 1 | intent_invalid | 812 |
| task0 eval null | 1 / 1 | eval_not_object, eval_types_invalid | 812 |
| task0 require_login missing | 1 / 1 | flag_invalid(require_login) | 812 |
| task0 require_reset `"false"` | 1 / 1 | flag_invalid(require_reset) | 812 |
| top level `{"tasks": [...]}` | **2 / 2** | **input_invalid, detail `'selected_task_ids'`** | 0 |
| top level `null` | **2 / 2** | **input_invalid, detail `'selected_task_ids'`** | 0 |
| duplicate key `"task_id": 811, "task_id": 0` | 0 / 0 | none | 812 |

There were no tracebacks and stderr was empty in every case.

## Findings

**F1 — The `tasks_not_list` finding is masked by an internal KeyError (latent, fixable defect).**
- Cause: `audit_tasks` returns only `findings`/`tasks`/`metrics` for a non-list top level. `read_snapshot` then
  evaluates `result["selected_task_ids"]`, raising a KeyError. `main` catches it and emits
  `input_invalid` with detail `'selected_task_ids'`.
- Effect: the exit (2) is stable and non-clean, but the named finding is discarded and replaced by an
  implementation key name. This contradicts claims line 17 ("malformed task shapes are instrument findings")
  and the contract's split between instrument defects and observations.
- Impacted axes: coverage/constructs (diagnostic identity).
- Smallest safe repair: make the early return keep the full result shape:
  `return {"findings": [{"id": "tasks_not_list"}], "tasks": [], "metrics": {}, "selected_task_ids": [], "duplicate_task_ids": [], "missing_task_ids": [], "unexpected_task_ids": []}`.
  The run then exits non-clean with `tasks_not_list` first. If L1 prefers exit 2 (could-not-evaluate),
  `read_snapshot` should return 2 explicitly on that ID instead of relying on a caught KeyError.

**F2 — The stock selftest guards none of the assigned task-shape branches (fixable, regression-guard gap).**
- Test: seven scratch mutants (`mutants.py`, `mutants.out.txt`). Each one passes the stock `--selftest`
  (exit 0, `SELFTEST clean cases=21`). My probes catch every one, comparing the mutant's findings with
  production's on the same input:
  - M1 `type(tid) is not int` → `isinstance(tid, int)`. On the full pinned population with `task[1].task_id = true`,
    production reports `{missing_task_id, task_id_invalid}`; the mutant reports `{}`, i.e. exit 0 with silent
    acceptance. Python treats `True == 1`, so the duplicate/missing accounting cannot catch it.
  - M2 deleting `task_not_object`: `{population_size, task_not_object}` → `{population_size}`.
  - M3 sites, M4 intent, M6 missing flag accepted, M7 empty eval_types accepted: each named finding → `{}` (silent).
  - M5 deleting `eval_not_object`: the named ID is lost and only `eval_types_invalid` remains.
- Why it matters: the selftest's 21 cases cover only `typed_flag` (a string flag) at task level. The candidate's
  `recheck` is `--summary and --selftest`, and the pinned bytes exercise no task-shape branch (section 1). A
  regression would therefore pass the candidate's own recheck while violating its falsifier "a task/evaluator is
  silently excluded".
- Impacted axes: coverage/constructs, calibration.
- Smallest safe repair: add eight `probe(...)` lines using the existing `miniature`/`probe` helpers:
  - `miniature + [7]` → `[task_not_object, population_size]`
  - `miniature*2` with the second `task_id=True` and size 2 → `[task_id_invalid, missing_task_id]`
  - `sites=None` → `[sites_invalid]`
  - intent removed → `[intent_invalid]`
  - `eval=None` → `[eval_not_object, eval_types_invalid]`
  - `eval_types=[]` → `[eval_types_invalid]`
  - `require_login` removed → `[flag_invalid]`
  - top-level `{}` → `[tasks_not_list]`, plus an assertion on the key shape (this case covers F1)
- Identity change: the selftest count moves from 21 to 29, so the candidate text "selftest21" and its receipts
  change. L1 must request same-identity rereads.

**F3 — A non-object task's raw value is absent from the per-task output (low severity).**
- The run is not silent: the finding is emitted and the exit is 1. But `tasks` has 811 records, and the finding
  carries only `task_position` with detail `""`. The raw value and its type are lost, which touches the
  candidate's falsifier "a raw task field is lost in the per-task output".
- Smallest repair: `fail("task_not_object", type(task).__name__)`, plus a record
  `{"task_position": position, "raw_task": task, "schema_status": "FAILED"}` before `continue`.

**F4 — Flag histograms merge invalid values with valid ones (low severity, failing runs only).**
- `counts[key][str(value).lower()]` puts the string `"false"` or `"False"` in the same `false` bucket as bool
  `False`. Example: `reset_str_False` → `reset_flags {"false": 1}` alongside `flag_invalid`.
- No clean run is affected, and the candidate publishes no flag histogram.
- Smallest repair: key the counter by `json.dumps(value)`.

## Non-findings (counterexamples tested and rejected)

- **Duplicate keys:** JSON last-wins merging silently shadows `"task_id": 811` (exit 0). This matches the
  consumer, since upstream also loads with `json`, and the pinned bytes have 0 duplicate keys. Not a defect for a
  fixed pinned audit.
- **Bool members:** bool members in sites and eval_types are rejected, and an `int`-typed `True` ID is rejected in
  production.
- **Crashes:** no crash in any of the 43 function probes or 12 CLI probes, and no silent exclusion in production
  for the assigned classes.

## VERDICT: PARTIAL

The candidate's measured task-shape claims hold on the pinned bytes: 812/812, IDs 0–811, and 0 schema findings,
reproduced by an independent census. Production gives stable non-clean results for every malformed task class
assigned to me. Two fixable defects remain:

- F1: a non-list top level emits an internal-key `input_invalid` instead of `tasks_not_list`.
- F2: none of the task-shape guards is protected by the selftest or the candidate's recheck. Mutant M1 reaches
  silent exit 0 on the full pinned population.

F3 and F4 are low-severity disclosures. I made no production edits; L1 resolves. Checks for L1 to run after any
repair: `--selftest` (expected 29 cases) and `--summary`, then a re-hash of the candidate.

---

## Repair re-probe v2 (2026-10-21, requested by KengakuR28; v1 above preserved unchanged)

Re-hashed identities:

| artifact | SHA256 |
|---|---|
| `plans/benchmark_spec_audit.py` (current, uncommitted working tree on top of 18b1922) | b7524c2f316f5ba850bd901c932811ca55cd4adff264242488f3842def5cca36 |
| draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | 3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182 |
| `test.raw.json` (unchanged) | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |

This is a bounded re-probe of my own control set only. I did not run the production suite. Production stayed
read-only: its hash was unchanged after probing and no `benchmark_spec_audit` bytecode was written. No installs.
The v1 outputs are archived under `scratch/FContractTaskSchema/v1/`. The v2 outputs are `probe.v2.out.txt`,
`cli_probe.v2.out.txt`, `mutants.v2.out.txt` and `repair_check/`.

Expectation change, as KengakuR28 requested: non-object tasks are now declared to be retained losslessly, so the
`task_int`, `task_null` and `task_list` probes expect 1 per-task record instead of 0. All other hand expectations
are the same as v1.

### Results

- **Function probes:** `crashes 0 id_mismatch 0 record_mismatch 0 cases 43`. Each non-object record keeps
  `raw_task` equal to the input, and the finding detail is `int`/`NoneType`/`list`. A non-list top level now
  returns all seven result keys with `selected_task_ids: []`. Invalid flag values are labelled:
  `invalid:"False"`, `invalid:null`.
- **CLI probes** (re-pinned scratch copies):
  - The unmodified control is byte-identical to v1: `findings=0 exit=0`, 812 records.
  - Top-level object and `null` now exit **1/1** with `[tasks_not_list, selection_mismatch]` and no traceback
    (v1: exit 2 with `input_invalid` `'selected_task_ids'`).
  - Replacing task 0 with an int now exits 1 with detail `int` and keeps **812** records (v1: 811).
  - Every other v1 row gives the same exits and finding IDs.
- **Mutants against the current bytes:** M0, the identity copy, passes the stock selftest with **67 cases**,
  matching the claim. Results:

| mutant | stock selftest | my probe |
|---|---|---|
| M1 bool ID accepted (`isinstance`) | killed (`boolean_id`) | killed (full pinned population → `{}` under mutant) |
| M2 `task_not_object` removed | killed | killed |
| M3 sites unchecked | killed | killed |
| M4 intent unchecked | killed | killed |
| M5 `eval_not_object` removed | killed | killed |
| **M6 missing/null flag accepted** | **survives (67 clean)** | killed (`{}` under mutant) |
| M7 empty eval_types accepted | killed | killed |
| M8 non-list result shape reverted (new repair) | killed (KeyError) | killed |
| M9 non-object record dropped (new repair) | killed (IndexError) | killed |
| **M10 flag buckets merged again (new repair)** | **survives** | killed (`"false"` merged into bool `false`) |
| **M11 non-object type detail dropped (new repair)** | **survives** | killed |

### Disposition of the v1 findings

- **F1 – repaired.** The non-list top level is a stable named finding with exit 1, and the selftest guards it
  (M8).
- **F2 – mostly repaired.** Six of the seven v1 guard mutants are now killed by the stock selftest. Residual:
  M6, inside my assigned "missing flags" scope. The selftest has only the string `"false"` flag case, so a
  regression that accepts a missing or `null` flag would pass the selftest and the candidate's recheck. In that
  case the run exits 0 and the flag is silently recorded as `invalid:null` in the histogram.
- **F3 – repaired** in behaviour (raw value retained, type in the detail). The record is guarded (M9); the type
  detail is not (M11).
- **F4 – repaired** in behaviour, but unguarded (M10).
  - Residual disclosure: an absent flag and an explicit `null` both map to `invalid:null` in the histogram. The
    per-task `raw_task` still distinguishes them, so record-level output is lossless.
  - Low severity; failing runs only.

### Smallest safe repair (verified on a scratch copy only, not applied)

Three selftest edits, with no change to audit logic:

1. Turn `probe("typed_flag", ...)` into `typed = probe(...)` and add
   `assert typed["metrics"]["reset_flags"] == {'invalid:"false"': 1}`.
2. Add `changed = copy.deepcopy(miniature); del changed[0]["require_login"]; probe("missing_flag", changed, ["flag_invalid"])`.
3. Extend the non-object assertion with `and malformed["findings"][0]["detail"] == "int"`.

On a scratch copy of the current bytes, the repaired selftest passes with 68 cases. M6, M10 and M11 each then
fail it (`AssertionError`). Applying this changes the selftest count from 67 to 68, so L1 must re-run
final-acceptance and Amendment2 on the new hash.

### Repair VERDICT: PARTIAL

On the current bytes `b7524c2f…`, the audit's behaviour is correct for every malformed task class I was
assigned: stable non-clean exits, no crashes, no silent exclusions, and non-object tasks retained losslessly. The
selftest guard gap that remains is in assigned scope: a regression accepting missing/null flags (M6) survives the
67-case selftest and the candidate's `--summary`/`--selftest` recheck. M10 and M11 show the same gap for the two
new repairs. The three-line repair above closes all three. This does not falsify any measured count: 812/812,
0 findings and the 67 cases all reproduce. Final-acceptance and Amendment2 hold only for `b7524c2f…`; any repair
needs a new execution on the new hash.
