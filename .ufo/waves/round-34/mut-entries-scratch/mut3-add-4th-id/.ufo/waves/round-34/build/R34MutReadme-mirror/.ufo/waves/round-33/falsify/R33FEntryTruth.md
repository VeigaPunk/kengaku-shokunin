# R33FEntryTruth — falsification of `corpus/knowledge/benchmark-grader-semantics.md` technical claims

Seat: R33FEntryTruth (falsify wave, round 33, hyaku run 7). Date: 2026-10-25.
Target: every technical claim in the current `corpus/knowledge/benchmark-grader-semantics.md` (171 lines),
attacked against the pinned Toolathlon capture (main.py + retry.py @ `9be8d8fe`) and the S104 capture
(arXiv 2412.05579v2 abs page), plus the S093 pins it restates (`SWE-bench_Pro-os` @ `66f92766`).
Named attack surfaces: 0.05 percentage-point wording · log-check exception-vs-missing-credentials paths ·
call count · prior-work S093 separation · LLM-as-judge survey attribution.

Method: no lsp server is mounted in this session (no `lsp` device among available tools), so all
caller/definition checks were done by numbered byte reads and live-fetch diffs — recorded here as the
fallback path, with grep only as a literal counter, never as semantic proof. Fixtures and fetched pins
live in `/tmp/r33f-entrytruth/`; every git command ran with explicit paths; zero lane-tree writes except
this report. Tools installed: none.

## 0. Provenance chain (verified first)

- `sha256sum` of the three digested captures matches the entry's Reading basis and
  `captures/SHA256SUMS.txt` exactly: main.py `3bad26b6…` (14,138 B, 297 ln), retry.py `db11e66e…`
  (4,519 B, 109 ln), arXiv html `44195c5f…` (43,661 B, 617 ln).
- Independent fetch of the pinned revisions (raw.githubusercontent.com @ `9be8d8fe07a4…`) →
  **byte-identical** to both Toolathlon captures (`diff` clean both ways, same sha256). The capture
  chain is sound; every line number below is from `cat -n` on the verified bytes.
- Same check for S093: `test.sh` + `parser.py` fetched at `66f92766` from `scaleapi/SWE-bench_Pro-os`;
  all restated anchors resolve (see §4).

## Findings by severity

### F1 — MEDIUM, uncaught: "No S093 file is in this wave's capture set" is false at tip
Entry line 40: *"No S093 file is in this wave's capture set: the S093 section below is a restatement…"*.
But `.ufo/waves/round-33/assimilation/captures/` holds **four** files, including
`swebench-pro-tests-test.sh` (7,864 B), and `sha256sum` gives `b6f26eec…976d0` — byte-identical to
round-31's `test.sh` capture **and** to my live fetch of S093's pinned `tests/test.sh` @ `66f92766`.
So an S093 file is in this wave's capture set. The gate itself treats the directory as the capture set
(`gate-receipts.txt` prints `artifacts=SHA256SUMS.txt,…,swebench-pro-tests-test.sh,…`), and
R33C1KillRule row 11 records that every UTF-8 file under `captures/` is a quote candidate. Mitigations,
for calibration: the *directory's* `SHA256SUMS.txt` carries exactly the three digests the entry names
(that clause is true), and the fourth file's bytes are the right bytes — the sentence is wrong, not the
pin. Build-side `R33EntryTruth.md` saw the file ("capture provenance gap") yet stamped
"entry-truth-clean"; it also asserts "no `entry-patched.md` exists in the wave tree", while
`.ufo/waves/round-33/assimilation/entry-patched.md` (12,984 B) exists at tip — the build report is
stale on both counts. Verdict: **caught here, uncaught by build**.

### F2 — MEDIUM, uncaught: the log-check summary elides the diagnostic-entry carve-out, and the code's own docstring/message contradict its behavior
Entry: the side-effect check *"requires the ab-testing logging bucket to contain no entries
(`check_abtesting_logging_bucket_clean`, `main.py:168-218`, called at `:234`)"*. The code requires no
**non-diagnostic** entries: the filter at `:178` appends `AND NOT jsonPayload.logging\.googleapis\.com/diagnostic`,
and `:198-205` manually skips diagnostic payloads *"if filter didn't work"*. A bucket full of
diagnostic-only entries passes the "clean" check. The entry — which exists to record what the grader
compares vs what it says it compares — never records that the function's docstring (`:169` "contains
only the preprocessing test log entry") and the `ValueError` message (`:235` "should contain only the
preprocessing test log") describe a contract the code does not implement: any non-diagnostic entry —
including a literal "preprocessing test log" entry — returns `False` at `:211`. Its fail-open/fail-closed
path analysis is otherwise byte-exact (see §2). Verdict: path claims **survive**; the summary and the
missing says-vs-does note are **defects, uncaught by build**.

### F3 — LOW, uncaught: `PROVINCE.md` anchor off by one line
Entry cites `PROVINCE.md:219-220` for *"it does not run a benchmark, certify a task, or own deployment
configuration, runtime task validity, hosted judges, contamination measurement"*. The quoted span sits
at `PROVINCE.md:218-219` (verified by `cat -n`; quote text itself byte-exact). Every corpus-side anchor
in the entry is otherwise exact — `README.md:276` (bullet) and `:278` ("and for Toolathlon") both
resolve. Verdict: **caught here, uncaught by build** (build's only line-precision NIT was about README).

### F4 — LOW, uncaught: S093 restatement compresses away the additions-vs-edits distinction
Entry (S093 section): the reset *"rewrites the tracked test-code surface while a file under a
data-directory parent is excluded from that rewrite"*, so *"a file the agent adds under one of those
parents never enters the reset list"*. At the pin this is true of the T/U lists (`is_test_code` `:40-44`
→ absent from `:60`/`:63`), **but** the reset's third pass also restores *modified tracked* files under
those parents: `git diff --name-only HEAD` → case `*testdata/*|*test_data/*|*fixtures/*|*fixture/*|*mocks/*|*mock/*|*__snapshots__/*`
→ `git checkout HEAD -- "$p"` (`test.sh:97-104`, checkout at `:102`; verified on my fetched pin).
Round-31's entry is explicit: "the hole is *additions*, not edits". The round-33 final clause ("the
agent adds") scopes correctly, but the middle clause read standalone implies any data-dir file escapes
the reset — false for edits. Verdict: **calibration defect**; the entry names the round-31 entry, so a
reader who follows the pointer gets the full rule.

### F5 — LOW, calibration: the [INFERENCE] percentage-point gloss is sound but under-cited — and less hedged than the registry row built from it
The entry rests the unit inference only on the `%` formatting in the failure message (`:86`, `:93`).
Stronger on-pin evidence is uncited: the CSV headers are required fields literally named
`"A_conversion %"`, `"B_conversion %"` (`main.py:25`), and the parser strips a `%` with the comment
`# Parse percentage values (remove % sign if present)` (`:42-45`). The 0.05-unit = 0.05-percentage-point
reading is **correct**; the hedge could be dropped or re-anchored. Inversion of authority: `SOURCES.md`
S103's `teaches` cell asserts "0.05 percentage points per scenario" flatly while the entry hedges the
same fact as [INFERENCE]. Verdict: claim **survives**; citation gap.

### F6 — LOW, uncaught: the contrast sentence generalizes one-task evidence to whole benchmarks
"SWE-bench Pro V2 and Toolathlon both grade without an LLM judge, but by different mechanisms" — each
half rests on one task's code (S093's `test.sh`/`parser.py`; S103's `main.py`). §What-this-does-not-
establish carries the scoping caveat only for Toolathlon ("what any Toolathlon task *outside* the
`ab-testing` family uses"); the SWE-bench Pro V2 half carries none in this entry (round-31 scopes it:
"one SWE-bench Pro V2 task"). Verdict: **scoping gap**, inherited prior work is properly scoped
upstream.

## Per-surface attack results (the five named)

1. **0.05 percentage-point wording — SURVIVES.** Signature default `tolerance_pct: float = 0.1` is
   byte-exact at `:58` (11 whitespace tokens, as counted); the sole call site `:280` passes
   `tolerance_pct=0.05` under `:279` `# Validate with 0.05% tolerance` (4 words + `#` marker, as
   counted); the executed comparisons are `if diff_A > tolerance_pct` / `if diff_B > tolerance_pct`
   (`:84`, `:91`) — exactly as the entry states. Values live on a percent scale (`:25` headers, `:42-45`
   parse, `:86`/`:93` `%±…%` formatting), so 0.05 units = 0.05 percentage points: the entry's
   [INFERENCE] is correct (F5). "The `0.1` default is never executed" holds — grep shows exactly two
   occurrences of `validate_record_data` (`:58` def, `:280` call).

2. **Log-check exception-vs-missing-credentials paths — SURVIVES byte-for-byte.** Verified on numbered
   capture lines: `(None, None)` returns at `:118-120` (FileNotFoundError) and `:121-123` (broad
   except); guard `if project_id_from_creds and credentials:` at `:176` → false → try ends without
   `return` → implicit `None`; `validate_task_completion`'s `if not check_…` at `:234` →
   `not None` is true → `raise ValueError` at `:235`. Fail-closed. The broad `except Exception` at
   `:216-218` returns `True` with the quoted comment — fail-open, reachable only for failures inside
   the guarded block (client construction `:177`, `list_entries` `:192-196`, payload inspection
   `:200-205`), since `get_project_id_and_credentials` never raises on credential failure. Missing
   `log_bucket_name.txt`: opened at `:171-172`, outside the `try` at `:173` — propagates, fail-closed,
   exactly as stated. Storage check: guard `:132`, gcloud fallback `:145-166`, `return False` on CLI
   failure `:164-166`, raise at `:230` — all exact. Exactly one caught-exception `return True` site
   exists (the entry's own falsifier #3 does not fire). Residual: F2's carve-out omission. (Pedantic
   residual, not a defect: `get_project_id_and_credentials`'s *print* statements sit inside its except
   handlers, so a broken stdout could surface a "credential" failure as a caught exception — outside
   every claim the entry makes.)

3. **Call count — SURVIVES exactly.** `grep -n` over the verified capture: `validate_record_data` at
   `:58` and `:280` only ("single call site" true); `grade_with_retry` at `:12` (import) and `:262`
   (call) only, no `max_attempts`/`poll_s`/`sleep_budget_s` override. `retry.py:44-45` = the two
   defaults, exactly as claimed; `grade_with_retry` calls `check_fn` at most `max_attempts` times
   (`:83` `range(1, max_attempts + 1)`, `:97-98` no sleep after final), docstring `:61-62`: "Maximum
   number of times check_fn will be called. Default 3 — i.e. 1 initial try + up to 2 retries" — the
   entry's "at most three" is exact. Record comparison at `:280` sits outside the wrapper; its failure
   path prints and `exit(1)` at `:293-295`; completion failure exits at `:263-265`. Both non-zero, as
   stated. Side-effect checks precede record validation in process order (`:262` before `:273-280`) —
   "first in the process order" verified.

4. **Prior-work S093 separation — SURVIVES with two defects (F1, F4).** Separation proper holds: the
   entry restates and cites rather than re-derives; `SOURCES.md` S093 `used-by` lists both
   `benchmark-verifier-execution-model.md` and `benchmark-grader-semantics.md` (verified row tail);
   S103/S104 rows: `status=mined`, `opened=2026-10-25`, `used-by` names the entry. Every restated
   anchor resolves at my independently fetched `66f92766` bytes: `test.sh:213-214`
   (`all_required = fail_to_pass | pass_to_pass` / `success = all_required <= passed_tests`),
   `:207-210` (PASSED filter), `:38` (the exact seven-dir `DATA_DIRS` set), `:43-44` (guard), `:71`
   (`T) git checkout HEAD -- "$path"`), `:33` (quoted banner); `parser.py:68` (the regex, byte-exact),
   `:88-90` (stderr rescan), `:121` (`unique_results = {result.name: result for result in
   results}.values()` — last-write-wins, as glossed). Round-31 captures (`round-31/assimilation/captures/`)
   exist as the stated re-location basis; note parser.py is *not* in this wave's set (test.sh is — F1),
   so the "re-located against test.sh and parser.py … this round" sentence is half-matched by wave
   artifacts and fully matched by the pins.

5. **LLM-as-judge survey attribution — SURVIVES fully.** `citation_title` at capture line 41 is
   byte-exact "LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods" (capital J);
   the abstract at line 124 contains the quoted sentence byte-for-byte with lowercase
   "LLMs-as-judges" — the entry's capitalization observation is exact, and the quote is 20
   whitespace-tokens, exactly as counted (≤ the 25-word kill-rule cap). The capture is the v2 page
   (12 occurrences of `2412.05579v2` vs 2 of v1, submission-history block present; `citation_online_date`
   2024/12/10 = v2). "(preprint)" is supported: comments cell at `:131` is "60 pages, comprehensive and
   continuously updated" (6 tokens, as the S104 row counts) and no journal-ref appears in the capture.
   The entry's use of S104 is honestly scoped — "that causal link is not asserted by the source" — and
   the five-part taxonomy is the abstract's own list. No misattribution found.

## Word-count audit (build seat's NIT is stale)

The committed entry's counts are all correct under its stated conventions: `:58` = 11 whitespace
tokens; `# Validate with 0.05% tolerance` = 4 words plus the `#` marker (build's "5 whitespace tokens"
counts the marker as a word — the entry's phrasing excludes it); `:280` call = 3 tokens (entry says 3;
build's "entry: '5 words'" matches no text in the committed file); S104 quote = 20 words; S093 row
quotes = 8/5 tokens; S104 row's `:131` = 6 tokens.

## Residual risk / verification gaps

- No lsp semantic checks (no server in session); "sole call site" is proven for this file by literal
  count, and the entry explicitly scopes its claims to this file — other-repo callers are out of its
  contract by construction.
- `swebench-pro-tests-test.sh` is digest-pinned nowhere this round (directory `SHA256SUMS.txt` has 3
  rows); identity established here only by my independent fetch comparison.
- `parser.py` re-verification this round rests on round-31 captures + my live fetch, not on a round-33
  committed capture — consistent with the entry's own Reading-basis disclosure, modulo F1.
- The arXiv "(preprint)" status is corroborated only by the abs page (no journal-ref); a later
  publication would not falsify the entry (it cites the v2 artifact), but the `recheck: 180d` line
  (next due 2027-04-23 — arithmetic checked) is the only guard.
- `entry-patched.md` vs the committed corpus entry was not diffed (out of seat scope); the build
  report's claim that it does not exist is falsified by the listing above.

## Verdict

**Entry survives falsification on all five named surfaces** — every operative technical claim about
the Toolathlon grader (tolerance, call sites, retry budget, log-check fail-open vs fail-closed paths,
no-judge scan, process order) and the S104 attribution is byte-accurate at the pinned revisions, and
the S093 restatement's anchors all resolve at the live pin. The entry is **not truth-clean**: two
MEDIUM defects in its own framing sentences (F1 "No S093 file is in this wave's capture set" — false
at tip; F2 the "no entries" log-check summary eliding the diagnostic carve-out and the unrecorded
docstring/message-vs-code contradiction) and four LOW items (F3 off-by-one PROVINCE anchor, F4
additions-vs-edits compression, F5 under-cited unit inference, F6 benchmark-level generalization of
one-task evidence). None of these flips the frozen C1 predicate; all six are actionable one-line to
one-paragraph repairs. The build-side "entry-truth-clean" verdict was too clean: F1–F3 were visible in
artifacts it had already opened.

## L1 integration correction

The six cited framing issues were corrected in the final entry: the S093 `test.sh` capture is now named and digest-listed (parser.py remains a pinned non-author re-open, not a retained capture); the log check is described as rejecting non-diagnostic entries while noting the docstring/message mismatch; the PROVINCE locator is `:218-219`; the reset distinguishes additions from modified tracked files; the percent-point inference now cites headers/parser; and the no-judge comparison is explicitly one task per benchmark. The original verdict above records the pre-correction snapshot.
