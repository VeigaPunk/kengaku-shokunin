# TallyR05 — independent oracle for C1: `attrib-r22-legs-hyper.log`
Read-only; grep/sed/awk only, no python, no lane scripts, no journal read. Identity: sha256
`f2978c2f0925de915b669fc67ff8eea21f901a531d257f5e04571cead35a7c6d`, 237 lines, last commit
`8a0848377ee19e03305a63afbe3b50a7ba6965c6` (2026-10-16 10:31:08 -0300).
## 1. Every `## GT + scoring at close` block
NONE. `grep -c '^## GT + scoring at close'` → 0; `grep -icE '^[ \t]*#+[ \t]*GT[ \t]*\+[ \t]*scoring'` → 0.
Only `##` header in the file is the addendum `:131` (`## Trial-runner-hyper addendum ...`), body `:132-237`.
Hence no authoritative block, no bar, no min-n, no scored n, no exclusions — all four fields N/A.
## 2. Authority under P1
The cited rule verifies at `attrib-r21-impl-ds-trials.log:316` (`AUTHORITATIVE SCORING SECTION: the
LAST "## GT + scoring at close" block above`), but binds nothing here; `grep -n AUTHORITATIVE` in
this file → NONE. Under P1 the file is trial-only and contributes **0 scored trials**. It is also not a
block-level dedup candidate (no block to compare).
## 3. Trial-only facts
- Trials 20 (`grep -c '^=== \['`=20); records `{"kind":"record"}`=20 at `:9-128`.
- First `T01 2026-10-16T11:50:58.065Z`; last `T20 2026-10-16T11:52:26.186Z` (headers = t0 start).
- Own close `:129`: `last_request_utc=2026-10-16T11:52:27Z` (T20 t0 + 1.362 s wall ≈ 11:52:27.5Z).
- `"status": 200, "error": null` ×20; no retries, no non-200.
## 4. No confusion table is possible
GT keys absent, not empty: `'"gt"'`=0, `'"correct"'`=0, `'"chain"'`=0, `'"gt_class"'`=0; `score_summary`=0.
Stored verdict lines: none — `grep -nE '^(ACCURACY|TARGET|BODY|STREAM TARGET)|STREAM TARGET'` rc=1.
Mis-attribution hazard: the only verdict-shaped text is prose at `:210` (`score block: TARGET
opencode-go on-target GT n=0 -> FAIL`), quoting `attrib-r22-legs.log:293`/`:345`; not this file's verdict.
## 5. Design tally (prediction only, NOT GT — do not score)
`10 force-hyper -> hyper` (conf 0.417–0.440); `10 force-opencode-go -> alibaba-token-plan` (0.480).
Body len: force-hyper 227 ×10; force-opencode-go 216 ×10.
## 6. Cross-file duplication
Exact header-timestamp collisions with both siblings: **0** (`comm -12`). Interleaving is real: 12
`attrib-r22-legs.log` + 17 `attrib-r22-opencode-trials.log` header trials inside hyper's window.
Body-len fingerprint is identical across all three files (227/216), so body length cannot separate
seats; only timestamps do. Hyper's 20 rows duplicate no scored block.
## 7. Trial ids + request timestamps (UTC, from `=== [..]` headers; equal record `t0_utc` 1:1)
T01 11:50:58.065 | T02 11:51:03.351
T03 11:51:07.200 | T04 11:51:11.964
T05 11:51:16.090 | T06 11:51:20.982
T07 11:51:24.852 | T08 11:51:29.655
T09 11:51:33.531 | T10 11:51:38.482
T11 11:51:42.352 | T12 11:51:47.270
T13 11:51:51.076 | T14 11:51:56.148
T15 11:52:00.063 | T16 11:52:05.861
T17 11:52:09.797 | T18 11:52:15.135
T19 11:52:19.027 | T20 11:52:26.186
Classes alternate hyper (odd) / opencode-go (even).
## 8. Remaining unknowns
Journal rows matching these 20 stamps (not read; out of scope); scorer's per-seat GT-join provenance
(addendum `:160-174`: not separable from the journal alone in the shared window).
VERDICT: `attrib-r22-legs-hyper.log` is **trial-only** — 0 scoring blocks, 0 GT fields, 0 stored
verdicts, 20 blind trials 11:50:58.065Z–11:52:26.186Z (close line 11:52:27Z); contributes **0 scored
trials** under P1 and cannot yield a per-leg confusion table or any interval estimate.
Installs: none.
