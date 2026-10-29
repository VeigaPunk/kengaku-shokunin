# C1ScoutSrcTB2 — search log (CORPUS.md rule 5)

Date: 2026-10-28. Seat: C1ScoutSrcTB2 (source scout, R53-C1 prior-art leg, kengaku round 53 wave 1).
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin.

**Question.** Which primary Terminal-Bench 2.0 / 2.1 material NOT yet rowed in `corpus/SOURCES.md`
(registry S001–S193; S191–S193 rejected) names concrete graders weakened or strengthened — repo README
sections, task docs, release notes, or pull requests editing specific `tests/test_outputs.py` files at
the pinned revision 2fd12b88 or a later one — especially evidence bearing on "tests that pass if the
named artefact merely exists" (the frozen presence-only definition, `.ufo/waves/round-53/p1-spec.md`)?

**Where searched.** GitHub REST API v3 only (curl); no search engine was needed because both primary
repositories' trackers are the authoritative record of grader changes:

- `repos/harbor-framework/terminal-bench-2-1`: `pulls?state=all` (3 pages), `issues?state=all`
  (3 pages, items #247→#1 complete), `issues/<n>` for 9 numbers, `pulls/<n>` for 5 numbers,
  `pulls/<n>.diff` for 5 numbers, `issues/<n>/comments` for 3 numbers, `releases` (empty).
- `repos/harbor-framework/terminal-bench-2`: `search/issues?q=repo:…+grader+OR+test_outputs+OR+verifier+in:title`
  (10 hits), `issues/67`.

**Population check.** Every candidate's task name was verified present in the frozen 88-task index
`corpus/evidence/round53/tests-index.json` (89 pin tasks minus the operator-excluded sanitize-git-repo).

## Counts

| sweep | identified | screened | included | excluded |
|---|---|---|---|---|
| A: TB2.1 pull requests (137 enumerated via pulls API, #247→#1) | 137 | 26 non-leaderboard task/verifier-touching PRs (5 opened, 21 title) | 2 (PR #234 → S945, PR #235 → S946) | 24 (detail below) |
| B: TB2.1 issues (31 enumerated via issues API, #247→#1 complete) | 31 | 31 (8 opened, 22 title, 1 already rowed) | 3 (#242 → S941, #237 → S943, #185 → S944) | 28 (detail below) |
| C: TB2.0 repo title search + #67 | 10 | 10 (1 opened, 9 title) | 1 (#67 → S942) | 9 |
| D: TB2.1 releases | 0 | 0 | 0 | 0 |
| **total** | **178** | **67** | **6** | **61** + 111 leaderboard-submission items screened out by title |

## Included (6, draft rows S941–S946)

#242 modernize-scientific-stack (dependency file only checked to exist), #67 make-doom-for-mips
(fake frame copied from the verifier's own reference image), #237 git-multibranch (pre-staged static
files pass), #185 custom-memory-heap-crash + polyglot-rust-c (stale binaries re-run), PR #234
make-doom-for-mips (existence-poll fix diff), PR #235 schemelike-metacircular-eval (no-op interpreter
fix diff). All six bear on presence-only passes — see draft-rows.md bearing table.

## Excluded, opened (8, draft rejection rows S947–S954)

- #161 — duplicate phenomenon/task of kept S945 (original report; the PR carries the diff).
- #135 — same task as kept S946, different gaming route (eval.scm path special-case).
- #239 sanitize-git-repo — false-fail class (thorough solution cannot pass); capture-excluded task.
- #243 nginx-request-logging — unchecked requirements over config content; not an existence pass.
- PR #37 configure-git-webserver — same defect already registered as S114 (issue #133).
- PR #236 custom-memory-heap-crash — exit-status/leak-classification shortcut; not existence.
- PR #241 adaptive-rejection-sampler — output-format substring oracle; verifier-CI kept as a lead.
- #154 caffe-cifar-10 — verifier trusts agent-controlled data; content, not existence, defeats it.

## Excluded, title-screened (no row; a row is a claim made after opening — CORPUS rule 1)

- TB2.1 issues: #246 (asset URL 404), #240 (unpinned upstream suite, false-fail), #238 (instruction
  omission, false-fail), #233 (verifier bootstrap broke, environment), #232 (leaderboard meta),
  #229/#228 (secret/leak exposure class), #215/#179/#177 (submission process, CI, traces availability),
  #214/#195 (qemu environment failures), #213 (network hardening), #194/#156/#11/#9 (instruction/
  parser mismatch, false-fail), #192 (withdrawn), #107 (harness execution failure), #100 (grader
  hard-codes one insertion site — false-fail), #10 (task enhancement), #133 (already rowed S114).
- TB2.1 PRs: #247 (solution-side solve.sh), #224 (Python bump), #188/#187 (image builds), #155/#124/#121
  (static-analysis infra), #149 (verifier timeouts, harness), #109/#108 (leaderboard judge prompts),
  #71 (lead: cites the already-rowed ABA paper), #12 (pipeline port), #8 (tmux install), #7 (traceback
  suppression, leak class), #6/#5/#4/#2/#1 (prompt/verifier-stability fixes, false-fail or leak class),
  #3 db-wal-recovery (already rowed S121). Remaining ~111 PRs are leaderboard submissions (intake).
- TB2.0 title-search hits: #85/#45/#1-raman (unstated conventions, false-fail), #84/#86 (sanitize-git-repo
  crash, false-fail), #39 (configure-git-webserver auth — task rowed via S114), #46 (BeautifulSoup
  normalization, content), #26 (missing test.sh, packaging), #75 (oracle unpinned, false-fail),
  #80 (CUDA verifier env, closed).

## Stop rationale (rule 5)

Both trackers are enumerated to #1 (247 items; the issues API flags 216 as pull requests while the
pulls API returns 137 — discrepancy recorded below), the releases endpoint returned zero releases, and
every non-leaderboard item was either opened or title-screened with a recorded reason. Late candidates
were surfacing only as duplicates of already-kept phenomena (#161 of #234's, #135 of #235's), so the
sweep stopped at saturation rather than at a count quota. Negative claims above are bounded by these
enumerations; nothing outside the two repos and their APIs was claimed absent.

## Tool-behaviour note

- `github issues API`: items flagged `pull_request` (216) disagree with the pulls-API total (137) for
  the same repository; both listings were screened, so no candidate was missed either way.

No tools were installed or upgraded (curl/python3 present); no pacman transaction attempted.
