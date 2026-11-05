# ExecC2Battery — R91-C2 control battery report

Full table with commands, rc and first defect lines: `controls.txt` (same directory).
Subject: `plans/round91_counter_pin.py` + `plans/counter-pins-r91.json` at tip C `a8de3e69`.
Work done in a scratch clone; the lane was not modified. No tool installs.

## Verdicts

| Control | Expected rc | Observed rc | Match | First defect |
|---|---|---|---|---|
| 1 positive (no skip) at a8de3e69 | 0 | 0 | yes | none; PINS 16/16, SELFTEST 8/8, PREDICATE pass |
| DN do-nothing at BASE 59764383 | 2 | 2 | yes | DEFECT SETUP unreadable plans/counter-pins-r91.json |
| 2 one-space append, round88_claim_figures.py | 1 | 1 | yes | DEFECT PIN-MISMATCH bytes plans/round88_claim_figures.py |
| 3 delete round91_burndown.py | 1 | 1 | yes | DEFECT PIN-MISMATCH absent plans/round91_burndown.py |
| 4 one-byte round89-q66-records.json | 1 | 1 | yes | DEFECT RECORD-TABLE mismatch plans/round89-q66-records.json |
| 5 checker-only self-leg forced green, committed, ledger untouched | 1 | 1 | yes (rc) | DEFECT PIN-MISMATCH bytes plans/round91_counter_pin.py (table leg fires first; SELF-PIN not reached) |
| 6 checker + ledger regenerated in one commit (`--skip-selftest`) | disclosed residual, expected pass | 0 | residual observed | PREDICATE R91-C2 pass |
| 7 blob-anchor-missing expectation weakened, pin not regenerated | 1 with SELFTEST lines | 1 | yes | DEFECT PIN-MISMATCH bytes plans/round91_counter_pin.py; weakened case stays green |
| 8 delete counter-pins-r91.json | 2 | 2 | yes | DEFECT SETUP unreadable plans/counter-pins-r91.json |

## Findings beyond the expected list

1. **Dirty-tree self-leg bypass is not closed by the self-pin leg when the selftest is skipped (5b).** An uncommitted edit that forces the self-pin comparison off, run against the clean pinned tip `a8de3e69` with `--skip-selftest`, exits 0 with `PREDICATE R91-C2 pass`. The table passes because the committed bytes match the pin, and the running copy never compares itself. Without `--skip-selftest` the same edit exits 1 via `SELFTEST self-pin-mismatch rc=0 want=1` (5b-full). The in-path selftest is the only thing that catches it, so the claim's self-pin narrowing depends on the selftest running. This route is not named in the claim text.
2. **Weakened selftest expectation plus regenerated pin passes (7b).** Changing one red case's expected string to `""` and regenerating the pin in one commit exits 0 with `SELFTEST cases=8 red-green-ok=8`. The selftest does not detect a weakened expectation of its own red cases. Same residual class as control 6, now on the selftest path. Not named in the claim text.
3. **Control 6 residual confirmed as stated.** One commit (checker + pin) passes `--skip-selftest` (rc 0). The default run catches the self-leg variant (6b, rc 1). Residual survives with `--skip-selftest` and for weakened selftest expectations (7b).
4. **Selftest summary line is inconsistent (cosmetic, 7c).** When one case fails, `SELFTEST cases=8 red-green-ok=0` prints while `SELFTEST-DETAIL` prints `red-green-ok=7`. The summary is all-or-nothing and disagrees with the detail line.
5. **Control 5 first-defect wording.** The rc matches "self pin", but the first defect line is `PIN-MISMATCH bytes` on the checker's own entry. The self-pin leg never executes for a committed edit; it fires only for an uncommitted running-file change (5c: `SELF-PIN-MISMATCH plans/round91_counter_pin.py`, rc 1, confirmed).

## Mispredictions (recorded, not repaired)

- SELFTEST case count: claims file predicted `C = 6`; measured `8`. PINS count `K = 16` predicted and measured (13 sha + 3 blob).

## Installs

None.

## Checks the main agent should run

- `python3 plans/round91_counter_pin.py --lane <lane> --rev a8de3e69 --work <scratch>` → expected rc 0 (control 1 reproduced).
- The residual and selftest-path findings (1, 2) belong in the R91-C2 claim's residual list before the score is recorded.
