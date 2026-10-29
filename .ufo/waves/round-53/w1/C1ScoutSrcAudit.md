# Report — C1ScoutSrcAudit (kengaku round 53, wave 1, 2026-10-28)

Source scout for the R53-C1 prior-art leg. Topic assigned: benchmark-validity checklists and meta-audits for agentic
benchmarks (task/outcome validity, BetterBench-style assessments) and works auditing verifiers/graders of terminal or
coding agents for false positives. Lane bounds respected: no edits outside my seat directory and scratch; no git/jj
mutations; no fixture repos needed; no subagents (leaf seat).

## What I did
1. Read the frozen claims (`plans/round-53-claims.md`, commit a34838f) and `.ufo/waves/round-53/p1-spec.md` (the one
   presence-only definition) in full before searching.
2. Read `corpus/SOURCES.md` in full and extracted every already-rowed URL:
   `grep -oE 'https?://[^ |)]+' corpus/SOURCES.md | sort -u` → 145 distinct URLs over 186 rows.
3. Ran 3 harness web searches (queries in `search-log.md`), screened 14 candidate URLs, fetched bytes for 10 with
   `curl -sL` into scratch, opened each, and archived the 6 keepers.
4. Verified every draft quote as a verbatim substring of its archived file, with line number and word count
   (python `str.find`; zero misses on final pass). One verification failure caught before any row was written:
   my first BetterBench arXiv guess (2410.20574) resolved to a differential-geometry paper — rejected, correct id
   (2411.12990) found via the project site instead of guessed.
5. Cross-checked the registry for the ABC line: **S091 already rows the ABC paper**
   (`https://arxiv.org/abs/2507.02825`, opened 2026-10-25, mined). I therefore rejected both ABC URLs I had fetched
   (arXiv HTML v1 and the uiuc-kang-lab project page) instead of re-rowing that work.

## Exact commands (representative; all run 2026-10-28)
- `for pair in "abc|https://arxiv.org/html/2505..snip" ...; do curl -sL -A "$UA" --max-time 60 -w '%{http_code}' -o "$n.out" "$u"; done` — 8 first-round fetches, all HTTP 200.
- `curl -sL ... -o bb-html2411.out "https://arxiv.org/html/2411.12990"` — 200, 532,811 bytes, title confirms BetterBench.
- `cp cand/benchjack.out fetched/benchjack-arxiv-2605.12673v1.html && truncate -s 1048576 ...` — BenchJack was
  1,908,264 bytes; archived as the first 1,048,576 bytes (1 MiB cap), quote verified inside the kept span.
- `sha256sum ... > SHA256SUMS` in the fetched directory.
- Quote verification: python `str.find` per draft quote; all 9 located fragments OK (line numbers below).

## Measured numbers
- Registry before: 186 rows; registry URLs: 145 distinct. Zero overlap between kept URLs and that set.
- Screened 16 URLs (13 sources) → opened 12 URLs (11 sources) → kept 6 → excluded 7 sources: 4 opened-and-rejected
  (rows S907–S910), 1 opened variant superseded by the kept archive of the same source (BetterBench NeurIPS PDF,
  archived from arXiv 2411.12990v1 instead), 2 screened-not-opened (EvilGenie, RHB — reasons in the search log);
  3 holdout sibling repos logged as leads (cap full).
- Archive sizes (bytes): 1,048,576 (BenchJack, trimmed from 1,908,264), 379,862 (Unearned Passes), 826,283
  (Verification Horizon), 17,773 (holdout README), 532,811 (BetterBench), 10,098 (Fantastic Bugs abstract page).
  All ≤ 1 MiB; free space seen on /fast: 518G available (36% used), no ENOSPC.
- Every kept quote located in-archive: BenchJack line 809 (22 words), Unearned Passes line 338 (19), Verification
  Horizon line 423 (14), holdout README line 3 (18), BetterBench line 256 (21, typographic apostrophe as in bytes),
  Fantastic Bugs line 159 (11).

## Draft rows
10 rows (S901–S906 queued; S907–S910 rejected with `REJECTED: …; flip: …` in `teaches`) in the exact 11-column
schema: `.ufo/waves/round-53/w1/C1ScoutSrcAudit/draft-registry-rows.md`.

## Bearing on "tests that pass if the named artefact merely exists"
- S901 BenchJack — **yes**: "near-perfect on nine of the ten benchmarks, including Terminal-Bench" (line 809) plus
  exploits that score "without actually solving a single task" (line 475); it also names Terminal-Bench explicitly,
  so a wave-2 phenomenon-known row can cite it.
- S902 Unearned Passes — **yes, most literally**: "whether expected files exist" (line 338) is the presence-only
  evaluation mode named in the wild, with a verifier-weakness category separate from evidenced hacking.
- S903 Verification Horizon — **yes at the framing level**: false positive = "an incorrect solution passes the
  tests" (line 423); it does not name existence-only tests specifically.
- S904 holdout-findings — **yes**: do-nothing passes, exit-code-only checks, failure-defaults-to-pass patterns and a
  `terminal_bench` adapter with agent-writable tests (issue #1934 row, line 37).
- S905 BetterBench — **no**: its 46 criteria assess design/implementation/documentation/maintenance (line 256 quote
  shows scope); it never probes grader acceptance of a bare artefact. Kept as the topic's named meta-assessment line
  and as negative-sweep material; not a prior-art source for the phenomenon.
- S906 Fantastic Bugs — **no**: flags invalid questions via response-pattern statistics (line 159 quote); item-level,
  not grader-level. Same dual use as S905.

## Files produced (absolute paths)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/draft-registry-rows.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/search-log.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/benchjack-arxiv-2605.12673v1.html`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/unearned-passes-arxiv-2609.34262v1.html`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/verification-horizon-arxiv-2606.26300v1.html`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/holdout-findings-readme-2026-10-28.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/betterbench-arxiv-2411.12990.html`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/fantastic-bugs-neurips2025-abstract.html`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcAudit/fetched/SHA256SUMS`
  (9164745f…, abe2155a…, 08fc5c5c…, 5195672a…, 27320202…, fa1ae5f7… — full digests in the file)

## Blindness, tools, incidents
- Blindness: I read no classifier file, no label file, and no other seat's output; the classifier/label void was not
  approached. My sources are external only.
- Tools: nothing installed or upgraded (system curl, coreutils, python3); no pacman transactions.
- Tool inconsistencies: none observed.
- Scratch `/fast/scratch/hyaku/kengaku-r53/C1ScoutSrcAudit/` removed before yield.
- Note for the L1: because S091 already owns the ABC line, the round's novelty sentence for C1's prior-art leg is
  best carried by S901–S903 (three fresh 2026 grader-audit papers) — none of which is a per-test static classifier,
  which is exactly the lane's claimed gap.
