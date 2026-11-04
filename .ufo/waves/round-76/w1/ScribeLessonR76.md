# ScribeLessonR76 — scoped drafting findings

Lane-root base for every relative pointer: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Axes: **coverage** (7, L0-capped), **calibration** (10, exercised). Behavior delivered: three integration drafts, not production edits or a round report. The canonical assignment governs; draft prose changes no contract or judgment.

## What ran and outcomes

**Shell/runtime commands executed by this seat: none.** No gates, census, git, fixtures, source fetch, tests, build, lint or formatter ran; there are no process exit codes to report as this seat's execution evidence. No installs/updates; no scratch tree created, so none remains to delete. Dedicated file read/search/write/edit tools supplied all observations and artifacts; their success is not a gate rc.

Read `plans/round-76-claims.md` in full before other tools, then the three assigned lessons: `corpus/lessons/round-75.md`, `round-74.md`, `round-75-verifier-spotcheck.md`. Read `SCORECARD.md:3375-3432`, `corpus/QUALITY.md` tail, `considerthese/2026-10-26.md:1-110`, the round76 evidence directory, both before receipts, census-before, C1/C2 controls/selftests/mutants, C2 git-state receipt, and local source capture lines 1698–1710. Subsequent targeted read observed `plans/round-76-claims.md` Amendment A1; search observed existing production lesson M76-5. Read godspeed and self-evaluation skills. No production file was edited.

Exact commands documented for the L1 (not executed here):

- `python3 plans/round76_c1_surface_resolver.py --lane .`
- `python3 plans/round76_c2_defect_discharge.py --lane .`
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`

The frozen claims report before gate rc 1 for both gates and before census rc 0. After rc 0 is a target, not an observation by this scribe. The receipt files inspected do not themselves print the shell process exit status.

## Verbatim lines that matter

`corpus/evidence/round76/c1-before.txt`:

```text
SURFACES total=11 present=4 absent=7 prose=0
AGREE agree=9 disagree=2
DEFECT STALE-TEXT 2 Local benchmark battery ~/archive/bench-arena/ asserts 'relocated intact' while absent
DEFECT UNDECLARED-ABSENT 4 Served local model (round 51 successor) http://127.0.0.1:45669
PREDICATE R76-C1 fail
```

`corpus/evidence/round76/c2-before.txt`:

```text
SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=2 wrong=12
PREDICATE R76-C2 fail
```

Conflict preserved: original frozen Before is `legs_pending=0 wrong=14`; receipt is `legs_pending=2 wrong=12`. Amendment A1 now explicitly corrects the prose to the receipt without changing the target/predicate/control/kill rule.

```text
CONTROL-SKIP rows=11 disagreements=1 target_reached=False
SELFTEST cases=7 red=6 failures=0 ok=True
MUTANTS total=5 killed=5 expected_matched=5 wrong_id=0 survived=0
CONTROL rows_claimed_closed=7 trivial_checks=1 failed_legs=3
SELFTEST cases=10 red=9 failures=0 ok=True
SELFTEST-GIT cases=3 failures=0 ok=True
MUTANTS total=8 killed=8 expected_matched=8 wrong_id=0 survived=0
```

These lines come respectively from `c1-control-declared.txt`, `c1-selftest.txt`, `c1-mutants.txt`, `c2-control-status.txt`, `c2-selftest.txt`, `c2-selftest-git.txt`, `c2-mutants.txt`. C1 selftest/mutant receipts both begin `LANE_TIP unknown` and `WORKTREE clean`; success tallies therefore do not establish a known measured commit.

## Numbered findings

1. **MEDIUM — C2 Before prose/receipt disagreement, corrected by L1 Amendment A1.** Pointer: `plans/round-76-claims.md` Before versus `corpus/evidence/round76/c2-before.txt:18`. Exact counterexample bytes are the two tally strings above; D4 and D5 are PENDING, so the receipt counts twelve rather than fourteen defects. Routed to `KengakuR76`, who confirmed and appended A1; the draft preserves the original conflict and the explicit correction. No fresh gate execution was needed or claimed.
2. **MEDIUM — unresolved C1 battery provenance at inspection time.** Pointers: `corpus/evidence/round76/c1-selftest.txt:1` and `c1-mutants.txt:1`, exact bytes `LANE_TIP unknown`. The drafts quote their passing tallies without treating them as revision-certified evidence. No counterexample execution or global stamp-policy verdict asserted.
3. **INFO — landing/census successes cannot yet be written as measured facts.** Pointer: inspected `corpus/evidence/round76/` directory listing lacked `c1-after.txt`, `c2-after.txt`, `census-after.txt`; L1 subsequently said these would be generated from a clean landing clone. All three drafts distinguish frozen targets from observed receipts. Census 243 → 244 is included as the prescribed trajectory, not a scribe-executed census result.
4. **LOW — proposal 1 has broader obligations than this discharge gate.** Pointer: `considerthese/2026-10-26.md:37-43` additionally requires age reporting and an over-two-round freeze refusal. Neither the frozen seven-id scope nor the inspected receipts establishes that global policy. QUALITY draft explicitly scopes the implemented witness and does not claim the whole proposal operational.
5. **LOW — existing Q55 citation needs semantic integration review.** Pointer: `corpus/QUALITY.md:1264-1270` cites lesson M76-5 for report-order/filed-byte discipline; the current production lesson M76-5 is actually **frozen-count collision**. L1 confirmed that M76-5 exists, so it is not a missing-anchor finding; its subject differs. The draft cites lesson Gate/Measurements and the closure R75-D1/D7 directly and does not invent a fifth assigned mistake or allocate a competing Q-number.

## Touched surfaces and artifact paths

Only these seat-owned outputs were written:

- `.ufo/waves/round-76/w1/ScribeLessonR76/corpus/lessons/round-76.md` — S252 admit, two reject flips, supplied M76-1…M76-4, controls/measurements/census/capability and explicit provenance limits.
- `.ufo/waves/round-76/w1/ScribeLessonR76/SCORECARD.md` — two claim rows with before→target, commands, pending verdicts and held scores; capabilities row and planner-seat mapping.
- `.ufo/waves/round-76/w1/ScribeLessonR76/QUALITY.md` — D1 criterion draft grounded in proposal 1 and the round-76 lesson; scope limit and numbering ownership explicit.
- `.ufo/waves/round-76/w1/ScribeLessonR76.md` — this report.

Production `corpus/`, `plans/`, PROVINCE, SKILL, SCORECARD, LOG and QUALITY intentionally unchanged by this seat. No judge/commit/push/deploy/runtime invocation, fleet/sibling edits, or broad report writing.

## Known limits / unverified

Historical failing runs for M76-1…M76-4 are assignment-supplied, not independently replayed or backed by newly discovered historical logs here. S252 URL/date/HTTP/size/hash are frozen-claims provenance; the local quote was inspected, but no fetch/hash was run. After predicates, final ledger discharge, capability admission, 244-row census, final report ordering, wave completion and no-axis-harmed are not verified by this seat. L1 should run the three exact commands above after integration and attach revision-bound receipts before replacing pending verdicts. Do not integrate this draft over existing later mistakes or corrections; it supplies the assigned four incident rows only.

## Self-evaluation

Accuracy 4/5 (all after states remain explicitly pending; source digest is attributed, not independently checked); completeness 4/5 (all three requested drafts delivered; final receipts belong to L1 and were unavailable at draft time); clarity 4/5 (target/evidence separation explicit but integration notes lengthen prose); actionability 4/5 (exact paths and commands supplied; final verdicts still require landing receipts); conciseness 4/5 (provenance cautions repeat across independently integrable fragments). Overall 4.0/5. Improvement priorities: integrate clean revision-bound receipts, reconcile Q55's semantic citation, then remove draft-only duplication when filing. User agreement expected on the distinction between completed drafts and unexecuted gates.
