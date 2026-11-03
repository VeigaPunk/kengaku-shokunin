# kengaku: second curated source to consider after hyaku

Date: 2026-11-03

**Status: unassimilated future candidate after hyaku.** Reading proposal only: no training, execution, assimilation, dependency adoption or external changes. Earlier notes remain unchanged.

## LiveCodeBench: date-windowed evaluation and explicit errata

- Primary source: <https://github.com/LiveCodeBench/LiveCodeBench/tree/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24>
- Domain fit and new gap: Adds a concrete temporal-cohort control beyond HELM’s coverage framing and EvalPlus’s stronger tests. The runner filters contest dates and supports fixed dataset versions; errata expose autograding problems that temporal freshness alone cannot repair.
- Precise reading: README.md — Dataset Versions; Code Generation / Evaluation; lcb_runner/evaluation/compute_scores.py — compute_scores date filtering and final denominator; ERRATA.md — Multiple Solutions Accepted; Interactive Problems; Erroneous Test Cases.
- Future question: Can a frozen post-cutoff cohort remain comparable after invalid problems are excluded?
- Proposed later evaluation (original lane-specific design): After hyaku, design a paper admission sheet for one date-bounded cohort: pin dataset revision, model cutoff evidence, inclusive date boundaries, difficulty/platform mix and exclusion reasons. Include boundary-date and empty-cohort controls. Report contamination exposure as unknown when model provenance is missing, and predeclare how removed tasks affect denominators. No model calls or benchmark execution.
- Limitations: Publication date does not prove absence from training. ERRATA prose counts do not match their lists; enumerate pinned dataset records rather than reuse headings. Repository licensing does not settle scraped contest-data rights.
- License/reuse: MIT; official pinned license read at <https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24/LICENSE>. Preserve applicable notices; dependencies and external data need separate review.
- Version/timestamp: Official API returned 28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24 with committer timestamp 2025-07-16T00:58:38Z. Commit snapshot, not a release assertion or proof of latest maintenance. Fetched 2026-11-03.
- Deduplication: All supplied lane existing-context files, including published first-batch notes, and existing-urls.json. Repository aliases and source-family names checked. Not a claim about unprovided historical files. No exact-URL or source-family match found.

### Verification links

- <https://api.github.com/repos/LiveCodeBench/LiveCodeBench/commits/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24>
- <https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24/README.md>
- <https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24/LICENSE>
- <https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24/ERRATA.md>
- <https://raw.githubusercontent.com/LiveCodeBench/LiveCodeBench/28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24/lcb_runner/evaluation/compute_scores.py>

