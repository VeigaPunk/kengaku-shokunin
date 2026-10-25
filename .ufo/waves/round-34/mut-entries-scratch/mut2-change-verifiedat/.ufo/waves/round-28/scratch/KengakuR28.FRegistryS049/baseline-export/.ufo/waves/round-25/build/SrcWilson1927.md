# SrcWilson1927 — Wilson 1927 frontier source (round 25, C1 novelty)

## Behavior
Opened Wilson 1927, "Probable Inference, the Law of Succession, and Statistical Inference", JASA 22(158):209–212, doi 10.1080/01621459.1927.10502953. Primary text obtained via an author/course-hosted scan. Draft one SOURCES candidate row (not written to the lane tree). No lane file written; no git/jj mutation.

## Sources attempted (exactly what happened)
| URL | Result |
|---|---|
| https://doi.org/10.1080/01621459.1927.10502953 | CrossRef metadata only (title, authors, pp.209–212, vol 22 no 158); "No abstract available". No body text. |
| https://www.tandfonline.com/doi/abs/10.1080/01621459.1927.10502953 | HTTP 403 |
| https://www.tandfonline.com/doi/pdf/10.1080/01621459.1927.10502953 | HTTP 403 |
| https://www.jstor.org/stable/2276774 (and ?seq=1) | "Client Challenge" page; not readable |
| https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf | **OPENED**: HTTP 200, application/pdf, 339,498 bytes, 5 pages; JSTOR cover page then printed pp.209–212 |

Fetch receipt (opened copy):
- URL actually opened: https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf
- Access time: 2026-10-20 21:16:27 -03 (= 2026-10-21T00:16:27Z), host clock.
- sha256 of fetched bytes: c2fc82b5c7c3fca821d8451dcaae82a047310b32b5bcfb2a4268362a1a438735
- Local copy: /tmp/kengaku-r25-SrcWilson1927/wilson1927_mcgill.pdf (scratch only)
- Text layer: none (`pdftotext` → 0 lines; `pdffonts` empty). Text obtained by `pdftoppm -r 300 -png` + `tesseract` (two psm modes agreed on the quoted sentence). Crops of pdf pages 2–3 viewed as images; the quoted sentence is on the line directly beneath the displayed range formula.
- Page map: PDF p.2 = printed p.209 ("Probable Inference (Usual)", "(Improved)"); PDF p.3 = printed p.210 (rule statement, "proper form"); PDF p.4 = printed p.211; PDF p.5 = printed p.212.

## Draft SOURCES.md row (contract-v1, 11 columns; id left as S0??; not written)
`| S0?? | Probable Inference, the Law of Succession, and Statistical Inference — Wilson, E.B., JASA 22(158):209–212 (1927) — https://doi.org/10.1080/01621459.1927.10502953 (opened copy: https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf, sha256 c2fc82b5…8735) | paper | A | Wilson's own statement of the score-type interval for a binomial rate p (not its coverage performance, which the paper does not evaluate) | printed pp.209–210: "Probable Inference (Improved)" p.209 and the rule with the quadratic-root range, "proper form" sentence p.210; revision JASA vol.22 no.158, 1927-06 | Wilson's quadratic-root range is the proper statement of probable inference about true p; the common "p lies within p0±λσ" form is "elliptical" (p.209), so interval statements must bound p, not the observed rate | queued | 2026-10-20 | 180d | — |`

Check: no `|` inside cells; 11 columns; tier A scoped to the paper's own statement; kind `paper`; status `queued`; recheck 180d (cadence, paper does not change; re-open only if the copy's provenance is questioned).

## Gate receipt (for the round lesson `## Gate`)
- URL opened: https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf (publisher page and JSTOR blocked, see table above).
- Access date/time: 2026-10-20 21:16:27 -03 (2026-10-21T00:16:27Z).
- Quote 1 (≤25 words), printed p.209, "Probable Inference (Usual)", paragraph 2: "Strictly speaking, the usual statement of probable inference as given above is elliptical." (13 words)
- Quote 2 (≤25 words), printed p.210, paragraph after the rule formula: "And this form of statement is not elliptical. It is the proper form of probable inference." (16 words)
- Quote 2 is the one grounding `teaches`.
- Caveat: the copy is a scan of the JSTOR PDF hosted on a university course site; quotes are OCR'd and eyeball-checked against the crop, not checked against the publisher's own text layer. Non-author verification should re-open the sample from the publisher or JSTOR if reachable.

## Findings
- F1 (source): The primary paper is openable only through the course-hosted scan; publisher (403) and JSTOR (challenge) are closed to this client. The DOI page yields metadata only and cannot ground `teaches`.
- F2 (teaches scope): Wilson's paper gives the interval and the argument for it; it does NOT evaluate coverage or compare with Clopper–Pearson. Any C1 claim about interval coverage must cite a different source. The row's scope is limited accordingly.
- F3 (relevance to C1): The paper defines the interval from the observed rate with the quadratic-root range (p.210). It states the Wald-type form is "elliptical" (p.209). This supports the framing that interval verdicts bound the true rate, not the observed rate. It does not supply an exact binomial interval.
- F4: `teaches` quote is grounded at printed p.210 (PDF p.3); the "elliptical" quote at p.209 (PDF p.2).

## Out of scope / not done
- No lane file written; no SOURCES.md edit; no knowledge entry; no S0?? number assigned (leave to integration owner).
- No live network model/endpoint calls; only public scholarly pages fetched.
- No corpus, plans/, or evidence files touched; no verification of attribution/state-check tooling.

## Installs / tools
- No installs or updates. Used pre-existing curl, pdftotext, pdftoppm, pdfinfo, tesseract (already on host). No pacman use.

## Artifacts
- Report: /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-25/build/SrcWilson1927.md
- Scratch (not in repo): /tmp/kengaku-r25-SrcWilson1927/ (PDF, PNG pages, OCR text, crops)

VERDICT: Wilson 1927 OPENED via course-hosted scan (sha256 c2fc82b5…8735); publisher/JSTOR blocked; one draft row (S0??, tier A, scope = Wilson's own interval statement, status queued) with two ≤25-word OCR-grounded quotes; no lane writes.
