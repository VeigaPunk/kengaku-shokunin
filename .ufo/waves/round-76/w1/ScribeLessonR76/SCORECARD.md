## Round 76 (2026-11-04) — live declared-surface resolution and executable routed-defect burn-down

Draft section for L1 integration; not a filed verdict. Base `fda63968f29f8f58dc2b28831acac879405b8326`; freeze `42fad4827797e540c60a00821d3f2f5c18539632`. Contract `plans/round-76-claims.md`; Amendment A1 corrects only C2's Before description to its actual receipt. Axes: **coverage**, **calibration**.

| claim / axis | before → after evidence | counting command | verdict / score |
|---|---|---|---|
| **R76-C1 / coverage** — lowest non-retired axis, L0-capped at 7; every PROVINCE surface resolved live and its dated declaration priced | Observed receipt `corpus/evidence/round76/c1-before.txt`, stamped `fda63968…`: `SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=9 disagree=2`, `DEFECT STALE-TEXT 2`, `DEFECT UNDECLARED-ABSENT 4`, `PREDICATE R76-C1 fail` (rc 1 per contract) → **after pending at draft time**; frozen target is the same surface counts with `AGREE agree=11 disagree=0`, no defects, `PREDICATE R76-C1 pass`, rc 0, intended receipt `corpus/evidence/round76/c1-after.txt` | `python3 plans/round76_c1_surface_resolver.py --lane .` | Before fails; after not yet evidenced to scribe, so admission is pending, not asserted. Coverage **7 → 7**, L0 cap held. |
| **R76-C2 / calibration** — held at 10, exercised; R75-D1…D7 registered and discharged by re-derived values and ancestor closing commits | Observed receipt `corpus/evidence/round76/c2-before.txt`: `SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=2 wrong=12`, seven `MISSING-ROW`, `PREDICATE R76-C2 fail` (rc 1 per contract) → **after pending at draft time**; frozen target `SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0`, no `DEFECT`/`LEG-FAIL`, `PREDICATE R76-C2 pass`, rc 0, intended receipt `corpus/evidence/round76/c2-after.txt` | `python3 plans/round76_c2_defect_discharge.py --lane .` | Before fails; after not yet evidenced to scribe, so admission is pending, not asserted. Calibration **10 → 10**, ceiling held; batteries report exercise, not landing acceptance. |

C2 original Before prose `legs_pending=0 wrong=14` disagreed with the actual `legs_pending=2 wrong=12`; Amendment A1 preserves and corrects the discrepancy. D4/D5 are PENDING in that rev-mode receipt. This draft neither changes the frozen target nor promotes the contract into execution evidence.

Controls read, not re-executed: `c1-control-declared.txt` prints `CONTROL-SKIP rows=11 disagreements=1 target_reached=False`; `c2-control-status.txt` prints `CONTROL rows_claimed_closed=7 trivial_checks=1 failed_legs=3`. Both print their control predicate `pass`: the fake-completion controls lose as intended. C1 selftest/mutant receipts report 7/6 and 5/5 respectively but stamp `LANE_TIP unknown`; C2 reports 10/9, git cases 3, mutants 8/8. Provenance defects must not be hidden by success tallies.

**capabilities:** proposed `declared-surface-resolver`; enter through a demonstrated C1 landing pass, not through this declaration.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| declared-surface-resolver | Resolves every PROVINCE surface live (paths with brace expansion and `test -e` semantics; localhost HTTP status) and prices dated ABSENT declarations plus stale present-tense text | `python3 plans/round76_c1_surface_resolver.py --lane .`; intended witness `corpus/evidence/round76/c1-after.txt` (**pending at draft time**) | 76 (conditional on demonstrated pass) |

**Planner-seat mapping:** L1 `KengakuR76` holds §3's planner seat; the planning data-walk rides scout `ScoutFrontierR76`. Frozen wave shape: one v1 wave, 14 seats (executor 3, scribe 3, scout 1, connector 1, reviewer 2, critic 1, mutation-tester 1, labrat 1, sentinel 1); attack 5/14 = 36%. These are contract counts, not execution/completion evidence.

Census trajectory **243 → 244** is contract-declared. `corpus/evidence/round76/census-before.txt` was read (25 W04 lines and `ok`); after receipt and 244-row validation are **pending at draft time**. Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (not run by this scribe).

Other scores are intentionally unchanged here: novelty 8, depth 10, operability 10, freshness 10, adjacency 9 (carried from round 75). No claim that every owned axis was independently re-measured or unharmed is made by this draft. Proposal provenance: `considerthese/2026-10-26.md` proposal 1; lesson `corpus/lessons/round-76.md`.
