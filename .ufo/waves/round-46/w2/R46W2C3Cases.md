# R46W2C3Cases — C3 case-table falsification

Axes: **coverage** (requirements/mechanisms exercised), **case fidelity** (recipe actually generates named state), **reproducibility** (same-state re-grade and receipt repeat).

## Evidence / repro

Cloned the frozen landing commit into `/fast/scratch/hyaku/kengaku-r46/R46W2C3Cases/lane`; checked top-level equals that clone and HEAD is `42d5043afac952fcb43bf4798757785dd258cf85`. Ran the full frozen probe, not stage-only, via the required envelope:

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" python3 "$S/lane/plans/polyglot_c_py_probe.py" --lane "$S/lane" --work "$S/work"`

Captured full stdout+envelope in `R46W2C3Cases/full-probe-envelope.txt`. Output: `exit=0`; `cases=18 observed_pass=7 observed_fail=11 mismatches=0`; `regrade cases=18 differ=7`; envelope end exit 0 and local-bin digest unchanged. This independently reproduces the committed receipt’s observed verdicts and re-grade count. The probe runs both grading calls against the same `work` tree (`run_case`, lines 390–393); the grader compiles `/app/polyglot/cmain` (captured test_outputs.py:23–25), after its one-time listing check (lines 17–18). Thus all seven first-pass states re-grade as F because the first grading call leaves cmain; this is real same-state non-idempotence, not just a prediction.

## Counterexamples / defects

1. **A stated instruction requirement is not represented by a discriminating case (coverage defect).** `instruction.md:7` says f(0)=0, f(1)=1, etc. The only graded N values are 42, 10, 0 (captured grader: `test_outputs.py:27`). `wrong-value` perturbs 42; `n-parsed-differently` varies parsing on 42/10 but matches at 0; lookup-table uses all three expected literals. Nothing exercises N=1, although the entry summarizes this as the requirement to print the kth Fibonacci number and the probe labels `fib-kth`. A candidate returning correct values for 0/10/42 but wrong at 1 still passes; this is a gap in the instruction-derived behavioral claim, not a defect in reproducing the grader’s exact verdict. The measured grader’s acceptance is necessarily only its three fixed points.
2. **`both-print` lacks a row which tests it, as the entry itself acknowledges.** The case table has `c-only` and `python-only`, each failing because one language is invalid, and `wrong-value` changes both outputs; none keeps both source forms valid and makes just one runtime’s stdout wrong. Therefore no case demonstrates the separately stated “both of these should print” behavior. At the underlying grader level, the conjunction is visible in `test_outputs.py:44`; coverage of its independent Python/C comparisons is incomplete. This is distinct from the N=1 hole above.
3. **Verdict-tuned overlap reduces mechanism isolation.** `wrong-value` is tagged only `fib-kth` but its C leg also creates cmain, so its re-grade fails on the listing rather than demonstrating the wrong-value mechanism on repeat; receipt nevertheless shows `regrade=same` because the first grade already failed. More generally every first-pass F is regrade=same, which says nothing about whether that failure is stable for its named reason. Stage-check confirms recipe state only, not which runtime/output predicate decided it. The normal first-grade F remains useful, but re-grade attribution should not be read as independently validating each named mechanism.
4. **Toolchain tag is not a behavioral instruction requirement.** Line 9 describes the author’s toolchain (“I’m using…”), not a tested version constraint. Marking `toolchain` “not exercised” is prudent and should not count as a coverage defect; however a requirement map that treats every tag uniformly can confuse descriptive context with an acceptance condition.

## Recipe fidelity

The landing receipt’s states are consistent with the recipes. The frozen stage-check receipt (`w1/R46ExecC3Probe/polyglot-c-py-stagecheck.txt`) reports all 18 `match=yes`, including oracle/lookup source, extra-file and cmain listings, empty bytes, and directory-in-place. My full run then exercised the actual grader and matched every frozen prediction. No recipe/state-name mismatch found.

## Smallest safe correction

Do not alter the frozen probe/table or claim this disproves the grader’s three-case verdict. In any successor claim about the instruction’s broader Fibonacci behavior, add a held-out N=1 discriminator and a valid dual-language source whose Python and C outputs differ (so each side’s comparison is isolated); label the inference as limited to sampled points. Keep “toolchain version” as disclosed environment context, not an unmet normative requirement. For current C3, report the two coverage limits explicitly; the re-grade finding survives.

VERDICT: c3-case-defects-2