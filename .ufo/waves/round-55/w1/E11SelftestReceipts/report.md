# E11SelftestReceipts — R55-C1 leg 2 self-test evidence (round 55, wave 1)

Seat: E11SelftestReceipts · Date: 2026-10-30 · Role: executor (C1 frozen leg 2 evidence)
Measured committed tip: `248a42b8c73b6415963f16b13127a9aa6d4c997c` (round-55 honest-stop commit)
Method: `git clone --shared` of the lane into `/fast/scratch/hyaku/kengaku-r55/E11SelftestReceipts/lane`
(clean, at tip); self-tests run with cwd = clone root. round54-c1 additionally run under a
scratch `opentimestamps` venv per its cell. No lane writes. Scratch removed after copy-out.

## Headline status (read first)

The five round-55 registry rows were **authored but NOT committed** at the measured tip.
E1RegistryRows wrote them into the working tree (SKILL.md:642–646, confirmed by peer IRC)
and confirmed "the L1 commits — I don't". The committed tip `248a42b8` is the round-55
**honest-stop** commit: "the wave was released un-settled. No results were integrated, no
claim was measured after the freeze, and no score moved." Across ~50 min of bounded waits
the L1 integration commit never landed (HEAD stayed `248a42b8`; nothing staged).

Consequence for leg 2: I executed each row's named self-test from a clean shared clone at
the tip. Three instruments are committed and ran authoritatively; two instruments
(`round55_c2_entryargv.py`, `round55_c3_chess_probe.py`) are uncommitted residue, so their
clean-clone self-test is not runnable at the tip — I recorded clearly-labeled work-tree
diagnostics instead. **No verdict-map cell is false**: the single apparent mismatch
(round54-c1 bare-host exit 1) is explicitly documented inside the cell as expected.

## Summary table

| row | cell self-test (as authored) | clean-clone run at tip | observed | vs cell | leg-2 verdict |
|---|---|---|---|---|---|
| round54-c1 | `…anchor.py selftest` (venv: 8/8 PASS ex0; bare host: ex1 ModuleNotFoundError) | yes (venv + bare-host control) | venv 8/8 PASS ex0; bare host ex1 | MATCH both branches | MATCH |
| round54-c2 | `…entrytruth.py --selftest` (7/7 PASS ex0) | yes | 7/7 PASS ex0 | MATCH | MATCH |
| round55-c2 | `…entryargv.py --selftest [--work]` (4/4 PASS ex0) | BLOCKED (script uncommitted) | work-tree 4/4 PASS ex0 | would MATCH | PENDING commit |
| round55-c2-controls | `…controls.py --selftest` (cases=4 failures=0 ex0) | yes | cases=4 failures=0 ex0 | MATCH | MATCH |
| round55-c3 | `…chess_probe.py --selftest [--work]` (cases=2 failures=0 ex0) | BLOCKED (script uncommitted) | work-tree cases=2 failures=0 ex0 | would MATCH | PENDING commit |

## Findings

1. **No false verdict-map cell found.** All five authored self-test cells name real, measured
   flags; every self-test I could run from a clean clone (or, for the two uncommitted
   instruments, from the work tree) produced exactly the outcome the cell claims. Leg 2's
   truth condition is met for the behavior; it is only **incomplete** because two rows are
   not yet committed (premise), not because any cell lies.

2. **round54-c1 self-test has a documented interpreter dependency (NOT a defect).** The cell
   states the self-test gives `8/8 PASS`, exit 0, **under the round-54 opentimestamps venv**,
   and exits 1 (`ModuleNotFoundError`) on bare host python3. I reproduced both: venv → 8/8
   PASS exit 0; bare host → exit 1. The cell is truthful on both branches, so this is not a
   leg-2 kill. (An earlier bare-host-only reading of mine that flagged this as a defect was
   **withdrawn** after reading the full committed cell text and E1's confirmation.)

3. **round55-c2 and round55-c3 self-tests are not clean-clone-runnable at the tip.** Their
   instruments are uncommitted working-tree residue; a clean shared clone at `248a42b8` lacks
   the files (an attempt would exit 2 "can't open file"). Work-tree diagnostics match the
   cells (4/4 PASS exit 0; cases=2 failures=0 exit 0). Full leg-2 closure for these two is
   gated on the L1 integration commit.

## Commands (cwd = clean clone unless noted) + exits

| command | exit |
|---|---|
| `git clone --shared <lane> …/lane` | 0 |
| `<otsenv>/bin/python plans/round54_c1_anchor.py selftest` (clone, venv) | 0 (8/8 PASS) |
| `python3 plans/round54_c1_anchor.py selftest` (clone, bare host) | 1 (ModuleNotFoundError — matches cell) |
| `python3 plans/round54_c2_entrytruth.py --selftest` (clone) | 0 (7/7 PASS) |
| `python3 plans/round55_c2_controls.py --selftest` (clone) | 0 (cases=4 failures=0) |
| `python3 plans/round55_c2_entryargv.py --selftest --work <s>` (clone) | n/a — file absent (would be 2) |
| `python3 plans/round55_c3_chess_probe.py --selftest --work <s>` (clone) | n/a — file absent (would be 2) |
| `python3 plans/round55_c2_entryargv.py --selftest --work <s>` (WORK TREE, diagnostic) | 0 (4/4 PASS) |
| `python3 plans/round55_c3_chess_probe.py --selftest --work <s>` (WORK TREE, diagnostic) | 0 (cases=2 failures=0) |
| `uv venv <scratch>/otsenv` + `uv pip install opentimestamps==0.5.0 opentimestamps-client==0.8.0` | 0 |

## Per-row receipts
`round54-c1.txt`, `round54-c2.txt`, `round55-c2.txt`, `round55-c2-controls.txt`, `round55-c3.txt`
(each quotes the authored cell text, the executed command, observed output+exit, and the comparison).

## Defects found
None against the authored cells. The only process defect is integration: the five rows and
two instruments were left uncommitted at the honest-stop tip.

## Dead ends
- Multiple bounded waits (initial 25 min + several 10–14 min windows) for the five rows to be
  committed all timed out; the L1 integration commit never landed in this seat's window.
- Could not produce clean-clone leg-2 runs for round55-c2 / round55-c3 (instruments
  uncommitted); substituted clearly-labeled work-tree diagnostics.

## Install/upgrade record
`uv venv` + `uv pip install opentimestamps==0.5.0 opentimestamps-client==0.8.0` into a scratch
venv (`/fast/scratch/.../otsenv`) — required by the round54-c1 self-test cell; scratch-only, no
PATH/global change. No other installs.

## Blockers (for L1)
- Leg 2 is **partially evidenced** at `248a42b8`: 3/5 clean-clone self-test receipts MATCH;
  2/5 (round55-c2, round55-c3) are gated on the L1 committing the rows + instruments. To
  close leg 2, land the integration commit, then re-run
  `python3 plans/round55_c2_entryargv.py --selftest` and
  `python3 plans/round55_c3_chess_probe.py --selftest --work <scratch>` from a fresh clean clone.
