# FPolicyE6 — independent E6 value check

Identity: **FPolicyE6; not candidate writer KengakuR27.** The proposed canonical entry `corpus/knowledge/extraction-policy-comparison.md` is absent at the pinned base; I read the whole draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including its full source line) before this scoped check. This is not an admission review.

## Scope and method

Observed clone base: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
Frozen E6 is claims line 43 plus Amendment 1 lines 164–166; implementation is `plans/parser_policy_compare.py:36,101-108`. The frozen bare fallback pattern is `plans/grader_perturb.py:35-36`; its pinned loader and population checks are `plans/grader_perturb.py:187-256`. The candidate describes E6 and its CommonMark limit at lines 40, 44–47, and 72–73.

I independently compiled the literal frozen any-label regex and bare regex, decoded the last matched fence then used the raw bare-last fallback only on decode failure, and compared type-tagged canonical JSON values—not verdicts—to the instrument's E6 result for every record returned by `build_population`. I also compared independent E6 values to E0 and used six off-population cases with hand-derived outputs.

## Evidence

Command `python3 plans/parser_policy_compare.py --summary` (exit 0), exact relevant output:

```text
POLICY E6 name=any-label-fence n=1964 agree=1964 flip_pf=0 flip_fp=0 none=0 pass=1021 pass_rate=0.5199 delta_pp=+0.00 cp95_lo=0.998124 cp95_hi=1.000000
TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5
EXIT=0
```

Command `python3 /tmp/kengaku-r27-FPolicyE6/e6_value_check.py --root /tmp/kengaku-r27-FPolicyE6; printf 'EXIT=%s\\n' "$?"` (exit 0), exact output:

```text
POPULATION records=1964 candidates=1964 excluded=0 pin_matches=4/4 errors=0
VALUES independent_vs_instrument_E6 exact=1964/1964 mismatches=0
VALUES independent_E6_vs_E0 equal=1964/1964 changed=0
EDGE permitted language object: expected=('dict', '{"x":1}') independent=('dict', '{"x":1}') instrument=('dict', '{"x":1}') E0=('dict', '{"x":1}') pass=True
EDGE permitted language scalar distinguishes E6 from lane: expected=('str', '"scalar"') independent=('str', '"scalar"') instrument=('str', '"scalar"') E0=('NoneType', 'null') pass=True
EDGE valid extended info string is outside the frozen label regex: expected=('NoneType', 'null') independent=('NoneType', 'null') instrument=('NoneType', 'null') E0=('NoneType', 'null') pass=True
EDGE successful fenced null ends extraction before bare fallback: expected=('NoneType', 'null') independent=('NoneType', 'null') instrument=('NoneType', 'null') E0=('dict', '{"fallback":true}') pass=True
EDGE invalid last matched fence falls back to last parseable bare candidate: expected=('dict', '{"earlier":1}') independent=('dict', '{"earlier":1}') instrument=('dict', '{"earlier":1}') E0=('dict', '{"earlier":1}') pass=True
EDGE CRLF after permitted label: expected=('list', '[1,2]') independent=('list', '[1,2]') instrument=('list', '[1,2]') E0=('list', '[1,2]') pass=True
EXIT=0
```

## Verdict, residual risk, verification gaps

**No actionable E6 implementation defect found in this scope.** Independent E6 returned the same extracted value as the instrument on all 1964 pinned records, with all four input pins matching and no exclusions; on these records E6's extracted values also matched E0. This finite equality is not arbitrary-input parser equivalence: off-population `python`-fenced scalar text yields `"scalar"` under E6 but `None` under E0, while a successful fenced `null` suppresses E6's bare fallback. The frozen regex is not CommonMark-complete, as disclosed.

`xd://lsp` is unavailable in the mounted tools (`No such tool`); no LSP status, references, definition, or diagnostics were obtainable. Literal search was only used to locate definitions, not as semantic proof. The parser's `--selftest` and non-E6 policies were not part of this scoped run. No tools were installed or updated.
