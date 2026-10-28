# R49C1RevNoHarm — fence-repair harm review

Axes named: calibration (assigned C1 axis) and security-boundary correctness (possible harmed axis). No code was changed and no R49-C1/C2 admission is claimed.

## Freeze and measured revision

The required stage-1 freeze was present and committed before this review; no scored counter/probe was run.

Exact commands and observed output:

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree 9d2900af41e4d1fc6022eff99010436fde6dbd93 -- plans/round-49-claims.md plans/fixture_fence.py plans/round46_c1_verify.py
100644 blob a2b128ae007bf47d3aefdeda6321ae118c7e5958\tplans/fixture_fence.py
100755 blob 415b40705749b5d3bada6929b34970acf0693d1c\tplans/round46_c1_verify.py
100644 blob 3ad92f056155b5cc0c3e2a60068b6b3cecf0c21d\tplans/round-49-claims.md
```

I cloned the lane read-only into `/fast/scratch/hyaku/kengaku-r49/R49C1RevNoHarm/lane`; `git rev-parse --show-toplevel` returned that exact path and `git rev-parse HEAD` returned `9d2900af41e4d1fc6022eff99010436fde6dbd93`. Review revision: `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`. Candidate reviewed from the round-49 executor report: fence A sha256 `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` (810 lines), applied from the R48 diff to the byte-identical base fence. No candidate scored here.

## Concrete boundary risk

**Medium — same-filesystem bind mount can make an outside backing tree appear inside `d`.** Fence A's new containment test compares `st_dev` for visited entries to `d`; same-filesystem bind mounts preserve that device number. The R48 candidate report records a direct mount probe: `MOUNT M3 same-fs bind worktree (lane/data): ADMITTED -- dev 66309->66309; admitted` and `MOUNT M4 same-fs bind store (objects/info): ADMITTED -- dev 66309->66309; admitted` (R48C1ExecFenceA.md §5.8). The R49 executor report states the same fence hash was re-applied at the frozen base, so this candidate property remains relevant. This is a boundary gap if the contract means backing bytes must originate inside `d`: a hostile fixture can bind-mount an outside directory or store into a lexically in-`d` path and pass the device test. This specifically weakens the claimed proof that every admitted store is fixture-owned; it is not demonstrated as a traced outside-path LEAK under the stated path-based metric.

**Testable risk:** mount an outside donor directory from the same filesystem at `d/lane/data` and separately at `d/lane/.git/objects/info`, run the candidate fence with the honest argv, and assert whether it admits; inspect donor identity/content to establish the backing source. The existing M3/M4 observations already report admission. A held-out sealed case should use an outside donor containing a redirected Git store and assert refusal under the actual v3 harness, not merely `touches=0` on the fence walk.

A second, bounded calibration risk is cross-device over-refusal: the candidate explicitly rejects entries whose `st_dev != ddev`, even when the mount is intentionally inside `d` and every accessed pathname is in-`d`. The earlier candidate report observed `MOUNT M1 cross-device store ... REFUSED` and `MOUNT M2 cross-device worktree ... REFUSED`; the R49 freeze wording says an honest boundary fixture is admitted iff every byte the decision reads is inside `d`. This can make a valid mounted honest fixture fail the HONEST leg. This is an observable mismatch to settle with a frozen honest fixture and the v3 counter.

The allowlist expansion itself does not show a direct escape in the reviewed evidence: it admits detached SHA HEAD, `info/refs`, `objects/info/packs`/commit-graph files, additional config declarations and `refs/notes`/`refs/stash`; the R48 negative probes specifically report outside symlink, alternate, include, redirect and config-path mutations refused. Those probes are development evidence only, not the frozen R49 sealed population. In particular, `[remote "<n>"] url` is admitted as inert configuration even for an outside URL (R49C1ExecFenceA.md §7); no fetch is described in the gated path, so this is not by itself an observed leak. Re-test if execution behavior or policy changes.

## Exact inspection commands and evidence

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree 9d2900af41e4d1fc6022eff99010436fde6dbd93 -- plans/round-49-claims.md plans/fixture_fence.py plans/round46_c1_verify.py
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
git rev-parse --show-toplevel
git rev-parse HEAD
```

Source evidence opened (local file URLs; access date 2026-10-28):
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` §C1, quote: “every byte the decision reads is inside `d`.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecFenceA.md` §5.8, quote: “MOUNT M4 same-fs bind store (objects/info): ADMITTED”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceA.md` §7, quote: “Same-filesystem bind mounts below `d` are admitted”.

Limits: I did not run the development harness, the scored v3 counter, or any fixture mutation. The mount outputs above are cited from the prior executor report, not re-measured by this seat. The R49 held-out sealed population and mutant battery are not assessed here. No external source was opened. LSP status/references/definition/diagnostics were unavailable in this reviewer environment; conclusions are based on the frozen source, claim text and cited wave reports, not semantic grep proof.

VERDICT: **Boundary risk remains actionable** — same-device bind mounts are admitted despite outside backing provenance; assess with a held-out sealed mount case and resolve the contract/measurement meaning before admission. Separate calibration risk: cross-device in-`d` honest mounts are refused. No admission judgment.
