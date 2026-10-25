writer: KengakuR29-2.FProfileTrailingSlashSensitivity-2

# FProfileTrailingSlashSensitivity — recompute the trailing-slash profile, its label, and its routing

**Attack:** independently project the pinned raw 812-task file through the pinned generator contract
under profile `trailing_slash_sensitivity`, without reading or importing
`plans/config_projection.py`; recompute `projected_text_sha256`,
`stimulus_observations.value_slash_then_raw_slash_junctions` and `string_leaf_count`; compare every
projected task object with `--json`; check the `stimulus_class` label against `profiles.json` and the
README example shapes recorded in S072; verify the stimulus observation is not routed into a finding
or exit 1. Round 29 only; lane head `56fd949a6478342531e61f4feecb4a685d831640`.

## Independence, inputs, tooling

I did **not** open or import `plans/config_projection.py`. I ran only its `--help`, `--summary`,
`--json` and `--selftest` interfaces and read stdout. Derivation used the prereg text
(`plans/round-29-claims.md`), the pinned generator bytes, the pinned raw file and `profiles.json`.
The pinned README copy used for the shape check is
`.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md`; its sha256 equals the S072 anchor hash. I
did not fetch the live URL.

| input | observed sha256 | manifest/claim |
|---|---|---|
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | matches assignment |
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | matches manifest |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | matches manifest |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | matches manifest |
| `.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md` | `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` | equals S072 anchor hash |

Raw input: 880776 bytes, ASCII, 0 CR, sha256 as above. `plans/config_projection.py` observed sha256
`5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`, 34007 bytes (read via
`sha256sum`, not by reading source). No tool installs or upgrades; python3 3.14.8 stdlib only; no
network.

## Method (scratch, own implementation)

Scripts under `.ufo/waves/round-29/scratch/falsify/FProfileTrailingSlashSensitivity-2/`:
`proj.py`, `census2.py`, `compare.py`, `evidence.py`; consolidated output in `evidence.txt`.
The projection decodes the pinned raw bytes as UTF-8, applies the six `str.replace` calls in the
pinned order `GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP`, hashes the resulting UTF-8
text, parses it with `json.loads`, walks every string leaf, counts raw token occurrences immediately
followed by `/`, and compares every `projected_task` and `would_be_file_sha256` record against the
instrument's captured `--json`.

```text
$ python3 plans/config_projection.py --summary   # exit 0
PROFILE trailing_slash_sensitivity ... projected_text_sha256=49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2
PROFILE trailing_slash_sensitivity ... string_leaf_count=10869 ...
PROFILE trailing_slash_sensitivity stimulus_observations={"value_slash_then_raw_slash_junctions": 697}
TOTAL findings=0 exit=0
```

## Observed recomputation

| metric | instrument | independent | result |
|---|---|---|---|
| `projected_text_sha256` | `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2` | same | match |
| projected UTF-8 bytes / chars | not printed | 906606 / 906606 | — |
| `string_leaf_count` | 10869 | 10869 (projected; original also 10869) | match |
| `value_slash_then_raw_slash_junctions` | 697 | 697 | match |
| parsed task count | 812 | 812 | match |
| all 812 `projected_task` objects | `--json` | independently parsed objects | 0 mismatches |
| all 812 `would_be_file_sha256` | `--json` | sha256 of `json.dumps(item, indent=2)`, UTF-8 | 0 mismatches |
| changed string leaves | 1416 | 1416 | match |
| changed leaves by token | 385/323/275/300/0/133 | 385/323/275/300/0/133 | match |
| remaining six known tokens | 0 in text and 0 decoded | 0 | match |

Junction accounting, independent: token occurrences in raw = 385/336/281/300/0/133 (total 1435);
occurrences immediately followed by `/` = 225/232/110/125/0/5 (total 697). The 697 occurrences sit
in 678 string leaves and 462 tasks. The projected text contains exactly 697 non-scheme `//` and zero
`///`. The six values all end `/`; therefore each of the 697 junctions is `value` + `/` = `//`.

## `stimulus_class` label audit

Exact label printed by both `--summary` and `--json` (`profiles.trailing_slash_sensitivity.stimulus_class`;
16 whitespace-separated words):

> `synthetic trailing '/' on all six values; a token followed by '/' becomes '//' by design`

`profiles.json:24–33` defines exactly six values, one per generator name; every value ends in one `/`
(`GITLAB` 28 chars, `REDDIT` 28, `SHOPPING` 30, `SHOPPING_ADMIN` 36, `WIKIPEDIA` 31, `MAP` 25).
`WIKIPEDIA` has 0 raw occurrences, which the instrument reports as `applied_replacements` 0.

The README shapes recorded in `corpus/SOURCES.md:94` (S072) and read from the pinned copy:

| README line | value shape | ends `/` |
|---|---|---|
| 86 `export SHOPPING="<your_shopping_site_domain>:7770"` (2 words) | scheme-less origin:port | no |
| 87 `export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"` (2 words) | origin:port plus `/admin` | no |
| 88 `export REDDIT="<your_reddit_domain>:9999"` (2 words) | scheme-less origin:port | no |
| 89 `export GITLAB="<your_gitlab_domain>:8023"` (2 words) | scheme-less origin:port | no |
| 90 `export MAP="<your_map_domain>:3000"` (2 words) | scheme-less origin:port | no |
| 91 `export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"` (2 words) | long documented path | no |
| 92 `export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder` (7 words) | placeholder | no |

No documented example ends in `/`, so the trailing slash is a genuine synthetic departure from all
seven documented shapes; the label does not claim README conformity. S072's teaches clause (20
words) says: `seven exported variables in scheme-less example origin:port form (SHOPPING_ADMIN adds
/admin, WIKIPEDIA adds a long path, HOMEPAGE is marked placeholder)`. Both label clauses check out:
clause 1 against `profiles.json`, clause 2 against the 697 identical `/`-followed occurrences and the
697 projected non-scheme `//`. The candidate draft records the same value at
`.ufo/waves/round-29/drafts/webarena-config-projection.md:48` (11 words): `value-/ then raw-/ junctions (//) | 697 under trailing_slash_sensitivity, 0 otherwise`,
and the expected-effect rule at `:65` (5 words): `Profile effects are stimulus observations.`

## Routing check

| observation | evidence |
|---|---|
| summary exit | `--summary` process exit 0; final line `TOTAL findings=0 exit=0` |
| JSON exit / findings | `--json` exit 0; top-level `findings` = `[]` |
| profile record | no `findings` key; `stimulus_observations` is a profile field only |
| selftest | `--selftest` exit 0; `SELFTEST clean cases=20` (`build-selftest.txt:1`) |
| exit-1 wiring exists | mutation receipt `build/mutation-witness.txt:4`: `url_only_substitution selftest exit 1 killed AssertionError | summary ['TOTAL findings=6 exit=1']` (11 words) |
| pinned stimulus not routed | 697 junctions present, `findings=0`, exit 0, and no `FINDING` line in the captured stdout |

The 697 junctions and the 1416 changed leaves are reported as a profile observation, not as a
projection finding. A real mutation receipt shows the instrument can emit findings and exit 1, so
exit 0 here is a positive routing result, not an inert exit path.

## Mismatches and boundaries

**No mismatch** was found in the three assigned recomputations, in the `stimulus_class` label, or in
the routing of the 697-junction stimulus. Supporting receipt comparison: current `--summary` stdout
is byte-identical, lines 1–47, to `corpus/evidence/round29-calibration/build-summary.txt` lines 1–47
(including trailing-slash `projected_text_sha256` line 39, `stimulus_observations` line 46, and
`TOTAL findings=0 exit=0` line 47); `--json` sha256 is
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, identical to
`build-json-sha256.txt:1`. The build-summary receipt has one extra line 48 `exit=0` beyond instrument
stdout; it is a receipt-envelope line, not a profile value, and lines 1–47 agree.

Non-defect boundaries observed:

- The label states the mechanism and the six-value class, not the README-difference prose or the
  462-task distribution; those appear in S072, the profile `purpose`, the top-level `LIMIT` lines and
  `stimulus_observations` respectively. No label clause is false.
- `WIKIPEDIA` is in the six values but has 0 raw occurrences; the instrument reports that explicitly
  rather than implying it was exercised.
- 697 is an occurrence count, not a task or leaf count (462 tasks, 678 leaves by independent walk).

## [INFERENCE]

- The extra `exit=0` line in `build-summary.txt` is most plausibly an enclosing shell echo of the
  instrument exit status; the instrument stdout itself ends at line 47. I did not reproduce the
  receipt-writing command.
- The pinned README copy is treated as byte-equivalent to the S072-recorded snapshot because its
  sha256 equals the row's anchor hash; I did not re-fetch the live URL to confirm current upstream
  bytes.
- I did not execute the upstream generator, a browser, a URL parser or an evaluator; no runtime
  normalization or deployment claim is made.

VERDICT: PASS
