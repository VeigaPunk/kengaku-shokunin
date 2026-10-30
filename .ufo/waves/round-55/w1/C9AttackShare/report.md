# C9AttackShare — seat report

Date: 2026-10-30. Lane tip context: base `798f5e9ef30ef39291295565209b65a17343c00e`, freeze
commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (both read-only `git log` verified implicitly
via claims file header; no git mutation run).

## What I ran (all read-only; commands, exit codes)

1. `read plans/round-55-claims.md` — frozen round shape: one v2 wave, band 64–128,
   ≥25 % strict attack share (reviewer+critic+mutation-tester; sentinels excluded, r54 ruling). OK.
2. `ls .ufo/waves/round-55/` — found `w1-spec.json` (present, authoritative per seat item)
   and `w1-dispatch.json`. OK.
3. Python census over `w1-spec.json` → 70 items; roles
   `{executor:16, scribe:7, scout:7, reviewer:12, critic:10, mutation-tester:6, sentinel:4,
   revenger:3, connector:3, simplifier:2}`; strict attack = 12+10+6 = 28; share = 40.0000 %.
   Exit 0.
4. Python census over `w1-dispatch.json` `registry.members` (70, all `kind=spawn`) → identical
   histogram; `counts={spawn:70, resume:0, total:70}`; policy `maxLanes=70`,
   `waveMinLanes=64`, `waveMaxLanes=128`, `declaredMaxLanes=70`, `hardCeiling=256`. Exit 0.
5. Cross-checks: spec↔dispatch role histograms equal; 70-name sets equal; no duplicate seat
   names; single wave only (no `w2-*`); band 64 ≤ 70 ≤ 128; share ≥ 0.25. All True. Exit 0.
6. `grep` on `scripts/hyaku/ufo-wave-policy-v2.json` — band fields confirmed at lines 88–90
   (`waveMinLanes: 64`, `waveMaxLanes: 128`). Exit 0.
7. `sed -n 1345,1420p .ufo/waves/round-55/build_spec_w1.py` — the builder itself computes
   strict attack as reviewer+critic+mutation-tester (line ~1353) and prints share (no floor
   assert in the builder; the floor is a frozen claim rule, verified here by this seat).
   Exit 0.
8. `sed -n 215,230p plans/round-54-claims.md` — r54 said only "≥25 % attack roles"; the strict
   sentinels-excluded definition is the r55 freeze's restatement (r54 spot-check ruling). Exit 0.

## Files I wrote (seat-scoped only)

- `.ufo/waves/round-55/w1/C9AttackShare/share.md` — formula + numbers + verdict.
- `.ufo/waves/round-55/w1/C9AttackShare/report.md` — this file.
- `.ufo/waves/round-55/w1/C9AttackShare.md` — scoped findings (Report trailer target).

No lane repo files touched. Scratch dir `/fast/scratch/hyaku/kengaku-r55/C9AttackShare/`
created then deleted (it held no artifacts; the analysis ran in-repo read-only).

## Findings

- **Strict attack share: MET — 28/70 = 40.0 % ≥ 25 %**, margin +15.0 pp. Breakdown:
  reviewer 12, critic 10, mutation-tester 6.
- **Band: MET — 70 seats ∈ [64,128]**; spec `maxLanes=70` == policy `declaredMaxLanes=70`
  ≤ `hardCeiling=256`.
- **One wave: MET — only `w1`; dispatch `counts.total=70`, `resume=0`.**
- Sentinels (4) correctly excluded; if included the lax figure would be 45.7 % — irrelevant
  under the frozen rule.
- No duplicate seat names; spec and dispatch censuses agree exactly, so the pre-dispatch
  claim "attack share satisfied" is verifiable from data already on disk.

## Defects found

None. No shortfall to name loudly — the floor is cleared by 11 seats of slack
(17.5 attack seats would be the 25 % floor at 70 total; the wave carries 28).

## Dead ends

None. `w1-results.json` does not exist yet (wave unsettled) — the dispatch registry was used
as the role census, per the claims doc: "final count and role mix are recorded in the dispatch
file and re-derived from w1-results.json after settle." Post-settle re-derivation should
re-run this seat's formula against `w1-results.json` and must get the same 28/70 unless a
seat was dropped, in which case the floor must be re-checked (drop tolerance: up to 11
attack-seat losses, or any 37 non-attack losses, before the floor is at risk).

## Installs

None (no tools installed or upgraded).
