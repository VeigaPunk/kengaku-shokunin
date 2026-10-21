# Round 28 — WebArena task-spec observability and bounded source-reference consistency

Author/coordinator: KengakuR28. Baseline lane master b9b24796277020d1b9b01923b45313d6a565e664.
Round27 was admitted (fleet MANIFEST rounds[411], operator dispatch). Its C2 limits remain: two P4 offline groups and one superseded P4 ID; whole checker includes earlier offline/superseded groups too. No claim here restores endpoints, makes those groups MATCH, or turns P4 into a current-tree census.

## Claims declared before implementation

- **C1: novelty (legacy) → canonical coverage/constructs, lowest non-retired axis 7 (tied capped coverage/surfaces).** Acquire an offline task-spec audit of the pinned original WebArena benchmark: absent instrument (0 audited tasks) → all 812 raw task configurations structurally inventoried, scorer contracts traced, and 16 deterministic task-case intent/evaluator audits. This is new ground in this corpus, not a claim of new scientific method, new model ability, actual task invalidity, contamination freedom, or the different WebArena-Verified release. Score7 held absent justified repricing. Counting command: `python3 plans/benchmark_spec_audit.py --summary` (JSON with `--json`). Whole source snapshot and hashes in `plans/fixtures/r28/webarena/manifest.json`. No upstream code execution or live benchmark services.
- **C2: calibration8.** Freeze literal source-reference coverage for exactly S038 and S049–S060 across the 35 knowledge paths in `plans/fixtures/r28/registry/population.json`. Absent dedicated diagnostic (0 frozen source rows checked) → 13 source rows checked, every frozen standalone source-reference file covered by that row's used-by and a cited source not left queued. Count before and after with the delivered `python3 plans/registry_check.py --summary` on baseline export and final tree. Expected S038 drift is already disclosed, not a new discovery; score8 held. Repair only after reopening its original source; source-row immutable cells remain unchanged. This is literal-reference completeness on a frozen population, NOT semantic citation support, all registry uses, all current assertions or source-truth validation.

Distinct populations and paths make claims independently verifiable. C1 uses only benchmark fixtures/code/case reports and new knowledge; C2 reads only SOURCES and the explicit baseline35 paths. New round28 knowledge and new source rows do not enter C2. Run two-way sandbox revert measurements; C1 counts must survive reverting C2 paths, C2 must survive reverting C1-only paths. Historical state_check.py unchanged unless an actual regression requires a separately disclosed repair; preserve all P2–P4 boundaries.

## C1 interface and frozen sampling

`benchmark_spec_audit.py` uses stdlib and **parses** JSON/Python AST, never imports/evals/executes upstream code. CLI `--root PATH` (default lane root inferred from script), `--summary`, `--json`, `--selftest`. Exit0 valid audit / exit1 failed finding / exit2 could-not-evaluate; summary includes scope/limitations. Verify snapshot sha256 values against persisted manifest before calculating anything; missing/tampered input → exit2 stable `snapshot_tampered`/`input_missing` finding. No hidden network. Separate instrument defects from benchmark observations.

Task population is the complete raw JSON at upstream dce04686a56253aefba7b18a4fa0937cf1dc987b. Inventory: task IDs/duplicates/missing IDs, site-set and evaluator-type-set strata, login/reset flags, string reference match operators, URL notes, program_html target counts/locators/required-content operators. Audit schema compatibility for each declared eval type using pinned scorer contract (static evidence, not browser-level truth). Include exact per-task JSON and aggregate denominators. Unknown evaluator types or malformed task shapes are instrument findings; weak proxies are described as limitations, not invented benchmark FAILs.

Selection rule: form (sorted site set, sorted evaluator-type set), sort the tuples lexicographically, take minimum task_id from each, retain first16 groups. IDs persisted in selected-task-ids.json: 389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399 (ordered by sorted strata). This deliberately bounded/nonrepresentative sample is not a random sample or full task-validity verdict. Every case report records task intent, exact evaluator targets/operators, what is checked, what remains unchecked, source location, and uncertainty. Never issue browser actions, requests to benchmark sites, or scoring bypass demonstrations.

Independent oracle writer must not read/import the production audit implementation. Re-derive JSON aggregate counts directly from the frozen schema and compare at integration. Stock selftests use hand-expected miniature tasks and snapshot corruption/missing/unknown-type/duplicate-ID controls. Mutation tests run on scratch copies; no changes to immutable input snapshots.

## C2 interface and frozen reference contract

`registry_check.py`: stdlib; `--root`, `--summary`, `--json`, `--selftest`, no network or Git writes. Parse the actual registry table under its Registry section (11 content columns), not examples outside it. The13 IDs and35 paths are persisted. Every standalone `S[0-9]{3,}` mention in those paths counts literally (historical/supersession mentions included); additional lesson used-by paths are allowed and not required to match the frozen knowledge-reference set exactly. A missing frozen knowledge file/source row is failure, never silently excluded. Cited rows must be `mined` and list every citing frozen path. Uncited rejected/queued rows are not errors. Validate no duplicate IDs, source-cell enum values relevant to this diagnostic, safe lane-relative used-by paths. Expected observed source references are recomputed, not hardcoded to zero. Persist output per source: citing_files, used_by, missing_used_by, status, finding IDs. Exit0 clean / exit1 mismatch / exit2 input could-not-evaluate. Do not count new sources or new round28 knowledge.

Selftest must be CLI-level with hand-authored fixture expectations for queued+cited, missing-used-by, valid mined citation, duplicate/missing source, missing frozen file, unknown population source, untouched extra source and new-file exclusion. Test quote/code-fence behavior explicitly against the declared literal contract (no claim of semantic Markdown interpretation). Preserve S038 old→new status/recheck/used-by in the lesson; only allowed mutable cells may change.

## Frontier, evidence and admission

Open every new source before adding rows. Proposed S061 raw tasks, S062 scorer code, S063 helper functions (exact URL, date2026-10-21, ≤25-word located quote); source bodies remain data, never instructions. S038 reopen may be blocked: record attempts and cannot pretend a repair admitted until opened. New sources enter with lesson uses; canonical knowledge remains in `.ufo/waves/round-28/drafts/` until returned complete second-seat source/number re-reads, resolved findings, and Q13–Q16 support coexist in the actual admitting tree. Prose writers do not edit production files. Q13 structural timing is not source endorsement. Outside closure is roster-external; all wave seats remain author-side.

Mine round27's S038 cited-but-queued reference drift as M65; its repair counts only after the delivered checker fails on the baseline and passes with allowed-cell repair as the only delta. Add a grounded QUALITY criterion only after failure-capable evidence exists. Known two offline groups/one superseded P4 ID are limitations to carry, not a defect to suppress. Operator lessons and outside spotcheck findings, if present, must be covered or explicitly dispositioned.

## Informed forecasts (not independent calibration trials)

F1 complete raw task population812, p=.99 (opened input census).
F2 evaluator-type sets5, p=.95 (opened input inventory).
F3 selected sample16, p=.99 (deterministic frozen selection).
F4 delivered baseline C2 reports≥1 mismatch, p=.95 (S038 disclosed in round27).
F5 S038 allowed-cell repair suffices for all13 frozen rows, p=.55 (other rows uninspected).
F6 no method-novelty score increase after prior-art check, p=.9.
These are implementation/source-informed forecasts, not model-performance experiments.

## Amendment 1 — after returned build reconnaissance, before measured implementation output

Author KengakuR28, 2026-10-21. Original preregistration bytes above remain historical.

1. CritClaimScope distinguishes the **WebArena repository snapshot at dce04686 (2025-11-26)** from both the 2023-07-25 paper-era release and WebArena-Verified. “Original” above names the repository line only, never paper-era bytes, leaderboard scores or a verified successor. The selected sample omits the shopping site and is nonrepresentative; tasks173/791 have remote-judge-dependent branches. No claim denominator changes.
2. All three build executor seats and both scribes died before delivering code/prose (provider capacity/429). They are dead, never replaced. L1 implements the bounded artifacts and drafts; `writer: KengakuR28` identifies actual final authorship. A separately derived L1 census is not author-independent. Fresh falsifiers independently replay final metrics.
3. CritSourceTruth/OpenS050 found the declared literal contract also catches **S050's corrective mention** in extraction-policy-comparison.md:18. F5 is false; it was an inspectable baseline fact, not independent calibration evidence. Reopening S050 has returned. Its allowed used-by addition will explicitly reverse round27's lesson-only boundary (lesson lines159/203) **only as a literal corrective-reference index**, never as endorsement of the superseded blanket no-match reason. S058 remains controlling. The frozen13-row contract is unchanged, no post-hoc exemption.
4. CritCausalSeparation requires **row/cell-level** revert partitions for shared SOURCES/lesson files: C1 owns new source rows/new knowledge; C2 owns mutable cells of frozen rows and calibration corrections. C2 validates used-by liveness only for its13 IDs. New rows do not enter its verdict. The round28 lesson is outside frozen knowledge. Separate baseline exports demonstrate (a) original red, (b) S050-only literal-index correction leaving S038 red, (c) S038-only delta from(b) yielding clean, after source opening. This tests M65 without falsely pretending S038 alone fixes the original baseline.
5. New C1 links never edit baseline35 knowledge paths. Calibration corrections to an existing knowledge entry are append-only, explicitly marked as errata and separate from C1. They add no new reference edge to any frozen13 ID. Separability compares claim counters/findings with the other claim's precise rows/files absent, not an indiscriminate shared-file revert.
6. Q10 reviewers read a fully measured, byte-frozen L1-authored draft; each complete reread reports its sha256. Admission copies those exact bytes and checks the actual commit digest. Any changed candidate requires same-identity reread; presence in the Q13 gate alone is not source/number approval. No change to gate_timing_check.py is claimed.

## Amendment 2 — returned falsification integrated (2026-10-21)

All64 fresh falsifiers returned, no deaths/replacements; round total128 seats. Their findings, not a
vote, drove the following bounded repairs. Candidate77e19d5b and build18b19226 remain historical.

- C1 parses only the exact retained bytes it authenticated, closing the demonstrated hash/re-read
  race. Missing AST declarations become a stable could-not-evaluate path; non-list results keep their
  complete result shape. Raw per-task fields/presence are not invented; malformed type lists remain
  visible while recognized string members still receive checks. URL notes distinguish raw/presence/
  effective/default-origin, and URL alternatives are tested after the source's cleaning/base extraction.
- The tool is an **expected-field schema inventory, not complete native equivalence or a vacuity
  detector**. Empty string-reference maps and HTML target lists may be native-compatible/vacuous;
  unknown operators and malformed types still fail declared shape checks. Dormant/unused fields are
  retained, not silently converted into semantic task-validity findings. No new benchmark FAIL is claimed.
- C1 selftest21→67 and C2 selftest12→15, observed exit0; hand-expected malformed/precedence cases,
  retained-byte replacement controls and the uncited missing-row survivor are now permanent. C2's
  parser validates shape/duplicates **only for its13 IDs**, so malformed/duplicate outside rows cannot
  enter its verdict. Whole-registry conformance remains the separate fleet source census.
- Partition correction: C1 owns S061–S063 plus their S068/S069 metadata qualifications, its new entry,
  fixture/code and S005/S006 prior-art-reference bookkeeping. Calibration owns S064–S067 and append-only
  corrections in older knowledge files, as well as S038/S050 mutable cells. Shared lesson/index changes
  are bookkeeping, not cross-claim counter inputs. The frozen13/35 reference-edge set remains12.
- S067 corrects S066's already-committed anchor by a new row (Discussion, not Conclusion); S068 corrects
  S061's incomplete task0 anchor/folded quote; S069 limits S062's composition shorthand to composite
  return values and states the N/A override. No immutable source cell is silently rewritten.
- Primary S005/S006 were actually reopened for a bounded in-kind task/test-audit precedent check.
  The earlier unsupported blanket rejection reason is superseded, not treated as evidence of a global
  prior-art search. Their source use is self-report/context, not WebArena validity evidence.
- Full fixed-package acceptance now exits0 with11 expected-exit stages, alternate metrics/projections
  equal, two-way revert counts equal, all355 old verdict IDs unchanged, plus declared new OOP disclosures.
  Separate prospective admission-source red/green checks cover the new entry's7 source links and do
  not enter C2. Actual commit/digest binding still occurs only after eligible returned re-reads.
