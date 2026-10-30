# E4LedgerTruth — kengaku round 55 wave 1 (v2) seat report

Scope: data corrections only in `plans/round54-entrytruth.json` (R55-C2 ledger-truth step)
plus this report/outputs under `.ufo/waves/round-55/w1/E4LedgerTruth/`.

## Base

Clean shared clone of the lane at `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
(base tip `798f5e9e…` + the frozen claims commit) under
`/fast/scratch/hyaku/kengaku-r55/E4LedgerTruth/lane` (`git clone --shared`).
Measurements ran against the clone at that revision; the two round-55 scripts not yet
committed (`plans/round55_c2_entryargv.py`, `plans/round55_c3_chess_probe.py`) were
overlaid from the lane working tree into a copy of the clone for their rows.

No tools installed or upgraded (none needed).

## What I ran (commands and observed exits)

1. `python3 plans/round35_c1_verify.py --lane .` (cwd = clone root) — **exit 1**, 0.5 s.
   Full output committed at `round35-c1-output.txt`:
   `V1 ok / V2 ok / V3 ok / V4 DEFECT knowledge files=58 index rows=58 (want 42/42) / V5 ok / V6 ok / checks=6 defects=1 / PREDICATE C1 fail`.
   The stale r54 fragment (`files=57 …`) is gone — the row's evidence is corrected to the
   verbatim `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)`; stays `red`, exit 1.
2. Five hermetic runs through the unchanged r54 module's `Worker`/`run_row` pattern
   (imported from `plans/round54_c2_entrytruth.py` on the clone), each in a scratch work
   dir under the seat scratch root:
   - `round54-c1` — argv `python3 plans/round54_c1_anchor.py verify --anchor corpus/evidence/round54/anchor --claims plans/round-54-claims.md --source . --work work/anchor-verify-row --controls` → **exit 1**, 0.4 s: `ModuleNotFoundError: No module named 'opentimestamps'` (the r54 OTS venv was scratch-only and is gone; no interpreter on this host has the library). Declared red, evidence verbatim.
   - `round54-c2` — argv `python3 plans/round54_c2_entrytruth.py --lane .` → **exit 2**, 0.6 s: `SETUP --source and --work are required unless --dry`. Declared red, evidence verbatim.
   - `round55-c2` — bare `python3 plans/round55_c2_entryargv.py` (working-tree file overlaid) → **exit 2**, 0.1 s: the same SETUP line. Declared red, evidence verbatim.
   - `round55-c2-controls` — bare `python3 plans/round55_c2_controls.py` → **exit 2**, 0.3 s: argparse `one of the arguments --case --selftest is required`. Declared red, evidence verbatim.
   - `round55-c3` — bare `python3 plans/round55_c3_chess_probe.py` (working-tree file overlaid) → **exit 0**, 0.4 s: real 12-case bwrap battery, `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`. Declared green.
   Per-row verbatim outputs: `round54-c1-output.txt`, `round54-c2-output.txt`,
   `round55-c2-output.txt`, `round55-c2-controls-output.txt`, `round55-c3-output.txt`;
   consolidated `measurements.json`.

## Files written

- Lane: `plans/round54-entrytruth.json` only. Diff vs HEAD: 73 insertions, 3 deletions —
  the `round35-c1-coverage` row (evidence/reason/sec) plus five new rows
  (`round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`)
  inserted in the file's existing alphabetical key order. No other row touched.
- Seat outputs: this `report.md`, `round35-c1-output.txt`, `round54-c1-output.txt`,
  `round54-c2-output.txt`, `round55-c2-output.txt`, `round55-c2-controls-output.txt`,
  `round55-c3-output.txt`, `measurements.json` in `.ufo/waves/round-55/w1/E4LedgerTruth/`.
- Scoped findings also at `.ufo/waves/round-55/w1/E4LedgerTruth.md` (Report trailer).

## Verification (all run)

- `python3 -c "import json;…print(len(d['rows']))"` → **83** (78 + 5).
- `git diff -- plans/round54-entrytruth.json` → only the changes above.
- r54 counter dry on the lane (`python3 plans/round54_c2_entrytruth.py --lane . --dry`):
  `registry=78 ledger=83 … argv_defect=0 bad_decl=0 … extra=5` — the five extras are the
  registry rows E1RegistryRows authors this wave; my rows raise no static defect.
- Landing simulation (clone + my ledger + five synthetic SKILL.md registry cells whose
  first `python3` backtick span token-mirrors each committed argv, rows inserted inside
  the registry table):
  - r55 counter `--dry`: `registry=83 ledger=83 missing=0 extra=0 argv_defect=17
    wrapper_defect=1 abbrev_defect=0 bad_decl=0 …` — every listed defect is a
    pre-existing row (17 placeholder-token mismatches such as `ledger-tip`,
    `stage-scan`, `sources-adopt`, and `tb2-grader-probe`'s `uv`-wrapper argv, which the
    new counter's L2 leg kills). **None of my five rows appears in any defect list.**
  - r54 counter `--dry` on the same tree: `argv_defect=0 bad_decl=0`.

## Coordination

The five committed `entry_argv` forms were fixed in messages to seat `E1RegistryRows`
(the SKILL.md registry-row author) so its cells' first `python3` spans are token-equal
to the ledger (R55-C2 L1 leg): verify-form for `round54-c1`; `--lane .` SETUP form for
`round54-c2`; bare for the three round-55 rows. E1 acknowledged and was composing its
row edit with these tokens at yield time.

## Defects found (reported, not fixed — outside my write scope)

1. `round35-c1-coverage`'s declared evidence fragment no longer appeared in the entry's
   output (r54 receipt `EVIDENCE-MISSING`) — corrected by this seat.
2. `round54-c1`'s advertised verify entry crashes at import (`opentimestamps` lived only
   in the r54 scratch venv) — declared red with the verbatim traceback fragment.
3. Pre-existing binding debt the L1/integration must close for R55-C2's after predicate:
   17 ledger rows whose `entry_argv` does not token-equal their registry cell
   (placeholder cells like `<lane>`, `DIR`, `[--work DIR]`), plus `tb2-grader-probe`'s
   `uv run … -c …` argv, which the new counter's L2 wrapper leg rejects. My seat was
   forbidden from touching those rows; they are flagged for their owners.
4. Design hazard recorded for the L1: declaring `round54-c2` with its full
   `--lane . --source … --work … --jobs 3 --timeout 900` flags would make the row
   self-executing at the R55-C2 after-run (the counter re-runs every ledger row,
   including itself, unboundedly). The stable truthful `--lane .` SETUP form is declared
   instead.

## Dead ends

- The full-flags `round54-c2` measurement ran (426.3 s, exit 1: `EVIDENCE-MISSING
  round35-c1-coverage`, `LAUNDERED round52-c2`, `PREDICATE R54-C2 fail`) but was not
  declarable: red at the base tip, green after this round's repairs, and recursion-prone
  at the after-run. Its output file was superseded by the declared `--lane .` form; the
  result is quoted above and in `measurements.json`'s `_note`.
- First landing-simulation inserted the synthetic registry rows above the table header
  (parser reported `bad_table_lines=1`); re-inserted inside the table — artifact of the
  simulation only, not of the committed data.

## Acceptance

`len(d['rows'])` = **83**. JSON parses; `git diff` shows only this seat's edits.
Scratch dir `/fast/scratch/hyaku/kengaku-r55/E4LedgerTruth/` deleted after the outputs
above were copied (driver, update script, clones and work dirs included).
