# FTask007 — falsification of BUILD case 7 (WebArena task_id 7)

Identity: seat `KengakuR28.FTask007`; author-side, read-only falsifier. Attack target is the
twice-asserted case-7 contract, not the other 15 cases:

- build case: `.ufo/waves/round-28/build/Task007.md`, sha256 `e0f4529571228839d7bd950f8811ef79b2e7561851497de945a780563261a911`
- raw task_id 7 in pinned `plans/fixtures/r28/webarena/config_files/test.raw.json`
- scorer/helpers: `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py`, `helper_functions.py`
- frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches the pinned frozen digest; rehashed at read time). Proposed canonical path `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted**; nothing here is an admission vote.
- pinned upstream revision `dce04686a56253aefba7b18a4fa0937cf1dc987b`; `manifest.json` `opened` `2026-10-21`.

No production, candidate, fixture, source, registry or code file was edited. No installs or updates.

## Integrity observed

| input | sha256 observed | manifest |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | equal |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | equal |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | equal |

All three were reopened as local bytes only; no URL was fetched and no upstream code was imported,
executed or evaled. Scratch probes below read the JSON as data and reimplement small predicates from
reading the pinned source; they are not an execution of the upstream scorer.

## Task-7 source re-read (observed facts)

Raw `test.raw.json:225–255` (numbering verified with `grep -n ''`):

- `sites ["map"]` 226–228; `task_id 7` 229; `require_login true` 230; `storage_state null` 231;
  `start_url "__MAP__"` 232; `geolocation null` 233; `require_reset false` 241;
  `intent_template_id 79` 254.
- intent line 240: `Tell me the full address of all international airports that are within a driving distance of 50 km to Carnegie Mellon University` (22 words). The template (234) parameterises airport type, radius and start; `instantiation_dict` 235–239 supplies `international airports`, `50 km`, `Carnegie Mellon University`.
- `eval` 242–253: `eval_types ["string_match"]` 243–245; `reference_answers` 246–248 with the sole key
  `exact_match` at 247 = `Pittsburgh International Airport, Southern Beltway, Findlay Township, Allegheny County, 15231, United States`;
  `reference_url ""` 249; `program_html []` 250; `string_note ""` 251;
  `reference_answer_raw_annotation` 252 = `Pittsburgh International Airport People Movers, Airport Boulevard, Findlay Township, Allegheny County, Pennsylvania, 15231, United States`.

Scorer path (line numbers from `grep -n` on the pinned bytes):

- `evaluator_router` 356–374 reads `configs["eval"]["eval_types"]` (361) and appends `StringEvaluator()` for `case "string_match"` 365–366. There is exactly one evaluator type, so `EvaluatorComb.__call__` 341–352 multiplies one factor (348–351).
- `StringEvaluator.__call__` 123–170: reads the config file 130–131, gets `trajectory[-1]` via `get_last_action` 47–56, pre-cleans `pred = self.clean_answer(last_action["answer"])` 133–134, initialises `score = 1.0` 136, iterates `configs["eval"]["reference_answers"]` 137, and for `case "exact_match"` 139–140 does `score *= self.exact_match(ref=value, pred=pred)`.
- `clean_answer` 80–86: `.strip()`, removes one enclosing `'…'` or `"…"` pair, `.lower()`.
- `exact_match` 90–94: `clean_answer(pred) == clean_answer(ref)`; `ref` is cleaned once, `pred` was already cleaned at 134, so prediction normalisation runs twice. `must_include` 98–111 is substring containment, tokenised only if `tokenize` and a one-character clean ref. `fuzzy_match`/`ua_match` 115–121 are only reached through the `case "fuzzy_match"` branch 150–169, which is not taken.
- `page`/`client` parameters 127–128 are never referenced in 130–170; the score path reads only the config's `eval.reference_answers` (and `intent` only in the unreachable fuzzy branch) and `trajectory[-1]["answer"]`. It never reads `require_login`, `storage_state`, `start_url`, `geolocation`, `require_reset`, map DOM, URL or map service state.
- `helper_functions.py`: `llm_fuzzy_match` 146–173 and `llm_ua_match` 176–208 (module imports 1–20). Neither is called on this path; the gpt-4-1106-preview judge is unreachable for task 7.

Numeric claims re-derived independently from the JSON (scratch `candidate_counters.py`, sha256 `dd2953644363ad0ddc27f16510a323f8e57b1eff1586ff8781f82aed79f06b19`, exit 0, assertions all pass):

| claim | source of claim | re-derived |
|---|---|---|
| raw tasks / distinct IDs 812 / 812, IDs 0–811 | candidate:101 | 812 / 812, exactly `range(812)` |
| evaluator-type sets 325/282/66/10/129 | candidate:102 | identical (unsorted authored order normalised) |
| site/evaluator strata 27; selected 16 | candidate:103, claims:19 | 27; first16 minima exactly `389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399` = `selected-task-ids.json` |
| string operators 45/176/118 | candidate:104 | identical |
| 651 program_html targets; exact 188, must_include 463 | candidate:105 | identical |
| locator classes 105/524/22 | candidate:106 | identical (`""`; `document.*` or `[`-expression; `func:`) |
| URL classes last 238 / navigation 338 / helper 75 | candidate:107 | identical (`"last"`; `func:`; other) |
| task-7 stratum 89 tasks, min id 7, key mix 43 fuzzy / 31 must_include / 13 exact / 2 fuzzy+must_include | build:26 | identical |

`test.raw.json` was never imported into a scorer; only `json.load` as data.

## Candidate case-7 language check

Candidate line 72 maps the third case in the group `556,356,7,377` to `Task007.md` and the third
descriptor is `fixed exact address`. The positional mapping is confirmed against the sibling reports:
`Task556.md` is README `must_include` substrings, `Task356.md` is routing-field `program_html`
predicates, `Task007.md` is the fixed `exact_match` address, `Task377.md` is the literal search-query
`url_match`. The descriptor is supported by raw 246–248 and `evaluators.py` 139–140. The candidate
does not claim task validity, runtime pass/fail, map state, or judge behaviour for case 7, and its
`59–60` selection statement matches `plans/round-28-claims.md:19` and the independent recomputation.
**No case-7 candidate language exceeds the pinned source.** The candidate's line-30 string-exact row
matches the source (80–94 normalisation; pre-clean at 134). Its line-31 includes row states two
necessary conditions for tokenisation but omits the additional `len(word_tokenize(clean_ref)) == 1`
test at 103–107; that is immaterial for case 7's exact_match path and for any reference longer than
one character.

## Falsification attempts and outcomes

1. **Missing target/operator/unchecked clause?** None found. Every intent clause is accounted for:
   full-address text → `exact_match`; `all` and `international` → no separate predicate (the strict
   single-address equality is the only implicit set constraint); `50 km driving` + CMU → not checked;
   map navigation/trajectory → not checked (`reference_url ""`, `program_html []`, `url_match` absent);
   paraphrase/ordering/state-name variants → not checked (`fuzzy_match`/`ua_match` unreachable).
   Build table lines 33–39 cover each of these, including the page/client-unused fact.
2. **Wrong source anchor?** All substantive anchors are exact. Two cosmetic range endpoints include
   trailing blank lines: `helper_functions.py:146-210` (build:39) while the two judge functions end at
   208 and 209–210 are blank (`PseudoPage` starts at 211), and `helper_functions.py:1-21` (build:41)
   while imports end at 20. No claim depends on the blank lines; the candidate's own `S063:146–208`
   is exact. This is a line-range nit, not a falsifier.
3. **Wrong numeric claim?** None; the table above reproduces all of them, plus build:26's 89/min-7/mix.
4. **Overstated determinism?** Build:41 says the score is a deterministic function of the final answer
   string and that there is no judge. For a well-formed trajectory this holds. One error-path boundary
   is not stated: if `trajectory[-1]` lacks an `"answer"` key, line 134 raises `KeyError` (no score),
   and a non-string answer reaches the beartype-decorated `clean_answer`. That is a harness-trajectory
   qualification, not a contradiction of the task-7 mapping.
5. **Candidate overreach for case 7?** None found (see above).

## Decisive boundary/control (observed, author-side derived probe)

Scratch `exact_match_probe.py`, sha256 `a02ed90567840737ad0081d26817a2c6651eb76227875d7e87952547d8193804`,
run with `python3 -B` over the pinned JSON, exit 0, assertions all pass. It reimplements `clean_answer`
(80–86), the line-134 pre-clean, `exact_match` (90–94) and `must_include` (98–111), and compares task 7
(exact_match) with task 9 (must_include, same template 79, `test.raw.json:293–320`, identical reference
string at 311–313). Exact output:

```text
task7 exact ref == task9 must_include[0]: True
task9 single-element tokenize flag derived as: True

prediction                                 task7 exact task9 must_include
exact reference                                    1.0                1.0
raw annotation                                     0.0                0.0
trailing period                                    0.0                1.0
trailing newline                                   1.0                1.0
leading+trailing spaces                            1.0                1.0
UPPERCASE                                          1.0                1.0
single outer double quote                          1.0                1.0
double outer quote layer                           1.0                1.0
natural sentence containing ref                    0.0                1.0
add Pennsylvania before ZIP                        0.0                0.0
add PA abbreviation                                0.0                0.0
```

Controls and interpretation:

- **Sibling-operator control (decisive).** The same reference string is graded by `exact_match` in
  task 7 and by single-element `must_include` in task 9. A natural sentence containing the reference
  scores **0.0** in task 7 and **1.0** in task 9; the raw annotation scores **0.0 in both**. Task 7's
  strictness is therefore the authored operator choice, not template-wide scorer behaviour, and the
  annotation is not a scoring path in either task. This confirms build limitations 1–2 and bounds the
  candidate's `fixed exact address` to a literal-equality predicate.
- **Normalisation boundary.** Case, outer whitespace/newline and one or two enclosing quote layers are
  normalised away (1.0); a trailing period, an added state token, or a sentence wrapper fails (0.0).
  The double-quote-layer pass is the observable form of the pred-twice/ref-once asymmetry the build
  calls minor; it has no effect on the actual reference, which contains no quotes.
- **Scorer-input boundary.** `page`/`client` are unused (127–128, 130–170); map DOM, route data, login,
  storage state and reset are never read. Only `trajectory[-1]["answer"]` and the config's one
  `exact_match` value feed the score, so task-7's score cannot depend on map state; it depends on the
  answer text and the frozen config bytes.

The probe is a derived model, not upstream execution: it makes the source-derived boundary observable
and does not certify the harness, map data or any real score.

## Residual unknowns (not closable statically)

- The generated `config_files/7.json` and the config generator/`run.py` are absent from the snapshot;
  whether generation preserves `exact_match` and the literal is unobserved.
- Deployed map search/reverse-geocode output, route distances CMU→PIT and competitors, the actual
  answer extraction, and graded trajectories are all unobserved. Whether any correct natural answer is
  penalised in practice, and whether task 7 is semantically valid, remain **undetermined**. Static text
  disagreement is not runtime task invalidity.
- The candidate's `schema findings 0` figure is an instrument-internal result and was not independently
  recomputed here; it is not needed for the task-7 intent→predicate mapping.

## Verdict

The build case-7 static mapping is complete and every sourced line/number I re-read is correct; the
candidate's case-7 descriptor is within the pinned source. The only defects found are a cosmetic
two-blank-line over-extension in one build anchor and an unstated missing-`answer` KeyError boundary,
neither of which changes any task-7 predicate, target, operator or unchecked-clause claim. No runtime
validity or invalidity is asserted.

VERDICT: PASS (scoped to BUILD case 7 and the candidate's task-7 descriptor; candidate bytes rechecked at `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`; this is not a whole-candidate Q10 reread or admission vote. Any candidate byte change invalidates this reread.)
