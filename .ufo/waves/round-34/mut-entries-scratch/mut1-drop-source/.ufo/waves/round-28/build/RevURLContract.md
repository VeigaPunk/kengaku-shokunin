# RevURLContract — URLEvaluator scorer contract review (round-28, C1)

- **Writer/seat:** KengakuR28.RevURLContract-2 (author-side review seat)
- **Date:** 2026-10-21
- **Scope:** `evaluation_harness/evaluators.py` `URLEvaluator` only — `reference_url` / ` |OR| ` alternatives, netloc/path/query handling, `matching_rule`; plus schema/semantic cases for the new static audit (`plans/benchmark_spec_audit.py`) and honest unprovability limits.
- **Pinned input:** `plans/fixtures/r28/webarena/` @ upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b` (manifest.json sha256s observed present; not re-hashed by this seat — audit does that).
- **Method:** read-only source review + `json.load`/`urllib.parse` (stdlib) parsing of `config_files/test.raw.json` as data. No upstream code imported/executed; no browser/site contact; stdlib semantics verified by direct calls. Scratch evidence: `.ufo/waves/round-28/scratch/RevURLContract-2/url_contract_evidence.json`.

## 1. Source-anchored contract (evaluators.py, all lines verified in pinned file)

| # | Contract fact | Anchor |
|---|---|---|
| C1 | Selected when `"url_match"` ∈ `eval.eval_types` via `evaluator_router`; unknown type → `ValueError`. Combined score = product over evaluators (`EvaluatorComb`), in **declared order** | L355–374, L336–352 |
| C2 | Reads `configs["eval"]["reference_url"]` raw; **no `__SITE__` placeholder substitution** occurs in the evaluator — substitution is caller-side and outside this snapshot | L213 |
| C3 | Alternatives split on literal `" |OR| "` (spaces both sides required); each alt then `clean_url`'d | L213–214 |
| C4 | `clean_url` = `str(url).rstrip("/")` — strips **all** trailing slashes | L187–190 |
| C5 | `matching_rule = eval.get("url_note", "GOLD in PRED")`; any value ≠ `"GOLD in PRED"` → `raise ValueError` (exception, not score 0). `"url_note": null` in JSON also raises (None ≠ default, `.get` returns the present null) | L215–216, L238–239 |
| C6 | `base_path = netloc + path` — **scheme dropped entirely** (http≡https), fragment ignored, `;params` dropped, userinfo and port **retained** in netloc, netloc **not** lowercased (`urlparse().netloc` keeps case; only `.hostname` lowercases) | L192–197 + verified stdlib |
| C7 | Base check `ref_base_path in pred_base_paths` is a **substring check on a string** (`pred_base_paths` is a single `str`, not a list): GOLD must appear anywhere inside PRED's netloc+path — prefix/partial path segments, interior netloc matches, and longer host/path strings containing the gold all pass | L220–227 |
| C8 | Query: `parse_qs` (default `keep_blank_values=False`) → dict key→list[str]. **Merged across OR alternatives** into `defaultdict(set)`; every decoded ref key must have ≥1 of its pooled decoded values present as an exact element of the pred's `parse_qs` values. Missing ref keys impose nothing; extra pred keys ignored; missing pred key → 0 for that factor | L196, L199–210, L228–235 |
| C9 | Final `score = base_score * query_score` — binary product {0.0, 1.0} | L236 |
| C10 | Predicted URL is live `page.url` at evaluation time; `trajectory`/`client` unused | L212, signature L177–183 |
| C11 | `reference_url` (and `url_note`) on tasks **without** `url_match` are dead fields — never read | L213–215 (read only inside `URLEvaluator.__call__`) |

### Derived semantic consequences (all stdlib-verified, none executed from upstream)

1. **Host-boundary false accepts:** `reddit.com` ⊆ `notreddit.com`, `site.com` ⊆ `site.com.evil.tld`, `a.com/f/x` ⊆ `a.com/f/xyz`. GOLD-in-PRED is substring, not origin/path equality.
2. **OR is path-level only in spirit but query-level merged:** ref `A?x=1 |OR| B?y=2` requires pred base ∈ {A,B} **and** `x∈{1}` **and** `y∈{2}` — cross-product, not per-alternative conjunction.
3. **`+` in ref query decodes to space** (tasks 274/276/277/278/326 e.g. `q=usb+wifi` ⇔ `q=usb%20wifi`). **Case-sensitive decoded values.**
4. **`parse_qs` silently drops** bare flags (`?flag`) and empty values (`?a=`); a ref carrying only such params imposes zero constraint.
5. **Percent-encoded path chars not normalized** by `urlparse` — encoded-vs-literal path diffs fail.
6. **Evaluation-time dependence:** `page.url` read when `URLEvaluator` runs. `program_html` `page.goto` navigation (L271–273) mutates `page.url`; score therefore depends on declared `eval_types` order. All 129 combo tasks declare `url_match` **before** `program_html` — audit must record this and flag any reversed declaration as a semantic hazard.
7. **Post-final-action drift:** anything changing `page.url` after the agent's last action (redirect, delayed JS nav) changes the score; trajectory is never inspected.

## 2. Raw-population findings (812 tasks parsed as data)

- `eval_types` strata: `{string_match} 325, {program_html} 282, {url_match} 66, {string_match,url_match} 10, {url_match,program_html} 129` → **205 url_match tasks**.
- `url_note`: 196 explicit `"GOLD in PRED"`, 9 absent→default (tasks 174–182). **No other value; no nulls** → zero `ValueError` risk and zero schema failures expected on this axis.
- `reference_url`: **all 205 url_match tasks contain a `__SITE__` template token** (REDDIT 83, SHOPPING 52, GITLAB 49, SHOPPING_ADMIN 28, MAP 5). Audit MUST model them as templates, not literal URLs — a raw `urlparse` puts `__GITLAB__` in `path`, not `netloc`.
- ` |OR| ` alternatives: exactly **7 tasks** (604, 608, 609, 625, 681, 682, 683); all path-only reddit alternatives → the C8 cross-product is **latent, not exercised** in this population (limitation, not defect).
- Query-bearing refs: **39**; multi-key `&` refs: 45, 46, 324, 325, 327, 328, 342, 354; decoded key inventory: `label_name[]` 10, `q` 10, `product_list_order` 8, `price` 5, `query` 5, `product_list_dir` 3, `sort` 2, `state` 2, `assignee_username`/`reviewer_username`/`search` 1 each.
- Uppercase path chars (genuine, `__SITE__` tokens stripped first): **8 tasks** [105, 106, 599, 604, 609, 636, 638, 684] — e.g. `/f/MachineLearning`, `/f/DIY`, `/f/LifeProTips`. Caveat for the audit: a naive `[A-Z]` regex over the raw ref over-counts (13 incl. 608/625/681–683) because `__REDDIT__` in later `|OR|` alternatives mimics path uppercase. Trailing-slash refs: **14 tasks** [157, 298, 299, 300, 375, 676–680, 708, 711–713] (C4 strips them symmetrically).
- **Dead-field census:** 607 non-`url_match` tasks carry `reference_url`/`url_note` keys; exactly one non-empty (task 247, `eval_types:["string_match"]`, `reference_url="Valorie doesn't have a email in the system"` — free text that is never read). Per assignment: field presence ≠ task validity.
- Selected-16 overlap: url_match tasks **44, 173, 377, 590, 681** (681 also OR-task; 377 has `%20` query `?query=restaurants%20near…`).

## 3. Hand-expected cases for the audit

| Case | Input shape | Expected audit result |
|---|---|---|
| S1 baseline | `eval_types:["url_match"]`, `reference_url:"__GITLAB__/dashboard/todos"` (task 44 shape) | SCHEMA_COMPATIBLE; url_rules["GOLD in PRED"] += 1 |
| S2 default rule | url_match task with **no** `url_note` key (tasks 174–182) | SCHEMA_COMPATIBLE; counted under default "GOLD in PRED" |
| S3 unsupported rule | `url_note:"EXACT"` / `"PRED in GOLD"` / any non-default | `url_rule_unsupported` finding (source raises ValueError) |
| S4 null rule | `"url_note": null` | `url_rule_unsupported` (`.get` returns present null → ValueError upstream) |
| S5 missing/empty ref | `reference_url` absent / `""` / `null` | `reference_url_invalid` (upstream: `.split` AttributeError or always-true `"" in …` tautology — audit should flag both, but the empty-string **always-passes** hazard deserves a distinct note: base_score=1.0 regardless of pred) |
| S6 OR inventory | `reference_url` containing `" |OR| "` | count alternatives; flag any empty part or part without `/` (empty part → `"" in base` tautology → unconstrained) |
| S7 dead field | non-url_match task with non-empty `reference_url` (task 247) | report as dead-field observation, NOT a task defect |
| S8 order hazard | `eval_types:["program_html","url_match"]` declared order | flag as url-timing hazard (program_html mutates `page.url`); zero such tasks in population — count expected 0 |

### 3b. Semantic trace cases (hand-expected score under C1–C11; for case-report writers / oracle cross-check — these are contract traces, not executions)

pred = substituted `page.url`; gold = substituted `reference_url`.

| # | Gold (after `__SITE__`→host) | Pred `page.url` | Expected | Rule exercised |
|---|---|---|---|---|
| T1 | `gitlab.com/dashboard/todos` | `https://gitlab.com/dashboard/todos` | 1.0 | exact modulo scheme-drop |
| T2 | same | `https://gitlab.com/dashboard/todos/` | 1.0 | C4 rstrip both sides |
| T3 | same | `https://gitlab.com/dashboard/todos?tab=foo` | 1.0 | extra pred query ignored |
| T4 | same | `https://gitlab.com/dashboard/todos2` | **1.0** | C7 substring false-accept boundary |
| T5 | same | `https://x.com/u/gitlab.com/dashboard/todos` | **1.0** | interior netloc/path substring |
| T6 | same | `https://gitlab.com/dashboard/TODOS` | 0.0 | case-sensitive path |
| T7 | `__REDDIT__/f/a \|OR\| __REDDIT__/f/b` | `https://r.com/f/b` | 1.0 | C3 alternative |
| T8 | `A?x=1 \|OR\| B?y=2` | `B?x=1&y=2` | **1.0** | C8 cross-product pooling |
| T9 | `shop.com/r?q=usb+wifi` | `…/r?q=usb%20wifi` | 1.0 | `+`≡space decode |
| T10 | `gl.com/i?label_name%5B%5D=BUG` | `…/i?label_name[]=BUG` | 1.0 | decoded key+exact value |
| T11 | `gl.com/i?label_name%5B%5D=BUG` | `…/i?label_name[]=bug` | 0.0 | case-sensitive value |
| T12 | `g.com/i?sort=a&state=opened` | `…/i?state=opened` | 0.0 | missing pred key → 0 |
| T13 | `g.com/i?flag` (bare flag) | `g.com/i` (no query) | 1.0 | parse_qs drops flag → no constraint |
| T14 | `http://g.com:8080/x` | `https://g.com/x` | 0.0 | port in netloc, scheme ignored |
| T15 | `g.com/x` | `g.com/x#frag` | 1.0 | fragment ignored |
| T16 | gold `g.com` | `notg.com/x` | **1.0** | host substring (netloc-in-netloc) |
| T17 | `g.com/a/b` | `about:blank` | 0.0 | non-http pred parses as path |
| T18 | `g.com/x` | `https://user:pw@g.com/x` | **1.0** | userinfo retained in netloc; `g.com` still ⊆ `user:pw@g.com` substring |

Rows T4, T5, T16, T18 are the scorer's real acceptance boundary — case reports should quote them as contract behavior, never as task-invalidity claims.

## 4. What a static task-spec inventory CANNOT prove (must be carried as limitations)

1. Whether the `__SITE__` template substitution upstream produces the intended host for any task (substitution code outside snapshot).
2. Whether any task's gold URL is actually reachable/intended on a live site — substring semantics mean the *stated* predicate is weaker than URL equality; whether that ever accepts a wrong page is a runtime property.
3. `page.url` at evaluation time (post-action navigation, redirects, JS pushes) — spec only says "whatever URL the page ends on".
4. Whether OR alternatives are semantically equivalent pages (e.g. `/f/deeplearning` vs `/f/singularity` are **different** forums — OR encodes scorer leniency, not page equivalence).
5. Order/timing interplay beyond the static declaration (actual `program_html` navigations happen at runtime).
6. Whether dead `reference_url` fields (task 247 etc.) were authoring leftovers vs. intentional — presence is unambiguous, intent is not.
7. Field presence/absence NEVER establishes task validity or invalidity — only schema conformance to the scorer's input contract.

## 5. Required code/output checks for the new audit (recommended additions beyond current schema pass)

Current `benchmark_spec_audit.py` covers: url_note default+enum (mirrors L215 correctly incl. the null edge), reference_url non-empty str, `|OR|` unaffected, order declared implicitly in `raw_task`. Gaps to add:

1. **Split/count ` |OR| ` alternatives per url_match task**; emit per-task alternative count; flag empty parts (tautology hazard).
2. **Query inventory per url_match task**: decoded keys via `parse_qs` on each alternative; count multi-key (`&`) refs, `+`-encoded values, percent-encoded keys, bare/blank-value params (dropped-by-parse_qs hazards).
3. **Template-token census**: distinct `__[A-Z_]+__` tokens in `reference_url` restricted to url_match tasks (expected: 5 tokens / 205 tasks).
4. **eval_types declared-order record** for every url_match+program_html task (expected: url_match first in all 129; any reversal = hazard finding).
5. **Dead-field report**: non-url_match tasks carrying `reference_url`/`url_note` (expected 607; exactly 1 non-empty = task 247).
6. **Case-report anchoring**: every selected-16 url_match report (44, 173, 377, 590, 681) should state expected base_path string(s), decoded query map, declared eval order, and which semantic cases (T4-style substring boundary) apply to that task's gold shape.
7. **No "task valid/invalid" output** from URL fields alone — counts are schema observations only (assignment + contract-compliance requirement).

## 6. Observed commands / limitations of this review

- Stdlib `json.load` on `test.raw.json`; `collections.Counter`; `urllib.parse.urlparse/parse_qs` calls to confirm C6/C8 decode facts; `grep`/`read` on pinned source. No upstream imports, no builds/tests run, no installs performed (none needed; RULES.md not required since zero installs).
- Did not re-verify manifest sha256s (audit owns that step); population facts derived from the pinned file as found.
- Report is author-side review evidence, not outside closure.

## Verdict

**PASS (scoped)** — URLEvaluator contract fully extracted and source-anchored (C1–C11); all 205 url_match tasks schema-compatible with observed `url_note` enum {GOLD in PRED, absent→default}; 7 OR tasks and 39 query-bearing refs inventoried; substring-acceptance boundary and OR-query cross-product identified as the scorer's real semantics with hand-expected traces; static-unprovable items enumerated for the audit's limitations section. No evidence warranting C1 score repricing — this is contract extraction, not task-invalidity proof.
