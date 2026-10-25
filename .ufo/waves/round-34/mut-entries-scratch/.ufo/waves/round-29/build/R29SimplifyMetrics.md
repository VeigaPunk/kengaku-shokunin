# R29SimplifyMetrics — occurrence / leaf / task / index metric design

**Seat / writer:** `KengakuR28.R29SimplifyMetrics-2`  
**Scope:** Read-only simplification design review for C1 generated-config projection observability (milestone: pinned projection metrics). No production edits, no `config_projection.py` execution (file absent at baseline `ed26bdf5d924755697cd6812129be2fa441c42a3` and prereg `31934e5660f1814326c6472eefdfa0c41e642a2f`; verified via `git cat-file -e …:plans/config_projection.py` → path does not exist).  
**Sources:** `plans/round-29-claims.md`, `plans/fixtures/r29/manifest.json`, `plans/fixtures/r29/profiles.json`, `plans/fixtures/r29/generate_test_data.py`, `plans/fixtures/r28/webarena/config_files/test.raw.json`, `plans/benchmark_spec_audit.py` (output shape precedent), `.ufo/waves/round-29/build-spec.json` (R29ExecCore / R29ExecOracle shared JSON keys).  
**Tooling installs:** none.

## Godspeed axes (this review)

| Axis | Intent here |
|------|-------------|
| **Novelty (C1)** | Smallest metric surface that still satisfies prereg + oracle cross-check |
| **Correctness** | Three count units never pooled; raw vs decoded vs runtime boundaries explicit |
| **Maintainability** | One projection pass, one leaf diff walk, flat JSON — no second schema authority |
| **Output cost** | Full `--json` is inherently large (2436 task records); avoid duplicate census frameworks |
| **Calibration / method** | Unchanged — no new scores or vacuity semantics |

## Frozen population (independent census)

Command: scratch census script → `.ufo/waves/round-29/scratch/R29SimplifyMetrics-2/census.json`.

| Unit | Value | Evidence |
|------|-------|----------|
| Input tasks | 812 | parsed `test.raw.json` |
| Distinct `task_id` | 812 | no duplicates |
| Profiles | 3 | `profiles.json` keys |
| Task×profile projections | 2436 | 812×3 |
| `output_index == task_id` (frozen) | all 812 | enumerate vs `task_id` |
| Raw serialized `__WIKIPEDIA__` | 0 | still report six-token row |
| Runtime markers (not env tokens) | `__last_url__` 65, `__page__` 12 | must not enter six-token residual |

Simulated faithful pipeline (global ordered replace → `json.loads` → leaf diff, `distinct_origins` profile): **replacement occurrences** sum **1435** per profile; **changed decoded leaves** **1416**; **tasks with ≥1 changed leaf** **812**; **remaining known six-token** raw and decoded **0** after projection. Gap 1435 vs 1416 is expected (multiple serialized hits can collapse to one decoded leaf) — pooling would violate prereg.

Prereg anchor (13 words): “distinguish replacement occurrence counts, changed-leaf counts and task counts; do not pool units.”

## Minimum unambiguous metric families (keep separate keys)

Implement exactly these **four non-interchangeable units** everywhere (production `--json`, oracle, L1 diff):

1. **`replacement_occurrence_count_by_token`** — per profile, dict of six keys `GITLAB`…`MAP`. Count non-overlapping `str.replace` hits on the **evolving serialized raw text** in manifest `replacement_order`. Unit: **occurrence**. `WIKIPEDIA: 0` must appear explicitly on frozen input.

2. **`changed_leaf_count`** — per profile, int. Walk decoded JSON after projection; count leaves where projected value ≠ original (same path set, same list ordering). Unit: **leaf**.

3. **`changed_task_count`** — per profile, int. Tasks with ≥1 changed leaf. Unit: **task** (≤812).

4. **`input_task_count` / `task_profile_projections` / `profile_count`** — population guards (812, 2436, 3).

**Do not** expose a single “change_count”, “substitutions”, or “fields_changed” rollup.

### Index vs task ID (fifth concept, not a “count unit”)

Per task record (required in full JSON):

- `output_index` — `enumerate` position (upstream writes `config_files/{idx}.json`).
- `task_id` — field from object.
- `index_equals_task_id` — bool per row; profile-level summary only lists **violations** (empty on frozen 812).

Hand witness (shuffled IDs) lives in `projection_cases.json` / selftest — not inferred from frozen population.

### Remaining placeholders (six-token contract only)

- `remaining_known_raw` — after full ordered replace on serialized text, counts for `__GITLAB__`…`__MAP__` only.
- `remaining_known_decoded` — same six literals in decoded string leaves after parse.

**Out of scope for these maps:** `__last_url__`, `__page__`, and any other runtime markers (report separately under `runtime_marker_counts_raw` if useful for debugging; **must not** mix into six-token residuals or replacement counts).

## Boring minimal implementation shape

Follow `benchmark_spec_audit.py` CLI habits: stdlib, `--root`, `--summary` human lines, `--json` machine document, exit 0/1/2, `LIMIT`/`FINDING` stable ids — **without** importing its schema-audit metrics.

### One internal pipeline (no parallel “authorities”)

```
read_bytes once → pin manifest → retain raw_text
→ AST-check generator replace order/names (inert file)
→ for each profile:
      projected_text = ordered_global_replace(raw_text, values)
      optional: digest raw_text / projected_text
      parse projected_text (failure → finding projection_json_invalid, exit 1)
      tasks = parsed list
      leaf diff vs original parsed list → changed paths + orig/projected values
      aggregate the four count families above
      emit per-task rows: task_id, output_index, output_relpath, projected_task object, changed_leaves[]
```

**Reject:** second JSON schema for metrics; a “vacuity” or semantic-validity layer; URL-normalization side channel; decoded-leaf oracle inside production (oracle stays separate per prereg).

### Changed-leaf record (minimal leaf payload)

Each element of `changed_leaves` (per task):

```json
{
  "path": "$[0].eval.reference_url",
  "original": "__SHOPPING__/…",
  "projected": "http://shopping.invalid:10103/…",
  "category": "decoded_string_value"
}
```

**Categories (closed enum, no framework):** `decoded_string_value` | `json_key` | `non_url_string_value` | `decode_failed_before_diff` — assign by fixed rules (token in key name vs value; non-URL field per hand cases). This satisfies prereg “category” without r28-style schema inventory.

**Reject:** free-form tags, scorer predicates, or “consumed vs unread metadata” verdicts in the projection tool (scouts/knowledge docs own that boundary).

### Raw occurrence provenance (minimal, not byte-based)

Prereg requires Unicode **codepoint** offsets, not bytes. Smallest sufficient design:

- Field names: `codepoint_start`, `codepoint_end` (half-open), `token` (six-name enum), `surface` (`raw_serialized`).
- **Attach provenance only on changed-leaf rows** where the leaf’s **original** decoded string contained a known placeholder, by scanning the **task’s slice** of pre-projection serialized text OR by recording global offsets filtered to the task boundary (pick one strategy; document which). Do **not** emit a separate 1435×3 global occurrence catalog unless L1 later proves oracle needs it — per-task changed-leaf + profile token counts already bound oracle totals; global offset list is optional compression **out of scope** for v1 if oracle agrees on aggregates + per-task objects (contract allows deferring only if Main’s compare still passes; default recommendation: profile-level offset list omitted, leaf-level offsets on changed fields only).

If profile-level offset census is required for a token scout seat, derive from one pass over `raw_text` with `str.find` in codepoint space (`len(s[:i])` on str is codepoint-safe in BMP-heavy JSON).

### `--summary` vs `--json`

- **`--summary`:** population lines, per-profile four unit families, digests, `index_equals_task_id` summary, synthetic profile purpose strings, finding count, exit code. No full projected objects.
- **`--json`:** top-level keys aligned with oracle spec (`input_tasks`, `profile_count`, `task_profile_projections`, `profiles` dict) plus `findings`, `limitations`, `source_digests`. Nested `profiles[name].projected_tasks[]` carries full objects (2436) — unavoidable for prereg.

**Reject:** a third output format, CSV sidecars, or writing `config_files/*.json` to disk.

### Oracle alignment (shared keys only)

Use the build-spec oracle key set as the **only** cross-tool contract; production may add non-conflicting fields (`findings`, `limitations`, AST witness) but must not rename:

`input_tasks`, `profile_count`, `task_profile_projections`, per-profile `task_count`, `changed_leaf_count`, `changed_task_count`, `token_occurrences`, `remaining_known_raw`, `remaining_known_decoded`, `projected_tasks`.

Map production `replacement_occurrence_count_by_token` → oracle `token_occurrences` (same integers).

## Deletion / anti-patterns (design-only; nothing removed in lane)

| Candidate bloat | Why reject |
|-----------------|------------|
| Unified “mutation” or “delta” score | Pools units; breaks M74/M75-style attribution |
| Byte offsets | Contradicts prereg |
| r28 `benchmark_spec_audit` eval-type / vacuity counters | Out of C1 scope; second source-truth |
| Importing `browser_env.env_config` or executing generator | Frozen contract forbids |
| Leaf-walk-only projection in production | Must match serialized replace first |
| Treating `__last_url__` as profile token | Contract names six env tokens only |

## Preserved behavior (must not simplify away)

- Six global replacements in fixed order before parse (`generate_test_data.py` lines 11–16 mirror).
- Authenticated single read of pinned bytes.
- Distinct handling of projection failure vs could-not-evaluate (exit 1 vs 2).
- Selftest hand cases including shuffled index≠id, JSON decode failure without repair, tamper/missing input.
- Independent oracle with explicit domain boundary on escape/cascade/quote cases.

Generator mirror quote (16 words): “raw = raw.replace … for idx, item in enumerate(data): … json.dump(item, f, indent=2)” — paraphrase spans lines 11–23 of pinned 838-byte fixture.

## Out-of-scope proposals (contract allows omitting)

- **Global 1435-entry occurrence atlas per profile** — redundant if oracle compares token sums + per-task leaf diffs; scouts own token-specific censuses.
- **Semantic “field consumed by scorer” classification** — belongs to r28 audit/knowledge, not projection CLI.
- **Canonical knowledge / SCORECARD rows** — L1 closure only.

## Unknowns / boundaries preserved

- Decoded-leaf oracle equivalence vs serialized replace on quote/backslash/cascade cases: production follows **text contract**; oracle reports boundary; Main diff must not treat oracle as universal truth outside benign frozen profiles.
- Whether 61 non-URL-ish changed paths (simulated) match F3 forecast is **source-informed**, not verified here.
- Production implementation not observed in lane tree at review time.

## Evidence commands (executed)

```text
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e ed26bdf5d924755697cd6812129be2fa441c42a3:plans/config_projection.py
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e 31934e5660f1814326c6472eefdfa0c41e642a2f:plans/config_projection.py
→ fatal: path does not exist (both)

python3 → census.json (see scratch path above)
```

VERDICT: PASS

Report: `.ufo/waves/round-29/build/R29SimplifyMetrics.md`
