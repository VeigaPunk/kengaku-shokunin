| # | mutant | edit (one commit on T) | expected detector | failing legs | rc | verdict |
|---|---|---|---|---|---|---|
| 1 | `M01` | receipt CASE C01 observed flipped P->F | L5/L6 | L5, L6 | 1 | killed |
| 2 | `M01b` | receipt drops case C13 (CASE+DETAIL) | L5/L6 | L5, L6 | 1 | killed |
| 3 | `M02` | receipt CASE C12 predicted+observed flipped to pass | L5/L6 | L5, L6 | 1 | killed |
| 4 | `M03` | receipt DETAIL C03 final digest edited | L6 | L6 | 1 | killed |
| 5 | `M04a` | receipt LANE_TIP -> descendant 23d58036 | L3 | L3 | 1 | killed |
| 6 | `M04b` | receipt LANE_TIP -> ancestor BASE 2233a661 | L3 | — | 0 | **SURVIVED** |
| 7 | `M05` | case table C11 predicted flipped | L4/L5 | L4, L5, L6, L9 | 1 | killed |
| 8 | `M06` | ledger member classes += numeric-band | L7 | L7 | 1 | killed |
| 9 | `M07` | ledger member round 99->98 | L7 | L7 | 1 | killed |
| 10 | `M08` | ledger member receipt path edited | L7 | L7 | 1 | killed |
| 11 | `M09` | ledger member subject tb2-header->tb2-body | L7 | L7 | 1 | killed |
| 12 | `M10` | second executed member build-pmars -> located | L7 | L7 | 1 | killed |
| 13 | `M11` | other executed member loses file-artifact class | L7/cells | — | 0 | **SURVIVED** |
| 14 | `M12` | SOURCES S342 added, unbound digest | L10 | L10 | 1 | killed |
| 15 | `M13` | SOURCES S342 added, correctly bound | L10/new_rows | — | 0 | **SURVIVED** |
| 16 | `M14` | SOURCES S341 removed | L10/new_rows | — | 0 | **SURVIVED** |
| 17 | `M15` | capture test_outputs.py byte appended | L2 | — | 2 | killed (rc 2) |
| 18 | `M16` | fixture final_bn_sample.csv byte appended | L2 | — | 2 | killed (rc 2) |
| 19 | `M17` | probe comment inserted | L6/L8/L9 | L6, L8, L9 | 1 | killed |
| 20 | `M18` | counter comment inserted | L11 | L11 | 1 | killed |
| 21 | `M19` | builder C03 draws U instead of D | L6/L8 | L6, L8, L9 | 1 | killed |
| 22 | `M20` | builder C03 seed 3->5 | L6(DETAIL)/L8 | L6, L8, L9 | 1 | killed |
| 23 | `M21` | builder C11 shift 0.045->0.060 | L6/L8 | L6, L8, L9 | 1 | killed |
| 24 | `M22` | builder C12 shift 0.050->0.040 | L6/L8 | L6, L8, L9 | 1 | killed |
| 25 | `M23` | builder C13 quantile grid -> seeded random | L6(DETAIL)/L8 | L6, L8, L9 | 1 | killed |
| 26 | `M24` | builder comment only | L6/L8 | L6, L8, L9 | 1 | killed |
| 27 | `M25` | probe mismatch check disabled (ok=True) | L6/L8 | L6, L8, L9 | 1 | killed |
| 28 | `M26` | receipt LEG_ORDER first two legs swapped | none | — | 0 | **SURVIVED** |
| 29 | `M27` | receipt HOST_BASH edited | L9 | L9 | 1 | killed |
| 30 | `M28` | receipt SUBJECT_SHA edited | L2 | L2 | 1 | killed |
| 31 | `M29` | receipt DATASET_SHA edited | L2 | L2 | 1 | killed |
| 32 | `M30` | ledger member status executed->located | L7 | L7 | 1 | killed |
| 33 | `M31` | extra file plans/round99_extra.txt added | none | — | 0 | **SURVIVED** |
| 34 | `M32` | SKILL file-artifact cell 34->35 | none | — | 0 | **SURVIVED** |
| 35 | `M33` | claims candidate-bytes SOURCES sha edited | none | — | 0 | **SURVIVED** |
| 36 | `M34` | receipt mismatches 0->1 | none | — | 0 | **SURVIVED** |
| 37 | `M35` | receipt GRADER_SIDE stamp 8.4.1->8.4.0 | L6 | L6 | 1 | killed |
| 38 | `M37` | weakened counter L10 + unbound SOURCES row (pair) | L11 | L10, L11 | 1 | killed |
| 39 | `M38` | frozen gate anchor_digest_check.py edited at rev | none | — | 0 | **SURVIVED** |
| 40 | `M39` | receipt file deleted | L1 | L1, L2, L3, L5, L6, L9 | 1 | killed |
