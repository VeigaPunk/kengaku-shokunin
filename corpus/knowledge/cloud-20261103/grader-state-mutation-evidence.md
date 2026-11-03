# Kengaku knowledge lesson 5: A correct reward can leave the wrong state

## Aim

Treat an evaluation oracle as software with both a return value and side effects. Test whether a grader preserves the episode it measures, whether its verdict matches known answers, and whether the integration uses the grader's output as intended. A correct value at one boundary does not guarantee a correct label at a later boundary.

## Case: the second reader sees the reference solution

In an October 2026 preprint, Junjie Chen audits an agent-evaluation harness built around τ-bench. The benchmark's `Env.calculate_reward()` first captures the agent's terminal database hash. To construct the ground-truth hash, it resets the database and replays the reference solution, but does not restore the original database before returning. The reward computed using the earlier agent-state hash is correct; the live database now contains the reference solution's state. [1, §§1, 4.1, 5]

The problematic label arises at an integration boundary. The upstream τ-bench runner consumes the reward returned by that call and does not reread the changed environment; the paper explicitly says that runner is unaffected. The author's separate harness, however, scores again after the session ends and rereads the database left by the first call. Its second read can mistake the reference state for the agent's result. The upstream side effect and the author's second read jointly produce this failure; the source does not establish that upstream scores are inflated. This is an accidental measurement defect, not evidence of an agent deliberately exploiting it. [1, §§1, 4.1]

The minimal counterexample is a constructed episode in a task requiring database writes: the agent writes nothing and says goodbye. The archived integration grades it as a database pass; the repaired path does not. This makes a false positive visible without attributing intent to an agent. The discovery on the original code and later validation by injected variants are separate evidence, not two independent discoveries of the same incident. [1, §4.1]

## Correction is replay, not a new model experiment

The authors replayed each recorded tool call against a clean database and compared the resulting terminal state with a reference hash. They did not regenerate the model episodes: the paper says the benchmark did not expose a deterministic seed and the provider did not offer immutable model versions. Replay changes the measurement of the recorded trajectories; it does not say how a fresh model run would behave. [1, §4.1]

Across the 4,320 recorded episodes, archived database-pass labels numbered 4,194; corrected replay yielded 2,883. Separately, overall success changed from 94.3% to 65.5%. Database pass and overall success are different measures: do not treat the two database counts as numerators for the overall-success percentages. The correction is also not a constant adjustment across agents: in the studied matrix the reported changes differ and the agent with the highest point estimate changes; neither the archived nor the corrected comparison resolves a single winner. These are conditional results for that matrix, not a universal adjustment for τ-bench. [1, §4.1, Table 4]

The paper reports two fidelity checks: all 33,402 observed tool-output strings matched the archive character for character, and all 137 step-limit episode labels, which did not traverse the defective scoring path, were reproduced. These checks support fidelity of the recorded tool-call replay on those observations; they do not reproduce the original model sampling or independently validate every aspect of the benchmark. [1, §4.1]

## What the audit detected and where it stopped

The audit combines five state-integrity invariants with three known-answer controls. The invariants ask about state preservation, repeat and order behavior, exception cleanup, and the state at session end. The controls test failure on no-op or output-only episodes, success of a reference solution, and acceptance of a valid alternative output. State checks and verdict checks answer different questions: a pure grader can be wrong, while a mutating grader can initially return the right value. [1, §§3.2, 4.1]

The authors injected 21 variants across three targets, giving 63 variant–target combinations. A differential gate judged 57 separable; the suite detected 54 of those 57, not 54 of 57 naturally occurring defects. The same variant was missed on each target: the oracle swallowed an internally raised exception, so the exception-path check recorded the probe as not applicable rather than a violation. The other six combinations were unresolved by the separability gate, not demonstrated safe. All variants were author-constructed, so the figures measure this particular battery rather than detection probability for unknown defects. [1, §§3.2, 4.1]

A portability attempt on a second independently implemented framework, AppWorld, did not transfer: the authors could not externally reconstruct the reference state needed for a valid positive control under its interface. The package does not distribute that framework's task data or reproduce those probes. The preprint and repository are author-produced sources, not independent confirmation of the results. [1, §§3.6, 4.3, 6; 2]

## A practical reasoning sequence

1. Specify the graded state, the expected verdict, the reference construction, and which component reads which state at each time. Record the oracle's contract, including whether it may mutate state.
2. Capture a comparable signature of the agent's terminal state before and after scoring. A changed signature violates a purity contract even if the returned reward is correct. Include action history and other relevant state, not only a convenient database field.
3. Include known negative and positive cases: an episode that omits required writes must fail, while a verified reference solution must pass. Include an allowed alternative when the task permits one.
4. Score repeatedly and vary ordering on fresh, controlled environments. Check both state and verdict. Agreement on repeated scoring is insufficient by itself: a stable grader can consistently return a wrong result.
5. Exercise interrupted or failing scoring paths and verify both cleanup and exception propagation. Treat an inapplicable probe separately from a successful check, especially if the defect could suppress its precondition.
6. If correcting archived outcomes, replay recorded actions from a clean initial state and compare observable outputs with preserved records. Report mismatches and limits. Do not describe action replay as regenerating model trajectories.
7. Publish distinct numerators and denominators for database checks and end-to-end success, with the task, framework, version, and caller boundary. Avoid extending a finding about one integration to a different runner without evidence.
8. Inject plausible faults and validate that the controls can distinguish each one from the baseline. Report separable, missed, and unresolved cases; do not treat a finite synthetic battery as a population-wide detection rate.

This sequence is a proposed design, not a claim that the lesson ran these checks.

## Practice: hypothetical falsifiable controls

The following examples are invented. Each names an observation that would support or reject the stated claim under its specified setup; they are not results from the paper.

1. **Purity:** A database hash is `H1` before grading and `H2` after, with no agent action between. A promise that scoring preserves this database is falsified even if the returned pass/fail is correct.
2. **No-write negative:** A task requires a new order entry. An agent says it created one but makes no write. If this episode passes the database criterion, the negative control exposes a false pass; a correct grader should reject it.
3. **State and verdict:** A scorer returns fail on an unfinished task both times, but its first call silently inserts a reference record. Repeat verdict equality passes, yet state preservation fails. Record both measurements.
4. **Known valid solution:** A verified reference performs all required actions and produces the allowed outputs. If the scorer rejects it under the same task specification, the positive control fails; this does not by itself say which component is defective.
5. **Valid alternative:** A rubric permits either `yes` or `YES`. A scorer accepts the reference `yes` but rejects otherwise identical `YES`. The accepted-alternative control exposes a stricter rule than the stated contract.
6. **Stable wrong result:** A scorer always returns pass for a verified no-write negative on every repeat and in every order. Its verdict is stable, but the known-answer control still fails. Repeatability alone is not correctness.
7. **Exception suppression:** A test injects a failure during reference construction. The oracle catches it and returns normally, leaving the exception-path probe unable to observe a raised error. Mark that probe inapplicable or failed as designed, not a clean pass; independently inspect state and require the intended error contract.
8. **Clean replay versus regeneration:** The recorded calls are replayed from the same initial database and reproduce recorded tool outputs. This supports fidelity for those calls. A newly sampled model conversation is a different trajectory and cannot be called a replay of the original episode.
9. **Separate denominators:** In a hypothetical 100 episodes, 90 pass the database check but only 80 meet every overall criterion. Database pass rate is 90/100; overall success is 80/100. Neither numerator may silently substitute for the other.
10. **Caller boundary:** A reward call returns the correct fail while mutating the database to the reference state. Caller A uses that returned fail; caller B scores again by rereading the mutated database and returns pass. The second caller is wrong in this example; it does not follow that caller A's result is wrong.
11. **Ordering:** Two independent fresh episodes produce expected outcomes when scored alone, but B's verdict changes only when A was scored first through a shared cache. The order-invariance claim is falsified; test cache isolation and save state between calls.
12. **Fault-battery accounting:** Of 12 injected cases, 9 are separable and 7 detected. Report 7/9 separable cases, with 2 separable misses and 3 unresolved, not 7/12 as a validated detection rate or 9/9 as full coverage.
13. **Replay mismatch:** A clean replay yields a different tool response from the preserved observation at step 4. The proposed replay fidelity claim is not established for that trajectory; investigate the initial state, tool version, and recorded arguments before interpreting its corrected label.
14. **No upstream extrapolation:** An author's post-run reread is proven wrong in a test, while the upstream runner consumes the correct first reward and performs no reread. The evidence supports the former integration's defect; it does not establish inflated scores for the upstream runner.

## Takeaway

A grader has two obligations: produce a sound verdict and preserve any state its callers reasonably rely on. Test both against known controls and trace the precise read and write boundaries. Replaying recorded actions can repair labels for those trajectories, but neither the replay nor a passing synthetic fault battery proves fresh model performance or correctness of a different integration.

## Sources and scope

1. Junjie Chen, “When Agent Evaluation Becomes Unreliable: An Empirical Study of Oracle Failures and Configuration-Dependent Measurement in an LLM Agent Benchmark,” arXiv:2610.16067v2, 21 October 2026, especially §§3.2, 3.6, 4.1, 4.3, 5–6: https://arxiv.org/html/2610.16067 . The paper is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); this lesson paraphrases and synthesizes it rather than reproducing the text.
2. Author's SimGlot repository, README and artifact documentation, accessed 3 November 2026: https://github.com/JunjieChen0/SimGlot . The repository identifies the study code as MIT-licensed and notes that the frozen episode records and model-served outputs have separate terms and distribution caveats. This lesson did not acquire or copy the code, archives, or outputs.

This lesson is an original synthesis of author-reported evidence. It selects, interprets, and reorganizes the paper's findings and adds hypothetical cases. No model, dataset, API, or system runs were performed for it.

## Manual review record

An independent reviewer manually assessed the 14 hypothetical controls as follows:

1. Mutation violates the stated purity contract.
2. A no-write database pass is a false pass under the stated task.
3. A stable verdict can mask state mutation.
4. Rejecting a verified reference fails the positive control; the cause remains unknown.
5. Rejecting the specified valid alternative violates the rubric.
6. A stable wrong verdict is still wrong.
7. Exception suppression is not a clean success for the exception-path check.
8. Fidelity of recorded-call replay is not regeneration of a model trajectory.
9. Database pass is 90/100 and overall success is 80/100 in this example.
10. The correct-return caller and the later rereading caller have different outcomes.
11. The shared-cache example falsifies order invariance.
12. Seven of nine separable cases are detected, with two misses and three unresolved; 7/12 is only an inclusive descriptive count, not the separable detection rate.
13. The mismatch blocks an unqualified replay-fidelity claim.
14. A defect in the post-run reread does not establish an upstream runner defect.

This record describes manual reasoning about invented examples. No model, dataset, API, or system tests were run.
