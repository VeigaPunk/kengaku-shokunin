# FxMutP3B — P3b checker omission probe (2026-10-21)
Axes: calibration / defect sensitivity; frozen-population fidelity; scratch isolation / exact restoration.
Scope: one checker mutant only, advisory, not judge. Read claims including POST-OUTPUT Amendment 1 and round-26 lesson.
Integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; fixture base: `f11bffbf9caa9c9e286fb32c568b81b97719656a`.

## Paths and exact commands
`L=/home/vgpnk/Projects/shokunin/kengaku-shokunin`; `S=/tmp/kengaku-r26-FxMutP3B-TdioyJ` (retained).
`C=$S/tool/plans/state_check.py`; `B=$S/base`; `P=$S/p3b-province-count`; all expanded paths absolute, execution cwd `/tmp`.
Read-only export: `git -C "$L" archive --format=tar 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 -- plans/state_check.py plans/fixtures/r25/shonen-seed.txt plans/fixtures/r26/state_p3` → exit 0.
Read-only export: `git -C "$L" archive --format=tar f11bffbf9caa9c9e286fb32c568b81b97719656a` → exit 0.
Archives extracted with Python `tarfile.extractall(filter='data')` into `$S/tool` and `$B`; `$B` copied to `$P`.
`git -C "$P" apply -p1 "$S/tool/plans/fixtures/r26/state_p3/p3b-province-count.patch"` → exit 0, stdout/stderr empty.
Patch SHA256 verified: `7e717d74c8db4d575efe925c10e2b75f720decbd9f6e05acd86ac0a2c314ba24`.
Detector invocations: `python3 "$S/detect.py" pristine`, `python3 "$S/detect.py" mutated`, `python3 "$S/detect.py" restored` → exits **0 / 0 / 0**.
Each invocation runs the same three commands concurrently, without changing the manifest expectations:
- `python3 "$C" --selftest`
- `python3 "$C" --root "$B" --json`
- `python3 "$C" --root "$P" --json`

## Mutant and expected detector
Delete the single behavior-bearing `p3_compare_groups` call for `P3b.province.interval-reverdict.unique-samples` (original lines 1387–1391).
Plausible defect: accidentally omit one numeric receipt comparison while retaining all neighboring P3b checks.
Expected detector: selftest or the frozen P3b manifest case should reject loss of that registered check; neither did.
```diff
--- pristine/plans/state_check.py
+++ mutated/plans/state_check.py
@@ -1387,5 +1386,0 @@
-    p3_compare_groups(
-        root, out, "P3b.province.interval-reverdict.unique-samples",
-        interval_row[0] if interval_row else None, interval_text,
-        r"(\d+)\s+unique samples", interval_summary,
-        r"unique_samples=(\d+)", ("unique_samples",), "PROVINCE.md")
```

## Observed outputs
| phase | selftest exit | base exit / assertions / mismatch | P3b fixture exit / assertions / mismatch | manifest target base→fixture | omitted ID |
|---|---|---|---|---|---|
| pristine | 0 | 1 / 275 / 5 | 1 / 275 / 6 | MATCH→MISMATCH | present, MATCH |
| mutated | 0 | 1 / 274 / 5 | 1 / 274 / 6 | MATCH→MISMATCH | ABSENT |
| restored | 0 | 1 / 275 / 5 | 1 / 275 / 6 | MATCH→MISMATCH | present, MATCH |
All three selftests printed `[selftest] ALL PASS`; stderr empty. Each also printed `selftest ok   P3b: instrument and exact-id-set red mutations (P3b.province.interval-reverdict.scored-trials)`.
Manifest row 4 targets `P3b.province.state-assertion-check.base-mismatch`: claim/receipt 10/10 at base, 11/10 after patch; P2 mismatches remain 0 in every run.
Base exit 1 is the registered five known mismatches, not a failing detector baseline: both manifest target expectations passed before mutation.
Selftest lines 1996–2024 exercise scored-trials and census ID sets, not unique-samples; the sole P3b manifest row exercises base-mismatch. The registered unique-samples assertion disappears undetected.
Full stdout/stderr and exact argv: `$S/pristine/`, `$S/mutated/`, `$S/restored/`, each with `results.json` and three command-output pairs. No changed-number acceptance case was run; current production comparison correctness is not impugned.

## Restoration evidence
Before SHA256: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
Mutant SHA256: `73c72bec6d7ae2f381f019405917d67d71ad13fe73fb8b4a278927b920730afa`.
Restored SHA256: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`; exact saved-byte comparison **true**, 98,853 bytes.
Restored the captured five lines before the restored run. Only this report was written in the lane; no code/state/index changes, build/lint, model traffic or installations. Existing Python 3.14.8 used.
VERDICT: SURVIVED — BLOCKER: the assigned selftest + P3b manifest detector accepts complete removal of a frozen P3b numeric comparison; coverage finding only, not a contract change.
