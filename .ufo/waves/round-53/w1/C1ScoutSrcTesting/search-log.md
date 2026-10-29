# Search log — C1ScoutSrcTesting (2026-10-28)

SOURCES contract v1 rule 5 (PRISMA-inspired): one bounded search, question/query, where searched, date,
identified / screened / included / excluded counts, exclusion reasons, stop rationale. Rule 6: no credential or
private-URL material. Registry cross-check: corpus/SOURCES.md read in full first (rows S001-S193 plus the standing
search log) so no URL already rowed was re-rowed.

## Question

"Does the software-testing literature already define or measure weak, existence-only assertions and oracle strength —
test smells (Assertion Roulette, Unknown Test, trivial assertions), mutation-testing-based oracle adequacy, and
'assertions that only check a file exists' — as primary prior art for the R53-C1 presence-only grader predicate?"

## Where searched, 2026-10-28

- web_search (this harness), three rounds: (1) open PDF for State of Mutation Testing at Google; (2) Schuler/Zeller
  checked-coverage PDF; (3) LLM-generated-tests weak-assertion empirical studies; plus follow-ups for the checked
  coverage 43% passage and the oracle-problem survey's open copy.
- Direct fetches (curl): arxiv.org (abs + PDF), static.googleusercontent.com (Google archive PDF), web.archive.org
  (id_ raw snapshots for xunitpatterns.com and st.cs.uni-saarland.de, both unreachable directly from this host),
  philmcminn.com (coauthor copy of the TSE survey), dl.acm.org (blocked, see e1).
- Corpus cross-check only: tsDetect FSE 2020 (testsmells.org) is already registered as S189 with the Unknown Test and
  Resource Optimism definitions, so it was screened, not re-rowed.

## Counts

- Identified: 17 distinct candidate sources (listed below).
- Screened: 17 — every candidate at title/abstract level; 8 opened at byte level (archived under fetched/ with
  SHA256SUMS): the survey, the Google paper, Schuler-Zeller, Mind the Gap, BlindSpotEval, MUTGEN abs, the xunitpatterns
  page, the Konstantinou abs page. To Kill a Mutant returned only a Cloudflare interstitial (no source bytes).
- Included: 6 (draft rows S901-S906, status queued).
- Excluded: 11 (2 as rejected rows S907-S908; 9 log-level, reasons below).

## Exclusions

- e1 To Kill a Mutant: On the Effectiveness of Mutation Testing (ICSE 2024, doi 10.1145/3597926.3598090) — unopenable:
  dl.acm.org returned a Cloudflare "Just a moment..." interstitial (5,483 bytes, not archived as a source); no open
  author copy located. Would have been a caveat row (crash-dominated mutant kills), not a definition source.
- e2 tsDetect FSE 2020 technical paper — already registered (S189, same URL, same Table 1); not re-rowed per registry
  cross-check.
- e3 Schuler and Zeller, "Checked coverage: an indicator for oracle quality", STVR 23(7) 2013 — journal duplicate of
  the kept ICST 2011 paper (S903); one row per source kept.
- e4 Oracle-based Test Adequacy Metrics: A Survey (arXiv:2212.06118) — secondary survey whose primaries are the kept
  rows; not opened once S903/S904 landed (kept as a lead, not evidence).
- e5 GAssert, Evolutionary improvement of assertion oracles (doi 10.1145/3368089.3409758) — improves oracles; defines
  and measures no existence-only weakness.
- e6 What It Would Take to Use Mutation Testing in Industry (arXiv:2010.13464) — adoption study, not an oracle-strength
  definition or measurement.
- e7 Yuan et al., Simple Testing Can Prevent Most Critical Failures (OSDI 2014) — measures the power of trivial
  crash-level checks in distributed systems; opposite direction and no benchmark-grader bearing.
- e8 arXiv:1408.2688 — wrong-ID fetch: that ID is a Kepler superflares paper, not the oracle-problem survey (this
  seat's ID assumption; both fetched files deleted; correct open copy is the coauthor's philmcminn.com PDF, kept).
- e9 Kali / An Analysis of Patch Plausibility and Correctness (ISSTA 2015) — patch-correctness line of work, not
  assertion weakness.

## Stop rationale (rule 5)

Six kept sources cover every named sub-topic with a primary: the umbrella oracle definition (S901), the industrial
covered-but-not-asserted statement plus its mutation measure (S902), the assertion-removal/checked-coverage instrument
(S903), the named oracle-gap metric (S904), and two modern oracle-strength measurements with the crash-kill exclusion
a presence-only classifier needs (S905, S906). The search is bounded to sources whose own text defines or measures the
weakness; further candidates (e4-e9) were screened to redundancy, off-direction, or unopenable, and S189 already holds
the test-smell catalogue. Diminishing returns: every additional hit recycled these six.
