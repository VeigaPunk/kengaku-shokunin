# FxMutP3E — P3e population-direction survivor

Seat: KengakuR26-2.FxMutP3E; 2026-10-21; advisory mutation probe, not an admission judgment.
Axes: calibration/detector sensitivity; scratch isolation; reproducibility/exact restoration.
Pinned integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; fixture base: `f11bffbf9caa9c9e286fb32c568b81b97719656a`.
Read claims including explicitly post-output Amendment 1 (§7/§9), round-26 lesson and outside-corpus audit draft.
Scratch retained: `/tmp/kengaku-r26-FxMutP3E-5lqae7n8`; no lane code/state/index writes, builds, lint or network.

## Mutant and expected detector
At `plans/state_check.py:1599`, use the row population in the file-to-row loop: plausible copy/paste direction error.
```diff
--- a/plans/state_check.py
+++ b/plans/state_check.py
@@ -1599 +1599 @@
-    for relative in P3E_FILE_PATHS:
+    for relative in P3E_ROW_PATHS:
```
This removes the frozen round-25 outside-spotcheck assertion and substitutes the already-indexed round-24 spotcheck, preserving assertion count.
Expected detector: unchanged `--selftest` plus every manifest fixture involving P3e; preserve manifest baseline/status/P2 expectations, verify patch hashes, reject setup failures.
Five fixtures: `p3e-row-removed`, `p3e-file-deleted`, `p3e-row-and-file-removed`, `supersede-frozen-restatement`, `supersede-rederived-control`.
Ten manifest expectations tested: eight P3e and the two coupled P3c supersession expectations. The base-summary diagnostic is recorded, not a manifest assertion.

## Exact commands and actual outputs
Exports: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` and the same command with `f11bffbf9caa9c9e286fb32c568b81b97719656a`, each exit 0; extracted only into scratch.
`python3 /tmp/kengaku-r26-FxMutP3E-5lqae7n8/detect.py --stage pristine` → exit 0; `selftest exit=0`, `patches pinned/applied=5/5`, `manifest_checks=10/10`, `DETECTOR=PASS`.
`python3 /tmp/kengaku-r26-FxMutP3E-5lqae7n8/detect.py --stage mutated` → exit 0; identical four output lines.
`python3 /tmp/kengaku-r26-FxMutP3E-5lqae7n8/detect.py --stage restored` → exit 0; identical four output lines.
Every stage invokes `python3 /tmp/kengaku-r26-FxMutP3E-5lqae7n8/integration/plans/state_check.py --selftest` and prints `selftest ok   P3e: row and file mutations (P3e.row-to-file.lessons/round-25.md; P3e.file-to-row.lessons/round-25.md)`.
Every patch SHA matches the manifest; all 15 scratch `git apply -p1` invocations exit 0. Each fixture's `--json` invocation exits 1 as expected; all baseline assertion statuses MATCH, all P2 mismatches 0.
The three deletion fixtures return MISMATCH in both directions; frozen-restatement returns MISMATCH and rederived-control SUPERSEDED for their P3e/P3c targets, in every stage.
Full expanded subprocess commands, cwd, stdout, stderr and exits: `/tmp/kengaku-r26-FxMutP3E-5lqae7n8/{pristine,mutated,restored}/*.command.json`; stage summaries: the corresponding `receipt.json` files.
Detector SHA-256: `340cdde730f5b74d733eceff1b06734b2328201f512755e9b7bdb9d5f2c36694`; manifest SHA-256: `c66b7c4c80f137c29b6971993254fbe5241de87ac75b5388f680df274dd93acf`.

## Concrete lost detection
The same checker `--root /tmp/kengaku-r26-FxMutP3E-5lqae7n8/base --json` diagnostic observes:
| bytes | assertions | match | mismatch | outside-spotcheck assertion | native exit |
|---|---:|---:|---:|---|---:|
| pristine | 275 | 266 | 5 | MISMATCH | 1 |
| mutated | 275 | 267 | 4 | ABSENT | 1 |
| restored | 275 | 266 | 5 | MISMATCH | 1 |
Exact lost ID: `P3e.file-to-row.lessons/round-25-verifier-spotcheck.md`; pristine observation is `exists=true`, `row_lines=[]`, `correction_line=null`.
Mutant instead emits MATCH for `P3e.file-to-row.lessons/round-24-verifier-spotcheck.md` with `row_lines=[92]`.
Pristine detector baseline passed; deliberately red manifest/native-base exits are expected observations, not a baseline detector failure or a killed mutant.
Coverage gap: selftest and relevant manifest expectations exercise the shared round-25 lesson path, not the asymmetric frozen outside-spotcheck member. Exact P3e ID-set/asymmetric missing-index assertions are absent from these detectors.

## Restoration evidence
Pristine/restored checker SHA-256: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
Mutated checker SHA-256: `88c2276e64e6c8a65694462fbe8764a3ff85286b811fd1f4e86473644508919b`.
`cmp --silent /tmp/kengaku-r26-FxMutP3E-5lqae7n8/state_check.pristine.py /tmp/kengaku-r26-FxMutP3E-5lqae7n8/integration/plans/state_check.py` → exit 0; SHA-256 output matches the pristine bytes above.
Active scratch checker is restored. `mutation.diff`, `state_check.pristine.py`, `state_check.mutant.py`, detector and fixtures/logs remain under the retained scratch path. No tools installed/updated.

VERDICT: SURVIVED — blocker in the assigned P3e mutation coverage; exact bytes restored; advisory finding only, no admission judgment.
