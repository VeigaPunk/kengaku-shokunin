# report-draft — kengaku round 19 (fleet report skeleton)

Scribe seat, round-19 goal wave. Written 2026-10-16, updated through 07:57Z
at HEAD `05cb955`. **This file writes nothing** — the round report is
PARENT-owned and lands at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/kengaku.md` (the
round-18 precedent: the lane's fleet report lives in the fleet repo; the
round-17 lane-local copy convention applies if the parent reuses it). The
skeleton carries the round-prompt's four required sections in order (work
performed / landed changes / before→after measurements / SHONEN —
`../templates/round-prompt.md` §4). A contentless report counts the round as
failed, so every `[PARENT]` slot must resolve to a real receipt or the bullet
must state its absence with polling evidence — placeholders must not ship.

---

```markdown
# SHONEN — Round 19: standing probe battery (calibration axis-move)

Starting commit `05cb955`. Lane: kengaku-shokunin (LLM/model research &
evaluation). Wave: 32-seat flash (zai-bucket). One axis-move: calibration —
a standing, pre-registered probe battery replacing the intermittent ad-hoc
prediction loop (r8–r11 history: 0/1, 1/1, 0/0, 1/1).

## Work performed

- Battery authorship: `plans/probe-battery-r19.md` — 9 falsifiable live-route
  probes (P1 quota-dead token-plan keys; P2/P3 codex service_tier acceptance
  set + inert priority; P4 cascade leg order post-M7/M9; P5 burst-vs-
  incremental per-leg transport; P6 zai flash lane; P7 opencode-go
  verify-first; P8 managed:kimi-code auth-dead; P9 absent served model
  `:34113`), every probe citing its round-18 receipt. [PARENT: confirm final
  probe/component counts match the frozen plan]
- Prediction freeze (registrar): first freeze `FROZEN: 2026-10-16T07:52:04Z
  sha256:e3f08a09…` (stale — hashed the pre-rebase bundle; BR-1), repaired
  by re-freeze `FROZEN: 2026-10-16T07:55:58Z
  sha256:e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`
  (scribe-verified with the plan's own §7 command). Seat-level
  pre-registrations also filed (shim-ds S1–S8 at 07:43:30Z, pre-dating the
  battery freeze; shim-glm G1–G8 at 07:55:05Z; hyper H1–H10 at 07:56:41Z;
  devin D1–D5 at 07:53:40Z).
- Freeze saga (recorded breach + repair, never patched): the v2 re-base
  (P4/P5 re-framed to the M7/M9 post-reorder serving plane) was
  receipt-informed — the plan's own §0 revision note says "after runner-seat
  receipts revealed" — and six seats executed against the stale freeze
  (first requests 07:52:25–07:54:38Z, all recording `e3f08a09…`). Plan §7.1's
  "no runner executions between the stale freeze and the re-freeze" is
  falsified by those logs' mtimes and content. [PARENT/scorer: rule which
  prediction set governs each outcome; re-based components whose outcomes
  predate 07:55:58Z are outcome-informed — findings, not forecast skill]
- Execution: `corpus/evidence/probe-r19-*.log` — {{N_LOGS}} runner logs with
  UTC stamps, exact commands, exits, response excerpts (credential values
  never captured). {{RUNNER_SUMMARY — one line per log: seat, probes,
  outcome; scribe-held state at 08:02Z: shim-ds S1–S8 9/9 HIT mean Brier
  0.0050; quota-23 P1 1a–1f all hit; listing-mismatch P1 duplicate;
  P1-key1 addendum 200; P6-zai 429 rate-limit 6a/6b miss 6c unprovable;
  opencode DEFECT 0 pre-run; devin seat-level D1 hit / D2 miss 400 / D3 hit
  / D4 range-hit 485 / D5 unrecorded; P4-glm + P5-glm both requests 400
  terminal (zai 429 + devin temperature rejection), 4a/4c-glm/5a
  UNPROVABLE; shim-glm G1–G8 mean Brier 0.0772 (battery 4a falsified via
  the leg-change path, 5a burst HIT); hyper run pending at last check}}.
- Scoring at close: `corpus/knowledge/probe-battery-r19.md` — ordering gate
  {{ORDERING_GATE_VERDICT}}; per-component scores; aggregate calibration
  read (mean Brier with the 0.25 always-0.5 reference beside it; mean
  abs-error per unit; range hit-rate; pass/fail/unprovable counts). No
  scalar axis verdicts.
- Template: `plans/probe-battery-TEMPLATE.md` — host-agnostic battery
  template for future rounds (landed; §0–§8 instrument + §9 instantiation
  checklist + §10 known instrument defects). Template sync defects recorded
  (scribe D-s14: superseded freeze hash cited at :17; §5 omits the BR-1
  re-verify-before-write step; breach doctrine vs the actual re-freeze;
  stale budget figures).
- Breach handling: DEFECT 0 (opencode, two live requests before the battery
  existed, self-reported, contained 07:46:36Z, excluded from the aggregate);
  BR-1 stale freeze + the outcome-informed v2 re-base (above); the duplicate
  P1 (two seats, 8 requests vs budget 4; battery-governed total exceeds §2's
  binding ≤20); the shim-glm reshaped retry after a 400 (§2 rule 3,
  transparently documented, isolating `temperature` as the rejected field);
  the P1-key1 addendum (outside §6, prediction filed the same second as its
  first request — r12 `<=` convention); the P4-devinleg runner crash
  (NameError) with data still captured. [PARENT: confirm the scorer's
  rulings]

## Landed changes

- `plans/probe-battery-r19.md` — battery plan + frozen predictions
  (battery-author + prediction-registrar seats; amended post-freeze, breach
  recorded).
- `corpus/evidence/probe-r19-*.log` — runner receipts ({{N_LOGS}} files).
- `corpus/knowledge/probe-battery-r19.md` — scorer note (scorer +
  note-writer seats). [PARENT: add the `corpus/README.md` index row if the
  scorer note lands — knowledge rows must equal knowledge files]
- `plans/probe-battery-TEMPLATE.md` — reusable template (template-author
  seat).
- `.ufo/rounds/round-19/goal-wave/` — scribe drafts (this round's three
  files).
- [PARENT: commit hash(es) carrying the above; LOG.md §19 entry; SCORECARD.md
  round-19 section — both drafted in `.ufo/rounds/round-19/goal-wave/`]

## Before → after measurements

- Before: calibration proxy 0/1, 1/1, 0/0, 1/1 across r8–r11
  (`SCORECARD.md:34-37`); no battery/template in `plans/` at round start
  (`ls plans/` at 07:44:09Z → 2 wwkd files; scribe re-verified 07:36Z).
- After: {{AFTER_MEASUREMENTS — from the scorer note: probes run frozen→
  scored N/N; mean Brier X over M binary components (always-0.5 reference
  0.25); mean abs-error per numeric unit; range hit-rate; ordering gate
  verdict; template landed}}. Measured against commit {{CLOSE_COMMIT}}.
- Standing-battery property (the round's structural claim): the battery is
  re-runnable next round from the template without re-authoring —
  {{TEMPLATE_REUSE_EVIDENCE}}.

## SHONEN

- [~] Real decision tables/error patterns/checklists/sources: unchanged this
  round (`SKILL.md` untouched by the battery). [PARENT: confirm]
- [~] End-to-end domain task executed and logged: the battery is a live
  model-route measurement round; LOG.md §19 entry drafts at
  `.ufo/rounds/round-19/goal-wave/log-entry-draft.md`. [PARENT: cite the
  landed LOG entry once integrated]
- [~] Instructions executable without oral context: the battery plan + the
  template are in-repo, host-agnostic, and self-gating (FROZEN line +
  ordering audit). [PARENT: the template strengthens this box's evidence;
  marks stay [~] without a non-author verifier]
- [~] No cross-domain bleed: serving-plane findings (P4 leg-order drift
  confirmation, any P9 restoration) route to the integrator/operator per
  `PROVINCE.md` §Refusals; no foreign scope absorbed. [PARENT: confirm from
  the scorer note's §5 findings]
```

---

**Parent fill rules:** resolve every `{{…}}` from landed artifacts (scorer
note first, runner logs second); quote receipts verbatim; if a pipeline stage
did not land (no freeze / no scorer note / no template), the corresponding
bullet states its absence with the polling evidence instead of a placeholder —
that is still a valid report; a placeholder shipped as-is is not.
