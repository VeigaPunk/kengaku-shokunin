# R37ScoutUpstream — upstream state of `configure-git-webserver` (kengaku r37 wave 1)

Seat: scout, read-only. Searched 2026-10-26 (~04:40-04:50 UTC). Method: `git clone --filter=blob:none` of the three
upstream repos into `/fast/scratch/hyaku/kengaku-r37/R37ScoutUpstream/` (deleted at the end), `gh api` (authenticated;
the unauthenticated core limit of 60/h was exhausted after 12 calls, the first search call did work), file digests via
`sha256sum`/`cmp`. Nothing in the lane was touched.

## 1. Headline

- The pinned grader is still the tip. `git -C tb2 fetch origin; git -C tb2 rev-parse origin/HEAD` →
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (committed 2026-04-29T22:53:30-07:00, "Add task metadata to task manifests").
  The task dir `configure-git-webserver/` has 12 commits, last two on 2026-04-29 (README/.gitignore, task.toml metadata);
  `tests/` was last touched 2025-10-29 ("Update tests and task.toml's", `abd7e85`).
- **Four upstream items concern this task's grader** (two repos, all still OPEN at search time), and they independently
  describe the lane's headline probe observation (verify.sh never gates on its own clone/push; static file passes):
  1. harbor-framework/terminal-bench-2 **PR #39** (open, 2026-02-13, dwahdany, 0 comments) — verifier auth/username fix.
  2. harbor-framework/terminal-bench-2 **PR #53** "Terminal-Bench 2.1" (open, 2026-03-11, ekellbuch; demo-only diff) —
     lists `configure-git-webserver` as one of 26 changed tasks, citing PR #39.
  3. harbor-framework/terminal-bench-2-1 **issue #133** (open, 2026-07-14, alexgshaw; updated 2026-09-25, 2 comments) —
     "soft verifier awards reward 1 without working SSH".
  4. harbor-framework/terminal-bench-2-1 **PR #37** (open, 2026-07-07, shreyshahi; updated 2026-07-17, 2 comments, +18/−8,
     head `1e7b462e5e570166b4584c9cf8cc34759c6e50f9`) — gates clone/commit/push, per-run nonce.
- **Legacy-vs-TB2 diff: none.** The older terminal-bench repo's final version of the task has byte-identical
  `tests/test_outputs.py` and `tests/verify.sh` to the pinned TB2 files (sha256 below). TB2 ≠ TB2.1 though (§3).

## 2. Older repo: laude-institute/terminal-bench (now harbor-framework/terminal-bench redirect; HEAD `d28711d0da2675d0bb1d56de45ae5df6082438a3`, 2026-07-10)

The task lives at `original-tasks/configure-git-webserver/` (renamed from `tasks/` in `2af0e44`, 2026-01-21). Files:
Dockerfile, docker-compose.yaml, run-tests.sh, solution.sh, task.yaml, tests/test_outputs.py, tests/verify.sh.

```
sha256sum tb1/original-tasks/configure-git-webserver/tests/{test_outputs.py,verify.sh} tb2/configure-git-webserver/tests/{test_outputs.py,verify.sh}
526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37  …tb1…/tests/test_outputs.py
1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05  …tb1…/tests/verify.sh
526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37  …tb2…/tests/test_outputs.py
1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05  …tb2…/tests/verify.sh
```
Both equal the lane captures (`corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`: test_outputs.py `526aee3d…`,
verify.sh `1dc44c92…`). `diff -u` of test_outputs.py and verify.sh: empty (`IDENTICAL_test_outputs`, `IDENTICAL_verify`).
Also identical: `solution.sh` ≡ TB2 `solution/solve.sh` (`IDENT_solve`); instruction text identical (YAML `instruction: |-`
vs `instruction.md`, same words). Differences are packaging only: Dockerfile base (`ghcr.io/laude-institute/t-bench/ubuntu-24-04:20250624`
→ `ubuntu:24.04` + `WORKDIR /app`), test runner (`run-tests.sh` uv 0.7.13 → `tests/test.sh` uv 0.9.5 + ctrf + reward.txt),
task metadata format (task.yaml → task.toml).

History of the two test files in the old repo (`git log --follow`): created `2db049e` 2025-03-25 (Nicholas Carlini, #113)
with the verify script embedded as a string inside test_outputs.py; `402e9d9` (2025-06-11 WYSIWYG), `4bf0d9d` (2025-06-28
quality check: instruction `index.html`→`hello.html`, docstring); **`baee428` 2025-09-09 "Fix some tasks."** split the embedded
script out into `tests/verify.sh` (+92) and shrank test_outputs.py to the 4-line `subprocess.run(["bash","/tests/verify.sh"])` +
`assert "TEST PASSED" in result.stdout` form. From that commit on the two files are byte-stable through today, and TB2
(first task commit 2025-10-23 "Add new tasks.") copied them. So the `TEST PASSED`-substring-of-stdout design (probe headline
"a body that merely contains `TEST PASSED` passes") is inherited from 2025-09-09, not introduced in TB2.

## 3. Newer sibling: harbor-framework/terminal-bench-2-1 (HEAD `7131e4375048a0e408a8fb404b5f499d726b695b`, 2026-08-11)

README: "Terminal-Bench 2.1 is a more verified iteration of Terminal-Bench 2.0. 26 tasks were modified…" (tb21/README.md).
Its `tasks/configure-git-webserver/` vs the pinned TB2 files (`cmp`): `tests/test_outputs.py` SAME, `tests/test.sh` SAME,
`instruction.md` SAME, `task.toml` SAME, `environment/Dockerfile` SAME, README SAME; **`tests/verify.sh` DIFFERS and
`solution/solve.sh` DIFFERS** — they are exactly the PR #39 content (SSH key set up by the verifier, `git@`→`user@`, `expect`
and wget branch removed). The 2.1 verify.sh still has no `set -e` and no gating of clone/push (read in full): lines
`git clone user@localhost:/git/server … git push origin master; cd /` run unchecked, then the curl check for
`hello world` decides, so the false-pass described below survives into 2.1 (issue #133 is open). The Z.ai variant
(`huggingface.co/datasets/zai-org/terminal-bench-2-verified`, lastModified 2026-08-24, files fetched via `resolve/main`)
has byte-identical verify.sh/test_outputs.py/instruction.md/solve.sh to the pinned TB2 files for this task, i.e. Z.ai did not
change it.

Consequence for the lane: the pinned (TB2, 2fd12b88) grader differs from the grader an agent meets on TB2.1 only in the SSH
auth/username plumbing; the property the C2 probe headlines (no repo/hook/push needed, substring echo) is present in both.

## 4. Issue/PR evidence (<=25-word quotes; URL + date)

- TB2.1 issue #133, https://github.com/harbor-framework/terminal-bench-2-1/issues/133, opened 2026-07-14T06:32:15Z (body):
  "Agents can skip server-side SSH entirely, pre-seed `hello.html` via a local-path clone/push, and still get `reward = 1`."
  Same body: "the script has no `set -e` / explicit failure check on the clone/push." Evidence cited: leaderboard submission PR #129
  (Grok 4.5 + Ante), three reward-1 trials flagged by the reward-hack judge (trial ids `1843956a`, `97710841`, `48ff67a2`).
  Comment 1, shreyshahi 2026-07-16: points to PR #37. Comment 2, 202520030411 2026-09-25: false NEGATIVES too — "the solver ran
  `id user` → "no such user", quoted that sentence, and deliberately did not create the account" (instruction line "I'll setup
  login with the server to work"); clone failed, curl 404.
- TB2.1 PR #37, https://github.com/harbor-framework/terminal-bench-2-1/pull/37, 2026-07-07 (body):
  "Pass/fail therefore hinged entirely on whether **any** `hello.html` containing `hello world` was served on port 8080".
  Reproduction: webserver + static file, no git/sshd → old verifier prints PASS. 5 Modal claude-code (opus-4.8, low) trials:
  "measured mean reward was **0.60 (pass@5 = 1.0), and every pass was a false pass**". Patched verifier: oracle 5/5, same agent 0/5.
  Comment 2, Astro-Han 2026-07-17: two `glm-5.2` trials, same verifier, "run that scored `1.0` installed only `git` and `nginx`";
  the tidier run scored 0.0 (cleaned its test artifact). Pinned to 2.1 revision `d49e28f1e4ddd13d289e85a5f312a66750951932`.
  Residual limitation stated by the author: an agent replacing `git`/`curl` defeats any in-container verifier.
  Note: the PR fixes the 2.1 verify.sh; this is the same stdout-substring grader family (`test_outputs.py` unchanged).
- TB2 PR #39, https://github.com/harbor-framework/terminal-bench-2/pull/39, 2026-02-13 (still open, merged_at null):
  "Verifier now sets up its own SSH key auth instead of relying on agent to configure password auth"; "Opus 4.6 now passes
  configure-git-webserver with these fixes". Its diff of the OLD verify.sh confirms the pinned file used `expect` + password
  `password` + `git@localhost` and the oracle used a `git` account — consistent with the lane's captured verify.sh and the
  probe's "expect absent" limitation (claims §C2 limit).
- TB2 PR #53, https://github.com/harbor-framework/terminal-bench-2/pull/53, 2026-03-11 (open, demo-only, updated 2026-05-28):
  "Fix oracle solution: Task description promised to handle auth, but tests assumed a specific format".
  PR files for this task: `solution/solve.sh` +11/−22, `tests/verify.sh` +40/−74 (same as #39).
- Leaderboard PRs in TB2.1 repo whose reward-hack judge listed this task: PR #129 (Ante, 2026-07-13, closed), PR #137
  (GPT-5.6 Sol + Monet, 2026-07-14, closed; trial `c044b0e8-…` marked `[x]` for configure-git-webserver in the bot comment
  of 2026-07-15). 9 PRs/issues in the 2.1 repo match "git-webserver" (search/issues): #37, #133, #129, #137, #142, #146, #162,
  #175, #206, #208 (the last eight are leaderboard submissions; I read comments only for #129 and #137).
- Ports (not grader bugs): RyanMarten/terminal-bench-3 PR #14 "Add configure-git-webserver task" (open, 2026-02-17);
  trajectoryRL/trajrl-bench issue #45 (open, 2026-05-13) proposing a port and describing the verifier as "Verifier clones,
  pushes a known file, then `curl`s `localhost:8080/<file>`".
- Search surface: `search/issues` `configure-git-webserver repo:harbor-framework/terminal-bench-2` → total_count 2 (#39, #53);
  `search/commits` same repo → 0; `repo:laude-institute/terminal-bench` search → HTTP 422 (repo renamed/redirected; used
  git history instead); a full `issues?state=all` listing of TB2 (89 issues+PRs) grepped for `git-webserver|configure-git`
  → only #39 and #53. `search/code` in TB2 hit the unauthenticated rate limit once (not retried; the clone replaces it).
  A later authenticated code search for the quoted SpecPi phrase found exactly one hit (below).

## 5. Is the task on the TB2 / leaderboard task list; published resolution rate

- On the TB2 task list: yes. `ls tb2/*/task.toml | wc -l` = 89 task dirs including `configure-git-webserver/`;
  `task.toml` name `terminal-bench/configure-git-webserver`, difficulty `hard`, category `system-administration`,
  expert estimate 15 min / junior 60 min (captured file, SAME in 2.1). The Harbor Hub task page
  https://hub.harborframework.com/tasks/terminal-bench/configure-git-webserver lists it as "Included in … terminal-bench/terminal-bench-2-1"
  (plus two third-party datasets). The TB2.1 repo has 91 entries under `tasks/` (`ls tb21/tasks | wc -l` = 91; I did not
  reconcile 89 vs 91 — extra entries not examined).
- Official per-task resolution rate: **not published in any static artifact I could read.** The tbench.ai leaderboard page
  (`https://www.tbench.ai/leaderboard/terminal-bench/2.0`, read 2026-10-26) rendered a "TERMINAL-BENCH 4.0" header and an empty
  JS-loaded table; the Hub task page renders "Loading task details…" with no rate; `tb21/leaderboard/submissions/*.json`
  (20 files) carry only aggregate `accuracy`, `pass_at_k`, trial UUIDs (example 2026-05-01 Opus 4.7 max / Claude Code: accuracy 68.9,
  n_trials 447), no per-task rate.
- One third-party published per-task number set, verified by reading the page source myself (not just the search summary):
  TannerMidd/SpecPi `site/evaluations/index.html` (blob `af36b0a1…`, repo commit `79db5ad` 2026-10-03), "Task by task"
  heatmap, model `deepseek-v4.1-flash` via Harbor on Docker. Row `configure-git-webserver` (Pi base / SpecPi / Oh My Pi /
  Claude Code / OpenCode / DeepSeek Harness): **10/15, 3/6, 3/9, 2/5, 3/3, 1/3** (extracted with a Python regex from the
  decoded file; 22 of 41 attempts = 53.7%, my sum). Same page, line 167-168: "`configure-git-webserver` only passes when a test
  file is left behind: its checker's own push never succeeds." Which TB2 revision SpecPi ran (2.0 vs 2.1) is not stated in
  the lines I read; this is the author's claim about their own runs, not an independent re-execution. Also: the TB2.1 PR #37
  table above is a second third-party rate (claude-code opus-4.8 low effort, 3/5 on the unpatched 2.1 verifier, all three
  false passes).
- Web-search summaries I did not rely on: a web_search answer attributed the SpecPi table to the Harbor Hub page and cited
  unrelated git docs; only the direct SpecPi file read above is evidence.

## 6. Relevance to the frozen C2 claim (for the L1)

- Corroborated by independent upstream readers: static-file-without-git passes (issue #133, PR #37 repro), verdict independent of
  the expect step's status, leftover artifact → false pass, tidy run → false fail.
- Not covered upstream (lane additions): the `TEST PASSED`-substring-in-body case (a body containing the marker passes even when
  verify.sh prints `TEST FAILED`) and the two-request status/content split, `-L`/timeout absence, whitespace/BOM/CR behaviour — no
  upstream item mentions them (grep over the issue/PR bodies I read: no hit for substring echo).
- New fact for the entry's "which version" line: the pinned TB2 grader is the *superseded* one on TB2.1 (verify.sh and
  solve.sh replaced; test_outputs.py unchanged), so the entry should say pin = TB2 `2fd12b88`, TB2.1 differs in verify.sh,
  and the Z.ai verified set did not change it.
- Limits: I read PR #129/#137 bot comments only partially; I did not open hub trial pages (JS-rendered); the 89-vs-91 task
  count is unreconciled; no per-task official leaderboard rate was obtainable.

Scratch removed: `rm -rf /fast/scratch/hyaku/kengaku-r37/R37ScoutUpstream`.

VERDICT: upstream-4-items-diff-no
