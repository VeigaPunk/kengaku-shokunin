# R29 token census — `__GITLAB__` (single-token slice)

Seat: `KengakuR28.R29TokenGitlab-2`. Actual writer: `KengakuR28.R29TokenGitlab-2`.
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Read-only seat: only this report
and own scratch were written; no production edit, no config_files output, no fleet/lane state touch.

Scope: literal/decoded occurrence census and provenance for exactly one token, `__GITLAB__`,
in the pinned raw serialized text; raw-vs-decoded/escaped distinction; non-URL metadata slice;
replacement-length and Unicode-codepoint-span implications under the three frozen profiles.
Not a census of the other five placeholders, not a production-tool check, not an endpoint check.

## 1. Authenticated inputs (read once per run, bytes retained after hash check)

Command:
```
sha256sum plans/fixtures/r29/manifest.json plans/fixtures/r29/generate_test_data.py \
  plans/fixtures/r28/webarena/config_files/test.raw.json plans/fixtures/r29/profiles.json
wc -c plans/fixtures/r29/generate_test_data.py \
  plans/fixtures/r28/webarena/config_files/test.raw.json plans/fixtures/r29/profiles.json
```
Observed (all four match the task pins and `manifest.json` `files`):
```
f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87  plans/fixtures/r29/manifest.json
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  plans/fixtures/r29/generate_test_data.py   (838 bytes)
7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652  plans/fixtures/r28/webarena/config_files/test.raw.json   (880776 bytes)
90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018  plans/fixtures/r29/profiles.json   (1391 bytes)
```
Raw text decoded length: 880776 codepoints; UTF-8 byte length 880776; maximal byte value 125
(pure 7-bit ASCII). Therefore codepoint offsets and byte offsets coincide for this exact frozen
input, while every offset below is named a Unicode-codepoint offset, not a byte offset.

Pinned generator replacement line (quoted as inert data; programmatic word count
`len(line.split())` = 4, within the 25-word cap):
`raw = raw.replace("__GITLAB__", GITLAB)`.
It is the first of the six replacements in the pinned order GITLAB, REDDIT, SHOPPING,
SHOPPING_ADMIN, WIKIPEDIA, MAP; the pinned source is only read, never imported/executed.

Profiles (own-work synthetic, each value's declared purpose is the 8-word string
`controlled synthetic text-substitution profile, not an observed deployment`;
programmatic word counts: generator replacement line 4, purpose string 8):
| profile | `__GITLAB__` value | value codepoints | delta vs token (10) |
|---|---|---|---|
| distinct_origins | `http://gitlab.invalid:10101` | 27 | +17 |
| path_prefix | `http://gitlab.invalid:10201/prefix` | 34 | +24 |
| trailing_slash_sensitivity | `http://gitlab.invalid:10301/` | 28 | +18 |

Fixture integrity: `__GITLAB__` literal count is 1 in the pinned generator (as a source string),
0 in `profiles.json`, 0 in `manifest.json`; the three profile value sets contain no literal
`__GITLAB__`. This is a fixture-value check only; it is not a census of the other five tokens.

## 2. Method (independent, no upstream or production import)

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29TokenGitlab-2/census_gitlab.py`
(9963 bytes) does: one `open(...,'rb').read()`; sha256 check against the pin (exit2 on mismatch);
`decode('utf-8')`; a self-contained JSON scanner over that retained text that records, for every
string token, `(JSON-pointer path, key|value role, raw codepoint span, decoded value)`; the scan is
asserted to consume the whole text. Token occurrences are then counted twice: literal occurrences
inside each raw string slice, and occurrences inside each decoded value. `json.loads` of the same
retained text supplies the parsed structure for task/field attribution and projected parse checks.
No `browser_env`, `env_config`, host environment, credentials, network or production
`config_projection.py` is read, imported or run.

Run command and log (exit 0):
```
python3 .ufo/waves/round-29/scratch/KengakuR28.R29TokenGitlab-2/census_gitlab.py \
  > .ufo/waves/round-29/scratch/KengakuR28.R29TokenGitlab-2/census_run2.log 2>&1
```
Full per-occurrence table (385 rows): scratch `occurrences.json` (76147 bytes);
per-profile projected spans: scratch `projected_spans.json` (20837 bytes).

Independent cross-check script (separate implementation path, re-reads/re-hashes the raw file):
`.../scratch/KengakuR28.R29TokenGitlab-2/crosschecks.py` (4337 bytes), run as
```
python3 .ufo/waves/round-29/scratch/KengakuR28.R29TokenGitlab-2/crosschecks.py \
  > .ufo/waves/round-29/scratch/KengakuR28.R29TokenGitlab-2/crosschecks.log 2>&1   (exit 0)
```
It recomputes the recursive leaf-walk occurrence map, text-level nearest-key/`task_id`
attribution, token-only projection leaf diff with set equality and hashes, the `program_html`
entry-index distribution, and the unit arithmetic. A plain independent `grep` count gave the
same literal total:
```
grep -o '__GITLAB__' plans/fixtures/r28/webarena/config_files/test.raw.json | wc -l   -> 385
```

## 3. Census result — counts, not pooled units

| measurement | value | unit |
|---|---|---|
| raw serialized literal occurrences | 385 | occurrence |
| occurrences inside JSON string slices (scanner) | 385 | occurrence |
| occurrences inside decoded string leaves | 385 | occurrence |
| occurrence only after unescaping (`\u005f`-style form) | 0 | occurrence |
| occurrences in JSON object keys | 0 | occurrence |
| occurrences outside strings / structural text | 0 | occurrence |
| distinct string leaves holding a token | 385 | leaf (exactly 1 occurrence each) |
| distinct tasks holding >=1 token | 204 | task |
| parsed tasks / distinct task_ids | 812 / 812 | task |

Raw and decoded counts agree, and per-leaf raw count equals per-leaf decoded count for every leaf
(`escaped_only_leaves: []`), so on this frozen input there is no token that exists only in unescaped
form. Every token-bearing raw slice is ASCII with no backslash and no interior quote; every token
starts at decoded offset 0 of its leaf and is immediately preceded by the opening quote in the raw
text (`value_starts_with_token_count` = 385). Rendering-escape and decoded-escape forms therefore
cannot diverge here, but the measurement is reported per form rather than assumed.

Scanner fidelity: the hand scanner's `(pointer, decoded value)` list equals `json.loads`'s
recursive string-leaf walk exactly, 10869 of 10869 values (includes non-ASCII rendered as `\uXXXX`
escapes elsewhere in the file), so decoded values and spans are not an artifact of the scanner.

## 4. Provenance — owning tasks, fields, JSON paths

Field totals (occurrence counts; JSON Pointer paths shown as pattern):

| field path | occurrences | leaves | example pointer |
|---|---|---|---|
| `start_url` | 196 | 196 | `/44/start_url` |
| `eval.reference_url` | 49 | 49 | `/44/eval/reference_url` |
| `eval.program_html[i].url` | 132 | 132 | `/398/eval/program_html/2/url` |
| `eval.program_html[0].required_contents.must_include[1]` | 8 | 8 | `/681/eval/program_html/0/required_contents/must_include/1` |
| total | 385 | 385 | |

`program_html` URL occurrences are not confined to entry 0: index 0 → 103, 1 → 21, 2 → 6,
3 → 1, 4 → 1 (sum 132). Tasks with a token in `program_html` number 111; per-task distinct
token-bearing entries: 90 tasks one entry, 15 tasks two, 5 tasks three, 1 task five. The
`must_include` token is always in `program_html[0]` at list element index 1 (8/8).

Raw codepoint spans: first `[42249,42259)`, last `[880440,880450)`, median start
491770; spans are strictly increasing and non-overlapping. Per-field span extremes:
`start_url` first `[42249,42259)` last `[879919,879929)`;
`eval.reference_url` first `[42548,42558)` last `[877777,877787)`;
`eval.program_html.url` first `[353887,353897)` last `[880440,880450)`;
`must_include` first `[692104,692114)` last `[701228,701238)`.

Occurrence-per-task histogram (204 tasks, sums to 385): 1 occurrence → 52 tasks,
2 → 131 tasks, 3 → 15 tasks (`576, 577, 578, 736, 742–746, 752–756, 804`),
4 → 5 tasks (`747, 748, 749, 750, 751`), 6 → 1 task (`398`; 1 `start_url` plus 5
`program_html` entries, indices 0–4). Every row has `task_index == task_id` (812/812 parsed IDs are distinct
and equal their array index), so for this token set the enumerate-index output ordinal and the
item `task_id` coincide; that is an observed property of this frozen input, not a claim about
shuffled or future inputs.

Token-bearing tasks are exactly the tasks whose `sites` contains the slug `gitlab`
(set equality, 204 = 204). Site-list shapes: `('gitlab',)` 180, `('gitlab','reddit')` 10,
`('reddit','gitlab')` 8, `('gitlab','wikipedia')` 6.

Independent text-level attribution check (separate run, not the scanner): for all 385 spans,
the nearest preceding `"key":` in the raw text equals the last path component of the recorded
field, and the count of preceding `"task_id"` keys minus one equals the recorded task index;
mismatches 0/385.

### 4a. Raw-vs-decoded/escaped and non-URL metadata

- Raw-serialized literal occurrences: 385. Decoded-leaf occurrences: 385. Escaped-only
  occurrences: 0. Key occurrences: 0. No occurrence is outside a JSON string.
- Non-URL-field occurrences: 8, all in
  `eval.program_html[0].required_contents.must_include[1]`, tasks 681–688, each task in site list
  `('reddit','gitlab')`. Values (public fixture data) are URL-shaped relative GitLab paths, e.g.
  `__GITLAB__/eriklindernoren/PyTorch-GAN`, `__GITLAB__/byteblaze/cloud-to-butt`,
  `__GITLAB__/lahwaacz/arch-wiki-docs`. Structurally these are evaluation required-content
  predicates, not navigation-URL fields; treating them as scorer behavior would be runtime
  inference and is not observed here. Classification is by owning field role, not string shape:
  all 385 values are URL-shaped and begin with the token, but only the 377 in `start_url`,
  `eval.reference_url`, and `eval.program_html[].url` sit in navigation/reference URL fields.
- Zero occurrences in `intent`, `intent_template`, `intent_template_id`, `instantiation_dict`,
  `sites`, `storage_state`, `geolocation`, `require_login`, `require_reset`, `task_id`,
  `reference_answers`, `string_note`, or `eval.eval_types`. In particular no token-bearing leaf
  is an auth-state path, and the site slug `gitlab` is not the token, so site identity is not
  rewritten by this replacement.
- Shape of the text following the token within its leaf: whole leaf equals token 160 (all
  `start_url`), path-only suffix 205, query-bearing suffix 20 (`?scope=all&state=opened…`,
  `?label_name%5B%5D=…`); 151 distinct suffixes, 0 fragments.

## 5. Replacement-length and codepoint-span implications (three profiles)

Replacement count is profile-independent (385 occurrences, 385 leaves, 204 tasks) because only
value text differs. Projected results below are from a GITLAB-only substitution
`text.replace("__GITLAB__", profile_value)` on the retained text, used as a measurement, not as
the production six-token projection.

| profile | delta/occurrence | total codepoint delta | projected codepoints | projected sha256 | parsed tasks | remaining `__GITLAB__` |
|---|---|---|---|---|---|---|
| distinct_origins | +17 | 6545 | 887321 | `355c7f50f797725f49ab4d82798f46959358a78c0e35708a91ec4e6f9ebcca5b` | 812 | 0 |
| path_prefix | +24 | 9240 | 890016 | `e69744a772be7f1071618e4ba5dc4a3cfaea87b5a8a8562467137f74fdd98df3` | 812 | 0 |
| trailing_slash_sensitivity | +18 | 6930 | 887706 | `7ce45c9bea93096cbdd901611b8f5afb0a3f77afa23142056347e43dafc9ee65` | 812 | 0 |

Span mechanics: occurrences are ordered by raw start offset; occurrence `i` (0-based) maps to
projected span `[start_i + i*delta, start_i + i*delta + len(profile_value))`, with all `i < 385`.
First projected span is `[42249, 42249+len(value))` under every profile: `[42249,42276)` /
`[42249,42283)` / `[42249,42277)`. Last projected span starts at 886968 / 889656 / 887352.
All projected span sequences are strictly increasing. Literal identity is preserved: the token-only
leaf diff between raw and projected parse shows exactly 385 changed leaves under each profile, the
changed-leaf path set equals the 385 token-bearing leaf path set exactly (0 leaf paths added,
0 removed), all 812 `task_id` values preserved, 0 tasks added/removed. Projected token-leaf value lengths: distinct_origins min 27 / mean 47.63 / max 115;
path_prefix 34 / 54.63 / 122; trailing_slash 28 / 48.63 / 116; the 160 bare-token leaves become
exactly the profile value.

Per-field total codepoint deltas: distinct_origins — start_url 3332, program_html.url 2244,
reference_url 833, must_include 136; path_prefix — 4704 / 3168 / 1176 / 192;
trailing_slash — 3528 / 2376 / 882 / 144.

Unit accounting, not pooled: 385 occurrences per profile → 1155 replacement occurrences over the
three profiles; 385 changed leaves per profile → 1155 leaf changes; 204 affected tasks × 3
profiles = 612 affected task/profile projections of 2436 (25.123%). The other 1824
task/profile projections contain no `__GITLAB__` and are untouched by this token.

Wrong-substitution bounds (derived from the census, no implementation run): a `start_url`-only
rewrite replaces 196/385 occurrences and misses 189 (49.0909%); a URL-typed-fields-only rewrite
(`start_url` + `eval.reference_url` + `eval.program_html[].url`) replaces 377/385 and misses 8
(2.0779%), leaving the placeholder inside evaluation predicates. Since GITLAB is replaced first
and no profile value contains a known placeholder literal, no later-token replacement can create
a new `__GITLAB__`; a correct global serialized rewrite of this token leaves 0 occurrences in the
token-only substitution above.

## 6. Boundaries and unknowns (preserved, not resolved)

- This is a `__GITLAB__`-only slice. Counts, spans, and remaining-token statements for the other
  five placeholders were not censused, and no statement here implies all markers are resolved in
  the full projection.
- Projected offsets above are exact for GITLAB-only substitution of the raw text. In the full
  six-token projection each GITLAB span additionally shifts by the total length delta of every
  other-token occurrence positioned earlier in the text; that shift is outside this slice and
  remains unquantified here.
- Upstream per-task output (`json.dump(item, indent=2)` into `config_files/<idx>.json`) is source
  behavior read from the pinned 838-byte generator; no per-task file was created, so re-serialized
  per-task byte layout and any escaping introduced by that dump are unmeasured.
- Evaluation-predicate consumption, scorer outcomes, browser/helper behavior and endpoint
  reachability are not observed. All profile strings are synthetic `*.invalid` fixtures, not
  deployment or runtime evidence. No endpoint, site, browser profile, cookie or credential was
  accessed.
- Production `plans/config_projection.py` behavior was not exercised by this seat; agreement with
  this independent census is for L1 to compare. One run reads the raw file once and retains the
  verified bytes; later independent cross-check runs each re-read and re-hash separately.

## 7. Cross-check summary

| check | result |
|---|---|
| sha256 of raw fixture vs pin | match |
| literal count via `grep -o` vs scanner vs bytes.count vs str.count | 385 / 385 / 385 / 385 |
| decoded leaf occurrence total vs raw literal total | 385 / 385 |
| per-leaf raw vs decoded multiplicity mismatches | 0 |
| scanner decoded values vs `json.loads` walk | 10869/10869 equal |
| independent nearest-key and preceding-`task_id` attribution | 0/385 mismatches |
| independent recursive leaf-pointer count map vs scanner map | identical, 385 leaves |
| token-only projection parses to 812 tasks under 3 profiles | yes, IDs preserved |

## Verdict

VERDICT: PASS

Scoped verdict, this seat only: the `__GITLAB__` census is reproducible from the pinned bytes —
385 raw serialized literal occurrences in 385 distinct leaves across 204 of 812 tasks, 0 escaped-only
or key occurrences, 377 URL-field plus 8 evaluation-predicate occurrences, with profile deltas
+17/+24/+18 and per-profile projected codepoints 887321/890016/887706. No round admission, no
canonical knowledge write, and no claim about the other five tokens, runtime behavior or production
tool correctness is made here.
