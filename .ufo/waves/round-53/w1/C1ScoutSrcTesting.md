# Report — C1ScoutSrcTesting (kengaku round 53, wave 1, R53-C1 prior-art source scout)

Date: 2026-10-28. Seat: source scout, software-testing literature on weak / existence-only assertions and oracle
strength. Blindness: this seat never opened, ran or asked for `plans/round53_c1_classify.py`, anything under
`.ufo/waves/round-53/w1/C1ExecClassifier*`, or any `C1Label*` file or directory; no other seat's output was read or
tuned against. Read first, in full: `plans/round-53-claims.md`, `.ufo/waves/round-53/p1-spec.md`,
`corpus/SOURCES.md` (registry + standing search log), `/home/vgpnk/Projects/shokunin/CORPUS.md` (SOURCES contract v1,
rules 1/5/6).

## What was done

One bounded search per SOURCES contract v1 rule 5 (full log: `.ufo/waves/round-53/w1/C1ScoutSrcTesting/search-log.md`):
identified 17, screened 17 (8 opened at byte level), included 6, excluded 11 (2 as rejected rows, 9 log-level with
reasons). Every kept source was opened this round and its read bytes archived (≤1 MiB each; one page-slice exception
noted below). Draft registry rows in the exact 11-column schema: `.ufo/waves/round-53/w1/C1ScoutSrcTesting/draft-registry-rows.md`
(placeholder ids S901-S908 for the L1 to renumber S194+; six queued, two rejected with flips).

## Kept sources (6) — quotes verbatim in archived bytes, ≤25 words, located

1. S901 Barr, Harman, McMinn, Shahbaz, Yoo — The Oracle Problem in Software Testing: A Survey (IEEE TSE 41(5), 2015).
   Quote (16 w, pdftotext lines 27-29): "a procedure that distinguishes between the correct and incorrect behaviors of
   the System Under Test (SUT)". Bearing: yes — defines the oracle whose weakest corner the presence-only assertion
   occupies; survey never names file-existence graders.
2. S902 Petrović, Ivanković — State of Mutation Testing at Google (ICSE-SEIP 2018). Quote (19 w, lines 74-76):
   "coverage alone might be misleading, as in many cases where statements are covered but their consequences not
   asserted upon". Bearing: yes — the industrial statement and mutation-based measure of the presence-only gap.
3. S903 Schuler, Zeller — Assessing Oracle Quality with Checked Coverage (ICST 2011). Quote (17 w, slice-pdftotext
   lines 239-240): "test suites with no assertions still detect a significant fraction of the mutations (43 % on
   average)". Bearing: yes — passes without assertions prove little; presence-only sits just above that floor.
4. S904 Jain, Kalburgi — Mind the Gap (arXiv:2309.02395v1, 2023). Quote (20 w, lines 80-82): "We define the oracle gap
   as the difference between source code coverage and mutation score for a given software element". Bearing: yes — a
   named metric for covered-but-not-asserted.
5. S905 BlindSpotEval (arXiv:2610.32548v1, 2026-10-23). Quote (18 w, line 244): "Oracle strength is high on average but
   uneven, with weaker assertions for object return property values and exceptions." Bearing: yes — per-assertion
   oracle-strength measurement that excludes incidental crash kills, the same exclusion a P1 classifier needs.
6. S906 MUTGEN (arXiv:2506.02954, v1 2025-06-03, IEEE TSE per abs comments). Quote (13 w, line 124): "some test suites
   achieve 100% coverage but only 4% mutation score". Bearing: yes — measured passing-without-constraining precedent.

Rejected with reasons and flips (opened, archived): S907 Meszaros, Assertion Roulette (xunitpatterns.com via Wayback
2025-01-18) — failure-localization smell, not oracle weakness (tsDetect S189 already rows the catalogue); S908
Konstantinou, Degiovanni, Papadakis (arXiv:2410.21136) — oracle-fidelity defect (actual-vs-expected), not
existence-only acceptance, names no benchmark grader.

## Commands run (exact)

- `mkdir -p .../w1/C1ScoutSrcTesting/fetched /fast/scratch/hyaku/kengaku-r53/C1ScoutSrcTesting`
- `curl -sL` fetches: `https://philmcminn.com/publications/barr2015.pdf`;
  `https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46584.pdf`;
  `https://web.archive.org/web/20260422011919id_/https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf`
  (then `qpdf sz-full.pdf --pages . 1,6 -- slice.pdf`, 751,031 bytes — full copy is 1,492,763 bytes and exceeds the
  1 MiB cap; the quoted paragraph is inside the slice);
  `https://web.archive.org/web/2024id_/https://www.xunitpatterns.com/Assertion%20Roulette.html` (gzip-decoded,
  18,201 bytes); `https://arxiv.org/abs/2610.32548` + `/html/2610.32548v1`; `https://arxiv.org/abs/2506.02954`;
  `https://arxiv.org/abs/2410.21136`; `https://arxiv.org/pdf/2309.02395v1`.
- Quote location: `pdftotext -q` per archived PDF, then `grep -n -F '<phrase>'` on the extraction (line numbers in
  report/rows); HTML anchors grepped on the archived HTML.
- `sha256sum * > SHA256SUMS` over the 13 archived files.

## Files produced (absolute)

- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcTesting/draft-registry-rows.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcTesting/search-log.md
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrcTesting/fetched/ — barr-harman-mcminn-
  shahbaz-yoo-oracle-problem-survey.{pdf(773,275 B),.txt}, petrovic-ivankovic-mutation-state-google.{pdf(419,943 B),
  .txt}, schuler-zeller-checked-coverage.pages1-6.wayback.{pdf(751,031 B),.txt}, jain-kalburgi-mind-the-gap.{pdf(514,190 B),
  .txt}, blindspoteval-2610-32548v1.html(306,270 B), meszaros-assertion-roulette.html(18,201 B), mutgen-abs.html(45,048 B),
  konstantinou-abs.html(42,261 B), SHA256SUMS.
- Nothing written outside my seat directory and scratch; scratch /fast/scratch/hyaku/kengaku-r53/C1ScoutSrcTesting
  removed before yield; two stray early fetches that briefly landed at the fleet root (before the `cd` guard was
  fixed) were moved into fetched/ — nothing at the fleet root remains from this seat.

## Tool notes

- No tools installed (existing curl/pdftotext/qpdf sufficed); pacman untouched per the 2026-10-20 pause.
- Tool inconsistency line: `bash: the harness prints "error: failed to redirect to <output path>: No such file or
  directory" when curl exits non-zero (observed on two unreachable hosts, xunitpatterns.com and st.cs.uni-saarland.de,
  http=000); the output file is simply absent — the message names the -o target, not a real redirect failure.`
- Host reachability: xunitpatterns.com and st.cs.uni-saarland.de unreachable directly (http=000); both read via
  web.archive.org id_ snapshots (snapshot ids in the rows). dl.acm.org serves a Cloudflare interstitial to curl.

## Hand-off to the L1 (wave 2)

- Renumber S901-S906 → S194+ if admitted; rows carry their own sha256s; wave-2 `phenomenon-new` sweep fetches can
  reuse S902/S904/S905 archives or re-fetch the canonical URLs.
- Unknown Test is already covered by S189 (tsDetect Table 1) — no new row needed; my S907 records why the smell
  catalogue does not reach existence-only assertions.
