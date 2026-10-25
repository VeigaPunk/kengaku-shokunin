# log-entry-draft — kengaku round 19

Scribe seat, round-19 goal wave. Written 2026-10-16, updated through
07:57Z at HEAD `05cb955`. **This file writes nothing** — `LOG.md` is
PARENT-owned; the block below is a paste-ready entry in the round-15…18 LOG
idiom (`## <n> — <title>` section with bullets; see `LOG.md` §15–§18).
`[PARENT]` markers and `{{PLACEHOLDER}}` slots must be resolved from landed
artifacts at integration time; every resolved value must quote its receipt
(lane rule: "Every change appends a LOG.md entry with the evidence that
motivated it"; "Never fabricate domain knowledge").

---

```markdown
## 19 — standing probe battery: live-route calibration, pre-registered and scored

2026-10-16 · calibration axis-move · 32-seat flash wave (zai-bucket lane) ·
starting commit `05cb955`.

- **Falsifiable claim (before, pre-registered in the battery itself):**
  `plans/probe-battery-r19.md` §0 — the calibration proxy (probes with
  predictions filed before the first request, scored at close) ran 0/1, 1/1,
  0/0, 1/1 across rounds 8–11 (`SCORECARD.md:34-37`): intermittent, ad hoc;
  no standing battery or reusable template existed at round start (verified:
  `ls plans/` at 2026-10-16T07:44:09Z → only `wwkd-round-16-recensus.md` +
  `wwkd-round-17-coverage.md`; scribe re-verified independently at 07:36Z).
- **Battery:** 9 falsifiable live-route probes (P1–P9), predictions frozen
  with UTC before any request — first freeze `FROZEN: 2026-10-16T07:52:04Z
  sha256:e3f08a09…` (stale, BR-1), repaired by re-freeze `FROZEN:
  2026-10-16T07:55:58Z
  sha256:e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`
  (frozen set: 23 binary + 7 numeric components, 19 HTTP requests; the
  scribe independently recomputed both §7 hashes). Seat-level
  pre-registrations also filed: `probe-r19-shim-ds-predictions.log` (S1–S8,
  07:43:30Z, block sha256 `78de64d9…`), `probe-r19-shim-glm-predictions.log`
  (G1–G8, 07:55:05Z, prereg `a1674cfc…`), `probe-r19-hyper-predictions.log`
  (H1–H10, 07:56:41Z, block `4fa6e0e6…`), `probe-r19-devin-shim-seat.log`
  (D1–D5, 07:53:40Z).
- **Freeze saga (recorded breach + repair, never patched):** the registrar's
  first freeze (`FROZEN: 2026-10-16T07:52:04Z sha256:e3f08a09…`) hashed the
  pre-rebase bundle while the battery-author's v2 re-base (P4/P5 re-framed to
  the M7/M9 post-reorder serving plane — the plan's own §0 revision note:
  "after runner-seat receipts revealed" the reorders) landed afterwards;
  six seats executed against the stale freeze in the 07:52:25–07:54:38Z
  window, every one recording `battery_sha256_at_start: e3f08a09…`. Repair:
  BR-1 (plan §7.1) + re-freeze `FROZEN: 2026-10-16T07:55:58Z
  sha256:e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`
  (scribe-verified with the plan's own §7 command). Consequence the scorer
  must carry: the re-based P4/P5 predictions are **outcome-informed** for
  every component whose outcome predates 07:55:58Z — they are recorded
  findings, not forecast skill; and §7.1's "no runner executions between
  the stale freeze and the re-freeze" is falsified by the same logs' mtimes
  (full receipt chain:
  `.ufo/rounds/round-19/goal-wave/scorecard-verdict-draft.md` D-s6).
- **Execution receipts:** `corpus/evidence/probe-r19-*.log` — {{N_LOGS}}
  logs, each with UTC stamps, exact commands, exits, response excerpts
  (credential values never captured; header names and length markers only).
  {{RUNNER_LOG_LIST — one bullet per log: seat, probes covered, outcome
  class; at scribe last check: shim-ds (S1–S8, 9/9 HIT, mean Brier 0.0050
  over 8 binary terms), quota-23 (P1 1a–1f all hit, implied resets within
  ±1 s of the r18 anchors), listing-mismatch (P1 duplicate — see breach
  list), P1-key1 (addendum, 200), P6-zai (429 rate-limit code 1302 — 6a/6b
  miss, 6c unprovable), opencode (DEFECT 0 pre-run), devin (seat-level:
  D1 hit, D2 MISS 400, D3 hit, D4 range-hit 485, D5 unrecorded), P4-glm +
  P5-glm (both requests 400 terminal — zai 429 + devin temperature
  rejection; 4a/4c-glm/5a UNPROVABLE on their receipts), shim-glm (G1–G8:
  mean Brier 0.0772 over 7 scored; battery 4a falsified via the leg-change
  path, 5a burst HIT; F-2 temperature-rejection defect), hyper (H1–H10:
  12/13 hit, mean Brier 0.0332 over 11 scored binaries; the one miss is the
  designed H8 coin-flip — burst-lane prior falsified as per-model, not
  per-lane; prompt-billing drift 31→48 routed to the serving plane).}}
- **Scored at close:** `corpus/knowledge/probe-battery-r19.md` — ordering
  gate {{ORDERING_GATE_VERDICT}}; per-component scores {{SCORING_SUMMARY}};
  aggregate calibration read (measurements, not axis scores):
  {{AGGREGATE_READ — mean Brier with the 0.25 always-0.5 reference beside
  it; mean abs-error per unit; range hit-rate; pass/fail/unprovable counts}}.
- **Template:** `plans/probe-battery-TEMPLATE.md` — host-agnostic battery
  template for future rounds (landed by 08:07Z): §0–§8 are the instrument
  (disclosure-mandatory round header, probe schema, prediction component
  schema, freeze discipline, receipt schema, scoring rules, quota
  etiquette), §9 the instantiation checklist, §10 the instrument's known
  defects. Its r19 citations are stale in three places (superseded
  `e3f08a09…` freeze cited at :17; §5 omits the BR-1-closing
  re-verify-before-write step; breach doctrine says errata-only where r19's
  actual repair was a re-freeze; :241 quotes the superseded 18/≤232 budget)
  — scribe D-s14, recorded for the template author.
- **Breaches and defects (recorded, never patched):**
  {{BREACH_LIST — the scribe's standing list at 08:02Z, full receipts in
  `.ufo/rounds/round-19/goal-wave/scorecard-verdict-draft.md` §3:
  (1) BR-1 stale freeze + outcome-informed v2 re-base (D-s6, above);
  (2) duplicate P1 — two seats ran the full 4-request set 21 s apart, 8
  requests where the plan budgeted 4; battery-governed total exceeds §2's
  binding ≤20 (D-s7);
  (3) runner-leg-opencode DEFECT 0 — two live requests 07:45:00–07:45:04Z
  before the battery existed, self-reported, gate contained 07:46:36Z,
  excluded from the aggregate (`probe-r19-opencode-health.log:8-42`);
  (4) shim-glm reshaped retry after a 400 (§2 rule 3), transparently
  documented, isolating `temperature` as the devin leg's rejected field
  (D-s11);
  (5) P1-key1 addendum filed outside §6 with prediction_filed_utc ==
  first_request_utc at one-second resolution (D-s8, r12 `<=` convention);
  (6) devin D5 TTFT not derivable from the landed log (D-s10);
  (7) serving-plane cluster routed to the integrator: shim redeploy
  (devin-openai-shim/2, 2026-10-15T17:16:22Z), devin-leg temperature
  rejection 400-terminal through the glm cascade, status masking, zai-leg
  429 pressure at ~36% serve under wave load, hyper prompt-billing drift
  31→48 on identical COUNT_PROMPT (D-s12);
  (8) template sync defects: superseded freeze hash cited as the lineage
  credential, §5 missing the BR-1 re-verify-before-write step, breach
  doctrine errata-only vs the actual re-freeze repair, stale budget figures
  (D-s14);
  (9) cosmetic: stray `EOF` prefix on the original shim-ds digest line
  (superseded); plan §0/§2/§6 token numbers reconcile as 232 serviced /
  240 incl. warm-up / 256 binding cap but the plan never states the
  reconciliation; P4-devinleg log's duplicate header blocks + runner
  NameError crash with data still captured (D-s13).}}
- **Serving-plane findings routed, not absorbed:** {{ROUTING_LIST — the
  confirmed leg-order drift (P4 drift note: r18 D9 numbers describe the
  pre-reorder state; M7/M9 reorders are operator serving-plane facts) and
  any P9 `:34113` restoration go to the integrator/operator per
  `PROVINCE.md` §Refusals; quote the scorer note's §5 findings}}.
- **Ledger:** {{SCORECARD_VERDICT_LINE — from
  `.ufo/rounds/round-19/goal-wave/scorecard-verdict-draft.md` §2, verdicts
  per gate, no scalar axis scores}}. Index parity at close:
  {{INDEX_PARITY — knowledge/lessons/evidence rows vs files per
  `corpus/README.md`; the scorer note needs a knowledge index row}}. Next
  move (§Planned): {{NEXT_MOVE — parent's judgement; the template makes the
  standing-battery leg repeatable}}.
```

---

**Fill sources:** battery plan `plans/probe-battery-r19.md` (frozen e3f08a09,
amended 8446efc7); runner logs `corpus/evidence/probe-r19-*.log`; scorer note
`corpus/knowledge/probe-battery-r19.md`; template
`plans/probe-battery-TEMPLATE.md`; the scribe's verdict draft (§2–§3 of
`scorecard-verdict-draft.md` in this directory). Dates: the lane's LOG dates
are local dates of the work; this round's work spans 2026-10-16 UTC (local
-03). The parent picks the entry date at commit time (round-14 precedent,
`r14-scribe-drafts.md` §6 item 7).
