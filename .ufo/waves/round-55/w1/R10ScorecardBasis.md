# R10ScorecardBasis — freeze §axis-state vs SCORECARD.md at tip

Seat: R10ScorecardBasis (kengaku round 55, w1). Scope: read-only verification.
Lane tip at review: `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (the landed freeze commit).
SCORECARD round-54 authority: the "Round-54 measured close — correction" block
(SCORECARD.md:2364-2397), which supersedes the round-54 section's earlier
"remain 9" for operability only.

## Axis-state table (acceptance: axis | scorecard line | freeze line | match)

| axis | scorecard line (quote) | freeze line (quote) | match |
|---|---|---|---|
| calibration 9 | SCORECARD.md:2347 — R54-C2 row: "**not admitted; 9→9 held — frozen kill rule fires**"; entering value confirmed by r53 close SCORECARD.md:2307 ("calibration **9→9 held**"); correction SCORECARD.md:2390 "All other scores remain as recorded." | plans/round-55-claims.md:4 — "Axis state carried from round 54: **calibration 9**, coverage 7 (L0-capped), …" | YES |
| coverage 7 (L0-capped) | SCORECARD.md:2356 — "**Coverage remains 7** (open L0 cap round-25/33/51; not waived)" | plans/round-55-claims.md:4 — "coverage **7 (L0-capped)**" | YES |
| novelty 8 | SCORECARD.md:2346 — R54-C1 row: "**not admitted; 8→8 held**"; r53 close SCORECARD.md:2306 "novelty **8→8 held**" | plans/round-55-claims.md:4 — "novelty **8**" | YES |
| depth 9 | SCORECARD.md:2356-2357 — "…depth/operability/freshness/adjacency remain 9." + correction SCORECARD.md:2390 "All other scores remain as recorded." | plans/round-55-claims.md:4 — "depth **9**" | YES |
| operability 8 (harmed 9→8) | SCORECARD.md:2384 — "**Operability harmed, 9→8**, superseding this section's earlier 'remain 9' for operability"; harm mechanism SCORECARD.md:2385-2388 — `integrate/round52-c2-regression.txt`, the registry counter reporting two missing newly advertised rows (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`), exit 1 | plans/round-55-claims.md:5 — "operability **8 (harmed 9→8 in r54 by the registry regression)**" | YES |
| freshness 9 | SCORECARD.md:2356-2357 — "…freshness/adjacency remain 9." + SCORECARD.md:2390 | plans/round-55-claims.md:5 — "freshness **9**" | YES |
| adjacency 9 | SCORECARD.md:2356-2357 — "…freshness/adjacency remain 9." + SCORECARD.md:2390 | plans/round-55-claims.md:5 — "adjacency **9**" | YES |

Also checked: freeze "Lowest non-retired axis: **coverage 7**" (claims.md:6) — coverage 7 is
the unique minimum of the carried set {9,7,8,9,8,9,9}. Consistent.

All seven carried numbers match the round-54 measured-close state, including the
correction-superseded operability value. The freeze's parenthetical characterizations
("L0-capped"; "harmed 9→8 … by the registry regression") are faithful to the SCORECARD text.

## Stagnation-waiver consistency (declared rule: SCORECARD.md:577 `## Saturation`)

Declared (round 24, SCORECARD.md:577): "saturation line: 8 (**every owned axis at ≥8**);
stagnation window N: 4 rounds (**no capability row entering within 4 completed rounds**)."

Freeze claims (plans/round-55-claims.md:6-7): "The stagnation nudge is not invoked (axes sit
below the saturation line 8)."

Verdict: **conclusion CONSISTENT; freeze's stated reason IMPRECISE.**

- Limb 1 (every owned axis ≥ 8): FAILS — coverage 7 < 8. The nudge's precondition is not
  met, so "not invoked" is correct under the declared rule.
- Freeze's reason as written is wrong in the plural: in the carried state 6 of 7 axes are at
  or above the line (calibration 9, novelty 8, depth 9, operability 8, freshness 9,
  adjacency 9); only coverage 7 sits below 8. Accurate phrasing would be "coverage sits below
  the line" / "the lowest axis sits below 8". Defect class: prose fidelity in a frozen
  justification, not a number, predicate, counter, or kill-rule error. Per the freeze's own
  amendment rule, any correction is L1's dated amendment row, not a seat edit.
- Limb 2 (window 4), not cited by the freeze, independently agrees: within the four completed
  rounds 51-54, r51 entered a capability row — SCORECARD.md:2241 "Capability entering the
  table this round: **surface-truth manifest counter** … first working round 51" — while r52
  (SCORECARD.md:2270 "No capability row enters"), r53 (:2322 "No capability enters…") and r54
  (:2391 "No claim admitted and no capability enters") entered none. (R51 sits exactly at the
  4-round window boundary; limb 1 already settles the verdict, so the boundary reading cannot
  change the outcome.) Precedent: the r52 preamble states the same conclusion explicitly
  (SCORECARD.md:2249 "Stagnation nudge not invoked.").
- Note: the r24 declaration's own basis sentence ("inactive while novelty sits below 8",
  SCORECARD.md:577) no longer applies since novelty is now 8; the freeze relies on the
  coverage limb instead, which is the correct limb under the declared rule.

## Defects found

1. (minor, frozen-prose) plans/round-55-claims.md:6-7 — "axes sit below the saturation line 8"
   misdescribes the carried axis state; only coverage 7 is below the line. The no-waiver
   conclusion is nonetheless consistent with SCORECARD.md:577 via both declared limbs.
   No seat may edit the freeze; L1 may file a dated amendment if judged material.

No other defects. No sibling-file defects observed in scope; SCORECARD.md numbers are
internally consistent across the r54 section (2346-2358), the measured close (2364-2392),
and the r53 close (2306-2321).

## Verification gaps / residual risk

- L0 question currency (round-25/33/51 still unanswered) was not independently re-derived;
  the seat checked consistency of the freeze's cap citation with SCORECARD.md:2356, not the
  L0 ledger itself.
- The stagnation window boundary (whether r51 counts as "within 4 completed rounds" at the
  round-55 freeze) was inspected but cannot change the verdict, as limb 1 fails regardless.
