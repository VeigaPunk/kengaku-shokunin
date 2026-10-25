# C1 source opening — Tam et al. (2024)

- **Fetched source:** `https://arxiv.org/pdf/2408.02442` — accessed `2026-10-21T06:52:45Z`; HTTP `200`; final URL unchanged; fetched PDF SHA-256 `172930a8e9166ded9df95bb9ec41aafb7f43907969d14ea2dd05240d2c902f75`.
- **Version/date:** PDF header identifies `arXiv:2408.02442v3 [cs.CL]`, dated `14 Oct 2024` (PDF p.1). The ACL Anthology records publication in *EMNLP 2024 Industry Track*, Nov. 2024, pp. 1218–1236, DOI `10.18653/v1/2024.emnlp-industry.91`: https://aclanthology.org/2024.emnlp-industry.91/.
- **Verbatim quote (21 words):** “we use an LLM prompted to extract the final answer from the text, rather than relying on regex or string parsers.”
- **Exact location:** §3.4, “Evaluation method,” “Perfect Text Parser” paragraph, arXiv v3 PDF p.4 (extracted text line 122).
- **Recommended SOURCES tier:** **A — primary**, for the scope of what this paper reports and how its linked authors’ implementation works. This is not evidence of absence from all other prior art.
- **Teaches:** It compares LLM task performance across output-format restrictions, uses an LLM to extract answers, and measures parsing errors. Its companion repository (`https://github.com/appier-research/structure-gen`) includes `study_llm_parser.py`: `prompt_others` sends the same sampled responses to different parser models and `plot_results` compares parsed answers with Cohen’s kappa. `tasks/llm_parser.py::parse(response)` is parser tooling. These are relevant adjacent work.
- **C1 prior-art verdict (this source only):** **No.** The paper and inspected companion code do not report verdict-invariance testing of an unchanged answer grader/extractor under meaning-preserving and meaning-changing perturbations to the same stored raw responses. Their format comparisons vary model generation/prompting; parser-model agreement and parse-failure rates do not constitute C1’s response-level metamorphic regrading and invariance/sensitivity estimates. This source is adjacent, not the preregistered construct.
- **Remaining gap:** This source-scoped finding does not settle overall C1 novelty. Search results also surfaced a separate, potentially closer 2026 study, *Judge Reliability Harness* (https://arxiv.org/html/2603.05399v1); its method/tooling and any registry matches require independent review before a global novelty +1.
- **Installs/updates:** None.

VERDICT: Tam et al. (2024) is relevant adjacent primary prior art on format effects and answer extraction, but it does not itself publish C1’s fixed-response grader/extractor verdict-invariance audit.
