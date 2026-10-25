# log-entry-draft — kengaku round 22

Scribe seat, round-22 goal wave. Written 2026-10-16, starting state captured
11:30–11:36Z at HEAD `78245e1` (round-21 records; r21 evidence commit
`0d23c61`). **This file writes nothing** — `LOG.md` is PARENT-owned; the
block below is a paste-ready entry in the round-19/20/21 LOG idiom
(`## <n> — <title>` section; see `LOG.md` §19–§21). `[PARENT]` markers and
`{{PLACEHOLDER}}` slots must be resolved from landed artifacts at
integration time; every resolved value must quote its receipt (lane rules:
"Every change appends a LOG.md entry with the evidence that motivated it";
"Never fabricate domain knowledge"). Placeholders must not ship — an
unresolved slot becomes an absence statement with polling evidence. No
scalar axis verdicts.

---

```markdown
## Round 22 — attribution leg coverage + battery fold (goal wave)

**Round 22 (2026-10-16).** Motivating evidence: r21 named hyper/opencode-go
UNTESTED — 0 GT trials each, "3 of the 5 roster legs were exercised at
all" (`SCORECARD.md:511`; `corpus/knowledge/attrib-r21.md` §8.3) — and the
attribution instrument stood outside the standing battery as a one-off
experiment (template had zero attribution/P10 content before the fold —
`grep -in 'attrib|P10' plans/probe-battery-TEMPLATE.md` → 0 hits at
11:30:10Z, scribe-verified). Landed (evidence commit [PARENT: hash]):
(a) forced-fallback trials through the ds cascade (127.0.0.1:8791)
covering hyper and opencode-go at ≥10 scored GT trials each, against the
extended feature table RE-FROZEN before the first forced request
({{REFREEZE_LINE — new FROZEN UTC + sha256; names the superseded
9f0244bb… hash and what moved, per the §11 re-freeze policy}}), accuracy
vs the 0.80 bar scored against post-trials journal GT ({{ACCURACY_LINES —
receipt-verbatim ACCURACY + GT counts per shim, natural/forced split}});
the honest limit carried in every quoting surface: **FORCED coverage is a
different claim than natural coverage** (template §11; r22 lesson 2 —
"forced trials establish 'the instrument attributes the leg under forced
fallback'; they do not establish 'the instrument attributes the leg in
natural traffic'"). (b) The battery template + note gained probe-type
**P10 (attribution health-check)** — frozen-table-ref schema, ≥10
scored-trials floor (below → UNPROVABLE, not FAIL), 0.80 bar with per-leg
GT counts and 0-GT legs UNTESTED, GT-post-trials ordering across all
shims, 44-request etiquette ceiling, ≥2.5 s spacing, re-freeze policy,
instrument sha pinned at trials AND scoring — template §11
(`plans/probe-battery-TEMPLATE.md:442`, battery-fold-impl) + fold record
(`corpus/knowledge/probe-battery-r19.md:598`). (c) The scorer's r22
addendum on `corpus/knowledge/attrib-r21.md` adjudicates the still-
unscored r21 official runner receipts ({{SCORER_ADDENDUM_STATE —
landed/pending with poll evidence; runner-B's T21 live error-path capture
is the only live `error_tells` observation on record}}). Lesson:
`corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md` — natural
coverage is weather, forced coverage is design; extension fields
re-derived from landed bytes (an empty table field is decision-rule
behaviour, not bookkeeping — contributing-0 semantics); the re-freeze
completes before the first forced request; if leg-1 cannot be forced to
fail through any disclosed mechanism, NOT-RUN-with-reason is the honest
coverage outcome (r20 P9 precedent). Wave: 32 seats, zai flash.

**Boundaries held.** Small localhost requests only ({{REQUEST_COUNT —
enumerated before the freeze}}; ≥2.5 s spacing; no retries); credentials
never read; journal reads are read-only GT after ALL trials; seats
committed nothing; parent integrated under the kengaku lane identity.
```

---

**Fill sources:** the fold lands `plans/probe-battery-TEMPLATE.md` §11 +
`corpus/knowledge/probe-battery-r19.md` §11 (battery-fold-impl seat;
on disk at the 11:34:15Z poll); the forcing lesson
`corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md`
(lessons-distiller, on disk 11:34:15Z); the table extension + re-freeze
(`plans/attrib-r21-frozen.md`, leg-coverage-impl — NOT yet landed at
11:35:30Z: block-sha still `9f0244bb…`, exit 0); the trial receipts
(`corpus/evidence/attrib-r22-*.log`, trial-runners — absent at
11:35:30Z); the scorer addendum (`corpus/knowledge/attrib-r21.md` tail —
absent at 11:35:30Z, grep 'r22 addendum' → 0). The r21 official runner
receipts (`attrib-r21-{ds,glm}-trials.log`) remain unscored at HEAD
(`grep -c 'GT + scoring'` → 0 both files, 11:30:10Z) — scorer-r22's
addendum owns that adjudication per the r22 lesson's named leftovers.
Dates: the lane's LOG dates are local dates of the work (2026-10-16 UTC,
local -03); the parent picks the entry date at commit time (round-14
precedent).
