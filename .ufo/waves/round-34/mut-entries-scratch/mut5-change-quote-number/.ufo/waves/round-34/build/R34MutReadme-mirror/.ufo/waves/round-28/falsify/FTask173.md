# FTask173 — author-side falsification of BUILD case173 (WebArena task_id 173)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Target under test: `.ufo/waves/round-28/build/Task173.md` (writer `KengakuR28.Task173-2`).
Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 173, lines `5520–5550`.
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256 recomputed
2026-10-21 = `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (equals the frozen value).
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted** — file is absent
from the tree; it is the named prospective target only, never opened or edited by this seat.
Scope: case 173 only. No other case, no C2, no production edit, no delegation.

## 0. Method and provenance

- Read-only over production. No installs or updates (tool log: none). No browser, no benchmark-site
  request, no upstream Python import/execution, no REA MCP, no scorer run.
- Commands on the pinned snapshot only: `sha256sum`, `wc -c`, `grep -n`, `sed -n`, and stdlib-only
  `python3` (`json.load`, brace counting, `urllib.parse` re-derivation), `PYTHONDONTWRITEBYTECODE=1`.
- Scratch evidence (mine, never production):
  - `.ufo/waves/round-28/scratch/FTask173/predicate-probe.txt` — SHA256 `120ae501f4cfb81c51916821f0576d071fec9a10749efcf21ae6f5737d03f442`.
  - `.ufo/waves/round-28/scratch/FTask173/class-census.txt` — SHA256 `de641ced2e9e8c3d60e02c2fd30110239e9fa93f5c6b813aaf2d81738ebad6f0`.
- Both probes are hand re-statements of pinned source lines applied to raw JSON. They are **not**
  execution of `evaluators.py`/`helper_functions.py`; no upstream module was imported.

Pin (all recomputed values equal `plans/fixtures/r28/webarena/manifest.json`):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

Upstream URL (manifest, opened 2026-10-21): `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`.
LICENSE is Apache-2.0. The build's `e23edb39…e00c22` and `ec758da4…77e275` truncations are suffixes
of the full hashes; `7b50386f…0537652` is not (see D2).

## 1. Raw case-173 facts (observed, line-exact)

| field | value | line |
|---|---|---|
| block open / close | `{` … `},` | 5520 / 5550 |
| sites | `["gitlab"]` | 5521–5523 |
| task_id | 173 | 5524 |
| require_login / storage_state | `true` / `./.auth/gitlab_state.json` | 5525 / 5526 |
| start_url / geolocation | `__GITLAB__` / null | 5527 / 5528 |
| intent_template / instantiation_dict | `Open my latest updated issue … "{{keyword}}" …` / `{"keyword": "better"}` | 5529 / 5530–5532 |
| intent | `Open my latest updated issue that has keyword "better" in its title to check if it is closed` | 5533 |
| require_reset | `false` | 5534 |
| eval key / close | `"eval": {` … `},` | 5535 / 5548 |
| eval_types | `["string_match","url_match"]` | 5536–5538 |
| reference_answers | `{"fuzzy_match": ["No, it is open"]}` | 5540–5542 (fuzzy at 5541) |
| reference_url | `__GITLAB__/byteblaze/empathy-prompts/-/issues/8` | 5543 |
| program_html | `[]` | 5544 |
| reference_answer_raw_annotation / string_note | `Not closed` / `""` | 5545 / 5546 |
| url_note | `GOLD in PRED` | 5547 |
| intent_template_id | 310 | 5549 |

## 2. Scorer anchors (every build anchor verified on pinned bytes)

`evaluators.py`:

- Router `355–374`: `eval_types` 361, loop 363, `match` 364–372 (`string_match` 365–366,
  `url_match` 367–368, `program_html` 369–370, unknown raises 371–372). Build's `L361–372` exact.
- `EvaluatorComb` `336–352`: score 1.0 at 348, loop 349, `score *= cur_score` 351. Build's `L348–352` exact.
- `StringEvaluator` `71–170`: `clean_answer` `80–86` (strip 81, one outer `'`/`"` pair 82–85, `lower()` 86);
  `exact_match` `88–94`; `must_include` `98–111`; `fuzzy_match` `113–116`; `__call__` `123–170`
  (`last_action` 133, `pred = self.clean_answer(last_action["answer"])` 134, `case "fuzzy_match"` 150,
  `intent` 151, `value == "N/A"` branch 152–163, `else` 164, list loop `165–169`, return 170).
- `URLEvaluator` `173–241`: `clean_url` `187–190` (`rstrip("/")` 189); `parse_url` `192–197`
  (`netloc + path` 195, `parse_qs` 196); `pred = clean_url(page.url)` 212; split `" |OR| "` 213;
  `matching_rule` 215; `parse_urls(ref_urls)` / `parse_url(pred)` 217–218; containment `223`;
  `base_score` 220–227; query loop 228–235; `score = base_score * query_score` 236; unknown rule raises 238–239.

`helper_functions.py`:

- `llm_fuzzy_match` `146–173`: prompt 150–155, call 161–168 (`model="gpt-4-1106-preview"` 162,
  `temperature=0` 164, `max_tokens` 165, `top_p` 166, `context_length` 167), `.lower()` 168,
  `if "partially correct" in response or "incorrect" in response: return 0.0` 169–170,
  `assert "correct" in response` 172, `return 1.0` 173.
- `llm_ua_match` `176–208` (not reached by task 173).

Every anchor in the build's case table and state section is line-exact except the two bibliographic
items in §5. The build's semantic reading — the URL comparison is `ref_base_path in pred_base_paths`
with `pred_base_paths` bound to a **str** — is literally correct.

## 3. Intent → predicate completeness (build mapping reproduced)

| intent element | build claim | independent result |
|---|---|---|
| "Open … issue" | final `page.url` only | exact: `URLEvaluator` reads `page.url` (212); no trajectory navigation check |
| "my latest updated issue" | ordering/ownership unchecked | exact: no code reads `updated_at`, authorship or assignee |
| "keyword 'better' in its title" | title match unchecked | exact: no title predicate anywhere in the path |
| "check if it is closed" | LLM judge vs `No, it is open` via `intent` | exact: fuzzy branch 150/165–169 → helper 146–173, question = `configs["intent"]` |
| scheme/query/fragment | unchecked (ref has no query) | exact: `urlparse` drops scheme/fragment; empty `ref_queries` ⇒ `query_score = 1.0` (228) |
| both evaluators | product, string→URL | exact: router order = list order 363–372; `score *= cur_score` 351 |

No intent element is silently dropped, and no unchecked item is missing from the build's list.
The build's "checked" set (judge equivalence of the cleaned final answer; substring containment of
reference `netloc+path` in final `netloc+path`) is complete for the pinned path.

## 4. Independent numeric/census checks (raw JSON only)

| claim | source | independent result |
|---|---|---|
| 812 tasks / IDs 0–811 / no gaps | candidate | exact; 812 unique IDs, no missing/duplicate |
| evaluator-type sets 325/66/282/10/129 | candidate | exact: `{string_match}`325, `{url_match}`66, `{program_html}`282, `{string_match,url_match}`10, `{program_html,url_match}`129 |
| 27 strata; 16 selected | candidate | exact; sorted minima = `389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399` (equals `selected-task-ids.json`) |
| 173 is the sampled case of its stratum | candidate/build | exact: `(gitlab, string_match+url_match)` = {173…182} (10 tasks); 173 is minimum |
| string operators 45/176/118 | candidate | exact; task 173 is one of 118 `fuzzy_match` |
| 651 targets; 188 `exact_match` + 463 `must_include` | candidate | exact, with `elif` precedence |
| locators 105 full-page / 524 JS / 22 helper; URLs 238 last / 338 navigation / 75 helper | candidate | exact (recomputed independently) |
| template 310 = 173–177 | build | exact (5 tasks) |
| 178 different gold `a11yproject/a11yproject.com/-/issues/566`, exact "Yes", annotation "Closed" | build | exact; 178 is template 500, same stratum, not selected |
| empathy-prompts tasks = {173,175,180,393,659} | build | exact; 175/180 target issue 18 read-only; 393 posts on MR 19; 659 is the only creator |
| 659 title "Integrating LLMs for better prompts", assignee Roshanjossey | build | exact at 22406 / 22407; intent 22410; `require_reset: false` 22411 |
| build scratch `stdlib-semantics.txt` content/hash | build | exists; SHA256 `d4fb776b8a3ead50510e0db88b28d51fe4418fc2f0ec7d488c3353065115633c`; matches described output |

## 5. Defects found in the build report

**D1 (real, bibliographic — task span).** §"Dynamic state" cites "task 659 (L22398–22430)".
The block actually spans `22394–22449` (open `{` 22394; `intent_template_id: 327` 22448; close 22449).
The stated end 22430 falls inside the second `program_html` element; the range omits the block's
final 19 lines and its opening brace. The load-bearing anchors are exact: title 22406, account 22407,
`require_reset` 22411. No semantic conclusion depends on the span.

**D2 (real, bibliographic — digest suffix).** The input table reports
`7b50386f…0537652` for `test.raw.json`. The full observed hash ends `...02537652`, whose last seven
characters are `2537652`; the printed suffix `0537652` is not a suffix of the observed digest
(it is the first character of the last eight plus the last six). The full digest matches the manifest,
so the cell's "(match)" verdict is true; the displayed truncation is a transcription error.

**D3 (minor, non-load-bearing overstatement).** §"Task-specific potential validity limitation" says
the fixed gold `issues/8` **and** `"No, it is open"` can go stale. The URL half is source-supported:
659 creates an open issue titled with `better` in the same project, so if it runs first and counts as
"mine", the correct page is no longer issue 8 and the fixed URL gold rejects correct behavior (unless
the new number begins with `8`). The answer half is not established by the pinned population: the new
issue is created open and no pinned task closes any empathy-prompts issue, so `"No, it is open"`
remains the correct answer for the new issue. The build's next sentence and "Neither effect is shown to
occur" limit the overstatement; it does not change the central limitation.

**D4 (nuance, unmarked inference).** The table's "Target" for S1 is "final stop-action answer text".
`get_last_action` (`evaluators.py` 46–56) returns `trajectory[-1]` without checking action type; the
stop-action contract is implied only by the comment at 53 ("add a fake stop action if needed"). Reads
better as "the last trajectory action's `answer` field".

Checked, **not** defects: `eval (L5536–5548)` is the `eval_types`-through-closing-brace span (`"eval": {`
itself is 5535); `url_note` reading 215–216; the query `1.0` result; the placeholder-unsubstituted
control; the "PASS for the scoped deliverable / validity UNDETERMINED" split.

## 6. Decisive boundary / controls

**B1 — URL containment is the decisive acceptance boundary (case-specific).**
`evaluators.py` 218 binds `pred_base_paths` to the str `netloc+path`; 223 evaluates raw substr containment.
Re-derivation with task 173's exact reference (`http://<host>:8023/byteblaze/empathy-prompts/-/issues/8`)
and `ref_queries = {}`:

| final page tail (same host/path prefix) | URL score |
|---|---|
| `/issues/8`, `/issues/8/`, `/issues/8/edit` | 1.0, 1.0, 1.0 |
| `/issues/80`, `/issues/89`, `/issues/899` | 1.0, 1.0, 1.0 |
| `/issues/7`, `/issues/08`, `/issues` | 0.0, 0.0, 0.0 |
| `/issues/8?x=1`, `/issues/8#note_1` | 1.0, 1.0 |

Consequences (source-level, not runtime): a wrong issue in 80–89/8xx and the issue *edit* page pass the
URL branch; a different issue number does not. Query and fragment are ignored. Host is pinned only
because the reference netloc literally prefixes the concatenation; a foreign-host URL whose **path**
embeds `<ref netloc>/byteblaze/...` also scores 1.0 (contrived control, host substitution dependent,
[INFERENCE]). This boundary, not the LLM score, is what decides whether the final page "is" issue 8.

**B2 — judge parser boundary (deterministic given a response).** Helper 169–172: `correct` → 1.0;
`Correct` → 1.0; `partially correct` → 0.0; `incorrect` → 0.0; `not incorrect; correct` → 0.0;
`the issue is open` → AssertionError. Static bytes cannot decide which response the external model
returns, so the string branch is runtime-unverified — exactly as the build and candidate state.

**B3 — product boundary.** Router order 361–372 + product 348–352: task score = string × URL. A correct
answer that ends on a URL not containing the reference base scores 0; a wrong issue 80–89 scores 1.0 on
URL and passes only if the judge also returns 1.0. Both branches must be 1.0.

**C1 — selection control.** Independent 27-strata/minima recomputation reproduces the persisted 16 IDs
exactly; 173 is the minimum of {173…182}. The audited case is the intended stratum representative.

**C2 — population control.** The only pinned tasks mentioning `empathy-prompts` are 173, 175, 180, 393,
659; 175/180 open issue 18 (read-only), 393 posts on MR 19, 659 creates the issue. No pinned task closes
issue 8 or renames a `better` title, so the build's dynamic-state enumeration is complete for the pinned
file.

**C3 — build scratch re-check.** Re-read `scratch/Task173/stdlib-semantics.txt`; its hash and its
"not incorrect; correct → 0.0" and `/issues/80 → contains` lines match the build's description.

## 7. Candidate case-specific language vs source

Candidate mentions of 173 (line numbers in the frozen draft):

- line 70, case-table boundary "hosted fuzzy judge" — supported: the routed string branch (150, 165–169)
  calls `llm_fuzzy_match` (146–173), whose model call is external (161–168).
- line 85, "**Task173/791:** remote-judge-dependent branches remain runtime-unverified; exact N/A is a
  separate branch." — supported: 173's value is a list, so the fuzzy branch runs; the N/A branch (152–163)
  is not 173's path. The sentence claims non-verification, not task invalidity.
- line 60, selected-ID list contains 173 — reproduces exactly from the selection rule.
- The candidate's S062/S063 line ranges adjacent to 173 (`StringEvaluator:71–170`, `S062:150–169`,
  `S063:146–173`, and the helper/model ranges) are line-exact on the pinned bytes.

No candidate sentence about case 173 turns an unobserved runtime condition into a success/failure, and
none exceeds the pinned source. The candidate's aggregate counters re-derived in §4 also reproduce.

## 8. Unresolved (not claimed)

- GitLab dataset state: is issue 8 open; do any 80–89/800+ issues exist; which titles contain `better`;
  what "my" means for `gitlab_state.json` (authored vs assigned).
- The `__GITLAB__` substitution value and the per-task generated config actually fed to the scorer
  (whether the reference keeps a scheme, port, or trailing slash).
- Harness execution order and reset policy between 659 and 173.
- Judge availability, exact model build and logged responses; temperature 0 does not prove determinism.
- Whether the last trajectory element is a stop action carrying `answer`.
- No browser, site request, scorer run, or production-instrument run by this seat; schema-findings 0 and
  selftest 21 remain producer claims.

## Verdict

Semantic case audit: **PASS** — every target, operator, checked/unchecked clause and semantic line anchor
in `build/Task173.md` reproduces from the pinned bytes; the substring reading, product order, query
`1.0`, placeholder control, and dynamic-state hedge are source-correct, and the candidate's case-173
language is fully supported. Citation layer: partial — D1 (659 span `22398–22430` vs actual
`22394–22449`) and D2 (truncated digest suffix `0537652` vs `2537652`); one non-load-bearing
overstatement (D3) and one unmarked inference (D4). The canonical candidate
`corpus/knowledge/webarena-task-spec-audit.md` is not admitted; the frozen draft
SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` was re-verified.

VERDICT: PARTIAL
