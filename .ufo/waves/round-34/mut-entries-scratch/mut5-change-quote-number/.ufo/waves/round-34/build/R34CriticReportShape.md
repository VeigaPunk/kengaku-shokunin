# Round-34 report compliance attack

## Evidence boundary
The requested standalone `kengaku-round-34.md` was not found at the fleet root or lane root (`read` returned not found); the round-34 claims file and prior report were available. The requirements below combine the user's explicit checklist with those inspected sources. Do not treat absence of the prompt file as evidence any requirement is waived.

Sources: `plans/round-34-claims.md:18-22,24-69,71-105,107-142`; `.ufo/reports/round-33/kengaku.md:8-16,18-25,27-89,91-115`.

## L1 checklist — report must satisfy

1. **Work performed** — state both frozen claims and actual disposition, plus frontier, assimilation/quarantine, considered proposals, and candid discrepancies/limitations. Keep frozen predicates unchanged; report actual evidence rather than retrofit claims.
2. **Landed changes** — table each landed change with lane commit(s) and LOG/evidence pointers. Identify commits or state missing/unobserved; do not imply a dirty/uncommitted wave artifact landed.
3. **Before→after measurements** — per C1 and C2 give frozen/control before receipt, exact command, output, exit code, final measured lane commit, after receipt/output, and score/trend interpretation. C1 frozen predicate requires 8 checks/0 defects and details V1–V8; C2 requires 8 mutants/8 detected, 8 checks/0 defects and both selftests, plus four class-specific red-before and green-after evidence. Include census before/after command/output/exit codes and registry/knowledge/index deltas. Distinguish state predicates from transition claims.
4. **Sources & frontier** — cite located S105/S106/S107 source anchors and expected artifacts; give source registry before/after and census receipts; explicitly state what the pinned evaluator tests and what it does not establish. Record S091/S105 payload-absent quarantine verdicts, adopted S108/S109 only if verified, with anchor/reason; screen package entries with admit/reject reasons. Name remaining frontier/open clauses and scope limits.
5. **Trend verdicts** — include expansion, quality, discernment, each with evidence and an explicit improved/held/harmed verdict. State numerical axis-score changes separately; no unsupported increase or “no harm” assertion.
6. **SHONEN** — exactly one physical report line per box (consult lane `SHONEN.md` for canonical four box texts/order). Marker rule: `[x]` only when done and supported by named independent verifier; `[~]` when progress/evidence pointer exists but remains incomplete; `[ ]` untouched/no supporting pointer. Each line needs a resolvable evidence pointer appropriate to its marker. The required literal gate is `grep -c '^## SHONEN'` on the final report; record command and observed count (expected exactly one).
7. **Stale-lane line** — include the explicit stale-lane status, not merely mention a final hash. State respawn-per-round and whether another lane mission remains open, only as observed/declarative facts.
8. **Tool installs/updates** — explicit line listing tool, version, channel, and reason for every install/update, or “none”; do not omit because there were no installs.
9. **Misroot sweep** — enumerate misrooted reports/artifacts discovered, recovery/copy evidence and cleanup status, or state sweep found none. Round 33 disclosed one report copied byte-exact and removed from fleet root (`round-33/kengaku.md:112`); do not silently omit this category.
10. **Pre-report gates** — after all lane changes, run `git ls-remote origin refs/heads/master` and compare its exact hash to final lane tip; report both and match/mismatch. Run `grep -c '^## SHONEN' <final report>` and report exact output. A stale/local-only hash or an unrecorded check is not a pass.
11. **Evidence discipline** — every numeric figure accompanied by producing command and output; quotes cite file:line/section. Separate observed fact from inference, preserve stdout and exit codes, and label inaccessible/unrun checks rather than inventing results.

## Round-33 content not to regress

- Keep all six named report sections and ordering: Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN (`round-33/kengaku.md:8,18,27,85,91,99`). Add the stale-lane, tool-install, misroot-sweep, and pre-report-gate lines without displacing them.
- Preserve detailed census before/after outputs, command, exit codes and explicit W04 delta; report registry/knowledge/index counts with source and measurement method (`:35-83`).
- Preserve claim-specific caveats and honest limitations: round-33 identified a false transition, counter blind spots, and unproven endpoint provenance (`:13-15,31-33,112-114`). Round 34 must likewise expose any failed frozen predicate and must not call counter success proof of source authenticity.
- Keep frontier scope narrow and explicit, distinguish what was discharged from what remains open (`:87-89`); include sourced claim and actual admission/refusal reasons.
- Preserve per-axis trend reasoning and explicit “no score changed/no axis harmed” only if supported (`:91-97`).
- Preserve SHONEN evidence pointers and status semantics, explicit stale-lane line, dead-seat/residual-call disclosure, open L0 status, tool-install disclosure, and misroot recovery disclosure (`:99-115`).

**Counterexample / attack:** A report can satisfy every claim counter while still be noncompliant if it omits the literal SHONEN marker-count gate or reports only the local tip instead of the remote comparison. C1's frozen counter checks corpus/index/frontier/capture conditions, not report shape or remote publication; C2's counter is explicitly separable from C1 artifacts (`round-34-claims.md:48-54,102-105`). Thus require these report-level gates independently.

VERDICT: critic-report-checklist (11 items)