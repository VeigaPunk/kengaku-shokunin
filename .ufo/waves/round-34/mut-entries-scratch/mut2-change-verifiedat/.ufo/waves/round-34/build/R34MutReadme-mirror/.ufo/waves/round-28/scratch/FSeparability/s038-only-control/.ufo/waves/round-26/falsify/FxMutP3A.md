# FxMutP3A — P3a checker deletion probe
Axes: calibration (assigned); detector sensitivity and exact-byte restoration. Advisory only, not admission judgment.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; fixture base `f11bffbf9caa9c9e286fb32c568b81b97719656a`.
Read `plans/round-26-claims.md` including POST-OUTPUT Amendment 1 and Amendment 2, and `corpus/lessons/round-26.md`.
Private scratch retained: `/tmp/kengaku-r26-FxMutP3A-ozfbk7q1`; only production write is this report; no lane code/state/index writes.
Setup: read-only `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar <revision>` piped to `tar -x -C <scratch>/integration` or `<scratch>/base`; both git/tar exits 0, stderr empty.
`python3 -B /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/detector.py prepare` exit 0: all four relevant manifest patch SHA-256 pins matched; all four scratch `git apply -p1` exits 0, stdout/stderr empty.
## Mutant and expected detector
Delete exactly the six-line comparison of the state capability's base mismatch number, leaving all other logic unchanged; plausible accidental omission of one numeric-token check.
Original site: `plans/state_check.py:1258-1263`. Exact `diff -u` output (exit 1, expected because files differ):
```diff
--- a/plans/state_check.py
+++ b/plans/state_check.py
@@ -1256,12 +1256,6 @@
         interval_selftest, r"selftest:\s*(\d+)\s+checks,\s*(\d+)\s+failed",
         ("checks", "failed"), "SCORECARD.md", ("{value} checks", "{value} failed"))
     p3_compare_groups(
-        root, out, "P3a.capability.state-assertion-check.base-mismatch",
-        state[0] if state else None, state[1] if state else "",
-        r"base\s+`?6180e4f`?.*?mismatch=(\d+)",
-        state_base, r"(?m)^assertions=.*?\bmismatch=(\d+)",
-        ("mismatch",), "SCORECARD.md")
-    p3_compare_groups(
         root, out, "P3a.capability.state-assertion-check.base-exit",
         state[0] if state else None, state[1] if state else "",
         r"base\s+`?6180e4f`?.*?exit\s+(\d+)",
```
Expected: selftest/committed manifest assertions reject losing a frozen P3a numeric comparison. Detector uses only `--selftest` and `--root <base or case> --json`, timeout 210s per invocation, max four concurrent; checks manifest target/base statuses, P2 mismatch expectations, and CLI exit semantics.
## Actual commands and outputs
`python3 -B /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/detector.py pristine` → `DETECTOR=PASS`, exit 0.
`python3 -B /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/detector.py mutated` → `DETECTOR=PASS`, exit 0.
`python3 -B /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/detector.py restored` → `DETECTOR=PASS`, exit 0.
All stages: `--selftest` exit 0, stderr empty, `[selftest] ALL PASS (...)`; P3a output `selftest ok   P3a: red mutation and full-token R26-E (P3a.capability.interval-reverdict.selftest-checks)`.
| Case | Pristine / mutated / restored target verdict | CLI exits | Total mismatches P/M/R |
|---|---|---|---|
| frozen base | MISMATCH / MISMATCH / MISMATCH (selftest-checks) | 1/1/1 | 5/4/5 |
| p3a-selftest-count-control | MATCH / MATCH / MATCH | 1/1/1 | 4/3/4 |
| p3a-selftest-count | MISMATCH / MISMATCH / MISMATCH | 1/1/1 | 5/4/5 |
| supersede-partial | MISMATCH / MISMATCH / MISMATCH | 1/1/1 | 5/4/5 |
| supersede-full-control | SUPERSEDED / SUPERSEDED / SUPERSEDED | 1/1/1 | 4/3/4 |
All P2 mismatch counts remain 0. CLI exit 1 is expected on these known-red base-derived trees, not a failed baseline detector.
Behavior-bearing loss: pristine/restored emit `P3a.capability.state-assertion-check.base-mismatch`, MISMATCH, claim `["11"]`, receipt `["10"]`, derived tokens `["mismatch=10"]`; mutated output omits it entirely. P3a population 11→10→11; total assertions 275→274→275.
Selftest checks no exact P3a ID population (`state_check.py:1953-1957`); all four relevant manifest rows target only `interval-reverdict.selftest-checks` (`manifest.tsv:2-3,21-22`). Thus they do not reject this numeric-comparison deletion. The changed totals are visible but not asserted by this bounded detector; a separate frozen-total assertion could kill it.
Full exact child commands, exits, stdout/stderr and parsed observations retained at `/tmp/kengaku-r26-FxMutP3A-ozfbk7q1/outputs/{pristine,mutated,restored}/*.capture.json` and `result.json`; detector source and `prepare.json` retained beside them.
## Restoration evidence
Before/restored SHA-256: `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
Mutated SHA-256: `3605c2b953fdbfbf5976d5f4d609ad956d393673bcf60fab426265f4a8aee9bd`.
Restored via `cp /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/state_check.py.pristine /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/integration/plans/state_check.py`; exit 0.
`cmp /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/state_check.py.pristine /tmp/kengaku-r26-FxMutP3A-ozfbk7q1/integration/plans/state_check.py` → no output, exit 0; `sha256sum` printed matching before/restored hashes. Mutant snapshot retained as `/tmp/kengaku-r26-FxMutP3A-ozfbk7q1/state_check.py.mutant`, not active.
No installs, builds, lint, formatters, network/model traffic or other runtime invocation. No production fix attempted; this is detector-coverage evidence, not a claim the pristine checker omits the check.
VERDICT: SURVIVED — BLOCKER under the assigned selftest/P3a-manifest detector; exact scratch bytes restored and restored detector PASS.
