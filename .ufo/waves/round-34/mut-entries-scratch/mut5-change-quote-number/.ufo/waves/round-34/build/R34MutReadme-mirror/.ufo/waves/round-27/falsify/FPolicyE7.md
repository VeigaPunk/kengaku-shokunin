# FPolicyE7 — E7 decode-first falsification

Identity: FPolicyE7; **not** candidate writer KengakuR27. Reviewed candidate draft against canonical target `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/extraction-policy-comparison.md`; no admission or Q15 judgment is made here. Scratch clone observed at `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

## Findings (severity order)

None. No E7 defect survived this scoped attack.

## Evidence

- Frozen contract is `plans/round-27-claims.md:44,47-48`: scan left-to-right at `{`/`[`; first successful `JSONDecoder.raw_decode`; no input from `want`, `ok`, or grader. Amendment1 `:165-166` repeats the brace/bracket start rule and explicitly limits equivalence to the corpus; `:187-190` discloses the unmatched-bracket cost and research-only boundary.
- `plans/parser_policy_compare.py:37,110-117` uses a shared default decoder, tries each `{`/`[` in character order, returns the first decoded value, skips failed starts, then returns `None`. My independent `e7_text` in `/tmp/kengaku-r27-FPolicyE7/e7attack.py` was written from the frozen text and constructs a fresh default decoder per start. It used `grader_perturb.build_population` only for pinned records, not its extractor.
- `python3 e7attack.py` (from the scratch clone): `POPULATION value-compare n=1964 instrument==text==oracle mismatches=0`; canonical JSON value comparison, not verdict-only comparison. All 16 hand-derived probes were confirmed off-population (`off_population=16/16`) and passed with zero failures. Examples: `'{bad, "x": [1]}' -> [1]` (bad `{` skipped); `'"[1, 2]" trailing' -> [1, 2]` (scan starts at bracket characters); nested object returns the entire outer object; first of two objects returns the first. E7's extracted values also equal E1 and E3 on 1964/1964 here; this is finite-corpus evidence only.
- The same harness independently regraded the text-derived values: `agree=1947 flip_pf=17 flip_fp=0 none=0 pass=1004`. `python3 plans/parser_policy_compare.py --summary` exited 0 and reported `POLICY E7 name=decode-first n=1964 agree=1947 flip_pf=17 flip_fp=0 none=0 pass=1004`; total: `population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`. `python3 plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FPolicyE7` exited 0 with the same E7 counts.
- `python3 plans/parser_policy_compare.py --selftest` exited 0: E7's 4 probes passed, and `E7-nesting-limited` was killed by `deep-nesting-outermost`; total `policies=9 cases=58 killed=9 failures=0`.
- Pin preflight also behaved as Amendment1 states: on a clone-local `pinrej` copy with one appended byte in the round8 response file, `python3 plans/parser_policy_compare.py --root pinrej --summary` exited 1, reported the changed SHA-256, and emitted 0 `POLICY` lines. `plans/parser_policy_compare.py:242-255` returns on population errors before entering the policy loop.

## Residual risk and verification gaps

- This establishes value equivalence only for the 1964 pinned records and the 16 named off-population examples; it does not establish arbitrary-input equivalence or production parser safety. A 20,000-unmatched-`[` probe returned `None` in 4.41s; the disclosed 200K probe was not rerun. Balanced nesting of 20,000 was accepted by the default decoder; this is not a general depth guarantee.
- LSP was unavailable: `read xd://lsp` returned “No such tool” and listed only REA devices. Source line references above come from direct file reads; runtime comparisons are the behavioral evidence. No build/lint was run.

VERDICT: SCOPED PASS — E7 matches the frozen decode-first policy by extracted value across the pinned population and all 16 hand-derived off-population cases; no actionable E7 defect found. No claim beyond this scope.

Installs: none.
