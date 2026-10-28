# C1ScoutPriorArt — round 52 wave 1

Scout seat. Priced public prior art for R52-C1 (novelty). No lane-tree edit, no git mutation, no tool install. Pacman was not used.

Axes used while fetching: (1) the HTTP body is the document, not a challenge page; (2) each quote is a ≤25-word substring of that body; (3) the page speaks to whole-benchmark grader triage, to V1 presence-only, or to V4 sparse tests; (4) each task verdict is phenomenon-known, phenomenon-new, or left unstated when the page does not support it. Pages that failed (2) or were only a summary of an unread PDF were not quoted.

## Verdict

**A whole-benchmark grader-vacuity triage at the lane's instrument level is phenomenon-new relative to this fetch.** No fetched page states the frozen V1 rule (presence marker, no content marker, no behaviour marker) or the frozen V4 rule (no marker class and ≤2 `def test_` functions), and none statically classifies the Terminal-Bench 2.0 grader population into those two classes.

**The surrounding phenomenon is phenomenon-known.** Fetched pages already audit Terminal-Bench 2.0/2.1 tests as a population and already name weak or wrong graders ("let any solution pass", "let non-compliant outputs through", "limited grading logic", a patch that passes tests and still misses the developers' expectations).

**No task-level phenomenon-new finding is established here.** This seat did not run `plans/round52_c1_grader_audit.py` and did not label the 89 graders. Eight tasks that public pages already tie to a grader or test defect are priced phenomenon-known below, for the defect the page states, which is not the V1/V4 rule. A later confirmation is phenomenon-new only when no fetched primary already documents that task's grader defect.

V1 hazard: PR #53 publishes `os.path.exists` / `os.path.isfile` as the repair for over-specified listings on `polyglot-c-py` and `polyglot-rust-c`. tsDetect flags a *missing* `exists()` / `isFile()` call (Resource Optimism). An existence check is a documented repair, not a documented vacuity class.

Quoted sources with a verified substring in an HTTP 200 body: **10**.

## What was fetched

Working directory for curls: `/fast/scratch/hyaku/kengaku-r52/C1ScoutPriorArt` (`TMPDIR` set to that tree's `tmp`). Bodies saved under `fetch/`. Status via `curl -sS -L -w '%{http_code} %{size_download} %{content_type} %{url_effective}'`. Quotes checked as substrings of the saved bodies (HTML stripped only to confirm; the quote itself is the page text). `pdftotext -layout -f 1 -l 4` on the tsDetect PDF.

Of 22 requests, 20 returned HTTP 200 and 2 returned 403. Two of the 200s are OpenReview challenge interstitials, not the paper. No package was installed.

| id | status | bytes | url |
|---|---:|---:|---|
| tb-arxiv-html | 200 | 1088268 | https://arxiv.org/html/2601.11868 |
| tb-arxiv-pdf | 200 | 2773926 | https://arxiv.org/pdf/2601.11868 |
| aba-html | 200 | 694146 | https://arxiv.org/html/2605.26079v2 |
| aba-abs | 200 | 42885 | https://arxiv.org/abs/2605.26079 |
| swe-arxiv | 200 | 214992 | https://arxiv.org/html/2503.15223 |
| swe-abs | 200 | 45536 | https://arxiv.org/abs/2503.15223 |
| gh-pr53 | 200 | 817911 | https://github.com/harbor-framework/terminal-bench-2/pull/53 |
| gh-api-pr | 200 | 28522 | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53 |
| tbench21 | 200 | 148013 | https://www.tbench.ai/news/terminal-bench-2-1 |
| hf-verified | 200 | 147928 | https://huggingface.co/datasets/zai-org/terminal-bench-2-verified |
| june | 200 | 50673 | https://june.kim/terminal-bench-frame |
| tsdetect-pdf | 200 | 562193 | https://testsmells.org/assets/publications/FSE2020_TechnicalPaper.pdf |
| testsmells | 200 | 21012 | https://testsmells.org/pages/testsmells.html |
| snorkel | 200 | 479156 | https://snorkel.ai/leaderboard/terminal-bench-2-1/ |
| gh-issue | 200 | 1165621 | https://github.com/harbor-framework/terminal-bench/issues/1387 |
| gh-issue-api | 403 | 280 | https://api.github.com/repos/harbor-framework/terminal-bench/issues/1387 |
| openai-swe | 403 | 10078 | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ |
| buchanan-pdf | 200 | 4783 | https://openreview.net/pdf?id=AhXMZPnOPS (effective URL: OpenReview challenge page) |
| buchanan-forum | 200 | 4787 | https://openreview.net/forum?id=AhXMZPnOPS (effective URL: OpenReview challenge page) |
| lacuna | 200 | 80381 | https://lacuna.tiptreesystems.com/work/benchmarks-as-software-a-case-study-on-terminal |
| arxiv-api | 200 | 3452 | arXiv query "Benchmarks as Software" AND Terminal-Bench (hit: RSIGym 2610.10310, not a grader audit) |
| arxiv-buchanan | 200 | 7257 | arXiv query au:Buchanan AND Terminal-Bench (hit: 2601.11868, the Terminal-Bench paper) |

Lacuna was not quoted. It summarizes the OpenReview paper this seat could not read, including a 28-of-89 defect rate. Those figures stay out of the findings.

## Quoted sources

Full cards, both weakness-class notes, and the task lines are in `prior-art.md` beside this report. Compact list:

1. https://arxiv.org/html/2601.11868 — 200 — line 4504, `p#S2.SS3.p2.1` — "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state." (24 words). Validity bar for a task's tests. Not a triage of the 89 graders. V1 breaks the "only if" direction; V4 can fail the same bar. The paper names neither rule.
2. https://arxiv.org/html/2605.26079v2 — 200 — abstract line 320 — "uncovering issues such as hidden environment dependencies, specification gaps, and limited grading logic." (13 words). Also line 782: "Our trajectory audit independently recovered 14 of these 21 issues under strict matching" against Terminal-Bench 2 PR #53. Agentic whole-benchmark audit, not a static V1/V4 instrument. "Limited grading logic" is the general weak-grader phenomenon.
3. https://github.com/harbor-framework/terminal-bench-2/pull/53 — HTML 200 and API 200 — PR body line 8 — "Tests were updated when they over-specified or let any solution pass." (11 words). Population-level vacuity clause, not pinned to a task id in the fetched body, and not the marker rules.
4. https://www.tbench.ai/news/terminal-bench-2-1 — 200 — `#what-changed` line 11 — "Some tasks had instructions that were not aligned to their tests." (11 words). Official 28-task revision (meta description, line 1: "fixes 28 tasks"). Nine dependency-drift tasks and eight resource-budget tasks are counted in the same section. Misspecification, not V1/V4.
5. https://huggingface.co/datasets/zai-org/terminal-bench-2-verified — 200 — line 142 — "the test logic itself misjudged valid submissions or let non-compliant outputs through" (12 words). Names dna-insert, make-doom-for-mips, filter-js-from-html, install-windows-3.11. False fail and false pass. Not the marker rules. Line 148 says the authors reviewed the entire Terminal-Bench 2.0 dataset.
6. https://june.kim/terminal-bench-frame — 200 — lead paragraph line 14 — "On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion" (15 words). Model-free probe of all 89 Terminal-Bench 2.1 graders. Frame-blindness, not V1/V4, and not the 2.0 pin.
7. https://testsmells.org/assets/publications/FSE2020_TechnicalPaper.pdf — 200 — Table 1, pdftotext line 292 — "A test method that does not contain a single assertion statement and @Test(expected) annotation parameter" (15 words). Static Java/JUnit smell detector (Unknown Test). Empty Test is line 280. Not Terminal-Bench. Resource Optimism (line 289) flags a missing `exists()` / `isFile()` / `notExists()` call, the opposite of a V1 flag. Catalog https://testsmells.org/pages/testsmells.html is also 200; line 418 starts the same Unknown Test sentence.
8. https://arxiv.org/html/2503.15223 — 200 — `p#abstract1.1` line 243 — "a patch may pass the tests but nevertheless fail to match the developers’ expectations." (14 words). SWE-bench Verified study (Wang, Pradel, Liu, per the abs-page citation meta). Weak-oracle literature. Not Terminal-Bench and not V1/V4.
9. https://snorkel.ai/leaderboard/terminal-bench-2-1/ — 200 — line 491 — "A revision of Terminal-Bench 2.0 that fixes 28 of 89 tasks and introduces continuous validation for agentic benchmarks." (18 words). Leaderboard restatement of the 2.1 revision. Nothing on presence-only or sparse tests.
10. https://github.com/harbor-framework/terminal-bench/issues/1387 — HTML 200, API 403 — issue body in the page payload, line 644 — "Verifiers that grade against a golden artifact instead of solution properties" (11 words). The same paragraph audits TB3 verifiers. Over-strict oracle match, the opposite of V1/V4.

## Findings

FINDING polyglot-c-py verdict=phenomenon-known because PR #53 body line 96 (API HTTP 200) documents the 2.0 test `os.listdir == ["main.c"]` and its replacement by `os.path.exists`. The documented defect is an over-specified listing, not V1. The existence check is the published repair.

FINDING polyglot-rust-c verdict=phenomenon-known because PR #53 body line 102 documents `os.listdir == ["main.rs"]` replaced by `os.path.isfile`. Same distinction: over-specified listing at 2.0, existence check as the repair, not a V1 finding.

FINDING query-optimize verdict=phenomenon-known because two fetched primaries document a spec/test mismatch and do not describe the same mechanism. PR #53 line 133 says the test checks a SHA256 hash of the database file. The Terminal-Bench 2.1 note, line 11, says the tests expected Spark SQL while the instructions asked for PostgreSQL. Neither quote is V1 or V4. This seat does not decide which description matches pin 2fd12b88.

FINDING dna-insert verdict=phenomenon-known because the Z.ai card line 142 names it under Grading/Test Fixes whose test logic misjudged valid submissions or let non-compliant outputs through. That is a published grader defect. It is not the V1 or V4 rule.

FINDING make-doom-for-mips verdict=phenomenon-known because the same Z.ai sentence names a grading/test fix. PR #53's entry for this task, as fetched, describes a stale apt index in oracle.sh, a different defect. V1/V4 is not stated by either quote.

FINDING filter-js-from-html verdict=phenomenon-known because the Z.ai card names a grading/test fix and PR #53 line 53 says the tests perform a very specific BeautifulSoup4 normalization that the description does not state. That is an underspecified content check, not V1 or V4.

FINDING install-windows-3.11 verdict=phenomenon-known because the Z.ai card names a grading/test fix and PR #53 line 73 replaces a hardcoded VGA-flag list with `pathlib.Path.is_socket()` while `test_windows_keys_with_visual_feedback` still checks screenshots. Not presence-only, and not a ≤2-test grader.

FINDING configure-git-webserver verdict=phenomenon-known because PR #53 line 39 says the tests assumed a specific auth format. Over-specification, not V1 or V4.

## Files

- Draft: `/fast/scratch/hyaku/kengaku-r52/C1ScoutPriorArt/prior-art.md` (removed with the scratch tree at the end of this seat).
- Kept pricing: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutPriorArt/prior-art.md`
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutPriorArt/report.md`
- Same report text: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutPriorArt.md`

Free space seen before fetch: `/fast` 538G available (804G volume, 34% used). No ENOSPC.

## Not done

The OpenReview PDF for "Benchmarks as Software: Continuous Validation and a Patch for Terminal-Bench 2.0" was not read (challenge page). The GitHub issue API and the OpenAI SWE-bench post returned 403. This seat did not classify the frozen 89-task population, so it cannot price a confirmed V1/V4 queue that does not exist yet.
