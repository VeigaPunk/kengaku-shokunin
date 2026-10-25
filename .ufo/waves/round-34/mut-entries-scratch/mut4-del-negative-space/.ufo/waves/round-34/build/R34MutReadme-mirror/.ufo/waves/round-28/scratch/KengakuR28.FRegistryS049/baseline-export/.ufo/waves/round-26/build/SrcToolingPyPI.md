# SrcToolingPyPI-4 — C1 prior-art, tooling registries (PyPI + npm), 2026-10-21

Method: every artifact below fetched 2026-10-21 06:54–07:02 UTC, urllib, UA `kengaku-r26-sourcetooling/1.0`;
URL, HTTP status, byte size, sha256 recorded per item (full bytes in /tmp/kengaku-r26-SrcToolingPyPI/).
PyPI HTML search endpoint BLOCKED: 4 queries (metamorphic, metamorphic+testing, perturbation, invariance+testing)
each returned an identical 3038-byte stub, sha256 32ed63159c77e21ee19ca1b9aa3213ccf0218eb59539560b132a8e68ef0e18ea, 0 package snippets — free-text sweep
redone via web_search over pypi.org (hits: pertpy, cpa-tools — single-cell biology, irrelevant); `cigate` and
`evalmut`/`llm-evalgate` verified by opening PyPI JSON + release bytes directly. No installs.

## 1. evalmut 0.1.0 — DIRECT PRIOR ART (verdict: YES)
- https://pypi.org/pypi/evalmut/json → 200, 14248 B, sha256 1595963783a1a76218a2325c2a911c531ebe7d9b34966c9165fbd61a6ef1ce18; v0.1.0 uploaded 2026-08-10.
- https://files.pythonhosted.org/packages/b0/42/d57ffbe3c5966b7563f077ba3eb6dd63c0b077a96f58cc79c17f529dedd9/evalmut-0.1.0.tar.gz → 200, 50245 B, sha256 b633c61734b94b33ad971be4b16951eb13524016b69115eeecc980766d03ad16 (== PyPI digest).
- Quote (README.md:61-63, "The two ways an eval lies"): "Inject an equivalent change (a trailing disclaimer after a complete answer, cosmetic whitespace, a JSON code fence); a sound grader must still pass it."
- Source: evalmut/operators.py:614 "EQUIVALENT MUTATIONS — the output changed but is STILL correct. A correct grader must hold; one that flips has a brittle spot"; operators `_trailing_disclaimer`:649, `_whitespace_noise`:674, `_json_code_fence`:697 (fence in/out), `_case_variant`:726; defect side `_near_miss_number`:255, `_garbage_answer`:328, `_blank_output`; polarity DEFECT/EQUIVALENT at evalmut/outcome.py:38-39.
- Tier: B (verified community-project release; direct evidence of shipped behavior, not independent validation). Teaches: grader-verdict invariance under equivalent (MP) format mutations + rejection of defect (MC) mutations, with polarity proven against declared case ground truth.
- Delta vs C1: evalmut mutates author-declared case outputs (synthetic GradeInput) to audit third-party grader checks; C1 perturbs sha-pinned stored model responses from the lane's own corpus with per-family CP95 intervals vs a 0.95 bar (incl. D1 last-block distractor). Core construct (grader verdict invariance under response-format perturbation, as tooling) is PUBLISHED.

## 2. checklist 0.0.11 (marcotcr) — verdict: NO for graders (model-side INV)
- https://pypi.org/pypi/checklist/json → 200, 9029 B, sha256 691111b2a1c7b02622b3329255ba70ce3440abdb3fbb1d45cc6691e165248243.
- sdist https://files.pythonhosted.org/packages/38/b3/8511f50025b9fc66f5feacf9eb2db044c321f4026b6937cb3820f29e9c1d/checklist-0.0.11.tar.gz → 200, 12082185 B, sha256 427cf87dbf47ce9f9ab059a9bbf393d9ebf967e266f8fca377420bd6995a95ac; v0.0.11 uploaded 2021-05-24.
- Quote (checklist/test_types.py:54-56, `class INV` "Invariance Test"): "Prediction probability threshold for invariance. Will consider pairs invariant even if prediction is the same when difference in probability is smaller than threshold."
- Perturbations (checklist/perturb.py:148 `add_typos`, :173 `remove_negation`, :318 `contractions`…) hit model INPUTS; INV compares model predictions. Canonical INV precedent named by the rubric; graded object is the model, never an answer grader. Tier B (community package source). Teaches: expectation-based invariance testing framework (the pattern C1 re-points at a grader).

## 3. giskard 3.0.1 (+ giskard-scan 1.0.1) — verdict: NO
- https://pypi.org/pypi/giskard/json → 200, 196983 B, sha256 df0498cc864274b8e4f9f2e39e1060b854f8eaa1f473855f4014a311f076dbd9; sdist https://files.pythonhosted.org/packages/b7/c0/93b1dcb7b47c142d9406234dd53718516887827f6a6c9b9e2aa9a8a1e4c3/giskard-3.0.1.tar.gz → 200, 12193 B, sha256 5f2d5901eb4a59e394ab93c9604acdf2a36a3e17e29ebc659f2e96a4b41dbab1 — shim `giskard_pypi_shim` (README.md:26,57): "Agent vulnerability scanner + RAG/quality evaluation — red teaming, prompt injection, jailbreaks & harmful content".
- https://pypi.org/pypi/giskard-scan/json → 200, 18760 B, sha256 50b6ea1084d2e2e86f3bd4cf594e93a477d34e7652111b79a80af842971d15b9; wheel https://files.pythonhosted.org/packages/c6/95/02bab6f0231def7d5c166a7b5dff092a622ab236ae46b5f339a30213a04b/giskard_scan-1.0.1-py3-none-any.whl → 200, 117394 B, sha256 71dd26ae5352f8870a538b84a94b12bf5c72547bce0cddd494b737c4f671b4b0; 67 entries (42 Python files inspected). Search hits concerned agent-scanner/generator/judge integrations; no response-perturbation grader/extractor audit located. Tier B (official project artifacts). Teaches: vuln-scanner framing of adversarial testing; no grader-invariance surface.

## 4. deepeval 4.3.1 — verdict: NO
- https://pypi.org/pypi/deepeval/json → 200, 850535 B, sha256 354e4964782c2c12e6b6a1c136e8f7b72fdb4bc39bb9fb3dba26e793e822fc06; sdist https://files.pythonhosted.org/packages/f8/32/7123fef688c50f06f77e72b62a31d82ca5f2dc70820e12355de01f670bb4/deepeval-4.3.1.tar.gz → 200, 1056961 B, sha256 0f0f1457cca315920b6e1c50876fabfda76e05981e91b9cf63e0a43a34e022b5.
- `grep -rn 'perturb|metamorph|invarian'` over sdist: only "metamorphic" inside an ARC benchmark question (benchmarks/arc/template.py:56) and "invariant" in telemetry comments — zero feature hits. Quote (PyPI JSON `info.summary`, deepeval 4.3.1): "The LLM Evaluation Framework". Metrics operate on test cases; no mutation loop over a grader. Tier B (community project source). Teaches: LLM-judge/metric evaluation of test cases.

## 5. promptfoo 0.124.1 (npm) — verdict: NO
- https://registry.npmjs.org/promptfoo → 200, 2916602 B, sha256 458f9ed137f8bf921f9314fac073cfb166895685a52a2381863e8e2e2a0c900f; tarball https://registry.npmjs.org/promptfoo/-/promptfoo-0.124.1.tgz → 200, 6700228 B, sha256 be3fe4dd4cd78e61a2fc81a8bcaaad1c8f29b63ebed16f08e629a5856f0c270f; latest 0.124.1 (2026-10-08).
- Quote (package/dist/src/main.js:20034): "Format validation: is-json, is-xml, is-sql" — deterministic assertions validate the MODEL's output format (evaluator is-json handler, dist/src/evaluator-Cjf-gFDb.js:2760-2769); redteam plugins attack the model. No perturbation/invariance testing of the assertion/grader itself. Tier B (vendor project artifact). Teaches: harness-level deterministic format assertions; no metamorphic loop.

## 6. math-verify 0.9.0 — verdict: NO
- https://pypi.org/pypi/math-verify/json → 200, 28454 B, sha256 e1ca42e4b1cdbbb1a2e11c8e68af3dd58de8c443c71f86123ccf9402f0b3b574; sdist https://files.pythonhosted.org/packages/4f/12/b8d13b581e110ac2f724a2351a8361a70fa36d057eb945d6379e8747c256/math_verify-0.9.0.tar.gz → 200, 60329 B, sha256 45ac6c61344ba056b9e99a660a4bc8d044ed408f730aed68c60435aa5eec4645; uploaded 2026-01-10.
- Quote (README.md:59): "Answer retrieval is done in format agnostic manner, with best effort to extract the answer." Ships an extractor (`src/math_verify/parser.py:465 extract_latex`, :573 extract_target_from_pred) + verifier (`grader.py:755 verify`) with fixture unit tests (tests/test_boxed.py), but publishes no perturbation/invariance audit of its own extractor-verdict stability. Tier B (community package source). Teaches: format-agnostic answer extraction design; closest "tested extractor" without metamorphic audit.

## 7. lm-eval 0.4.13 — verdict: NO
- https://pypi.org/pypi/lm-eval/json → 200, 95974 B, sha256 705690e204994d2ba60cfa7f092f5d64ab66c8bb71989364511be25d39a62791; sdist https://files.pythonhosted.org/packages/89/b1/cfcdf2a8c8b8e755ec7103a7d4b6f8673f7916641ca08df83412c531935b/lm_eval-0.4.13.tar.gz → 200, 3471075 B, sha256 f592269f21a5e173d7993ae01267f61fc84be393cee1f51779e3e104a70c967e; uploaded 2026-08-31.
- Answer extraction+scoring at lm_eval/api/task.py:403 `process_results`; bundled gsm_plus README.md:7: "evaluate the robustness of LLMs’ math reasoning capability by testing a wide range of question variations" — perturbations are of QUESTIONS (model robustness, third-party GSM-Plus), never of the harness's grader. Tier B (community project source). Teaches: harness consumes others' perturbations; extractor un-audited.

## 8. cigate 0.2.0 — verdict: NO (calibration-adjacent)
- https://pypi.org/pypi/cigate/json → 200, 15843 B, sha256 318b81e582a65cab39e5f3011ba751875cbb143fe17c6aefe7e936d1e1bac151; sdist https://files.pythonhosted.org/packages/62/0c/e56a006d335f0bcad532157c636498c87cc7580f1176c5a5f572bc6490e7/cigate-0.2.0.tar.gz → 200, 1114212 B, sha256 f363906a9c90812aef55a1101d8edd767fd7276b11512f511dc5fe2428cf4e2b; uploaded 2026-07-19.
- Quote (src/cigate/calibrate.py:45, `--perturb-judge`): "Simulate judge drift: degrade sensitivity/specificity on subjective axes." Gates merges on the CI lower bound of a bias-corrected LLM-judge score (docs/METHODOLOGY.md:38-40 "The confidence interval: adjusted-Wald delta method", :97 "flags drift when accuracy < 80% or κ < 0.70"). Perturbs the JUDGE (mock) to demo drift detection; no response-format invariance audit. Tier B (official project artifact). Teaches: CI-lower-bound gating precedent supporting the lane's CP95 bar practice (relevant to calibration axis, not C1).

## 9. llm-evalgate 0.6.0 (free-text discovery) — verdict: NO
- https://pypi.org/pypi/llm-evalgate/json → 200, 39041 B, sha256 b8b392ed3d3ababcefcaeaef3820b992908b5465237fd0ebf2e1f63b56aa7e8e; wheel https://files.pythonhosted.org/packages/8c/7e/302fc3c9e6f52214379c09ba408ce3ed5f6396a9456401c93e995d2c307f/llm_evalgate-0.6.0-py3-none-any.whl → 200, 70541 B, sha256 a3b8d1c97dd5e44b74aa550ad30b1dcfc2afc9c499e219ca2b31339872c3e622; 46 entries, zero perturbation files. "Eval gates with confidence intervals … a statistically honest regression gate". Tier C lead (calibration-adjacent only).

## C1 prior-art verdict (registry lane)
YES — the construct is published as tooling: evalmut 0.1.0 (PyPI, 2026-08-10) ships verdict-invariance testing of answer graders under equivalent response-format mutations (code fence, whitespace, trailing prose, case) plus defect-mutation sensitivity, and CheckList publishes perturbation-invariance (INV) testing for models. Per round-26 plan rubric leg (c): novelty HELD at 7; the C1 observable (stored-response population, per-family CP95 vs 0.95 bar, D1/G1/G2 families) remains recordable as the lane-specific instantiation. Recommended SOURCES tiers: evalmut B, checklist B, cigate B, giskard B, deepeval/promptfoo/math-verify/lm-eval B; llm-evalgate C lead.

VERDICT: evalmut 0.1.0 is direct tooling prior art for grader verdict-invariance under response-format perturbation → C1 novelty held at 7, observable recordable; no installs.
