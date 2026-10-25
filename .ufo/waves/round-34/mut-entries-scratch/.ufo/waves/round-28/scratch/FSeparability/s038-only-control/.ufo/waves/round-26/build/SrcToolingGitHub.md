# C1 tooling prior-art scout — GitHub

Axis: novelty (C1). Searched GitHub with `answer extraction robustness`, `metamorphic testing LLM evaluation`, `grader fuzz`, and `autograder metamorphic` (`site:github.com` web searches). Access date for source bytes: 2026-10-21. All sources below are community or first-party repository artifacts, never Tier A.

**Verdict: YES, prior art exists at the published method/tooling level.** `evalmut` explicitly tests whether a sound grader still passes equivalent output changes, naming cosmetic whitespace and JSON code fences. The companion PyPI scout independently confirms v0.1.0 mutates synthetic declared case outputs, not a frozen stored-response corpus or CP95 families (`SrcToolingPyPI.md:10–16`). ROGUE separately documents a response-artifact re-grade probe. Under `plans/round-26-claims.md` §C1 lines 92–96, hold novelty at 7; the lane-specific P1/family/interval observable remains distinct. This report supplies the GitHub evidence; see `SrcToolingPyPI.md` for registry findings.

- **egnaro9/evalmut — direct prior art.** Recommended Tier **B**, for the repo's own documented tool behavior (not independent validation). `README.md`, §“The two ways an eval lies”, lines 70–76; `main` (repo pushed 2026-10-20): [README](https://raw.githubusercontent.com/egnaro9/evalmut/main/README.md). Access 2026-10-21; HTTP 200; SHA-256 `fc61efbbd9464766dce8583753c9643d9029b90acb9ef719ef7557bd88c86bb5`.
  Quote: “Inject an equivalent change (a trailing disclaimer after a complete answer, cosmetic whitespace, a JSON code fence); a sound grader must still pass it.”
  Teaches: probe false rejection of known-equivalent response changes as well as missed defects; directly overlaps C1 format-robustness method.
- **nguiaSoren/ROGUE — close response-artifact prior art.** Recommended Tier **B**, for its own probe design. `docs/research/judge_artifact_robustness.md`, §“The gap this closes”, lines 7–10; `main` (repo pushed 2026-08-03): [source](https://raw.githubusercontent.com/nguiaSoren/ROGUE/main/docs/research/judge_artifact_robustness.md). Access 2026-10-21; HTTP 200; SHA-256 `e12c909e568ca0716deab015bbf926063b6b2b394b9418e0fa2dad58327c82ce`.
  Quote: “superficial, harm-preserving edits to the graded response that move the verdict without changing what the response says”.
  Teaches: re-grade a labeled response slice under benign artifacts and quantify verdict/error-rate shifts; safety-judge/content artifacts, not specifically JSON extraction or serialization.
- **maobupa/multi-agent-autograder — adjacent.** Recommended Tier **C** lead for C1. `README.md`, §“Perturbation Testing”, lines 245–263; `main` (repo pushed 2026-02-10): [README](https://raw.githubusercontent.com/maobupa/multi-agent-autograder/main/README.md). Access 2026-10-21; HTTP 200; SHA-256 `b6ba35589cf91d6e73b6c637a73c72afc822c609428e366a335a15c4d7984acb`.
  Quote: “Tests grading robustness under code transformations”.
  Teaches: compares grades of original vs. perturbed student programs (including whitespace and semantically equivalent statement reorder), not model-response formatting.
- **parag-labs/metamorph — adjacent.** Recommended Tier **C** lead. `README.md`, §“Why”, lines 40–44; `main` (repo pushed 2026-09-21): [README](https://raw.githubusercontent.com/parag-labs/metamorph/main/README.md). Access 2026-10-21; HTTP 200; SHA-256 `e5e27784d88e85941db7ac2d195f63b3c27c58fbfbc2ee2ba209f74da3ff0061`.
  Quote: “the same question answered differently when rephrased”.
  Teaches: metamorphic invariance of model answers under prompt changes; tests the model, not the grader/extractor.
- **steven-b-cho/llmorph — adjacent.** Recommended Tier **B** for the official artifact of its stated ICSME’25 paper; not a grader-invariance source. `README.md` lines 1–9; `main` (repo pushed 2026-10-06): [README](https://raw.githubusercontent.com/steven-b-cho/llmorph/main/README.md). Access 2026-10-21; HTTP 200; SHA-256 `961e70b60f92dbaca299a112cbbd7a4431be952d4b307831db82d7435f5df4ff`.
  Quote: “LLMorph is a tool to automatically test Large Language Models (LLMs) using Metamorphic Testing (MT)”.
  Teaches: metamorphic robustness testing for NLP models; output satisfaction is judged after task/input relations, not grader-parser format stability.
- **drdezarza/metamorphic-llm-evaluation — adjacent.** Recommended Tier **C** lead. `README.md` lines 5–12; `main` (repo pushed 2026-01-12): [README](https://raw.githubusercontent.com/drdezarza/metamorphic-llm-evaluation/main/README.md). Access 2026-10-21; HTTP 200; SHA-256 `5831970f694c25a9527a453e40ade7647742f2d407eab1ae0b651baa5e8f1f8c`.
  Quote: “assessing semantic invariance in LLM reasoning, systematically evaluating model responses across eight metamorphic relations”.
  Teaches: model-response semantic consistency across prompt/reasoning variants; no grader/extractor format perturbation described.
- **openai/monitorability-evals — adjacent.** Recommended Tier **B** for the official repository's released eval-data schema, not C1 grader robustness. `README.md` lines 28–35; `main` (repo pushed 2026-08-17): [README](https://raw.githubusercontent.com/openai/monitorability-evals/main/README.md). Access 2026-10-21; HTTP 200; SHA-256 `9f25531cc7596effd8aec273ad2724bf99fc5b38e20434049348d6233c35f434`.
  Quote: “there are two rows with the same ID: one that is perturbed, one that is unperturbed”.
  Teaches: paired prompt-side intervention examples and answer-evaluation prompts, not perturbations of stored raw answers to test extractor invariance.

No tools installed or updated.