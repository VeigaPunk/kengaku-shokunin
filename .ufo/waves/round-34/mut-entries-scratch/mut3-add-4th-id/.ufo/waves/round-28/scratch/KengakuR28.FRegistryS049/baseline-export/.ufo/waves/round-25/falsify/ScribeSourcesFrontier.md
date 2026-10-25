# ATTACKS: round-25 Sources & frontier numbers (SOURCES counts, tiers, statuses, S011 used-by, README frontier partial discharge), 6180e4f vs 8ea41f9ed

Scratch: /tmp/k25w2-ScribeSourcesFrontier/{base,tip}/ (git archive copies; no lane writes). Tool installs: none.

## Commands and observed output

1. `git show 6180e4f:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'` -> `26`; `git show 8ea41f9ed:...` -> `37`; same grep on archive copies -> `26` / `37`.
2. Tier histogram (`awk -F'|' '{gsub(/ /,"",$5); print $5}'`): base `24 A, 2 C`; tip `34 A, 1 B, 2 C`.
3. Status histogram (column 9): base `18 mined, 5 queued, 3 rejected`; tip `26 mined, 8 queued, 3 rejected`.
4. Rows added at tip, S027-S037 (`grep -E '^\| *S0(2[7-9]|3[0-7]) *\|'`): tier A x10 (S027-S035, S037), tier B x1 (S036); status mined x8, queued x3 (S031, S032, S035).
5. `git diff 6180e4f 8ea41f9ed -- corpus/SOURCES.md | grep -E '^[-+]\|'`: 1 removed line (old S011), 12 added lines (new S011 + S027-S037).
6. S011 used-by, old -> new: `corpus/knowledge/llm-judge-calibration.md` -> `corpus/knowledge/llm-judge-calibration.md, corpus/knowledge/attribution-interval-calibration.md`. Status stays `mined`.
7. README frontier (`corpus/README.md` §Frontier, `awk` on `^- \*\*`): base 5 bullets, tip 5 bullets. `grep -c 'Partly discharged'` base `0`; tip diff adds one sub-bullet under "Judge calibration applied inward".
8. `sh plans/round25_census.sh` run in tip scratch copy: `sources_rows=37`, `tiers A=34 B=1 C=2`, `mined=26 queued=8 rejected=3`, `sources_new_rows_r25=11`, `calib_summary ... transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0`, `state_check ... mismatch=0 superseded=1`.
9. `sha256sum` of `corpus/evidence/attrib-r23-stream.log` at 8ea41f9ed = `afaae9dd...8131`, identical to the 99cf615 blob; gate.md hash matches.
10. Quote presence: `STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL` at line 239 of the log (S036 anchor); S037 transitions string present in `round25-calibration/attrib-calibration-summary.txt`.
11. Web spot-check S027 (web_search, not a fetch): SciPy docs show `proportion_ci(confidence_level=0.95, method='exact')`; the quoted sentence "Use the Clopper-Pearson exact method [1]" was NOT in the snippets, so the quote is unverified (not contradicted).

## Draft section for the round-25 fleet report: "Sources & frontier"

- SOURCES rows: 26 (6180e4f) -> 37 (8ea41f9ed), +11 (S027-S037). Counted by `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md`.
- Tiers: A 24 -> 34, B 0 -> 1, C 2 -> 2. Added rows by tier: A=10, B=1.
- Statuses: mined 18 -> 26, queued 5 -> 8, rejected 3 -> 3.
- Rows touched: one old row, S011 used-by `llm-judge-calibration.md` -> `llm-judge-calibration.md, attribution-interval-calibration.md`. No other pre-existing row changed.
- Frontier: "Judge calibration applied inward" stays open (5 bullets before and after). Partly discharged: exact CP95 verdicts on the r21-r23 receipts (S027-S030, S033, S034, S037) and the Rogan-Gladen share bound (S011 eq. 4-5 form). Still open: the S010 perturbation audit and grader.py outputs.
- Caveat: the lane's bound is a worst-corner CP-lower-bound box, not S011's own adjusted-Wald interval (`attribution-interval-calibration.md` lines 68-72). The README wording should name the Rogan-Gladen bound and say S011's CI method was not ported.

## Findings

- F1 (open): S036 says "supersedes S025", but S025 stays tier A, `queued`, used-by `—`. Both rows cite `attrib-r23-stream.log:239` at the same commit, so the anchor is duplicated with no status flip.
- F2 (wording): the README partial-discharge sentence names only exact-interval verdicts. The knowledge doc and instrument (`plans/attrib_calibration.py:179,462,623`) also carry the Rogan-Gladen bound. That bound is the part that discharges the S011 correction, and the README does not say so.
- F3 (pre-existing, not round 25): S023 and S026 are the same URL (`https://scale.com/blog/swe-bench-pro`), both tier C. Confirmed in base (6180e4f) and tip. S026 was added in e21f9ea.
- F4 (caveat): S033 (Rogan & Gladen) is tier A, `mined`, abstract-only scope. The knowledge doc says the full text was not openable. The gate receipt discloses this; the row is scoped correctly.
- Not a row (correct): Clopper & Pearson 1934 stays a lead; the gate states it was not openable.

VERDICT: PARTIAL — all SOURCES counts, the S011 used-by change, and the S036 sha/quote reproduce exactly. The frontier wording omits the Rogan-Gladen bound and does not say S011's CI method was not ported; S025/S036 duplicate anchor is unflipped.
Installs: none.
