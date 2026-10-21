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
