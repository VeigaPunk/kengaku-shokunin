# RevHTMLRequired — HTMLContentEvaluator `required_contents` scorer contract + audit cases

- **Seat / writer:** `KengakuR28.RevHTMLRequired-2` (reviewer leaf, author-side; no subagents dispatched)
- **Date:** 2026-10-21
- **Scope:** Review exactly the pinned WebArena `HTMLContentEvaluator` `required_contents` operator semantics (`exact_match` / `must_include` / `must_exclude` question) and the target conjunction; produce a source-anchored scorer contract plus concrete hand-expected schema/semantic cases for the C1 audit (`plans/benchmark_spec_audit.py`). Static source/JSON analysis only.
- **Source opening (access date 2026-10-21, ≤25-word located quotes below):**
  - S062 `evaluation_harness/evaluators.py`, pinned upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b` — quote (lines 305–312): *“if "exact_match" in target["required_contents"]: … elif "must_include" in target["required_contents”]”* — scope: operator dispatch only.
  - S061 `config_files/test.raw.json`, same revision — quote (task 590 target 2, `must_include`): *“Jan 16, 2030”* — scope: illustrative reference-content sampling.
  - S063 `evaluation_harness/helper_functions.py`, same revision — quote (lines 117–141): *“account_idx = page.evaluate(…) … except Exception: role = ""”* — scope: locator-helper behavior referenced by `func:` locators.
- **Snapshot integrity (observed):** `sha256sum` of all four manifest-listed files reproduces `plans/fixtures/r28/webarena/manifest.json` exactly (`test.raw.json` 7b50386f…37652, `evaluators.py` e23edb39…0c22, `helper_functions.py` ec758da4…e275, LICENSE c71d239d…d0ab4). Counting below is valid on this verified input.
- **Tools used:** preinstalled `python3` (stdlib `json`, `collections`) and `sha256sum` for read-only counting on the frozen snapshot; no installs, no pacman, no network, no upstream code imported/executed, no benchmark sites contacted.
- **Limitation:** every count below is a static census of the pinned snapshot; it is scorer-contract evidence, not runtime/browser truth, and not a task-validity verdict.

---

## 1. Scorer contract (source-anchored, evaluators.py @ dce04686)

### 1.1 Routing and conjunction (upstream chain)

1. `evaluator_router` (evaluators.py:356–374) iterates `configs["eval"]["eval_types"]` and instantiates `HTMLContentEvaluator()` only for the literal string `"program_html"` (line 369–370). **The `program_html` block is dead configuration unless `"program_html"` is a member of `eval_types`.** Any other eval_type raises `ValueError` (line 372).
2. `HTMLContentEvaluator.__call__` (lines 247–333) sets `score = 1.0` and multiplies per-target sub-scores: **targets are conjunctive (AND)** — a single failing target yields task score 0.0 (lines 260, 310, 327).
3. `EvaluatorComb.__call__` (lines 340–352) multiplies all routed evaluators' scores: program_html also ANDs with `url_match` / `string_match` sub-scores. Final task score is a product, hence 0.0 if any component is 0.0.
4. `HTMLContentEvaluator` never calls `get_last_action`/`get_last_state`; it reads only live page state (and `page.url` via `__last_url__` substitution). The agent's final `answer` is irrelevant to this evaluator.

### 1.2 Target traversal and locator-class chain (lines 261–303)

Per target, in exact source order:

1. `target["url"]` (line 262): if it `startswith("func")` (line 263 — **no colon required**), the remainder after `"func:"` is Python-`eval`ed with `__last_url__` textually replaced by `page.url` (lines 264–266). Else if the URL is the literal `"last"`, no navigation happens — checks run on the **current** page (lines 271–273). Any other value is `page.goto(target_url)` + fixed `time.sleep(3)` (lines 272–273).
2. Locator dispatch, mutually exclusive:
   - `locator.strip()` empty → `selected_element = page.content()` — the **full page HTML** (lines 276–277).
   - starts with `"document."` or `"[...document."` → optional `prep_actions` are `page.evaluate`d with exceptions **silently swallowed** (lines 282–287), then `selected_element = str(page.evaluate(f"() => {locator}"))`; JS exception or falsy result → `""` (lines 288–294).
   - starts with `"func:"` → Python-`eval` after `__page__`→`page` substitution (lines 296–299). `prep_actions` is **not** consulted in this branch.
   - anything else → `raise ValueError(f"Unknown locator: …")` (lines 300–301): **no score is returned**; the process crashes.
3. `selected_element = html.unescape(selected_element)` (line 303) — HTML entities are decoded **before** matching.

### 1.3 `required_contents` operator dispatch (lines 305–332)

- **`elif` chain — the operators are mutually exclusive, and `exact_match` shadows `must_include`:** `if "exact_match" in target["required_contents"]` is tested first; a dict carrying both keys would be scored by `exact_match` alone with no diagnostic (lines 305, 312).
- **`exact_match`** (lines 305–311): value is used as-is (`beartype` enforces `str`). Calls `StringEvaluator.exact_match(ref=…, pred=selected_element)`.
- **`must_include`** (lines 312–328): asserted `list` (line 314 — a non-list raises `AssertionError`, unscorable); each element must be a `str` (beartype via `StringEvaluator.must_include`).
- **`must_exclude` DOES NOT EXIST in the pinned revision.** `grep -rn "must_exclude"` over the whole snapshot returns nothing (scorer and tasks alike). Any audit artifact that inventories `must_exclude` as a supported operator is describing a *different* upstream release and is a same-identity defect for this pin. The supported key set is exactly `{exact_match, must_include}`; `else: raise ValueError(f"Unknown required_contents: …")` (lines 329–332) makes any other key set a crash, not a 0.0.

### 1.4 Match-primitive semantics (StringEvaluator, lines 78–111) — shared by both operators

`clean_answer` (lines 80–86): `strip()` outer whitespace; remove **one** layer of matched surrounding `'…'` or `"…"` quotes; **`.lower()`** (ASCII-case-fold). Both `ref` and `pred` go through it.

- `exact_match(ref, pred)` = `clean(ref) == clean(pred)` (lines 90–94): equality is **case-insensitive and trim/quote-insensitive**, on the *whole* selected element.
- `must_include(ref, pred, tokenize=False)` (lines 96–111): HTMLContentEvaluator always passes `tokenize=False` (line 322), so it is the plain branch: `clean(ref) in clean(pred)` — **case-insensitive substring containment**. The tokenize branch (`clean_ref in word_tokenize(clean_pred)`) is **dead code** on this path; per-character `len(clean_ref) == 1` triggers it only when `tokenize=True`, which program_html never does. Consequences the audit must encode: single-character or numeric refs such as `"0"` substring-match anywhere (e.g. inside `"10"`); there is no word-boundary protection on this path.
- **Conjunction inside `must_include`:** per element, `content.split(" |OR| ")` yields alternatives; sub-score = `any(must_include(alt) for alt in alternatives)` (lines 316–326) — **OR within one element; AND across elements** of the list. Scoping note (corrected, see §7): the comprehension at line 324 (`for content in content_or`) rebinds `content` inside the comprehension's implicit scope, so `ref=content` at line 320 binds to **each alternative**. The behavior is exactly plain OR over the split alternatives; a plain-OR reimplementation is same-identity. (An earlier revision of this report claimed a first-alternative whole-string quirk; that claim was wrong and is retracted — the outer loop variable from line 315 is shadowed, not reused, and `content_or[0] == content` does not even hold when an `|OR|` exists, e.g. `"a |OR| b".split(" |OR| ") == ["a", "b"]`.)
- **Vacuous-truth trap:** empty-string refs are total matches — `"" == x` fails but Python `"" in x` is `True` for any `x` (incl. `""`), and `split(" |OR| ")` on `""` yields `[""]`. An empty `exact_match` ref matches only a selected element that cleans to `""` — including the *locator-failed* `""`.

### 1.5 Score = 0 collapse points (contract-level)

The scored value 0.0 arises when any conjunct fails; it does **not** distinguish:

- locator raised in JS / element missing → `selected_element = ""` (lines 292–294) → non-empty ref fails;
- locator succeeded but returned `""`/falsy → same;
- element present with different content;
- `prep_actions` exception silently swallowed → possibly wrong page state before selection (lines 286–287).

A static audit can therefore never infer "score 0 ⇔ page wrong"; it can only inventory which tasks are *sensitive* to these collapses. Conversely `gitlab_get_project_memeber_role` (helper_functions.py:115–143) returns `""` on any exception, and `""` fails every non-empty ref — the helper's own error convention feeds the same collapse.

### 1.6 Environment placeholders and `func:` inventory (JSON + helper_functions.py)

`test.raw.json` URLs/locators reference placeholder tokens (`__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__` …) substituted before the config reaches the evaluator (out-of-snapshot tooling); the audit can only inventory them lexically. Python-`eval`ed identifiers must resolve inside `HTMLContentEvaluator.__call__`'s scope or the pinned `helper_functions.py` imports. Observed inventory: URL funcs `shopping_get_latest_order_url()` (10 targets), `reddit_get_post_url('__last_url__')` (65); locator funcs `gitlab_get_project_memeber_role(__page__, '<account>')` (11, accounts abisubramanya27/yjlou/koush/lahwaacz/vinta/a11yproject) and `shopping_get_sku_latest_review_{rating,author}('<SKU>')` (11, SKUs B00J8RZL7I/B07HZB38XH/B0041MSF2S/B07DFJ5XKH/B09P7BFL4H — one rating+author pair each). All 22 locator-func names and all 2 URL-func names exist in `helper_functions.py`; `__page__`/`__last_url__` are the only injected names. Helper calls perform **live HTTP/JS** at scoring time (e.g. `requests.post` shopping auth, helper_functions.py:23–35) — inherently outside static proof.

---

## 2. Observed population facts (static census, verified hashes; denominators explicit)

Population: 812 raw tasks. Facts the new audit must reproduce exactly:

| # | Fact | Value |
|---|------|-------|
| P1 | tasks with a `program_html` block (regardless of routing) | 411 |
| P2 | tasks with `eval_types` containing `"program_html"` (routed) | 411 |
| P3 | targets under routed tasks (scorer-relevant) | 651 |
| P4 | tasks with `program_html` **not routed** | 401, and **all 401 have `"program_html": []` (empty list)** — includes selected IDs 132, 173, 44, 791, 7, 377, 97; no runtime effect, and no unconsumed nonempty predicate exists anywhere in the pin |
| P5 | routed-but-absent (`program_html` in `eval_types`, key missing) | 0 |
| P6 | routed target operators: `must_include` / `exact_match` | 463 / 188 (sums to P3) |
| P7 | `required_contents` key combinations observed | `{must_include}` 463, `{exact_match}` 188, `{both}` 0, `{empty}` 0 |
| P8 | locator classes (all targets): empty/full-page `document.`-JS `func:` other | 105 / 524 / 22 / **0** |
| P9 | `prep_actions` targets | 10, all paired with `document.`-class locators (0 on `func:`/empty ⇒ no dead-prep instances in pin) |
| P10 | url forms: `last` / literal-with-placeholder / `func:` | 238 / 576 / 75 |
| P11 | `must_include` items containing ` |OR| ` | 5 of 815 items (4 with one `|OR|`, 1 with two) |
| P12 | eval_types combos | `string_match` 325, `url_match` 66, `program_html` 282, `string_match+url_match` 10, `program_html+url_match` 129 |

**P4 is the single most important scorer-contract fact for C1 — and it is sharper than "presence ≠ scoring":** the `program_html` key is present in **all 812** raw configs (exact partition: 401 `[]`-not-routed + 411 nonempty-routed; zero `null`, zero key-absent, zero nonempty-but-unrouted). Key *presence* therefore carries zero information; the audit's operative strata are **empty-list-not-routed vs. nonempty-routed**. The audit MUST NOT count task validity or "program_html coverage" from field presence alone, and must NOT describe the 401 as "unconsumed nonempty predicates" — they are empty-list shells whose only scorer-relevant role is the routing check itself. Denominators for scorer-sensitive inventory remain routed tasks/targets (P2/P3).

## 3. Concrete hand-expected cases for the new audit (miniatures + per-task cases)

### 3.1 Schema cases (hand-expected `exit`/`finding` per pinned scorer contract)

| Case | Miniature task JSON (hand-written) | Expected audit finding / exit |
|---|---|---|
| S1 | `program_html` target, `required_contents` `{}` | instrument finding `unknown_required_contents` (scorer raises ValueError, evaluators.py:329–332); exit 1 if this task is in population |
| S2 | `required_contents` `{"must_exclude": "x"}` | same `unknown_required_contents` class — **must_exclude is not a supported operator at this pin**; audit must NOT model it as a third operator |
| S3 | `required_contents` `{"must_include": "Thanks"}` (scalar) | `must_include_non_list` finding (scorer would AssertionError, line 314); schema check distinct from instrument crash |
| S4 | `required_contents` `{"must_include": ["a", 3]}` | `must_include_item_non_string` (beartype contract, lines 318–323) |
| S5 | `required_contents` `{"exact_match": 1}` (int) | `exact_match_non_string` (beartype `ref: str`, line 90) |
| S6 | `required_contents` `{"exact_match": "x", "must_include": ["x"]}` | `shadowed_operator` finding: exact_match wins, must_include dead (elif, lines 305/312); 0 instances in pin (P7) |
| S7 | locator `"xpath=//div"` | `unknown_locator` finding (scorer crashes, lines 300–301); pin count 0 (P8) |
| S8 | `prep_actions` on `func:` or empty locator | `dead_prep_actions` advisory (branch never reads it); pin count 0 (P9) |
| S9 | locator `document.querySelector("[name=route_from")` (unterminated attribute) | static CSS well-formedness **advisory only** (`locator_suspect`), never a FAIL: cannot prove browser parser leniency (see §4). Pin contains real instances: tasks 356, 759 (`[name="route_from"`, `[name="route_to"`), 424 (`[id="sidebar_content"`) |
| S10 | eval block `{"program_html": {...}}` present, `eval_types` = `["string_match"]` | `program_html_not_routed` observation stratum (P4); counts as inventory, NOT a defect |
| S11 | `eval_types` contains `"program_html"` but key absent | `routed_missing_program_html` (runtime KeyError); pin count 0 (P5) |
| S12 | `must_include` item `""` or `"a  \|\|OR\|\|  "`-split producing `""` | `vacuous_ref` advisory (always-true alternative; §1.4); pin count 0 observed |
| S13 | snapshot file hash ≠ manifest | instrument exit 2, stable `snapshot_tampered` — checked **before** any counting (prereg line 15) |
| S14 | URL `func:nonexistent_helper()` | `unresolved_eval_name` (NameError at runtime); verify callee identifier ∈ {helper_functions names} ∪ {page, client, trajectory, configs, target, time, html, importlib … imports} |

### 3.2 Semantic micro-model cases (hand-computed expected score under the §1 contract; implement as pure reimplementation tests, never by importing upstream)

Scorer model: `score = ∏targets op(clean(ref), clean(unescape(selected)))`, `exact_match` ⇒ equality, `must_include` ⇒ substring, OR-in-item/AND-across-items, `""`-locator ⇒ `""`.

| Case | selected_element (post-eval) | required_contents | expected score |
|---|---|---|---|
| M1 | `"I am a robot"` | `exact_match: "I am a robot"` | 1.0 |
| M2 | `"I am a robot."` | `exact_match: "I am a robot"` | 0.0 (whole-string equality) |
| M3 | `"  \"I Am A Robot\"  "` | `exact_match: "'I am a robot'"` | 1.0 (trim+one-quote-layer+case-fold both sides) |
| M4 | `"Release Jan 16, 2030"` | `must_include: ["jan 16, 2030"]` | 1.0 (case-insensitive substring) |
| M5 | `"2023 release"` | `must_include: ["2030"]` | 0.0 |
| M6 | `"route 10 stop 2"` | `must_include: ["2"]` | 1.0 (**substring trap**: no tokenize on this path, §1.4) |
| M7 | `""` (JS locator failed) | `must_include: ["anything"]` | 0.0; audit must record `empty_selection` ambiguity (missing element indistinguishable from empty content, §1.5) |
| M8 | `""` (JS locator failed) | `must_include: [""]` | 1.0 (**vacuous**); must raise `vacuous_ref` advisory |
| M9 | `"Alpha Beta"` | `must_include: ["gamma \|OR\|\| beta"]` | 1.0 (OR-in-item) |
| M10 | `"Alpha only"` | `must_include: ["gamma \|OR\|\| beta", "alpha"]` | 0.0 (AND across items) |
| M11 | `"x&amp;y"` raw page → `"x&y"` after `html.unescape` | `must_include: ["x&y"]` | 1.0 (unescape precedes matching, line 303) |
| M12 | target2 score 0 | two conjunctive targets | 0.0 (AND across targets, lines 260–327) |
| M13 | page url `…/f/space/1`, element `"gan implementation __GITLAB__/eriklindernoren/PyTorch-GAN"` | `must_include: ["gan implementation", "__GITLAB__/eriklindernoren/PyTorch-GAN"]` | 1.0 — models task 681's AND-of-two-refs on one locator |

### 3.3 Per-task expectations for the 16 selected IDs (what the delivered audit must state per case)

Routed with program_html targets (9): **389** (1 target, empty locator=full-page `page.content()`, must_include `["Thanks, working on reviews"]`); **590** (3 targets, all `last`, `#content-body`/`.block.start_date`/`.block.due_date` outerText, must_include incl. `"Jan 16, 2030"`); **552** (1 target, raw-file URL `__GITLAB__/…/urls.txt`, empty locator, must_include list of 5 `__REDDIT__/f/space/…` URLs — note **no ` |OR| `**, refs are case-folded-substring URLs); **681** (1 target, `last`, `.submission__inner` outerText, AND of `"gan implementation"` + `"__GITLAB__/eriklindernoren/PyTorch-GAN"`); **556** (1 target, raw README URL, empty locator, must_include 12 movie titles, AND); **356** (3 targets, `last`, `exact_match "1"` on `select…selectedIndex` + two must_include route-field values; two locators carry unterminated attribute selectors → S9 advisory); **759** (3 targets, same shape as 356, refs Boston/New York, same advisory); **424** (1 target, `last`, `[id="sidebar_content"` unterminated → S9 advisory, must_include `["Pittsburgh"]`); **399** (1 target, literal `__REDDIT__/user/MarvelsGrantMan136` URL, `.user-bio__biography` outerText, `exact_match "I am a robot"`). Unrouted (7): **132, 173, 44, 791, 7, 377, 97** — each has `program_html: []` **and** no `"program_html"` in `eval_types` (per §2 P4 partition, all unrouted tasks in the pin are empty-list shells); case reports must state "not scorer-active; no program_html contribution," and must not fabricate evaluator targets for them.

Descriptive observation to carry as a limitation (not a FAIL, per prereg "weak proxies are limitations"): task 590's `intent` states dates 1/16/2023–1/30/2023 while its routed checker requires `"Jan 16, 2030"`/`"Jan 30, 2030"`. A static inventory can *surface* this intent/evaluator divergence; it cannot adjudicate task validity, and the audit must not convert it into a benchmark FAIL.

## 4. What a static task-spec inventory cannot prove (explicit non-claims)

1. **Runtime selection truth** — whether each JS locator selects a non-empty node on the live page; score-0 collapses (§1.5) make "element missing" vs. "empty content" vs. "wrong content" indistinguishable from the config side.
2. **`eval()` results** — values of `func:` helpers depend on live HTTP (shopping auth/order APIs, helper_functions.py:23–59) and live GitLab DOM queries (115–143); only identifier resolvability and argument shape are static.
3. **Browser CSS parser leniency** — whether Playwright/Chromium accepts the unterminated attribute selectors of tasks 356/759/424; static well-formedness is an advisory, not proof either way.
4. **Placeholder substitution effects** — `__GITLAB__`/`__REDDIT__` etc. are replaced by out-of-snapshot deployment config before scoring; only the lexical token inventory is static.
5. **Semantic appropriateness** — case-folded substring matching may over- or under-approximate the task intent (e.g. numeric `"2"` inside `"12"`); static analysis cannot prove a ref is *discriminating* for its intent (task 590 divergence is the observed example).
6. **Task validity / achievability** — field presence proves nothing about whether a competent agent can reach the required page state; in this pin `program_html` presence is universal and uninformative (§2 P4), and the 401 empty-list/not-routed tasks are a scorer-routing stratum, not invalidity. No browser action, no live task execution, no bypass demonstration is performed or proposed.
7. **Navigation success** — `page.goto` outcomes and the fixed 3-second sleep's sufficiency (line 273) are runtime-only.

## 5. Recommended checks for `benchmark_spec_audit.py` (program_html slice)

- **R1 hash-gate first** (prereg line 15): verify all four manifest sha256s before any count; mismatch ⇒ exit 2 `snapshot_tampered`.
- **R2 routing stratification:** count `program_html` presence vs. `eval_types` membership separately; report P2–P5; any count derived from field presence alone must be labeled "not scorer-active."
- **R3 operator-key conformance per target:** key set ⊆ `{exact_match, must_include}`, exactly one, with S1–S6 type checks (str / list[str] / shadowing); report unknown keys incl. `must_exclude` as unsupported-at-pin.
- **R4 locator classification** exactly per §1.2 prefix rules (empty / `document.` / `[...document.` / `func:` / other), with counts (P8), `prep_actions` pairing (P9), and advisory-only CSS well-formedness probe (S9).
- **R5 URL-form classification** (`last` / `func:`-prefix / literal) + placeholder token inventory + `func:` callee resolvability against the pinned `helper_functions.py` name set (S14) — via `ast.parse` of evaluators.py/helper_functions.py and string analysis of JSON; never `import`/`eval`.
- **R6 ref-content advisories:** empty-string refs / OR-alternative empties (`vacuous_ref`), single-char and pure-numeric refs (`weak_discriminator`), ` |OR| ` item counts (P11).
- **R7 hand-expected cases:** §3.1 miniatures as CLI selftest fixtures (exit-code + finding-name assertions) and §3.2 as a pure reimplementation micro-model scored against hand-computed expectations (M1–M13); both must be independent of the production implementation (prereg line 21 oracle separation).
- **R8 per-task JSON in case reports:** exact target counts, locator class, operator(s), ref lists, URL form, advisories, and the not-scorer-active statement for the 7 unrouted selected IDs (§3.3).
- **R9 stable exit discipline:** schema findings ⇒ exit 1 (`failed finding`); unreachable/tampered inputs ⇒ exit 2 with stable codes; summary must carry scope/limitations incl. §4 non-claims.
- **R10 must not:** import/execute upstream code; issue network requests; treat `must_exclude` as supported; derive validity from field presence; emit browser actions.

## 6. Verdict

**PASS (scoped)** — for the reviewed contract slice: the pinned `HTMLContentEvaluator` `required_contents` semantics are fully traceable to `evaluators.py` @ dce04686 (§1), the pinned population reproduces consistent aggregates (§2, hash-verified), and §3 gives concrete hand-expected schema/semantic cases sufficient to build and self-test the audit slice without executing upstream code. `must_exclude` is absent from this pin and must be reported as unsupported rather than modeled. Residual risks: (a) §4 non-claims mean every program_html audit output is contract-level evidence only; (b) the `elif` operator shadowing (§1.3) is a behavioral corner where a "cleaner" reimplementation (e.g. scoring both keys) would diverge from same-identity semantics — the `|OR|` comprehension is *not* such a corner (§7: plain-OR is exact); (c) counts in §2 are valid only for the verified snapshot revision and must be re-gated by R1 on any input change.

## 7. Corrections (rev 2, 2026-10-21, after KengakuR28 IRC review)

Two claims in rev 1 were challenged and re-checked against the exact pinned source; both corrections are recorded here and applied in place above. No other section's findings, counts, or expected-case values changed (M1–M13 expected scores were already computed under plain-OR semantics and remain correct).

- **C-1 (retracted): "`ref=content` passes the whole original string for the first `|OR|` alternative."** Exact source (evaluators.py:315–325, re-read raw): the argument `ref=content` at line 320 sits inside the list comprehension `[StringEvaluator.must_include(ref=content, …) for content in content_or]` at lines 317–325; in Python 3 the comprehension is an implicit function scope and its iteration variable shadows the outer loop variable from line 315 for the entire comprehension body. Verified with an isolated pure-Python scoping probe (own snippet, no upstream import): for content `"a |OR| b"` the callee received refs `["a", "b"]`, not `["a |OR| b", …]`. The rev-1 rationalization (`content_or[0] == content`) is false whenever an `|OR|` exists. Corrected in §1.4: behavior is exactly plain OR over split alternatives; a plain-OR reimplementation is same-identity. Recommendation R7 is unchanged except that no shape-mimicry is required here.
- **C-2 (sharpened): 401 not-routed configs are empty-list shells.** Rev 1's "present-not-routed" phrasing could suggest unconsumed nonempty predicates. Re-categorized all 812 configs by key state × routing: exactly two buckets — 401 `"program_html": []` not routed, 411 nonempty routed; zero `null`, zero key-absent, zero nonempty-but-unrouted. The key is therefore present in every raw config and carries no information; "field presence" must not be read as unconsumed predicates anywhere in this pin. Corrected in §2 (P4 row + following paragraph), §3.3 (all 7 unrouted selected IDs have `program_html: []` and no `"program_html"` in `eval_types`), and §4.6.

Correction method: re-read of `evaluators.py:305-333` raw; one stdlib-only population categorization over the hash-verified `test.raw.json`; one isolated pure-Python scoping probe. No production files touched; no broader checks rerun, per instruction.

---
report-by: KengakuR28.RevHTMLRequired-2 — seat review, author-side advice, not outside non-author closure. Paths relative to lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Sources: `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` (S062), `plans/fixtures/r28/webarena/config_files/test.raw.json` (S061), `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` (S063), opened 2026-10-21 at pinned revision dce04686a56253aefba7b18a4fa0937cf1dc987b.
