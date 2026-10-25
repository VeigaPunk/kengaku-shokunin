# OpenScorer — S062 source opening: WebArena `evaluators.py` (round 28, author-side)

Writer/seat: `KengakuR28.OpenScorer-2` (read-only scout). This is author-side advice, not outside non-author closure. I did not edit the registry or any production file.

## Opening

- URL: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py
- Access date: 2026-10-21. HTTP 200.
- Remote sha256: `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22`. This equals the local snapshot `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` and `plans/fixtures/r28/webarena/manifest.json` (13264 bytes, 374 lines). The fetched copy is in `.ufo/waves/round-28/scratch/OpenScorer/openscorer-evaluators.py`.
- LICENSE: the pinned `LICENSE` remote sha256 is `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`, which equals the local snapshot and manifest. It is Apache License 2.0; line 189 holds the unfilled appendix template `Copyright [yyyy] [name of copyright owner]`, so there is no named copyright holder in the file. Quoting short spans and keeping a hashed snapshot for audit is consistent with Apache-2.0 [INFERENCE — not legal advice; the NOTICE file was not checked because it is not in the snapshot].
- I did not fetch auth files or credential data. All 812 raw configs carry a `storage_state` key; I did not open or follow those paths.
- The upstream code was never imported, executed or evaluated. The only things I ran locally were `sha256sum`, `curl` against raw.githubusercontent.com (the pinned source, not a benchmark site), and stdlib `json` parsing of the snapshot data file `config_files/test.raw.json`.

## Located quote (≤25 words, two spans, elision marked)

`evaluators.py:351` + `:365–370`: "score *= cur_score … case "string_match": evaluators.append(StringEvaluator()) case "url_match": evaluators.append(URLEvaluator()) case "program_html": evaluators.append(HTMLContentEvaluator())"

What each span grounds:

- **Router.** `evaluator_router` (`:355–374`) builds one evaluator for each entry in `configs["eval"]["eval_types"]`. Any other type raises `ValueError(f"eval_type {eval_type} is not supported")` (`:371–372`).
- **Three classes.** `StringEvaluator` (`:71`), `URLEvaluator` (`:173`) and `HTMLContentEvaluator` (`:244`).
- **Multiplication.** `EvaluatorComb.__call__` starts at `score = 1.0` and multiplies every evaluator's score (`:348–352`).

If one contiguous quote is required, use `:350–351`: "cur_score = evaluator(trajectory, config_file, page, client) score *= cur_score". Cite the router separately at `:365–370`.

## Source's own behavior (static reading; candidates for tier A)

1. **Composition.** The task score is the product of the per-type scores. Inside each class it is also a product: over the reference-answer keys (`:136–170`), over the query keys (`:229–236`), and over the `program_html` targets and their required items (`:260–333`). One zero factor zeroes the task. The code returns no partial credit and no explanation of which factor failed.
2. **String.** `clean_answer` strips whitespace, removes one pair of matching outer quotes and lowercases (`:80–86`).
   - `exact_match` compares for equality (`:90–94`).
   - `must_include` is a substring test. It switches to token membership only when the call passes `tokenize` (set when the list has exactly one item, `:148`) and the cleaned reference is one character long (`:103–109`).
   - `fuzzy_match` and `ua_match` hand off to helper LLM judges (`:115–121`). Their behavior belongs to S063 and is not established here.
   - In the `fuzzy_match == "N/A"` branch, a non-1 running score is *overwritten* by `score = 1.0 * self.ua_match(...)` against `eval.string_note` (`:152–163`). This discards earlier factors rather than multiplying them.
3. **URL.**
   - `parse_url` returns a `str` base path (netloc+path, `:192–197`). As a result, `ref_base_path in pred_base_paths` (`:221–226`) is a **substring** test against the one predicted URL, not membership in a list.
   - Query values from all ` |OR| ` alternatives are merged into one dict per key (`:199–210`). Every key from any alternative must then have some matching value.
   - Trailing `/` is stripped (`:187–190`).
   - The only accepted `url_note` is `"GOLD in PRED"`, which is also the default (`:215–239`).
4. **HTML.**
   - Target URLs that start with `func` are built by `eval` after substituting `__last_url__` (`:263–266`). URLs other than `"last"` are opened with `page.goto` followed by a fixed `time.sleep(3)` (`:271–273`).
   - The locator can be empty (full `page.content()`), a JS `document.` / `[...document.` expression evaluated in the page, or a `func:` helper call evaluated with `eval` (`:276–301`).
   - Exceptions in `prep_actions` are silently swallowed (`:283–287`). A failing JS locator becomes `""` (`:291–294`).
   - The selected content is HTML-unescaped. It is then scored with `exact_match`, or with `must_include` where each item may hold ` |OR| ` alternatives (`:303–327`).
   - Any other `required_contents` key raises `ValueError` (`:329–332`).
5. **Inputs each class reads.**
   - `StringEvaluator` reads only the last action's `answer` (`:133–134`).
   - `URLEvaluator` reads only `page.url` (`:212`).
   - `HTMLContentEvaluator` reads page/DOM state, or helper output from the API (`:259–333`).
   - No class inspects the full trajectory beyond its last action and state accessors (`:47–68`).

## Snapshot cross-check (stdlib JSON parse of the pinned data, not scorer execution)

- There are 812 tasks. The evaluator-type sets are `string_match` 325, `program_html` 282, `url_match`+`program_html` 129, `url_match` 66, and `string_match`+`url_match` 10. That is five sets, which matches F2 as an observation.
- Every declared type is routable, and no task uses an unsupported type.
- `reference_answers` key-sets on the 335 `string_match` tasks: `must_include` 172, `fuzzy_match` 114, `exact_match` 45, and `must_include`+`fuzzy_match` 4 (tasks 34, 35, 267, 268; all four use list fuzzy refs, not N/A).
- There are 36 `fuzzy_match: "N/A"` tasks. All of them are string-only with a single key, and all carry `eval.string_note`.
  - So the overwrite in behavior 2 changes no score in this snapshot. It is a latent property of the source only.
  - Task 723 has an extra top-level `string_note`, but its `eval.string_note` is what the code reads.
- `url_match` tasks: `url_note` is `GOLD in PRED` in 196 and absent in 9 (the default applies). 7 have ` |OR| ` reference URLs.
- `program_html` targets:
  - `required_contents`: `must_include` 463, `exact_match` 188.
  - Locators: JS 524, empty 105, `func:` 22.
  - Target URLs: literal 338, `last` 238, `func` 75.
  - 10 have `prep_actions`; 5 must-include items use ` |OR| `.
- These counts are this seat's direct parse. They are not the production `benchmark_spec_audit.py` output and should be reconciled at integration.

## Proxy predicates versus intent completeness

The scorer measures **declared proxy predicates**: normalized string equality or substring, URL substring plus query-value membership, and DOM or API content equality or substring. It does **not** measure whether the natural-language `intent` was completed.

- `must_include` is satisfied by over-inclusive answers. Nothing penalizes extra content.
- URL substring matching accepts any predicted URL that contains the gold base path.
- HTML checks look only at the named targets and locators. Unnamed side effects, extra edits and action order go unchecked.
- `fuzzy_match` and `ua_match` delegate to an LLM judge whose verdict is not static evidence.

These are scope limits on what a 1.0 or 0.0 certifies. They are **not** findings that any task is invalid, mis-scored, or exploitable, and no bypass was attempted or described.

## Proposed rows (no registry edit; my seat owns S062 only)

- **S061 — Tasks** (`config_files/test.raw.json`, sha256 `7b50386f…537652`): the Task seat must open and quote it. I make no claim here beyond the parse counts above.
- **S062 — Scorer (this seat):**

  | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
  |---|---|---|---|---|---|---|---|---|---|---|
  | S062 | WebArena evaluator harness @dce04686 — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py | code | A | this pinned file's own static routing and scoring behavior (three evaluator classes, multiplicative composition, string/URL/HTML predicates); not helper/LLM-judge behavior, runtime outcomes, task validity or WebArena-Verified | `evaluator_router` :355–374, `EvaluatorComb` :348–352, `StringEvaluator` :123–170, `URLEvaluator` :212–241, `HTMLContentEvaluator` :259–333; sha256 e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22; Apache-2.0 LICENSE c71d239d… | eval_types route to String/URL/HTML evaluators and every factor multiplies, so the score certifies declared proxy predicates (substring URL base, over-inclusive must_include, N/A ua_match overwrite), not intent completeness | queued | 2026-10-21 | 2027-01-19 | (round-28 knowledge path once admitted) |

  - Status should stay `queued` until a second seat re-reads it and a round-28 knowledge path cites it. If the row became `mined` with an empty used-by, C2-style rules would flag it, although S062 is outside the frozen C2 population.
  - The recheck date `2027-01-19` follows the existing 90-day convention [INFERENCE].
- **S063 — Helpers** (`evaluation_harness/helper_functions.py`, sha256 `ec758da4…7e275`): the Helpers seat must open it. It owns the `llm_fuzzy_match`, `llm_ua_match` and site-helper semantics that S062 explicitly excludes.

## Limits

- This is static reading only. `browser_env`, the helper functions, Playwright and the LLM judge were not snapshotted or run, so the real score values from `fuzzy_match`, `ua_match` and `func:` helpers are unknown. In particular, whether they are binary is unknown.
- Behaviors that depend on `eval` or `page.evaluate` (`func` URLs and locators, JS locators) are described as code paths only. I did not run them.
- The substring reading in behavior 3 rests on the annotation and return type of `parse_url`. It was not confirmed by any executed control.
- The source's own licence text names no copyright holder, and NOTICE was not checked.
- This is not the WebArena-Verified release. No claim is made about contamination, model ability or method novelty.

## Verdict

**PASS (scoped)** for the S062 source opening:

- The pinned URL was opened and is byte-equal to the snapshot (digest above).
- The located ≤25-word quote grounds the router, multiplication and three classes.
- Proxy-versus-intent limits are separated from benchmark-validity claims.
- The licence was checked.
- A tier-A row is proposed, scoped only to the source's own behavior.

This is not a C1, C2 or round PASS. S061 and S063 remain with their own seats.
