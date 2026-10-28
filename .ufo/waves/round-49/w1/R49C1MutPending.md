# R49C1MutPending — blocked/pending/never-returned accounting

## Axes and freeze gate

Axes: **calibration** (C1 trace-accounting sensitivity) and **control false-pass**.

Verified before measurement in the committed lane tree:

```text
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 3a548330c4899c6c5df34168a44a59f66828ce74 9d2900af41e4d1fc6022eff99010436fde6dbd93
3a54833 ancestor of freeze: YES
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
```

Created one shared clone at `/fast/scratch/hyaku/kengaku-r49/R49C1MutPending/lane`; asserted `rev-parse --show-toplevel` equals that path, checked out exactly `9d2900af41e4d1fc6022eff99010436fde6dbd93`, and observed a clean worktree. The freeze predates this probe. **Stage 2 is absent**: `plans/round49_c1_verify.py` and its controls/receipt pins are not in the frozen tree. No scored R49 counter, control, or claimed-work run was made.

## Mutant and bounded detector

Targeted the inherited, digest-pinned trace-accounting helper `plans/round46_c1_verify.py::analyse()` at the smallest behavior-bearing point: the final loop that accounts for an unfinished syscall still pending at EOF. Mutant: replace `for head in pending.values():` with `for head in ():`; all other bytes unchanged.

The detector loads source bytes directly and supplies one synthetic strace record for an outside-`d` `openat` left `<unfinished ...>` at EOF. It reports the touched path and the resulting refusing-fence classification (`READ` when the touch is observed, `clean` when suppressed). This tests the exact pending-at-EOF branch; it is not a scored counter receipt.

Exact commands and actual output (all measured against `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`):

```text
sha256sum lane/plans/round46_c1_verify.py
 ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508  lane/plans/round46_c1_verify.py
python3 /fast/scratch/hyaku/kengaku-r49/R49C1MutPending/probe_pending.py lane/plans/round46_c1_verify.py
PENDING calls=1 touches=1 hits=[('openat', '/root/fx/pad/sibling/outside')]
REFUSED-FENCE-PENDING classification=READ
DETECTOR_EXIT=0

sha256sum lane/plans/round46_c1_verify.py
b0d22b7981ddc3fa65341a00d3886fdb67e45984d18f4b5d9b7927bc61180743  lane/plans/round46_c1_verify.py
python3 /fast/scratch/hyaku/kengaku-r49/R49C1MutPending/probe_pending.py lane/plans/round46_c1_verify.py
PENDING calls=0 touches=0 hits=[]
REFUSED-FENCE-PENDING classification=clean
DETECTOR_EXIT=0

# Restore, after asserting the clone top-level equals $D:
git -C "$D" checkout -- plans/round46_c1_verify.py
sha256sum lane/plans/round46_c1_verify.py
ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508  lane/plans/round46_c1_verify.py
python3 /fast/scratch/hyaku/kengaku-r49/R49C1MutPending/probe_pending.py lane/plans/round46_c1_verify.py
PENDING calls=1 touches=1 hits=[('openat', '/root/fx/pad/sibling/outside')]
REFUSED-FENCE-PENDING classification=READ
RESTORED_DETECTOR_EXIT=0
git -C "$D" status --porcelain
# (empty)
```

Pristine and restored SHA-256 are identical (`ef19380e…`); mutant SHA-256 was `b0d22b79…`. Detector passes pristine and restored, and observably loses the touch under the mutant. **Verdict: KILLED** by this bounded detector. This synthetic fixture demonstrates the specific accounting sensitivity; it does not establish population coverage.

## Control false-pass check and limits

I did not run a scored stage-2 control because the v3 counter and its stage-2 pins/receipts do not exist at the frozen revision. The named controls therefore have no R49 measured pass/fail result from this seat.

The accounting mutant has a concrete false-pass *channel*: if a fence/control's only out-of-`d` event is an unfinished syscall that never resumes, suppression changes a refusing result from `READ` to `clean`. Under the frozen r49 contract, the counter must retain this touch to reject a fence that probes outside `d` and then refuses. This is not evidence that a named control actually false-passes. As comparison only, the committed round-48 control report measured the admit-all and round-45 keyed controls as `REFUSALS clean=0` and `SEALED clean=0`, with admissions reported separately as benign; it states: “The hostile legs still cannot print `clean=total`”. Thus those prior controls failed independently of this pending-touch channel. R49's actual controls must be checked against the stage-2 counter; no R49 false-pass claim is made here.

Limits: the detector uses a synthetic strace line, not a live strace/bwrap run or the unavailable R49 v3 counter. It tests the inherited pending-at-EOF parser branch only. No external sources were opened and no tools were installed.

## Sources opened

All are local lane/skill sources; URL: not applicable. Access date: 2026-10-28.

- `plans/round-49-claims.md` at `9d2900af…`; quote: “a mutant is caught iff the mutated fence no longer prints the clean signature”
- `corpus/lessons/round-48-verifier-spotcheck.md`; quote: “the mutation floor committed with receipts”
- `plans/round46_c1_verify.py` at `9d2900af…`; quote: “blocked and never resumed: rule (h)”
- `plans/fixture_fence.py` at `9d2900af…`; quote: “None when it cannot be read.”
- `.ufo/waves/round-48/w1/R48C1ExecControls.md`; quote: “The hostile legs still cannot print `clean=total`.”
- `skill://godspeed`; quote: “Iterate cheap, in parallel.”

**VERDICT:** pending-at-EOF accounting mutant killed by the bounded detector; restored counter bytes hash-identically. R49 named-control false-pass status is **unmeasured pending stage 2**; no scored run and no C1/C2 admission claim.
