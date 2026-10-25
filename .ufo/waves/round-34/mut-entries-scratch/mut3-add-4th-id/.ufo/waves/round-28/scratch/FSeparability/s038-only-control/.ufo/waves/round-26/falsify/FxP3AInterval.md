# FxP3AInterval — round 26 falsify

## Finding — Medium: P3a does not compare every numeric token in the capability cell

`plans/state_check.py:1173-1177` uses `re.search`, and `check_p3a()` at `:1225` enumerates only selected first-match patterns. It does not inventory/reject unparsed or duplicate numeric claims in the frozen capability row. On `/tmp/kx-p3a-duplicate-mut/SCORECARD.md:558`, I appended `duplicate unique_samples=999` after the correct `unique_samples=4`; v3 returned exactly the same P3a verdict map and total counts as the unmutated base. On `/tmp/kx-p3a-runid-mut/SCORECARD.md:558`, changing `(red runs R1–R6 included)` to `(red runs R1–R5 included)` likewise left every P3a assertion unchanged. The receipt has the red-run lines, but no P3a assertion checks the claimed run range. This leaves a contradictory numeric assertion able to survive the promised cell-to-receipt audit.

## Confirmed closures

- Frozen base v3: `P3a.capability.interval-reverdict.selftest-checks` is MISMATCH (`14,0` in SCORECARD vs `18,0` in `attrib-calibration-selftest-v2.txt`); `P3a.capability.state-assertion-check.base-mismatch` is MISMATCH (`11` vs `10`). Other nine P3a assertions MATCH. These are the two expected capability mismatches.
- Integrated revision `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`: `P3a.capability.interval-reverdict.selftest-checks` is SUPERSEDED at `SCORECARD.md:748` with exact derived tokens `18 checks`, `0 failed`; `P3a.capability.state-assertion-check.base-mismatch` is SUPERSEDED at `:749` with `mismatch=10`. Remaining nine P3a assertions MATCH.
- Wrong-target scratch mutation (`R26-E5` points to `P3a.capability.interval-reverdict.summary-exit`) leaves the selftest-count assertion MISMATCH; earlier R26-E1 citations are not accepted as an exact token set. Thus the integrated E5 closes the exact assertion/value, not a near-id.
- `state_check.py --selftest` passes and prints `P3a: red mutation and full-token R26-E`; this tests the stale 14→18 defect and full-token supersession.
- P2 population preserved on the same frozen base tree: v2 and v3 contain identical 247 P2 id/verdict pairs (same ids and same verdicts). No P2 re-scope observed.

## Commands and exits

- `git archive f11bffbf9caa9c9e286fb32c568b81b97719656a | tar -x -C /tmp/kx-p3a-base` — scratch base export.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 | tar -x -C /tmp/kx-p3a-int` — scratch integrated export; exit 0.
- `python3 /tmp/kx-p3a-base/plans/state_check.py --root /tmp/kx-p3a-base --json` — exit 0; v2 summary `235 assertions, mismatch=0`.
- `python3 /tmp/kx-p3a-int/plans/state_check.py --root /tmp/kx-p3a-base --json` — exit 1; v3 base `mismatch=5` (P3a IDs above, plus two P3b and P3e).
- `python3 /tmp/kx-p3a-int/plans/state_check.py --selftest` — exit 0; `[selftest] ALL PASS`.
- `python3 /tmp/kx-p3a-int/plans/state_check.py --root /tmp/kx-p3a-int --json` — exit 1; P3a E5/E6 superseded; remaining mismatches are `P3b.province.public-literature-registry.rows` and `P3b.province.round25-correction.rows`.
- Mutant runs, each exit 1 with P3a verdicts unchanged from v3 base: `python3 /tmp/kx-p3a-int/plans/state_check.py --root /tmp/kx-p3a-runid-mut --json`; `... --root /tmp/kx-p3a-duplicate-mut --json`.
- Wrong-id run, exit 1; `P3a.capability.interval-reverdict.selftest-checks` MISMATCH: `python3 /tmp/kx-p3a-int/plans/state_check.py --root /tmp/kx-p3a-e5-badid --json`.

## Residual risk and verification gaps

Integrated v3 still exits 1 on the two P3b mismatches listed above; this P3a-only seat did not inspect their causes. LSP device is unavailable (`read xd://lsp` returned “No such tool”); no LSP references/definition/diagnostics were available. No installs or lane/live-tree modifications were made; all test mutations were under `/tmp`.

VERDICT: FALSIFIED — P3a catches the stale fourteen and exact E5 repair, but its “every numeric token” coverage claim is not met.