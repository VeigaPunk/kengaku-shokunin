# R36ScoutPriorArt — prior art for the C2 instrument pattern (kengaku r36 W1)

Question: is "a fixed-log pattern grader accepts a literal alternation of its expected outputs and leaves
boundary/validity requirements unenforced", found by running the task's own grader on synthetic
requirement-targeted candidates, novel, incremental or established?

Method: web_search for leads, then every cited hit fetched with `read` (URL below). Search-engine summaries were not
used as evidence; quotes come from fetched pages. Local artifacts of the fetches: ~/.omp session artifacts 83380 (ABC html), 83381 (TB paper html), 83697 (VerifierBench pdf).
Read-only: nothing in the lane except this file was written.

## The 6 strongest hits

### H1 — Agentic Benchmark Checklist (Zhu et al.), arXiv 2507.02825 — ESTABLISHES the "enumerate all answers" and "insufficient tests" classes
- URL: https://arxiv.org/abs/2507.02825 (abstract); full text https://arxiv.org/html/2507.02825v1 (§1, §5).
- Quote (abstract): "SWE-bench Verified uses insufficient test cases, while TAU-bench counts empty responses as successful."
- Quote (§5, check O.b.2, html line 563-564): "τ-bench also allows agents to list every possible answer, violating check O.b.2 and overestimating performance by 40%."
- Quote (§5, html line 369-370): "recommend formulating tasks carefully to prevent success by listing all possible answers (O.b.2) or guessing (O.b.3)."
- Overlap: O.b.2 is exactly "a grader that a literal enumeration of the expected answers passes"; O.e.1-e.3 cover missing edge cases. Method there is checklist + a few targeted experiments (KernelBench fuzzer, τ-bench empty agent), not "run the task's own grader on a requirement-by-requirement candidate battery".
- Confidence: high (fetched, quoted).

### H2 — Terminal-Bench paper (Merrill et al.), arXiv 2601.11868, App. B.4-B.5 — the benchmark owner's own audit names this exploit and scores TB as robust to it
- URL: https://arxiv.org/html/2601.11868v1 (Appendix B.4 "Adversarial Exploit Agent"; Table 3 in B.5).
- Quote (B.4): "generating all possible answers with the hope that tests might only check existence of a correct answer but not absence of wrong answers"
- Table 3 row (B.5): "I.b.2: Is robust against systematically listing all possible answers. | 1" (i.e. scored passing for the whole benchmark).
- Quote (Conclusion, line 625): "verifying that all properties tested have been adequately specified in the task description" — note the direction: tested-but-unspecified, the converse of "specified-but-unenforced".
- Overlap: the exploit class and the audit are established for TB; the blanket score `1` on I.b.2 is a per-benchmark judgement, so a concrete per-task counterexample (regex-log) is a new data point against it, not a new class.
- Confidence: high.

### H3 — Terminal-Bench / Harbor reviewer rubric `task-implementation.toml` (criterion `test_instruction_alignment`) — the "unenforced requirement" count is a published review criterion
- URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/docs/prompts/task-implementation.toml (criterion `test_instruction_alignment`); process in https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/docs/REVIEWING.md (steps 5-7: oracle/nop validation, `/cheat` adversarial trials).
- Quote: "every requirement in the instruction should have corresponding test coverage"
- Quote: "FAIL if tests introduce requirements that contradict or go beyond what the instruction describes, or if the instruction describes requirements that are not tested."
- Quote (criterion `reviewable`): "Hardcoded expected values without derivation are a red flag."
- Overlap: defines exactly the metric (instruction requirements with no enforcing test). Applied by an LLM rubric + a `/cheat` agent, not by executing a purpose-built candidate battery on the grader; REVIEWING.md calls the rubric "a first-pass signal, not a final judgment".
- Confidence: high (note: this is the TB3 repo's rubric; TB2 tasks predate it — [INFERENCE] about whether regex-log was ever reviewed against it).

### H4 — VerifierBench / Verifier4Verifier, arXiv 2610.28679 (2026-10-19) — mutation testing of verifiers is an established audit step, and it already found a TB grader defect
- URL: https://arxiv.org/abs/2610.28679 ; text https://arxiv.org/pdf/2610.28679v1.pdf (§2.3 check 6; Appendix B.1).
- Quote (§2.3, check 6): "Modify one check in the source verifier (DeMillo et al., 1978); some test case must then receive different valid decisions from the two versions."
- Quote (§2.3): "All 37 Terminal-Bench tasks are removed, 35 of them because its test-output parser counts skipped tests as passes"
- Quote (§2.3, check 5): "Verifiers that always accept, always reject, or accept only the reference solution must be exposed by negative cases, positive cases, and valid variants"
- Overlap: audit-by-mutating-the-verifier and trivial-baseline candidates are established practice (published 6 days before this round); the regex-log probe's candidates are requirement-targeted *candidate artefacts* against a fixed grader (equivalent to checking each grader assertion's kill-set), a close sibling of check 5/6. VerifierBench does not cover pattern-valued answers or TB task-level assertion coverage (its TB tasks were excluded wholesale for the parser defect).
- Confidence: high.

### H5 — EvalPlus (arXiv 2305.01210) and UTBoost (arXiv 2506.09289) — fixed visible tests accepting wrong candidates is the founding result of the field
- URLs: https://arxiv.org/abs/2305.01210 ; https://arxiv.org/abs/2506.09289
- Quote (EvalPlus abstract): "these test-cases can be limited in both quantity and quality for fully assessing the functional correctness of the generated code"
- Quote (EvalPlus abstract): "reducing the pass@k by up-to 19.3-28.9%"
- Quote (UTBoost abstract): "the manually written test cases included in these pull requests are often insufficient, allowing generated patches to pass the tests without resolving the underlying issue."
- Overlap: same phenomenon (finite visible fixtures accept candidates violating the spec), measured with generated tests and mutation-based input fuzzing; so "a grader's fixed cases under-constrain the spec" is textbook. Differences: they add tests to find false positives at benchmark scale; here the grader is the unit, the answer is a pattern (not code), and the output is a per-requirement enforced/unenforced map.
- Confidence: high.

### H6 — Terminal-Bench 2.1 `regex-log` (primary, instance-level) — the exact task is public and still carries the same fixture
- URLs: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/tasks/regex-log/tests/test_outputs.py ; .../README.md ; .../instruction.md
- Observed (command, 2026-10-25): `curl -sL .../terminal-bench-2-1/main/tasks/regex-log/tests/test_outputs.py | sha256sum` = `345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72`, byte-identical (`diff` empty) to the pinned round-36 capture `corpus/evidence/round36/tb2-regex-log/test_outputs.py`. Last commit touching it (GitHub API): `5fc7d3b91d 2026-05-05 "Move dataset files under tasks"` — a file move, no content change.
- Quote (test_outputs.py): "# Expected matches based on \"last date after a valid IPv4\" rule" followed by `expected_dates = [` (nine dates) and `matches = re.findall(pattern_text, log_text, re.MULTILINE)` / `assert matches == expected_dates`.
- Quote (README.md "Key Constraints"): "IPv4 addresses must be valid (decimal notation, octets 0-255, no leading zeros)" and "Dates and IPs must not be preceded or followed by alphanumeric characters (word boundaries)".
- Quote (README.md "Verification"): "The regex correctly matches dates in 26 different test scenarios" — the file has 25 `sample_logs` lines (round-36 receipt: 25-line fixed log), a small README/test mismatch, [INFERENCE] stale count.
- Overlap: README lists the validity/boundary requirements as constraints while the single assertion is `matches == expected_dates` on one fixed log: the TB maintainers themselves state the requirements, and the weakness persists in the current 2.1 release. I found no issue/PR/blog/paper auditing this (searches below); absence of hits is not proof of absence.
- Confidence: high on facts above; medium on "nobody else reported it".

## Searches that found nothing specific (so novelty is bounded, not proven)
- `Terminal-Bench 2.0 task regex-log verifier hardcoded dates weak tests audit task quality errors` — returned only task/spec pages (tbench.ai, TB2.1 repo, Harbor registry); no critique of the fixture.
- `regex synthesis benchmark overfitting ... alternation of examples` — only general regex-synthesis literature. Regex+ (Barbone et al., https://par.nsf.gov/servlets/purl/10336574) reportedly says optimising specificity only "gets 0 benchmarks correct, as all of the outputs are way too tailored to the inputs" — that quote came from a search-engine snippet; my direct fetch of the PDF timed out twice, so it is NOT a verified hit and is excluded from the six. It concerns synthesizer output, not grader false-accept.
- No published false-accept-rate figures found for regex/pattern-answer graders; ABC/UTBoost/EvalPlus report rates for code/answer graders only.

## Verdict on the observation
Decomposed:
1. "a fixed-fixture grader accepts a literal enumeration of its expected outputs" — ESTABLISHED (H1 O.b.2; H2 B.4; EvalPlus/UTBoost insufficient-tests line; VerifierBench trivial-baselines).
2. "requirements stated in the instruction that no assertion enforces" — ESTABLISHED as a review criterion (H3 `test_instruction_alignment`; ABC task/outcome validity), measurable with a traceability matrix.
3. "run the grader against requirement-targeted synthetic candidates / mutate the verifier and count survivors" — ESTABLISHED method (H4 mutation testing, V4V check 5/6; the round-35 thin-mutant protocol already priced it so).
4. "this particular grader (TB2 `regex-log`, still unchanged in TB2.1) does this, with the concrete list: literal 9-date alternation passes; leading-zero octets, digit-adjacent dates, 5/other-width years, month-length validity, Feb 29 permitting side unenforced" — NOT found in any searched source; INCREMENTAL, instance-level. It also contradicts the TB paper's Table 3 score of 1 on I.b.2 for this task (H2), which is the one publishable delta.

Do not claim methodological novelty. The defensible claim is: a new, executed, receipted instance within a published class, with a counterexample to the owner's self-assessment, and the pattern-valued-answer variant (agent writes a regex, grader applies it to one log) being under-covered in the literature found.

VERDICT: priorart-6-hits-novelty-incremental
