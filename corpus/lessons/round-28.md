# Round 28 — pinned WebArena task-spec inventory and literal source-reference coverage

Writer/coordinator: KengakuR28; canonical planner seat held by L1. Baseline master
b9b24796277020d1b9b01923b45313d6a565e664, preregistration f0ba09be0f3066daba2134b943d973ad1588f34a.
Round27 was admitted by roster-external closure (operator dispatch, MANIFEST rounds[411]); it did not
establish all-current-tree consistency. Its P4 two offline groups and one superseded ID remain limits.
Claims: C1 lowest legacy novelty7→canonical coverage/constructs, local task-spec observability;
C2 calibration8, bounded13-row/35-path literal reference coverage. Scores held, no method novelty.

## Mistakes

| id | class | evidence pointer · captured-by | fix and failure-capable evidence |
|---|---|---|---|
| M65 | reference-drift | round27 lesson:18–20 disclosed S038 cited-but-queued; attribution-interval-calibration.md:144–145 cites it; source registry S038 queued with no used-by. SOURCES contract status/used-by and R12 should catch it, but P4 was explicitly narrower | Dedicated frozen literal-reference diagnostic, source reopened before mutable-cell repair. Baseline and only-delta receipts are appended after execution; no repair credit before observed red/green. |
| M66 | reference-drift | build/OpenS049.md reopens identical d6de8164 bytes: group_select default at27, not25. Round27 M61 and source header repeated an erroneous reviewer correction; captured-by Q10, which itself failed | Append a named source-location erratum to existing knowledge, retain original header and round27 records. No numeric policy result changes. |
| M67 | scope | build/CritSourceTruth.md and OpenS050.md: declared literal contract counts “S058, correcting S050”; round27 deliberately kept S050 lesson-only. Captured-by no prior literal-versus-support distinction | Preserve contract, record F5 miss, index this corrective mention explicitly without treating S050 as supporting truth; S058 remains controlling. The old lesson-only boundary is explicitly superseded only for literal discoverability. |
| M68 | reference-drift | build/OpenS054.md: CommonMark closing fence requires same type and at-least opening length, not equal length implied by S054's type/length shorthand; captured-by Q10 | New opened-source row S064 supersedes that shorthand; old row unchanged. Existing knowledge's broader “fence-length rules” statement remains true. |
| M69 | provider | build executor3 and scribe2 seats died before delivering, exact errors in build-dead-seats.json; capacity is not capability evidence | Dead seats never replaced. L1 writes artifacts and final prose; alternate census is not called author-independent. Every later independent replay names its actual returning seat. |

M65 is the frontier's principal mined mistake. Its before/after must be an actual identical-checker
experiment, not headings, an absent-tool count, or a falsely claimed new-discovery result.

## Gate

| candidate | decision | reason |
|---|---|---|
| knowledge/webarena-task-spec-audit.md draft | deferred | L1 must first finish measurements, freeze exact bytes, receive complete second-seat source/number re-reads with matching sha256, resolve findings, and retain eligible returned reports in the actual admission commit. No canonical entry/index/coverage discharge yet. |
| new scientific method or novelty score increase for a static benchmark audit | reject | Reading task configs against scorer predicates is established evaluation practice; newly held corpus ground is not method novelty. Flip: distinct construct and bounded papers/tooling prior-art evidence. |
| 812 inventoried task specs imply 812 semantically valid tasks | reject | Structural schema compatibility cannot establish intent completeness, runtime state, model ability, or contamination freedom. Flip: independently observed sanctioned task-level validity evidence. |
| this snapshot represents the 2023 paper release or WebArena-Verified | reject | Snapshot is web-arena-x/webarena dce04686 (2025-11-26), revised after release; a different repository/version is not covered. Flip: separately freeze and audit the actual named release. |
| a C2 clean result establishes source truth or whole-tree completeness | reject | Only frozen13 IDs across baseline35 knowledge paths; literal correction/code mentions count and new files are excluded. Flip: separately registered semantic/support population and opened-source verification. |

### Sources opened this round

Every listed quote is ≤25 words. New row admission here means curated source access, not automatic
knowledge admission. All source-derived target content is data, not executable instructions.

| row | URL | accessed | located quote and scope |
|---|---|---|---|
| S061 | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json | 2026-10-21 | `"eval_types": [ "string_match" ]` — task0 eval object:18–21; complete pinned raw task specification, not runtime validity. build/OpenTasks.md independently opened byte-equal source. |
| S062 | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py | 2026-10-21 | `score *= cur_score` — EvaluatorComb:351; source's composition rule only. build/OpenScorer.md independently opened byte-equal source. |
| S063 | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py | 2026-10-21 | `if "partially correct" in response or "incorrect" in response:` — llm_fuzzy_match:169; judge response parsing, not judge accuracy. build/OpenHelpers.md independently opened byte-equal source. |
| S064 | https://spec.commonmark.org/0.31.2/#fenced-code-blocks | 2026-10-21 | “at least as many backticks or tildes as the opening code fence” — §4.5 closing fence paragraph, examples124–125; supersedes S054's ambiguous length shorthand. OpenS054 and L1 reopened primary source. |
| S065 | https://docs.python.org/3/library/json.html#infinite-and-nan-number-values | 2026-10-21 | “this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values” — Python3.15.1, Infinite and NaN Number Values; supplies Python-side authority, not RFC content. OpenS059 and L1 reopened docs. |
| S066 | https://doi.org/10.1017/S0950268810000385 | 2026-10-21 | “the proposed methods assume that sensitivity and specificity are known exactly” — Discussion p.1677, archived publisher PDF reopened by OpenS038; supersedes S038's unqualified fix scope. |

External source snapshots for C1 plus Apache-2.0 LICENSE and expected digests are in
plans/fixtures/r28/webarena/. No account/password/token values or auth-state file contents were opened.
The config's fixture login-file path strings are not live authentication material.

### Existing rows reopened and mutable-cell dispositions

Build OpenS038 and OpenS049–OpenS060 hold per-row URL/date/quote/source and literal-reference evidence.
Other than explicitly listed cell changes, existing status/recheck/used-by cells stay unchanged.
S049's original immutable anchor27 was right; the mistaken later header25 is corrected append-only.
S050's blanket no-match reason remains superseded by S058. Adding a corrective-mention path to S050
will reverse round27 lesson159/203's lesson-only indexing decision, **not** its rejection of that reason.
S053's Unicode-strip comparison and S059's Python extension clause are lane comparisons, not words from
the RFC; S065 supplies explicit Python-side authority. S051's same-policy-class claim is not a faithful
exception-handling port: upstream catches ValueError, lane catches broader exceptions (OpenS051).

Actual mutable-cell changes after returned openings (OpenS038/OpenS050):

| row | cell | old → new |
|---|---|---|
| S038 | status | queued → mined |
| S038 | used-by | — → corpus/knowledge/attribution-interval-calibration.md |
| S050 | used-by | corpus/lessons/round-27.md → corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |

Existing recheck/opened cells are unchanged. S050's used-by addition is a corrective-reference index,
explicitly reversing only round27 lesson159/203's lesson-only indexing; it is **not** a truth endorsement.
S058 still supersedes S050's blanket reason. New rows S061–S066 initially enter mined with the paths
listed in their actual cells; any later used-by change is separately recorded.
S038's live DOI/publisher fetches returned429; OpenS038 opened an authenticated Wayback capture of the
publisher PDF (2026-10-04, sha256 fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c).
Live publisher HTML through WebFetch was corroborating and possibly cached, not called a live PDF fetch.
Its ≤25-word coverage quote: “actual coverage at a nominal level of 95 % can be as low as 60 %” —
Introduction p.1675/PDFp2. Full access-attempt evidence is build/OpenS038.md; S066 records known-vs-estimated scope.

### Adjacent routing (evidence sent, not absorbed)

build/ConnectScope.md: benchmark evaluation remains kengaku; chousa owns general research/claim-source
method, tameshi general testing patterns, kotoba prompt-writing implications, kake actual web properties,
kaidoku shipped-artifact reconstruction. Registry gates already exist in kagi/kumitate: C2 is lane-local
calibration, not fleet-first methodology. No sibling files or benchmark environments are changed.

## Wave evidence and provider boundaries

Build64 validated seats: executor3/scout32/reviewer8/critic6/revenger6/mutation-tester3/scribe2/connector2/
simplifier2. L1 planner is the canonical frozen seat. First batch call was job-cap refused with no agents;
same payload accepted on second attempt after180s. Registry records accepted identities with -2 suffix.
TaskCall context/tasks were dispatched unchanged; routing is role-bound, no model parameters.
Dead seats remain dead; final totals/errors appended from actual terminations. No replacements.

## Outside spot-check

Pending roster-external closure. All64 build seats and every later lane-dispatched falsifier are author-side.
SHONEN remains evidence-backed [~], not promotion or outside discernment agreement.

## Tool installs

None by L1. Final seat install disclosures are recorded at close; no pacman or host-service changes authorized.

## Build measurements and resolved reconnaissance

C1 summary exit0:812 tasks/812 distinct IDs,5 evaluator-type sets,27 strata,16 selected cases,651 targets;
selftest21 cases exit0. C2 summary exit0:13 rows/35 paths,**12 row-file reference links across2 files**,
0 mismatched rows; selftest12 cases exit0. Baseline identical checker exits1 with2 mismatched rows and
3 findings (S038 status/used-by, S050 missing-used-by); afterS050-only repair still exits1 onS038;
S038-only status/used-by delta then exits0. Same-command receipts and exact input digests:
`corpus/evidence/round28-calibration/build-acceptance/registry-only-delta.json` and adjacent stdout files.
This is the shown-able-to-fail M65 repair. S050 is separately disclosed, not secretly folded into S038.

- M70 · reference-drift: RevHTMLRequired's initial OR-comprehension quirk was false. L1 challenged its
  source reading; same-identity re-read retracts the claim (report rev2 §7). Plain OR is controlling;
  all its hand cases were already computed under plain OR. Its “401 not-routed fields” are actually
  empty lists, not unconsumed nonempty predicates. No false quirk enters the candidate.
- M71 · scope: initial acceptance's final equal-entire-ID-set assertion wrongly rejected new
  OUT_OF_POPULATION disclosure records. All355 existing records and all329 checked verdicts retain
  their previous verdicts;2 new round28 artifact disclosures are not new checked assertions.
  Red `build-acceptance-run.txt`, exact `build-preservation-delta.json`, and corrected-on-the-same-
  captured-output `build-preservation-corrected.json` are retained. Main did not rerun the checker to
  confirm the failure. The permanent harness now permits only newly named OUT_OF_POPULATION records.
- M72 · number-drift: CritSourceTruth's “13 row-file pairs” denominator conflated13 frozen IDs with12
  cited IDs; S060 is uncited. Actual baseline/final counters and alternate derivation give12 links.
  The13 rows and35 paths remain correct;33 paths are zero-reference controls.

RevHTMLLocator's malformed-helper URL/target-denominator findings and RevRouterMix's explicit contract/
ordering findings were integrated before counting: raw target count no longer relies on valid locators,
all locator classes have hand cases, malformed func-without-colon URLs and empty URL alternatives fail,
AST-derived dispatch/product/N/A-override facts and ordered evaluator histograms are emitted. N/A reason
schema and explicit reference-approach order were added from RevStringFuzzy/RevStringExact. These are
instrument-compatibility details, not new task-validity discoveries or a scorer execution port.

The initial11 acceptance command stages all had their expected exits. Its final preservation assertion
failed for M71, not a schema or historical checked-verdict mismatch. The later corrected harness run
will be reported separately; no “whole acceptance PASS” is inferred from those11 exits.

Build terminal outcomes:59 completed,5 dead (3executor capacity,2scribe429),0 replacements. All source/
case/contract reports returned; same-identity correction of RevHTMLRequired added no new seat.
Unused isolated clone scaffolds were removed only after all3 assigned writer seats died.

Source-browser scaffold cleanup: OpenS038's timeout-bounded headless Chromium created a disposable
profile under scratch/OpenS038/chr (runtime Cookies/Login Data/History databases, not analytical
evidence). L1 removed only that profile before packaging; PDF/text/HTML/access-attempt receipts remain.
The same source seat confirmed its owned invocation had exited0 and no matching process remained.
No live auth values were read, no profile or credential-store files are committed, no host service changed.

Candidate freeze before fresh falsification: writerKengakuR28, SHA256
`77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`;
`.ufo/waves/round-28/candidate-freeze.json` pins both candidate and measured instrument digests.

## Falsification outcomes and repairs (2026-10-21)

Fresh wave64 completed64, dead0, replacements0; round seats128. Roles:
scout22/revenger14/reviewer12/critic11/mutation-tester4/connector1. Reports are author-side advice,
not64 whole-round approvals. Frozen draft77e19d5b and its21-case/12-case instruments are historical.

| id | class | evidence · captured-by | disposition / demonstrated repair |
|---|---|---|---|
| M70 | reference-drift | build/RevHTMLRequired rev1 OR-scope claim; Q10 source reread | Same-identity rev2 retracts it; plain OR remains controlling. No numeric candidate change. |
| M71 | scope | build acceptance equal-entire-ID-set assertion; frozen-population boundary | Existing355 IDs retained; only new OOP records may grow. Corrected permanent harness exits0, old red retained. |
| M72 | number-drift | CritSourceTruth's13 row-file pairs; Q17 denominator discipline | Actual12 links/13 rows/35 paths;33 paths are zero-reference controls. No population reinterpretation. |
| M73 | scope | disposable OpenS038 Chromium profile; CORPUS no credential material | Runtime profile removed before build packaging; owned process confirmed exited, analytical PDF/text/HTML retained. |
| M74 | attribution | falsify/FContractPopulationPin hash/re-read counterexample; PROTOCOL evidence identity | C1 retains authenticated bytes and parses only them. Permanent post-read-replacement controls cover raw JSON and scorer bytes; fixed selftest67 exits0. |
| M75 | attribution | falsify/FContractURLSchema and FContractStringSchema invented defaults/projections; Q3 | Raw/presence/effective URL-note fields separated,196 explicit/9 defaulted; missing/raw type fields retained. Cleaned empty URL bases fail, metadata does not masquerade as authored data. |
| M76 | survivor | FContractHTMLSchema/StringSchema/TaskSchema mutants and FMutMissing uncited-row survivor; gate selftest standard | Hand-expected malformed/precedence cases added; C1 selftest67 and C2 selftest15 pass. Uncited missing frozen row is now a permanent control. Original survivor receipts remain. |
| M77 | reference-drift | FSourceS066/FBoundaryNoAxisHarm: caveat in Discussion, not listed Conclusion; Q10 | NewS067 supersedes S066 anchor after its build commit; old cells preserved. Scientific scope unchanged. |
| M78 | reference-drift | FSourceS061 folded quote/incomplete object anchor; Q10 | NewS068 and corrected Gate opening record below use exact single-line quote and full task0 locations. Old source row is not silently rewritten. |
| M79 | attribution | FContractAstAuthority fixed annotations called AST-derived; Q3 | Candidate distinguishes AST-derived dispatch/statement locations from hand-read operation/error-phase annotations, hash-bound but not AST-proven semantics. S069 qualifies composition scope. |
| M80 | scope | FBoundaryLiteralScope/FConnector outside-row coupling; frozen13 contract | Parser shape/duplicate findings now apply only to13 IDs; permanent outside-malformed/duplicate controls pass. Fleet census still checks whole registry. |
| M81 | reference-drift | FTask reports' citation ranges, false universals and runtime assumptions; Q10 | Original live build authors appended dated errata, preserving original report bytes; corrected-case evidence remains beside the falsification. Runtime validity stays unobserved. |
| M82 | number-drift | FRegistryS052 counted all32 S-ID tokens as S052; FTask377 assumed unlabeled column order; Q10/Q17 units | S052 count corrected to2 with1 file-link; FTask377 retracts arithmetic accusation: columns are product/base/query, while probe provenance/fidelity remains limited. |
| M83 | scope | FFrontierGate unsupported “established practice” rejection reason; Q9 | S005/S006 actually reopened for narrow task/test-audit precedents; property-matching reason below supersedes the blanket phrase. No exhaustive novelty search or score credit. |
| M84 | number-drift | L1 prior-art quote counts manually overstated; CORPUS count command | prior-art-reopen.txt retains the correction: actual len(quote.split()) is21/22, both≤25; source text unchanged. |

`corpus/evidence/round28-calibration/final-acceptance-run.txt` now records exit0:
all11 command stages have expected exits; alternate C1 metrics/C2 projections and two-way revert
counters agree; all355 existing verdict IDs persist;329 checked318/0/6/5, old26 OOP plus2 new.
`final-acceptance/admission-source-links.json` separately proves7 missing canonical used-by links red1
and allowed-cell link additions green0. It is **not** part of C2 and does not claim actual admission yet.

Build recommendations disposition: adopt field-shape controls, explicit precedence, raw/effective
provenance and retained-byte identity. A full vacuity/dead-field semantic classifier was not claimed:
empty native-compatible containers can be schema-compatible, unused fields remain metadata, and
`prep_actions` is checked only on the branch that consumes it. No hidden new benchmark FAILs.
Task247 is an explicit out-of-sample unread-reference_url observation, not a17th selected case or
task-validity verdict. The sample omissions (shopping, helpers, prep and content-OR paths) remain open.

Partition correction to Amendment1: C1 owns S061–S063/S068/S069 and S005/S006 prior-art bookkeeping;
calibration owns S064–S067 and older-entry append-only corrections plus S038/S050 cells. New source
rows never enter the frozen13 C2 verdict. The whole-registry census is separate and still mandatory.

Case-report fixes are append-only in build/Task044,Task097,Task132,Task173,Task356,Task377,Task389,
Task399,Task424,Task552,Task556,Task681,Task759,Task791.md. No report becomes a runtime validity PASS.
Small non-load-bearing broad source spans in other reports are explicitly bounded by their fresh
falsifiers, not silently treated as exact quote boundaries.

## Gate — post-falsification source corrections

These records supersede the earlier abbreviated opening records where named, without rewriting filed
source rows. All new rows were opened before addition; S067–S069 are metadata/scope corrections to
already opened primaries, not new publications. Final new rowsS061–S069 are9 tierA rows.

| row / corrective opening record | URL | accessed | exact located quote (≤25 words) |
|---|---|---|---|
| S067, corrects S066 location | https://doi.org/10.1017/S0950268810000385 | 2026-10-21 | “the proposed methods assume that sensitivity and specificity are known exactly” — Discussion p.1677, archived text243–245;11 words. No live publisher-success claim. |
| S068, corrects S061 quote/anchor | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json | 2026-10-21 | `\"eval_types\": [` — single source line19;2 words. Intent16, complete eval18–29, references22–24, program_html26. Original folded excerpt is not the final literal quote. |
| S069, qualifies S062 composition | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py | 2026-10-21 | `score = 1.0 * self.ua_match(` — source159;5 words. Composite return values multiply at351; not every within-string branch multiplies. |
| S065 full-context supplement | https://docs.python.org/3/library/json.html#infinite-and-nan-number-values | 2026-10-21 | “Despite that, by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values” — Infinite and NaN Number Values paragraph;22 words. |
| S005 reopen, bounded prior art | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | 2026-10-21 | “Many task statements were underspecified, which could lead to multiple valid interpretations - while the tests only covered a specific one.” — Background bullet;21 words, self-report. |
| S006 reopen, bounded prior art | https://openai.com/index/separating-signal-from-noise-coding-evaluations/ | 2026-10-21 | “An initial automated filter reviews the instructions given to the model, attempts by the model to solve the task, and the tests” — Methodology paragraph after workflow image;22 words, self-report. |

Counts/locations: source-correction-quotes.json and prior-art-reopen.txt in round28-calibration.
S066's source scope remains right but its anchor is superseded byS067; the Gate and older-entry
clarification correctly named Discussion from the start. S061's full-object range18–21 was not right;
S068 supplies18–29. S062's true composite product does not imply uniform within-string multiplication.

Mutable-cell changes after these reopens:

| row | cell | old → new |
|---|---|---|
| S005 | used-by | corpus/knowledge/agent-time-horizon-and-task-validity.md → same, corpus/lessons/round-28.md |
| S006 | used-by | corpus/knowledge/agent-time-horizon-and-task-validity.md → same, corpus/lessons/round-28.md |

All existing opened/recheck/status cells remain unchanged at this step. S067 initially lists lesson
and attribution-interval-calibration.md; S068/S069 initially list this lesson. Canonical-entry link
changes are recorded only when the actual entry is admitted.

Rejection-reason correction (supersedes the earlier “established evaluation practice” cell): new-method
or novelty-score credit is rejected because this round demonstrates local instrumentation of already
published S061–S063 artifacts, while reopened S005/S006 document in-kind task/test alignment audits.
This is not an exact implementation-prior-art or exhaustive literature absence claim. Flip: a distinct
registered construct plus property-matching papers/tooling evidence. F6 receives no independent
calibration credit. WebArena was selected as accessible, pinned, inert task/scorer ground; it does not
replace the frontier's still-unopened Terminal-Bench/Toolathlon/SWE-bench Pro specs or contamination work.

Gate transcription erratum (same source opening, 2026-10-21): the literal backslashes in the
S068 code span in the preceding table are presentation characters, not source characters. Its
final exact located quote is **`"eval_types": [`**, source line19 (2 whitespace-delimited words),
at https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json.
This line supersedes only that escaped display; the S068 registry anchor and JSON evidence were right.

### Final scope boundaries

The current implementation passes the independent41 string-schema and43 task-shape probes, but the
67-case stock selftest is not exhaustive mutation coverage. Additional test-only survivors include
some missing/null-flag, reference-order and per-element-type regressions; the production checks and
current pinned output are correct. These bounds are not presented as a complete general-input parser
certificate or future regression-proof suite. Every concrete source/type repair claimed above has
its named evidence; no claim that all possible validator mutants were killed is made.

Earlier “no account values” wording means **no authentication-secret values or auth-state contents**,
not absence of public usernames in the authored tasks. The final candidate states that distinction.
The instruction to keep verified variants/successors separate is not a proven lineage claim about
WebArena-Verified. Historical freeze-v1 and freeze-v2 remain evidence; final wording-only freeze-v3
binds the final candidate and unchanged measured instruments. Outside non-author closure is still separate.

### Final admission decision — v4 exact bytes

| candidate | decision | reason |
|---|---|---|
| `knowledge/webarena-task-spec-audit.md` | admit | Complete corrected-entry judgments returned in `.ufo/waves/round-28/falsify/FContractEntry.md` and `.ufo/waves/round-28/falsify/FFullEntry.md`, both final VERDICT: PASS for SHA256 `50589759b82b26a7199d157035c852260ab1b10b59815f7b57e7534eccfd2ead`. Writer KengakuR28 differs from both registered reviewer identities. Canonical copy is byte-identical to the reviewed draft and candidate-freeze-v4.json; earlier PARTIAL sections name earlier digests and remain historical. Entry/index/coverage/source-use links and returned reports coexist in the admitting package. Q13 actual-commit result and report-byte pins are recorded after landing; structural presence is not endorsement. |

Source-use cell changes at admission (all statuses/rechecks unchanged):

| rows | used-by old → new |
|---|---|
| S005, S006 | corpus/knowledge/agent-time-horizon-and-task-validity.md, corpus/lessons/round-28.md → corpus/knowledge/agent-time-horizon-and-task-validity.md, corpus/lessons/round-28.md, corpus/knowledge/webarena-task-spec-audit.md |
| S061, S062, S063, S068, S069 | corpus/lessons/round-28.md → corpus/lessons/round-28.md, corpus/knowledge/webarena-task-spec-audit.md |

S061/S062 appearances include their corrective S068/S069 qualifications, not endorsement of superseded
metadata shorthand. S005/S006 are bounded self-report precedent context. The new admission links are
checked separately from C2's frozen13/35 population. Outside non-author verdict remains pending.

### Actual-commit conformance correction

First admitting commit df33fc83764975fd808b0945097b5d0c7aca3901 had two observed red checks,
retained in actual-gate.txt and actual-census.txt. These are not represented as passes.

- M85 · attribution · Q13: FFullEntry's real v4 PASS was heading-form, without an anchored plain
  VERDICT line; one valid report was already present, but the invalid additional citation made Gate
  exit1. Its same-identity formatting-only append now supplies plain `VERDICT: PASS`, v4 digest and
  canonical path. Original returned bytes remain intact.
- M86 · scope · frozen-population contract: check_p4a read the round26 revision section through EOF,
  so legitimate round28 “Scores stay7/8” text made the historical score-token disclosure ambiguous
  and converted one offline group to MISMATCH. The root cause is fixed by bounding the slice at the
  next H2, not by changing round28 wording or suppressing the finding. A permanent later-round-score
  fixture is red1 before that single production-line fix and green0 after; current JSON restores
  329/318/0/6/5 and P4's48 MATCH/1 SUPERSEDED/2 offline groups.

This narrowly supersedes earlier state_check.py byte-unchanged statements: its reviewed old/new digests
and red/green receipts are in plans/fixtures/r28/state-check-scope-fix.json. C1/C2 new instruments,
candidate50589759…, source data and their67/15 selftests remain unchanged. The acceptance fixture
pins this intentional scope-fix digest rather than silently dropping the old-code preservation guard.
Final measured revision and both actual-commit checks are recorded after this corrective commit.
