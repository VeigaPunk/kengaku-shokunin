# R48C1MutBoundary — inside-`d` boundary mutation probe

Axes named: calibration (R48-C1).

**VERDICT: INCONCLUSIVE / BLOCKED — no mutants scored.** The stage-1 claims freeze is present at the required base revision, but the stage-2 pinned v3 counter and its frozen fixture population are absent there. The task requires recording which frozen case kills each mutation; without that frozen detector, a scored run would violate the freeze/order rule. No counter or probe execution was run; no case-to-mutant kills are claimed.

## Evidence

Scratch clone: `/fast/scratch/hyaku/kengaku-r48/R48C1MutBoundary/lane`.

Exact commands and observed outputs:

```text
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1MutBoundary
export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1MutBoundary
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D"
git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r48/R48C1MutBoundary/lane
git -C "$D" checkout -q a543d92083557dd9b33ee674e9b99b03411f80af
git -C "$D" rev-parse HEAD
a543d92083557dd9b33ee674e9b99b03411f80af
git -C "$D" ls-tree -r --name-only HEAD plans/ | grep round-48
plans/round-48-claims.md
git -C "$D" cat-file -e HEAD:plans/round48_c1_verify.py
fatal: path 'plans/round48_c1_verify.py' does not exist in 'HEAD'
git -C "$D" show HEAD:plans/fixture_fence.py | sha256sum
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  -
```

The clone top-level was verified to equal `$D` before checkout; measured revision (`REV`): `a543d92083557dd9b33ee674e9b99b03411f80af`. The frozen claims blob is `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`. Its C1 text specifies that `plans/round48_c1_verify.py` is pinned at stage 2 and that the honest population and literals are also frozen at stage 2. The file is absent at the stage-1 base. Stage 1 therefore predates this attempted probe, but the required scored detector freeze does not exist in this tree.

No inside-boundary mutation was applied or executed: the repair/landed fence is not available in the stage-1 tree, and the requested per-frozen-case kill attribution cannot be made absent the stage-2 counter and population. The 20 refusal and 12 sealed module filenames exist at this base, but those alone do not define the full C1 scoring detector. This report does not claim admission or any mutant catch rate.

## Source locator records

- URL: `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md`; accessed 2026-10-27. Located quote (21 words): “Counter `python3 plans/round48_c1_verify.py --lane .` (written in wave 1, pinned at stage 2).”
- URL: `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md`; accessed 2026-10-27. Located quote (15 words): “9/9 novel honest controls refused”; “fence mutants 2/13 caught.”

## Limits and cleanup

The stage-1 tree is not the eventual stage-2 frozen counter/population, so no claims are made about what a future detector will catch. No tools were installed. Scratch cleanup is performed before yielding; no lane production files were modified.
