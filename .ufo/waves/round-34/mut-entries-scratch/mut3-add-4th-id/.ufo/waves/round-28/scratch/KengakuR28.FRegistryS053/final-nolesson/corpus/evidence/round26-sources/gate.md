# Round 26 source-opening receipts — accessed 2026-10-21

| row | URL or own-work path | exact location | located quote (≤25 words) | receipt |
|---|---|---|---|---|
| S043 | https://aclanthology.org/2020.acl-main.442.pdf | §2.2, PDF p.2 / proceedings p.4903 | “An Invariance test (INV) is when we apply label-preserving perturbations to inputs and expect the model prediction to remain the same.” | build/SrcCheckList.md:6-11; HTTP 200, sha256 98d15d259acf15136feed5cd5d4921b60cf313704a629901d115fe910fdb00e1 |
| S044 | https://arxiv.org/pdf/2405.11874 | v3 (2025-02-25), Abstract, PDF p.1 | “As evaluation frameworks commonly use Regular Expression (RegEx) for answer extraction, models may adjust their responses to fit formats easily handled by RegEx.” | build/SrcXFinder.md; HTTP 200, sha256 4b1a8c60b6350c1dfd7fdf578b1d82ff7ca8e04a1bdfb033a69ee77ce0b28f74 |
| S045 | https://pypi.org/pypi/evalmut/json and its digest-verified 0.1.0 release tarball | README.md:61-63, §The two ways an eval lies | “Inject an equivalent change (a trailing disclaimer after a complete answer, cosmetic whitespace, a JSON code fence); a sound grader must still pass it.” | build/SrcToolingPyPI.md:10-16; JSON sha256 1595963783a1a76218a2325c2a911c531ebe7d9b34966c9165fbd61a6ef1ce18; tarball b633c61734b94b33ad971be4b16951eb13524016b69115eeecc980766d03ad16 |
| S046 | https://docs.python.org/3/library/re.html | Python 3.15.0, Regular expression syntax → special sequence backslash-s | “This includes `[ \t\n\r\f\v]`” | build/SrcPythonJsonRe.md:9-12; HTTP 200, sha256 59d4a9c0e254047735e4756fe684dafa323c4d9b24ab055b4d1997534be268a0 |
| S047 | corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt | final result line at f11bffbf | “selftest: 18 checks, 0 failed” | build/ScribeRepairRows.md; round-start receipt and outside spot-check confirm 18, not S037's earlier 14 |

The self-reporting tooling's claims are scoped to shipped mechanism, not independent validation. No package
was executed or installed. Fetched copies are in the source seats' /tmp directories; hashes identify the
observed bytes, while located quotes are the re-open authority for dynamic pages.

## Bounded prior-art search

Question: is response-format metamorphic testing of answer graders already published as method or tooling?
Paper openings: CheckList, Segura survey, Chen survey, S010 rubric bias, lm-eval trenches, xFinder,
Sclar format sensitivity, Let Me Speak Freely, One Token to Fool LLM-as-a-Judge, Raina robustness (10).
Additional docs/project openings: Python json/re docs and Math-Verify README. Registry sweep opened nine
PyPI/npm project families (evalmut, checklist, giskard, deepeval, promptfoo, math-verify, lm-eval, cigate,
llm-evalgate); GitHub seat opened seven sources. These are overlapping scoped lists, not a deduplicated
PRISMA count. Identified/screened count by bounded paper list = 10/10; included as new paper rows = 2;
8 not separately registered (general method/model-side attacks or already registered S010). Registry families
9/9 screened, one included as direct-prior-art row S045; eight not separately registered (adjacent scope,
already registered cigate, or weak lead). GitHub's independent evalmut discovery corroborates S045.
PyPI free-text endpoint returned a challenge stub, so direct package JSON/releases and site search replaced
it; this is not a complete registry search. Stop: a direct match was found; no global absence claim remains.
No novelty +1. Full opened-source detail and rejects remain in build/Src*.md, never converted into invented
source rows.

## Pre-admission correction S048 (2026-10-21)

Supersedes S043's initial location in the table above. URL https://aclanthology.org/2020.acl-main.442.pdf,
reopened by FxSourceCheckList on 2026-10-21, HTTP200, same SHA-256 98d15d259acf15136feed5cd5d4921b60cf313704a629901d115fe910fdb00e1.
Quote (21 words): “An Invariance test (INV) is when we apply label-preserving perturbations to inputs and expect the model prediction to remain the same.”
Exact location: **§2.2, PDF p.3 / proceedings p.4904**, not PDF p.2 / p.4903.
Evidence: `.ufo/waves/round-26/falsify/FxSourceCheckList.md:7-10`, whose page-specific text extraction
found no quote on p.2 and the quote on p.3. TierA scope and teaching unchanged. S048 is a new mined row,
used by the round-26 lesson; the knowledge draft cites S048 before admission. Round totals therefore gain
one superseding source row (not one new external source). No old immutable source cell was rewritten.
