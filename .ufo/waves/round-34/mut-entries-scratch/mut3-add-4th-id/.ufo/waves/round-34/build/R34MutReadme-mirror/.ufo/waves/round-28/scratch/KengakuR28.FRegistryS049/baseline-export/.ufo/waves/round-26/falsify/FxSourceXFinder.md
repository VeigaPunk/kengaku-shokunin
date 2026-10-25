# FxSourceXFinder — Q10 source/number re-read

Axes: source fidelity; numerical claim provenance; admission readiness.

## S044 — independently reopened

- Directly opened `https://arxiv.org/pdf/2405.11874`; the PDF is arXiv `2405.11874v3`, stamped **25 Feb 2025** on PDF p.1. The arXiv reader metadata says published 2024-05-20 (initial work metadata); this does not conflict with the v3 date.
- HTTP fetch: `curl --location --silent --show-error --output /tmp/fxsourcexfinder-arxiv-2405.11874.pdf --write-out 'HTTP_STATUS=%{http_code}\nEFFECTIVE_URL=%{url_effective}\n' https://arxiv.org/pdf/2405.11874` → HTTP_STATUS=200; EFFECTIVE_URL=https://arxiv.org/pdf/2405.11874. The fetch completed; the first combined shell call exited 1 only because its following `sha256sum` misspelled the PDF path (omitted `.pdf`).
- Corrected hash command: `sha256sum /tmp/fxsourcexfinder-arxiv-2405.11874.pdf /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt` → exit 0:
  - downloaded S044 PDF: `4b1a8c60b6350c1dfd7fdf578b1d82ff7ca8e04a1bdfb033a69ee77ce0b28f74`
  - local S047 receipt: `75db30f95088b9aa859cf80cc48430a13a3d42adb446410920413f9647f05f29`
- `corpus/SOURCES.md:66` records S044 as xFinder, tier A, limited to its own answer-extraction motivation/method (not general extractor accuracy), with location arXiv v3 (2025-02-25), Abstract, PDF p.1. Its URL is `https://arxiv.org/abs/2405.11874`; the lesson uses the PDF URL above.
- Exact located Gate quote, matching the opened PDF Abstract on PDF p.1 (23 words): “As evaluation frameworks commonly use Regular Expression (RegEx) for answer extraction, models may adjust their responses to fit formats easily handled by RegEx.” The wording, version/date, and location in `corpus/lessons/round-26.md:48` and `corpus/evidence/round26-sources/gate.md:6` match the PDF. No S044 quote/location contradiction found.
- Draft `grader-perturbation-audit.md:19-21` uses S044 only for the qualitative motivation that RegEx-oriented extraction can favor easily extracted responses, then explicitly disclaims general reliability evidence. This is within S044's scope; S044 does not establish this lane's audit outcomes or novelty.
- Number audit: the S044-dependent numbers are the version date (v3, 2025-02-25) and arXiv identifier; the draft does not reuse S044's abstract metrics. The opened abstract reports a 500-million-parameter smallest model, 93.42% extraction accuracy, 74.38% RegEx accuracy, and 97.61% judgment accuracy; none are used as draft evidence. Draft's 1964 population/results are its pinned local corpus/instrument; novelty 7 is attributed to direct prior art S045 / CheckList S048, not S044.

## S047 — local receipt

- `corpus/lessons/round-26.md:51` and `corpus/SOURCES.md:69` identify the local receipt and anchor it at base `f11bffbf`.
- `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt:19-20` reads `selftest: 18 checks, 0 failed` and `exit=0`; the local file SHA-256 is above. This supports 18, not the superseded 14-check count.
- No S044-dependent finding relies on S047's selftest number; it is a separate own-work source row.

LSP availability: no `lsp` device/server is exposed in the available tool routing; source-reference searches were literal fallback only. The quote and page/version facts above were checked against the directly reopened PDF, not treated as grep proof. No tools were installed.

Q10 source/number seat: **PASS**. Remaining admission unknowns outside this seat: Q13's actual registered-report support and the other required family/entry reviews.

VERDICT: PARTIAL — S044/S047 source and number evidence passes; overall admission is not established until Q13 support and the remaining required reviews return.