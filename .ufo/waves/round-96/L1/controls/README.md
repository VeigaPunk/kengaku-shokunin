# Round 96 — pre-freeze controls (P2)

Every control below was executed against the P1/P1b instrument bytes (`plans/round96_c1_replay.py`
P1 `cea469bd`, `plans/round96_standing_battery.py` P1b `e8a80c0e`) before F. Fixture clones were
built by `sim_c.py` (copied here) under `/fast/scratch/hyaku/kengaku-r96/L1/` with
`git clone --shared` + a clone-local fixture identity; nothing was committed to the lane by them.
The candidate R96-C2 repair bytes are `candidate-edits.diff` / `candidate-edits.sha256` (the same
hashes as the claims file's `candidate-bytes` table).

| file | control | target | expected | observed |
|---|---|---|---|---|
| `c1-do-nothing.txt` | R96-C1 do-nothing: the lane at P1b (no receipt, no ledger flip) | real lane `e8a80c0e` | fail rc 1 | `LEGS` all fail, `PREDICATE R96-C1 fail`, rc 1 |
| `c1-positive.txt` | R96-C1 positive: P1b + C1 flip (dry-run receipt, ledger row, SKILL cells) + draft claims file | fixture `6c19ae9a` | pass rc 0 | 9/9 legs, `TARGET executed_rows=40 … cases=17 legs=68 mismatches=0 defects=0`, pass, rc 0 |
| `c1-forged-receipt.txt` | R96-C1 forgery: receipt's C04 observation changed to `P,P,F,0` | fixture `1a630770` | fail rc 1 | L5 + L6 fail, `PREDICATE R96-C1 fail`, rc 1 |
| `c1-wrong-cwd.txt` | R96-C1 cwd refusal (round-95 routed defect 6): run from /tmp | real lane | rc 2 | `could-not-evaluate`, rc 2 |
| `c2-full.txt` | R96-C2 positive: candidate bytes + mteb subject re-pin + C1 flip | fixture `0499fc3c` | pass | `STANDING red=0`, `BITES bitten=12`, `GROWS tolerant=6`, pass |
| `c2-c1-only.txt` | R96-C2 do-nothing at a C1-landed tip | fixture `4c60027b` | fail | `STANDING green=7 red=7` (round 95 joins the red set), fail |
| `c2-delete-l7.txt` | R96-C2 forgery: L7 disabled in rounds 90–95 | fixture `2e7f9004` | fail | `STANDING red=0` but `BITES bitten=0`, fail |
| `c2-repin-abs.txt` | R96-C2 forgery: L7 re-pinned to the absolute total 40 | fixture `d478b48e` | fail | bites 12/12 but `GROWS tolerant=0`, fail |
| `c2-c2-only.txt` | R96-C2 separability: candidate bytes + re-pin, NO C1 flip | fixture `5ef39249` | pass | red 0, bitten 12, tolerant 6, pass |
| `c2-p1a-receipts/` | the same full / c1-only / delete-l7 runs on the P1 battery (before the grow leg) | — | — | superseded by the rows above; kept, not cited for the predicate |

Known receipt defects (disclosed, not repaired): (1) in every `c2-*.txt` the trailing `rc=` stamp
is wrong — it was written as `echo "fixture_rev=$(cat …) rc=$?"`, so `$?` is the command
substitution's status, not the battery's (lesson M2); the battery's `PREDICATE` line is the verdict
(its exit code is defined as 0 iff that line says pass). (2) `c1-forged-receipt.txt`'s fixture
receipt holds two forged C04 lines (a `sed` insert and the python replace both applied), so
`mismatches=2`; the forgery still fails exactly as designed.
