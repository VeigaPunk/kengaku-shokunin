# R52-C1 prior art — independent wave-2 pricing (seat W2ScoutPriorArtFresh)

Access date 2026-10-28. Read-only: no lane file was modified; the frozen pin
`harbor-framework/terminal-bench-2` `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (89 tasks) was not
re-fetched into the lane tree. This seat priced the **five confirmed findings** produced by the
wave-2 confirmation seats (W2ExecConfirmA/W2ExecConfirmB, identical rows): presence-only test
functions in `bn-fit-modify`, `build-cython-ext`, `caffe-cifar-10`, `cancel-async-tasks`,
`code-from-image`. The A5-excluded capture (`sanitize-git-repo/tests/test_outputs.py`) was not
touched and its absence is not counted here.

## Sources fetched (all HTTP 200 on 2026-10-28)

14 URLs fetched, 14 with status 200. Quotes are verbatim substrings located in the fetched bodies
(saved under scratch `fetch/` during the seat run; receipts copied to the wave report dir).

| id | URL | status | located quote (≤25 words) |
|---|---|---|---|
| S1 | https://arxiv.org/abs/2601.11868 | 200 | "Current benchmarks either do not measure real-world tasks, or are not sufficiently difficult to meaningfully measure frontier" |
| S2 | https://arxiv.org/html/2601.11868v1 (TB2 paper, Merrill et al.) | 200 | "Test case quality is not assessed via objective, automated metrics. Instead, the benchmark relies on extensive human review" (§B.5) |
| S2b | same body, §B.4 | 200 | "tests might only check existence of a correct answer but not absence of wrong answers" |
| S3 | https://arxiv.org/abs/2507.02825 (ABC checklist) | 200 | "SWE-bench-Verified uses insufficient test cases, while τ-bench counts empty responses as successful" |
| S3b | https://arxiv.org/html/2507.02825v2 | 200 | "Since such tests can be incomplete or not perfectly sound, a patch that passes them may still be wrong" |
| S4 | https://arxiv.org/html/2605.26079v1 (Auto Benchmark Audit) | 200 | "an agentic framework that systematically audits individual benchmark tasks, uncovering issues such as hidden environment dependencies, specification gaps, and limited grading logic" |
| S4b | same body | 200 | "filtering out these tasks with issues shifts model rankings and increases average performance on SWE-bench Verified and Terminal-Bench 2 by 9.9% and 9.6%" |
| S5 | https://arxiv.org/html/2604.24955v2 (BenchGuard) | 200 | "many apparent agent failures are not failures of the agent at all—they are failures of the benchmark itself" |
| S6 | https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/67 | 200 | "The agent instead built a fake MIPS binary that prints the DOOM init banner" |
| S7 | https://api.github.com/repos/harbor-framework/terminal-bench/issues/2086 | 200 | "Task Audit: A review of all current tasks, mapping their verification categories to potential cheating paths" |
| S8 | https://api.github.com/repos/harbor-framework/terminal-bench/issues/1387 | 200 | "Below are the 33 tasks whose reward depends (fully or partly) on matching the oracle" |
| S9 | https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/CONTRIBUTING.md | 200 | "a solution passes verification if and only if it successfully completes the instruction" |
| S10 | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53 | 200 | "Tests were updated when they over-specified or let any solution pass" |
| S10b | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53/files | 200 | patch hunk touching `caffe-cifar-10/tests/test_outputs.py` with `def test_prototxt_files_exist():` unchanged in context |
| S11 | https://www.tbench.ai/news/terminal-bench-2-1 | 200 | "Eight tasks had insufficient resource budgets for at least one valid approach" (misspecification item: "instructions that were not aligned to their tests") |
| S12 | https://june.kim/terminal-bench-frame | 200 | "On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion" |

(URL count: S1,S2,S2b,S3,S3b,S4,S4b,S5,S6,S7,S8,S9,S10,S10b,S11,S12 = 14 distinct fetched URLs.)

## What each source says about the claim's two halves

- **S2/S2b (TB2 paper).** *Instrument:* the benchmark's own QC runs a benchmark-wide adversarial
  exploit agent (§B.4, OpenHands, all trajectories hand-verified) and self-assesses on the ABC
  (§B.5) — a whole-benchmark grader triage already exists in print, in dynamic agent form. The same
  §B.5 concedes the lane's variant is absent there: no objective automated test-quality metric.
  *Findings:* the authors themselves publish that existence-only checks are a common exploit
  ("tests might only check existence…"), and "Weak Verification" is a named class in their own
  failure taxonomy (§C.2).
- **S3/S3b (ABC).** *Instrument:* a published checklist for auditing agentic benchmarks'
  outcome/task validity (manual, 10 benchmarks). *Findings:* insufficient/incomplete test cases
  documented as inflating agent scores by "up to 100% in relative terms" — the presence-only
  weakness class is known.
- **S4/S4b (ABA).** *Instrument:* automated static+trajectory audit, **run on the exact same
  Terminal-Bench 2 population (n=89, $0.64/task)**, with a static mode ("Static and trajectory
  modes yield the identical audit results for many tasks"), validated against maintainer PR #53
  (strict recall 14/21 = 66.7%). *Findings:* flagged TB2 tasks; removing them lifts per-model
  scores by ~9.6%. This is the strongest single piece of instrument-level prior art.
- **S5 (BenchGuard).** *Instrument:* automated auditing of evaluation infrastructure, evaluated on
  a TB2 gold-issue set (24 findings). *Findings:* rigid evaluation scripts mis-grading valid work.
- **S6 (tb2 issue #67).** *Findings:* a specific TB2 grader (make-doom-for-mips) publicly shown
  reward-hackable. Not one of the confirmed five.
- **S7 (tb issue #2086).** *Instrument:* a proposed "Task Audit: A review of all current tasks"
  mapping verification categories to cheating paths — whole-population grader triage as a public
  proposal.
- **S8 (tb issue #1387).** *Instrument+findings:* a published per-task enumeration of grader flaws
  (33 oracle-matching tasks, TB3) — instance-level population audit, opposite failure mode.
- **S9 (CONTRIBUTING.md).** *Instrument:* the maintainer quality bar ("if and only if") plus
  "automated and manual review" of tasks.
- **S10/S10b (PR #53, base sha = the lane's pin `2fd12b88`).** *Instrument+findings:* maintainers
  audited and revised 26 tasks; their own vacuity language is "let any solution pass". The diff
  rewrites `caffe-cifar-10/tests/test_outputs.py` but leaves `test_prototxt_files_exist()`
  untouched — the presence-only test survived the maintainer fix unflagged.
- **S11 (2.1 release note).** *Findings:* the official 28-task revision of TB 2.0 (drift,
  resource, misspecification categories); no presence-only category.
- **S12 (frame-blindness probe).** *Instrument:* a whole-population dynamic grader probe
  (re-run official grader under mutations) on 2.1; 40/83 gold-passing tasks certify after careless
  deletion. Version differs from the pin; mechanism (final-state-only grading) differs from
  presence-only classification, but it is a whole-benchmark grader audit in print.

## Per-finding verdicts

Method: each confirmed finding (the presence-only test in that task's grader) was searched for in
every fetched primary: ABA per-task tables (text search of S4 body), PR #53's 57-file list and
task sections (S10/S10b), the 2.1 note's task categories (S11), issues #67/#1387/#2086, and the
TB2 paper body (S1/S2 — all five names appear only in the Appendix H task list, which lists the
population, not defects).

FINDING bn-fit-modify verdict=phenomenon-new because no fetched primary names this task (0 hits in ABA's per-task tables; absent from PR #53's 57 files and the 2.1 note's 28 tasks); only the weakness class is published (S2b existence-only checks; S10 "let any solution pass").

FINDING build-cython-ext verdict=phenomenon-new because no fetched primary names this task (0 ABA hits; absent from PR #53 files and the 2.1 note); class-level documentation only.

FINDING caffe-cifar-10 verdict=unclear because this task's grader is publicly reviewed twice — ABA flags two over-strict Evaluation issues and PR #53 rewrites `tests/test_outputs.py` — yet the presence-only `test_prototxt_files_exist` survives both unflagged: weakness-level new, task-level known. Weakest of the five.

FINDING cancel-async-tasks verdict=phenomenon-new because no fetched primary names this task (0 ABA hits; absent from PR #53 files and the 2.1 note); class-level documentation only.

FINDING code-from-image verdict=phenomenon-new because no fetched primary names this task (0 ABA hits; absent from PR #53 files and the 2.1 note); class-level documentation only.

## Overall verdict on instrument-level novelty

1. **The category is phenomenon-known.** Whole-benchmark grader triage and published audits of
   Terminal-Bench 2 graders exist in fetched primaries in at least four forms: the benchmark's own
   adversarial exploit agent + ABC self-assessment (S2), an automated static+trajectory audit of
   the same 89-task population (S4), a community framework proposal to review all tasks' verifiers
   (S7), and the maintainers' own 26-task/28-task public revisions (S10, S11). The claim's wording
   "the lane has no instrument that audits a benchmark's graders as a population … This claim lands
   the first one" is true of the lane and false of the world.
2. **The specific static variant is not documented.** No fetched primary describes a static,
   per-test-function, marker-vocabulary presence-only classifier over grader bytes (P1/P2/P3/P0).
   TB2's own §B.5 concedes no objective automated test-quality metric exists in its QC; ABA's
   static mode is LLM-rubric per-task auditing, not marker classification.
3. **The findings class is known; the instances are new.** The score rule's
   "phenomenon-new" leg survives only under weakness/instance-level pricing (4 of 5 findings new,
   1 unclear). Under class-level pricing it fails: S2b, S3, and S10 document existence-only
   tests and "let any solution pass" in this very benchmark.
4. **Recommended disclosure for the lane's prior-art.md:** cite S2 (§B.4/§B.5), S4, S5, S10 and
   S11 as the class-level price; keep per-finding weakness-level verdicts with the per-task
   negative searches (ABA tables, PR #53 file list, 2.1 note categories); state the dual reading
   explicitly. A prior-art leg that prices only instance-level novelty without these citations
   overstates novelty and is falsifiable by S4 alone.

Confidence: high on fetch statuses and quotes (bodies retained as receipts); high on ABA/PR #53
task-level negatives (direct text search of fetched bodies); medium on "not documented anywhere" —
absence over the fetched set only, not the whole web.

Cross-reference vs wave 1 (`C1ScoutPriorArt/prior-art.md`): independent pricing reached the same
structural verdict (instrument variant new, phenomenon class known) with 4 sources wave 1 did not
have (ABC, BenchGuard, issues #67/#2086, PR #53 files endpoint) and extends wave 1 by pricing the
five confirmed task ids wave 1 explicitly could not ("this seat has no confirmed task id").
