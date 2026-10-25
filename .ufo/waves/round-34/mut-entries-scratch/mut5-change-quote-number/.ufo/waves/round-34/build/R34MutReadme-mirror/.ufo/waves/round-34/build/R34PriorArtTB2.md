# R34 prior-art check: TB2 evaluator wording

Axes: prior-art novelty (instrument pattern) and coverage (the pinned task-specific grader).

## Hits

1. **DNA Chisel** — https://github.com/Edinburgh-Genome-Foundry/DnaChisel — Published Python sequence constraint/optimization library with translation-preservation and windowed GC constraints; a close analogue for static sequence checks, though not the exact ordered-subsequence task rule.
2. **DNA Chisel paper** — https://doi.org/10.1093/bioinformatics/bty558 — Describes a general-purpose DNA sequence optimizer with constraint/objective evaluation; establishes the broader sequence-verification pattern as published work.
3. **Codon Context Optimization in Synthetic Gene Design** — https://arxiv.org/abs/1508.03428 — Published codon-context optimization and evaluation of coding sequences; relevant to translation/codon-level assessment, not evidence of the exact TB2 grader.
4. **An exploratory in silico comparison of open-source codon optimization tools** — https://link.springer.com/article/10.1186/s12934-023-02230-y — Compares existing codon optimization tooling and its sequence-quality evaluation, including translation and GC-related measures.
5. **CodonTransformer: a multispecies codon optimizer using context-aware language models** — https://www.nature.com/articles/s41467-025-58588-7 — Published codon design/evaluation work reporting GC and codon-profile metrics; related instrumentation, not the benchmark's specific checker.

## Evidence and limits

- Frozen claim says C1 opens the pinned `protein-assembly` evaluator (`tests/test.sh`, `tests/test_outputs.py`) and grounds it against `environment/antibody.fasta` and `environment/pdb_ids.txt`: `plans/round-34-claims.md:24-37`.
- Frozen wording explicitly characterizes the delta as coverage of a TB2 task's own scoring code, with canonical coverage unchanged: `plans/round-34-claims.md:66-69`.
- Web search returned the DNA Chisel repository and codon-optimization comparison/paper links above; arXiv API query returned `Codon Context Optimization in Synthetic Gene Design` at `https://arxiv.org/abs/1508.03428v1` (tool output title/link). The API query was broad and its response included irrelevant results; it is discovery, not exhaustive literature review.
- These sources support that static translation/GC constraint evaluation and codon-sequence scoring are established patterns. The search did not establish prior publication of the exact conjunction *translation + ordered-subsequence + GC-window* as a reusable grader, nor did it establish whether a particular hit includes ordered-subsequence validation. Do not claim novelty for that instrument pattern.

**Wording implication:** describe the entry as coverage: reading and grounding a pinned Terminal-Bench 2.0 task's own evaluator against its expected artifacts. State clearly that the static-constraint-checker instrument pattern is not method novelty; do not imply invention of translation, subsequence, or GC-window checks.

VERDICT: priorart-tb2 5 hits, novelty=no-claim
