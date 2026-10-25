# FTask377 — author-side falsification of BUILD case377 (WebArena task_id 377)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`

- Target under test: `.ufo/waves/round-28/build/Task377.md` (original reviewed SHA256 `ecca67cd0fe0db3bf982aabbe9df80be2870fd816b42acd8e5cd30def04d82af`; the author's 2026-10-21 erratum appends text, current SHA256 `f16a7c8dd5b574a4a64da6c1f3031cbfa9d57b29115442d67c815db0da8bbb09` — see §5 D5 correction).
- Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 377, L11713–L11739.
- Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`. Candidate SHA256 recomputed 2026-10-21: `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — equals the frozen value.
- Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md`: **not admitted, ENOENT** (`ls` observed). Not read, not written.
- Scope: case 377 only; static pinned bytes. No C2, no other case audit, no production edit.

## 0. Method and provenance

- Read-only over production. No installs or updates (tool log: none). No browser, no benchmark-site request, no upstream Python import/execute/eval, no REA MCP, no production instrument import or run.
- Bytecode disabled (`python3 -B`, `PYTHONDONTWRITEBYTECODE=1`). No command wrote outside `.ufo/waves/round-28/scratch/FTask377/` and this report.
- Commands used: `sha256sum`, `wc -c`, `nl -ba`/`sed -n` on pinned bytes, and two stdlib-only Python probes in my own scratch. No alternate oracle imported before deriving.
- Own scratch evidence: `.ufo/waves/round-28/scratch/FTask377/probe.py` (`cd24ca8a…c8480f6`), `probe.out.txt` (`3791b0c5…42bd6e7`), `census.out.txt` (`75b5fe07…67edd962`). `probe.py` reimplements only L187–236 with `urllib.parse`; it does not import upstream code.

Pin (all recomputed values equal `manifest.json`):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

Upstream revision in the manifest: `dce04686a56253aefba7b18a4fa0937cf1dc987b`; source URL root `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/`, accessed 2026-10-21. The build's truncated digests `7b50386f…37652`, `e23edb39…00c22`, `ec758da4…7e275` match these full hashes' suffixes.

## 1. Raw case 377 (observed, line-exact)

| field | value | line |
|---|---|---|
| block open / close | `{` … `},` | 11713 / 11739 |
| sites | `["map"]` | 11714–11716 |
| task_id | `377` | 11717 |
| require_login / require_reset | `true` / `false` | 11718 / 11728 |
| storage_state | `null` | 11719 |
| start_url | `__MAP__` | 11720 |
| geolocation | `null` | 11721 |
| intent_template | `Find the {{space}} around {{location}}` | 11722 |
| instantiation_dict | `space="resturants"`, `location="CMU ArtPark Lab"` | 11723–11726 |
| intent | `Find the resturants around CMU ArtPark Lab` | 11727 |
| eval_types | `["url_match"]` | 11730–11732 |
| reference_answers | `null` | 11733 |
| reference_url | `__MAP__/search?query=restaurants%20near%20CMU%20ArtPark%20Lab` | 11734 |
| program_html | `[]` | 11735 |
| url_note | `GOLD in PRED` | 11736 |
| intent_template_id | `59` | 11738 |

Located quotes (≤25 words, 2026-10-21, raw `dce04686`):

- `"intent": "Find the resturants around CMU ArtPark Lab",` — test.raw.json L11727.
- `"reference_url": "__MAP__/search?query=restaurants%20near%20CMU%20ArtPark%20Lab",` — test.raw.json L11734.
- `matching_rule = configs["eval"].get("url_note", "GOLD in PRED")` — evaluators.py L215.
- `ref_base_path in pred_base_paths` — evaluators.py L223.

Every build §1 anchor (L11713–L11739; task_id L11717; eval_types L11730–L11732; reference_answers L11733; reference_url L11734; program_html L11735; url_note L11736) is exact.

## 2. Scorer path (all anchors verified one by one)

`evaluators.py`:

- Router `355–374`; `case "url_match": evaluators.append(URLEvaluator())` at `367–368`; returns `EvaluatorComb` at `374`. `EvaluatorComb.__call__` `341–352`: starts `score = 1.0` at `348`, multiplies at `351`; one evaluator means the final task score is the URL score.
- `URLEvaluator.__call__` `177–241` (class starts `173`). `trajectory` and `client` occur only in the signature; neither is read. `pred = clean_url(page.url)` at `212` is the only agent-derived input.
- `clean_url` `187–190`: `str(url)` then `rstrip("/")`; no other normalization.
- Reference: `configs["eval"]["reference_url"].split(" |OR| ")` at `213`, then `clean_url` at `214`; task 377 has one alternative, so no OR handling is exercised.
- `matching_rule` at `215`; `if matching_rule == "GOLD in PRED":` at `216`; `else: raise ValueError(...)` at `238–239`. The task's explicit note is the matching literal, so the raise is unreachable here.
- `parse_url` `192–197`: `urllib.parse.urlparse` (`194`), `base_path = parsed_url.netloc + parsed_url.path` (`195`), `query = urllib.parse.parse_qs(parsed_url.query)` (`196`), returns `(base_path, query)` (`197`).
- Base check `217–227`: `ref_base_paths, ref_queries = parse_urls(ref_urls)` (`217`), `pred_base_paths, pred_query = parse_url(pred)` (`218`), `base_score = float(any([ref_base_path in pred_base_paths ...]))` (`220–227`).
- Query check `228–235`: `query_score = 1.0` (`228`); for each reference key, `query_score *= float(any(possible_ref_value in pred_query.get(k, []) ...))` (`229–235`).
- Score `236`: `score = base_score * query_score`; return `241`.
- `helper_functions.py` `PseudoPage` `211–221` (`self.url = url` at `213`); it would override `.url` only if the unpinned harness wraps the page, and no helper or LLM function is reached by this case. `StringEvaluator` (`71–170`) and `HTMLContentEvaluator` (`244–333`) are never routed because `eval_types` is exactly `["url_match"]`.

## 3. Intent → predicate completeness

| intent element | scorer predicate | checked? |
|---|---|---|
| "Find" (discovery) | no result/route/answer predicate; only a URL string | no |
| "resturants" (typo) | not checked; the reference value spells `restaurants` | no — different literal token |
| "around" | not checked; the reference value spells `near` | no — different literal token |
| "CMU ArtPark Lab" | only inside the exact decoded `query` value; no geocoder or place-identity check | no independent check |
| results render / are restaurants / are near the place | no program_html target; `program_html: []`; no DOM read | no |
| answer string | no `string_match`; `reference_answers: null` | no |
| login state | no evaluator reads authentication; `require_login: true` is a harness flag only | no |
| intermediate trajectory | unused; only final `page.url` at `212` | no |
| alternative strategies (other phrasing, category search, panning) | only the literal reference URL passes | no |

The case's checked/unchecked split is therefore complete in substance: one URL path substring plus one exact decoded query value are checked; everything semantic is unchecked. The build's central limitation — intent wording (`resturants`, `around`) differs from the reference literal (`restaurants`, `near`), and an empty/wrong result list still scores 1 — reproduces exactly (controls B3 below).

## 4. Independent census and numeric checks

Derived directly from the pinned JSON; no production/alternate oracle imported (`census.out.txt`).

| claim (build or candidate) | independent result |
|---|---|
| raw tasks 812 / distinct IDs 812 / IDs 0–811, no missing | exact (`tasks 812 distinct_ids 812 id_min 0 id_max 811 missing_ids []`) |
| template-59 siblings 378, 379, 380, 381; all `url_match`, `GOLD in PRED` | exact; template 59 = {377, 378, 379, 380, 381}, all five `url_match` / `GOLD in PRED` |
| 377 is the only task whose intent contains `resturant` | exact; also the only task where `resturant` occurs in any string field |
| 377 is the only task that mentions `ArtPark` | exact over all string fields (case-insensitive scan: intent, instantiation, reference_url only) |
| selection: 27 strata, sorted-minimum rule → persisted 16 | exact; rule output `[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]` equals `selected-task-ids.json`; 377 is rank 11 (12th) and the minimum of stratum `(('map',),('url_match',))` = {377, 378, 379, 380, 381} |
| candidate evaluator-set histogram 325/66/282/10/129 | exact; 205 tasks contain `url_match` (66 alone + 10 + 129) |
| 16 selected case reports exist | exact; all 16 files present under `build/` (`Task044.md`, `Task007.md` zero-padded; rest as named) |
| build probe output rows | 15 of 16 score rows reproduce under the artifact's (query, base, product) column order; `urlparse-probe.txt:17` (`/prefix/search`) prints `0 0 1` where the arithmetic gives `1 0 0` (D5). The two parse lines (`raw-unsubstituted`, `ref`) match. **Corrected 2026-10-21:** the receipt's actual order is (product, base, query); under it all 16 rows are consistent — see §5 D5 correction. |

## 5. Defects found in the build report

**D1 (real, behavioral description). Build line 34: "Scheme, port position and fragment are ignored."** The port is not ignored. `parse_url` builds `netloc + path` (L195), and the base check is `ref_base_path in pred_base_paths` (L223); `netloc` includes the port, so the reference netloc must appear as a substring, port included. Controls (same path and exact query): `https` instead of `http` → 1; `#fragment` → 1; port `3001` instead of `3000` → 0; default port omitted → 0; different host → 0. The build's own probe uses `map.invalid:3000` as `<map-host>`, so the phrase is also internally inconsistent. Correct statement: scheme and fragment are ignored; host **and port** are compared as part of the substring. No deployed host/port mismatch is claimed (the substitution is unpinned), so this is a description defect, not evidence of task failure.

**D2 (real, behavioral universal). Build line 58: "A correct search followed by any further navigation scores 0."** Only the final `page.url` is read (L212). A further URL update that still contains the reference path and the exact `query` value scores 1: extra query key (`&foo=1`) → 1; `&zoom=12#map` → 1; a repeated `query` value → 1; a percent-encoded spelling of the same value → 1. Only navigation that loses the path substring or the exact value scores 0 (`/node/123` → 0, `/prefix/search` → 0, missing query → 0). The build's own probe line "extra `&k=v` … 1" already contradicts the universal. Correct statement: navigation away from a URL that satisfies the base+query predicate scores 0; harmless URL updates do not.

**D3 (minor, phrasing). Build line 34: "L218 returns a str for pred."** L218 is `pred_base_paths, pred_query = parse_url(pred)`; `parse_url` returns `tuple[str, dict[str, list[str]]]` (L192, L197), and `pred_base_paths` is the string. The semantic point (substring test) is unchanged.

**D4 (minor, causal). Build line 37: "No helper or LLM judge is invoked … (`reference_answers` is null)."** The reason is that `eval_types: ["url_match"]` makes the router append only `URLEvaluator` (L361–368); `StringEvaluator` is never constructed. If a `StringEvaluator` were routed with `reference_answers: null`, it would raise at L137 (`configs["eval"]["reference_answers"].items()`) rather than skip. The observation "no helper/LLM judge is invoked" is true; the parenthetical explanation is not.

**D5 (minor, cited evidence artifact). Build line 41 says the probe "replicates the L192–236 arithmetic on hypothetical final URLs." One row does not: `scratch/Task377/urlparse-probe.txt:17` prints `0 0 1 /prefix/search?query=restaurants%20near%20CMU%20ArtPark%20Lab`. The case's table line 46 fixes the intended component order as "base 1, query 0" for value-only misses, so the artifact's first two columns are (query, base); for `/prefix/search` the computed triple is query 1, base 0, product 0 (`1 0 0`), not `0 0 1`. No case-table row or conclusion uses the prefix case, and the case's prose only claims extra characters *after* the reference path, so this is an evidence-file defect, not a semantic-claim defect.

**Correction — 2026-10-21 (appended to D5; the paragraph above is preserved).** The author's erratum at `build/Task377.md:101–115` (current SHA256 `f16a7c8dd5b574a4a64da6c1f3031cbfa9d57b29115442d67c815db0da8bbb09`; the review above applied to the original `ecca67cd…04d82af`) records that the original heredoc printed `int(base*q), int(base), int(q)` — i.e. the receipt's column order is **(product, base, query)**, not (query, base, product). The receipt itself has no column header, so my D5 inference of an arithmetic error is **withdrawn: no arithmetic error is established from the unlabeled columns.** Independent focused recheck (`scratch/FTask377/correction-probe.py` `6d0208da…28590e1ce`, `correction-probe.out.txt` `83dd5943…8d3581a05`): under (product, base, query) all 16 score rows of `urlparse-probe.txt` are consistent, including L17 `0 0 1` = product 0, base 0, query 1. The author's labelled controls (`scratch/Task377/erratum-probe.py` `487f3c0f…0a0b16f06`, `erratum-probe.out.txt` `c4a14b6d…6970ecca21`) show the same order. What remains is **provenance/fidelity, which the original receipt still does not support:** it lacks column labels and its generating source was not saved; the erratum itself withdraws the claim that it replicates L192–236 and notes the original query loop used one `any` across keys rather than the L229–235 per-key product (equivalent here only because the reference has a single `query` key). The labelled re-run is a new artifact, not the original receipt. D5 is therefore downgraded to a documentation/provenance defect, not an arithmetic inconsistency; this supersedes §4's "15 of 16" phrase and the D5 clause in the Verdict. D1/D2 (accepted in the same erratum) and the candidate's 377 language are unchanged.

Not defects after checking: all raw line anchors and ranges; the digest truncations; "the trajectory and last action are unused" (true; `trajectory` is only a parameter); "PseudoPage L211–221 … overrides `.url`" (class ends at 221; `self.url = url` at 213); the "only task" and sibling claims; the "one reference" claim; the `__MAP__`-generator-absence claim; the probe's two parse lines and all 16 score rows under the receipt's actual (product, base, query) order (see D5 correction). The `__MAP__` substitution step itself is outside the pinned bytes and the build labels it a dynamic dependency; B4 shows why its exact form is pass/fail-decisive, not merely cosmetic.

## 6. Decisive boundaries / controls

**B1 — netloc (host and port) is the real base boundary; scheme and fragment are not.** With everything else identical, changing only the port flips the score 1↔0; changing only the scheme or adding a fragment does not. This is the boundary the build's "port … ignored" sentence misstates.

**B2 — final-URL-only boundary.** The trajectory is irrelevant. A correct search followed by a URL update that preserves `<host>/search` and the exact `query` value still scores 1 (`&foo=1`, `&zoom=12#map`, repeated query, percent-encoded letters); navigating to a result path (`/node/123`) scores 0. This is the precise form of the build's overbroad "any further navigation" sentence.

**B3 — intent literal vs reference literal (the case's central limitation).** `query=resturants%20around%20CMU%20ArtPark%20Lab` (the intent's own words) → base 1, query 0, score 0; `query=restaurants%20near%20CMU%20ArtPark%20Lab` (the reference) → 1. Capitalised, singular, and trailing-space variants also score 0. This decisively confirms the case's "reference phrase ≠ intent wording; URL-only proxy" limitation.

**B4 — substitution exactness.** With the reference built by substituting `__MAP__`: a host with a trailing slash (`http://map.invalid:3000//search?...`) yields base `map.invalid:3000//search` and score 0; an unsubstituted reference yields base `__MAP__/search` and score 0; a changed port yields 0. The build's runtime-evidence item 1 (exact substituted reference URL and start URL) is therefore pass/fail-decisive, not just informational.

## 7. Candidate case-specific language vs source

- Candidate SHA256 is the frozen `77e19d5b…ac20a8`; canonical path not admitted.
- 377 appears in the candidate at L60 (persisted selected IDs), L72 (case-table row "377 … literal search query"), and is covered by the URL row at L34.
- "literal search query": supported. The URL evaluator checks one decoded literal value with exact, case-sensitive membership (L229–235) after a substring base check (L220–227). The candidate does not claim exact URL identity.
- URL row "uses netloc+path substring containment, ignores scheme/fragment": supported; it does **not** repeat the build's port error or the "any further navigation" universal. No case-377-specific candidate sentence turns an unobserved runtime condition into success/failure, and no candidate 377 language exceeds source.
- Adjacent candidate line ranges checked against pinned bytes: `S062:187–239` (clean_url through the `GOLD in PRED` raise), `199–235` (parse_urls/pooling), `348–352` (product), `361–374` (router), `URLEvaluator:173–241`, `HTMLContentEvaluator:244–333`, `combination/router:336–374`, `StringEvaluator:71–170`, `S063:146–208` — all exact.
- Candidate counts relevant to 377's stratum and population (812/66/10/129/27/16) reproduce exactly; the 16 selected IDs and their order equal the rule output.
- This assessment is tied to candidate SHA256 `77e19d5b…ac20a8`; any byte change requires a fresh same-identity reread before admission.

## 8. Unresolved (not claimed)

- The unpinned run harness: whether scoring receives `page` or `PseudoPage`, and what `.url` holds at that point.
- The config generator's exact substitution output (host, port, trailing slash) and whether it is identical for `start_url` and `reference_url`.
- The map frontend's real search path/encoding and whether it rewrites `page.url` via history.
- The live geocoder's response for `restaurants near CMU ArtPark Lab`.
- A trajectory distribution (human/agent) showing alternative phrasings or post-search navigation.
- The production instruments `plans/benchmark_spec_audit.py` and `plans/registry_check.py` were **not** run by this seat; the JSON-derivable counters and the URL predicate arithmetic above were recomputed independently from the pinned bytes.

## Verdict

The intent→predicate trace, every raw/scorer line anchor, the census/numeric claims, the selection membership, and the case's central validity limitation reproduce from the pinned bytes. The candidate's case-377 language is source-supported and does not exceed the source. Two behavioral descriptions in the original build report are false — D1 (port treated as ignored; it is part of the compared netloc) and D2 ("any further navigation scores 0"; only a final URL that fails the base+query predicate does) — and the original probe receipt is unlabeled with its generating source unsaved (D5; the earlier arithmetic-error reading is withdrawn on recheck — see §5 correction), with D3/D4 as minor phrasing/causal imprecisions. These do not overturn the build's own PARTIAL task-validity verdict, which remains undetermined on runtime evidence 1–5. No production edits; L1 resolves.

VERDICT: PARTIAL
