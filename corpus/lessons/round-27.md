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
| novelty +1 for extraction-policy comparison | reject | xFinder and fixed-output rescoring are direct prior art in kind; flip: a distinct construct with papers and tooling search, not an exact nine-policy spelling match |
| E4 strict-whole as model accuracy on these fenced prompts | reject | it contradicts the historical one-fenced-block instruction; flip: task contract/constrained-output request requiring whole-output JSON and independently verified truth |
| pooled CP95 as independent future-response guarantee | reject | deterministic replay, repeated conversation units and known format mix do not define an iid future sample; flip: registered independently sampled units and sampling model |
| E7/E8 as production untrusted-input parsers | reject | sentinel measured ~285s on 200K unmatched brackets; flip: separately specified work bounds and adversarial resource tests, not finite-corpus success |

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
