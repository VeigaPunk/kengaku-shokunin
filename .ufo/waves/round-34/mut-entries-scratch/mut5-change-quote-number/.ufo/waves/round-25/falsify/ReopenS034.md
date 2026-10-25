ATTACKS: non-author re-open of SOURCES S034 (Lang & Reiczigel 2014, PubMed abstract) — quote verbatim/location, anchor cell, tier/scope honesty, sha256

Fetch: `curl -sSL 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=24416798&rettype=abstract&retmode=xml'`
→ http=200, 7106 bytes, sha256 `50f5a105767d6b7ec9f66032a627c242d721254b2f092cd38b78237ad25f12dc`; two independent re-fetches
byte-identical to the gate hash, so the gate's "dynamic page may hash differently" caveat does not even apply here.

Per-cell verdict (SOURCES.md:56):
- source/citation — AGREE. XML: Volume 113, Issue 1, MedlinePgn 13-22, PubDate 2014 Jan 01, DOI
  `10.1016/j.prevetmed.2013.09.015`, authors Lang, Reiczigel. Every number in the citation is exact.
- kind `paper` — AGREE (`<PublicationType>Journal Article`).
- tier `A` — AGREE. Original paper's own text for a scope explicitly limited to the abstract; contract v1
  "original paper"; same treatment as S032/S033/S035.
- scope — AGREE. "reported coverage" is real: abstract says "mini-mum coverage is above 88%, 93%, and 98% at
  nominal 90%, 95%, and 99%"; "full text not opened" is honest — ScienceDirect article URL still 403 today.
- anchor — AGREE. Quote sits at `PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Abstract/AbstractText`
  (single AbstractText, unlabelled, no structured sections); EFetch 200. `https://www.sciencedirect.com/science/
  article/pii/S0167587713002936` → `http=403` today; DOI → linkinghub 200 redirect page, consistent with the
  "ScienceDirect HTTP 403" claim. PubMed HTML landing is a 203 cookie-challenge shell, so EFetch is the right route.
- teaches — **DISAGREE on the trailing clause only**. First half agrees: quote is a verbatim 23-word substring,
  found in no other text node; "approximate CI ... sensitivity and specificity estimated from independent
  samples" is a narrowing, not a widening. Trailing "— the coverage-exact alternative the lane's conservative
  corner bound does not attempt" is contradicted by the same abstract: it proposes "approximate confidence
  intervals", applies an Agresti–Coull-like adjustment "to improve coverage", and reports minimum coverage
  BELOW nominal (88/93/98% at 90/95/99%). "coverage-exact" appears nowhere in the quoted bytes and is false of
  S034; it also contradicts the row's own scope cell ("approximate interval"). Q3 widening in an appraisal cell.
  Knowledge doc is correct — attribution-interval-calibration.md:72 says the lane bound is "conservative, not
  coverage-exact" — so the defect does not propagate into the load-bearing entry; it is SOURCES-only wording.
- status `mined` / opened 2026-10-20 — AGREE (gate 21:16 -03 = 2026-10-21T00:16Z, local round date).
- recheck `180d` — AGREE within round 25 (S030/S032 same value); differs from r24 ISO-date style but consistent.
- used-by — AGREE: file exists and cites S034 at :70-72 as proposing "approximate limits", accurately.

sha256 — AGREE, exact and reproducible (not merely quote-verified).
Smallest honest change: replace "the coverage-exact alternative" with "an approximate, Agresti–Coull-adjusted
alternative, itself below nominal in minimum coverage" (or delete the appositive). Not fixed here (lane bound).

VERDICT: PARTIAL — quote (verbatim, 23 words), location, anchor, citation, tier, scope, sha256 all survive; the
teaches cell's "coverage-exact" clause breaks (contradicted by S034's own reported coverage and by its own scope cell).
Installs: none.
