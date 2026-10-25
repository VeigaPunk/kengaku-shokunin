# ScoutL0Status: kengaku round 27, read-only L0 ruling check

Scope: fleet `.ufo/` plus fleet-root `AXES.md` (definitions). Read-only; this file is the only write. No installs. Milestone work (extraction-policy comparison, state_check P4, sources) was not performed; it is outside this assignment.

## Answer
- Coverage cap (L0 `.ufo/l0-questions.md:72`, kengaku r25): NOT RULED. No operator or orchestrator answer exists anywhere in `.ufo/`.
- Novelty verdict conversion (L0 `.ufo/l0-questions.md:73`, kengaku r25): NOT RULED. Same result.
- The lane still treats both as open: `kengaku-shokunin/plans/round-27-claims.md:17-19` ("coverage stays capped ... until the operator rules L0 `.ufo/l0-questions.md:72`").

## What was read
- `.ufo/l0-questions.md` is 79 lines. Lines 52-79 were read raw. Lines naming kengaku at or after 72: exactly 72 and 73. Lines 74-79 were read in full: no kengaku mention and no answer to 72 or 73.
- Answer-style markers in the queue: `:52-53` "L0 ANSWER (hyaku orchestrator for the operator, 2026-10-19; operator may override)" (kama r11, tsukuroi r12, planner seat); `:77` "RESOLVED-BY-RULING (Main, in-session orchestrator)" (tabi r19). None concerns kengaku.
- Earlier kengaku lines: `:7` (gate standard, answered by protocol ruling, `.ufo/reports/AGGREGATE.md:1812`); `:35` (round-13 namespace and tie-break; digest `.ufo/waves/kaika-w1/l0.md:98` status OPEN). Other lanes mention kengaku in passing (e.g. `:2`, `:6`, `:50`); none is a kengaku question.
- Question-specific greps over all of `.ufo/` (gitignore off): cap / declared-but-unresolvable / Historical; ClaimCritic / binding ruling; verdict conversion / novelty verdict / retroactive; answer or ruling words within 200 characters of those terms; kengaku r23-25 status rows near RULED / ruling / answer (no matches). A broad marker grep was paginated and is not relied on. Hits are listed below.
- Also searched `.ufo/{state,prompts,scopes,round-10,round-44,l0-recovery-20261015T054007Z,interactive-l1-20261015T050057Z}` for ruling terms: no ruling text. `.ufo/prompts/kengaku-round-{24,25,26,27}.md` contain only generic rules ("Report all verdicts and let the operator rule", `kengaku-round-27.md:37-40`). `.ufo/waves/round-27` exists only lane-local.

## Coverage cap (72): evidence, nothing operator-binding
- Filed: `.ufo/reports/round-24/kengaku.md:221-223`. Re-filed: `.ufo/reports/round-25/kengaku.md:121`. Held open: `.ufo/reports/round-26/kengaku.md:141` ("remains open; coverage stays 7").
- Only in-lane ruling: `.ufo/reports/round-24/kengaku.md:200-201` "The score holds at 7 under ClaimCritic-3's binding ruling: a Historical-absent section does not clear the cap." ClaimCritic-3 is a lane critic seat (`round-24/kengaku.md:65`). The lane re-filed the question afterwards, so it did not treat that as settling it.
- Non-author review (orchestrator-dispatched, kaika-w3): `.ufo/waves/kaika-w3/kengaku-review.md:106` "cap stands per lane's PROVINCE §Historical (I did not independently re-test route-telemetry absence)". This is agreement, not an L0 answer. `AXES.md:47-48` says a dispatched subagent does not count as the named non-author reviewer.
- Outside closure r26: `.ufo/reports/round-26/kengaku-closure-evidence.json:13` "coverage": "unchanged 7 capped". Its limitations (`:563-567`) never address Historical-absent surfaces.
- Operator-side definition: `AXES.md:12` coverage = "Fraction of the domain's real surfaces the skill governs". The declared-but-unresolvable clause lives in the lane rubric (`kengaku-shokunin/SCORECARD.md:247`). Whether a retired surface sits in the denominator is exactly L0:72, and AXES.md does not settle it.

## Novelty conversion (73): evidence, nothing operator-binding
- Filed: `.ufo/reports/round-24/kengaku.md:224-225`. Re-filed: `.ufo/reports/round-25/kengaku.md:122`. The round-25 +1 was withdrawn on prior art (`round-25/kengaku.md:124`); the conversion question "stands".
- Round 26: "no retroactive conversion or +1 is taken" (`.ufo/reports/round-26/kengaku.md:141`).
- Outside closure r26 rejected a novelty +1 candidate: `.ufo/reports/round-26/kengaku-closure-evidence.json:541-545` (gate reject, outside agree, "Novelty 7 held is honest"). This is per-round only and silent on retroactive conversion and on who converts.
- Non-author review (kaika-w3): `.ufo/waves/kaika-w3/kengaku-review.md:103` novelty "7->7 unchanged, agree".
- Numeric state: last numeric novelty is 7 at r14; r19-r22 are verdict-only (`.ufo/waves/kaika-w1/kengaku-state.md:65-71`, `:226`). That audit proposes, without ruling, either re-deriving +/-1 per verified claim or marking the axis "verdict-only, no numeric" (`:301-305`).
- Operator-side rule: `AXES.md:43-55` already permits a verdict-only row for exploratory moves ("the row says which one it is") with a named non-author reviewer. It governs future rows; it does not cover retroactive conversion of r21 or "by whom".
- Precondition: `novelty` is not among AXES.md's six axes (grep over AXES.md: no match). D-78 is OPEN (`.ufo/reports/AGGREGATE.md:736`; "RULED-partially ... operator action owed" at `:1236`). Integrator position: "the scores are calibration defects until the vocabulary exists" (`.ufo/reports/round-11/protocol.md:235-240`). A novelty numeric conversion is therefore blocked on the operator's D-78 action, not only on L0:73.

## Adjacent (not asked)
- "C2 admission" (`.ufo/reports/round-24/kengaku.md:226-227`) was never queued to L0; not ruled.
- `.ufo/waves/hyaku/PHASE2.md:447-448`: kengaku r25 "rejected-honest-stop (... operator may rule the tip-corrected reading admissible)". Open operator item, unrelated to 72 or 73.
- `.ufo/waves/kaika-w1/l0.md:10-16` (2026-10-19 triage) recorded 0 in-place answers on 51 lines. The queue is now 79 lines with the markers above.

## Files written
- `kengaku-shokunin/.ufo/waves/round-27/build/ScoutL0Status.md` (this file only).

## Installs
- None.

VERDICT: Both L0:72 (coverage cap) and L0:73 (novelty conversion) remain unruled in `.ufo/` (no operator or orchestrator answer); only in-lane critic and review opinions exist, so coverage and novelty stay at 7 for round 27, and any novelty number is also blocked on operator D-78.
