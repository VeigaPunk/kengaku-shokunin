# Probe battery r19 — scored at close (2026-10-16T08:23Z)

Source: `plans/probe-battery-r19.md` (freeze-1 `FROZEN: 2026-10-16T07:52:04Z
sha256:e3f08a09…`; freeze-2 `FROZEN: 2026-10-16T07:55:58Z
sha256:e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`,
line 415; freeze record §7.1 BR-1 + RA-1…RA-5, lines 417–490) + 15 runner
receipts `corpus/evidence/probe-r19-*.log`. Scorer seat, round-19 flash wave
(zai bucket). Every number below is a **measurement**; the lane idiom forbids
scalar axis verdicts. Close timestamp: 2026-10-16T08:23:33Z (last log sweep;
P2/P3/P8/P9 had no runner logs at close).

Finalized by the note-writer seat 2026-10-16T08:29:50Z, on top of the
scorer's numbers: every §2/§4 aggregate was recomputed from the §2 tables
and the receipts (battery 2.0197/11 = 0.1836; seat pool 1.6030/26 = 0.0617;
combined 3.6227/37 = 0.0979; zai-miss mass 1.6749/2.0197 = 82.9%; hit-term
mean 0.3448/9 = 0.0383; reliability bands 6/8 · 2/2 · 1/1 — all reproduce),
and the citations were re-verified against the landed files (battery §7.1
RA-1…RA-5; `probe-r19-quota23.log:71-86`; TEMPLATE `:17`/`:160`/`:242`).
This pass corrected defect 10's log filename, and added §0.1 (design +
freeze discipline) and §8 (honest limits); no scored number was altered.

## 0. The round's falsifiable claim, checked

Before (pre-registered, battery §0): the calibration proxy ran 0/1, 1/1, 0/0,
1/1 across rounds 8–11 — intermittent, ad hoc, no standing battery or template.

After (claimed): ≥6 falsifiable probes, predictions hashed before any request,
all executed with receipts, scored at close with an aggregate read, plus a
reusable template; ordering audited. **Verdict: partially met, honestly
reportable.**

- Battery frozen: YES — twice (see §1); 9 probes, 30 §6 rows in the final
  (freeze-2) table.
- Predictions hashed before any request: YES for every scored outcome — each
  outcome postdates a registrar freeze line whose hash its runner verified
  pre-request (RA-2/RA-3), and every seat-level set was hashed before its own
  first request. The freeze *chain* was breached mid-window (BR-1) and
  repaired; recorded, never patched.
- All executed with receipts: **NO — 4 of 9 probes (P2, P3, P8, P9) have no
  runner log at close (UNRUN)**. The claim's "all executed" is falsified in
  part; recorded per §4.2 as UNRUN rows.
- Scored at close with aggregate read: YES — this note, in-round (the r12
  in-round clause is met for the first time since r11).
- Reusable template: YES — `plans/probe-battery-TEMPLATE.md` (two stale
  freeze references inside it; §6 defect 11 — cross-reference corrected from
  "defect 12" in this pass; defect 12 is the v1 §6 totals miscount).

## 0.1 Battery design and the freeze-before-request discipline (note-writer)

**Design.** Nine probes, each a falsifiable claim sourced from a round-18
receipt (battery §1 provenance table): P1 quota-dead token-plan keys stay
dead past their stated resets (meter state, not model state — the
`ledger-route-telemetry.md:60-62` frame); P2/P3 the codex `service_tier`
acceptance set and priority's accepted-but-inert echo; P4/P5 cascade leg
order and burst-vs-incremental transport; P6 the operator's zai flash lane;
P7 the verify-first opencode-go add; P8 `managed:kimi-code` auth-dead; P9
the absent `:34113` served model. Budget: ≤20 requests, ≤256 output tokens,
one attempt per probe, strictly sequential, ≥2 s spacing, no retries on
status responses, dead lanes get exactly one confirming call (battery §2).
The prediction set (§6) splits into binary components scored with Brier
`(p−o)²` and numeric components scored with signed abs-error plus a
pre-registered range/band; components whose event never materializes are
UNPROVABLE and leave the denominators (the r18 M3 idiom).

**The freeze discipline, as it actually behaved.** The gate is three lines
in a file: runners poll until §7 carries `FROZEN: <UTC> sha256:<H>`, verify
`H` by recomputing the §0–§6 byte range, and only then send. It held in
every runner that enforced it in code — and the round stress-tested the
three ways a freeze protocol breaks:

1. **The freeze is a race, not a line (BR-1).** Freeze-1 (07:52:04Z,
   `e3f08a09…`) was byte-valid at stamp time (three independent
   recomputes, RA-1) but the battery-author kept editing above the anchor;
   the posted hash stopped covering the bytes runners read. The repair —
   re-freeze 07:55:58Z `e1a86777…` after a double-read stability check,
   plus §7 step 4's re-verify-immediately-before-writing — is the fix that
   must migrate to the template.
2. **A hash procedure can hash the wrong range.** The original §7 step-2
   `sed` pattern self-matched its own command text, truncating the hashed
   range; the `[R]` bracket breaks the self-match (§6 defect 2). A freeze
   command must state its byte range exactly and be tested against a
   deliberate edit.
3. **A "dry" mode that is a label, not a gate, sends live traffic.** The
   round's only ordering breach (opencode DEFECT 0, two requests before
   the battery existed) came from a probe loop that never checked its
   `--live` flag. Enforcement lives in code; containment was a verbatim
   self-report with receipts and exclusion from scoring.

The discipline's honest edge cases, all recorded: seat-level prediction
sets (shim-ds, shim-glm, hyper, devin) froze their own numbers before their
own requests — valid ordering at the seat layer even when the battery-level
freeze they cite was later superseded (the hyper seat's erratum states the
correct rule: seat predictions must precede the seat's requests, not the
battery freeze); the P1-key1 addendum filed its prediction at the same UTC
second as its request (defect 13 — only `filed ≤ request` is provable at
1 s resolution, the lane's anti-pattern 15); and the registrar's step-1
"no runner log exists" check was unsatisfiable at the re-freeze instant
(defect 3). None of these produced an outcome that preceded its
prediction — the gate's substance held everywhere it was enforced.

## 1. Ordering gate (§4 rule 1)

Gate test per log: `frozen_utc < first_request_utc` AND
`battery_sha256_at_start ==` the §7 hash **as it stood at that log's
execution time** (the only executable reading — runners cannot see future
edits). Rulings:

| run (seat) | verified hash | first request | gate |
|---|---|---|---|
| P6 (runner-leg-zai) | e3f08a09 (recomputed pre-send) | 07:52:25Z | PASS (freeze-1 live) |
| P7 (runner-leg-opencode) | e3f08a09 | 07:52:29Z | PASS (freeze-1 live) |
| P1 ×2 seats (runner-quota-23, runner-listing-mismatch) | e3f08a09 | 07:52:53Z / 07:53:02Z | PASS (freeze-1 live) |
| shim-ds S1–S8 (runner-shim-ds) | e3f08a09 + own prereg 78de64d9 (07:44:02Z) | 07:52:48Z | PASS |
| P4-glm v1 leg (runner-leg-glm-cascade) | e3f08a09 (07:52:40Z) | 07:53:22Z | PASS (freeze-1 live) |
| devin seat-check D1–D3 (runner-leg-devin) | own prereg d9cc90fb (07:53:46Z) | 07:53:54Z | PASS (seat layer) |
| shim-glm G-run (runner-shim-glm) | own prereg a1674cfc (07:55:05Z) | 07:56:26Z | seat layer PASS; battery rows n/a (RA-3 b) |
| P4-glm v2 leg (runner-leg-glm-cascade) | e1a86777 (07:57:44Z) | 07:58:16Z | PASS (freeze-2 live) |
| **P4-devinleg (runner-leg-devin)** | **e3f08a09 cited; requests 07:56:39Z+ postdate freeze-2** | 07:56:39Z | **FAIL (§4 hash mismatch at execution) — excluded from the battery aggregate** per RA-3(c); receipts preserved as seat/corroborating evidence |
| opencode pre-run (runner-leg-opencode) | none (battery unborn) | 07:45:00–04Z | ORDERING-BREACH, self-filed (DEFECT 0), excluded |

Freeze-1 was byte-valid at stamp time and ≥54 s after (RA-1: three
independent recomputes reproduced e3f08a09 — the registrar's ~07:52:15Z, the
glm seat's 07:52:40Z, shim-glm's 07:52:58Z; my own recompute at ~07:53:1x
also reproduced it, pre-edit). The freeze-invalidating event is the
post-freeze above-anchor edit (observed on disk: v1 content still present at
~07:53:1x; battery mtime 07:53:28Z; intermediate hash states `312798e8…` and
`d2f08f12…` recorded by this scorer and by runner-quota-23
(probe-r19-quota23.log:71–86) before the e1a86777 re-freeze). BR-1's two
factual bullets are falsified by receipts and corrected in RA-1/RA-2
(plans/probe-battery-r19.md:443–465). **No outcome precedes its prediction
anywhere in the scored set** — the breach is bookkeeping (which text was
frozen), not ordering.

## 2. Scored battery components (gate-passing receipts only)

Binary (Brier `(p − o)²`):

| id | prediction | p | observed | o | Brier | verdict |
|---|---|---|---|---|---|---|
| 1a | key2 chat → 429 | 0.93 | 429 insufficient_quota (retry-after 634027/634017) | 1 | 0.0049 | HIT |
| 1b | key3 chat → 429 | 0.93 | 429 insufficient_quota (retry-after 1066018/1066010) | 1 | 0.0049 | HIT |
| 1e | both bodies contain `insufficient_quota` | 0.85 | yes/yes | 1 | 0.0225 | HIT |
| 1f | both /models → 200 | 0.90 | 200/200 (16 ids each, configured model present) | 1 | 0.0100 | HIT |
| 4c | glm shim /health legs == [zai, devin, hyper] | 0.85 | exact match (probe-r19-P4-glm.log v2 [1/2]) | 1 | 0.0225 | HIT |
| 4d | glm stream served by leg-1 zai | 0.90 | journal `leg=1/zai OK status=200 stream=True 2.097s`; z.ai header family; echo `glm-5.3-flash` | 1 | 0.0100 | HIT |
| 5b | glm stream burst (span < 50 ms) | 0.50 | first→last delta span 0 ms (14 reasoning deltas, one flush) | 1 | 0.2500 | HIT |
| 6a | zai lane chat → 200 | 0.93 | **429 code 1302 "Rate limit reached"** | 0 | 0.8649 | MISS |
| 6b | usage block, completion_tokens > 0 | 0.90 | **absent** | 0 | 0.8100 | MISS |
| 7a | opencode chat → 200, no 403/1010 | 0.90 | 200 | 1 | 0.0100 | HIT |
| 7b | stream model echo `deepseek-v4.1-flash` | 0.90 | exact (`x-zen-model` + stream field) | 1 | 0.0100 | HIT |

Numeric (signed error, range/band):

| id | prediction | observed | abs error | range/band |
|---|---|---|---|---|
| 1c | key2 implied reset = 2026-10-23T16:00:00Z (±7200 s) | 16:00:00Z (+0.1 s) and 15:59:59Z (−1 s) — two seats | 0.1 s / 1 s | HIT ×2 |
| 1d | key3 implied reset = 2026-10-28T16:00:00Z (±7200 s) | 15:59:59Z (−0.8 s) and 15:59:59Z (−1 s) | 0.8 s / 1 s | HIT ×2 |
| 4f | glm prompt_tokens 30, range [15, 60] | 30 | 0 | HIT (exact) |
| 7c | opencode prompt_tokens 45, range [20, 120] | 48 | +3 | HIT |
| 7d | opencode first-decoded TTFT 4000 ms, range [1500, 6500] | 1724 ms | −2276 | HIT (point miss low) |

Range hit-rate: 5/5 scoreable rows (1c/1d double-measured → 7 hit
observations of 7). 6c (zai TTFT 3000 [1500, 6000]) UNPROVABLE — the lane
answered 429 with a JSON error body, no stream.

UNPROVABLE (excluded from denominators, with reasons):

- 4a, 4b, 4e, 5a — the 4x/5x rows were rewritten between freeze-1 and
  freeze-2 (RA-3); the pre-freeze-2 P4/P5 outcomes (07:53:22–25Z) precede
  freeze-2 and the post-freeze-2 ds-side measurements sit on the
  stale-hash devinleg run (RA-3 c, excluded — its ds receipt: prompt_tokens
  48, span 0 ms, would have matched v1-4b/5b exactly; recorded as
  corroborating seat evidence, not scored). Additionally the freeze-2 P4
  body carried `temperature:0`, which the devin fallback leg refuses
  (DEFECT-3) — v1's 4a/4c were unmeasurable by construction under the live
  leg order.
- 6c — no stream (see above).

UNRUN (no runner log at close; predictions frozen but unexercised):
2a, 2b, 3a–3d (codex service_tier set), 8a, 8b (managed:kimi-code 401),
9a (`:34113` absent-surface freshness probe). Nine components.

## 3. Probe verdicts (§4 rule 3)

| probe | verdict | basis |
|---|---|---|
| P1 | PASS | 6/6 components hit (two seats ran it — see §6 defect 7; receipts agree on every observation) |
| P4 | PASS (freeze-2 rows) | 4c/4d/4f hit; v1-era rows unprovable; 4e unprovable (its only gate-clean measurement predates freeze-2 — ordering-excluded) |
| P5 | PASS (scored component hit; caveat) | 5b hit; 5a unprovable — a contested excluded receipt (ds span 0 ms) would have falsified the v2 "incremental" prediction if admitted |
| P6 | FAIL | 6a/6b miss (zai 429 rate-limit window); 6c unprovable |
| P7 | PASS | 4/4 |
| P2, P3, P8, P9 | UNRUN | no runner logs by close |

Tally: 3 PASS, 1 FAIL, 1 PASS-with-caveat, 4 UNRUN (of 9 probes; 5 executed).

## 4. Aggregate calibration read (measurements, not axis verdicts)

(i) **Mean Brier, battery layer: 0.1836** over 11 scored binaries (sum
2.0197), with the always-0.5 reference **0.25** stated beside it as a
comparison, not a grade. 9 hits / 2 misses; the two misses (6a+6b, both the
zai-lane rate-limit outcome) carry **82.9% of the total Brier mass**
(1.6749 of 2.0197); the 9 hit components average 0.0383.

(ii) **Mean abs-error by unit**: implied-reset offsets 0.725 s mean
|offset| over 4 observations (nominally 630,000–1,062,000 s horizons);
prompt_tokens: 0 (4f) and +3 (7c); TTFT: −2276 ms (7d). Range/band
hit-rate: 5/5 scoreable.

(iii) **Reliability points** (battery layer; too few events for a fitted
slope — the r12 slope needed 416 events, this battery has 11): pred ≥0.9:
predicted 0.9113, observed 6/8 = 0.750 (n=8); pred 0.8–0.9: predicted
0.850, observed 2/2 = 1.000 (n=2); pred 0.50: observed 1/1 (n=1). Overall
predicted mean 0.8627 vs observed frequency 0.8182 — mild overconfidence,
concentrated entirely in the two p≥0.9 zai rows.

(iv) **Probe counts**: 3 PASS, 1 FAIL, 1 PASS-with-caveat, 4 UNRUN.

**Seat-level layer** (own preregs, all filed pre-request, all scored at
close — separate from the battery aggregate per TEMPLATE §10):

| seat set | terms | sum | mean Brier | notes |
|---|---|---|---|---|
| shim-ds S1–S8 | 5 filed-p binaries | 0.0325 | 0.0065 | 9/9 claims survived; S3/S4 abs-errors 0.016/0.552 s, in band; S6/S7 pass-fail hits with no filed p (defect 9 — pointer corrected from "defect 10" in the note-writer pass; defect 10 is devin D5) |
| devin D1–D5 | 3 binaries | 0.6650 | 0.2217 | D2 miss (0.64) — temperature:0 → 400 on swe-2; D4 range hit, point off by 11678; D5 unprovable |
| glm G1–G8 | 7 binaries | 0.5405 | 0.0772 | G1 0.2025 (low forecast, right), G4 0.3025; G3 unprovable |
| hyper H1–H10 | 11 binaries | 0.3650 | 0.0332 | 12/13 hit; H8 the designed adjudication miss (0.3025) |
| **pooled seat layer** | **26** | **1.6030** | **0.0617** | |

Addendum (P1-key1, outside §6, parent-dispatched): 3-way forecast
(200 p=0.75 / 429 p=0.20 / other p=0.05), observed 200 — modal branch hit;
multi-class Brier Σ(p−o)² = 0.105 (main-branch binary term 0.0625).
Finding: token-plan key 1 is alive on 2026-10-16, consistent with r18 M3.

Combined (battery + seat, descriptive only): **37 Brier terms, sum 3.6227,
mean 0.0979.**

Seat-layer reliability contrast (the round's calibration lesson): seat
forecasts grounded in same-day route-state evidence (shim journals, code
pins, live config reads) went **19/19 at p≥0.9** (predicted mean 0.938);
battery forecasts carried forward from r18's numbers across an unseen
serving-plane redeploy went **6/8 at p≥0.9** (predicted 0.911). The misses
were not noise — they were stale-premise forecasts, and the battery caught
them, which is the instrument working.

## 5. Findings (route/serving-plane; routed, not absorbed)

1. **Both cascades were redeployed 2026-10-15T17:16:22Z** with new software
   (`Server: devin-openai-shim/2` vs the r18 census `BaseHTTP/0.6`), live
   leg orders ds `alibaba-token-plan → hyper → opencode-go` (M7) and glm
   `zai → devin → hyper` (M9). Every r18 cascade number (D9 prompt-token
   taxes, burst table, cascade TTFT medians) describes a configuration that
   no longer exists. Integrator material: any cross-round comparison drawn
   from cascade lanes must be re-based (probe-r19-P4-glm.log findings 1–2;
   probe-r19-shim-glm-run.log F-1).
2. **The devin shim rejects `temperature:0`** (400 `invalid_argument`,
   `devin_shim_error`) — on swe-2 (D2), opus (r18 M10), and the glm
   cascade's fallback leg (v1 attempts + shim-glm attempt-1 + a direct-8787
   cross-check); the glm cascade treats that 400 as terminal, so a
   temperature-bearing body during a zai-429 window loses the call
   (probe-r19-shim-glm-run.log F-2). Unowned serving plane → integrator.
3. **zai rate-limit pressure**: P6's 429 (07:52:25Z) matches the shim
   journal's burst-window reading (547 zai-leg 429s vs 302 OK, 35.6% serve
   rate); by the 07:58:18Z v2 run zai served 200. Transient congestion, plausibly
   the 32-seat wave's own aggregate load on the shared subscription (RA-5
   concurs). Route-state observation, not a model signal
   (`corpus/knowledge/ledger-route-telemetry.md:60-62` frame).
4. **Burst-vs-incremental is per-leg/per-model, not a lane property**:
   zai-glm burst (span 0 ms, v2 5b + G5 hit), ds-alibaba burst (span 0 ms,
   excluded corroborating receipt), hyper-deepseek incremental (145 ms,
   TPS 434.91 — H8 MISS falsifies the census "burst lane" row's
   transferability; probe-r19-hyper.log finding 1).
5. **Prompt-token state moved on hyper**: COUNT_PROMPT billed 48 vs the
   census's 31 (+17, same body shape — serving-side change; hyper.log
   finding 2). Meanwhile glm-zai billed exactly 30 (4f exact) and ds billed
   exactly 48 (excluded devinleg receipt) — the r18 token bands held where
   the serving software was unchanged.
6. **opencode TTFT moved 3356/4958 → 1724 ms** (n=1, different day;
   identity headers exact, no reroute — within M6's own warning terms).
7. **P9 never ran**: the `:34113` absent-surface freshness probe has no
   receipt this round; the battery-author's disclosed `ss -ltn` read
   (07:40:22Z, no listener) remains the only same-day evidence. The
   standing-battery pattern wants this probe run every round — flagging the
   gap for the next instantiation.

## 6. Defects and breaches (recorded, never patched)

1. **BR-1 freeze chain** (`plans/probe-battery-r19.md:419–441`): stale
   freeze-1 (e3f08a09) while above-anchor edits landed mid-window
   (observed mtimes 07:53:28Z, 07:54:27Z; intermediate hashes `312798e8…`,
   `d2f08f12…`); re-frozen e1a86777 at 07:55:58Z. BR-1's own two factual
   bullets ("edits landed through 07:52:08Z"; "no runner executions in the
   window") are falsified by receipts and corrected in RA-1/RA-2
   (lines 443–465) — the corrections match this scorer's independent audit.
2. **§7 step-2 sed self-match defect**: the original command's pattern
   matched its own command text, so freeze-1's hash covered less than the
   full anchor range; fixed post-freeze with the `[R]` bracket (receipt:
   probe-r19-quota23.log:71–86).
3. **Registrar step 1 was unsatisfiable at the re-freeze**: runner logs
   already existed on disk at 07:55:58Z (receipt: probe-r19-P4-glm.log
   cross-freeze note; RA-2).
4. **ORDERING-BREACH (runner-side, self-filed)**: runner-leg-opencode's
   draft harness sent 2 live requests at 07:45:00–04Z, before the battery
   existed (DEFECT 0, probe-r19-opencode-health.log:8–42); gate fixed and
   re-tested; excluded from scoring.
5. **§2 rule-3 reshaped retry**: shim-glm attempt 2 re-sent the P4 body
   minus `temperature` after a 400 (self-disclosed,
   probe-r19-shim-glm-run.log §2; RA-4 i). Its receipt supplied the
   temperature/shape discrimination — data kept, breach recorded, battery
   4x/5x rows still unprovable on it (RA-3 a).
6. **Stale-hash execution**: runner-leg-devin's P4 log cites e3f08a09 while
   its requests (07:56:39Z+) postdate freeze-2 — §4 gate mismatch, excluded
   from the battery aggregate per RA-3(c) (scorer's ruling; receipts
   preserved). Its DEFECT-2 (NameError mislabeling a 200 as `http=error`)
   and duplicated header block are in the same file (RA-4 iii).
7. **Duplicate execution**: P1 ran in two seats (8 requests for a
   4-request probe; receipts agree on every component); P4(i) ran in three
   seats (7 requests to :8793 vs 2 budgeted) — the ≤20-request budget is
   breached in aggregate when seat-level probes on shared hosts are counted
   (RA-4 ii). Cross-seat ≥2 s spacing was also broken twice on token-plan
   (1 s gaps at 07:53:01→02, 07:53:05→06). The wave has no dispatch ledger
   for seat-level dedup — the template should require one.
8. **DEFECT-3 (battery-design)**: the frozen P4 body (`temperature:0`) was
   unservable on the live shim — the v1 P4 predictions were unmeasurable by
   construction (probe-r19-P4-devinleg.log addendum). A body-servability
   pre-check (mock or stub) should precede any freeze (template §9 step 4
   covers mock-smoking the runner; extend it to the frozen body).
9. **shim-ds seat aggregate imputation**: S6/S7 were scored with Brier
   0.0025 each though no probability was filed for them (implicit p=0.95);
   scorer recomputation over the 5 filed-p terms: mean 0.0065 vs the seat's
   stated 0.0050 (probe-r19-shim-ds-run.log:161–162).
10. **devin D5 unprovable** — harness did not persist first-content timing
    (DEFECT-1, `probe-r19-devin-shim-seat.log` seat-scoring section).
11. **Template staleness**: `plans/probe-battery-TEMPLATE.md` cites the
    superseded freeze as "verified working" (line 17, line 160) and
    "18 requests, ≤232 output tokens" (line 242) — the final freeze is
    e1a86777, 19 requests/≤240 tokens.
12. **v1 §6 totals miscount**: the freeze-1 table stated 22 binary rows; it
    contained 20 (scorer's count of the pre-edit bytes).
13. **P1-key1 same-second filing**: prediction_filed_utc == first_request_utc
    (07:52:50Z) — only `filed ≤ request` is provable at 1 s resolution (the
    lane's own anti-pattern 15 caveat; r12 precedent).

## 7. Inputs for the SCORECARD calibration proxy (parent's row)

- (a) probes run in-round with predictions filed before the first request
  **and** scored at close: **5 executed / 5 scored** (P1, P4, P5, P6, P7 —
  P4/P5 via their freeze-2 rows; every scored outcome postdates a verified
  freeze or a hashed seat prereg). 4 probes UNRUN (P2, P3, P8, P9). Five
  seat-level prediction sets also filed pre-request and scored at close —
  the widest predict→observe→score loop the lane has run (r11: 3 events;
  this round: 11 battery + 26 seat-layer Brier terms + 7 numeric rows).
- (b) artifacts produced: 15 evidence logs + battery + template + this
  note, all working-tree at scoring time — commit/index/LOG is the
  parent's landing step (proxy (b) completes there).
- (c) not re-run by this seat (scorecard rows are parent-owned).

## 8. Honest limits (note-writer)

1. **The aggregate rests on few events.** 11 battery-layer binaries (2
   misses) and 26 seat-layer terms. A mean Brier over 11 events has wide
   uncertainty; the r12 reliability slope needed 416 events. The
   reliability table (§4 iii) has n=8/2/1 per band — directional, not
   fitted. The combined 37-term figure mixes layers with different
   information states and is descriptive only.
2. **The battery is host- and day-specific.** Every number is a
   2026-10-16 observation of this host's shims, subscriptions, and
   provider routing: the zai 429 is a transient meter state; the shim
   redeploys of 2026-10-15T17:16:22Z sit between every r18 number and
   this round (§5 finding 1); hyper's prompt-token drift (§5 finding 5)
   shows even unchanged-looking lanes move. Nothing here transfers to
   another host or week without re-running the battery.
3. **Coverage is partial and uneven.** 4 of 9 probes never ran (P2, P3,
   P8, P9 — UNRUN); the executed set skews to quota/transport probes
   because P1/P4–P7 were picked up by runner seats while the codex and
   freshness probes were not. P9 — the cheapest probe (one localhost GET,
   zero quota) — is among the unrun, so the round's freshness value on
   `:34113` is unrealized (§5 finding 7).
4. **The freeze chain was breached mid-round.** Freeze-1 was valid at
   stamp time but stopped covering the bytes runners read; the repair
   (freeze-2) is verified byte-exact, and no scored outcome precedes its
   prediction — but the round's freeze discipline is "breached and
   repaired", not "clean". The v1-window runs are scoreable only because
   RA-3(a) proves the rows they scored are byte-identical across both
   freezes.
5. **Several verdicts rest on adjudicated exclusions.** The battery
   aggregate excludes the devinleg ds-side receipt (stale-hash citation,
   defect 6) and the pre-freeze-2 P4/P5 outcomes (RA-3 a); the 5b
   "burst" reading uses the any-delta basis because the stream carried
   no content deltas (P4-glm caveat). A second scorer could defensibly
   re-admit the excluded receipts and shift 4b/5a from UNPROVABLE to
   scored; the numbers here are one adjudication, not the only possible
   one.
6. **Seat-level and battery-layer numbers are not commensurable.** Seat
   forecasts were grounded in same-day route-state evidence (journals,
   code pins); battery forecasts carried r18 numbers across an unseen
   redeploy. The 0.0617 vs 0.1836 contrast (§4) is the round's
   calibration lesson, not a quality ranking of seats.
7. **No prior-art pricing this round.** The novelty proxy (fetched-URL
   prior-art verdicts) was not exercised — this is a calibration
   axis-move; the battery's findings (§5) are route-state measurements
   awaiting prior-art pricing if any is ever promoted to a claim.

## 9. Sources

- `plans/probe-battery-r19.md` — battery, freeze lines 395–415, freeze
  record §7.1 (BR-1, RA-1…RA-5) lines 417–490.
- Receipts: `corpus/evidence/probe-r19-{opencode-health,shim-ds-predictions,
  shim-ds-run,devin-shim-seat,P4-glm,P5-glm,P4-devinleg,shim-glm-predictions,
  shim-glm-run,hyper-predictions,hyper,P1-key1-quota,p1-listing-mismatch,
  quota23,P6-zai}.log` (15 files).
- Knowledge basis: `corpus/knowledge/kimi-model-routing-round18.md`
  (r18 digest); `corpus/knowledge/ledger-route-telemetry.md:60-62`
  (meter-vs-model frame); `corpus/knowledge/bench-arena-fresh-run.md:11`
  (`:34113` absence).
- Prior scoring idioms: `corpus/evidence/round11-power/analysis_r11.md`,
  `corpus/evidence/round12-ladder/analysis_r12.md` §Prediction scoring.
