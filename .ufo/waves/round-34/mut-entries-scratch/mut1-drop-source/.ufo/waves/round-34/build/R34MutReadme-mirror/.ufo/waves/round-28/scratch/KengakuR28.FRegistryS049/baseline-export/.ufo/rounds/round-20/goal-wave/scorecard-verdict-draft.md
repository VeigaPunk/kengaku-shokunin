# scorecard-verdict-draft — kengaku round 20 (calibration: battery completion, grid 5/9 → 9/9)

Scribe seat, round-20 goal wave. Written 2026-10-16, updated through
2026-10-16T09:55Z — all round-20 artifacts landed and folded in: the four
completion receipts (09:14:49–09:19:25Z), the scorer's §10 extension
(`corpus/knowledge/probe-battery-r19.md`, scored 09:21:55Z, mtime 09:23Z),
and the template revision (`plans/probe-battery-TEMPLATE.md`, mtime 09:22Z).
Starting commit `f330e2b` (round-19 records; the r19 evidence commit is
`0671bb0`). **This file writes nothing**: every block
below is a paste-ready delta for a PARENT-owned file (`SCORECARD.md`,
`LOG.md`); the parent integrates under the kengaku lane identity.
`[PARENT]` markers flag cells the parent must confirm or fill from landed
artifacts at integration time; `{{PLACEHOLDER}}` slots resolve from landed
artifacts or are replaced by an absence statement with polling evidence —
placeholders must not ship. No scalar axis verdicts — verdicts are recorded
per gate, per the round-16 idiom (`corpus/lessons/round-16-recensus.md`
"Verdict lines (measured)").

Round-20 scope (one axis-move, CALIBRATION — battery completion, close the
grid): no gate/tool changes; no new battery probes; P2/P3/P8/P9 run exactly
as specified in the r19 frozen battery; predictions are FROZEN from r19 and
must not be edited.

## 0. Measured state at draft time (09:15Z), first update (09:25Z), final update (09:55Z)

| Quantity | Value | Command |
|---|---|---|
| HEAD | `f330e2b` | `git rev-parse --short HEAD` (09:15Z) |
| Working tree (lane) | at 09:15Z: `?? .ufo/interactive-sessions/` only; by 09:20Z the four completion receipts had landed (untracked) | `git status --porcelain` |
| Freeze-2 still valid | `e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1` == the FROZEN line (`plans/probe-battery-r19.md:415`) — predictions byte-unchanged since r19 close; re-verified by this scribe at 09:15Z **and independently by all four executor seats pre-request** (each receipt's header, D20-s10) | `sed -n '1,/FROZEN-PREDICTIONS-ANCHO[R]/p' plans/probe-battery-r19.md \| sha256sum` (run 09:15Z) |
| Evidence inventory | at 09:15Z: 15 receipts, no `probe-r19-P[2389]*` (`grep 'probe-r19-P[2389]'` → exit 1); at 09:20Z: **19 receipts** — `probe-r19-P2-servicetier.log`, `probe-r19-P3.log`, `probe-r19-P8-kimi-code-auth.log`, `probe-r19-P9-absent-port.log` | `ls corpus/evidence/ \| grep -c 'probe-r19-.*\.log'` |
| Scorer note | r19 close state through 09:15Z; **§10 extension landed at 09:23Z** (scored 09:21:55Z): ordering gate PASS ×4, 9 components scored, grid 9/9, aggregate 0.1495/20 | `corpus/knowledge/probe-battery-r19.md:425-596` (§10–§10.6) |
| Template | r19 state through 09:15Z; **revision landed at 09:22Z** (308→437 lines): freeze-after-last-edit guard (§5 step 3), completion gate (§7 rule 1), provenance table (§7 rule 6), close-the-grid checklist (§9 step 7), named-runner assignment (§9 step 8); stale `e3f08a09` refs replaced with the superseded/valid pair | `plans/probe-battery-TEMPLATE.md:17-24, 137-216, 261-316, 377-398` |
| Gate | [PARENT: re-run `python3 grader.py` at close — no gate change this round, so the r17 verdict is expected to stand] | `python3 grader.py` |

## 1. The round's falsifiable claim, with receipts

**Before-claim (this round's own premise):** the battery stands at **5/9
probes executed** (P1, P4, P5, P6, P7) with **4 named-UNRUN** (P2/P3/P8/P9
— named, not hidden), aggregate computed over 11 gate-passing binaries
(mean Brier 0.1836), and the template lacks the freeze-after-last-edit
guard and the unrun-completion checklist.

Scribe re-verification of the before-state (independent, at 09:15Z):

- **5/9 executed** — `corpus/knowledge/probe-battery-r19.md` §3 tally:
  "3 PASS, 1 FAIL, 1 PASS-with-caveat, 4 UNRUN (of 9 probes; 5 executed)";
  §7 proxy (a) row: "5 executed / 5 scored … 4 probes UNRUN (P2, P3, P8,
  P9)". The unrun components are §6 rows 2a, 2b (P2), 3a–3d (P3 — derived
  from P2's captures, zero extra requests), 8a, 8b (P8), 9a (P9): nine
  binaries, all frozen in r19 (`plans/probe-battery-r19.md:364-370,
  385-387`).
- **Aggregate over 11 binaries** — same note §4 (i): "Mean Brier, battery
  layer: 0.1836 over 11 scored binaries (sum 2.0197)" with the 0.25
  always-0.5 reference beside it.
- **Predictions frozen and untouched** — the §7 step-2 recompute over the
  current bytes returns `e1a86777…` exactly (§0 table). The frozen §6 set
  is 23 binary + 7 numeric rows / 19 enumerated requests; the four
  completion probes spend 9 of the never-executed requests (P2: 7, P8: 1,
  P9: 1, P3: 0) — **the completion widens no budget**: the r19 §6
  enumeration already included these 9 requests.
- **Template gaps** — `plans/probe-battery-TEMPLATE.md` §5 (registrar
  procedure, steps 1–7 at `:131-172`) has no "re-verify immediately before
  writing" step; the r19 plan carries it at
  `plans/probe-battery-r19.md:404-406` as the BR-1-closing repair, and the
  r19 note's defect 11 (`corpus/knowledge/probe-battery-r19.md:333-336`)
  records the template's stale citations (`:17`, `:160`, `:242`). No
  unrun-completion checklist exists anywhere in the template (§9 step 6
  `:287-291` has the in-round clause but nothing forces per-probe closure).
- **Named-UNRUN, not hidden** — the r19 close note lists them with the
  UNPROVABLE/UNRUN idiom (§2 "UNRUN … Nine components", §8 limit 3); P9 —
  the cheapest probe (one localhost GET, zero quota) — is among them
  (§5 finding 7 of the note).

**After-claim (this round's deliverable):** all 9 probes have executed
outcomes scored against the SAME frozen predictions (no prediction edits);
the aggregate read is recomputed across all executed binaries; the grid is
9/9 with per-round provenance; the template gains the
freeze-after-last-edit guard + the unrun-completion checklist.

## 1.1 Completion receipts — the after-state as landed (read 09:19–09:25Z)

All four probes executed; every receipt freeze-verified `e1a86777…`
pre-request; every one of the 9 formerly-UNRUN components now has a recorded
outcome (component verdicts below are the receipts' own observations — the
official scores and the recomputed aggregate remain the scorer seat's call):

| probe | receipt | ordering (first request vs freeze 07:55:58Z) | component outcomes (receipt-verbatim) | probe basis |
|---|---|---|---|---|
| P2 | `probe-r19-P2-servicetier.log` (P2-executor) | verified pre-run; requests 09:18:22–39Z, 7 POSTs, gaps 4/3/2/4/2/2 s | 2a: status vector `[200,200,400,200,400,400,400]` **exact match → HIT**; 2b: all four 400 bodies name `Unsupported service_tier: <value>` → **HIT** | PASS |
| P3 | `probe-r19-P3.log` (P3-executor) | zero-request derived probe; gate-checks P2's bytes; analysis 09:19:25Z | 3a HIT (echo `default` ×3, `priority` never appears, sequences byte-identical); 3b HIT (credits 62500.0000000000 ×3); **3c MISS** (used-percent 7/7/7 > frozen ≤2 — mechanism: plan-window consumption between rounds, r18 basis read 1 on 2026-10-15; inertness itself holds — 7/7/7 static across tiers); 3d HIT (usage input_tokens 7/7/7) | FAIL basis (3c) |
| P8 | `probe-r19-P8-kimi-code-auth.log` (P8-executor) | double-read stability 09:14:36/37Z; request 09:14:49Z | 8a: HTTP 401 → **HIT**; 8b: body contains both `invalid_authentication_error` and `Invalid Authentication` → **HIT** | PASS |
| P9 | `probe-r19-P9-absent-port.log` (runner-p9) | recompute 09:14:47Z; request 09:15:04Z | 9a: connection refused, curl exit 7, http 000, 3 ms → **HIT**; freshness clause NOT triggered (no HTTP status of any kind — absence re-confirmed same-day) | PASS |

New Brier sum over the 9 components, per the receipts' own arithmetic:
**0.9700 (8 hits / 1 miss — the 3c miss carries 0.8100 of it, 83.5%)** —
reproduced exactly by the scorer's §10.2 table. The r20 battery-layer
aggregate, recomputed by the scorer across all executed binaries
(`corpus/knowledge/probe-battery-r19.md:516-549`): **mean Brier 0.1495
over n = 20 scored binaries (sum 2.9897 = r19's 2.0197/11 + r20's
0.9700/9), always-0.5 reference 0.25 beside it**; 17 hits / 3 misses; the
three misses (6a+6b zai rate-limit, 3c used-percent drift) carry 83.1% of
the mass; per-wave split r19-close 0.1836/11 → completion 0.1078/9;
reliability bands 9/12 · 7/7 · 1/1; probe counts **7 PASS, 2 FAIL,
0 UNRUN** — grid **9/9 executed with per-round provenance** (P1, P4, P5,
P6, P7 in r19; P2, P3, P8, P9 in r20).

## 2. Verdict draft — calibration axis-move (paste-ready section)

```markdown
## Round 20 — battery completion: the grid closes (calibration axis-move)

The round completes the r19 standing battery instead of authoring a new
one: P2/P3/P8/P9 executed with receipts under the SAME frozen prediction
set (`FROZEN: 2026-10-16T07:55:58Z sha256:e1a86777…` — scribe-recomputed
byte-exact at 2026-10-16T09:15Z; the battery file's mtime is unchanged
since the r19 freeze record), no prediction edits, aggregate recomputed
across all executed binaries (scorer §10.4), grid 9/9 with per-round
provenance (scorer §10.4 iv), template revised with the
freeze-after-last-edit guard + the unrun-completion checklist.

| Axis | Verdict | Evidence / limit |
|---|---|---|
| calibration | [PARENT: verdict line per gate — the scorer's §10 gives the measurements; the parent judges the axis] | `plans/probe-battery-r19.md` (predictions unchanged, freeze `e1a86777…` re-verified); `corpus/evidence/probe-r19-P{2,3,8,9}*.log` (4 new receipts, 19 total); `corpus/knowledge/probe-battery-r19.md` §10 (mean Brier 0.1495/20, 0.25 reference; 7 PASS / 2 FAIL / 0 UNRUN; grid 9/9 with per-round provenance); `plans/probe-battery-TEMPLATE.md` (revised: §5 step 3 freeze-after-last-edit guard, §7 rule 1 completion gate, §7 rule 6 provenance table, §9 step 7 close-the-grid checklist, §9 step 8 named-runner assignment) |
| novelty | unchanged | No new construct: the round completes an existing instrument's grid against its existing frozen predictions; no new probe authored. |
| operability | unchanged | No gate/tool change (round scope); grader state [PARENT: re-run at close]. |
| freshness | [PARENT: verdict — P8/P9 re-confirmations, no freshness event fired] | P8: `managed:kimi-code` still auth-dead (401, both predicted strings — 8a/8b HIT); P9: `:34113` absence re-confirmed with a same-day receipt (curl exit 7, 3 ms, zero-traffic corroboration) — freshness clause NOT triggered; the r19 finding-7 gap is closed as a re-confirmation, not a restore (scorer §10.5 finding 4). |
| coverage | [PARENT: verdict — the battery's probe coverage moves 5/9 → 9/9, a fact about the instrument's grid] | Scorer §10.4 iv: grid 9/9 executed with per-round provenance (r19: P1/P4/P5/P6/P7; r20: P2/P3/P8/P9, receipts 09:14:49–09:19:25Z). |
| depth | unchanged | No new sourced claim beyond the completion receipts, the scorer §10 extension, and the template guards. |
| adjacency | unchanged | All four probes in-province, small requests (9 total, inside the frozen §6 enumeration); no serving-plane surprise fired — the one falsification (3c) is a route-state threshold drift, recorded not patched (scorer §10.3). |

Proxy (a) reading for this round (measurement, not a score): **9 executed /
9 scored** (5 in r19 + 4 in r20), all against the freeze-2 prediction set —
the proxy's "predictions filed before the first request" clause is met by
the frozen battery itself for all 20 scored binaries (scorer §10.6 a).
Battery-layer mean Brier 0.1495/20 (r19-close 0.1836/11; completion wave
0.1078/9); seat pool 0.0617/26 unchanged; combined 0.0998/46 (descriptive).
Timestamp/ordering state: ordering gate PASS on all four completion
receipts — `frozen_utc 07:55:58Z < first_request_utc` in every case,
`battery_sha256_at_start == e1a86777…` verified pre-request by every seat
(P8 with a double-read stability check); no ordering breach, no new
defects; the r19 exclusions (RA-3(a)/(c), DEFECT 0, the reshaped-retry
rows) stand unchanged — no r20 seat re-ran those probes (scorer §10.1,
§10.2 UNPROVABLE note).
```

**[PARENT] Fill rules for the section above:**

1. The scorer's numbers are landed — `{{AGGREGATE_READ_R20}}`,
   `{{PROXY_A_LINE_R20}}`, `{{ORDERING_LINE_R20}}` are resolved inline
   above from `corpus/knowledge/probe-battery-r19.md` §10 (scored
   09:21:55Z); the parent quotes them as landed, or re-quotes from the
   note at integration if the note gained further rows.
2. `{{N_NEW_LOGS}}` resolved: 4 (`probe-r19-P2-servicetier.log`,
   `probe-r19-P3.log`, `probe-r19-P8-kimi-code-auth.log`,
   `probe-r19-P9-absent-port.log`); evidence set 15 → 19.
3. The calibration cell's verdict line must be a verdict *per gate*
   (round-16 idiom), not a scalar. Whether calibration moves is the
   parent's judgement; this draft files the evidence.
4. **Premise guard (satisfied, verified):** the after-claim required zero
   prediction edits — verified three ways: the scribe's 09:15Z recompute
   of the §7 hash over the current bytes == `e1a86777…`; the battery
   file's mtime unchanged (08:06Z local) since the r19 freeze record;
   the scorer's own 09:14:31Z recompute (§10 preamble). The D20-s2
   consequence clause stands as the guard for any future round.

## 3. Scribe findings (filed, not patched; each with its receipt)

- **D20-s1 (before-state re-verification — the round's premise holds at
  draft time):** every leg of the before-claim verified independently at
  2026-10-16T09:15Z (§0 table + §1 receipts): 15 receipts with no
  P2/P3/P8/P9 log, scorer note at its r19 close state, template without
  either new guard, freeze recompute byte-exact. The premise "5/9 with 4
  named-UNRUN" is true at round start.
- **D20-s2 (the SAME-frozen-predictions premise — verified, and load-
  bearing):** `sed -n '1,/FROZEN-PREDICTIONS-ANCHO[R]/p'
  plans/probe-battery-r19.md | sha256sum` →
  `e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1` ==
  the FROZEN line at `plans/probe-battery-r19.md:415`. The completion
  probes are therefore scoreable against predictions that predate every
  r20 request by >1 h. Consequence: any round-20 prediction edit is a
  freeze breach by the battery's own §7 step 6 / template §5 step 6
  doctrine ("any edit above the anchor after the freeze invalidates the
  freeze and is recorded as a breach") — recorded, never patched, and the
  affected components leave the "scored against the same frozen
  predictions" class. The r20 scorer note must state explicitly that no
  edit occurred (the expected case) or record the breach.
- **D20-s3 (template revision spec — the defect inventory the
  template-reviser closes; template-reviser-owned file, recorded not
  patched by the scribe):**
  (a) `:17` lineage row cites `FROZEN 2026-10-16T07:52:04Z sha256
  e3f08a09…98943` — the hash plan §7.1 BR-1 records as "the identity of
  the pre-rebase bytes, not a valid freeze" (the valid freeze is the
  07:55:58Z `e1a86777…` re-freeze; r19 note defect 11);
  (b) §5 step 5 (`:156-160`) presents the stale-hash recompute as "r19
  verified working: recomputation reproduced `e3f08a09…98943` exactly" —
  same staleness;
  (c) §5 lacks the **freeze-after-last-edit guard**: no
  "re-verify-immediately-before-writing" step (the r19 plan's §7 step 4,
  `plans/probe-battery-r19.md:404-406`, is the seed text), no double-read
  stability check, and no positive rule that the freeze must be the file's
  LAST above-anchor edit (draft-complete-then-freeze; re-freeze after any
  above-anchor edit). Step 6's breach doctrine (`:161-163`) says
  corrections land as appended errata below the anchor — true, but it does
  not describe what actually repaired r19 (a re-freeze with a new hash +
  a §7.1 record);
  (d) `:242` quotes the superseded "18 requests, ≤232 output tokens"
  budget (re-based final: 19 / ≤240);
  (e) **no unrun-completion checklist**: §9 step 6 (`:287-291`) has the
  in-round scoring clause, but nothing in the instrument forces every
  probe to end the round as `executed-with-receipt` **or**
  `NOT-RUN-with-reason` before close — the exact gap that left r19 at 5/9
  until the close note named the four. The r19 close note's UNRUN rows
  (`corpus/knowledge/probe-battery-r19.md:179-181`) are the idiom to
  codify.
  **Landed 09:22Z — spec verified covered:** (a) lineage row
  (`TEMPLATE:18`) now reads "freeze-1 … superseded mid-window — BR-1;
  freeze-2 07:55:58Z `e1a86777…a00a1` valid" + a new r20 hardening row
  (`:19`); (b) §5 step 5 rewritten — the stale "verified working"
  sentence is gone, replaced by both-window verification history
  (`:195-203`); (c) §5 step 3 carries the freeze-after-last-edit guard
  verbatim ("Freeze after the LAST edit (the BR-1 TOCTOU guard)",
  `:177-190` — author confirmation + double-read stability H1==H2) plus
  a bracketed-AND-line-anchored hash command and a decoy scan
  (`:139-160`), step 4 adds pre-write recompute + post-write third
  recompute (`:187, 193-195`), step 6 becomes re-freeze-only repair with
  the superseded hash preserved and the RA-3 byte-identity rule
  (`:205-213`); (d) §8 first bullet corrected to "r19: 19 requests,
  ≤240 output tokens" (`:326-328`); (e) §7 rule 1 completion gate
  (`:261-276`) + §7 rule 5 recompute-on-completion with both
  denominators preserved (`:296-302`) + §7 rule 6 multi-round provenance
  table (`:303-315`) + §9 step 7 close-the-grid checklist (`:377-392`) +
  §9 step 8 named-runner assignment (`:393-398`). No re-filed defect 11.
  [PARENT: spot-check at integration.]
- **D20-s4 (ordering-gate carryover — the r20 aggregate must be auditable
  against the r19 one):** the r19 adjudications exclude specific receipts
  from the battery aggregate (RA-3(a) pre-freeze-2 P4/P5 outcomes; RA-3(c)
  the stale-hash devinleg run; DEFECT 0 pre-run; the shim-glm reshaped
  retry for the 4x/5x rows) — `corpus/knowledge/probe-battery-r19.md:101-133,
  166-181, 285-341`. The r20 recomputation must restate those exclusions,
  not silently inherit a denominator: the honest r20 aggregate line names
  its base (the 11 r19-scored binaries) and its addition (the new P2/P8/P9
  receipts' components, P3 derived off P2's captures). [PARENT/scorer:
  confirm the r20 note carries the carried-over exclusion list.]
- **D20-s5 (per-round provenance — what "grid 9/9 with per-round
  provenance" must mean):** for each of the 9 probes the r20 note's grid
  should carry: executed-in round (r19 | r20 | r19+r20 for multi-seat
  probes), receipt file(s), executor seat, and the freeze each receipt
  verified (`e3f08a09…` for freeze-1-window runs, `e1a86777…` for
  freeze-2). A grid cell saying "done" without receipt + round is the
  defect class this round exists to close. P1's two-seat and P4(i)'s
  three-seat execution (r19 note §6 defect 7) is the precedent for why
  per-round provenance needs seat names, not just counts.
- **D20-s6 (NOT-RUN-with-reason is a legal close — the grid closes 9/9
  honestly either way):** the round's hard rules require a probe that
  cannot run as specified to be recorded NOT-RUN with reason, never
  improvised. If any of the four ends NOT-RUN, its components are
  UNPROVABLE (excluded from denominators, listed with reasons — battery
  §4 step 2) and the after-claim's "all 9 probes have executed outcomes"
  leg is **unmet in part** and must be reported as such (the r19 close's
  own verdict shape: "partially met, honestly reportable"). The grid is
  then 9/9-with-reasons, not 9/9-executed; the verdict table must not
  launder one into the other.
- **D20-s7 (freshness-event clauses live in the frozen probes):** P9 — a
  200 (or any HTTP status) on `:34113` is a freshness event: report to
  the integrator instead of absorbing a re-pin (battery §3 P9,
  `plans/probe-battery-r19.md:299-304`; TEMPLATE §9 step 1). P8 — a 200
  falsifies (store repopulated), 404/5xx falsifies the route-shape part
  (`:273-286`). If either fires, the finding is routed, not absorbed —
  same discipline as r19's serving-plane cluster.
- **D20-s8 (scribe self-disclosure, ordering-safe):** this seat issued
  zero HTTP requests to any probe target. Reads were lane files plus one
  `date -u` per session start. No predicted event was observed by the
  scribe before any runner's request; nothing this seat did can enter an
  ordering audit.
- **D20-s9 (artifact tracking — superseded by D20-s10, corrected by
  D20-s13):** at 09:15Z none of the round-20 seats had landed. The four
  completion receipts landed 09:14:49–09:19:25Z (mtimes 06:15–06:19
  local) and were caught by the 09:19–09:24Z `ls | grep` poll; the
  scorer §10 extension (mtime 09:23Z) and template revision (mtime
  09:22Z) landed DURING the subsequent polling window but were reported
  "pending" by the scribe's polls — the polls' file-freshness predicate
  was wrong (D20-s13), not the pipeline. Final state: all round-20
  artifacts landed by 09:23Z.

- **D20-s10 (the completion receipts — component outcomes, ordering gate
  clean on all four):** read in full at 09:19–09:25Z; per-probe outcomes
  in §1.1. Ordering gate: every receipt records
  `battery_sha256_at_start: e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`
  and a first_request/analysis_utc that postdates freeze-2 (07:55:58Z) —
  P8 09:14:49Z (double-read stability check, the r19 §7-step-4 practice,
  applied spontaneously by the seat), P9 09:15:04Z, P2 09:18:22–39Z
  (≥2 s gaps, one attempt per variant, no retries), P3 zero-request with
  an explicit gate-check of its source receipt's ordering. **No outcome
  precedes its prediction; no prediction edit was needed or made.** The
  single miss (3c, used-percent 7 > 2) is a route-state falsification with
  a mechanism note in the receipt (weekly plan-window consumption between
  rounds; the inertness claim — static across tiers — still holds), not a
  scoring defect. The P9 receipt additionally re-confirms the absence with
  zero-traffic corroboration (`ss -ltn` grep → 0; no llama-server process)
  and correctly does NOT trigger the freshness-event clause.
- **D20-s11 (recorded interpretation, adjudicated by the scorer):** the
  wave-generic ≤2-requests rule vs the battery's frozen 7-request P2 set
  — `probe-r19-P2-servicetier.log:10` disclosed the supersession
  in-receipt, and the scorer's §10.1 provenance note rules the same way:
  "the frozen pre-registered battery set governs (the battery IS the
  round's pre-registration — §2 rule 5 forbids widening it, and 2a's
  7-element vector is unscoreable without all 7); the seat disclosed the
  supersession in-receipt". Deviation recorded, not a breach; the
  template's §8 "budget is enumerated" clause is the standing rule.
- **D20-s12 (scribe arithmetic guard — resolved):** the sums this draft
  carried from the receipts (§1.1: 0.9700 over 9; per-component Briers)
  reproduce exactly in the scorer's §10.2 table (2a 0.0100, 2b 0.0225,
  3a 0.0225, 3b 0.0225, 3c 0.8100, 3d 0.0100, 8a 0.0100, 8b 0.0225, 9a
  0.0400 — sum 0.9700). The landed aggregate is the scorer's: 0.1495/20
  (§10.4).
- **D20-s13 (scribe polling defect — recorded, never patched):** the
  scribe's 09:25–09:47Z polls for the scorer note and template revision
  used `find <file> -newermt '2026-10-16 09:00'` — a **local-time**
  predicate (local -03 → 12:00Z), which can never fire for same-day
  09:1x–09:2xZ UTC mtimes; 36 polls returned "pending" while both files
  were already on disk (note mtime 09:23Z, template 09:22Z). The defect
  was caught only when the scribe re-checked with `stat` at 09:48Z. The
  receipts' own `ls | grep` poll (D20-s9) was name-based and unaffected.
  Lesson for the wave protocol: freshness polls must use UTC-stamped
  predicates (`-newermt` with a UTC-explicit date string or `find
  -newer <reference-file>`), or `stat`-compare mtimes directly — a
  timezone-naive freshness check silently inverts "landed" into
  "pending" and would have pushed the parent to integrate a half-tested
  round. The scribe's drafts carried the pending state as provisional
  (§5's own integration-option framing), so no false "pending" claim
  ships in any paste-ready block; this finding is the correction of
  record.
- **D20-s14 (the completion's one falsification — 3c, cross-referenced):**
  the scorer's §10.3 carries the full mechanism read (plan-window
  consumption 1 → 7 between 2026-10-15 and 2026-10-16; inertness across
  tiers holds; countdown fields move, level fields static) and prices
  the lesson: "a standing battery should re-pin such thresholds per
  instantiation rather than freeze absolute level predictions across
  days" — template material for the next instantiation, recorded here
  not patched (the frozen row stays as frozen). The scorer's §10.5
  finding 5 is the routed form.

## 4. Sources for every claim in this draft

- `plans/probe-battery-r19.md` — the frozen battery: FROZEN line `:415`
  (`e1a86777…`, re-verified byte-exact by this scribe at 09:15Z);
  §6 prediction table `:354-390` (23 binary + 7 numeric; completion rows
  2a/2b `:364-365`, 3a–3d `:366-369`, 8a/8b `:385-386`, 9a `:387`);
  §3 P2 `:128-146` (7 requests), P3 `:149-161` (0 extra), P8 `:273-286`
  (1 request), P9 `:288-304` (1 request + freshness-event clause);
  §7 step 4 `:404-406` (the re-verify-before-write seed text); §7.1
  freeze record `:417-507`.
- `corpus/knowledge/probe-battery-r19.md` — the r19 close note: §2 UNRUN
  rows `:179-181` (nine components named); §3 tally `:183-194`; §4 (i)
  aggregate `:196-203`; §7 proxy inputs `:343-355`; defect 11 (template
  staleness) `:333-336`; §8 honest limits `:357-401` (limit 3: coverage
  partial, P9 unrealized) — **plus the r20 §10 extension** (scored
  09:21:55Z, mtime 09:23Z): §10 preamble `:425-437` (premise re-verified
  09:14:31Z, battery mtime check), §10.1 ordering gate `:439-462`, §10.2
  new components `:464-489`, §10.3 verdicts + full-grid tally
  `:491-514`, §10.4 recomputed aggregate `:516-549`, §10.5 findings
  `:551-577`, §10.6 proxy inputs `:579-596`. Cosmetic citation slip
  filed by the scribe: §10.6(b) says "§8 completion gate, line 260" —
  the completion gate is §7 rule 1 (line 261 of the revised template);
  line 260 is §7's header.
- `plans/probe-battery-TEMPLATE.md` — **r19 state (superseded this
  round)**: `:17` stale lineage ref, §5 without the TOCTOU guard,
  `:242` stale budget — all recorded as D20-s3's spec. **Revised state
  (landed 09:22Z, 437 lines)**: lineage rows `:17-19` (freeze-1 marked
  superseded; r20 hardening row), §5 step 3 guard + decoy scan
  `:137-190`, step 4 pre/post-write recompute `:187-195`, step 5
  both-window history `:195-203`, step 6 re-freeze doctrine `:205-213`,
  §7 rule 1 completion gate `:261-276`, rule 5 recompute-on-completion
  `:296-302`, rule 6 provenance table `:303-315`, §8 corrected budget
  `:326-328`, §9 step 7 close-the-grid checklist `:377-392`, step 8
  named-runner assignment `:393-398`, §10 wave-skew + template-staleness
  pricing `:417-437`.
- `SCORECARD.md:33-46` (proxy (a)–(c) definitions), `:416-454` (round-19
  section — 5 executed / 4 UNRUN named, mean Brier 0.1836/11,
  ADMIT-with-correction).
- `LOG.md` §19 (round-19 entry; the paste-target idiom for this round's
  log-entry draft).
- `corpus/lessons/2026-10-16-round19-freeze-chain.md` — the r19 lesson
  land (the freeze-chain failure modes the template guards must encode).
- `corpus/lessons/2026-10-16-round20-grid-closure.md` — the r20 lesson
  land (lessons-distiller seat): "a battery with unrun probes is an open
  battery" — the selection-not-sampling read of why 0.1836/11 and
  0.1495/20 are different numbers (runner-seat self-picking skew), with
  every number reproduced from the §2/§10.2 tables before citing.

## 5. Status at scribe handoff (2026-10-16T09:55Z)

**All round-20 artifacts landed and covered by this draft:**

- the r19 battery + freeze (`e1a86777…`, re-verified by this scribe at
  09:15Z, by every executor seat pre-request, and by the scorer at
  09:14:31Z — the battery file untouched since the r19 freeze record);
- the 15 r19 receipts + **4 completion receipts**
  (`probe-r19-P2-servicetier.log`, `probe-r19-P3.log`,
  `probe-r19-P8-kimi-code-auth.log`, `probe-r19-P9-absent-port.log`;
  outcomes in §1.1, findings D20-s10…s14);
- the scorer's §10 extension (`corpus/knowledge/probe-battery-r19.md`,
  scored 09:21:55Z, mtime 09:23Z): ordering gate PASS ×4, 9 components
  scored (8 HIT / 3c MISS), grid 9/9 with per-round provenance,
  aggregate recomputed 0.1495/20;
- the template revision (`plans/probe-battery-TEMPLATE.md`, 437 lines,
  mtime 09:22Z): freeze-after-last-edit guard + completion gate +
  multi-round provenance table + close-the-grid checklist — D20-s3
  (a)–(e) verified covered;
- the r20 lesson land (`corpus/lessons/2026-10-16-round20-grid-closure.md`,
  lessons-distiller seat): the selection-not-sampling read of the
  partial-vs-completed aggregate, numbers reproduced from §2/§10.2.

**Nothing is pending from the round-20 seat set.** The parent's
integration steps remain: LOG.md §20 entry, SCORECARD.md round-20
section, the fleet report, index/commit — all drafted in this directory
(log-entry-draft.md, report-draft.md, §2 above).

[Scribe polling-defect note for the audit trail: the "pending" states
this draft reported between 09:25Z and 09:47Z were a scribe tooling
error (local-time `-newermt` predicate, D20-s13), not pipeline state —
the landed artifacts postdate the receipts and predate 09:48Z. Every
paste-ready block in §2 quotes only landed artifacts.]
