# Round 53 — frozen triage and executed tip-state calibration

Round resumed after the 2026-10-28 operator wrap-up; original claims and amendments A1–A3 remain unchanged (`plans/round-53-claims.md`). Motivation and eventual measurement revision are recorded in LOG.md and SCORECARD.md's round-53 entry. Original honest-stop report remains in fleet history; this is completion of the same round, not a new claim.

## Gate

Four new source rows were opened on 2026-10-30. S194–S196 are admitted for bounded interpretation, cited by `corpus/knowledge/tb2-presence-only-triage.md`; S197 is rejected. Source row count is not expansion credit. Gate evidence: `.ufo/waves/round-53/w3/C1ScribeSources2A/gate.md`, `rows.md`, `fetch-log.tsv`; the L1 also reopened S194–S196 live. No existing row's status/recheck/used-by changed. New rows are born mined/mined/mined/rejected; draft queued-to-mined is not an edit of a registered row.

| row | URL and location | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S194 | https://philmcminn.com/publications/barr2015.pdf — p.1 Introduction | 2026-10-30 | “a procedure that distinguishes between the correct and incorrect behaviors of the System Under Test (SUT)” | admit B, oracle definition |
| S195 | https://arxiv.org/html/2609.34262v1 — §1 Introduction, first paragraph | 2026-10-30 | “Most benchmark verifiers evaluate observable outcomes, such as whether expected files exist, tests pass, or specified conditions are satisfied.” | admit A for authors' own framing |
| S196 | https://arxiv.org/html/2606.26300v1 — §2.1 Reward Faithfulness | 2026-10-30 | “the absence of false positives (an incorrect solution passes the tests) and false negatives” | admit A for authors' own framing |
| S197 | https://www.xunitpatterns.com/Assertion%20Roulette.html via https://web.archive.org/web/20250118170143id_/https://www.xunitpatterns.com/Assertion%20Roulette.html — raw HTML line 78, scribe A fetch | 2026-10-30 | “hard to tell which of several assertions within the same test method” | reject: failure localization, not existence-only oracle strength; flip: explicit existence-only assertion classification |

Search: bounded wave-1 source candidates were reopened by two scribes and a literature scout. Only these four rows are adopted; other proposals stay in seat directories, not a bulk registry append. A temporary S900–S927 census block appeared in production SOURCES; it was uncommitted, unadmitted and removed before final census, with proposals retained in scribe B's rows.md. This is not source-id reuse in a committed registry.

Pricing interpretation: the task's own captured/public grader source is the object under study, not independent prior art. A separate public issue, report or transcript documenting that task/test's existence-only weakness counts known. This is applied consistently to all pricing parts. A negative sweep is bounded evidence of search, never a universal novelty proof.

Spot-check: lane-dispatched reviewers agree with selected source quotes and reject weak fits (`w3/C1RevSources2.md`); they are not the protocol's non-author verifier. Independent closure must still sample an admit and a reject. No outside agreement is pre-claimed.

## Mistakes

| class | evidence pointer | captured-by | fix / measured limit |
|---|---|---|---|
| counter-reachable-without-the-work | w1/C1CritCounterReach/results/composite-fixture.txt; w1/C2CritLedgerReach/out/SUMMARY.txt beneath `.ufo/waves/round-53/` | Q42 and wave-1 attacks | A1 closes named forged-complete routes; committed counter selftests show those forgeries red (C1 47 cases, C2 52 cases; claims/c1-selftest.txt and c2-selftest.txt). New survivors remain evidence, not retroactive rule edits. |
| rule-unit-leak | round-52 W2CritC1Reach/receipts/live_tests.json; w1/C1ExecClassifier/fix-round-receipt.txt | round-52 outside spot-check, Q42 | AST function boundaries and helper attribution replace lexical splitting; adversarial fixture failures before the repair and zero after are committed in the classifier seat's receipts. |
| false-registry-cell | claims/c2-run1.txt: 18 mismatches | executed counter, Q42(c) | corrected ledger was independently rerun by w3/C2MeasureExecA/B: only the prematurely green round53-c1 remained mismatched. Final scored receipt, not prose intent, decides closure. |
| ledger-reason-overstates-cause | w3/C2RevLedgerPlan.md, round46-c3 sample | reviewer | reason must distinguish unexercised/rejected map rows from absent source content; declaration truth is more than a plausible explanation. |
| mechanical-verification-blocked | w3/C1TouchExecA/touch-run.json | touch executor | L1 installed pytest 9.2.0 through uv pip in scratch, preloaded imports and ran under bwrap: w3/C1TouchExecL1/touch-run-l1.json records 26 selected tests passing; synthetic module stubs mean no task-image claim. |
| never-read-is-not-never-examined | A1 Not changed; w3/C1CritNeverRead.md | wave-1 and wave-3 critics | frozen blocklist definition stays narrow; earlier machine class receipts do contain the task names. No rewrite of the definition after scoring. |
| oracle-integrity-limit | w3/C1CritOracle2.md | critic | content audit survives, integrity guarantee does not; record the failure instead of calling the instrument unforgeable. |
| incomplete-mutation-detector | w3/C1MutClassifier.md | mutation tester | 20/42 killed, 22 survive including witness-bearing mutants. The shipped suites do not prove classifier completeness. |
| unsafe-third-party-archive | w3/R53SentinelFetch2.md F1/F2 | stage_scan and sentinel | Substack analytics-token archive and Harbor API-key-placeholder fetch are withheld from landing; no credential values copied into lesson or report. |
| operator-interruption-partial-wave | original fleet round-53 report at e99074ba; goal run-11 wrap-up | operator | wave 3 completes remaining work; prior stopped seats are counted and not relabeled as completed findings. |

## Limits

Only the frozen predicates decide admission. Static presence-only labels concern individual tests, not the correctness of their surrounding task or whole-suite gameability. Label seats share a specification; independence is a protocol fact not guaranteed by the counter. Four re-label reviewers agree on 80/80 selected tests; this does not eliminate shared-spec bias. C2 may truthfully declare an unsound gate green or a legitimately stale pin red; matching exit codes are calibration, not repaired gate quality. Surface SF20 is down and SF14's count pin is stale-growth; no serving-plane intervention occurred.

## Assimilation

Assimilation: none. No considerthese proposal taken; frozen claims unchanged. Coverage cap questions remain open (kengaku round-25, round-33, round-51).

## Measured close

Unchanged C1 and C2 predicates both pass at d244d4d324636953cd7192f2586fe0332b874e57
(`.ufo/waves/round-53/claims/c1-final.txt`, `c2-final.txt`). Prior art covers 20/20 confirmed
tasks, known 7 / bounded-search new 13 / 13 URLs; C2 re-executes 78/78, zero mismatches or
missing evidence, green 66 / red 12. These measurements do not erase the integrity/argv critiques:
the SCORECARD holds novelty 8 and calibration 9 rather than claiming outside admission.

W3 WAVE-DONE received with 32 settled results; round total dispatched 109. Scout B's empty output
and failed wake (HTTP 429, retry-after-ms 13394000), Touch B's environment error and partial
mutation-counter output remain in results; they are not independent clearance. The L1 completed
the four missing pricing tasks from bounded archived tracker searches, without respawning a seat.
No further attack or bypass reproduction followed the orchestrator's defensive/documentary boundary.

Final census: 186→190 rows, exit 0→0; added tier A 3 and B 1, mined 3 and rejected 1.
Fleet misroot sweep found only orchestrator `.scratch/` and Mori's `count-c1.cover`/`count-c2.cover`
(owner path confirmed with `strings`); no kengaku misroot copied or deleted.
