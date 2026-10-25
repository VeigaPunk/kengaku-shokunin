# R29CritResidualMarkers — residual-marker attack on six-token resolution

Seat: KengakuR28.R29CritResidualMarkers-2 (critic, leaf). Actual writer: this seat's agent (Cursor, model "Auto").
Scope: does the survival of `__last_url__`, `__page__` and other non-env markers falsify the declared
six-env-token resolution of round-29 C1? This is author-side review, not outside closure or round admission.
No production edits, no installs or updates, no network, no upstream import/exec. `generate_test_data.py`
and `evaluators.py`/`helper_functions.py` were read as text only.
Scratch (own): `.ufo/waves/round-29/scratch/R29CritResidualMarkers/` — `census.py`/`census.out`,
`census2.py`/`census2.out`, `helper_tasks.out`, `order_wiki.out`, `mutants.py`/`mutants.out`, `quotes.out`.

## Inputs (sha256 recomputed via `sha256sum`, all equal to manifest pins)

- `plans/fixtures/r29/manifest.json` f6390b92…bf87
- `plans/fixtures/r29/generate_test_data.py` 45ddba7b…21cd
- `plans/fixtures/r29/profiles.json` 90fdc34d…e018
- `plans/fixtures/r28/webarena/config_files/test.raw.json` 7b50386f…7652 (880776 bytes)
- `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` e23edb39…0c22 (= r28 webarena manifest)
- `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` ec758da4…e275 (= r28 webarena manifest)
- Lane HEAD `31934e5` (prereg), parent `ed26bdf` (baseline).

## Census (units kept separate: raw-text occurrences / decoded string-leaf occurrences / tasks)

Raw text: 880776 codepoints, 0 non-ASCII, 49 `\uXXXX` escapes. 812 tasks, 812 distinct task_id.
Maximal dunder identifiers `__ident__` in raw text (regex `__([A-Za-z0-9]+(?:_[A-Za-z0-9]+)*)__`):

| identifier | raw-text occ | decoded-leaf occ | tasks | leaf paths |
|---|---|---|---|---|
| `__GITLAB__` | 385 | 385 | 204 | start_url, program_html.url, reference_url, must_include |
| `__REDDIT__` | 336 | 336 | 128 | same + reference_answer_raw_annotation (2) |
| `__SHOPPING_ADMIN__` | 300 | 300 | 182 | start_url, program_html.url, reference_url |
| `__SHOPPING__` | 281 | 281 | 192 | start_url, reference_url, program_html.url |
| `__MAP__` | 133 | 133 | 128 | start_url, reference_url |
| `__WIKIPEDIA__` | 0 | 0 | 0 | — |
| `__last_url__` | 65 | 65 | 55 | only `eval.program_html[].url`, every one inside a `func:` string |
| `__page__` | 12 | 12 | 9 | only `eval.program_html[].locator`, every one inside a `func:` string |

Raw-text count equals decoded-leaf count for every identifier, so no token is hidden behind a `\u` escape.
164 further `__` positions are CSS BEM selectors (`user-bio__biography`, `submission__vote`, `submission__inner`), not markers.
Case-insensitive token counts equal exact counts. No token literal is a substring of another (including SHOPPING inside SHOPPING_ADMIN).
Same-leaf co-occurrence of an env token with `__last_url__`/`__page__`: **0 leaves**. `__last_url__` and `__page__` tasks overlap: 0.

Other non-dunder markers that survive projection: url `== "last"` 238 leaves / 109 tasks; `func:` url leaves 75, `func:` locator leaves 22;
`|AND|` in start_url 5 leaves; `|OR|` in reference_url 7, in must_include 6 leaves; literal http(s) hosts (pages.gitlab.io 4, www.reddit.com 2,
web.cmoa.org 2, egg.tart.com 2, helloworld.xyz 2, www.apache.org 1 raw-text occurrences) are task content, not deployment tokens.

Post-projection, for all three frozen profiles: JSON parses; six known tokens remaining = 0 each; residual dunder set is exactly
`{__last_url__: 65, __page__: 12}`, identical to the raw counts. No profile value contains `__`.

## Source boundary (where the residual markers are consumed)

These markers are substituted at evaluation run time, not at config generation, per the pinned evaluator (line numbers from `quotes.out`):
- `evaluators.py:265` "func = func.replace("__last_url__", page.url)" (4 words)
- `evaluators.py:298` "func = func.replace("__page__", "page")" (4 words)
- `evaluators.py:271` "if target_url != "last":" (4 words)
- The generator's WIKIPEDIA line `generate_test_data.py:15` "raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)" (4 words) has 0 raw matches.
Survival of these markers is therefore the source-faithful output of the generator. It is not a resolution failure. Run-time behavior is NOT
observed here; this is a source reading only.

## Strongest actual objection

The prereg metric is closed over the six known names only: "changed string leaves by JSON path and category, remaining known placeholders;"
(`round-29-claims.md:65`, 11 words), with forecast "F2 remaining six known tokens0, p=.9;" (`:105`, 6 words). A zero for the six names is
**necessary but not sufficient** for "the six-token resolution is complete and the remaining markers are benign". The prereg requires no closed
inventory of non-env residuals and no invariance check on them. Without that, three distinct defects all report six-token remaining = 0
and would pass (bounded in-memory mutants, `mutants.out`):

| mutant | six-only check | closed residual check |
|---|---|---|
| CONTROL frozen raw, distinct_origins | all 0 | no findings |
| M1 seventh env-style token (`start_url "__MAP__"`→`"__HOMEPAGE__"`, one occurrence) | all 0 (passes) | `unclassified_residual_marker __HOMEPAGE__ 1` |
| M2 profile value carrying a runtime marker (`SHOPPING=…/__page__`) | all 0 (passes) | `__page__` 12→293 (12 + 281 SHOPPING occurrences) |
| M3 projector bug that also strips `__last_url__` | all 0 (passes) | `__last_url__` expected 65, got 0 |

On the frozen pinned input M1 is closed by the sha256 pin, which would give exit 2 for snapshot_tampered. M2 is excluded by the frozen profiles.
M3 is an implementation-defect class that the six-only metric cannot see. So none of these falsifies the claim **on frozen data**. They show that the
output, as preregistered, cannot by itself demonstrate that "only `__last_url__`/`__page__` remain, unchanged". This seat's census supplies that
demonstration for the frozen data, but the instrument does not.

Detector choice matters too (M4 on the distinct_origins projection): `__[A-Z_]+__` reports 0 residuals, hiding the run-time markers.
`__\w+__` reports exactly 65/12. The lazy regex `__.+?__` adds 5 spurious matches spanning BEM selectors.

## Related residual-boundary facts (fixable, not falsifying)

1. **WIKIPEDIA is vacuous on frozen data.** 0 raw occurrences. The 23 tasks with `wikipedia` in `sites` (ids 97, 265–268, 424–430, 556–561, 737–741)
   use start_url `__MAP__` (17) or `__GITLAB__` (6), and "wikipedia" appears only in `sites[]` leaves. Every WIKIPEDIA profile value enters 0 projected tasks.
   F2's zero for WIKIPEDIA is true before projection. Effective frozen replacements are 5 of 6, and only the selftest exercises WIKIPEDIA.
2. **Order is unobservable on frozen data.** All 720 permutations of the six replacements yield one identical projected text per profile
   (canonical sha256: distinct_origins 2aec098e…07f4, path_prefix 54cf9833…744b, trailing_slash_sensitivity 49bbee2e…01b2; `order_wiki.out`).
   "ordered replacement behavior and whether index==task_id on the frozen input" (`:69`, 10 words) can only be a null on frozen data. The
   "must have a failing" wrong-order witness (`:99`) can only come from synthetic hand cases. This is consistent with the prereg's cascade selftest,
   but the output must not present frozen-data order evidence as discriminating.
3. **Hidden SHOPPING dependency through helper functions, outside the text channel.** 20 `func:` leaves contain no env token but call helpers that
   build URLs from the imported `SHOPPING` at run time: `shopping_get_latest_order_url` 10 url leaves, and `shopping_get_sku_latest_review_author`/`_rating` 5+5 locator leaves.
   See `helper_functions.py:58` "order_url = f"{SHOPPING}/sales/order/view/order_id/{order_id}/"" (3 words) and `:69,:86`.
   That is 15 tasks (436–440, 506–510, 585–589); all 15 also carry `__SHOPPING__` elsewhere, so the dependency is hidden at field level but not at task level.
   This is a second authority for SHOPPING (the profile text versus run-time env_config) that the projection cannot see. It is outside C1's
   offline claim (no helper behavior claim), so it does not falsify C1. It does mean "known placeholders remaining 0" must not be worded as "environment-resolved".
4. **Codepoint versus byte offsets.** Raw text and all three projections are 100% ASCII, so codepoint offsets equal byte offsets numerically on frozen data.
   Only the UTF-8 selftest case can discriminate the prereg-required codepoint unit.

## Smallest safe correction (no code written by this seat)

Add one required output and one invariant to `config_projection.py` and the oracle; neither touches r28 code or the frozen P2–P4 classes:
- A per-profile **closed residual-marker inventory**: every `__ident__` matched by the identifier regex above (not `__[A-Z_]+__` or a lazy `.+?`).
  Classify each as known env token (must be 0), or allow-listed run-time marker `__last_url__` (expected `program_html[].url` func, 65 leaves / 55 tasks)
  or `__page__` (expected `program_html[].locator` func, 12 leaves / 9 tasks), with evaluator source lines 265/298 as provenance. Anything else gets the stable
  finding `unclassified_residual_marker` and exit 1.
- An invariant that the residual-marker counts in projected text equal those in the raw text, for each profile. This catches M2/M3 classes. A schema check
  that profile values contain no `__` is the cheaper partial form.
- Report per token `WIKIPEDIA raw_occurrences=0` explicitly. Label order evidence and offset-unit evidence on frozen data as non-discriminating,
  with the selftest as the discriminating witness. Label the 20 helper-mediated leaves / 15 tasks as `runtime_env_import_helper`, "not projected; outside claim".
None of these strengthens C1's acceptance beyond its declared scope. They prevent false provenance ("resolved"/"order-verified") and make the
six-only zero non-vacuous.

## Unknowns preserved

Run-time evaluator/helper behavior under any deployment is not observed. Whether upstream at other revisions has a seventh token is not examined
(no network). The raw-text `\u` escapes were bounded only by the count-equality check, not decoded individually. Operator-reported r28 admission was not rechecked.

## Commands run (all read-only except own scratch writes)

`sha256sum` on the six inputs; `git log --oneline -3`; `python3 census.py`, `python3 census2.py`, `python3 mutants.py`, plus inline `python3 -` blocks
recorded in `helper_tasks.out`, `order_wiki.out` and `quotes.out`; `rg -n` over the pinned evaluator/helper files. Tools installed/updated: none.

VERDICT: PASS
Scope of this verdict: `__last_url__`/`__page__` and the other listed markers remain without falsifying the declared six-token resolution on the frozen
pinned input under all three profiles. The closed residual inventory and invariance check above are fixable instrument defects, required before
"remaining known placeholders 0" is cited as residual-completeness evidence. This is not round admission.
