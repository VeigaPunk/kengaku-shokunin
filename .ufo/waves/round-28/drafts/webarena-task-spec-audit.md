source: S061 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json task0:18–28 and selected task IDs below; S062 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py StringEvaluator:71–170, URLEvaluator:173–241, HTMLContentEvaluator:244–333, combination/router:336–374; S063 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py fuzzy/UA:146–208 — byte-pinned snapshots plans/fixtures/r28/webarena/
verified-at: 2026-10-21 — static source opening and frozen input census, not live benchmark execution
recheck: on-release — python3 plans/benchmark_spec_audit.py --summary and --selftest; reopen the three source URLs at the pinned revision
writer: KengakuR28

# WebArena task-spec audit — inventory a scorer's predicates without certifying task validity

## What this adds and what it does not

Extends corpus/README.md Frontier “Agentic benchmark task-spec audits”. The lane previously held
benchmark-selection recommendations and lab self-audit summaries, not a task-spec-to-scoring contract
inventory for this repository. The acquired repertoire is **static task-spec observability**, not a new
scientific method, task-validity seal, model capability result, contamination audit or benchmark run.

The source is the **web-arena-x/webarena repository snapshot dce04686a56253aefba7b18a4fa0937cf1dc987b,
committed2025-11-26**, not its2023-07-25 paper-era release and not WebArena-Verified. Paper-era or
leaderboard performance numbers cannot be attached to these bytes. Build/CritClaimScope independently
found changed scoring fields relative to the release; this entry does not import its comparison count
as a new measured result.

S061 is authoritative for authored specs; S062/S063 for their own code behavior, **not** actual browser
state or judge correctness. The pinned Apache-2.0 LICENSE is retained. Only fixture login-state path
strings occur in the task data; no account/token/cookie values or auth-state files were opened. The
instrument parses JSON and Python AST, never imports/executes upstream source or contacts benchmark sites.

## Authored predicates are narrower than natural-language intent

| source contract | actual predicate (pinned source lines) | what a passing score does not by itself establish |
|---|---|---|
| String exact | S062:80–94 trims, strips one outer quote pair and lowercases before equality; the routed string path also pre-cleans pred at134, so prediction normalization is applied twice | semantic correctness, provenance, permitted side effects or equivalence to direct exact_match on a raw prediction |
| String includes | S062:98–111,142–149 uses substring containment; tokenization only when its tokenize flag is true AND the cleaned reference is one character | semantic equivalence, absence of extra incorrect claims, intended unit or entity |
| String fuzzy | S062:150–169 invokes S063:146–173 for non-N/A references | judge validity, endpoint availability or reproducibility from temperature0 alone |
| Unachievable answer | S062:152–163 accepts exact N/A first, otherwise calls S063:176–208 against string_note | actual impossibility of the task; no-action failure requires environment evidence |
| URL | S062:187–239 strips trailing slash, uses netloc+path substring containment, ignores scheme/fragment and separately checks reference query values | correct rendered content, exact URL identity, task intent completeness or the agent's actions |
| Page content | S062:258–333 selects configured page/locator, unescapes HTML, applies exact_match before must_include; targets multiply | whole-state correctness, action causality, runtime DOM compatibility or fixture freshness |
| Composite | S062:348–352,361–374 executes declared evaluator types in list order and multiplies results; preserve order because page-content checks can navigate | that every intent clause is checked, or that reordering stateful evaluators is equivalent |

URL alternatives split on the exact OR delimiter; query values are pooled across reference alternatives,
not paired with each alternative's base path (S062:199–235). This is source behavior, not a live task
failure rate. HTML targets using `last` do not navigate; other URLs navigate and sleep a fixed interval.
JavaScript selector errors become empty selected text, while helper-call errors have different paths
(S062:271–301). Unknown/missing runtime conditions are not silently reclassified as task failures here.

This normalizer is not idempotent for all quote/whitespace strings: direct exact_match and the routed
string path can differ (build/RevStringExact.md). Page-content exact matching does not use the string
path's pre-clean step. Similarly, the N/A fallback assigns its judge score rather than multiplying into
an earlier accumulated approach score (S062:159); all N/A tasks in the pinned population use only that
approach (build/RevStringFuzzy.md). Composite evaluators still multiply; this is not an all-branches
faithful execution port and no upstream scorer was run.

The two LLM helper branches call gpt-4-1106-preview and interpret response keywords (S063:161–173,
196–208); unexpected replies can reach assertions rather than a normal score. Exact N/A bypasses the
reason judge. These are judge-dependency facts, **not** evidence of judge accuracy or a prompt-injection
attack. No judge request was issued. Upstream dynamic function strings are inspected as text only.

## Deterministic case audits and their limits

The selection is registered in plans/round-28-claims.md: sort (sorted site-set, sorted evaluator-type-set)
strata lexicographically, take each minimum task_id, retain the first16 groups. Persisted selected IDs:
389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399. This is deliberately **not random or
representative**; the shopping site is omitted. The whole raw population remains separately inventoried.
The selected cases also omit dynamic helper URL/locator paths, preparation actions and OR-alternative
content checks (build/RevSamplePopulation.md). Their source contracts are read, but these branches
have no selected task-case witness; static whole-population inventory does not close that coverage gap.

Each task has an author-side, source-anchored intent→predicate audit under .ufo/waves/round-28/build/:

| cases | report paths | important boundary |
|---|---|---|
|389,590,132,173|Task389.md, Task590.md, Task132.md, Task173.md|comment/page state, date-key disagreement, tokenized numeric answer, hosted fuzzy judge|
|44,552,681,791|Task044.md, Task552.md, Task681.md, Task791.md|URL-only navigation, fixed link set, cross-site literals, N/A exact/fallback branch|
|556,356,7,377|Task556.md, Task356.md, Task007.md, Task377.md|README substrings, routing-field predicates, fixed exact address, literal search query|
|759,424,97,399|Task759.md, Task424.md, Task097.md, Task399.md|route inputs not duration, sidebar text not place identity, unit spelling, final profile text|

Illustrative source disagreements, not observed runtime-invalid tasks:

- **Task590:** intent names January2023 dates while configured page-content targets name2030. This
  mismatch exists in authored text; actual runtime task invalidity still requires the generated config,
  deployed GitLab/date rendering and reference-trajectory evidence (Task590.md).
- **Task97:** the graded reference is `914km` while its raw annotation spells `914 km`. The substring
  rule does not normalize units or internal whitespace; whether correct deployed-map answers are rejected
  remains unmeasured (Task097.md).
- **Task356/759/424:** the locators contain unclosed attribute-selector brackets in source. This audit
  does **not** infer browser rejection from bracket counting; engine parsing/runtime DOM is untested.
- **Task173/791:** remote-judge-dependent branches remain runtime-unverified; exact N/A is a separate
  branch. Neither a source-level predicate map nor a static census can settle those scores.

All cases separate “what the scorer checks” from “what the task means” and list required runtime
observations before a validity verdict. Their potential limitations are not a collection of confirmed
benchmark defects. No browser bypass, live site action or benchmark score is claimed.

## Observed static inventory (2026-10-21)

Commands executed on the prospective package: `python3 plans/benchmark_spec_audit.py --summary`
and `--json`; receipts `corpus/evidence/round28-calibration/audit-summary.txt` and
`build-acceptance/audit-current.stdout`. This is a working-tree measurement; the admitting commit's
exact-byte proof must name the shipped revision separately.

| observable | measured value |
|---|---|
| raw tasks / distinct IDs |812 /812, IDs0–811, no missing/duplicate/unexpected IDs|
| evaluator-type sets |string_match325, program_html282, url_match66, string_match+url_match10, program_html+url_match129|
| site/evaluator strata / selected case audits |27 /16; lexicographic rule, not random sampling|
| string operator task counts |exact_match45, must_include176, fuzzy_match118; operators can coexist|
| page-content targets / effective operators |651 / exact_match188 + must_include463|
| locator classes |full-page105, JavaScript524, helper22|
| target URL classes |last238, navigation338, helper75|
| schema findings |0, meaning pinned-source structural compatibility only|

The JSON preserves each complete raw task and explicit reference-approach order. Set histograms use
sorted labels for grouping; ordered evaluator histograms and per-task lists preserve execution order.
The AST-derived scorer-contract block records dispatch, ordered product, the N/A assignment override
and distinct error phases; it is static evidence, not an executable scorer port.

`python3 plans/benchmark_spec_audit.py --selftest` executed21 hand-expected/CLI cases, exit0, including
snapshot/manifest/missing-input rejection and a product-law AST mutation. The separately derived
`plans/fixtures/r28/benchmark_oracle.py` agrees on every metric and selected ID. That alternate code
was also authored by KengakuR28 after the assigned oracle seat died: **independent logic, not independent
authorship**. Build source/case seats supplied separate source censuses; fresh falsification must re-read
these final candidate bytes and reproduce the final counters.

## Operational decision rule

1. Freeze the named repository revision, raw task bytes, scorer/helper bytes, LICENSE and persisted digests.
2. Run the static inventory; distinguish exit0 schema cleanliness from any semantic task-validity judgment.
3. For a task, trace its declared evaluators to the exact predicates, data dependencies and failure branches.
4. Record unchecked intent clauses and runtime evidence needed; do not interpret field presence as validity.
5. Treat hosted judges and mutable state/reset policy as unverified dependencies until observed separately.
6. Keep paper-era releases, revised snapshots and verified successors as distinct populations.

Falsifiers: a pinned input digest changes; a task/evaluator is silently excluded; a recorded operator
contradicts the source branch; a raw task field is lost in the per-task output; or a task report silently
turns an unobserved browser/judge condition into a confirmed success/failure. The main acceptance test
must compare full counters with separately derived logic and returned independent author-side replays.

## Calibration and adjacent scope

The new audit does not count the round28 source-reference diagnostic. That separate calibration claim
reads only its frozen baseline knowledge paths and source rows. Shared sources/lesson bookkeeping are
partitioned by precise rows/cells, not treated as one combined improvement. Scores stay novelty7 and
calibration8; no coverage-cap relief or method-novelty score is inferred.

Benchmark evaluation stays kengaku; general research method stays chousa, reusable testing patterns
stay tameshi, prompt-writing advice stays kotoba, actual web-property operations stay kake. Domain source
trees and benchmark environments remain read-only. Outside admission is roster-external, never a vote
from this lane's own swarm.
