# Round 94 — pre-freeze controls (P2)

Every receipt here ran the instrument bytes committed at P1 `997a6fe5fbb4a4af9f38e436bccd8f604da1d746`
from a `git clone --shared` detached at P1 (scratch `/fast/scratch/hyaku/kengaku-r94/L1/p2`, removed
after landing), before the claims file (F) existed. BASE = `0cbb927914e07818e1aaee7e72d8b3c90a2d21c2`.

| receipt | what it controls | expected | observed |
|---|---|---|---|
| `c1-base.txt` | do-nothing: R94-C1 counter at BASE | fail, rc 1 | 9/9 legs fail, rc 1 |
| `c1-at-P1.txt` | instruments only, no receipt, no flip | fail, rc 1 | 9/9 legs fail, rc 1 |
| `c1-forgery-ledger-only.txt` | ledger flip without any probe receipt (fixture commit on a P1 clone) | fail, rc 1 | only L7 passes, rc 1 |
| `c1-forgery-member-swap.txt` | flip + swap `circuit-fibsqrt`→`path-tracing` (same classes: aggregates 38 / 29 / 13 / 15 hold) — round-93 W-5 | L7 fail (member set) | L7 fail `set_added=[path-tracing, write-compressor] set_removed=[circuit-fibsqrt]`, rc 1 |
| `c1-sandbox-red.txt` | `--bwrap /nonexistent/bwrap` (round-92 M13) | could-not-evaluate, rc 2 | rc 2 |
| `c2-base.txt` | do-nothing: R94-C2 counter at BASE (gate v2 absent) | fail, rc 1 | 0 of 5, rc 1 |
| `c2-real-at-P1.txt` | positive: real gate v2 at P1 | W1 W2 W3 W5 pass; W4 fails only because the claims file does not exist yet | 4 of 5 (W4 `claims-add-commits=0`), rc 1 |
| `c2-false-r93-gate.txt` | cheapest control: the admitted round-93 gate offered as v2 | fail | fail: treesame-merge, second-block, duplicate-row RED; W3 cases=10; W5 anchors missing |
| `c2-false-x-head-not-rev.txt` | round-93 seat forgery (ExecC2Rerun F1) | its designated fixture RED | `w2-rev-below-head` RED (plus the r93-base fixtures), rc 1 |
| `c2-false-x-diff-rev-minus-1.txt` | round-93 seat forgery (F2) | designated RED | `w2-edit-revert-unrelated` RED, rc 1 |
| `c2-false-x-table-at-rev.txt` | round-93 seat forgery (F3) | designated RED | `w2-lie-repaired` RED, rc 1 |
| `c2-false-m06-cne-exit0-pass.txt` | round-93 surviving mutant m06 | designated RED | `w2-not-ancestor` RED, rc 1 |
| `c2-false-m13-table-read-at-rev.txt` | round-93 surviving mutant m13 | designated RED | `w2-lie-repaired` RED, rc 1 |
| `before-r93-counter-*.txt` | the BEFORE value: the frozen round-93 counter (`plans/round93_c2_counter.py`) at BASE with the same five false gates and the r93 gate | — | `PREDICATE R93-C2 pass`, rc 0 for all six |

The five known false gates are built on the round-93 gate, so they also fail the v2-only fixtures
(TREESAME, second block, duplicate row) and W3 (`cases=10`). Their designated fixtures are what
distinguishes each one; W5 repeats each attack against the v2 gate itself (CLI-path mutants, battery
honest), where no other fixture or leg can be the killer.
