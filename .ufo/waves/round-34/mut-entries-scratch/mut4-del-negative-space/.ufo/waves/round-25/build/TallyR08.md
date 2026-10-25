# TallyR08 — hand-tally: `corpus/evidence/attrib-r23-stream-trials.log`
Read-only C1 oracle; `grep`/`sed`/`awk` only (no python, no lane scripts, no network). sha256 `5ce762aa27fc42489510b2d6cc4aaef184dcb0ba6df1a0e4329e7d75ce2112fb` = HEAD blob (`git cat-file -p HEAD:corpus/evidence/attrib-r23-stream-trials.log | sha256sum`, HEAD `3f371d2`); 481 lines, 44 records, 2 metas.
## 1. `## GT + scoring at close` blocks: NONE (trial-only)
`grep -c 'GT + scoring'`=0; `AUTHORITATIVE`=0; `^\| T[0-9]+`=0; `"gt"|"gt_class"|"correct"|"chain"`=0; `^(ACCURACY|TARGET|BODY|STREAM TARGET)` → rc=1. Sole `scoring` token is prose `:476`.
⇒ blocks 0; authoritative block none; confusion table (rows=GT leg) not derivable; scored n=0; correct n/a; excluded none; stored ACCURACY/TARGET/BODY/STREAM TARGET lines none. **P1 contribution of this file = 0 scored trials.**
Owed, not lost: `:232` "score phase appends below AFTER all trials"; `:223-226` §F owes "Journal GT for the 14 rids"; `:476` scoring "must still state the mixed join".
## 2. Inventory (two appended blind runs, no GT)
A `:1-109`: 14 trials, headers `:11-102`, records `:17-108`, done `:109` (n=14, last_request_utc 13:39:45Z); classes insp 5 / insplong 5 / std 2 / marker 2; meta `:10` frozen `77b8d4a0…` (r22 v2), instrument `bb6bd919…` (`:5`).
B `:227-418`: 30 trials, headers `:235-412`, records `:241-417`, done `:418` (n=30, bodies hint 3 / inspection 24 / marker 3, last_request_utc 13:49:04Z); classes `stream-stream-*` (double prefix is in the bytes; `:457-459` calls it cosmetic at `plans/attrib_probe.py:802/823`); meta `:234` frozen `1b2d6a01…` (r23 v3), instrument `cce53a16…` (`:229`).
Count **44** (14+30); first request `2026-10-16T13:38:14.075Z` (`:11` A/T01), last trial t0 `13:49:00.941Z` (`:412` B/T30), completion stamp 13:49:04Z; predictions hyper 34 / alibaba 10; `trial_id` is no key: ids 1-14 occur twice (14 duplicate ids in-file).
## 3. Trial ids + request timestamps (all `2026-10-16Z`)
A `:11-102`:
`T01=13:38:14.075Z T02=13:38:19.771Z T03=13:38:25.797Z T04=13:38:29.700Z T05=13:38:33.832Z T06=13:38:39.455Z T07=13:38:50.850Z T08=13:38:54.751Z`
`T09=13:38:58.812Z T10=13:39:04.601Z T11=13:39:15.664Z T12=13:39:21.052Z T13=13:39:31.365Z T14=13:39:36.770Z`
B `:235-412`:
`T01=13:46:18.559Z T02=13:46:23.357Z T03=13:46:30.154Z T04=13:46:34.248Z T05=13:46:38.100Z T06=13:46:44.641Z T07=13:46:48.557Z T08=13:46:52.702Z`
`T09=13:47:00.220Z T10=13:47:04.462Z T11=13:47:10.543Z T12=13:47:17.490Z T13=13:47:23.620Z T14=13:47:29.290Z T15=13:47:35.521Z T16=13:47:40.799Z`
`T17=13:47:46.767Z T18=13:47:52.189Z T19=13:47:58.277Z T20=13:48:03.469Z T21=13:48:09.224Z T22=13:48:14.844Z T23=13:48:20.489Z T24=13:48:26.211Z`
`T25=13:48:31.706Z T26=13:48:38.010Z T27=13:48:43.670Z T28=13:48:49.436Z T29=13:48:55.154Z T30=13:49:00.941Z`
## 4. Cross-file duplication
0/44 t0 values occur in any other P1 file (`comm -12` on unique `t0_utc` sets per file; `attrib-r23-stream.log shared_t0=0`, `attrib-r22-opencode-trials.log shared_t0=0`).
B twins the scored run in `attrib-r23-stream.log` (`:194-257`, `:258-321`; last = authoritative under P1; t0 13:46:41.501-13:49:24.572): identical (trial_id,class,prediction) **30/30** after zero-pad normalisation, GT {hyper 24, alibaba 6}, both sibling blocks' verdicts identical (`ACCURACY 30/30 … PASS`, `STREAM TARGET opencode-go 0/0 … FAIL`) → sibling's 2 blocks = 1 sample.
Do NOT transplant that GT by id: `:460-478` §I records min |t0 gap| **0.07 s** and a **MIXED** rid-level join. P1's identical-table rule ⇒ the 30-trial protocol is ≤1 sample; its scored instance is the sibling, not this file.
A's 14 trials have no GT in P1 (sibling journal window starts `@1792158396` = 13:46:36Z) → UNTESTED, not excluded.
## 5. Verdict-like lines present (landing counts, not interval verdicts)
`:180` bar 0.80 cited once; **no min-n in this file**. `:179-190` ">=10 on-target (bar 0.80)" → NOT MET / NOT-RUN-with-reason; `:446` on-target 0/24; `:451-452` 0/34; `:226` same. None is a fraction carrying a CP verdict.
## 6. GT-free checks
Per-record `hdr_tells` → landing: `server:google-frontend`→hyper 34, `server:istio-envoy`→alibaba 10; predicted × header-inferred diagonal 44/44:
| predicted \ hdr-inferred | hyper | alibaba |
|---|---|---|
| hyper (34) | 34 | 0 |
| alibaba-token-plan (10) | 0 | 10 |
Reproduces §C `:157-163`/§H `:440-443`; self-agreement with the tell map, **not** accuracy (no GT). A: header `blind_prediction` == record `prediction` 14/14 (paste/awk). §H denominator 10+24=34 ✓.
## 7. Consequences for `plans/attrib_calibration.py`
1. `parse_receipt` → **0 blocks** here; never synthesise rows from §C/§H prose.
2. Dedup key needs file+run+t0 (`trial_id` collides 14× in-file, 30× with the sibling).
3. Run B's `stream-stream-*` tokens defeat exact `stream-inspection` filters (24 missed).
4. Bar 0.80 but no min-n; sibling-local min 20 / on-target 10; P1 power ask n≥17 — use P1's rule.
VERDICT: trial-only — 0 `## GT + scoring at close` blocks, 0 scored rows, 44 unscored blind trials (14+30) from 2026-10-16T13:38:14.075Z to 13:49:00.941Z; P1 contribution 0 scored trials; its run-B table duplicates the sibling's scored protocol (one sample there); the §F GT append never landed. Installs: none.
