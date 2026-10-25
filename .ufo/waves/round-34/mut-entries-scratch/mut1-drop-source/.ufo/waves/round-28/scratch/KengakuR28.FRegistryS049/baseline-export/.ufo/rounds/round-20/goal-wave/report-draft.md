# report-draft — kengaku round 20 (fleet report skeleton)

Scribe seat, round-20 goal wave. Written 2026-10-16, updated through
09:55Z at HEAD `f330e2b` (all round-20 artifacts landed and folded in:
4 completion receipts, scorer §10 extension scored 09:21:55Z, template
revision landed 09:22Z). **This file writes
nothing** — the round report is PARENT-owned and lands at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-20/kengaku.md` (the
round-18/19 precedent: the lane's fleet report lives in the fleet repo).
The skeleton carries the round-prompt's four required sections in order
(work performed / landed changes / before→after measurements / SHONEN —
`../templates/round-prompt.md` §4). A contentless report counts the round
as failed, so every `[PARENT]` slot must resolve to a real receipt or the
bullet must state its absence with polling evidence — placeholders must
not ship.

---

```markdown
# SHONEN — Round 20: battery completion (calibration axis-move)

Starting commit `f330e2b`. Lane: kengaku-shokunin (LLM/model research &
evaluation). Wave: 32-seat flash (zai-bucket). One axis-move: calibration —
close the r19 battery's grid: 5/9 probes executed → 9/9, scored against
the SAME frozen predictions (no prediction edits), aggregate recomputed
across all executed binaries, template gains the freeze-after-last-edit
guard + the unrun-completion checklist. No gate/tool changes; no new
battery probes.

## Work performed

- Battery completion (P2/P3/P8/P9 executors): all four UNRUN probes from
  r19 executed exactly as specified in the frozen battery
  (`plans/probe-battery-r19.md` §3), every receipt freeze-verified
  pre-request against `e1a86777…`. Component outcomes (receipt-verbatim;
  official scoring is the scorer's): P2: status vector
  [200,200,400,200,400,400,400] exact (2a/2b HIT); P3 (derived off P2's
  captures): 3a/3b/3d HIT, 3c MISS (used-percent 7/7/7 > frozen ≤2 —
  plan-window consumption between rounds, inertness across tiers holds);
  P8: 401 with both predicted strings (8a/8b HIT); P9: connection
  refused, curl exit 7 (9a HIT, freshness clause NOT triggered).
  Receipt-level Brier sum 0.9700 over 9 components (8 hit / 1 miss);
  receipts: `corpus/evidence/probe-r19-P2-servicetier.log`,
  `probe-r19-P3.log`, `probe-r19-P8-kimi-code-auth.log`,
  `probe-r19-P9-absent-port.log`. Scorer verdicts (§10.3): P2 PASS, P3
  FAIL (3c), P8 PASS, P9 PASS — full grid 7 PASS / 2 FAIL / 0 UNRUN.
- Prediction integrity: predictions FROZEN from r19, not edited —
  `FROZEN: 2026-10-16T07:55:58Z sha256:e1a86777…` re-verified byte-exact
  at 09:15Z (scribe) and 09:14:31Z (scorer §10 premise check, with the
  battery file's mtime unchanged at 08:06:37Z since the r19 freeze
  record); every executor seat verified the same hash pre-request (P8
  with a double-read stability check). No prediction edit was made.
- Scoring at close: `corpus/knowledge/probe-battery-r19.md` r20 addendum —
  the new receipts scored against the same §6 rows (2a/2b, 3a–3d, 8a/8b,
  9a), the aggregate recomputed across all executed binaries with the
  0.25 always-0.5 reference beside it, the grid table 9/9 with per-round
  provenance (r19 vs r20 per probe, receipt + seat + freeze per cell),
  the r19 exclusions restated. No scalar axis verdicts.
  Ordering gate (§10.1): PASS on all four completion receipts —
  `frozen_utc 07:55:58Z < first_request_utc` in every case,
  `battery_sha256_at_start == e1a86777…` verified pre-request; no
  ordering breach, no new defects.
- Template revision: `plans/probe-battery-TEMPLATE.md` (landed 09:22Z,
  308 → 437 lines) — the freeze-after-last-edit guard (§5 step 3:
  author-confirmation + double-read stability + bracketed-AND-
  line-anchored hash command with a decoy scan; step 4: pre-write
  recompute + post-write third recompute; seed text
  `plans/probe-battery-r19.md:404-406`) and the unrun-completion
  discipline (§7 rule 1 completion gate with the three legal closes —
  run-in-round cheapest-first / carry against the SAME freeze /
  NOT-RUN-with-reason; §7 rule 5 recompute-on-completion preserving both
  denominators; §7 rule 6 multi-round provenance table; §9 step 7
  close-the-grid checklist; §9 step 8 named-runner assignment). The
  stale `e3f08a09…` citations (:17/:160) and stale budget (:242) are
  replaced; scribe verified all five D20-s3 spec items covered.
- Breach handling: no ordering breach and no new defects in the
  completion (scorer §10.1); recorded deviations and findings: P2's
  7-request supersession of the wave's generic ≤2 cap (disclosed
  in-receipt, adjudicated in §10.1's provenance line — the frozen
  battery set governs); 3c's threshold-carrying miss (absolute level
  frozen across a plan-window boundary — §10.3 prices the lesson:
  re-pin levels per-run or predict deltas; the frozen row stays as
  frozen); scribe self-filed polling defect (local-time `-newermt`
  predicate reported landed artifacts pending for ~25 min — D20-s13,
  no paste-ready block shipped the false state); cosmetic citation slip
  in the note's §10.6(b) ("§8 completion gate" → §7 rule 1, line 261).
  The r19 exclusions (RA-3(a)/(c), DEFECT 0, reshaped-retry rows) stand
  unchanged. Recorded, never patched.

## Landed changes

- `corpus/evidence/probe-r19-P{2,3,8,9}*.log` — 4 completion receipts
  (`probe-r19-P2-servicetier.log`, `probe-r19-P3.log`,
  `probe-r19-P8-kimi-code-auth.log`, `probe-r19-P9-absent-port.log`),
  extending the r19 battery's evidence set from 15 to 19 logs.
- `corpus/knowledge/probe-battery-r19.md` — r20 §10 extension: grid 9/9
  with per-round provenance + recomputed aggregate 0.1495/20 (scorer
  seat, scored 09:21:55Z).
- `plans/probe-battery-TEMPLATE.md` — freeze-after-last-edit guard +
  completion gate + provenance table + close-the-grid checklist
  (template-reviser seat, 437 lines).
- `corpus/lessons/2026-10-16-round20-grid-closure.md` — the completion
  lesson (lessons-distiller seat).
- `.ufo/rounds/round-20/goal-wave/` — scribe drafts (this round's three
  files).
- [PARENT: commit hash(es) carrying the above; LOG.md §20 entry;
  SCORECARD.md round-20 section — both drafted in
  `.ufo/rounds/round-20/goal-wave/`]

## Before → after measurements

- Before (re-verified at 09:15Z): 5/9 probes executed (P1, P4, P5, P6,
  P7), 4 named-UNRUN; mean Brier 0.1836 over 11 gate-passing binaries
  (9 hit / 2 miss — the two zai misses carry 82.9% of the mass);
  `corpus/knowledge/probe-battery-r19.md` §3/§4; template without either
  new guard.
- After: grid **9/9 executed with per-round provenance** (scorer §10.4
  iv: P1/P4/P5/P6/P7 in r19, receipts 08:23Z close; P2/P3/P8/P9 in r20,
  receipts 09:14:49–09:19:25Z) — 7 PASS / 2 FAIL / 0 UNRUN (P5 keeps its
  r19 caveat); recomputed mean Brier **0.1495 over n = 20 executed
  binaries** (sum 2.9897 = 2.0197/11 + 0.9700/9), always-0.5 reference
  0.25 beside it; 17 hits / 3 misses carrying 83.1% of the mass;
  per-wave split r19-close 0.1836/11 → completion 0.1078/9; reliability
  bands 9/12 · 7/7 · 1/1, predicted mean 0.8645 vs observed 0.8500;
  mean abs-error per unit unchanged (the completion adds no numeric
  rows); range/band hit-rate 5/5 scoreable; ordering gate PASS ×4 with
  no new defects. Measured against commit {{CLOSE_COMMIT}}.
- Standing-battery property (the round's structural claim): the template
  now carries the completion discipline — a future round that leaves
  probes unrun must close them as NOT-RUN-with-reason or carry them
  against the ORIGINAL freeze (§7 rule 1, `:261-276`; §9 step 7,
  `:377-392`), a completing round recomputes the aggregate across all
  executed binaries with both denominators preserved (§7 rule 5,
  `:296-302`), fills the multi-round provenance table (§7 rule 6,
  `:303-315`), and a freeze can no longer race its own last edit (§5
  step 3 freeze-after-last-edit guard, `:137-190`).

## SHONEN

- [~] Real decision tables/error patterns/checklists/sources: the template
  gains the guards this round (freeze-after-last-edit §5 step 3
  `:137-190`; completion gate §7 rule 1 `:261-276`; provenance table §7
  rule 6 `:303-315`; close-the-grid checklist §9 step 7 `:377-392`) — a
  checklist-class change to the standing instrument, verified landed by
  the scribe (D20-s3 (a)–(e)).
- [~] End-to-end domain task executed and logged: the battery completion
  is a live route-state measurement round; LOG.md §20 entry drafts at
  `.ufo/rounds/round-20/goal-wave/log-entry-draft.md`. [PARENT: cite the
  landed LOG entry once integrated]
- [~] Instructions executable without oral context: the battery plan +
  revised template are in-repo, host-agnostic, and self-gating (FROZEN
  line + ordering audit + completion checklist). [PARENT: marks stay [~]
  without a non-author verifier]
- [~] No cross-domain bleed: no freshness event fired (P8 401 / P9
  connection-refused both matched their frozen predictions — §10.5
  finding 4 records the re-confirmation) and no serving-plane surprise
  arose; the one falsification (3c) is a route-state threshold drift
  recorded in the note, not absorbed. No foreign scope absorbed.
```

---

**Parent fill rules:** every pipeline stage landed (4 completion receipts,
scorer §10 at 09:23Z, template revision at 09:22Z); the remaining
`[PARENT]` markers are genuine parent-owned values — the close commit
hash(es), the LOG/SCORECARD/report integration citations, the grader
re-run, the axis verdict lines, and index parity. Quote landed artifacts
verbatim; do not recompute scorer numbers.
