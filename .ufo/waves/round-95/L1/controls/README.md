# Round 95 pre-freeze controls (P2; executed against P1 `16dcfed7`, BASE `4524072d`)

| receipt | what | want | observed |
|---|---|---|---|
| `before-r94-counter-<id>.txt` ×14 (P0) | BEFORE: frozen round-94 counter at BASE, `--tool-file` each known false gate of `plans/round95-false-gates.tsv` | — | 14 × `PREDICATE R94-C2 pass`, rc 0 |
| `c2-census-do-nothing-r94-counter.txt` | do-nothing: the R95-C2 census scoring the frozen round-94 counter | census fail | `FALSEGATES total=14 passing=14 designated_red=0 honest=pass`, rc 1 |
| `c2-census-at-P1.txt` | the census with the P1 round-95 counter (claims not yet frozen) | honest fails W4 only; 14 designated RED | `passing=0 designated_red=14 honest=fail` (W4 `claims-add-commits=0`), rc 1 |
| `c1-base.txt` | do-nothing: P1 C1 counter at BASE | rc 1 | L1..L9 fail, rc 1 |
| `c1-at-P1.txt` | P1 C1 counter at P1 (no receipt, flip or claims) | rc 1 | L1..L9 fail, rc 1 |
| `c1-pos.txt` | positive, receipt side: scratch clone of P1 + DRAFT claims table of the P1 instrument bytes + the probe's own receipt + flip with legacy fields (round-94 W-6: receipt-side legs never ran positively) | rc 0 | all nine legs pass, rc 0 |
| `c1-D4-probe-swap.txt` | probe replaced by a stub printing predicted as observed, receipt regenerated (W-6 m11) | rc 1, L8 | rc 1, L2 L3 L6 L8 L9 fail |
| `c1-D5-foreign-lane-tip.txt` | LANE_TIP an orphan commit (m10) | rc 1, L3 | rc 1, L3 fail |
| `c1-D6-cases-dropped.txt` | C02–C04 removed from the observation block (m03+m04) | rc 1, L5+L6 | rc 1, L5 L6 fail |
| `c1-D7-stamp-forged.txt` | VULNERABLE_BOTTLE_SHA forged outside the observation block | rc 1, L6 | rc 1, L6 fail |
| `c1-D8-legacy-fields-omitted.txt` | flip without receipt/subject/verdict (routed defect 5) | rc 1, L7 | rc 1, L7 fail |
| `c1-ledger-only.txt` | flip without a receipt | rc 1, L1 | rc 1, L1 L2 L3 L5 L6 L9 fail |
| `c1-member-swap.txt` | honest flip + write-compressor unflipped + regex-chess flipped | rc 1, L7 | rc 1, L7 fail |
| `c1-sandbox-red.txt` | `--bwrap /nonexistent/bwrap` on the positive state | rc 2 | rc 2 |

Driver: `c1_controls.py` (this directory; every git call `-C <scratch clone>`, fixture identity, toplevel asserted; scratch removed). Summary: `c1-receipt-side-summary.txt` (9/9 OK).
