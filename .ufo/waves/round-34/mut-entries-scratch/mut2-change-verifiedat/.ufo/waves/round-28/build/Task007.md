# Task007 — WebArena task_id 7 static task-spec / scorer audit (C1 case)

Writer/seat: `KengakuR28.Task007-2` (scout, read-only, author-side advice; not outside closure).
Scope: one case, task_id 7, of the frozen 16-case selection. Static reading of pinned files only; no upstream code imported/executed, no benchmark site contacted, no browser action.

## Inputs (pinned snapshot, upstream dce04686a56253aefba7b18a4fa0937cf1dc987b)

| File (lane-relative under `plans/fixtures/r28/webarena/`) | sha256 observed = manifest | Source URL (manifest) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…37652` ✓ | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…00c22` ✓ | …/dce04686…/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…7e275` ✓ | …/dce04686…/evaluation_harness/helper_functions.py |

Access date 2026-10-21 (manifest `opened`); I opened the local pinned copies, not the URLs. Observed commands: `sha256sum` on the three files; `python3 -c` with `json.load` over `test.raw.json` (data parse only, nothing upstream imported); `sed -n 225,262p`; Grep/Read on the two `.py` files.

Located quotes (≤25 words, scope = the scorer path for this task):
- `evaluators.py:365-366`: `case "string_match": evaluators.append(StringEvaluator())`
- `evaluators.py:139-140`: `case "exact_match": score *= self.exact_match(ref=value, pred=pred)`
- `evaluators.py:91-93`: `StringEvaluator.clean_answer(pred) == StringEvaluator.clean_answer(ref)`

## Task 7 spec (`test.raw.json:225-255`)

- sites `["map"]` (l.226-228); `require_login: true` (l.230); `storage_state: null` (l.231); `start_url: "__MAP__"` (l.232); `geolocation: null`; `require_reset: false` (l.241); `intent_template_id: 79` (l.254).
- intent (l.240): "Tell me the full address of all international airports that are within a driving distance of 50 km to Carnegie Mellon University"
- eval (l.242-253): `eval_types ["string_match"]`; `reference_answers = {"exact_match": "Pittsburgh International Airport, Southern Beltway, Findlay Township, Allegheny County, 15231, United States"}` (l.247); `reference_url ""`, `program_html []`, `string_note ""`; `reference_answer_raw_annotation` (l.252): "Pittsburgh International Airport People Movers, Airport Boulevard, Findlay Township, Allegheny County, Pennsylvania, 15231, United States".
- Stratum: (sites `[map]`, eval types `[string_match]`), 89 tasks, minimum id 7, which is consistent with the frozen selection rule. The reference-key mix in this stratum is fuzzy 43, must_include 31, exact 13, and fuzzy+must_include 2.

## Case table (for L1)

| Intent element | Evaluator/operator | Target | Checked? | Anchor |
|---|---|---|---|---|
| Final answer text | `evaluator_router` → `StringEvaluator` (sole member of `EvaluatorComb`, product of 1 score) | `last_action["answer"]` = `trajectory[-1]` | yes: only input read | evaluators.py:356-374, 336-352, 133-134, 47-56 |
| "full address" of the airport | `exact_match`: `clean_answer(pred) == clean_answer(ref)`. `clean_answer` strips whitespace, removes one pair of enclosing `'`/`"` quotes, and lowercases. `pred` is cleaned twice (l.134 then l.92), `ref` once | literal l.247 string | yes, as whole-string equality, case-insensitive | evaluators.py:80-86, 90-94, 139-140 |
| "all" airports (set completeness) | none separate; exact_match against one address implies the expected set has size 1 | — | only implicitly, through string equality | test.raw.json:247 |
| "international" (airport type) | none | — | no | — |
| "driving distance of 50 km" from CMU (the route constraint) | none. The scorer never reads `page`, `client`, URL, or map state | — | no (the process is unchecked; only the outcome string counts) | evaluators.py:123-170 (page/client unused) |
| Map navigation / trajectory | none (`url_match` and `program_html` are not declared; `reference_url` is empty) | — | no | test.raw.json:243-250 |
| Semantic equivalence (paraphrase, ordering, "Pennsylvania"/"PA") | `fuzzy_match`/`ua_match` are not used | — | no: any added or reworded token gives 0.0 | evaluators.py:150-169 not reached |
| Helper functions / LLM judge | `llm_fuzzy_match`, `llm_ua_match` (gpt-4-1106-preview) not reached; the module is only imported | — | n/a | helper_functions.py:146-210; evaluators.py:18-27 |

Dynamic state and judge dependencies: the score is a deterministic function of the agent's final answer string. The map service state, OSM data version, login (`require_login` true), and reset are not consulted by the scorer. They only shape what an agent can observe. There is no LLM judge on this path. Import-time dependencies (beartype, nltk, playwright, `browser_env`, `llms.providers.openai_utils`) are required to load the module but play no role in the scoring logic `[INFERENCE from imports at evaluators.py:12-27, helper_functions.py:1-21]`.

## Potential validity limitations (task-specific; not proven defects)

1. **The exact reference disagrees with its own raw annotation.** The scored target (l.247) uses "Southern Beltway" and omits "Pennsylvania". The raw annotation (l.252) names "…People Movers, Airport Boulevard, …, Pennsylvania, …". Under `exact_match`, an agent that copies the raw-annotation address, or any equally valid geocoder rendering, scores 0.0.
2. **The operator is stricter than the sibling instance.** Task 9 (same template 79, a different start point, 30 km) uses the identical address but under `must_include` (`test.raw.json:312`). Task 7 uses `exact_match`. A natural answer to task 7, such as "The only international airport is Pittsburgh International Airport, Southern Beltway, …", contains the reference yet scores 0.0 here, while the same answer would pass task 9.
3. **"Full address" depends on the instance.** The reference is one particular reverse-geocode/search rendering (it has no house number and omits the state). The intent does not pin down the format, so correctness relative to the reference depends on which map result the agent reads.
4. **The geographic premise is unchecked.** The claim that exactly one international airport lies within 50 km of driving distance from CMU is asserted by the reference, not verified by the scorer. It also depends on the map data and routing profile deployed at evaluation time.

## Runtime evidence needed before calling task 7 valid or invalid

- The deployed map instance's search/reverse-geocode output for "Pittsburgh International Airport". This would show whether the l.247 string is the exact text an agent sees, and whether the l.252 rendering also appears.
- Driving-route distances CMU→PIT and CMU→other candidate international airports on that instance, to confirm the set has exactly one member under the 50 km bound.
- The actual harness invocation: whether `config_files/7.json` (generated from raw) keeps `exact_match`, and how the agent's stop/answer string is extracted. `run.py` and the config generator are not in the snapshot.
- Graded trajectories or human answers showing whether correct natural-language answers are being scored 0.0.

None of these were collected (that would require site contact or execution, which is forbidden here).

## Uncertainty / gaps

- The double `clean_answer` on `pred` (l.134 and l.92) can strip a second layer of quotes from the prediction but not from the reference. This is a minor asymmetry with no observed effect for this reference.
- I did not check WebArena-Verified or any later upstream fix; the scope is the pinned revision only.
- No knowledge admission or source row was proposed.

## Verdict

**PASS (scoped):** the static task-7 intent→scorer mapping is complete and anchored. The benchmark validity of task 7 is **UNDETERMINED**. The four limitations above are potential issues; settling them requires the runtime evidence listed. This is not a round-level PASS. No tools were installed or updated.
