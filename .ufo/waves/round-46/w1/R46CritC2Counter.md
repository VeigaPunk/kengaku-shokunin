# R46CritC2Counter — C2 pre-data attack

## Axes
Depth (routed correction fidelity); calibration of the C2 admission predicate.

## Ranked finding

1. **False correction cell is invisible to leg A (real design defect; verdict impact conditional).** The gate treats a superseder as a repair when it has any captured, line-cited, defect-free anchor and `teaches` starts `supersedes S0NN —`; it does not check the truth of the rest of `teaches` or require that it describes the superseded defect. In a scratch clone, I changed S161's `teaches` to `supersedes S152 — the Dockerfile says no seed is run`. This is false: the captured Dockerfile runs `bash /app/setup.sh` (capture `corpus/evidence/round45/tb2-password-recovery/Dockerfile`, line 17; entry also quotes that line at `corpus/knowledge/tb2-password-recovery-grader.md:49`). The unmodified gate nevertheless reported S152 `repaired by=S161`, `live=0`, exit 0. This directly demonstrates that a false superseding-row cell passes leg A. It is **not demonstrated as a full `PREDICATE C2 pass`**: my constructed overall candidate still had one C-leg range defect, and the C2 counter returned fail. Therefore this is a plausible verdict-changing gap under the frozen repair intent, but not a reproduced end-to-end pass; do not count it as proven verdict-changing.

## Evidence / commands

Clone root verified as `/fast/scratch/hyaku/kengaku-r46/R46CritC2Counter/lane` (`git clone -q --shared ...`; `git rev-parse --show-toplevel`). All counter, fixture mutation, and gate runs below used the mandated envelope; each ended `local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

- Base: `python3 plans/round46_c2_verify.py --lane . --work "$S"` → PINS `3/0`; A live=8; B disagree=6; C bad=4, marks=0/5; D exit=0; `PREDICATE C2 fail`, exit 1.
- Candidate preparation: scratch helper appended superseders with captured line/range/word anchors and corrected predictor + errata; no frozen tool was changed. Candidate counter → A live=0, B disagree=0 (10 pass/6 fail), D exit=0, but C source_ranges_bad=1, so `PREDICATE C2 fail`, exit 1.
- False-cell mutation: scratch helper replaced S161 `teaches` with the false statement above. `python3 plans/anchor_line_check.py --lane .` → `ROW S152 state=repaired by=S161` and `ANCHORLINE ... defective=8 repaired=8 live=0`, exit 0.

Envelope evidence common to the above: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" <command>`; recorded starts/ends and unchanged digest in tool outputs. The attempt to run a diagnostic one-line Python command for the remaining C range was a syntax error and is not evidence.

## Not established

I did not establish an end-to-end false `PREDICATE C2 pass`; no claim is made for BOM/NUL/surrogate/very-long-line variants, deleting predictor prose, or capture swaps. No verdict-changing bypass is counted from these experiments.

## Smallest safe correction

Require the superseder's correction cell to state the actual repaired claim (for S152, a verifiable correction that the Dockerfile runs the seed), rather than treating the `supersedes` prefix plus a valid anchor as proof. At minimum, add a focused red selftest with a correctly anchored superseder whose `teaches` makes a demonstrably false assertion; ensure it cannot discharge the defective row. Any remaining C2-predicate adjustment belongs to the canonical judge.

VERDICT: c2-counter-bypasses-1-verdict-changing-0
