writer: KengakuR29-2.FProfileDistinctOrigins-2

# FProfileDistinctOrigins-2 — attack on profile `distinct_origins`

Seat: KengakuR29-2.FProfileDistinctOrigins-2 (read-only leaf, no subagents).
Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Target under attack: integrated round-29
C1 projection, profile `distinct_origins` quota of the 812x3 = 2436 task/profile projection.
Lane HEAD observed with `git rev-parse HEAD` = `56fd949a6478342531e61f4feecb4a685d831640`;
`git status --porcelain` over the instrument/fixtures/receipts/SOURCES paths was empty before my run.

Independence: I did NOT read or import `plans/config_projection.py` source at any point. I ran its
CLI (`--summary`, `--json`, `--selftest`) and compared stdout only. My projection, leaf census and
junction count were re-derived from the prereg sentence in `plans/round-29-claims.md`, the pinned
generator bytes, `manifest.json`, `profiles.json`, the pinned raw JSON, and the pinned README
snapshot. I did read build evidence (`corpus/evidence/round29-calibration/*`), the S072 row
(`corpus/SOURCES.md:94`), the pinned README, and the draft knowledge file after/beside my own
computations; none of their aggregate numbers were used as inputs to my scripts.
Tooling: no installs or upgrades; python3 stdlib (`json`, `hashlib`, `urllib.parse`) plus shell
`sha256sum`/`diff`/`cmp`.

Input authentication observed before projection (`sha256sum`):

| file | bytes | sha256 |
|---|---|---|
| plans/fixtures/r29/manifest.json | 1061 | f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87 |
| plans/fixtures/r29/profiles.json | 1391 | 90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018 |
| plans/fixtures/r29/generate_test_data.py | 838 | 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd |
| plans/fixtures/r28/webarena/config_files/test.raw.json | 880776 | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |

Raw input is pure ASCII with 0 `\r` bytes, so UTF-8 and text/byte I/O differences are inert.
README snapshot `.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md` hashes to
`081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287`, the hash named in S072.

## Attack 1 — independent `projected_text_sha256`

Independent projection: read the pinned raw bytes once, apply the six global replacements in the
manifest order (`manifest.json:19-25`: GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) with
the six `distinct_origins` values (`profiles.json:5-10`), then SHA-256 the UTF-8 text. A second pass
did byte-level replacement and hashed bytes; both agree.

Observed independent applied occurrence counts: GITLAB 385, REDDIT 336, SHOPPING 281,
SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133 (sum 1435). Projected text: 905171 UTF-8 bytes, ASCII.

- independent text SHA-256: `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`
- independent byte SHA-256: same value
- instrument `--summary` / `--json` `projected_text_sha256`:
  `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`
- match, 0 mismatch.

## Attack 2 — independent `string_leaf_count`

Own JSON walk over `json.loads(projected_text)` counting string values (list items and dict values),
not dict keys. Observed: 10869 string values, 1008 of them empty, 3523 distinct values; 18140 dict
keys; 15574 scalar leaves. Only the 10869 definition equals the instrument value.

- instrument `string_leaf_count` = 10869; independent = 10869; match.
- The original raw parse also yields 10869 string values because replacement preserves string typing;
  the metric therefore cannot by itself distinguish original from projected parse, but it is
  consistent with the projected parse and with `parsed_task_count=812`.

## Attack 3 — independent `stimulus_observations` and junction semantics

Definition applied: at each replacement step, count token occurrences immediately followed by a raw
`/` for tokens whose profile value ends with `/`. For `distinct_origins` no value ends with `/`
(`profiles.json:5-10`, all end in a port digit), so the count is necessarily 0. Cross-checks:

- independent junction count: `distinct_origins` 0, `path_prefix` 0, `trailing_slash_sensitivity` 697.
- alternative formula on projected text, sum of `count(value + "/")` for slash-ending values:
  `distinct_origins` 0, `trailing_slash_sensitivity` 697.
- `//`-delta cross-check: raw text has 23 `//`; projected `distinct_origins` has 1458 = 23 + 1435
  scheme slashes (each `http://` value), 0 junctions; projected `trailing_slash_sensitivity` has 2155
  = 1458 + 697 junctions.
- instrument: `--summary:24` and JSON `stimulus_observations` for `distinct_origins` =
  `{"value_slash_then_raw_slash_junctions": 0}`; trailing profile = 697. Match, 0 mismatch.

## Attack 4 — `stimulus_class` label against `profiles.json` and README shapes

Observed actual values (`profiles.json:5-10`, reproduced verbatim in JSON `profiles.distinct_origins.values`):
six `http://<name>.invalid:<port>` strings. `urllib.parse.urlsplit` gives, per value, scheme `http`,
non-empty hostname, a port, and empty path, query and fragment. Distinct value strings 6/6; distinct
(scheme, host, port) origins 6/6. Label as printed, 9 words:
"origin-only synthetic values; not the README-documented SHOPPING_ADMIN '/admin' shape".
JSON field name is `stimulus_class`; summary field name is `stimulus` (`build-summary.txt:15`),
values are byte-identical (observed string equality).

Against S072 (`corpus/SOURCES.md:94`, 8-word quote: "seven exported variables in scheme-less example
origin:port form") and pinned README lines 86-92:

- README line 86 `export SHOPPING="<your_shopping_site_domain>:7770"`; line 87, 2 words:
  `export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"` — SHOPPING_ADMIN carries `/admin`;
  the profile value has no path, so the label's negative clause is accurate.
- README line 91, 2 words:
  `export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"`
  — WIKIPEDIA carries a long path; the profile value is origin-only. `origin-only` covers this, but
  the label does not name WIKIPEDIA separately.
- README examples are scheme-less host:port strings; the profile adds the `http` scheme. An origin
  includes its scheme, so `origin-only` remains true of the profile values; the README's scheme-less
  spelling is not claimed.
- README's seventh variable HOMEPAGE is marked placeholder (line 92) and is not one of the six
  generator tokens; profiles.json correctly contains only the six tokens.

Verdict of this check: the label is true for the frozen values; no false statement. [INFERENCE] The
README comparison in the label is partial (SHOPPING_ADMIN `/admin` named; WIKIPEDIA path not named),
but this cannot mask a projection defect: WIKIPEDIA token occurrences are 0 (observed above) and the
label's subject is the stimulus class of frozen synthetic values, not README conformance.

## Attack 5 — no stimulus effect routed to a FINDING or exit 1

Observed, on the integrated instrument and the build receipts:

- `python3 plans/config_projection.py --summary; echo EXIT=$?` -> 47 stdout lines, stderr 0 bytes,
  `TOTAL findings=0 exit=0` (receipt `build-summary.txt:47`), EXIT=0. Field line for this profile is
  `build-summary.txt:24`, junction count 0.
- `python3 plans/config_projection.py --json` -> JSON top-level `findings` is `[]`, `profiles` has
  812 task records each for all three profiles, JSON SHA-256
  `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, byte-identical to
  `corpus/evidence/round29-calibration/build-json-sha256.txt` and to a second run; EXIT=0.
- `--summary` output is byte-identical to `build-summary.txt` except the build receipt's appended
  line `exit=0` (`diff` output: only `47a48 > exit=0`); no drift between built and integrated state.
- The stimulus-bearing sibling profile `trailing_slash_sensitivity` actually creates 697 junctions
  (`build-summary.txt:46`) and still reports findings=0, exit=0; `path_prefix` likewise 0/0. So the
  observed per-profile stimulus effects are not routed to a finding.
- The finding channel is live but stimulus-independent: `mutation-witness.txt:4`
  (`url_only_substitution`) contains the summary fragment `TOTAL findings=6 exit=1` (3 words) beside
  selftest exit 1. No stimulus value is involved in that control.
- `--selftest` exit 0, `SELFTEST clean cases=20` (build-selftest receipt; reproduced).

No stimulus effect was observed entering `findings` or forcing exit 1.

## Corroborating per-task checks (independent oracle on the same frozen bytes)

- `projected_task` deep-equality for all 812/812 task records against my independent
  `json.loads(projected_text)`; 0 mismatches.
- `changed_leaves`: 1416 leaves; every `json_pointer` (with its leading task index) resolves on the
  original and projected documents, 0 value mismatches, every listed token present in the original
  and its replacement present in the projected value.
- Per-task changed-leaf counts equal my tree-diff for all 812 tasks; independent aggregates match
  instrument: start_url 812, program_html[].url 338, reference_url 205, must_include[] 60,
  reference_answer_raw_annotation 1; url_field 1355 / non_url_field 61.
- Token attribution matches: GITLAB 385, REDDIT 323, SHOPPING 275, SHOPPING_ADMIN 300, WIKIPEDIA 0,
  MAP 133; 13 leaves carry more than one occurrence (1 annotation/REDDIT, 5 start_url/SHOPPING,
  7 reference_url/REDDIT), explaining applied 1435 vs leaf 1416.
- `occurrence_provenance`: 1435 entries; slice at `original_input_codepoint_offset` equals the token
  in 1435/1435; pointers resolve to string values containing the token in 1435/1435; role `value`
  1435/1435. Offsets are codepoint offsets on ASCII input here; no byte-offset claim tested.
- Output mapping: `output_index=i` and filename `config_files/{i}.json` for 812/812; task_ids are
  0..811 in input order; `index_equals_task_id` true 812/812, `violations` empty.
- Population cross-checks: tasks carrying each token 204/128/192/182/0/128, tasks with any token 812;
  `__last_url__` 65 and `__page__` 12; all match instrument.

## Mismatches found

- Recomputed values: none. `projected_text_sha256`, `string_leaf_count`,
  `stimulus_observations`, applied counts, per-task objects, changed leaves, provenance and mapping
  all match exactly at the locations and values above.
- [INFERENCE] Label-scope observation only, not a value or claim mismatch: the `stimulus_class`
  string names SHOPPING_ADMIN's `/admin` deviation but not README's WIKIPEDIA long path or the
  scheme-less README spelling. `origin-only` entails no path for all six values and WIKIPEDIA has 0
  token occurrences, so no effect on this projection; the label remains true of the frozen values.
- [INFERENCE] `string_leaf_count` is invariant between original and projected parse (both 10869), so
  it is a valid but non-discriminating census; it does not weaken any stated claim.

## Evidence writes

Lane writes: this report only. All intermediate outputs were under `/tmp` (including
`/tmp/r29_fpd2.json`, `/tmp/r29_fpd2_run2.json`, `/tmp/fpd2_sum4.txt`, `/tmp/fpd2_selftest.txt`,
`/tmp/fpd2_err.txt`); no fixture, production, corpus, SOURCES or SCORECARD file was modified and no
git index/ref state was touched.

VERDICT: PASS
