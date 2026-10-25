# R29SimplifyOutputSize — output-size design review

**Seat / writer:** `KengakuR28.R29SimplifyOutputSize-2` (leaf, read-only)  
**Scope:** C1 generated-config projection observability (`plans/round-29-claims.md`); no production edits, no builds/tests.  
**Primary prereg:** `plans/round-29-claims.md` (read 2026-10-21).  
**Tool installs:** none.

## Godspeed axes (this review)

| Axis | Question |
|------|----------|
| **A — stdout/memory weight** | Avoid re-embedding 880 KiB raw tasks and wave-scale duplicates on every run. |
| **B — contract fidelity** | Preserve read-once pins, 812×3=2436 projections, full per-task projected objects in machine output, oracle-comparable objects. |
| **C — boring implementability** | One loader, two emitters (`--summary` vs `--json`), mirror `benchmark_spec_audit.py` CLI shape. |
| **D — unit clarity** | Keep occurrence / changed-leaf / task / projection denominators separate in summary rollups. |
| **E — source vs runtime** | Fixture digests and synthetic profiles only; never imply deployment or scorer outcomes. |

## Evidence (executed)

| Observation | Command / source | Result |
|-------------|------------------|--------|
| Baseline lacks instrument | `git cat-file -e ed26bdf5…:plans/config_projection.py` | path absent at base |
| Pinned raw812 digest | `sha256sum` on `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386f…`, **880 776** bytes |
| Pinned manifest | same on `plans/fixtures/r29/manifest.json` | `f6390b92…` (matches prereg) |
| Task population | `python3` `json.loads` raw | **812** tasks; one task JSON **643** chars; full array **688 785** chars |
| Naïve triple embed | estimate `688785 × 3` | **~2 066 355** chars if three full projected arrays duplicated flat |
| r28 JSON bloat pattern | `python3 plans/benchmark_spec_audit.py --json \| wc -c` | **1 900 693** bytes stdout |
| r28 summary slim | `… --summary \| wc -c` | **1 505** bytes stdout |
| r28 `raw_task` dominance | programmatic split on 812 records | **51.2%** of per-task JSON bytes are duplicate full `raw_task` blobs; denormalized fields add another ~half per record |

Upstream enumerate-index contract (source-only, inert fixture):

```21:23:plans/fixtures/r29/generate_test_data.py
    for idx, item in enumerate(data):
        with open(f"config_files/{idx}.json", "w") as f:
            json.dump(item, f, indent=2)
```

## Problem statement

Prereg requires **2436** `(task × profile)` projections with **exact projected task objects** and changed-leaf witnesses (`plans/round-29-claims.md` L62–L71). That legitimately produces **~2 MiB** compact JSON if each profile carries 812 full tasks. The avoidable waste is (1) **re-reading** pinned inputs per profile, (2) **re-embedding** the raw812 array or prior-wave artifacts in stdout, and (3) **mirroring r28’s** `raw_task` plus denormalized mirror fields when the contract already names `projected_task` + `changed_leaves`.

## Recommended boring minimal shape

### 1. Read-once input bundle (internal)

Single `load_pinned_inputs(root) -> Inputs` that:

- Reads **once**: `plans/fixtures/r29/manifest.json`, `plans/fixtures/r29/profiles.json`, `plans/fixtures/r29/generate_test_data.py`, `plans/fixtures/r28/webarena/config_files/test.raw.json`.
- Verifies manifest SHA256 **inside the tool** (independent pin, same pattern as prereg L57–L58) before any projection.
- Retains **authenticated bytes** in memory; parses `test.raw.json` **once** to `tasks812: list` for index/ID checks; retains **raw text** `str` (UTF-8 decode of verified bytes) for serialized replacement path.
- Runs AST/source contract check on generator bytes without import/exec.

Per profile loop: `projected_text = apply_six_replaces(raw_text, profile_values)` → `json.loads(projected_text)` → diff leaves vs parsed raw tasks812. **Do not** `read_bytes()` the raw file again; **do not** stash three copies of the 880 KiB raw blob in the result tree—only three projected texts transiently (≤ ~2.6 MiB peak working set, bounded).

### 2. Explicit `--summary` vs `--json` paths (CLI)

Match `plans/benchmark_spec_audit.py` behavior:

| Mode | Emits | Must omit |
|------|-------|-----------|
| **`--summary`** (default when neither flag) | `LIMIT` lines, scope + profile purposes, `FINDING` lines, **aggregate** metrics: 812/812 IDs, profile_count=3, projection_count=2436, per-profile token replacement counts, projection digests, changed-leaf **histograms**, remaining placeholder counts, index==task_id verdict, shuffled-ID witness **reference** (hand-case id, not full 812 rows) | Full `projected_task` objects |
| **`--json`** | Full nested document for oracle/Main compare | Pretty-print optional; **compact** `json.dumps(..., sort_keys=True)` preserves semantics at ~40% smaller than `indent=2` |

Require **exactly one** of `--summary` or `--json` per invocation (or document default `--summary` when both absent—same as r28 audit). **Never** emit 2436 full tasks on summary path.

### 3. JSON document layout (dedupe metadata, not tasks)

```text
inputs          # once: relative paths, sha256 per pinned file, generator replacement_order witness
profiles[]      # 3 entries
  profile_id, purpose, projection_text_sha256, replacement_counts_by_token,
  parsed_task_count, changed_leaf_rollup_by_path, remaining_placeholders,
  occurrence_provenance[]   # Unicode codepoint offsets, named fields
  tasks[]       # 812 entries ONLY under this profile
    task_id, output_index, output_filename,
    projected_task,          # required full object
    changed_leaves[]         # path, category, original, projected
global: projection_count, distinct_task_ids, index_equals_task_id_on_frozen_input,
        shuffled_id_witness, findings[], limitations[]
```

**Per-profile nesting** avoids repeating profile metadata 812 times. **Do not** add `raw_task` or duplicate 812× denormalized r28 audit fields unless prereg later demands them (it does not).

### 4. Changed-leaves vs projected_task (not redundant if bounded)

Prereg requires both. **Do not** propose dropping `projected_task` from `--json` (oracle compares every object, L79–L81). **Do** omit `original_task` embed when every original value already appears in `changed_leaves` **for changed paths only**; unchanged tasks still carry full `projected_task` with `changed_leaves: []`.

### 5. Deletion candidates (for implementer, not executed here)

| Candidate | Rationale | Semantic callers |
|-----------|-----------|-------------------|
| r28-style `raw_task` in projection JSON | Not in r29 required output; doubles size | None required by prereg |
| Embedding full raw812 array in stdout | Digests + pinned paths suffice | None |
| Re-read of fixture files inside profile loop | Violates read-once spirit (L57) | N/A |
| `indent=2` on `--json` | Formatting only | Oracle must compare parsed JSON, not whitespace |

LSP/`references` not run: `plans/config_projection.py` absent from shared tree at review time.

## Out of scope (explicit)

| Proposal | Why out of scope | Contract basis |
|----------|------------------|----------------|
| Streaming/chunked JSON or external sidecar files for 2436 tasks | Would break “stdout only” and complicate oracle byte-compare unless prereg amended | Tool interface L51–L52 |
| Omitting full `projected_task` in `--json` | Oracle/Main must compare every per-task object | L79–L81 |
| Writing `config_files/{idx}.json` | Explicitly forbidden | L51–L52 |
| Deduplicating identical projected tasks across profiles | Profiles differ by construction (three sensitivity fixtures); objects are not identical | Frozen profiles |

## Preserved contract (must not regress)

- Read each pinned input **once**; retain verified bytes; parse only those bytes.
- Counting command `python3 plans/config_projection.py --summary` exposes 812 tasks, 3 profiles, **2436** projections with no hidden exclusions.
- `--json` carries complete per-task/profile projected objects and changed-leaf paths; occurrence offsets are **Unicode codepoints**.
- Distinguish replacement **occurrence**, changed-**leaf**, changed-**task**, and **2436 projection** units in summary output.
- Stdlib-only, read-only, exit 0/1/2 semantics unchanged.
- Synthetic `*.invalid` profiles labeled as controlled fixtures, not deployment.

## Tradeoffs

- **~2 MiB compact `--json`** is **expected and in-contract**; simplification targets **avoidable** duplication (raw re-embed, r28 double storage, summary path bloat), not shrinking required projected objects.
- Peak memory **~3× projected text** during tri-profile pass is acceptable vs disk re-read; alternative single-pass multi-profile replace on one buffer is **not** recommended (violates serialized six-global-replace order per profile semantics).
- Compact JSON slightly harms human `less`; oracle should `json.loads` stdout—human inspection uses `--summary`.

## Unknowns / boundaries

- `plans/config_projection.py` not present in lane shared tree at review time; recommendations target `R29ExecCore` landing per build dispatch.
- Independent oracle output shape not fixed here; production JSON should remain self-contained for Main compare without requiring oracle fields.
- Exact changed-leaf census under quote/backslash JSON-decode failure cases remains oracle-domain bounded (prereg L44–L45); output must surface decode failure as finding, not repair.

## Quote (programmatic word count)

Prereg: “Read each pinned input ONCE, retain authenticated bytes, parse only those bytes.” — **13 words** (`split()`).

VERDICT: PASS

Report: `.ufo/waves/round-29/build/R29SimplifyOutputSize.md`
