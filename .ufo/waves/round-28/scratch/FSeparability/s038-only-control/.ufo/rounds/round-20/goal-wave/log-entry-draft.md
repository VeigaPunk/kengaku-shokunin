# log-entry-draft — kengaku round 20

Scribe seat, round-20 goal wave. Written 2026-10-16, updated through
09:55Z at HEAD `f330e2b` (all round-20 artifacts landed and folded in:
4 completion receipts, scorer §10 extension, template revision).
**This file writes nothing** —
`LOG.md` is PARENT-owned; the block below is a paste-ready entry in the
round-15…19 LOG idiom (`## <n> — <title>` section with bullets; see
`LOG.md` §19). `[PARENT]` markers and `{{PLACEHOLDER}}` slots must be
resolved from landed artifacts at integration time; every resolved value
must quote its receipt (lane rule: "Every change appends a LOG.md entry
with the evidence that motivated it"; "Never fabricate domain knowledge").
Placeholders must not ship — an unresolved slot becomes an absence
statement with polling evidence.

---

```markdown
## 20 — battery completion: the r19 grid closes 5/9 → 9/9 under the same frozen predictions

2026-10-16 · calibration axis-move (battery completion) · 32-seat flash
wave (zai-bucket lane) · starting commit `f330e2b`.

- **Falsifiable claim (before):** the r19 standing battery stood at 5/9
  probes executed (P1, P4, P5, P6, P7) with 4 named-UNRUN (P2, P3, P8, P9
  — named, not hidden), aggregate computed over 11 gate-passing binaries
  (mean Brier 0.1836), and the template lacked the freeze-after-last-edit
  guard and the unrun-completion checklist. Scribe re-verified at
  2026-10-16T09:15Z: 15 receipts with no `probe-r19-P[2389]*` log, scorer
  note at r19 close state, template unrevised, and the freeze recompute
  byte-exact — `sed -n '1,/FROZEN-PREDICTIONS-ANCHO[R]/p'
  plans/probe-battery-r19.md | sha256sum` →
  `e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1` ==
  the FROZEN line at `plans/probe-battery-r19.md:415`.
- **Same frozen predictions (the round's load-bearing premise):** no
  prediction edit this round — the §6 rows the four probes score
  (2a/2b, 3a–3d, 8a/8b, 9a) were frozen in r19 and predate every r20
  request by >1 h. Verified three ways: the scorer's premise check at
  09:14:31Z (freeze recompute == FROZEN line; battery mtime 08:06:37Z
  untouched since the r19 freeze record —
  `corpus/knowledge/probe-battery-r19.md:429-434`); the scribe's 09:15Z
  independent recompute (`e1a86777…` byte-exact); every executor seat's
  own pre-request verification (`battery_sha256_at_start` in all four
  receipts, P8 with a double-read stability check).
- **Completion receipts:** `corpus/evidence/probe-r19-P{2,3,8,9}*.log` —
  4 new receipts extending the r19 battery's evidence to 19, each with UTC
  stamps, exact commands, exits, response excerpts (credential values
  never captured; header names and length markers only), and a pre-request
  freeze verification of `e1a86777…` (P8 with a double-read stability
  check). Component outcomes (receipt-verbatim; official scoring is the
  scorer seat's):
  - **P2** (codex `service_tier` set, 7 POSTs 09:18:22–39Z, ≥2 s gaps, no
    retries): status vector `[200,200,400,200,400,400,400]` **exact match**
    (2a HIT); all four 400 bodies name `Unsupported service_tier: <value>`
    (2b HIT). Serviced legs omit/default/priority, ≤16 output tokens each.
  - **P3** (zero-request, derived off P2's captures): 3a HIT (final echo
    `default` ×3, `priority` never appears, echo sequences
    byte-identical); 3b HIT (credits 62500.0000000000 ×3); **3c MISS**
    (`x-codex-primary-used-percent` 7/7/7 > frozen ≤2 — the receipt's
    mechanism note: the weekly plan window had consumed 7% by 09:18Z vs
    the r18 basis reading 1 on 2026-10-15; the inertness claim itself
    holds — 7/7/7 static across tiers, no per-request movement); 3d HIT
    (usage input_tokens 7/7/7 identical).
  - **P8** (`managed:kimi-code`, 1 unauthenticated GET 09:14:49Z): 401
    `invalid_authentication_error` / "Invalid Authentication" (8a HIT,
    8b HIT — both predicted strings present). Auth-dead state re-confirmed
    same-day; zero quota spent.
  - **P9** (`:34113`, 1 localhost GET 09:15:04Z): connection refused,
    curl exit 7, http 000, 3 ms (9a HIT); freshness-event clause **not
    triggered** — no HTTP status of any kind; absence re-confirmed with
    zero-traffic corroboration (`ss -ltn` → no listener; no llama-server
    process).
  - Receipt-level Brier sum over the 9 new components: **0.9700**
    (8 hits / 1 miss — 3c carries 0.8100 of it, 83.5%).
- **Scored at close (aggregate recomputed across all executed binaries):**
  `corpus/knowledge/probe-battery-r19.md` §10 (scored 09:21:55Z) —
  ordering gate PASS on all four completion receipts (§10.1: every
  `battery_sha256_at_start == e1a86777…` verified pre-request;
  `frozen_utc 07:55:58Z < first_request_utc` in every case; no ordering
  breach, no new defects; P2's 7-request supersession of the wave's
  generic ≤2 cap disclosed in-receipt and ruled in the note's provenance
  line); newly scored components (§10.2): 2a 0.0100, 2b 0.0225, 3a
  0.0225, 3b 0.0225, **3c 0.8100 MISS**, 3d 0.0100, 8a 0.0100, 8b
  0.0225, 9a 0.0400 — sum 0.9700 over 9, UNPROVABLE: none added;
  full-grid verdicts (§10.3): **7 PASS, 2 FAIL, 0 UNRUN** — grid **9/9
  executed with per-round provenance** (P1/P4/P5/P6/P7 in r19; P2/P3/
  P8/P9 in r20, receipts 09:14:49–09:19:25Z); aggregate recomputed
  (§10.4): **mean Brier 0.1495 over n = 20 scored binaries (sum 2.9897 =
  2.0197/11 + 0.9700/9), always-0.5 reference 0.25 beside it as
  comparison, not a grade**; 17 hits / 3 misses carrying 83.1% of the
  mass (6a+6b zai rate-limit, 3c used-percent drift); per-wave split
  r19-close 0.1836/11 → completion 0.1078/9; reliability bands 9/12 ·
  7/7 · 1/1; predicted mean 0.8645 vs observed 0.8500 — near-flat;
  range/band hit-rate 5/5 scoreable (unchanged — the completion adds no
  numeric rows); the partial-close reading is preserved beside the
  completed grid with both denominators (the template's §7 rule 5
  idiom). Measurements, not axis scores.
- **Template revised:** `plans/probe-battery-TEMPLATE.md` (landed 09:22Z,
  308 → 437 lines) gains the freeze-after-last-edit guard (§5 step 3:
  author-confirmation + double-read stability H1==H2 + a
  bracketed-AND-line-anchored hash command with a decoy scan; step 4:
  pre-write recompute + post-write third recompute — the r19 plan's §7
  step 4 seed hardened into procedure) and the unrun-completion
  discipline (§7 rule 1 completion gate: run-in-round cheapest-first /
  carry-to-next-instantiation-against-the-SAME-freeze / NOT-RUN-with-
  reason; §7 rule 5 recompute-on-completion with both denominators
  preserved; §7 rule 6 multi-round provenance table; §9 step 7
  close-the-grid checklist; §9 step 8 named-runner assignment at
  dispatch). The stale `e3f08a09…` citations (:17/:160) and the stale
  budget (:242) are replaced (lineage row marks freeze-1 superseded —
  BR-1; §8 quotes 19 requests/≤240 tokens). Scribe verified the landed
  revision covers all five spec items (D20-s3 (a)–(e),
  scorecard-verdict-draft.md §3).
- **Freshness events:** none fired — P8's 401 and P9's connection
  refusal both matched their frozen predictions, so the battery's
  freshness clauses did not trigger; the outcomes are same-day
  re-confirmations of declared states (auth-dead `managed:kimi-code`;
  absent `:34113`, corroborated zero-traffic: no listener, no
  llama-server process, 09:15:14Z). The r19 finding-7 gap (P9 never ran)
  is closed as a re-confirmation, not a restore (scorer §10.5 finding 4).
- **Breaches and defects (recorded, never patched):** none in the
  completion itself — scorer §10.1: "No ordering breach; no new
  defects." Recorded deviations and scribe findings: (1) P2's 7 POSTs
  exceed the wave's generic ≤2-requests-per-probe rule — the frozen
  pre-registered battery set governs, disclosed in-receipt
  (`probe-r19-P2-servicetier.log:10`) and adjudicated in the note's
  §10.1 provenance line; (2) 3c's miss is a threshold-carrying
  calibration hazard (absolute level ≤2 frozen across a plan-window
  boundary; the note §10.3 prices the lesson for the next instantiation
  — re-pin levels per-run or predict deltas); (3) scribe self-filed:
  the scribe's own freshness polls used a local-time `-newermt`
  predicate that never fired, reporting landed artifacts "pending" for
  ~25 min (D20-s13 in scorecard-verdict-draft.md — no paste-ready block
  shipped the false state); (4) cosmetic: the note's §10.6(b) cites
  "§8 completion gate, line 260" — the gate is §7 rule 1 at line 261.
  The r19 exclusions (RA-3(a)/(c), DEFECT 0, reshaped-retry rows) stand
  unchanged — no r20 seat re-ran those probes (§10.2 UNPROVABLE note).
- **Ledger:** verdicts per gate drafted at
  `.ufo/rounds/round-20/goal-wave/scorecard-verdict-draft.md` §2
  (calibration cell carries the scorer §10 measurements: grid 9/9,
  mean Brier 0.1495/20 vs the 0.25 reference; novelty/operability/depth/
  adjacency unchanged; freshness = same-day re-confirmations, no event;
  no scalar axis scores) — [PARENT: the axis verdict lines and the
  admission decision are the parent's judgement]. Index parity at close:
  the r20 note is an addendum to an already-indexed knowledge file, so
  no new knowledge row is expected; battery/template are already indexed;
  [PARENT: verify per `corpus/README.md` and add any required row]. Next
  move (§Planned): [PARENT: the standing battery is now a repeatable
  9/9-closable instrument with completion discipline baked into the
  template; the note §10.5 finding 5 prices the threshold-carrying
  hazard for the next instantiation].
```

---

**Fill sources:** the r19 battery `plans/probe-battery-r19.md` (frozen
`e1a86777…`); the four completion receipts
`corpus/evidence/probe-r19-P{2,3,8,9}*.log`; the r20 scorer §10 extension
`corpus/knowledge/probe-battery-r19.md:425-596`; the revised template
`plans/probe-battery-TEMPLATE.md`; the r20 lesson
`corpus/lessons/2026-10-16-round20-grid-closure.md`; the scribe's verdict
draft (§2–§3 of `scorecard-verdict-draft.md` in this directory). Dates:
the lane's LOG dates are local dates of the work; this round's work spans
2026-10-16 UTC (local -03). The parent picks the entry date at commit time
(round-14 precedent, `corpus/evidence/round14-fleet/r14-scribe-drafts.md`
§6 item 7).
