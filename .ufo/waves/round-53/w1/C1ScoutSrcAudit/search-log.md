# Search log — C1ScoutSrcAudit (R53-C1 prior-art source scout), 2026-10-28

Topic: benchmark-validity checklists and meta-audits for agentic benchmarks (task/outcome validity, BetterBench-style
assessments) and papers/curations auditing verifiers/graders of terminal or coding agents for false positives.

## Procedure
1. Read `plans/round-53-claims.md` (frozen, commit a34838f) and `.ufo/waves/round-53/p1-spec.md` (the one
   presence-only definition) in full.
2. Read `corpus/SOURCES.md` in full (240 lines, 186 registry rows + search log) and extracted every URL already
   rowed: `grep -oE 'https?://[^ |)]+' corpus/SOURCES.md | sort -u` → 145 distinct URLs. No kept URL below appears
   in that set. S091 already rows the ABC paper (`https://arxiv.org/abs/2507.02825`, opened 2026-10-25), so the ABC
   line is treated as already registered and its URLs are rejected here, not re-rowed.
3. Searched (web_search harness), opened every serious candidate with `curl -sL`, archived kept bytes, verified
   each draft quote as a verbatim substring of the archive with its line number (python `str.find`).

## Queries (harness web search, 2026-10-28)
1. `"Agentic Benchmark Checklist" benchmark validity task validity outcome validity`
2. `BetterBench assessing benchmark quality NeurIPS Datasets Benchmarks`
3. `benchmark test grader false positive reward hacking coding agent "pass" empty file verifier audit paper`
(where searched: arxiv.org, github.com, papers.nips.cc, betterbench.stanford.edu,
uiuc-kang-lab.github.io, holdout-cc GitHub org; follow-on discovery: BetterBench arXiv id 2411.12990 found via the
betterbench.stanford.edu landing page, not guessed)

## Counts
- identified: 16 distinct candidate URLs over 13 sources surfaced and screened (the wrong BetterBench guess
  arXiv 2410.20574 contributes both its abs and html URLs; generic aggregator/blog hits were never promoted to
  candidates and are not counted)
- opened (bytes fetched and read): 12 URLs over 11 sources
- included (kept, rows S901–S906): 6
- excluded: 7 sources — 4 opened-and-rejected (rows S907–S910), 1 opened variant superseded by the kept archive of
  the same source (BetterBench NeurIPS proceedings PDF → archived from arXiv 2411.12990v1 instead), 2
  screened-not-opened (EvilGenie, RHB)

## Exclusion reasons
- `arxiv.org/html/2507.02825v1` (ABC paper HTML) — duplicate of rowed S091. flip in row S907.
- `uiuc-kang-lab.github.io/agentic-benchmarks/` — companion page of the same S091 work. flip in row S908.
- `arxiv.org/abs/2410.20574` — wrong paper (scout's incorrect id guess; differential geometry). Row S909.
- `betterbench.stanford.edu/` — landing page of the paper rowed as S905, nothing evidentiary. Row S910.
- EvilGenie (`arxiv.org/pdf/2511.21654`) and Reward Hacking Benchmark (`arxiv.org/html/2605.02964v1`) — screened,
  not opened: agent-side reward-hacking benchmarks (agents hardcode or edit tests), not audits of graders that
  accept a merely-existing artefact; wrong phenomenon side.
- LinkedIn post, emergentmind, daily.dev, towardsdatascience, onext, adaline blog — screened, not opened:
  non-primary commentary; contract favours primary sources.

## Leads passed forward (not rowed, not opened)
- `github.com/holdout-cc/reward-hack-patterns` — "a catalogue of the ways graders give credit for work that was not
  done" (linked from S904's README); pattern 01 is "do-nothing passes".
- `github.com/holdout-cc/rl-env-checklist` — a quality-assurance checklist to run before shipping an RL environment
  or agent benchmark.
- `github.com/holdout-cc/grader-bug-corpus` — regression-test corpus of real grading bugs, each paired with its fix.
These three are the strongest future prior-art candidates for a grader-level phenomenon leg; the 6-kept cap for this
seat was already full.

## Stop rationale
The 6-source cap was reached with all three requested lines covered: (a) the checklist line is already in the
registry (S091; duplicates refused here), (b) the meta-assessment line is covered by S905+S906 (BetterBench paper and
its successor), and (c) the grader false-positive audit line is covered by three fresh 2026 sources (S901–S903) plus
a community catalogue (S904). Remaining candidates are either duplicates, wrong-phenomenon (agent-side hacking), or
logged leads above; opening them would not add a new line.

## Discipline notes
- No credentials or private URLs recorded; all sources are public.
- Scratch lived only under `/fast/scratch/hyaku/kengaku-r53/C1ScoutSrcAudit/` and is removed before yield.
- No tools installed or upgraded (system curl, coreutils, python3 only); no pacman use.
