# R44ConnClaims — cross-document drift report (wave, round 44)

Seat: connector. Scope: compare the frozen claims (`plans/round-44-claims.md`), the counters' docstrings
(`plans/round44_c1_verify.py`, `plans/round44_c2_verify.py`), `claims/frozen-digests.txt`, the SCORECARD
`### Planned (round 44)` block, and this wave's context, for contradictions in mutant counts, case counts, row
ids, predicates and envelope wording. Nothing was written outside this report; all runs below are read-only
(fetch/hash/grep), so no envelope was required.

## 0. Consistency verified first (no drift found in these)

- Frozen artifacts match their pins. `sha256sum` of the 12 files listed in `claims/frozen-digests.txt` equals the
  pins exactly (claims `9ab0f035…`, C1 counter `6cf05323…`, C2 counter `334ce2da…`, probe `0e7a59da…`,
  spec `1f31cf40…`, gate `ea638822…`, anchor `11bb2cad…`, order `948d5e1d…`, dry table `07f1d0df…`,
  witness `f3855ae1…`, envelope `2a484c28…`, SHA256SUMS `9ecc3aeb…`).
- Envelope: `cmp claims/envelope.sh .ufo/waves/round-43/claims/envelope.sh` → identical, so the claims'
  "round-43 envelope unchanged" (claims:25) holds; envelope.sh implements home read-only, ~/.cache overlay,
  `date +%T` start/end, PATH-dir digest, exit 4 + `measurement INVALID` on change (envelope.sh:14-28).
- Commit anchors exist with matching messages: `5f16ed0` freeze, `45dc0bc` first recorded probe run,
  `0cb2e22` baseline spot-check (`git log`).
- C1 counts/predicate: claims:47-50 and counter docstring (c1:10-15) state the same frozen predicate;
  witness-run.txt shows `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`,
  `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, all kills `value=differs`; nothing control shows `fixtures=0`
  `killed=0 survived=5` exit 1; standing batteries (71 fixtures, incl. b42/b43 modules) `killed=0 survived=5`;
  no-mutants, span-forced (`unattributed=5`), site-equal-forced (`unattributed=5`), tool-edited (`PINS
  mismatched=1`), mislabel restore (`SURVIVED exhibits=0>1,rc-mirror`) and hostile f1–f6 (SETUP refusals, exit
  2; f4 round-43 hang exit 124 at 60 s) all reproduce the claims' descriptions (claims:51-59).
- C2 counts/predicate: claims:92-93 and counter docstring (c2:8-10) match `checks=11 defects=0` /
  `PREDICATE C2 pass`; nothing control shows `checks=11 defects=8` exit 1; receipt has 14 cases,
  `observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`; dry table `predicted_pass=8
  predicted_fail=6`; stage-check `cases=14 failed=0`; predictor control `states=48` 24/24 with 24/12/18
  disagreements and substring ok (claims:94-97).
- Row ids: spec rows S138–S146 (9) map to the nine upstream paths and digests that equal the capture manifest;
  C2 `CAPTURES` has the eleven files incl. feal.c + gitignore; V1/V3 logic matches.
- Grader facts vs captures: 100 decimal constants span `test_outputs.py:4-103` (first on line 4, last on 103);
  `:120` `data = open("/app/plaintexts.txt").read()`; `:121-122` `for c in soln.split(): assert c in data`;
  `gen.py:18-28`/`:57-62` derive plaintexts as `sha256(seed_hash + counter_bytes)[:8]` with counters 32-131;
  `test.sh` reward goes to `reward.txt` on pytest exit (`:25-29`); `instruction.md` names no output format.
- Frontier math: R43ConsiderThese.md:27 has 9/89 tasks read (10%); claims' "10 of 89" (claims:78) is the
  post-admission expectation (+1 F1 task), consistent.

## 1. Drifts (each with both locations)

### drift-1 — C1 fence inventory: SCORECARD lists four, claims/counter freeze six
Location A: `SCORECARD.md:1901-1904` (Planned round 44, Calibration) names the re-freeze fence set as F1–F4:
"`rev-parse --absolute-git-dir` inside d and no `.git` FILE (R43SentinelCounter F1), no depth cap (F2), leg i …
(F3, R43CritC1Counter V2′), timeouts on parent-side git calls (F4)".
Location B: `plans/round-44-claims.md:43-46` and `plans/round44_c1_verify.py:17-27` define F1–F6, adding F5
(`core.worktree --local --no-includes`, any include refused, `objects/info/alternates` refused) and F6
(`GIT_CEILING_DIRECTORIES` at the fixture parent + `--lane` discovery must live inside d). Counter code
implements F5/F6 (`repo_breach`, `lane_breach`, c1:475-594). Same subject, different inventories.

### drift-2 — Round-43 R5's carried items vs round-44 R5 closure scope
Location A: `corpus/lessons/round-43-verifier-spotcheck.md:169-171` (§5 R5) carries forward "counter fences
F1–F4 and V2′, 7/15 C1 guards and 7/13 V9/V10 guards that survived mutation, and the envelope's mode-only blind
spot (R43ReviewEnvelope)".
Location B: `plans/round-44-claims.md:119-121` (closure R5) states only "V11 above; fences F1–F6 in C1;
mutation results of round 43 carried". The guard inventories (7/15, 7/13) and the envelope blind spot are
absent, and the envelope is byte-unchanged (drift-1/verified above), so the blind-spot item is neither carried
nor disclosed as deferred.

### drift-3 — SCORECARD routed slate missing from claims' routed section
Location A: `SCORECARD.md:1915-1917` (Routed) lists for round 44: "envelope v2 (mode bits, unreadable entries —
R43ReviewEnvelope); R43MutC2Counter 7 surviving V9/V10 guards; README lessons index parity (33 rows for 60
lesson files) and round-41/42 evidence sections".
Location B: `plans/round-44-claims.md:114-121` (Frontier step and routed work) covers only R1–R5 and
considerthese; none of the four scorecard items appears or is disclosed as deferred.

### drift-4 — gen.py deletion line citation off by one vs the pinned Dockerfile
Location A: wave context (this assignment) says "gen.py is deleted from the image (Dockerfile:12-13)".
Location B: pinned capture `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/Dockerfile`: line 12 is blank,
line 13 `RUN rm orig_plaintexts.txt`, line 14 `RUN rm gen.py` — the gen.py removal is at `:14`, not `:12-13`.
(Related nit: "test.sh:22-26 rewards pytest's exit status": pytest invocation spans `:18-22`, the reward write is
at `:25-29`.)

### drift-5 — R43PlanNext price-table line citations vs the frozen counter's adv cells
Location A: `.ufo/waves/round-43/build/R43PlanNext.md` §B.1 rows 7 and 9 cite the advertised sentences at
anchor tool lines 99-100 ("twin captures not a defect") and 106-108 ("lessons from work tree").
Location B: `plans/round44_c1_verify.py:241-250` quotes the same sentences at `anchor_digest_check.py:98-99`
and `:106-107`; the actual text spans 98-99 and 106-107 (verified in the tool), so the pricing table is one
line ahead on U7 and one line beyond on U9.

### drift-6 — "gen.py:12 prints the four round keys" wording vs the capture
Location A: receipt `corpus/evidence/round44/feal-linear-probe.txt:11` (`./decrypt … with the four round keys
printed in the public gen.py:12`) and the probe's case predictions.
Location B: `gen.py:12` only defines the list `keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]`; nothing
in gen.py prints the keys (they are CLI arguments). Wording nit, not a count error.

## 2. Notes (planned-vs-executed, not counted as drift)

- SCORECARD's "one probe shape" for a pinned task (scorecard:1909-1911) became the frozen 14-case probe
  (claims:82-86) — an expansion, not a contradiction.
- The scorecard's C2 "content leg" example (blind non-author mechanism table) was implemented as V11's held-out
  predictor with red copycat controls (claims:88-97) — the planned direction, differently mechanized.

VERDICT: drift-6
