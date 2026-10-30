# C9AttackShare — scoped findings (round 55, wave 1)

**Verdict: strict attack share floor MET before dispatch settlement — 28/70 = 40.0 % ≥ 25 %,
inside the 64–128 band (70 seats, single v2 wave). No shortfall.**

## Derivation

Frozen rule (`plans/round-55-claims.md` §Round shape): strict attack = reviewer + critic +
mutation-tester; sentinels do not count (r54 spot-check ruling); floor ≥ 25 % inside band
64–128.

From `w1-dispatch.json` `registry.members` (70 seats, all `kind=spawn`), cross-checked
identically against `w1-spec.json` `items`:

- reviewer 12, critic 10, mutation-tester 6 → strict_attack = **28**
- total = **70** → share = 28/70 = **40.0 %** (floor 25 % → PASS, +15.0 pp margin)

## Shape verification

- Band: policy `waveMinLanes`=64, `waveMaxLanes`=128 → 70 ∈ [64,128] PASS.
- `maxLanes`: spec=70, dispatch `declaredMaxLanes`=70, `hardCeiling`=256 → sane PASS.
- One wave: only `w1` under `.ufo/waves/round-55/`; `counts={spawn:70, resume:0, total:70}`.
- Spec↔dispatch censuses identical; no duplicate seat names.

## Notes for the L1

- `w1-results.json` is not yet written (wave running); re-derive this formula after settle.
  Floor tolerance: attack-seat losses ≤ 11 (or any 37 non-attack losses) keep 25 %.
- Sentinels (4) excluded per the frozen rule; counting them would give 45.7 % — do not use
  the lax figure.

No defects found; no lane files touched. Full working notes:
`.ufo/waves/round-55/w1/C9AttackShare/share.md` and `report.md`.
