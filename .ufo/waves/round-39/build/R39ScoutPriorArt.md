# R39ScoutPriorArt — prior art for the `git-leak-recovery` grader findings (kengaku round 39, wave 1)

Seat: scout, leaf, read-only. All sources below were **opened** (fetched bytes, not search snippets) on 2026-10-26 via `gh api`, `git clone --depth 1` into
`/fast/scratch/hyaku/kengaku-r39/R39ScoutPriorArt/` (deleted at the end), or the `read` tool. Nothing in the lane was edited.
Baseline reused: `R38PlanNext.md` §2.5 (lines 126-135), whose URLs were "not opened"; this seat opened them.

## 0. Answer in one paragraph

No opened source reports this grader's permissiveness as the lane measured it (literal-only flag test; secret commit retained in reflog/object
store while all five tests pass; do-nothing passing 4 of 5 tests). One artifact **names and dismisses** the reflog gap (JonathanGabor audit, §2.D).
Task-level "do-nothing is rejected" is published three ways (TB docs, a TB-hosted fixture, two third-party validation runs) and is **consistent** with
the lane's receipt — the lane's `untouched` case is a per-test result (`FPPPP`), the whole-task reward is 0 in both. The `must score exactly 0.0`
quote R38 §2.5 attributed to TB was **not found** in any opened TB doc (§1.4); the contract wording found is "Doing nothing fails tests".
No tier-B SOURCES row qualifies (§4).

## 1. Terminal-Bench / Harbor nop validation (the "published class")

### 1.1 `docs/TASK_REVIEW_AUTOMATION.md` — OPENED
- URL: https://github.com/harbor-framework/terminal-bench/blob/main/docs/TASK_REVIEW_AUTOMATION.md (file last touched 2026-10-15, commit `2e29ca91d5f1`; `main` tip read = `e67a2cb7db4d`, 2026-10-23). State: live doc.
- Quote, line 244: "**Nop Validation** confirms doing nothing fails tests (task is non-trivial)." (11 words); table line 29: "Doing nothing fails tests".
- Reports this grader's permissiveness? **No.** It states the contract (nop must not pass). "fails tests" is the task-level verdict: TB's `test.sh` writes reward 1 only if pytest exits 0 (see the Marginlab capture of `git-leak-recovery/tests/test.sh`, `if [ $? -eq 0 ]; then echo 1 > /logs/verifier/reward.txt`).
  A nop that passes 4/5 and fails 1 is a **rejected** nop under this contract.

### 1.2 `scripts/checks/test-tasks/fail-validate-nop` — OPENED (R38 cited it as `checks/test-tasks/...`; real path has `scripts/`)
- URL: https://github.com/harbor-framework/terminal-bench/tree/main/scripts/checks/test-tasks/fail-validate-nop (dir last touched 2026-08-26, `d6e6f61a05`). README row: "`fail-validate-nop` | Nop agent passes (tests are broken)" (`scripts/checks/test-tasks/README.md:53`).
- Fixture contents: `tests/test_state.py` = `def test_always_passes(): assert True == True`; `instruction.md:3` "The test suite is intentionally designed to pass without any agent intervention, which means the nop validation step should flag this".
- Reports this grader's permissiveness? **No** — a synthetic always-true grader that exercises the nop gate; it says nothing of `git-leak-recovery`. It shows TB's nop gate is whole-task (all-tests) pass, not per-test.
- The pass/fail criterion of hosted validation is **not in the repo**: `.github/workflows/validate-task.yml` (63 lines) contains no `nop` string; it installs `harbor==$(< .github/harbor-version)` and "Launch hosted validation". [UNRESOLVED: criterion not read.]

### 1.3 `docs/REVIEWING.md`, `CONTRIBUTING.md`, `docs/prompts/task-implementation.toml` — OPENED
- `CONTRIBUTING.md:448-450`: "# Validation (oracle + nop)" … "harbor run -p tasks/your-task --agent nop". `REVIEWING.md:35`: "Execution checks (Docker build, oracle, nop) run on every push." Rubric toml: only unrelated "exactly 0 or 1" reward-binary criterion (line 514).

### 1.4 The "must score exactly 0.0" quote
`grep -n -i -E 'nop|exactly 0|do-nothing|do nothing'` over `TASK_REVIEW_AUTOMATION.md`, `REVIEWING.md`, `CONTRIBUTING.md`, `task-implementation.toml`: the only "exactly 0" hit is the binary-reward rubric line (not nop). **R38 §2.5's quote is unsupported by anything opened**; use §1.1's wording. (Also: that doc's scope is TB3/4 tasks under `tasks/`; TB2 `git-leak-recovery` predates it — it lives at `legacy/git-leak-recovery` and `archive/`.)

### 1.5 Adjacent TB issue #1192 — OPENED, not a hit
https://github.com/harbor-framework/terminal-bench/issues/1192 "check "do not modify" lines in tasks" — opened 2026-06-13, closed 2026-08-10. Do-not-modify enforcement sweep of TB3/4 tasks (`git-leak-recovery` appears nowhere in the 4026-byte comment). Matched only on semantic search. Not about this grader.

## 2. Issue / PR search (state=all) — `gh api -X GET search/issues` + full issue lists

Repos: `harbor-framework/{terminal-bench, terminal-bench-2, terminal-bench-2-1, harbor}` (`laude-institute/*` redirects to the same; `-2-1` has no laude copy).
Queries: `git-leak`, `git leak`, `leak recovery`, `reflog`, `dangling`, `fsck`, `git-leak-recovery`, `"git gc" "reflog expire"`, `nop agent passes tests per-test`, `verifier too permissive git`. Plus complete listings: TB2 `issues?state=all` = 89 rows (`tb2_issues.tsv`), TB2.1 = 247 rows, filtered on `git|leak|reflog|nop|fsck|secret|dangl`.

**Result: zero issues or PRs name `git-leak-recovery` as a defect.** The title/body hits for the string `git-leak-recovery` are leaderboard-submission PRs and reproducibility PRs that list it among 89 tasks:
| hit | URL | date / state | what it is |
|---|---|---|---|
| TB2.1 PR #146 "Leaderboard Submission: Grok 4.5 (medium) + Ouroboros" | https://github.com/harbor-framework/terminal-bench-2-1/pull/146 | 2026-07-16, closed | result listing; no grader finding |
| TB PR #1584 `fix pretrain-shard-corruption` | …/terminal-bench/pull/1584 | 2026-08-12, closed | matched `reflog` in an unrelated task |
| TB PR #934 `Add Task: ext4-forensic-recovery` | …/terminal-bench/pull/934 | 2026-05-28, closed | matched `fsck`; different task |

**Adjacent (same task family, different task):**
- TB2.1 issue #239 — https://github.com/harbor-framework/terminal-bench-2-1/issues/239 — 2026-09-25, open — "sanitize-git-repo: verifier diffs against a hard-coded commit SHA, so removing the secrets from history (which the instruction asks for) makes the verifier error out" (title, 29 words → quote the first 17: "sanitize-git-repo: verifier diffs against a hard-coded commit SHA"). Same TB2 "git history + secret" family; a *crash* on correct cleanup, not a permissive pass.
- TB2 issues #84 (2026-09-28, open, "verifier crashes with GitPython ValueError when the agent rewrites git history to remove the secrets") and #86 (fix PR for the same). Same class as #239.
- TB2.1 issue #134 — https://github.com/harbor-framework/terminal-bench-2-1/issues/134 — 2026-07-14, open — "fix-code-vulnerability: leftover git HEAD still contains the oracle fix" (title). Setup-leak, not a grader permissiveness finding.
- TB issue #2086 "Vectors and mitigations for reward hacking during verification" (https://github.com/harbor-framework/terminal-bench/issues/2086, 2026-09-23, open, 54 885 chars): grep for `git leak|reflog|fsck|dangling|\.git` → only "dangling symlink" (artifact collection). No git-history grader content.
- TB2 PR #53 "Terminal-Bench 2.1" (2026-03-11, open, the diff-demonstration PR): 26 tasks changed; file listing contains **no** `git-leak-recovery` path. Consistent with the byte-identity below.

**Grader unchanged upstream:** `tests/test_outputs.py` for `git-leak-recovery` in TB2 @ `2fd12b88aa…` (`git-leak-recovery/tests/test_outputs.py`), TB2.1 `main` (`tasks/git-leak-recovery/tests/test_outputs.py`, commits `320a8be8b6` 2026-05-05, `5fc7d3b91d` 2026-05-05), and the HF fork `harithoppil/terminal-bench-2-verified` are byte-identical to the lane capture:
`sha256 dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775` for all four (`sha256sum` of the lane capture, the pinned fetch, the 2.1 fetch and the fork's file — one hash). `instruction.md` also identical TB2 vs 2.1 (`diff` empty, sha256 `54ac693f…`). So no upstream maintainer or fork has fixed or flagged the grader.

## 3. Third-party audits / write-ups

### D. JonathanGabor/terminal-bench-2-audit — the only entry that touches the reflog dimension — OPENED
- Repo https://github.com/JonathanGabor/terminal-bench-2-audit @ `35f110397bc8ea58538424a1951760a9c5a0a710` (2026-01-23). Entry: `audit_results/20260120_125158/audit.txt:1450-1500` (rating 4, `ratings.json`); method (README): an LLM rates each challenge's test coverage 1-5 from the task, container state and reference solution — **LLM prose, not a reproduction**. Background post cited by the README: https://jonathanpgabor.substack.com/p/every-benchmark-is-broken (not opened).
- Quote, `audit.txt:1485` (under "## Potential Gaps:"): "Doesn't explicitly check `git reflog` entries (though fsck should catch objects if they become dangling after cleanup)" (17 words).
- Also `audit.txt` "Strengths": "The fsck-based check for dangling objects is quite thorough for this type of task" (14 words).
- Reports this grader's permissiveness? **Partially names the reflog gap, then dismisses it.** It does not report the literal-only flag test, the nop 4/5, or that `git gc --prune=now` without a reflog expire leaves the secret commit in place; its dismissal ("fsck should catch…") is contradicted by the lane's probed cases `echo-gc-only` and `echo-reflog-expire` (tests `PPPPP`, receipt `git-leak-probe.txt:9-10`). A `challenges/git-leak-recovery/` dir is a copy of the task (compose.yaml, eval.yaml, tests); no further analysis.

### E. kimjune01/terminal-bench-audit — nearest *reproducible* report, but not this finding — OPENED
- https://github.com/kimjune01/terminal-bench-audit @ `bbe0f8c39fc291e3c3eb20bb0dc47c1c861d5d23` (2026-07-20; Zenodo doi 10.5281/zenodo.21463236 per its README). TB2.1 frame-validity audit with pinned image digests (`sha256:62160e52…` for this task).
- `results/verdicts-2.1.jsonl` lines 161-165 for `git-leak-recovery`: `baseline` reward 1 `gold_pass`; `nuke-git` reward 0 `caught`; `nuke-preexisting` reward 0 `caught`; `reset-hard` reward 1 `FRAME_BLIND`; `wipe-sentinel` reward 1 `FRAME_BLIND`.
- Reports this grader's permissiveness? **Something else**: collateral-damage blindness (what the grader ignores after a *correct* solution), not "an incomplete cleanup passes". Two cautions: (1) `wipe-sentinel` deletes `~/.tbaudit-user-assets`, which no grader reads — true for 83/83 tasks, not specific; (2) `harness/mutations.sh:11` runs `set -e; … git reset --hard HEAD~3` and applicability (`mutation_applicable`, lines 25-26) only requires a `.git` dir, while `DESIGN.md:85` says "≥3 commits"; this repo has ≤2-3 commits (Kilo post: "two commits"), so the reset may have **failed and changed nothing** and the reward-1 verdict be vacuous. [INFERENCE — not run; `harness/regrade.sh` needs docker + the pinned image.] Do not cite as a finding about this grader's test coverage.
- Also notes `nuke-git` is **caught** here (the `chore: init` test and the checksum), a sensitivity control — not evidence for or against the lane's findings.

### F. Task-level nop validation by third parties — corroborate the whole-task reward, say nothing of per-test
- Evan-Kim2028/task_validation — https://github.com/Evan-Kim2028/task_validation @ `7fd6346ec799d235867a574412b4fa5be593c0ce` (2026-09-15), `data/gold/tb21_census_verdicts.jsonl:33`: `{"unit_id": "git-leak-recovery", "invalid": false, … "grade": "A", "evidence": "reference pass, nop reject", "adjudicator": "machine"}`. Quote: "reference pass, nop reject" (4 words).
- laion/terminal-bench-2-1-apptainer-v1 — https://huggingface.co/datasets/laion/terminal-bench-2-1-apptainer-v1 (created 2026-09-25), README.md:107 table row `git-leak-recovery | validated | 2/2 | 0` with line 22 "gold solution passes in 2/2 offline oracle runs, and an empty attempt scores 0" (16 words) and line 39 "empty-solution control (harbor `nop` agent)".
- Verdict: both match the lane's receipt at task level (`untouched` `FPPPP` ⇒ reward 0). **The R38 §2.5 snippet "1 of 5 passing" at no-op was not found in any opened page**; the only thing that says "1 of 5" is the reverse of what this receipt shows (the lane's nop is **4 of 5** passing). Leave it out of the entry.

### G. Other opened pages — no grader finding
- Kilo blog "We Asked Grok Build 0.1 to Recover a Secret Hidden in Git History" (2026-06-10, https://blog.kilo.ai/p/we-asked-grok-build-01-to-recover): a walkthrough of one passing run. Closest content: "Expiring the reflog had not been enough on its own" (10 words) and "The three objects were still there" — an agent observing that the reflog expiry alone leaves the objects (it then ran `git gc --prune=now`). That observation is about the **solution**, not the grader; the blog never says the grader would accept the incomplete state. In this blog's repo state the hard-reset commit was dangling after the reflog expire — i.e. the object store retains the secret (same retention the lane probes), but there the dangling commit would fail test 4.
- Marginlab explorer https://marginlab.ai/explorers/terminal-bench/git-leak-recovery/ (opened): mirror of task + tests + solve.sh; no commentary. Test text matches the capture.
- `web_search` AI-synthesis answers (not primary; no URL I could open carries the claim): one asserted "the published Terminal-Bench `git-leak-recovery` grader has a **weak-verifier** gap … a reflog blind spot and a dangling-versus-unreachable blind spot", citing only the Harbor hub task page and the `legacy/` dir (the sources are the task itself, not a report). Treat as the "search-engine prose" R38 saw; it is derived from reading the same test, not an upstream or third-party finding. It also (separately) says it could not verify any "1 of 5" nop claim — matches §F.
- Skills/marketplace pages (Letta `git-leak-recovery` skill, mcpmarket) describe reflog/gc cleanup steps for agents; not grader findings.

## 4. SOURCES row proposal

**None qualifies as tier B for "prior report of this grader's permissiveness".**
- The only source naming the reflog gap (§3.D) is LLM output, non-reproduced, and dismisses the gap: it is tier C (lead) at best and cannot be sole support (SOURCES contract: "C — lead only").
- §3.E is a reproducible audit (would be tier B) but it reports a different class and its `reset-hard` row may be vacuous on this repo (§3.E caution 2).
- §3.F corroborates only the task-level nop reject; the lane's claim is per-test, so it contradicts nothing and does not report permissiveness.
- Optional for wording the entry's limit (not a prior-art row): the entry may cite `docs/TASK_REVIEW_AUTOMATION.md:244` as a **tier-A maintainer statement of the validation contract** ("Nop Validation confirms doing nothing fails tests (task is non-trivial)", 11 words, opened 2026-10-26, https://github.com/harbor-framework/terminal-bench/blob/main/docs/TASK_REVIEW_AUTOMATION.md). S117/S118 are reserved for the grader and instruction, so the next free id is S119. This is the main agent's call; it is not "prior art for the finding".

## 5. Wording the entry should use (replaces R38 §2.5 / claims-file "Limits" sentence)
- "Task-level nop rejection is TB's own validation contract (`TASK_REVIEW_AUTOMATION.md:244`) and holds for `git-leak-recovery` in two third-party validation runs (`nop reject`; empty-attempt reward 0). The lane's observation is finer: the do-nothing run passes four of five tests and fails only the flag test; writing the literal alone passes all five while the secret commit stays in reflog/object store (`echo-only`, `echo-gc-only`, `echo-reflog-expire`)."
- "No upstream issue/PR in `terminal-bench-2`, `terminal-bench-2-1`, `terminal-bench` or `harbor` reports this; one LLM audit (JonathanGabor, `audit.txt:1485`) names the reflog gap and dismisses it. The grader is byte-identical in TB2 @ `2fd12b88aa`, TB2.1 `main` and the `harithoppil/terminal-bench-2-verified` fork (sha256 `dc7b01c1…`)."
- Do NOT write: "TB requires nop to score exactly 0.0" (not found); "third-party repo reports 1 of 5 at no-op" (not found).

## 6. Limits
- GitHub search covers only the four repos above; third-party forks (`jarvishappy`, `audreycs`, `kyuz0`, `varunisrani`) hold copies of the task, none opened for commentary. HF leaderboard trial logs that include this task (`terminal-bench-2-leaderboard`, LemonHarness etc.) not opened.
- The Substack post behind the Gabor repo and TB docs on tbench.ai were not opened.
- No command here executed the grader or the probe; the lane's receipt lines are quoted from `corpus/evidence/round39/git-leak-probe.txt` (lines 6, 8, 9, 10).
- `gh search issues` returns `[]` for `terminal-bench-2` where the REST `search/issues -X GET` finds PR #53; relied on the REST output and full issue listings.

## 7. Receipts (commands run, abridged outputs)
- `gh issue view 1192 -R harbor-framework/terminal-bench --json …` → state CLOSED, comment body 4026 B, no `git-leak` match.
- `gh api repos/harbor-framework/terminal-bench/contents/docs/TASK_REVIEW_AUTOMATION.md | base64 -d | grep -n -i nop` → lines 27-29, 40, 242, 244, 332.
- `gh api repos/harbor-framework/terminal-bench-2/git/trees/main?recursive=1 | grep git-leak` → `git-leak-recovery/{tests/test_outputs.py,…}`; same for `-2-1` under `tasks/`.
- `sha256sum` of lane capture, TB2 pinned, TB2.1 main, harithoppil fork → one hash `dc7b01c1…c5`; `diff i2.md i21.md` empty.
- `grep -n git-leak …/verdicts-2.1.jsonl` → lines 161-165 (see §3.E); `sed -n 1484,1485p …/audit.txt` → the quoted lines.
- laion `README.md` lines 22, 39, 107 (sha256 `f93d6af0…`); Evan `tb21_census_verdicts.jsonl:33`.
- Scratch `/fast/scratch/hyaku/kengaku-r39/R39ScoutPriorArt` removed at the end; no tools installed.

VERDICT: prior-art-1-hits-row-no
