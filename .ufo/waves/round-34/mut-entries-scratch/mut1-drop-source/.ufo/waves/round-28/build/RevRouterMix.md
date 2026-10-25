# RevRouterMix — evaluator_router / EvaluatorComb review (round 28, author-side)

Writer/seat: `KengakuR28.RevRouterMix-2` (reviewer, leaf — no subagents). Date: 2026-10-21.
Scope: exactly `evaluator_router` and `EvaluatorComb` — dispatch and mixed-type multiplicative scoring — in the pinned snapshot, plus the contract and hand-expected cases the new audit (`plans/benchmark_spec_audit.py`) must satisfy for these two symbols. This is author-side advice, not outside non-author closure.
Trailer path: `.ufo/waves/round-28/build/RevRouterMix.md` (relative to `/home/vgpnk/Projects/shokunin/kengaku-shokunin`).

Godspeed axes named: **novelty** (judged — findings must be new ground vs sibling reports), **groundedness** (every claim line-anchored to pinned bytes), **actionability** (cases the audit selftest can adopt verbatim), **harm-none** (no upstream execution, no network, no production edits, no validity claims). Moves kept: dead-field census, phase-separated error contract, ordered-chain uniformity proof, vacuous-factor classes; nothing narrowed the scope.

## Inputs and observed commands

- Pinned sources read in full: `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` (374 ln), `evaluation_harness/helper_functions.py` (221 ln), `config_files/test.raw.json` (812 tasks), `manifest.json`.
- Read-only instrument reviewed: `plans/benchmark_spec_audit.py` (262 ln, lane copy; the ExecBenchmark worktree did not yet contain `plans/benchmark_spec_audit.py` at review time — it carries the lane file set only).
- Digest verification before any counting (`sha256sum`): all four snapshot files match `manifest.json`; `manifest.json` matches the instrument's `MANIFEST_SHA256` pin (`c78b1478…23a6dd`); `selected-task-ids.json` matches `SELECTION_SHA256` (`5f7eea2e…f3ed17a`) and contains exactly the pinned 16 IDs. Remote byte-equality to upstream dce04686 is attested by OpenScorer's fetch, not re-fetched here.
- Census: stdlib `python3` parse of `test.raw.json` only (script kept at `.ufo/waves/round-28/scratch/KengakuR28.RevRouterMix-2/census.py`, outputs in `NOTES.md`). `grep` counts for `client`/`get_last_state` usage. **No tool installs or updates were performed.** No builds/tests/linters run; no upstream code imported/executed; no network access.

## A. Source-anchored contract — dispatch

`evaluator_router(config_file)` (`evaluators.py:355-374`), `@beartype` on `config_file: Path | str`:

1. Opens and `json.load`s `config_file` (`:358-359`) and reads `configs["eval"]["eval_types"]` (`:361`). Missing `eval`/`eval_types` → `KeyError`; non-dict `eval` → `TypeError`/unhashable — **construction-phase** failures needing no trajectory.
2. Builds one evaluator per entry, **in list order** (`:363-370`): `string_match`→`StringEvaluator()`, `url_match`→`URLEvaluator()`, `program_html`→`HTMLContentEvaluator()`. Order is preserved and is semantically load-bearing (§C4).
3. Any other entry → `ValueError(f"eval_type {eval_type} is not supported")` (`:371-372`) — **construction-phase** (raised before any page/trajectory exists).
4. Duplicates are **not** rejected: `["url_match","url_match"]` yields two instances; the product squares a binary URL score, and a duplicated fuzzy string evaluator would call the LLM judge twice.
5. Empty list is accepted: `EvaluatorComb([])` then returns `1.0` unconditionally (`:348-352`) — a vacuous pass.
6. Returns `EvaluatorComb(evaluators)` (`:374`).

`EvaluatorComb.__call__` (`:336-352`), `@beartype` on `(trajectory: Trajectory, config_file, page: Page|PseudoPage, client: CDPSession)` — `client` is required here even though every dispatched evaluator ignores it (`grep`: `client` appears only in signatures and the pass-through `:350`; no body use — dead at scoring time).

Per-evaluator read-sets (what each dispatched evaluator actually reads):

| evaluator | reads | ignores |
|---|---|---|
| StringEvaluator (`:123-170`) | `trajectory[-1]["answer"]` via `get_last_action` (`:133-134`), `eval.reference_answers`, `eval.string_note` (N/A branch only), `configs["intent"]` | `page`, `client`, `eval.reference_url`, `program_html`, `trajectory[:-1]` |
| URLEvaluator (`:177-241`) | `page.url` (`:212`), `eval.reference_url` split on `" \|OR\| "` (`:213`), `eval.url_note` default `"GOLD in PRED"` (`:215`) | trajectory, `reference_answers`, `program_html` |
| HTMLContentEvaluator (`:248-333`) | `eval.program_html` targets: `url` (eval'd if `func`-prefixed `:263-266`, `page.goto`+`time.sleep(3)` unless `"last"` `:271-273`), `locator` (empty→`page.content()` `:276-277`; `document.`/`[...document.`→`page.evaluate` `:279-294`; `func:`→`eval` helper `:296-299`; else `ValueError` `:301`), `required_contents` (`:305-332`), optional `prep_actions` (exceptions swallowed `:282-287`) | trajectory, answer |

Dead inputs across all three: `get_last_state` (`:59-68`) is never called by any evaluator; only `trajectory[-1]` is read. `client` is unused. `config_file` is re-opened independently by the router and by every evaluator call (`:130`, `:184`, `:255`) — N+1 disk reads whose consistency is unprovable at runtime (moot for frozen bytes). Beartype asymmetry: `StringEvaluator.__call__` (`:123`) is undecorated while `URLEvaluator.__call__` (`:176`) and `HTMLContentEvaluator.__call__` (`:247`) are `@beartype`.

## B. Source-anchored contract — mixed multiplicative scoring

1. **Across evaluators:** `score = 1.0; for evaluator …: score *= cur_score` (`:348-351`). Pure product; no partial credit, no factor attribution.
2. **Within StringEvaluator** (`:136-170`): product over `reference_answers` approaches — `exact_match` (cleaned equality `:90-94`, cleaning = strip → strip one matching outer quote pair → lowercase `:80-86`), `must_include` per element (`:143-149`, `tokenize=(len(value)==1)`), `fuzzy_match` per element (`:164-169`).
   - **The single non-multiplicative override in the whole harness:** in the `fuzzy_match == "N/A"` branch, `if score != 1: score = 1.0 * self.ua_match(...)` (`:152-163`) **assigns**, discarding all earlier factors. A config `{"must_include": ["x"], "fuzzy_match": "N/A"}` whose pred misses "x" but whose reason matches `eval.string_note` scores **1.0**, not 0.0.
   - **Tokenize quirk:** the token path requires `tokenize and len(clean_ref) == 1 and len(word_tokenize(clean_ref)) == 1` (`:103-109`) — the comment says "single word" but the code tests single **character**. With `tokenize=True` only when the list has exactly one element (`:148`), the token path is exercised exactly when a single-element `must_include` holds a one-character ref (31 tasks in the population, e.g. 132 `["1"]`, 14 `["0"]`).
3. **Within URLEvaluator** (`:212-241`): `base_score` = any ref base path (`netloc+path`, `:192-197` returns **str**) **contained as a substring** in the predicted base (`:220-227`) — substring, not host equality, so `x.com/item` passes inside `shop.x.com/item/extra`; fragments ignored; per-key query factor = any merged `|OR|` alternative value present (`:228-236`); extra predicted query keys ignored; empty `""` reference would vacuously pass (empty string is contained anywhere). Any `url_note` other than the `"GOLD in PRED"` default → `ValueError` — **call-time** phase (`:238-239`).
4. **Within HTMLContentEvaluator** (`:258-333`): product over targets; per target, `exact_match` wins over `must_include` via `elif` (`:305-314`) — a both-keys target silently ignores `must_include`; `must_include` items split on `" \|OR| "` with any-alternative substring semantics (`:315-327`); locator/JS exceptions → `selected_element = ""` (`:288-294`), prep_action exceptions silently pass (`:283-287`) — so a failing locator plus `exact_match: ""` scores 1.0 vacuously; unknown locator or unknown `required_contents` keys → `ValueError` — **call-time** phase (`:301`, `:329-332`).
5. **Phase separation the audit must encode:** dispatch errors (unknown eval type) surface at construction with no trajectory; `url_note`, locator, and `required_contents` errors surface only at call time; `prep_actions`/locator failures never surface at all (silently absorbed into `""`/no-op).
6. **Score range:** binary (0.0/1.0) is provable for URL, HTML, and non-fuzzy string factors from `float(bool)` returns; factors delegating to `llm_fuzzy_match`/`llm_ua_match` (`:115-121` → `helper_functions.py:146-208`) are opaque at this scope (S063 boundary). Mixed combos are therefore provably binary only on their non-fuzzy factors.

## C. Population facts the audit's output must reproduce (independent first-hand census)

812 tasks; `task_id` int 0..811 contiguous, 0 duplicates. Chains: `string_match` 325; `program_html` 282; `[url_match, program_html]` 129; `url_match` 66; `[string_match, url_match]` 10; **no** other combo, 0 empty, 0 duplicates, 0 unknown types. **Order is 100% uniform**: all 129 mixed url+html chains are url-first; all 10 string+url chains are string-first. Distinct `(sites, sorted eval_types)` strata: 27.

Nulls/dead fields: `eval.reference_answers` null on 477 tasks; `eval.reference_url` null on 7 (program_html-only tasks 118, 356, 369–373); task 247 is string-only with a prose `reference_url` ("Valorie doesn't have a email in the system") that no evaluator ever reads. `eval.string_note` present on 335 tasks, non-empty on 36.

String operators (335 string-dispatched tasks): `exact_match` 45, `must_include` 176 (98 single-element, 78 multi-element; **31 tasks** take the token path), `fuzzy_match` 118 (82 lists + 36 `"N/A"`); all 36 N/A configs are single-key string-only with `eval.string_note` present — so the §B2 override is **latent** (0 live occurrences). URL: 205 tasks, `reference_url` always non-empty; 7 use `|OR|` (604, 608, 609, 625, 681, 682, 683 — all alternatives non-empty); `url_note` "GOLD in PRED" 196 explicit + 9 absent-default + 0 non-default. HTML: 651 targets — locator full_page 105 / javascript 524 / `func:` 22 / unsupported 0; target url `last` 238 / navigation 338 / `func`-prefix 75; operators `must_include` 463 / `exact_match` 188 / both 0 / neither 0; `prep_actions` 10; 5 `|OR|` must-include items, all alternatives non-empty; 0 empty `exact_match`, 0 `""` items.

Selected-16 mixed representation: 590 and 681 (url+html), 173 (string+url); 791 exercises fuzzy N/A + `string_note` "the subreddit does not exist"; 132 exercises the single-char token path (`["1"]`). These counts match OpenScorer's independent parse everywhere both exist.

## D. Hand-expected schema/semantic cases for the new audit

Format: config → expected instrument behavior | expected runtime semantics per §A/§B. ✅ = current selftest covers; ❌ = missing.

- **H1 ❌→✅ unknown type**: `eval_types:["recon"]` → finding `unknown_eval_type`, exit 1 | runtime: construction-phase `ValueError` (`:371-372`), no trajectory needed. Covered (`unknown_evaluator`).
- **H2 ❌ empty chain**: `eval_types:[]` → instrument `eval_types_invalid` (stricter than runtime) | runtime: `EvaluatorComb([])` → unconditional 1.0 vacuous pass (`:348-352`).
- **H3 ❌ duplicate type**: `["url_match","url_match"]` → finding `duplicate_eval_type` | runtime: two instances, product squared (idempotent for binary URL; double LLM call if fuzzy string duplicated).
- **H4 ❌ ordered mixed chain**: `[url_match, program_html]` (pinned 590, 681) → chain `[URL, HTML]` recorded in order; URL scores `page.url` **before** HTML's `page.goto` navigates away; reverse order would make URL score a helper-navigated page. Population is uniform url-first (129/129), so the hazard is latent.
- **H5 ✅ string exact**: pinned 7, ref "Pittsburgh International Airport, …, United States" → cleaned equality.
- **H6 ❌ single-char token path**: pinned 132 `["1"]`: pred "1" → 1.0; pred "21" → **0.0** although `"1" ∈ "21"` as substring — token membership beats substring. 31 tasks take this path.
- **H7 ❌ vacuous string factors** (synthetic, 0 in population): `must_include:[]` and `[""]` and `fuzzy_match:[]` → runtime factor 1.0 unconditionally; instrument's `all(...)` schema accepts them.
- **H8 ✅/❌ fuzzy N/A single-key**: pinned 791 → pred cleaned `"n/a"` ⇒ 1.0; otherwise `score = 1.0 * ua_match(intent, eval.string_note, pred)` — assignment, not multiply. Schema covered (`na_requires_reason`/`na_reason_present`); the override semantics are not stated anywhere in instrument output (ME1).
- **H9 ❌ N/A + earlier zero** (synthetic; 0 live occurrences): `{"must_include":["x"],"fuzzy_match":"N/A"}`, pred misses "x", ua_match→1.0 ⇒ runtime **1.0**. Any score model that multiplies here mispredicts; this case locks the override.
- **H10 ❌ URL containment + OR**: pinned 44/681 → base test is substring of `netloc+path` (`x.com/item` passes inside `shop.x.com/item/extra`); per-key any-of over merged `|OR|` values; extra query keys and fragments ignored. `reference_url` `|OR|` structure is currently schema-unchecked; an empty alternative would vacate the base factor (population: 7 OR urls, 0 empty parts — verified).
- **H11 ✅ url_note**: absent → default `"GOLD in PRED"`; any other value → finding `url_rule_unsupported` | runtime call-time `ValueError` (`:238-239`). Covered (`unknown_url_rule`).
- **H12 ❌ html elif precedence** (synthetic; 0 both-keys in population): `required_contents:{exact_match:"A", must_include:["B"]}` → exact wins, `must_include` is dead data both at runtime and in the instrument's winner-only validation; flag as informational, not error.
- **H13 ❌ html failure absorption** (synthetic): locator raises → `selected_element=""` → `must_include("x")` 0.0, but `exact_match("")` would pass vacuously; `prep_actions` exceptions always silent. Instrument is schema-only here.
- **H14 ✅/❌ html OR items**: 5 live items, all alternatives non-empty; any-alternative substring passes, ANDed across items. `hand_html` feeds `"x |OR| y"` as schema input only.
- **H15 ❌ vacuous URL factor** (synthetic): `reference_url:""` with url dispatched → runtime base `""` contained always ⇒ 1.0 any URL; instrument flags `reference_url_invalid` (deliberately stricter; population 0).
- **H16 ❌ dead-field visibility**: pinned 247 — string-only, prose `reference_url` never read; plus 477 null `reference_answers`, 7 null `reference_url`, dead `string_note: ""` on 299 tasks, top-level `string_note` (task 723) never read anywhere. Correct behavior = record raw, no finding; recommended: derive an `evaluated_fields` marker from the chain so presence ≠ checked is machine-visible.

## E. What a static task-spec inventory cannot prove

1. That any predicate is satisfiable on a live trajectory — no score value is decidable statically.
2. Helper and LLM-judge outputs and correctness (`func:` target URLs and locators call network helpers; `llm_*` verdicts) — S063 boundary; `browser_env`/`llms` are not in the snapshot.
3. Semantics of dynamic strings: `func`-prefixed target URLs, `func:` locators, JS locators, `prep_actions` — presence/shape only.
4. Runtime page state per evaluator: the audit proves ORDER from `eval_types` (statically: url-first in 129/129; the goto-then-score hazard is latent), but not which page state each evaluator actually observed.
5. `page.url` ↔ trajectory correspondence — URLEvaluator scores eval-time `page.url`; trajectory actions are unchecked beyond the last answer.
6. `__GITLAB__`-style placeholder → live host mapping — substitution happens outside the frozen files; only raw templates are pinned.
7. Intent satisfaction / task validity — e.g. pinned 590 requires "Jan 16, 2030" while intent/instantiation say 1/16/**2023**: an observable intent-vs-evaluator discrepancy to RECORD with uncertainty, not adjudicate (and not evidence of task invalidity).
8. Runtime consistency of the N+1 `config_file` reads; adequacy of `time.sleep(3)`; beartype's runtime effects (decorator asymmetry documented statically only).

## F. Instrument review — findings by severity

All against `plans/benchmark_spec_audit.py` (lane copy). No finding changes this snapshot's counts or exit codes; every gap below has 0 live incidence or is an output-enrichment item.

- **ME1 (Medium — claims coverage).** "Scorer contracts traced" is satisfied only weakly: `contract_anchors` is a name/line inventory from `ast.walk` (`:173-180`) plus source sha pins; nothing in the output states the dispatch table, the product law (`:348-351`), the N/A override (`:152-163`), or phase labels. The schema predicates are hand-derived with no in-instrument statement tying them to the pinned scorer semantics. Recommendation: add a static `SCORER_CONTRACT` block to the output (dispatch map, product law, single override, construction-vs-call-time error phases) derived from the sha-pinned bytes — no upstream execution needed — and lock it with H4/H8/H9.
- **ME2 (Medium).** `reference_url` `|OR|` structure unchecked (`:126-130` checks non-empty str only): an empty alternative would vacate the URL base factor at runtime. Population verified clean (7 OR urls, 0 empty parts). Add alternatives-non-empty schema check + H10 selftest.
- **ME3 (Medium-Low).** Ordered-chain information is erased in metrics: `eval_type_sets` counts `",".join(sorted(kinds))` (`:85`, `:152`). Per-record `eval_types` retains order (`:141`), so no data loss, but the 129/129 + 10/10 order uniformity (a real latent-hazard fact) is not machine-checkable from the output. Add an ordered `eval_type_chains` counter.
- **LO1 (Low).** Vacuous-factor schema classes absent: empty `must_include`/`fuzzy_match` lists, `""` items, `""` `exact_match` all pass as SCHEMA_COMPATIBLE while being runtime-vacuous or near-vacuous (§D H7/H13). 0 incidence here; optional enrichment, never a validity claim.
- **LO2 (Low).** Both-keys targets validate only the elif winner (`:130-139`) — runtime-faithful, but the ignored loser's malformed value is silently dead; 0 incidence. Informational flag recommended.
- **LO3 (Low).** `eval_types_invalid` fallback `kinds = []` makes `",".join(sorted(kinds))` add a `""` bucket to `eval_type_sets` (`:81-85`). Cosmetic; 0 incidence.
- **LO4 (Low).** Records carry raw fields but no evaluated/unread distinction (§D H16); presence-vs-checked is currently prose (`unchecked` list), not per-record.
- **INFO (correct as-is, keep).** Digest-gate order manifest→files→selection with stable exit-2 ids (`:159-172`); selection = min per sorted stratum, first16, pinned-file comparison (`:150-152`, `:174-176`); strict finding-id-set selftest assertions (`:186-214`); elif precedence encoded with the source-matching comment (`:130`); the URL-vs-locator prefix asymmetry (`func` vs `func:`) correctly mirrored (`:26-34` vs `:127`). Deliberate strictness divergences from runtime (H2, H3, H15, missing `reference_answers`/`program_html` flagged while runtime vacuous-passes or `KeyError`s) are sound but should be listed in LIMITS as "stricter than runtime" so nobody overclaims semantic equivalence.

## G. Required code/output checks (recommendations for the delivered instrument)

Code: (1) digest gate precedes all computation with stable `manifest_tampered`/`snapshot_tampered`/`input_missing`/`selection_tampered` exit-2 ids — present ✓; (2) parse-only — verified by reading: stdlib imports only, `ast.parse` of pinned sources, no `import`/`eval`/`exec` of upstream modules ✓; (3) router model = ordered chain + unknown-type finding + duplicate/empty strictness — present ✓, add H2/H3/H4 selftests; (4) composition statement per ME1 with H8/H9; (5) determinism (pure function of pinned bytes) ✓. Output: per-task record with ordered `eval_types`, `schema_status`, `unchecked` — present ✓; add `evaluated_fields` (LO4), ordered chain counter (ME3), OR-alternative check (ME2); aggregate denominators must equal the §C table at integration (two-way reconcile against the oracle seat's independent recount); 16 case reports must include 590/681/173 and record 590's date mismatch as observation. No validity field anywhere — present ✓, keep.

## H. Field presence ≠ task validity

The instrument's binary `schema_status` + fixed `unchecked` list correctly refuses validity claims; §C's dead/null-field census (477 null `reference_answers`, 7 null `reference_url`, task 247's dead prose predicate, 299 dead empty `string_note`s) is the concrete demonstration that a complete-looking config can carry unread or vacuous declarations. Conversely §D's vacuous-factor cases show present-and-typed fields can constrain nothing. The audit's schema verdict classes must stay "constraining / vacuous / malformed / unknown", never "valid/invalid task"; 590's intent-vs-evaluator discrepancy is recorded, not adjudicated.

## Limitations

Static reading + stdlib JSON census of the frozen snapshot only; no upstream execution, no browser, no LLM judge, no network (remote byte-equality attested by OpenScorer, not re-fetched). The ExecBenchmark worktree had no diverging copy of `benchmark_spec_audit.py` at review time, so findings target the lane copy as of 2026-10-21 and must be re-checked at integration if it moves. Helper-function semantics (`llm_*`, site helpers) are excluded (S063's scope). Login/reset flag semantics and per-task case reports belong to other seats. [INFERENCE] items: the `func` vs `func:` prefix-distinction intent, and the deliberate-strictness rationale, are my readings of code, not author statements.

## Verdict

**PASS (scoped)** for this review's deliverable: the router/comb contract is fully source-anchored (`:336-374` plus factor laws), the mixed-multiplicative law and its single N/A override are pinned with hand-expected cases (H1–H16), the population census is first-hand and reproducible (`census.py`), and it independently confirms OpenScorer's counts. **PARTIAL (recommendation) for the delivered instrument's router/comb coverage**: no defect affects this snapshot's counts or exit codes — all four snapshot digests and both instrument pins verify, exit-code contract and parse-only discipline hold — but ME1 (no composition/ordering statement in output), ME2 (unchecked `|OR|` structure), and ME3 (order erased in metrics) should land, with selftests H2/H3/H4/H9/H10, before the round's C1 counting command is treated as complete. This is not a C1, C2, or round PASS.

*Trailer: `.ufo/waves/round-28/build/RevRouterMix.md`; scratch: `.ufo/waves/round-28/scratch/KengakuR28.RevRouterMix-2/` (`census.py`, `NOTES.md`).*
