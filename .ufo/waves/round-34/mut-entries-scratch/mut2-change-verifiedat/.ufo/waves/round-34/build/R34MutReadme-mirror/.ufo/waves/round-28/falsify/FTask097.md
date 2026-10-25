# FTask097 — author-side falsification of BUILD case097 (WebArena task_id 97)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Target under test: `.ufo/waves/round-28/build/Task097.md` (8917 bytes, sha256 `19ac0848756274987616ad4a9e4e27d096b1c25c820a952080a69fcf078378db`).
Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 97, lines 3100–3129.
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`.
Candidate SHA256 (recomputed 2026-10-21, unchanged): `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`.
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted** (absent; not created or edited by this seat).
Scope: case 97 only; pinned static bytes; no runtime-validity claim. Findings only, no production/candidate edit.

## 0. Method and provenance

- Read-only over production. No installs or updates (tool log: none). No browser, no benchmark-site request, no upstream Python imported/executed, no REA MCP.
- Commands on pinned bytes only: `sha256sum`, `wc`, `awk`/`sed` line-numbered reads, `grep -n`, and `python3 -B` (`json.load` census plus a local four-line re-implementation of `clean_answer`/`must_include`). The re-implementation is not upstream execution; it reproduces L80–86 and L98–111 semantics.
- `nltk` is absent on this host; this does not affect the trace: with `len(clean_ref) == 5` the L103–107 conjunction is false before `word_tokenize` is reached, so the tokenized branch is not taken.
- No production instrument (`benchmark_spec_audit.py`, `benchmark_oracle.py`, `registry_check.py`) was imported or run.

Pin (recomputed; equals `plans/fixtures/r28/webarena/manifest.json`):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

Build's truncated digests `7b50386f…37652`, `e23edb39…00c22`, `ec758da4…7e275` all match. `LICENSE` first lines are `Apache License` / `Version 2.0`.

## 1. Raw case-97 facts (observed, line-exact)

| field | value | line |
|---|---|---|
| task block | `{` … `},` | 3100 / 3129 |
| sites | `["map","wikipedia"]` | 3101–3104 |
| task_id | 97 | 3105 |
| require_login / storage_state | true / null | 3106 / 3107 |
| start_url / geolocation | `__MAP__` / null | 3108 / 3109 |
| intent_template = intent | "Tell me the distance to drive from Carnegie Mellon University to the top computer science school in massachusetts" | 3110 / 3112 |
| instantiation_dict / require_reset | `{}` / false | 3111 / 3113 |
| eval_types | `["string_match"]` | 3115–3117 |
| reference_answers | `{"must_include": ["914km"]}` | 3118–3122 (literal 3120) |
| reference_url / program_html / string_note | `""` / `[]` / `""` | 3123–3125 |
| reference_answer_raw_annotation | `"914 km"` | 3126 |
| intent_template_id | 120 | 3128 |

Every field bullet in the build's "Task spec" section reproduces exactly, including that the record's own annotation is spaced and the scored literal is not.

Stratum and selection:

- 27 strata under (sorted site set, sorted evaluator-type set). The `(map,wikipedia)+(string_match)` stratum is `{97, 265, 266, 267, 268}`; 97 is the minimum.
- `intent_template_id: 120` occurs only on task 97 (full-file census).
- Lexicographic strata minima reproduce exactly the persisted IDs `[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]`; 97 is the 15th. The sample contains no `shopping` site (759 is `map` + `shopping_admin`).

## 2. Evaluator chain — every anchor reproduces

| build claim | observed |
|---|---|
| `evaluator_router` L356–374, `string_match` appends `StringEvaluator()` | `def evaluator_router` 356; case 365–366; `return EvaluatorComb` 374 |
| `EvaluatorComb.__call__` L341–352, product | 341 def; `score *= cur_score` 351; `return score` 352 |
| `StringEvaluator.__call__` L123–170 | 123 def; `return score` 170 |
| `get_last_action` L47–56, `trajectory[-1]` | 47 def; `trajectory[-1]` 50; `return` 56 |
| `pred = clean_answer(last_action["answer"])` L134 | exact at 134 |
| `must_include` branch L142–149, `tokenize=(len(value)==1)` | 142–149; `len(value) == 1` 148 |
| `must_include` L98–111, `clean_answer` both sides | 98 def; 99–100; tokenize gate 103–107; else 110–111 |
| `clean_answer` L80–86 strip/quote/lower | 81 strip; 82–85 one outer quote pair; 86 `.lower()` |
| helper functions L146–210 imported L18–27, never called | imports 18–27; `llm_fuzzy_match` 146–173, `llm_ua_match` 176–208; no `fuzzy_match` key on task 97 |

Additional observations supporting the build's unchecked-clause map:

- `reference_answer_raw_annotation` appears **zero** times in `evaluators.py`; it is never scored.
- `StringEvaluator.__call__` reads only `configs["eval"]["reference_answers"]`, `configs["intent"]` and (fuzzy only) `string_note`; `reference_url` is read only at 213 (inside `URLEvaluator`) and `program_html` at 258 (inside `HTMLContentEvaluator`), neither instantiated for `["string_match"]`.
- `StringEvaluator.__call__` uses `page`/`client` only as unused parameters; the score path has no DOM/URL read and no LLM call.

## 3. Decisive boundary / control

**Control C1 — operator table.** Local re-implementation of L80–86 + L98–111 (tokenized branch unreachable) gives:

| prediction | cleaned | score |
|---|---|---|
| `914km` | `914km` | 1.0 |
| `It is 914KM via I-90` | `it is 914km via i-90` | 1.0 |
| `914 km` (annotation's own form, L3126) | `914 km` | **0.0** |
| `914.0 km` | `914.0 km` | 0.0 |
| `914 kilometers` | `914 kilometers` | 0.0 |
| `568 miles` | `568 miles` | 0.0 |
| `1914km` | `1914km` | 1.0 |
| `walking: 914km` | `walking: 914km` | 1.0 |
| `914km to Harvard` | `914km to harvard` | 1.0 |
| `  914km  ` | `914km` | 1.0 |

Every row of the build's "Static operator consequences" table is confirmed, including the decisive boundary: the annotator's own spaced form scores 0 while any unspaced substring — even `1914km`, or a wrong-mode/wrong-destination answer — scores 1.0.

**Control C2 — tokenize gate.** `len("914km") == 5 != 1`, so L103–107 is false and L111 `clean_ref in clean_pred` decides. This is why `1914km` is a false positive; if the reference had been one character the tokenized path would have excluded it. `word_tokenize` is never reached; `nltk` absence is immaterial.

## 4. Falsified / imprecise claims in the build report

**D1 (falsified universal).** The build states: "No `must_include` reference in the corpus uses a spaced unit." Literally false. Counterexamples in the pinned bytes, all `string_match` tasks:

- task 3, `must_include` line 115: `Sprite Stasis Ball 65 cm` (`65 cm`).
- task 6, `must_include` lines 211 and 215: `Sprite Yoga Strap 6 foot` (`6 foot`), `Sprite Stasis Ball 65 cm`.

If "numeric+unit references" is read without an operator restriction, tasks 267/268 (the same `map`+`wikipedia`+`string_match` stratum) also carry spaced time values: `fuzzy_match` `1h 23min` (line 8420) and `10h 33min` (line 8455), matching their raw annotations.

Scope that survives: restricted to **distance-unit (km/m) `must_include` literals**, the sentence is true and the surrounding census is exact — exactly seven such literals (32 `2.0km`, 33 `1.4km`, 97 `914km`, 98 `653m`, 99 `4.0km`, 100 `557m`, 265 `457km`), the six others unspaced and present verbatim in their annotations, and 97 the only one whose raw annotation spaces the unit. So this is a quantifier/scope overreach in a "for context only" sentence, not an error in the task-97 operator trace.

**D2 (numeric mislabel).** The build's "Located quote (evaluators.py L111, 3 words)" is arithmetically wrong: `return float(clean_ref in clean_pred)` has 4 whitespace-separated tokens (`python3 -B` control printed 4). The quote is still ≤25 words, so no quote-length breach; the annotation itself is the defect.

**D3 (minor boundary).** The build cites `helper_functions.py` "L146–210". `llm_fuzzy_match` is 146–173 and `llm_ua_match` is 176–208; lines 209–210 are blank before `class PseudoPage` at 211. The candidate's header range `146–208` is exact; the build's range overstates by two blank lines only.

Not defects after checking: the `128` login/storage count; "every map-site task has `storage_state` None"; "not specific to task 97"; "no `requests` or page-helper dependency **at scoring time**" (module import does pull `requests` at `helper_functions.py:6`, but the string-scoring path never calls it); "`require_reset: false` and `storage_state: null` mean no per-task state is restored" (accurate paraphrase of the two flags).

## 5. Candidate case-specific language vs source

The candidate mentions task 97 in only three places: the persisted selected-ID list; the case-table row `759,424,97,399 … unit spelling`; and the illustrative bullet:

> Task97: the graded reference is `914km` while its raw annotation spells `914 km`. The substring rule does not normalize units or internal whitespace; whether correct deployed-map answers are rejected remains unmeasured (Task097.md).

Each clause is source-supported:

- "graded reference is `914km`": `test.raw.json:3120`; the scorer reads `reference_answers` only and never `reference_answer_raw_annotation`.
- "raw annotation spells `914 km`": `test.raw.json:3126`.
- "substring rule does not normalize units or internal whitespace": `clean_answer` does strip/one-quote-pair/lower only (L80–86); `must_include` returns `clean_ref in clean_pred` (L111). No unit conversion and no internal-whitespace collapsing.
- "whether correct deployed-map answers are rejected remains unmeasured": correct; neither the case nor the candidate asserts a runtime rejection. No unobserved browser/judge condition is turned into success or failure.

The candidate's adjacent S062/S063 citations bearing on this case are also line-exact on pinned bytes: `StringEvaluator:71–170`, `URLEvaluator:173–241`, `HTMLContentEvaluator:244–333`, `combination/router:336–374`, helper `146–208`; `exact 80–94`, `includes 98–111,142–149`, `fuzzy 150–169`, N/A `152–163` with assignment at 159, URL `187–239`, page content `258–333`, composite `348–352,361–374`. The URL row's cited range stops at the `raise` (239) while `return score` is 241; no stated URL claim depends on 241. No case-97 candidate sentence exceeds source.

## 6. Independent population cross-checks (JSON-derived, not instrument output)

All equal the candidate's measured table:

| observable | independent value |
|---|---|
| raw tasks / distinct IDs | 812 / 812, IDs 0–811, no missing/duplicate |
| evaluator-type sets | 325 string_match, 282 program_html, 66 url_match, 10 string_match+url_match, 129 program_html+url_match |
| strata / selected minima | 27 / exact 16 persisted IDs |
| `program_html` targets / operators | 651 / 463 must_include + 188 exact_match |
| locator classes | JavaScript 524, full-page 105, helper 22 |
| target URL classes | navigation 338, last 238, helper 75 |
| string operator task counts | must_include 176, fuzzy_match 118, exact_match 45 |
| require_login true + storage_state null | 128, exactly the 128 map-site tasks (109 map-only, 17 map+wikipedia, 2 map+shopping_admin) |
| distance-unit must_include literals | 7 (32, 33, 97, 98, 99, 100, 265), only 97's annotation spaced |

The candidate's "shopping site is omitted" holds for site id `shopping`; `shopping_admin` does appear (759).

## 7. Unresolved (not claimed)

- Rendered spacing of the deployed map distance string, its routing profile/data version, and the Wikipedia passage resolving "top computer science school in massachusetts". No site/browser action was taken.
- Whether the generated evaluation config is byte-equivalent to the raw `eval` block (not pinned here).
- Instrument-internal claims (selftest 21, schema findings 0) were not re-exercised; only JSON-derivable counters were recomputed.
- Frequency of spaced or unit-converted agent answers (needed to size false negatives).
- The case's own PARTIAL (static trace complete; validity unresolved) is therefore affirmed.

## Verdict

Semantic case-97 audit: every task-97 intent/target/operator/unchecked-clause and line anchor reproduces from pinned bytes, and the candidate's task-97 language does not exceed source. The build report nevertheless contains one falsified corpus-wide universal about spaced units (D1), one wrong quote word count (D2), and a two-blank-line range overstatement (D3); none alters the task-97 operator trace or the case's PARTIAL conclusion.

VERDICT: PARTIAL
