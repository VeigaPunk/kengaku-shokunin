# FPolicyE5 — E5 scoped falsification

Identity: KengakuR27.FPolicyE5, independent reviewer; **not** candidate writer KengakuR27. Axes: novelty (find a surviving E5 defect) and calibration (bound any equivalence claim to exercised inputs).

Candidate reread: `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (full entry). The canonical `corpus/knowledge/extraction-policy-comparison.md` is absent from the frozen base clone; this is a candidate-only reread, not admission or an entry rewrite.

## Contract and implementation

Scratch clone was created from the requested lane and switched to the frozen revision; observed `git rev-parse HEAD`: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

Frozen definition: `plans/round-27-claims.md:37,42` specifies E5 as the last fenced block using E0's regex, parsed or None, without bare fallback. Amendment 1 at `plans/round-27-claims.md:164-166` explicitly says last **matched** fence only, no fallback, and warns corpus equivalence is not arbitrary-input equivalence. Instrument at `plans/parser_policy_compare.py:92-98` obtains regex matches, loads only `blocks[-1]`, and returns None on absent/invalid last match. Candidate E5 wording and its finite-population row are at draft lines 39 and 65.

## Executed evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FPolicyE5/e5_text_probe.py /tmp/kengaku-r27-FPolicyE5` — exit 0. This scratch implementation independently transcribed the frozen fence regex and last-match/JSON-load/no-fallback rule; it used the pinned population loader only. All four pinned SHA-256 values matched; population=1964; extracted-value mismatches against `e5_fence_only`=0; both implementations returned Python `None` on 145 records. This is value comparison, not merely verdict comparison.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE5 --summary` — exit 0. Output: `POLICY E5 name=fence-only n=1964 agree=1938 flip_pf=26 flip_fp=0 none=145 pass=995 ...`; `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`. Candidate draft line 65 matches the E5 counts. These are verdict/count results, not proof of general parser equivalence.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FPolicyE5` — exit 0; independent oracle output for E5: `agree=1938 flip_pf=26 flip_fp=0 none=145`, matching the instrument.
- `PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FPolicyE5 --selftest` — exit 0; `SELFTEST KILLED E5 mutant=E5-fallback-leak by=no-fence-no-fallback`; total `policies=9 cases=58 killed=9 failures=0`.

Five off-population strings were confirmed absent from the loaded raw responses; hand-derived result = independent result = instrument result in each case:

| Input edge | Hand-derived E5 value |
|---|---|
| Bare JSON only (`prose {"n": 1} more prose`) | None: no fence; no fallback. |
| Valid first fence, invalid last fence, then bare JSON | None: only the last matched fence is tried; it fails; no bare fallback. |
| CRLF-delimited JSON fence | `{"n": 2}`: frozen `\s*\n` opener matches CRLF and JSON parses. |
| Fenced JSON scalar `false` | `False`: valid parsed JSON value, not a parse failure. |
| Triple backticks inside a fenced JSON string | None: the frozen non-greedy regex terminates at the embedded delimiter, leaving invalid JSON. |

These probes expose last-matched-vs-last-parseable, no-fallback, CRLF, scalar, and regex-delimiter behavior. The result is limited to the 1964 pinned raw responses plus these five exact strings; it makes no claim of equivalence for arbitrary inputs, JSON-null-vs-absence observability, parser safety, or instruction-exactness.

Installs: none.

VERDICT: No actionable E5 defect found. The instrument's extracted values are exactly equivalent to the frozen E5 text on all 1964 pinned records and the five stated off-population probes; this scoped result does not establish general parser equivalence or admission.