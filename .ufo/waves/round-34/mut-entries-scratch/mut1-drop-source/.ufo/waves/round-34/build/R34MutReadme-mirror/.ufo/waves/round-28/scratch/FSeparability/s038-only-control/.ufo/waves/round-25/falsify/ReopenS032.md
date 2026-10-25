ATTACKS: SOURCES row S032 (Newcombe 1998, PubMed abstract) — re-fetched the gate URL, re-parsed the bytes, cross-checked Europe PMC, and tested every recorded cell (URL, sha256, quote, location, anchor, tier, scope, teaches).

## Method (observed)
- `curl` of the exact gate URL (`...efetch.fcgi?db=pubmed&id=9595616&retmode=xml`): HTTP 200, 4111 bytes, 2026-10-21T00:48:02Z. Second, independent fetch (urllib) ~00:51Z: 4111 bytes.
- sha256 both fetches = `e914ec0c036df445fd9476e90a172d9f3bc0d04863df7ddf089da870a7d7ba30` — identical to `gate.md:18`; stable, not a dynamic page.
- Parsed the single `<AbstractText>` (810 chars) and split it into sentences; character-identical to Europe PMC REST `EXT_ID:9595616 SRC:MED` `abstractText`.
- DOI resolves (doi.org → onlinelibrary.wiley.com, HTTP 403); Europe PMC `isOpenAccess=N`, `inEPMC=N`.

## Per-cell verdicts
- gate URL (`gate.md:18`) — AGREE: fetched; record is PMID 9595616, title/journal/DOI match the row.
- gate sha256 — AGREE: e914ec0c…7ba30 reproduced twice, byte count 4111 as recorded.
- gate quote verbatim — AGREE: the 14-word string occurs exactly once, inside AbstractText, verbatim (final period included).
- gate location "Abstract, final sentence" — DISAGREE: the abstract has five sentences; the quote is #4. The actual final sentence is: "In each case, methods are available that aim to align either the minimum or the mean coverage with the nominal 1 -alpha."
- SOURCES anchor (`corpus/SOURCES.md:54`, "Abstract, PubMed PMID 9595616 (EFetch)") — AGREE: MEDLINE record 9595616, abstract present.
- SOURCES source/citation — AGREE: title, "Statistics in Medicine 17(8):857–872 (1998)", author Newcombe, and the DOI identical to PubMed's `ArticleId IdType="doi"`.
- SOURCES tier A — AGREE: the original paper's own abstract, tier scoped to the abstract-only scope; lane precedent (S001, S004, S011, S017, S020–S022 are abstract-anchored tier A).
- SOURCES scope — AGREE: "abstract's comparison criteria and recommendation only; full text not opened" is honest — Wiley 403 reproduced; no OA copy (EPMC isOpenAccess=N/inEPMC=N).
- SOURCES teaches — AGREE: sentence 1 ("Simple interval estimate methods for proportions exhibit poor coverage…") and sentence 4 support both clauses; "simpler score methods" → "simple score" is a fair paraphrase. Minor ambiguity only: "simple single-proportion intervals" can read as if intervals are simple, where the abstract says simple *methods*; the row is `queued`, used-by `—`.
- census: `scripts/sources-census.sh validate --root … kengaku` → `kengaku ok`, exit 0.

## Blast radius
- S032 is cited by nothing: `grep -rn "S032\|9595616\|Newcombe"` over the lane finds only SOURCES.md:54, gate.md:18/28, and wave-1's `.ufo/waves/round-25/build/SrcNewcombe1998.md:36`, which repeats the same "final sentence" error.
- No content or hash break in the row; the defect is the sentence-position label in the receipt.

VERDICT: PARTIAL — S032's row, verbatim quote, anchor, tier, scope and sha256 all survive; the gate's location cell "Abstract, final sentence" is false (the quote is sentence 4 of 5).

Installs: none.
