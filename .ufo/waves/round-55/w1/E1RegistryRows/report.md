# E1RegistryRows — round 55 wave 1 seat report

Seat: E1RegistryRows (leaf, executor). Target: `SKILL.md` `## Gate/probe registry` table only.
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin (base tip 798f5e9ef30ef39291295565209b65a17343c00e).
Round claims read first: plans/round-55-claims.md (frozen, commit 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb).

## What I did

Appended exactly five rows to the registry table (after the `stage-scan` row, before the
Round-43 addendum prose), in the required order: `round54-c1`, `round54-c2`, `round55-c2`,
`round55-c2-controls`, `round55-c3`. No other SKILL.md byte changed.

Before writing I read each script's argparse and docstring (all five scripts existed in the
tree by write time — `plans/round55_c2_entryargv.py` and `plans/round55_c3_chess_probe.py`
landed from sibling seats mid-wave). Entry cells' FIRST `python3` backtick span is token-equal
to the ledger `entry_argv` that E4LedgerTruth-2 declared it would commit (coordinated over
agent messages; R55-C2's L1 leg shlex-splits that span and requires token equality with
`plans/round54-entrytruth.json`):

1. `round54-c1`: `python3 plans/round54_c1_anchor.py verify --anchor corpus/evidence/round54/anchor --claims plans/round-54-claims.md --source . --work work/anchor-verify-row --controls`
2. `round54-c2`: `python3 plans/round54_c2_entrytruth.py --lane .`
3. `round55-c2`: `python3 plans/round55_c2_entryargv.py` (bare)
4. `round55-c2-controls`: `python3 plans/round55_c2_controls.py` (bare)
5. `round55-c3`: `python3 plans/round55_c3_chess_probe.py` (bare)

Verified post-write by a parser replicating `registry_entry_argv`: all five spans token-match
E4's argvs; E4's five ledger rows (landed, ledger=83) match in return.

## Commands run and exit codes (measured 2026-10-30, all on the working tree)

| command | exit | note |
|---|---|---|
| `python3 plans/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (before my edit) | 1 | MISSING 3 (round54_c1_anchor, round54_c2_entrytruth, round55_c3_chess_probe); ADVERTISED 80 REGISTERED 77 |
| `python3 plans/round54_c1_anchor.py --lane .` | 2 | argparse usage (no `--lane` mode) |
| `python3 plans/round54_c1_anchor.py selftest` (bare host python3) | 1 | ModuleNotFoundError: opentimestamps |
| `uv venv otsenv && VIRTUAL_ENV=… uv pip install opentimestamps==0.5.0 opentimestamps-client==0.8.0` (in my scratch) | 0 | ots import ok |
| `…/otsenv/bin/python plans/round54_c1_anchor.py selftest` | 0 | 8/8 PASS |
| `python3 plans/round54_c2_entrytruth.py --lane .` | 2 | `SETUP --source and --work are required unless --dry` |
| `python3 plans/round54_c2_entrytruth.py --selftest` | 0 | 7/7 PASS |
| `python3 plans/round55_c2_entryargv.py --lane .` | 2 | same SETUP line |
| `python3 plans/round55_c2_entryargv.py --selftest --work <scratch>` | 0 | 4/4 PASS |
| `python3 plans/round55_c2_controls.py --lane .` | 2 | argparse: one of --case --selftest required |
| `python3 plans/round55_c2_controls.py --selftest` | 0 | SELFTEST cases=4 failures=0 |
| 4× `python3 plans/round55_c2_controls.py --case <abbreviated-selftest\|uv-decoy-script> --against <r54\|r55>` | 0 each | r54: `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)`; r55: ARGV-DEFECT + ABBREV/WRAPPER-DEFECT lines, `COUNTER EXIT 1`, `ROUTE kill demonstrated` |
| `python3 plans/round55_c3_chess_probe.py --selftest --work <scratch>` | 0 | SELFTEST cases=2 failures=0 |
| `python3 plans/round55_c3_chess_probe.py --lane .` | 0 | `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass` (battery, no receipt) |
| `python3 plans/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (after my edit) | 0 | **ADVERTISED 82 REGISTERED 82 rows=84; MISSING 0; INCOMPLETE 0; ENTRY-MISSING 0; SELFTEST-UNBACKED 0; DUPLICATE 0; PREDICATE R52-C2 pass** |
| `git diff --stat -- SKILL.md` | 0 | `1 file changed, 5 insertions(+)` — only SKILL.md |
| `python3 plans/round55_c2_entryargv.py --lane . --dry` (after my edit) | 1 | ROWS registry=83 ledger=83 missing=0 extra=0 **argv_defect=17 wrapper_defect=1** abbrev_defect=0 … — none of the 17+1 defects name my five rows |

Acceptance: `MISSING 0` printed (all R52-C2 legs pass right now, exit 0); SKILL.md diff names
one file with five added lines. Met and exceeded.

## Pins written (sha256, first 16 hex of the in-tree files at write time)

- `plans/round54_c1_anchor.py` `e08152a55fefa54a`
- `plans/round54_c2_entrytruth.py` `44c3f41285239645`
- `plans/round55_c2_entryargv.py` `2bf9e66ce3d5bace`
- `plans/round55_c2_controls.py` `c7591bc6d682c542`
- `plans/round55_c3_chess_probe.py` `7bd2863ca745f165`

## Files written

- `SKILL.md` — five registry rows (lines 642–646).
- `.ufo/waves/round-55/w1/E1RegistryRows/report.md` (this file) and
  `.ufo/waves/round-55/w1/E1RegistryRows.md` (same content, the seat's Report path).
- `.ufo/waves/round-55/w1/E1RegistryRows/evidence/` — r52 counter after-run receipt
  (`r52-c2-registry-after.txt`), r55 dry after-run (`r55-c2-entryargv-dry-after.txt`),
  `skill-diff-stat.txt`, `skill-diff-head.txt`, and the ten bare-entry/measurement outputs
  (`e1-*.out/.err`).

No git/jj mutation run (read-only `git status/diff` only). No fleet-root tracked file touched.
Scratch `/fast/scratch/hyaku/kengaku-r55/E1RegistryRows/` (incl. the otsenv venv) removed
after evidence copy.

## Defects found (reported, not fixed — outside my write bounds)

1. **Pre-existing L1 ARGV-DEFECTs under the new r55 counter (17 rows) + 1 WRAPPER-DEFECT
   (`tb2-grader-probe`, argv[0]=`uv`).** Their registry cells' first `python3` spans use
   placeholder/optional-flag syntax (e.g. `--work DIR`, `[--revision REV]`, `<lesson.md>`)
   that cannot token-equal the measured ledger argvs. The frozen R55-C2 after-predicate
   requires `argv_defect=0 wrapper_defect=0` at the measured-after revision; as things stand
   that number is 17/1. None of my five rows contribute. Fixes belong to the owners of those
   cells/rows or to an L1-level amendment — rewriting 17 reviewed cells by hand is itself
   flagged as a documentation-attack surface in the kill-rule note. E13BindingScan/SC3ArgvUniverse/
   R8CounterSoundness seats are on this.
2. **`round54_c1_anchor.py selftest` needs the round-54 `opentimestamps` venv** (bare host
   python3 exits 1 ModuleNotFoundError). My self-test cell documents both measurements;
   E11SelftestReceipts-3 acknowledged and will run it with the venv python from a clean clone.
3. Minor (pre-existing, not mine): the `round53-c2` ledger row's reason text says the registry
   cell "does not name" `--source`/`--work` although the current cell does — stale reason from
   an earlier cell revision. Left untouched (ledger is E4's file, and this row is not in the
   frozen correction set).

## Dead ends / decisions

- Considered writing rows with the full canonical flag sets in the first spans (e.g. `--lane .
  --source <clean clone> --work <scratch>`); rejected after measuring that L1 strict token
  equality plus L4 hermetic re-execution make placeholder spans unmatchable/unrunnable, and
  after E4 confirmed the bare/ledger-declared argvs above (including its recursion warning:
  a self-executing `round54-c2` full-form row would cascade at the after-run).
- `plans/round55_c2_entryargv.py` and `plans/round55_c3_chess_probe.py` were absent at seat
  start; a bounded poll (≤9 min) found both landed (12:38), so all flags were verified
  against real argparse bodies — no "flag per frozen contract" note was needed in the end.
- Installs: none system-wide. Created a scratch-only venv `otsenv` (uv, PyPI) with
  opentimestamps 0.5.0 + opentimestamps-client 0.8.0 under
  /fast/scratch/hyaku/kengaku-r55/E1RegistryRows/ to measure the anchor self-test truthfully;
  deleted with the scratch dir. uv version: host-installed.

## Unrun / not claimed

- I did not run the full `round55_c2_entryargv.py` (non-dry) — it needs a clean clone +
  scratch and re-executes all 83 ledger rows; that is the L1's after-run, not my seat's.
- I did not run `round54_c2_entrytruth.py` full form (recursion risk documented above).
- The R55-C1 leg-2 self-test execution belongs to E11SelftestReceipts-3 (pinged; rows are in
  the tree for it now).
