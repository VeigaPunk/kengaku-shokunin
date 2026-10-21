# AwkOracleExec — r25 C1 cross-check oracle (writer; novelty → coverage)

Clone `/tmp/kengaku-r25-AwkOracleExec`, branch `r25-AwkOracleExec`, observed base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a` (from `git switch -c … 3f371d2 && git rev-parse HEAD`). Receipts are byte-identical to master `6180e4fb92e9`: `git diff --stat 6180e4fb92e9 3f371d2 -- 'corpus/evidence/attrib-r2*'` printed nothing. Nothing committed.
**File changed:** `plans/fixtures/r25/attrib_oracle.sh` (new, 100755, 463 lines). POSIX sh + awk; no python, no network. Per file it takes the LAST `## GT + scoring at close` block and re-derives every stored line from that block's own rows (`GT counts`, `ACCURACY`, `TARGET`, `BODY`, `STREAM TARGET`, `score_summary` JSON); each disagreement prints `MISMATCH`. Duplicates are detected by `table_md5` and `key_md5` (key = sorted trial/prediction/GT/chain). Modes: `--intervals` (CP/Wilson/verdict/Rogan–Gladen, arithmetic only), `--cp-table N`, `FILE...`, `--root DIR`. Exit 0/1/2 as in the python CLI.

## Output: `sh plans/fixtures/r25/attrib_oracle.sh` (cwd = clone) → exit 0
```
# attrib_oracle files=9 block=LAST '## GT + scoring at close' md5=md5sum root=/tmp/kengaku-r25-AwkOracleExec
corpus/evidence/attrib-r21-ds-trials.log blocks=0 trial-only trials=20 scored=0 correct=0
corpus/evidence/attrib-r21-glm-trials.log blocks=0 trial-only trials=22 scored=0 correct=0
corpus/evidence/attrib-r21-impl-ds-trials.log blocks=4 prior=130:diff,176:diff,222:diff last=268-313 trials=20 rows=20 excl=0 scored=20 correct=20 gt[alibaba-token-plan=20/20] pred[alibaba-token-plan=20] table_md5=43a1f91b8e91200a5e8f4d9964119d65 key_md5=76e6b765d65b4cbb29244becf68f6755 unit=ds-flash-shim win=1792146059-1792146169 win_req=20 extra_req=0 read_lag_s=252 summary_verdict=PASS(accuracy) checks=4/4
corpus/evidence/attrib-r21-impl-glm-trials.log blocks=1 last=142-189 trials=22 rows=22 excl=0 scored=22 correct=22 gt[devin=9/9,zai=13/13] pred[devin=9,zai=13] table_md5=9698cce1077b985bbe75adae821b4bd4 key_md5=61c7f3237ccb87ac56217ae4dbc5715c unit=glm-flash-shim win=1792146147-1792146311 win_req=99 extra_req=77 read_lag_s=112 summary_verdict=PASS(accuracy) checks=4/4
corpus/evidence/attrib-r22-legs-hyper.log blocks=0 trial-only trials=20 scored=0 correct=0
corpus/evidence/attrib-r22-legs.log blocks=2 prior=260:diff last=312-363 trials=40 rows=20 excl=0 scored=20 correct=20 gt[alibaba-token-plan=10/10,hyper=10/10] pred[alibaba-token-plan=10,hyper=10] table_md5=71b4c55bc128a2b379a8269699aafee9 key_md5=ef6b7f498641864bbf961713f1d773f5 unit=ds-flash-shim win=1792151616-1792151737 win_req=37 extra_req=17 read_lag_s=122 summary_verdict=PASS(accuracy) checks=6/6
corpus/evidence/attrib-r22-opencode-trials.log blocks=1 last=204-255 trials=20 rows=20 excl=0 scored=20 correct=20 gt[alibaba-token-plan=10/10,hyper=10/10] pred[alibaba-token-plan=10,hyper=10] table_md5=71b4c55bc128a2b379a8269699aafee9 key_md5=ef6b7f498641864bbf961713f1d773f5 unit=ds-flash-shim win=1792151440-1792151562 win_req=68 extra_req=48 read_lag_s=-19 summary_verdict=PASS(accuracy) checks=6/6
corpus/evidence/attrib-r23-stream-trials.log blocks=0 trial-only trials=44 scored=0 correct=0
corpus/evidence/attrib-r23-stream.log blocks=2 prior=194:same last=258-321 trials=30 rows=30 excl=0 scored=30 correct=30 gt[alibaba-token-plan=6/6,hyper=24/24] pred[alibaba-token-plan=6,hyper=24] table_md5=d7782e4c14ffa63f2addd1a4d1e2fbd6 key_md5=0c323f60dad963b7e089a10c009fcf9a unit=ds-flash-shim win=1792158396-1792158594 win_req=160 extra_req=130 read_lag_s=82 summary_verdict=FAIL(stream-target) checks=8/8
DUP key_md5=ef6b7f498641864bbf961713f1d773f5 keep=corpus/evidence/attrib-r22-opencode-trials.log dup=corpus/evidence/attrib-r22-legs.log table_md5_equal=yes journal_windows=disjoint ablations_equal=no
OVERLAP none (no two last blocks share a unit and a journal window)
TOTAL files=9 with_block=5 trial_only=4 scored=112 correct=112 unique_samples=4 dedup_scored=92 dedup_correct=92 files_with_mismatch=0
```
`--intervals` → exit 0, 43 lines (the 13 above plus per-estimate lines). Excerpt:
```
# cp_selfcheck=ok max_abs_err=3.1e-16 lo(16/16)=0.794093 lo(17/17)=0.804936
  reverdict TARGET:hyper 10/10 cp=[0.6915,1.0000] wilson=[0.7225,1.0000] -> INDETERMINATE | stored point=PASS
VERDICTS(dedup) acc: PASS=4 FAIL=0 INDETERMINATE=0 UNTESTED=0
VERDICTS(dedup) stored: PASS=4 FAIL=0 INDETERMINATE=1 UNTESTED=2
VERDICTS(dedup) recall: PASS=2 FAIL=0 INDETERMINATE=5 UNTESTED=5
VERDICTS(dedup) spec: PASS=6 FAIL=0 INDETERMINATE=5 UNTESTED=1
```

## Findings (receipt paths under `corpus/evidence/`)
1. **Stored lines:** all 28 match their rows (4+4+6+6+8). No `correct` cell disagrees with prediction==GT. **P5 false:** 112/112 scored rows are correct.
2. **P1 true:** stored `TARGET hyper 10/10 -> PASS` (`attrib-r22-legs.log:344`, `attrib-r22-opencode-trials.log:236`) re-verdicts INDETERMINATE (CP lower 0.6915). **P3 true:** dedup accuracy 4/4 PASS (CP lower 0.8316/0.8456/0.8316/0.8843). **P4 true:** 5 recalls INDETERMINATE (e.g. glm devin 9/9 → [0.6637, 1]).
3. **P2 fires on the frozen key, but the two r22 blocks are distinct runs.** `key_md5` and `table_md5` are equal (`legs:318-339` = `opencode:210-231`). The journal windows are disjoint (`legs:313` vs `opencode:205`), and `loo:hdr_tells` differs (19/20 at `legs:349`, 18/20 at `opencode:241`). Dedup takes n from 112 to 92. A different parser reproduces DupR22Scout.
4. **One r23 block stores two conflicting verdicts.** `attrib-r23-stream.log:298` `ACCURACY … -> PASS`, but the JSON verdict at `:320` is `FAIL`, which equals `STREAM TARGET` at `:303` (instrument `489f938a`, `:262`). Block `:194` has an identical table (`prior=194:same`) and JSON `PASS` (`:256`). The python instrument must name which one it re-verdicts; the oracle re-verdicts both (PASS; 0/0 UNTESTED).
5. **Other traffic in GT windows.** Journal request lines exceed table rows in 4 of 5 blocks: glm 99/22 (`:144`), legs 37/20 (`:314`), opencode 68/20 (`:206`), r23 160/30 (`:260`). Only `attrib-r21-impl-ds-trials.log:270` is 20/20.
6. **Journal read before the window closed.** Opencode was read 19 s before `--until` (`:204` 11:52:23Z vs `:205` @1792151562 = 11:52:42Z). r23's two reads of one window differ, 152 vs 160 request-lines (`:196` vs `:260`), because block 1 was read at 13:49:42Z, before `--until` at 13:49:54Z. [That end time is derived as 13:51:16Z minus read_lag_s 82.]
7. **Power ask:** 0.025^(1/16) = 0.794093, which prints 0.7941 at 4 dp; `round-25-claims.md:43` prints 0.7940 (truncated). The n=17 threshold 0.804936 stands.
8. **Leg universe:** legs that appear only as `scores=` keys (`src=s`) give recall UNTESTED and spec PASS (e.g. glm hyper 22/22). The python must use the same universe, or the spec tallies diverge.

## Verification exercised
- **3 toolchains × 3 modes, byte-identical output:** GNU Awk 5.4.1 under `/bin/sh`→bash; `gawk --posix` under `bash --posix`; the existing BusyBox v1.36.1 `ash`+`awk` (no libm), `/usr/lib/initcpio/busybox`.
- **CP values:** `--cp-table 40` matches `/tmp/kengaku-r25-CpReferenceExec/plans/fixtures/r25/cp_reference.tsv` byte for byte (862 lines, max |Δ| 0 at 12 dp).
- **Sibling fixtures** (`/tmp/kengaku-r25-CalibSelftestExec/plans/fixtures/r25/attrib-cal/`, read-only) all match `EXPECTED.tsv`: gt-flip exit 1 (3 MISMATCH, 19/20 INDETERMINATE); duplicate-block `prior=2:same`, 16/16 INDETERMINATE; n16 INDETERMINATE; n17 PASS; n0 UNTESTED; upper-below-bar FAIL [0, 0.1951].
- **Red runs on copied receipts** (`/tmp/awkoracle-red`): a byte-copy of r23 gives `DUP journal_windows=identical ablations_equal=yes` with dedup_scored still 92. Flipping one GT cell (opencode T07, line 218) gives exit 1 with 5 MISMATCH: rows, GT_counts, ACCURACY, TARGET:hyper, score_summary.
- **table_md5 by a second route:** `sed -n '268,313p' corpus/evidence/attrib-r21-impl-ds-trials.log | grep '^|' | md5sum` → `43a1f91b…`; r23 `258,321` → `d7782e4c…`.

## Risks / for L1
- **My dedup choice:** "keep" = earliest journal `--since`; the frozen rule names none. Totals do not depend on it.
- **Possible key collision:** chains are truncated to 80 chars (`attrib_probe.py:999`), so two chains sharing that prefix would share `key_md5`.
- **ACCURACY k is re-scored, not counted:** it comes from `attrib_probe.py:965-973`. It equals the prediction-column count in all 5 blocks today; any future divergence will show as a MISMATCH by design.
- **Possible index refresh:** one `git status --short` in the live lane, run read-only, may have refreshed the Git index stat cache (no `GIT_OPTIONAL_LOCKS=0`). No other live-lane action besides writing this report.
- **Suggested checks:** compare `sh plans/fixtures/r25/attrib_oracle.sh --intervals` with `python3 plans/attrib_calibration.py --json`, and diff `--cp-table 40` against the python CP values.

VERDICT: Oracle landed and run. All 28 stored lines match their rows. P1, P3 and P4 are true; P5 is false. P2 fires on the frozen key, but the two r22 blocks are distinct runs (disjoint journal windows, different ablations). Interval values agree exactly with the reference CP table and across three toolchains.
Installs: none (gawk 5.4.1 and BusyBox 1.36.1 were already present; no pacman/uv/npm).
