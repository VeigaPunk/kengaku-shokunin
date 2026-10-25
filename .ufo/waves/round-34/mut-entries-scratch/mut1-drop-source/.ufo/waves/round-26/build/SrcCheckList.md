# C1 prior-art source: CheckList

Axis: novelty.

## Observed
- Paper fetched as real PDF bytes: https://aclanthology.org/2020.acl-main.442.pdf; accessed 2026-10-21T06:51:26Z; HTTP 200; 400,832 bytes; SHA-256 `98d15d259acf15136feed5cd5d4921b60cf313704a629901d115fe910fdb00e1`.
- ACL metadata: Ribeiro, Wu, Guestrin & Singh, *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*, Proceedings of ACL 2020, pp. 4902–4912; July 2020, DOI 10.18653/v1/2020.acl-main.442 (ACL Anthology page, accessed 2026-10-21).
- Quote (21 words): “An Invariance test (INV) is when we apply label-preserving perturbations to inputs and expect the model prediction to remain the same.” Location: §2.2, PDF p. 2 / proceedings p. 4903, extracted PDF text line 82; ACL 2020 version (July 2020).
- Teaches: capability-oriented behavioral testing of NLP models with MFT, INV, and DIR test types; INV tests whether a model prediction stays stable after label-preserving input perturbations.
- Tier recommendation: **A — primary** for the published INV/DIR behavioral-testing method for NLP model predictions. The paper is the primary ACL publication; the linked community-hosted GitHub code should not itself be tier A.
- The linked tool is `https://github.com/marcotcr/checklist`, inspected at commit `4e6e5e33a26f30c20ed602b2050f6c73e123cc23` (commit date 2023-09-26). `checklist/test_types.py:40,74` defines `INV` using `Expect.inv`; `checklist/expect.py:418-451` compares original and perturbed **predictions** (and confidence tolerance); `checklist/perturb.py:39` perturbs test input `data`.

## Inference / C1 verdict
- **No exact C1 prior-art match in this source or its linked tool:** they test invariance of NLP model predictions under input perturbation, not verdict invariance of an answer grader/extractor under response-format perturbation of model responses. This is adjacent method prior art for metamorphic invariance, not publication of C1's target construct.
- C1 should not claim novelty for metamorphic/invariance testing in general. This source alone does not settle the required full papers + PyPI/GitHub prior-art sweep or any novelty-score decision.

Remaining unknown: prior art outside this CheckList paper and the linked repository is not assessed here.
VERDICT: No exact C1 prior-art match; CheckList is adjacent metamorphic input-invariance prior art. Installs: none.