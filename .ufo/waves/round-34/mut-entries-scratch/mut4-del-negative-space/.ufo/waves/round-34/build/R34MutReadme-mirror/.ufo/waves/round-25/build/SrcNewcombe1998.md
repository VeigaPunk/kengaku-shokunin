# Round 25 · SrcNewcombe1998 — frontier source opening (C1 novelty)

Scope: open Newcombe 1998, *Stat Med* 17(8):857–72; draft ONE SOURCES.md candidate row + Gate receipt. No lane file written; no subagents; no live model calls.

## What opened (observed)

| URL | Result | Bytes | sha256 |
|---|---|---|---|
| https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9595616&retmode=xml | HTTP 200 — PubMed record incl. full abstract | 4111 | e914ec0c036df445fd9476e90a172d9f3bc0d04863df7ddf089da870a7d7ba30 |
| https://pubmed.ncbi.nlm.nih.gov/9595616/ (via reader) | Abstract + MeSH, same text | — | — |
| https://doi.org/10.1002/(sici)1097-0258(19980430)17:8<857::aid-sim777>3.0.co;2-e | Resolves to Wiley; HTTP 403 (Cloudflare "Just a moment…" challenge) | 5768 | eab6a1b3c300e0121d16641bed8a00018fd5d2414bad7b0209bb72b633619c0a (challenge page, not article) |
| https://onlinelibrary.wiley.com/doi/abs/… and /doi/pdf/… | HTTP 403 (Cloudflare challenge) | 5798 | e51bc58a201be8fa1a966f9d6cb4e2572163dc71ae3a096d00b5b6bd5b23629c / 818b488d6ea0f2737c1b219b6dadf79ed2fad8cb533b033d2b7390c71c790494 (challenge pages) |
| Crossref (via reader) | Metadata only; "No abstract available" | — | — |
| Semantic Scholar API | HTTP 200; `openAccessPdf.status: CLOSED`, url empty | 454 | 6bb5e94d0759c3a0f2e438aab120564ddcaf58849eef43149c809678dae03504 |
| Unpaywall API | HTTP 200; `is_oa: false`, `best_oa_location: null` | 986 | 1514049bcd92c01cdb3b28bac5a4627368c194bac1938bd5baf09ae8010ed73f |

Result: **full text NOT opened**. The article is closed-access (Unpaywall/S2 both confirm); the publisher blocks automated access. Only the PubMed-hosted abstract was opened. Anything beyond the abstract is unobserved and must not be attributed to this row.

Access timestamp: assignment date 2026-10-20; host clock at fetch read 2026-10-21T00:16:26Z (UTC).

## Draft SOURCES.md row (status queued; id left as S0??)

Shape: contract-v1 11 columns, id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by

```
| S0?? | Newcombe RG (1998) Two-sided confidence intervals for the single proportion: comparison of seven methods — Stat Med 17(8):857–72 — https://doi.org/10.1002/(sici)1097-0258(19980430)17:8<857::aid-sim777>3.0.co;2-e | paper | A | two-sided CI methods for a single binomial proportion: coverage, location, width, aberrations (abstract scope only) | PubMed PMID 9595616, Abstract, EFetch sha256 e914ec0c…7ba30, publ. 1998-04-30; full text not opened (Wiley 403, closed access) | Gives criteria to judge single-proportion intervals (coverage, location, width, limits outside [0,1]) and names tail-area and score intervals as recommended | queued | 2026-10-20 | 180d | — |
```

Tier note: `A` is the original paper for its scope, but this round's evidence is the abstract only. If a later round opens full text and finds a claim not in the abstract, it must be a new row or a logged scope change. The `teaches` cell claims only what the abstract says.

## Gate receipt

- URL actually opened: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9595616&retmode=xml (PubMed PMID 9595616, mirrors publisher abstract)
- Access: 2026-10-20 (assignment); observed UTC 2026-10-21T00:16:26Z
- Fetched bytes sha256: e914ec0c036df445fd9476e90a172d9f3bc0d04863df7ddf089da870a7d7ba30 (4111 bytes), saved in scratch /tmp/kengaku-r25-SrcNewcombe1998/pubmed.xml
- Quote (14 words), location: PubMed record PMID 9595616, Abstract, final sentence of the abstract text:
  > "Intervals based on tail areas and the simpler score methods are recommended for use."
- Supporting quote (location: same abstract, first sentence): "Simple interval estimate methods for proportions exhibit poor coverage and can produce evidently inappropriate intervals." (19 words)
- Discrepancy: Crossref reports "No abstract available"; PubMed carries the abstract. The PubMed text is used.

## Rejected / lead notes

- None rejected. The `teaches` cell does not claim the Clopper–Pearson name; the abstract says only "tail areas". Mapping "tail areas" to Clopper–Pearson needs a source that says so explicitly (not opened this round). That mapping is `[INFERENCE]`.
- Lead (unopened, not a row): Stat Med 2005 letter in the "Comment in" list (doi 10.1002/sim.2164). Not opened.

## Installs / tooling

None. Used curl and python3 stdlib (XML parse, sha256sum). No pacman, no package transactions.

## Files touched

- Written: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-25/build/SrcNewcombe1998.md` (this report).
- Scratch only: `/tmp/kengaku-r25-SrcNewcombe1998/` (fetched bytes).
- Not written: any corpus/SOURCES.md or lane file.

VERDICT: Newcombe 1998 is closed access and only its PubMed abstract opened; one tier-A "queued" row is drafted with the abstract quote and a sha256 receipt, and full-text claims remain unverified.
