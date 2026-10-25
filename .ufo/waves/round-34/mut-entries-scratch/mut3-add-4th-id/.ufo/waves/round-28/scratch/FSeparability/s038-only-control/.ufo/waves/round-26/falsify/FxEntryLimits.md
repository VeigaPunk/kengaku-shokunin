# FxEntryLimits — round 26 C1 draft review

Scope: draft `.ufo/waves/round-26/drafts/grader-perturbation-audit.md` (proposed admission path `corpus/knowledge/grader-perturbation-audit.md`); compared with `plans/round-26-claims.md` Amendments 1–2 and `corpus/lessons/round-26.md` §Gate/M44.

## Findings by severity

None. The requested negative-space limits are stated and I found no broader population or future-performance guarantee.

- **CP / iid:** the entry calls intervals nominal/descriptive and explicitly denies independent-binomial or independent-generalization coverage over correlated deterministic transforms. This matches Amendment 1 §4 and M44.
- **Duplicates / clustering:** it reports 1,451 unique `raw+want+grader` inputs and 513 excess duplicates, notes shared turns and model/conversation format clustering, and reports the F1/F2 file+pid composite as 187/194, CP95 [0.927072, 0.985372], INDETERMINATE. It does not present pooled PASS as an iid inference.
- **Extrapolation / future probability:** “What this does not establish” disclaims live capability, endpoint identity, future-response failure probability, and natural format frequency; unobserved formats are not generalized to.
- **Format negative space:** the entry limits F1/F2 to the last matched answer fence and marks unmatched closing fences inapplicable. It separately excludes bracket-bearing suffixes, deeper nested JSON, invalid JSON, and unobserved fence variants. It reports the MULTI counterexample (14/31; 0/17 baseline-PASS) and explicitly warns that pooled PASS does not erase it.
- **R8/R9 provenance:** it explicitly says historical run-script byte provenance is weaker than R11/R12 machinery pins. The R8-only MULTI counterexample is not represented as live-model or independently authenticated provenance.
- **Claim strength:** family rates are finite-corpus observations; MP/MC bar results are described, while D1 is explicitly PC and NOT_SCORED for robustness. F5/F6 use fixed bracket-free strings; their “cannot add a parseable bracket candidate” interpretation is consistent with those transforms, not a claim about bracket-bearing suffixes.

## Verification and gaps

- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary` — exit 0. Key output: F1/F2 `n=1819 k=1802`, pooled PASS; composite `194/187`, INDETERMINATE; MULTI `31/14`; formats `FJ1=1296 FJM=492 MULTI=31 DANGLE=57 BARE=88`; dedup `unique_raw_want_grader=1451 excess_duplicate_records=513`; total `1964`, excluded `0`, `15168` audited verdicts, `909` policy checks.
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — exit 0; independently agrees on all listed family n/k counts, including F1/F2 `1819/1802` and D1 `909/909`.
- Static evidence: `plans/grader_perturb.py:401-449, 504-563, 698-712`; `grader.py:121-134`; draft §Exact perturbation policy, §Observed finite-population results, and §What this does not establish.
- LSP device unavailable: `read xd://lsp` returned “No such tool”; therefore no LSP status/references/definition/diagnostics were available. Literal search was fallback only, not semantic proof. No installs or edits to production files.

Residual risk: these are scoped findings about the draft and pinned corpus only; they do not authenticate original R8/R9 run machinery or predict future responses.

VERDICT: PASS — every assigned limitation is explicitly bounded; no stronger generalization survives this review.