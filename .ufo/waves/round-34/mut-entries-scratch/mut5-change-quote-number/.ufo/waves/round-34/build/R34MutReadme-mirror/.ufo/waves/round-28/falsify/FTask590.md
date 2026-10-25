# FTask590 — falsification of BUILD case590 (WebArena task 590)

Seat: `KengakuR28.FTask590` (leaf, read-only, author-side). Date: 2026-10-21.
Scope: static case590 + its case-specific candidate language. No upstream code imported or executed,
no benchmark site contacted, no browser action, no scorer run, no production edit.

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Reviewed bytes (observed)

| artifact | path | sha256 |
|---|---|---|
| build case | `.ufo/waves/round-28/build/Task590.md` | `a44ea380d99a1daeef744c54a51e1a9877f2f4d42a88552aec25da3e26cfbf47` |
| frozen candidate draft | `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` |
| raw tasks | `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| scorer | `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` |
| helpers | `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` |
| manifest | `plans/fixtures/r28/webarena/manifest.json` | `c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd` |

The three source digests and byte counts (880776 / 13264 / 7565) equal the manifest values; manifest
revision is `dce04686a56253aefba7b18a4fa0937cf1dc987b`. The frozen draft hash equals the context-declared
`77e19d5b…20a8`.

Canonical admission target `corpus/knowledge/webarena-task-spec-audit.md` is **absent** on disk at
review time (no canonical bytes exist to review). Every `PASS` statement below is scoped to the frozen
draft and `build/Task590.md`; it is not an admission, not a whole-candidate Q10 source/number approval,
and not a runtime task-validity claim.

## Method

`json.load` of the raw task file (data only), `grep -n`/`sed -n` over the pinned files, an independent
replay of the stratum/selection census, and a standalone reimplementation of `clean_url` / `parse_url` /
`clean_answer` / `must_include` semantics. No lane or upstream module was imported; no production file
was modified. No tool install or update was needed.

## Task590 raw record (observed; all anchors reproduce)

- `task_id` 590 at line 19576; `intent` at 19587; `eval_types` 19590–19592; `reference_url` 19595;
  three `program_html` targets at 19598/19607/19616, locators 19599/19608/19617, `must_include` values
  19602/19611/19620; `url_note` 19625; `intent_template_id` 19627.
- Values: sites `["gitlab"]`; `require_login: true`; `storage_state ./.auth/gitlab_state.json`;
  `require_reset: false`; `start_url __GITLAB__/primer/design`; `reference_answers: null`.
- Intent: “Create a milestone for the upcoming event of product launch starting on 1/16/2023 and ending
  on 1/30/2023” (17 words).
- Targets: `#content-body` must include `product launch`; `.block.start_date` must include
  `Jan 16, 2030`; `.block.due_date` must include `Jan 30, 2030`; all `url: "last"`.

Every line number and literal in Task590.md's task-spec bullet list reproduces exactly.

## Evaluator trace (observed)

| claim | source anchor | verified behavior |
|---|---|---|
| router / order | `evaluators.py` 356–374; cases 366–370 | `url_match` → `URLEvaluator`, then `program_html` → `HTMLContentEvaluator`; order follows `eval_types` |
| product | 336–352; multiply at 348–352 | `EvaluatorComb` starts at 1.0 and multiplies each evaluator result |
| URL normalize | 187–190 | `clean_url` = `str(url).rstrip("/")` only |
| URL parse | 192–197 | returns `(netloc+path, parse_qs(query))`; no scheme/fragment |
| URL predicate | 218, 220–227 | `pred_base_paths, pred_query = parse_url(pred)`; `ref_base_path in pred_base_paths` is a **string substring** test |
| URL query | 228–235, 236 | no reference query in task590 ⇒ `ref_queries` empty ⇒ `query_score = 1.0`; `score = base_score * 1.0` |
| HTML `last` | 271–273 | `"last"` skips `page.goto` and the 3 s sleep |
| HTML selector | 279–289 | `document.` branch runs `page.evaluate("() => " + locator)` |
| HTML failure | 290–294 | falsy result or exception ⇒ `selected_element = ""` |
| HTML normalize | 303 | `html.unescape(selected_element)` |
| content operator | 312–327; 98–111; 80–86 | `must_include` split on `" |OR| "` (none), then `StringEvaluator.must_include(tokenize=False)`; `clean_answer` strips one quote pair + lowercases; final test is `clean_ref in clean_pred` |
| helpers | `helper_functions.py` 211–221; imports 9–20 | `PseudoPage` only; task590 has no `func:` URL/locator and no fuzzy/UA reference, so the three helpers are never called |

The only non-substantive anchor imprecision found: Task590.md cites the router as 361–372 while the
`return EvaluatorComb(...)` is at 374; the cited append lines (368, 370) are inside 361–372. The S062
quote range 222–223 includes the list bracket at 222 while the quoted expression is on 223. Neither
changes the claim.

## Independent numerics (observed)

- 812 raw tasks, 812 distinct IDs, 0–811, no missing/duplicate.
- Stratum `(("gitlab",), ("program_html","url_match"))`: **23 tasks**, minimum ID **590**. Full
  sorted-strata replay gives exactly the persisted 16 IDs: 389, **590**, 132, 173, 44, 552, 681, 791,
  556, 356, 7, 377, 759, 424, 97, 399; 590's stratum is rank 1.
- `intent_template_id: 339` has 5 tasks (590–594). 591/592: intent 2023, required 2030, same
  `__GITLAB__/primer/design` project. 593/594: 2044 in both intent and required contents.
- Intents containing the literal `2030`: only 658 and 809. Eval objects containing `2030`: only
  590, 591, 592, 658, 809 (the latter two are intent-consistent issue tasks).
- Task590.md's 23-task / min-590 / sibling / “only 658 and 809” numbers all reproduce.

## Decisive boundaries / controls

### B1 — The intent/scorer year mismatch is real and operator-decisive (static)

Intent says `1/16/2023`–`1/30/2023`; H2/H3 require `Jan 16, 2030` / `Jan 30, 2030`. Under the exact
source semantics, `clean_answer` lowercases only and `must_include` is substring containment:

```
must_include("Jan 16, 2030", "Start date: Jan 16, 2023") -> False
must_include("Jan 16, 2030", "Start date: Jan 16, 2030") -> True
```

A `.block.start_date`/`.block.due_date` selection that shows the literal intent dates therefore scores
0 on H2/H3; passing requires a 2030 literal that the intent never states. This is a decisive
source-level boundary, independent of any audit formatting. It does **not** prove the deployed page
shows only the 2023 date: the generated config, GitLab DOM/date rendering and clock remain unobserved,
exactly as Task590.md states. No runtime invalidity is claimed.

Separate unchecked clause: the intent's “upcoming” relation to the environment clock is not a
predicate — the scorer compares date text only. A 2030 literal is future relative to the 2025-11-26
snapshot/review date, but the deployed clock is unobserved; no claim is made that “upcoming” is
enforced or violated.

### B2 — URL `GOLD in PRED` is substring-only; U does not establish creation (static)

`parse_url` returns a `str` base path (192–197), and the predicate is `ref_base_path in pred_base_paths`
(223), not list membership. With `__GITLAB__` substituted to `gitlab.example.com`, ref
`gitlab.example.com/primer/design/-/milestones`:

| prediction URL | U result |
|---|---|
| `…/primer/design/-/milestones` (list page) | True |
| `…/primer/design/-/milestones/new` | True |
| `…/primer/design/-/milestones/7` (existing milestone) | True |
| `…/primer/design/-/milestones/7/edit` | True |
| `…/primer/design/-/milestones_old` (different route) | True |
| `…/primer/design/-/issues` | False |

So the list page, `/new`, an existing milestone and even a `milestones_old` route pass U. Combined with
`require_reset: false` and siblings 591/592 (same project, 2030 dates), U cannot distinguish “created”
from “navigated to an existing matching milestone”; H1–H3 would have to carry that distinction.

### B3 — H1 is page-text substring, not a title binding (static)

`#content-body` outerText must contain `product launch`. The intent's title `event of product launch`
does contain it, but so does any description or other page text containing the phrase
(`"launch of product"` alone does not, `"event of product launch"` does). The build report's H1
unchecked cell is correct: title identity, persistence, state and uniqueness are not checked.

## Candidate case-specific language (frozen draft `77e19d5b…`)

1. “Task590: intent names January2023 dates while configured page-content targets name2030.” —
   **supported**; intent is 2023, targets are 2030.
2. “This mismatch exists in authored text; actual runtime task invalidity still requires the generated
   config, deployed GitLab/date rendering and reference-trajectory evidence.” — **supported**; it is a
   subset of Task590.md's runtime-evidence list and claims no observed runtime failure.
3. Table label “date-key disagreement” — telegraphic; the underlying source disagreement is a
   date-value/year mismatch (2023 vs 2030), not a field-key swap (`.block.start_date` /
   `.block.due_date` are correctly keyed to start/end). Non-blocking editorial imprecision; the
   detailed bullet directly below is exact. If the label is touched, “date-year/value disagreement” is
   the supported wording.
4. The draft's 16-ID selection and lexicographic rule reproduce exactly; 590 is the second group's
   minimum.

No case-specific candidate statement was found to exceed the pinned source. The candidate does not
claim runtime task invalidity, a judge result, or a 590 score.

## Non-blocking precision notes on Task590.md

- “`clean_url` only strips a trailing `/`”: `rstrip("/")` strips all trailing slashes; no effect here.
- “`Mon D, YYYY`” is a paraphrase; the literal is `Jan 16, 2030` (abbreviated month, day, comma, year),
  not strftime `Mon` (weekday).
- Router anchor 361–372 excludes the return at 374 (cited appends are inside the range).
- S062 quote range 222–223: the expression is on 223; 222 is `[`.
- H1 unchecked “project ownership” is broader than the combined check: U's path substring does
  constrain the project route; the content check alone does not bind the title to the project. If read
  as H1-only, the row is accurate.

## Remaining unknowns (runtime, not observed)

1. Actual scored per-task config after `__GITLAB__` substitution / generation (generation step is not in
   the pinned snapshot).
2. Deployed GitLab DOM classes `.block.start_date`/`.block.due_date`, date format, locale, timezone and
   environment clock.
3. Pre-existing `primer/design` milestone state, including siblings 591/592 and any earlier run under
   `require_reset: false`.
4. Reference-trajectory scores for literal 2023 vs 2030 entry.

These are the case's own listed unknowns; none is converted to a confirmed success or failure here.

## Verdict

**VERDICT: PASS** — case590 falsification, static scope.

Every Task590.md source-line anchor, numeric count and operator claim reopened here reproduces against
the pinned bytes at `dce04686…`. The intent/scorer 2023→2030 mismatch (B1) and the substring-only URL
proxy (B2) are real, decisive boundaries; the combined evaluator is correctly described as binary; the
candidate's substantive case-specific language is supported and does not exceed source (the §Candidate
table-label note is editorial, not a source overclaim). The case's own **PARTIAL**
(runtime validity open) is the correct scope and is not contradicted. Canonical candidate
`corpus/knowledge/webarena-task-spec-audit.md` is not admitted; this PASS is not admission, whole-
candidate Q10 approval, or runtime task validity.

Cross-check (author-side, not authority): peer `FContractURLSchema.md` independently derives the same
`ref_base_path in pred_base_paths` substring rule and confirms Task590's raw-placeholder empty-netloc
statement; peer `FSourceS062.md` confirms the S062 class/router boundaries (336–352, 356–374). Neither
contradicts a case590 claim; their findings are instrument/registry issues outside this case scope.

Confidence: high on all static claims (direct source reopen + independent census/predicate replay);
runtime claims remain unobserved.
