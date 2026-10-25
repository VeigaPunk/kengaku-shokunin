# report-draft — kengaku round 21 (fleet report skeleton)

Scribe seat, round-21 goal wave. Written 2026-10-16, starting state
captured 10:04–10:08Z at HEAD `3688f76` (round-20 records; r20 evidence
commit `af0e3e6`). **This file writes nothing** — the round report is
PARENT-owned and lands at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-21/kengaku.md` (the
round-18/19 precedent: the lane's fleet report lives in the fleet repo;
note D21-s11 — the fleet round-20 dir held no kengaku copy at 10:06Z).
The skeleton carries the round-prompt's four required sections in order
(work performed / landed changes / before→after measurements / SHONEN —
`../templates/round-prompt.md` §4). A contentless report counts the
round as failed, so every `[PARENT]` slot must resolve to a real receipt
or the bullet must state its absence with polling evidence —
placeholders must not ship.

---

```markdown
# SHONEN — Round 21: blind cascade-leg attribution instrument (novelty axis-move)

Starting commit `3688f76`. Lane: kengaku-shokunin (LLM/model research &
evaluation). Wave: 32-seat flash (zai-bucket). One axis-move: novelty —
N1 (registered by the r20 scout after pricing latency-fingerprinting out
of novelty): blind cascade-leg attribution with shim-journal ground
truth — instrument-level novelty, phenomenon-incremental, scoped
honestly. Build and validate the instrument: frozen feature table
(latency band / header tells / error-wording shape / body schema;
weights pre-registered, sha-frozen BEFORE any trial), ≥20 blind trials
per shim, accuracy ≥ the frozen bar (80%), GT read ONLY after trials,
mimicry probes against feature-profile padding.

## Work performed

- Feature-freezer: `plans/attrib-r21-frozen.md` — the feature table with
  pre-registered weights (8 features), the 0.80 bar with
  `min_scored_trials_per_shim: 20`, the enumerated request set (21 ds +
  23 glm), the GT match rule, and the mimicry protocol with its
  `honest_read` clause, frozen `FROZEN: 2026-10-16T10:20:08Z
  sha256:9f0244bb…` with the double-read stability guard; pin verified
  at freeze, at every trial start, and post-append.
- Trial-runners + instrument-impl: `corpus/evidence/attrib-r21-ds-trials.log`,
  `attrib-r21-glm-trials.log` (runner seats A/B) +
  `attrib-r21-impl-{ds,glm}-trials.log` (impl's own runs with the
  scoring blocks) — 84 blind trials total (duplicate execution
  disclosed in-receipt; r19 defect-7 recurrence), ≥2.5 s spacing, no
  retries, no Authorization header, journal GT untouched during the
  trial window (ordering clean globally: last trial 10:25:01Z < first
  GT read 10:25:25Z).
- Scorer + note-finalizer: `corpus/knowledge/attrib-r21.md` — GT read
  AFTER trials (gt_first_read_utc > last_trial_utc asserted per shim),
  accuracy scored against the frozen bar with the chance baseline (1/3)
  beside it, mimicry arm reported separately, verdicts per the frozen
  rule, defects recorded never patched.
- Prior-art-lander: `corpus/knowledge/attrib-prior-art-r21.md`
  (landed 10:08:50Z) — verdict "INSTRUMENT-NOVEL, PHENOMENON-
  INCREMENTAL (search-set verdict)", 9/9 arXiv primaries fetched HTTP
  200 (§7 receipt), honest N1 scoping §4, citation correction §5 (the
  brief's "LLMmap/2508.09021" conflates LLMmap = 2407.15847 with Kurian
  et al. = 2508.09021; verdict unaffected, recorded not patched).
- **Instrument-impl:** `plans/attrib_probe.py` (663 lines, stdlib-only,
  chose `plans/` per its write ownership) + its own validation runs
  `corpus/evidence/attrib-r21-impl-{ds,glm}-trials.log` (the receipts
  carrying the scoring blocks); the blind rule enforced in code
  (`journalctl` only inside cmd_score); matcher defects A/B/C fixed
  mid-round with the append-only debugging trail preserved in the ds
  receipt; `cmd_block_sha` TypeError at `:627` recorded [PARENT:
  confirm stranger-runnable].
- Lessons-distiller: `corpus/lessons/2026-10-16-round21-attribution-
  freeze-surface.md` (landed ~10:40Z) — seven lessons incl. the
  freeze-surface thesis (the table was frozen; the code was not),
  the canned-GT smoke move, bookkeeping-FAIL vs mechanism-FAIL, and
  the mimicry lower-bound read.
- Breach handling (from the landed receipts + lesson; the scorer note's
  own defect list appends at integration): matcher defects A/B/C fixed
  pre-adjudication with the append-only debugging trail preserved in
  the ds receipt (two 0/0 bookkeeping FAILs, one 18/18
  denominator-refusal FAIL, then the authoritative 20/20 PASS);
  instrument sha unrecorded at scoring (b3e18c78 → effa7ea7); the
  frozen-table §0 conflated citation + 233-byte figure permanent inside
  the pin (errata-only); duplicate execution 84 trials vs frozen 44,
  disclosed in-receipt by both seats; `cmd_block_sha` TypeError at
  `:627`; `plans/__pycache__/` should not land. All recorded, never
  patched. {{BREACH_LINE — append the scorer note's defect list when it
  lands}}. Scribe findings filed pre-landing: D21-s1…D21-s15
  (`.ufo/rounds/round-21/goal-wave/scorecard-verdict-draft.md` §3) —
  notably D21-s3 (the r20 §10 note extension + template revision are
  uncommitted at HEAD; the r20 SCORECARD section cites working-tree
  bytes) and D21-s2 (the scout's pricing evidence is dispatch
  provenance; the prior-art note fetches its own URLs).

## Landed changes

- `plans/attrib-r21-frozen.md` — the frozen feature table + bar +
  request enumeration + GT matcher (feature-freezer seat).
- `corpus/evidence/attrib-r21-{ds,glm}-trials.log` — the blind-trial
  receipts (trial-runner seats).
- `corpus/knowledge/attrib-r21.md` — the scored note (scorer +
  note-finalizer seats).
- `corpus/knowledge/attrib-prior-art-r21.md` — the prior-art note with
  fetched URLs (prior-art-lander seat).
- `plans/attrib_probe.py` — the instrument + its validation receipts
  `corpus/evidence/attrib-r21-impl-{ds,glm}-trials.log`
  (instrument-impl seat).
- `corpus/lessons/…` — the round lesson (lessons-distiller seat).
- `.ufo/rounds/round-21/goal-wave/` — scribe drafts (this round's three
  files).
- [PARENT: commit hash(es) carrying the above; LOG.md §21 entry;
  SCORECARD.md round-21 section — both drafted in
  `.ufo/rounds/round-21/goal-wave/`; the inherited r20 dirty bytes
  (D21-s3)]

## Before → after measurements

- Before (re-verified at 10:04–10:08Z): no attribution instrument
  in-repo (no `tools/` dir; zero `attrib*` files; the 4 `.py`/`.sh`
  `attribut` hits are r12 error-record bookkeeping); every prior leg
  attribution in the corpus is post-hoc journal consultation
  (`probe-r19-P4-glm.log:137-139`, `probe-r19-shim-ds-run.log:52-55`);
  N1 registered (`.ufo/rounds/round-20/kengaku.md:36-37`); runnable
  `.py`/`.sh` baseline 37 at HEAD.
- After: frozen table `plans/attrib-r21-frozen.md` (FROZEN 10:20:08Z,
  sha `9f0244bb…`, scribe-reproduced); 84 blind trials across four
  receipts; **ds 20/20 = 1.000 PASS, glm 22/22 = 1.000 PASS** (bar
  0.80, chance 1/3; GT counts ds alibaba×20 single-leg, glm zai 13 /
  devin 9, hyper UNTESTED both shims); all 11 mimicry/ablation arms
  1.000 on both shims (information-dependence lower bound per the
  frozen `honest_read` clause); GT ordering clean globally (last trial
  10:25:01Z < first GT read 10:25:25Z); prior-art verdict
  INSTRUMENT-NOVEL / PHENOMENON-INCREMENTAL with 9/9 fetched URLs;
  instrument in-repo at `plans/attrib_probe.py`. Measured against
  commit {{CLOSE_COMMIT}}; the scorer note's adjudication
  ({{SCORER_NOTE_STATE}}) supersedes where it disagrees.
- Standing-instrument property (the round's structural claim): the
  attribution instrument is the lane's second standing instrument
  (after the r19/r20 probe battery) — a future round can re-run the
  frozen table against a re-deployed shim to MEASURE attribution decay
  rather than re-derive leg tells from scratch; the mimicry arm bounds
  what the instrument claims (padding-resistance, or its absence).

## SHONEN

- [~] Real decision tables/error patterns/checklists/sources: the frozen
  feature table IS the decision table (per-leg tells → leg attribution,
  weights pre-registered, bar pinned) — [PARENT: marks stay [~] without
  a non-author verifier].
- [~] End-to-end domain task executed and logged: blind trials against
  the live shims with journal GT, scored at close; LOG.md §21 entry
  drafts at `.ufo/rounds/round-21/goal-wave/log-entry-draft.md`.
  [PARENT: cite the landed LOG entry once integrated]
- [~] Instructions executable without oral context: the frozen table +
  instrument + receipts are in-repo and self-gating (FROZEN line +
  double-read guard + GT-after assertion + enumerated request set).
  [PARENT: marks stay [~] without a non-author verifier]
- [~] No cross-domain bleed: all requests localhost shims; credentials
  never read; the journal read is the lane's own-probe GT pattern
  (r19-established), not mori's fleet-liveness reading (D21-s8); any
  serving-plane finding routed to the integrator, not absorbed.
```

---

**Parent fill rules:** five of six seat artifacts landed by 10:40Z;
`corpus/knowledge/attrib-r21.md` (scorer + note-finalizer) was absent
at the 10:38:51Z poll — the remaining `{{SCORER_NOTE_STATE}}` /
`{{ACCURACY_SCORER_LINE}}` slots resolve from it at integration, or
become an absence statement with polling evidence. Quote landed
artifacts verbatim; do not recompute scorer numbers. The remaining
`[PARENT]` markers are genuine parent-owned values: the close commit
hash(es), the LOG/SCORECARD/report integration citations, the grader
re-run, the axis verdict lines, index parity, the D21-s3 decision on
the inherited dirty r20 bytes, and the duplicate-execution
adjudication (§1.2 item 4).
