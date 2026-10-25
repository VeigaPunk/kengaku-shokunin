# round-12 integrator notes — L1 adjudications, deltas, corrections

Owner: L1 (kengaku). No L2 wrote a shared file this round; every L2 artifact is
committed verbatim under `corpus/evidence/round12-fleet/`, and this file is the
only place L1's rulings, deltas and corrections are recorded (r10/r11
convention). Where a ruling changes an L2 draft, the draft is **not** edited in
place — the ruling here plus the promoted `recompute_r12.py` / `grader.py`
carry it.

Authority order for round 12: `probe_plan_r12.md` (hashed v1, incl. its §9
pre-hash amendment log) → this file → L2 drafts.

## 0. Round-12 timeline facts (all committed)

| event | UTC | evidence |
|---|---|---|
| design-critic verdict lands (DO-NOT-RUN, 1 FATAL / 5 MAJOR / 4 MINOR) | before any hash existed | `r12-critic-design.md`; plan §6 step 4 note |
| bundle v1 hashed (9 files) | `2026-09-29T01:16:08Z` pre and post | `ordering.log` lines 1–3; `prereg-bundle.sha256` |
| run scripts hashed post-D1-rewrite | `2026-09-29T01:16:08Z` | `ordering.log` lines 4–5 (`probe_r12.py` `1871697f…`, `run_r12.py` `3beb91ea…`) |
| mock smoke (n=2/n2=2, proxy → 127.0.0.1:18114) | first `request_ts` `01:18:02Z` | 142 records exactly as §4 predicts; descriptor model id `mock-r12` in both descriptor records ⇒ zero real-endpoint traffic |
| real-endpoint smoke (n=1/n2=1) | first `request_ts` `01:18:37Z` | 72 records exactly; served model id = the r11 string; pid 1299, 41 argv tokens; 22/22 graded `finish=stop`, 0 parse failures |
| main run launched | `ordering.log` `main-run-launch` line | 416 jobs, 4 000 chat + 2 GET |

## 1. Adjudications of `r12-recompute-notes.md` (§2–§4 ambiguity list)

RATIFIED = the draft's choice stands. OVERRULED = the promoted engine must
change; the reason is the amended plan or a pinned interface.

| id | ruling | reason |
|---|---|---|
| 1a sum-of-ranks vs mean-rank | **RATIFIED** (sum form) | plan §2.3 E1 pins `L = Σ_j (j+1)·R_j` with `R_j` = the arm's rank *sum* |
| 1b tie correction | **RATIFIED**, with a promotion-time numerical check | the permutation-variance derivation must equal §2.3's `5·S²_block` at k=4; the promoted engine carries a selftest asserting both forms agree on a tied block (`(1,2.5,2.5,4)` → per-block var 8.333…) |
| 1c blocks with missing arms | **RATIFIED** (listwise: a pid enters E1 only with final-turn records in all four ladder arms) | keeps Page's blocks complete; matches §2.3's contingency |
| 2a clip epsilon 1e-6 | **RATIFIED** | pinned in plan §2.3 E6 (critic D5) |
| 2b slope before intercept | **RATIFIED** | matches §5's literal `slope=… intercept=…` |
| 3a reliability quintiles, fixed edges, `%.1f-%.1f` labels | **RATIFIED** + empty bin prints `pred=n/a obs=n/a n=0` | plan §5 (critic D8) |
| 3b E6 event count | **RATIFIED at 416** | plan amended (§9 row L1-E6): 5×64 + 2×48 = 416; 448 was an L1 arithmetic slip found independently by ScribeDrafts and ExecutorRecompute |
| 3c error-excluded pids dropped from E6 | **RATIFIED** (uniform family-level listwise deletion, E6 included, dropped from score **and** climatology) | plan §2.3 contingency as amended (critic D6) |
| 4a "shared turns" per arm | **RATIFIED** (the turns participating in that arm's paired contrasts: INC [4,7,10], 4710 [4,7,10], 710 [7,10], CKPT10 [10], MONO [1], T-DENSE [7,10], T-SPARSE [7,10]) + the `Shared-turn sets used:` audit line must print | column 4 only; no verdict depends on it |
| 4b markdown separator row | **RATIFIED** | r11 precedent |
| 4c ack compliance lines | **OVERRULED → exactly 5 lines** in §4 order (`A-CKPT4710-ack`, `A-CKPT710-ack`, `A-CKPT10-ack`, `T-DENSE-ack`, `T-SPARSE-ack`); no `A-INC-ack 0/0 = n/a` row | critic D7 absorbed into plan §5; a 6th row would make the gate's count check ambiguous |
| 4d missing/partial probability file | **OVERRULED in part** — keep `n/a` + the `E6 events: k/n` coverage line as a defensive path, but a coverage shortfall must **fail hard (exit 2)**, not print `UNDERPOWERED-INDETERMINATE` | the three prediction artifacts are inside the hashed bundle with pinned sha256s, so partial coverage means a corrupted tree, not a small sample; the `UNDERPOWERED-INDETERMINATE` label is reserved for the 44/44 error-deletion floors |
| 4e `L` format | **OVERRULED → always `%.1f`** | plan §5 amended to `L=<f.1>` (critic D2); one fixed format keeps the gate regex single-valued |
| 4f `E_L` / `var_L` format | **OVERRULED for `E_L` → `%.1f`**; `var_L` stays `%.3f` | plan §5 amended (`E_L=<f.1> var_L=<f.3>`) |
| 4g census literals | **RATIFIED** (actual counts from the bytes, r11 convention) | the gate recomputes the same census from committed bytes |
| 4h descriptor counting | **OVERRULED → the census line reads `2 descriptors`** (folding `descriptors_end` in), with a separate audit line naming both | plan §5 census line amended to `2 descriptors`; §4 pins exactly two descriptor records |
| 4i POINT-MATCHES placement | **RATIFIED** (same line, appended, with the condition in the rule comment above) — **but with the renamed R2 branch labels** `REPEATS-r11` / `REPEATS-DOWNGRADED` / `DIRECTIONAL` / `DOES-NOT-REPEAT` | plan §2.3 amended (§9 row L1-C2): the prior-art ruling forbids "replication" wording for a same-unit/same-problem/same-seed re-measurement |
| 4j n for the floors + unattributable errors | **RATIFIED** (meta-derived n minus excluded, plus the conservative guard on the primary paired n). Error-record family attribution is pinned: the runner writes `job = [cell, fam, pid]`, so family = `job[1]`, pid = `job[2]`; anything unattributable prints `ERROR RECORD UNATTRIBUTED …` and never drops silently | floors are **44/44** per `power_analysis_r12.md`, not 56/42 (critic D3) |
| 4k ordering sentence | **RATIFIED** shape, extended: it must also carry the two `run-script-hash` lines and the `main-run-launch` line, since r12's ordering chain covers the code that ran (r11 precedent) | plan §6 step 5 |
| 4l "Abs error" unit for count predictions | **RATIFIED** (r11's proportion convention), and the table must gain one row per arm's predicted pass count from `predictions-r12.md` §2 | plan §5 amended |
| §5 probability-file interface | **OVERRULED — exact names and schemas pinned, no candidate search, no markdown fallback**: `predictions-r12-perproblem.jsonl` (416 lines; keys `arm`,`family`,`pid`,`p_pass`,`base_arm`,`x_pid`,`delta_arm`), `predictions-r12-signevents.jsonl` (304 lines; keys `contrast`,`label`,`turns`,`family`,`pid`,`p_diffpos`), run-level RL1–RL7 parsed from `predictions-r12.md` §5. Hard-fail if any is absent or its sha256 disagrees with the bundle | the files exist and are hashed; a tolerant reader would let a substituted file pass unnoticed |

Also binding on the promoted engine (from the amended plan, not in the draft's
question list): three event sets scored separately (416 pass / 304 sign / 7
run-level = 727), BSS per set **and** pooled with the pooled pass BSS labelled
`persistence + arm-rate transport`, calibration on pass events (primary) and
all events (secondary), the degenerate conventions (sd=0 → `t=+0.000
p=1.0000` + `NOTE degenerate:`; Var_L=0 → `z=+0.000 p=1.0000`; b=c=0 →
`p=1.0000`), the neutral-sign downgrade, `direction=<+1|-1|NEUTRAL>` on the E2
sign line, and the `Realized arm positions after deletion:` block (5 rows).

## 2. Defects L1 found in its own work this round (recorded, not hidden)

| id | defect | how found | disposition |
|---|---|---|---|
| L1-E6 | E6 denominator written as 448 when 5×64 + 2×48 = 416 (448 = 7×64, and also the `A-CKPT4710-ack` count — the likely copy/paste origin) | ScribeDrafts and ExecutorRecompute, independently | plan amended pre-hash (§9); 416/727 everywhere |
| L1-tilt | the fitted difficulty slope (c = −5.03) saturates the sigmoid, so arm-mean predicted probability drifted from its base rate (A-MONO mean p 0.372 vs base 0.143; predicted passes 23.8 vs 9.1) | L1, on inspecting the first `predict_r12.py` output | per-arm mean-preserving logit offset `delta_arm` solved by bisection with the clip inside the target; after the fix every arm's mean p equals its base rate exactly and predicted passes = base × n (41.1/29.0/21.0/13.0/9.1/21.8/15.8) |
| L1-precheck | `precheck_r12.py` asserted family-1 problems overlap the r8/r9 sets; family 1 reuses **r11**'s problems, so zero overlap with r8/r9 is the correct outcome | the precheck's own FAIL line | assertion inverted to disjointness (23/23 PASS, exit 0) before hashing |
| L1-C2 | C2 worded as "replication" | ScoutPriorArtLadder (C2 verdict + forbidden-wording list: llama.cpp #7052, Thinking Machines 992/1000, vLLM docs) | reworded to *within-run repeatability* pre-hash; R2 branch labels renamed |
| L1-D1 | the first landed `run_r12.py` was still a copy of `run_r11.py` (two arms, `KENGAKU_R11_*`, `results-r11.jsonl`) and `probe_r12.py` kept r8's A/B/C `main()` | CriticDesign FATAL D1 + LabratMock (independently) | runner rewritten; `main()` replaced by a die-guard so importing the machinery can never fire an off-design request; both re-hashed at `01:16:08Z` before any request |

## 3. Erratum candidate carried from round 11 (found by ScribeDrafts, verified by L1)

Round 11 publishes `grader.py` as `936 → **1709** lines` at three sites
(`LOG.md` round-11 entry, `SCORECARD.md` round-11 operability row,
`.ufo/reports/round-11/kengaku.md`) while the committed artifact at `f09ff1f`
is **1711** lines (`git show f09ff1f:grader.py | wc -l` → 1711;
`wc -l < grader.py` → 1711; non-blank 1527 + blank 184). No counting
convention on the committed bytes yields 1709, and the before-half (936 at
`0c51208`) and the 280-check count are exact. Provenance is `[INFERENCE]`:
most likely measured before the last two comment lines landed in the same
commit. Disposition per house rule: recorded as an erratum in `SCORECARD.md`
and `LOG.md`, **never patched in place** in the round-11 rows.

## 4. Wave roster and file ownership

Wave 1 (10 L2 in ONE batched `task` call): CriticDesign (critic),
ScoutPriorArtLadder (scout), ScoutPriorArtTransport (scout), ScoutEndpointFresh
(scout), ConnectorFleet (connector), ReviewerBaseline (reviewer), LabratMock
(labrat), ExecutorRecompute (executor), ExecutorGrader (executor), ScribeDrafts
(scribe). Wave 2a (batched, run-independent): ReviewerCitations (reviewer),
SentinelScope (sentinel). Wave 2b (after the run lands): MutationTesterR12,
CriticLanded. Each wrote only its own artifact(s).
