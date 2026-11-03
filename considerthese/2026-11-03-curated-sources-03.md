# kengaku: third curated source to consider after hyaku

Date: 2026-11-03

**Status: unassimilated future reading after hyaku.** This is a candidate, not adopted methodology, verified capability or permission to run an evaluation. No source code, model or benchmark was executed.

## POSIX: response sensitivity beyond answer accuracy

**Primary source:** Chatterjee et al., [POSIX: A Prompt Sensitivity Index For Large Language Models](https://aclanthology.org/2024.findings-emnlp.852/), Findings of EMNLP 2024, pages 14550–14565, DOI 10.18653/v1/2024.findings-emnlp.852. The [proceedings PDF](https://aclanthology.org/2024.findings-emnlp.852.pdf) identifies November 12–16, 2024. Read on 2026-11-03; this is the proceedings edition, not a latest-model claim.

**Why this gap:** Existing coverage includes grader validity, contamination and temporal cohorts. POSIX instead compares response log-likelihood under intent-preserving prompt variants. Its unit is model sensitivity, not whether an answer is correct. That distinction could prevent unchanged pass rates from hiding a changed response distribution.

**Reading path:** Section 3.1 definitions of intent alignment; Section 3.2 sensitivity definition; Section 3.3 interpretation; Section 4 experimental design; Limitations on page 14558. Read the assumptions before the result tables.

**Domain question:** Could two prompt wrappers produce the same accuracy while differing materially in response stability?

**Possible later exercise, original proposal:** After hyaku, design a small paper comparison with three deliberately equivalent wrappers and one meaning-changing negative control. Freeze the response set, tokenizer, model identity and likelihood-access requirements. Specify separate columns for answer correctness, contract compliance and likelihood sensitivity. Have kotoba review equivalence; keep capability measurement here. Do not select a wrapper from the same cases used to report its advantage.

**Limits and rights:** Proposed intent alignment is not demonstrated invariance. Tokenization and likelihood availability matter; comparisons grow quadratically with variants. Low sensitivity does not establish correctness or safety. ACL's [copyright policy](https://aclanthology.org/faq/copyright/) places post-2016 ACL material under CC BY 4.0; attribute the paper. Code and underlying datasets require separate license checks. Source title, author-repository alias and identifier were absent from the reviewed registry and both previous curation batches.
