## Round 55 — registry closure under a newly frozen rule; entry-argv structural binding; thirteenth TB2 grader executed (coverage attempt, L0-capped)

Base `798f5e9ef30ef39291295565209b65a17343c00e`; frozen claims and instruments
`plans/round-55-claims.md` at freeze commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`.
Frozen predicates: `plans/round-55-claims.md`. Before receipts:
`.ufo/waves/round-55/claims/c1-before.txt`, `c2-before-abbreviated-selftest.txt`,
`c2-before-uv-decoy-script.txt`, `c3-before.txt`.

Measured revision for all after receipts: **<PENDING-L1>**, clean shared clone.

| claim / axis | before → after evidence | counting command | predicate / score |
|---|---|---|---|
| R55-C1 / operability | ADVERTISED 79, REGISTERED 77, MISSING 2 (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`), INCOMPLETE 0, ENTRY-MISSING 0, SELFTEST-UNBACKED 0, DUPLICATE 0, `PREDICATE R52-C2 fail`, exit 1 → (measured close pending) | `python3 plans/round52_c2_registry.py --lane <clone>` | <PENDING-L1> |
| R55-C2 / calibration | abbreviated-selftest fixture: `PREDICATE R54-C2 pass`, counter exit 0, TRUE REGISTRY ENTRY exit 1 (laundering demonstrated); uv-decoy-script fixture: same shape (`PREDICATE R54-C2 pass`, exit 0, true entry exit 1) → (measured close pending) | `python3 plans/round55_c2_entryargv.py --lane <clone> --source <clean clone> --work <scratch> --jobs N` (fixture kills via `plans/round55_c2_controls.py --case <name>`) | <PENDING-L1> |
| R55-C3 / coverage (attempt, L0-capped) | probe receipt absent (exit 1); `grep -c thirteenth PROVINCE.md` → 0; `grep -c chess-best-move corpus/README.md corpus/SOURCES.md` → 0 0 → (measured close pending) | `python3 plans/round55_c3_chess_probe.py` (receipt `corpus/evidence/round55/chess-best-move-probe.txt`) | <PENDING-L1> — score capped at 7 by open L0 `kengaku | round-25/33/51` |

Receipts (after): `.ufo/waves/round-55/integrate/c1-after.txt`, `c2-after.txt`,
`c2-fixture-kills.txt` (PENDING-L1); probe receipt `corpus/evidence/round55/chess-best-move-probe.txt`
(PENDING-L1).

Notes for the close (PENDING-L1 items only):

- Axis state carried into round 55: calibration 9, coverage 7 (L0-capped), novelty 8, depth 9,
  operability 8 (harmed 9→8 in r54), freshness 9, adjacency 9. Axis dispositions after
  measurement: <PENDING-L1>.
- Registry rows added in round 55 (frozen): `round54-c1`, `round54-c2`, `round55-c2`,
  `round55-c2-controls`, `round55-c3`; frozen leg-2 truth spot-leg receipts under
  `.ufo/waves/round-55/integrate/`: <PENDING-L1>.
- Ledger truth corrections (data, before after-run): (a) `round35-c1-coverage` evidence
  fragment re-derived; (b) `round52-c2` stays green; (c) ledger rows added for the new
  registry rows — landing state: <PENDING-L1>.
- Kill-rule outcomes: C1 verdict-map cell truth at landing revision <PENDING-L1>;
  C2 soundness-break fixtures <PENDING-L1>; C3 oracle-identity / mismatch-counting / upstream
  identity at the pin <PENDING-L1>.
- Round shape: one v2 wave; dispatch records spawn 70 / total 70 with strict attack share
  28/70 = 40% (reviewer 12 + critic 10 + mutation-tester 6); settle-derived counts from
  `w1-results.json`: <PENDING-L1>.
- Census before receipt `.ufo/waves/round-55/claims/census-before.txt`; end receipt
  `integrate/census-end.txt`: <PENDING-L1>.
- R55-C3 sourced claim: SOURCES rows S201 (grader, code A) and S202 (instruction, docs A)
  opened 2026-10-30; amendment A1 drops the duplicate verifier-runner row (byte-identical to
  S109); knowledge entry `corpus/knowledge/tb2-chess-best-move-grader.md` admission under
  QUALITY Q1–Q17 with Q13/Q14 second-seat re-read: <PENDING-L1>.
- Assimilation none (114 mass-ID collisions under L0 `kengaku | round-54`); r52 GH013 L0
  unanswered (no new upstream capture committed; in-repo pinned bytes verified); r52-repair
  carried defect reconstructed as evidence (R11/RV3), production r52 counter unchanged.

### Planned (round 56)

< skeleton — L1 fills after outside closure of round 55 >
Carried items the close must resolve before new scope (PENDING-L1 where unknown): coverage
stays capped by open L0 `kengaku | round-25/33/51` unless those are answered; no assimilation
until the L0 `kengaku | round-54` mass-ID collision question is answered; the r52 GH013
push-protection L0 stays open; the r52 patch remains refused until its order-check regression
and masked K7 control are fixed; ledger/registry set equality and frozen-rule integrity are
the standing calibration baseline.
