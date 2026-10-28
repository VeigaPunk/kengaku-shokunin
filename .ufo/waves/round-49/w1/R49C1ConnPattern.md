# R49C1ConnPattern — C1 measurement-boundary comparison

Axes named: **calibration** (assigned); operability/evidence integrity are affected risks, not claimed axes. This is one bounded comparison, not a claim admission or scored counter run.

## Freeze and inspected revision

Stage-1 freeze was checked in the committed lane tree before measurement. Exact commands and output:

```text
git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
git show -s --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
```

The stage-1 commit predates this inspection. A `git clone --shared` was checked out at that exact commit; `git rev-parse HEAD` returned `9d2900af41e4d1fc6022eff99010436fde6dbd93`, and `git rev-parse --show-toplevel` returned `/fast/scratch/hyaku/kengaku-r49/R49C1ConnPattern/lane`. Current lane tip observed separately: `af88aab193e6034cb9b386472064e3c18fa90128`. No scored counter/probe was run; the stage-2 v3 counter and stage-2 populations/mutant battery are absent at this frozen revision.

## One non-obvious reused failure mode and bounded move

**Finding — lexical path containment is not mount/backing-store containment.** The frozen C1 claim requires the mount-point boundary to be honored: an honest fixture whose store sits on a mount boundary inside `d` is admitted iff every byte the decision reads is inside `d` (claims lines 85–88). The inherited round-46 measurement boundary resolves syscall path strings lexically (`plans/round46_c1_verify.py`, `_paths`/`_outside`, lines 269–298) and explicitly limits measurement to paths under its scratch root. It treats a path below `d` as in-bound, without resolving that path's backing mount. The lane's own prior mount-boundary analysis records the concrete matching gap: `fixture_fence.py` `_tree` rejects symlinks/special files but does not check mount identity; `_store` can follow a bind-mounted `.git` directory backed outside `d` (`.ufo/waves/round-46/w2/R46W2C1Intent.md:7-11`). Thus the fence's structural predicate and the counter's trace boundary share the same blind spot: an outside-backed read through an in-`d` mountpoint can appear inside by pathname and evade the counter's LEAK classification. This is directly material to calibration, not an abstract syscall limitation.

**Proposed move (one bounded implementation constraint):** make the C1 measurement boundary mount-aware for traced paths under `d`: compare each resolved path's mount identity/backing mount against `d` before treating the access as inside; record outside-backed mount accesses as outside touches. Add a deterministic selftest/control fixture with a bind-mounted store to demonstrate the detector catches the case. Keep the frozen predicate, population, controls, and kill rule unchanged; this implements the stated boundary rather than changing it. If this host cannot produce bind-mount fixtures, record that as an unexercised limit rather than treating lexical containment as proof.

Second-order effects: counter-side mount attribution improves calibration evidence but must not itself read attacker-controlled fixture data or turn ordinary paths into false positives; gate-side rejection and counter-side attribution should agree. Keep the evidence in committed stage-2 inputs/receipts with their existing pin and REV discipline. `grader.py` is a useful contrasting verification pattern: its r12 mutation battery attributes each mutation to an expected check id (`grader.py:4882-4885`, `5388-5404`), whereas the frozen C1 MUTANTS wording counts a mutated fence when it no longer prints the clean signature. For C1, preserve the frozen rule, but make each committed mutant receipt show the measured leg/result and whether the outcome was a legitimate predicate change or an execution/build error; do not silently credit inability to measure as evidence of boundary detection. This is a reporting requirement, not a re-freeze proposal.

## Comparison evidence / exact commands

Commands run (read-only inspection unless noted; no fixture writes):

```text
# Required documents, read in full:
read plans/round-49-claims.md
read corpus/lessons/round-48-verifier-spotcheck.md
# Tooling prerequisite:
read /home/vgpnk/.omp/agent/RULES.md
# Freeze verification:
git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git show -s --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
# Scratch clone identity/revision:
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r49/R49C1ConnPattern/lane
git -C /fast/scratch/hyaku/kengaku-r49/R49C1ConnPattern/lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /fast/scratch/hyaku/kengaku-r49/R49C1ConnPattern/lane rev-parse HEAD
git -C /fast/scratch/hyaku/kengaku-r49/R49C1ConnPattern/lane rev-parse --show-toplevel
# Pattern inventory and inspection:
git ls-tree -r 9d2900af41e4d1fc6022eff99010436fde6dbd93 --name-only
git diff -u plans/round46_c1_verify.py .ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py
sha256sum .ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py
```

Relevant observed outputs:

- Frozen base contains `grader.py`, `plans/pkg_gate.py`, `plans/anchor_line_check.py`, `plans/fixture_fence.py`, `plans/order_check.py`, and `plans/round46_c1_verify.py`; it does not contain `plans/honest49/`, `plans/sealed49/`, or `plans/mutants49/`.
- `plans/round46_c1_verify.py` `analyse()` identifies touches only when normalized syscall path is under `root` and not lexically equal to/below `d` or `ctl` (`_outside`, lines 292–298); the file itself lists host paths outside the scratch root as unmeasured (docstring limits, lines 91–94).
- `plans/fixture_fence.py` `_argv` rejects `{...}` placeholders, but this is unrelated to the mount gap. The r48 report documents the prior `{WORK}` placeholder issue as a fence refusal; the r48 honest population README documents normalized relative argv. It is not evidence of a new v3 counter defect.
- The r48 v2 counter is a useful extant implementation reference: digest `8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f`; it imports pinned `round46_c1_verify.py`, classifies `ERROR` and `HUNG` separately, checks honest novel counts and extras, and rechecks pins. Its `kind_of` remains built on the same path-only `run_fence`/`analyse`, so it does not close mount attribution. Do not infer that r49 has adopted this candidate; it is an r48 wave artifact only.
- `grader.py` recomputes offline and maps unexpected exceptions to input errors; `pkg_gate.py` maps clause exceptions to defects and gates optional reruns; `anchor_line_check.py` separately checks source-anchor line claims. These are distinct content-verification domains and do not provide mount identity evidence for C1.

## Sources opened (local URLs, accessed 2026-10-28)

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` — “the mount-point boundary is honoured” (quote under 25 words).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` — “Any future C1 admission attempt needs the mutation floor committed with receipts.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` — “host paths outside the scratch root are not counted”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` — “Only the exact contract shape and inside-`d` path values pass.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w2/R46W2C1Intent.md` — “lexical containment is not backing-store containment.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/grader.py` — “each corruption must be killed by the specific check id named in the battery.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg_gate.py` — “a clause that cannot run is a defect, never a pass.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/anchor_line_check.py` — “the quote is a substring of line N”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/order_check.py` — “Anything else … means the probe ran.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/README.md` — “argv values are relative … no absolute scratch path enters a receipt.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecControls.md` — “the r46 ‘9/9 refused’ was a `{WORK}` placeholder-argv artifact”.

## Limits

Source comparison only; no r49 counter implementation exists at the measured stage-1 revision, and no scored counter run was executed. Mount identity detection is proposed, not implemented or exercised. This report makes no R49-C1 or R49-C2 admission claim. No tools installed.

Scratch directory removed before yield. No lane production file was changed.

VERDICT: calibration boundary comparison; identified reused lexical-mount containment failure mode; no scored measurement and no admission judgment.