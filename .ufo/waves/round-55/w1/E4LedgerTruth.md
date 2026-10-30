# E4LedgerTruth — scoped findings (Report trailer)

Full detail in `.ufo/waves/round-55/w1/E4LedgerTruth/report.md`.

- Corrected `round35-c1-coverage` in `plans/round54-entrytruth.json` from a re-measured
  run on a clean clone at `80afa613` (base `798f5e9e` + freeze): the declared fragment
  was stale (r54 receipt `EVIDENCE-MISSING`); the row stays `red` exit 1 with the
  verbatim current fragment `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)`.
  Observed output committed at `E4LedgerTruth/round35-c1-output.txt`.
- Added five rows, each from its own r54-style hermetic measurement (Worker/run_row,
  scratch work dir), schema/shape identical to existing rows; ledger now has **83** rows:
  - `round54-c1` (hand-contract verify entry) — red exit 1, evidence
    `ModuleNotFoundError: No module named 'opentimestamps'` (r54 scratch venv gone).
  - `round54-c2` (`--lane .`) — red exit 2, evidence `SETUP --source and --work are
    required unless --dry`. The full-flags form was measured too (exit 1, 426.3 s,
    `EVIDENCE-MISSING round35-c1-coverage` + `LAUNDERED round52-c2`) but is
    un-declarable at this tip and would self-recurse at the R55-C2 after-run — see
    defect 4 in the report.
  - `round55-c2` (bare) — red exit 2, same SETUP evidence.
  - `round55-c2-controls` (bare) — red exit 2, evidence `one of the arguments --case
    --selftest is required`.
  - `round55-c3` (bare, working-tree probe overlaid) — green exit 0, real 12-case bwrap
    battery `cases=12 observed_pass=5 observed_fail=7 mismatches=0`.
- Entry argv forms coordinated token-exactly with `E1RegistryRows` for the R55-C2 L1
  binding leg; validated in a landing simulation (five synthetic registry cells):
  the five rows appear in no defect list; r54 dry legs `argv_defect=0 bad_decl=0`.
- Defects flagged for their owners (not touched, per seat bounds): 17 pre-existing
  ledger↔registry argv mismatches (placeholder cells) and `tb2-grader-probe`'s uv-wrapper
  argv (L2 kill under the new counter) must be reconciled by the L1 for the R55-C2 after
  predicate; `round54-c1`'s verify entry needs an `opentimestamps` interpreter to run.
- Files written: `plans/round54-entrytruth.json` (only lane file) plus
  `E4LedgerTruth/{report.md,measurements.json,*-output.txt}`. No installs. Scratch
  `/fast/scratch/hyaku/kengaku-r55/E4LedgerTruth/` removed.
