# xFinder prior-art source review

Axis: novelty (C1).

- **Opened primary bytes:** https://arxiv.org/pdf/2405.11874 — fetched 2026-10-21; HTTP 200; SHA-256 `4b1a8c60b6350c1dfd7fdf578b1d82ff7ca8e04a1bdfb033a69ee77ce0b28f74`.
- **Version/location:** PDF p.1, Abstract; arXiv v3 dated 2025-02-25 (paper marked “Published as a conference paper at ICLR 2025”).
- **Verbatim quote (23 words):** “As evaluation frameworks commonly use Regular Expression (RegEx) for answer extraction, models may adjust their responses to fit formats easily handled by RegEx.”
- **Recommended SOURCES tier:** **A — primary**, for the stated scope of xFinder’s empirical claims about answer-extraction errors and extraction/judgment accuracy; it is the authors’ peer-reviewed ICLR paper. Community artifacts are not A-tier.
- **Teaches:** Regex answer extractors can misread nonstandard model responses; xFinder is a learned key-answer extractor evaluated for extraction accuracy.
- **C1 prior-art verdict:** **No for the exact C1 construct; adjacent prior art.** The paper studies extraction errors on varied responses (§1, PDF p.2), reports extractor accuracy on held-out/generalization data (§5.1, pp.7–8), and augments training examples by varying answer phrasing (§4.3, pp.6–7). It does not publish paired, meaning-preserving perturbations of the same response followed by verdict-invariance measurement of a fixed answer grader/extractor. Its robustness/generalization claims are therefore related, not the C1 invariance audit.
- **Tooling cross-check:** The linked author GitHub repository and PyPI xfinder package expose an extractor/evaluator (e.g. `src/xfinder/eval.py::evaluate_single_item`, `src/xfinder/modules/answer_extractor.py::generate_output`) and extraction-accuracy examples; the reviewed material does not describe a perturbation-invariance test suite.
- **Remaining gap:** This finding covers xFinder only; it does not establish absence of the C1 construct in other papers or tooling registries.
- **Installs/updates:** None.

VERDICT: xFinder is A-tier, directly relevant extraction-reliability prior art, but it does not publish C1’s paired response-format verdict-invariance audit.
