# Wave-2 seat report — W2ScoutPriorArtFresh (kengaku round 52, falsify)

Date 2026-10-28. Lane: kengaku-shokunin. Read-only prior-art pricing seat (novelty). No lane
file, fleet file, `.ufo/state/`, watchdog log, template, script or manifest was modified; no git
or jj mutation was run; the A5-excluded capture was never fetched into the lane tree.

## What I attacked

The **PRIOR-ART leg** of R52-C1: whether the five confirmed grader-vacuity findings (presence-only
test functions confirmed independently by W2ExecConfirmA and W2ExecConfirmB — `bn-fit-modify`,
`build-cython-ext`, `caffe-cifar-10`, `cancel-async-tasks`, `code-from-image`) are already
documented in public primaries, and whether the instrument (whole-benchmark grader triage) is
itself novel. I read `plans/round-52-claims.md` in full first, including Amendments A1–A5.

## Measured result

**14 public primaries fetched, 14 with HTTP status 200** (all quotes verified as verbatim
substrings of the fetched bodies; receipts in `receipts/fetch/`):

| # | URL | status |
|---|---|---|
| 1 | https://arxiv.org/abs/2601.11868 | 200 |
| 2 | https://arxiv.org/html/2601.11868v1 | 200 |
| 3 | https://arxiv.org/abs/2507.02825 | 200 |
| 4 | https://arxiv.org/html/2507.02825v2 | 200 |
| 5 | https://arxiv.org/html/2605.26079v1 | 200 |
| 6 | https://arxiv.org/html/2604.24955v2 | 200 |
| 7 | https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/67 | 200 |
| 8 | https://api.github.com/repos/harbor-framework/terminal-bench/issues/2086 | 200 |
| 9 | https://api.github.com/repos/harbor-framework/terminal-bench/issues/1387 | 200 |
| 10 | https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/CONTRIBUTING.md | 200 |
| 11 | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53 | 200 |
| 12 | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53/files | 200 |
| 13 | https://www.tbench.ai/news/terminal-bench-2-1 | 200 |
| 14 | https://june.kim/terminal-bench-frame | 200 |

## Per-finding verdicts

- FINDING bn-fit-modify verdict=phenomenon-new
- FINDING build-cython-ext verdict=phenomenon-new
- FINDING caffe-cifar-10 verdict=unclear
- FINDING cancel-async-tasks verdict=phenomenon-new
- FINDING code-from-image verdict=phenomenon-new

All five with evidence clauses in `prior-art.md`. Grounds: none of the five tasks is named in any
fetched primary (text search of the ABA body: 0 hits for four tasks; `caffe-cifar-10` has two
hits, both over-strict Evaluation issues, not presence-only). PR #53 (base sha = the lane's pin
`2fd12b88`) touches `caffe-cifar-10/tests/test_outputs.py` but its diff leaves
`test_prototxt_files_exist()` unchanged — the presence-only test survived the maintainer fix
unflagged. The weakness **class** is published by the benchmark's own authors (TB2 paper §B.4:
"tests might only check existence of a correct answer but not absence of wrong answers"; PR #53:
"Tests were updated when they over-specified or let any solution pass").

## Overall verdict on instrument-level novelty

**The category is phenomenon-known; the lane's static marker variant is not documented.**
Whole-benchmark grader triage and published audits of TB2 graders exist in fetched primaries in at
least four forms: the benchmark's own benchmark-wide adversarial exploit agent + ABC self-assessment
(S2, §B.4/§B.5); an automated static+trajectory audit of the exact same 89-task population (ABA,
S4 — strict recall 14/21 vs maintainer PR #53, +9.6% leaderboard lift when flagged tasks are
dropped); a proposed all-tasks verification audit (S7); and the maintainers' own 26-task/28-task
public revisions (S10, S11). No fetched primary describes a static, per-test-function,
marker-vocabulary presence-only classifier over grader bytes; TB2's own §B.5 concedes "Test case
quality is not assessed via objective, automated metrics". Consequence for the score rule: the
`CONFIRMED new ≥ 1` novelty leg survives **only** under weakness/instance-level pricing (4 new,
1 unclear); under class-level pricing it fails. If the lane's prior-art leg prices only
instance-level novelty without citing S2/S4/S10/S11, it overstates novelty and is falsifiable by
the ABA paper alone.

## Exact commands run

```
mkdir -p /fast/scratch/hyaku/kengaku-r52/w2-W2ScoutPriorArtFresh/fetch
curl -sS -L -o fetch/tb2-paper.html -w "STATUS=%{http_code}\n" https://arxiv.org/abs/2601.11868
curl -sS -L -o fetch/tb2-paper-full.html -w "STATUS=%{http_code}\n" https://arxiv.org/html/2601.11868v1
curl -sS -L -o fetch/abc-paper.html https://arxiv.org/abs/2507.02825
curl -sS -L -o fetch/abc-paper-full.html https://arxiv.org/html/2507.02825v2
curl -sS -L -o fetch/aba-paper.html https://arxiv.org/html/2605.26079v1
curl -sS -L -o fetch/whoguards-paper.html https://arxiv.org/html/2604.24955v2
curl -sS -H "Accept: application/vnd.github+json" -o fetch/tb2-issue67.json https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/67
curl -sS -H "Accept: application/vnd.github+json" -o fetch/tb-issue2086.json https://api.github.com/repos/harbor-framework/terminal-bench/issues/2086
curl -sS -H "Accept: application/vnd.github+json" -o fetch/tb-issue1387.json https://api.github.com/repos/harbor-framework/terminal-bench/issues/1387
curl -sS -o fetch/contributing.md https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/CONTRIBUTING.md
curl -sS -H "Accept: application/vnd.github+json" -o fetch/tb2-pr53.json https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53
curl -sS -H "Accept: application/vnd.github+json" -o fetch/tb2-pr53-files.json "https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53/files?per_page=100"
curl -sS -L -o fetch/tb21-note.html https://www.tbench.ai/news/terminal-bench-2-1
curl -sS -L -o fetch/frameblind.html https://june.kim/terminal-bench-frame
# quote extraction: python3 regex over the fetched bodies (script inline, saved transcripts above)
```

Tooling: no installs or upgrades were needed (curl, python3 preexisting); nothing to record under
the tooling directive.

## Files produced (absolute paths)

- `/fast/scratch/hyaku/kengaku-r52/w2-W2ScoutPriorArtFresh/prior-art.md` (working copy, scratch —
  removed at yield)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/prior-art.md` (copied receipt)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/receipts/fetch/` (14 fetched bodies)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/report.md` (this file)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScoutPriorArtFresh.md` (scoped findings, per item)

## Did the attack land?

**Landed (partially).** The attack landed against the *category-level* novelty framing: the claim's
"first instrument that audits a benchmark's graders as a population" is falsified as a world-first
statement by the TB2 paper's own §B.4 and by ABA's audit of the same 89-task population. The attack
did **not** overturn the per-finding novelty leg: 4 of 5 confirmed findings price phenomenon-new at
weakness level under my fetches (1 unclear), so the frozen score rule's letter can still be met —
provided the lane's prior-art file prices at that level and cites the class-level primaries.
Scratch dir removed after copying receipts; free space seen at start: 543G on /fast.
