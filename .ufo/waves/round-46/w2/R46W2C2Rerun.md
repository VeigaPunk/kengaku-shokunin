# R46W2C2Rerun — C2 frozen counter rerun

## Axis: depth

### Predicate
Clean `--no-local` clone at `42d5043afac952fcb43bf4798757785dd258cf85` (clone top and HEAD verified; see receipts) under the prescribed envelope:

- Command: `python3 plans/round46_c2_verify.py --lane "$S/lane" --work "$S/work"`
- Output: `PINS total=3 mismatched=0`; `A anchorline live=0 repaired=8 base_rows=149 base_missing=0 base_changed=0 ok`; `B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok`; `C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok`; `D selftest exit=0 ok`; `checks=4 defects=0`; `PREDICATE C2 pass`; exit 0. Envelope output had `local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged` (not invalid).
- `python3 plans/anchor_line_check.py --selftest` under envelope printed RED `rc=1 want_rc=1`, GREEN `rc=0 want_rc=0`, JUNK `rc=1 want_rc=1`, `SELFTEST pass`; exit 0 and envelope unchanged.

### Controls
Replayed all five committed C2 controls with `claims/stage2_controls.py`'s C2 clone/tool-overlay/transforms, in separate clean clones, under the envelope; each clone HEAD was `64ba8385ea10af1b78d367dcb242b92d97062af7`. Every control printed `PREDICATE C2 fail`, exit 1, so 5/5 fail as required. Outcomes match stage-2 frozen receipts for the measured predicates: nothing `live=8/disagree=6/ranges_bad=4/errata=0`; inplace `live=5/base_changed=3/disagree=6/ranges_bad=4/errata=0`; junk supersede `live=11/disagree=6/ranges_bad=4/errata=0`; splitlines `live=8/disagree=4/ranges_bad=4/errata=0`; errata-only `live=8/disagree=6/ranges_bad=4/errata=5`. Full captured outputs and commands are in `receipts/controls.txt`.

### Comparison and caveat
The prompt-designated `.ufo/waves/round-46/integrate/tip-c2.txt` does not exist in the lane; the integration directory contains `c2-landing.txt`, which records the same C2 predicate output and pass at commit `e9d201455c3774921aa5dfc287f07b4b9f113e76`. My rerun at the requested final TIP matches its predicate lines and numeric values exactly. The absence of the named `tip-c2.txt` prevented literal comparison to that path; used `c2-landing.txt` as the available integration record. Rerun receipt and selftest output: `receipts/counter.txt`, `receipts/selftest.txt`.

No tools installed or updated.

VERDICT: c2-rerun-predicate-pass-controls-failing-5/5
