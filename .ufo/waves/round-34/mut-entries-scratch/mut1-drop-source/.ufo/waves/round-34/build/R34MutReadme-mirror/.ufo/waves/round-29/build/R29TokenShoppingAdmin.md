# Round 29 token census — `__SHOPPING_ADMIN__`

Seat: `KengakuR28.R29TokenShoppingAdmin-2`. Actual writer: same seat (single leaf; no delegation,
no production edits, no production-tool run). Scope: this token's raw/decoded census, field
provenance and own-token 3-profile span arithmetic. Not a six-token census and not a round
admission.

## Inputs read once (pins verified before census)

| input | bytes | sha256 observed |
|---|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| `plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |
| `plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |
| `plans/fixtures/r29/generate_test_data.py` (inert data, not imported/executed) | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |

All four match the manifest/profile pins. Interpreter `Python 3.14.8`; no installs or upgrades were
needed or performed. Raw text is UTF-8, 880776 bytes = 880776 Unicode codepoints, 0 non-ASCII
codepoints, so for this input only, codepoint offset equals byte offset. Offsets below are labeled
as codepoints.

Generator confirms the frozen order at line 14 (quote, 4 words: `raw = raw.replace("__SHOPPING_ADMIN__", SHOPPING_ADMIN)`)
and index-based output naming at line 21 (quote, 5 words: `for idx, item in enumerate(data):`).

## Observed census

Raw literal occurrences: **300**. Decoded string-value occurrences: **300**. String value leaves
containing the token: **300** (one token per leaf, no leaf with two). Key literals containing the
token: **0**. Raw count equals decoded count; no `\u005f` escape form and no backslash inside any
token-bearing literal. This equality is token-local: the file contains 1335 backslash escapes
elsewhere (1274 `\"`, 12 `\n`, 49 `\uXXXX` such as 19 `\u2019`, 8 `\u00ee`), none inside a
token-bearing literal.

Raw token-start offsets (codepoints): min **172**, max **855286**; first three **172, 975, 1762**;
last three **847765, 848015, 855286**. Every occurrence is at content position 0 of its string
literal (opening quote at offset−1); occurrence order is task-index nondecreasing.
A recursive parse of the raw text checked 10869 value string literals against independent
`json.loads` lookup: **0 mismatches**.

### Owning tasks

182 tasks contain the token; all and only tasks with `sites == ["shopping_admin"]` (182 of 812).
Two further tasks include `shopping_admin` in `sites` (`task_id` 759, 760, `sites`
`["map","shopping_admin"]`, `start_url` `__MAP__`) and contain no `__SHOPPING_ADMIN__`.
Corpus-wide `index == task_id` is 812/812 with 812 unique IDs.
Occurrences per token task: 1×88, 2×82, 3×5, 4×4, 5×1, 6×2 (182 tasks, 300 occurrences).
Declared `eval_types` in token tasks: `string_match` 88, `program_html` 66,
`url_match+program_html` 25, `url_match` 3. 28 tasks carry the token in `eval.reference_url`
(25+3), 66 tasks in `eval.program_html[*].url`; no token task has it in both.

### Field and JSON-path provenance

| JSON path | occurrences | tasks | distinct values | value == token | token + suffix | raw token-offset range (cp) |
|---|---|---|---|---|---|---|
| `/start_url` | 182 | 182 | 7 | 175 | 7 | 172–855286 |
| `/eval/reference_url` | 28 | 28 | 13 | 0 | 28 | 143453–742588 |
| `/eval/program_html/*/url` | 90 | 66 | 84 | 0 | 90 | 387574–848015 |
| total | 300 | 182 | 98 | 175 | 125 | 172–855286 |

`/start_url` token tasks are split: 175 whole-value placeholders (`__SHOPPING_ADMIN__` exactly)
and 7 placeholder+path values. All 28 `reference_url` and 90 `program_html` url values are
placeholder+path. Of the 173 `program_html` entries in token tasks (163 with keys
`locator,required_contents,url`; 10 adding `prep_actions`), 90 `url` values carry the token.

Suffix shapes: 125 values have a character after the token; 86 of those end in `/`; 5 contain
`/../` (e.g. `__SHOPPING_ADMIN__/../antonia-racer-tank.html`); none contain `?`, `#` or `%`;
longest value is 87 codepoints. Each profile's `SHOPPING_ADMIN` replacement string was checked for
substitution safety: no quote, no backslash, and none of the other five token literals.

### Non-URL metadata

Token occurrences in `intent`, `intent_template`, `instantiation_dict`, `storage_state`,
`require_login`, `geolocation`: **0 each**; in JSON keys: **0**. By field type all 300 occurrences
are in URL-typed fields. By string shape, **0 of 300** values are `scheme://`-prefixed before
projection: the placeholder occupies the scheme/authority position or is the whole value. Thus
"non-URL metadata" contributes 0 occurrences, while "URL-shaped before projection" is also 0 — the
two classifications must not be conflated. [INFERENCE] A decoded-leaf oracle that requires
`scheme://` at the token position matches 0/300 here; a field-name/leaf walk matches 300/300, so
those two oracle styles are not equivalent on this input.

## Own-token projection arithmetic (3 frozen profiles)

Replacement values (`profiles.json` → `SHOPPING_ADMIN`; purpose quote, 8 words:
`controlled synthetic text-substitution profile, not an observed deployment`):

| profile | replacement | len | Δ/occurrence | own total Δ (300) | projected file cp, this token only | offset predictions | parses | token left | repl occurrences | `//` after authority |
|---|---|---|---|---|---|---|---|---|---|---|
| `distinct_origins` | `http://shopping-admin.invalid:10104` | 35 | +17 | +5100 | 885876 | 300/300 | 812 tasks | 0 | 300 | 0 |
| `path_prefix` | `http://shopping-admin.invalid:10204/prefix` | 42 | +24 | +7200 | 887976 | 300/300 | 812 tasks | 0 | 300 | 0 |
| `trailing_slash_sensitivity` | `http://shopping-admin.invalid:10304/` | 36 | +18 | +5400 | 886176 | 300/300 | 812 tasks | 0 | 300 | 125 |

Span rule observed: each raw token span `[o, o+18)` becomes `[o+δ, o+δ+len(replacement))` where δ is
the cumulative own-token delta of earlier occurrences in file order; predicted positions equal
actual `str.replace` positions for all 300 occurrences in all three profiles. 175 whole-value
leaves project to the replacement exactly; 125 leaves project to replacement+suffix. Under
`trailing_slash_sensitivity`, those 125 become `:10304//<suffix>` (double slash inserted); under
the other two profiles no double slash appears. `/../` segments are preserved verbatim in all
profiles. No normalization, escaping repair or URL-only substitution is applied in these figures.

Units are kept separate: 300 raw occurrences = 300 leaves = 300 replacement events per profile
(900 across three profiles), in 182 tasks = 182 task/profile projections per profile (546 across
three; shared expectation for the whole round is 812×3=2436, context only, not executed here).
These projected lengths are own-token-only; the other five tokens' deltas are outside this slice,
so absolute projected offsets must add them.

## Cross-token and cascade boundary

`__SHOPPING__` is not a substring of `__SHOPPING_ADMIN__` (nor the reverse), no leaf in the corpus
contains two distinct tokens (0), and no `SHOPPING` profile value contains the admin token, so the
preceding `SHOPPING` replacement cannot create or consume `__SHOPPING_ADMIN__` occurrences under
any of the three profiles. Earlier-token replacements (GITLAB, REDDIT, SHOPPING) still shift
absolute projected offsets of this token's occurrences; that shift is not computed here.

## Commands (cwd = lane root) and exact outputs

```
sha256sum plans/fixtures/r28/webarena/config_files/test.raw.json plans/fixtures/r29/manifest.json \
  plans/fixtures/r29/profiles.json plans/fixtures/r29/generate_test_data.py
LC_ALL=C grep -o '__SHOPPING_ADMIN__' plans/fixtures/r28/webarena/config_files/test.raw.json | wc -l
python3 .ufo/waves/round-29/scratch/KengakuR28.R29TokenShoppingAdmin-2/token_census.py \
  plans/fixtures/r28/webarena/config_files/test.raw.json \
  > .ufo/waves/round-29/scratch/KengakuR28.R29TokenShoppingAdmin-2/census.json
python3 .ufo/waves/round-29/scratch/KengakuR28.R29TokenShoppingAdmin-2/field_provenance.py
python3 .ufo/waves/round-29/scratch/KengakuR28.R29TokenShoppingAdmin-2/span_projection.py
printf '%s' 'controlled synthetic text-substitution profile, not an observed deployment' | wc -w
```

Verbatim stdout for `grep|wc -l`, `field_provenance.py` and `span_projection.py`
(saved in scratch as `field_provenance.out`, `span_projection.out`):

```
300
tasks=812 token_tasks=182 leaves=300
index_eq_task_id=812/812
ids_unique=812
task_sites_token_only_shopping_admin={('shopping_admin',)}
field=start_url occurrences=182 tasks=182 distinct_values=7 exact_token=175 suffixed=7
field=eval.reference_url occurrences=28 tasks=28 distinct_values=13 exact_token=0 suffixed=28
field=eval.program_html[*].url occurrences=90 tasks=66 distinct_values=84 exact_token=0 suffixed=90
nonurl_field=intent tasks_with_token=0
nonurl_field=intent_template tasks_with_token=0
nonurl_field=instantiation_dict tasks_with_token=0
nonurl_field=storage_state tasks_with_token=0
nonurl_field=require_login tasks_with_token=0
nonurl_field=geolocation tasks_with_token=0
key_literals_with_token=0
values_scheme_prefixed=0
values_starting_with_token=300
eval_types_token_tasks=[(('string_match',), 88), (('program_html',), 66), (('url_match', 'program_html'), 25), (('url_match',), 3)]
token=__SHOPPING_ADMIN__ len=18 raw_occurrences=300
raw_codepoints=880776 raw_bytes=880776 non_ascii=0
profile=distinct_origins repl_len=35 delta=17 total_own_delta=5100 projected_len=885876 offset_predictions=300/300 parses_tasks=812 token_remaining=0 repl_occurrences=300 double_slash_after_authority=0
profile=path_prefix repl_len=42 delta=24 total_own_delta=7200 projected_len=887976 offset_predictions=300/300 parses_tasks=812 token_remaining=0 repl_occurrences=300 double_slash_after_authority=0
profile=trailing_slash_sensitivity repl_len=36 delta=18 total_own_delta=5400 projected_len=886176 offset_predictions=300/300 parses_tasks=812 token_remaining=0 repl_occurrences=300 double_slash_after_authority=125
distinct_leaf_values=98
```

Selected `census.json` values (saved JSON, not stdout lines):
`raw_literal_occurrences=300`, `decoded_value_occurrences=300`, `raw_equals_decoded_values=true`,
`string_value_leaves_with_token=300`, `key_literal_hits=[]`, `url_typed_field_occurrences=300`,
`non_url_typed_field_occurrences=0`, `value_string_literals_checked=10869`,
`parser_vs_jsonloads_mismatches=0`,
`json_valid_after_own_token_replacement={"valid": true, "tasks": 812, "token_remaining": 0}`.

Scratch artifact hashes (sha256), current bytes:
`token_census.py` `850b54e95986efc4643c641d4d4394202fadfe46edf650d0fc56604c5df65297`;
`field_provenance.py` `c8f0c37ac88881b4f75762d67d4c999683b5761b4383015046eaa43ed307e708`;
`span_projection.py` `32242a70061db68f883257a2d607fd2e963c54536b422e2851f2e06053774dff`;
`census.json` `774ab0099f172824f73084bf161332484b74f0e01277c4a00cecb870e0b8e0cb`;
`span_projection.out` `e0e91f0c4841977254bfac5b672ecc3ca8d8076b73cf2c360bda9f0e022db810`;
`field_provenance.out` `a3f4777baaef14092b3061aee4c443037759b6209c0e9c9b5b29c4f8ee7776fd`.

## Unknowns and boundaries

- Only `__SHOPPING_ADMIN__` was censused; the other five tokens' occurrence and delta totals are
  not measured here and no total-marker-resolution claim is made.
- Own-token-only projected text parses to 812 tasks with 0 token left in all three profiles; full
  six-token projection validity and per-task object equality are not claimed by this seat.
- `eval_types` are declarative data; runtime consumption of `start_url`, `reference_url` or
  `program_html[*].url` by any harness/scorer was not observed.
- Tasks 759/760 (map+shopping_admin, no token) and the 83 non-token `program_html` entries in
  token tasks were observed but not explained; they are outside this token's slice.
- No actual `config_files` outputs were written; no production code was imported or executed; no
  endpoint, browser profile, cookie or credential store was touched.

VERDICT: PASS
