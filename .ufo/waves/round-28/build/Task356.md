# Task356 — C1 case audit, WebArena task_id 356 (author-side)

Writer/seat: KengakuR28.Task356-2 (read-only scout seat; author-side advice, not outside closure).
Scope: one static task-spec/scorer audit of task 356 in the pinned snapshot. It is not a task-validity verdict, a benchmark-wide claim, or a browser-level result. No upstream code was executed, imported or evaluated, no benchmark site was contacted, and no tool was installed or updated.

## Inputs (pinned, hash-verified locally)

| File (under `plans/fixtures/r28/webarena/`) | sha256 (observed = manifest) | Pinned URL (manifest; opened as local snapshot 2026-10-21) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…37652` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…0c22` | …/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…5275` | …/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py |

Commands observed: `sha256sum` on the three files (all matched `manifest.json`); `jq` selections of task 356 and of the map-site and routing-locator strata; `sed`/`grep -n` for line anchors. All of these were read-only.

## Task spec (test.raw.json lines 11036–11086)

- `task_id` 356, `sites` `["map"]`, `start_url` `__MAP__`, `require_login` true, `storage_state` null, `require_reset` false, `geolocation` null, `intent_template_id` 49 (used only by this task), `instantiation_dict` `{}`.
- Intent (L11046): "Show the route from SCS CMU in Pittsburgh to the location where the Declaration of Independence and Constitution were signed".
- `eval_types` `["program_html"]`; `reference_answers` null; `reference_url` null; no `string_note`, `url_note` or `prep_actions`.

## Intent → evaluator mapping

Routing: `evaluator_router` (evaluators.py L355–374). For `"program_html"` it adds `HTMLContentEvaluator()` (L369–370). `EvaluatorComb` multiplies the results (L348–352), so the final score is the product of the three target scores below. Each target is 0 or 1.

| # | Intent element | url / locator (raw JSON line) | Operator → target | Scorer path |
|---|---|---|---|---|
| T1 | Travel mode, which the intent never states | `last`, `document.querySelector("div#content select.routing_engines").selectedIndex` (L11058) | `exact_match` → `"1"` | L270–273: `last` means no navigation. L279–294: JS evaluate, then `str(...)`; an exception gives `""`. L303: `html.unescape`. L304–310 calls `exact_match` (L90–94, `clean_answer` strips, removes surrounding quotes, lowercases) |
| T2 | Origin "SCS CMU in Pittsburgh" | `last`, `document.querySelector('[name="route_from"').value` (L11065) | `must_include` → `["Gates and Hillman Centers", "Pittsburgh"]` | L312–327: each item is split on ` \|OR\| ` (no OR here). `must_include(tokenize=False)` (L98–111) does a lowercase substring test, and the per-item scores are multiplied |
| T3 | Destination, the signing place of the Declaration and Constitution | `last`, `document.querySelector('[name="route_to"').value` (L11075) | `must_include` → `["Independence Hall", "Philadelphia"]` | Same as T2 |

What `"1"` means: across the 17 routing tasks in the snapshot, index 1 goes with task 762 ("using driving options") and with tasks 759/760 ("driving time"). Index 2 goes with tasks 761 and 763–767 ("walk options"/"walkway"). So index 1 most likely means a car engine **[INFERENCE: this comes from co-stratum intents; the option order was not observed]**.

## Checked vs unchecked

**Checked (static):**
- On the final page, an element matching `div#content select.routing_engines` exists and its `selectedIndex` equals 1.
- The `route_from` input value contains "gates and hillman centers" and "pittsburgh", case-insensitively, as substrings in any order.
- The `route_to` input value contains "independence hall" and "philadelphia", under the same rules. Swapping from and to makes T2 and T3 fail.

**Unchecked:**
- Whether a route was actually computed or rendered. Nothing checks the route line, distance/time, instructions or the page URL.
- Whether the input values come from a geocoded selection or are free text the agent typed.
- That the destination is the intended feature. The substring test is the only constraint, and extra text is allowed.
- The meaning of the travel mode (only the index is compared).
- The agent's final answer. `trajectory`/`last_action` is not read by `HTMLContentEvaluator` (L247–334).
- Login state. `require_login` is true but `storage_state` is null, which is the same for all 109 map tasks.

## Dynamic state and judge dependencies

- The result depends entirely on the live DOM of the last page (`url: "last"`). That makes it depend on the map instance's frontend version (element ids/classes, engine option order) and its geodata (the exact OSM names "Gates and Hillman Centers" and "Independence Hall").
- No LLM judge is used. `llm_fuzzy_match`/`llm_ua_match` are unreachable for this task.
- No helper function from `helper_functions.py` is called. The module is only imported at evaluators.py L18–27, and nothing uses `func:` (no `eval` path at L263–266/L296–299). No network or API calls are made by the scorer.
- Because of the broad `except` at L292–294, a missing element or a thrown selector error turns into the empty string `""`, and the target scores 0. This happens silently.

## Potential validity limitations (task-specific; not proven defects)

1. **The required mode is not stated.** T1 requires index 1 (most likely driving). The intent only says "Show the route", so an agent that picks walking or cycling fails even if it shows a correct route. If the instance preselects index 1 by default, T1 instead passes vacuously. Neither the default nor the option order was observed.
2. **"SCS CMU" maps to only one building.** T2 accepts only "Gates and Hillman Centers". An origin geocoded to another SCS building, or a generic "Carnegie Mellon University" result, would fail even though it is a plausible reading of the intent. The other routing tasks start from "Carnegie Mellon University", not SCS.
3. **The selectors are malformed.** The T2 and T3 locators lack the closing `]` (`'[name="route_from"'`). This form appears in all 17 routing tasks (356, 737–741, 757–767); no correctly closed variant exists. If the browser's `querySelector` throws on it, both targets always score 0 because of the L292–294 catch, and the task becomes unpassable. If the browser's CSS error recovery closes the bracket at end of input, the locator works. **[INFERENCE: browser behaviour was not observed.]**
4. **The proxy is weak.** Typing the two strings into the inputs, with no route computed, appears to satisfy T2 and T3.

## Runtime evidence needed before calling 356 valid or invalid

None of this can be obtained without running the benchmark environment, which this round forbids. It would need to be gathered on a sanctioned offline instance by a separate, authorised seat:

- (a) Whether the pinned browser (Playwright Chromium) evaluates the unclosed `'[name="route_from"'` selector or throws a SyntaxError.
- (b) The option labels and their order in `select.routing_engines` on the pinned map image, plus the default `selectedIndex` on a fresh load.
- (c) Whether `div#content select.routing_engines` and the `route_from`/`route_to` inputs exist (possibly hidden) outside the directions view.
- (d) The geocoder display strings for the Gates and Hillman Centers and Independence Hall features in the instance's OSM extract.
- (e) Reference-trajectory scores: a correct driving route must score 1, and walk/bike, swapped endpoints and typed-text-only runs should be recorded.

## Compact case row for L1

| task | sites / eval_types | targets (operator → value) | judge / helper / dynamic | key limitation | static audit | validity |
|---|---|---|---|---|---|---|
| 356 | map / program_html | T1 `selectedIndex` exact_match "1"; T2 `route_from.value` must_include {Gates and Hillman Centers, Pittsburgh}; T3 `route_to.value` must_include {Independence Hall, Philadelphia} | none / none / last-page DOM, frontend version, geodata | mode not stated but index 1 required; unclosed `[name=...` selector (17-task stratum); SCS mapped to a single building; no check that a route was computed | complete | undetermined, needs (a)–(e) |

Limitations: the analysis is static and covers one case. The index→mode reading and all browser behaviour are inference. Line numbers refer to the pinned files. This report is not endorsement of any source, and it adds no source row or knowledge.

**Final verdict (scoped to the static case audit of task 356): PASS.** The intent→operator/target mapping, checked/unchecked properties, dependencies and anchors are complete. Whether task 356 is valid is left **undetermined**: no defect is claimed.
