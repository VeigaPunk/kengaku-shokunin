# R34ReviewConsiderthese — Q23 draft review

Seat: R34ReviewConsiderthese (reviewer, leaf). Date: 2026-10-25.
Reviewed: `.ufo/waves/round-34/build/R34Considerthese/q23.md` vs `considerthese/2026-10-25.md`
(proposal 2) and the existing `corpus/QUALITY.md` Q22.

## Criterion matrix

| Check | Result | Evidence |
|---|---|---|
| Cites file + date | PASS | Draft header: `Source: \`considerthese/2026-10-25.md\`, proposal 2, lines 39–45`, `Date: 2026-10-25`; Lesson citation repeats file §Self-improvement suggestions, proposal 2 (2026-10-25), lines 39–45. Line range verified exact: proposal 2 spans lines 39–45 of the source (grep -n + read 39-51; line 39 opens the proposal, line 45 ends `byte-compared … D3 mechanically.`). |
| Names recurring class evidence (D2 r30→r31) | PASS | Verbatim core carries source line 41: "D2 is a recurrence" with r30/r31 context in the same quote; Lesson citation names "the recurring D2 and D3 receipt failure" as motivating evidence. |
| Names Q22 debt | FAIL (minor) | The draft never literal "Q22". Its Named-debt section restates the substance — "The persistent `corpus/defects.jsonl` ledger remains unimplemented" — but does not link it to Q22, which is the criterion that already names this exact debt (`corpus/QUALITY.md` Q22 Limits line: "it does not build the persistent `defects.jsonl` ledger … named here as debt"). The Q22 anchor is missing from the evidence chain. |
| Has mechanical check line | PASS | `**Mechanical check:**` paragraph present: pre-registration gate rejects recurrence count ≥2 unless a counter check for that class is present and its class-specific mutation test demonstrates detection; tip-receipt validator re-runs each `corpus/evidence/**` receipt and byte-compares output. |
| Not a restatement of Q22; adds recurrence-block rule | PASS | Q22 (`corpus/QUALITY.md` lines 257–271) is only the tip-receipt cheap half (receipts re-run at tip). Q23 adds the recurrence-block rule — class recurring twice blocks pre-registration unless a hardened counter check + class-specific mutation test demonstrates detection — which Q22 does not contain. Shared tip-receipt-validator clause is an extension from proposal (c), not a restatement. |

## Findings by severity

1. **[minor] Q22 debt not named by label** — `q23.md` (Named debt section) restates the
   unimplemented `corpus/defects.jsonl` ledger debt without citing Q22, although the check
   "Q22 debt" is the prior criterion's named debt and Q23 is the second half of the same
   proposal. Recommend adding a line tying the draft to Q22 (e.g. "Q22's named debt —
   persistent defects.jsonl ledger — remains unimplemented"). No factual content error;
   a missing anchor.

No other actionable findings. The citation line range (39–45) matches the source exactly;
the checkbox block is not a restatement of Q22; the mechanical check line is present and
operational.

VERDICT: review-q23 findings 1
