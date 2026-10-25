writer: KengakuR29-2.FReviewSpanScanner-2

# FReviewSpanScanner — scoped review of `string_spans()` / `provenance()`

**Area (as assigned):** JSON string span scanner correctness on escaped quotes, nested
containers, numbers/literals, whitespace, keys; offset frame; bisect boundary conditions.
**Target:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py`
**Item id:** FReviewSpanScanner (round-29 POST-CRASH FALSIFY wave)

---

## 0. Scope, method, and the version that was actually attacked

**I read the production source.** This is a source-level review item (unlike the
oracle/independence items), so `plans/config_projection.py` was read in full
(lines 1–153, 149–233, 229–438, 439–548) and imported as a module for differential testing.
No production file, fixture, corpus row, SOURCES row, SCORECARD or candidate was modified.

**Critical scoping fact — the production file changed three times while I reviewed it.**
The lane contract names lane master `56fd949a6478342531e61f4feecb4a685d831640` as the
integrated state under attack, but `plans/config_projection.py` was an *uncommitted,
actively edited* file throughout my window:

| bytes | sha256 | when observed |
|---|---|---|
| lane master `56fd949a` | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` | contract target |
| worktree A | `a91f39434f29de6f1a332c326ab72177b878b5f3682ee861a4495c327b0472cf` | 14:16 local |
| worktree B (final) | `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142` | end of window |

Both versions were snapshotted byte-for-byte into my own scratch dir
`.ufo/waves/round-29/scratch/falsify/FReviewSpanScanner/` and every finding below was
re-verified against **both**. Findings are reported against the contract target
(`56fd949a`) and explicitly noted as **fixed** or **still live** in the final worktree.
I did not edit, stage, commit, or reset anything; `git status` shows the file as
pre-existing ` M` (not mine).

**Method (all independent of production logic):**

1. **Independent spec-based reference scanner** (`ref.py`) — hand-written JSON tokenizer
   with its own escape decoder; compared against `string_spans()` output.
2. **Independent regex literal tokenizer** (`indep.py`) — `"(?:[^"\\]|\\.)*"` plus a
   `json.loads` structure walk; used to check span membership, decode equality, and to
   classify every token occurrence's role.
3. **Independent full recomputation of every published number** (`recompute.py`) — reads
   only the pinned raw file + `profiles.json` and plain `json`/`str` operations; it does
   **not** import or read `plans/config_projection.py`.
4. **Randomized differential fuzz** — 4000 + 3000 + 2000 documents with escaped quotes,
   nested containers, whitespace variants, numbers/literals, unicode escapes.
5. **Path-aware provenance oracle** — derives each occurrence's role/pointer/template/task
   index from the regex tokenizer + an ordered `json.loads` walk (`object_pairs_hook`),
   then compares field-by-field against production output.

**Tooling:** no installs were needed. Python 3.14.8 (stdlib `json`, `ast`, `bisect`,
`hashlib`, `re`) only. Recorded per the operator directive: *tool: none installed;
version: n/a; channel: n/a; reason: stdlib sufficed for every probe.* One environmental
note: `/tmp` reached 100% (128G/128G) from other agents' scratch during my window; I
relocated my own scratch to my lane scratch dir and freed only my own files
(`/tmp/r29span`, a stray `/tmp/kengaku-r29-projection-*`). I did not delete any other
agent's data.

---

## 1. What I could NOT break (verified-correct; reported as negative findings)

These are the areas my assignment named. I attacked each and found no defect:

**Escaped quotes.** The pinned raw file contains **1274** `\"` escapes, **49** `\uXXXX`
escapes and **12** `\n` escapes (counted programmatically from the raw bytes). Every one
of the **29009** spans production emits is exactly a JSON string literal, decodes to
`json.loads` of that literal, and appears in the independent regex tokenizer's literal
set — **0 problems, 0 missing, 0 extra**. The scanner uses `json.decoder.scanstring`
(line 163), the same C scanner `json.loads` uses, so escape and surrogate handling is
authoritative by construction, not by re-implementation.

**Nested containers.** Fuzz over 9000 randomized documents (depth ≤ 3, mixed dict/array,
whitespace sprinkled between tokens): **0 mismatches** vs. the independent reference and
**0 mismatches** vs. `json.loads`-derived ground truth (path, role, decoded value).

**Numbers / literals.** `NUMBER_RE` (line 45) is anchored `-?(?:0|[1-9][0-9]*)...` and is
applied with `.match(text, i)` after literal `true/false/null` are tried by prefix
(line 188). In the **contract target** `string_spans` **raises `AssertionError` on
`[NaN]`, `[Infinity]`, `[-Infinity]`** — but `json.loads` *accepts* all three, so
`audit_text` would already have parsed the document successfully and then crashed in the
scanner. **This is a genuine contract-target defect (F1 below).** In the final worktree
the literal tuple is extended with `"NaN", "Infinity", "-Infinity"` (line 214) and all
three now scan cleanly — **fixed**.

**Whitespace.** `skip()` (line 154) accepts exactly `" \t\n\r"`, the JSON whitespace set.
I confirmed the pinned raw file is pure ASCII (880776 bytes = 880776 chars, zero
non-ASCII) with **no carriage returns** — so the instrument's own stated "universal
newlines / locale encoding is inert here" limitation is factually correct on this input.

**Offset frame.** `original_input_codepoint_offset` is a codepoint offset into the
**original** raw text, as claimed. On the pinned file all **1435** offsets equal my
independent `text.find(token)` result, and the instrument's own selftest line 410
distinguishes codepoint from byte offsets on a non-ASCII case. `json_pointer` for all
1435 value-role occurrences resolves against `json.loads(text)` to a string that literally
contains the token: **0 unresolvable, 0 mismatched**.

**Bisect boundary conditions.** This was the named target and it holds. `starts` is
strictly increasing and the spans are non-overlapping (verified on the pinned file:
29009 spans, `all(starts[i] < starts[i+1])` True, `all(spans[i][1] <= spans[i+1][0])` True).
`bisect_right(starts, at) - 1` therefore selects the unique candidate, and the guard
`spans[index][0] < at and at + len(token) <= spans[index][1]` correctly rejects a token
whose extent crosses out of the containing literal. Boundary probes:

| input | production result |
|---|---|
| `["__MAP__"]` | 1 record, role `value`, offset 2 |
| `["x__MAP__"]` | 1 record, role `value`, offset 3 |
| `["__MAP__x"]` | 1 record, role `value`, offset 2 |
| `["a__MAP__b"]` | 1 record, role `value`, offset 3 |
| `["__MAP__","__MAP__"]` | 2 records, offsets 2 and 12, each in its own span |
| `["__MA__MAP__"]` | 1 record, offset 6 (the later `__MAP__`, correctly) |

**No mismatches found.** The `bisect` boundary logic is correct.

---

## 2. Defects found

### F1 — `template()` raises `IndexError` on any path whose first element is an integer
**Severity: HIGH (contract target) / FIXED (final worktree)**
**Location (contract target `56fd949a`): `plans/config_projection.py:208`**

```python
parts[-1] = parts[-1] + "[]" if parts else "[]"
```

Python parses this as `parts[-1] = (parts[-1] + "[]") if parts else "[]"`. The `else`
branch was clearly intended to *append* a fresh `"[]"` component when the list is still
empty, but it instead assigns to `parts[-1]` of an **empty list** — an unconditional
`IndexError`. The guard `if parts else` protects the *right-hand side* of the assignment,
not the *target index*.

Exact reproduction (contract-target bytes, `template_master.py`):

```
template((0, 0))     -> EXC IndexError: list assignment index out of range
template((0, 0, 'x'))-> EXC IndexError: list assignment index out of range
```

The crash is reachable through the **production entry point**, not only by calling the
helper directly. `provenance()` line 225 calls `template(span[2])` on the span path, and
`audit_text` line 271 calls `provenance()`. A document whose root array holds an array —
e.g. `[["__MAP__"]]` — is perfectly valid JSON (`json.loads` succeeds) but aborts the
whole audit:

```
audit_text('[["__MAP__"]]', ...) -> IndexError: list assignment index out of range
  File ".../config_projection.py", line 225, in provenance
    "path_template": template(span[2]) if span else None})
  File ".../config_projection.py", line 208, in template
    parts[-1] = parts[-1] + "[]" if parts else "[]"
```

Via the real `main()` this surfaces as **exit 2** with `FINDING {"id": "input_invalid",
"detail": "IndexError('list assignment index out of range')"}` — i.e. a *valid* JSON
document is reported as an invalid input. (The same failure also reaches `diff()`'s
`template(path)` call at line 313.)

**Not triggered by the pinned corpus.** The pinned raw file's root array holds 812
**dicts**, so every `span[2]` path has a string as its second element and the buggy
branch is never taken. I confirmed the pinned run is unaffected: production's exit is 0
with zero findings and every published number matches my independent recomputation.

**Status in final worktree `135cc682`:** **FIXED.** `template()` (lines 230–239) now
reads `elif parts: parts[-1] += "[]"` / `else: parts.append("[]")` — the correct
append. `template((0,0))` now returns `'[]'` and `provenance('[["__MAP__"]]', ...)`
completes, returning one value-role record with `json_pointer "/0/0"`.

### F2 — key-role occurrences report the **container's** pointer/template, not the key's own
**Severity: MEDIUM — still live in the final worktree**
**Location: `plans/config_projection.py:222` (path assembly) vs `:224`–`:225` (record emission) — contract target and final worktree alike**

`string_spans()` records a **key** span with the *parent* path, not the key's own path
(line 175/201: `spans.append((i, end, path, "key", key))` — `path` is the enclosing
object's path). `provenance()` then reconstructs the correct full path at line 222:

```python
path = span[2] + ((span[4],) if span and span[3] == "key" else ()) if span else None
```

…but the record emission at lines 224–225 uses the **un-augmented** `span[2]` for both
`json_pointer` and `path_template`, while `task_index` is taken from the augmented
`path`. The two path bases are therefore mixed within a single record.

Consequence: two **different** keys carrying the same token are emitted with **identical**
`json_pointer` and **identical** `path_template`, and the key's own name is not
recoverable from the record at all:

```
input : '[{"alpha__MAP__":1,"beta__MAP__":2}]'
record: {"token":"__MAP__","original_input_codepoint_offset":8,
         "string_role":"key","json_pointer":"/0","path_template":"","task_index":0}
record: {"token":"__MAP__","original_input_codepoint_offset":24,
         "string_role":"key","json_pointer":"/0","path_template":"","task_index":0}
-> the two keys are indistinguishable; 'alpha'/'beta' appear nowhere in the record
```

The nested case shows the pointer resolving to the *containing object* rather than to the
member:

```
input : '[{"sites":[{"__MAP__":1}]}]'
record: {"string_role":"key","json_pointer":"/0/sites/0","path_template":"sites[]",...}
```

`/0/sites/0` addresses the **object that owns the key**, and `sites[]` describes that
object's template — neither names the offending key.

Note the same `span[2]`-vs-`path` split makes `task_index` a **string** rather than an
integer when the root is an object (contract target line 224 and worktree line 252):

```
input : '{"__MAP__":1}'
record: {"task_index":"__MAP__", ...}   # type str, not int
```

The instrument treats key-role occurrences as a *finding* (`token_outside_string_value`,
line 285–286), so a key-role record is a diagnostic artifact rather than a census row —
but the record it emits is still wrong in the two fields that are supposed to say *where*.

**Materiality on the pinned corpus: none.** The pinned file's **18140** object keys
contain **zero** tokens; `occurrence_roles` is `{"value": 1435}` with **0** key-role and
**0** outside-string occurrences. I confirmed all 1435 records match my independent
oracle field-for-field. This defect is therefore latent on the pinned input and only
manifests on a corpus whose key names literally embed a token.

**Status in final worktree `135cc682`:** **still live** — lines 250–253 are byte-identical
to the contract target on this point. The instrument's own selftest exercises a key-role
token (final worktree line 473) but asserts only `string_role == "key"` and the finding
set; it never asserts the key-role `json_pointer`/`path_template`, so the gap is
untested.

### F3 — `pointer()` on the empty path returns `"/"` in the contract target (RFC 6901 deviation)
**Severity: LOW (contract target) / FIXED (final worktree)**
**Location (contract target `56fd949a`): `plans/config_projection.py:201`**

```python
return "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in path)
```

For `path == ()` this returns `"/"`. RFC 6901 §3: the empty string `""` is the JSON
Pointer that references the **whole document**; `"/"` references the member whose name is
the empty string. The contract target conflates the two.

This is observable through the production `diff()` path (line 236: `problems.append(pointer(path))`
with `path == ()` when the root type differs) and through `provenance()` for a
root-level key span (`span[2] == ()` → `json_pointer "/"`). Reproduction on contract-target
bytes: `pointer(())` → `'/'`.

**Not triggered by the pinned corpus.** The pinned root is an array of dicts, so no
`span[2]` is ever `()` and `diff()` never reports a root-level type difference (the
pinned run has `problems == []` for all three profiles, confirmed independently).

**Status in final worktree `135cc682`:** **FIXED.** `pointer()` (line 227) is now
`"".join("/" + str(part)...)`, so `pointer(())` → `''`, matching RFC 6901, and
`pointer((0,))` → `'/0'` is unchanged.

---

## 3. Independent agreement on the pinned run (the load-bearing positive result)

I recomputed **every** published metric from the pinned raw file + `profiles.json` using
only `json`/`str` operations, with no access to `plans/config_projection.py`, and diffed
against production's `--json` output. **Mismatches: 0.**

| metric | independent | production |
|---|---|---|
| `input_task_count` | 812 | 812 |
| `distinct_task_ids` | 812 | 812 |
| `original_occurrences_by_token` | GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133 | identical |
| `occurrence_roles` | `{"value": 1435}` | `{"value": 1435}` |
| `tokens_followed_by_slash` | 697 | 697 |
| `other_double_underscore_markers` | `{"__last_url__": 65, "__page__": 12}` | identical |
| `tasks_with_token` | GITLAB 204, REDDIT 128, SHOPPING 192, SHOPPING_ADMIN 182, WIKIPEDIA 0, MAP 128 | identical |
| `tasks_with_any_token` | 812 | 812 |
| `task_profile_projections` | 2436 | 2436 |
| `changed_leaf_count` (all 3 profiles) | 1416 | 1416 |
| `changed_task_count` | 812 | 812 |
| `changed_leaves_by_category` | `{"non_url_field": 61, "url_field": 1355}` | identical |
| `changed_leaves_by_token` | GITLAB 385, REDDIT 323, SHOPPING 275, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133 | identical |
| `changed_leaves_with_multiple_occurrences` | 13 | 13 |
| `remaining_known_tokens_text` / `_decoded` (all profiles) | all 0 | all 0 |
| `projected_text_sha256` (3 profiles) | 2aec098e…, 54cf9833…, 49bbee2e… | identical |
| `index_equals_task_id` / violations | 812 / 0 | 812 / 0 |
| `findings` | — | `[]` (exit 0) |

**All 1435 provenance records** were verified field-by-field against my independent
path-aware oracle: **1435/1435 match** on `token`, `original_input_codepoint_offset`,
`string_role`, `json_pointer`, `path_template` and `task_index`; every `json_pointer`
resolves against `json.loads(text)` to a string containing its token (0 unresolvable,
0 mismatched); every `task_index` equals the corresponding `task_id` (0 mismatches).

Baseline `python3 plans/config_projection.py --selftest` on the final worktree bytes:
`SELFTEST clean cases=28 …`, exit 0.

---

## 4. Residual risk and verification gaps

- **[INFERENCE]** F1 and F3 are latent on the pinned corpus (I verified the pinned
  numbers are unaffected), but they are **not** hypothetical: F1 aborts a valid-JSON
  audit with a misleading `input_invalid` finding, and F3 violates RFC 6901 for the
  root pointer. Both are reachable through the production `main()` on inputs the
  manifest does not currently pin. Neither is a "the pinned numbers are wrong" claim.
- **[INFERENCE]** F2 is the one finding that survives into the final worktree. Its
  blast radius is limited to corpora whose object *keys* embed a token — zero such keys
  in the pinned file — and the affected records are diagnostic artifacts for a finding
  the instrument already raises. I did not find any pinned number that F2 changes.
- **Gap — duplicate object keys.** `json.loads` keeps the **last** duplicate key;
  `string_spans()` records **both** key spans with the **same** path. On
  `{"a":"x__MAP__","a":"y__MAP__"}` the two occurrences are both reported with
  `json_pointer "/a"` and `path_template ""`. The pinned raw file has **0** duplicate
  keys (verified by an `object_pairs_hook` census), so this is unreachable on the pinned
  input, and the final worktree's selftest now includes a
  `duplicate_keys_list_tasks_key_order` case. I flag it as a residual inconsistency
  between the two decoders, not as a distinct defect.
- **Gap — version churn.** The production file was edited three times under me and the
  final bytes (`135cc682`) were still uncommitted at the end of my window. My findings
  are pinned to explicit sha256 values, but a later edit could move the line numbers I
  cite. The line numbers in this report refer to `56fd949a` (contract target) and
  `135cc682` (final worktree) respectively.
- **Gap — I did not attack** the `diff()` walker, the `project()` replacement cascade,
  the `source_contract()` AST extraction, the exit-code mapping, or the hand-fixture
  adoption; those are other reviewers' areas. My `template()`/`pointer()` conclusions
  do cover the two helper functions that `provenance()` and `diff()` both call.
- **Gap — `/tmp` exhaustion** (host-wide, not caused by me) briefly blocked my scratch
  relocation; I moved my scratch into my lane dir and verified my probes still ran
  against the same bytes.

---

## 5. Scoped verdict

Against the **contract target** (`56fd949a`) the scanner/provenance pair is **not
defect-free**: F1 is a hard `IndexError` on valid JSON reachable through `main()`, F3 is
an RFC 6901 deviation, and F2 misreports the location of key-role occurrences. Against
the **final worktree** (`135cc682`) F1 and F3 are **fixed** and verified fixed; F2
**survives** but is latent on the pinned corpus.

On the **pinned corpus and the C1 deliverable itself** — 2436 task/profile projections,
the 1435 occurrence records, the offset frame, the bisect boundaries, the escaped-quote
and nested-container handling, and every published counter — the instrument's scanner and
provenance agree with my fully independent recomputation with **zero mismatches**, so I
found **no defect that changes a claimed C1 number on the frozen input**.

Scope is this review item only (scanner/provenance), and is not a round admission.

VERDICT: PARTIAL
