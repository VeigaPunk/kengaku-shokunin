# Seat E2EntryArgvCounter — round 55 wave 1 report

## Assignment
NEW `plans/round55_c2_entryargv.py` — the R55-C2 entry-argv structural binding counter
(frozen contract: `plans/round-55-claims.md` §R55-C2). Only file written:
`kengaku-shokunin/plans/round55_c2_entryargv.py` (plus this report dir under `.ufo/waves/`).
No sibling file touched; no mutating git anywhere (read-only `git -C` only, all inside
scratch fixtures with a toplevel guard).

## What was built
- Imports the **unchanged** r54 module via importlib (`_load_r54`, same pattern as
  `round55_c2_controls.py::_load`) and reuses `static_legs`, `registry_rows`, `row_script`,
  `load_ledger`, `hermetic_env`, `Worker`, `run_row`, `git_rev`, `MIN_REASON_WORDS`,
  `REGISTRY_HEADING`/`LEDGER`/`SCHEMA` (rebound as REGISTRY/LEDGER/SCHEMA).
- `registry_entry_argv(line)`: first backtick span in the entry cell starting with `python3`,
  `shlex.split`, None if absent/unparseable.
- Three binding legs in `binding_static_legs(root)` (each its own ROWS field + `  <TAG>` line):
  - L1 `ARGV-DEFECT` — ledger `entry_argv` token-list != registry cell argv (exact equality;
    merged into the r54 `argv_defect` list so the frozen ROWS field covers it).
  - L2 `WRAPPER-DEFECT` — argv[0] not in {python3, python}, or any token in
    {uv, pipx, poetry, npx, uvx} or starting with `-c`.
  - L3 `ABBREV-DEFECT` — an argv flag token absent verbatim from the script body but a proper
    prefix of a body flag (argparse abbreviation, no execution).
- `evaluate(lane, source, work, jobs, timeout, dry)` — r54 shape: same ROWS fields plus
  `wrapper_defect=N abbrev_defect=N`, per-defect lines, `BINDING l1 l2 l3` line, SOURCE,
  RUN/TIPSTATE/MIGRATION, `PREDICATE R55-C2 pass|fail`, exit 0/1/2. `static_ok` also requires
  the three new lists empty. L4 execution runs the **registry cell argv** (overridden into the
  row spec) through r54's Worker/run_row hermetic path. `--dry` = static legs only.
- CLI exactly `--lane --source --work --jobs --timeout --dry --selftest`. Selftest fixtures
  live under `--work` or TMPDIR (never a hardcoded /tmp) and reuse the controls module's
  git-fixture shape with a `git rev-parse --show-toplevel` guard.

## Commands run and observed exits (receipts in this directory)
| command | exit | evidence file |
|---|---|---|
| `python3 plans/round55_c2_entryargv.py --selftest` | 0 (4/4 PASS) | `selftest.txt` |
| `python3 plans/round55_c2_entryargv.py --selftest --work <scratch>` | 0 (4/4 PASS) | run interactively |
| controls `--case abbreviated-selftest --against r55` | 0 (kill demonstrated; counter exit 1) | `fixture-kill-abbreviated-selftest.txt` |
| controls `--case uv-decoy-script --against r55` | 0 (kill demonstrated; counter exit 1) | `fixture-kill-uv-decoy-script.txt` |
| controls `--selftest` (before-state: r54 passes both laundering fixtures) | 0 | `controls-selftest-before-state.txt` |
| counter `--dry --lane <lane>` | 1 (mid-wave defects, expected) | `dry-lane-working-tree.txt` |
| counter full run `--lane/--source <lane> --jobs 8 --timeout 45` | 1 (mid-wave, expected) | `full-lane-working-tree.txt` |

Fixture-kill attribution, as frozen: abbreviated-selftest → `ARGV-DEFECT fixture-gate:` (L1) +
`ABBREV-DEFECT fixture-gate:` (L3); uv-decoy-script → `ARGV-DEFECT fixture-gate:` (L1) +
`WRAPPER-DEFECT fixture-gate:` (L2); both `PREDICATE R55-C2 fail`, counter exit 1.

## Defects found (DATA — reported, not fixed; none are in my file)
Working-tree static state (mid-wave): `ROWS registry=78 ledger=78 missing=0 extra=0
argv_defect=17 wrapper_defect=1 abbrev_defect=0 … headings=1`, `BINDING l1=17 l2=1 l3=0`.
- 16 L1 mismatches where the SKILL registry cell uses placeholder tokens (`<expect.json>`,
  `DIR`, `REV`, `[--evidence-ref head or index]`, `PATH...`, `<clean git clone of the landing
  tip>` etc.) while the ledger row carries the resolved argv: adoption-check,
  anchor-digest-check, coverage-census, gate-flip-check, gate-timing, ledger-tip,
  mutant-direction-check, package-gate, round-close-check, round28-census, round50-c1,
  round53-c2, scratch-root-guard, sources-adopt, stage-scan, tip-receipts.
- `tb2-grader-probe`: registry entry cell has no `python3` backtick span AND ledger argv[0] is
  a `uv` wrapper (`uv run --no-project --with biopython==1.85 python3 …`) → L1 + L2 defects.
  This is exactly the wrapper class R55-C2 L2 exists to surface; the row needs a data
  correction (registry cell + ledger argv rebound to a plain `python3 …` entry, or a frozen
  amendment) before the after-run.
- Full run (45 s cap, mid-wave): 9 TIMEOUTs (my cap, not the frozen 900), 1 EVIDENCE-MISSING
  (`round35-c1-coverage` — the frozen claims doc schedules its evidence re-derivation this
  round), 1 LAUNDERED (`round52-c2` declared green, entry exit 1 — the known r54 regression
  under repair by the R55-C1 seat right now). All expected mid-wave; the predicate can only
  pass at the measured-after revision after the L1's data corrections.

## Dead ends / notes
- Cloning the lane and running the counter from the clone fails: the clone only has committed
  bytes and my file is uncommitted until the L1 integrates (`full-clone-attempt.txt`). The
  after-run at the measured-after revision is unaffected.
- One design iteration during the seat: my first binding loop skipped L2/L3 once L1 fired,
  which suppressed the frozen `WRAPPER-DEFECT`/`ABBREV-DEFECT` attribution; fixed by running
  all three legs independently (they are independent defect lists).
- No tools installed; no pacman; nothing written to PATH dirs; no fleet-root tracked file
  touched. Scratch dir deleted after staging receipts.
