# R29 simplification design — artifact scope and read-only paths

**Seat:** `KengakuR28.R29SimplifyArtifactScope-2` (leaf, read-only; no production edits in this seat)  
**Writer:** `KengakuR28.R29SimplifyArtifactScope-2`  
**Prereg:** `plans/round-29-claims.md`; baseline `ed26bdf5d924755697cd6812129be2fa441c42a3`; landed prereg `31934e5660f1814326c6472eefdfa0c41e642a2f`  
**Milestone:** Build pinned generated-config projection observability (design review only)  
**Tool installs:** none (stdlib-only design; pacman paused per lane contract)

## Godspeed axes (this seat)

| Axis | Question |
|------|----------|
| Contract fidelity | Does the boring path emit every preregistered metric and 812×3 projections without silent exclusions? |
| Attack / leakage surface | Are auth state, host env, real endpoints, and disk writes under `config_files/` absent? |
| Implementation surface | Fewest files, stdlib-only, no duplicate authority with oracle or r28 audit? |
| Source vs runtime boundary | Are six generator tokens, serialized-text semantics, and enumerate-index kept separate from evaluator runtime markers? |
| Observability | Can L1 compare production stdout to independent oracle JSON on shared pinned bytes only? |

## Evidence (read-only census, lane root)

**Pinned manifest** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json`  
SHA-256: `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` (matches prereg).

| Path | SHA-256 | Size |
|------|---------|------|
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | 838 B |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 B |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | (verified) |

**Baseline / worktree:** `git cat-file -e ed26bdf5…:plans/config_projection.py` → absent; worktree file absent (`WORKTREE_ABSENT`).

**Frozen raw population:** `task_count=812`, `distinct_ids=812`, `index_eq_task_id=True` on enumerate order (all positions `i` satisfy `tasks[i].task_id == i`).

**Literal six-token occurrences in raw serialized text** (whole-file `str.count`, not decoded-leaf oracle):

| Token | Count |
|-------|------:|
| `__GITLAB__` | 385 |
| `__REDDIT__` | 336 |
| `__SHOPPING__` | 281 |
| `__SHOPPING_ADMIN__` | 300 |
| `__WIKIPEDIA__` | 0 |
| `__MAP__` | 133 |

**Runtime evaluator markers (not preregistered substitution tokens):** `__last_url__` 65, `__page__` 12 — appear inside locator/helper strings (e.g. `func:reddit_get_post_url('__last_url__')`), not as generator `env_config` placeholders.

**AST contract from pinned generator (inert data, `ast.parse` only):** six `raw.replace("__TOKEN__", NAME)` in order GITLAB → REDDIT → SHOPPING → SHOPPING_ADMIN → WIKIPEDIA → MAP; wildcard `from browser_env.env_config import *` at L5 must never execute.

**Index vs task_id source anchor** (`plans/fixtures/r29/generate_test_data.py` L21–23):

> for idx, item in enumerate(data):

Programmatic word count for that line alone: **5** words (≤25).

**Profiles:** three keys `distinct_origins`, `path_prefix`, `trailing_slash_sensitivity`; each holds six variable names and `*.invalid` synthetic URLs; each `purpose` states controlled synthetic substitution (8 words).

**Pattern precedent:** `plans/benchmark_spec_audit.py` — manifest SHA pin, single read retained bytes, `--root` / `--summary` / `--json` / `--selftest`, exit 0/1/2, selftest tamper harness uses `tempfile` under scratch only (not lane `config_files/`).

## Recommended boring minimal implementation

One production module: **`plans/config_projection.py`** (stdlib: `argparse`, `ast`, `hashlib`, `json`, `pathlib`, `sys`; selftest may use `tempfile`/`shutil`/`subprocess` like r28 audit). Separate files per build spec: `plans/fixtures/r29/projection_oracle.py`, `plans/fixtures/r29/projection_cases.json` — **no import edges** between oracle and production.

### Read path (minimal)

1. Resolve `--root` (default: lane root = parent of `plans/`, same as `benchmark_spec_audit.py`).
2. Read **`plans/fixtures/r29/manifest.json` once**; reject if manifest bytes ≠ pinned SHA-256 `f6390b9…` (`manifest_tampered`, exit 2).
3. For each `manifest["files"]` entry: **one** `read_bytes()`, store in an in-memory `verified[path]` dict; reject on SHA mismatch (`snapshot_tampered`, exit 2).
4. Parse `profiles.json` from retained bytes; require three profiles, each with `purpose` + `values` dict covering exactly the six names in `manifest["replacement_order"]`.
5. Parse generator with **`ast.parse(verified[generator_path])`** only — extract ordered `(old_string, new_identifier)` pairs; mismatch → stable finding / exit 2 (`source_contract_unrecognized` or prereg-named ids).
6. Parse raw tasks with **`json.loads(verified[raw_path].decode("utf-8"))`** only after projection pipeline on **serialized text**, not by re-reading from disk.

No other inputs: no `corpus/SOURCES.md`, no `browser_env/env_config.py`, no `os.environ`, no credential or cookie paths, no network.

### Projection path (faithful, no extras)

Per profile:

1. Start from **retained raw text** (UTF-8 decode for `str.replace` only).
2. Apply six global replacements **in manifest order**, values from profile `values` keyed by identifier names (GITLAB, …, MAP) — including **WIKIPEDIA when count=0** (no-op on frozen input, still contract-faithful).
3. **`json.loads(projected_text)`** — on failure emit `projection_json_invalid`, exit 1; **no** repair, escape fix, or URL normalization.
4. **`enumerate(parsed_list)`** for output ordinal and nominal filename `f"{idx}.json"` **as metadata in JSON stdout** — do not create files.
5. For each task: record `task_id`, `output_ordinal`, `output_filename`, full projected object, and changed string leaves vs **original parsed task** (deep equality walk, JSON paths); categorize leaves (URL vs non-URL) without claiming runtime consumption.

**Provenance:** for each of the six tokens, scan **pre-replacement raw text** for literal occurrences; report **Unicode codepoint offsets** (not byte offsets) with brief string/key context. Count **replacement occurrences** separately from **changed-leaf counts** and **task counts**.

**Residual markers:** after projection, report counts of the six known placeholders remaining in serialized text and in decoded string leaves; **do not** fold `__last_url__` / `__page__` into “known six” or treat them as profile substitution targets.

**Digests:** SHA-256 of raw text and of projected text per profile (on retained string bytes).

### Write path (read-only observability)

- **Normal audit (`--summary` / `--json`):** stdout only. **Never** open `config_files/test.json`, `config_files/{idx}.json`, or any benchmark output path for write in the lane tree.
- Docstring and LIMIT lines must state scope: offline source-faithful projection; synthetic profiles; not deployment; not task validity; not runtime generated-config opened by evaluators (r28 boundary preserved).
- Exit codes: **0** audit completed with expected structural identities; **1** projection/invariant finding; **2** could-not-evaluate (missing/tampered manifest/input, bad profile shape, unrecognized source contract).

### Selftest boundary (allowed writes)

Mirror `benchmark_spec_audit.py`: tamper/missing-input cases run in **`tempfile.TemporaryDirectory`**, copy fixtures into temp `--root`, mutate there. That is **not** “actual config_files outputs created in lane” for the primary counting command. Hand cases load **`plans/fixtures/r29/projection_cases.json`** (delivered by R29ExecCases); include shuffled task-id vs index witness, post-read replacement race on retained bytes, and JSON-decode failure cases.

### What not to build (duplicate authority / weight)

| Reject | Why |
|--------|-----|
| Import or `exec` pinned `generate_test_data.py` | Wildcard `env_config` import must never run (prereg). |
| Fetch upstream `env_config.py` or README URLs for values | Host/deployment leakage; profiles are own-work synthetic. |
| Materialize upstream disk workflow (`test.json` + 812 files) | Prereg: stdout never writes real benchmark files; index is observability field. |
| Primary decoded-leaf rewriter | Oracle-only alternate within benign domain; production is serialized-then-parse. |
| Shared Python module imported by oracle and production | Independent oracle is preregistered. |
| Extend `benchmark_spec_audit.py` in place | Different manifest, population, and claim; keeps r28 frozen classes untouched. |
| `json.dump` projected tasks to repo paths for “debug” | Violates read-only lane artifact rule; use `--json` stdout. |

## Deletion candidates (implementation phase — not executed here)

These are **design-time removals** relative to naïve “run upstream generator” or over-engineered audits:

1. **Disk split write loop** from upstream — keep enumerate/index/filename as reported fields only.  
2. **Live env_config resolution** — delete any code path that reads deployment env or private profile stores.  
3. **SOURCES-driven default base URLs** — delete; only `profiles.json` supplies substitution values.  
4. **URL normalization helpers** — delete; prereg forbids silent repair.  
5. **Optional `--write-configs` CLI** — do not add; out of prereg interface (`--root`, `--summary`, `--json`, `--selftest` only).

**Preserved contract:** all 812×3 task/profile projections in JSON; per-task objects and leaf paths; token provenance; oracle-comparable keys; stable tamper/missing findings; AST order check; shuffled-index selftest witness; separation of occurrence vs leaf vs task units; F1–F5 forecasts unchanged in scope (scored after execution, not in this seat).

## Explicitly out of scope (contract allows deferral)

| Feature | Why out of scope |
|---------|------------------|
| Real WebArena deployment URLs or auth material | Synthetic `*.invalid` profiles only; no credentials in artifacts. |
| Substituting `__last_url__` / `__page__` | Runtime evaluator/helper markers, not the six generator tokens. |
| Task validity, browser runs, model scores | C1 is generated-config projection capability only. |
| Editing `corpus/SOURCES.md` or opening S070–S073 rows | Source scouts own registry; simplifier does not touch SOURCES. |
| Canonical knowledge draft promotion | Deferred until Q10 exact-byte rereads (prereg frontier). |
| Proving eval-time generated config matches projection | Source-faithful offline audit; runtime config remains r28-class unknown unless separately pinned. |

## Tradeoffs

- **Large `--json`:** 2436 full projected objects are required for oracle diff; streaming or summar-only JSON would shrink scope illegally.  
- **Wikipedia zero occurrences:** still run sixth replace for contract match; residual count should be 0 for all three profiles on frozen input (supports F2).  
- **Selftest temp dirs:** small on-disk mutation isolated from lane; production counting path stays stdout-only.

## Suggested L1 verification commands (not run in this seat)

```bash
python3 plans/config_projection.py --summary
python3 plans/config_projection.py --json
python3 plans/fixtures/r29/projection_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/config_projection.py --selftest
```

Compare oracle vs production on every required metric and per-task object per prereg.

---

**Report path (relative to lane root):** `.ufo/waves/round-29/build/R29SimplifyArtifactScope.md`

VERDICT: PASS
