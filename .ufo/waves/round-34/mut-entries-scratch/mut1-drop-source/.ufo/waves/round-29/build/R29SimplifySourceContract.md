# R29 simplification design — minimal exact-six-assignment AST source contract

**Seat:** `KengakuR28.R29SimplifySourceContract-2` (actual writer: same)  
**Scope:** Read-only design review for `plans/config_projection.py` (not present in lane at prereg HEAD). No production edits, builds, or tests run in this seat.  
**Prereg:** `plans/round-29-claims.md`; manifest `plans/fixtures/r29/manifest.json` sha256 `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`.  
**Tool installs:** none.

## Godspeed axes (this review)

| Axis | Question |
|------|----------|
| **Fidelity** | Does the audit match upstream *serialized* six-pass `str.replace` then `json.loads`, with enumerate-index outputs? |
| **Safety** | Zero execution/import of `browser_env.env_config`, host env, network, or benchmark file writes? |
| **Boring surface** | Stdlib-only, one module, no generic Python interpreter? |
| **Observability** | `--summary` / `--json` expose 812×3, provenance, digests, per-task diffs, exit semantics? |
| **Pin integrity** | Single read, retained bytes, manifest/profile/raw SHA checks before parse? |
| **Contract rigidity** | AST rejects tampered generator shape (order, literals, RHS names) with exit 2? |

**Frontier moves kept (improve ≥1 axis, harm none):** structural AST extractor + manifest cross-check; projection as six literal `str.replace` on retained text; leaf diff via parsed JSON only; reuse r28 audit CLI/pin patterns.  
**Moves rejected:** `_load_machinery`-style partial exec; star-import resolution; URL-only substitution; JSON repair; decoded-leaf as primary path.

## Pinned source contract (static)

**Generator bytes:** `plans/fixtures/r29/generate_test_data.py` (838 B, sha256 `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`).

Located quotes (word count = `len(split())`):

| Line | Quote | Words |
|------|-------|------:|
| 1 | `Replace the website placeholders with website domains from env_config` | 9 |
| 5 | `from browser_env.env_config import *` | 5 |
| 11–16 | six `raw = raw.replace("__…__", NAME)` assignments | 4 each |
| 20–23 | `data = json.loads(raw)` then `for idx, item in enumerate(data):` | 5 / 6 |

**AST walk (executed locally on pinned bytes, no import/exec):** `ast.parse` → sole `main()` body yields **exactly six** consecutive assignments `raw = raw.replace(<Constant str old>, <Name new>)` with:

1. `__GITLAB__` → `GITLAB`  
2. `__REDDIT__` → `REDDIT`  
3. `__SHOPPING__` → `SHOPPING`  
4. `__SHOPPING_ADMIN__` → `SHOPPING_ADMIN`  
5. `__WIKIPEDIA__` → `WIKIPEDIA`  
6. `__MAP__` → `MAP`  

Then `json.loads(raw)` → `for idx, item in enumerate(data):` with per-index `json.dump` (output ordinal = **enumerate index**, not `task_id`).

**Manifest cross-check:** `manifest.json` `replacement_order` matches the six RHS names in the same order (tokens `__NAME__` derived mechanically).

**Inert import rule:** AST MUST record `ImportFrom(module='browser_env.env_config', names=star)` and MUST NOT import or execute that module. Profile values come only from `plans/fixtures/r29/profiles.json` (synthetic `*.invalid` URLs).

## Minimal boring implementation (recommended)

### 1. `extract_replace_contract(source_bytes) -> Contract | finding`

Single function, ~40–60 lines, no classes required:

- `ast.parse` UTF-8; syntax error → finding `source_contract_unrecognized`, exit **2**.
- Locate `def main`; walk **only** `main.body` in statement order.
- Accept replace steps iff: target is `Name(id='raw')`, value is `Call` to `.replace` on `Name(id='raw')`, arg0 is `Constant` str, arg1 is `Name` (not attribute, not literal).
- After six replaces, require `json.loads` into `data` and `For` with `enumerate(data)` (optional strict check on filename pattern `{idx}.json` — **nice for selftest, not required for prereg observability**).
- Compare extracted `(old_literal, rhs_name)` list to manifest `replacement_order` + expected `__{name}__` literals.
- Any extra replace, wrong order, non-literal old, non-Name new, missing main, or mismatch vs manifest → `source_contract_unrecognized` or `source_contract_tampered`, exit **2**.

**Do not** use `grader.py` `_load_machinery` / partial `exec`: upstream `main()` performs I/O and depends on star import; executing any part risks env side effects and blurs source-vs-runtime boundary.

### 2. `project_raw(raw_text, profile_values, order) -> str`

```text
text = raw_text
for name in order:  # manifest order
    text = text.replace(f"__{name}__", profile_values[name])
return text
```

- Values keyed by the six names in each profile object (`distinct_origins`, `path_prefix`, `trailing_slash_sensitivity`).
- Missing key / non-string value → `profile_missing_key` / `profile_invalid_type`, exit **2**.
- `json.loads` failure → `projection_json_invalid`, exit **1** (no repair).

### 3. Audit pipeline (mirror `benchmark_spec_audit.py` pin flow)

1. Resolve `--root` (default: lane root).  
2. Read once: manifest, profiles, generator, `test.raw.json`; verify SHA256 against manifest; retain bytes in memory.  
3. Run AST contract on retained generator bytes.  
4. For each profile: global replace → parse → 812 tasks; record digests, per-token **occurrence counts** on pre-replace text (Unicode **codepoint** offsets for each match, not byte offsets).  
5. Per task: `task_id`, output index `idx`, filename `{idx}.json`, full projected object, changed string leaves (JSON path + original/projected string values from placeholder-bearing parse vs projected parse).  
6. Report remaining `__KNOWN__` markers after projection.  
7. On frozen812: report whether `index == task_id` (here: **812/812 match**); selftest must include **shuffled** `task_id` witness where index ≠ `task_id`.

**Unit separation (prereg):** replacement **occurrence** counts ≠ changed-**leaf** counts ≠ **task** counts — never aggregate in summary lines.

### 4. CLI / exits (copy r28 audit shape)

- `--summary`, `--json`, `--selftest`; usage misuse → **2**.  
- **0** = audit completed, structural identities OK.  
- **1** = projection/invariant finding (e.g. unexpected placeholders, JSON invalid on benign profile, oracle disagreement when wired).  
- **2** = could not evaluate (missing/tampered inputs, contract unrecognized).  
- Stdout only; never write `config_files/test.json` or per-task files.

### 5. Independent oracle boundary (out of production import graph)

`plans/fixtures/r29/projection_oracle.py` performs decoded-leaf substitution for **benign** profiles only. Production MUST treat serialized-then-parse as authoritative. Where they diverge (quotes, backslashes, token cascades into inserted profile strings), report explicit non-equivalence — hand counterexample below.

## Hand counterexamples (wrong interpretations)

**A. Decoded-leaf-first vs serialized-global (cascade):**  
If profile `GITLAB = "http://evil/__REDDIT__/path"`, serialized pass 1 leaves `__REDDIT__` inside the inserted substring; pass 2 replaces it. Leaf-only rewrite on the initial parse without global re-scan on the whole text diverges. Production must follow serialized passes.

**B. JSON repair forbidden:**  
Raw fragment `{"url": "http://x/__GITLAB__\\"}"}` with replacement value containing `"` yields invalid JSON after replace; upstream does not repair. Correct behavior: `projection_json_invalid`, exit **1**.

**C. Index vs task_id:**  
`[{"task_id": 999}, {"task_id": 1}]` → files `0.json` / `1.json`, not keyed by `task_id`. Frozen812: `len=812`, index/task_id mismatches **0** (local `json.loads` census).

**D. URL-only substitution:**  
Replacing only fields matching URL heuristics drops placeholders in `must_include`, keys, and non-URL strings — violates “changes outside URL-valued fields preserved” and breaks occurrence census.

## Frozen input census (read-only)

**Raw812 placeholder counts** (`test.raw.json` sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`):

| Token | Occurrences |
|-------|------------:|
| `__GITLAB__` | 385 |
| `__REDDIT__` | 336 |
| `__SHOPPING__` | 281 |
| `__SHOPPING_ADMIN__` | 300 |
| `__WIKIPEDIA__` | 0 |
| `__MAP__` | 133 |
| `"task_id"` fields | 812 |

Expected projections: **812 tasks × 3 profiles = 2436** (`python3 plans/config_projection.py --summary` counting command per prereg — **not run here**; module absent at HEAD).

**Baseline check:** `git cat-file -e ed26bdf5…:plans/config_projection.py` → path does not exist; same at prereg `31934e5660f…`. Lane HEAD = `31934e5660f1814326c6472eefdfa0c41e642a2f`.

## Deletion / do-not-build candidates (design)

| Candidate | Why safe to omit | Evidence |
|-----------|------------------|----------|
| Generic Python interpreter for generator | Star import + I/O; prereg forbids executing upstream | AST: `ImportFrom … import *`; lines 9–23 I/O |
| Resolve `GITLAB` via `env_config` | Credentials/host env out of scope | Claims § frozen semantics |
| Partial `exec` of generator (`_load_machinery`) | Does not model replace chain faithfully; exec risk | `grader.py:2138–2169` pattern unlike 838 B generator |
| URL-only / field-filtered replace | Fails non-URL placeholder fields | r28 task audits (e.g. `must_include` placeholders) |
| `json.loads(..., strict=False)` repair | Contradicts quote/backslash selftest | Claims § selftest |
| Writing real `config_files/` outputs | Read-only audit | Claims § tool interface |
| Using `task_id` as output filename | Contradicts enumerate | Generator L21–23 |

## Explicit out-of-scope (contract-allowed)

- **Live `env_config` / deployment URLs:** synthetic profiles only; not observed benchmark deployment.  
- **Decoded-leaf oracle as primary metric:** separate script; bounded to benign profiles with disclosed domain limits.  
- **Exhaustive mutation beyond persisted selftest cases:** prereg caps hand-expected coverage.  
- **Browser, auth-state, site traffic:** unchanged from r28 static boundary.  
- **Canonical knowledge Q10 / SCORECARD capability row:** requires L1 execution + second-seat verification; not this seat.

## Preserved unknowns (source vs runtime)

- Substituted **live** hosts in real WebArena runs are **runtime** configuration; pinned raw JSON is **source** template data only.  
- Whether decoded-leaf oracle agrees with serialized projection for all **2436** rows on frozen inputs — must be measured at ExecCore/Oracle merge; not assumed here.  
- Semantic task validity, browser scoring, and placeholder substitution at evaluation time remain outside this instrument (r28 P2–P4 classes unchanged).

## Existing patterns to reuse (no new conventions)

- Pin/read/selftest: `plans/benchmark_spec_audit.py` (`read_bytes` retention, `--root`, exit 0/1/2, tamper/missing findings).  
- CLI docstring + LIMIT lines: `plans/attrib_calibration.py`.  
- AST parse without exec: `grader.py` `_load_machinery` **only** as negative example — do **not** copy exec path for this generator.

## Tradeoff

**Exact-six AST contract** is brittle to upstream refactors of `generate_test_data.py` — intentional: tampering or drift must exit **2**, not silently project wrong text. The cost is a few dozen lines of structural matcher vs a “flexible” interpreter; fidelity and safety axes win.

---

VERDICT: PASS

Scoped to: read-only simplification design for minimal exact-six-assignment AST contract and boring serialized projection observability aligned with `plans/round-29-claims.md`. Does not admit round closure, certify `--summary` execution, or claim oracle agreement — `plans/config_projection.py` remains absent at prereg HEAD; implementation proof belongs to L1/ExecCore after landing.
