# R29 single-token census — `__SHOPPING__`

Seat / actual writer: `KengakuR28.R29TokenShopping-2` (worker itself; no delegation).
Round: 29, claim C1 evidence slice only. Report path (lane-relative): `.ufo/waves/round-29/build/R29TokenShopping.md`.
Scope: one token, one pinned raw serialized file, three frozen synthetic profiles. No production edits,
no other-token census, no canonical six-token projection, no endpoint/runtime check.

## Inputs (read once per script run, authenticated bytes retained)

| Input | Bytes | SHA-256 |
|---|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| `plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |
| `plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| `plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |

Source facts, `generate_test_data.py` lines 11–16 in order: GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN,
WIKIPEDIA, MAP. Line 18 writes the replaced text to `config_files/test.json`. Lines 20–23 parse that
projected text and write per-task files by `enumerate` index with `json.dump(item, f, indent=2)`.
Line 13 quote, programmatic word count 4 (`printf ... | wc -w`):
`raw = raw.replace("__SHOPPING__", SHOPPING)`

Raw file properties: 880776 bytes, 880776 Unicode codepoints, pure ASCII true, UTF-8 BOM false,
29604 lines (`wc -l`), 812 top-level items, 812 distinct `task_id`, all ASCII. Because the
file is pure ASCII and carries no escapes inside token-bearing literals, codepoint offset == byte
offset here; offsets below are nevertheless named and computed as **Unicode codepoints**.

## Exact counts (units kept separate)

Commands (cwd `plans/fixtures/r28/webarena/config_files`), with observed output:

```
grep -c '__SHOPPING__' test.raw.json              -> 275     # lines, NOT occurrences
grep -o '__SHOPPING__' test.raw.json | wc -l      -> 281     # occurrences
grep -o '__SHOPPING_ADMIN__' test.raw.json | wc -l-> 300     # sibling form, excluded (no shared prefix match)
grep -o '__SHOPPING[A-Z_]*' test.raw.json | wc -l -> 581     # 281 + 300, no other form
dd if=test.raw.json bs=1 skip=20068  count=12     -> __SHOPPING__
dd if=test.raw.json bs=1 skip=308024 count=12     -> __SHOPPING__
dd if=test.raw.json bs=1 skip=862731 count=12     -> __SHOPPING__
```

| Unit | Count |
|---|---|
| Raw serialized literal occurrences | **281** |
| Decoded leaf occurrences (post-JSON-parse) | **281** |
| String literals/leaves containing the token | **275** |
| Distinct JSON paths | **275** |
| Tasks owning at least one occurrence | **192** |
| Occurrences in JSON keys | **0** (all 275 are values) |
| Leaves with >1 occurrence | 5 (270 leaves ×1, 4 ×2, 1 ×3) |
| Tasks with >1 occurrence | 78 (114 ×1, 68 ×2, 9 ×3, 1 ×4) |
| Occurrences after SHOPPING-only substitution | **0** |

Occurrence distribution by owner key (occurrences / distinct leaves):

| Key | Occ | Leaves |
|---|---|---|
| `start_url` | 198 (171 bare + 27 token+path) | 192 |
| `eval.reference_url` | 52 | 52 |
| `eval.program_html[].url` | 31 | 31 |

Value shapes: 171 occurrences are the whole value (`value == "__SHOPPING__"`, length 12 codepoints);
110 are a prefix immediately followed by `/` and then a URL path (leaf length 20–609). Next character
after the token is `/` in 110 cases and end-of-value in 171; no other follower exists. Multi-occurrence
leaves: `[431].start_url` (3), `[432..435].start_url` (2 each). Task 431 owns 4 occurrences
(`start_url` ×3 + `program_html[0].url` ×1). The 192 affected tasks form 30 contiguous index ranges:
(21–26), (47–51), (96), (117–118), (124–126), (141–150), (158–167), (188–192), (225–235), (238–242),
(260–264), (269–286), (298–302), (313), (319–338), (351–355), (358–362), (368), (376), (384–388),
(431–440), (465–469), (506–521), (528–532), (571–575), (585–589), (653–657), (671–675), (689–693),
(792–798).

Examples (public fixture data): `[21].start_url` = `__SHOPPING__/6s-wireless-headphones…` (cp 20068,
line 683); `[47].start_url` = `__SHOPPING__` (cp 44214, token-only); `[431].start_url` holds 3
occurrences; `[798].start_url` = `__SHOPPING__` (cp 862731, line 28996, last occurrence).

## Raw serialized vs decoded/escaped vs non-URL metadata

- 0 of the 275 token-bearing literals contain any backslash; raw literal content equals the decoded
  string for every one. 0 occurrences of `\u005f`/`\u005F` exist anywhere in the file (file-wide, 642
  string literals do contain backslashes, but none of those holds the token). Therefore raw and decoded
  occurrence counts are both 281 and their value-relative positions correspond exactly; no
  decode-escape mapping was needed in the token slice.
- All 281 occurrences sit in URL-valued fields: `start_url`, `eval.reference_url`,
  `eval.program_html[].url`. **0 occurrences in non-URL metadata fields.**
- Case-sensitive separation: the lowercase word `shopping` occurs 222 times across 192 tasks in
  `sites[0]` (192 values that are exactly `"shopping"`), `intent` (15) and `intent_template` (15).
  None starts with `http`, and none is a replacement target; the generator replaces only the exact
  uppercase `__SHOPPING__` token. These are metadata mentions, not token occurrences, and must not be
  pooled with the 281 count.

## Replacement-length and codepoint-span implications (three frozen profiles)

Each profile substitutes exactly this token only (SHOPPING-only measurement; see boundary below).
Token length 12 codepoints.

| Profile | Replacement | Len | Delta/occ | Total delta | Projected cp | Last occ cp |
|---|---|---|---|---|---|---|
| `distinct_origins` | `http://shopping.invalid:10103` | 29 | +17 | 4777 | 885553 | 867491 |
| `path_prefix` | `http://shopping.invalid:10203/prefix` | 36 | +24 | 6744 | 887520 | 869451 |
| `trailing_slash_sensitivity` | `http://shopping.invalid:10303/` | 30 | +18 | 5058 | 885834 | 867771 |

Derived and measured span behavior, per profile:

- First occurrence start stays at cp 20068 (`[21].start_url`); last occurrence start moves 862731 →
  867491 / 869451 / 867771.
- Per-task codepoint delta = occurrences-in-task × delta: 17/34/51/68 (114/68/9/1 tasks),
  24/48/72/96, 18/36/54/72. Maximum task delta 68/96/72 (task 431, 4 occurrences).
- Forward span formula `task_start + Σ prior task occurrence deltas` matched all 812 task starts and
  all 812 task ends against a fresh parse of the projected text for every profile.
- Every occurrence offset projected by `raw_cp + k × delta` (k = prior occurrences) selects exactly
  the profile replacement string in the projected text; offsets are monotone.
- Upstream per-task artifacts are re-serialized with `json.dump(item, indent=2)`, so raw-slice offsets
  do not survive into those files. Measured serialized-length delta equals occurrences × delta for all
  192 affected tasks under all 3 profiles: 0 mismatches; sums 4777 / 6744 / 5058 characters. All
  characters are ASCII, so codepoints == bytes in those artifacts.
- String-shape implications only, not resolution claims: `trailing_slash_sensitivity` yields a double
  slash at 110 token+path joins (`…/10303//<path>`) and a single trailing slash at 171 token-only
  values; `path_prefix` nests the 110 existing paths under `/prefix` and turns the 171 bare values
  into `…/10203/prefix`; `distinct_origins` yields `…/10103/<path>` with no trailing slash.

Ordering/no-cascade guard (SHOPPING is replacement 3 of 6): applying each profile's GITLAB then REDDIT
values first leaves the exact-token count at 281 (measured for all 3 profiles); those values contain
no `__SHOPPING__`; the SHOPPING replacement value contains none of the six `__…__` forms, so no later
token is introduced by it. SHOPPING-only substitution removes all 281 occurrences. Counts of the other
placeholder forms were unchanged by this substitution (guard measurement only; their populations are
other seats' scope and are not claimed here).

Boundary: projected totals/offsets above are **SHOPPING-only**, not the canonical six-token projection.
The canonical order additionally applies GITLAB and REDDIT before this token (shifting all offsets) and
SHOPPING_ADMIN, WIKIPEDIA, MAP after it (extra length/offset changes from their own occurrences); those
deltas are outside this seat's slice.

## Index vs task_id

All 812 items have distinct `task_id`; `index == task_id` holds for all 812 (observed) and for all 192
token-owning tasks (0 mismatches, both instruments). Upstream names per-task artifacts by `enumerate`
index, so on this frozen input the ordinal equals the task ID for this token's slice. No shuffled-ID
witness is claimed here; that experiment is the L1 selftest's scope.

## Independent oracle agreement

`/usr/bin/jq` = jq-1.8.2 (verified `--version`; earlier one bare `jq` resolution in this shell reported
jaq 3.1.1, so the absolute path is recorded). Independent jq results: items 812; token-bearing values
275; occurrences 281 via `match(...,"g")`; token-only values 171; token+path values 104; owning tasks
192; leaves by key 192/52/31; global `index != task_id` 0; affected `index != task_id` 0. Every value
equals the own-parser result. A `paths(strings)` count of all 10869 string values also matches the
parser's value-literal count (29009 total literals − 18140 keys).

Count-unit trap observed and recorded: `grep -c` = 275 is a **line** count; jaq's `scan`/`indices`
returned 275 (first match per string); `grep -o | wc -l` = 281; jq `match(...,"g")` = 281; a Python
`str.find` loop = 281. The occurrence unit is 281. Token-bearing lines are 275 of 29604 because five
leaves carry 2–3 occurrences on one line each.

## Artifacts and limits

Scratch (absolute, this seat only):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29TokenShopping-2/`
with `census_shopping.py`, `census_out.txt` (839 lines), `aggregates_shopping.py`, `aggregates_out.txt`,
`final_shopping.py`, `final_out.txt`, and `occurrences_shopping.csv` (281 data rows; columns include
JSON path, top-level index/task_id, key, value shape, leaf length, raw cp offset, decoded cp offset
within the leaf, occurrence ordinal, source line, and per-profile delta/projected cp). The CSV retains
per-occurrence provenance; the report above is the bounded digest.

No fixture or production file was modified; the raw SHA was the pinned value at every read. No
`config_files/*.json` output was created. The upstream generator and `browser_env.env_config` were
never imported or executed; the source was read as inert data. No network, browser profile, cookie,
credential, host-environment value or real endpoint was touched. Profiles are controlled synthetic
`*.invalid` fixtures, not deployment or model evidence. Other token populations and the canonical
six-token projection remain unmeasured by this seat. Adjacent guard observation, explicitly outside
this seat's scope and left to its owning seat/L1: the literal `__WIKIPEDIA__` occurs 0 times in the raw
file (`grep -c` and jq agree); no population conclusion is drawn here.

No installs or updates were performed (python3 3.14.8, jq 1.8.2, pi-uu-grep 0.2.0, gawk 5.4.1,
coreutils dd/wc used as present).

VERDICT: PASS
(Scoped to this single-token census and its three-profile length/span derivation only; not an
independent oracle's full projection check, not round admission, and no claim about the other five
tokens or scoring validity.)
