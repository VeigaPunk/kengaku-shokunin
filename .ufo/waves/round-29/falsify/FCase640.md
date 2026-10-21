writer: KengakuR29-2.FCase640-2

# FCase640 — raw task_id 640 across all three frozen profiles

Scope: attacks claim C1 only at one task: the exact projected object and changed leaves for raw
task_id 640, compared field-by-field with the record at `output_index` 640 in every profile of
`plans/config_projection.py --json`.

Independence: I did **not** read or import `plans/config_projection.py`. My oracle was derived from
the prereg text (`plans/round-29-claims.md`, section "Frozen inputs and semantics"), the pinned
generator bytes, `profiles.json`, and the raw task file; it was compared against the instrument's
`--json` output only. I ran the instrument read-only.

Units: 1 raw task, 3 profiles, 3 task/profile projections. Counts below are per-task/profile or
explicitly labelled global; occurrences, changed leaves and tasks are never pooled.

## Method / commands (all run from lane root)

1. `python3 plans/config_projection.py --summary` → exit 0, `TOTAL findings=0 exit=0`,
   `POPULATION {"distinct_task_ids": 812, "input_task_count": 812, "profile_count": 3,
   "task_profile_projections": 2436, ...}`.
2. `python3 plans/config_projection.py --json > .ufo/waves/round-29/scratch/falsify/FCase640/instrument.json`
   → exit 0, 3,881,050 bytes.
3. Independent oracle `scratch/falsify/FCase640/oracle640.py`: read raw bytes once, apply the six
   text replacements in generator order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP,
   `json.loads` the projected text, take element 640, walk all leaves of raw element 640 against
   projected element 640, and separately serialise the projected object with the generator's
   per-index call (`json.dump(item, f, indent=2)`) to a `/tmp` file and hash the bytes.
4. `compare640.py` diffs each instrument record (fields below) against the oracle.

Raw facts observed: raw file 880,776 bytes, 880,776 codepoints, 0 non-ASCII bytes, 0 CR bytes,
812 tasks, task_id == index for all 812 positions; raw task 640 has task_id 640, 23 scalar leaves
of which 17 are strings, and exactly 2 `__REDDIT__` occurrences. Global occurrences: GITLAB 385,
REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133 (total 1435).

## Independent projection of task 640 (oracle result)

Only two leaves change, in every profile; both are URL-valued strings, each containing exactly one
token occurrence:

| pointer | original | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|---|
| `/640/start_url` | `__REDDIT__` | `http://reddit.invalid:10102` | `http://reddit.invalid:10202/prefix` | `http://reddit.invalid:10302/` |
| `/640/eval/reference_url` | `__REDDIT__/f/books` | `http://reddit.invalid:10102/f/books` | `http://reddit.invalid:10202/prefix/f/books` | `http://reddit.invalid:10302//f/books` |

Byte-level `would_be_file_sha256` (per-index file, generator call, no trailing newline):
- distinct_origins `903f8bc550f3aa18bf0a005cc4b96cc1a31c789675cb889e5e936b0a58b2330c` (1161 bytes)
- path_prefix `8e7a9a6b53ce93bd6a34cc5b33dbcf1057accc086d8d1be370f6cd107e3bb19c` (1175 bytes)
- trailing_slash_sensitivity `69be2e7ff2c65f6cbc4e2b4a7a305c3dc68540a561c6b2a026a4a5da1d13efed` (1163 bytes)

## Field-by-field comparison with instrument record at output_index 640

| field | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| `task_id` = oracle | 640 = 640 | 640 = 640 | 640 = 640 |
| `output_index` | 640 | 640 | 640 |
| `output_filename` = `config_files/640.json` | equal | equal | equal |
| `index_equals_task_id` | true (correct: raw element 640 has task_id 640) | true | true |
| `projected_task` deep-equal to oracle | yes | yes | yes |
| `would_be_file_sha256` = oracle byte hash | equal | equal | equal |
| `changed_leaves` set equal (pointer, category, tokens, original, projected) | yes, 2 = 2 | yes, 2 = 2 | yes, 2 = 2 |
| `changed_leaves[i].tokens` | `["__REDDIT__"]` | `["__REDDIT__"]` | `["__REDDIT__"]` |
| `changed_leaves[i].category` | `url_field` both | `url_field` both | `url_field` both |
| `changed_leaves[i].path_template` | `start_url`, `eval.reference_url` | same | same |

The instrument's two leaves are exactly the oracle's two leaves, with identical `original` and
`projected` strings — including the literal double slash `http://reddit.invalid:10302//f/books`,
i.e. no silent URL normalisation, escaping repair, or URL-only substitution at this task.

Context unchanged on both sides: `eval/program_html/0/url` is `func:reddit_get_post_url('__last_url__')`
and carries the non-env marker `__last_url__`; it is untouched, as are `storage_state`,
`intent`, `instantiation_dict.*`, `sites`, `eval/eval_types`, `eval/url_note`, `eval/reference_answers`
(null), `eval/program_html/0/locator` and the three `must_include` strings.

Ancillary checks that also agree: instrument `projected_text_sha256` for all three profiles equals
my whole-text hashes (2aec098e…, 54cf9833…, 49bbee2e…); instrument `raw_text_sha256` equals the raw
file SHA-256 `7b50386f…`; `manifest_sha256` equals `f6390b92…`. A global independent leaf census
reproduces 1416 changed leaves per profile with 1355 `url_field` / 61 `non_url_field`.

## Non-URL field changes and multi-occurrence leaves at task 640

- Non-URL field changes: **none**. Task 640's only changed leaves are `start_url` and
  `eval/reference_url`. So this task exercises no non-URL substitution path.
- Multi-occurrence leaves: **none**. Each changed leaf holds one occurrence of one token
  (`token_occurrences_in_leaf` = 1 for both). Task 640 is not among the 13 leaves with ≥2
  occurrences, which an independent census locates only at `/66/eval/reference_answer_raw_annotation`,
  `/431/start_url` (3), `/432/start_url`, `/433/start_url`, `/434/start_url`, `/435/start_url`,
  `/604/eval/reference_url` (3), `/608/eval/reference_url`, `/609/eval/reference_url` (3),
  `/625/eval/reference_url`, `/681/eval/reference_url` (3), `/682/eval/reference_url` (4),
  `/683/eval/reference_url`. This reproduces the instrument's `changed_leaves_with_multiple_occurrences=13`,
  and reconciles its per-token changed-leaf counts (REDDIT 323 = 336 occurrences − 13 extra
  occurrences; SHOPPING 275 = 281 − 6).
- Replacement order is inert for task 640 (its single token is `__REDDIT__`, and no profile value
  contains another token), so 640 cannot witness a wrong-order error; no later-token cascade occurs.

## Occurrence provenance at task 640

Provenance rows for `task_index` 640: offsets 636847 (`/640/start_url`) and 637436
(`/640/eval/reference_url`), both slicing exactly `__REDDIT__` from the original text (contexts
`"start_url": "__REDDIT__",` and `"reference_url": "__REDDIT__/f/books",`), both `string_role`
`value`. Globally the 1435 provenance rows are exactly the multiset of the 1435 raw-text
occurrences (0 missing, 0 extra), and 0 object keys contain any known token. Because the raw file is
pure ASCII (0 bytes ≥ 0x80), codepoint offsets coincide with byte offsets here, while the field is
still labelled as codepoints — correct terminology for the general case.

## Ancillary observations (not mismatches)

- `changed_leaves` order is original-text occurrence order (`start_url` at 636847 before
  `eval/reference_url` at 637436), not document order (the `eval` block precedes `start_url` in the
  raw JSON). The prereg pins no leaf ordering, so this is a presentation convention, not a violation.
- `index_equals_task_id: true` is correct here but **non-discriminating**: task_id equals array
  position for all 812 frozen items, so a confuse-index-with-task_id bug would also yield `true` and
  identical objects at 640. Only the shuffled-ID hand witness can discriminate; this task cannot.
- Instrument `source_contract` line numbers match the pinned generator verbatim: env_config star
  import line 5, six replace steps lines 11–16, `json.loads` line 20, `for idx, item in
  enumerate(data)` line 21, template `config_files/{idx}.json` line 22. Spot-quoted lines
  (word counts computed programmatically): `raw = raw.replace("__REDDIT__", REDDIT)` (4 words),
  `json.dump(item, f, indent=2)` (3), `config_files/{idx}.json` (1).

## Findings

No mismatch found between the oracle projection of raw task 640 and the instrument record at
output_index 640 in any of the three profiles: projected object, changed leaves (pointers,
categories, tokens, originals, projections), filename, index/task_id flag and would-be file hash all
agree, and the would-be hashes match byte-level files produced with the generator's own per-index
call. This item returns no evidence either way on the non-URL-change and multi-occurrence frontiers,
nor on index-vs-task_id mapping, which task 640 does not exercise.

Tool installs/upgrades: none (python3 stdlib only).

Remaining unknowns within this item: none about the 640 record; the index-vs-ID behaviour is
untested by 640 by construction (see above).

VERDICT: PASS
