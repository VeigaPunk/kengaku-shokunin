# RevRepairRows — round 26

Axis: calibration. Read-only review of §0 against the named rows and receipts; no lane files other than this report were written.

## Findings (severity order)

**HIGH — E3 must distinguish the actual r25 landing tree from the later r26-base state, and v3 must search the correction where it is appended.** `PROVINCE.md:112` says “25 rows”; `:119` says “holds 37 after round 25.” Those are different snapshots: the 37 count is consistent with the r25 landing `8ea41f9`; S038–S042 were added later and the r26 base `f11bffbf` carries 42. `round25-census-after.txt:2-7` prints `head=8ea41f9` alongside 42 rows / A=38 B=2 C=2 / mined=30 queued=9 rejected=3 / 16 new r25 rows, but that 42-row census is not the `8ea41f9` commit-tree census: `RevGateSection.md:10` says that tip had only S027–S037 (11 new rows; no S038). State the two revisions explicitly; do not cite that receipt as proof that 8ea41f9 contained 42 rows. Also, current `plans/state_check.py:407-417` searches superseding lines in SCORECARD.md only, while E3 is to be appended to PROVINCE.md. v3 must resolve the combined P3b assertion there (or an otherwise correctly scoped correction can never become SUPERSEDED).

Proposed single-line PROVINCE append (have v3 emit/use this combined assertion ID for the two linked census assertions):
```text
- **R26-E3 (2026-10-21)** supersedes `P3b.province.public-literature-registry` — PROVINCE.md:112 “25 rows” and :119 “holds 37 after round 25” are superseded as current-state assertions (37 was the 8ea41f9 landing count); at r26 base f11bffbf the SOURCES census is `sources_rows=42` `sources_malformed=0` `sources_tier_histogram=A=38 B=2 C=2` `sources_status_histogram=mined=30 queued=9 rejected=3` `sources_new_rows_r25=16`; the later rows are S038, S039, S040, S041, S042.
```
The listed 42-row values match `round25-census-after.txt:3-7`; the commit label in that receipt conflicts with its own later-row population, so v3/current-tree census evidence must bind the correction to f11bffbf.

**MEDIUM — E1/E2 need full receipt tokens and exact P3a assertion IDs, not merely “correction row.”** Existing `plans/state_check.py:191-192,407-417` recognizes an exact backticked assertion ID and collects backticked correction tokens. Keep old-text quotations and receipt references unbackticked after the ID so they cannot be mistaken for the `now` tokens. Proposed SCORECARD append lines:
```text
- **R26-E1 (2026-10-21)** supersedes `P3a.capability.interval-reverdict` — SCORECARD.md:558’s “--selftest 14 checks 0 failed” is superseded; now `TOTAL files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 estimates=35 PASS=7 FAIL=0 INDETERMINATE=11 UNTESTED=12 shares=12 n_ge_17=12 stored_verdicts=7 transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0 dup=[corpus/evidence/attrib-r22-legs.log:312-362=corpus/evidence/attrib-r22-opencode-trials.log:204-254]` `selftest: 18 checks, 0 failed`. Receipts: corpus/evidence/round25-calibration/attrib-calibration-summary-v2.txt and attrib-calibration-selftest-v2.txt.
- **R26-E2 (2026-10-21)** supersedes `P3a.capability.state-assertion-check` — SCORECARD.md:559’s “base 6180e4f mismatch=11” is superseded; base now `assertions=241 match=228 mismatch=10 superseded=0 offline_unverifiable=3` `exit=1`; landed tree now `assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3` `exit=0`; selftest now `ALL PASS` `exit=0`. Receipts: corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt, state-check-after-v2.txt, and state-check-selftest-v2.txt.
```
Evidence: `SCORECARD.md:558-559`; interval summary v2 line 54 and selftest v2 line 19; state-check-before v2 line 2 and exit line 14; state-check-after v2 line 1 and exit line 15; state-check-selftest v2 lines 1-2. These values correct 14→18 and 11→10 while preserving the complete base/landed summaries. The source-receipt references in the example are plain text intentionally: the current matcher extracts every code span after the assertion ID.

**MEDIUM — E4 is a historical Gate/Q13 correction, not a P3 `state_check` supersession.** Round-25 Gate cell `corpus/lessons/round-25.md:29` says “and by wave-2 seats.” `RevGateSection.md:6` records the falsify directory empty in the `8ea41f9` landing tree; preregistration records landing at 21:44:48 -03 and first wave-2 report at 21:49:53 -03 (5m05s later). Proposed append in `corpus/lessons/round-26.md`:
```text
- **R26-E4 (2026-10-21)** supersedes the round-25 Gate Q10 support phrase “and by wave-2 seats” (corpus/lessons/round-25.md:29): the landing tree 8ea41f9 (2026-10-20 21:44:48 -03) contained no .ufo/waves/round-25/falsify/ reports; the first wave-2 report arrived at 21:49:53 -03, 5m05s after admission. The generic phrase therefore supplied no second-seat evidence at admission. Q13 now counts only named report paths present in the landing commit; generic seat references support nothing. The red-before command is python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9 and must exit 1 naming the Q10 cell.
```

## Residual risk / verification gaps
- The r26 preregistration names base `f11bffbf`; the existing census receipt labels its output `head=8ea41f9` despite the later rows. Bind the E3 receipt to the actual measured tree and retain the 37-at-landing / 42-at-base distinction.
- LSP is unavailable: `read xd://lsp` returned “No such tool”; no caller/definition/diagnostics query was possible. No code changes, builds, tests, or installs were in this read-only assignment.

Installs: none.
VERDICT: R26-E1/E2/E3 exact append-only wording is grounded above; E3 requires v3 PROVINCE-aware supersession and a tree-identified census receipt, while E4 must be handled by Q13 rather than P3.
