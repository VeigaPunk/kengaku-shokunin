# FxMutP3D — one P3d checker mutation
Axes: calibration/content-pin failure sensitivity; isolation; exact-byte restoration. Advisory, not admission or outside verification.
Read claims including explicitly post-output Amendment 1, Amendment 2, round-26 lesson, and draft.
Integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; fixture base: `f11bffbf9caa9c9e286fb32c568b81b97719656a`.
Scratch retained: `/tmp/kengaku-r26-FxMutP3D.dYjeEg` (checker restored). No lane code/state/index writes.
Runtime: `python3 --version` → `Python 3.14.8`, exit 0. Installs/updates: none. No build/lint.
## Mutation and expected detector
At scratch `plans/state_check.py:1561–1562`, remove the content-token predicate while preserving frozen anchor presence, axis identity, and in-range checks.
Expected: `--selftest` exits 1 at P3d; manifest `p3d-content-shifted` falsely becomes MATCH, violating its expected MISMATCH; anchor-shift remains detectable.
Exact mutation diff (the `diff -u` command below exited 1):
```diff
--- plans/state_check.py.pristine
+++ plans/state_check.py.mutated
@@ -1561,2 +1561 @@
-        ok = (len(hits) == 1 and hits[0][0] == axis and in_range
-              and all(count == 1 for count in needle_hits.values()))
+        ok = len(hits) == 1 and hits[0][0] == axis and in_range
```
## Commands and observed outputs
`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 plans/state_check.py plans/fixtures/r25/shonen-seed.txt plans/fixtures/r26/state_p3 | tar -x -C /tmp/kengaku-r26-FxMutP3D.dYjeEg` → no output, exit 0.
`mkdir -p /tmp/kengaku-r26-FxMutP3D.dYjeEg/base && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive f11bffbf9caa9c9e286fb32c568b81b97719656a SCORECARD.md | tar -x -C /tmp/kengaku-r26-FxMutP3D.dYjeEg/base` → no output, exit 0.
`cp -a /tmp/kengaku-r26-FxMutP3D.dYjeEg/base /tmp/kengaku-r26-FxMutP3D.dYjeEg/p3d-anchor-shifted && git -C /tmp/kengaku-r26-FxMutP3D.dYjeEg/p3d-anchor-shifted apply -p1 /tmp/kengaku-r26-FxMutP3D.dYjeEg/plans/fixtures/r26/state_p3/p3d-anchor-shifted.patch && cp -a /tmp/kengaku-r26-FxMutP3D.dYjeEg/base /tmp/kengaku-r26-FxMutP3D.dYjeEg/p3d-content-shifted && git -C /tmp/kengaku-r26-FxMutP3D.dYjeEg/p3d-content-shifted apply -p1 /tmp/kengaku-r26-FxMutP3D.dYjeEg/plans/fixtures/r26/state_p3/p3d-content-shifted.patch` → no output, exit 0.
`diff -u --label plans/state_check.py.pristine --label plans/state_check.py.mutated /tmp/kengaku-r26-FxMutP3D.dYjeEg/state_check.py.pristine /tmp/kengaku-r26-FxMutP3D.dYjeEg/plans/state_check.py` → only the predicate diff shown above, exit 1.
Same detector in every phase: `/tmp/kengaku-r26-FxMutP3D.dYjeEg/probe.py` runs selftest and manifest cases concurrently, verifies both manifest patch hashes, and invokes the actual `check_p3d` on frozen-base and separately patched SCORECARD exports.
Selftest subcommand every phase: `/usr/bin/python3 -B /tmp/kengaku-r26-FxMutP3D.dYjeEg/plans/state_check.py --selftest`.
`python3 -B /tmp/kengaku-r26-FxMutP3D.dYjeEg/probe.py pristine` → selftest exit 0; both base controls MATCH; anchor-shift MISMATCH; content-shift MISMATCH; `DETECTOR EXIT 0` (shell exit 0).
`python3 -B /tmp/kengaku-r26-FxMutP3D.dYjeEg/probe.py mutated` → selftest exit 1, stderr `selftest: P3d anchor-content mutation survived`; both base controls MATCH; anchor-shift MISMATCH; content-shift MATCH against expected MISMATCH; `DETECTOR EXIT 1` (shell exit 1).
`python3 -B /tmp/kengaku-r26-FxMutP3D.dYjeEg/probe.py restored` → selftest exit 0; both base controls MATCH; anchor-shift MISMATCH; content-shift MISMATCH; `DETECTOR EXIT 0` (shell exit 0).
All manifest target observations concern `P3d.axis.novelty.anchor.1.pin`; manifest P2b collateral rows and whole-tree CLI exit behavior are unobserved, not counted as passes.
Complete selftest stdout/stderr, commands, statuses, assertion observations, and exits: `/tmp/kengaku-r26-FxMutP3D.dYjeEg/pristine.json`, `/tmp/kengaku-r26-FxMutP3D.dYjeEg/mutated.json`, `/tmp/kengaku-r26-FxMutP3D.dYjeEg/restored.json`.
## Restoration evidence
The inverse scratch-only edit restored the original two lines before the final detector run.
`cmp -s /tmp/kengaku-r26-FxMutP3D.dYjeEg/state_check.py.pristine /tmp/kengaku-r26-FxMutP3D.dYjeEg/plans/state_check.py` → no output, exit 0.
SHA-256 pristine: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
SHA-256 mutated: `d025a39666f43979122ba66cb26f3b22946040255e5d4170f3e6bd9fd61eb816`.
SHA-256 restored: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
The lane checker had the same pristine SHA-256 both before and after this probe (`sha256sum`, exit 0); only this report was written in the lane.
Fixture SCORECARD SHA-256: base `0f1dfa45f0bfb647dcb3acbc75bc1d8c9be3ac7376b83002bfdc42701e419d68`; anchor-shift `2577e05fb3f7a48e46fa7722aa89f3aca179ace462c8b0abd1263b45af1282b6`; content-shift `279455efa22432986d76b2c0dc4a725cfe38f36432d9ba9990adcd6657bbef4e`.
VERDICT: KILLED — the single content-predicate mutant fails both selftest and the P3d content-shift manifest expectation; pristine/restored detectors pass. No surviving mutant in this assigned probe; no broader admission claim.
