# SrcHanleyRuleOfThree — Round 25, C1 frontier source (read-only seat)

Scope: open Hanley & Lippman-Hand 1983 (JAMA 249(13):1743–1745, doi 10.1001/jama.1983.03330370053031); draft ONE SOURCES row. No lane file written. Scratch: /tmp/kengaku-r25-hanley.

## Opening attempts (observed)
| # | URL | Result |
|---|---|---|
| 1 | https://doi.org/10.1001/jama.1983.03330370053031 | Resolved to CrossRef metadata only (title, author, 1983-04-01, "No abstract available"). No article text. |
| 2 | https://jamanetwork.com/journals/jama/article-abstract/370053 | HTTP 403 (publisher). |
| 3 | https://jamanetwork.com/journals/jama/fullarticle/370053 | HTTP 403 (publisher). |
| 4 | https://pubmed.ncbi.nlm.nih.gov/6834526/ | Opened, but that PMID is Hautmann & Osswald 1983 — WRONG RECORD, discarded. |
| 5 | https://pubmed.ncbi.nlm.nih.gov/6867335/ | HTTP 203 / unrelated; discarded. |
| 6 | https://www.ncbi.nlm.nih.gov/pubmed/?term=10.1001%2Fjama.1983.03330370053031 | HTTP 200, search page; not the record. |
| 7 | https://api.crossref.org/works/10.1001/jama.1983.03330370053031 | HTTP 200, JSON metadata only. |
| 8 | web_search → https://pubmed.ncbi.nlm.nih.gov/6827763 (PMID 6827763, JAMA 1983) | Correct PubMed record located via search; not separately fetched for text. |
| 9 | https://jhanley.biostat.mcgill.ca/Reprints/If_Nothing_Goes_1983.pdf | HTTP 200, application/pdf, 75962 B, 3 pages, Adobe Paper Capture scan (JBIG2 images, NO text layer). Hashed; not quotable by pdftotext. |
| 10 | https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf | HTTP 200, application/pdf, 15770 B, 4 pages, text layer present, header "James A. Hanley and Abby Lippman-Hand, JAMA, April 1, 1983—Vol 249, No. 13 pp 1743-1745". USED FOR QUOTE. |

Conclusion: the typeset JAMA page was not openable (403). The article text was opened via the author's own reproduction (row 10) and the author's scanned reprint (row 9, hash only). The quote below is from row 10, which is an author-hosted copy, not the JAMA typeset page. This is the weakest point of the receipt and is recorded as such in the anchor.

## Gate receipt
- URL actually opened (text): https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf
- URL actually opened (scan, hash only): https://jhanley.biostat.mcgill.ca/Reprints/If_Nothing_Goes_1983.pdf
- Access: 2026-10-20 local (2026-10-21T00:16:25Z UTC), curl GET, User-Agent Mozilla/5.0.
- sha256 of fetched bytes:
  - zero_numerator.pdf: e3150aecd069144dcd81004171348bb7a658852da6e52a2b4e257c23fd746d79
  - If_Nothing_Goes_1983.pdf: 229925fb0674a6b4f57005bf93c1a039cc19fc46fa9892f9bd04fe81fc8bc4bf
- Quote (19 words), exact: "we can be 95% confident that the chance of this event is at most three in n (ie, 3/n)"
- Location: zero_numerator.pdf p.1 of 4, section "Making Inferences: The Rule of Three", paragraph 2 (pdftotext: line 63 of page-1 extract; "To be 95% confident ... a simple rule (of unknown origin) can be applied" precedes it).
- Companion sentence, same section (for teaches): "when n is larger than 30, the rule of three agrees with the exact calculation to the nearest percentage point; below 30, it slightly overestimates the risk".

## Independent check (stdlib python3, offline)
Exact one-sided 95% upper limit for 0/n is 1 − 0.05^(1/n):
| n | 3/n (rule) | exact 1−0.05^(1/n) | paper's stated value |
|---|---|---|---|
| 10 | 0.300 | 0.2589 | "maximum risk [ie, 26% if n=10]" — matches |
| 14 | 0.214 | 0.1926 | "correct upper confidence limit based on 0/14 is 19%" — matches |
| 30 | 0.100 | 0.0950 | "agrees ... to the nearest percentage point" — matches |
Rule-of-three overestimates for small n, as the paper states.

## Draft SOURCES.md row (contract v1, 11 columns; NOT written)
| S0?? | If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators — Hanley JA, Lippman-Hand A, JAMA 1983;249(13):1743-1745 — https://doi.org/10.1001/jama.1983.03330370053031 | paper | A | upper 95% confidence limit of a zero-numerator (0/n) rate, the "rule of three" | author-hosted copy https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf, p.1 of 4, section "Making Inferences: The Rule of Three"; publication 1983-04-01; typeset JAMA page not opened (HTTP 403) | with 0 events in n, the 95% upper limit is about 3/n; accurate to the nearest point for n>30, overestimates below 30 (n=10 gives 26% exact, 30% by rule) | queued | 2026-10-20 | 180d | — |

Tier note: A is per contract (original paper for this scope). Downgrade to B if the lane prefers to tier author-hosted reproductions below typeset primaries; the anchor already discloses the copy.

## Out of scope / not done
- Source not cited in any knowledge entry; used-by is "—" (status queued).
- No knowledge/ or lessons/ writes; no lane file written; no git/jj in the live lane.
- Reprint scan (row 9) not OCR'd; only its hash is recorded.

## Installs
None. Used existing curl, pdftotext/pdfinfo (poppler), python3 stdlib.

VERDICT: Source opened via author-hosted text copy (JAMA typeset 403); one queued tier-A row drafted with sha256 receipt and a 19-word verbatim quote; exact-bound check confirms the paper's 3/n statements.
