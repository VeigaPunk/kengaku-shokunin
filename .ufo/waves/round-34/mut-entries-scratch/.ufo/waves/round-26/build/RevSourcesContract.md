# RevSourcesContract — read-only review

Axes: novelty (source/prior-art integrity); calibration is not changed by this registry review.

## Findings

- **No actionable SOURCES contract defect found.** S040 (SOURCES.md:62) uses the same arXiv URL as S035 (SOURCES.md:57), but scopes differ: S035 limits its row to means/quantiles/regression and excludes classifier sensitivity/specificity; S040 cites §4.2.2 label-shift class-share inference. S040's `teaches` begins `supersedes S035 —`, as CORPUS.md:116-118 requires for an appended correction. Therefore the validator's `W04` is the intended cross-scope warning, not an E04 same-scope duplicate or a reason to suppress/change the row. The warning is non-fatal (sources-census.sh:33, 643-649).
- The latest SOURCES id is S042 (SOURCES.md:64); S043 is not present yet. No candidate row is assessed for source substance because none has landed in SOURCES.md.

## Verification

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`:
  `kengaku<TAB>W04<TAB>S040 duplicate url arxiv.org/abs/2301.09633 across scopes`
  `kengaku<TAB>ok<TAB>/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`
- Manual contract checks on the current registry: 42 rows; malformed=0; no duplicate IDs; no kind/tier/status enum or community-at-A violations; no missing `used-by` path (including non-mined rows with a path); highest ID S042. Census itself reports no other E*/W* finding.
- `CORPUS.md:86-108` defines the eleven cells and their values; `CORPUS.md:112-128` requires rows to follow a source opened this round, append-only corrections, and a bounded search log. The current C1 registration additionally requires each opened-source URL, access date and located quote (≤25 words) in `corpus/evidence/round26-sources/gate.md` (round-26-claims.md:160-163).

## Required round-26 row shape

Append after S042 in `## Registry`; use S043 first, then S044… sequentially for additional opened sources. Keep exactly eleven cells and no `|` inside a value. Do not edit S035/S040 to silence W04.

```text
| S043 | <title — canonical URL or DOI> | <kind enum> | <A/B/C> | <specific scope> | <exact section/page/line + version or publication date> | <grounded teaching claim; or REJECTED: reason; flip: condition> | queued | <ISO date actually opened> | <ISO date, NNd, or symbolic cadence> | — |
```

For a source cited by the admitted C1 entry, use `mined` and its actual repo-relative `corpus/knowledge/grader-perturbation-audit.md` path in `used-by` (the target must exist in the landing tree); otherwise keep it `queued` with `—`. If an existing row's status/recheck/used-by changes, record old→new in the round lesson. Append a search-log note covering question/query, places searched, date, identified/screened/included/excluded counts and reasons, and stop rationale (CORPUS.md:116-128). The row's anchor must be specific, not a bare homepage; retain the ≤25-word located quote in the round-26 source evidence gate.

## Residual risk and verification gap

No LSP device/server is mounted (`read xd://lsp` returned “No such tool”); this is a literal Markdown/table and validator review, not LSP semantic-reference evidence. The report does not independently adjudicate C1 prior art or any future S043+ source's accuracy/tiering; those require the round's source-opening evidence and second-seat re-read.

VERDICT: Recommend treating W04 for S040 as legitimate and non-blocking; current registry has no malformed-row or used-by defect.