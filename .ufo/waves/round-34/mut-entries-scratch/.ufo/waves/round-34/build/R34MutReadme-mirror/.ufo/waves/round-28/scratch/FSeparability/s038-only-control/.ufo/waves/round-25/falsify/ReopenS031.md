ATTACKS: SOURCES row S031 (Wilson, "Probable Inference, the Law of Succession, and Statistical Inference", JASA 22(158):209-212, 1927) — re-fetched the anchor's own URL, recomputed sha256, OCR'd and visually read both cited pages at 400 dpi, and re-checked quote, location, anchor, tier/scope, used-by and census validity at the landed tip.

F1 sha256 — AGREE. `curl -L https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf` -> HTTP 200, 339498 bytes; `sha256sum` = c2fc82b5c7c3fca821d8451dcaae82a047310b32b5bcfb2a4268362a1a438735, exactly gate.md:17. Second fetch is byte-identical (`cmp` -> IDENTICAL_BYTES), so the pin is not a dynamic-page capture.

F2 quote — AGREE verbatim. 400 dpi crop of PDF p.3 reads: "bad as p_0 is less or equal to P_lambda.   And this form of statement is not elliptical.   It is the proper form of probable inference." Word-for-word identical to gate.md:17 (16 words, under the 25-word cap). Only delta: the print sets double spaces after the periods; the receipt normalises to single — spacing, not wording.

F3 location — AGREE. Printed 210 = PDF page 3 (PDF p.1 is the JSTOR cover; OCR headers of pp.4-5 read "211"/"212"). The sentence follows the displayed two-sided range (p_0+t/2 +/- sqrt(p_0 q_0 t + t^2/4), all over 1+t) and the "such hard luck" clause — precisely "after the range formula" (gate.md:17, SOURCES.md:53).

F4 anchor cell — AGREE, both halves. p.209 para 2 = "Strictly speaking, the usual statement of probable inference as given above is elliptical." (crop `crop_p209_para2.png`), supplying the "usual ... is elliptical" half of `teaches`; p.210 supplies the "proper form" half. URL as written is live (200); no-www variant also 200. "(scan, OCR; publisher and JSTOR blocked)" is accurate: DOI resolves to tandfonline.com and returns 403; https://www.jstor.org/stable/2331968 returns a 3 KB `<title>Client Challenge` page, i.e. blocked.

F5 tier/scope — AGREE. Tier A matches the in-file legend "original paper" (SOURCES.md:11-12). Scope honestly limits to Wilson's own statement and disclaims coverage performance: the article contains no coverage grid or simulation, only the P_lambda bound on observing so bad a p_0 — an inference statement about the observation, not interval coverage. "score-type" is exact, not loose: with t = lambda^2/n the printed range is algebraically the Wilson score interval (p+z^2/2n)/(1+z^2/n) +/- (z/(1+z^2/n)) sqrt(p q/n + z^2/4n^2).

F6 remaining cells — AGREE. kind=paper, status=queued, opened=2026-10-20, recheck=180d, used-by=— all match schema and practice. `bash scripts/sources-census.sh validate --file kengaku-shokunin/corpus/SOURCES.md --today 2026-10-20` -> `file ok`, exit 0 (row has 11 columns / NF=13). `grep -rn S031` across *.md/*.py finds only SOURCES.md:53 and gate.md:17, so "used-by —" is honest, not a dropped citation.

F7 tip provenance — AGREE. Compared against `git show HEAD:...` at 8ea41f9ed: the S031 line in SOURCES.md and gate.md is byte-identical to the working tree (sha256 prefixes fda30a6e… / 5501c656… on both). The only dirty diff in those files is a peer's late S038 addendum. So every finding above is about the landed tip, not uncommitted bytes.

F8 caveat, not a break — the pinned PDF has no text layer: `pdffonts` is empty, `pdfimages -list` shows 5 1-bit CCITT images, `pdftotext` emits 5 bytes. "OCR" in the anchor/gate is therefore the reader's OCR, not an embedded layer, so a stranger cannot grep this quote from the artifact — reproduction needs tesseract/vision. The disclosure ("scan", "(OCR of scan)") is adequate, but the gate's hash->quote check is not machine-checkable for this row.

F9 gate-level nit, not the row — gate.md:29 groups S031 under "repository/author copies"; S031's copy is a third-party course-page mirror of a JSTOR scan (JSTOR cover is PDF p.1), neither a repository deposit nor an author copy. The row's own anchor says only "opened copy", so the row is accurate while the gate summary overgeneralises.

No counterexample found to any S031 cell: the interval, the page, the words, the access claim and the scope limit all reproduce from the URL the row itself names.

VERDICT: SURVIVES — quote verbatim at printed p.210 after the range formula, anchor/tier/scope honest, sha256 stable and exact; only a disclosed no-text-layer reproducibility caveat and a gate-summary provenance nit.

Installs: none — tesseract 5.5.3 (leptonica 1.87.0) and poppler 26.08.0 were already present; no pacman/uv/npm/cargo transaction run.
