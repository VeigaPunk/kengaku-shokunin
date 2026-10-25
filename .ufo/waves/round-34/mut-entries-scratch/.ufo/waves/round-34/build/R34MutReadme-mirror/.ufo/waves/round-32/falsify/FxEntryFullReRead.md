# FxEntryFullReRead — full re-read of C1's drafted entry against fresh fetches

Seat: L1Kengaku32.FxEntryFullReRead (leaf, 2026-10-25).
Scope: `corpus/knowledge/benchmark-grader-semantics.md` (uncommitted draft) + draft registry rows S094/S097 (and S093's row anchors as bonus) vs my own re-fetches of the three pinned sources. No production edits; scratch under `/tmp/r32f-FxEntryFullReRead/` (75 KB, under 60 MB). No tool installs were needed (curl + sha256sum present).

Method: fetched every pinned URL myself with `curl -fsSL` (raw.githubusercontent.com full-commit pins; arXiv abs page), computed my own sha256 per fetch, then checked every quoted span byte-for-byte at the stated `file:line` against my fetch. A span is `ok` when the exact bytes occur at the stated line, `moved` when they occur elsewhere in the same file, `absent` when they occur nowhere.

## 1. Fetch manifest (my own fetches, 2026-10-25)

| source | fetch URL (pin) | my sha256 | bytes | status | capture manifest comparison |
|---|---|---|---|---|---|
| S094 toolathlon main.py | `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` | 14138 | 200 OK | **identical** to `.ufo/waves/round-32/assimilation/captures/SHA256SUMS.txt` line 3 |
| S094 toolathlon retry.py | `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/utils/evaluation/retry.py` | `db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e` | 4519 | 200 OK | no capture exists (gap, see §4.3) |
| S093 SWE-bench_Pro-os test.sh | `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh` | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` | 7864 | 200 OK | no capture exists (gap) |
| S093 SWE-bench_Pro-os parser.py | same pin, `…/tests/parser.py` | `303ceda2c97816c27383b767baa9e2f28f8e9b0cebed4dd5d6159c6760770b66` | 4229 | 200 OK | no capture exists (gap) |
| S097 arXiv abs | `https://arxiv.org/abs/2412.05579` | `851b03db6bf5ae74ac7abe0512a0d12be97c8d7b6f99916e7e09356ae67b043d` | 43647 | 200 OK | **identical** to SHA256SUMS.txt line 4 |

Both pins and the arXiv URL resolved; the pinned revisions exist and serve the expected objects. My main.py and arXiv sha256s match the lane captures exactly → the lane's two captures are the same bytes I fetched; retry.py / test.sh / parser.py have no lane capture (missing from `SHA256SUMS.txt`).

## 2. Entry span table (draft `benchmark-grader-semantics.md`)

Every quoted span in the entry, byte-for-byte against my fetch:

| # | entry text (quote) | entry's loc | my loc | result |
|---|---|---|---|---|
| E1 | `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` | main.py:58 | main.py:58 (whole line) | **ok** |
| E2 | `# Validate with 0.05% tolerance` | main.py:279 | main.py:279 (inside line) | **ok** |
| E3 | `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` | main.py:280 | main.py:280 (inside line) | **ok** |
| E4 | `Missing scenarios:` | main.py:70 | main.py:70 | **ok** |
| E5 | `Unexpected scenarios:` | main.py:72 | main.py:72 | **ok** |
| E6 | `raise ValueError(f"Record validation failed:` | main.py:100 | main.py:100 | **ok** |
| E7 | `return True  # Don't fail evaluation if we can't check logs` | main.py:217-218 | main.py:**218** (line 217 is the preceding `print(f"Warning: Could not check…")` inside the same `except`; literal does not span 217-218) | **ok** (range nit, §4.1) |
| E8 | `DEFAULT_MAX_ATTEMPTS = 3` | `utils/evaluation/retry.py:44-45` | retry.py:44 | **ok** |
| E9 | `DEFAULT_POLL_S = 5` | retry.py:44-45 | retry.py:45 | **ok** |
| E10 | `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` | arXiv 2412.05579v2 Abstract | present verbatim in raw HTML (`arxiv-2412.05579.html`) and in the extracted `<blockquote class="abstract">` text | **ok** |

## 3. Draft row anchor citations (SOURCES.md rows S094/S097; S093 as bonus)

| # | row | anchor citation | my loc | result |
|---|---|---|---|---|
| R1 | S094 | `main.py:279-280 "# Validate with 0.05% tolerance" then "validate_record_data(actual_records, expected_records, tolerance_pct=0.05)"` | 279 / 280 | **ok** |
| R2 | S094 | `:58 default "tolerance_pct: float = 0.1"` | 58 | **ok** |
| R3 | S094 | `:217-218 "return True  # Don't fail evaluation if we can't check logs" (8 words)` | 218 (not spanning 217) | **ok** (range nit) |
| R4 | S094 | `utils/evaluation/retry.py:44-45 "DEFAULT_MAX_ATTEMPTS = 3" / "DEFAULT_POLL_S = 5"` | 44 / 45 | **ok** |
| R5 | S097 | `Abstract: "This paper presents … Limitations." (20 words)` | verbatim in abstract | **ok** (token count = 20, verified) |
| R6 | S097 | arXiv 2412.05579v2, submitted 7 Dec 2024, last revised 10 Dec 2024 | page meta: `citation_date content="2024/12/07"`, `citation_online_date content="2024/12/10"`, `[v2]` marker present | **ok** |
| R7 | S097 | page title matches survey title, no journal reference | `<title>[2412.05579] LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods</title>`, `citation_title` matches; no `citation_journal_title`, no `journal_ref`, no `Comments:` field | **ok** |
| R8 | S093 | `test.sh:33 "Resetting test-space to base state (full test-code surface)..." (8 words)` | test.sh:33 `echo "Resetting test-space to base state (full test-code surface)..."` | **ok** |
| R9 | S093 | `:71 `T) git checkout HEAD -- "$path"`` | test.sh:71 (`T) git checkout HEAD -- "$path" 2>/dev/null || true`) | **ok** |
| R10 | S093 | `:214 "success = all_required <= passed_tests" (5 words)` | test.sh:214 | **ok** |

## 4. Findings

### 4.1 Span-location nits (do not fail any span)
- **E7/R3**: the `return True  # Don't fail evaluation if we can't check logs` literal is entirely on main.py line 218; line 217 is the `print(f"Warning: Could not check abtesting_logging bucket: {e}")` inside the same `except`. The cited range `217-218` covers the literal but the literal does not span two lines. Cosmetically over-wide range.
- **Word-count labels are inconsistent across quotes** (entry/rows): E1 labelled "9 words" (whitespace tokens = 11; even dropping operators ≈ 10), E3 labelled "4 words" (3 tokens), E7 labelled "8 words" (11 tokens; 8 only if counting comment words `Don't fail evaluation if we can't check logs`), E10 "20 words" ✓, R8 "8 words" ✓, R10 "5 words" ✓. No single counting rule reproduces all labels. Cosmetic calibration nit.

### 4.2 Statement-precision defects (entry's prose, not spans)
- **“the only extra module import resolves to a poll-retry wrapper” (entry line 30) is imprecise**: main.py has four non-stdlib imports — `google.cloud.storage, logging`, `google.oauth2.service_account`, `google.api_core.exceptions`, and `utils.evaluation.retry.grade_with_retry`. The retry wrapper is merely the *only non-Google-SDK* import. As written ("the only extra module import") it overstates; the intended meaning is recoverable only by reading "extra" as "non-Google/local".
- **“retried up to three times five seconds apart” (entry line 53)**: `DEFAULT_MAX_ATTEMPTS = 3` means at most 3 *total attempts* = 1 initial try + up to 2 retries (retry.py docstring: "Default 3 — i.e. 1 initial try + up to 2 retries"; "3 trials, 5s interval"). "retried up to three times" could be read as three retries beyond the initial try. Also, the retry wraps only the two side-effect infra checks (`grade_with_retry(_check_completion)`, main.py:262); the `record.csv` comparison at 267–281 runs once, after `ok`. The entry's sentence is consistent with this (it scopes retries to the "whole gate" of side-effect checks), but the count wording is off by one.
- Entry's "a case-insensitive scan … finds no LLM or judge path" is confirmed exactly: the regex `prompt|judge|model|openai|chat|gpt|llm|claude|anthropic` (case-insensitive) has zero hits in my fetched main.py (verified programmatically).

### 4.3 Capture gap (lane artifact, not a span failure)
- `.ufo/waves/round-32/assimilation/captures/SHA256SUMS.txt` records only 2 fetches (toolathlon main.py, arXiv abs). The S094 row and the entry cite `utils/evaluation/retry.py` (S094 row header explicitly includes "and the retry wrapper it imports"), and S093's test.sh/parser.py are cited by both the round-31 entry and this one — but no capture or checksum for any of those three files exists in the captures dir. My fresh fetches all resolve, so the citations are sound; the lane's capture record is incomplete relative to its own citations.

### 4.4 S093 restated claims re-verified at the pinned revision (they resolve)
- `tests/test.sh` prints the reset message at :33; the tracked/untracked walk uses `T) git checkout HEAD -- "$path"` (:71) and `U) rm -f -- "$path"` (:72); the third pass `git diff --name-only HEAD` with fixtures checkout at :97–104 (checkout at :102) exists; reward: `all_required = fail_to_pass | pass_to_pass` (:213), `success = all_required <= passed_tests` (:214).
- `parser.py` regex `` ^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR) `` at :68, `re.match` on stripped lines at :71 and :90 (stdout at :70–86, stderr at :88–105); last-write-wins dedupe at :121 `unique_results = {result.name: result for result in results}.values()`; the `PASSED`-only set is built in `test.sh` :207–210 (`if test.get('status') == 'PASSED': passed_tests.add(...)`), not in parser.py (which exports all statuses to `output.json`).

### 4.5 Claim-level confirmations (semantic)
- Comparator: `record.csv` (agent workspace) vs `groundtruth_workspace/expected_ratio.csv` — main.py:53–56, 268, 273–274, 280.
- Operative tolerance 0.05 set at call site (280) overriding default 0.1 (58); diff compared in percentage-point units (`diff_A = abs(actual_A - expected_A) > tolerance_pct`, :83–94; values parsed as floats after stripping `%`, :44–45).
- One missing or extra scenario fails: :66–72 build errors; :98–100 `raise ValueError`. Verified.
- Prefix existence check: `bucket.name.startswith(bucket_prefix)` over the whole bucket list (:134–139); gcloud fallback also uses `startswith` (:155–158). The only `subprocess.run` in the file is the gcloud call (:149–152); `subprocess` otherwise appears at import (:5) and in the except clause (:164).
- Fail-open: `except Exception as e: print(...); return True  # Don't fail evaluation` (:216–218). Verified.

## 5. Distinct attack items (≥32 required)

Span/quote checks: E1–E10 (10), R1–R10 (10) → 20. Semantic/structural items (all executed):
21. fetch-by-pin works for both raw pins + arXiv (resolve + sha256 recorded)
22. main.py sha256 == capture manifest (3bad26b6…)
23. arXiv html sha256 == capture manifest (851b03db…)
24. case-insensitive scan regex → zero hits
25. only subprocess.run is the gcloud fallback (:149–152)
26. imports: four non-stdlib modules — `google.cloud.storage/logging`, `google.oauth2.service_account`, `google.api_core.exceptions`, `utils.evaluation.retry.grade_with_retry` (impression "only extra module import" flagged)
27. `record.csv` vs `expected_ratio.csv` wiring (paths + load calls)
28. 0.05 call-site override vs 0.1 default
29. per-scenario touching-point comparison (not ratio)
30. missing/extra-scenario failure path (:66–72, :98–100)
31. bucket prefix existence check (:134–139) + gcloud fallback startswith (:155–158)
32. fail-open on error (:216–218)
33. infra gate retried via `grade_with_retry(_check_completion)` (:262); record compare runs once after (:267–281)
34. retry default counts: 3 total attempts = 1 + 2 retries, 5 s interval (retry.py:44–45, docstring :60–63, :75)
35. parser regex at :68; re.match at :71/:90
36. stderr scan presence (:88–105)
37. dedupe last-write-wins at parser.py:121
38. PASSED-only set built in test.sh :207–210 (not in parser.py)
39. reward line all_required :213 / success :214
40. tracked/untracked reset T/U cases :68–74
41. fixture-diff third pass :97–104 with checkout at :102
42. reset message :33
43. arXiv version v2 marker present; submitted 7 Dec 2024 / revised 10 Dec 2024 meta values
44. arXiv title (page `<title>` + citation_title) matches S097 row title
45. no journal/venue reference on abs page (citation_journal_title/journal_ref absent) → supports tier B
46. abstract token count = 20 (matches "20 words" label)
47. entry structure: exactly three `source:` lines S093/S094/S097, `verified-at: 2026-10-25`, `recheck: 180d` (read full draft)
48. README has exactly one index row for the entry (README.md:67)
49. S093 row `used-by` includes both verifier-execution-model.md and benchmark-grader-semantics.md (SOURCES.md:112 tail)
50. S094 row `used-by` names the entry (SOURCES.md:114 tail)
51. S097 row `used-by` names the entry (SOURCES.md:115 tail)
52. capture gap: retry.py/test.sh/parser.py absent from SHA256SUMS.txt (2 entries only)

52 distinct items executed; all spans located.

## 6. Verdict

All quoted spans in the entry and all anchor citations in draft rows S094/S097 (plus S093's row anchors) were found verbatim in my own fetches at the stated file:line (with the single cosmetic range nit on main.py:217–218, literal fully on 218). No span is absent or moved. No C1 kill-rule trigger: all three pinned sources resolve and their quotes are locatable at the pinned revisions.

`VERDICT: all-located` (non-span nits recorded in §4.1–4.3: word-count label inconsistency, "only extra module import" overstatement, retry-count wording, capture-dir gap).
