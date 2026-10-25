writer: KengakuR29-2.FTokenGitlab-2

# FTokenGitlab — attack on the `__GITLAB__` census

Target: the integrated round-29 projection instrument (lane master
`56fd949a6478342531e61f4feecb4a685d831640`) and its stdout, not the source.
Items attacked: `ORIGINAL_OCCURRENCES_BY_TOKEN`, `TASKS_WITH_TOKEN`, and the per-profile
`applied_replacements` / `changed_leaves_by_token` / `changed_tasks_by_token` rows for
`__GITLAB__`, plus substring overlap against the other five tokens.

## Independence

I did **not** read or import `plans/config_projection.py` source. I executed it read-only
(`--summary`, `--json`, `--selftest`) and consumed stdout only. All production numbers below
were compared against a separately written oracle:
`.ufo/waves/round-29/scratch/falsify/FTokenGitlab/census.py`
(sha256 `e3d67a3b753cc5a61308737c0ca8eefea2cc136c1b1c328d452ade5e659d125b`), output
`census.json` (sha256 `627d2e6173b42a1115f2b3da1c92d6891c6e933b34509391b5fcbd4d8a8ebbee`).
The oracle read only: the prereg TEXT `plans/round-29-claims.md`, generator bytes
`plans/fixtures/r29/generate_test_data.py`, `manifest.json`, `profiles.json`, the raw task
file, and the instrument's stdout JSON. Oracle exit 0.

Authenticated inputs (my `sha256sum`, matching manifest):
`generate_test_data.py` `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`;
`profiles.json` `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`;
`manifest.json` `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`;
raw `test.raw.json` `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`.
Raw is 880776 bytes/chars, pure ASCII, no CR.

## Attack method

1. **Two parses.** Decoded task objects with `json.loads`, and independently recovered the
   exact raw-text span of each of the 812 array elements with `json.JSONDecoder.raw_decode`
   scanning from the open bracket.
2. **Raw census, two counting semantics.** `str.count` (non-overlap) and lookahead-regex
   (overlap) per token; third method
   `grep -o '__GITLAB__' plans/fixtures/r28/webarena/config_files/test.raw.json | wc -l`.
3. **Decoded-leaf walk.** JSON-pointer walk of every string value in every task; counted
   occurrences, leaves, and tasks per token; checked keys separately.
4. **Structural exclusion.** Stripped all JSON string literals with
   `"(?:[^"\\]|\\.)*"` and recounted tokens in the remaining structural text.
5. **Provenance set check.** Compared the 385 `occurrence_provenance` GITLAB records' offsets,
   task indices and JSON pointers against the independently enumerated offsets and the raw
   element spans; recomputed each record's `path_template` from its pointer.
6. **Per-profile simulation.** Re-implemented the pinned generator's six ordered
   `str.replace` steps over raw text for each profile, parsed the result, and recomputed
   applied counts, changed leaves/tasks by token, projected-text digests, and per-task objects.
7. **Substring lattice.** All 30 ordered pairs of the six tokens under `in`; token-in-other-
   token-occurrence counts; self-overlap adjacency; bare stems.
8. **Whole-object fidelity.** Deep-equality of all 812×3 projected task objects and all 2436
   `would_be_file_sha256` values (`json.dumps(item, indent=2)` of the independently parsed
   projected task), plus per-task `changed_leaves` (pointer/original/projected/tokens).

## GITLAB result vs instrument

| metric | instrument stdout | independent | match |
|---|---|---|---|
| `ORIGINAL_OCCURRENCES_BY_TOKEN.__GITLAB__` | 385 (summary line 9) | 385 raw `str.count`; 385 overlap-regex; 385 `grep -o \| wc -l`; 385 decoded leaves; 385 provenance records | yes |
| `TASKS_WITH_TOKEN.__GITLAB__` | 204 (line 10) | 204 decoded tasks; per-task raw-span counts identical to decoded counts for every token | yes |
| `PROFILE *.applied_replacements.GITLAB` | 385 in all 3 profiles (lines 16, 27, 38) | 385 at step 1 in all 3 simulations | yes |
| `PROFILE *.changed_leaves_by_token.__GITLAB__` | 385 in all 3 (lines 20, 31, 42) | 385 leaves in all 3; per-task changed-leaf lists identical (0 mismatches over 2436 tasks) | yes |
| `PROFILE *.changed_tasks_by_token.__GITLAB__` | 204 in all 3 (lines 21, 32, 43) | 204 in all 3 | yes |
| `OCCURRENCE_ROLES.value` | 1435 | 1435 = sum of all six raw counts | yes |
| remaining GITLAB text/decoded | 0 / 0 each profile (lines 22–23, 33–34, 44–45) | 0 / 0 each profile | yes |

GITLAB occurrence shape (independent): distribution per leaf `{1: 385}`; max per leaf 1; max
per task 6; field split `start_url` 196 and `eval` 189
(`eval.program_html[].url` 132, `eval.reference_url` 49, `must_include[]` 8 — the last
recomputed from provenance pointers with 0 label mismatches across all 1435 records).
Adjacent raw characters: token preceded by `"` in all 385 cases; followed by `"` in 160 and
by `/` in 225; zero occurrences in keys and zero outside JSON string literals. The 8
`must_include` occurrences are tasks 681–688, all with `start_url` `__REDDIT__` and
`program_html[0].url` `last`, originals like `__GITLAB__/eriklindernoren/PyTorch-GAN`.

Provenance validation for GITLAB (instrument JSON, checked against raw text): 385 records;
offset set equal to the independent 385 (missing 0, extra 0, duplicate 0); each offset slices
exactly `__GITLAB__`; task-index mismatches 0; pointer-first-segment/task-index mismatches 0;
per-pointer record counts equal independent leaf occurrence counts (0 mismatched pointers);
0 pointers failing to resolve to a token-bearing leaf. Offsets are unique across all tokens
(1435 offsets, 0 cross-token duplicates); the ASCII input makes them simultaneously Unicode
codepoint and byte offsets at these positions.

## Overlap / substring findings (all consistent with instrument)

- No token is a substring of another: all 30 ordered `in` pairs are false. In particular
  `__SHOPPING__` is not in `__SHOPPING_ADMIN__` and vice versa, so the instrument's
  `__SHOPPING__` 281 does not absorb `__SHOPPING_ADMIN__` 300; bare stems would instead give
  `SHOPPING` 581 = 281 + 300.
- 0 GITLAB occurrences lie inside another token's occurrence; 0 self-overlap adjacencies
  (token border `__` would permit overlap at distance 10, but none exists), so overlap and
  non-overlap counting are identical for every token.
- No frozen profile value contains any token, so sequential order cannot cascade; the
  per-step applied counts equal the original counts for all six tokens in all profiles.
  GITLAB is first anyway.
- GITLAB task set intersects only REDDIT: 17 tasks (552–555, 562–566, 681–688);
  0 with SHOPPING/SHOPPING_ADMIN/MAP/WIKIPEDIA. Sum of per-token task counts is 834 and
  union is 812, reproducing the candidate's non-additivity statement.
- Slash boundary: 225 GITLAB tokens are followed by `/`; under `trailing_slash_sensitivity`
  the independent `value`+`/` junction count is 225 for GITLAB and 697 for all tokens, and 0
  in the other two profiles, matching summary lines 24/35/46 and the candidate line 48.

## Projection-wide checks run alongside

All three profiles: `projected_text_sha256` reproduced
(`2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`,
`54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b`,
`49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`); parsed task count 812 and string leaf
count 10869 each; changed leaves 1416 and changed tasks 812 each; multi-token-occurrence
leaves 13 each; per-token changed-leaf/task rows for every token equal to the instrument's;
path-template totals `start_url` 812, `program_html[].url` 338, `reference_url` 205,
`must_include[]` 60, annotation 1; category 1355 url / 61 non-url matched. Per-task
`changed_leaves` (pointer, original, projected, tokens) matched for all 2436 task/profile
records; projected task deep equality 2436/2436; `would_be_file_sha256` 2436/2436 (my digest
computed from insertion-order `json.dumps(..., indent=2)`). Multi-occurrence arithmetic is
consistent: REDDIT leaves `{1:315, 2:4, 3:3, 4:1}` (8 multi, 13 surplus occurrences) plus
SHOPPING `{1:270, 2:4, 3:1}` (5 multi, 6 surplus) = 13 multi leaves, 19 surplus = 1435−1416.

## Mismatches

None. My comparison array `instrument_vs_independent` in `census.json` is empty (`[]`).
No metric line for GITLAB, its provenance records, its per-profile rows, or any adjacent
all-token row disagreed with independent re-derivation. The only textual difference found
was between the build receipt and instrument stdout itself: `corpus/evidence/round29-calibration/build-summary.txt`
has one extra final line `exit=0` (receipt wrapper artifact, line 48) that the instrument
`--summary` does not emit; the 47 instrument lines are identical. The current `--json`
sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` (3881050 bytes) matches `build-json-sha256.txt`.

## Residual ambiguity / limits (not mismatches)

Everything above this heading is observed from the named command stdout/`census.json`; the
inferential reading below is tagged `[INFERENCE]`, and the remaining bullets are scope limits.

- Every GITLAB-bearing leaf carries exactly one GITLAB occurrence, so the GITLAB row cannot
  by itself distinguish leaf counting from occurrence counting; 385 is both. The instrument's
  leaf semantics appear only through REDDIT (323 leaves vs 336 occurrences) and SHOPPING
  (275 vs 281). [INFERENCE] The GITLAB row is correct under either reading on this input, so
  its semantics are under-discriminated here; that is an observability limit, not an error.
- Whether `applied_replacements` is recomputed per step or copied from the original counts is
  not distinguishable on this input, because no profile value contains a token (output would
  be byte-identical either way).
- The raw file is ASCII, so codepoint offsets equal byte offsets here; this item does not
  exercise a multibyte-offset discrimination.
- Scoped to census/projection of public raw data; no runtime scorer, URL validity,
  deployment or task-validity claim was tested.

## Candidate cross-check (observed, no contradiction)

Candidate `.ufo/waves/round-29/drafts/webarena-config-projection.md` sha256
`7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc`
lines 41–44, 46–48, 51–52 and 60 were independently reproduced: occurrence vector
385/336/281/300/0/133 = 1435; task vector 204/128/192/182/0/128 with sum 834 and union 812;
1416 changed of 10869 leaves, 13 multi; category split 1355/61 (must_include 60, annotation
1); markers `__last_url__` 65, `__page__` 12; index==task_id 812/812; `//` junctions 697
under trailing-slash profile and 0 otherwise; candidate line 52's 8-word assertion, "none is
inside a key or structural text", holds for all 1435 occurrences. `sites` is not a token
carrier: GITLAB appears only under `start_url` and `eval`.

## Commands (all run from lane root; stdout in scratch)

- `sha256sum` over the four pinned inputs → hashes above.
- `python3 plans/config_projection.py --summary` → exit 0, 47 lines; diff vs build receipt
  shows only the receipt's appended `exit=0`.
- `python3 plans/config_projection.py --json` → exit 0, 3881050 bytes,
  sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`.
- `python3 plans/config_projection.py --selftest` → exit 0, one line reporting
  `SELFTEST clean cases=20`.
- `python3 .ufo/waves/round-29/scratch/falsify/FTokenGitlab/census.py` → exit 0,
  `census.json` sha256 `627d2e6173b42a1115f2b3da1c92d6891c6e933b34509391b5fcbd4d8a8ebbee`.
- `grep -o '__GITLAB__' plans/fixtures/r28/webarena/config_files/test.raw.json | wc -l`
  → 385; `__SHOPPING__` → 281; `__SHOPPING_ADMIN__` → 300.

Tooling: no installs or upgrades performed. No pacman transactions. No production, fixture,
corpus, SOURCES, SCORECARD, candidate or lane-state writes; scratch and this report only.

VERDICT: PASS
