# R32SrcS094b — S094 recon: Toolathlon ab-testing evaluation main.py @ 9be8d8f

**Source:** hkust-nlp/Toolathlon, pinned commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, file
`tasks/finalpool/ab-testing/evaluation/main.py` (raw.githubusercontent, fetched 2026-10-25).
**Bytes:** 14,138; **lines:** 297; **sha256:** `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`.
Sibling `utils/evaluation/retry.py` at the same pin also fetched (4,519 bytes, sha256
`db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e`) to resolve the only non-stdlib /
non-google import. No tool installs performed (curl only).

## (a) Scoring-path calls other than `validate_record_data`

Main flow (`__main__`, :237-297), in execution order:

| Line | Verbatim one-line quote |
|---|---|
| 257 | `            validate_task_completion(args.launch_time, _eval_time)` |
| 262 | `    ok, err = grade_with_retry(_check_completion)` |
| 273 | `        actual_records = read_record_csv(agent_record_file)` |
| 274 | `        expected_records = load_expected_records(args.groundtruth_workspace)` |
| 280 | `        validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` |

Inside `validate_task_completion` (:220-235), the task-completion gate:

| Line | Verbatim one-line quote |
|---|---|
| 225 | `    bucket_exists = check_storage_bucket_exists("promo-assets-for-b")` |
| 234 | `    if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):` |

Inside `check_storage_bucket_exists` (:125-166): `get_project_id_and_credentials()` at :131;
`list(storage_client.list_buckets())` at :134; gcloud fallback `subprocess.run(` at :149 with
`['gcloud', 'storage', 'buckets', 'list', '--project', project_id, '--format', 'value(name)'],` at :150.
Inside `check_abtesting_logging_bucket_clean` (:168-218): `get_project_id_and_credentials()` at :175;
`list(client.list_entries(` at :192 (time-window filter built at :186-190, `page_size=500` at :195).
`load_expected_records` itself calls `read_record_csv(expected_file)` at :56.

## (b) Judge prompt / rubric / LLM call search

- Case-insensitive grep of `main.py` for `prompt|judge|model|openai|chat|gpt|llm|claude|anthropic` → **zero matches**.
- Broad grep for `requests|urllib|socket|http|https|api_key|API_KEY|endpoint|token|inference|generation|completion`:
  the only hits are the repo's own identifiers `_check_completion` (:255, :257, :262) and
  `validate_task_completion` (:220, :257) containing the substring "completion" — no network/LLM markers.
- Imports (:1-12): only stdlib `argparse/os/csv/json/subprocess/pathlib/datetime`,
  `google.cloud.storage/logging`, `google.oauth2.service_account`, `google.api_core.exceptions`, and
  `utils.evaluation.retry`. No HTTP/OpenAI/Anthropic SDK, no API-key handling.
- The only `subprocess` invocation is the `gcloud storage buckets list` CLI (:149-152), not an LLM.
- The imported `grade_with_retry` (`utils/evaluation/retry.py` at same pin, fetched) is a pure poll-retry
  loop (`time.sleep`, max 3 attempts, no LLM calls).

**Conclusion: no judge prompt, rubric, or LLM call appears anywhere in the file.**

## (c) State-vs-tolerance character

The grader is fully deterministic and state-based: it gates on binary infrastructure state (GCS bucket
existence by prefix listing; Cloud Logging bucket cleanliness by entry-count within a launch-to-eval time
window) and then compares the agent's `record.csv` conversion rates against ground-truth
`expected_ratio.csv` within a fixed absolute numeric tolerance (0.05% in main), with no LLM/judge path.

VERDICT: deterministic
