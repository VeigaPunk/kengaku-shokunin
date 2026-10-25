# log-entry-draft — kengaku round 21

Scribe seat, round-21 goal wave. Written 2026-10-16, starting state
captured 10:04–10:08Z at HEAD `3688f76` (round-20 records; r20 evidence
commit `af0e3e6`). **This file writes nothing** — `LOG.md` is
PARENT-owned; the block below is a paste-ready entry in the
round-19/20 LOG idiom (`## <n> — <title>` section with bullets; see
`LOG.md` §19/§20). `[PARENT]` markers and `{{PLACEHOLDER}}` slots must be
resolved from landed artifacts at integration time; every resolved value
must quote its receipt (lane rule: "Every change appends a LOG.md entry
with the evidence that motivated it"; "Never fabricate domain knowledge").
Placeholders must not ship — an unresolved slot becomes an absence
statement with polling evidence. No scalar axis verdicts.

---

```markdown
## 21 — blind cascade-leg attribution instrument (novelty axis-move)

2026-10-16 · novelty axis-move (N1: blind leg attribution with
shim-journal ground truth — instrument-level novelty,
phenomenon-incremental) · 32-seat flash wave (zai-bucket lane) ·
starting commit `3688f76`.

- **Falsifiable claim (before):** no instrument exists that can attribute
  which cascade leg served a given response without operator-side ground
  truth. Scribe re-verified at 2026-10-16T10:04–10:08Z: no `tools/` dir;
  zero `attrib*` files in `plans/`, `corpus/knowledge/`,
  `corpus/evidence/`; the only in-repo `.py`/`.sh` `attribut` hits are
  r12 error-record bookkeeping (`ERROR RECORD UNATTRIBUTED`,
  `corpus/evidence/round12-ladder/recompute_r12.py:53-55`) — not
  cascade-leg attribution. N1 was registered by the r20 novelty scout
  after pricing latency-fingerprinting OUT of novelty (crowded published
  space) — `.ufo/rounds/round-20/kengaku.md:36-37`.
- **Frozen feature table (frozen BEFORE any trial):**
  `plans/attrib-r21-frozen.md` — latency band / header tells /
  error-wording shape / body schema, weights pre-registered, accuracy
  bar 0.80 with `min_scored_trials_per_shim: 20` and denominator pinned
  pre-trial, request set enumerated (21 ds + 23 glm), GT match rule and
  mimicry protocol frozen. `FROZEN: 2026-10-16T10:20:08Z
  sha256:9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c`
  (§6) — the scribe independently reproduced the block hash from the
  fenced bytes (match: True); the pin verified at freeze, at every
  trial start (`frozen_sha256_at_start` in all four receipts' metas),
  and post-append via `freeze-check --double-read` exit 0 (distiller);
  enforcement in code — `trials` refuses to send on a pin mismatch
  (exit 2, nothing sent).
- **Blind trials + GT-after ordering (clean globally):** receipts
  `corpus/evidence/attrib-r21-{ds,glm}-trials.log` (trial-runner
  seats A/B) + `attrib-r21-impl-{ds,glm}-trials.log` (instrument-impl's
  own validation runs) — 84 blind trials total (40 ds / 44 glm vs
  frozen 21/23 budgets; the duplicate execution disclosed in-receipt by
  both seats, r19 defect-7 recurrence, no dispatch ledger). Ordering:
  frozen 10:20:08Z < first trial 10:21:00.575Z < last trial 10:25:01Z <
  first journal GT read 10:25:25Z. ≥2.5 s spacing, one attempt per
  trial, no retries, no Authorization header, localhost only,
  credentials never read.
- **Scored at close (receipts' authoritative blocks; scorer note
  {{SCORER_NOTE_STATE}}):** ds **20/20 = 1.000 → PASS** (bar 0.80,
  block 10:27:01Z); glm **22/22 = 1.000 → PASS** (block 10:27:03Z) —
  GT counts ds `{alibaba-token-plan: 20}` (single-leg; hyper/
  opencode-go 0 GT trials = UNTESTED, pre-named by frozen table §5),
  glm `{devin: 9, zai: 13}` (hyper UNTESTED); chance baseline 1/3.
  Mimicry/ablation arm: all 11 ablations 1.000 on both shims — an
  information-dependence lower bound per the frozen `honest_read`
  clause, not a padding adversary (lesson 5). The bar's denominator
  guard demonstrably fired mid-round (the 18/18 = 1.000 FAIL at
  n < 20). Falsifiability shape intact: a bookkeeping FAIL (0/0
  UNMATCHED, matcher bugs) and a mechanism FAIL (denominator refusal)
  both occurred and were kept separable — recorded, never patched.
- **Prior-art pricing:** `corpus/knowledge/attrib-prior-art-r21.md`
  (landed 10:08:50Z) — verdict "INSTRUMENT-NOVEL,
  PHENOMENON-INCREMENTAL (search-set verdict)": all 9 arXiv abs pages
  fetched in-session, HTTP 200 ×9 (note §7 receipt: 2407.15847,
  2508.09021, 2410.20247, 2608.22213, 2605.29979, 2411.01076,
  2412.15431, 2409.20002, 2605.14786); honest N1 scoping per note §4
  (instrument + GT protocol fleet-local, NOT a new phenomenon — "No
  round-21 text may claim the phenomenon as a discovery"); §5 citation
  correction recorded, not patched (the brief's "LLMmap/2508.09021"
  conflates LLMmap = 2407.15847 with Kurian et al. = 2508.09021; the
  note supplied the missing IDs 2410.20247 / 2608.22213 and
  cross-checked via OpenReview + the ICLR 2025 proceedings page).
  Novelty-proxy reading (SCORECARD.md:47-54): the fetched-URL leg
  fires — first exercise since r14; phenomenon-INCREMENTAL /
  instrument-NOVEL.
- **Instrument:** `plans/attrib_probe.py` (instrument-impl seat chose
  `plans/`, 663 lines, stdlib-only) — inspectable in-repo; blind rule
  enforced structurally (`journalctl` occurs only inside cmd_score);
  `freeze-check` exits 0/2 with a verdict; `score` exits 0/1 on the
  frozen bar; recorded defects: `cmd_block_sha` TypeError at `:627`,
  `datetime.utcnow()` deprecation warnings, instrument sha unrecorded
  at scoring time (b3e18c78 → effa7ea7 — lesson 1's next-instantiation
  pin). Trials metas record `instrument_sha256: b3e18c78…`.
- **Breaches and defects (recorded, never patched):** matcher defects
  A/B/C fixed pre-adjudication, append-only trail in the ds receipt
  (two 0/0 bookkeeping FAILs, one 18/18 denominator-refusal FAIL, then
  the authoritative 20/20 PASS); instrument sha unrecorded at scoring
  (b3e18c78 → effa7ea7 — lesson 1); frozen-table §0 conflated citation
  + 233-byte figure permanent inside the pin (errata-only — lesson 7);
  duplicate execution 84 trials vs frozen 44, disclosed in-receipt by
  both seats (r19 defect-7 recurrence, no dispatch ledger);
  `cmd_block_sha` TypeError at `plans/attrib_probe.py:627`;
  `plans/__pycache__/` should not land. {{DEFECTS_LINE — append the
  scorer note's defect list when it lands}}. Scribe
  findings filed pre-landing: D21-s2 (RESOLVED by the lander — the
  scout's pricing was dispatch provenance; the note re-verified
  seat-side), D21-s3 (the r20 §10 note extension and template revision
  are
  uncommitted at HEAD — the r20 SCORECARD section cites
  working-tree-only bytes; r8/r17 breach class), D21-s5 (request-budget
  supersession: the frozen enumerated set governs, disclosed
  in-receipt — the r20 §10.1 precedent), D21-s6 (bar denominator
  pinned pre-trial; mimicry arm outside the 80% denominator), D21-s7
  (GT matcher pinned pre-trial), D21-s12 (scribe's offline self-check
  caught the instrument's freezability crash pre-freeze), D21-s13/s14
  (the frozen citation; the two pre-named hazards materializing).
  Full list:
  `.ufo/rounds/round-21/goal-wave/scorecard-verdict-draft.md` §3.
- **Ledger:** verdicts per gate drafted at
  `.ufo/rounds/round-21/goal-wave/scorecard-verdict-draft.md` §2 —
  [PARENT: the axis verdict lines and the admission decision are the
  parent's judgement]. Index parity at close: [PARENT: verify per
  `corpus/README.md` — new rows expected for `attrib-prior-art-r21.md`,
  `attrib-r21.md`, the trials logs' evidence dir, and
  `plans/attrib-r21-frozen.md`]. Next move (§Planned): [PARENT: the
  standing battery + the attribution instrument are now two standing
  instruments; the mimicry arm's outcome prices the padding-resistance
  claim for any future cross-host transfer attempt].
```

---

**Fill sources:** the frozen table `plans/attrib-r21-frozen.md`
(feature-freezer seat); the trial receipts
`corpus/evidence/attrib-r21-{ds,glm}-trials.log` (trial-runner seats);
the scorer note `corpus/knowledge/attrib-r21.md` (scorer +
note-finalizer seats); the prior-art note
`corpus/knowledge/attrib-prior-art-r21.md` (prior-art-lander seat); the
instrument (instrument-impl seat, `tools/` or `plans/`); the lesson
(`corpus/lessons/`, lessons-distiller seat); the scribe's verdict draft
(§2–§3 of `scorecard-verdict-draft.md` in this directory). Dates: the
lane's LOG dates are local dates of the work; this round's work spans
2026-10-16 UTC (local -03). The parent picks the entry date at commit
time (round-14 precedent, `corpus/evidence/round14-fleet/r14-scribe-drafts.md`
§6 item 7).
