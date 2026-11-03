# Primary-source openings, 2026-11-03

Opened after reviewer freeze d7af088c78c5b469cc89f6f0018b050cafff3379, before first-answer commit cd0797c349d45cf7d7f81607b62b229bcdcc91ba. Web reads only; no full HTML/PDF/source capture saved or redistributed.

S240: official HumanEval evaluation.py opened on master, then pinned raw b9453e8f1865df0a0057a1383767caa400acfbcf (git ls-remote returned that master). Functions estimate_pass_at_k and evaluate_functional_correctness, raw displayed lines11–33 and70–82. Anchor: "Calculates 1 - comb(n - c, k) / comb(n, k)." Caller inspected independently: per-task counts, mean, every-task n>=k filter. Code read, not executed.

S241: Yao et al., tau-bench arXiv2406.12045v1 (17June2024), https://arxiv.org/html/2406.12045v1 section3 Pass^k metric, displayed lines179–182. Anchor: "all $k$ i.i.d. task trials are successful, averaged across tasks." Read displayed paired formulas and their iid qualification, not merely abstract/reviewer summary. Author-reported metric, not independently replicated empirical results.

S242: Chen et al. arXiv2107.03374v2 abstract (14July2021), https://arxiv.org/abs/2107.03374v2. Anchor: "measure functional correctness for synthesizing programs from docstrings". Opened, but excluded as sole support for detailed finite-pool/selector/validity conclusions because abstract does not establish them. The official implementation and metric section are the actual method support. No claim paper itself is false; rereading full method could support a future separately scoped use.
