| mutant | expected | rc | failing legs | predicate | verdict |
|---|---|---|---|---|---|
| r1_lanetip_nonancestor | L3 | 1 | L3 | fail | killed |
| r2_detail_digest | L6 | 1 | L6 | fail | killed |
| r3_case_observed_flip | L5,L6 | 1 | L5,L6 | fail | killed |
| r4_case_dropped | L5,L6 | 1 | L5,L6 | fail | killed |
| r6_subject_sha | L2 | 1 | L2 | fail | killed |
| r7_tool_sha | L6,L9 | 1 | L6,L9 | fail | killed |
| r8_host_bash | L9 | 1 | L9 | fail | killed |
| r10_receipt_absent | L1,L2,L3,L5,L6,L9 | 1 | L1,L2,L3,L5,L6,L9 | fail | killed |
| t1_predicted_flip | L4,L5,L6 | 1 | L4,L5,L6,L9 | fail | killed |
| t2_app_swap | L4,L6 | 1 | L4,L6,L9 | fail | killed |
| t4_case_reorder | L4,L6 | 1 | L4,L6,L9 | fail | killed |
| t5_table_whitespace | L4 | 1 | L4,L6,L9 | fail | killed |
| g1_extra_executed_member | L7 | 1 | L7 | fail | killed |
| g2_removed_executed_member | L7 | 1 | L7 | fail | killed |
| g3_legacy_receipt | L7 | 1 | L7 | fail | killed |
| g4_classes | L7 | 1 | L7 | fail | killed |
| s1_bad_anchor_row | L10 | 1 | L10 | fail | killed |
| s2_valid_anchor_row | pass-control | 0 | - | pass | SURVIVED |
| p1_probe_comment | L6,L8,L9 | 1 | L6,L8,L9 | fail | killed |
| c1_capture_byte | setup-refusal | 2 | - | could-not-evaluate | could-not-evaluate |
| k1_l10_ignore_flagged | pass (self-binding gap) | 0 | - | pass | SURVIVED |
| k2_l7_superset | pass (round-97 defect 2) | 0 | - | pass | SURVIVED |
| d1_k1_s1 | pass (survivor pair) | 0 | - | pass | SURVIVED |
| d2_k2_g1 | pass (survivor pair) | 0 | - | pass | SURVIVED |
| r11_receipt_mismatches_field | SURVIVOR (field unread) | 0 | - | pass | SURVIVED |
| d3_t5_table_stamp_coordinated | L4 only | 1 | L4 | fail | killed |
| d4_p1_probe_stamp_coordinated | L8 only | 1 | L8 | fail | killed |
| restored | pass (pristine) | 0 | - | pass | SURVIVED |
