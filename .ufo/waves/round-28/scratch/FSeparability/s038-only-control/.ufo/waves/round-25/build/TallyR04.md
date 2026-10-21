# TallyR04 — independent hand-tally: attrib-r21-impl-glm-trials.log

Receipt: `corpus/evidence/attrib-r21-impl-glm-trials.log` — 226 lines, sha256 `04c505e4d384ce345ec4ac23462c6392428b0493aaba5c3213a6ce45d2556744`. Method: grep/sed/awk on committed bytes only; no python, no lane scripts, no endpoint.

## Blocks
- `grep -n '^## '` → 142 `## GT + scoring at close`, 190 `## Seat adjudication`. Exactly one scoring block exists.
- Scored block range **142–188**: provenance 142–145, table header 147, separator 148, scored rows 149–170, GT counts 172, ACCURACY 173, honesty note 174, ablation block 176–187, `score_summary` JSON 188. Line 189 blank; 190 opens the adjudication.
- Authoritative: the P1 rule (last block) and the file's own note AGREE; the only block is authoritative. Note at 192–195: "AUTHORITATIVE SCORING SECTION: the single "## GT + scoring at close" block above".
- `## Seat adjudication` (190–226) carries no GT rows and records no post-scoring requests (223–226).

## Confusion table (rows = GT leg, cols = prediction; 22 rows via awk)
| GT \ pred | devin | zai | row n |
|---|---|---|---|
| devin | 9 | 0 | 9 |
| zai | 0 | 13 | 13 |
| hyper | 0 | 0 | 0 |
| col n | 9 | 13 | 22 |

- Recall devin 9/9 = 1.000, zai 13/13 = 1.000, hyper 0/0 → UNTESTED. Specificity devin 13/13, zai 9/9. Both off-diagonals are zero.
- Distinct predictions are {devin, zai}: hyper is never predicted and never GT, so this receipt yields no hyper evidence at any n.
- Parse hazard: `gt_class` is `served` on all 22 rows (149–170); the leg label exists only in column GT. Keying on `gt_class` collapses to a single class.
- Parse hazard: chain cells contain `FAIL` (9 rows, e.g. 149 `1/zai FAIL 429`) — loser-leg records, not verdicts.

## Scored totals, exclusions, bar
- Scored n = 22, correct = 22, accuracy 1.000. Rows 149–170 are all `YES`; GT counts 172 `{"devin": 9, "zai": 13}`; 188 `"scored": 22, "correct": 22`.
- Excluded trials: **none** (188 `"excluded": []`). No footnote, annotation or non-YES row exists; `grep -c '^|'` = 24 = header + separator + 22 rows, and rows = records = headers = 22.
- Bar 0.80, min scored n 20 (both on 173). 22 ≥ 20, so the receipt's own point rule is satisfied. Provenance of "min scored n 20" is not in this file.

## Stored verdict lines
- 173: `ACCURACY: 22/22 = 1.000 (bar 0.80, min scored n 20) -> PASS` — the only stored verdict.
- 193: restatement inside the seat note (`ACCURACY 22/22 = 1.000 -> PASS`), not an independent verdict.
- No TARGET / BODY / STREAM TARGET verdict exists: `grep -nE 'ACCURACY|TARGET|BODY|STREAM'` → hits only 173 and 193.
- No per-leg recall or specificity verdict is stored; hyper UNTESTED appears only as prose (174, 194).

## Trial inventory — ids + request t0 (UTC, 2026-10-16)
T01 10:22:32.489 · T02 36.624 · T03 40.870 · T04 45.163 · T05 10:23:03.673 · T06 16.731 · T07 21.542 · T08 27.205 · T09 31.303 · T10 35.844 · T11 40.117
T12 44.812 · T13 49.057 · T14 53.398 · T15 10:24:03.521 · T16 14.147 · T17 18.232 · T18 22.467 · T19 26.860 · T20 31.337 · T21 35.698 (err) · T22 41.660 (err)
- First 10:22:32.489Z, last 10:24:41.660Z; line 140 `last_request_utc=2026-10-16T10:24:43Z` (completion stamp, wall 2.038 s). std=20 err=2 matches meta line 7.

## Independent checks
- Journal window 143 `--since @1792146147 --until @1792146311` = 10:22:27Z–10:25:11Z. All 22 `t0_epoch` in [1792146152.489, 1792146281.661]: outside_window=0, non_monotonic_pairs=0.
- Duplication vs `attrib-r21-glm-trials.log`: shared t0 = 0/22, shared body `id_value` = 0, table rows differ → different samples; dedup does NOT fire for this pair. That sibling is trial-only (0 `## ` headings, 22 trials).

## Gaps / inference
- Observed: everything above. Inferred: none required for the tally. Unresolved: none for the assigned question.
- Immaterial sibling quirk (outside this file): `attrib-r21-glm-trials.log` has 21 `id_value` keys for 22 records; this file has 22/22.

VERDICT: authoritative block = the file's only scoring block, lines 142–188 (P1-last rule and the :192–195 note agree); 22/22 correct, devin 9/9 and zai 13/13 recall (specificity 13/13, 9/9), hyper 0/0 UNTESTED, 0 excluded, bar 0.80 vs min-n 20 met; one stored verdict, ACCURACY PASS at :173, no TARGET/BODY/STREAM TARGET verdicts; sample distinct from attrib-r21-glm-trials.log (0 shared timestamps or body ids).
Installs: none.
