# Chen et al. (2018) — C1 prior-art source

- **Work:** Tsong Yueh Chen et al., “Metamorphic Testing: A Review of Challenges and Opportunities,” *ACM Computing Surveys* 51(1), 4:1–4:27 (2018), DOI [10.1145/3143561](https://doi.org/10.1145/3143561).
- **Open copy fetched:** University of Wollongong Research Online item: https://ro.uow.edu.au/articles/journal_contribution/Metamorphic_Testing_A_Review_of_Challenges_and_Opportunities/27764520?file=50531136
- **Fetch record:** public PDF-preview endpoint `https://ro.uow.edu.au/ndownloader/files/50531136/preview/50531136/preview.pdf`; access date **2026-10-21**; HTTP **302 → 200** (`application/pdf`; 786,787 bytes). Final S3 path: `https://s3-ap-southeast-2.amazonaws.com/figshare-production-eu-uow-previews4887-ap-southeast-2/50531136/preview.pdf` (temporary signed query omitted). SHA-256 of fetched bytes: `f4314f395151e620f52f3597d87c93a0753dd2a1f17b8a4b6b45cccd17987866`.
- **Version/date:** institutional repository copy whose article body labels itself “Manuscript submitted to ACM”; UOW item history says posted **2024-11-15**; article published **2018**. The PDF includes a UOW repository cover (PDF page 1); article pagination follows it.

## Quote (13 words)
> “MT was thus recognized as a promising approach for alleviating the oracle problem.”

Exact location: **§2.1**, printed article p. 4 / fetched repository PDF p. 6, extracted-text line 81; submitted-manuscript copy, UOW item posted 2024-11-15.

## Tier and teaching
- **Recommended SOURCES tier: B — secondary**, for the stated scope of established metamorphic-testing method and oracle-problem framing. It is a survey, not primary evidence for C1’s specific grader audit.
- **Teaches:** Metamorphic testing uses relations across related inputs and outputs to check software behavior when a single-run test oracle is unavailable.

## C1 prior-art verdict (this source only)
- **Exact answer-grader/extractor response-format audit: No.** The survey presents general metamorphic testing, including machine-learning-classifier applications (§4.1), but does not publish testing of an answer grader/extractor under response-format perturbations or such a tool. Full-text search of the fetched PDF for `grader|extractor|response-format|language model|NLP|natural language|answer` returned no matches; relevant framing in §§1–2.2 and §4.1 was read.
- **Scope qualification:** this is conceptual prior art for metamorphic/invariance-style testing generally, not an exact C1 disclosure. C1 novelty should be limited to the specific application to stored model-response grading and its perturbation/measurement design, not metamorphic testing itself.

Installs: none.

VERDICT: B-tier general-method prior art; no exact C1 grader/extractor response-format audit in this survey.