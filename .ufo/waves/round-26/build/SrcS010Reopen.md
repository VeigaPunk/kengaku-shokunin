# S010 reopen — C1 prior art

- Source: Xu et al., “Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge,” arXiv:2602.02219v3 (last revised 2026-09-09; abstract HTML lines 115, 168–169).
- Accessed 2026-10-21. Requested URL `https://arxiv.org/abs/2602.02219`: HTTP 200; fetched 43,708 bytes; SHA-256 `e26408beac6830a5083a2869128c449ad34b99805c22ba6b31e351f4ac97a31d`.
- Full text `https://arxiv.org/html/2602.02219`: HTTP 200; fetched 281,257 bytes; SHA-256 `a89e2256f106c2a2daa72711175b6355951636a2f76e9db2e117dcc02aa49678`. The response identifies the v3 paper (v3/version metadata and `2602.02219v3` resources).
- **Method observed:** §3.1 (HTML line 383) balances score-option positions across multiple LLM evaluation runs using forward and reverse cyclic permutations (10 orderings for five scores); §4.3 (lines 475–483) evaluates balanced, fixed, and randomized orderings. §5.6 (line 1008) compares candidate rankings under balanced vs fixed rubric ordering and measures top-1 reversal.
- **Judge vs deterministic grader:** this is a study of LLM-as-a-Judge, not a deterministic grader or answer extractor. §4.1 says six open-weight models are evaluated (line 394); §4.2 names the six LLM judges (line 460). The output flip rate is a rank change after rubric-order perturbation, not response-parser verdict invariance.
- **Verbatim quote (13 words):** “rubric ordering alone flips the top-1 candidate on 15% to 41% of prompts” — §1, contributions, HTML line 344; v3, revised 2026-09-09.
- **Recommended SOURCES tier:** A — primary source for its own rubric-order position-bias method and results.
- **Teaches:** Balanced score-option/criterion permutations expose model-specific rubric-position bias and downstream ranking reversals.
- **C1 prior-art verdict (S010-specific): NO.** S010 does not publish verdict-invariance testing of a deterministic answer grader/extractor under response-format perturbations; it perturbs LLM judge rubric inputs and observes judge outputs/rankings. This does not settle prior art beyond S010; C1 separately requires a tooling-registry search (round-26-claims.md:92–96).
- C1 scope checked against `plans/round-26-claims.md:37–44,54–73`: response-format changes to stored `raw`, regraded through `extract_json_block` and deterministic grader functions.
- Installs/updates: none.

VERDICT: S010 is relevant perturbation/flip-rate precedent for LLM-as-a-Judge rubric ordering, but not prior art for C1's deterministic response-grader format-invariance construct.