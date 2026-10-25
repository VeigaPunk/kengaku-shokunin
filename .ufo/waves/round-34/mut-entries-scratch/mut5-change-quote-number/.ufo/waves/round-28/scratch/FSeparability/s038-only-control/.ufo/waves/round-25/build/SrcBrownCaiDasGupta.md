# R25 · SrcBrownCaiDasGupta — frontier source opening (C1 novelty)

Seat: KengakuR25.SrcBrownCaiDasGupta (scribe, leaf, no dispatch). Lane: kengaku-shokunin, base 3f371d2.
Lane tree, lane git/jj state, SOURCES.md and corpus/ NOT written. Only this report file.

## Behavior
Opened Brown, Cai & DasGupta 2001, "Interval Estimation for a Binomial Proportion", Stat. Sci. 16(2):101–133, doi 10.1214/ss/1009213286.
The publisher page was blocked; the full article was opened from the UPenn repository deposit (author/repository copy, not the publisher PDF).

## Routes tried (exact outcome)
- projecteuclid.org …/10.1214/ss/1009213286.full (publisher HTML): Incapsula challenge page, no article text.
- projecteuclid.org …/ss/1009213286.pdf and …/journalArticle/Download?urlid=…: same Incapsula challenge.
- projecteuclid.org/euclid.ss/1009213286 (legacy permalink): same challenge.
- doi.org/10.1214/ss/1009213286 (Crossref metadata): opened; title, authors, Stat. Sci., published 2001-05-01, abstract confirmed.
- api.unpaywall.org (email placeholder): is_oa=false, oa_status=closed, best_oa_location=null, has_repository_copy=false. Discrepancy: the Euclid .full page advertises "Open Access May 2001" (web_search snippet); Unpaywall disagrees. Recorded, not resolved.
- jstor.org/stable/2676784: "Client Challenge" page, no content.
- pubmed term search: zero results for the title.
- semanticscholar.org search and api.semanticscholar.org DOI query: "Invalid URL format" / no paper ID extracted.
- web_search returned two author-copy candidates. stat.wharton.upenn.edu/~tcai/paper/Binomial-StatSci.pdf: curl exit 28, connect timeout after 135 s (HTTP 000). www-stat.wharton.upenn.edu/~lbrown/Papers/2001a…pdf: HTTP 404 (HTML, discarded).
- OPENED: https://repository.upenn.edu/bitstreams/c3690c8b-efaf-485b-a984-39cfc22aae13/download → 302 to https://repository.upenn.edu/server/api/core/bitstreams/c3690c8b-efaf-485b-a984-39cfc22aae13/content, HTTP 200.

## Gate receipt (the opened copy)
- URL opened: https://repository.upenn.edu/bitstreams/c3690c8b-efaf-485b-a984-39cfc22aae13/download
- Access: curl at 2026-10-21T00:16:37Z = 2026-10-20 21:16 -03 (local). Assignment date 2026-10-20 used for `opened`.
- Bytes: 737317, sha256 626d61d966ec920bb54e825399383cd0759450cae310c980298fac9beb0b76e0 (re-hashed after extraction; unchanged). Local copy /tmp/kengaku-r25-BrownCai/upenn.pdf.
- Identity: pdfinfo → PDF 1.3, 33 pages. pdftotext page 1 carries "Statistical Science 2001, Vol. 16, No. 2, 101–133" and the full abstract, so it is the full typeset article (not an excerpt).
- Quote A (teaches grounding, 15 words): "chaotic coverage properties of the Wald interval are far more persistent than is appreciated"
  Location: Abstract, paragraph 1, journal p.101 (PDF p.1). Verified with `pdftotext -f 1 -l 1` and whole-document search.
- Quote B (recommendation, 14 words): "we recommend the Wilson interval or the equal-tailed Jeffreys prior interval for small n"
  Location: Abstract, paragraph 2, journal p.101 (PDF p.1). The PDF line-break hyphen in "equal-tailed" was dropped by pdftotext; the printed text has the hyphen.

## Draft candidate row (contract v1, 11 columns; id left as S0??)
| S0?? | Interval Estimation for a Binomial Proportion — Brown, Cai & DasGupta, Statistical Science 16(2):101–133 (2001) — https://doi.org/10.1214/ss/1009213286 | paper | A | coverage and expected length of binomial-proportion intervals (Wald vs. Wilson, Jeffreys, Agresti–Coull) as this paper reports them | Abstract, p.101 (Stat. Sci. 16(2), May 2001); opened copy repository.upenn.edu bitstream c3690c8b-efaf-485b-a984-39cfc22aae13, typeset PDF 33 pp. | Wald coverage is erratic and its textbook safety rules are unreliable; recommends Wilson or equal-tailed Jeffreys for small n and Agresti–Coull for larger n | queued | 2026-10-20 | 180d | — |

Column check: 11 cells, no `|` inside any cell, tier A (original paper, scope = its own coverage/length study), status queued, used-by — (not yet cited).

## Tier caveat for the integrator
- The opened file is a repository deposit of the typeset article, not the publisher's PDF; the publisher page was never readable. Content identity is by journal header, page count and abstract text, not by publisher bytes. Recommend a non-author re-open of the publisher version when the challenge clears, which would confirm the anchor and quotes against the publisher bytes.
- Tier A is kept because scope is the paper's own study and the deposit is the paper itself. If the integrator treats a repository copy as insufficient, downgrade is not warranted by evidence in hand; flag to the scribe reviewer instead.

## Out-of-scope / not done
- Did not read or write SOURCES.md, knowledge/, lessons/, or the lane tree. Did not assign the S-number. No other sources opened.
- No model or endpoint requests. The Unpaywall call was a public DOI metadata lookup with a placeholder email; no secrets used.

## Installs
None. Used existing curl, pdfinfo and pdftotext (/usr/bin/pdftotext). No pacman, uv, or npm transactions.

## Findings
1. The primary publisher URL is Incapsula-blocked for this host. Confirmed via 4 distinct Euclid URL forms and JSTOR.
2. Published Open Access status conflicts: Euclid page label vs Unpaywall is_oa=false.
3. Author copy at tcai Wharton host unreachable from this host (connect timeout). The UPenn deposit is the only openable full text.

VERDICT: Source opened via UPenn repository deposit (sha256 626d61d9…, 33 pp, full article); draft row S0?? tier A, status queued, with two verified quotes; publisher page remained blocked, so re-open of publisher bytes is recommended.
