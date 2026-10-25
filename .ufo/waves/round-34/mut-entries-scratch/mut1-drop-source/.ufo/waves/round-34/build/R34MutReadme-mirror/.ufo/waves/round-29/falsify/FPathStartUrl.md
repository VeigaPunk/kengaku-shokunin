writer: KengakuR29-2.FPathStartUrl-2
seat: KengakuR29-2.FPathStartUrl-2 (leaf member, read-only; no subagents, no REA devices)
item: FPathStartUrl — attack the changed-leaf count and JSON-path category for template `start_url`
scope: round 29 integrated lane master 56fd949a6478342531e61f4feecb4a685d831640; instrument `plans/config_projection.py`
date: 2026-10-21

# Attack

Independent leaf census of the pinned raw task file, focused on the JSON path `start_url`:

1. enumerate every raw task leaf at `start_url`, whether it contains a replacement token, and
   how many of those leaves change under each of the three frozen profiles;
2. independently derive `changed_leaves_by_path_template` and `changed_leaves_by_category`
   (declared predicate: `url_field` = `start_url`, `eval.reference_url`,
   `eval.program_html[].url`; everything else `non_url_field`; strictly by JSON path);
3. sample five changed `start_url` leaves per profile, print original→projected values, and
   re-derive each by hand from the raw task slice;
4. compare only against the instrument's `--summary` and `--json` **output**.

All experiments ran read-only; my scripts and captured outputs live only under
`.ufo/waves/round-29/scratch/falsify/FPathStartUrl/`. No production file, fixture, corpus,
SCORECARD, SOURCES or candidate file was written. No tools installed or upgraded (python3
3.14 stdlib only); no pacman transactions.

## Independence statement

**I did not read or import `plans/config_projection.py`.** I read only the prereg text
`plans/round-29-claims.md`, the pinned generator `plans/fixtures/r29/generate_test_data.py`
(11 code lines), `plans/fixtures/r29/manifest.json`, `plans/fixtures/r29/profiles.json`, and
the pinned raw file `plans/fixtures/r28/webarena/config_files/test.raw.json`. My oracle
(`scratch/.../oracle_v2.py`) implements the text contract with its own walk, my own six
sequential `str.replace` steps and its own `json.loads`; the comparator
(`scratch/.../compare_start_url.py`) reads the instrument's stdout capture only. I computed
the instrument file's sha256 (`5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`)
without reading its contents.

# Commands and exact outputs (units stated)

| # | command | exit | observed |
|---|---|---|---|
| 1 | `python3 plans/config_projection.py --summary` | 0 | 47 lines; sha256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`; repeat run identical |
| 2 | `python3 plans/config_projection.py --json` | 0 | 3,881,050 bytes; sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`; repeat run identical |
| 3 | `python3 .ufo/waves/round-29/scratch/falsify/FPathStartUrl/oracle_v2.py` | 0 | independent census (below) |
| 4 | `python3 .ufo/waves/round-29/scratch/falsify/FPathStartUrl/summary_check.py` | 0 | `SUMMARY_START_URL_MISMATCHES 0` |
| 5 | `python3 .ufo/waves/round-29/scratch/falsify/FPathStartUrl/compare_start_url.py` | 0 | `TOTAL MISMATCH GROUPS 0` |
| 6 | `python3 .ufo/waves/round-29/scratch/falsify/FPathStartUrl/hand_rederive.py` | 0 | `HAND_SAMPLE_FAILURES 0 of 15` |

Pinned input identities re-verified by me: raw `sha256 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, 880,776 bytes/chars (ASCII);
manifest `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`; profiles
`90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`; generator
`45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`.

# Observed facts

## A. Raw task leaf census at `start_url`

My own parse of the raw bytes: 812 top-level task objects; no duplicate object key anywhere
(`object_pairs_hook` check); whole-document leaf walk = 15,574 leaves, of which 10,869 are
strings (matching the instrument's `string_leaf_count`).

At the path template `start_url` (top level of each task):

- **812 leaves**, one per task index 0..811, all JSON type `str`; no other template in the
  file ends with the segment `start_url` (only `start_url` itself).
- **812/812 contain at least one replacement token**; therefore every one of them can change.
- Token composition by *leaf*: `__GITLAB__` 196, `__REDDIT__` 114, `__SHOPPING__` 192,
  `__SHOPPING_ADMIN__` 182, `__WIKIPEDIA__` 0, `__MAP__` 128 (sum 812). Each leaf carries
  exactly one token *type* (no mixed-type leaf).
- Token *occurrences* inside `start_url` = 818, i.e. 6 more than leaves: `__SHOPPING__`
  occurs 198 times across 192 leaves (one leaf ×3 at index 431; four leaves ×2 at indices
  432–435). Occurrences must not be pooled with leaves.
- No `__last_url__`, `__page__` or other `__…__` marker appears in any `start_url` value (0).
- Raw-text token total (1,435) equals the sum of token occurrences over all string leaves
  (1,435), so no occurrence sits outside a leaf value (e.g. no token in a key).

## B. Change per profile (my independent projection)

Sequential replacements in generator order (source lines 11–16: GITLAB, REDDIT, SHOPPING,
SHOPPING_ADMIN, WIKIPEDIA, MAP), then my own `json.loads`. Applied counts per profile:
GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133.

| profile | projected text sha256 | parsed tasks | changed leaves | changed tasks | changed `start_url` leaves | all `url_field` | changed indices |
|---|---|---|---|---|---|---|---|
| distinct_origins | `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` | 812 | 1,416 | 812 | **812** | 812 | 0..811 |
| path_prefix | `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` | 812 | 1,416 | 812 | **812** | 812 | 0..811 |
| trailing_slash_sensitivity | `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2` | 812 | 1,416 | 812 | **812** | 812 | 0..811 |

Total changed `start_url` leaf instances = 812 × 3 = **2,436**. No type change at any leaf
under any profile; every changed leaf is a string; no projected `start_url` retains a known
token (0 of 2,436).

## C. Instrument output vs. oracle — exact agreement

`--summary` lines 18/19, 29/30, 40/41 report (three profiles, identical values):

- `start_url` = **812** in `changed_leaves_by_path_template` on lines 19, 30, 41;
- `changed_leaves_by_category` = `{"non_url_field": 61, "url_field": 1355}` on lines 18, 29, 40;
- other templates: `eval.program_html[].required_contents.must_include[]` 60,
  `eval.program_html[].url` 338, `eval.reference_answer_raw_annotation` 1,
  `eval.reference_url` 205. Sum 60+338+1+205+812 = 1,416 = `changed_leaf_count`; category sum
  61+1,355 = 1,416. My independent values are identical under `summary_check.py`
  (`SUMMARY_START_URL_MISMATCHES 0`).

`--json` network-level cross-check, three profiles:

- per-task `changed_leaves` entries: 1,416 per profile (4,248 total); my pointer-keyed
  reconstruction has the *identical* pointer set (0 only-instrument, 0 only-oracle), no
  duplicate pointers, and **0** value, 0 path-template, 0 category and 0 token-attribution
  mismatches;
- full `projected_task` objects equal my independent projection for **2,436/2,436** records;
  `projected_task.start_url` equal in 2,436/2,436;
- `start_url` changed-entry count 2,436; every one has `"category": "url_field"`;
- path→category pairs observed across the three profiles: `start_url`→`url_field` 2,436,
  `eval.reference_url`→`url_field` 615, `eval.program_html[].url`→`url_field` 1,014,
  `eval.program_html[].required_contents.must_include[]`→`non_url_field` 180,
  `eval.reference_answer_raw_annotation`→`non_url_field` 3. This is exactly the declared
  path rule with no exceptions;
- `changed_leaves_with_multiple_occurrences` = 13 matches my count: 5 `start_url` leaves
  (1×3 + 4×2 = 6 extra occurrences) + 7 `eval.reference_url` leaves + 1
  `eval.reference_answer_raw_annotation` leaf = 19 extra occurrences over 1,416 leaves
  → 1,435 raw occurrences. Occurrence/leaf/task units are not pooled;
- `occurrence_provenance`: 1,435 entries, **0** where
  `raw[original_input_codepoint_offset : +len(token)] != token`; 818 entries at
  `start_url` (196/114/198/182/0/128), equal to my raw occurrence counts.

## D. Hand re-derivation — five changed `start_url` leaves per profile

Method: `json.JSONDecoder().raw_decode` slice of raw task `i`; six literal `str.replace`
calls in generator order with that profile's values; `json.loads`; read `start_url`. Each
result was compared with the instrument's `changed_leaves` entry and `projected_task.start_url`.
15/15 matched (`HAND_SAMPLE_FAILURES 0 of 15`), with `output_index == task_id == i` and
`config_files/<i>.json`:

| task idx | original `start_url` | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|---|
| 0 | `__SHOPPING_ADMIN__` | `http://shopping-admin.invalid:10104` | `http://shopping-admin.invalid:10204/prefix` | `http://shopping-admin.invalid:10304/` |
| 7 | `__MAP__` | `http://map.invalid:10106` | `http://map.invalid:10206/prefix` | `http://map.invalid:10306/` |
| 27 | `__REDDIT__` | `http://reddit.invalid:10102` | `http://reddit.invalid:10202/prefix` | `http://reddit.invalid:10302/` |
| 44 | `__GITLAB__` | `http://gitlab.invalid:10101` | `http://gitlab.invalid:10201/prefix` | `http://gitlab.invalid:10301/` |
| 431 | 609-char `|AND|`-joined triple `__SHOPPING__` | 660 chars, prefix `http://shopping.invalid:10103/tall-pink-taper-candles-4-piece…` | 681 chars, prefix `http://shopping.invalid:10203/prefix/tall-pink-taper-candles…` | 663 chars, prefix `http://shopping.invalid:10303//tall-pink-taper-candles…` (documented `//` junction) |

Additional hand checks: raw field context is `"start_url": "__SHOPPING_ADMIN__",` etc. (task
0); task slice 44 contains two `__GITLAB__` occurrences but only one is in `start_url`, and
the instrument counts that as **one** changed leaf — the correct unit. For task 431 all three
`__SHOPPING__` occurrences inside `start_url` were replaced in each profile and the full
609→660/681/663-character strings matched byte-for-byte.

# Mismatches

**None.** Every attacked number and category assignment for `start_url` agrees with my
independent derivation on all three profiles:

- 812 raw `start_url` leaves, all token-bearing; 812 changed per profile; 2,436 total;
- `changed_leaves_by_path_template["start_url"] = 812` × 3 (summary lines 19, 30, 41);
- `url_field` includes exactly the three declared templates, `start_url` among them;
- per-task JSON values, pointers, categories and token lists all match;
- occurrence provenance offsets for `start_url` all verify against the raw bytes.

# Caveats / residual unknowns

1. **Category name is path-based, not value-based (observed).** All 61 `non_url_field`
   changed leaves per profile (183 across profiles) hold projected values that contain
   `http://` or `https://` — 60 `eval.program_html[].required_contents.must_include[]` and 1
   `eval.reference_answer_raw_annotation`. This is *correct* under the declared path
   predicate (and the instrument's category totals match it exactly), but "non_url_field"
   does not mean "the value is not a URL". The `--summary`/`--json` output I read does not
   print the predicate itself, so the rule cannot be recovered from output alone.
   [INFERENCE] A consumer that reads the category as value semantics would misclassify those
   61 leaves per profile.
2. **Leaf vs. task counting is not discriminable at this path (observed constraint).** One
   `start_url` leaf per task makes 812 both a leaf count and a task count. The additive
   template sum (equals 1,416) plus one entry per task in `changed_leaves` supports leaf
   units, but this input alone cannot falsify a task-counting implementation for
   `start_url`. [INFERENCE] The `changed_leaf_count`/template-sum identity is the strongest
   available evidence for leaf units.
3. Not attacked here (out of item scope, other seats cover it): selftest, exit-1/exit-2
   paths, mutation witnesses, non-`start_url` template internals beyond the totals above,
   and the knowledge candidate. No unknown remains for the specific `start_url` count and
   category question.

VERDICT: PASS
