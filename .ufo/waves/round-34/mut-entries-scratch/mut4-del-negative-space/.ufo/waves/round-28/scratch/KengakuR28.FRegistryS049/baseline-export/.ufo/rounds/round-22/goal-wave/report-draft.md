# report-draft — kengaku round 22 (fleet report skeleton)

Scribe seat, round-22 goal wave. Written 2026-10-16, starting state
captured 11:30–11:36Z at HEAD `78245e1` (round-21 records; r21 evidence
commit `0d23c61`). **This file writes nothing** — the round report is
PARENT-owned and lands at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-22/kengaku.md` (the
round-18/19/21 precedent: the lane's fleet report lives in the fleet
repo). The skeleton carries the round-prompt's four required sections in
order (work performed / landed changes / before→after measurements /
SHONEN — `../templates/round-prompt.md` §4). A contentless report counts
the round as failed, so every `[PARENT]` slot must resolve to a real
receipt or the bullet must state its absence with polling evidence —
placeholders must not ship.

---

```markdown
# SHONEN — Round 22: attribution leg coverage + battery fold
(operability/coverage axis-move)

Starting commit `78245e1`. Lane: kengaku-shokunin (LLM/model research &
evaluation). Wave: 32-seat flash (zai-bucket). One axis-move:
operability/coverage — cover the untested attribution legs AND fold the
instrument into the standing battery. Falsifiable claim: **before** —
attribution is validated only for the legs that naturally serve (hyper
and opencode-go: 0 GT trials, named UNTESTED in the r21 record;
`SCORECARD.md:511`), and the instrument is a one-off experiment rather
than a standing probe type (template had no P10/attribution content at
11:30:10Z, scribe-verified); **after** — (a) forced-fallback trials land
≥10 each on hyper and opencode-go through the ds cascade with the
extended feature table (RE-FROZEN before trials if extended), accuracy vs
the 0.80 bar scored against post-trials journal GT — with the honest
limit named that FORCED coverage is a different claim than natural
coverage; (b) the battery template + note gain probe-type P10
(attribution health-check schema, etiquette, re-freeze policy).

## Work performed

- Battery-fold-impl: `plans/probe-battery-TEMPLATE.md` §11 "Probe-type
  P10 — attribution health-check" (landed by 11:34:15Z) — frozen
  feature-table ref verified in code before the first request
  (mismatch → exit 2, nothing sent), ≥10 scored trials per shim (below →
  UNPROVABLE, not FAIL — the r21 bar-refusal precedent), bar accuracy
  ≥0.80 with per-leg GT counts and 0-GT legs UNTESTED, GT-post-trials
  ordering across all shims, the 44-request r21 scale as ceiling,
  ≥2.5 s spacing, re-freeze policy (any table change = new freeze naming
  the superseded hash; instrument sha pinned at trials AND scoring —
  r21 defect 2's mitigation adopted as schema), and the forced-vs-natural
  honest limit. Companion fold record:
  `corpus/knowledge/probe-battery-r19.md` §11 (stamped 11:30Z).
- Lessons-distiller: `corpus/lessons/2026-10-16-round22-leg-coverage-
  forcing.md` (landed by 11:34:15Z) — four lessons: coverage weather vs
  design; forced-vs-natural is mechanistic (fallback walls include the
  failed leg-1 attempt, so band features abstain and tells/schema carry
  the trial); extension fields re-derived from landed bytes (an empty
  field is decision-rule behaviour under the additive rule — filling one
  changes the rule's behaviour); the fold converts coverage honesty into
  standing schema. Named leftovers: the unscored r21 official receipts
  belong to scorer-r22's addendum; NOT-RUN-with-reason is the honest
  outcome if leg-1 cannot be forced.
- Leg-coverage-impl: `plans/attrib-r21-frozen.md` extension + re-freeze
  {{LEG_COVERAGE_STATE — landed/pending with poll evidence; at 11:35:30Z
  the block pin was still `9f0244bb…` (block-sha exit 0), i.e. no
  extension had landed}}. The extension must re-derive every filled
  value from landed receipts (r19/r21 bytes, not the wave brief) and
  report still-empty fields in the r22 receipt (r22 lesson 3).
- Trial-runners: `corpus/evidence/attrib-r22-*.log` {{RUNNER_STATE —
  landed/pending with poll evidence; absent at 11:35:30Z}} — forced-
  fallback trials through ds (:8791), ≥10 scored GT trials each on hyper
  and opencode-go, receipts recording the forcing mechanism in-band
  (r22 lesson 2 corollary (a): an undisclosed forcing mechanism is
  indistinguishable from weather), the new `frozen_sha256_at_start`, and
  `instrument_sha256_at_start`/`_at_scoring` per template §11.
- Scorer-r22: the r22 addendum on `corpus/knowledge/attrib-r21.md`
  {{SCORER_STATE — landed/pending with poll evidence; absent at
  11:35:30Z}} — adjudicates the r22 trials against the 0.80 bar with the
  natural/forced GT split, AND the still-unscored r21 official runner
  receipts (runner-B's T21 live `devin_shim_error` capture is the only
  live `error_tells` observation on record — r22 lesson, named
  leftovers).
- Scribe: the three drafts under `.ufo/rounds/round-22/goal-wave/` (this
  round's three files); zero requests, zero journal reads (D22-s9).
- [PARENT: commit hash(es) carrying the above; LOG.md round-22 entry;
  SCORECARD.md round-22 section — drafted in
  `.ufo/rounds/round-22/goal-wave/`]

## Landed changes

- `plans/probe-battery-TEMPLATE.md` — §11 P10 schema (battery-fold-impl).
- `corpus/knowledge/probe-battery-r19.md` — §11 fold record
  (battery-fold-impl).
- `corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md` — the
  round lesson (lessons-distiller).
- `plans/attrib-r21-frozen.md` — extended feature table + new FROZEN
  line {{LEG_COVERAGE_STATE}} (leg-coverage-impl).
- `plans/attrib_probe.py` — {{INSTRUMENT_STATE — changed only if the
  extension required code support; any change is leg-coverage-impl's
  sole write; landing-time sha was `effa7ea7…` at 11:30:10Z}}.
- `corpus/evidence/attrib-r22-*.log` — trial receipts (trial-runners).
- `corpus/knowledge/attrib-r21.md` — r22 addendum (scorer-r22).
- `.ufo/rounds/round-22/goal-wave/` — scribe drafts (this round's three
  files).
- [PARENT: commit hash(es); index rows in `corpus/README.md` for the new
  evidence receipts; the inherited dirty bytes (the r21 lesson file
  untracked at HEAD, D22-s2)]

## Before → after measurements

- Before (re-verified 11:30–11:36Z): hyper/opencode-go 0 GT trials
  (r21 GT counts ds `{alibaba-token-plan: 20}`, glm `{devin: 9, zai: 13}`
  — receipt-verbatim, `attrib-r21-impl-{ds,glm}-trials.log`); template
  attribution/P10 content 0 hits at 11:30:10Z; block pin `9f0244bb…`
  (block-sha exit 0, 11:30:10Z and 11:35:30Z); instrument sha
  `effa7ea7…`; runnable `.py`/`.sh` baseline 38 at HEAD.
- After: {{AFTER_LINES — resolve from the landed receipts + scorer
  addendum: per-shim ACCURACY lines vs the 0.80 bar, per-leg GT counts
  split natural/forced, ≥10 scored per targeted leg, the re-freeze
  hash, and the fold's template/note sections}}. The honest limit rides
  with every quoting surface: forced coverage validates the feature
  table against a leg's serve path — it does not establish
  discrimination under natural traffic (template §11; r22 lesson 2).
- Standing-instrument property: the attribution instrument is now the
  battery's probe-type P10 — a future instantiation re-runs it against a
  re-deployed shim under a fresh per-instantiation freeze, measuring
  attribution decay instead of re-deriving leg tells from scratch.

## SHONEN

- [~] Real decision tables/error patterns/checklists/sources: the P10
  schema (template §11) + the extended frozen table are the decision
  surfaces; every filled extension value cites a landed receipt (r22
  lesson 3). [PARENT: marks stay [~] without a non-author verifier].
- [~] End-to-end domain task executed and logged: forced-fallback
  attribution trials with journal GT, scored at close; LOG.md round-22
  entry drafts at `.ufo/rounds/round-22/goal-wave/log-entry-draft.md`.
  [PARENT: cite the landed LOG entry once integrated]
- [~] Instructions executable without oral context: template §11 +
  frozen table + receipts are in-repo and self-gating (pin checks in
  code; the re-freeze policy names the superseded hash). [PARENT: marks
  stay [~] without a non-author verifier]
- [~] No cross-domain bleed: all requests localhost shims; credentials
  never read; the journal read is the lane's own-probe GT pattern; any
  serving-plane finding (forcing mechanism behaviour, leg-1 failure
  modes) routed to the integrator, not absorbed.
```

---

**Parent fill rules:** two of the wave's seat artifacts landed by
11:34:15Z (fold template §11 + note §11; the r22 lesson); the table
extension/re-freeze, the r22 trial receipts, and the scorer addendum
were absent at the 11:35:30Z poll — their slots resolve at integration
from the landed bytes or become absence statements with polling
evidence. Quote landed artifacts verbatim; do not recompute scorer
numbers. The remaining `[PARENT]` markers are genuine parent-owned
values: the close commit hash(es), the LOG/SCORECARD/report integration
citations, the grader re-run, the axis verdict lines, index parity, and
the D22-s2 decision on the inherited untracked r21 lesson file.
