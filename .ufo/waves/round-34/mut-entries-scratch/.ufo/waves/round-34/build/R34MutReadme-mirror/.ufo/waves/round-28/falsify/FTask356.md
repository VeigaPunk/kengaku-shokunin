# FTask356 — author-side falsification of BUILD case356 (WebArena task_id 356)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Target under test: `.ufo/waves/round-28/build/Task356.md`
Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 356, lines 11036–11086
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
Candidate SHA256 (recomputed 2026-10-21): `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — equals the frozen value and `candidate-freeze.json`.
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted**: `ls` fails, file absent. It is named here as the prospective target only; nothing was edited.
Scope: case 356 only, static source bytes. No C2, no other case report, no production edit, no browser, no benchmark site, no scorer execution.

## 0. Method and provenance

- Read-only over production. No installs or updates (tool log: none). No browser opened, no site request, no upstream Python imported/executed/evaluated, no REA MCP. Production instruments `benchmark_spec_audit.py` / `registry_check.py` were **not** run by this seat; the JSON-derivable counters below were re-derived independently from raw bytes with stdlib `json.load` only.
- Commands: `sha256sum`, `wc`, `python3` (`json.load` + line-numbered printing), `awk`, `sed -n`, `grep -n`, `cat -A`. All read-only.
- Pins (full digests recomputed and equal to `manifest.json`; text opened as the local pinned snapshot 2026-10-21):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

Upstream (manifest): `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json` and `.../evaluation_harness/{evaluators,helper_functions}.py`. The build's truncated digests `7b50386f…37652`, `e23edb39…0c22`, `ec758da4…5275` all match the full hashes above.

## 1. Raw case-356 facts (observed, line-exact)

| field | value | line |
|---|---|---|
| task object open/close | `{` … `},` | 11036 / 11086 |
| sites | `["map"]` | 11037–11039 |
| task_id | 356 | 11040 |
| require_login / storage_state / require_reset | true / null / false | 11041 / 11042 / 11048 |
| start_url / geolocation | `__MAP__` / null | 11043 / 11044 |
| intent_template (also the authored quote) | "Show the route from SCS CMU in Pittsburgh to the location where the Declaration of Independence and Constitution were signed" | 11045 |
| instantiation_dict | `{}` | 11046 |
| intent (identical to template) | same 20-word quote | **11047** |
| eval_types / reference_answers / reference_url | `["program_html"]` / null / null | 11050–11052 / 11053 / 11054 |
| program_html | 3 targets | 11055–11083 |
| intent_template_id | 49 (unique in the 812-task population) | 11085 |

Targets (corrected ranges; the build gives locator lines only, and those are exact):

| # | range | url | locator | required_contents |
|---|---|---|---|---|
| T1 | 11056–11062 | `last` | `document.querySelector("div#content select.routing_engines").selectedIndex` (11058) | `exact_match "1"` (11060) |
| T2 | 11063–11072 | `last` | `document.querySelector('[name="route_from"').value` (11065) | `must_include ["Gates and Hillman Centers","Pittsburgh"]` (11067–11070) |
| T3 | 11073–11082 | `last` | `document.querySelector('[name="route_to"').value` (11075) | `must_include ["Independence Hall","Philadelphia"]` (11077–11080) |

No `prep_actions`, no `func:` locator, no `func` URL, no `string_note`/`url_note`, no ` |OR| ` element anywhere in the case. Eval keys are exactly `['eval_types','reference_answers','reference_url','program_html']`.

## 2. Scorer path (observed, anchors re-checked one by one)

- Imports of `helper_functions` at `18–27`; no call path reaches them for this case.
- `StringEvaluator` `71–170`; `clean_answer` `80–86` (strip, one outer quote pair, lowercase); `exact_match` `90–94`; `must_include` `98–111` (`clean_ref in clean_pred` when `tokenize=False`); routed pre-clean of `pred` at `134`.
- `HTMLContentEvaluator` `244–333`; targets at `258`; score 1.0 at `260`; `func` URL branch `263–266` (false: all urls `last`); goto+sleep `271–273` (skipped by `target_url != "last"`); document-selector branch `279–294`; `str(page.evaluate(f"() => {locator}"))` at `289`; falsy reset `290–291`; `except Exception: selected_element = ""` `292–294`; helper-locator branch `296–299` (unused); `html.unescape` `303`; `exact_match` branch `305–310`; `must_include` branch `312–327` with split on `" |OR| "` at `316` and `tokenize=False` at `322`; multiply at `310`/`327`; return `333`.
- `EvaluatorComb.__call__` `341–352`: starts at 1.0 and multiplies per evaluator (`351`). One evaluator here, so the task score is the HTML score.
- Router `355–374`; `program_html` at `369–370` appends only `HTMLContentEvaluator`.

Consequence: the case score is the product of three deterministic DOM predicates, each 0/1. Any `page.evaluate` exception substitutes `""` and then fails closed (0), so a selector error alone zeroes the task independently of agent behaviour.

## 3. Intent → predicate completeness

| intent element | predicate | unchecked remainder |
|---|---|---|
| "Show the route" | none directly; route/instructions/URL never read | whether a route was computed or rendered |
| travel mode (not stated) | T1 engine `selectedIndex == "1"` via `exact_match` on `str(...)` | what index 1 means; default index on load |
| origin "SCS CMU in Pittsburgh" | T2 `route_from`.value contains `gates and hillman centers` and `pittsburgh`, case-insensitive substrings, both required | geocoding source; alternate spelling/feature name; free text vs map click |
| destination "location where Declaration … signed" | T3 `route_to`.value contains `independence hall` and `philadelphia`, same rules | feature identity beyond the substring; alternate display name |
| final answer / login / reset | not read | answer string (`reference_answers` null); login state; environment reset |

The build's checked/unchecked split reproduces from the code. The "swapping from and to makes T2 and T3 fail" claim is correct: swapped values cannot contain the other field's required literals.

## 4. Independent numeric/census checks (raw JSON only, no production import)

| claim | independent result |
|---|---|
| 812 tasks / 812 distinct IDs, 0–811 no gaps/dups | exact |
| 5 evaluator-type sets 325/66/282/10/129 | exact |
| 27 site/evaluator strata; 16 selected | exact |
| 651 `program_html` targets; 188 `exact_match` + 463 `must_include` | exact, disjoint |
| locator classes 105 full-page / 524 JavaScript / 22 helper | exact |
| target URL classes 238 `last` / 338 navigation / 75 helper | exact |
| string operator tasks 45 exact / 176 include / 118 fuzzy | exact (coexistence explains 339 > 325) |
| 17 routing tasks; index `"1"` = 11 tasks [356,737–741,757–760,762]; index `"2"` = 6 tasks [761,763–767] | exact; zero tasks expect `"0"` |
| unclosed routing selectors: 17 `route_from` + 17 `route_to`, 0 correctly closed variants (`[name="route_from"]`/`[name="route_to"]` absent) | exact |
| 356 is the minimum of stratum `(('map',),('program_html',))` = 15 tasks [356,369–373,757,758,761–767] | exact |
| persisted selection = first 16 lexicographic strata minima, in order | exact: [389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]; 356 is 0-based index 9 |
| selected cases omit OR/func/prep_actions; no `shopping` site | exact for all 16 |
| map-only tasks 109 (all require_login true, storage_state null, require_reset false); 128 tasks include `map` (all storage null) | exact; `109` matches the instrument's `SITE_SETS["map"]` (map-only) convention |
| intent_template_id 49 unique to 356 | exact |

## 5. Defects found in `build/Task356.md`

**D1 (real, bibliographic). The intent anchor is off by one line.**
The build says at line 19: `Intent (L11046): "Show the route from SCS CMU …"`. In the pinned bytes, 11046 is `"instantiation_dict": {}`; the `"intent"` value is on **11047** (`cat -A` confirmed). The object span 11036–11086 and the quoted text are exact. This directly undercuts the build's closing claim that "…anchors are complete." No semantic conclusion depends on it.

**D2 (minor, span/attribution imprecision).**
- `L304–310 calls exact_match`: 304 is blank; the branch is `305–310` (call 307–309, multiply 310).
- `HTMLContentEvaluator (L247–334)`: the class is `244–333`; 247 is `@beartype`, 334 is blank (method body 248–333).
- "`EvaluatorComb` multiplies the results (L348–352), so the final score is the product of the three target scores": the three target multiplications are at 310/327 **inside** `HTMLContentEvaluator`; `EvaluatorComb` (`348–352`) multiplies the single evaluator score. The final product statement is true; the attribution is loose.

**D3 (real, prose overreach). "The other routing tasks start from 'Carnegie Mellon University', not SCS" is false as written.**
Only 737–741 (template 94, sites `["wikipedia","map"]`) use that origin. The other 11 routing tasks start elsewhere: 757 "home of the 1980 Super Bowl champions", 758 "the big apple", 759 "the city where my E-commerce customer Sophia Young lives", 760 "Allentown, PA", 761 "Carnegie Science Museum", 762 "Carnegie Music Hall in NYC", 763–767 "401 Shady Ave, Pittsburgh". Inside 356's own stratum the other routing tasks are 757, 758, 761–767 — none starts from "Carnegie Mellon University". The surrounding point (T2's literal is narrower than the intent) survives; the sibling generalisation does not.

**D4 (completeness, not a false statement).** `require_reset: false` is recorded but its consequence is not analysed. Runtime-evidence item (b) asks for the default `selectedIndex` "on a fresh load", yet the task does not reset the environment; whether the harness reloads the map before evaluation is not in the pinned fixtures (the snapshot holds the raw task file, the scorer/helper bytes, LICENSE and manifest/selection metadata; no run loop). The mismatch is an unlisted assumption, not a claim of invalidity; labelled `[INFERENCE]` about harness semantics.

**D5 (minor incompleteness).** The mode census names 3 of the 11 index-`"1"` tasks (762, 759, 760). The index-`"2"` half is exhaustive. The inference "index 1 most likely means a car engine" remains supported by the named witnesses; the unstated 11/6 split weakens only the audit's precision, not its conclusion.

Not defects after checking: the "109 map tasks" figure matches the map-only site set (128 include `map`; all have null `storage_state`); `str(...)` of the numeric `selectedIndex` is `"1"`; the `except` at 292–294 does fail closed for these three locators; no helper/LLM path is reachable.

## 6. Decisive boundary / controls

**B1 — unstated travel-mode gate (356-specific and decisive).** The authored intent says only "Show the route"; T1 demands engine `selectedIndex == "1"`. A correct walking or cycling route scores 0. This is sharper than the sibling 759, whose intent explicitly says "driving time"; 356's mode requirement is not derivable from its intent. The build states this as limitation 1 and correctly does not claim invalidity. The option order/default are unobserved, so the static fork stays open.

**B2 — malformed-selector all-or-nothing gate.** T2/T3 selectors omit the closing `]` (`[name="route_from"`, `[name="route_to"`). Under `292–294`, if Chromium rejects the selector both targets are `""` and fail for **every** trajectory; if it tolerates the block, the two `.value` substring checks are satisfiable. Shared with 759/424 (34 locators / 17 routing tasks / 0 closed variants). The build states both branches and labels browser behaviour `[INFERENCE]`; that refusal is correct and is not overreach.

**B3 — literal spelling/feature gate (static, no runtime claim).** The required substrings are literal: `gates and hillman centers` excludes "Gates & Hillman", "Gates-Hillman Center", and a generic "Carnegie Mellon University" geocode; `independence hall` excludes "Independence National Historical Park". `html.unescape` can turn `&amp;` into `&`, which still does not create the word "and". The build's limitation 2 covers the building/CMU alternative but not the spelling variant; this is a predicate precision fact, not a confirmed defect.

**B4 — typing-only proxy.** If B2 is tolerated and T1's index is 1 (default or selected), typing the two literals scores 1.0 without any computed route. The build says "appears to satisfy" and lists the reference-trajectory check; that hedge is correct.

Controls: **C1** 356 is the minimum of the 15-member map-only `program_html` stratum and the 10th persisted case, so it is the intended representative, not a duplicate. **C2** the 11/6 engine-index census is a structural, population-wide control for the index-1 inference (none expect "0"). **C3** the unclosed-selector defect is not manufactured for the case: it is stratum-wide and the candidate's named trio {356,424,759} is exactly the selected-case intersection. **C4** all four pin digests equal the manifest, and the candidate hash equals the freeze.

## 7. Candidate case-specific language vs source

The frozen candidate mentions 356 only as: (a) the row "556,356,7,377 | … routing-field predicates …", (b) "Task356/759/424: the locators contain unclosed attribute-selector brackets in source. This audit does not infer browser rejection…", and (c) the persisted selected-ID list. All three are supported by the pinned bytes; (b) is discriminating (356/759/424 all have unclosed attribute selectors) and (c) reproduces exactly. No 356-specific candidate sentence turns an unobserved runtime condition into a success or failure.

Candidate meta-line citations re-checked on the pinned bytes and exact: `task0` eval object 18–28; `StringEvaluator:71–170`; `URLEvaluator:173–241`; `HTMLContentEvaluator:244–333`; `combination/router:336–374`; `S063` fuzzy/UA 146–208 with model `gpt-4-1106-preview` at 162/197 and keyword logic 169–173/204–208; string table 80–94, 134, 98–111/142–149, 150–169, 152–163/159, 187–239, 199–235, 258–333, 348–352/361–374, 271–301. The selection rule in `plans/round-28-claims.md:19` reproduces `selected-task-ids.json` exactly.

## 8. Unresolved (not claimed)

- Chromium/Playwright parse outcome for `[name="route_from"` / `[name="route_to"` (B2).
- Map front-end option labels/order and default `selectedIndex` (B1).
- Whether `div#content select.routing_engines` and the `route_from`/`route_to` inputs exist (possibly hidden) outside the directions view.
- Geocoder display strings for the Gates and Hillman Centers and Independence Hall features (`Gates & Hillman` vs "and" spelling).
- Reference-trajectory scores: correct driving route, walk/bike, swapped endpoints, typed-text-only.
- `require_reset: false` / browser-context carry-over semantics (run loop not pinned).
- Production instrument counters and selftest-21: producer claims, not re-exercised here; the numeric table above is an independent raw-byte census, not an instrument run.

## Verdict

Semantic case audit: **PASS-equivalent** — every target, operator, checked/unchecked clause, and the routing-stratum census reproduce from the pinned bytes, and the candidate's 356 language does not exceed source. Bibliographic/prose: the intent anchor is wrong (`L11046` → `11047`), two evaluator spans are imprecise (`304–310` → `305–310`; `247–334` → `244–333`), and the sibling-origin sentence in limitation 2 is false for 11 of the other 16 routing tasks. The audit's own "PASS … anchors are complete" claim is therefore not fully supported.

VERDICT: PARTIAL
