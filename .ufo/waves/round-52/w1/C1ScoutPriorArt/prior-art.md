# R52-C1 prior art — whole-benchmark grader-vacuity triage

Seat C1ScoutPriorArt. Access date 2026-10-28. Population pin named by the frozen claim: harbor-framework/terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (89 tasks). This seat did not run `plans/round52_c1_grader_audit.py` and did not label graders V1/V4. Findings below price defects that fetched public pages already name.

Weakness classes in the frozen claim (section C1), file-level, first match:

- **V1** — a presence marker (`exists(`, `is_file(`, `is_dir(`, `os.path.exists`) and no content marker and no behaviour marker. The grader can pass on mere presence of an artefact.
- **V4** — no marker class matches and there are ≤2 `def test_` functions. The graded surface is sparse.

## Overall verdict

A whole-benchmark grader-vacuity triage **at this instrument level** is not described in any page fetched here. No source states the V1 rule or the V4 rule, and none statically classifies the Terminal-Bench 2.0 grader population into those two classes. Relative to this fetch, that instrument is **phenomenon-new**.

The surrounding phenomenon is **phenomenon-known**. Fetched pages already audit Terminal-Bench 2.0/2.1 task tests as a population, and they already name weak or wrong graders: tests that "let any solution pass", test logic that "let non-compliant outputs through", "limited grading logic", and patches that pass tests while missing the developers' expectations.

Score-rule consequence: a later confirmed V1 or V4 finding is phenomenon-new only when no fetched primary already documents that task's grader defect. Every task-id below is phenomenon-known for the defect the primary actually states. None of those statements is the V1 or V4 rule. This seat establishes no task-level phenomenon-new finding, because it did not classify the 89 graders.

Hazard for V1: PR #53 publishes `os.path.exists` and `os.path.isfile` as repairs for over-specified directory listings on `polyglot-c-py` and `polyglot-rust-c`. tsDetect's Resource Optimism smell is a *missing* `exists()` / `isFile()` call. An existence check is a documented repair and a documented expectation, not a documented vacuity class.

## Sources

Quoted sources with a verified substring in an HTTP 200 body: **10**. Full request tally is in the seat report.

### S1. Terminal-Bench 2.0 paper

- URL: https://arxiv.org/html/2601.11868
- HTTP: 200 (HTML 1,088,268 bytes; PDF of the same id also 200)
- Anchor: `p#S2.SS3.p2.1`, fetched HTML line 4504
- Quote (24 words): "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state."
- (a) States the validity bar for a terminal-bench task's tests. It does not triage the 89 graders.
- (b) V1 violates the "only if" direction when presence alone is treated as an acceptable end state. V4 can fail the same bar when two tests do not capture the acceptable states. The paper does not name either rule.

### S2. Auto Benchmark Audit (ABA)

- URL: https://arxiv.org/html/2605.26079v2
- HTTP: 200 (694,146 bytes). Abs page https://arxiv.org/abs/2605.26079 also 200.
- Anchor: abstract, fetched HTML line 320
- Quote (13 words): "uncovering issues such as hidden environment dependencies, specification gaps, and limited grading logic."
- Additional location, same page, `p#S4.SS1.SSS0.Px1.p1.1`, line 782 (13 words): "Our trajectory audit independently recovered 14 of these 21 issues under strict matching"
- (a) An agentic audit of individual tasks across 168 benchmarks, applied to Terminal-Bench 2, overlapping maintainer PR #53 (22 tasks; 14 of 21 extracted issues strictly matched). This is a whole-benchmark audit. It is not a static marker instrument.
- (b) "Limited grading logic" names weak graders in general. It does not define presence-only tests or a ≤2-test cutoff.

### S3. Maintainer proposal for Terminal-Bench 2.1

- URL: https://github.com/harbor-framework/terminal-bench-2/pull/53
- HTTP: 200 for the HTML page and 200 for `https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53` (title "Terminal-Bench 2.1", state open, merged false). Quotes are from the API `body`, which matches the PR description.
- Anchor: PR body line 8
- Quote (11 words): "Tests were updated when they over-specified or let any solution pass."
- (a) A maintainer list of instruction, test, and resource changes across the tasks named in that body. "Let any solution pass" is a population-level vacuity clause. The fetched body does not attach that clause to a task id.
- (b) The clause is the vacuity harm (a test that accepts anything), which is what V1 and V4 can cause. The body does not use those marker rules. See task findings for the existence-check repairs.

### S4. Official Terminal-Bench 2.1 note

- URL: https://www.tbench.ai/news/terminal-bench-2-1
- HTTP: 200 (148,013 bytes)
- Anchor: `#what-changed`, fetched HTML line 11, Misspecification item
- Quote (11 words): "Some tasks had instructions that were not aligned to their tests."
- Additional location, line 1 meta description (5 words): "fixes 28 tasks"
- (a) Official account of a 28-task revision of Terminal-Bench 2.0, with counted categories on the same page: nine tasks whose external dependencies changed, eight tasks with insufficient resource budgets, plus misspecification. Not a static grader classifier.
- (b) The quoted defect is instruction/test misalignment. The `query-optimize` example in that same list item is a wrong expected stack (Spark SQL vs PostgreSQL), not V1 or V4.

### S5. Z.ai Terminal-Bench 2.0 Verified card

- URL: https://huggingface.co/datasets/zai-org/terminal-bench-2-verified
- HTTP: 200 (147,928 bytes)
- Anchor: dataset card, 2026.08.18 update, fetched HTML line 142
- Quote (12 words): "the test logic itself misjudged valid submissions or let non-compliant outputs through"
- (a) Says the authors reviewed grading and instructions after Terminal-Bench 2.1 and, earlier on the same card (line 148), "conducted a comprehensive review of the entire Terminal-Bench 2.0 dataset". The grading sentence names four tasks, not an 89-way static triage.
- (b) "Let non-compliant outputs through" is a false pass (the harm of V1 and of a sparse V4). "Misjudged valid submissions" is a false fail. The card does not state the marker rules.

### S6. Terminal-Bench Is Blind to Destruction

- URL: https://june.kim/terminal-bench-frame
- HTTP: 200 (50,673 bytes). Page title in the fetched HTML: "Terminal-Bench Is Blind to Destruction".
- Anchor: lead paragraph, fetched HTML line 14
- Quote (15 words): "On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion"
- (a) A model-free probe of the official grader on all 89 Terminal-Bench 2.1 tasks (83 gold-passing). Whole-benchmark grader measurement, by re-running graders, not by static markers. The subject is 2.1, not pin `2fd12b88`.
- (b) The measured hole is unasserted destruction outside the graded target. A content-checking grader can still be frame-blind, so this is not V1 or V4. It does show that a whole-population grader probe already exists.

### S7. tsDetect (static test-smell tool)

- URL: https://testsmells.org/assets/publications/FSE2020_TechnicalPaper.pdf
- HTTP: 200 (562,193 bytes, `application/pdf`). Quotes from `pdftotext` of that PDF, Table 1.
- Anchor: Table 1, Unknown Test row, pdftotext line 292
- Quote (15 words): "A test method that does not contain a single assertion statement and @Test(expected) annotation parameter"
- Additional row, Empty Test, pdftotext line 280 (11 words): "A test method that does not contain a single executable statement"
- Corroborating catalog, also HTTP 200: https://testsmells.org/pages/testsmells.html line 418 begins "A test method that does not contain a single assertion statement".
- (a) A static, AST-based detector for Java/JUnit test smells. Not a Terminal-Bench grader triage.
- (b) Unknown Test and Empty Test are assertion-free / empty tests, which is adjacent to vacuity and not the same as V1 (V1 has a presence assertion) or V4 (≤2 tests and no markers). Table 1 Resource Optimism, pdftotext line 289, is the opposite of a V1 flag: "A test method utilizes an instance of a File class without calling the method exists(), isFile() or notExists()".

### S8. SWE-bench plausible-patch study

- URL: https://arxiv.org/html/2503.15223
- HTTP: 200 (214,992 bytes). Abs page https://arxiv.org/abs/2503.15223 also 200. Abs citation meta names You Wang, Michael Pradel, Zhongxin Liu, "Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study".
- Anchor: `p#abstract1.1`, fetched HTML line 243
- Quote (14 words): "a patch may pass the tests but nevertheless fail to match the developers’ expectations."
- (a) An empirical study of SWE-bench Verified patches, not a Terminal-Bench grader census.
- (b) Documents the weak-oracle harm (tests pass, result still wrong). It does not describe presence-only checks or a ≤2-test class, and it is not Terminal-Bench 2.0.

### S9. Snorkel Terminal-Bench 2.1 leaderboard

- URL: https://snorkel.ai/leaderboard/terminal-bench-2-1/
- HTTP: 200 (479,156 bytes)
- Anchor: visible revision sentence, fetched HTML line 491 (same sentence in the meta description, line 14)
- Quote (18 words): "A revision of Terminal-Bench 2.0 that fixes 28 of 89 tasks and introduces continuous validation for agentic benchmarks."
- (a) Restates a whole-benchmark revision count (28 of 89) and continuous validation. Not an independent static triage; treated as a leaderboard restatement of the 2.1 revision.
- (b) Says nothing about presence-only tests or sparse test counts.

### S10. Terminal-bench issue #1387 (adjacent; TB3)

- URL: https://github.com/harbor-framework/terminal-bench/issues/1387
- HTTP: 200 for the HTML (1,165,621 bytes). `https://api.github.com/repos/harbor-framework/terminal-bench/issues/1387` returned **403**.
- Anchor: issue body embedded in the page payload, fetched HTML line 644. Page title: "verifiers overfit to oracle solution".
- Quote (11 words): "Verifiers that grade against a golden artifact instead of solution properties"
- (a) The same paragraph says "Auditing the TB3 verifiers". This is Terminal-Bench 3, not the 2.0 pin.
- (b) The pattern is over-strict grading against an oracle artifact (exact string, JSON, or diff). That is the opposite of V1/V4 vacuity.

## Not used as primaries

- https://openreview.net/pdf?id=AhXMZPnOPS and https://openreview.net/forum?id=AhXMZPnOPS returned HTTP 200 but the effective URL was an OpenReview challenge page (4,783 and 4,787 bytes). The paper body was not fetched. An arXiv API query for Buchanan and Terminal-Bench returned the Terminal-Bench paper (2601.11868), not a separate "Benchmarks as Software" preprint.
- https://lacuna.tiptreesystems.com/work/benchmarks-as-software-a-case-study-on-terminal returned HTTP 200 and summarizes that unread paper (including a 28-of-89 defect rate). Those sentences are not quoted here, because they were not checked against the paper.
- https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ returned HTTP 403.

## Findings

FINDING polyglot-c-py verdict=phenomenon-known because PR #53 body line 96 (API HTTP 200) documents the 2.0 test `os.listdir == ["main.c"]` and its replacement by `os.path.exists`. The documented defect is an over-specified listing, not V1. The existence check is the published repair.

FINDING polyglot-rust-c verdict=phenomenon-known because PR #53 body line 102 documents `os.listdir == ["main.rs"]` replaced by `os.path.isfile`. Same distinction: over-specified listing at 2.0, existence check as the repair, not a V1 finding.

FINDING query-optimize verdict=phenomenon-known because two fetched primaries document a spec/test mismatch and do not describe the same mechanism. PR #53 line 133 says the test checks a SHA256 hash of the database file. The Terminal-Bench 2.1 note, line 11, says the tests expected Spark SQL while the instructions asked for PostgreSQL. Neither quote is V1 or V4. This seat does not decide which description matches pin 2fd12b88.

FINDING dna-insert verdict=phenomenon-known because the Z.ai card line 142 names it under Grading/Test Fixes whose test logic misjudged valid submissions or let non-compliant outputs through. That is a published grader defect. It is not the V1 or V4 rule.

FINDING make-doom-for-mips verdict=phenomenon-known because the same Z.ai sentence names a grading/test fix. PR #53's entry for this task, as fetched, describes a stale apt index in oracle.sh, a different defect. V1/V4 is not stated by either quote.

FINDING filter-js-from-html verdict=phenomenon-known because the Z.ai card names a grading/test fix and PR #53 line 53 says the tests perform a very specific BeautifulSoup4 normalization that the description does not state. That is an underspecified content check, not V1 or V4.

FINDING install-windows-3.11 verdict=phenomenon-known because the Z.ai card names a grading/test fix and PR #53 line 73 replaces a hardcoded VGA-flag list with `pathlib.Path.is_socket()` while `test_windows_keys_with_visual_feedback` still checks screenshots. Not presence-only, and not a ≤2-test grader.

FINDING configure-git-webserver verdict=phenomenon-known because PR #53 line 39 says the tests assumed a specific auth format. Over-specification, not V1 or V4.

No FINDING line above is phenomenon-new. The phenomenon-new claim is the instrument (static V1/V4 triage of the whole 2.0 grader population), which these pages do not describe, and for which this seat has no confirmed task id.
