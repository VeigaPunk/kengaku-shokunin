# FxMutP3C — P3c whole-file content-pin mutant

Round 26 attempt1; 2026-10-21; lane-dispatched advisory mutation probe, not outside verification or admission.
Axes: calibration (detector sensitivity), specificity (frozen-case expectations), isolation/exact restoration.
Read claims including POST-OUTPUT Amendment 1 (and Amendment 2), round-26 lesson, and integration-revision.txt.
Measured integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; fixture data: `f11bffbf9caa9c9e286fb32c568b81b97719656a`.
Scratch S = `/tmp/kengaku-r26-FxMutP3C.eKLw5t`; D = S + `/probe_data`; scratch retained, checker restored.

## Mutant and expected detector
One expression removed from S/plans/state_check.py:1474; line-anchored checks remain intact:
```diff
@@ -1474 +1474 @@
-        target_ok = (target_text is not None and token_hits == 1
+        target_ok = (target_text is not None
```
This is the whole-file (`target_line is None`) branch used by all four Box-1 SKILL.md content pins.
[INFERENCE from code] With the pointer unchanged and the file readable, missing/duplicated frozen headings no longer make these P3c assertions red; a missing-heading witness was not separately run.
Expected detector: `--selftest` plus every manifest row whose class is P3c or assertion id starts P3c (5 distinct patches, 8 rows, including supersession controls).
The detector fails on selftest failure, wrong named assertion status, unexpected P2 mismatch count, or CLI/summary exit disagreement. Adequate whole-file-pin regression coverage should kill this mutant.

## Commands and actual output
Exports (read-only lane Git; git apply only inside disposable exports):
`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 | tar -x -C /tmp/kengaku-r26-FxMutP3C.eKLw5t` → exit 0.
`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar f11bffbf9caa9c9e286fb32c568b81b97719656a | tar -x -C /tmp/kengaku-r26-FxMutP3C.eKLw5t/probe_data/base` → exit 0.
`python3 -B /tmp/kengaku-r26-FxMutP3C.eKLw5t/probe_data/probe.py pristine` → exit 0.
`python3 -B /tmp/kengaku-r26-FxMutP3C.eKLw5t/probe_data/probe.py mutated` → exit 0.
`python3 -B /tmp/kengaku-r26-FxMutP3C.eKLw5t/probe_data/probe.py restored` → exit 0.
Actual detector output (same runner and same fixture bytes all three phases):
```text
DETECTOR=PASS phase=pristine manifest_rows=8 unique_patches=5 failures=0
DETECTOR=PASS phase=mutated manifest_rows=8 unique_patches=5 failures=0
DETECTOR=PASS phase=restored manifest_rows=8 unique_patches=5 failures=0
```
All three `--selftest` runs exited 0 and printed `selftest ok   P3c: red mutation (P3c.box.3.pointer.1)` and `[selftest] ALL PASS`.
In every phase the unpatched base's selected assertions were MATCH; base CLI exit 1 / mismatch=5 is the known frozen-base state, not detector failure.
Patched results below were identical pristine / mutated / restored; all had CLI exit 1 and P2 mismatch=0:
| Fixture | Named assertion | Observed status | Total mismatch |
|---|---|---|---|
| p3c-pointer-moved | P3c.box.3.pointer.1 / P2c.box.3.pointer.1 | MISMATCH / MATCH | 6 |
| p3c-content-shifted | P3c.box.3.pointer.1 / P2c.box.3.pointer.1 | MISMATCH / MATCH | 6 |
| p3c-province-append | P3c.box.4.pointer.1 / P2c.box.4.pointer.1 | MISMATCH / MATCH | 6 |
| supersede-frozen-restatement | P3c.box.4.pointer.1 | MISMATCH | 8 |
| supersede-rederived-control | P3c.box.4.pointer.1 | SUPERSEDED | 6 |
Full exact subprocess argv/cwd/stdout/stderr/exits and receipts: `/tmp/kengaku-r26-FxMutP3C.eKLw5t/probe_data/logs/{pristine,mutated,restored}/`; runner and mutation.diff are under D. All five patch SHA-256 pins were checked before use.

## Restoration and scope
SHA-256 before: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
SHA-256 mutant: `bd3863cb7f285286adb462fa6c652f2571af022141a375851ed0ab50c829dd6a`.
SHA-256 restored: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
`cmp /tmp/kengaku-r26-FxMutP3C.eKLw5t/probe_data/state_check.py.original /tmp/kengaku-r26-FxMutP3C.eKLw5t/plans/state_check.py` → exit 0, no output; subsequent sha256sum matched both files.
Only this report was written in the lane; no production code/state/index changes, installations, endpoints, build/lint/formatters, delegation, or alternate runtime.
Coverage finding: the assigned P3c selftest exercises Box 3; the retained P3c manifest targets Boxes 3/4, leaving whole-file Box-1 token enforcement unchallenged. No broader checker pass is claimed.

VERDICT: SURVIVED — BLOCKER: removing P3c whole-file token enforcement passes the pristine-valid assigned detector unchanged; exact scratch restoration confirmed.
