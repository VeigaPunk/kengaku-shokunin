# ConnChousa — chousa-shokunin overlap scan: statistics/interval convention (round 25)

Read-only scan; no sibling or lane write. chousa HEAD `d730ae4c33989ad9c8535764d4cae77b4db869f6` (2026-10-19, round-24 verifier spot-check); kengaku base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`. No network, no installs.

## Answer to the assigned question
chousa's QUALITY and SKILL define **no statistics or interval convention**. There is nothing there for C1's Clopper–Pearson verdicts or C2's re-derivation to cite instead of building. The genuine overlaps are research-method surfaces (already declared chousa's and routed out by kengaku) and fleet `PROTOCOL.md` evidence/gate rules (cite the fleet file, not chousa).

## Sweep (negative claim carries its sweep)
- Governance surface, **0 hits** (`grep` exit 1): `grep -rniE 'clopper|wilson|confidence interval|credible interval|rogan|gladen|binomial|interval estimat|statistical power|sample size' SKILL.md corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge/ SCORECARD.md PROVINCE.md SHONEN.md MINT.md` (cwd `chousa-shokunin`).
- Wide tokens (`uncertainty|significance|p-value|interval|power|sample`) → 11 hits, none a convention: replay/audit "samples" (`corpus/knowledge/claim-verification-r2.md:5,31,134`; `audit-r11.md:259`; `SCORECARD.md:294` "28 samples"), quantities compared at a citation hop (`corpus/knowledge/citation-chain-fidelity-r24.md:25-26`), one quoted study's "n=86" (`:33`).
- Whole tree incl. `.ufo`: **1 hit**, `chousa-shokunin/.ufo/plans/round-1-interactive-20261015T050057Z.md:19` ("source uncertainty") — a round-1 plan note, not a convention.
- Fleet `AXES.md PROTOCOL.md PROTOCOL-APPENDIX.md LEARNING.md CORPUS.md MISSION.md ROADMAP.md`: **0 hits** on the same interval pattern.

## Overlaps, rulings, routing
| # | overlap | chousa evidence | ruling | what kengaku should cite / route |
|---|---|---|---|---|
| O1 | statistics/interval convention | absence (sweep) | **none** | C1 owns it. Cite kengaku's own `corpus/SOURCES.md:33` (S011 sens/spec-bias correction), `:37` (S015 error bars/power), `:40` (S018 resolution) plus the sources opened this round. Do not route to chousa. |
| O2 | per-claim source admission | `chousa-shokunin/SKILL.md:22`; `corpus/knowledge/contextual-source-admission-r24.md` | **adjacent-report-out** | Already routed at `PROVINCE.md:133`, `corpus/QUALITY.md:7-8`, `corpus/SOURCES.md:17`. C1 rows follow kengaku's SOURCES contract v1 + Q1/Q2/Q5; do not copy chousa's seven admission fields into kengaku. |
| O3 | claim-support four states | `chousa-shokunin/SKILL.md:23`; `corpus/knowledge/claim-support-states-r24.md:13-15` | **adjacent-report-out** | In-lane equivalent is Q3/Q4. Consequence for C1: each new row's <=25-word quote must *state* its `teaches` cell at the named anchor; on-topic-only leaves the claim unresolved. |
| O4 | counting command / absence sweep / quote location | `chousa-shokunin/SKILL.md:62` restates it; the home is fleet | **none** (fleet-owned) | Cite `../PROTOCOL.md:352` for C1's "Before" sweep and C2's counting command. No chousa citation. |
| O5 | gate contract (exit 0/1/2, `--selftest`, offline, no live-tree write, finding id) | `chousa-shokunin/SKILL.md:66-78` is an instance | **none** (fleet-owned) | Cite `../PROTOCOL.md:386-388`. |
| O6 | disagreeing estimators | `chousa-shokunin/SKILL.md:44` "report both; do not average them" | **adjacent-report-out** | C1's CP verdict + Wilson sensitivity column already conforms; cite only if method provenance for not blending is wanted. |
| O7 | count != semantic proof; no "improved" from a census | `corpus/lessons/round-24-verifier-spotcheck.md:17`; `SCORECARD.md:575` | **adjacent-report-out** (precedent) | Supports C2's declared decision not to claim calibration +1; no rule imported. |
| O8 | one home per number; append-only erratum | `corpus/QUALITY.md:33` (crit. 9), `:52` (crit. 12) | **none** | chousa's criteria are lane-local restatements of fleet `PROTOCOL.md:512-516`; kengaku R1/R5 (`corpus/QUALITY.md:86,90`) already instantiate them. No citation, no routing. |
| O9 | model-evaluation province | `chousa-shokunin/PROVINCE.md:10`; `SKILL.md:53` refuse model-quality -> kengaku | **none** | chousa will not claim C1's instrument accuracy; no filing needed. |
| O10 | chousa's own r25 planned claims | `SCORECARD.md:1282-1296` (metadata screen, index re-derive, stale restatements) | **none** | No statistical construct and no shared artifact/population with C1/C2; do not report C2 as duplicating its claims 2/3. |

**No duplicate found.** The only duplication risk is prospective: restating O2's admission fields or O3's four states inside kengaku — the rulings above say cite, do not restate.

## Handed to C2 (path/anchor hazard, actionable)
`plans/round-25-claims.md:14-15` and `:70` cite bare `AXES.md:12` / `AXES.md:15`; the lane has no `AXES.md` (verified absent at lane root). Fleet `/home/vgpnk/Projects/shokunin/AXES.md:12` (coverage/"edge classes") and `:15` (calibration) do match the quotes, and the lane's established form is `../AXES.md` (`corpus/QUALITY.md:93`; `SCORECARD.md:8,13,63`). A lane-root resolver will emit spurious P2b/P2d mismatches — resolve fleet files via `../` or the fleet root. Same for P2c's seed: fleet `../PROTOCOL.md:439`; and the novelty mapping's warrant: `../PROTOCOL.md:505-516` (rule at `:514-516`).
Prior in-lane precedent for keeping analysis in-lane: `corpus/evidence/round11-fleet/r11-connector.md:13`; `corpus/evidence/round12-fleet/r12-connector.md:99`.

installs: none
VERDICT: no chousa statistics/interval convention exists to cite — keep C1's interval instrument and C2's re-derivation in-lane, route nothing new to chousa, and cite fleet `../PROTOCOL.md:352,386-388,439,505-516` for the sweep/counting-command/gate/seed/mapping rules.
