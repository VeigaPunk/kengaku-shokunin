# C1 novelty prior-art review

**Scope/axis:** C1 novelty only (mapped to coverage/constructs); calibration is not adjudicated here.

## Counterexample

C1’s core observable—whether a grader’s verdict remains stable under meaning-preserving perturbations—uses an established metamorphic/invariance-testing method, not a new construct:

- **CheckList (ACL 2020), published method + open-source tool:** the paper defines INV as “label-preserving perturbations to inputs” for which “the model prediction [is expected] to remain the same.” It also defines DIR perturbations whose label is “expected to change in a certain way.” This covers C1’s F1–F7/D1 invariance and G1–G2 sensitivity pattern at the method level. Opened paper and implementation: [ACL paper](https://aclanthology.org/2020.acl-main.442.pdf), [GitHub](https://github.com/marcotcr/checklist).
- **JudgeSense (arXiv:2604.23478v3, dated 2026-09-18):** an evaluator robustness benchmark asks whether “a judge returns the same verdict when the same request is worded differently”; it evaluates verdict agreement across equivalent prompt wordings and reports item-level instability. This predates this round’s registration. [Paper](https://arxiv.org/html/2604.23478).
- **Judge-LS (arXiv:2606.14278v1, dated 2026-06-12):** its protocol states, “A reliable judge should preserve its preference under label-preserving language transformations.” It perturbs answer-pair presentations, measures judgment/correctness flips, and reports intervals. This is published evaluator-response robustness testing, not merely ordinary model accuracy testing. [Paper](https://arxiv.org/html/2606.14278v1).
- **Probatio (`probatio-llm` on PyPI + GitHub):** its documentation defines metamorphic relations as semantics-preserving changes that “do not change the verdict,” with per-relation violation rates; its test example applies `@format_jitter` around an LLM-app verdict. PyPI records version 0.1.0 uploaded 2026-09-06, before round registration. [PyPI](https://pypi.org/project/probatio-llm/0.1.0/), [release JSON/timestamp](https://pypi.org/pypi/probatio-llm/json), [GitHub](https://github.com/Lexieli666/probatio).

## Boundary and ruling

None of these is an exact copy of C1’s intervention on committed `raw` response bytes through this lane’s `extract_json_block` + grader, its frozen four-file population, or its exact F1–G2 family definitions. Those are legitimate lane-specific implementation and measurement contributions. But C1 preregisters novelty of the *construct*—verdict invariance under response perturbation—and explicitly says published method/tooling means novelty stays at 7 (round-26-claims.md:37–44, 92–96). CheckList establishes the method; JudgeSense/Judge-LS establish evaluator-judgment robustness suites; Probatio establishes existing tooling that reports metamorphic verdict invariance, including formatting jitter. A narrower implementation does not restore construct novelty under that frozen rule.

**Smallest safe correction:** retain the completed audit and its observable, but record C1 as a lane-specific application of established metamorphic/invariance testing and hold **novelty at 7**; do not claim +1. No change to the harness or C2/Q13 follows from this prior-art finding.

**Impacted axes:** novelty held at 7; coverage/constructs receives no independent claim this round; calibration unaffected.

**Search/open coverage:** opened CheckList’s ACL paper and GitHub tool, JudgeSense and Judge-LS papers, and Probatio’s PyPI project/JSON plus GitHub repository. The Forus judge-perturbation article was found but its page fetch returned HTTP 429, so it is not relied on.

Installs: none.
VERDICT: Hold novelty at 7; prior art defeats C1’s preregistered construct-novelty leg, while the lane-specific measurement remains useful.