# Scratch notes — KengakuR28.RevRouterMix-2 (round 28, reviewer: evaluator_router / EvaluatorComb)

Seat: reviewer (read-only). Only writes: this scratch dir + `.ufo/waves/round-28/build/RevRouterMix.md`.
No tool installs/updates. No upstream code imported/executed. No network access performed by this seat.

## Inputs verified (sha256sum, 2026-10-21)

| file | sha256 (first8…last8) | matches |
|---|---|---|
| config_files/test.raw.json | 7b50386f…537652 | manifest ✓ |
| evaluation_harness/evaluators.py | e23edb39…e00c22 | manifest ✓ |
| evaluation_harness/helper_functions.py | ec758da4…97e275 | manifest ✓ |
| LICENSE | c71d239d…35d0ab4 | manifest ✓ |
| manifest.json | c78b1478…23a6dd | instrument MANIFEST_SHA256 pin ✓ |
| selected-task-ids.json | 5f7eea2e…f3ed17a | instrument SELECTION_SHA256 pin ✓ |

`selected-task-ids.json` content = [389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399] exactly.

## Commands observed

- `sha256sum` on the 4 snapshot files, manifest.json, selected-task-ids.json.
- `python3` (stdlib only) read-only parse of test.raw.json — census script in `census.py`, outputs below.
- `grep -n` counts on evaluators.py (client/get_last_state usage), `wc -l` + `grep -n` on plans/benchmark_spec_audit.py.
- `ls`/`mkdir -p` for scratch only.

## Census outputs (first-hand, frozen snapshot)

- total 812; task_id all int, 0..811 contiguous, 0 duplicates.
- eval_type chains: (string,) 325; (program_html,) 282; (url,program_html) 129; (url,) 66; (string,url) 10. No other combo, 0 empty, 0 in-task duplicates.
- Order uniformity: all 129 (url,html) are exactly ["url_match","program_html"]; all 10 (string,url) are ["string_match","url_match"].
- eval null fields: reference_answers null on 477 tasks; reference_url null on 7 (program_html-only tasks 118, 356, 369, 370, 371, 372, 373).
- Dead reference_url (non-empty, url_match not dispatched): task 247 (string-only), value `"Valorie doesn't have a email in the system"`.
- string tasks 335: reference_answers always dict; operators: exact_match 45, must_include 176, fuzzy_match 118 (82 list + 36 "N/A").
- must_include lists: 98 single-element (tokenize=True at call), 78 multi-element; 31 tasks take the token path (single-element AND single-char ref), e.g. 132 ["1"], 14 ["0"], 128 ["9"].
- fuzzy N/A: all 36 are single-key {"fuzzy_match":"N/A"} on string-only chains; all 36 have eval.string_note. N/A+other-approach configs: 0 (overwrite latent).
- eval.string_note present on 335 tasks, non-empty on 36.
- url tasks 205: reference_url always non-empty str; 7 with " |OR| " (604, 608, 609, 625, 681, 682, 683), all alternatives non-empty; url_note "GOLD in PRED" 196 explicit, 9 absent (default), 0 non-default.
- program_html targets 651: locator full_page 105 / javascript 524 / helper("func:") 22 / unsupported 0; target url last 238 / navigation 338 / helper("func" prefix) 75; required_contents must_include 463 / exact_match 188 / both 0 / neither 0; prep_actions present 10; html must_include " |OR| " items 5, all alternatives non-empty; empty exact_match "" 0; "" items 0.
- Selected-16 chains: 389 html; 590 url+html (3 targets); 132 string must_include ["1"]; 173 string+url (fuzzy list); 44 url; 552 html; 681 url+html (OR url, 1 target); 791 string fuzzy N/A; 556 html; 356 html (3 targets); 7 string exact; 377 url; 759 html (3 targets); 424 html; 97 string must_include ["914km"]; 399 html. Mixed representation: 590, 681 (url+html), 173 (string+url).
- Distinct (sites, sorted eval_types) strata: 27.
- Task 590: intent/instantiation "1/16/2023"/"1/30/2023" vs required_contents "Jan 16, 2030"/"Jan 30, 2030" (observable intent-vs-evaluator discrepancy; record, do not adjudicate).

## Cross-checks

- My counts match OpenScorer.md's independent parse exactly wherever both exist (combos, 27→five sets claim F2, string operators, N/A 36, url_note 196+9, 651 targets with 524/105/22 and 238/338/75 and 463/188, prep 10, OR 7+5).
- Instrument pins verified: manifest.json and selected-task-ids.json byte-digests equal the constants in plans/benchmark_spec_audit.py.

## Boundary note

Remote byte-equality of the snapshot to upstream dce04686 is attested by OpenScorer's fetch (its report); this seat verified only local-internal consistency (files ↔ manifest ↔ instrument pins).
