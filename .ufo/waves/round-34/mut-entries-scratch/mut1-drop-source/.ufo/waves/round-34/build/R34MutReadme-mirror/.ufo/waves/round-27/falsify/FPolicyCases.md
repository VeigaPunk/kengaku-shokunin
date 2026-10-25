# FPolicyCases — KengakuR27 falsification report

Identity: KengakuR27.FPolicyCases; **not** candidate writer KengakuR27. Frozen clone base observed: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` at `/tmp/kengaku-r27-FPolicyCases`. Scope: the E0–E8 synthetic hand-expected fixtures and their test/mutant behavior.

## Findings by severity

None. No actionable defect found in this assigned fixture scope.

## Evidence

- Diff against registered base `b5719440e5eee46c1886fddbdf7bdc1624829454`: `plans/policy_cases.py` is newly added (84 lines); `git cat-file -e b5719440:plans/policy_cases.py` returned 128 (absent at base). The policy instrument and independent oracle are also new at this revision.
- `plans/policy_cases.py:8-84` holds 58 literal `(policy, name, raw, expected)` tuples, distributed E0–E8 as 6/6/7/6/6/6/7/6/8 (every policy covered; total exceeds 40). The expected values are literal JSON-compatible values/`None`; this file has no executable extraction logic. `plans/parser_policy_compare.py:462-473` compares each tested `POLICIES[pid]` output against those constants. I found no evidence that fixture outputs were generated from the implementation under test, so the case oracle is not circular.
- Independent synthetic cross-check: loaded those fixture literals and called the separately implemented `plans/fixtures/r27/policy_oracle.py:91-110` `extract()`; output `independent_oracle_fixture_cases=58 policies={'E0': 6, 'E1': 6, 'E2': 7, 'E3': 6, 'E4': 6, 'E5': 6, 'E6': 7, 'E7': 6, 'E8': 8} failures=0` (exit 0). The oracle does not import the comparison instrument.
- Command from the frozen clone: `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --selftest` (exit 0). Key output: `SELFTEST pass hand_cases=58 failed=[]`; `SELFTEST total policies=9 cases=58 killed=9 failures=0`. Each of the nine registered mutants was killed: E0 fallback, E1 fence order, E2 fence leakage, E3 candidate order, E4 stripping, E5 fallback leakage, E6 label recognition, E7 nesting, E8 contained-span reuse. The run also reported `pin-reject-before-policies ... policy_calls=0`.
- Edge diversity (`plans/policy_cases.py:9-83`): first/last/invalid fences and fallback/no-fallback/null; raw regex candidate ordering, arrays/nesting/malformed candidates and fence-straddling input; strict whole-output whitespace, prose/fence rejection and scalar JSON; accepted/rejected fence-label forms; decoder depth, malformed openings, quoted prose, scalar-only input, adjacent/crossing and contained spans. This is meaningfully broader than repeated happy-path objects.
- Independent population-oracle command: `PYTHONDONTWRITEBYTECODE=1 python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FPolicyCases` (exit 0); it returned the registered per-policy counts: E0 1964/0/0/0; E1 1947/17/0/0; E2 1964/0/0/0; E3 1947/17/0/0; E4 952/1012/0/1876; E5 1938/26/0/145; E6 1964/0/0/0; E7 1947/17/0/0; E8 1964/0/0/0 (agree/flip_pf/flip_fp/none). This is supporting fixed-population evidence, not a substitute for synthetic-case validation.

## Residual risk and verification gaps

The 58 tests are finite examples, not an exhaustive parser proof or an arbitrary-input safety claim; the fixture and independent oracle share the registered policy contract and regex semantics. No LSP device is mounted (`read xd://lsp` returned “No such tool”), and no LSP caller/definition/diagnostics query or grep was used. The reread was of the draft candidate, not a canonical admission: canonical path `corpus/knowledge/extraction-policy-comparison.md` was not reread; identity is not candidate writer KengakuR27. P4/Q15 are outside this fixture assignment and are not assessed here. Installs: none.

VERDICT: PASS — scoped synthetic E0–E8 fixture, independence, edge-diversity, and seeded-mutant checks.