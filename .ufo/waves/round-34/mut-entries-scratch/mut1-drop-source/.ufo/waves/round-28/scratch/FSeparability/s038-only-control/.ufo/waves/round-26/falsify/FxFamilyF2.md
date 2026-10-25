# FxFamilyF2 — round 26, attempt 1

Axes: F2 contract fidelity; pinned-raw result correctness/coverage; novelty attribution. Scope is only `plans/grader_perturb.py` F2 and its oracle comparison. No production files changed; base diff showed the instrument, oracle, and draft as new files. No tools installed.

## Finding — LOW: F2 applicability is narrower than Amendment 1; oracle also diverges at an invalid-block edge

`grader.py:122` recognizes whitespace after a `json` fence label with `\s*`. `plans/grader_perturb.py:414` instead accepts only ASCII space/tab and optional CR before LF. A last parseable answer fence accepted by the grader can therefore be excluded from F2 without an Amendment-1 exclusion. In an isolated probe, ` ```json` + vertical-tab + LF + `{"x":1}` + closing fence had one extractor match and extracted `{'x': 1}`; the instrument returned not-applicable while the oracle transformed it (`/tmp/kengaku-f2-oracle-edge.py`, exit 0). This separator is not present in the frozen population, so it does not change the reported finite-population count.

The oracle has the opposite edge: `perturb_oracle.py:286-292` checks only that the last match starts with ` ```json`, not that its body parses. For ` ```json\nnot-json\n````, the instrument returned not-applicable but the oracle returned a transformed raw string; extractor result remained `None` (same probe). Thus current count agreement does not establish exact F2 applicability agreement beyond the pinned raws. Align the instrument with extractor-matched openers while retaining parseability, and make the oracle enforce parseability before counting.

## Frozen-raw recomputation and evidence

Independent script `/tmp/kengaku-f2-independent.py` reads the four pinned JSONL files directly, verifies hashes, derives truth from metadata via `grader.py`, replays baselines, and computes the F2 mutation without importing either audit instrument or oracle. Command (repo cwd): `python3 /tmp/kengaku-f2-independent.py` — exit 0. Output: all four `PIN ... match=True`; `INDEPENDENT_POP candidates=1964 included=1964 excluded=0 baseline_bad=0 want_mismatch=0 missing_meta_or_want=0 pins_ok=True`; `F2_ELIGIBILITY no matched fence=145`; `F2_INDEPENDENT n=1819 k=1802 flips_PASS_to_FAIL=17 flips_FAIL_to_PASS=0`.

Independent F2 strata: FJ1 `1296/1296` (710 PASS, 586 FAIL); FJM `492/492` (268 PASS, 224 FAIL); MULTI `31/14` (17 PASS→FAIL, 14 FAIL preserved); DANGLE `0/0`; BARE `0/0`. PID composite is `187/194` (7 failing units). The target summary reports its nominal descriptive CP95 as `[0.927072,0.985372]`, INDETERMINATE; pooled F2 is `1802/1819`, nominal CP95 `[0.985079,0.994547]`, PASS. These are not iid/future-response guarantees.

Concrete raw counterexample: `corpus/evidence/round8-horizon/results.jsonl:223`, B-clean-plain, pid 1, `ok=true`. Its three fenced answers are operations 8, 9, 10; after changing only the final `json` label, the case-sensitive extractor falls back to operation 9, whose object lacks `gaskets`, and the verdict flips to FAIL. This supports the observed MULTI `14/31` and `0/17` among baseline-PASS records; it is not a new method/novelty result.

Commands and observed F2 agreement: `python3 plans/grader_perturb.py --summary` — exit 0, `FAMILY F2 kind=MP n=1819 k=1802 ... composite=194/187 ... composite_verdict=INDETERMINATE`; `CLASSES F2 ... FJ1=1296/1296 ... FJM=492/492 ... MULTI=31/14 ...`; `FORMATS FJ1=1296 FJM=492 MULTI=31 DANGLE=57 BARE=88`; `TOTAL population=1964 excluded=0 ...`. `python3 plans/fixtures/r26/perturb_oracle.py --root .` — exit 0, `POPULATION candidates=1964 included=1964 excluded=0`, exclusions all zero, `F2 kind=MP n=1819 k=1802`.

## Draft review, residual risk, gaps

Draft `grader-perturbation-audit.md:39-41,62-63,87-91` accurately describes the registered last-fence change, 17 flips, and MULTI counterexample. Its statement that F2's pooled PASS does not erase the bad stratum is supported. The novelty discussion at lines 17-21 correctly treats this as a lane-specific instantiation, not a new method; holding novelty at 7 is consistent. Amend the F2 eligibility/oracle edge before relying on these implementations for cases outside the frozen bytes; current frozen n/k remain reproduced independently.

Residual risk: this is a deterministic audit of the byte-pinned population only. LSP was unavailable (`read xd://lsp` returned “No such tool”; static source reading used as fallback). No selftest/build was run; F2 selftest coverage was inspected at `plans/grader_perturb.py:567-645`. No admission or judgment is made.

VERDICT: F2’s pinned result is independently confirmed, with the intended MULTI counterexample; LOW-severity F2 applicability/oracle mismatch remains outside the frozen population and should be corrected or explicitly bounded before admission.