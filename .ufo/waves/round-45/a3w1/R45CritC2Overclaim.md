# R45CritC2Overclaim — C2 overclaim review

Measured lane: `git -C /fast/scratch/hyaku/kengaku-r45/R45CritC2Overclaim/lane rev-parse HEAD` → `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (dispatch tip).

## Findings and corrections

1. **The C2 wording conflates “no separate predicate” with “case-free.”** Frozen claims §C2 lines 77–81 calls the grader “format-, case-, order-, count-free”; the landed entry repeats at lines 20–23 that it has “no format, case, order, count or uniqueness check.” But exact membership of the literal `8XDP5Q2RT9ZK7VB3BV4WW54` does constrain case and whole-line content: lowercasing it or joining it to other text fails. Distinction from `feal-linear` is real but within the same F1 family, not a new class: F1 means file constant/answer comparison; `password-recovery` tests one exact line, whereas `feal-linear` searches the whole file for 100 substrings. This is a meaningful mechanism variant and a fair **task-level** coverage move (the existing frontier was selecting an unread task in F1), not evidence of a new grader family.

   **Measured counterexample:** command: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/password_recovery_probe.py" --lane "$S/lane" --work "$S/probe-work"` (with `$S=/fast/scratch/hyaku/kengaku-r45/R45CritC2Overclaim`). Output: `constant-joined predicted=fail observed=fail tests=PF`; `password-eq predicted=fail observed=fail tests=PF`; final `cases=16 observed_pass=5 observed_fail=11 mismatches=0`; envelope `start 00:33:18`, `end 00:33:22 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. Both states contain the expected password as a substring, so they distinguish exact line membership from the prior 100-substring rule. The receipt/source facts are independently visible at `corpus/evidence/round45/password-recovery-probe.txt:10,19` and `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md:20-22`.

   **Smallest safe correction to entry:** replace “no format, case, order, count or uniqueness check” with “no separate format or case validation: exact whole-line membership necessarily fixes the answer’s characters and case; count, order, and uniqueness are not checked.” In the frozen-claim description, likewise replace “format-, case-, order-, count-free” with “no separate format/case predicate; exact-line membership, with no order/count/uniqueness constraint.” This preserves the actual contrast without implying a lowercase answer could pass.

   The “eleventh grader class exemplar” phrase is ambiguous, not evidence of a new class: `corpus/README.md:78` calls this the eleventh *task* and second F1 exemplar, while the round-43 histogram has F1 = “file: constant/answer compare” (`.ufo/waves/round-43/build/R43ConsiderThese/hist.md:3`), and its table classifies `password-recovery` F1 from the literal test assertion (`table.md:59`). Safer heading: “eleventh task grader; second F1 exemplar.” This is clarification, not a second substantive overclaim.

2. **Internet access is material and adequately disclosed.** The captured `task.toml:34` says `allow_internet = true`; the entry quotes it (`:52`), explains the public-repo shortcut (`Findings §3`), and S156 teaches the leak-channel implication. It matters because the pinned repository exposes the answer in `test_outputs.py`, while the verifier-execution-model says `/tests` is uploaded at verification time rather than being the agent’s task image (`corpus/knowledge/benchmark-verifier-execution-model.md:62-66`). The probe does not exercise a live fetch: it is explicitly offline and mounts a captured public file at `/pub` (`plans/password_recovery_probe.py:10-21,213-226`). The entry’s negative-space limitation that no agent/trajectory was run prevents this from becoming a claim that an agent actually fetched it. **No correction required** beyond keeping that distinction explicit.

3. **Tier A is supported.** SOURCES contract says A is primary/authoritative for its stated scope (`corpus/SOURCES.md:11-16`). S149–S156 are pinned primary task files, and their scopes are bounded to those files’ contents and task metadata, not broader validity claims. The probe’s host execution does not make the upstream-source rows secondary; it is reported separately as the lane’s own measurement. **No tier correction required.**

## Counter coverage

The frozen C2 counter was run on a clean shared clone at the measured tip:

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c2_verify.py" --lane "$S/lane" --work "$S/work"` (`$S` as above) → `checks=11 defects=0`, `PREDICATE C2 pass`, exit 0; envelope `end 00:31:24 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. Full output is retained in `R45CritC2Overclaim/c2-counter-run.txt`; probe output with complete envelope lines is in `R45CritC2Overclaim/probe-run.txt`.

**Impacted axes:** coverage (the task-level F1 extension is legitimate); calibration/claim precision (the only substantive correction is avoiding the false “case-free” implication); novelty (do not present this as a new class). No defect found in the internet disclosure, tiering, or probe’s advertised setup substitution.

VERDICT: c2-overclaims-1
