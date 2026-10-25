# TallyR06 — independent oracle: corpus/evidence/attrib-r22-legs.log (C1)
Read-only seat. Method: grep/sed/awk only (no python, no lane scripts), no network. Installs: none.

## Blocks (every `## GT + scoring at close`)
- Block A = lines 260–311 (header 260 @11:57:30Z; table header 266; rows 268–287; GT counts 289; verdicts 290/292/293; JSON 310; 311 blank).
- Block B = lines 312–363 (header 312 @11:57:39Z; table 318; rows 320–339; GT counts 341; verdicts 342/344/345; JSON 362; 363 blank).
- Seat addendum 364–440 follows both blocks.
- Two trial runs precede them: run-1 lines 9–129 (T01 11:50:06.945Z … T20 11:51:49.176Z), run-2 lines 138–258 (T01 11:53:41.144Z … T20 11:55:07.542Z) — 40 trials, 20 per run, ids reused.

## Authority under P1
- P1 rule = plans/round-25-claims.md:28-30 ("the scored block is the LAST `## GT + scoring at close` block"), citing corpus/evidence/attrib-r21-impl-ds-trials.log:316.
- Therefore the counted block for this file is Block B (line 312); Block A contributes 0 scored trials under P1.
- File's own note at lines 378–379 says "both score blocks above are this seat's authoritative adjudication" — conflicts with P1's one-block-per-file rule; P1 governs (pre-registered).
- Block A ≠ Block B: full-table diff (T,class,pred,GT,correct) differs only at T03 (A: pred/GT opencode-go; B: pred/GT hyper); not an in-file identical-table duplicate.

## Authoritative block B tally (rows 320–339; 20 rows; T01–T20 once each)
| GT \ pred | hyper | alibaba-token-plan | opencode-go | n | correct |
|---|---|---|---|---|---|
| hyper | 10 | 0 | 0 | 10 | 10 |
| alibaba-token-plan | 0 | 10 | 0 | 10 | 10 |
| opencode-go | 0 | 0 | 0 | 0 | 0 |
- scored n = 20; correct = 20; accuracy 1.000; excluded = none (line 362 `"excluded": []`; all 20 correct cells YES).
- bar 0.80; min scored n 20 (line 342); per-target min on-target n 10 (lines 344–345).
- Internal checks: every chain's last "N/leg OK 200" equals its GT cell (awk, 20/20); table prediction sequence diff-equals run-2 `prediction` records (empty diff after T01→T1 normalisation).
- Header tells corroborate GT fingerprints: 10/10 hyper rows server:google-frontend; 10/10 atp rows server:istio-envoy (lines 139–257). Corroboration of the recorded response, not independent GT.

## Stored verdict lines (path:line)
- 342: ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS
- 344: TARGET hyper: on-target GT n=10, correct 10/10 = 1.000 (bar 0.80, min on-target n 10) -> PASS
- 345: TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL
- No BODY / STREAM TARGET verdict lines exist in the file (grep -ic 'stream target|body target' = 0).
- Block A verdicts (not counted by P1, for contrast): 290 ACCURACY 20/20 PASS; 292 TARGET hyper 9/9 -> FAIL (n<10); 293 TARGET opencode-go 0/0 -> FAIL.

## Trial ids + request timestamps (for cross-file duplication checks; 2026-10-16Z)
Block B (authoritative): T01 11:53:41.144, T02 11:53:46.303, T03 11:53:50.172, T04 11:53:55.557, T05 11:53:59.453, T06 11:54:04.680, T07 11:54:08.510, T08 11:54:13.474, T09 11:54:17.323, T10 11:54:22.360,
T11 11:54:26.264, T12 11:54:31.668, T13 11:54:35.528, T14 11:54:41.128, T15 11:54:44.942, T16 11:54:49.821, T17 11:54:53.913, T18 11:54:58.890, T19 11:55:02.734, T20 11:55:07.542.
Block A: T01 11:50:06.945, T02 11:50:12.437, T03 11:50:16.398, T04 11:50:36.396, T05 11:50:40.241, T06 11:50:45.370, T07 11:50:49.261, T08 11:50:54.697, T09 11:50:58.539, T10 11:51:03.833, T11 11:51:07.691, T12 11:51:12.500, T13 11:51:16.372, T14 11:51:20.993, T15 11:51:24.887, T16 11:51:30.692, T17 11:51:34.559, T18 11:51:39.631, T19 11:51:43.560, T20 11:51:49.176.

## Duplication / provenance findings
- None of block B's 20 stamps appears in attrib-r22-legs-hyper.log or attrib-r22-opencode-trials.log (per-stamp `grep -l` = 0 other hits).
- However block B's table is identical (T, class, prediction, GT, chain, correct) to attrib-r22-opencode-trials.log:210-231 (diff empty); that file's trials ran 11:50:45.244–11:52:12.302Z. Under P1's literal dedup clause ("same trial ids, predictions, GT, chains") this is ONE sample; under request provenance they are distinct request sets. Both facts stated; the dedup call belongs to the calibration seat.
- attrib-r22-legs-hyper.log has 0 scoring blocks: trial-only, 20 trials, 11:50:58.065Z–11:52:26.186Z.
- Block B GT is a journal join, not recoverable from this file: window 11:53:36–11:55:37Z reports request-lines=37, leg-rids=36 against 20 trials (line 314); addendum 415–434 declares rid-level provenance MIXED (twin traffic).
- P1-rule consequences (pre-registered rule, not my computation): accuracy n=20 ≥ power ask 17 -> interval PASS possible; TARGET hyper n=10 < 17 -> point PASS cannot be interval PASS; TARGET opencode-go n=0 -> UNTESTED, the stored FAIL is a point-rule artifact.

VERDICT: Block B (line 312) is authoritative — 20 rows, GT×pred confusion diagonal 10 hyper + 10 alibaba-token-plan, 0 errors, 0 exclusions, bar 0.80, min n 20/10; stored verdicts 342 PASS, 344 PASS, 345 FAIL(n=0); no BODY/STREAM verdicts; block B's table duplicates attrib-r22-opencode-trials.log's sample.
Installs: none.
