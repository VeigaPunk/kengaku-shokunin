# R7ProbeOracleAudit — scoped findings (R55-C3 probe oracle audit)

Seat: R7ProbeOracleAudit (reviewer, leaf). Target: `plans/round55_c3_chess_probe.py`
(sha256 `7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60`, lane working tree;
**untracked at tip `80afa613…`** — see Defect D1). Read-only audit; no lane writes. All
experiments in `/fast/scratch/hyaku/kengaku-r55/R7ProbeOracleAudit/` (deleted after copying
receipts here). Full report: `report.md` in this directory.

## Verdict
All five in-scope properties hold. 14/14 attack checks pass. One lane-hygiene defect (untracked
instrument) and one presentation-level ambiguity (double-escaped frozen card) are named; neither
is an oracle hole. No input found that can make an observed≠predicted case print `mismatches=0`
or exit 0, and no input can steer a verdict outside the pinned grader's own execution.

## Checked properties (evidence in `attacks-receipt.txt`, `probe-stdout.txt`)

1. **Verdict derives only from the captured grader's own test function in bwrap — HOLDS.**
   The executed oracle string is only `import test_outputs as t; t.test_move_correct()` with
   `/tests` at `sys.path[0]`; the probe itself never reads `move.txt` or re-derives the
   assertion (verdict = rc 0 → P; `AssertionError` in output → F; else SETUP, exit 2).
   - Any grader other than the pinned capture is refused before any case runs (sha gate,
     attacks `sha-gate-tampered-capture`, `sha-gate-alternative-grader`: exit 2, no CASE lines).
   - 12/12 probe verdicts equal direct, independent bwrap executions of the same function
     (attack `probe-verdicts-equal-direct-grader-executions`).
   - Raw-semantics proof: `fullwidth-unicode-digit`, `uppercase-white`, `duplicate-move`
     all observe F exactly as the un-normalized grader dictates.
2. **`/tests` bound read-only; capture is a runtime-sha-checked byte-copy — HOLDS.**
   `materialize_grader` sha256-checks the lane capture against the frozen pin and writes those
   same bytes; the sandbox mounts the copy with `--ro-bind`. A write to `/tests` inside the
   sandbox fails `EROFS` (attack `tests-readonly-write`); the in-sandbox file hashes to the
   pin (attack `tests-bytecopy-in-sandbox-sha`). Four-way pin equality verified: probe constant
   `a540714e…30cb8f286` = claims doc = in-repo capture = upstream
   `harbor-framework/terminal-bench-2@2fd12b88…/chess-best-move/tests/test_outputs.py`
   (read-only GET, HTTP 200, `cmp` byte-identical).
3. **12-case table matches the frozen list byte-for-byte — HOLDS (with a naming caveat).**
   The frozen card (w1-spec.json / w1-dispatch.json E5ChessProbe item) and the probe agree on
   all 12 names, order, bytes, and predictions. The card renders bytes double-escaped
   (`\\n` for LF) because `build_spec_w1.py` stores single-escaped strings and emits `{b!r}`;
   the probe's table equals the card decoded two levels (and equals `build_spec` CASES after
   one `unicode_escape`), all 12 rows. The reading is objectively forced: the literal
   backslash-n reading makes the PASS-predicted two-line case FAIL under the pinned grader
   (attack `candidate-B-bytes-contradict-frozen-PASS`), while the probe's bytes reproduce all
   12 frozen predictions in 4 independent runs (E5 verify, E6 run1/run2, this audit — all
   byte-identical).
4. **A mismatch necessarily changes printed M and the exit code — HOLDS.**
   Code: `mismatches` increments on every observed≠predicted (non-SETUP), is printed in the
   summary line, and drives exit 0 iff 0 (else 1; any SETUP forces 2). Verified live: flipping
   one prediction → `mismatches=1`, exit 1, `PREDICATE R55-C3 fail`
   (attack `prediction-flip-counts-mismatch`); flipping one case's bytes → its observed verdict
   flips, `mismatches=1`, exit 1 (attack `case-byte-flip-changes-observed-and-mismatch`).
   Within the frozen table SETUP is unreachable from case bytes (the probe always writes valid
   UTF-8; the grader can only exit 0 or raise AssertionError), so an observed≠predicted verdict
   cannot be laundered through SETUP without failing the whole run with exit 2.
5. **No case's outcome can depend on wall-clock/network/env — HOLDS.**
   Sandbox is `--unshare-all` (network namespace included): a connect to 1.1.1.1:80 fails with
   OSError and `/proc/net/dev` shows only `lo` (attacks `no-network-in-sandbox`,
   `only-loopback-in-sandbox`). The child env is exactly the fixed 7-var `ENV`; runs under
   hostile ambient env (PYTHONHASHSEED 0/424242, LANG C/ja_JP.UTF-8, TZ UTC/Kiritimati,
   TMPDIR=/nonexistent, HTTPS_PROXY, PYTHONPATH) are byte-identical to baseline (attacks
   `hostile-env-run-0/1`). No time reads exist; two runs plus the landed receipt are
   byte-identical (attacks `determinism-two-runs-byte-identical`,
   `matches-landed-corpus-receipt`). Measured wall time 0.38 s for the battery; per-case
   timeout 120 s ⇒ worst-case 24 min ≤ the 25-min bound.

## Defects / holes (none exploitable into a false pass)

- **D1 (lane hygiene, not an oracle hole):** `plans/round55_c3_chess_probe.py` is untracked
  (`??` at tip `80afa613`). A clean-clone after-run would lack the instrument. L1 must commit
  it before the clean-clone re-verification. (Also flagged by E6ChessReceipt.)
- **D2 (presentation ambiguity, grounded):** the frozen card's byte notation is double-escaped;
  a seat mechanically copying the card into source would produce backslash-literal bytes that
  contradict the frozen predictions under the pinned grader (attack input: `g2g4\ne2e4\n` as
  literal-backslash single-line bytes → F against a frozen PASS). The probe avoids this; the
  claims-doc wording ("frozen case table … byte-identical") is the anchor that forced the
  correct reading. No probe change needed; no lane write made.
- **D3 (harness heuristic, conservative):** the F/SETUP boundary keys on the literal output
  string `AssertionError`. For this capture the only nonzero-exit path is the assert, so F
  detection is exact; for any future grader whose failure raises another exception, the case
  becomes SETUP (exit 2) — an honest failure, never a hidden mismatch.

## Residual risk
None identified beyond D1–D3. The oracle is the pinned capture's own `test_move_correct`
executed in a namespace-isolated, read-only-/tests, network-less sandbox with a fixed env;
the verdict table is observational, the counting is live, and the identity gate is
sha-enforced at runtime and independently re-verified against upstream at the pin.
