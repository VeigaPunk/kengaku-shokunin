# SrcPredictionPowered — round 25 frontier source gate (C1 novelty)

Behavior: opened the primary source (PPI, Angelopoulos et al. 2023). Drafted ONE candidate SOURCES row. No lane file written; no git/jj mutation; scratch only in /tmp/kengaku-r25-SrcPredictionPowered.

## What opened (observed)
- https://arxiv.org/abs/2301.09633 — read tool (arXiv API reader): abstract + metadata only. abs HTML fetched via curl: 42,033 bytes, sha256 03a457a2bb906d78aeca4a61aae40b56c633814265df1a97b3f06276c4cf2bef. Versions: v1 23 Jan 2023, v2 2 Feb 2023, v3 16 Feb 2023, v4 9 Nov 2023.
- https://arxiv.org/pdf/2301.09633 — OPENED (primary full text). HTTP 200, application/pdf, 4,833,991 bytes, sha256 a16bf2c108fea9f559d00708c731d29d673c1dcce5d4acfd65e64a694b7ae17a. `pdfinfo`: Pages 40, producer pdfTeX, created 9 Nov 2023 (= v4). Text via `pdftotext -layout`.
- https://www.science.org/doi/10.1126/science.adi6000 (DOI 10.1126/science.adi6000) — NOT OPENED. HTTP 403, Cloudflare "Just a moment..." challenge page, 5,497 bytes, sha256 7b6534e2a2ebda0ae9190c2bcb683e567b2d00504b0d11e2d26f62c285673740. Not bypassed.
- https://api.crossref.org/works/10.1126/science.adi6000 — OPENED (metadata only). HTTP 200, sha256 c8bc7a622d939653d3aae1136bcdb8e6e6f3dca43bcc5ad84237cc5257fcd69f. Science, vol 382, issue 6671, pp. 669-674, published-print 2023-11-10; title "Prediction-powered inference"; authors Angelopoulos, Bates, Fannjiang, Jordan, Zrnic.
- PubMed/PMC/JSTOR: not tried. The arXiv PDF opened, so the fallback chain was not needed.
- Access: 2026-10-20 21:16 -03:00 (2026-10-21 00:16 UTC), observed by `date`.

## Quotes (grounding)
- Q1 (grounds `teaches`), 12 words: "without making any assumptions on the machine-learning algorithm that supplies the predictions". Location: arXiv v4 PDF p.1, Abstract (printed page 1; "machine-/learning" is hyphen-wrapped in the PDF, rejoined here).
- Q2, 9 words: "more accurate predictions translate to smaller confidence intervals". Same location (p.1, Abstract).

## Scope check (C1 relevance)
- `grep -n -i 'clopper|rogan|gladen|sensitivity|specificity' arxiv.txt` → 0 hits. The paper does NOT cover classifier sensitivity/specificity correction, Rogan–Gladen, or Clopper–Pearson. The row's scope is therefore narrowed to mean/quantile/regression CIs from a gold-labelled sample plus predictions. It must NOT be cited for C1's attribution-accuracy intervals.
- Limitation: the anchor cites the arXiv v4 author copy. The Science text was not opened, so equivalence of Q1/Q2 to the Science version is [INFERENCE].

## Draft SOURCES row (NOT written to any lane file)
| S0?? | Prediction-powered inference (Angelopoulos, Bates, Fannjiang, Jordan, Zrnic) — https://arxiv.org/abs/2301.09633; DOI https://doi.org/10.1126/science.adi6000 | paper | A | its own prediction-powered CIs for means, quantiles and linear/logistic regression coefficients; does not cover classifier sensitivity/specificity or Rogan–Gladen correction | arXiv 2301.09633v4 (9 Nov 2023), PDF p.1 Abstract; Science 382(6671):669-674 (print 10 Nov 2023) per Crossref, publisher page not opened | small gold-labelled sample plus ML predictions gives CIs valid for any predictor, tighter as predictions improve ("without making any assumptions on the machine-learning algorithm that supplies the predictions", p.1 Abstract) | queued | 2026-10-20 | 180d | — |

Column check: 11 cells, no `|` inside cells, id left as `S0??` per instruction.

## Gate receipt
- URL actually opened: https://arxiv.org/pdf/2301.09633 (arXiv v4, 9 Nov 2023)
- Access date/time: 2026-10-20 21:16 -03:00 (2026-10-21 00:16 UTC)
- sha256 of fetched bytes: a16bf2c108fea9f559d00708c731d29d673c1dcce5d4acfd65e64a694b7ae17a
- Quote + location: Q1 above (≤25 words, p.1 Abstract)

## Leads / rejections
- Science publisher page: blocked (403 Cloudflare). Recheck needed before the row can claim the published text. Lead, not evidence.
- Rejection noted, not made: a PPI-based CI for classifier error rates (sensitivity/specificity) would need a separate source. None was opened this round.

## Tooling
- Installs: none. Used pre-existing `curl`, `pdftotext`, `pdfinfo`, `sha256sum`, python3 3.14.8.

## Out of scope / not touched
- No writes to corpus/SOURCES.md, corpus/evidence, plans/, or any git/jj state in the live lane. The only file written is this report.

VERDICT: primary arXiv PDF opened and hashed; Science publisher page blocked (403), Crossref metadata confirmed; one candidate tier-A row drafted with scope narrowed to CIs from gold labels plus predictions (no sensitivity/specificity coverage); status queued, nothing written to lane files. Installs: none.
