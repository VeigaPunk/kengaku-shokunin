# FContractPopulationPin — falsification of manifest/selection/source identity pin

Seat: KengakuR28.FContractPopulationPin (critic, author-side, read-only over production).
Candidate examined as context: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (frozen). Canonical candidate
path `corpus/knowledge/webarena-task-spec-audit.md` is not admitted and was not read as authority.
Instrument under attack: `plans/benchmark_spec_audit.py` (316 lines), `read_snapshot`/`main`/`audit_tasks`/`scorer_contract`.
Contract clause attacked: round-28-claims.md:15, "Verify snapshot sha256 values against persisted manifest
before calculating anything; missing/tampered input → exit2 stable `snapshot_tampered`/`input_missing` finding."

## Pinned identity (observed, `sha256sum`, production read-only)

| file | observed sha256 | pin location |
|---|---|---|
| manifest.json | c78b1478…a6dd | code constant `MANIFEST_SHA256` |
| selected-task-ids.json | 5f7eea2e…d17a | code constant `SELECTION_SHA256` |
| config_files/test.raw.json | 7b50386f…7652 | manifest |
| evaluation_harness/evaluators.py | e23edb39…0c22 | manifest |
| evaluation_harness/helper_functions.py | ec758da4…e275 | manifest |
| LICENSE | c71d239d…0ab4 | manifest |

All six match. The pinned JSON and Python sources contain 0 non-ASCII bytes, so locale-dependent
`read_text()` decoding cannot change the parse (host Python 3.14.8, UTF-8 preferred encoding).

## Probes (scratch only)

Script: `.ufo/waves/round-28/scratch/FContractPopulationPin/probe.py`; captured output:
`.ufo/waves/round-28/scratch/FContractPopulationPin/probe-output.json`. Each probe copies the fixture
into a fresh temp root under that scratch directory, runs with `python3 -B` and bytecode disabled, and
removes the temp roots afterwards. No upstream code was imported or executed: `evaluators.py` is only
`ast.parse`d by the lane tool. No full selftest or acceptance rerun.

### Static rebinding and missing/non-object inputs: hypothesis survives

CLI `python3 -B plans/benchmark_spec_audit.py --root <scratch-root> --json`:

| probe | exit | finding | inventory emitted |
|---|---|---|---|
| P0 unmodified copy | 0 | none | yes |
| P1 manifest missing | 2 | input_missing | no |
| P2 manifest replaced by `[]` (non-object) | 2 | manifest_tampered | no |
| P3 manifest is a directory | 2 | input_invalid | no |
| P4 selection missing | 2 | input_missing | no |
| P5 selection replaced by `{}` | 2 | selection_tampered | no |
| P6 population replaced by `{}` (non-list) | 2 | snapshot_tampered | no |
| P7 population replaced by `[]` | 2 | snapshot_tampered | no |
| P8 coherent rebind: population truncated to 16 tasks, manifest sha rewritten to match, selection rewritten to `[0..15]` | 2 | manifest_tampered | no |

The manifest and selection digests are code constants, and the manifest pins every consumed source.
So no file-only edit can coherently rebind manifest, selection and population together (P8). Rebinding
requires editing the instrument itself, which is outside a fixture-level attack. Missing and non-object
manifest, selection and population all exit 2 with a stable finding and emit no inventory.

### Counterexample: verified bytes are not the audited bytes

`read_snapshot` hashes each manifest file with `read_bytes()` (lines 188–191), then discards those bytes
and re-opens the files:

- `test.raw.json`: once more, `read_text()` at line 194;
- `evaluators.py`: twice more, at lines 200 and 205;
- `helper_functions.py`: once more, at line 200.

The manifest (line 184) and selection (line 192) are each read once and parsed from the verified bytes.
That is the correct pattern, and it is not applied to the three sources.

R-probes import the lane tool as a module in scratch and simulate a writer that replaces one file
immediately after its hash read. This is an explicitly assigned miniature function probe; it monkeypatches
`Path.read_bytes` in-process only. The outcome is mapped exactly as `main()` maps it.

| probe (replacement written after hashing) | observed outcome | provenance in output |
|---|---|---|
| R1 population → `{}` | exit 2 `input_invalid`, detail `'selected_task_ids'` (a KeyError), not a stable finding id | none |
| R2 population → `[1, 2, 3]` | **exit 1**, findings task_not_object×3, missing_task_id, population_size, selection_mismatch; **inventory emitted** with task_count=3 | **claims `source_sha256` 7b50386f…7652 and upstream_revision dce04686**; the bytes actually audited are a36b1f2c…07f3 |
| R3 population → first 400 tasks | **exit 1**, missing_task_id, population_size, selection_mismatch; **inventory emitted** with task_count=400 | **claims pinned 7b50386f…7652**; the bytes actually audited are 8c7ee260…0bc9 |
| R4 evaluators.py → `x = 1\n` | **uncaught `StopIteration`** from `next(...)` without a default at line 166; it is not in `main()`'s except tuple (line 299), so the CLI would print a traceback and exit 1, which the contract reserves for "failed finding" | n/a |
| R5 control: selection → `[]` | exit 0, no findings, task_count=812 (the verified in-memory bytes were used) | correct |
| R6 control: manifest → `[]` | exit 0, no findings, task_count=812 (the verified in-memory bytes were used) | correct |

For R5 and R6, the `bytes_actually_audited_sha256` field in the probe output is the on-disk file after the
swap. Those runs did not parse that file; they parsed the verified bytes. The field only means "audited
bytes" for R1–R4.

Impact:

- **False provenance.** R2 and R3 emit an inventory labelled with the pinned digest and revision for bytes
  that were never verified. This violates "verify … before calculating anything" and the candidate's
  decision rule 1, "Freeze … raw task bytes … and persisted digests" (draft line 123).
- **Unstable finding and exit class.** A non-list population under the race gives `input_invalid` with a
  KeyError detail (R1). That happens because the `tasks_not_list` early return (line 43) omits
  `selected_task_ids`, so its own stable finding id never surfaces. A swapped scorer crashes into the
  exit 1 class (R4).
- **Reachability is narrow.** The race needs a concurrent writer to the fixture during one run. The
  delivered measurements (812 / 27 / 651, selftest 21) are not contradicted. This is a fixable instrument
  defect in the identity boundary, not a benchmark observation and not a judge-level tradeoff.

Impacted axes: canonical coverage/constructs7 (C1 provenance of the measured inventory). No C2 (calibration8)
impact: `registry_check.py` was out of scope and was not probed.

## Smallest safe correction (not applied; L1 resolves)

In `read_snapshot`, keep the bytes that were verified and parse only those:

```python
verified = {}
for relative, expected in manifest["files"].items():
    data = (fixture / relative).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected["sha256"]:
        return {"findings": [{"id": "snapshot_tampered", "path": relative}], "limitations": LIMITS}, 2
    verified[relative] = data
...
result = audit_tasks(json.loads(verified["config_files/test.raw.json"]))
...
tree = ast.parse(verified[relative].decode("utf-8"))
...
result["scorer_contract"] = scorer_contract(verified["evaluation_harness/evaluators.py"].decode("utf-8"))
```

Two optional hardenings close the secondary symptoms. Neither is needed once the single read lands,
because pinned bytes cannot reach these paths:

- In `scorer_contract`, use `next(..., None)` for `router` and `comb`, and fold `None` into the existing
  `ValueError("scorer_contract_unrecognized")`.
- In `audit_tasks`'s `tasks_not_list` return, include `"selected_task_ids": []`.

A matching selftest case is `scorer_contract("x = 1\n")` raising `scorer_contract_unrecognized`. No
production patch was made.

## Tool installs

None. Only the existing stdlib `python3` 3.14.8 and coreutils were used. RULES.md was not needed.

VERDICT: PARTIAL. Static manifest+selection+population rebinding is refused, and missing or non-object
manifest, selection and population all exit 2 with a stable finding (P1–P8). But hashed bytes are re-read
before auditing, so unverified population bytes can be inventoried under the pinned digest (R2, R3), and a
swapped scorer escapes as an uncaught exit 1 (R4).

---

## Amendment v2: independent re-probe of the repaired instrument (2026-10-21; v1 above preserved verbatim)

The v1 report's SHA256 before this append was
`9b15a3e270a9be24d4a3535cb647c878470eb2d94abc5696d42ecfa05f7d463c`.

Code under test:

- `plans/benchmark_spec_audit.py` (433 lines), SHA256
  `b7524c2f316f5ba850bd901c932811ca55cd4adff264242488f3842def5cca36`.
- This equals `instrument_sha256` in `.ufo/waves/round-28/candidate-freeze-v2.json` (file SHA256
  `7bfa6b5b013acbb5828dcfc6147e1e2eb0006e05e481520d3c833a3ac58dd259`).
- The candidate draft at the frozen path was not re-read for this amendment. Only the instrument was
  re-probed.
- Production files stayed read-only. I did not run the author's selftest (67 cases) or the acceptance
  suite. I also did not take the author's report of exit 0 as evidence.

Repair, read statically (lines 195–222):

- `read_snapshot` stores each hashed source's bytes in `verified[relative]`.
- `audit_tasks(json.loads(verified["config_files/test.raw.json"]))`, the `ast.parse(verified[relative])`
  anchor pass and `scorer_contract(verified["evaluation_harness/evaluators.py"])` read no file a second
  time.
- There is no `read_text()` left on the `read_snapshot` path. `ast.parse` and `json.loads` take bytes
  directly (PEP 263 UTF-8 default; JSON UTF detection), and the pinned sources are pure ASCII.
- `scorer_contract` now uses `next(..., None)` for both `router` and `comb`, which raises
  `ValueError("scorer_contract_unrecognized")` (lines 175–187).
- The `tasks_not_list` return (line 45) now carries `selected_task_ids` and the other id lists.

### Rerun 1: unchanged v1 probe

Script: `probe.py`, SHA256 `dc383f5a59104e56a20b7c88bf9f0dfacf98218a621537bd9f008b79b413fdcf`, the same
file as v1.

- Output: `probe-output-v2.json`, SHA256
  `f4fc726fdede56edd9c8010b14907f8552bb7c25af80a426028a03778d77eced`.
- The v1 output `probe-output.json` (SHA256
  `a7e222b70bbed3d60961e46c90837587beb5cab0d3546ec34890517362337dec`) is kept unchanged.
- P0–P8 match v1 exactly: P0 exits 0; P1–P8 each exit 2 with `input_missing`, `manifest_tampered`,
  `input_invalid`, `input_missing`, `selection_tampered`, `snapshot_tampered`, `snapshot_tampered` and
  `manifest_tampered`; none emits an inventory.
- R1–R4 (population swapped to `{}`, to `[1, 2, 3]` or to its first 400 tasks; `evaluators.py` swapped to
  `x = 1`) now all exit 0, with no findings and task_count=812. There is no KeyError, no exit 1 inventory
  and no uncaught `StopIteration`.
- The probe's `bytes_actually_audited_sha256` field now shows only the swapped bytes left on disk; the
  next probe shows those bytes are no longer audited.

### Rerun 2: new equivalence probe

Script: `probe_v2_equivalence.py`, SHA256
`2ffc286ce45643c5731e9cf9d292355ae6e1760a025a70bb03fd5985d956dd31`. Output: `probe-v2-equivalence.json`,
SHA256 `94e8aed4e855285adb19e7be1643b1d4f804485d0dae7a60ddcef02a1da58f85`.

Hand-derived expectations for a correct repair:

1. Each raced `read_snapshot` result equals the unraced result on every field.
2. Each raced target is read exactly once.
3. The bytes left on disk differ from the reported `source_sha256`.

Observed:

| raced target (replacement written after its first and only read) | exit | result identical to unraced | reads of target | disk now differs |
|---|---|---|---|---|
| population → `{}` | 0 | true | 1 | true |
| population → `[1, 2, 3]` | 0 | true | 1 | true |
| population → first 400 tasks | 0 | true | 1 | true |
| evaluators.py → `x = 1` | 0 | true | 1 | true |
| helper_functions.py → a different function | 0 | true | 1 | true |

- Unraced run: exit 0. Every row has the same canonical result SHA256,
  `a0e1b786fd5a723d6afdb64884fd977ca064d5523b7987712b3ba828eecd12f9`.
- `scorer_contract("x = 1\n")` raises `ValueError: scorer_contract_unrecognized`.
- A source with a valid router but no `EvaluatorComb` also raises `ValueError: scorer_contract_unrecognized`.
- `audit_tasks({})` gives findings `[tasks_not_list]` and includes the `selected_task_ids` key.

Conclusion:

- The audited bytes are now exactly the authenticated bytes for every manifest-pinned source.
- The pinned manifest, selection and population still cannot be coherently rebound by fixture edits.
- Missing, non-object and tampered inputs still exit 2 with stable findings.
- The secondary symptoms of v1 (the KeyError detail and the uncaught `StopIteration`) are closed.

Residual, not a defect: P3 (a directory in place of the manifest) gives `input_invalid` rather than
`input_missing`. That is a stable exit 2 and consistent with the contract.

Tool installs for v2: none. I used only stdlib `python3` 3.14.8 and coreutils.

VERDICT (v2, repaired instrument b7524c2f…ca36): PASS. The v1 PARTIAL stands for the instrument it tested.
