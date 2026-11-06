# Round 100 prefreeze controls of record (P2; L1 KengakuR100)

All controls run against the P1c instrument bytes (`f07c026e`) in fixture clones under
`/fast/scratch/hyaku/kengaku-r100/L1/ctl-<run>/` (never the lane). Each fixture first commits a fixture-only
`plans/round-100-claims.md` with the frozen-instruments block of the P1c bytes and the candidate-bytes block of
`candidate/`, so L3/L4/L8/L11/L12 and K1/K9/K10 resolve; both counters run from the fixture root. The battery
ran TWICE (`-run1`, `-run2`); the LEGS/TARGET/PREDICATE/rc/GATE/VERDICT lines agree run1 = run2 for all 32
receipt pairs (md5 of those lines). Every forgery printed `TREE-DIFF <name> vs <positive>: n paths` with n > 0
(Q85; `console-run{1,2}.txt`) and the runner runs under `set -euo pipefail`. Runner: `run_controls.sh <run> <P1c> <venv>`.
Dry batteries (not of record): `dryrun-p1a/` (P1a bytes; exposed amendment 1) and `dryrun-p1b/` (P1b bytes; REF
peeled to F itself, amendment 1b; verdicts identical to the record).

| counter | control | run1 | run2 | failing legs |
|---|---|---|---|---|
| c1 | both | pass | pass | — |
| c1 | c2only | fail | fail | L1 L2 L3 L5 L6 L7 L9 L10 L12 |
| c1 | counter-edit | fail | fail | L11 L12 |
| c1 | do-nothing | fail | fail | L1 L2 L3 L5 L6 L7 L9 L10 L12 |
| c1 | extra-file | fail | fail | L12 |
| c1 | extra-member | fail | fail | L7 L12 |
| c1 | extra-row | fail | fail | L10 L12 |
| c1 | forged-receipt | fail | fail | L3 L6 |
| c1 | positive | pass | pass | — |
| c1 | receipt-identity | fail | fail | L3 |
| c1 | skill-cell | fail | fail | L12 |
| c1 | typed-words | fail | fail | L12 L13 |
| c2 | both | pass | pass | — |
| c2 | c1only | fail | fail | K4 K5 K10 |
| c2 | c2-extra-file | fail | fail | K10 |
| c2 | c2counter-edit | fail | fail | K1 K10 |
| c2 | capture-edit | fail | fail | K4 K5 K6 K10 |
| c2 | do-nothing | fail | fail | K4 K5 K10 |
| c2 | duplicate-line | fail | fail | K4 K5 K10 |
| c2 | fabricated-id | fail | fail | K4 K10 |
| c2 | fourth-cell | fail | fail | K3 K10 |
| c2 | gate-edit | fail | fail | K1 K10 |
| c2 | live-forged | fail | fail | K9 K10 |
| c2 | outside-rebind | fail | fail | K4 K7 K10 |
| c2 | outside-row-delete | fail | fail | K8 |
| c2 | partial | fail | fail | K4 K5 |
| c2 | positive | pass | pass | — |
| c2 | row-edit | fail | fail | K4 K5 K6 K8 K10 |
| c2 | sha-column | fail | fail | K4 K10 |
| c2 | url-channel | fail | fail | K3 K4 K10 |

Pre-freeze standing-gate check on the `both` fixture (round-99 routed defect 1): `prefreeze-both-run{1,2}.txt`
`VERDICT clean` (no new line-gate live row, no new registry DEFECT line against BASE).

C1 positive TARGET: see `c1-positive-run1.txt`; C2 positive TARGET and `GATE defects base=33 ref=32 rev=23`: `c2-positive-run1.txt`.
