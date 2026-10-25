# PointVerdictScout — statements resting on a point attribution verdict (r25 inventory, read-only)

Population: SCORECARD.md, LOG.md, corpus/knowledge/*.md (9 mention "attrib"; 2 carry verdicts — attrib-r21.md, probe-battery-r19.md; attrib-prior-art-r21.md is bar-only), plans/attrib-r2[123]-frozen.md. Paths relative to /home/vgpnk/Projects/shokunin/kengaku-shokunin. `n` = trials behind the stored verdict at that line; `bar` = threshold stored there or in the receipt line it quotes; "min" = stored min-n gate. No verdict recomputed or judged; no network; no external source opened (frontier: none this round).

## A. r21 overall accuracy — bar 0.80, min scored n 20
- A1 SCORECARD.md:496-498 · LOG.md:172-173 · corpus/knowledge/attrib-r21.md:56-58 — "**100% accuracy both shims** — ds 20/20 (GT: alibaba 20), glm 22/22"; "both PASS (bar 0.80, min scored n 20)" · n=20/22 · bar 0.80/min 20
- A2 corpus/knowledge/attrib-r21.md:133,143,167 · plans/attrib-r21-frozen.md:279 — "ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS"; "22/22 = 1.000 … -> PASS"; "the 1.000 PASS is a two-leg accuracy" · n=20/22 · bar 0.80/min 20
- A3 corpus/knowledge/attrib-r21.md:139-140,154,156 — "Wilson 95% CI on 20/20: [0.839, 1.000]"; "22/22: [0.851, 1.000]"; "42/42 = 1.000, Wilson [0.916, 1.000] — a summary, not an independent n" · n=20/22; 42 pooled · no bar (interval, Wilson not CP)
- A4 corpus/knowledge/attrib-r21.md:166-167,387 · corpus/knowledge/probe-battery-r19.md:630-632 — "`18/18 = 1.000 FAIL` … refused the shrunken denominator (min scored n 20)"; "`20/20 = 1.000 PASS`" · n=18 / 20 · bar 0.80/min 20
- A5 plans/attrib-r21-frozen.md:255-256,267-268 — "20/20 EXCLUDED:UNMATCHED -> ACCURACY 0/0 FAIL"; "matched 22/22"; "the impl-ds FAIL is an instrument-clock defect" · n=0 / 22 · bar 0.80/min 20
- A6 corpus/knowledge/attrib-r21.md:373-377 — "n = 20 and 22 … **3 of the 5 roster legs were exercised at all**, and the 0.80 bar was met on the 3 that served" · n=20/22; per-leg 20/13/9/0/0 · bar 0.80
- A7 corpus/knowledge/attrib-r21.md:39 · plans/attrib-r21-frozen.md:8-10,33 — claim "over >=20 blind trials per shim at accuracy >= the frozen bar (0.80)"; machine `"bar": {"min": 0.8, "min_scored_trials_per_shim": 20}` · n planned 20+2 · bar 0.80/min 20
- A8 SCORECARD.md:509-510,514-515,610 — novelty "**improved** … blind leg attribution validated against operator-journal GT"; coverage "**improved narrowly** (hyper/opencode-go legs UNTESTED — 0 GT trials)"; "r21 \"improved\" verdict … verdict-only, unconverted" · derived from A1/A6 · bar 0.80 (derived)

## B. r21 ablations — descriptive, no stored bar
- B1 SCORECARD.md:499-500 · LOG.md:174 · corpus/knowledge/attrib-r21.md:67-68,186-190 — "all 11 frozen ablations … at 1.000"; "11/11 ablations"; "1.000 on both shims (20/20 ds, 22/22 glm, receipt-verbatim)" · n=20/22 per arm · no bar

## C. r22 hyper — bar 0.80, min on-target n 10
- C1 SCORECARD.md:533,541 · LOG.md:188-189 · corpus/knowledge/attrib-r21.md:463 — "hyper **COVERED** (run-2: 10/10 on-target = 1.000, bar 0.80)"; "hyper validated" · n=10 · bar 0.80/min 10
- C2 corpus/knowledge/attrib-r21.md:463 — "Run-1 was 9/9 on-target but n<10, so run-2 closed the count" · n=9 · bar 0.80/min 10 (stored FAIL by min-n)
- C3 plans/attrib-r22-frozen.md:286-288 — "hyper 19/19 = 1.000 across both runs (>=10 bar MET in run-2: 10/10 PASS); opencode-go 1/1 … n=1, far below the >=10 bar" · n=19 / 10 / 1 · bar 0.80/min 10
- C4 plans/attrib-r22-frozen.md:305-309 — "run-1 ACCURACY 20/20 = 1.000 PASS … run-2 … TARGET hyper 10/10 -> PASS"; "hdr_tells LOO 17/20 … and 19/20"; "header-strip mimicry 19/20 and 20/20" · n=20/20/10; 20 · bar 0.80/min 20 shim + min 10 target
- C5 plans/attrib-r22-frozen.md:9-11,51,182 — "accuracy vs the 0.80 bar"; "per-target verdicts need >=10 on-target GT trials each at accuracy >= 0.80"; machine min 0.8/min 20 · n planned 10+10 · bar 0.80/min 10 target, min 20 shim
- C6 plans/attrib-r22-frozen.md:302 · corpus/knowledge/attrib-r21.md:476-477 — "greedy in-order assignment disambiguated … (40/40 chain-consistent)"; "`hdr_tells` LOO 17/20 and 19/20 … header-strip … 19/20 and 20/20" · n=40 joins / 20 · no accuracy bar (join audit, descriptive)

## D. r23 stream — bar 0.80, min scored n 20; target min 10
- D1 SCORECARD.md:574 · LOG.md:215 · corpus/knowledge/attrib-r21.md:522,545-547 — "30/30 = 1.000 over GT `{"alibaba-token-plan": 6, "hyper": 24}`"; "ACCURACY: 30/30 = 1.000 … -> PASS" · n=30 · bar 0.80/min 20 (receipt attrib-r23-stream.log:234)
- D2 corpus/knowledge/attrib-r21.md:545,551-554 — "14/14 = 1.000 … -> FAIL — the FAIL is the frozen shim-level bar's **min-n 20**" · n=14 · bar 0.80/min 20
- D3 corpus/knowledge/attrib-r21.md:549 — "combined main receipt (b1+b2) … 44/44 = 1.000 … Wilson [0.920, 1.000]" · n=44 · no bar restated
- D4 corpus/knowledge/attrib-r21.md:546-547,557-563,620 — batch-2 impl and twin "30/30 = 1.000"; "same-class twins are GT-equivalent here" · n=30 ×2 (duplicate sample) · bar 0.80/min 20
- D5 corpus/knowledge/attrib-r21.md:522,590-593 — "`stream-inspection` arm landed **hyper 24/24**"; "r22 stream:false: 10/10 … r23 stream:true: 24/24"; "alibaba — +10 stream-mode natural trials at 1.000" · n=24 / 10 / 10 · bar 0.80/min 10 for hyper; none for alibaba
- D6 SCORECARD.md:573,576 · LOG.md:215,224-225 · corpus/knowledge/attrib-r21.md:526 — "on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL"; "(30/30) stands as a characterization"; "NOT-ADMITTED" · n=0 / 30 · bar 0.80/min 10
- D7 plans/attrib-r23-frozen.md:9,39,166,191 — claim "scored against the 0.80 bar"; "the r23 verdict needs >=10 on-target opencode-go GT trials at accuracy >= 0.80"; clause "NOT met" rule; machine min 0.8/min 20 · n planned 30 · bar 0.80/min 10 target, min 20 shim
- D8 corpus/knowledge/attrib-r21.md:563,575 — "`loo:hdr_tells` **14/30 = 0.467**"; "LOO 10/14, 14/30" · n=30 / 14 · no bar (descriptive)
- D9 corpus/knowledge/probe-battery-r19.md:633-635,664-665 — "Bar accuracy ≥ 0.80 against journal GT, per shim … (r21: hyper / opencode-go — the honest boundary of the 1.000)"; "passing the bar on forced trials validates the feature table against that leg's serve path, not discrimination under natural traffic" · n/a · bar 0.80

## E. Interval-sensitive register (mechanical; not adjudicated)
- Point PASS with n<17 (pre-registration power ask, plans/round-25-claims.md): C1/C3 run-2 10/10, C2 9/9, C3 opencode 1/1, D2 14/14 — "Any point PASS with n < 17 cannot be an interval PASS".
- Stored FAIL whose printed basis is the min-n gate, not the fraction: A4 18/18 (min 20), C2 9/9 (min 10), C3 1/1 (min 10), D2 14/14 (min 20), D6 0/0 (n=0).
- n=0 stored FAIL → UNTESTED under the frozen n=0 rule: D6 / SCORECARD.md:573.
- n≥17 zero-error PASS unaffected mechanically: A1/A2 20/20 & 22/22, A5 22/22, C3 19/19, C4 20/20, D1 30/30, D3 44/44, D5 24/24; A3 42/42 is pooled across shims and Wilson rows are not CP.

## F. Checked, excluded (no stored point verdict)
- corpus/knowledge/attrib-prior-art-r21.md:21,110,128-130 — bar-only ("frozen bar (80%)"; AdaptPrint 80.6% comparison); no verdict.
- SCORECARD.md:555-556,614 · LOG.md:262 — grader/freeze-check PASS, not attribution accuracy.
- SCORECARD.md:46,329 · probe-battery-r19.md:16,194-201 — critic reproduction / r19 grid tallies.
- SCORECARD.md:574 "table pin `plans/attrib-r23-frozen.md:214`" — FROZEN hash, not a verdict.
- knowledge files with unrelated "attribut*": agent-time-horizon-and-task-validity, bailian-cli-telemetry, bench-arena-fresh-run, bench-arena-round12-ladder, bench-arena-task27-timeout-anatomy, ledger-route-telemetry.

VERDICT: 24 grouped inventory rows (A8+B1+C6+D9) covering every point-attribution-verdict statement in the four assigned file groups; stored bars are uniformly 0.80 with min-n gates (20 shim-scored / 10 per-target); n ranges 0–44; nothing adjudicated. No installs; no network.
