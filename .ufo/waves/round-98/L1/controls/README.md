# Round 98 prefreeze controls (P2; L1 KengakuR98)

All controls run against the P1 instrument bytes (`350d0e59`) in fixture clones under
`/fast/scratch/hyaku/kengaku-r98/L1/` (never the lane), each battery TWICE (`-run1`, `-run2`) before F
(QUALITY Q80). Runners: `run_c1_controls.sh`, `run_c2_controls.sh` (exact commands inside). Candidate
bytes tested are retained in `candidate/` and are byte-identical to the frozen candidate-bytes table
(`ledger.json` lands as `plans/grader-population-ledger.json`).

## R98-C2 (`c2-*-run{1,2}.txt`, fixture at P1; counter from the lane)

| control | expected | run1 / run2 | failing legs |
|---|---|---|---|
| do-nothing | fail | fail / fail | K3 K4 (`still=39`) |
| positive (PROVENANCE.md only) | pass | pass / pass | — |
| partial (one line short) | fail | fail / fail | K3 K4 (`still=1`) |
| row-edit forgery (tokens blanked in the 39 rows) | fail | fail / fail | K3 K4 K5 K7 |
| wrong-capture forgery (round-52 twins) | fail | fail / fail | K4 (`unbound=10`) |
| gate-edit forgery (provenance present, gate bytes changed) | fail | fail / fail | K1 only |
| capture-edit forgery (one capture changed) | fail | fail / fail | K3 K4 K6 K7 |
| c1only (C1 candidate bytes, no provenance) | fail | fail / fail | K3 K4 |
| both | pass | pass / pass | — |

Runs agree line for line except the informational `GATE defects base= rev=` line, identical too.

## R98-C1 (`c1-*-run{1,2}.txt`, fixture at P1 + a fixture-only freeze table; counter from the fixture root)

| control | expected | run1 / run2 | failing legs |
|---|---|---|---|
| do-nothing (freeze table only) | fail | fail / fail | L1 L2 L3 L5 L6 L7 L9 L10 |
| positive (probe receipt + C1 candidate bytes) | pass | pass / pass | — |
| extra-member forgery (`crack-7z-hash` also flipped) | fail | fail / fail | L7 only (`set_added` two members) |
| forged-receipt (one DETAIL digest altered) | fail | fail / fail | L3 L6 |
| c2only (PROVENANCE.md only) | fail | fail / fail | as do-nothing |
| both | pass | pass / pass | — |

Run1/run2 differ only in fixture commit hashes printed by L3 in `forged-receipt` (each run builds its own
fixture commits); the LEGS/TARGET/PREDICATE/rc lines agree for every control. The positive TARGET line
equals the frozen target string in both runs.

## Pre-freeze source gate

`candidate/sources-validate.txt`: `sources-census.sh validate --file` on a `git archive` mirror of the lane
with the candidate SOURCES.md → rc 0 (only the 30 pre-existing W04 warnings).
`anchor_digest_check.py` on a fixture with the candidate SOURCES.md and the P0 flat captures: `rows=325
defects=86` (BASE 86): none of S326–S333 flagged.
