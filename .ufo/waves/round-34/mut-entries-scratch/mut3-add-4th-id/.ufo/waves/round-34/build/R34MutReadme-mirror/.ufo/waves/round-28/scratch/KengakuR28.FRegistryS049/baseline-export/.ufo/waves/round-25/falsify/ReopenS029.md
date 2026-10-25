ATTACKS: S029 (Brown, Cai & DasGupta 2001) — re-fetched the gate's repository URL, re-verified both quotes verbatim + location, `anchor`, tier/scope, and the sha256 receipt.

Method: `curl -sS -L` the gate URL (2026-10-21T00:48Z) into /tmp/k25w2-ReopenS029; `pdftotext -raw/-layout`; pristine copy `git archive 8ea41f9ed` at /tmp/k25w2-ReopenS029/fleetroot; live tree untouched.

Fetch + hash (corpus/evidence/round25-sources/gate.md:14)
- 302 → `repository.upenn.edu/server/api/core/bitstreams/c3690c8b-…/content`, HTTP 200, `content-disposition: inline;filename="euclid.ss.1009213286.pdf"`, `etag "c396a64eb00bff79b9c11ef54978e92b"`, 737317 B, 33 pp.
- `sha256sum s029.pdf` = `626d61d966ec920bb54e825399383cd0759450cae310c980298fac9beb0b76e0` — **identical** to the gate cell. Not a dynamic page; the receipt is byte-exact, so the "dynamic-page may re-hash" caveat never applies here.

Quote cells (AGREE both)
- q1 gate:14 "chaotic coverage properties of the Wald interval are far more persistent than is appreciated". PDF p.101 ¶1: "We begin by showing that the chaotic coverage properties of the Wald inter-/val are far more persistent than is appreciated." Only delta is the line-break hyphen (`inter-\nval`), the normal de-hyphenation case; 14 words ≤25. No negation in the sentence (checked surrounding 280 chars).
- q2 gate:15 "we recommend the Wilson interval or the equal-tailed Jeffreys prior interval for small n". PDF p.101 ¶2: "Based on this analysis, we recommend the Wilson interval or the equal-tailed Jef-/freys prior interval for small n and the interval suggested in Agresti and Coull for larger n." Same hyphen-only delta; 14 words ≤25.
- Location cells "Abstract ¶1, p.101" / "Abstract ¶2, p.101": AGREE. PDF page 1 footer prints 101, last page prints 133; abstract is exactly two paragraphs (`pdftotext -raw` lines 6-12 and 14-20).

Anchor cell (AGREE)
- corpus/SOURCES.md:51 anchor = "Abstract ¶1–2, p.101; opened copy: University of Pennsylvania repository deposit of the typeset article (publisher and JSTOR pages blocked)". Deposit is the publisher typeset TeX output (`pdfinfo`: CreationDate 2001-09-11, DVIPSONE; filename euclid.ss.1009213286.pdf), pp. 101–133 complete — so "typeset article", not preprint: AGREE.
- "blocked" is true but only in the challenge sense: re-fetch of `doi.org/10.1214/ss/1009213286` → 200 at projecteuclid with a 1161-B Incapsula stub, 0 occurrences of the quote; `jstor.org/stable/2673783` → 200 titled "Client Challenge", 0 occurrences. Both are bot-walls served as HTTP 200, so a status-code-only checker cannot call this cell false; phrase is imprecise (403 vs challenge), not wrong.

teaches cell (AGREE, one scope note)
- "Wald coverage is erratic even at large n" is licensed inside the anchor: p.101 ¶1 itself states the textbook rule "should be used only when n · min(p,1−p) is at least 5 (or 10)" and calls those safety prescriptions "misleading and defective … and cannot be trusted" — a large-n safety rule refuted at p.101.
- The sharpest large-n datum (coverage 0.948 at n=953 falling to 0.852 at n=954) is on printed p.102, i.e. **outside** the declared anchor; the row does not cite it, so this is under-declaration headroom, not a widening.
- "Wilson or equal-tailed Jeffreys … for small n" matches ¶2 exactly; "why a point or Wald reading cannot be a verdict" is lane inference, consistent with ¶1's "cannot be trusted".

source / kind / tier / scope / status / opened / recheck / used-by (AGREE all)
- source: title, authors, Statistical Science 16(2):101–133 (2001) and DOI 10.1214/ss/1009213286 all match p.101 masthead and the DOI's resolution to that exact Euclid article.
- tier A is honest for a typeset original paper; scope "coverage and length … as this paper reports them" is inside the deposit (§3.3 "Expected Length", printed p.110) and not narrower than use.
- corpus/knowledge/attribution-interval-calibration.md:59 cites "S029, Abstract ¶1"+¶2 correctly for "Point and Wald readings mislead at small n" — strictly narrower than the row's licence, so Q3 (QUALITY.md:33) holds.
- Validator on the pristine tip copy: `scripts/sources-census.sh validate --today 2026-10-20 /tmp/k25w2-ReopenS029/fleetroot/kengaku-shokunin` → `kengaku-shokunin	ok	…/corpus/SOURCES.md`, EXIT=0 (no E01–E12 on S029). Noted: gate.md:5's relative `scripts/sources-census.sh` does not exist in-lane (fleet path only) — sibling finding, not a row defect.

Only nit (non-breaking): q2's truncation at "for small n" is not forced by the 25-word cap — the full clause through "for larger n" is exactly 25 words — and it drops the Agresti–Coull recommendation. The retained words "for small n" prevent any widening, and the knowledge entry restates the qualifier, so no downstream claim over-reads it.

Row stability: S029 was at `corpus/SOURCES.md:51` at tip 8ea41f9ed and still at :51 in the working tree; the only concurrent SOURCES.md edit during this re-open appended S038 at :58 (not mine, not the S029 row). My writes: this report only.

Installs: none (poppler `pdftotext`/`pdfinfo` already present; no pacman/uv/npx used).

VERDICT: SURVIVES — quotes, locations, anchor, tier, scope and sha256 all agree exactly on re-fetch; the row's only imprecision is "blocked" describing HTTP-200 bot-wall stubs.
