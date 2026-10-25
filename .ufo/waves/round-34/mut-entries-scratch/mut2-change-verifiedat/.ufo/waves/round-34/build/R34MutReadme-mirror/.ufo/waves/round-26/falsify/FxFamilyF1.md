# FxFamilyF1 — scoped falsification report

Scope: F1 only, round 26 attempt 1. Integrated revision `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`, base `f11bffbf`; revision record is `.ufo/waves/round-26/integration-revision.txt`.

LSP status unavailable: `read xd://lsp` returned “No such tool” and the mounted-device inventory had no LSP device. Therefore no LSP status/references/definition/diagnostics were available; code reads below are not presented as semantic-LSP proof.

## Frozen population and commands

`sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/{round8-horizon/results.jsonl,round9-replication/results-r9.jsonl,round11-power/results-r11.jsonl,round12-ladder/results-r12.jsonl}` was run with explicit absolute paths, exit 0. Observed hashes match the instrument pins: `bd986e5e…e2204`, `c20158be…affbcb`, `918bf7aa…8f51ad`, `ad9c88e7…b842f1` (full values in command output).

- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary` — exit 0. F1: `n=1819 k=1802`, rate `.990654`, nominal CP95 `[.985079,.994547]`, pooled verdict PASS; 1964 candidates, 0 excluded.
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — exit 0; independently reports 1964/1964, 0 excluded, F1 `n=1819 k=1802`.
- `python3 /tmp/fx_family_f1_recompute.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — exit 0; oracle-path recomputation: F1 `1819/1802`, 17 PASS→FAIL; FJ1 `1296/1296`, FJM `492/492`, MULTI `31/14`, DANGLE `0/0`, BARE `0/0`; file+pid composite (C=file+cell+rep) `187/194`, 7 failing units. All 31 MULTI records are round-8 B cells with operation-8/9/10 labels.
- `python3 /tmp/fx_family_f1_oracle_edge.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — exit 0; frozen per-record core/oracle applicability+transform differences `0/1964`; synthetic invalid-last-fence probe differs (below).

The zero F1 applications outside the 1819 matched-fence strata are exactly the summary's 57 DANGLE + 88 BARE records. In the pinned raws, every matched-fence record has a parseable final block and an actual transform. Core applicability is `_answer_fence` selecting `blocks[-1]` and requiring `json.loads` (`plans/grader_perturb.py:279-289`); F1 replaces only that match with its body (`:401-408`). A full population replay yielded 1964 candidates, 0 excluded, so no unsupported-grader, malformed-raw/ok, missing/mismatched truth, or baseline-replay exclusion changed these rates.

## Findings (severity ordered)

**Low — independent-oracle F1 precondition is broader than Amendment 1/core.** `plans/fixtures/r26/perturb_oracle.py:279-285` strips `blocks[-1]` without checking that its body parses as JSON; core F1 declines when the final matched block is invalid (`plans/grader_perturb.py:279-289`). Probe `raw='```json\\n{"x":1}\\n```\\n```json\\nnot-json\\n```'`: core says non-applicable; oracle transforms it to leave `not-json` unfenced. No pinned record exercises this edge (0/1964 differential), so current n/k are unaffected, but the oracle does not independently encode the exact “answer fence” precondition. Align the guard or add an explicit fixture before treating oracle agreement as semantic parity beyond this finite corpus.

**Observed F1 counterexample (accurately disclosed, not an undisclosed draft defect).** `corpus/evidence/round8-horizon/results.jsonl:223` is `B-clean-plain`, pid 1, stored PASS. Its operation-8/9/10 JSON blocks end with operation 10 as the answer; stripping only that final fence leaves operation 9 as the last matched fence, which `grader.py:121-134` then parses. The extracted state loses `gaskets: 4`, turning the PASS into FAIL. MULTI is `14/31`; all 17 baseline-PASS records there flip (`0/17` invariant). The other F1 strata are invariant on these raws. The pooled PASS and file+pid composite INDETERMINATE (`187/194`, CP95 `[.927072,.985372]`) must not erase this failure stratum.

D1 cross-check: `grader_perturb.py:438-449,490-496` gates previous-truth appending on PASS, turn>1, state/seq, excludes A-MONO/B/C, and measures extraction of previous truth as PC capture, not MP correctness invariance. The frozen `state/seq` mapping at `:168-184` yields ordinary A-/T-operation rows only; core and oracle both report D1 `PC 909/909`. Draft `:50-52` states this distinction correctly.

Draft review: `.ufo/waves/round-26/drafts/grader-perturbation-audit.md:39-52,60-85,91-100` reports the F1 transform, pooled/stratified/composite values, multi-block cause, nominal-interval limitation, and D1 PC interpretation consistently with the observed output. No F1 number or stated scope discrepancy found.

Residual risk / verification gap: CP95 remains nominal/descriptive for this fixed, correlated corpus; F1’s robust result is limited to observed formats. LSP was unavailable as above. No live model/endpoint traffic or out-of-scope checks were performed.

VERDICT: Pinned F1 result and disclosed MULTI counterexample are supported; the draft is accurate on F1/D1. Keep the low oracle-precondition mismatch visible as a narrow parity gap; it does not alter the current frozen-population F1 counts.