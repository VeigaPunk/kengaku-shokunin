# Round 25 — SrcRoganGladen (frontier source opening, C1 novelty)

Seat: KengakuR25.SrcRoganGladen (leaf scribe, no dispatch). Lane: kengaku-shokunin, base 3f371d2.
No lane file written. Fetched bytes kept only in /tmp/kengaku-r25-SrcRoganGladen (scratch).

## Target
Rogan WJ, Gladen B. "Estimating prevalence from the results of a screening test."
Am J Epidemiol 107(1):71–76, 1978. doi 10.1093/oxfordjournals.aje.a112510 (PubMed 623091).

## Open attempts (what did and did not open)
| URL | Result | Bytes / sha256 |
|---|---|---|
| https://doi.org/10.1093/oxfordjournals.aje.a112510 | Opened via CrossRef-backed metadata page; metadata only, "No abstract available" | not hashed (read tool) |
| https://api.crossref.org/works/10.1093/oxfordjournals.aje.a112510 | OK, metadata JSON; reference-count 0, no abstract | not hashed (read tool) |
| https://academic.oup.com/aje/article/107/1/71/98459 | HTTP 403 | n/a |
| https://academic.oup.com/aje/article-pdf/107/1/71/9941166/107-1-71.pdf | HTTP 403 (full-text PDF not openable) | n/a |
| https://academic.oup.com/aje/article-abstract/107/1/71/98459 (curl) | HTTP 403 | oup-landing.html, not usable |
| http://aje.oxfordjournals.org/cgi/content/abstract/107/1/71 (curl) | HTTP 200, but a JS cookie challenge page (no article text) | legacy-aje-abstract.html 1449 B, sha256 202a03b00e6df1c4a0772c4ed0592348101caf2488c49f099d3d0d207bcccc42 |
| https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=623091&retmode=xml (curl) | OK, PubMed record incl. AbstractText | pubmed-623091.xml 3323 B, sha256 f7abdc9070c541963124f8fdcce0c169305afa9c00f19696f50e2363460c41a2 |
| Europe PMC REST search DOI:10.1093/oxfordjournals.aje.a112510 (curl) | OK, JSON incl. abstractText; inPMC=N, hasPDF=N, isOpenAccess=N | epmc-doi.json 2838 B, sha256 74f96bb9261e2a2e5a895aef958419ac0147d3ca64573b3d8791aa709ea5ab3f |

Verdict on access: ONLY the abstract opened (PubMed efetch + Europe PMC, identical text). Full text
(the Rogan–Gladen estimator and its variance) is NOT opened: publisher HTML and PDF return 403; no
PMC copy exists (inPMC=N). Nothing about the estimator formula is grounded by this round's bytes.

Access timestamp (curl, `date -u`): 2026-10-21T00:16:29Z; local clock 2026-10-20 (UTC-3).
Row `opened` uses the local calendar date 2026-10-20 as assigned.

## Draft SOURCES.md row (status queued, id left as S0??)
| S0?? | Estimating prevalence from the results of a screening test — Rogan WJ, Gladen B, Am J Epidemiol 107(1):71-76 (1978) — https://doi.org/10.1093/oxfordjournals.aje.a112510 | paper | A | the abstract's claim that positive-test frequency is a biased prevalence estimate and that adjustment is needed; full text not opened | Abstract (PubMed 623091 AbstractText, pubmed-623091.xml:4), Am J Epidemiol 107(1), Jan 1978 | positive-test frequency is a poor prevalence estimate and the paper gives adjustments; the adjustment formula is not in the opened abstract, so do not cite it as admitted content until full text opens | queued | 2026-10-20 | 180d | — |

Tier note: A is the original-paper criterion, but it is scoped to the abstract only. If the
full-text route stays 403, a knowledge entry citing the estimator must cite a different A/B source
or stay unadmitted. Flip: an opened full text (OUP PDF, library copy, or author copy) with the
estimator equation, which would let the scope widen.

## Gate receipt
- URL actually opened (text grounding `teaches`): https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=623091&retmode=xml ; cross-checked against https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1093/oxfordjournals.aje.a112510&format=json&resultType=core
- Access date/time: 2026-10-21T00:16:29Z (UTC; 2026-10-20 local)
- sha256 of fetched bytes: pubmed-623091.xml f7abdc9070c541963124f8fdcce0c169305afa9c00f19696f50e2363460c41a2 ; epmc-doi.json 74f96bb9261e2a2e5a895aef958419ac0147d3ca64573b3d8791aa709ea5ab3f
- Quote (17 words, verbatim incl. source typo "adjustmants"), location pubmed-623091.xml:4, AbstractText element (same text in epmc-doi.json abstractText field):
  "frequency of positive tests is shown to be a bad estimate, and the necessary adjustmants are given."

## Not grounded (not in any opened byte)
- The Rogan–Gladen correction formula, its Se/Sp assumptions, and its variance are recalled from outside knowledge: [INFERENCE] only, NOT verified here. Do not place in the row or in a knowledge entry on the strength of this round.

## Installs
None. Tools used: curl 8.23.0 (already installed, pacman untouched), sha256sum, date.

## Out of scope
No lane files, no SOURCES.md, no git/jj in the live tree, no subagent dispatch, no model or endpoint
requests. Scratch only in /tmp/kengaku-r25-SrcRoganGladen.

VERDICT: Abstract-only open (PubMed + Europe PMC, hashed); full text 403 everywhere; draft row A/queued with narrow scope, estimator formula ungrounded.
