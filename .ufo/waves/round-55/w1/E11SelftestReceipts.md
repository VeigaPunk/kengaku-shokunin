# E11SelftestReceipts — scoped findings (R55-C1 leg 2)

Seat E11SelftestReceipts · 2026-10-30 · measured committed tip `248a42b8` (round-55 honest-stop)

## Bottom line
Every round-55-added registry row's self-test that could be executed **matches** its authored
verdict-map/self-test cell. **No false cell found** — so C1 leg 2's kill rule is NOT triggered
by any observed verdict. Leg 2 is, however, only **partially evidenced** because the five rows
and two of the instruments were authored in the working tree but **never committed** (the wave
was released un-settled at the honest-stop tip; the L1 integration commit did not land within
this seat's ~50 min of bounded waits).

## Per-row leg-2 result
- **round54-c1** — self-test `…anchor.py selftest`. Clean-clone under the round-54 opentimestamps
  venv: `8/8 PASS`, exit 0 (= cell). Bare-host control: exit 1 `ModuleNotFoundError` (= cell's
  documented bare-host branch). **MATCH (both branches).** Interpreter dependency is documented
  in the cell, not a defect.
- **round54-c2** — `--selftest`: `7/7 PASS`, exit 0 from clean clone. **MATCH.**
- **round55-c2-controls** — `--selftest`: `cases=4 failures=0`, exit 0 from clean clone. **MATCH.**
- **round55-c2** — `--selftest`: clean-clone run **blocked** (instrument uncommitted); work-tree
  diagnostic `4/4 PASS`, exit 0 (= cell). **PENDING commit; would MATCH.**
- **round55-c3** — `--selftest`: clean-clone run **blocked** (instrument uncommitted); work-tree
  diagnostic `cases=2 failures=0`, exit 0 (= cell). **PENDING commit; would MATCH.**

## Findings
1. No verdict-map cell is false; leg-2 kill rule not fired by any self-test.
2. round54-c1's self-test is venv-gated by design and the cell says so — earlier bare-host-only
   concern withdrawn.
3. round55-c2 / round55-c3 self-tests are not clean-clone-runnable at the tip (uncommitted
   instruments); full closure requires the L1 integration commit.

## Defect (process, not cell)
The five rows + two instruments were left uncommitted at the honest-stop tip; leg 2 cannot be
fully closed for round55-c2 / round55-c3 until they land.

Evidence: `.ufo/waves/round-55/w1/E11SelftestReceipts/` (per-row receipts + report.md).
