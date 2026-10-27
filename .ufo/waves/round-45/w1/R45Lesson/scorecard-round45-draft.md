# SCORECARD draft — round-45 section (paste at integration)

Shape copied from `SCORECARD.md:1929-1975` (round 44): a `##` heading that names the measured claim, a
baseline/freeze/landing paragraph, one table row per claim with `before → after` and the counting command, a
limits paragraph, an "other axes held" paragraph, and a `### Round-45 capabilities` table. **Nothing below is a
measurement this draft made**; `<<FILL: …>>` slots are the L1's at integration from the named receipt.

```markdown
## Round 45 (hyaku run 9, 2026-10-26): the advertised fixture fence calibrated to <<FILL: contradicted=0 | N>>
contradictions over ten hostile modules and 104 honest fixtures; an eleventh TB2 grader executed (exact
line-membership of one constant)

Baseline as read `9d5f9715ebb0343984171be312d44e681f96b9a8`; freeze `b4fcd35141acda5fa0980a34dd29ab880b702ee6`;
post-freeze C2 spec/counter re-pin `52d7486a8caf930855cd1f748032ac21648303f5` (both digests kept in
`.ufo/waves/round-45/claims/frozen-digests.txt`); probe receipt `23:27:11-23:27:15 -03`; claim landing
`<<FILL: hash>>`. Frozen prereg `plans/round-45-claims.md`. Lowest non-retired axis: coverage 7, tied with novelty
7; coverage chosen (frozen tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No stagnation
waiver. Landing measurement `<<FILL: .ufo/waves/round-45/integrate/measure-final.txt on a clean --no-local clone>>`,
baseline `<<FILL: integrate/measure-baseline.txt>>` at `b4fcd351`.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 the advertised fixture fence (`fenced-fixture-discovery`, SCORECARD round 44) vs the fence the counter runs — calibration count over the ten hostile modules of `plans/refusals45/` and the 104 honest fixtures of batteries 42+43+44 | **calibration** — advertised-vs-observed contradiction count for one lane gate tool | `python3 plans/round45_c1_verify.py --lane .`: before `REFUSALS total=10 clean=3 leaked=3 read=4`, `CALIBRATION advertised=10 contradicted=7`, `PREDICATE C1 fail` (`.ufo/waves/round-45/claims/control-c1-fence-r44.txt`; nothing control `contradicted=10`, `control-c1-nothing.txt`; refuse-all `HONEST refused=104`, admit-all `leaked=10`, static-only `contradicted=1`) → after `<<FILL: PINS total=33 mismatched=0 … REFUSALS total=10 clean=10 … HONEST fixtures=104 admitted=104 … CALIBRATION advertised=10 contradicted=0 / PREDICATE C1 pass, exit 0>>` | `<<FILL: score; calibration 8 held or moved>>` |
| C2 pinned TB2 `password-recovery` grader admitted with a 16-case executed probe (S149–S156, tier A) and the hardened held-out predictor leg V11 | **coverage** (lowest, tied) — one §Frontier TB2 sub-bullet narrowed by one task (11 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 51→52, SOURCES 141→149; a grader class distinct from round 44's substring-of-one-file: one constant as a whole line of an agent-written guess list (format-, case-, order-, count-free) | `python3 plans/round45_c2_verify.py --lane .`: before `checks=11 defects=8`, `PREDICATE C2 fail`, exit 1 (`.ufo/waves/round-45/claims/control-c2-nothing.txt`) → after `<<FILL: checks=11 defects=0 / PREDICATE C2 pass, exit 0>>`; probe `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`; V11 controls `CONTROL-C2-PREDICTOR red-as-required` (membership `ok … disagree=0`; always-true 30, substring 12, password-eq 21 disagreements; lookup-table lint DEFECT) | `<<FILL: coverage held 7 (L0 cap) or moved>>` |

Limits found by the wave (frozen counters not edited; routed): `<<FILL: fence held-out attacks by wave critic
seats; V11 residual (an open-coded truth table small enough to pass the lint); the entry's `source:` ranges; any
`sandbox escape` count>>`.

Other axes held: novelty 7 (no claim), depth 9, operability 8 (`<<FILL: riders>>`), freshness 8 (nine captures
re-fetched `cmp`-identical — this seat 23:3x `http=200` ×9, `R45ScoutRefetch` independently), adjacency 8
(`<<FILL: PROVINCE routing seat>>`).

### Round-45 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `fence-calibration-count` | Turn "the fence refuses what it says it refuses" into a count over hostile modules plus a 104-fixture honesty leg, with a refuse-everything control that fails | `python3 plans/round45_c1_verify.py --lane .` → `<<FILL>>`; controls `claims/control-c1-fence-{nothing,r44,admit_all,refuse_all,static_only}.txt` | `<<FILL: 45 or carried>>` |
| `whole-line-membership-grader` | Judge an entry's stated grader rule for a task whose score is one constant as one line of an agent-written file, with the predictor lint and a 48-state held-out sample | `python3 plans/round45_c2_verify.py --lane .` V11 `ok states=48 … disagree=0`; `claims/control-c2-predictor.txt` | `<<FILL>>` |

### Planned (round 46)

`<<FILL: from the wave's data-walk seat and the round-45 residual limits>>`
```

## Notes for the L1 (not part of the pasted block)

- The round-44 table's C1 cell ran to ~700 words; the block above deliberately keeps the *before* line verbatim
  (it is a receipt label, not prose) so a reader can diff it against `claims/control-c1-fence-r44.txt`.
- `contradicted=7` is the number this section may quote as the round's before-state without any new run; it is a
  committed control, not a this-seat measurement.
- If C1 does not pass, the round-45 section MUST say so in the heading, as round 43's section does for its seat
  floor — do not let the heading's kill count outrun the counter's last line.
