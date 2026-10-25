# R29CritClaimScope — adversarial claim-scope critique of round-29 C1

Seat: KengakuR28.R29CritClaimScope-2 (critic, leaf). Actual writer: this seat. Author-side critique,
not outside closure, not an admission or judgment. No production edits, no subagents, no installs,
no network, no host env or credential reads. `scripts/generate_test_data.py` was never imported or
executed. It was read as text only.

Scope attacked: whether "2436 task/profile projections" in `plans/round-29-claims.md` (prereg
`31934e5660f1814326c6472eefdfa0c41e642a2f`, base `ed26bdf5d924755697cd6812129be2fa441c42a3`) could
be read as 2436 model trials, 2436 production configs, or a statistical generalization. Operator-reported
r28 admission (rounds[423]) is taken as given and was not rechecked.

## Sources (opened 2026-10-21, lane-relative)

- `plans/round-29-claims.md` (108 lines), `plans/fixtures/r29/{manifest.json,profiles.json,generate_test_data.py}`,
  `plans/fixtures/r28/webarena/config_files/test.raw.json`, `SCORECARD.md:928`, `PROVINCE.md:201`,
  `corpus/knowledge/webarena-task-spec-audit.md:85`, `README.md`.
- Pin check (`sha256sum`): generator `45ddba7b…d921cd` (838 bytes per `wc -c`), manifest `f6390b92…7bf87`,
  profiles `90fdc34d…e018`, raw `7b50386f…37652`. All four match the manifest and the claims file.

## Commands run (scratch: `.ufo/waves/round-29/scratch/R29CritClaimScope/`)

1. `python3 census.py`: my own stdlib census of the raw JSON. It does six ordered `str.replace` calls per profile,
   then `json.loads`, then a leaf comparison. It is independent of any production code because
   `plans/config_projection.py` does not exist in this tree. These are critic numbers, not the delivered
   tool's output, and they do not score F1–F5.
2. A read-only census of the `sites` field, multi-token `start_url` values, Task590, and non-URL leaves (inline `python3 -`).
3. `python3 quotes.py`: checks that each quote is an exact substring of its cited line and counts its words with `str.split`.
   Output: `ALL_OK True`, with 10 quotes of 4–14 words each.

Observed census output (units are labeled):

| Quantity | Unit | Value |
|---|---|---|
| raw bytes / Unicode codepoints / non-ASCII codepoints | bytes / codepoints | 880776 / 880776 / 0 |
| tasks, distinct task_id, index==task_id for all | tasks | 812, 812, True |
| raw occurrences GITLAB/REDDIT/SHOPPING/SHOPPING_ADMIN/WIKIPEDIA/MAP | token occurrences | 385/336/281/300/**0**/133 |
| runtime markers `__last_url__` / `__page__` (not environment tokens) | occurrences | 65 / 12 |
| tasks with ≥1 token | tasks | 812 |
| token-bearing string leaves | leaves | 1416 (start_url 812; program_html url 338; reference_url 205; must_include 60; reference_answer_raw_annotation 1) |
| tokens in JSON keys | keys | 0 |
| `sites` entries tagged wikipedia | tasks | 23 |
| changed leaves per profile (distinct_origins / path_prefix / trailing_slash) | leaves | 1416 / 1416 / 1416 |
| parsed tasks per profile; remaining six tokens | tasks; occurrences | 812 each; 0 each |
| `.invalid:<port>//` occurrences in projected text | occurrences | 0 / 0 / 697 |

## Strongest objection

The claim's disclaimers are adequate on their face. Line 16 of the claims file says
"No new scientific method, actual deployment config, task validity,". The headline count is the weak
point. Line 13 gives "neutral substitution profiles (2436 task/profile projections), including
replacement occurrence/field", but 2436 is not 2436 independent observations of anything:

- **One input, one source revision, three author-chosen maps.** The count is 812 × 3 deterministic text
  transforms of a single pinned file. None of the profiles was sampled from a deployment population, so
  the count supports no generalization, no confidence interval and no "N trials" reading.
- **The structural metrics are the same across profiles by construction.** No profile value contains a
  `__X__` token or a JSON-special character. So per-token occurrence counts, the 1416 changed-leaf set,
  the 812 parsed tasks and the 0 remaining tokens are identical in all three profiles. The only
  profile-dependent signal is the replaced value text. One example is the 697 double slashes that appear
  only in `trailing_slash_sensitivity`. Agreement between the production tool and the oracle on 2436
  projections is therefore one leaf-set agreement repeated three times plus three value maps, not 2436
  confirmations.
- **One of the six tokens is never exercised.** The raw file has 0 occurrences of `__WIKIPEDIA__`. Line 15
  of the source does `raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)`, but it is a no-op on the frozen
  input. So the WIKIPEDIA value in all three profiles never appears in any of the 2436 projections. 23
  tasks are tagged `wikipedia` in `sites`, yet none of their config text contains that token. One sample
  is task 97, whose `start_url` is `'__MAP__'`. How those tasks reach Wikipedia at runtime is not
  observable from config text. That is `[INFERENCE]`/unknown and must stay a source-versus-runtime
  boundary. On the frozen data, the six-token coverage is 5/6 real and 6/6 only in the selftest.

## Decisive bounded counterexample

Suppose a reader cites "2436 projections with oracle agreement" as evidence that the WebArena generated
configuration is correct for Wikipedia tasks under the three profiles. The counterexample is the per-token
row, which shows `WIKIPEDIA = 0` in every profile. Under any WIKIPEDIA profile value, the 2436 projections
are byte-identical to the ones the round would produce. So the count says nothing about WIKIPEDIA
substitution, and the same applies to deployment correctness for the other tokens. It is bounded to this
one pinned input. I make no claim about other WebArena revisions.

## Secondary findings (fixable, not rejections)

1. **The README pointer does not resolve.** Line 15 cites "README's generated-eval-config frontier only for an
   offline source-faithful projection. Score7 held;". The lane `README.md` has 0 case-insensitive matches for
   `frontier`, `generated` and `config` (`rg -c`). The frontier as stated in the lane is
   `SCORECARD.md:928`, "Frontier: generated task configurations/runtime evidence, additional benchmark specs and semantic",
   and `PROVINCE.md:201`, "generated configs, runtime task validity, hosted judges and contamination remain open."
   If line 15 means the upstream WebArena README, it must say so. Either way, the pointer is currently false provenance.
2. **Task590 must not be discharged.** `corpus/knowledge/webarena-task-spec-audit.md:85` says "mismatch exists in
   authored text; actual runtime task invalidity still requires the generated config,". In the projection, Task590
   changes only its `start_url` (`'__GITLAB__/primer/design'`). Its `program_html` urls are `last`, which is a
   runtime marker, not a token. The synthetic `*.invalid` projection is not "the generated config" meant there,
   so the r29 entry must not be cited as closing that condition. The deployed GitLab, the date rendering and
   the reference trajectory are all still required.
3. **The F3 resolution depends on an undefined category.** Lines 64–65 require "changed string leaves by JSON path
   and category, remaining known placeholders;". Line 106 forecasts "F3 global replacement changes at least one
   non-URL-valued field, p=.7;". The non-URL paths that change in my census (must_include 60,
   reference_answer_raw_annotation 1) hold URL-shaped strings. For example, task 552 must_include contains
   `'__REDDIT__/f/space/134164/…'`. So F3 comes out true under a JSON-path category and possibly false under
   a value-shape category. This is not a defect in the task data. It is a forecast-resolution ambiguity.
4. **The units are artifacts versus projections.** Upstream writes `test.json` plus 812 `{idx}.json` per profile,
   which is 813 would-be artifacts per profile and 2439 across the three. The "2436 task/profile projections"
   unit excludes the three whole-file projections. This is fine if it is named. Do not relabel it as "configs written".

## Impacted axes

- **coverage/constructs (C1):** the claim survives in its offline source-faithful scope, but the WIKIPEDIA
  token is not covered by real data.
- **calibration:** F3 needs a frozen category before scoring. F2 is near-trivial given the profile domain,
  and its forecast is already labeled as not independent.
- **novelty:** held at 7, consistent with the claim. Nothing found here supports an increase.
- **provenance:** the README pointer.

No other axis is affected.

## Smallest safe correction (wording and reporting only, no new acceptance gate)

- In the delivered `--summary`, knowledge entry and SCORECARD row, state that 2436 = 812 tasks × 3 synthetic
  profiles of one pinned input, and that it is not trials, configs written, or a sample. Report the structural
  metrics once, with an explicit per-profile equality assertion. Show WIKIPEDIA's 0 occurrences as a named
  zero, and label the WIKIPEDIA profile value as unexercised on the frozen data.
- Replace "README's" on line 15 with `SCORECARD.md:928`/`PROVINCE.md:201`, or explicitly name the upstream README.
- Before F3 is scored, fix its category as JSON-path-based (start_url, program_html url and reference_url are URL
  fields, everything else is non-URL). Score F3 against that list.
- The knowledge entry should carry one line saying the Task590 runtime-invalidity condition remains open.

These corrections do not reopen frozen inputs, P2–P4 classes, r28 code or the manifest pins. None of them asserts
task invalidity.

Unknowns preserved: delivered tool and oracle outputs (not present in this tree), runtime Wikipedia reachability,
and actual deployment env values. All of these were left unread by design.

Tool installs/updates: none.

VERDICT: PARTIAL
