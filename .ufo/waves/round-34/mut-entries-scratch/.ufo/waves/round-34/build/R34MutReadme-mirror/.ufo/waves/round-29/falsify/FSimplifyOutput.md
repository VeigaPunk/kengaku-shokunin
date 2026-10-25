writer: KengakuR29-2.FSimplifyOutput-2

# FSimplifyOutput — `--json` duplication and minimal contract-preserving cut

**Attack:** Falsify the hypothesis that the integrated `--json` stream is already near-minimal for `plans/round-29-claims.md` C1. Measure byte ownership, test claimed redundancies (profile metadata, occurrence vs leaf witnesses, `projected_task` vs `changed_leaves`), map fields to prereg lines 62–71, and size a cut that preserves oracle-comparable semantics.

**Production source read:** yes — `plans/config_projection.py` (for field provenance only; sizes recomputed from stdout capture).

**Tool installs:** none (python3 stdlib only).

## Godspeed axes

| Axis | This review |
|------|-------------|
| **A — stdout weight** | Shrink avoidable duplication without dropping required witnesses. |
| **B — contract fidelity** | Keep 2436 full `projected_task` objects, occurrence codepoint provenance, separate unit counts. |
| **C — boring implementability** | Prefer hoisting identical subtrees over new encodings. |
| **D — unit clarity** | Do not merge occurrence (1435), changed-leaf (1416), task (812), projection (2436) denominators. |
| **E — source vs runtime** | No implication that smaller JSON weakens pinned-input or synthetic-profile semantics. |

## Evidence (executed)

| Observation | Command | Result |
|-------------|---------|--------|
| JSON byte length | `python3 plans/config_projection.py --json \| wc -c` | **3881050** bytes (~3.88 MiB) |
| Build receipt digest | `corpus/evidence/round29-calibration/build-json-sha256.txt` | **c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630** (matches scratch capture) |
| Summary size | `--summary \| wc -c` | **6914** bytes |
| Top-level key sizes (programmatic `json.dumps` compact) | scratch analyzer on captured stdout | `profiles` **3622843**; `occurrence_provenance` **254746**; remainder **<2 KiB** each |
| Per-profile `tasks[]` share | same | **~1.20–1.22 MiB** each (dominant) |
| Exit / findings | `--json` | exit **0**, `findings` **[]** |

Top-level keys (sorted): `findings`, `index_mapping`, `inputs`, `limitations`, `manifest_sha256`, `occurrence_provenance`, `population`, `profiles`, `raw_text_sha256`, `source_contract`, `upstream_revision`.

Per-task record keys (`profiles.*.tasks[0]`): `changed_leaves`, `index_equals_task_id`, `output_filename`, `output_index`, `projected_task`, `task_id`, `would_be_file_sha256`.

## Byte ownership (one profile: `distinct_origins`)

| Field (aggregated over 812 tasks) | Bytes (compact JSON) |
|-----------------------------------|----------------------|
| `projected_task` | 678041 |
| `changed_leaves` | 332628 |
| `would_be_file_sha256` | 53592 |
| `output_filename` + `output_index` + `task_id` + `index_equals_task_id` | ~28266 |

Across three profiles, **`projected_task` + `changed_leaves` ≈ 93%** of total stdout.

## Redundancy tests (mismatch = falsification of “safe to drop”)

| Claim tested | Method | Mismatch |
|--------------|--------|----------|
| `changed_leaves[].projected` agrees with `projected_task` at `json_pointer` | walk 2436×1416 leaves | **0** |
| `category` derivable from `path_template` vs `URL_FIELD_TEMPLATES` | all leaves | **0** |
| `tokens` derivable as env-token substring of `original` | all leaves | **0** |
| `changed_leaves` static columns identical across profiles for same `output_index` | compare `json_pointer`, `path_template`, `original`, `tokens` on indices 0, 44, 100 | **0** |
| Profile-level census blocks identical on all three profiles | byte-equal compare | **0** for 13 keys (see below) |
| `population.tasks_with_token` derivable from `occurrence_provenance` | re-aggregate | **0** (key order only differs) |
| `occurrence_provenance` redundant with `changed_leaves.tokens` | unit counts 1435 vs 1416; offsets only in former | **Not redundant** — different units (prereg L68, L71) |

**Identical triplicated profile keys** (safe to hoist once): `changed_leaf_count`, `changed_leaves_by_category`, `changed_leaves_by_path_template`, `changed_leaves_by_token`, `changed_leaves_with_multiple_occurrences`, `changed_task_count`, `changed_tasks_by_token`, `parsed_task_count`, `purpose`, `remaining_known_tokens_decoded`, `remaining_known_tokens_text`, `steps`, `string_leaf_count` — **1140** bytes×2 avoidable (~0.03% of total; counts identical because replacement *counts* do not depend on profile *values* on this population).

**Not redundant across profiles:** `values`, `projected_text_sha256`, `stimulus_class`, `stimulus_observations`, every `projected_task`, every `changed_leaves[].projected`.

**`steps[].token` vs `name`:** always `token == "__{name}__"` — derivable; **0** mismatches.

## Prereg-required vs optional in current `--json`

Source: `plans/round-29-claims.md` L62–71, L51–55.

| Required by prereg | Present in `--json` |
|--------------------|---------------------|
| 812 / distinct IDs / 3 profiles / 2436 projections | `population.*` |
| Per-profile replacement counts, projection digest, parsed count, changed-leaf rollups, remaining placeholders | `profiles.*.steps`, `projected_text_sha256`, rollups, `remaining_known_tokens_*` |
| Per task/profile: `task_id`, output ordinal, filename, full `projected_task`, changed paths + original/projected | `tasks[]` (all fields) |
| Occurrence provenance with **Unicode codepoint** offsets | `occurrence_provenance[]` |
| index vs task_id on frozen input + shuffled witness | `index_mapping`; witness in `--selftest` / hand fixtures, not full JSON |
| Separate occurrence / leaf / task units | `population`, profile rollups, `occurrence_provenance` vs `changed_leaves` |
| Pin witnesses | `inputs`, `manifest_sha256`, `raw_text_sha256`, `source_contract` |
| Scope / limitations in output | `limitations` |

| Not named in prereg L62–71 | In `--json` today | Safe cut? |
|---------------------------|-------------------|-----------|
| `would_be_file_sha256` | yes | **Yes** for prereg; **No** if downstream falsify seats compare it (wave spec, not prereg) |
| Per-task `index_equals_task_id` | yes | **Yes** — derivable from `output_index` vs `task_id`; frozen file has 812/812 in `index_mapping` |
| Per-task `output_filename` | yes | **Yes** with documented rule `config_files/{output_index}.json` (already in `source_contract.per_task_filename_template`) |
| Per-leaf `category` | yes | **Yes** — derivable from `path_template` (0 mismatches) |
| Per-leaf `tokens` | yes | **Yes** — derivable from `original` (0 mismatches) |
| `population.tokens_followed_by_slash` | yes | Optional aggregate; not in `--summary` lines |
| Triplicated identical profile census | yes | **Yes** — hoist once |

**Not prereg-safe to drop:** full `projected_task` in `--json` (L79–81: Main compares every per-task object); `occurrence_provenance` (offsets + occurrence-level unit); per-profile `values` (oracle must not re-read production code — values still required in output or via authenticated `inputs` + external `profiles.json` read; hoisting to a single pinned digest is OK, omitting values is not).

## Occurrence vs changed-leaf (attack on “merge these”)

- **`occurrence_provenance`:** 1435 records; fields include `original_input_codepoint_offset`, `string_role`, `task_index`, `token` (sample: offset **42249**, token `__GITLAB__`, pointer `/44/start_url`).
- **Changed leaves:** 1416 per profile; no codepoint offset; carries decoded `original` / `projected` strings.
- Gap **1435 − 1416 = 19** explained by multiple occurrence hits collapsing to one changed leaf (13 leaves with >1 occurrence in rollup; selftest `units_not_pooled` encodes the distinction).

**Verdict on merge:** treating occurrence list as redundant with per-leaf `tokens` **fails** prereg and loses offset/role witnesses.

## Minimal contract-preserving cut (estimated, not implemented)

Hoist shared profile census; hoist one `changed_leaf_skeleton_by_task` (shared `json_pointer`, `path_template`, `original`, `tokens`); per profile retain `values`, digests, `stimulus_*`, and per task retain `output_index`, `task_id`, full `projected_task`, and parallel `changed_leaves_projected[]` only; drop derivable per-task fields above; keep global `occurrence_provenance`, `population`, pins, `index_mapping`, `limitations`, `findings`.

| Schema | Compact JSON bytes (modeled from captured stdout) |
|--------|---------------------------------------------------|
| Actual integrated | **3880542** |
| Modeled minimal cut | **2991202** |
| Savings | **~22.9%** (~889 KiB) |

Remaining bulk is **mandatory**: three full projected task arrays (~2.0 MiB) plus occurrence list (~255 KiB). Aligns with build design note `R29SimplifyOutputSize.md` (~2 MiB expected for 2436 full tasks); delivered **3.88 MiB** because **`changed_leaves` re-embeds changed string values already inside `projected_task`** (~713 KiB duplicated projected strings inside leaves, plus ~239 KiB triplicated static leaf metadata).

Dropping `projected_task` while keeping only `changed_leaves` would violate L66–67 / L79–81 even though leaves alone determine diffs on this population (812/812 tasks have ≥1 changed leaf).

## Relation to build-wave design

`/.ufo/waves/round-29/build/R29SimplifyOutputSize.md` pre-landed the same split (`--summary` slim / `--json` full tasks, no raw812 embed). Integrated instrument matches that shape; extra weight vs the **~2 MiB** design target is mostly **dual storage of changed URL strings**, not raw re-embed (raw only via `raw_text_sha256` + pins).

## Scoped mismatches (instrument vs redundancy hypothesis)

**None** for derivability checks above. **No** incorrect pooling of occurrence vs leaf counts observed in output.

## Tradeoff

A ~23% slimmer JSON requires oracle/Main to accept hoisted skeleton + documented filename rule + dropped `would_be_file_sha256`. Prereg C1 unchanged; wave-local falsify items that hash `projected_task` with indent=2 would need to recompute that hash locally.

VERDICT: PASS
