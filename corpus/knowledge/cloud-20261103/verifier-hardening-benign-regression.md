# Kengaku knowledge lesson 10: A verifier must preserve valid paths

## Aim

Judge a hardened verifier on two different obligations: reject demonstrated exploits and preserve legitimate solutions. A reference solution passing is evidence about one path, not proof that diverse valid paths remain open. Track the exact verifier snapshot and the provenance of every patch before drawing a conclusion.

## Case: a guardrail that missed legitimate CUDA paths

Ziqian Zhong and colleagues' hacker–fixer loop alternates attempts to exploit a verifier with patches intended to block them. Its intended solver guardrail checks that legitimate work still passes. In the KernelBench study, however, the researchers substituted the deterministic reference solution for a diverse solver during patch validation. That saved effort but checked only the path the reference actually exercised. [1, §§3–4.2]

The loop was run across KernelBench tasks sharing evaluation infrastructure, but the reported held-out case examined here is **task 001**, square-matrix multiplication. The reference did not use PyTorch's inline compilation path. A defense that obstructed stack inspection also broke that legitimate path, yet the reference still passed. A second defense, involving a fresh thread for each trial, interfered with valid solutions that created their own cuBLAS handles because their context did not carry across trials as expected. Other legitimate handle-use patterns could behave differently. [1, §4.2 and Appendix E.3]

The raw loop output illustrates why “zero attacks succeeded” is not enough. In Table 2, raw iteration 11 accepted **94% of 49 Gemini 3.1 Pro benign attempts** and **22% of 50 Claude Opus 4.7 benign attempts**. These rounded percentages describe the paper's specified model, snapshot, corpus, and reward rule. They do not describe every raw snapshot: raw iterations 8 and 13 each show **0% benign acceptance for both models**. The prose in §4.2 summarizes the raw iteration 8–13 results as 0–22%, which conflicts with the table's 94% Gemini value at iteration 11. Appendix E.3 itself also names 94% and 22%. Retain the table's distinctions rather than silently reconciling the discrepancy. [1, Table 2, §4.2 and Appendix E.3]

During iteration 11, a pool synchronization imported shared defenses. The fixer separately checked a synthetic inline-compilation solution, noticed the breakage, and narrowed that defense. Later pool synchronizations reintroduced the broader pattern and overwrote this interim repair. The remaining thread-related restriction could still reject some valid handle-using solutions. The later **post-loop** relaxation was a separate operation: a fixer saw the verifier and one failing legitimate solution, and relaxed both over-restrictive checks. The same relaxation was applied to snapshots 8, 11, and 13. Table 2 reports 98% benign acceptance for Gemini and 92% for Claude after this relaxation at each of those snapshots. [1, §4.2 and Appendix E.3]

For those snapshots, Table 2 also reports 0% observed attack success on its fixed held-out attack sets, both before and after the post-loop relaxation. The sets are finite and the figures are not a guarantee against future or adaptive attacks. Table 2 describes 133 hint-prompted attacks for its stated hinted evaluation and 49 unhinted attacks per model; benign denominators are 49 Gemini and 50 Claude. The paper generated submissions once and rescored the same submitted kernels across verifier snapshots. This measures how those fixed submissions fare against different verifiers, not whether a model improved across iterations. Attack success used a reported reward of at least 12×, while a benign pass used at least 0.5×, so the two rates have different definitions and populations. [1, §4.2 and Appendix E.2]

The paper's 12× attack threshold was chosen to avoid counting some 10–12× numerically lossy TF32 submissions that might be legitimate. A reported “benign pass” combines verifier acceptance with the stated reward threshold; it is not a complete independent proof that every accepted candidate is correct, or that every failure was an over-restriction. There is no evidence in this case that the changes were adopted upstream. [1, Table 2]

## A practical reasoning sequence

1. Define the legitimate task and the verifier's acceptance contract. Name valid implementation families and boundary conditions, including paths the reference does not exercise. Keep correctness, performance, and security criteria distinct.
2. Preserve a small, independently reviewed set of legitimate solutions as negative controls for false rejection. Include distinct compilation, library, resource, concurrency, and input paths when relevant. Document why each is valid and which criterion it tests.
3. Record exploit examples as positive controls for undesirable acceptance. Specify attacker visibility, feedback, success threshold, time budget, and denominator. Label disputed cases rather than forcing them into a clean category.
4. Freeze each submitted solution and each verifier snapshot, and record the relation between them. Compare the same submissions under the same conditions when the question is the verifier change. If submissions or attacker information change, report that as a different comparison.
5. For each proposed patch, record its source, diff or change description, parent version, intended exploit, and effects on both control sets. Run preservation checks after shared-pool merges and synchronization, not only after local edits. Investigate conflicts rather than assuming the latest sync retains an earlier repair.
6. Evaluate new and adaptive attackers separately from the fixed corpus. Report the attack and benign results together, with counts, exclusions, thresholds, uncertainty and known limitations. A zero numerator in a finite sample is an observation, not proof of immunity.
7. Hold a release decision when valid paths fail or provenance is unclear. A targeted relaxation can be a candidate fix, but re-evaluate exploit controls and valid-path coverage on the exact resulting snapshot; do not claim adoption or deployment without evidence.

This sequence is proposed reasoning, not a report that tests were run for this lesson.

## Practice: invented evidence packages

The examples below are hypothetical and do not add results to the paper. “Accept” means accept only the explicitly stated bounded conclusion, not approve deployment.

1. **Reference alone.** Package: a patch rejects 12 known exploits, while the sole reference solution passes; no other legitimate implementation was checked. **Decision: Hold.** Exploit rejection and reference compatibility are established for those examples, but preservation of other valid paths is untested.
2. **Negative control finds a regression.** Package: a separately reviewed inline-compilation solution gives correct outputs and meets the published performance rule before a patch, then fails because a dependency needed by compilation is unavailable; the reference still passes. **Decision: Reject the claim of full valid-path preservation.** Investigate the restriction and retest the precise patch.
3. **Fixed submissions, changed verifier.** Package: 40 saved benign submissions are rescored unchanged; 32 pass snapshot A and 38 pass snapshot B under the same rule, with recorded build settings. **Decision: Accept** a six-submission, 15-percentage-point increase on this fixed set, subject to review of failures. **Reject** the claim that the model became better: no new model submissions were generated.
4. **Changing test population.** Package: snapshot A rejects 3 of 30 attacks; snapshot B rejects 28 newly generated attacks from a different procedure out of 30. **Decision: Hold** a causal comparison of defenses. The populations changed; run matched fixed-submission checks and report the fresh attack campaign separately.
5. **Finite zero.** Package: 0 of 25 prespecified fixed attacks succeed against a named snapshot. **Decision: Accept** that observed zero in this corpus. **Reject** “the verifier is secure against all attacks.” Seek varied, independently generated and adaptive attempts within an explicit budget.
6. **Adaptive discovery.** Package: after observing the patched verifier and receiving feedback, an attacker constructs a novel submission that receives a passing reward without doing the required task; logs and independent review confirm it. **Decision: Reject** the claim that the patch resists that attack. The earlier fixed-corpus result remains an accurate but narrower historical observation.
7. **Denominator and threshold confusion.** Package: 4 of 20 attacks achieve the attack threshold, while 18 of 30 legitimate submissions meet a different benign threshold. **Decision: Accept** 20% observed attack success and 60% benign pass for those respective sets. **Reject** treating their numerators or denominators as interchangeable, or calling the gap a single accuracy score.
8. **Pool regression.** Package: local patch P restores a valid library-handle solution; a later shared-pool merge creates snapshot Q. Q's manifest omits P, and the same negative control fails on Q. **Decision: Reject** a claim that P's protection survived the merge. Trace the changed lines and revalidate a reconciled snapshot against both exploit and benign controls.
9. **Relaxation with incomplete security evidence.** Package: patch R restores 9 of 10 independently validated legitimate paths, but the team reruns only benign tests and assumes all earlier exploit blocks survive. **Decision: Hold.** Run the defined attack controls on R, and investigate the remaining valid-path failure before claiming the tradeoff is acceptable.
10. **Disputed ground truth.** Package: a fast solution is rejected and its author calls it legitimate; reviewers have not established whether its numerical behavior meets the task's tolerance. **Decision: Hold** classification as a false rejection until the contract and independent checks resolve the tolerance question. Do not automatically count it as either valid or malicious.
11. **Bounded preservation evidence.** Package: a versioned patch passes 25 independently reviewed legitimate examples across four documented implementation families, blocks all 20 specified exploit controls, and has a reproducible parent and merge record. **Decision: Accept** those observed results for that exact patch and environment. **Hold** a universal preservation or security claim; families, edge cases, and adaptive attacks remain finite or untested.
12. **Missing provenance.** Package: a report says the relaxed verifier passed all controls, but its hash, parent, and relation to the deployed candidate are missing. **Decision: Hold** any conclusion about the candidate. Identify the exact artifact and rerun or trace the recorded checks before attributing results to it.

## Independent tabletop review

An independent reviewer checked the source claims and manually assessed the 12 invented evidence packages above. The review was a tabletop judgment of the stated evidence and decisions, not a model, dataset, API, tool, or system test, and not a formal gate or admission. The reviewer reported the following outcomes:

1. Hold: the reference alone does not establish preservation of other valid paths.
2. Reject the full-preservation claim when the validated inline-compilation path fails.
3. Accept the bounded increase of 6 submissions, or 15 percentage points, and reject a model-improvement claim.
4. Hold the causal comparison when the attack populations differ.
5. Accept the observed 0/25 result and reject a universal-security claim.
6. Reject resistance to the independently confirmed adaptive exploit.
7. Accept 20% attack success and 60% benign pass with their separate denominators and thresholds.
8. Reject the claim that the demonstrated valid-path protection survived the pool merge.
9. Hold the tradeoff judgment until exploit controls and the remaining legitimate failure are investigated.
10. Hold the false-rejection classification until the contract and evidence resolve the disputed tolerance.
11. Accept the bounded observations and hold the universal claim.
12. Hold attribution to the candidate until its identity and relation to the checked artifact are established.

## Takeaway

A verifier is useful only if its defenses and its legitimate-solution coverage are both examined. This case shows how a reference-only guardrail missed valid CUDA paths, how a shared sync could undo an interim repair, and how a later relaxation recovered acceptance on a fixed evaluation while retaining zero observed successes on that particular finite attack corpus. It does not establish universal security or upstream adoption.

## Sources and reuse

1. Ziqian Zhong, Ivgeni Segal, Ivan Bercovich, Shashwat Saxena, Kexun Zhang, and Aditi Raghunathan, “Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops,” arXiv:2606.08960v1, 8 June 2026, especially §4.2, Table 2, and Appendices E.2–E.3: https://arxiv.org/html/2606.08960 . Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This lesson is an original synthesis and changes the source's presentation by selecting, interpreting, and reorganizing the case, explicitly noting its internal numerical inconsistency, and adding hypothetical practice packages. No source code or dataset is reproduced.
2. Authors' implementation repository, Apache-2.0: https://github.com/few-sh/harden-v0 . This link identifies the implementation; no repository code is copied into this lesson. Repository contents can change, so the historical numerical claims are attributed to the paper.

The lane already covers verifier design generally. The bounded novelty is this specific reference-only guardrail, the model- and snapshot-specific preservation results, the overwritten interim fix, and the separately applied post-loop relaxation, not the general idea of checking false rejections.
