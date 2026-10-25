# FxFamilyG2 — G2 deletion sensitivity audit
Axes: G2 MC applicability, transform semantics, frozen-population sensitivity, format strata and pid-composite integrity.
Scope: round 26 attempt 1, FALSIFY/advisory only; integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`. Production files untouched; no tools installed.

## Recount and oracle
Independent recount script: `/tmp/FxFamilyG2_recount.py`. It SHA-256 checked all four frozen result files directly, parsed their raw+ok rows, checked the complete population identity against exact baseline replays, independently constructed deletion objects and grade outcomes, and did not parse a summary. The grader's canonical extraction and transformation were cross-checked against those independently built objects.
Command: `python3 /tmp/FxFamilyG2_recount.py` — exit 0.
Output: `PINS=4/4 candidate_raw_ok=1964 included=1964 excluded=0`; `G2 independent n=1021 k=1021 failures=0 rate=1.000000`; `G2 skip=baseline_not_PASS:943`; `G2 payloads=dict:1000 list:21`; `G2 expected-vs-parsed-transform-mismatches=0`.
Independent oracle command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — exit 0; output: `POPULATION candidates=1964 included=1964 excluded=0`, `EXCLUDED baseline=0 missing_want=0 meta_truth=0`, `G2 kind=MC n=1021 k=1021`.
Canonical command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary` — exit 0; G2 `n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS`, composite `143/143` (`cp95_nominal=[0.974534,1.000000]`, PASS).

## Applicability, format, edge
`plans/grader_perturb.py:458-465` conditions G2 on `stored_ok is True`, a nonempty dict/list mutation, and a non-`None` `_dump_like` result. Dict deletion uses `square` for C graders when present, otherwise first key; list deletion removes index 0 (`:390-398`). The independent recount found 943 baseline FAIL rows intentionally outside the MC denominator; all 1,021 baseline PASS rows had a nonempty structured answer and a changed transform. No other applicability exclusion or transform/parser disagreement occurred. Types: 1,000 dict / 21 list.
Format strata independently recounted and matching canonical `CLASSES G2`: FJ1 `710/710`; FJM `268/268`; MULTI `17/17`; DANGLE `17/17`; BARE `9/9` (all are k/n sensitivity; no eligible stratum omitted). G2 pid-composite: `143/143`, using file+pid and C file+cell+rep as specified.
Counterexample edge (test coverage, not a corpus outcome): `plans/grader_perturb.py:609-615` gives G2 only a dict fixture, while the real list deletion is at `:396-397`. In an in-memory-only probe, patched the list branch to return an unchanged copy; `_selftest()` still reported `SELFTEST G2 PASS`, `SELFTEST_TOTAL_PASSED=11 FAILED=0`, and the broken result was `['a', 'b']`. Thus the selftest cannot detect a no-op list-deletion regression, despite the observed 21/21 list outcomes currently rejecting.

## Draft and scope check
Draft `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/drafts/grader-perturbation-audit.md:31-35,48-52,69-79` matches the observed G2 population, PASS-only MC polarity, result and descriptive-interval limitation. G2 deletions actually change the graded object in all 1,021 eligible rows. D1 is correctly stated separately as PC at `:50-52`: PASS, turn>1 ordinary state/sequence records with previous truth different from want; capture of the appended prior truth is not MP invariance or G2 correctness. The oracle also reports D1 `909/909` separately; do not fold it into G2 or robustness verdicts.
LSP status was attempted via `read xd://lsp/status`; response: `Tool 'lsp' has no doc topics.` No LSP server/device was available; source checks above use direct reads, not grep.

Finding (low, test coverage): add a list-shaped G2 selftest/assertion so an unchanged list mutant fails; no observed G2 corpus sensitivity or count defect.
VERDICT: SCOPED G2 POPULATION RESULT CONFIRMED; list-branch selftest gap remains actionable, with no observed frozen-data metric defect.