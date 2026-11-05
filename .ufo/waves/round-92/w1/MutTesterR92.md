# MutTesterR92 — scoped findings (round 92, wave w1)

Judged on: coverage, calibration, operability. Mutation battery only; no repairs to the lane.
Full mutant lines and controls: `.ufo/waves/round-92/w1/MutTesterR92/report.md`; receipts in
`.ufo/waves/round-92/w1/MutTesterR92/receipts/`.

## Coverage (R92-C1, the tenth replay)

- The counter is sensitive to the things it reads: a case-table vector flip (L4, L5, L6, L9), a wrong
  frozen table sha (L4), a case-id parse regression (L5), a wrong executed total (L7). The bs probe's bwrap
  guard fires (`DEFECT SETUP sandbox-unavailable`, rc 2).
- Blind spot: the packer slot budget 36 -> 40 yields byte-identical plans for all 19 case inputs, so the
  rerun (L6) cannot see it. Only the tool pin (L8) and the stamp (L9) catch it. The frozen input does not
  exercise the budget; this is a coverage gap in the 10-case table, not in the counter.
- Pre-flip, L7 is red at both 35 and 36 (member unexecuted); the executed-total mutant is only measurable at
  the flip. Control C-sim (scratch reconstruction, disclosed) is green (rc=0), so the C1 kills are real.

## Calibration (R92-C2, counter conformance)

- M7 and M12 behave as predicted on the BASE and tip-of-control counters (base red, tip green / closed).
- M9 is not green at B2: `plans/round91_counter_pin.py` still carries `--skip-selftest` in its docstring
  (lines 16 and 211), so `tip-flag-absent=False`. The flag check is literal-hyphen only: an underscore-only
  spelling passes both the original and the weakened check (survivor). Only the self-pin catches a byte edit.
- Conflicts that the commit-C flip would create: (a) the probe's tool pin (required by C1 L8) raises the pin
  count to 18, breaking M9's literal `PINS checked=17`; (b) the ledger flip turns the round-91 counter red on
  the M7 tip leg (`executed_total=36`).

## Operability (R92-C3, gate v3)

- The `--selftest` battery is correct at the control: 10/10 red-green, with each mutant turning exactly its
  named case red (chain walk, vacuous check, owner lane-id).
- The default predicate path does not complete: the selftest child is not recognised as a child (the parent
  argv lacks `--selftest`), so it recurses and dies by a 600 s TimeoutExpired with no PREDICATE line.
- The gate's BATTERY skip is forgeable: a planted marker file in `--work` (no parent proof) makes the default
  run print `PREDICATE R92-C3-BATTERY pass` with zero SELFTEST lines. The in-child proof is unchanged by the
  mutant; only the existence check was added.
- At B2 the gate refuses (`freeze=refused pending=1 malformed_unresolved=1`, `check-failed R82-V8`); the
  predicted `freeze=admitted pending=0` is not reached. The R82-F1 row is schema-invalid, not a chain, so the
  chain-aware resolver does not clear it.
- M6 does not hold inside the gate: `run_check` strips SHOKUNIN_ROOT, so R82-V8 falls back to the worktree's
  `origin.parent` and fails. With SHOKUNIN_ROOT present the same check passes. The check is therefore still
  clone-path dependent under the gate.

## Named defects (not repaired; for the L1 integrator)

1. M9 red at B2 (docstring `--skip-selftest`).
2. PINS count conflict (C1 L8 vs C2 M9 literal 17).
3. Commit-C flip breaks round-91 M7 tip leg (L7 executed_total).
4. Gate default path recursion; no PREDICATE line from the default invocation.
5. Gate BATTERY-skip forgery via planted marker file.
6. R82-V8 clone-path dependence under the gate (SHOKUNIN_ROOT not propagated).
7. B2 gate refused (R82-F1 malformed line 125, R82-V8).
8. bs-probe stamp `WORKTREE` always `dirty` (empty-output `absent` sentinel).

## Tooling and bounds

- No tool installs or upgrades. Existing `/usr/bin/python3` (3.14.8), git, /usr/bin/bwrap and
  /usr/bin/openssl (3.6.5) were used. Passwordless sudo and pacman were not touched.
- No lane, fleet-root, sibling or lane-index mutation; all `--work` dirs under scratch; the lane's
  `.ufo/waves/round-92/w1/MutTesterR92/` receipts are the only writes outside scratch.
- Scratch `/fast/scratch/hyaku/kengaku-r92/MutTesterR92/` removed before yield.
