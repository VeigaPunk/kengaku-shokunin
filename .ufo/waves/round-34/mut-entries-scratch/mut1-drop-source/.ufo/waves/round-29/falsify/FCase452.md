writer: KengakuR29-2.FCase452-2

# FCase452 — raw task_id 452 under all three synthetic profiles

**Attack:** falsify the integrated projection record at `output_index` 452 by deriving it
independently from the prereg TEXT plus pinned bytes, then comparing field-by-field against
`python3 plans/config_projection.py --json`. Target: `projected_task`, `changed_leaves`
(pointer/category/tokens/original/projected), `output_filename`, `index_equals_task_id`,
`would_be_file_sha256`, and the occurrence-provenance rows for `task_index` 452.

**Production source read:** **no**. I did not read, import or grep `plans/config_projection.py`.
I read `plans/round-29-claims.md`, the pinned generator/raw/profiles bytes, the instrument's
stdout (`--summary`, `--json`, `--selftest`), and one `strace` syscall observation of it.

**Tool installs:** none. `strace` was already present at `/usr/bin/strace`; no pacman, no
network fetch, no language package install.

## Godspeed axes

| Axis | This item |
|------|-----------|
| A — derivation independence | Rebuild task 452 from text contract only; never see production code. |
| B — comparison breadth | Every emitted per-task field for 452 in all 3 profiles, plus its provenance rows. |
| C — discriminating power | Prefer checks a fake/naive projector would fail: hash of exact written bytes, `//` retention, key order. |
| D — unit separation | Keep occurrence (2), changed leaf (2), task (1), projection (3) denominators distinct. |
| E — scope honesty | States what 452 cannot discriminate (ASCII, index==task_id, no quote context). |

## Method (own oracle, reproducible)

Own script `/.ufo/waves/round-29/scratch/falsify/FCase452/oracle452.py`, output
`/.ufo/waves/round-29/scratch/falsify/FCase452/oracle452.out` (both under the lane scratch dir).
It implements the generator's literal semantics: decode pinned raw bytes as UTF-8, apply six
global text replacements in generator order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA,
MAP, `json.loads` the projected text, take element 452, re-serialise with
`json.dumps(item, indent=2)`, and diff the decoded leaves of raw element 452 against projected.

Commands and captured outputs:

```
python3 plans/config_projection.py --json > /tmp/fc452.json      # exit 0, 3881050 bytes
sha256sum /tmp/fc452.json
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630
python3 .ufo/waves/round-29/scratch/falsify/FCase452/oracle452.py /tmp/fc452.json "$PWD"
```

The capture digest equals `corpus/evidence/round29-calibration/build-json-sha256.txt`
(`c8da0c5a...4630`), so the compared stream is the delivered instrument output, not a local
variant. `--summary` exit 0, 47 lines; `--selftest` exit 0, `cases=20`; `--json` `findings` `[]`.

Pinned bytes I hashed myself (all equal the instrument's `inputs` map and `manifest.json`):

| Input | Bytes | sha256 |
|-------|-------|--------|
| `plans/fixtures/r29/manifest.json` | 1061 | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |
| `plans/fixtures/r29/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| `plans/fixtures/r29/profiles.json` | 1391 | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |

Generator facts I used, from the 838-byte file itself: line 11 `raw = raw.replace("__GITLAB__", GITLAB)`;
line 20 `json.loads(raw)`; line 21 `enumerate(data)`; line 22 filename template
`config_files/{idx}.json`; line 23 `json.dump(item, f, indent=2)`.

## Raw task 452 as pinned

Element 452 occupies codepoint span 416898..417799 (901 chars) of the raw text. Inside that
span: `__GITLAB__` appears exactly **2** times, at codepoint offsets **417052** and **417529**;
`__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`, `__last_url__`,
`__page__` each appear **0** times. The element has 17 leaves, 11 of them strings. No duplicate
object keys (`object_pairs_hook` scan). Every emitted `original` for its changed leaves starts
with its token.

## Field-by-field comparison (3 profiles × 7 record fields; 2 leaves × 6 subfields; 2 provenance rows × 6 fields)

| Profile | `start_url` projected | `eval.program_html[0].url` projected | file bytes | `would_be_file_sha256` (mine = instrument) |
|---------|----------------------|-------------------------------------|-----------|--------------------------------------------|
| `distinct_origins` | `http://gitlab.invalid:10101` | `http://gitlab.invalid:10101/byteblaze` | 871 | `3461e599e706bf2ef87c4585f83553d9c445c082f1a9ccd2921ef694fdefae69` |
| `path_prefix` | `http://gitlab.invalid:10201/prefix` | `http://gitlab.invalid:10201/prefix/byteblaze` | 885 | `00dc60fdf7efce4477be342d03a3b9a4782392376eea0891fca8da2c1d96a78d` |
| `trailing_slash_sensitivity` | `http://gitlab.invalid:10301/` | `http://gitlab.invalid:10301//byteblaze` | 873 | `2b77c0edce56ff4f0033ad22b38363919bedbedfb7b65deedb4a18d9faa0a2c3` |

`changed_leaves` agreed on all three profiles, exactly these two entries each:

| Pointer | `path_template` | `category` | `tokens` | `original` |
|---------|-----------------|-----------|----------|------------|
| `/452/start_url` | `start_url` | `url_field` | `["__GITLAB__"]` | `__GITLAB__` |
| `/452/eval/program_html/0/url` | `eval.program_html[].url` | `url_field` | `["__GITLAB__"]` | `__GITLAB__/byteblaze` |

Compared and equal in all three profiles: `output_index` 452; `output_filename`
`config_files/452.json`; `task_id` 452; `index_equals_task_id` true; `projected_task` deep-equal
to my independent object (17 leaves, key order included, see hash rows); `changed_leaves` pointer
set, `path_template`, `category`, `tokens`, `original`, `projected` per leaf; `would_be_file_sha256`.
Record key set is exactly `changed_leaves`, `index_equals_task_id`, `output_filename`,
`output_index`, `projected_task`, `task_id`, `would_be_file_sha256`, with no extra keys and none
missing. `occurrence_provenance` rows for `task_index`
452 are exactly two, with `json_pointer` `/452/start_url` at
`original_input_codepoint_offset` 417052 and `/452/eval/program_html/0/url` at 417529, both
`string_role` `value`, both token `__GITLAB__`, both `path_template` matching the leaf table —
equal to my span scan. Whole-projected-text digests also matched my independent text projection:
`2aec098e...707f4`, `54cf9833...74476`, `49bbee2e...3e01b2`.

Unchanged in 452 and confirmed unchanged in the emitted `projected_task`: `sites` `["gitlab"]`,
`storage_state` `./.auth/gitlab_state.json`, `intent` text, `instantiation_dict.url`
`byteblaze.github.io`, `required_contents.exact_match` `byteblaze.github.io`, `locator` (decoded text retains `[itemprop="url"]`), `eval_types`, `reference_answers` null, `reference_url` empty,
`intent_template_id` 331, `require_login` true, `require_reset` false, `geolocation` null.

**Mismatches: none.** 21 record-field comparisons + 36 leaf-field comparisons + 12 provenance-field
comparisons, all equal. No field of the 452 record differs from my derivation, including the two
values that a naive projector would corrupt: trailing-slash profile keeps `//byteblaze` (no
normalisation) and the leaf `original` keeps the raw token rather than a decoded placeholder.

Key-order sensitivity check: re-dumping the same object with `sort_keys=True` gives different
digests (`723528fe...1dfb`, `73eaa586...4568`, `e1133e00...a4bb`), so the matching unsorted
digests are evidence the emitted hash follows the raw element's key order (the order upstream
`json.dump` preserves), not merely equal values.

## Non-URL field change at 452

**None.** Both changed leaves are `category` `url_field`. The element's URL-shaped values that
live in fields not named `url` — `required_contents.exact_match` and `instantiation_dict.url`,
both `byteblaze.github.io` — contain no token and do not change. The `sites` array and the
`storage_state` path likewise contain no token.

Adjacent population observation (outside the 452 record; observed counts, then one inference).
Prereg F3 wording under test:

> "global replacement changes at least one non-URL-valued field"

- Observed: the only two `non_url_field` templates are
  `eval.program_html[].required_contents.must_include[]` (180 leaf rows = 60 leaves × 3 profiles)
  and `eval.reference_answer_raw_annotation` (3 rows = 1 leaf × 3).
- Observed: a census over all 4248 changed-leaf rows (1416 × 3) found every `original` string
  starts with its token, e.g. `__REDDIT__/f/space/134164/...`.
- `[INFERENCE]` The `non_url_field` class is therefore a *field-name* class, not a value-shape
  class: under a value-shape reading of the quoted F3 phrase (8 words), the number of
  changed non-URL-valued leaves is 0 in all 3 profiles, while the field-name reading gives 61.
  That is a wording risk in the claim, not a projection error, and it does not touch task 452.

## Multi-occurrence leaf at 452

**None.** Each of the two changed leaves carries one `__GITLAB__` occurrence; the two occurrences
occupy different leaves, so no collapse occurs. The 13 population-wide multi-occurrence leaves
(known from the instrument and reproduced by my own census) are at pointers `/66/eval/reference_answer_raw_annotation`,
`/431..435/start_url`, `/604`, `/608`, `/609`, `/625`, `/681`, `/682`, `/683` (`eval.reference_url`);
none is 452.

## Runtime hygiene observed (strace, read-only run)

`strace -f -e trace=openat,open,connect,socket,rename,unlink,mkdir python3 plans/config_projection.py --json`
opened the four pinned inputs, the `plans/` directory and the script's own file, every one
`O_RDONLY`; it made **0** `socket`/`connect` calls and **0** write-mode opens
(`O_WRONLY`/`O_RDWR`/`O_CREAT`). Its stdout digest equalled the earlier capture. No auth-state,
`.env` or `env_config` path was opened.

## Limits of this item (what 452 cannot falsify)

- The pinned raw text is pure ASCII (0 bytes >127) and CR-free (0 CR, 0 tab bytes), so codepoint
  and byte offsets coincide, `ensure_ascii` true/false are byte-identical, and text-mode newline
  translation is inert; the codepoint-offset and encoding clauses are labelled but not exercised.
- `index_equals_task_id` holds for all 812 frozen elements (raw list is 0..811 contiguous), so
  element 452 cannot distinguish enumerate-position output from `task_id`-keyed output; the
  shuffled witness lives in the hand fixtures, outside this item.
- Task 452 contains no quote, backslash or escaped-token context, so a text-level and a
  decoded-leaf oracle produce the same bytes here (I confirmed both: identical digests). This item
  therefore cannot discriminate those two oracle families; only their agreement on 452 is observed.
- The benchmark was never executed and no generator code was run; upstream I/O equivalence is
  argued from the pinned ASCII/CR-free bytes, not observed.

## Remaining unknowns

- `[INFERENCE]` Whether the non-benign, credential-bearing profile domain would preserve every
  property checked here; out of scope and untested.
- Whether the production implementation reaches these values by text substitution or by leaf
  rewriting is unobservable from outside and, per the two-oracle agreement on 452, immaterial for
  this element's emitted record.
- Longest double-quoted span in this report: 8 words (measured by script over backtick-stripped,
  code-fence-stripped text).

VERDICT: PASS
