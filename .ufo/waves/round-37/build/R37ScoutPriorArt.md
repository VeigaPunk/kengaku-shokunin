# R37ScoutPriorArt — prior-art check for the C2 observations (kengaku round 37, wave 1)

Seat: scout, leaf, read-only. No lane file edited; no scratch dir needed (web reads only; one lane capture read with `grep`).
Fetch date 2026-10-26. All URLs below were fetched this run unless marked "search-snippet only".

## Observations checked

- **O1** Verdict is a substring of stdout that echoes agent-controlled content (verdict-token injection / output spoofing). In the pinned grader: `test_outputs.py` asserts `"TEST PASSED" in result.stdout`. `verify.sh` echoes the served body (`echo "Content: $CONTENT"`, and `Got: '$CONTENT'` on the FAILED branch). Located in the lane capture `corpus/evidence/round37/tb2-git-webserver/verify.sh:62,68` (grep output this run).
- **O2** Shell-script verifier ignores intermediate exit statuses (no `set -e`; expect-step status never read).
- **O3** Published audits of TB2.0 tasks reporting broken or weak tests, especially `configure-git-webserver`.

## Verdicts (summary)

| Obs | Verdict | One-line reason |
|---|---|---|
| O1 class (stdout/log scraping spoofed by agent-controlled output) | **published** | SWE-bench #601, #667; env-r2e-gym #11; hud-python #736; reward-hack-patterns RHP-06; BenchJack V7 |
| O1 instance (TB2 `configure-git-webserver`: served body echoed into stdout, `TEST PASSED` substring, verify.sh prints `TEST FAILED`) | **not found** (incremental) | Only one source mentions the substring plumbing, and it calls it "unchanged", not a flaw |
| O2 for this task | **published** | TB2.1 issue #133 (names "no `set -e`"), PR #37, JonathanGabor audit (weakness 3) |
| O2 generic (shell verifier without `set -e`) | **not found** as a named class; adjacent: RHP-07 exit-code-only | no source treats missing `set -e` as a class |
| O3 | **published** for "task is soft"; **not found** for the rest of the receipt's headline observations | see §3 |

## 1. O1 — verdict token / stdout echo

Hits (all fetched):

1. **SWE-bench #601**, "[Bug] Test Result Hijacking via Stdout Forging in Evaluation Harness", https://github.com/swe-bench/SWE-bench/issues/601 (Description). Quote: "By forcing the application to print forged success indicators (such as === 1 passed ===), the regex parser is tricked". Maintainer comment, Aug 14 2026: "grading refuses to score a run that reports no failures while the tests exited non-zero." Same class (verdict read from agent-influenced stdout); channel is the patched code's own stdout, not a served HTTP body.
2. **SWE-bench #667**, https://github.com/SWE-bench/SWE-bench/issues/667 (Description, open). Quote: "a patch that prints the marker during the test run is scored resolved" (title). Shows a forged marker inside the parsed region defeats an exit-code guard (rows D1/D2 of its table).
3. **GeneralReasoning/env-r2e-gym #11**, filed finding https://github.com/holdout-cc/holdout-findings/tree/main/findings/GeneralReasoning__env-r2e-gym__parse-log-passed-substring (Summary). Quote: "`FAILED ...::test_distance - PASSED` is recorded as passed." Closest structural match to O1: the grader scans a line that **echoes failure data** (the message) for the token `PASSED`, so data content becomes the verdict. Open, no fix PR (as of 2026-10-25).
4. **reward-hack-patterns RHP-06 "Pass counts or results scraped from stdout"**, https://github.com/holdout-cc/reward-hack-patterns/tree/main/patterns/06-stdout-scraping (What it is). Quote: "The code under test writes to the same stdout and stderr, so it can print a fake summary." Seen-in-the-wild list: hud-python #736 (`print("10 passed")`), env-r2e-gym #11.
5. **BenchJack paper**, arXiv 2605.12673, https://arxiv.org/html/2605.12673v1 §4.1. Taxonomy classes "V5 Weak string matching" and "V7 Trusting untrusted output"; V7 "generalizes ... to any signals (e.g., test output) that the agent can potentially influence." Berkeley RDI blog https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/ pattern 5: "WebArena's `must_include` uses substring containment."
6. TB2 paper, arXiv 2601.11868 §2.1 (https://arxiv.org/pdf/2601.11868). Quote: "they do not test the agent's commands or console output." This is a stated design principle that the pinned grader violates in practice (it reads console output); the paper does not examine any task for it.

Instance search (TB2 `configure-git-webserver` body echo → `TEST PASSED`):

- **harbor-framework/terminal-bench-2-1 PR #37** (https://github.com/harbor-framework/terminal-bench-2-1/pull/37, Summary) is the only hit that names the plumbing: "the reward plumbing (`test_outputs.py` greps stdout for `TEST PASSED`) is unchanged." It gates clone/commit/push and adds a per-run nonce, but treats the substring plumbing as out of scope. It never says a body containing `TEST PASSED` passes while verify.sh prints `TEST FAILED`. A body equal to the nonce string would still be echoed on the `Content:` line, so I infer (not run) the patched script keeps the echo; the PR diff was not read.
- The TB2.1 `main` verify.sh and test_outputs.py I fetched (raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/tasks/configure-git-webserver/tests/) still have the unconditional `echo "Content: $CONTENT"` and `assert "TEST PASSED" in result.stdout` (fetched this run; PR #37 and issue #133 are still open).
- Web-search for the string combination found nothing naming a body-injection exploit. A search-assistant answer (snippet-only, unverified) described the substring check as "a potential false-positive path" but conceded "Direct retrieval of the full files failed" and cited no source with an exploit. I do not count that.
- BenchJack's 219 flaws / Terminal-Bench entry (§5.1, https://arxiv.org/html/2605.12673v1) lists TB's major flaw as V1 (binary trojans), not per-task verifier echo. I grepped the fetched part for `git-webserver`/`TEST PASSED`: no hit. The remaining lines of the paper (appendices, 3533 lines total) were grepped only, not read.

**O1 verdict:** class = published (6 hits). Task instance = not found, so the instance is incremental: a data channel (HTTP body from a service the agent runs) that reaches the verdict substring via a helper script's echo, in a TB2 task. Near-neighbour that blunts novelty: env-r2e-gym #11 (data echoed into the scanned line).
Caveat on novelty wording: do not claim "first token-injection grader". Claim only "first probed instance for TB2 `configure-git-webserver`, shown by executed probe".

## 2. O2 — shell verifier ignoring intermediate statuses

- **TB2.1 issue #133** "configure-git-webserver: soft verifier awards reward 1 without working SSH", https://github.com/harbor-framework/terminal-bench-2-1/issues/133 (Actual behavior). Quote: "the script has no `set -e` / explicit failure check on the clone/push." Opened by alexgshaw (benchmark lead) Jul 14 2026; reproduced on leaderboard PR #129 trials with reward 1.0 and no sshd. Suggests `set -euo pipefail`. Open.
- **TB2.1 PR #37** (same URL as above). Quote: "never checked whether its own `git clone` / `git commit` / `git push` succeeded." Matrix row: "Webserver + static file only, no git/ssh (cheat) | PASS". Also reports 3 of 5 opus-4.8 trials were false passes; verdict "anticorrelated with solution quality". Open PR, one commit, 2 participants.
- **JonathanGabor/terminal-bench-2-audit**, audit run 20260120_125158, https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/audit_results/20260120_125158/audit.txt (lines 592-627). Quote: "The expect script doesn't explicitly verify that git operations succeeded before checking the web server." Rated the task 4 ("solid coverage"); that audit read the TB2.0 expect-based script (same shape as the pinned one). So an LLM auditor saw O2 for this exact script in January 2026 and rated it a minor weakness.
- Contrast hit (search-snippet only): Marginlab explorer shows TB2 `git-multibranch` test using `#!/bin/bash set -e`, so TB2 authors used `set -e` elsewhere. Not independently fetched.

**O2 verdict:** published for this task (3 hits, one by the TB2.1 maintainer). Not found as a generic class; nearest class is RHP-07 (exit-code-only, https://github.com/holdout-cc/reward-hack-patterns/tree/main/patterns/07-exit-code-only), which is about verdicts from exit codes, not about missing `set -e` in shell helpers. Note #133 and PR #37 date from July 2026, after the TB2.0 pin the lane used; they are about the TB2.1 file, whose auth block differs (SSH key, `user@localhost`) from the pinned expect/password version.

## 3. O3 — audits of TB2.0 tasks reporting broken or weak tests

- **TB2 paper** arXiv 2601.11868 (https://arxiv.org/pdf/2601.11868) §2.3 and §7: three human reviews per task ("roughly three reviewer-hours"), and "We acknowledge that our benchmark may still have flaws." Appendix task table (line 1640 of fetched text) lists `configure-git-webserver` only as a task description. No verifier-weakness finding for it.
- **TB2.1 release note**, https://www.tbench.ai/news/terminal-bench-2-1. Quote: "fix issues in 28 of the 89 tasks"; chart lists configure-git-webserver at +4.2%. Categories: external dependencies, resource mismatches, misspecification. PR #53 (https://github.com/harbor-framework/terminal-bench-2/pull/53) says for this task only: "Fix oracle solution: Task description promised to handle auth, but tests assumed a specific format." It does not mention the soft verifier or the substring check. Hence TB2.1 fixed the auth contradiction (PR #39 at https://github.com/harbor-framework/terminal-bench-2/pull/39: "Verifier now sets up its own SSH key auth") but not O1/O2; issue #133 filed 2026-07-14 is the follow-up.
- **Z.ai `zai-org/terminal-bench-2-verified`**, https://huggingface.co/datasets/zai-org/terminal-bench-2-verified (dataset card). Quote: "Instruction Fixes (11 tasks)"; its grading-fix list (dna-insert, make-doom-for-mips, filter-js-from-html, install-windows-3.11) and 11-task instruction table do not include configure-git-webserver.
- **JonathanGabor audit** (above): LLM audit of all TB2 tasks; rates this one 4/5 with weaknesses 1 and 3 naming O2 and "pre-populate content" (the O2 consequence).
- **TB2.1 issue #133 comment** by 202520030411, Sep 25 2026: false negatives from the same instruction sentence ("I'll setup login with the server to work"): solver did not create `user`, clone failed, curl 404. Evidence that this instruction/verifier pair also rejects honest solutions (a TB2.1-script observation, not tied to the pinned probe's cases).
- **BenchJack** arXiv 2605.12673 / Berkeley RDI: audits Terminal-Bench as a whole (100%, binary trojans), no per-task entry for this task.
- Other: Rohan Verma, https://rohanverma.net/pages/harness-engineering/research/pi-weaver/tasks/configure-git-webserver/ — a harness experiment page, no verifier critique (I read it; an earlier search-assistant claim that it says the task "only passes when a test file is left behind" is NOT supported by the page; that sentence appears to come from PR #37/#133 and the assistant misattributed it).
- TB2 repo issue search `configure-git-webserver` returns 2 PRs (#53, #39), no issue. TB2.1 repo search returns issue #133, PR #37, and 8 leaderboard PRs.

Receipt-observation coverage by prior art (what the receipt headline lists vs what I found):

| Receipt observation | Prior art |
|---|---|
| Static file on :8080, no git/hook/push → pass | published (issue #133, PR #37 matrix row, audit weakness 1) |
| verify.sh never reads the expect step status | published for the TB2.1 script as "no `set -e`"; expect-specific wording only in the audit |
| Body containing `TEST PASSED` passes though verify.sh prints `TEST FAILED` | not found |
| Status and content from two separate requests | not found (the scripts are quoted in #133 but the two-request gap is not discussed) |
| curl without -L and without timeout | not found |
| Trailing newline stripped, other whitespace/case/CR/BOM not | not found |

## Residual gaps (what I did not do)

- I did not clone or diff PR #37; its post-patch verify.sh echo behaviour is inferred.
- I did not read the BenchJack appendices (only grep hits) or the 361-line RDI blog past line 300.
- I did not search arXiv full text beyond the cited hits; a broader literature sweep (e.g. "Agentic Benchmark Checklist", Zhu et al., cited in BenchJack §2) was not fetched.
- Dates: sources show 2026 dates relative to fetch date 2026-10-26; no source was newer than 2026-10-25.

## Counts

Hits fetched and located: SWE-bench #601, SWE-bench #667, env-r2e-gym #11 finding, RHP-06, RHP-07, BenchJack arXiv 2605.12673, Berkeley RDI blog, TB2 paper 2601.11868, TB2.1 news, TB2 PR #53, TB2 PR #39, TB2.1 issue #133, TB2.1 PR #37, JonathanGabor audit, Z.ai verified card, Rohan Verma page = 16 hits; 6 are about O1's class, 3 about O2 for this task, 10 touch O3. Hits that name the O1 instance: 0.

VERDICT: priorart-16-hits-token-injection-published
