# Round 34 gate baseline

Axes: operability; baseline agreement with round-33 receipts. Commands executed from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. All ten requested commands exited 0.

| Command | Final output line | Exit |
|---|---|---:|
| `python3 grader.py` | `VERDICT: PASS — stored evidence fully re-derives offline` | 0 |
| `python3 grader.py --selftest` | `[selftest] ALL PASS` | 0 |
| `python3 plans/state_check.py --summary` | `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5` | 0 |
| `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=17 failed=0` | 0 |
| `python3 plans/registry_check.py --selftest` | `SELFTEST clean cases=15 valid_literal_fence,queued_and_missing,missing_used_by,duplicate,source_missing,uncited_source_missing,unsafe_used_by,bad_enum,extra_queued_source,outside_duplicate_excluded,outside_malformed_excluded,new_file_excluded,missing_frozen_file,cli_population_tampered,cli_population_missing` | 0 |
| `python3 plans/config_projection.py --selftest` | `SELFTEST clean cases=31 six_tokens_and_non_url_field,units_not_pooled,codepoint_offsets_and_key_token,escaped_token_not_replaced,quote_backslash_decode_failure_and_escape_semantics,profile_map_errors,hand_fixtures_authenticated,independent_nine_domain_error_cases,hand_cascade_order_R29_ORDER_CASCADE_01,hand_url_only_R29-URL-ONLY-UNREAD-METADATA-01,hand_index_r29_index_shuffled_ids_1_0,verbatim_slash_and_path_category,all_url_path_categories,duplicate_keys_list_tasks_key_order,source_order_swap,source_literal_rhs,source_extra_step,source_id_filename,source_data_mutated,source_write_dropped,source_text_truncated,exit_mapping,real_audit_finding_exit_one,cli_optimized_refused,cli_snapshot_tampered,cli_input_missing,cli_coherent_rebinding,post_read_replacement…` | 0 |
| `python3 plans/benchmark_spec_audit.py --selftest` | `SELFTEST clean cases=67 hand_expected_scorer_contract,scorer_product_mutation,hand_exact,unknown_evaluator,unknown_string_operator,na_requires_reason,na_reason_present,duplicate_and_missing_ids,hand_url,unknown_url_rule,empty_url_alternative,hand_html,hand_javascript_locator,hand_helper_locator,malformed_helper_url,unknown_locator,invalid_locator_keeps_target_count,typed_flag,non_list_population,empty_population,non_object_task_retained,boolean_id,negative_id,null_sites,empty_sites,blank_intent,numeric_intent,null_eval,duplicate_eval_type,scalar_eval_types,empty_eval_types,mixed_eval_types_preserved,null_refs,empty_refs_native_vacuity,exact_nonstring,include_not_list,include_nonstr_element, fuzzy_scalar,fuz…` | 0 |
| `python3 plans/catalog_probe.py --verify --lane .` | `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok` followed by `HF missing fields: author, sha, lastModified, gated` | 0 |
| `python3 plans/round33_defects.py --lane .` | `checks=6 defects=0` | 0 |
| `python3 plans/round33_c1_verify.py --lane .` | `checks=8 defects=0` | 0 |

**Comparison:** The round-33 receipts available in `.ufo/waves/round-33/build/receipts/selftests.txt` cover a different eight-command selftest battery, not this ten-command set; no direct command-for-command mismatch can be established. The two round-33 counters requested here are green (`checks=6 defects=0`, `checks=8 defects=0`). State summary reports 318 matches, zero mismatches, six superseded, and five offline-unverifiable assertions; these include superseded/out-of-population findings as printed. No fixes made. The truncated final lines above are exactly what the tool returned; full untruncated output was not captured for those two long selftest listings.

VERDICT: gates-baseline green (10/10)
