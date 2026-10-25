writer: KengakuR29-2.FMutUrlOnly-2
# Round 29: URL-fields-only substitution mutation probe

## Scoped result

**KILLED.** Both requested detectors reject the single URL-fields-only mutant. Pristine and restored runs pass. This is a PASS for this assigned mutation probe, not a round-admission judgment or an exhaustive coverage claim.

Axes: detector sensitivity; complete exact mismatch evidence; isolation and byte restoration. No contract or production correction was attempted.

Production source read: **yes**, to choose the mutation site and locate the detector. This is not an independence-qualified oracle item. The generator was read as source data and was not imported or executed. No delegation, host-service action, package transaction, linter, formatter, Git mutation, judge, or other orchestration runtime was invoked. No tools were installed or updated. Interpreter: existing Python 3.14.8.

## Isolated intervention and expected detector

Copied the complete lane `plans/` tree with Python stdlib `shutil.copytree` from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans` to `/tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe/plans`. The only experimental edit was in `/tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe/plans/config_projection.py`. All detector `--root` arguments point to `/tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe` because the pinned paths include the `plans/` prefix. The lane's instrument and fixture bytes were not edited.

Authority: `plans/fixtures/r29/generate_test_data.py:11-16` performs the ordered global replacements before JSON parsing at line 20. `plans/round-29-claims.md:35-46,73-77` freezes global serialized-text behavior and requires non-URL coverage.

Intervention: replace the single behavior-bearing statement at original `plans/config_projection.py:146`:

```python
text = text.replace(token, values[name])
```

with these copied-file lines 146-148:

```python
for start, end, path, role, _ in reversed(string_spans(text)):
    if role == "value" and template(path) in URL_FIELD_TEMPLATES:
        text = text[:start] + text[start:end].replace(token, values[name]) + text[end:]
```

The mutant restricts replacement to value spans whose existing path category is `start_url`, `eval.reference_url`, or `eval.program_html[].url` (`URL_FIELD_TEMPLATES`, production line 39). Reverse-span slicing preserves serialized spacing and untouched text. Token order, profile values, inputs, tests, and assertions remain unchanged. Original step accounting at line 145 remains global; its reported `applied_replacements` is therefore unchanged even though the mutant skips non-URL occurrences. This deliberate one-site intervention does not weaken the detector.

Expected detector: the first non-URL selftest at original lines 392-398 and the real-data leaf-coverage/residual-token checks at original lines 316-318 and 336-337.

Source-code excerpt word counts, computed with `len(text.split())`: original statement 4; replacement lines 8, 8, 8 (24 for the replacement block); failing assertion 13. All are at most 25 words. Full observed process outputs below/in the annex are execution evidence, not external prose quotations.

## Commands and actual outputs

These exact commands were each run once on pristine, once on mutated, and once on restored module bytes. The three modes ran concurrently within each stage, with `subprocess.run(..., capture_output=True, text=True, timeout=90)` and scratch root as working directory. `--json` was added to obtain every exact mismatch; it is not a substitute for either requested detector.

```text
python3 /tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe/plans/config_projection.py --selftest --root /tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe
python3 /tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe/plans/config_projection.py --summary --root /tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe
python3 /tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe/plans/config_projection.py --json --root /tmp/KengakuR29-2.FMutUrlOnly-2.30j8crfe
```

| Bytes | --selftest exit | --summary exit | --json exit | Observed result |
|---|---:|---:|---:|---|
| pristine | 0 | 0 | 0 | SELFTEST clean cases=20; TOTAL findings=0 exit=0 |
| mutated | 1 | 1 | 1 | AssertionError; 6 audit findings |
| restored | 0 | 0 | 0 | SELFTEST clean cases=20; TOTAL findings=0 exit=0 |

The mutated selftest wrote no stdout. Its stderr ends in `AssertionError` at copied-file line **398**, corresponding to pristine/restored line **396**:

```python
assert not findings and [s["applied_replacements"] for s in record["steps"]] == [2] * 6
```

The call stack is copied-file line 550 (module), line 535 (`main`), line 398 (`selftest`). The first assertion stopped the selftest; no claim is made that the later adopted URL fixture executed in the mutant run. Baseline and restored runs did report all 20 cases clean, including that adopted fixture. Full actual selftest stdout/stderr are retained in the receipt annex.

The mutated summary emitted exactly these findings, then `TOTAL findings=6 exit=1`:

```text
FINDING {"changed": 1355, "id": "leaf_change_unexplained", "profile": "distinct_origins", "token_leaves": 1416, "unexplained": 0}
FINDING {"id": "known_token_remaining", "profile": "distinct_origins"}
FINDING {"changed": 1355, "id": "leaf_change_unexplained", "profile": "path_prefix", "token_leaves": 1416, "unexplained": 0}
FINDING {"id": "known_token_remaining", "profile": "path_prefix"}
FINDING {"changed": 1355, "id": "leaf_change_unexplained", "profile": "trailing_slash_sensitivity", "token_leaves": 1416, "unexplained": 0}
FINDING {"id": "known_token_remaining", "profile": "trailing_slash_sensitivity"}
```

The reference receipt `corpus/evidence/round29-calibration/mutation-witness.txt:1-5` was read but not accepted as proof. The fresh control hash and observed URL-only selftest exit 1 / summary findings 6, exit 1 reproduce its reported outcome independently.

## Frozen real-data sensitivity and exact mismatches

**Frozen real data alone detects this mutant: yes.** The separate `--summary` run returned exit 1 without invoking selftest. `audit`, production lines 347-359, reads the authenticated generator/raw/profiles and calls `audit_text`; it does not load hand fixtures.

Observed from complete retained `--json` outputs and the programmatic recursive comparison:

- Input tasks 812; profiles 3; task/profile projections 2436 in both pristine and mutant outputs. Population and index mapping do not expose this fault by themselves.
- **183 projected string-leaf mismatches**, comprising **61 exact raw leaf paths in each profile**. These involve **18 distinct task indices**: 66, 552, 553, 554, 555, 562, 563, 564, 565, 566, 681, 682, 683, 684, 685, 686, 687, 688.
- Each profile leaves **62 known-token occurrences**: 8 GITLAB and 54 REDDIT. The 61-versus-62 difference is a unit distinction, not rounding: raw task 66's annotation contains two occurrences in one string leaf.
- The pristine changed paths include 60 `eval.program_html[].required_contents.must_include[]` leaves and one `eval.reference_answer_raw_annotation` leaf that the mutant omits. URL-field changes remain 1355 per profile.
- Complete recursive comparison of the entire JSON result yields **468 difference records** (including projected values, changed-leaf metadata, task/file digests, aggregate metrics, and added findings). All exact paths and both values are retained, including complete objects for missing/added entries. This is not a sampled comparison.

These metric values apply identically to each of the three profiles:

| JSON profile-relative location | Pristine value | Mutant value |
|---|---|---|
| `changed_leaf_count` | `1416` | `1355` |
| `changed_task_count` | `812` | `812` |
| `changed_leaves_with_multiple_occurrences` | `13` | `12` |
| `changed_leaves_by_category` | `{"non_url_field": 61, "url_field": 1355}` | `{"url_field": 1355}` |
| `changed_leaves_by_path_template` | `{"eval.program_html[].required_contents.must_include[]": 60, "eval.program_html[].url": 338, "eval.reference_answer_raw_annotation": 1, "eval.reference_url": 205, "start_url": 812}` | `{"eval.program_html[].url": 338, "eval.reference_url": 205, "start_url": 812}` |
| `changed_leaves_by_token` | `{"__GITLAB__": 385, "__MAP__": 133, "__REDDIT__": 323, "__SHOPPING_ADMIN__": 300, "__SHOPPING__": 275, "__WIKIPEDIA__": 0}` | `{"__GITLAB__": 377, "__MAP__": 133, "__REDDIT__": 270, "__SHOPPING_ADMIN__": 300, "__SHOPPING__": 275, "__WIKIPEDIA__": 0}` |
| `changed_tasks_by_token` | `{"__GITLAB__": 204, "__MAP__": 128, "__REDDIT__": 128, "__SHOPPING_ADMIN__": 182, "__SHOPPING__": 192, "__WIKIPEDIA__": 0}` | `{"__GITLAB__": 196, "__MAP__": 128, "__REDDIT__": 119, "__SHOPPING_ADMIN__": 182, "__SHOPPING__": 192, "__WIKIPEDIA__": 0}` |
| `remaining_known_tokens_text` | `{"__GITLAB__": 0, "__MAP__": 0, "__REDDIT__": 0, "__SHOPPING_ADMIN__": 0, "__SHOPPING__": 0, "__WIKIPEDIA__": 0}` | `{"__GITLAB__": 8, "__MAP__": 0, "__REDDIT__": 54, "__SHOPPING_ADMIN__": 0, "__SHOPPING__": 0, "__WIKIPEDIA__": 0}` |
| `remaining_known_tokens_decoded` | `{"__GITLAB__": 0, "__MAP__": 0, "__REDDIT__": 0, "__SHOPPING_ADMIN__": 0, "__SHOPPING__": 0, "__WIKIPEDIA__": 0}` | `{"__GITLAB__": 8, "__MAP__": 0, "__REDDIT__": 54, "__SHOPPING_ADMIN__": 0, "__SHOPPING__": 0, "__WIKIPEDIA__": 0}` |

Projected serialized-text hashes differ by profile:

| Profile | Pristine SHA-256 | Mutant SHA-256 |
|---|---|---|
| `distinct_origins` | `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` | `e7d2b91427231f008c98f9465238ab1708c82a7f2372c1fe6894dced0bf2b00f` |
| `path_prefix` | `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` | `0711f465c0981b8e28a38b8e6fb4e2c8faf3f6ab89d900ee7845d95e393fb601` |
| `trailing_slash_sensitivity` | `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2` | `3fd255a7a367e5d2d0758df583bbdcafaf4e85ca27084e7956a9ba4dcf7b007b` |

Concrete exact witness: `plans/fixtures/r28/webarena/config_files/test.raw.json:2126`, raw JSON pointer `/66/eval/reference_answer_raw_annotation`. Its two literal REDDIT occurrences start at original-input Unicode-codepoint offsets 61888 and 61968, line 2126 columns 43 and 123 (line/column 1-based). Exact three-profile values from the observed outputs:

```jsonl
{"json_pointer": "/profiles/distinct_origins/tasks/66/projected_task/eval/reference_answer_raw_annotation", "mutant": "__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter", "pristine": "http://reddit.invalid:10102/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10102/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter", "profile": "distinct_origins"}
{"json_pointer": "/profiles/path_prefix/tasks/66/projected_task/eval/reference_answer_raw_annotation", "mutant": "__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter", "pristine": "http://reddit.invalid:10202/prefix/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10202/prefix/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter", "profile": "path_prefix"}
{"json_pointer": "/profiles/trailing_slash_sensitivity/tasks/66/projected_task/eval/reference_answer_raw_annotation", "mutant": "__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter", "pristine": "http://reddit.invalid:10302//f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10302//f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter", "profile": "trailing_slash_sensitivity"}
```

### Exhaustive mismatch annexes (integral to this report)

- `.ufo/waves/round-29/scratch/falsify/FMutUrlOnly/projected-leaf-mismatches.jsonl:1-183`: every projected-task mismatch, exact output JSON pointer, raw pointer, task/output index, raw occurrence offsets and line/column, pristine value and mutant value. One record per mismatching projected string leaf; all three profiles are explicit.
- `.ufo/waves/round-29/scratch/falsify/FMutUrlOnly/all-output-mismatches.jsonl:1-468`: every recursive whole-output mismatch. `json_pointer` is relative to the instrument's JSON output; `kind` distinguishes value/type/missing/added, and `pristine`/`mutant` contain complete exact observed values as applicable. Lists are compared by ordinal, matching the output-index contract.
- `.ufo/waves/round-29/scratch/falsify/FMutUrlOnly/probe-evidence.json`: commands, every exit, complete summary and selftest stdout/stderr, SHA-256 of every stdout/stderr stream (including full JSON streams), mutation, input hashes, word counts, comparison counts, and restoration results. Full JSON stdout is represented by its digest plus exhaustive differences rather than duplicated unchanged task objects.

All counts above were computed from retained command outputs using `json.loads`, recursive dictionary/list/scalar comparison, `len`, sets of exact pointers/indices, and `Counter`; no benchmark count was estimated.

| Evidence file | UTF-8 bytes | Records | SHA-256 |
|---|---:|---:|---|
| `.ufo/waves/round-29/scratch/falsify/FMutUrlOnly/probe-evidence.json` | 32586 | receipt object | `2acd2c5ee1276d48d996a38426f63a90b5edc74cd5c24be797aade57d1d81dc9` |
| `.ufo/waves/round-29/scratch/falsify/FMutUrlOnly/projected-leaf-mismatches.jsonl` | 110024 | 183 | `d30e81877bebad5e479a074c93497a2c9500422ad9ff3fcd2772b1b78a9c0c12` |
| `.ufo/waves/round-29/scratch/falsify/FMutUrlOnly/all-output-mismatches.jsonl` | 170216 | 468 | `b1f6602ac35756e7dde8d04c5dd5cffe712f58cfb1604adc259e74c9517c8a62` |

## Exact restoration and noninterference evidence

| Instrument state | SHA-256 |
|---|---|
| Lane before / copied pristine | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |
| Copied mutant | `e12e84e38f26377f5824d988c32739db21bd5c4336631957875d98507dd1d004` |
| Copied restored / lane after | `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` |

The inverse surgical edit restored original line 146; copied module equality against the saved pristine bytes was **true**, not merely a matching summary. Every restored detector exit, stdout byte string, and stderr byte string equals its corresponding pristine capture. Restored stdout SHA-256: selftest `1fa3c1fcb6d6b3f7b2a83097b8473343bf278fb20b88c1fcfa99161878058d44`, summary `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`, JSON `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`.

Each following pinned input hash matched both the copied input after the probe and the lane input after the probe:

| Input | Before/after SHA-256 |
|---|---|
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |

The experimental copy is restored in `/tmp`; lane writes are confined to this report and the three evidence annexes in this item's allowed scratch directory. No production change is proposed or shipped.

[INFERENCE] This killed mutant establishes sensitivity to this particular path-restricted substitution fault, not exhaustive mutation coverage or a runtime/task-validity claim. No survivor or baseline failure occurred in this probe.

VERDICT: PASS
