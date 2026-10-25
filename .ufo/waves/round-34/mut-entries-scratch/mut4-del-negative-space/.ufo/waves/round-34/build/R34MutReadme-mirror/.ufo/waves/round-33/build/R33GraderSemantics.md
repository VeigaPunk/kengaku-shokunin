# R33GraderSemantics — independent reading of Toolathlon's ab-testing grader (S103 ground truth)

Round 33 (hyaku run 7), 2026-10-25. Lane: kengaku-shokunin.
Role: revenger / independent grader read — ground truth the committed entry `corpus/knowledge/benchmark-grader-semantics.md` must agree with. No production edits; read-only lane access; scratch under /tmp/r33-R33GraderSemantics/.

## Provenance (all byte-verified at the pin)

- Capture `toolathlon-ab-testing-evaluation-main.py` (lane wave capture) is **byte-identical** to the pin:
  `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`
  — sha256 `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` on both, `diff -u` IDENTICAL, 297 lines. Capture line numbers = pin line numbers.
- `utils/evaluation/retry.py` fetched at the same pin (repo root; confirmed by contents API — it is not under `tasks/`):
  sha256 `db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e`, 109 lines.
- Token scan over the full 297-line main.py, case-insensitive, `prompt|judge|model|openai|chat|gpt|llm|claude|anthropic`: **zero matches**.
- Access date for every opened source: 2026-10-25.

## Function table (main.py @ 9be8d8fe)

| Function | Lines | Role | Key facts |
|---|---|---|---|
| `read_record_csv(csv_path)` | 14-51 | Parse a CSV into `{scenario: {'A': float, 'B': float}}` | Requires headers `scenario`, `A_conversion %`, `B_conversion %` (25-28); rejects missing file (16-17), headerless file (22-23), empty scenario or rate cells (35-40), non-numeric rates (42-47); strips an optional `%` sign (44-45). Used for **both** sides. |
| `load_expected_records(groundtruth_workspace)` | 53-56 | Load `groundtruth_workspace/expected_ratio.csv` via `read_record_csv` | Same parser as the actual side — structural validation applies to expected data too. |
| `validate_record_data(actual, expected, tolerance_pct=0.1)` | 58-102 | Core comparison vs `expected_ratio.csv` | See "Comparisons" below. Signature default 0.1; executed call overrides to 0.05 (280). |
| `get_project_id_and_credentials(credentials_file="configs/gcp-service_account.keys.json")` | 104-123 | Resolve GCP creds | Keys file relative to CWD (108-110). Missing file → warning, `(None, None)` (118-120). Any other failure → warning, `(None, None)` (121-123). |
| `check_storage_bucket_exists(bucket_prefix, project_id="mcp-bench0606")` | 125-166 | Storage-bucket existence | See "Storage bucket existence". |
| `check_abtesting_logging_bucket_clean(task_launch_time=None, task_eval_time=None)` | 168-218 | Log-bucket cleanliness | See "Early-return paths". |
| `validate_task_completion(task_launch_time, task_eval_time)` | 220-235 | Side-effect gate | See "Gate". Returns `None` on success; raises `ValueError` on failure. |
| `__main__` block | 237-297 | Orchestration | `--agent_workspace`, `--groundtruth_workspace`, `--res_log_file` required; `--launch_time` optional (242). Gate first (262-265), record comparison second (268-295). Exit 1 on either failure; success banner at 297 exits 0 implicitly. |

## Comparisons against `expected_ratio.csv`

1. **Structural (both sides parsed by the same `read_record_csv`)**: required headers, non-empty cells, numeric rates. A malformed expected file fails the run just like a malformed actual file.
2. **Scenario-set symmetric difference**: `missing_scenarios = expected − actual`, `extra_scenarios = actual − expected` (63-67). Both are errors — "Missing scenarios:" (70) and "Unexpected scenarios:" (72) — appended to `validation_errors`; any error → `raise ValueError("Record validation failed:\n…")` (98-100) → caught at 293 → `exit(1)`. Extra and missing scenario names are symmetric failures.
3. **Per-scenario, per-arm numeric comparison** (76-96): for every scenario in the intersection, A and B are checked independently: `diff = abs(actual − expected)`; error iff `diff > tolerance_pct` (84, 91).
   - **Unit**: percentage points — values are percentages after stripping `%`; error strings print `±{tolerance_pct}%`.
   - **Tolerance**: executed value is `0.05` at the call site (280); the `0.1` signature default (58) is **never executed** for this task. Boundary-inclusive: a diff of exactly 0.05 passes.
   - **Fails-closed on validation**: any error at any scenario/arm fails the whole run (one scenario fails all).
4. Post-validation, an `"overall (total_store_views/total_clicks)"` row, if present, only prints a winner; if absent, a warning (284-291). Informational only — never a pass/fail input.

## Early-return paths in `check_abtesting_logging_bucket_clean` (168-218)

- **Pre-try, 171-172**: `open(…/groundtruth_workspace/log_bucket_name.txt)` is **outside** the `try`. Missing file → `FileNotFoundError` propagates uncaught → caught by `_check_completion` → retried → `exit(1)`. **FAIL-CLOSED.**
- **211**: `return False` — ≥1 non-diagnostic entry in the window → gate raises (234-235). **FAIL-CLOSED.**
- **214**: `return True` — zero non-diagnostic entries → genuine pass (not fail-open).
- **218**: `return True` — blanket `except Exception` around the Cloud Logging path after credentials loaded ("Don't fail evaluation if we can't check logs"). **FAIL-OPEN — the function's only fail-open surface.** Triggers observable in code: `logging.Client(...)`/`list_entries` API errors (permission, unreachable), **and a malformed `--launch_time` string** (the `strptime` calls at 186/189 are inside the try; `task_eval_time` always comes from `_eval_time` at 253 with the matching format).
- **Implicit `return None`**: when `get_project_id_and_credentials` yields no usable pair (missing/unparseable keys file, or `project_id` key absent — `if project_id_from_creds and credentials` at 176 is False), the try body is skipped, no exception fires, and the function falls off the end → `None` → falsy → gate raises (234-235). **FAIL-CLOSED.**
- Window semantics: `log_filter` names a **Cloud Logging log**, not a GCS bucket — `projects/{project}/logs/{log_bucket_name}` (178). Diagnostic entries are excluded twice: in the server-side filter string (178) and manually by payload key (199-205). `list_entries` is exhausted to the end (page_size=500 is not a cap; 192-196). With `task_launch_time=None`, no lower bound is applied → **all** entries ever in that log count, so even a legitimate preprocessing-test entry would fail the check (the launch-time window is what reconciles the docstring's "contains only the preprocessing test log entry" with the code's zero-entries requirement — [INFERENCE] on intent; the zero-entries-in-window rule is code fact). Timestamp conversion uses `astimezone(default_timezone)` but hardcodes `+00:00` in the `strftime` format (186, 189) — on a non-UTC host the window labels are mislabeled as UTC (code fact).

## `validate_task_completion` gate (220-235)

1. Storage-bucket existence first: `check_storage_bucket_exists("promo-assets-for-b")` (225); falsy → `raise ValueError("…promo-assets-for-b' was not created")` (230).
2. Log-bucket cleanliness second: `check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time)` (234); falsy → `raise ValueError(…)` (235).
3. Both checks run inside `grade_with_retry(_check_completion)` (262), i.e. **at most 3 calls** (1 initial + up to 2 retries, 5 s apart) via `_check_completion` (255-260), which converts any exception to `(False, str(e))`. On exhaustion → `(False, last_err)` → `exit(1)` (263-265).
4. The gate runs **before** the record comparison; the record comparison is **outside** the retry wrapper and runs exactly once.

## Storage bucket existence ("anything about storage bucket existence")

- Hard-coded prefix `"promo-assets-for-b"` at the call site (225); default `project_id="mcp-bench0606"` in the signature (125).
- Match is `bucket.name.startswith(bucket_prefix)` over a **full bucket list of one project** (134-138) — a bucket named e.g. `promo-assets-for-b2` passes.
- Two credential paths, two possible projects: (a) service-account path uses the keys-file project (131-140); if listing succeeds with no match → `return False` **immediately, without trying gcloud** (139-140); any exception → falls through to (b). (b) gcloud fallback uses the signature's `project_id` (default `mcp-bench0606`), `gcloud storage buckets list --project <id> --format value(name)`, `subprocess.run(..., timeout=30)` (146-152); rc≠0 → False (161-163); `TimeoutExpired`/`FileNotFoundError` (gcloud absent) → False (164-166). (Note: `CalledProcessError` is listed at 164 but `run()` without `check=True` won't raise it — dead clause.)
- **No fail-open path in this function**: every False leads to the gate raise at 230; the only path to `True` is an actual prefix match from either branch. The two branches can inspect different projects (keys-file project vs `mcp-bench0606`), so a bucket in the wrong project is invisible → fail-closed.

## Retry layer (pinned `utils/evaluation/retry.py`)

- `DEFAULT_MAX_ATTEMPTS = 3` (line 44) and `DEFAULT_POLL_S = 5` (line 45) — exactly as the draft cites.
- `grade_with_retry(check_fn, max_attempts=3, poll_s=5)` (48-109): returns `(True, None)` on the first `ok=True`; retries after 5 s sleeps (max 2 sleeps ≈10 s); **absorbs exceptions raised by `check_fn`** into `(False, "check raised …")` (84-90); returns `(False, last_err)` on exhaustion (109). In this grader, `_check_completion` already catches everything, so the outer except is a no-op safety net.
- It wraps only the side-effect gate — the record comparison is unretried.

## Disagreements with the committed draft `corpus/knowledge/benchmark-grader-semantics.md`

**None — every draft claim about the grader checks out against the pinned bytes:**

- Draft:37 quote (`main.py:58`) ✔ byte-identical; word count 11 ✔ (≤25-word rule).
- Draft:41-42 quotes (`main.py:279` comment, `main.py:280` call) ✔ byte-identical; 0.05 at the call site confirmed (sole call at 280).
- Draft:46-47 (`main.py:70` "Missing scenarios:", `:72` "Unexpected scenarios:", `:100` "raise ValueError(f\"Record validation failed:") ✔ present verbatim.
- Draft:50 `main.py:125-140,225` bucket-prefix locator ✔ (function 125-166, service-account branch 130-140, call at 225).
- Draft:52 `main.py:213-218` "returns True both for a clean bucket and for some caught exceptions" ✔ (214, 218).
- Draft:53-55 credential failure → implicit `None` → gate raises (fail-closed, not fail-open) ✔ (176, 234-235).
- Draft:57-60 retry constants and scope (`retry.py:44-45` = 3/5; wrapper applies to the side-effect check only; never turns implicit-None into success) ✔ verified against pinned `retry.py`.
- Draft:31-33 "no model or judge call" ✔ — scan found **zero** occurrences of any token, stronger than "no such scoring path".
- The two repaired misstatements (executed tolerance 0.05 vs signature default 0.1; credential-failure fail-closed vs "fail open") read correctly in the draft.

**Completeness notes (facts the draft omits; none contradict it; suggested as additions):**
- Hard-coded prefix `promo-assets-for-b` and default project `mcp-bench0606`; `startswith` semantics (a `promo-assets-for-b2` bucket would pass); one-project listing.
- The single fail-open surface is the blanket catch → True (218), with malformed `--launch_time` as a concrete trigger; the missing-`log_bucket_name.txt` pre-try open fails closed; credential absence fails closed via implicit None (not via the catch).
- Log check counts **zero** non-diagnostic entries in the window (not "only the preprocessing test log"); with `--launch_time` omitted, all entries ever are counted. Timestamp labels hardcode `+00:00` regardless of local zone.
- Per-arm split and boundary-inclusive tolerance (diff == 0.05 passes).
- `' '.join(args.launch_time)` (247) scatters the string's characters; the mangled value is only printed — the raw `args.launch_time` is what is parsed (257). Cosmetic only.
- Dead import `from google.api_core import exceptions` (8); `CalledProcessError` in the gcloud except tuple (164) is unreachable from `run()` without `check=True`.
- `validate_task_completion` returns `None` on success (success is absence of exception); exit codes 1/1/0.

## VERDICT

**grader-read.** Independent ground truth established: capture ≡ pin (sha256 `3bad26b6…`, 297 lines); `retry.py` fetched at the same pin (sha256 `db11e66e…`); every quoted span and every semantic claim in the committed draft verified byte-for-byte; zero disagreements; fail-open surface enumerated exactly one (the catch → True at 218), everything else fail-closed or genuine pass; retry ≤3 attempts/5 s on the gate only.
