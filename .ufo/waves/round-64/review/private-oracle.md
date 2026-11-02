# Kengaku64 reviewer private oracle
Reviewer: /root/judge_kengaku_round64 (parent appointed, not author dispatched).
Author contract: 5e1c817fca0799419ceceee0ab409d6d5f019c32.
Frozen before challenge exposure, 2026-11-02. Manual derivation only.

Complete-case A easy9/10 hard3/10; B easy19/20 hard7/15, B superior in both. Pooled A90/140=9/14; B80/130=8/13; A-B=5/182. Different observed stratum proportions cause Simpson reversal, not evidence A dominates. Common target easy1/4 gives A9/20=.45, B47/80=.5875, B-A11/80=.1375; descriptive, missingness not identified away.

All assigned n100 each. A easy[.72,.92], hard[.18,.58]; B easy[.38,.98], hard[.42,.52]. Weighted A[.315,.665]=[63/200,133/200]; B[.41,.635]=[82/200,127/200]; B-A[-.255,.32]=[-51/200,64/200]. Both endpoint completions achievable: B missing all0/A all1 gives lower; reverse upper. Paired prompts do not restrict cross-system missing binary values. Bounds are identification sets, not confidence intervals or deployment estimates. Finite-panel robust margin .05 fails (HOLD), not proof B is worse.

Cost denominator100 each regardless outcome. A easy200/100=2 hard400/100=4; weighted3.5. B easy300/100=3 hard600/100=6; weighted5.25 meets inclusive5.4. Cost met is not enough for quality; success/completion denominators wrong. Deadline records remain known zeros even if later responses arrive; do not add them to u.

Recovered original contemporaneous logs (not rerun): A adds10 easy12 hard, B adds12 easy8 hard. Rates A(.82,.30), B(.50,.50). At easy1/4, A.43, B.50, B-A.07: finite-panel policy GO, population release HOLD (no sampling/transport assurance). 60-second outcomes cannot be retroactively substituted for90-second? Correct policy in challenge is60 seconds; later90-second results excluded.

For easy weight w in[1/5,3/10], recovered contrast=.20-.52w, sign crossing5/13. Margin>=.05 iff w<=15/52. B cost6-3w<=5.4 iff w>=1/5. Joint eligible weights[1/5,15/52]; robust across full declared interval fails atw=.3 (gap.044). Atw=.2 gap.096, cost5.4 inclusive passes. Atw=.3 cost5.1. Cost ceiling5.0 requires w>=1/3, disjoint from margin set, so none. Do not switch weights post hoc to obtain GO.

Repair: recover immutable original logs with provenance; if impossible report bounds or preregister a fresh symmetric rerun as a different panel with original attempts preserved, fixed deadline/scoring, versions, paired IDs, full cost and outcome handling; deployment release needs target population/mix evidence, sampling/cluster-aware uncertainty and prespecified margin/risk rule. No arbitrary MAR, unknown-as-zero point estimate, selective B-only retry or drop-timeout rescue.

Exploratory verdict depends on eventual reusable entry and reasoned independent quality judgment, not diagnostic numerical score. Sources Ailem §3.3 and Manski §1 support framing, binary bounds direct derivation, timeout/cost supplied policy not falsely attributed. No executable/counter/generator ran.

Pre-exposure editorial correction: the tentative '60-second outcomes ...90-second?' sentence above is not a rule. Precisely: original60-second scores remain fixed; later90-second success is not substitution evidence. Source-contract attribution erratum edda2bfd changes prior-art pointer only, not the mathematical/task model.
