writer: KengakuR29-2.FReviewHandFixtures-2

# FReviewHandFixtures — review of adopted hand fixtures `plans/fixtures/r29/hand/`

Scope: byte equality with build-seat scratch, authorship vs the seats' `build/` reports, whether the
expected values were hand-derived rather than produced by the production code, and whether the
selftest consumes them unchanged. Scoped to this item only; not a round admission.

**Reviewed bytes.** The integrated state under attack is lane master `56fd949a6478342531e61f4feecb4a685d831640`,
whose `plans/config_projection.py` is sha256 `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`
— the same digest recorded in `.ufo/waves/round-29/candidate-freeze-v1.json` and in
`corpus/evidence/round29-calibration/mutation-witness.txt`. Every line number, digest and
experiment below is against those frozen bytes, extracted to `/tmp/lm29` with `git show`.

During the review the working tree's `plans/config_projection.py` was modified by another agent
(observed digests `3530cd28…`, `a91f3943…`, `c6f84aee…`, `e88471ca…`; `git status` shows it
uncommitted, ` M plans/config_projection.py`). That edit adds built-in hand witnesses
(`INDEX_WITNESS_RAW`, `ORDER_WITNESS_RAW`, `ORDER_WITNESS_VALUES` at lines 57–59) and a
`witnesses()` function, renames `index_mapping["violations"]` to `index_task_id_mismatches`, and
grows the selftest from 20 to 27 cases. I re-verified every finding against those bytes too; the
result is in the "Concurrent working-tree edit" section below. The frozen lane master is the
scoped verdict basis.

I read the production source for this item (explicitly permitted by the assignment) and I ran the
instrument read-only. My own re-derivation of the expectations was done from the pinned generator
bytes and the pinned raw data, not from `plans/config_projection.py`; the instrument's `--json` /
`--summary` / `--selftest` output was used only for comparison. All experiments that mutate
anything ran on copies under `/tmp/`.

## Attack

For each of the four adopted fixture files: (1) compare bytes to the build-seat scratch original
and to the `build/` report's stated hash; (2) check the fixture's own authorship field against the
seat that actually wrote it; (3) re-derive every declared expected value from the pinned generator
source and the pinned inputs; (4) instrument the selftest to record which fixture keys it actually
reads, and mutate the production `project()` to see which hand block is load-bearing.

## 1. Byte equality with build-seat scratch — CONFIRMED

All four adopted files are byte-identical to their build-seat scratch originals, both on disk
(`cmp`, byte-identical) and in the Git index (same blob id).

```
$ sha256sum plans/fixtures/r29/hand/* .ufo/waves/round-29/scratch/R29MutOrder-2/cascade-order.case.json \
    .ufo/waves/round-29/scratch/R29MutUrlOnly-2/fixture.json .ufo/waves/round-29/scratch/R29MutUrlOnly-2/expected.json \
    .ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/index-shuffled-ids.fixture.json
4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3  plans/fixtures/r29/hand/cascade-order.case.json
4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3  .../R29MutOrder-2/cascade-order.case.json
938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254  plans/fixtures/r29/hand/index-shuffled-ids.fixture.json
938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254  .../KengakuR28.R29MutIndex-2/index-shuffled-ids.fixture.json
e68e7a0dd8719b85a8db143748989a36dbc955a23b67209b8d76add720f1f5e5  plans/fixtures/r29/hand/url-only.expected.json
e68e7a0dd8719b85a8db143748989a36dbc955a23b67209b8d76add720f1f5e5  .../R29MutUrlOnly-2/expected.json
2c78b19909c0c9b4b601f500301d1036c7e00d31454594ec4435c7d28407055e  plans/fixtures/r29/hand/url-only.fixture.json
2c78b19909c0c9b4b601f500301d1036c7e00d31454594ec4435c7d28407055e  .../R29MutUrlOnly-2/fixture.json
```

`cmp` reported no difference for every pair. Git blob ids also match: `cascade-order.case.json` =
`e686ef91…`, `url-only.fixture.json` = `73681808…` (= scratch `fixture.json`),
`url-only.expected.json` = `d431022a…` (= scratch `expected.json`),
`index-shuffled-ids.fixture.json` = `67903f9c…`.

These four hashes also appear in the build-seat reports: `build/R29MutOrder.md:137`,
`build/R29MutIndex.md:109`, `build/R29MutUrlOnly.md:93-94`. Each hash value matches the adopted
file exactly.

## 2. Authorship — CONFIRMED, with one naming inconsistency

| adopted file | fixture's own field | build report line 3 | match |
|---|---|---|---|
| `cascade-order.case.json` | `"author": "KengakuR28.R29MutOrder-2"` | `build/R29MutOrder.md:3` "Seat / actual writer: `KengakuR28.R29MutOrder-2`" | yes |
| `index-shuffled-ids.fixture.json` | `"writer": "KengakuR28.R29MutIndex-2"` | `build/R29MutIndex.md:3` "Seat and actual writer: `KengakuR28.R29MutIndex-2`" | yes |
| `url-only.fixture.json` / `url-only.expected.json` | (no authorship field at all) | `build/R29MutUrlOnly.md:3` "Seat: R29MutUrlOnly. Actual writer: KengakuR28.R29MutUrlOnly-2" | unattributed in the file itself |

Observation (not a defect against the contract): the url-only pair carries no writer field. The
authorship is recoverable from `build/R29MutUrlOnly.md:3` and from the scratch path
`…/scratch/R29MutUrlOnly-2/`, so provenance is not ambiguous; it is just not self-describing in the
bytes, unlike the other two files.

Observation: the three scratch directories are named inconsistently —
`R29MutOrder-2`, `R29MutUrlOnly-2`, `KengakuR28.R29MutIndex-2` — while all three reports name the
same agent-id prefix `KengakuR28.`. The coordinator's task context likewise says "build-seat scratch
R29MutOrder-2, R29MutUrlOnly-2, R29MutIndex-2", but the third directory is actually
`KengakuR28.R29MutIndex-2`. Directory naming only; the file bytes and the `writer` field are correct.

## 3. Were the expected values hand-derived rather than produced by the production code? — YES

I re-derived every declared expectation from the pinned generator bytes
(`plans/fixtures/r29/generate_test_data.py`, sha256 `45ddba7b…`) applied to the fixture's own input
text with the fixture's own values, using the source order GITLAB, REDDIT, SHOPPING,
SHOPPING_ADMIN, WIKIPEDIA, MAP. Every field matched:

- `cascade-order.case.json`: `expected_projected_text` match; all six `expected_after_each_source_step[i].text`
  match; all six `expected_dynamic_replacement_hits_by_source_step` = 1 match;
  `expected_parsed_value` match; `expected_original_occurrences_by_name` = {GITLAB: 1, rest 0} match;
  `expected_remaining_known_token_occurrences` = 0 match;
  `expected_original_known_token_occurrences` = 1 match; `expected_task_count` = 1 match;
  `expected_changed_string_leaf_count` = 1 match;
  `predicted_mapping_order_mutant_text` match; `predicted_simultaneous_mutant_text` match.
- `url-only.expected.json`: `projection` match; `changed_string_leaf_paths` =
  `["$[0].eval.reference_answer_raw_annotation", "$[0].intent", "$[0].start_url"]` match;
  `raw_replacement_occurrences_by_token` {__REDDIT__: 4, rest 0} match;
  `remaining_known_environment_token_occurrences` = 0 match; `input_task_count` = 1 match;
  `changed_task_count` = 1 match; `task_profile_projection_count` = 1 match.
- `index-shuffled-ids.fixture.json`: `expected_projected_raw_text` match; `expected_records` match on
  all four fields of both records (task_id, output_ordinal, output_filename, projected_task);
  `expected_index_equals_task_id` = [false, false] match; `expected_filename_to_task_id` match;
  `expected_input_task_ids` = [1, 0] match; `expected_output_ordinals` = [0, 1] match;
  `expected_counts` match.

Corroborating evidence that the values were not produced by the production code:

- The fixture inputs are not the production input. `url-only.fixture.json` is a *reduced* task-66
  analogue, not the pinned task 66. Real task 66 (from
  `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 66) has 12 top-level keys
  (`sites, task_id, require_login, storage_state, start_url, geolocation, intent_template,
  instantiation_dict, intent, require_reset, eval, intent_template_id`); the fixture has 5
  (`task_id, start_url, intent, eval, fixture_markers`). Real `intent` is
  `"Among the top 10 post in \"books\" forum, …"`; the fixture substitutes
  `"Literal __REDDIT__ is task text, not a URL-valued leaf."`. Real `eval` has 6 keys including
  `string_note`; the fixture's `eval` has 5 and omits `string_note`. The fixture adds
  `fixture_markers: "__last_url__ __page__"`, which is not in real task 66. Real task 66 carries 3
  `__REDDIT__` occurrences inside its own leaves; the fixture carries 4 (the extra one is in the
  synthetic `intent`). The `scope` field and the `fixture_provenance` field of
  `scratch/R29MutUrlOnly-2/mutant-spec.json` both disclose exactly this ("Replaces intent with
  explicit synthetic non-URL token-bearing text; adds fixture_markers; omits other raw fields.
  This is not an exact task66 copy or benchmark validity observation."), so the divergence is
  declared, not concealed. The fixture's own `scope` string also says so.
- `build/R29MutOrder.md:5` and `build/R29MutIndex.md:3` both state no production implementation was
  read, mutated, or executed, and both mark their mutant status `DESIGN_ONLY_NOT_EXECUTED` /
  `NOT RUN`. `build/R29MutUrlOnly.md:8` states it is "not a mutation of the production instrument,
  an independent oracle, a fresh-seat falsifier, or round admission"; its own-work experiment ran
  against its own scratch `candidate.py` (`scratch/R29MutUrlOnly-2/candidate.py`, sha256
  `268de37d…`), a separate implementation from `plans/config_projection.py`.
- Timing corroborates: the three fixture scratch files are mtime 2026-10-21 13:05–13:07, while
  `plans/config_projection.py` is mtime 2026-10-21 13:34:56. The expectations existed before the
  production code was written.

## 4. Does the selftest consume the fixtures unchanged? — YES for the values it reads; two gaps

`plans/config_projection.py:436,444,445,453` read the four files verbatim via
`json.loads((root / HAND / "<name>").read_text())` and assert against the parsed values. No
normalisation, no re-derivation, no rewriting of the fixtures. The instrument never writes to
`plans/fixtures/r29/hand/`.

I instrumented `json.loads` to record every key access on the four fixture dicts during a real
`--selftest` run. The keys the production code actually reads are:

- `cascade-order.case.json` → `case_id, mapping_insertion_order, values, raw_serialized_text,
  expected_projected_text, expected_dynamic_replacement_hits_by_source_step,
  predicted_mapping_order_mutant_text`
- `url-only.fixture.json` → `case_id, replacement_order, values, raw_text`
- `url-only.expected.json` → `projection, raw_replacement_occurrences_by_token,
  changed_string_leaf_paths`
- `index-shuffled-ids.fixture.json` → `case_id, replacement_order, profile_values, input_raw_text,
  expected_index_equals_task_id, expected_records`

**Finding 1 (low, factual): 30 of the 52 declared expectation keys are never read by the
selftest.** Specifically never read: `cascade-order.case.json` → `author, status, purpose,
source_order, expected_after_each_source_step, expected_parsed_value,
expected_original_known_token_occurrences, expected_original_occurrences_by_name,
expected_remaining_known_token_occurrences, expected_task_count, expected_changed_string_leaf_count,
predicted_simultaneous_mutant_text, predictions_are_observations`; `url-only.fixture.json` → `scope,
profile_id, profile_purpose`; `url-only.expected.json` → `input_task_count, profile_count,
task_profile_projection_count, changed_task_count, remaining_known_environment_token_occurrences,
expected_mutant`; `index-shuffled-ids.fixture.json` → `writer, kind, scope, profile_name,
expected_projected_raw_text, expected_counts, expected_input_task_ids, expected_output_ordinals,
expected_filename_to_task_id, output_interpretation`.

I confirmed this is inert, not merely unreferenced: editing any of these keys to a wrong value
leaves the selftest at exit 0 with the same 20 clean cases. Examples, each run on a `/tmp` copy:
`cascade-order.case.json.expected_after_each_source_step[3].text = "GARBAGE"` → exit 0;
`index-shuffled-ids.fixture.json.expected_filename_to_task_id = {"config_files/0.json": 99, …}` →
exit 0; `index-shuffled-ids.fixture.json.expected_counts = {"input_tasks": 777, …}` → exit 0;
`url-only.expected.json.expected_mutant.detector_exit = 0` and
`remaining_known_environment_token_occurrences = 42` → exit 0;
`cascade-order.case.json.author = "KengakuR29-2"` → exit 0.

This is not a correctness defect: the unread fields are extra hand material, and I independently
verified all of them are correct (section 3). It is a scope-observation: the selftest is a
*partial* consumer of the hand fixtures, so a reader must not assume the whole fixture is asserted.

**Finding 2 (medium): the url-only fixture's changed-leaf path convention is reconstructed by
string surgery on a JSON pointer, not taken from the instrument's own `path_template` field, and
the reconstruction is not equivalent for list-nested paths.**

`plans/config_projection.py:449` compares

```
sorted("$[%d]%s" % (int(l["json_pointer"].split("/")[1]),
                     "".join("." + p for p in l["json_pointer"].split("/")[2:]))
        for t in record["tasks"] for l in t["changed_leaves"])
   == url_expected["changed_string_leaf_paths"]
```

The production code already computes a per-leaf `path_template` field (line 336,
`"path_template": template(path)`), but line 449 does not use it; it re-derives a path string from
the RFC-6901 pointer by splitting on `/` and re-joining with `.`. For the fixture's actual leaves
the two happen to coincide, so the assertion passes. For a list-nested leaf they do not. Measured
on a `/tmp` probe with a task containing `eval.program_html[0].url`:

```
json_pointer           : /0/eval/program_html/0/url
line-449 reconstruction: $[0].eval.program_html.0.url     <- what is compared
production path_template: eval.program_html[].url          <- the instrument's own field
```

The seat's own detector (`scratch/R29MutUrlOnly-2/detector.py`, `string_leaves`) uses a third
convention, `$[0].eval.program_html[0].url`. The fixture's `changed_string_leaf_paths` uses the
seat convention, which is why the current fixture passes: its three changed leaves are all
non-nested. Consequence: the assertion is a coincidence of the current fixture's shape, and any
future hand case with a list-nested changed leaf will compare a production-internal reconstruction
against a seat-convention string and mismatch for reasons unrelated to the projection. The
`path_template` field at line 336 is the value that would match the fixture's convention family
for non-nested paths and needs a defined convention for nested ones.

**Finding 3 (low): the `url-only.expected.json` file mixes an expectation set with a mutant
expectation that the selftest never applies.** Its `expected_mutant` block
(`{changed_string_leaf_paths: ["$[0].start_url"], remaining_known_environment_token_occurrences: 3,
mismatch_paths: […], detector_exit: 1}`) describes the seat's own scratch detector's expectation
for its own scratch candidate, per `scratch/R29MutUrlOnly-2/mutant-spec.json`. The production
selftest never reads it (confirmed by the key-access trace) and never runs a mutant. The block is
correct and truthful as scratch-scoped evidence, but inside a file named `url-only.expected.json`
under the production fixture directory it reads as a production expectation. I verified the values
are right for the seat's mutant: with the seat's exact `replace_url_fields` semantics applied to
`plans/config_projection.py`, the mutated run leaves 3 `__REDDIT__` occurrences and changes only
`$[0].start_url`, matching the recorded `expected_mutant`.

## 5. Load-bearingness: which hand block actually catches a mutant

I mutated the production `project()` (on `/tmp` copies only) and neutralised each hand block in
turn by replacing its `assert` statements with `pass`, then observed which assertion failed.

| mutant (production `project()`) | all hand blocks present | cascade neutralised | url-only neutralised | index neutralised |
|---|---|---|---|---|
| iterate `values` (mapping order) instead of `ORDER` | killed, line 438 (cascade assert) | **survives, exit 0** | killed, line 438 | killed, line 438 |
| `output_filename` keyed by `task_id` | killed, line 456 (index assert) | killed, line 456 | killed, line 456 | **survives, exit 0** |
| URL-fields-only substitution (seat-exact `replace_url_fields` semantics) | killed, line 408 (inline case `six_tokens_and_non_url_field`) | killed, line 408 | killed, line 408 | killed, line 408 |
| `eval` subtree left unprojected | killed, line 447 (url-only assert) | killed, line 447 | **survives, exit 0** | killed, line 447 |
| non-env markers `__last_url__`/`__page__` also rewritten | killed, line 447 (url-only assert) | killed, line 447 | killed, line 517 | killed, line 447 |

Reading of that table:

- The **cascade** hand block is the sole killer of the mapping-order mutant. Without it that
  mutant survives the entire selftest.
- The **index** hand block is the sole killer of the `task_id`-keyed-filename mutant.
- The **url-only** hand block is the sole killer of the "eval subtree left unprojected" mutant.
- The **URL-fields-only** mutant (the seat's own designed defect) is *not* caught by the url-only
  hand block; it is caught earlier by the inline case at line 408
  (`assert not findings and [s["applied_replacements"] for s in record["steps"]] == [2] * 6`).
  This is consistent with the coordinator's own note that the fixture's job is the unread-metadata
  path, but it means the url-only hand fixture does not by itself demonstrate the URL-only
  substitution defect; the inline case does.

**Finding 4 (medium, receipt-vs-reality): the build receipt `mutation-witness.txt` attributes the
reversed-order kill to a mechanism that does not exist, and the recorded mutant identity does not
match the seat's designed mutant.**

`corpus/evidence/round29-calibration/mutation-witness.txt` reads:

```
control sha256 5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3
control selftest exit 0 SELFTEST clean cases=20 six_tokens_and_non_url_field,units_n
wrong_order_reversed selftest exit 1 killed AssertionError | summary ['TOTAL findings=0 exit=0']
url_only_substitution selftest exit 1 killed AssertionError | summary ['TOTAL findings=6 exit=1']
index_by_task_id selftest exit 1 killed AssertionError | summary ['TOTAL findings=0 exit=0']
```

I reproduced all three kills and their `--summary` totals exactly (reversed → `TOTAL findings=0
exit=0`; url-only → `TOTAL findings=6 exit=1`; filename-by-task_id → `TOTAL findings=0 exit=0`), and
the control sha256 matches the current `plans/config_projection.py` byte-for-byte
(`sha256sum` → `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`). The receipt is
honest about outcomes.

The defect is in what the receipt leaves unstated, given that the same wave also produced the
cascade hand fixture and the draft that leans on it:

(a) The receipt's `wrong_order_reversed` kill is **not** the cascade hand case's kill. A true
reversal of `ORDER` is killed at line 416 by the inline `escaped_token_not_replaced` case
(`assert record["steps"][0]["applied_replacements"] == 1 and
record["remaining_known_tokens_text"]["__GITLAB__"] == 0`), i.e. before the cascade block at
lines 436–443 is reached. Neutralising the cascade block does not un-kill a reversed-order mutant.
The mutant the cascade fixture is actually load-bearing against is *mapping-insertion-order*
iteration (`for name in values:`), which is the defect `build/R29MutOrder.md` specifies
("R29_M_ORDER_01 … change only the serialized replacement-loop iterator from source order to
profile-mapping iteration order") and the same defect
`scratch/R29MutOrder-2/mutant-spec.json` names. The receipt records a different mutant under the
name `wrong_order_reversed`, and records no mutant for the mapping-order defect that the cascade
fixture exists to catch. The `--summary` totals cannot distinguish the two (both are
`TOTAL findings=0 exit=0`, because the frozen profiles' values contain no tokens, so order is
invisible on real data — the draft says this explicitly).

(b) The receipt's `url_only_substitution` kill is also **not** attributable to the url-only hand
block; that mutant is killed at line 408 by the inline `six_tokens_and_non_url_field` case, as
shown in the table above.

(c) The receipt records no mutant for the index-by-task_id kill's dependency: the index hand
block is the *sole* killer of that defect, and the receipt does not say so.

**Finding 5 (medium, reproducibility): the hand fixtures are not covered by any persisted
integrity pin, so a tampered fixture can launder a mutant on the frozen lane master.**

The manifest `plans/fixtures/r29/manifest.json` pins exactly three files, and
`plans/config_projection.py:105` enforces that exact file set:

```
if sorted(manifest["files"]) != sorted([GENERATOR, RAW, PROFILES]) or tuple(manifest["replacement_order"]) != ORDER:
```

Adding the hand directory to the manifest is therefore *rejected*, not merely absent: I copied the
lane master to `/tmp`, added `plans/fixtures/r29/hand/index-shuffled-ids.fixture.json` to
`manifest["files"]` with its correct sha256, and the instrument returned
`{"findings":[{"id":"manifest_tampered"}]}` with exit 2. The hand fixtures are read at lines
436/444/445/453 with no digest check at all, and no receipt under `corpus/evidence/` records their
digests (I grepped `corpus/` for all four hashes: no hit).

Consequence, demonstrated on a `/tmp` copy of the frozen lane master: editing
`index-shuffled-ids.fixture.json`'s `expected_records[*].output_filename` to the mutant's
task-id-keyed names and running the filename-by-task_id mutant gives **selftest exit 0, "SELFTEST
clean cases=20 …"** — the mutant is laundered by editing the fixture instead of the code. The
tamper alone (no mutant) is correctly caught at the fixture assert; the laundering requires both
edits. The same tamper leaves `--json` byte-identical (sha256
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, matching
`build-json-sha256.txt`), because `--json` never reads the hand directory.

This does not affect the claim's measurements: the `--json`/`--summary` population of 812 × 3 =
2436 does not depend on the hand fixtures at all. It affects the *test* claim only — the
independence of the hand-case oracle rests on file bytes that nothing in the shipped artifact
authenticates. A one-line change to `plans/config_projection.py:105` (extend the allowed manifest
file set and the `read_pinned` loop) plus adding the four fixture digests to
`plans/fixtures/r29/manifest.json` would close it; the manifest sha256 already persisted in
`config_projection.py:26` would need updating, and that is the lane owner's call, not mine.

**Finding 6 (low): a missing hand fixture is an uncaught exception with exit 1, not a
could-not-evaluate exit 2.** Deleting `plans/fixtures/r29/hand/url-only.fixture.json` on a `/tmp`
copy and running `--selftest` gives an uncaught `FileNotFoundError` traceback and exit 1. The
preregistered exit contract is 0 = audit ok, 1 = projection/invariant finding, 2 = could-not-evaluate
including missing input. A missing *input* here exits 1, which is the "finding" code, not the
"could-not-evaluate" code. The same applies to a corrupt (non-JSON) fixture file. This is
consistent with the pre-existing `input_missing` handling for the three manifest-pinned inputs
(lines 108, 118), which correctly raises `Unevaluable("input_missing")` → exit 2; the hand
directory has no equivalent handling because it is outside `read_pinned`.

**Finding 7 (informational): the selftest's hand-fixture path is not root-relative-safe in the
same way as the pinned inputs.** `HAND` (line 28) is a relative path joined to `--root`, so the
fixtures follow `--root` correctly (I verified the whole `/tmp` copy tree with `--root
/tmp/r29hf/lane`). No defect.

## Concrete defects, ranked

1. **Finding 5** — hand fixtures unauthenticated; a fixture edit launders the `task_id`-filename
   mutant to a clean selftest (exit 0, 20 clean cases). Locations: `config_projection.py:28, 105,
   436, 444, 445, 453`; `plans/fixtures/r29/manifest.json` (no `hand/` entries);
   `corpus/evidence/round29-calibration/` (no fixture digests). Manifest cannot accept the hand
   files today: `manifest_tampered` exit 2 on a `/tmp` copy that adds one.
2. **Finding 4** — `mutation-witness.txt` records `wrong_order_reversed` and `url_only_substitution`
   kills that are attributable to inline selftest cases (lines 416 and 408), not to the cascade
   (436–443) and url-only (444–452) hand blocks; and it records no mutant for the
   mapping-insertion-order defect that the cascade hand fixture is the *sole* killer of. The
   recorded `--summary` totals cannot distinguish the two order defects (both
   `TOTAL findings=0 exit=0`).
3. **Finding 2** — `config_projection.py:449` reconstructs changed-leaf paths by splitting the
   JSON pointer on `/` instead of using the instrument's own `path_template` field (line 336);
   the reconstruction diverges from both the production `path_template` and the seat's
   `detector.py` convention for list-nested paths (`$[0].eval.program_html.0.url` vs
   `eval.program_html[].url` vs `$[0].eval.program_html[0].url`). Currently masked because the
   fixture's three changed leaves are all non-nested.
4. **Finding 6** — missing or corrupt hand fixture → uncaught exception, exit 1, instead of the
   preregistered exit 2 for a missing input (`config_projection.py:436/444/445/453`).
5. **Finding 3** — `url-only.expected.json` carries a scratch-scoped `expected_mutant` block
   inside a production fixture file; the production selftest never reads it.
6. **Finding 1** — 30 of 52 declared expectation keys are never read by the selftest (all
   verified individually correct by independent re-derivation, so inert, not wrong).
7. Naming inconsistencies: url-only scratch `fixture.json`/`expected.json` were renamed on
   adoption to `url-only.fixture.json`/`url-only.expected.json`; the three scratch directory
   names use two different prefixes; the url-only pair has no in-file writer field.

## Concurrent working-tree edit (not the frozen lane master)

Another agent modified `plans/config_projection.py` in the working tree while I was reviewing;
`git status` shows it uncommitted (` M plans/config_projection.py`) and I observed four successive
digests: `3530cd28…`, `a91f3943…`, `c6f84aee…`, `e88471ca…`. The lane master digest
`5673405e…` is what `candidate-freeze-v1.json` and `mutation-witness.txt` record, so the frozen
state is the scoped basis. I nevertheless re-verified each finding against the last working-tree
bytes I could read (`e88471ca…`).

What the concurrent edit does, and its effect on my findings:

- It adds built-in hand witnesses `INDEX_WITNESS_RAW`, `ORDER_WITNESS_RAW`, `ORDER_WITNESS_VALUES`
  (lines 57–59) and a `witnesses()` function (lines 383–391). I verified the claim in the source
  comment "raw text byte-equal to the adopted seat-authored fixtures" is true:
  `INDEX_WITNESS_RAW == index-shuffled-ids.fixture.json["input_raw_text"]` → True;
  `ORDER_WITNESS_RAW == cascade-order.case.json["raw_serialized_text"]` → True;
  `ORDER_WITNESS_VALUES == cascade-order.case.json["values"]` → True.
- It renames `index_mapping["violations"]` to `index_task_id_mismatches` (line 379) but leaves the
  consumer at old line 420 and the selftest consumer updated — on the intermediate bytes
  `a91f3943…` this left `--summary` crashing with `KeyError: 'index_equals_task_id'` and
  `--selftest` crashing with `KeyError: 'violations'` at line 505. That was a transient mid-edit
  state, since fixed in the later bytes; I am recording it only because it is the observed
  behavior of one of the digests in flight, not as a defect in the frozen lane master.
- **Finding 5 is materially weakened on the new bytes.** The new line 517
  (`assert built_in["index"]["records"] == [{"output_filename": "config_files/0.json", "task_id": 1, …}]`)
  compares against a *hardcoded literal in the instrument*, not against the fixture. I confirmed
  that with the fixture tampered to the mutant's names, the filename-by-task_id mutant is now
  killed at that built-in assert instead of surviving. So the new bytes no longer let a fixture
  edit launder that mutant. The hand fixtures are still outside the manifest pin and still have
  no receipt digest; the difference is that the instrument now carries its own second, pinned copy
  of the same expectation.
- **Finding 1 (unread keys inert) and Finding 2 (path reconstruction) persist unchanged.** On the
  new bytes the path-reconstruction assert is at line 507 and still splits `json_pointer` on
  `"/"`; a corrupted `expected_filename_to_task_id` or `expected_after_each_source_step[3].text`
  still leaves the selftest at exit 0.
- **Finding 6 (missing hand fixture → exit 1) persists**: deleting
  `plans/fixtures/r29/hand/url-only.fixture.json` still yields an uncaught `FileNotFoundError` and
  exit 1, not the preregistered exit 2 for a missing input.
- The concurrent edit also adds a `categories` assert (new line 511) checking
  `url_field` / `non_url_field` per changed leaf, which is a real strengthening of the url-only
  case beyond what the fixture file itself supplies.

I did not edit, stage, or revert any of these concurrent changes; `git status` shows the
modification is another agent's.

## Residual risk and verification gaps

- I did not execute the production instrument against a live WebArena deployment, an
  `env_config`-derived value set, or any benchmark endpoint; the whole review is offline over
  pinned bytes, as scoped.
- The mutants I used are my own constructions in `/tmp`, not the seats' exact mutant bytes for
  `R29_M_ORDER_01` and `wrongoutputfilenamebasedontask_id`; I used the seats' *semantics* as
  written in their `mutant-spec.json` files. A seat executing its own spec bytes may observe
  different failing lines than I did. I could not run the seats' specs verbatim because they are
  design-only specifications, not scripts.
- I did not re-derive the `url-only` fixture's `expected_mutant` against the production instrument
  as a mutant; the production instrument has no mutant mode, so that block is only verifiable
  against the seat's own scratch candidate, which I did read and did reproduce.
- I did not evaluate whether the frozen `profiles.json` values or the 812-task population is
  correct; that is outside this item.
- `build/R29MutOrder.md` and `build/R29MutIndex.md` are design-only reports whose mutant status
  is `NOT RUN` / `INCONCLUSIVE`; I did not attempt to close those, and I did not treat the
  coordinator's `mutation-witness.txt` as a seat-authored observation.
- The 23 dead build seats (all killed by the host SIGHUP at 2026-10-21T16:10:51Z) produced no
  reports; I did not attempt to reconstruct their contributions and no fixture in `hand/` traces
  to any of them.
- Tooling: no packages were installed, updated, or removed for this review. Everything used was
  already present: `python3` 3.14.8 (stdlib only), `git` (read-only `rev-parse`/`log`/`show`/
  `ls-files`), `sha256sum`, `cmp`, `grep`. No linters or formatters were run. No pacman, uv,
  cargo, or npm transaction was performed. The host locale is `en_US.UTF-8`; all four fixture
  files are pure ASCII, so the implicit locale decode at lines 436/444/445/453 is inert here.

## Scoped conclusion

The four adopted hand fixtures are byte-identical to their build-seat scratch originals, their
authorship matches the seats' own reports, and every declared expectation re-derives exactly
from the pinned generator source and the pinned inputs — they were hand-derived, not produced by
the production code, and the selftest consumes the values it reads without alteration. Each of the
three hand blocks is load-bearing for at least one mutant (mapping-insertion-order, eval-subtree
unprojection, and `task_id`-keyed filenames respectively). The defects found are in the receipt
and pinning story around the fixtures, not in the fixture values themselves: the hand fixtures are
unauthenticated and a fixture edit launders a mutant; the build receipt attributes two kills to
mechanisms that do not produce them and omits the one the cascade fixture exists for; the
url-only path comparison is reconstructed rather than taken from the instrument's own field; and a
missing hand fixture exits 1 instead of the preregistered 2. None of these changes any published
measurement (812 tasks × 3 profiles = 2436; the `--json` output is byte-identical with or without
the hand directory).

On the frozen lane master `56fd949` (the state under attack, and the digest the candidate freeze
and the build receipt record) all seven findings stand as written. On the concurrent uncommitted
working-tree bytes, Finding 5 is materially weakened — the instrument now carries a second,
hardcoded copy of the index expectation, so a fixture edit can no longer launder the
filename-by-task_id mutant — while Findings 1, 2, 3, 6 and the receipt findings (4) persist
unchanged. The verdict below is scoped to the frozen lane master, with that caveat stated.

VERDICT: PARTIAL
