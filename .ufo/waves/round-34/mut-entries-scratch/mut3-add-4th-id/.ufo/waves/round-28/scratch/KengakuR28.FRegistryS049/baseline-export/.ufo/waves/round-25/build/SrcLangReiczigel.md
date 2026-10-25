# SrcLangReiczigel — round 25 frontier source (C1 novelty)

Scope: open Lang & Reiczigel 2014 and draft one SOURCES row. No lane file written; this report carries the draft.

## Opened

- OPENED (abstract only): PubMed record PMID 24416798, DOI 10.1016/j.prevetmed.2013.09.015, Prev Vet Med 113(1):13–22 (print 2014-01-01).
  URL actually fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=24416798&rettype=abstract&retmode=xml (NCBI E-utilities, official API).
  Access: 2026-10-21T00:16:35Z (host-local 2026-10-20 21:16 −03).
  sha256 of fetched bytes: 50f5a105767d6b7ec9f66032a627c242d721254b2f092cd38b78237ad25f12dc (7106 bytes), saved only in /tmp/kengaku-r25-SrcLangReiczigel/efetch-24416798.xml.
- NOT OPENED (failed or no record):
  - https://doi.org/10.1016/j.prevetmed.2013.09.015 — returned Crossref metadata only; abstract field "No abstract available".
  - https://www.sciencedirect.com/science/article/pii/S0167587713003152 — HTTP 403.
  - https://www.sciencedirect.com/science/article/abs/pii/S0167587713002936 — HTTP 403.
  - https://www.researchgate.net/publication/259118112_… — HTTP 403.
  - https://pubmed.ncbi.nlm.nih.gov/24416798/ (HTML) — cookie wall, no record content; the E-utilities XML above is the record.
  - https://pubmed.ncbi.nlm.nih.gov/?term=… — cookie wall.
  - PMC: esearch db=pmc, term 10.1016/j.prevetmed.2013.09.015 → Count 0 (`[DOI]` tag rejected by pmc, so the query fell back to all-fields; "No items found"). No open full text located.
- Full text (Elsevier PDF/article) NOT opened. No access-control bypass attempted. Simulation details beyond the abstract are therefore unverified.

## Quote (Gate)

Location: PubMed record PMID 24416798, efetch XML `<AbstractText>` (the Abstract), sentence 4 of the abstract.
Quote (23 words): "we propose a new method to construct approximate confidence intervals for the true prevalence when sensitivity and specificity are estimated from independent samples"
Word count checked with `python3 -c` split: 23.

## Draft SOURCES row (contract v1, 11 columns; id left as S0??)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0?? | Confidence limits for prevalence of disease adjusted for estimated sensitivity and specificity — Lang Z, Reiczigel J, Prev Vet Med 113(1):13–22 — https://doi.org/10.1016/j.prevetmed.2013.09.015 (PMID 24416798) | paper | A | the authors' own approximate CI method for true prevalence when sensitivity and specificity are estimated from independent samples, as stated in its Abstract | Abstract, PubMed record via E-utilities efetch retrieved 2026-10-21T00:16Z; print issue 2014-01-01; full text not opened | Rogan–Gladen prevalence correction with an Agresti–Coull-style adjustment for estimated sensitivity and specificity; abstract reports minimum coverage above 88%, 93%, 98% at nominal 90%, 95%, 99% down to n=30 | queued | 2026-10-20 | 180d | — |

Notes on the row:
- Tier A is scoped to the method the abstract states. Full text was not opened, so no claim about the derivation, the exact interval formulas or the simulation design is admitted from this row. If C1 needs those, the row must be re-opened in full text or the tier stays scoped to the abstract.
- `opened` is 2026-10-20 (host local date, as instructed). UTC retrieval is 2026-10-21; the row keeps the instructed date.
- The abstract says "mini-mum coverage" (source typo); the quote above avoids it.

## Relevance to C1 (not a verdict)

- [INFERENCE] The abstract's method is the approximate-CI analogue of the Rogan–Gladen correction with estimated sensitivity and specificity. That is the situation C1's `rg_bound` addresses, so the row is a candidate reference for that interval. Whether `attrib_calibration.py` uses or should use this method is not checked here.

## Installs

None. Tools used: curl (already present), python3 (already present), NCBI E-utilities over HTTPS (no key, low volume).

VERDICT: one candidate row drafted from the PubMed abstract (opened, 23-word quote with location); full text and the Elsevier landing page were blocked (HTTP 403), so the row is abstract-scoped.
