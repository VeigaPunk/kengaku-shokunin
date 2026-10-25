# R25 SrcClopperPearson — Clopper & Pearson (1934) frontier source

Seat: KengakuR25.SrcClopperPearson (leaf scribe, no dispatch). Owned axis: novelty (C1 source).
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Nothing written to the live lane tree, git/jj state, or SOURCES.md.

## Outcome: NOT OPENED — lead only, no SOURCES row admitted

The primary paper was NOT opened. Per CORPUS.md §SOURCES rule 1 ("a row is a claim; write it only after opening the source"),
and §Leads ("a lead is not evidence and never a row"), no registry row is admissible this round. Quote requirement cannot be met.

## Access attempts (exact)

| # | Channel | Observed | Result |
|---|---|---|---|
| 1 | https://doi.org/10.1093/biomet/26.4.404 (reader, Crossref-backed) | text/markdown, method=crossref | Metadata only; "Abstract: No abstract available." No body text. |
| 2 | https://api.crossref.org/works/10.1093/biomet/26.4.404 (curl) | HTTP 200, 1967 B | Metadata opened (identity only). |
| 3 | https://academic.oup.com/biomet/article-pdf/26/4/404/823407/26-4-404.pdf (curl, UA set) | HTTP 403, text/html, 5600 B | Publisher challenge page, not a PDF. |
| 4 | https://academic.oup.com/biomet/article/26/4/404/230356 and .../article-abstract/26/4/404/291538 (reader) | HTTP 403 | Blocked. |
| 5 | https://www.jstor.org/stable/2331986 (reader) | "Client Challenge" page | Blocked. |
| 6 | https://www.scienceopen.com/document?vid=70f78b7c-1182-4b9b-9e6f-4a0f774e6cd6 (reader) | HTTP 403 | Blocked. |
| 7 | https://api.unpaywall.org/v2/10.1093/biomet/26.4.404 (curl) | HTTP 200; is_oa=false, oa_status=closed, best_oa_location=null, oa_locations=[] | No open copy exists to fetch. |
| 8 | archive.org advancedsearch (clopper pearson 1934 binomial) | HTTP 200, numFound=0 | No copy. |
| 9 | PubMed/PMC | not queried | Not a PMC-indexed title; Unpaywall reports no repository copy (has_repository_copy=false). |

I did not attempt to defeat the OUP/JSTOR challenge or paywall (no browser automation, no header games beyond a UA string). Those are access controls; that is the boundary.

## Receipts for what did open (identity only, not claims about content)

- URL opened: https://api.crossref.org/works/10.1093/biomet/26.4.404 (and https://doi.org/10.1093/biomet/26.4.404)
- Access time: 2026-10-21T00:16:50Z (UTC; host-local date 2026-10-20).
- sha256 crossref.json (1967 B): e81e9ac6cd8db3e2d17e643f9a7af954d79808a2f907cf0e6f10c8e9312eeb97
- Extracted fields: title "THE USE OF CONFIDENCE OR FIDUCIAL LIMITS ILLUSTRATED IN THE CASE OF THE BINOMIAL"; authors C. J. Clopper, E. S. Pearson; Biometrika vol 26 issue 4, pp. 404-413, 1934; publisher OUP; is-referenced-by-count 4275.
- sha256 of the OUP 403 challenge bytes (5600 B, NOT the paper): 23a7fc6b78b6d1e6fc6587a0a501a3894db91b57919b6751b1b3564f68711a22.
- No ≤25-word verbatim quote exists from the paper: none was retrieved. Any quote here would be fabricated; none is given.

## Lead note (draft, NOT a row — for the lane owner)

- LEAD: Clopper & Pearson 1934, "The use of confidence or fiducial limits illustrated in the case of the binomial", Biometrika 26(4):404-413, doi:10.1093/biomet/26.4.404. Status: unopened (paywalled; OUP/JSTOR challenged; no OA copy per Unpaywall). Candidate use: primary anchor for the exact two-sided Clopper–Pearson interval used by plans/attrib_calibration.py `clopper_pearson`. Would become a row only after a human or a run with paper access opens the PDF, records URL/time/sha256, and quotes the interval definition (≤25 words, with page/section).
- Substitute to consider (NOT verified by this seat, do not cite as opened): an authorised library copy of the same article, or a textbook (e.g. Brown, Cai & DasGupta 2001 "Interval Estimation for a Binomial Proportion", Statistical Science 16(2)) which is a separate candidate and not opened here.
- REJECTED: none. This is a lead only; a rejection needs an opened source (rule 5 "a rejection is evidence of taste").

## Findings for C1 (novelty axis, source side)

- The C1 interval rule in plans/round-25-claims.md:35 names the two-sided 95% Clopper–Pearson interval (α=0.05). The source that defines it is unopened here, so this seat cannot confirm the rule's attribution wording from the paper. The implementation's correctness is for the calc writer and the replay to check, not this seat.
- The paper's bibliographic identity is confirmed by Crossref (title, volume, issue, pages, year). That confirms the citation, nothing about the method's content.

## Installs / updates
None. Used curl, jq, sha256sum (preinstalled). pdftotext present, unused. Scratch: /tmp/kengaku-r25-SrcClopperPearson (scratch only, no clone created).

## Out of scope
No edits to corpus/SOURCES.md, no knowledge/lessons entries, no plans/ files, no MANIFEST, no git/jj mutation.

VERDICT: Clopper & Pearson 1934 is NOT opened (publisher challenge/paywall, no OA copy); no SOURCES row admitted; lead-only note above; identity confirmed via Crossref; no quote exists so no row is drafted.
