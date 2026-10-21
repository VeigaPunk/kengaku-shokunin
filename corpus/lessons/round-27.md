# Round 27 — fixed-response parser-policy sensitivity and frozen P4 assertions

L1/writer KengakuR27; holds the canonical planner seat. Base b5719440; pre-registration landed
11a7fc8c64dc5d634331be24ccf5936f84a11f03 before build dispatch. Round 26 was outside-admitted by
CloseKengaku26; `.ufo/reports/round-26/kengaku-closure-evidence.json` at the fleet root contains four
outside admit/reject agreements, no new disagreement. Its first limitation motivates P4, not a claimed
repair of an outside-rejected round. Round25 remains rejected-honest-stop.

## Mistakes

| id | class | evidence and captured-by | fix and failure-capable evidence |
|---|---|---|---|
| M55 | survivor | `.ufo/waves/round-27/build/MutGateTiming.md`: replacing commit-tree reads with working-copy reads survives the old exit-vector (selftest0/r25red1/r26green0), although inventory leaks 0→87 reports. Q13/Q14 intended timing, but stock selftest did not separate absent-in-commit/present-on-disk support | add the sandbox identical-lesson early/late-commit pair as a permanent selftest; red mutant and restored green receipts retained before counting the fix |
| M56 | scope | build context called SOURCES “13 columns”; RowGsm8kYaml/RowLmEvalFilters/RowCommonMarkFence correctly found 11 content columns, NF13 includes empty edges | Amendment1 preserves the contract's actual shape; the maintained census rejects malformed rows; no registry schema change |
| M57 | scope | RevSeparabilityPlan found P4a's live round26 census would count C1 source/knowledge additions and v4 self-inclusion | freeze historical claims against their named committed receipts/base revision, not today's counts; explicit two-way revert check at close |
| M58 | survivor | MutStateCheckSupersede: narrow R25–R29 regex to R25–R26 survives old selftest; suppress all21 OUT_OF_POPULATION lines also survives exit-only checks | v4 needs R27 correction acceptance and disclosure output controls; cannot call old green exit complete coverage |

M55 is the frontier's principal mined mistake. S038's cited-but-queued drift was independently found by
RevengeMistakeMine; it is out of frozen P4e (S043–S048), not silently counted as a P4 discovery or repaired
without reopening its source. It stays an explicitly disclosed lead rather than a false whole-registry PASS.

## Gate

Candidate `corpus/knowledge/extraction-policy-comparison.md` is drafted outside corpus under
`.ufo/waves/round-27/drafts/`. Admission is deferred until returned complete/source/number rereads,
resolved findings, and Q13/Q14 support coexist in the actual admitting tree.

| candidate | decision | reason |
|---|---|---|
| knowledge/extraction-policy-comparison.md draft | deferred | pending returned falsify rereads and final correction checks; no knowledge/index/coverage-row admission yet |
| `corpus/knowledge/extraction-policy-comparison.md` | admit | Q1–Q16 scoped artifact: corrected complete source/number/contract reread returned in `.ufo/waves/round-27/falsify/FEntryNumbers.md`, and corrected RFC anchor reread in `.ufo/waves/round-27/falsify/FSourceS053.md`. All cited reports are returned, role-eligible and distinct from writer KengakuR27. Their final PASS supersedes preserved PARTIAL findings. The candidate is copied byte-exact from reviewed draft A42E; entry/index/coverage row and these reports coexist in the admitting tree. Structural checks grade that actual tree before close, never infer endorsement from presence. |
| novelty +1 for extraction-policy comparison | reject | xFinder and fixed-output rescoring are direct prior art in kind; flip: a distinct construct with papers and tooling search, not an exact nine-policy spelling match |
| E4 strict-whole as model accuracy on these fenced prompts | reject | it contradicts the historical one-fenced-block instruction; flip: task contract/constrained-output request requiring whole-output JSON and independently verified truth |
| pooled CP95 as independent future-response guarantee | reject | deterministic replay, repeated conversation units and known format mix do not define an iid future sample; flip: registered independently sampled units and sampling model |
| E7/E8 as production untrusted-input parsers | reject | sentinel measured ~285s on 200K unmatched brackets; flip: separately specified work bounds and adversarial resource tests, not finite-corpus success |
| json-repair as an added E9 policy this round (S060) | reject | frozen eight-policy denominator, stdlib constraint and repair-versus-span-selection semantics; flip: separately register a pinned repair policy with truth-sensitive controls and an independent oracle |

### Sources opened this round (access date 2026-10-21 for every row)

| row | URL | located quote (≤25 words) and location |
|---|---|---|
| S049 | https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/filters/extraction.py | `match = match[self.group_select]` — RegexFilter :47–49 |
| S050 | https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | “If the pattern contains no capture groups, the full match is compared against the target.” — docstring :62–64 |
| S051 | https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py | “If the sampled string is not valid JSON, it will never match” — eval_sample :82, file last change4b7a66bd |
| S052 | https://docs.python.org/3/library/json.html#json.JSONDecoder.raw_decode | “This can be used to decode a JSON document from a string that may have extraneous data at the end.” — raw_decode paragraph |
| S053 | https://www.rfc-editor.org/rfc/rfc8259 | `JSON-text = ws value ws` — §2 JSON Grammar |
| S054 | https://spec.commonmark.org/0.31.2/#fenced-code-blocks | “Closing code fences cannot have info strings” — §4.5 |
| S055 | https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47 | `match = re.search(ANSWER_PATTERN, response_text)` — math_eval.py:53 |
| S056 | plans/parser_policy_compare.py | `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` — --summary final line |
| S057 | https://arxiv.org/pdf/2405.11874v3 | “we replicated only the RegEx methods on each framework and ensured consistency in other settings.” — §5.3 Setup, PDFp9, reopened2026-10-21 |
| S058 | https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | `reason="no_response" if empty else "invalid_response_format"` — no-match branch:122; independently opened2026-10-21 by FSourceS050 and L1 |
| S059 | https://www.rfc-editor.org/rfc/rfc8259 | “Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted.” — §6 Numbers, txt377–378; opened2026-10-21 |
| S060 | https://pypi.org/project/json-repair/ | “A package to repair broken json strings” — PyPI summary,0.64.1, opened2026-10-21 by SrcJsonRepair |

Hashes and exact opening seats: `corpus/evidence/round27-sources/gate.md`. Eight new tierA rows initially
enter mined with used-by solely this lesson. S049/S050/S055 establish ordering precedents, not JSON-policy
ports; S051 whole-output class, S052 decoder primitive, S053/S054 grammar limits. S044 was reopened by
SrcXFinderReopen. No existing status/recheck/used-by cell is changed at this stage.

## Build wave and returned findings

82 seats, one validated dispatch, role mix scout22/executor14/reviewer12/scribe10/critic8/connector6/
revenger4/sentinel2/mutation-tester2/simplifier2. L1 holds planner; no model parameter was passed.
19 provider deaths, never replaced: six connectors quota-exhausted until 2026-10-25, thirteen other seats
ended on Haiku429 with ~3h retry-after. Exact names/errors `.ufo/waves/round-27/build-dead-seats.json`.
Some failed seats left partial reports; report presence is not successful completion or admission evidence.
Same-identity follow-ups to successful seats add no new seats. Fresh falsifiers will attack the integrated
artifacts, not act as replacement identities for failed build seats.

Key findings before admission:
- E1/E3/E7 share17 PASS→FAIL events in MULTI, pooled agreement1947/1964 masks14/31; E5 drops26 fallback
  successes; E4 is instruction-contradicting, not model-error evidence. E0/E2/E6/E8 verdict-equivalence is
  finite-population only. SrcXFinderReopen/SrcPriorArtTooling rule prior art in kind: score7 held.
- RevSpecE1E2/E5E6/E7E8 clarify matched-vs-parseable selection, raw nonoverlapping candidates, null,
  restricted labels and contained spans. Amendment1 discloses that it follows output.
- Oracle seat disclosed reading the baseline regex and contextual grader lines; it is separately written,
  never imported production extraction, but not fully source-blind. Claims never call it source-blind.
- SentPolicyNoLeak observed all17676 calls with poisoned expected-answer fields and found no leak.
  SentRegexCost bounds utility to pinned data, not a general untrusted parser.
- ScoutSiblingParsers scanned21 sibling repos and found no sibling measuring this LLM-response construct.
  Testing technique remains adjacent to tameshi, research method to chousa, format craft to kotoba,
  serving identity to kama, route policy to kumitate, citation-drift mechanics to souji.
- Scope pins from ScoutSourcesUsedBy: P4e covers knowledge/lessons teaching uses; literal source-inventory
  mentions and S043 supersession pointer are not new uses. No all-current-assertions claim follows P4.

## Tool installs

RowInspectPattern resolved inspect-ai0.3.282 via `uv run --with inspect-ai` (PyPI, scratch source inspection).
RowInspectMatch installed inspect-ai0.3.282 in /tmp/r27-rim/venv via uv/PyPI to exercise match_str.
SrcJsonRepair installed json-repair0.64.1 in a scratch venv via uv/PyPI to inspect its last-value/repair
behavior (not added as an unfrozen E9 policy). No pacman/system upgrade or host-service change.

## Build follow-up dispositions before falsification

- M55 fix now exists: `plans/gate_timing_check.py --selftest` permanently exercises early0/late1 report
  inventory under identical lesson bytes. `plans/fixtures/r27/gate-timing-worktree-mutant.txt` is red1;
  restored receipt is green0. QUALITY Q15 records the invariant. The actual admission still needs Q13.
- Updated policy audit rejects pin/population errors before any E-policy call. Its poisoned-policy
  pin-rejection selftest observed calls0, exit1 in summary and JSON modes. `plans/policy_cases.py` contains
  58 hand-expected policy cases, run by `parser_policy_compare.py --selftest`; nine seeded policy mutants
  are killed. This table lives beside the instrument (not the initially proposed fixtures path).
- RevR26ClosureMapping's remaining limitations are explicit: the three P2 offline-unverifiable surfaces
  remain unverifiable; P4 is a frozen extension, not restoration of missing endpoints. New formats and
  future generalization remain frontier. D1 stays policy conformance, never robustness PASS.
- Existing round26 P3-oracle extension-only historical-range observations are outside P4. The claim that
  README had their errata was not located by that reviewer; this round does not assert it as established.
  Existing README source-support correction to S043–S048 is locatable; it is not proof of every oracle
  extension finding. No historical outside verdict is rewritten on this basis.
- P4 excludes LOG's round26 prose and surrounding PROVINCE/README admission-bar history. Old Q1–Q8/Q13
  descriptions are superseded by explicit current Q1–Q15 here, not silently counted as frozen P4 successes.
  Current checker FAIL=0 does not prove all current assertions or registry uses are complete (S038 lead).
- CP calculation is independently checked by RevCPReuse (1964-scale Decimal reference) and will receive
  a fresh falsify bound check. Reused interval code is not a second independent authority.
- Outside verification is the orchestrator's roster-external closure, not any of these dispatched seats.
  SHONEN stays four evidence-backed `[~]` boxes. No promotion is claimed.
- Existing L0 coverage cap (:72) and novelty-conversion (:73) remain unruled; numbers stay7/8.
  Connector deaths are provider failures, not replaced; the next wave keeps one connector seat.

Source-inventory addendum before admission: S057 is the ninth added tierA row (S049–S057), not an extra
publication. It extends S044's abstract-only scope to the reopened §5.1/§5.3 comparison and records the
uncertain item-pairing/denominator limits. The earlier “eight” inventory is superseded by nine; rows57,
tierA52/B3/C2, mined45/queued9/rejected3 before any later source-use changes.

## Frozen P4 integration before falsification

Final v4 registers49 IDs (48 grouped checks plus one assertion-inventory control),0 in v3.
P4a9/P4b8/P4c11/P4d14/P4e6; exact list `plans/fixtures/r27/p4_assertion_ids.txt`.
Delivered checker on b5719440 export and live candidate both exits0 with327 assertions,
318 MATCH/0 MISMATCH/6 SUPERSEDED/3 offline-unverifiable; P4 contributes48 MATCH/1 SUPERSEDED.
The old README source-range erratum is recognized, not falsely rediscovered as a current mismatch.
An early v4 draft ignored it and was corrected before landing. C2's base mismatch≥1 forecast is false
under the delivered instrument; no “one new defect fixed” credit is taken.

P4a historical C2/census claims read committed receipts, not recursive current-checker outputs. P4e
freezes the two base teaching-use files; new round27 mentions do not grow its expected citing-file set.
P4c history-repository selection requires the exact b5719440 commit witness, preventing a fleet repo
from pretending to be lane history. Missing lane Git authority is unverifiable, not zero tree counts.
P2/P3 full keyed298-record projection is unchanged on base. Selftest includes exact existing-erratum
remove/wrong/partial controls, R27 acceptance, P4 R29 rejection, inherited P2/P3 R27/R29 acceptance and
population-disclosure retention. Build report retains original and corrected findings.

The inventory seat's317 literal-token candidates are an **exploratory raw inventory**, not the delivered
P4 register: they include source identifiers, serialized/report mentions and score tokens. No claim that
all317 became independent assertions is made. The registered grouped comparisons and residual limits
must be judged against the frozen pre-registration; the falsify inventory seat checks omitted promises.

## Falsification corrections before admission

- **M59 · vacuous:** E6 last→first fence mutant survived the shipped selftest58 cases (FMutPolicyE6),
  while an independent two-fence witness failed. Add the witness as a permanent hand-expected case and
  retain red-before/restored-green receipts; policy semantics and corpus counts do not change.
- **M60 · reference-drift:** FSourceS050 found that the candidate's blanket no-hit reason omitted empty/
  whitespace `no_response`; S058 supersedes that part of S050. The corrected draft qualifies the reason.
- **M61 · reference-drift:** FSourceS053 found candidate NaN/Infinity claim accurate but anchored only to
  RFC§2; new S059 explicitly anchors§6. S049's default-selector anchor is25, not27; operative47–49 was
  correct. Draft provenance uses25; this correction does not rewrite the earlier source row.
- S058/S059 were opened before addition; total new source rows now11 (S049–S059), all tierA. Historical
  eight/nine-row snapshots remain as written; final census is authoritative. No existing status/recheck/
  used-by changes yet. S050 stays lesson-only as a superseded reason, not silently passed as accurate.
- P4 falsification found genuine detector gaps: role-mix/comparison deletions, family-denominator
  comparison deletion, rejected full-valued family supersession, hard-coded recovery+3, same-document
  score consistency presented as outside truth, missing four-repair split and summary-disclosure mutant.
  Repairs and explicit unverifiable findings must precede any clean C2 claim;49-ID build PASS is not
  a final coverage judgment (`FMutP4a/b/c/d`, `FP4Inventory`, `FP4d`, `FDisclosure`).
- Q1–Q8 outcomes independently score1,1,1,0,1,1,0,1; Brier0.1471875 (FForecasts). These were informed
  code/corpus forecasts, no calibration credit; the separate P4 mismatch forecast is false as disclosed.

### Final mutation-driven repair interpretation

M62 · survivor/scope: FGateQ15's early-break traversal mutant passed a one-report fixture; caller
GIT_INDEX_FILE also escaped temporary-repo writes. Q16 extends the fixture to two cited reports and
isolates Git environments; both worktree and traversal mutants are red, restored inventory0→2 green.
Earlier0→1 receipts stay byte-identical; new receipts have `gate-timing-v2-*`/`parse-tree-mutant` names.

M63 · vacuous: FMutP4a/c/d and FDisclosure exposed positive-fixture-only guards; FP4Inventory/FP4d
found same-document score tokens reported as truth, omitted numeric-repair split, unsupported recovery+3,
manifest-only count authority and silent adjacent-numeric omission. Final v4 has51 IDs (not49):
P4a10/P4b8/P4c11/P4d15/P4e6 plus inventory1. P4 contributes48 MATCH,1 SUPERSEDED,2 explicit
OFFLINE_UNVERIFIABLE groups (eight score tokens and adjacent audit numerics). Base and current author
summaries both329 assertions/318 MATCH/0 MISMATCH/6 SUPERSEDED/5 offline-unverifiable, exit0.
These two added disclosures complete the promised frozen-target interpretation after output; they are
not new discoveries or newly sampled assertions. Old P2/P3 keyed298 records remain unchanged.
Final checker compares actual JSONL breakdowns as well as manifest/command evidence, derives four numeric
repairs plus one index repair from the base receipt, and reads the committed recovery receipt rather than
assuming+3. A complete wrong-claim/correct-value R27 family correction can supersede; partial/wrong values
cannot. Specific selftest guards now catch comparison removal, denominator removal and summary suppression.

Final source inventory before admission: S049–S060 are12 added rows,11 tierA and1 tierB. S060 retains the
opened json-repair policy rejection with reason/flip, rather than losing it as an unrecorded lead. It is
lesson-only and is not a newly inserted E9 or a load-bearing claim in the admitted candidate.

### Admission support and source-use changes

Complete reader FEntryNumbers reopened all load-bearing sources, independently replayed every numeric
table, checked prompt contracts/rejection reasons, then reread the whole corrected A42E draft and closed
both low findings. Its original numeric PASS, later PARTIAL and final scoped source/numeric PASS remain.
FSourceS053 reread S059 and closed the RFC-anchor gap. FSourceS050's same-identity follow-up failed on
Zai429; it is not claimed returned corrected support. FEntryNumbers actually reopened S058 independently.
FEntryAll died and is never cited as admission support or replaced by a new identity.

Used-by changes (each old→new; status/recheck unchanged): S049,S051,S052,S053,S054,S055,S056,S057,S058,S059:
`corpus/lessons/round-27.md` → `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`.
S050 remains lesson-only as a superseded reason; S060 remains lesson-only as a rejected policy candidate.
No S001–S048 registry cells or historical knowledge entries were changed.

Final gate code also binds production reads to the requested --repo under hostile GIT_DIR/object selectors;
FGateQ15 independently closed this residual on sourceSHA25651c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a.
Fresh-bare victim/index/object sentinels remain untouched. All three gate mutants are red; restored green.
P4Inventory and FMutP4d independently closed their original defects on checkerSHA2565db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c;
FDisclosure independently killed the exact stdout-suppression mutant. Census alone does not detect that
mutant: selftest is the regression guard. No broader coverage is inferred from a zero exit.

Two waves82+64=146 unique starts; build19/falsify21 original provider deaths, never replaced.
Falsify43 initial successful returns plus3 failed-seat partial reports are retained. One successful source
seat's later follow-up failed separately (S050). Same-identity continuations add no fresh seats.
All falsify critics/executors/sentinel/connector died; L1's residual checks and returned reviewers/mutators
provide the exercised coverage, not an invented returned role mix. Outside closure remains the orchestrator.
