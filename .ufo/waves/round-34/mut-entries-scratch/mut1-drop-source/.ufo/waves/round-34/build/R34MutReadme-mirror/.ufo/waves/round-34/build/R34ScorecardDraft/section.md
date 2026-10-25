## Round 34 — coverage move; calibration hardened (draft)

The lowest non-retired axis is **coverage (7)**, tied with **novelty (7)** at the frozen baseline. Per the recorded tie-break, coverage wins: the pinned TB2 evaluator can be opened and grounded against expected artifacts with local tools, while the novelty alternative lacks an identity-verified endpoint. The canonical coverage score remains capped at 7 while the round-25 L0 cap is open; report a ledger delta and `improved` trend, not a raised score. Frozen basis: `plans/round-34-claims.md` lines 10–16, 66–69.

### Claims

| Claim | Before → After | Counting command / evidence | Score | Verdict |
|---|---|---|---|---|
| C1 — TB2 `protein-assembly` evaluator opened and grounded against `antibody.fasta` and `pdb_ids.txt` | [MEASURED] → [MEASURED] | `python3 plans/round34_c1_verify.py --lane .` → [MEASURED]; inspect `.ufo/waves/round-34/` capture and committed receipts | Coverage 7 → 7 (capped); ledger delta [MEASURED] | [MEASURED] |
| C2 — defect counter and mutation harness cover four defect classes | [MEASURED] → [MEASURED] | `python3 plans/round34_mutate.py`; `python3 plans/round34_defects.py --lane .`; selftests per frozen predicate | Calibration [MEASURED] → [MEASURED] | [MEASURED] |

### Axes

| Axis | Before → After | Evidence / score rationale |
|---|---|---|
| **coverage** *(lowest-axis obligation)* | 7 → [MEASURED] (canonical cap 7) | C1 opens the pinned task evaluator and records new grounded corpus evidence; score movement remains capped per frozen claim. [MEASURED receipt pointer] |
| **calibration** | [MEASURED] → [MEASURED] | C2 has red-before receipts by class and green-after mutation/counter evidence. [MEASURED receipt pointer] |
| novelty | [MEASURED] → [MEASURED] | [MEASURED: state held unless a sourced, independently qualifying novelty result exists.] |
| depth | [MEASURED] → [MEASURED] | [MEASURED] |
| operability | [MEASURED] → [MEASURED] | [MEASURED] |
| freshness | [MEASURED] → [MEASURED] | [MEASURED] |
| adjacency | [MEASURED] → [MEASURED] | [MEASURED] |

### Capability rows (include only if demonstrated)

| Capability | Evidence | Verdict |
|---|---|---|
| [MEASURED: add only a capability demonstrated by round-34 receipts; otherwise remove this table.] | [MEASURED] | [MEASURED] |

### Frontier and assimilation

Census before → after: [MEASURED] (attach the exact command and exit/output from the closeout receipt). Mistake mined: [MEASURED; cite `corpus/lessons/round-34.md` section/line]. Sourced claim: C1, supported by the round's located Gate quotes and captured bytes [MEASURED receipt pointers]. Quarantine/admission verdicts and reasons: [MEASURED; cite Gate/report].

### Planned (next axis-move)

[MEASURED: name the next lowest non-retired axis and tie-break from the landed scorecard; state one falsifiable move, its counting command, and known cap. Do not infer next-round values from this draft.]
