# C1ScoutSrcBench — R53-C1 prior-art source scout (kengaku round 53, wave 1)

Seat: source scout, leaf (no subagents). Date of all fetches and searches: 2026-10-28.
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Assignment: find and archive prior art for
the R53-C1 topic "agent-benchmark test-quality audits" — SWE-bench test-patch insufficiency
(UTBoost, SWE-bench+, SWE-bench Verified follow-ups), Terminal-Bench / Harbor issue trackers and
PRs reporting tests that "let any solution pass" or only check artefact presence, and published
counts of such tasks — then draft registry rows and reject the rest with reasons.

Blindness compliance: this seat never read, ran or asked for `plans/round53_c1_classify.py`, any
`C1ExecClassifier*` file, or any `C1Label*` file or directory. Nothing below is tuned against any
other seat's output.

## What I did

1. Registry de-duplication first (contract rule 1): `grep https?:// corpus/SOURCES.md` plus full
   reads of all S001–S193 rows in two ranged reads. Relevant URLs already registered and therefore
   NOT re-rowed: PR #53 "over-specified or let any solution pass" (S184), TB2.1 announcement (S185),
   zai-org terminal-bench-2-verified card (S186), ABA audit arXiv 2605.26079 (S187), "Are Solved
   Issues Really Solved Correctly?" (S188), tsDetect (S189), TB2.0 paper incl. §2.3 Specificity
   (S020/S190), TB2.0 announcement (S090), OpenAI Verified retirement and Pro retraction (S005/S006),
   TB2.1 issue #133 (S114), TB2.1 PR #3 (S121), TB2.1 PR #245 (S124), legacy issue #1387 (S192,
   rejected), June Kim TB-frame blog (S191, rejected), Snorkel leaderboard (S193, rejected).
2. Six web_search queries (Q1–Q6, listed in `search-log.md`), 33 unique candidates identified.
3. Opened and archived 15 files / 14 distinct sources under `fetched/` (see Commands).
4. Drafted 6 kept rows (placeholders S901–S906; L1 to renumber S194+ on commit, per
   round-53-claims "S194+") and 8 rejected rows (S907–S914). No credentials, no private URLs
   (contract rule 6).

Commands (exact, abbreviating only the repeated fetch call):

```
grep https?:// corpus/SOURCES.md                     # registry URL extraction (read tool for full rows)
curl -sSL --max-time 60 -A "kengaku-r53-C1ScoutSrcBench/1.0" -o <slug>.<ext> <url>   # 15 fetches
wc -c * ; sha256sum $(ls -1 | grep -v '^SHA256SUMS$') > SHA256SUMS
head -c 1000000 preferencemodel-tb4-issues.html      # 1 MiB cap truncation (stated per contract)
grep -n -m1 "<quote>" <archive>                      # quote line-location for every row
```

Tool installs: none (no pacman, no uv/npm installs; nothing to record).

## Funnel numbers

identified 33; screened 14 (+1 corroboration file, trustworthy-env README); included 6; excluded 8;
unopenable 1 (OpenAgentsInc literal-artifact-checks raw doc: HTTP 404, demoted to unopened lead);
unopened leads 18. Full query list, exclusion reasons and stop rationale:
`.ufo/waves/round-53/w1/C1ScoutSrcBench/search-log.md`.

## Presence-only bearing of the six kept sources

The audit question per source: does it bear on "tests that pass if the named artefact merely
exists" in a benchmark grader? Quotes are verbatim from the archived bytes, at the stated line.

- S901 UTBoost — literal existence-only: **no**; topic's other disjunct "let any solution pass":
  **yes** — "the manually written test cases included in these pull requests are often
  insufficient, allowing generated patches to pass the tests without resolving the underlying
  issue" (utboost-abs.html:30).
- S902 SWE-bench+ — literal: **no**; weak-test disjunct: **yes** — "the tests were not adequate to
  verify the correctness of a patch" (swebenchplus-abs.html:30).
- S903 Probe to Generate — literal: **no**; test-gap disjunct: **yes** — "many previously accepted
  patches exploit benchmark test gaps rather than fully satisfying the intended repair semantics"
  (probe2gen-abs.html:30).
- S904 SWE-ABS — literal: **no**; weak-suite disjunct: **yes** — "passing only because weak test
  suites fail to expose their errors" (sweabs-abs.html:30).
- S905 UC Berkeley RDI (BenchJack) — literal: **YES** — "test 1 checks that C functions exist, but
  never calls them" and "The dummy .so satisfies the existence check" (rdi-trustworthy-benchmarks.html:179,202);
  a Terminal-Bench grader shown passing on the mere existence of the compiled artefact, plus a
  count (45 confirmed hacking proofs across 13 audited benchmarks).
- S906 tb-2-1 issue #156 — literal: **YES (in part)** — the verifier's own checks are filed as
  "No (existence, executability, prediction correctness only)" (tb21-issue-156.json:1): the
  benchmark's own issue tracker naming an artefact-existence verifier check.

If the L1's prior-art leg requires only literal presence-only sources, S905 and S906 carry that
burden alone; S901–S904 are the published-count prior art for the broader weak/insufficient-test
phenomenon named in the seat topic.

## Draft registry rows (placeholders; L1 renumbers to S194+)

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S901 | UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench — https://arxiv.org/abs/2506.09289 | paper | A | the paper's own insufficiency audit of SWE-bench test patches and its corrected leaderboard counts; not evidence about Terminal-Bench graders | arXiv 2506.09289 (10 Jun 2025; ACL 2025), abs page line 30 (og:description = abstract): "we identified 36 task instances with insufficient test cases and uncovered 345 erroneous patches incorrectly labeled as passed" (17 words); archive fetched/utboost-abs.html sha256 ebb9635f1fe675d13be3ac5d58719395b3000203fbbb59b27d96447e1fe24272 | published count that SWE-bench's own test patches are insufficient — patches pass without resolving the issue — with corrections hitting 40.9% of Lite and 24.4% of Verified leaderboard entries, so weak-test graders are documented and measured prior art | queued | 2026-10-28 | 180d | — |
| S902 | SWE-Bench+: Enhanced Coding Benchmark for LLMs — https://arxiv.org/abs/2410.06992 | paper | B | its own manual screen of SWE-Agent+GPT-4 passing patches against the gold pull requests; the weak-test-case share it reports | arXiv 2410.06992 (9 Oct 2024), abs page line 30: "31.08% of the passed patches are suspicious patches due to weak test cases" (13 words); archive fetched/swebenchplus-abs.html sha256 4c4f67e667cac4dc3881855b8c70f2713e945a49087b1bdc49ee68bee682812b | the earliest quantified weak-test share — 31.08% suspicious patches, resolution rate 12.47% to 3.97% after filtering — establishing that benchmark tests can fail to verify a patch's correctness | queued | 2026-10-28 | 180d | — |
| S903 | Probe to Generate: Program Variant-Guided Test Augmentation for Repository-Level Repair Benchmarks — https://arxiv.org/abs/2604.01518 | paper | B | its own variant-probe measurement of SWE-bench Verified test-suite gaps and the re-evaluated top-10 agent rates | arXiv 2604.01518 (2 Apr 2026), abs page line 30: "On SWE-bench Verified, 77% of instances admit at least one surviving variant" (12 words) and "many previously accepted patches exploit benchmark test gaps rather than fully satisfying the intended repair semantics" (16 words); archive fetched/probe2gen-abs.html sha256 1488003017e80c3fc66b573d04b4eb3f559cbef31c7ec515aff8d481e1fe93b9 | 77% of Verified instances admit a surviving variant and 1,014 generated tests across 211 instances cut top-10 resolved rates by 4.2-9.0% — a published count of under-constrained benchmark test suites | queued | 2026-10-28 | 180d | — |
| S904 | SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates on Test-based Benchmark — https://arxiv.org/abs/2603.00520 | paper | B | its own adversarial strengthening of SWE-bench Verified suites and the rejection share it reports | arXiv 2603.00520 (28 Feb 2026), abs page line 30: "passing only because weak test suites fail to expose their errors" (11 words); archive fetched/sweabs-abs.html sha256 6e2799f9c19d1de11680f7bd9f0cc6067d4c018b9c3766593820cc04ed251e58 | one in five top-30 "solved" patches semantically incorrect; strengthening 50.2% of Verified instances rejects 19.71% of previously passing patches and drops the top score 78.80% to 62.20% — the newest Verified follow-up count | queued | 2026-10-28 | 180d | — |
| S905 | We Scored 100% on AI Benchmarks Without Solving a Single Problem (UC Berkeley RDI; tool BenchJack) — https://rdi.berkeley.edu/blog/trustworthy-benchmarks/ | docs | A | the lab's own audit of 13 benchmarks with 45 confirmed hacking proofs of concept and the Terminal-Bench fake-C-extension walkthrough; self-published, not peer reviewed | post dated April 2026 (Hao Wang, Qiuyang Mang, Alvin Cheung, Koushik Sen, Dawn Song), body line 179: "test 1 checks that C functions exist, but never calls them" (11 words) and line 202: "all three tests pass without writing any meaningful C code" (10 words); archive fetched/rdi-trustworthy-benchmarks.html sha256 2e5c7b1bb11f94052eae4badcb56b587ca937d2f563872d1556d5d0a52f56877; companion tool repo archived fetched/trustworthy-env-readme.md sha256 d356c76b02a8bd8e0828e5cf8907405cb417586629e7faeb15426639a651d5a9 | the literal presence-only pass demonstrated end to end: an existence check on the compiled artefact plus wrapper-level correctness and performance tests let a dummy .so score fully; 45 confirmed hacks across 13 audited benchmarks including Terminal-Bench | queued | 2026-10-28 | 90d | — |
| S906 | harbor-framework/terminal-bench-2-1 issue #156 "pytorch-model-cli: README requires C but instruction/verifier do not" — https://github.com/harbor-framework/terminal-bench-2-1/issues/156 | docs | B | what the benchmark's own tracker reports about this task's verifier contract mismatch; the TB2.1 tree, not the TB2.0 pin | issue opened 2026-07-18 by alexgshaw, state open at access; API JSON body line 1, Contract-mismatch row for tests/test_outputs.py: "No (existence, executability, prediction correctness only)" (6 words); archive fetched/tb21-issue-156.json sha256 376e1706a43dca4147432520936d27aa736a4fd1b479e7e41f4f796acc8289f0 | a maintainer-filed issue naming a Terminal-Bench verifier whose checks are existence, executability and prediction correctness only — artefact-presence grading acknowledged inside the benchmark's own issue tracker | queued | 2026-10-28 | 90d | — |
| S907 | SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents — https://arxiv.org/abs/2609.04167 | paper | B | its own review-constraint benchmark and the functional-pass vs constraint-compliance gap it reports | arXiv 2609.04167 (3 Sep 2026), abs page line 30: "among 644 repairs that pass the functional tests, 221 fail to satisfy the provided review constraints" (17 words); archive fetched/swe-gate-abs.html sha256 c5cb239d77fb48911c9bd1f3fc9f55e01b52e8fa640157630d4c29b2d501d060 | REJECTED: measures review-constraint compliance, a different defect axis — its functional tests are not the broken element and nothing turns on artefact presence; flip: a SWE-Gate-style finding that functional tests alone admit artefact-creation solutions | rejected | 2026-10-28 | 180d | — |
| S908 | A Determinacy Audit of SWE-bench Pro (June Kim) — https://www.june.kim/a-determinacy-audit-of-swebench-pro | community | C | the audit's own determinacy classification of 728 public SWE-bench Pro tasks; not its view of other audits' weak-test findings | published 2026-06-21, addendum 2026-10-09; rendered line 14: "The broader audits also examine other defects, including tests that accept incomplete solutions" (13 words); archive fetched/junekim-swebench-pro-determinacy.html sha256 69124a53f9e118e751a5259fbd457dca9f39f8c20bef9b6a3990ffee56eb40f0 | REJECTED: measures underdetermined task specifications on SWE-bench Pro, not weak or presence-only graders, and places tests-accept-incomplete-solutions among other audits' findings; flip: a presence-only finding about the TB2.0 pin in its committed artifact | rejected | 2026-10-28 | 90d | — |
| S909 | harbor-framework/terminal-bench issue #1634 "math-eval-grader: do not pass submitted answer text to sympy.sympify" — https://github.com/harbor-framework/terminal-bench/issues/1634 | docs | B | what the tracker reports about this grader's unsafe parsing of submission-controlled text | issue body, API JSON line 1: "sympy.sympify is not safe for untrusted input"; archive fetched/tb-issue-1634.json sha256 76ba6981ae22c90ec7a3920d4af1669c70848fdeaa2e169f5bd51b8397dd2844 | REJECTED: grader input-injection (submitted answer text evaluated by sympify), a code-execution channel defect, not a test that passes on artefact presence; flip: the same tracker documenting a grader whose assertions are satisfied by creating the named file | rejected | 2026-10-28 | 90d | — |
| S910 | harbor-framework/terminal-bench issue #1636 "embedding-drift-monitor: verifier tampering" — https://github.com/harbor-framework/terminal-bench/issues/1636 | docs | B | what the tracker reports about forged per-test verdict bytes in this task's verifier channel | issue body, API JSON line 1: "forks. The child closes only the read end, drops privileges, and"; archive fetched/tb-issue-1636.json sha256 0303be3384db17032ce9825c2ee57e0701f706b90d0c61d3d0cb9439afd45302 | REJECTED: forged per-test pass bytes through a writable verifier channel, an integrity-channel attack, not a test-strength or presence-only defect; flip: a tracker item asserting a test passes whenever the named artefact exists | rejected | 2026-10-28 | 90d | — |
| S911 | bohrin docs/WEAKNESSES.md — https://raw.githubusercontent.com/prabhu-gopal/bohrin/main/docs/WEAKNESSES.md | community | C | the repo's own weaknesses note for its graders; no benchmark task, pin or grader bytes named | docs/WEAKNESSES.md at main, line 345: "A grader whose logic never inspects the work (it checks who spoke last, or that a file exists) passes anything that reaches it." (23 words); archive fetched/bohrin-weaknesses.md sha256 11a20d288acedf4e0b35c4a538308e2fe9438835674bbaece6d7f4a2f6aa980d | REJECTED: an unrefereed in-repo note about its own harness; states the phenomenon class but names no benchmark task or measured count; flip: a published audit naming a TB2.0-pin task whose grader only checks existence | rejected | 2026-10-28 | 90d | — |
| S912 | Benchmark Integrity Maintenance (Unearned Passes and Channel Closure), howardism.dev — https://www.howardism.dev/articles/benchmark-integrity-maintenance | community | C | the essay's own maintenance methodology and its worked violation examples | article published 2026-10-21; rendered line 19: "a Terminal-Bench agent that received the first six characters of the answer" (11 words, HARDCODE_OUTPUT case); archive fetched/howardism-benchmark-integrity.html sha256 b72fb6ef71fc5c00783da0f94c2f08b6ca6d613005664ab29a94d5443ef29dfa | REJECTED: a methodology essay on auditing unearned passes; its examples are reward-hacking taxonomy (SCOPE_MISMATCH, PROCESS_SHORTCUT, HARDCODE_OUTPUT), not existence-only graders; flip: the essay adding task-level evidence for a TB2.0-pin presence-only grader | rejected | 2026-10-28 | 90d | — |
| S913 | dynamo/log-report — a repaired Terminal-Bench 2 (Harbor) task (MihirBindu/dynamo-log-report-fix) — https://github.com/MihirBindu/dynamo-log-report-fix | community | C | the fork's own reproduction of the original task's grader checks and its pass-without-solving list | README at main, lines 77-78: "def test_report_nonempty():" / "assert Path(\"/app/report.json\").stat().st_size > 0" and line 82 "echo '{}' > /app/report.json" (empty object, no required keys); archive fetched/dynamo-readme.md sha256 bb8fef17f9a808b8afc39016f5d01ebc8bba75d50cd4c857e51ba493f398fa9c | REJECTED: a third-party repair fork; the original grader checked existence plus a size value (so a 2-byte JSON object passes), which is the size class not presence-only, and the task's identity in the 2fd12b88 pin is unverified; flip: the same weakness documented for a task confirmed in the pin | rejected | 2026-10-28 | 90d | — |
| S914 | Terminal Bench 4: Every Issue We Found (Preference Model) — https://preferencemodel.com/blog/terminal-bench-4-is-saturated/issues/ | community | C | the post's own per-issue list of Terminal Bench 4 grading problems | page title element (line 1 of the archived bytes; site name elided here to keep the cell pipe-free): "Terminal Bench 4: Every Issue We Found"; archive fetched/preferencemodel-tb4-issues.html (first 1000000 bytes of a larger JS-rendered page, byte cap applied) sha256 471cfde2563553733251c2f6797ea509edb5fd22defc6bbeba24ff745bab2f34 | REJECTED: measured on Terminal Bench 4, not the TB2.0 pin (the pin-mismatch rule that rejected S191), and the archived first MiB yielded no located per-task grader statement; flip: a pin-2fd12b88 per-task grader table from the same reviewer | rejected | 2026-10-28 | 90d | — |

## Files produced (absolute paths)

- Report: /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcBench.md
- Search log: /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcBench/search-log.md
- Archives (15 files, each ≤ 1 MiB) + SHA256SUMS:
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcBench/fetched/
  utboost-abs.html, swebenchplus-abs.html, probe2gen-abs.html, sweabs-abs.html,
  rdi-trustworthy-benchmarks.html, tb21-issue-156.json, swe-gate-abs.html,
  junekim-swebench-pro-determinacy.html, tb-issue-1634.json, tb-issue-1636.json,
  bohrin-weaknesses.md, howardism-benchmark-integrity.html, dynamo-readme.md,
  trustworthy-env-readme.md, preferencemodel-tb4-issues.html (truncated from a larger page to the
  1 MiB cap, first 1000000 bytes), SHA256SUMS.

## Inference flags and remaining unknowns

- [INFERENCE] The Terminal-Bench task behind the Berkeley fake-C-extension example was identified
  by a search-result summary as `portfolio-optimization`; neither the blog nor the archived
  trustworthy-env README names the task, and I did not verify it in the TB registry. The S905 row
  deliberately does not depend on that name.
- Which TB release the S905 task belongs to (1.x hub, 2.0 pin, or other) is unresolved; the blog
  says only "Terminal-Bench".
- The seat brief cites "CORPUS.md rules 1/5/6"; the contract was found at the fleet root
  /home/vgpnk/Projects/shokunin/CORPUS.md (SOURCES contract v1 carried in full), not at
  corpus/CORPUS.md. Rules 1, 5 and 6 were followed.
- Bash jobs ran as supervised background services in this environment (no output lost; all
  verified via proc:// reads). No ENOSPC seen; no tool output behaved inconsistently with its
  documentation (no tool-issue lines to add).
- Scratch: /fast/scratch/hyaku/kengaku-r53/C1ScoutSrcBench/ was created for this seat and removed
  before yield (it held no deliverables).
