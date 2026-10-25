# Round 27 — no-harm critic (build)

Review only; no edits to the lane, no checks executed, no installs. I treat the seven scored dimensions as novelty plus the six formal axes: depth, coverage, operability, freshness, calibration, adjacency (SCORECARD.md:8-20; AXES.md:7-16).

## Counterexamples / corrections

1. **New README rows can disappear without making v4 fail.** The base `state_check.py` deliberately freezes `README_INDEX_PATHS`; new rows/files are emitted as `OUT_OF_POPULATION`, not `MISMATCH` (plans/state_check.py:65-68, 1216-1255; OUT_OF_POPULATION does not fail the CLI at 1823-1838, 2546-2549). Thus a missing `knowledge/extraction-policy-comparison.md` index row can coexist with a passing P2/P3 projection; P4b only checks the frozen round-26 supporting-artifact table (round-27-claims.md:111-119). The round-26 census already has a bidirectional knowledge-file/index check (plans/round26_census.sh:111-147), but it does not verify the new coverage-map claim.
   - **Axes:** coverage, depth, operability; indirectly freshness (undiscoverable/stale entry).
   - **Smallest safe correction:** retain frozen P2/P3; require the round-27 census to report exact bidirectional knowledge index parity *and* an explicit coverage-map row for the new entry. Do not treat `state_check --summary` or census exit 0 alone as that proof.
   - **Availability:** the declared `plans/round27_census.sh` was not present in the observed lane tree (`read` of the absolute path returned “not found”); do not report this check as passed until it lands. The existing round-26 census only covers knowledge index parity, not the new coverage-map row.
   - **Check:** from lane root, `sh plans/round27_census.sh`; require `knowledge_readme_parity=match` and the new coverage-map row result to be `match`. Also run `python3 plans/state_check.py --summary` for frozen assertions.

2. **E0 replay is not proof that the graders stayed fixed.** C1's 1964-record baseline catches changed outcomes in the frozen sample, not a grader edit affecting an unobserved input. A `grade_state` branch changed only for a value absent from these records can leave all E0 verdicts identical while violating “graders unchanged” (round-27-claims.md:29-31, 56-57; grader_perturb.py:187-256, 259-276). This would confound the extractor-only comparison and its novelty/calibration interpretation.
   - **Axes:** novelty, calibration, depth, operability.
   - **Smallest safe correction:** leave `grader.py` and the existing `grader_perturb.py` replay path untouched; pin their source to the frozen base, rather than infer immutability from E0 agreement.
   - **Checks:** `git diff --exit-code b5719440 -- grader.py plans/grader_perturb.py`; then `python3 plans/parser_policy_compare.py --summary`, `python3 plans/parser_policy_compare.py --selftest`, and `python3 plans/fixtures/r27/policy_oracle.py --root .` (the latter two must detect each policy mutant and agree on all E0-E8 counts).

3. **P4e could pass a false citation audit.** The SOURCES validator's E11 verifies that `used-by` paths exist; it does not verify those files cite the row ID (scripts/sources-census.sh:538-570, 669-674). A P4e implementation searching the registry itself, or matching `S043` as a substring of another token, could claim citation coverage when the named document has no citation.
   - **Axes:** depth, freshness, operability, calibration.
   - **Smallest safe correction:** restrict P4e to each S043-S048 row's declared `used-by` files and require a delimited exact ID token there; add per-ID removal mutants that assert the corresponding `P4e.*` assertion turns red. Do not count SOURCES.md as a cited target.
   - **Checks:** `python3 plans/state_check.py --selftest` (each P4 class must fail on its own mutant), plus `sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (exit 0; the two pre-existing W04 warnings are not new failures).

4. **P4 growth / SCORECARD edits can silently broaden or rewrite the frozen population.** P2/P3 are explicitly frozen; P4 is only the base-enumerated round-26 population (round-27-claims.md:102-137). Appending R27 rows is safe; editing/reflowing historic rows or letting P4a scan the new round creates drift or self-reference. The scorecard says novelty maps to the lane-defined proxy, and pre-registration holds novelty at 7 absent a successful prior-art result (SCORECARD.md:8-20; round-27-claims.md:73-83).
   - **Axes:** calibration, operability, depth; novelty if the C1 measurement is promoted to method novelty; freshness if old claims are rewritten.
   - **Smallest safe correction:** append only; P4a must remain bound to the exact base P4a lines/tokens and named receipts, never all of SCORECARD. Report CP95 as descriptive for this finite population, not a future-response guarantee (round-27-claims.md:50-57).
   - **Checks:** `python3 plans/state_check.py --summary` and `python3 plans/state_check.py --selftest`; compare P2/P3 keyed JSON at base v3 vs v4:
     `tmp=$(mktemp -d); mkdir "$tmp/base"; git archive b5719440 | tar -x -C "$tmp/base"; python3 "$tmp/base/plans/state_check.py" --root "$tmp/base" --json > "$tmp/v3.json"; python3 plans/state_check.py --root "$tmp/base" --json > "$tmp/v4.json"; python3 -c 'import json,sys; a,b=(json.load(open(p)) for p in sys.argv[1:]); f=lambda d:[x for x in d["assertions"] if x["id"].startswith(("P2","P3"))]; assert f(a)==f(b)' "$tmp/v3.json" "$tmp/v4.json"`

## Seven-axis no-harm boundary

- **Novelty:** keep the score held unless the registered prior-art condition is met; xFinder and common harness filters are already named prior art (round-27-claims.md:73-79). No method-novelty inference from a new instrument alone.
- **Coverage:** C1 remains exactly four pinned files / 1964 responses / 0 excluded; no claim about future responses or general harness quality (round-27-claims.md:29-31, 50-57).
- **Calibration:** preserve frozen P2/P3 keyed results; P4 claims only its enumerated base population. Require P4a-P4e target-specific red mutations, not merely any nonzero selftest failure.
- **Operability:** preserve state_check's CLI/exit map; keep all checks offline/stdlib-only and do not alter the existing grader replay. Run the commands above plus both independent C1 selftests/oracle.
- **Freshness:** add SOURCES rows only for sources actually opened this round, with exact quote/location and recheck; path existence is not citation or source verification (QUALITY.md:15-39, 97-119). Validate the 13-column registry and actual used-by paths with the census command above.
- **Adjacency:** keep this claim about answer-extraction policies separate from model-side response-format invariance; cite each harness's own documented semantics, and do not imply those docs establish cross-policy verdict accuracy.
- **Depth:** retain E0-E8 exact semantics, per-format/per-cell results, and the independent oracle; keep every P4 token linked to its named receipt/command. Do not compress counts in the new SCORECARD section into an unauditable headline.

Installs: none.
VERDICT: Fixable no-harm risks identified; the README parity gap and finite-sample grader-provenance gap need explicit guards before the claims are safe.