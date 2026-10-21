# FPolicyE1 — E1 first-fence falsification

Seat: `KengakuR27.FPolicyE1`. Scratch clone observed at `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

## Findings (severity order)

None. No actionable E1 defect found in the assigned scope.

## Scoped evidence

Frozen semantics are Amendment 1: try the first **matched** fence only; a decode failure immediately falls back to bare-last over the whole response; a successfully decoded JSON `null` returns `None` without fallback (`plans/round-27-claims.md:155-166`). The implementation selects `blocks[0]`, returns when `_loads` succeeds, and otherwise calls `_bare_last(raw)` (`plans/parser_policy_compare.py:48-72`). Its fence and bare patterns are the frozen patterns (`plans/grader_perturb.py:36-37`). Hand cases independently pin the failed-first/no-retry and null behaviors (`plans/policy_cases.py:17-23`).

Independent value comparison, implemented from the frozen text and run against `grader_perturb.build_population` on the pinned clone:

- Command: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FPolicyE1/independent_e1_check.py /tmp/kengaku-r27-FPolicyE1`
- Exit: `0`; 1964 candidates, 1964 population, 0 excluded, all four pins match.
- Instrument E1 vs independent E1: **0 extracted-value mismatches / 1964** (canonical JSON-value comparison).
- Independent E1 vs stored verdicts: 1947 agree, 17 PASS→FAIL, 0 FAIL→PASS; 1004 PASS and 0 extracted `None`.
- E1 vs E0: 31 records have different extracted values; **14 of those still have the same verdict**. Thus the observed verdict agreement is not parser/value equivalence. Example equal-verdict differences are the `B-corrupt-plain` records at `round8-horizon/results.jsonl:221,233` and `B-corrupt-hint` at line 222; each displayed E0/E1 pair grades FAIL under both.

Four hand-derived off-population cases returned the expected value in both the independent implementation and the instrument: (1) valid first JSON fence plus trailing bare object → first-fence object; (2) first fence containing JSON `null` plus trailing bare object → `None`, with no fallback; (3) malformed first fence, valid second fence, then a bare object → trailing bare object, since the second fence is not retried and raw bare-last sees both objects; (4) uppercase `JSON` fence label plus a bare object → bare object, because the frozen lane regex does not match uppercase `JSON`.

Instrument check:

- Command: `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE1 --summary`
- Exit: `0`; exact E1 line: `POLICY E1 name=first-fence n=1964 agree=1947 flip_pf=17 flip_fp=0 none=0 pass=1004 pass_rate=0.5112 delta_pp=-0.87 cp95_lo=0.986177 cp95_hi=0.994950`; total: `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`.

- Command: `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE1 --selftest`
- Exit: `0`; E1 probe passed and seeded E1 last-fence mutant was killed; `hand_cases=58 failed=[]`; all 9 seeded mutants killed.

I read the complete candidate draft at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` for the proposed canonical `corpus/knowledge/extraction-policy-comparison.md` entry reread. Reviewer identity is `KengakuR27.FPolicyE1`, **not** candidate writer `KengakuR27`. The draft’s E1 summary and finite-corpus counts match this scoped evidence (`:30-50`, `:58-76`).

## Residual risk and verification gaps

This establishes scoped equivalence only for E1 on the pinned population and these four explicit fixtures; it makes no equivalence, performance, or safety claim for arbitrary inputs. LSP was unavailable: `read xd://lsp` returned “No such tool” and the mounted-device list did not include an LSP device. No semantic caller/definition/diagnostics checks were made, and no grep result is used as semantic proof. This report does not review E2–E8, P4, or Q15.

VERDICT: PASS — E1 matches Amendment 1 on the 1964 pinned records and four hand-derived off-population cases; no surviving E1 defect.

Installs: none.
