# FMatrix — fixed-response matrix falsification

Identity: FMatrix reviewer; **not** candidate writer KengakuR27. I read the full draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`, proposed canonical path `corpus/knowledge/extraction-policy-comparison.md`; the draft remains the reviewed object, not an admission. Observed scratch clone base: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

## Findings

No actionable defect in the assigned matrix / event-count scope. Candidate claims at draft lines 55–72 match the pinned replay below.

## Evidence

- On the frozen clone, `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --summary` exited 0; final line: `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`. Its emitted matrix, in E0…E8 order, was:

  | |E0|E1|E2|E3|E4|E5|E6|E7|E8|
  |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
  |E0|0|17|0|17|1012|26|0|17|0|
  |E1|17|0|17|0|995|43|17|0|17|
  |E2|0|17|0|17|1012|26|0|17|0|
  |E3|17|0|17|0|995|43|17|0|17|
  |E4|1012|995|1012|995|0|1004|1012|995|1012|
  |E5|26|43|26|43|1004|0|26|43|26|
  |E6|0|17|0|17|1012|26|0|17|0|
  |E7|17|0|17|0|995|43|17|0|17|
  |E8|0|17|0|17|1012|26|0|17|0|

- Independently re-expressed E0–E8 from the frozen policy table / Amendment 1; used the pinned population loader and the unchanged grader dispatch, not `parser_policy_compare` policy functions. `PYTHONDONTWRITEBYTECODE=1 python3 fmatrix_rebuild.py` exited 0 (population 1964, pins match, exclusions 0, stored PASS 1021). A compare of its matrix to every emitted instrument cell returned `matrix_mismatches=[]`, `COMPARE_EXIT=0`; symmetry `true`, zero diagonal `true`. Relevant claim: draft lines 35–51, 55–72.
- Independent vectors: E1 = E3 = E7 exactly. All 17 E1-vs-E0 changes are PASS→FAIL, MULTI rows in `corpus/evidence/round8-horizon/results.jsonl`: lines 223–232, 234, 236, 239, 244–245, 247–248. Each has E0=true / E1=false. MULTI agreement is 14/31 for each of E1/E3/E7 (draft line 76).
- Rebuilt per-policy counts agree with draft lines 61–69 and oracle output: E0/E2/E6/E8 each agree 1964, flips 0, none 0, PASS 1021; E1/E3/E7 each agree 1947, PF 17, FP 0, none 0, PASS 1004; E4 952, PF 1012, FP 0, none 1876, PASS 9; E5 1938, PF 26, FP 0, none 145, PASS 995. `PYTHONDONTWRITEBYTECODE=1 python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FMatrix` exited 0 with matching agree/PF/FP/none counts.
- The 1089 is the sum of alternative-vs-E0 policy/response disagreement events: `17+17+1012+26+17`. The union is **1021 distinct response records**, not 1089: E1∩E4=17, E4∩E5=17, and E5 contributes 9 records outside E4; `1089−1021=68` repeat events. Thus draft line 72 correctly labels events as non-unique responses; the independently computed distinct count adds precision, not a contradiction.

## Residual risk and verification gaps

This is finite-population evidence only. Parser policies were independently re-expressed, while frozen loading/grading reused `grader_perturb`'s pinned loader and grader dispatch; the independent oracle also matched. P4 assertions and Q15 authority were outside this seat's enumerated matrix checks and are not adjudicated here. No tool was installed or updated.

VERDICT: **PASS — scoped to the pinned fixed-response matrix, E1/E3/E7 row identity, 17-row set, and 1089-event vs 1021-distinct-response count.**