# FPolicyE0 — frozen lane extractor comparison

## Scope and axes
- Axes exercised: novelty (whether the fixed-response extractor comparison is grounded in the frozen lane policy) and calibration (value-level fidelity to that policy).
- Private clone base observed: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
- Source contract: `plans/round-27-claims.md:37` defines E0 as the last matching fenced block parsed as JSON, else the last parseable `BARE_RE` candidate; Amendment1 `:160-163` clarifies successful JSON `null` stops without fallback and the exact raw-string fallback semantics.

## Findings (severity order)
- No surviving E0 implementation mismatch found within the assigned finite scope. The independent implementation transcribed the frozen fence and bare-candidate patterns, and did not call the instrument's E0 function to derive its result. Source comparison points: `plans/parser_policy_compare.py:56-63`; canonical extractor `grader.py:121-134`; E0 baseline assertion `plans/parser_policy_compare.py:268-271`.

## Evidence
- Command (cwd `/tmp/kengaku-r27-FPolicyE0`): `python3 plans/fpolicy_e0_independent.py` — exit 0. Output: `POPULATION n=1964 candidate_count=1964 excluded=0 pin_matches=4/4`; `VALUES {'independent_vs_instrument': 0, 'independent_vs_grader': 0, 'none': 0}`. Thus every extracted JSON value (canonicalized with sorted object keys) matched both `e0_lane` and `grader.extract_json_block`, not merely its verdict. Frozen population/pin loading is in `plans/grader_perturb.py:187-256` and pin identities at `:21-35`.
- The same command checked four hand-derived off-population inputs; independent result, instrument result, and canonical grader result all matched each expected value: `valid-fence-precedes-later-bare` → `{"fenced":2}`; `bad-last-fence-then-bare-last` → `{"last":3}`; `fenced-json-null-stops-before-valid-fallback` → `null` (Python `None`); `deep-bare-nesting-selects-max-supported-regex-match` → `{"b":{"c":1}}`. All printed `ok=True`.
- Harness correction, resolved: the first run of `python3 plans/fpolicy_e0_independent.py` exited 1 because my hand expectation for the deep-nesting case was wrong; output was `EDGE deep-bare-nesting-selects-innermost-regex-match expected= {"c":1} independent= {"b":{"c":1}} instrument= {"b":{"c":1}} grader= {"b":{"c":1}} ok= False`. I corrected the expectation to the regex's last parseable supported match `{"b":{"c":1}}`; the final rerun exited 0 as recorded above.
- Command (same cwd): `python3 plans/parser_policy_compare.py --summary` — exit 0. Output lines: `POLICY E0 name=lane n=1964 agree=1964 flip_pf=0 flip_fp=0 none=0 pass=1021 pass_rate=0.5199 delta_pp=+0.00 cp95_lo=0.998124 cp95_hi=1.000000`; `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`. The latter total is verdict accounting across E1–E8, not evidence of value-level equivalence; that was established by the independent command above.

## Residual risk and verification gaps
- This is exact scoped equivalence on the four byte-pinned files and four stated probes, not proof for arbitrary response text. The deep-nesting probe demonstrates frozen `BARE_RE` can return a supported nested fragment rather than the whole outer object; this matches the defined E0 behavior, not an implementation discrepancy. `None` also represents both parsed JSON `null` and extraction miss; the output's `none` counter is literally `value is None` (`plans/parser_policy_compare.py:203`). No population record returned `None`.
- No `lsp` device is mounted in the available tool routes, so status/references/definition/diagnostics were unavailable; no grep result is presented as semantic proof. No installs.

VERDICT: Scoped PASS recommendation for E0 extracted-value fidelity on the frozen population and four hand-derived probes only; not arbitrary-input equivalence or candidate admission.
