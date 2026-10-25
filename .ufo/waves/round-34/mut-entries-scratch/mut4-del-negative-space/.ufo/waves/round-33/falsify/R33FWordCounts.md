# R33FWordCounts — S103 anchor quote word counts (falsify wave)

Seat: `KengakuR33.R33FWordCounts` — lane `kengaku-shokunin`.
Item: anchor quote word counts for S103 (Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe…`).
Method: re-ran the current quote gate on the staged `append-rows.md`; per-span tokenization; label-mutation controls in a `/tmp` sandbox. No lane/file mutated; no tools installed (nothing needed — `python3`, `grep`, `sed`, `wc`, `tr` already present).

## 1. Gate re-run (verbatim, current working tree)

```
$ python3 plans/sources_adopt.py --quote-file .ufo/waves/round-33/assimilation/append-rows.md --artifact .ufo/waves/round-33/assimilation/captures --url-map .ufo/waves/round-33/assimilation/url-map.json
QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=url-map.json entries=3
  ok S103 words=11 ... quote="def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:" bound=...->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe.../tasks/finalpool/ab-testing/evaluation/main.py
  ok S103 words=5 ... quote="# Validate with 0.05% tolerance" bound=... (same URL)
  ok S103 words=3 ... quote="validate_record_data(actual_records, expected_records, tolerance_pct=0.05)" bound=... (same URL)
  ok S103 words=11 ... quote="return True  # Don't fail evaluation if we can't check logs" bound=... (same URL)
  ok S103 words=4 ... quote="if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):" bound=... (same URL)
  ok S104 words=8 ... (2 more S104 spans) 
EXIT=0
```

Exit 0, `spans=8` (S103 has 5, S104 has 3), `overlong=0`, `absent=0`, `malformed=0`. Every S103 span is located in the capture and bound to the pinned blob URL.

## 2. Per-span word counts — gate vs staged vs landed vs entry

Word counter is `len(text.split())` (whitespace tokens), shared with `round30_defects.words` (`sources_adopt.py:280-282`). Capture line numbers verified with `grep -n` (`:58`, `:218`, `:234`, `:279`, `:280`).

| # | capture line | quoted span | gate words (`wc -w` = same) | staged `append-rows.md` label | landed `corpus/SOURCES.md:118` label | entry `benchmark-grader-semantics.md` phrasing |
|---|---|---|---|---|---|---|---|
| 1 | 58 | `def validate_record_data(...) -> None:` | **11** | `(11 words; signature default, not executed)` | `(11 words)` | “11 whitespace-separated tokens” |
| 2 | 279 | `# Validate with 0.05% tolerance` | **5** | `(5 words)` | `(5)` | “4 words plus the `#` marker” |
| 3 | 280 | `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` | **3** | `(3 words; the only call, so 0.05 is the executed tolerance)` | `(3)` | “3 whitespace-separated tokens” |
| 4 | 218 | `return True  # Don't fail evaluation if we can't check logs` | **11** | `(11 words; caught exceptions fail open)` | `(11)` | — |
| 5 | 234 | `if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):` | **4** | `(4 words; absent credentials fall through to implicit None, which fails the task)` | `(4)` | — |

All five gate counts match the staged and landed labels exactly. No numeric discrepancy between staged anchor labels and the gate.

## 3. The 0.05% comment count (verified)

`# Validate with 0.05% tolerance` = **5 whitespace tokens**: `#`, `Validate`, `with`, `0.05%`, `tolerance`. `0.05%` is one token. The gate's 5 includes the `#` comment marker; the prose word count is 4. The staged label `(5 words)` and the gate both count the marker as a token; the entry's “4 words plus the `#` marker” is the same 5 tokens stated in prose words. All three phrasings reconcile; under the gate's token convention the count is 5 and the 25-word cap is nowhere near.

Context (retained evidence): the round-33 build report `R33CaptureToolathlon.md:145-156` documents this exact span as an earlier annotation defect (entry lines 41-42 said “4 words” for the comment and “5 words” for the call; measured `wc -w` gives 5 and 3). The current entry already carries the corrected phrasing (“4 words plus the `#` marker”, “3 whitespace-separated tokens”), so the integration fix landed.

## 4. Discrepancy/limitation findings

1. **The gate is label-blind (proven, sandbox only).** The gate recomputes counts from the quoted bytes and never reads the `(N words)` annotations. In `/tmp/r33wc/sb` I copied the staged package, relabeled `(5 words)` → `(1 word)` (a.md) and → `(99 words)` (b.md), and re-ran the identical command: both exit 0 with `words=5` unchanged, `overlong=0`, identical receipts. A stale, overstated, or fabricated count in any anchor label would green-light. The current labels happen to be correct; correctness is not enforced.
2. **Per-row vs per-span cap.** The cap is per span. S103's anchor cell carries 11+5+3+11+4 = **34 tokens across 5 spans**; all pass. `sources_adopt.py`'s contract text (“an anchored quote is at most 25 words”) is per quote, so this is a limitation, not a violation — but the SOURCES header's “a ≤25-word quote per row” phrasing (`corpus/SOURCES.md:5`) is looser than what any gate enforces.
3. **`#` counts as a word.** The comment's “5 words” is 5 tokens; a reader counting English words sees 4. Harmless here (5 ≪ 25), but the numbers in any annotation are only reproducible under the whitespace-token convention, and nothing states that for S103's labels except the entry's “whitespace-separated tokens” phrasing.

## 5. Verdict

- S103 anchor word counts: **not falsified** — all five counts reproduce exactly (11/5/3/11/4) across gate, staged labels, landed registry, and entry; all ≤25; all located and bound; exit 0.
- 0.05% comment count: **verified** — 5 whitespace tokens (4 prose words + `#` marker); staged label and gate agree; earlier annotation defect (4/5) already fixed in the entry.
- Labels-unverified gate: **limitation** (uncaught by design) — demonstrated with sandbox mutations; gate exit is independent of the `(N words)` annotations.
- Per-row 34-token anchor total vs per-span 25 cap: **limitation** — consistent with the gate's own per-quote contract, but the “per row” wording in `corpus/SOURCES.md:5` is not enforced.

## 6. Files changed / tools

No files changed in the lane (including the falsify directory — this report is the only write). Git/JJ/index untouched. No tools installed or upgraded. Sandbox `/tmp/r33wc` removed.
