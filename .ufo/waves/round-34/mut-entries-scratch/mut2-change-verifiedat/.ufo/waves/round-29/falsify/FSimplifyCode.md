writer: KengakuR29-2.FSimplifyCode-2

# FSimplifyCode — YAGNI review of `plans/config_projection.py`

**Attack:** Godspeed YAGNI pass on the integrated round-29 projection instrument: dead stores, redundant JSON echo fields, duplicated tree walks, and the broad `main()` exception tuple. Goal: deletions/refactors that leave pinned `--summary` and `--selftest` byte-identical.

**Production source read:** yes (this review item permits it). **LSP:** unavailable; reachability via ripgrep (no `import config_projection` / `from config_projection` in lane production `.py`) and scratch mutants under `.ufo/waves/round-29/scratch/falsify/FSimplifyCode-2/`.

## Axes (godspeed)

| Axis | Lens |
|---|---|
| **novelty (C1)** | `--summary` / `--json` / oracle-facing fields must stay aligned with prereg `plans/round-29-claims.md` required output. |
| **calibration** | `--selftest` (20 cases) is the landed gate; summary-only “safe” mutants that drop invariant findings are false positives. |
| **operability** | Remove dead stores and duplicate hot-loop work without second conventions. |
| **separability** | Oracle must not import this module; simplifications here must not assume oracle reads Python source. |

## Baseline (observed)

Commands (lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`):

```bash
python3 plans/config_projection.py --summary --root "$ROOT"
python3 plans/config_projection.py --selftest --root "$ROOT"
python3 plans/config_projection.py --json --root "$ROOT" | sha256sum
```

| Artifact | SHA-256 |
|---|---|
| `--summary` stdout | `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f` |
| `--selftest` stdout | `1fa3c1fcb6d6b3f7b2a83097b8473343bf278fb20b88c1fcfa99161878058d44` |
| `--json` stdout | `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` (matches `corpus/evidence/round29-calibration/build-json-sha256.txt`) |

Instrument: 548 lines, 16 top-level functions, exit 0 on pinned audit/selftest.

## Confirmed dead / redundant (with location)

### 1. Dead population field `tokens_followed_by_slash`

- **Write:** `plans/config_projection.py:284` — computed into `population` dict.
- **Reads:** none in module (ripgrep only hit is line 284). Not emitted in `--summary` (population keys at `summary_lines` `367–371` omit it).
- **Effect of removal (scratch `mut_m20_drop_tokens_followed_by_slash.py`):** `--summary` unchanged, `--selftest` unchanged, `--json` SHA-256 → `916923167f78fe6c…` (differs from baseline).
- **Preserved contract:** summary + selftest gates. **Tradeoff:** JSON consumers lose an unused population key; junction signal remains in per-profile `stimulus_observations.value_slash_then_raw_slash_junctions` (`320–329`).

### 2. Duplicate `template(path)` in changed-leaf loop

- **Site:** `plans/config_projection.py:313–314` — `template(path)` evaluated twice per changed leaf.
- **Scratch `mut_m13_cache_template.py`:** bind `pt = template(path)` once; `--summary`, `--selftest`, `--json` all **byte-identical** to baseline.

### 3. `STIMULUS.get(name)` after exhaustive profile validation

- **Site:** `plans/config_projection.py:293` — `check_profiles` (`117–127`) forces keys == `STIMULUS` exactly before `audit_text` runs on pinned inputs.
- **Scratch `mut_m6_stimulus_bracket.py`:** `STIMULUS[name]`; all three outputs unchanged.

### 4. `distinct_task_ids` via `json.dumps` on integer IDs

- **Site:** `plans/config_projection.py:278` — `len(set(map(json.dumps, ids)))`.
- **Pinned input:** all `task_id` values are integers `0..811`; scratch `mut_m7_distinct_ids_set.py` → `len(set(ids))` with identical summary/selftest/json.
- **Tradeoff:** [INFERENCE] Non-JSON-serializable or colliding-under-`dumps` IDs would diverge; frozen raw file does not exercise that.

## Duplicated walks (not safely deletable)

| Walk | Sites (approx.) | Notes |
|---|---|---|
| `string_values` on projected tree | `307–308`, `323` (+ `316` on original) | Three passes per profile in `audit_text`; scratch merge to two passes (`mut_m15_merge_string_values.py`) is output-identical but still double-walks projected tree. |
| `json.loads` + `string_spans` on raw | `269–270` | Required by prereg: parsed objects for diff/projection vs codepoint occurrence map (`round-29-claims.md` lines 68–69). |
| Token census | `279` (`raw_text.count`), `145` (`project` steps), `214–227` (`provenance`) | Different units (global count vs per-step vs per-occurrence provenance); not redundant authorities. |
| Slash/junction logic | `284` (dead population field) vs `320` (`junctions` for stimulus) | Overlapping *idea* but only `320` is consumed; deleting `284` is the safe trim. |

## Over-broad exception handling (`main`)

- **Site:** `plans/config_projection.py:538–539` — single handler for `(OSError, ValueError, KeyError, TypeError, AssertionError, IndexError)` → finding `input_invalid`, exit 2.
- **Pinned path:** removing `AssertionError` (`mut_m1_no_assertion_in_handler.py`), `IndexError` (`m16`), or `TypeError` (`m17`) leaves summary/selftest/json unchanged.
- **Observation:** Normal audit calls `json.loads` before `string_spans` (`269–270`); invalid JSON fails in `loads`, not in `string_spans` asserts. [INFERENCE] The `AssertionError` arm is latent for “valid to stdlib JSON decoder but assert-fails in custom scanner” inputs not covered by selftest.
- **YAGNI verdict:** Tuple is wider than exercised on frozen inputs; narrowing is operability-only unless a deliberate “assert → exit 2” policy is documented.

## False-safe deletions (pass summary/selftest, **change audit semantics**)

### `leaf_change_unexplained` carrier invariant (`316–318`)

Scratch mutants:

- **`mut_m2_drop_leaf_unexplained.py`:** delete entire block (including `carriers` walk).
- **`mut_m14_unexplained_only.py`:** keep only `unexplained > 0` branch; drop `carriers != len(changed)`.

Both leave pinned `--summary` and `--selftest` **byte-identical** (including JSON SHA-256).

**Mismatch (counterexample):** identity profile values `values[k] = "__%s__" % k` on raw `[{"task_id":0,"start_url":"__GITLAB__"}]`.

| Variant | Findings IDs |
|---|---|
| Baseline `audit_text` | `leaf_change_unexplained`, `known_token_remaining` |
| `mut_m2` | `known_token_remaining` only |
| `mut_m14` | `known_token_remaining` only |

Baseline finding payload: `{"id":"leaf_change_unexplained","profile":"p","unexplained":0,"token_leaves":1,"changed":0}` at logic `316–318`.

**Conclusion:** Treating carrier check as YAGNI **fails calibration axis** — selftest never uses identity substitution values, so the gate is blind to this deletion. Falsify item: **integrated selftest ⊄ invariant semantics**.

## JSON-only trims (summary/selftest unchanged, digest changes)

Scratch-verified on pinned root; all break `build-json-sha256.txt` receipt:

| Mutant | Lines / change | JSON SHA prefix |
|---|---|---|
| `mut_m5_drop_source_contract_meta.py` | `89–91` documentary `source_contract` keys | `49f8902b6cdc0068` |
| `mut_m8_drop_steps_token.py` | drop `token` in `project` step dict `145` | `ecaf405979b76dcd` |
| `mut_m9_drop_record_values.py` | drop echoed `"values"` in profile record `293` | `3b4b7261fb15ddcb` |
| `mut_m10_drop_would_be_sha.py` | drop `would_be_file_sha256` in tasks `333` | `61b5b528e490f009` |
| `mut_m12_drop_index_rule.py` | drop static `output_index_rule` `343–344` | `5a098eadd4266521` |
| `mut_m20_drop_tokens_followed_by_slash.py` | drop dead population field `284` | `916923167f78fe6c` |

Prereg **required output** (`round-29-claims.md` lines 62–71) includes per-task projected objects, changed leaf paths, occurrence provenance, and source contract extraction — so these JSON fields are **not** lane-deletable without contract amendment even when `--summary` omits them.

## Contract-required (do not delete)

| Area | Evidence |
|---|---|
| `remaining_known_tokens_decoded` + keys walk | Selftest `escaped_token_not_replaced` asserts decoded census `417`; mutant `m3` fails selftest at `417`. |
| `occurrence_provenance` / `string_spans` | Selftest `codepoint_offsets_and_key_token` reads `409–411`; `m4` fails selftest. |
| `remaining_known_tokens_text` vs decoded split | Pinned summary shows both zero, but escaped-literal case needs both channels (`416–417`). |
| Full `tasks[]` in `--json` | ~3.6M of 3.88M JSON bytes; prereg lines 66–67 require per-task projected objects and changed leaves. |
| `selftest` `wrong` cascade witness | `439–442` — used in assert, not dead. |

## Recommended moves (preserve verified behaviour)

1. Apply **`m13`** (cache `template(path)`) — strict improvement, zero output change.
2. Apply **`m6`** / **`m7`** on pinned-int `task_id` domain — zero output change on frozen inputs.
3. Remove **`tokens_followed_by_slash`** (`284`) only if JSON schema drift is acceptable (summary/selftest safe).
4. **Do not** remove `leaf_change_unexplained` carrier branch without adding selftest coverage for identity-value profiles.
5. Optionally narrow `538–539` after documenting desired assert-failure policy (untested on pinned path).

## Installs

None (Python 3.14 stdlib only).

## Preserved contract

Pinned `--summary` and `--selftest` outputs listed above; no lane files modified.

VERDICT: PARTIAL
