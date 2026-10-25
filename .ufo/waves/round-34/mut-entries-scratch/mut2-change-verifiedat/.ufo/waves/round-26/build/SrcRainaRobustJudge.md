# Source opening — Raina, Liusie & Gales (2024)

- **Fetch (observed):** `https://arxiv.org/pdf/2402.14016`; accessed 2026-10-21; HTTP 200; final URL unchanged; 1,281,498 bytes; SHA-256 `d10f97ce404e460004a35cd0ca4093f7bbd547230986280be1f5f4460fac9b12` (`curl --location --silent --show-error --output ... --write-out ...`; `sha256sum`).
- **Version/date (observed):** PDF title block identifies `arXiv:2402.14016v2 [cs.CL] 4 Jul 2024` (PDF p.1, extracted-text line 15).
- **Quote (verbatim, 13 words):** “a phrase δ of length L ≪ |x| is added to the original text x” — §4.1 “Attack Threat Model,” PDF p.3, extracted-text line 110; arXiv v2, 4 Jul 2024.
- **Recommended SOURCES tier:** **A**, scoped to the authors’ own adversarial-attack method and results on zero-shot LLM assessment: this is the original paper, meeting the lane’s A definition for an original paper. It is not primary evidence for response-extractor invariance.
- **Teaches:** §4–5 describes learning short concatenated phrases that perturb assessed natural-language inputs to raise a judge LLM’s scores/ranks, including transfer from a surrogate model; it evaluates attack success by candidate rank (PDF pp.3–6, §§4–5).
- **C1 prior-art verdict (this source):** **No.** It studies meaning-changing attacks to the judged text and resulting model predictions; it does not publish meaning-preserving response-format perturbations of stored judge outputs or verdict-invariance testing of a response extractor/grader. The method is adjacent at the broad “perturbation robustness of assessment” level, not the C1 construct.
- **Unresolved:** This single paper does not establish absence in the broader literature or PyPI/GitHub tooling registries; the pre-registration’s full papers-and-registries prior-art search remains necessary before any C1 novelty increase.
- **Installs/updates:** none.

VERDICT: Primary input-attack prior art; not prior publication of C1’s stored-response format-invariance audit.
