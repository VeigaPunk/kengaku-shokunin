# ExecC3GateBattery — scoped findings (R92-C3, measured at B2 f0018773)

Full record: `ExecC3GateBattery/report.md` and `ExecC3GateBattery/controls.txt`; receipts in
`ExecC3GateBattery/receipts/`.

Judged on: coverage, calibration, operability.

## Coverage
- Standalone selftest: 10/10 red-green (control 4 passes).
- The predicate-path battery (M8) never completes. Child gates re-run the battery without end
  (F-1). No selftest case resolves an invalid root (F-2). Green selftest does not cover the
  predicate path.

## Calibration (expected vs observed)
- Control 1 (B2, v3): expected pending=0 and no DEFECT. Observed refused, pending=1 from the
  malformed root `line 125 / R82-F1`, plus `check-failed R82-V8`. Predicate not met.
- Control 2 (BASE, v3): expected three override-unjustified DEFECTs with oldest 82. Observed
  refused, pending=1, oldest 10000, same two DEFECTs. Mismatch.
- Control 3 (BASE-era ledger via v2 at B2): matches the do-nothing expectation, plus one extra
  `check-failed R82-V8` (F-3).

## Operability
- F-1 `in_child_mode` requires `--selftest` in the parent argv (round92_burndown.py:553-567). The
  predicate invocation's children therefore recurse, 600 s per level, and the process dies with
  a traceback (rc 1), printing no freeze/PREDICATE line.
- F-2 invalid-root resolution uses `chain_end_cache.get(sid, sid)` (line 263) and never calls
  `chain_end(sid)`. R82-F1 (line 125) -> R82-F1-R90 (line 213) -> R82-F1-R91 (line 214, closed) is
  never walked from the root. [INFERENCE on mechanism; observed on the real ledger.]
- F-3 `run_check` (line 157) passes only PATH/HOME/LANE; checks never receive SHOKUNIN_ROOT, so
  R82-V8 falls back to the gate's own scratch parent and fails. Reproduced in a scratch worktree
  (`CHECK v8 fail` under the gate env; `CHECK v8 ok` with SHOKUNIN_ROOT set). The same shape is in
  round91_burndown.py (line 120).
- F-5 (disclosed, not a gate defect): without SHOKUNIN_ROOT and a clone whose parent lacks
  shokunin.conf, the gate fails closed with rc 2.

## Status
- R92-C3 predicate at B2: not met (F-1, F-2, F-3 each block it).
- Lane master beyond B2 already holds repairs for all three defects (`a0c7438a` E5,
  `b72c83e9` E6, `dd48027f` E7). Those are post-freeze; the L1 decides what T is.
  Not tested here (outside the pinned scope).
- Open question for the L1: confirm F-2 on a one-level fixture before the repair route is chosen.

## Tools
None installed or updated.
