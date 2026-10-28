# R49C1HoMount — C1 honest mount-boundary fixture

Axes: **calibration** (honest mount-boundary admission vs the fixture fence's advertised boundary); containment/provenance is the associated assertion under attack. No C1/C2 admission claim.

## Freeze / measurement boundary

**REV `9d2900af41e4d1fc6022eff99010436fde6dbd93`** (frozen lane clone; stage-1 commit dated 2026-10-28 09:14:40 -0300). Before any counter/probe scoring, I verified the frozen claims blob matches the lane file and the commit predates this development measurement. The stage-1 claims are present; `plans/round49_c1_verify.py` is absent at the frozen commit and in its tree. No scored counter or probe was run; the fence calls below are explicitly unscored fixture diagnostics.

Commands and observed outputs:

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --format='%H %ci %s' -3 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
3a548330c4899c6c5df34168a44a59f66828ce74 2026-10-27 09:58:06 -0300 round-48 verifier spot-check (integrator, hyaku): non-author admit/reject
d4eacdfb56307c069c245270f4d78e2ec314829e 2026-10-27 09:20:03 -0300 round-48: record honest-stop C1/C2 evaluation and frontier evidence
$ git cat-file -e 9d2900af41e4d1fc6022eff99010436fde6dbd93:plans/round-49-claims.md && git show 9d2900af41e4d1fc6022eff99010436fde6dbd93:plans/round-49-claims.md | sha256sum && sha256sum plans/round-49-claims.md
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  -
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  plans/round-49-claims.md
$ git -C "$D" cat-file -e 9d2900af41e4d1fc6022eff99010436fde6dbd93:plans/round49_c1_verify.py || echo 'v3-counter absent'
v3-counter absent
```

## Fixture and counterexample

I constructed two namespace-local mounted-store fixtures under the seat scratch. Both are regular initialized Git stores copied to a mount source, then bind-mounted over `d/repo/.git`; every fixture Git invocation used `git -C "$D"` where `$D` was inside my scratch clone/scratch tree, and I checked `rev-parse --show-toplevel` before subsequent fixture writes. The honest fixture's mount source `d/internal-store` is inside `d`. The control mounts an otherwise identical store from sibling `scratch/external-store`, outside its `d`. Both are same-filesystem XFS bind mounts, the strongest counterexample to relying on `st_dev` alone.

The exact diagnostic command was:

```sh
set -eu
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1HoMount
D="$TMPDIR/lane"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
test "$(git -C "$D" rev-parse HEAD)" = 9d2900af41e4d1fc6022eff99010436fde6dbd93
unshare -rm /usr/bin/python3 "$TMPDIR/mount_probe.py" "$TMPDIR" "$D/plans/fixture_fence.py" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py
```

The fixture driver created and checked the repo with `git -C <repo> init`, followed by `git -C <repo> rev-parse --show-toplevel` (asserted equal to `<repo>`), copied `.git` to the selected backing directory, removed the original `.git`, created an empty `.git` mount target, then used `mount --bind <backing> <d>/repo/.git`. It called `breach(d, ["--lane", str(repo)], "anchor")` on each fence and unmounted afterward. The honest fixture is a positive honest-class witness; the sibling-backed case is an explicit hostile provenance control. The disposable driver SHA256 was `ebf51f6860f31a9cd35fe57fce0d67b5491b3af4b57c3bff90e94ecebbac36e2`.

Verbatim output:

```text
STAT honest-internal d dev=66309 mount=/fast
STAT honest-internal store-source dev=66309 mount=/fast
STAT honest-internal mounted-store dev=66309 mount=/fast/scratch/hyaku/kengaku-r49/R49C1HoMount/fixture/repo/.git
RESULT honest-internal base=ADMIT
RESULT honest-internal candidate=ADMIT
STAT hostile-external-backing d dev=66309 mount=/fast
STAT hostile-external-backing store-source dev=66309 mount=/fast
STAT hostile-external-backing mounted-store dev=66309 mount=/fast/scratch/hyaku/kengaku-r49/R49C1HoMount/fixture-external/repo/.git
RESULT hostile-external-backing base=ADMIT
RESULT hostile-external-backing candidate=ADMIT
FIXTURE-CLAIM honest: source and mounted store are under d; hostile: store backing is outside d
```

Fence hashes at measurement: base `plans/fixture_fence.py` `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`; candidate `R49C1ExecFenceA/fence_a.py` `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`. The candidate admits the honest mounted store, as desired, **but also admits the same-device bind whose backing store is outside `d`**. The `st_dev` comparison cannot distinguish these cases. This reproduces the same-filesystem bind limitation called out in the candidate's own header, and is a direct counterexample to any interpretation of “every byte read is inside `d`” as backing-store provenance rather than pathname containment.

## Smallest safe correction and limits

Do not treat equal `st_dev` as proof that mounted bytes originate under `d`. The minimum correction depends on the frozen contract: if backing provenance is required, the decision needs a way to identify bind-mount origins and distinguish an in-`d` source from an out-of-`d` source; this is not established by `st_dev` or the current pathname-only fence. If the required prohibition on reading outside `d` disallows consulting mount metadata, the two requirements (admit an internal bind mount, reject an otherwise equivalent external bind mount) are not demonstrated satisfiable by this fence; the frozen claim must stop rather than claim the `iff` property. The honest fixture alone passes, but does not establish the converse.

Limits: this was a direct, unscored `breach()` diagnostic in an `unshare -rm` namespace, not a run through the frozen v3 counter's build/strace harness. The mount is live only in this namespace; the counter's isolated fixture-builder namespace cannot persist a module-created mount into the later fence namespace, so this fixture cannot be delivered as an ordinary static `FIXTURES` module without harness support. No external web source was opened (no URL/date/quote applicable). No tool installed or updated.

VERDICT: honest-mount-positive reproduced; same-device external-backing counterexample falsifies provenance inference; C1 admission not claimed.
