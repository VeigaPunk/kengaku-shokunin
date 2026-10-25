# FxFamilyD1 — bounded review

## Finding — draft reporting gap [MEDIUM]

`drafts/grader-perturbation-audit.md:71,73-75` records D1 as PC and 909/909, but says its capture interval is “shown separately” without displaying it; the entry also omits D1’s format strata and file+pid composite. Amendment 1 §4 (`plans/round-26-claims.md:192-195`) requires these strata/composites; Amendment 2 §3 explicitly keeps D1’s PC rate/interval separate from scored MP/MC families (`:216-221`). Add the D1 figures or revise the “shown separately” wording. This is a presentation gap, not an instrument count disagreement.

## Independent D1 recomputation

Commands and results (all exit 0):

- `python3 /tmp/fxd1_independent.py /home/vgpnk/Projects/shokunin/kengaku-shokunin`
  ```text
  candidate_raw_ok=1964 pins_match=True state_seq_candidates=1948 baseline_mismatches=0
  eligibility=baseline_pass=1008 turn_gt_1=914 not_A_MONO=914 not_B_C=914 previous_available=914 previous_differs=909
  D1 n=909 k_capture=909 post_transform_task_pass=0 non_A_T=0
  strata=FJ1=639/639 FJM=244/244 MULTI=0/0 DANGLE=17/17 BARE=9/9
  original_matched_fence=883 no_matched_fence=26
  pid_composite=129/129 failed_units=0
  EXIT=0
  ```
  Independent logic reads the four frozen JSONL files, verifies their four pinned hashes, rebuilds truth from metadata operations, and applies the canonical grader to baseline and transformed answers; it does not import `grader_perturb.py` or the oracle.
- `python3 plans/grader_perturb.py --summary; rc=$?; printf 'EXIT=%s\n' "$rc"` (exit 0). D1 output: `FAMILY D1 kind=PC n=909 k=909 capture_rate=1.000000 cp95_nominal=[0.995950,1.000000] verdict=NOT_SCORED composite=129/129@1.000000 cp95_nominal=[0.971809,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=NOT_SCORED`; `CLASSES D1 FJ1=639/639@1.000[639/639;0/0]cp95_nominal=[0.994,1.000] FJM=244/244@1.000[244/244;0/0]cp95_nominal=[0.985,1.000] MULTI=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]`; total `population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`.
- `python3 plans/fixtures/r26/perturb_oracle.py --root .; rc=$?; printf 'EXIT=%s\n' "$rc"` (exit 0): `POPULATION candidates=1964 included=1964 excluded=0`; `D1 kind=PC n=909 k=909`.

## Interpretation / polarity edge

The code conditions in `plans/grader_perturb.py:438-449` match Amendment 1 §3 (`round-26-claims.md:188-191`): only state/sequence, baseline-PASS, turn>1, non-A-MONO/B/C, previous truth available and different from want. Recomputed counts: 1,948 state/sequence candidates; 1,008 baseline PASS; 914 turn>1; no previous truth missing; five have previous truth equal to want, leaving 909. The two baseline-PASS A-MONO and 18 baseline-PASS B records are all turn 1; the 16 remaining candidates are C/c-grader records. Every selected record is an ordinary A-/T- operation cell, so the oracle’s extra A-/T- prefix check changes no result.

Concrete polarity check: all 909 appended blocks are captured, while grading the captured previous truth against current want yields PASS for 0/909. D1 is therefore policy capture, **not** MP correctness invariance; the observed edge confirms Amendment 1’s reclassification. The D1 composite is 129/129 file+pid units, all captured; it remains NOT_SCORED, not an iid guarantee. Format counts are 639 FJ1, 244 FJM, 0 MULTI, 17 DANGLE, 9 BARE. The 26 DANGLE/BARE raws have no pre-existing matched fence, so those cases test capture of the appended block but not competition against an earlier matched block; 883 such prior-fence cases capture 883/883.

## Verification gap and residual risk

`read xd://lsp` returned `No such tool: xd://lsp` and listed the mounted devices; no LSP status, references, definition, or diagnostics were available. Findings above use direct source reads, not grep as semantic proof. No live/runtime or additional build checks were run. D1 has no MULTI cases after the registered B exclusion; do not generalize its perfect capture rate beyond this frozen population and policy.

VERDICT: D1 implementation and oracle agree on the scoped 909/909 PC result; do not treat D1 as MP robustness. Correct the draft’s missing D1 interval/stratum/composite presentation before relying on its “shown separately” statement; the 26 no-prior-fence cases remain an explicit scope limit.