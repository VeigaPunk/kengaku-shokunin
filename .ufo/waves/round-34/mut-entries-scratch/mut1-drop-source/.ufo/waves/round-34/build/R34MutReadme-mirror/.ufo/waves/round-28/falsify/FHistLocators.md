# FHistLocators — independent replay of locator + target-URL class metrics

Seat: KengakuR28.FHistLocators (falsification wave, 2026-10-21). Read-only over production.
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (verified, matches pinned digest).
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` not yet admitted — frozen draft is the object under test.

## Claims under replay (candidate lines 105–107)

| candidate cell | value |
|---|---|
| page-content targets | 651 |
| locator classes | full-page 105, JavaScript 524, helper 22 |
| target URL classes | last 238, navigation 338, helper 75 |

## Independent census (no production/alternate oracle imported)

Classification rules derived from the raw data families, not from `benchmark_spec_audit.py` logic —
the data itself shows three locator families (empty `""`, `document.`/`[...document.` JS selectors,
`func:name(__page__/…)…` helper calls) and three URL families (`last`, `func:name(…)`,
`__SITE__/…` navigation templates). Verified exhaustively:

- `jq -r '[.[].eval.program_html[]? | .locator] | map(select(. != "" and (startswith("document.")|not) and (startswith("[...document.")|not))) | group_by(.)…'`
  → only `func:` strings remain: 14 distinct `func:` locators, **22** total
  (`gitlab_get_project_memeber_role` × 12, `shopping_get_sku_latest_review_author/rating` × 10). No other non-JS family exists.
- `jq -r '[.[].eval.program_html[]? | .url] | map(select(. != "last" and (startswith("func")|not) and (startswith("__")|not))) | unique[]'` → empty.
  Every non-`last`, non-`func` URL is a `__SITE__/` navigation template.
- `func:` URL family is `func:reddit_get_post_url('__last_url__')` × 65 + `func:shopping_get_latest_order_url()` × 10 = **75**; all 75 carry the colon (0 `func`-without-colon malformed forms).
- Zero whitespace-only and zero non-string locators or URLs in the population.

Exact commands and observed outputs:

1. `jq '[.[].eval.program_html | length] | add' plans/fixtures/r28/webarena/config_files/test.raw.json`
   → `651`
2. Scratch Python census (stdlib `json`/`collections`, saved
   `scratch/FHistLocators/…`; classifiers: empty→full_page, `document.`/`[...document.`→javascript,
   `func:`→helper, else unsupported; url `last`→last, `startswith("func")`→helper, else navigation):
   ```
   targets: 651
   locator_classes: {'full_page': 105, 'javascript': 524, 'helper': 22}
   url_classes: {'last': 238, 'navigation': 338, 'helper': 75}
   odd_loc: {}  odd_url: {'func_colon': 75}
   ```
3. jq-only recount, independent classifier:
   ```
   {"locator":{"full_page":105,"helper":22,"javascript":524},
    "url":{"helper":75,"last":238,"navigation":338},"total":651}
   ```

## Production audit comparison (read-only run)

`cd kengaku-shokunin && python3 plans/benchmark_spec_audit.py --json > scratch/FHistLocators/audit.json`
→ `exit=0`, `findings: 0`, observed:
```
program_html_targets: 651
locator_classes: {"full_page": 105, "helper": 22, "javascript": 524}
target_url_classes: {"helper": 75, "last": 238, "navigation": 338}
```
Exact agreement on every relevant field: program_html_targets, all three locator classes (no
`unsupported` entry — consistent with 0 malformed locators and findings=0), all three URL classes.
Per-task records preserved: 812 records, `sum(len(t.program_html)) = 651`, 411 tasks declare
`program_html`. `source_sha256["config_files/test.raw.json"] = 7b50386f…37652` matches the
manifest-pinned input digest I hashed independently before any run.

## Boundary observations (agree with instrument semantics, checked on data)

- Locator `full_page` keyed on empty-string after `.strip()`; population contains zero
  whitespace-only locators, so strip-vs-raw-equality cannot diverge here.
- URL `helper` keyed on `startswith("func")` (not `func:`); all 75 observed `func` URLs have the
  colon, so prefix-vs-colon semantics cannot diverge here; `target_url_func_malformed` never fires.
- Locator `javascript` covers both `document.` and `[...document.` prefixes; both families present.

## Findings

None. Independent census (two distinct implementations), production `--json`, and candidate cells
agree on 651 targets and all six class counts. Both class histograms partition 651 exactly
(105+524+22 = 238+338+75 = 651). No silent exclusion, no unsupported/malformed entries hiding
outside the histograms.

Residual gap (not a defect): class definitions are instrument conventions; data exhaustively shows
only the three families per axis, so no hidden fourth family exists. Semantic correctness of the
helper/JS locator strings themselves (e.g., unclosed selector brackets flagged in Task356/759/424)
is out of this metric's scope and separately disclosed in the candidate.

## VERDICT: PASS
