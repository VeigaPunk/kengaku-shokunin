# R33EntryTruth — adversarial truth check of `corpus/knowledge/benchmark-grader-semantics.md`

Scope: committed draft (already carrying the R33 admission-patch header `→ admission patch KengakuR33`;
no `entry-patched.md` exists in the wave tree — globbed, absent) vs captured/pinned bytes under
`.ufo/waves/round-33/assimilation/captures/` plus the round-31 capture set it explicitly defers to.

Captures verified: `sha256sum` on the three SHA256SUMS-listed captures all match
(main.py `3bad26b6…`, retry.py `db11e66e…`, arxiv html `44195c5f…`). `url-map.json` pins both
Toolathlon files at `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`. Line numbers below are the
capture files' own numbered lines (re-derived by grep with match-line output, not estimated).

## Per-claim verdict table

| # | Entry claim | Verdict | Deciding byte + line |
|---|-------------|---------|----------------------|
| 1 | No model/judge scoring path; case-insensitive scan for `prompt\|judge\|model\|openai\|chat\|gpt\|llm\|claude\|anthropic` finds none | **supported** | main.py capture, full-file scan returns zero matches (re-run with explicit upper/mixed-case variants — still zero); only scoring imports are `google.cloud storage/logging`, `google.oauth2`, `google.api_core`, `utils.evaluation.retry` (`main.py:1-12`) |
| 2 | Signature default `tolerance_pct: float = 0.1` at `main.py:58`; "signature default is 0.1%" | **supported** | `main.py:58` `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` — byte-exact quote; percent semantics corroborated by `expected {…}%±{tolerance_pct}%` format at `:86,:93` |
| 3 | Executed tolerance is 0.05, set at call site (`main.py:279-280`) | **supported** | `main.py:279` `# Validate with 0.05% tolerance`; `main.py:280` `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` — both byte-exact; `:280` is the sole call site (only other occurrence is the `:58` def) |
| 4 | One missing or extra scenario fails the task (`:70`,`:72`,`:100`) | **supported** | `main.py:70` `Missing scenarios:`, `:72` `Unexpected scenarios:` append to `validation_errors`; `:99-100` non-empty errors → `raise ValueError(f"Record validation failed:…")`; caught at `:293-295` → `exit(1)` |
| 5 | Side-effect check precedes record comparison; storage-bucket prefix match (`:125-140,225`); `gcloud` CLI is fallback for storage check | **supported** | `main.py:136`/`156` `startswith(bucket_prefix)` inside `check_storage_bucket_exists` (`:125`); gcloud fallback at `:141-160` (`subprocess.run(['gcloud','storage','buckets','list',…])`); call site `:225` `check_storage_bucket_exists("promo-assets-for-b")` inside `validate_task_completion` (`:220`), executed at `:257` before `validate_record_data` at `:280` |
| 6 | Log check returns `True` for a clean bucket AND for some caught exceptions (`:213-218`); not every inability passes | **supported** | `main.py:213-214` clean path → `return True`; `:216-218` `except Exception … return True  # Don't fail evaluation…`; conversely `log_bucket_name.txt` open at `:171` sits outside the try → `FileNotFoundError` propagates to `_check_completion` → `False` |
| 7 | Credential failure falls through to implicit `None` and fails the task-completion check ("fail closed", not fail-open) | **supported** | `main.py:175-214`: entire logging-client body is inside `if project_id_from_creds and credentials:` (`:176`); creds `None,None` (returns at `:118,:123`) → `if` false → try ends → implicit `None`; `:234-235` `if not check_abtesting_logging_bucket_clean(…): raise ValueError(…)` |
| 8 | Retry applies to the task-completion side-effect check only; ≥at most 3 attempts; doesn't retry record comparison or turn implicit-`None` into success | **supported** | `main.py:262` `ok, err = grade_with_retry(_check_completion)` wraps `validate_task_completion` (`:256-257`); `validate_record_data` called bare at `:280`; retry.py `:44-45` `DEFAULT_MAX_ATTEMPTS = 3` / `DEFAULT_POLL_S = 5`; falsy `ok` from `None`-returning check fn → `last_err` path → `(False, err)` (retry.py:83-109) |
| 9 | S104 five-part survey structure quote | **supported** | `arxiv-2412.05579v2-abs.html:124` (blockquote abstract; also meta tags `:30`,`:41`): `…from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` — byte-exact including `LLMs-as-judges` hyphenation; whitespace-token count = 20, matching entry's "20 words" |
| 10 | S093 reward = binary set containment (`success = all_required <= passed_tests`) over log-derived last-write-wins `PASSED` set | **supported** | test.sh capture `:213-214` `all_required = fail_to_pass \| pass_to_pass` / `success = all_required <= passed_tests`; binary reward `:12-23` `echo 1/0 > /logs/verifier/reward.txt`; log-derivation + last-write-wins grounded by round-31 capture `parser.py` (`…/round-31/assimilation/captures/parser.py`): regex at `:68,71` and `:88-90` scans stdout+stderr lines, dict-comprehension dedupe `unique_results = {result.name: result for result in results}.values()` at `:121` — later record overwrites earlier per name. S093 row quotes resolve byte-exact at capture `:33`,`:71`,`:214` |
| 11 | S093 reset order: reset precedes `git apply` of the test patch | **supported** | test.sh `:33-105` reset work (T/U loop `:68-74`, patch-path v5 loop `:86-94`, modified-file v6 loop `:97-104`) all before `:107-108` `Applying test patch…` / `git apply --verbose /tests/test_patch.patch` |
| 12 | S093 fixture asymmetry: reset restores tracked test code but not newly added fixture files | **supported** | `is_test_code` excludes `DATA_DIRS` parents `{'testdata','test_data','fixtures','fixture','mocks','mock','__snapshots__'}` (`:38-41`) → untracked fixture files skip the `U) rm` branch (`:72`); `git diff --name-only HEAD` (`:97`) lists only tracked modifications (v6 restores modified *tracked* fixtures `:99-102`, consistent with the claim's wording); only files the test patch itself creates are removed (`:77-79`,`:84-85`) |

## Asserted-but-uncaptured scan (flag list)

Nothing load-bearing lacks byte coverage. Three residual notes, none an entry misstatement:

- **LOW — capture provenance gap, not entry defect:** `swebench-pro-tests-test.sh` (234 ln) is
  absent from `captures/SHA256SUMS.txt` and `url-map.json`, so its identity against
  `66f92766bba6…` isn't digest-pinned this round. Mitigation: all three S093-row located
  quotes resolve byte-exact at the capture's own `:33`,`:71`,`:214`; round 31's checksummed
  `test.sh`/`parser.py` captures (`…/round-31/assimilation/captures/`) carry the parser half.
- **NIT — word-count convention:** `# Validate with 0.05% tolerance` is 5 whitespace tokens
  (entry: "4 words"); `:280` call line is 3 whitespace tokens (entry: "5 words"). Both
  byte-exact and far under the >25-word refusal bound; counts vary by convention only.
- **NIT — line precision:** `corpus/README.md:276` names the frontier bullet line; the literal
  "and for Toolathlon" clause sits at `:278` inside the same bullet (discharged text now at
  `:279`). Same bullet, correct reference granularity.

## Residual risk / verification gaps

- `parser.py` was not re-captured this round; "last-write-wins" is grounded on round-31's
  captured bytes at the same pinned commit — a restatement claim, so acceptable, but the
  S093 source line's `parser.py` half is not re-verifiable from round-33 artifacts alone.
- The entry's claim `arXiv 2412.05579v2` is a preprint is corroborated only by the abs-page
  html (no journal-ref banner observed in the capture; consistent but not independently proven).
- `verified-at`/access-date `2026-10-25`, `recheck: 180d` → `2027-04-23` recompute correctly.

Tools installed: none (built-in coreutils + repo captures only).

VERDICT: entry-truth-clean
