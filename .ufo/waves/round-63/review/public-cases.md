# Independent manual challenge — Kengaku63
Reviewer: /root/judge_kengaku_round63. Author must not read before contract/source freeze.
All calculations are manual; no R/Python/source/counter/fixture execution authorized.
For C1–C6, use alpha=q=1/20, complete fixed family m, valid marginal p-values; assume independent hypotheses except C5. Report Holm, BH, BY adjusted p vectors in ORIGINAL label order and rejection sets (<= threshold), explaining decisive rank/cumulative operations. Exact rationals preferred; decimals absolute tolerance 1e-8. Interpret adjustment as error-rate control, not truth of each hypothesis. C1–C6 each one case, all requested cells needed. C7–C10 each one interpretation case, all claims addressed. No score/axis/cap increase derives from this challenge alone.

C1. Labels A,B,C: p=(1/100,1/25,41/1000). Explain why unmonotonized rank products are not adjusted p-values.
C2. Labels A,B,C: p=(3/100,1/25,49/1000). Can BH stop when rank1 fails its local threshold? Compare Holm stopping.
C3. Labels A,B,C,D: p=(1/25,1/1000,1/25,1/5). Preserve ties and restore input order.
C4. Labels A,B,C,D: p=(1/80,1/40,3/80,1/20). Explain equality at the rejection boundary; do not round before comparing.
C5. Labels A,B,C: p=(1/200,1/50,1/25). Tests share tasks and dependence is arbitrary/unknown; valid marginal p-values stipulated. Calculate all three outputs but distinguish which control guarantees are licensed under this assumption.
C6. Five candidates A,B,C,D,E form the prespecified family: p=(3/250,1/5,3/10,2/5,1/2). Analyst retains only best A and applies m=1. Compare full-family arithmetic against singleton arithmetic and decide if selection licenses the latter.
C7. A procedure controls FDR at .05 and rejects four hypotheses. Analyst says (i) probability ANY false rejection is <=.05 and (ii) <=5% of these four must be false. Define V,R,FDR,FWER including R=0 and assess both assertions.
C8. A valid difference test has adjusted p=.30 and a confidence interval [-.20,.30] for model improvement. Practical-equivalence margin is [-.05,.05]. Analyst says models are equivalent and there is no meaningful improvement. What is justified; what further design/evidence is needed?
C9. Analyst has 100 repeated generations on each of five tasks for each model, treats all generations as independent despite task clustering, constructs p-values, then applies BY. Does BY fix validity of those tests or license generalization to all tasks? State unit, estimand, validity prerequisites and correction's limited role.
C10. Fixed family has six hypotheses; three were chosen after inspecting results and their p-values alone reported. Is declaring these three a new confirmatory family sufficient? Can unseen adjusted p-values/rejection sets be reconstructed from only selected values when full vector is unavailable? State a defensible reporting path, limits, and what genuine prospective confirmation would require.
