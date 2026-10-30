# Round 55 wave 1 — strict attack share derivation

Seat: C9AttackShare (critic). Date: 2026-10-30.
Authority: `plans/round-55-claims.md` §"Round shape (frozen before dispatch)" — band 64–128,
≥25 % strict attack share (reviewer + critic + mutation-tester; sentinels do not count — r54
spot-check ruling). Inputs: `.ufo/waves/round-55/w1-spec.json` and `w1-dispatch.json`
(both present on disk; `w1-results.json` not yet written — wave still running, so the dispatch
registry is the authoritative role census, with the spec as cross-check).

## Formula

    strict_attack = n(reviewer) + n(critic) + n(mutation-tester)
    share         = strict_attack / total_seats
    floor verdict = share >= 0.25  AND  64 <= total_seats <= 128  AND  maxLanes field sane  AND  one wave

Sentinels, revengers, connectors, simplifiers, scouts, scribes, executors are NOT attack roles
under the frozen strict definition.

## Numbers (dispatch registry, 70 members, all kind=spawn)

| role            | seats |
|-----------------|------:|
| executor        |    16 |
| scribe          |     7 |
| scout           |     7 |
| reviewer        |    12 |
| critic          |    10 |
| mutation-tester |     6 |
| sentinel        |     4 |
| revenger        |     3 |
| connector       |     3 |
| simplifier      |    2 |
| **total**       |  **70** |

strict_attack = 12 + 10 + 6 = **28**
share = 28/70 = **0.4000 = 40.0 %**  (floor: ≥25 % → **PASS**, margin +15.0 pp)

## Band and shape checks

- total seats = 70; policy `waveMinLanes`=64, `waveMaxLanes`=128 → 64 ≤ 70 ≤ 128 **PASS**.
- spec `maxLanes` = 70; dispatch policy `maxLanes` = 70, `declaredMaxLanes` = 70,
  `hardCeiling` = 256 → declared == actual, inside ceiling **PASS**.
- one wave: only `w1` exists under `.ufo/waves/round-55/`; dispatch `counts` =
  `{spawn: 70, resume: 0, total: 70}`; no `w2-*` file present **PASS**.
- spec vs dispatch census: identical role histograms, identical 70-name set, no duplicate
  seat names **PASS**.

## Verdict

**Strict attack share floor MET: 40.0 % ≥ 25 % inside the 64–128 band (70 seats, one v2 wave).
No shortfall.** If sentinels were (wrongly) counted the figure would be 32/70 = 45.7 %; the
frozen r55 definition excludes them and the floor is met without them.
