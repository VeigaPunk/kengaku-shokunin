# R2C2FixturesRepro — scoped findings (R55-C2 red-before reproduction)

**Scope:** independent rebuild of the two frozen R55-C2 laundering fixtures with my own
minimal builder and re-demonstration of the red-before state vs the committed
before-receipts. Calibration target.

## Findings

1. **Red-before state reproduced — both frozen cases.** My independently-built
   one-row scratch git fixtures (registry row `fixture-gate`, entry
   `python3 plans/fixture_gate.py`, gate exiting 1 with
   `entry failed: fixture gate is broken on purpose`) run under the **unchanged**
   `plans/round54_c2_entrytruth.py` print `PREDICATE R54-C2 pass`, counter exit 0, on both
   `abbreviated-selftest` (ledger argv `python3 plans/fixture_gate.py --selft`, argparse
   prefix abbreviation, declared green) and `uv-decoy-script` (ledger argv
   `uv run --no-project --offline python3 -cprint('wrapper green') python3 plans/fixture_gate.py`,
   declared green). Ground truth: the registry-declared entry run directly exits 1 on both.
   Receipts: `R2C2FixturesRepro/repro-{abbreviated-selftest,uv-decoy-script}.txt`.
2. **Receipt comparison: MATCH modulo per-fixture commit hash.** Every output line of both
   reproductions equals the committed `.ufo/waves/round-55/claims/c2-before-*.txt` receipts
   except the `SOURCE rev=` line, which necessarily differs because each fixture is its own
   scratch git repository (my revs `36835d6e…` / `6682f5c3…` vs committed `82c52797…` /
   `8d00e0a2…`). No semantic divergence.
3. **Byte-level equivalence to the frozen fixture spec.** Oracle cross-check (committed
   `plans/round55_c2_controls.py::_fixture` used for verification only, not as my builder):
   all six tree files (`SKILL.md`, `plans/fixture_gate.py`,
   `plans/round54-entrytruth.json` × 2 cases) are byte-equal between my fixtures and the
   committed builder's. My builder `build_and_run.py` is original code written from the
   frozen claims spec.
4. **Mechanism confirmed live.** The r54 counter's `entry_mode_ok` flags neither argv
   (`--selft` is outside the forbidden-token set; the `uv` argv passes the
   python3+script scan) and its verdict is unwired in r54 (`entry_mode_ok=None` in the
   r54 probes), so both rows execute hermetically green while the declared entry is truly
   red — the exact structural gap R55-C2's new binding legs (L1–L4) close.

## Defects found

None in scope. No divergence from the committed before-receipts beyond the explained
`SOURCE rev=` line.

## Residual risk / gaps

- The r55 binding counter `plans/round55_c2_entryargv.py` is being built by other seats
  this wave; kill-line verification (`ARGV-DEFECT` / `WRAPPER-DEFECT`) at the
  measured-after revision is outside this seat's target and unrun here.
- `uv` availability (0.13.0) on the shared host is load-bearing for the uv-decoy case;
  a host without `uv` would turn the row into an ERROR mismatch rather than a laundered
  green. The committed receipt already demonstrates the laundered route on this host class.
