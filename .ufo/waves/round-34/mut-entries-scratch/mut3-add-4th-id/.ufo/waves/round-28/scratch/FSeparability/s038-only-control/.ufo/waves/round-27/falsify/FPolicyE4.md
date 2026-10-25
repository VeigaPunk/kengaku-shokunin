# FPolicyE4 — strict-whole E4 review

Axes: novelty, calibration. Reviewer identity: `KengakuR27.FPolicyE4`; this review is **not** by candidate writer `KengakuR27`.

Entry reread: read the whole candidate draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:1-110`. The proposed canonical `corpus/knowledge/extraction-policy-comparison.md` was not present/readable at this pinned candidate snapshot; this finding concerns the draft only.

## Result

No actionable E4 defect found. The frozen definition is `json.loads(raw.strip())`, else `None` (`plans/round-27-claims.md:41`); Amendment 1 explicitly retains `raw.strip()` and limits the comparison to a policy class, not a source-exact OpenAI/evals implementation (`plans/round-27-claims.md:167-170`). The instrument implements that definition at `plans/parser_policy_compare.py:41-45,87-89`. Candidate disclosure of Python decoder behavior and the finite scope is at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:44-50,72-73`.

Independently transcribed E4 directly from the frozen text, independently SHA-256-checked the four pinned files, loaded the `raw` records (1964), and compared canonicalized returned **extracted values** with `e4_strict_whole` for every record: **1964 compared, 0 value differences**. This is stronger than verdict agreement but remains finite-population evidence, not arbitrary-input parser equivalence. The independent run also found 88 successful parses, zero successful JSON-null values, and zero extracted-value differences between stripped E4 and the disclosed source-exact `json.loads(raw)` probe on these records.

## Reproducible evidence

All commands ran against private clone `/tmp/kengaku-r27-FPolicyE4`, whose `git rev-parse HEAD` returned `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (the frozen revision). No target-tree edits or installs.

- `PYTHONDONTWRITEBYTECODE=1 python3 e4_independent_probe.py` — exit 0. Output: `POPULATION records=1964 pinned_files=4`; `E4_VALUE_COMPARISON compared=1964 differences=0`; `E4_PARSE parse_success=88 successful_json_null=0`; `STRIP_COMPARISON raw_vs_stripped_extraction_differences=0`.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE4 --summary` — exit 0; E4 output: `POLICY E4 name=strict-whole n=1964 agree=952 flip_pf=1012 flip_fp=0 none=1876 pass=9 pass_rate=0.0046 delta_pp=-51.53 cp95_lo=0.462405 cp95_hi=0.507091`; total: `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` (`plans/parser_policy_compare.py:87-89,149-153,237-258`). These are verdict metrics, not parser-equivalence evidence.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FPolicyE4` — exit 0; `POLICY E4 agree=952 flip_pf=1012 flip_fp=0 none=1876` (`plans/fixtures/r27/policy_oracle.py:66-68,166-180`). This also checks counts, not extracted values.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE4 --selftest` — exit 0; `SELFTEST pass policy=E4 probes=4 failed=[]`; `SELFTEST KILLED E4 mutant=E4-strip-omitted by=strip-form-feed`; `SELFTEST total policies=9 cases=58 killed=9 failures=0` (`plans/parser_policy_compare.py:363-366,402-406,528-547`).

## Hand-derived off-population edge cases

The independent probe and instrument agree with the hand-derived outcomes in all five cases:

- `\x0c{"x":1}\x0c` → `{"x":1}`: Python `str.strip()` removes form-feed before JSON decoding.
- `answer: {"x":1}` → `None`: the whole stripped string is not JSON; E4 does not extract the embedded object.
- `{"x":NaN}` → `{"x": nan}`: Python's default `json.loads` accepts `NaN`; this is not RFC-8259-strict parsing, as disclosed in `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:47-49`.
- `null` → returned `None` after a successful parse: the frozen return type conflates JSON null with failure; there is no fallback. No such successful-null record occurred in the pinned population.
- `{"x":1} {"y":2}` → `None`: the whole input contains trailing extra data and `json.loads` rejects it.

## Residual risk / verification gaps

No claim is made for arbitrary strings, every Python decoder failure mode, or exact equivalence to a third-party harness. In particular, the form-feed case distinguishes frozen stripped E4 from `json.loads(raw)` outside this population; Amendment 1 already records this distinction. Python's `NaN` acceptance and the `None` sentinel collision are properties of the frozen definition, not defects against it. This review did not assess P4/Q15 or admission authority.

VERDICT: **Scoped E4 PASS** — the independent `json.loads(raw.strip())` implementation and candidate instrument returned identical extracted values on all 1964 pinned records and matched five hand-derived off-population cases; finite-corpus verdict agreement is not treated as parser equivalence.

Installs: none.
