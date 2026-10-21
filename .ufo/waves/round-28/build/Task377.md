# Round 28 C1 case audit — WebArena task_id 377

Writer/seat: `KengakuR28.Task377-2` (read-only scout, author-side advice; not outside non-author closure).
Scope: one pinned static task spec plus the scorer code it routes to. No upstream import/exec/eval, no benchmark-site contact, no browser action, no install/update.

## Inputs (local pinned snapshot, opened 2026-10-21)

| File | sha256 (observed = manifest) | Upstream URL @ dce04686a56253aefba7b18a4fa0937cf1dc987b |
|---|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386f…37652` ✓ | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` | `e23edb39…00c22` ✓ | …/evaluation_harness/evaluators.py |
| `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` | `ec758da4…7e275` ✓ | …/evaluation_harness/helper_functions.py |

Located quotes (≤25 words):
- test.raw.json L11727: `"intent": "Find the resturants around CMU ArtPark Lab",`
- test.raw.json L11734: `"reference_url": "__MAP__/search?query=restaurants%20near%20CMU%20ArtPark%20Lab",`
- evaluators.py L215: `matching_rule = configs["eval"].get("url_note", "GOLD in PRED")`

Task 377 object: test.raw.json L11713–L11739 (`task_id` L11717; `eval_types` L11730–L11732; `reference_answers` L11733; `program_html` L11735; `url_note` L11736).

## Task spec (test.raw.json L11713–L11739)

sites `["map"]`; require_login `true`; storage_state `null`; start_url `__MAP__`; geolocation `null`; require_reset `false`; intent_template `Find the {{space}} around {{location}}` (template 59); instantiation `space="resturants"`, `location="CMU ArtPark Lab"`; eval_types `["url_match"]`; reference_answers `null`; program_html `[]`; url_note `GOLD in PRED`.
Template-59 siblings (all `url_match`, `GOLD in PRED`): 378, 379, 380, 381. Task 377 is the only task in the 812 raw tasks whose intent contains `resturant`, and the only task that mentions `ArtPark`.

## Routing → operator → target mapping

| Step | Source anchor | Behaviour for 377 |
|---|---|---|
| Router | evaluators.py L355–374 (`url_match` → `URLEvaluator()` L367–368) | `EvaluatorComb([URLEvaluator])`. Product of one score (L348–352). |
| Pred | L212 `pred = clean_url(page.url)`, `clean_url` L187–190 (only `rstrip("/")`) | **Final** `page.url` at evaluation time. The trajectory and last action are unused. |
| Ref | L213–214 split on ` \|OR\| `, then `clean_url` | One reference: `__MAP__/search?query=restaurants%20near%20CMU%20ArtPark%20Lab` (`__MAP__` replaced by the config generator before scoring; that generator is not in the pinned snapshot). |
| Rule | L215–216 → `GOLD in PRED` branch L216–236 | Other rules would raise at L238–239. They are not reachable here. |
| Base check | L192–197 `parse_url` = `netloc+path`; L218 returns a **str** for pred; L220–227 `ref_base_path in pred_base_paths` | Substring containment of `<map-host>/search` in the pred `netloc+path`. Scheme, port position and fragment are ignored, and so are any extra path characters after the reference path. |
| Query check | L196 `parse_qs`; L228–235 | Key `query` must contain a value **exactly equal** (case-sensitive, post-decode) to `restaurants near CMU ArtPark Lab`. Extra keys are allowed. Any of several repeated `query` values may match. |
| Score | L236 `base_score * query_score` | Binary 0/1. |
| Helpers | helper_functions.py L211–221 `PseudoPage` (only if the harness wraps the page; it overrides `.url`) | No helper or LLM judge is invoked: no `fuzzy_match`/`ua_match` (`reference_answers` is null) and no `program_html` targets. |

## Static parse probe (stdlib only)

Command: `python3 - <<EOF … EOF` (Python 3.14.8; `urllib.parse` only; placeholder host `map.invalid:3000`, no network). Output saved at `.ufo/waves/round-28/scratch/Task377/urlparse-probe.txt`. It replicates the L192–236 arithmetic on hypothetical final URLs. It does not import upstream code.

| Final-URL property (hypothetical) | Score |
|---|---|
| Exact reference; `+` instead of `%20`; extra `&k=v`; `#map=…` fragment; trailing `/` on path | 1 |
| Capitalised `Restaurants…`; all-lowercase `cmu artpark lab`; intent-literal `resturants`; `around` instead of `near`; singular `restaurant`; trailing space; location-only query | 0 (base 1, query 0) |
| Clicked into a result (e.g. `/node/<id>`) after a correct search | 0 |
| Unsubstituted `__MAP__` reference | Parses to netloc `''`, path `__MAP__/search`. Valid only after host substitution. |

## Checked vs unchecked

Checked: the final URL's host+path contains `<map-host>/search`, and the `query` parameter equals one literal phrasing, case-sensitively.

Unchecked:
- Whether any results render, whether they are restaurants, or whether they are near CMU ArtPark Lab.
- Whether the geocoder resolves "CMU ArtPark Lab" at all.
- The agent's answer string.
- Intermediate trajectory states. A correct search followed by any further navigation scores 0.
- Alternative valid strategies: a different phrasing, a category or nearby search after locating the place, or map panning.
- Login state, despite `require_login: true`, `storage_state: null`.

## Dynamic dependencies

- Runtime `__MAP__` host substitution, done by the config generator outside the snapshot.
- The harness's choice of `page` versus `PseudoPage` and its `url` (run harness not pinned).
- The map frontend's actual search URL scheme and encoding. `%20` and `+` both pass.
- The live geocoder data in the map instance.
- Browser `page.url` reflecting client-side history updates.

No LLM judge dependency.

## Potential validity limitation (task-specific; not a proven defect)

The scorer accepts one literal, case-sensitive query phrase, `restaurants near CMU ArtPark Lab`. That phrase differs from the intent's own wording (`resturants`, `around`). An agent that uses the intent's words, or another reasonable phrasing, could find restaurants and still score 0. Conversely, the right URL scores 1 even when the result list is empty or wrong, because the result content is never inspected. Whether this happens in practice is `[INFERENCE]` until the runtime evidence below exists.

## Runtime evidence required before calling 377 valid/invalid

1. The pinned config generator output: the substituted reference URL and the start URL.
2. The pinned run harness: how `page` / `PseudoPage.url` is supplied at scoring.
3. A captured map-frontend search URL format for a typed query (encoding, path, any extra parameters).
4. The geocoder response for the reference query in the benchmark's map data snapshot: does it return restaurants near CMU ArtPark Lab?
5. A trajectory distribution (human or agent) showing whether alternative phrasings or post-search navigation occur and score 0.

None of these were collected, by design. No site contact.

## Case row for L1

| task | sites | eval_types | operator/target | checked | unchecked | judge | dynamic deps | limitation | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 377 | map | url_match | `GOLD in PRED`: substring `<MAP>/search` in final netloc+path, AND `query` == `restaurants near CMU ArtPark Lab` exact, case-sensitive (evaluators.py L212–236) | final-URL path + one literal query value | results content and relevance, answer, trajectory, alternative strategies, login | none | `__MAP__` substitution, harness page/PseudoPage, frontend URL scheme, geocoder data | reference phrase ≠ intent wording; URL-only proxy for "find" | PARTIAL |

## Limitations

- This is static evidence from one bounded, non-random sample case. It is not browser-level truth.
- The config generator and run harness are absent from the snapshot.
- The probe models only the stdlib parse semantics.
- No claim of actual task invalidity.

Final scoped verdict: **PARTIAL**. The intent→evaluator mapping, anchors and checked/unchecked boundary are fully traced for case 377. Validity cannot be determined without runtime items 1–5. This verdict covers case 377 only. It is not a round-level PASS.

## Erratum — 2026-10-21 (appended; text above preserved unchanged)

Original receipts: this report as reviewed, sha256 `ecca67cd0fe0db3bf982aabbe9df80be2870fd816b42acd8e5cd30def04d82af`. Original probe `scratch/Task377/urlparse-probe.txt`, sha256 `34876e23faa99a4a4298636e0102faac6dfad0dc3bcb4ddd193164a55d3d0b0b` (unmodified).
Trigger: `.ufo/waves/round-28/falsify/FTask377.md` §5 D1–D5 and §6 B1–B4. Falsifier controls: `scratch/FTask377/probe.py` `cd24ca8a…c8480f6`, `probe.out.txt` `3791b0c5…42bd6e7`.
Fresh labelled controls: `scratch/Task377/erratum-probe.py` `487f3c0f9f821ab039c4cecd77554f1693699eab38452271641a77f7a0b16f06` and `erratum-probe.out.txt` `c4a14b6d89f1bc41a3ec3d514be6bfb4e8be9f3e96f274542d7b4d6970ecca21`. These are stdlib only, with no upstream import, no network and no refetch.

Accepted corrections:
- **D1.** Withdrawn: "Scheme, port position and fragment are ignored." The correct statement is that scheme and fragment are ignored, but host **and port** are part of the compared `netloc+path` substring (evaluators.py L195, L223). Controls: https gives 1; port 3001 gives 0; omitting the port gives 0.
- **D2.** Withdrawn: "A correct search followed by any further navigation scores 0." Only the final `page.url` is read (L212). Navigation that keeps the `<host:port>/search` substring and the exact `query` value scores 1, e.g. `&zoom=12#map=…`. Navigation that loses either one scores 0, e.g. `/node/123`.
- **D3.** Rephrased: L218 unpacks `(pred_base_paths, pred_query) = parse_url(pred)`. `parse_url` returns `tuple[str, dict]` (L192, L195–197), so `pred_base_paths` is the string used by the L223 `in` test.
- **D4.** Cause corrected: no helper or LLM judge runs because the router appends only `URLEvaluator` for `eval_types: ["url_match"]` (L361–368). The cause is not that `reference_answers` is null. A routed `StringEvaluator` would raise at L137 on `None.items()`.

D5 is partly accepted:
- **Arithmetic: no error found.** The original heredoc printed `int(base*q), int(base), int(q)`, i.e. the column order is (product, base, query). Read in that order, row 17 `0 0 1` for `/prefix/search` is product 0, base 0, query 1. The labelled re-run gives the same row (`orig:17 prefix path 0 0 1`). The falsifier read the columns as (query, base, product). That reading agrees with mine on every row except this one, the only row where query ≠ product.
- **Fidelity: withdrawn.** I withdraw the claim that `urlparse-probe.txt` replicates the L192–236 arithmetic, because the artifact lacks column labels and its source was not saved. Use `erratum-probe.py` / `erratum-probe.out.txt`, plus the falsifier's controls, as the probe evidence. Also note that the original probe's query loop used one `any` across keys rather than the L229–235 per-key product. That is equivalent only because this reference has a single key.

Corrected L1 row cells:
- **operator/target:** substring `<MAP host:port>/search` in the final netloc+path, AND `query` == `restaurants near CMU ArtPark Lab` exactly and case-sensitively (L212–236). Scheme and fragment are ignored.
- **unchecked:** adds "navigation path; only the final URL counts".
- **dynamic deps:** adds the exact `__MAP__` substitution form (host, port, trailing slash), which decides pass or fail (falsifier B4).

Verdict unchanged: **PARTIAL** for case 377 only. Validity cannot be determined without runtime items 1–5. No production, candidate or pinned-input edits, and no installs.
