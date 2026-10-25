# Task097 — C1 case audit, WebArena task_id 97 (author-side, read-only)

Writer/seat: `KengakuR28.Task097-2` (scout, leaf, no delegation). Advice only: this is not an outside non-author closure.
Scope: one task (97) in the pinned snapshot at upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`. This is a static spec/scorer trace. It does not judge browser-level truth or establish actual task validity. Nothing upstream was executed, imported or evaluated, and no benchmark site was contacted.

## Inputs (hashes re-verified by `sha256sum`, matching `plans/fixtures/r28/webarena/manifest.json`)

| file | sha256 | source URL (opened 2026-10-21 per manifest) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…37652` | raw.githubusercontent.com/web-arena-x/webarena/dce0468…/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…00c22` | …/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…7e275` | …/evaluation_harness/helper_functions.py |

Paths are relative to `plans/fixtures/r28/webarena/`.

## Task spec (`config_files/test.raw.json` lines 3100–3129)

- `sites: ["map","wikipedia"]`, `start_url: "__MAP__"`, `require_login: true`, `storage_state: null`, `require_reset: false`, `geolocation: null`, `intent_template_id: 120`, `instantiation_dict: {}`.
- Intent (line 3112): "Tell me the distance to drive from Carnegie Mellon University to the top computer science school in massachusetts".
- `eval_types: ["string_match"]`. `reference_answers: {"must_include": ["914km"]}` (line 3120). `reference_url: ""`, `program_html: []`, `string_note: ""`.
- `reference_answer_raw_annotation: "914 km"` (line 3126). This has a space; the scored reference does not.
- Stratum `(("map","wikipedia"),("string_match",))` contains tasks `[97, 265, 266, 267, 268]`. Task 97 is the minimum ID and is the only task on template 120.

## Evaluator chain (`evaluators.py`)

1. `evaluator_router` (L356–374): the `"string_match"` case appends `StringEvaluator()`. No `URLEvaluator` or `HTMLContentEvaluator` is built, so `reference_url` and `program_html` are never read.
2. `EvaluatorComb.__call__` (L341–352) multiplies the scores of its evaluators. Here there is only one.
3. `StringEvaluator.__call__` (L123–170) takes the final action via `get_last_action` (L47–56, `trajectory[-1]`) and computes `pred = clean_answer(last_action["answer"])` (L134). It then iterates over the keys of `reference_answers`; only `must_include` is present.
4. In the `case "must_include"` branch (L142–149), the value list has length 1, so the call passes `tokenize=True`.
5. `must_include` (L98–111) calls `clean_answer` on both strings (L80–86: strip whitespace, strip one pair of matching outer quotes, lowercase). The tokenized path needs `len(clean_ref) == 1`, but `len("914km") == 5`, so it falls through to the plain substring test `"914km" in clean_pred` (L111).
6. Helper functions: `llm_fuzzy_match` and `llm_ua_match` (`helper_functions.py` L146–210) are imported (evaluators.py L18–27) but never called for this task, because there is no `fuzzy_match` key. There is no LLM-judge dependency and no `requests` or page-helper dependency at scoring time.

Located quote (evaluators.py L111, 3 words): "`return float(clean_ref in clean_pred)`".

## Intent → operator/target mapping

| intent component | evaluator operator / target | checked? |
|---|---|---|
| Distance value | `must_include` substring `"914km"` in lowercased, stripped final answer | **checked**, but only as that literal byte sequence |
| Unit (km) | embedded in the same literal, with no space | checked, only in the no-space form |
| Mode "drive" (not walk/transit) | none | unchecked |
| Origin = Carnegie Mellon University | none | unchecked |
| Destination = "top CS school in Massachusetts" (Wikipedia resolution, presumably MIT [INFERENCE]) | none; no school name is in `must_include` | unchecked |
| Agent actually used map routing / Wikipedia | none (no URL or HTML evaluator; `reference_url` is empty) | unchecked |
| Final page state | none | unchecked |
| Any extra or contradictory text in the answer | none (substring only, no exact match) | unchecked |

## Static operator consequences (derived from Python `in` semantics, not executed)

| final answer (hypothetical) | after `clean_answer` | `"914km" in pred` | score |
|---|---|---|---|
| `914km` | `914km` | yes | 1.0 |
| `It is 914KM via I-90` | `it is 914km via i-90` | yes | 1.0 |
| `914 km` (the raw annotation's own form, L3126) | `914 km` | **no** | 0.0 |
| `914.0 km` / `914 kilometers` / `568 miles` | — | no | 0.0 |
| `1914km` or `walking: 914km` | — | yes | 1.0 |
| `914km to Harvard` (destination not checked) | — | yes | 1.0 |

## Dynamic state and judge dependencies

- The score depends only on the agent's final `answer` string. There is no runtime page, URL or DOM read, and no LLM judge.
- The correctness of the 914km reference depends on runtime state that is not pinned in this snapshot: the hosted map instance's routing engine/profile and OSM data version, its distance rendering format (whether units are printed with or without a space), and the Wikipedia snapshot that defines "top" school. `require_reset: false` and `storage_state: null` mean no per-task state is restored. 128 tasks share the `require_login: true` with `storage_state: null` pattern, and every map-site task has `storage_state` None, so this flag combination is not specific to task 97.

## Potential validity limitation (task-specific; not proven defect)

The scored reference `"914km"` differs from the task's own raw annotation `"914 km"` by a space. With plain substring matching, a correct answer typed in the annotator's own spaced form scores 0. The same matcher gives credit for any answer containing `914km`, whatever the route mode or destination (for example `1914km`). There is also an ambiguity risk in the "top computer science school" destination, which the scorer never checks.

For context only: the six other numeric+unit references in the corpus (tasks 32, 33, 98, 99, 100, 265) also use the no-space form and their raw annotations match. No `must_include` reference in the corpus uses a spaced unit. Task 97 is the only one of these where the raw annotation is spaced. [INFERENCE] The no-space convention may mirror the map UI's rendering, which would make the gap matter only to agents that reformat the value.

## Runtime evidence required before declaring task 97 valid or invalid

1. Rendered output of the pinned map instance's driving route CMU→MIT (and CMU→any plausible alternative "top" school), showing the exact distance string and its spacing.
2. The Wikipedia snapshot passage that resolves "top computer science school in massachusetts".
3. The version of the map routing profile/data used when the reference was annotated, compared with the deployed one.
4. Observed agent final answers (or human trials) showing whether spaced or converted-unit forms occur, and how often. This is needed to measure false negatives, not just argue they are possible.

None of this was gathered. Gathering it requires site contact or live tasks, which are forbidden in this seat.

## Compact case row (for L1)

| task | stratum | eval chain | scored target | checked | unchecked | judge/dynamic | limitation | verdict |
|---|---|---|---|---|---|---|---|---|
| 97 | map+wikipedia / string_match | router L356–374 → Comb L341–352 → String L123–170 → must_include L142–149 → substring L111 (tokenize path skipped because len 5≠1, L104–107) | `"914km"` (json L3120) | substring `914km` in lowercased stripped final answer | drive mode, origin, destination/school identity, route provenance, unit variants, extra text | no LLM; reference depends on unpinned map routing/data + Wikipedia | reference/annotation spacing mismatch (`914km` vs `914 km`, L3126) → plausible false negatives; substring false positives (`1914km`) | **PARTIAL (static trace complete; validity unresolved pending runtime evidence)** |

## Commands observed

`sha256sum` on the three inputs; read-only `python3` JSON parsing of `test.raw.json` (task fields, template-120 siblings, stratum membership, numeric+unit reference census, login/storage counts); `grep`/`sed` reads of `evaluators.py` and `helper_functions.py`. Nothing was installed, there was no network access, and no file other than this report was written.

## Limitations

This is a static trace only. The behavior shown in the operator table follows from the source text and Python semantics; it was not executed. The destination identity is an [INFERENCE]. No source row or knowledge was admitted.

Final scoped verdict: **PARTIAL**. The case-97 static audit is complete and anchored to source lines. Whether the task is valid stays unresolved until the runtime evidence above exists. This is not a round-level PASS.

## Erratum — 2026-10-21 (raised by KengakuR28; original text above left unchanged)

1. **Overclaim narrowed.** The sentence "No `must_include` reference in the corpus uses a spaced unit" is false as written. Task 3 has `"Sprite Stasis Ball 65 cm"`, and task 6 has `"Sprite Yoga Strap 6 foot"` and `"Sprite Stasis Ball 65 cm"` (re-read from `test.raw.json`). The census regex only matched `\d (km|m|min|miles?)\b`, so it could not see `cm` or `foot`. Corrected statement: no `must_include` reference in the corpus uses a spaced **distance unit `km` or `m`**. The no-space `km`/`m` set is still tasks 32, 33, 97, 98, 99, 100 and 265. Task 97 is the only one of these whose raw annotation is spaced.
2. **Word count.** The located quote of `evaluators.py` line 111, `return float(clean_ref in clean_pred)`, is **4** words, not 3.
3. **Helper span.** `llm_fuzzy_match` and `llm_ua_match` occupy `helper_functions.py` lines **146–208**. Lines 209–210 are blank, and `class PseudoPage` starts at line 211.

None of these change the case-97 claims: the scorer chain, the `"914km"` substring target, the spacing gap against the raw annotation (line 3126), the checked/unchecked mapping, the runtime-evidence list and the **PARTIAL** verdict all stand. Re-checked by reading `test.raw.json` tasks 3 and 6, `evaluators.py` line 111 and `helper_functions.py` lines 205–212. Nothing was refetched, and no production or candidate files were edited.
