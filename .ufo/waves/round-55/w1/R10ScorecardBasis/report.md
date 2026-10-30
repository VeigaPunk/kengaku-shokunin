# R10ScorecardBasis — seat report (kengaku round 55, w1)

**Task:** Verify the freeze's carried axis numbers against SCORECARD.md at the tip, and confirm
the freeze's no-stagnation-waiver claim against the declared saturation line 8 / window 4.

**Method:** Pure read-only verification. No clone, no fixture, no counter execution was in
scope (the seat verifies documentation consistency, not instruments). One scratch dir was
created per contract and removed empty.

## What I ran (commands + exit codes)

| command | exit |
|---|---|
| `read plans/round-55-claims.md` (freeze, commit 80afa613) | 0 |
| `read SCORECARD.md` (head + :573-578 + :2203-2245 + :2271-2295 + :2337-2397) | 0 |
| `grep -n` over SCORECARD.md for round-54 rows, measured close, Saturation, capability rows | 0 |
| `grep -n` over plans/round-55-claims.md for axis-state/stagnation lines | 0 |
| `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`; `git status --porcelain` (dirty tree = other seats' in-flight work; untouched by this seat) | 0 |
| `mkdir -p` wave output dir + scratch dir; final `rm -rf` of scratch dir | 0 |

No installs, no network calls, no git/jj mutations, no subagents.

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/R10ScorecardBasis.md`
  — scoped findings (axis table + stagnation check + defects). Same content as below.
- This report.

## Findings (see R10ScorecardBasis.md for the full table)

**Axis state: all seven numbers match.** calibration 9 (SCORECARD.md:2347, r53 :2307,
correction :2390), coverage 7 L0-capped (:2356), novelty 8 (:2346, r53 :2306), depth 9
(:2356-2357, :2390), operability 8 harmed 9→8 (:2384, mechanism :2385-2388), freshness 9
(:2356-2357, :2390), adjacency 9 (:2356-2357, :2390). Freeze quotes at
plans/round-55-claims.md:4-5. Lowest-axis claim (coverage 7) consistent.

**Stagnation: conclusion consistent, reason imprecise.** Declared rule SCORECARD.md:577
(line 8 = every owned axis ≥8; window 4 = no capability row within 4 completed rounds).
Limb 1 fails on coverage 7 < 8 → nudge not invoked (freeze correct). Limb 2 independently
agrees (r51 entered the surface-truth manifest counter, SCORECARD.md:2241; r52/r53/r54 none).
Defect: freeze's "(axes sit below the saturation line 8)" is wrong in the plural — 6 of 7
axes are ≥8; only coverage is below. Minor frozen-prose fidelity issue; not a rule/number
error; L1 may amend by dated row if judged material.

## Dead ends

None. No unrun checks (nothing in scope required execution).
