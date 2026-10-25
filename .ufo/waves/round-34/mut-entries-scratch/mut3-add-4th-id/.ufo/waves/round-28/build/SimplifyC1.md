# C1 declared-interface simplification review

Writer/seat: KengakuR28.SimplifyC1-2 (author-side advice only). Date: 2026-10-21.

## Axes and scoped verdict

Axes: novelty mapped to canonical coverage/constructs (7 held); source fidelity; per-task auditability; implementation weight; calibration (8 held, not independently evaluated here).

**PASS — declared C1 can be satisfied by a static inventory without a second scorer. PARTIAL — production implementation, its CLI checks, and completion of the 16 prose audits were not reviewed or certified.** This is not a round PASS, benchmark-validity verdict, score increase, or outside closure.

No deletions made; no code changes. Recommendations below are design-level deletion/avoidance candidates, not proven-dead functions. The declared interface itself does not require an evaluator abstraction hierarchy. At review time the lane `plans/` listing did not contain `benchmark_spec_audit.py`; this review addresses the preregistered interface, not a writer's separate clone.

## Binding contract retained

`plans/round-28-claims.md:8,15–21` requires complete 812-task structural inventory, exact per-task JSON, source hashes checked before calculation, static scorer-contract tracing, and 16 deterministic intent/evaluator audits. Preserve all CLI forms (`--root`, `--summary`, `--json`, `--selftest`), exit0/1/2 meanings, missing/tampered-input findings, and scope/limitations. No import/eval/exec of upstream code, network, browser task execution, or scoring port is necessary.

Smallest recommended representation (a recommendation, not a new required schema):

1. **One pinned-input authority:** retain the existing manifest, upstream revision, URLs, SHA-256 and byte lengths. Output references the manifest and reports verification; do not maintain another manually edited pin catalog. Retain LICENSE and historical provenance.
2. **One lossless task record per raw array element:** source JSON pointer/index plus the original task object, including task ID, intent, sites, login/reset flags and complete eval object. Keep array index as identity as well as task ID so duplicate IDs remain visible. Preserve null, absent, empty, value type, list order and every target's optional `prep_actions`; do not convert raw values into a lossy normalized evaluator language.
3. **Derived summaries only:** task/unique/duplicate/missing-ID counts, site-set/eval-type-set strata, flags, string operators and values, URL targets/notes, HTML target counts/locators/content operators. Derive these from the same raw records, not a parallel handwritten table. Named convenience fields are acceptable if generated, never a second authority.
4. **A small located static contract inventory:** the three routed evaluator types and the pinned AST/source spans supporting their accepted fields and branch semantics. Straightforward functions/tables suffice; no plugin registry, runtime evaluator objects, strategy protocol, adapter hierarchy or executable score callbacks. This must still inspect the pinned scorer AST, not replace tracing with an ungrounded constant list.
5. **Exactly 16 case audit records:** reference frozen task IDs and source pointers, record intent, exact targets/operators, checked/unchecked aspects and uncertainty. Quote targets when necessary for readable audits, but reconcile quotes against the lossless record. Generate summary/text/JSON from one audit result; CLI presentations are not separate implementations.

## Concrete weight to avoid, with boundaries

- Avoid porting string cleaning/tokenization/fuzzy judging (`evaluators.py:78–170`), URL matching (`187–239`), HTML selection/content execution (`258–333`), or evaluator multiplication (`336–374`). Record what those branches do; do not compute benchmark scores. A second scorer would add behavioral obligations without increasing the declared task-spec coverage.
- Do not flatten all operators into one generic AND/OR evaluator. String reference approaches are iterated (`137–169`); HTML uses `exact_match` before `must_include` via `if/elif` (`305–328`); URL has a default note and its own query/base-path handling (`213–239`). Retain raw operators and describe effective branches; two present HTML keys are not necessarily two executed checks.
- Do not replace source target strings with only helper names, host categories or selector counts. HTML target URLs, locators and optional preparation actions have distinct roles (`262–299`). Keep them as inert strings. Static helper references are sufficient; helper bodies need not become runnable adapters.
- Do not normalize inactive evaluator fields into required non-null objects. The frozen raw data contains 477 null `reference_answers` and 7 null `reference_url` values. Located examples: raw JSON `1423–1428` (URL evaluation with null answers) and `3809–3813` (null URL with HTML targets). Validate requirements conditional on declared evaluator types. Preserve malformed data as findings rather than silently dropping it.
- Keep the independent oracle and hand-expected selftests: independent re-derivation is deliberate evidence, not a duplicate production authority (`claims:21`). Likewise the 16 audits cannot be deleted merely because a census exists. Stop simplification before removing these independent evidence axes.

## Observed evidence

A data-only stdlib JSON census (not upstream execution and not a production check) found 812 records, 812 unique IDs, range 0–811; 27 site/evaluator strata; five evaluator-type sets: string_match325, url_match66, program_html282, string_match+url_match10, program_html+url_match129 (sum812). Re-deriving the declared first16 sorted-strata minimum-ID selection exactly matched `selected-task-ids.json`: 389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399. This supports retaining the denominator and sampling contract; it does not certify the missing production instrument or case prose.

Observed HTML target keys: `locator`, `prep_actions`, `required_contents`, `url`; answer operators: exact_match/fuzzy_match/must_include; HTML content operators: exact_match/must_include. An initial exploratory comprehension failed with TypeError on null reference answers; the corrected census handled null only for counting. This is disclosed exploration failure, not an upstream or production-check failure, and not permission to erase nulls in the proposed lossless output.

### Opened source locations

All below were opened as local pinned source data on **2026-10-21**; URLs identify provenance, not a live-site fetch. Quotes are at most25 words each.

- Raw tasks: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json — local `plans/fixtures/r28/webarena/config_files/test.raw.json:19–23`: `"eval_types": [ "string_match" ], "reference_answers": { "exact_match": "Quest Lumaflex™ Band"` (Unicode escape decoded for display). Scope: one located example; full denominator from the separate data census.
- Scorer: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py — local `evaluation_harness/evaluators.py:361`: `eval_types = configs["eval"]["eval_types"]`. Scope: router field authority; concrete router branches at365–372.
- Helper: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py — local `evaluation_harness/helper_functions.py:38–39`: `def shopping_get_latest_order_url() -> str:` / `Get the latest order url from the shopping website.` Scope: helper purpose only; static source shows network dependencies, not observed runtime behavior.

## Commands, isolation, limitations and tradeoff

Observed shell command, run twice read-only from lane root: `sha256sum plans/round-28-claims.md plans/fixtures/r28/webarena/manifest.json plans/fixtures/r28/webarena/config_files/test.raw.json plans/fixtures/r28/webarena/evaluation_harness/evaluators.py plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py`. All five digests were byte-identical between readings. Raw/scorer/helper digests matched manifest values: respectively `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22`, `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275`.

Only this assigned report was written. No scratch mutation experiment, production edit, Git/index operation, install/update, upstream execution, benchmark-site contact, REA call, build/test/lint/formatter or production audit invocation occurred. Read and data-only analysis do not require a mutable scratch copy. Protected reviewed inputs were unchanged; no whole-shared-tree byte-identity claim is made amid concurrent author work. No LSP device is available in this seat, and no semantic no-caller proof or concrete code deletion is claimed; text search was only source-location evidence.

Narrow retained-behavior check for the integration owner: the preregistered instrument summary/JSON and hand-expected selftest, with independent census comparison and 16 located case rereads. Not exercised here. Q13 structural evidence is not endorsement. C2, prior P4 offline/superseded boundaries, endpoint restoration, scientific-method novelty and actual task success remain outside this verdict.

Tradeoff: retain a little raw-data/output redundancy to preserve exact reconstructability and readable case evidence; remove only a hypothetical second semantic authority, not the raw source, oracle or audits. Further deletion of per-task values, pins, 812 denominator or 16 audits would harm auditability/coverage and is rejected.
