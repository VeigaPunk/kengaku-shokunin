# C1ScoutSrcTB2 — source scout report (R53-C1 prior-art leg, wave 1)

Date: 2026-10-28. Seat: `C1ScoutSrcTB2`, kengaku round 53 wave 1, lane `kengaku-shokunin`.
Assignment: find primary Terminal-Bench 2.0/2.1 material the lane has NOT rowed (`corpus/SOURCES.md`,
S001–S193) that names concrete graders weakened or strengthened; keep ≤ 6 with archived bytes, draft
registry rows, and a search log.

## What I did

1. Read the frozen claims (`plans/round-53-claims.md`), the presence-only definition
   (`.ufo/waves/round-53/p1-spec.md`), `CORPUS.md` (SOURCES contract v1, rules 1/5/6) and the full
   `corpus/SOURCES.md` registry + search log, so no already-rowed URL was re-rowed.
2. Enumerated the two primary repositories' trackers via the GitHub REST API (curl):
   - `harbor-framework/terminal-bench-2-1`: all 247 tracker items (#247→#1: 216 PR-flagged by the
     issues API, 137 returned by the pulls API over 3 pages, 31 issues), releases (zero),
     9 issue bodies, 5 PR bodies + 5 `.diff` files, 3 comment threads.
   - `harbor-framework/terminal-bench-2`: title search `grader OR test_outputs OR verifier in:title`
     (10 hits), issue #67 opened.
3. Verified every candidate task name against the frozen 88-task index
   `corpus/evidence/round53/tests-index.json` (all kept-source tasks are in the population).
4. Archived every opened body and diff under `fetched/`, hashed them, and byte-verified all 16 row
   quotes verbatim with archive line numbers.

## Commands (exact)

```sh
curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls?state=all\&per_page=100\&page=N   # N=1..3
curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues?state=all\&per_page=100\&page=N  # N=1..3
curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/<n>          # n in {9,10,11,100,107,133,134,135,154,161,185,192,215,214,237,238,239,242,243,246}
curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/<n>           # n in {37,234,235,236,241}
curl -sL https://github.com/harbor-framework/terminal-bench-2-1/pull/<n>.diff                # n in {37,234,235,236,241}
curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2-1/releases?per_page=20
curl -s "https://api.github.com/search/issues?q=repo:harbor-framework/terminal-bench-2+grader+OR+test_outputs+OR+verifier+in:title&per_page=50"
curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/67
```

## Measured numbers

- Tracker identified/screened/included/excluded: 178 / 67 / 6 / 61 (+111 leaderboard submissions
  screened by title) — see `search-log.md` for the per-sweep table and every exclusion reason.
- Kept sources: 6, all distinct URLs, none present in `corpus/SOURCES.md` (grep over the registry
  returned no matches for any of the 14 candidate URLs).
- Archives: 19 files, each ≤ 7.7 KiB (limit 1 MiB), all listed in `fetched/SHA256SUMS`.
- Quotes: 16 of 16 verified byte-verbatim inside my archived bytes, ≤ 25 words each, with line numbers.

## Kept sources and presence-only bearing (all six: yes)

| draft row | source | task(s) | why it bears |
|---|---|---|---|
| S941 | TB2.1 issue #242 | modernize-scientific-stack | `test_dependency_file_exists` asserts only `Path(f).exists()` and never opens the file — "touch requirements.txt plus a script with two hardcoded print() calls passes" (body line 3) |
| S942 | TB2-repo issue #67 | make-doom-for-mips | frame tests pass on `/tmp/frame.bmp` byte-copied from the verifier's own reference image — the artefact merely existing is the pass (body line 4) |
| S943 | TB2.1 issue #237 | git-multibranch | "An SSH Git server with **no hook**, plus two pre-written static files, passes" (body line 4) — pre-staged artefacts satisfy the deployment check |
| S944 | TB2.1 issue #185 | custom-memory-heap-crash, polyglot-rust-c | "the test runs the stale binary" (body line 47) — a verifier sharing the agent filesystem grades a leftover artefact, generalised to every in-place build/execute |
| S945 | TB2.1 PR #234 (diff) | make-doom-for-mips | grader "poll[s] for the existence of `/tmp/frame.bmp`" (body line 3) and "the two frame tests happily pass on the old frame" (line 6); diff adds `frame_path.unlink(missing_ok=True)` at base 7131e437 |
| S946 | TB2.1 PR #235 (diff) | schemelike-metacircular-eval | "Replacing it with an empty script makes a trivial `eval.scm` pass all 63 programs" (body line 1); a missing evaluator also passed 1 program (line 12); diff rewrites both grader copies at base 7131e437 |

Novelty note for the L1: all six name tasks absent from registry rows S079–S193 (the previously rowed
TB2 tasks were protein-assembly, regex-log, configure-git-webserver, build-pmars, git-leak-recovery,
db-wal-recovery, constraints-scheduling, circuit-fibsqrt, both feal tasks, password-recovery,
polyglot-c-py, bn-fit-modify, pytorch-model-recovery, torch-tensor-parallelism). configure-git-webserver
was deliberately NOT re-rowed (PR #37 rejected as S951: same defect already registered as S114).

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcTB2/draft-rows.md`
  — 14 draft rows in the exact 11-column schema: keeps S941–S946 (status `queued`), rejections
  S947–S954 (status `rejected`, `REJECTED: <reason>; flip: <condition>` in `teaches`), plus the
  bearing table. Placeholder ids, `opened` 2026-10-28, `used-by` `—`.
- `.../C1ScoutSrcTB2/search-log.md` — question, where searched, counts, exclusion reasons, stop
  rationale (CORPUS rule 5).
- `.../C1ScoutSrcTB2/fetched/` — 19 archived files + `SHA256SUMS` (sha256, one line per file):
  `tb2-issue-067-body.md`, `tb21-issue-{135,154,161,185,237,239,242,243}-body.md`,
  `tb21-pr-{037,234,235,236,241}-body.md`, `tb21-pr-{037,234,235,236,241}.diff`.
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcTB2.md`.

## Blindness, tooling and discipline notes

- Blindness rules respected: this seat never read `plans/round53_c1_classify.py`, any
  `C1Label*` file or directory, `oracle-labels.json`, or any other seat's wave-1 output. The only
  round-53 artifacts read are the frozen claims, `p1-spec.md` (the shared definition) and
  `tests-index.json` (a frozen pin artifact named by the spec).
- No tools installed or upgraded (curl/python3 already present); no pacman transaction attempted.
- Tool-behaviour inconsistency observed: the GitHub issues API flags 216 of 247 tracker items as
  `pull_request` while the pulls API returns 137 over 3 pages; both listings were screened so no
  candidate was missed — `github issues API: pull_request flag count (216) disagrees with pulls API
  total (137) for terminal-bench-2-1`.
- Scratch `/fast/scratch/hyaku/kengaku-r53/C1ScoutSrcTB2/` (raw API JSON + diffs; free space seen
  487 GB) is removed before this seat yields; only `fetched/` copies are kept. No fixture repos, no
  git mutations, no writes outside the seat directory.
