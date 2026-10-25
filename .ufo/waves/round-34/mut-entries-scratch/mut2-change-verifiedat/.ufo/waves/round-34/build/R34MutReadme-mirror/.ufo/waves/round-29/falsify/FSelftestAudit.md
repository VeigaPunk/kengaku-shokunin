writer: KengakuR29-2.FSelftestAudit-2

# FSelftestAudit — scoped audit of the round-29 `--selftest` (20 cases)

Scope: `plans/config_projection.py` `selftest()` at lane master `56fd949a6478342531e61f4feecb4a685d831640`
(548 lines, sha256 `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`), prereg
`plans/round-29-claims.md` lines 73-77. Round 29 only. No production, fixture, corpus, SOURCES, SCORECARD or
candidate file was edited; no git index/lane mutation; no delegation; no pacman; no REA MCP.

I read the production source (required to map assertions to case names). For the independence check in §5 I
re-derived hand-fixture expectations from the fixture bytes and the generator bytes **without** importing
`plans/config_projection.py` (script `urlonly_check.py` / `indep.py` under my scratch dir; they use only
`json`/`re`). I did not import the production module in the re-derivation scripts.

## Target identity and a mid-review divergence

Observed fact: at review start the lane worktree file was byte-identical to HEAD
(sha256 `5673405e…`, 548 lines). During the review a sibling edited the worktree file to 596 lines
(sha256 `7d42acb9…`, `git status` shows ` M plans/config_projection.py`). [INFERENCE] that edit is a
concurrent, uncommitted sibling change, not a falsify-lane mutation; I made no edit to that file.

Every mutation result in §3/§4 was produced against the **pinned HEAD copy** at
`.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2/head/config_projection.py`
(`git show HEAD:plans/config_projection.py`, sha256 `5673405e…`), so the results are reproducible against the
lane master named in my assignment.

**Re-verified against the later sibling commit `dbcecde`** ("repair falsify findings, persist mutation
witness, add S074, freeze candidate v2"), which landed mid-review and supersedes `56fd949a` on the branch
(655 lines, sha256 `135cc682…`; pinned copy at `…/FSelftestAudit-2/head2/config_projection.py`).
Re-running my key survivors against `dbcecde` (patch targets taken from the `dbcecde` text):

| Mutant | vs `56fd949a` | vs `dbcecde` |
|---|---|---|
| `url_templates_only_start_url` | SURVIVED | **SURVIVED** |
| `url_templates_no_program_html` | SURVIVED | **SURVIVED** |
| `audit_always_exit0` | SURVIVED | **SURVIVED** |
| `drop_projection_count_invalid` | SURVIVED | **SURVIVED** |
| `projected_text_sha_zero` | SURVIVED | **SURVIVED** |
| `would_be_file_sha_zero` | SURVIVED | **SURVIVED** |
| `upstream_revision_hardcoded` | SURVIVED | **SURVIVED** |
| `drop_leaf_change_unexplained` | SURVIVED | patch no longer applied (that code was rewritten) |
| `drop_task_population_invalid` | SURVIVED | patch no longer applied (finding id renamed) |

`dbcecde` adds the `-O`/`assertions_disabled` guard, an `exit_mapping` case and CLI-child isolation
(`-I -S`, empty env) — i.e. it addresses E1 and the assert-stripping weakness — but **not** the exit-code-1
assertion gap, **not** the URL-field-classifier coverage gap (B22/B23), and **not** the digest / upstream-revision
assertion gaps (B26/B27/B29). The §3 survivor table therefore still applies to the current branch tip.

## 1. Baseline

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/config_projection.py --selftest; echo "EXIT=$?"
SELFTEST clean cases=20 six_tokens_and_non_url_field,units_not_pooled,codepoint_offsets_and_key_token,escaped_token_not_replaced,quote_backslash_decode_failure_and_escape_semantics,profile_map_errors,hand_cascade_order_R29_ORDER_CASCADE_01,hand_url_only_R29-URL-ONLY-UNREAD-METADATA-01,hand_index_r29_index_shuffled_ids_1_0,source_order_swap,source_literal_rhs,source_extra_step,source_id_filename,cli_snapshot_tampered,cli_input_missing,cli_coherent_rebinding,post_read_replacement_test.raw.json,post_read_replacement_generate_test_data.py,post_read_replacement_profiles.json,cli_manifest_tampered
EXIT=0
```

Byte-identical to the build receipt `corpus/evidence/round29-calibration/build-selftest.txt` (control sha256
`5673405e…` matches).

## 2. Case name → the assertion that would fail if the behaviour broke

Line numbers are HEAD lines. "Killed by" is the mutant class that the assertion detects (all observed, §3).

| # | Case name | Assertion line(s) | What breaks it | Killed by |
|---|---|---|---|---|
| 1 | `six_tokens_and_non_url_field` | L396 `not findings and [s["applied_replacements"] …] == [2]*6`; L397 `changed_leaf_count == 12 and changed_leaves_by_category == {"non_url_field":6,"url_field":6}`; L398 `tasks[5].projected_task.intent == "see http://map.invalid:1"` | token replacement count; leaf-count/category split; per-token value mapping | A1 (order reversed) L398; B21 (changed_task_count→leaf count) L403; B18 (multi-occurrence→0) L404; S3/S4 (category always url / always non-url) L397; B24/B25 (URL template set) L397 |
| 2 | `units_not_pooled` | L403 `original_occurrences_by_token["__GITLAB__"] == 2 and changed_leaf_count == 2 and changed_task_count == 1`; L404 `changed_leaves_with_multiple_occurrences == 1 and changed_leaves[1].json_pointer == "/0/x/0"` | occurrence vs leaf vs task unit separation | A3 (wrong URL-only) L406; S2 (URL-only leaves only) L410; A10 (byte offset) L410; B16 (string role inverted) L411; B3/B4 (drop token_outside/projection_structure) L411; B20 (occurrence_roles constant) L411 |
| 3 | `codepoint_offsets_and_key_token` | L410 `prov["__MAP__"]["original_input_codepoint_offset"] == raw.index("__MAP__") == 16 and len(raw[:16].encode()) == 18`; L411 `prov["__GITLAB__"]["string_role"] == "key" and {f["id"]} == {"token_outside_string_value","projection_structure_changed"}` | codepoint-vs-byte offset (explicit `len(raw[:16].encode()) == 18` proves bytes differ); key-role detection | B1 (drop `known_token_remaining`) L417; A10 L410; B16/B3/B4 L411 |
| 4 | `escaped_token_not_replaced` | L416 `steps[0]["applied_replacements"] == 1 and remaining_known_tokens_text["__GITLAB__"] == 0`; L417 `remaining_known_tokens_decoded["__GITLAB__"] == 1 and {f["id"]} == {"known_token_remaining"}` | escaped spelling not replaced in serialized text but present after decode | B1 L417 |
| 5 | `quote_backslash_decode_failure_and_escape_semantics` | L422 `[f["id"] for f in findings] == ["projection_json_invalid"]` (for `'http://x"y'` and `"http://x\\y"`); L424 `projected_task.start_url == "a\nb"` | quote/backslash breaks JSON rather than being repaired; JSON escape decoded not literal | S1 (backslash kept literal) L422; B10 (extra-key check off) L433 |
| 6 | `profile_map_errors` | L431 `error.finding["id"] == expected` for `missing`→`profile_missing_key`, `nonstring`→`profile_invalid_type`, `extra`→`profile_unexpected_key` | map-entry validation | B9 (missing-key check off) → `KeyError: 'MAP'` at L134; B10 L433 |
| 7 | `hand_cascade_order_R29_ORDER_CASCADE_01` | L438 `text == expected_projected_text and [applied_replacements] == expected_dynamic_replacement_hits_by_source_step`; L442 `wrong == predicted_mapping_order_mutant_text != text` | exact order + later-token cascade (6 ordered `str.replace` vs simultaneous) | A2 (mapping-insertion order) L438; C1 (simultaneous replacement) L439; B19 (other markers→0) L451 |
| 8 | `hand_url_only_R29-URL-ONLY-UNREAD-METADATA-01` | L448 `projected_task == url_expected["projection"] and not findings`; L449 changed-leaf paths; L450 `original_occurrences_by_token`; L451 `other_double_underscore_markers == {"__last_url__":1,"__page__":1}` | global (not URL-field-only) substitution; unread metadata preserved | B17 (index_equals always true) L457; A3 L406 |
| 9 | `hand_index_r29_index_shuffled_ids_1_0` | L456 `[{task_id, output_ordinal, output_filename, projected_task}] == expected_records`; L457 `[index_equals_task_id] == expected and violations == [{"output_index":0,"task_id":1},{"output_index":1,"task_id":0}]` | enumerate-index vs task_id naming | index-by-task_id mutant → L456; B17 L457 |
| 10 | `source_order_swap` | L466 `mutated != source`; L470 `error.finding["id"] == "source_contract_unrecognized"` | generator replace-order swap rejected | B14 (drop source order check) L473 |
| 11 | `source_literal_rhs` | L466, L470 | non-literal replace RHS rejected | (rejected with detail `non-literal replace step`) |
| 12 | `source_extra_step` | L466, L470 | extra replace step rejected | B14 L473 |
| 13 | `source_id_filename` | L466, L470 | `{item['task_id']}.json` filename rejected | B15 (drop filename check) L473 |
| 14 | `cli_snapshot_tampered` | L483 `output.returncode == code and findings[0].id == expected` | raw-file digest pin | A6 (snapshot pin removed) L483 |
| 15 | `cli_input_missing` | L483 | missing input file | B13 (rename `input_missing`) L483 |
| 16 | `cli_coherent_rebinding` | L483 | coherent input+manifest rebinding | A5 (manifest SHA pin removed) L483 |
| 17 | `post_read_replacement_test.raw.json` | L515 `swapped and code == 0 and retained["population"]["task_profile_projections"] == 2436` | file replaced after read must not feed projection | A7 (re-read raw from disk) L515 |
| 18 | `post_read_replacement_generate_test_data.py` | L515 | same, generator | A8 (re-read generator) → `Unevaluable` at L68 |
| 19 | `post_read_replacement_profiles.json` | L515 | same, profiles | A9 (re-read profiles) → `Unevaluable` at L122 |
| 20 | `cli_manifest_tampered` | L483 | manifest digest pin | A5 L483 |

Note on attribution method: for each mutant I captured the **deepest** traceback frame inside the mutated
copy and mapped that source line to the nearest preceding `cases.append`. Some cases share one assertion
line (10-13 share L466/L470; 14-16 and 20 share L483), so a kill at a shared line is attributed to that
shared assertion, not uniquely to one case name. Cases 10-13 are distinguished by the *mutant* used, not by
a distinct assertion.

## 3. Mutation battery (39 applied to a copy of HEAD; 24 killed, 15 survived)

Method: each mutant is a textual patch to a copy of the HEAD instrument in
`.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2/`; run as
`python3 <mutant> --selftest --root <lane>`. Exit 0 ⇒ SURVIVED. Harness: `final_battery.py`;
results: `final_results.json`.

**Killed (24):** A1 order reversed (L398) · A2 wrong-order mapping insertion (L438) · A3 wrong-URL-only
(L406) · A4 filename from task_id (L330) · A5 manifest SHA pin removed (L483) · A6 snapshot pin removed
(L483) · A7/A8/A9 re-read raw/generator/profiles from disk (L515 / L68 / L122) · A10 byte offset for
codepoint (L410) · B1 drop `known_token_remaining` (L417) · B3/B4 drop `token_outside_string_value` /
`projection_structure_changed` (L411) · B9/B10 map-entry checks (L134 / L433) · B13 `input_missing` renamed
(L483) · B14/B15 source order / filename checks (L473) · B16 string role inverted (L411) · B17 index_equals
always true (L457) · B18 multi-occurrence→0 (L404) · B19 other markers→0 (L451) · B20 occurrence_roles
constant (L411) · B21 changed_task_count→leaf count (L403) · B24/B25 URL template set (L397) · C1
simultaneous replacement (L439) · S1 backslash kept literal (L422) · S2 URL-only leaves (L410) · S3/S4
category always url / always non-url (L397) · index-by-task_id (L456).

**SURVIVED (15)** — each is a behaviour change the selftest does not detect:

| Mutant | Behaviour change | Real-world impact at the pinned data |
|---|---|---|
| B22 | `URL_FIELD_TEMPLATES` → `{"start_url"}` | `--json` `changed_leaves_by_category` changes from `{"non_url_field":61,"url_field":1355}` to `{"non_url_field":604,"url_field":812}` — **543 leaves mis-categorised**, exit stays 0, no finding |
| B23 | `URL_FIELD_TEMPLATES` → `{"start_url","eval.reference_url"}` | category becomes `{"non_url_field":399,"url_field":1017}` — **338 leaves mis-categorised** |
| B12 | `audit()` returns exit 0 unconditionally | exit-1 (projection/invariant finding) path is never exercised by any selftest case; `grep -c "code=1\|code == 1"` on HEAD = **0** |
| B2 | drop `leaf_change_unexplained` finding | the "changed leaf not explained by a token" invariant is never asserted; the prereg requires "no URL-only substitution silently introduced" |
| B5 | drop `projection_count_invalid` finding | the 2436-count invariant is unguarded; only the happy-path count is asserted (L515) |
| B6 | drop `task_population_invalid` finding | 812-task / distinct-ID population invariant unguarded |
| B7 | drop `profile_missing`/`profile_unexpected` finding | missing/extra *profile* (as opposed to missing/extra *map key*) undetectable |
| B8 | drop `manifest_contract_mismatch` check | a manifest listing the wrong files or a wrong `replacement_order` is accepted |
| B11 | profile `purpose` no longer required to be a string | `profile_invalid_type` no longer raised for a malformed purpose |
| B26 | `projected_text_sha256` → 64 zeros | per-profile projection digest becomes a constant; the digest is prereg-required output ("source text/projection digests") and is unasserted |
| B27 | `would_be_file_sha256` → 64 zeros | same, for the per-task digest |
| B28 | `stimulus_class` → `None` | the "profiles' synthetic purposes" label required by the prereg tool-interface section disappears from `--json` |
| B29 | `upstream_revision` → `"deadbeef"` | the pinned upstream revision is misreported; unasserted |
| B30 | `changed_leaves_by_token` counts occurrences not leaves | at the pinned data the values are **identical** (`{"__GITLAB__":385,"__REDDIT__":323,…}`), so this is an equivalent mutant on the frozen input, but the selftest's own multi-occurrence case does not exercise it either — the unit-separation guarantee is untested for this field |
| A11 | backslash-escape not decoded in the decoded census | escape-semantics check is one-sided (see §4) |

Two further notes on the battery:
- B31 (`profile_count` → 0) failed to patch (`"profile_count": len(results),` is not in HEAD; the key is
  `"profile_count": len(results)` inside `population` in `audit_text` with different surrounding text). Not
  counted as a result.
- The worktree 596-line copy additionally hardens `-O` handling (`assertions_disabled`, exit 2) and adds an
  `exit_mapping` case; those changes are not present in HEAD and are not credited to my findings.

## 4. Vacuous, tautological, and one-sided cases

**V1 — `L461` is redundant with an internal guard (weak, not dead).**
`assert [s["name"] for s in source_contract(source)["replace_steps"]] == list(ORDER)`. `source_contract`
already raises `source_contract_unrecognized` unless the `(token, name)` pairs equal
`[("__%s__" % n, n) for n in ORDER]` (HEAD L82-83). So whenever `source_contract` returns, L461 is true by
construction. I probed reachability: scrambling the *returned* names after the internal guard still trips L461
(killed at L463 in the probe — the `source_contract(source)` call at L461 raises on the scrambled value), and
weakening the internal guard to a token-only comparison leaves the selftest **green** (exit 0). L461 therefore
tests nothing the guard does not already enforce. It is not dead code — it does fire — but it is a
tautology given `source_contract`'s own contract. Severity: low.

**V2 — the URL-only mutant expectation is persisted but never asserted.**
`plans/fixtures/r29/hand/url-only.expected.json` contains an `expected_mutant` block
(`changed_string_leaf_paths: ["$[0].start_url"]`, `remaining_known_environment_token_occurrences: 3`,
`mismatch_paths: ["$[0].eval.reference_answer_raw_annotation","$[0].intent"]`, `detector_exit: 1`).
`"expected_mutant" in <HEAD instrument source>` → **False**. The fixture's URL-only mutant contract is
therefore never exercised. [INFERENCE] the *behaviour* is still covered (A3/S2 URL-only mutants are killed at
L406/L410), so the gap is in the persisted expectation being dead, not in coverage.

**V3 — the cascade fixture's per-step expectations are persisted but never asserted.**
`plans/fixtures/r29/hand/cascade-order.case.json` contains `expected_after_each_source_step` (6 entries),
`expected_parsed_value`, `expected_original_known_token_occurrences`,
`expected_original_occurrences_by_name`, `expected_remaining_known_token_occurrences`, `expected_task_count`,
`expected_changed_string_leaf_count`, `predicted_simultaneous_mutant_text`, `source_order`. The selftest
asserts only `expected_projected_text`, `expected_dynamic_replacement_hits_by_source_step`,
`predicted_mapping_order_mutant_text`, `mapping_insertion_order`, `values`, `raw_serialized_text`,
`case_id`. The **per-step** texts (`expected_after_each_source_step`) — the most direct expression of "exact
order and later-token cascade" — are unasserted. The prereg says "Inputs/expected values persisted"; they are
persisted, but 9 of 17 cascade keys and 1 of 8 url-only-expected keys and 7 of 17 index-fixture keys are never
read by the selftest. I confirmed the unused set programmatically (`keys.py`).

**V4 — the escaped-token and quote/backslash cases are one-sided.**
Case 4 asserts `remaining_known_tokens_text["__GITLAB__"] == 0` while `remaining_known_tokens_decoded["__GITLAB__"] == 1`
— a genuine decoded-vs-text distinction. But A11 (removing backslash-escape decoding from the decoded census)
**survives**, and the mutated mutant I wrote only removed strings containing `\\n`. [INFERENCE] the
escape-semantics assertion at L424 (`start_url == "a\nb"`) is the real guard and it does fire (S1 killed at
L422). No defect claimed here; recorded so the one-sidedness is not read as coverage of the decoded census.

**V5 — no case asserts exit code 1.** All four CLI cases call `cli(name, expected)` with the default
`code=2` (HEAD L481). L515 asserts `code == 0` for the post-read witness. Exit 1 — "projection/invariant
finding" per prereg L54 — is asserted by **no** selftest case (B12 survives). This is the prereg gap most
directly visible in the table.

**V6 — no case asserts the frozen 812-task population's shape.** The only 2436 assertion (L515) is on the
post-read witness, which passes because the files are unchanged, not because the population invariant was
checked. B6 (drop `task_population_invalid`) survives: a raw file with duplicate or non-contiguous task IDs
would produce no finding. Prereg L65-66 require "812 input tasks, distinct IDs, profile count 3, task/profile
count 2436 and no hidden exclusions"; the selftest pins none of these as an invariant.

**V7 — "non-URL fields" and "overlapping field contexts" are covered only at the shape level.**
Prereg L73-74 requires "non-URL fields; overlapping field contexts". The selftest's non-URL witness is the
`intent` field in cases 1/2/8 and the `eval.reference_answer_raw_annotation` leaf in the url-only fixture.
No selftest input has a non-empty `eval.reference_url` or any `eval.program_html[]` entry — the url-only
fixture has `eval.reference_url: ""` and `eval.program_html: []`. Meanwhile the **frozen input has 206 tasks
with a non-empty `eval.reference_url` and 651 `program_html[]` entries carrying both `url` and
`required_contents`** (i.e. the genuinely overlapping nested contexts). The category classifier's behaviour on
those nested shapes is never asserted — which is exactly why B22/B23 survive. [INFERENCE] this is the
mechanism behind the two highest-impact survivors.

**V8 — no case asserts the hand fixtures' independent authorship.** The selftest reads the fixtures and
compares against them, but nothing asserts *where* the expectation came from. I verified byte identity of the
adopted copies against the seat scratch files: `plans/fixtures/r29/hand/url-only.fixture.json` ==
`.ufo/waves/round-29/scratch/R29MutUrlOnly-2/fixture.json` (both sha256 `2c78b199…`) and
`url-only.expected.json` == `…/R29MutUrlOnly-2/expected.json` (both `e68e7a0d…`); `cascade-order.case.json` ==
`…/R29MutOrder-2/cascade-order.case.json` (both `4f957db3…`); `index-shuffled-ids.fixture.json` ==
`…/KengakuR28.R29MutIndex-2/index-shuffled-ids.fixture.json` (both `93877104…`). The `author`/`writer` fields
are present in the fixtures but never read by the selftest.

## 5. Independence of the hand fixtures (no production-computed expectations)

Re-derived from fixture bytes + generator bytes only, without importing the instrument
(`indep.py`, `urlonly_check.py`):

- `cascade-order.case.json`: `expected_projected_text` **matches** my independent six-step
  `str.replace` derivation; `expected_dynamic_replacement_hits_by_source_step` `[1,1,1,1,1,1]` **matches**;
  `expected_after_each_source_step` (all 6) **matches** my derivation.
- `url-only.expected.json`: `projection` **matches** my independent derivation;
  `raw_replacement_occurrences_by_token` **matches**; `expected_mutant.changed_string_leaf_paths`
  `["$[0].start_url"]` **matches** my independent URL-only mutant derivation; `remaining_known_environment_token_occurrences`
  `3` **matches**.
- `index-shuffled-ids.fixture.json`: `expected_records` **matches**; `expected_index_equals_task_id`
  **matches**; `expected_filename_to_task_id` **matches**; `expected_projected_raw_text` **matches**.

**No case asserts a hand fixture whose expected value was computed by the production code.** The fixtures are
independently re-derivable from the generator text alone. This is the opposite of the failure mode I was asked
to look for.

## 6. Write containment — CONFIRMED

`strace -f -e trace=openat,unlink,unlinkat,rename,mkdir,mkdirat` over the HEAD selftest
(`scratch/falsify/FSelftestAudit-2/strace_head.txt`):

- Every write-mode open (`O_WRONLY|O_RDWR|O_CREAT`) resolves to a path under
  `/tmp/kengaku-r29-projection-39sd7mlw/` (the `tempfile.TemporaryDirectory(prefix="kengaku-r29-projection-")`
  at HEAD L474) plus one anonymous `/tmp/oe8pgnbv` created and immediately `unlink`ed by `tempfile` internals.
- Write-mode opens under the lane path `/home/vgpnk/Projects/shokunin/kengaku-shokunin`: **0**.
- Lane files are opened `O_RDONLY` only: `plans/config_projection.py`, the four pinned inputs, and the four
  hand fixtures.
- All `unlink`/`unlinkat`/`rename` targets are inside the temp dir; the temp dir is removed at exit
  (`ls -d /tmp/kengaku-r29-projection-*` → 0 matches).
- `--summary` and `--json` alone: **zero** write-mode opens, zero unlink/rename.
- The selftest copies the four pinned inputs into the temp scratch before mutating them (HEAD L475-479), so the
  tamper/rebinding/post-read cases never touch the lane's own fixtures. Confirmed by the strace paths above.

**Confirmed: the selftest writes only inside a `tempfile.TemporaryDirectory` under `/tmp`, and `--summary`/
`--json` write nothing at all.**

## 7. Additional defect found while attacking the CLI child

**E1 — the CLI child inherits the full parent environment (no `-I`/`-S`, no `env=`).**
HEAD L482: `output = subprocess.run(command, capture_output=True, text=True)` with `command` =
`[sys.executable, str(Path(__file__).resolve()), "--root", str(scratch), "--json"]`. No `env=`, no `-I`, no `-S`.
Observed: with `PYTHONPATH` pointing at a directory containing a `sitecustomize.py` that appends its PID to a
marker file, one `--selftest` run produced **5** interpreter startups (parent + 4 CLI children), i.e. every CLI
child loaded the injected `sitecustomize`. The selftest still exited 0. A `PYTHONPATH`/`PYTHONHOME`/`PYTHONSTARTUP`
in the operator's environment can therefore change what the four `cli_*` cases observe. The concurrent 596-line
worktree copy already adds `-I -S` and an empty environment (visible in `git diff HEAD -- plans/config_projection.py`),
which fixes this; HEAD does not. Severity: medium for HEAD (environment-dependent test verdicts), fixed in the
in-flight worktree.

## 8. Residual risk and verification gaps

- **Not exhaustive.** 39 textual mutants over 24 distinct production behaviours is a sample, not a mutation
  coverage metric; the prereg forbids claiming exhaustive mutation coverage and I do not claim it.
- **No property/fuzz testing.** I did not fuzz `string_spans` (a hand-rolled JSON scanner), `diff`, `provenance`
  or `template` with generated inputs. `string_spans` uses `assert` for structural invariants (HEAD L177, L186,
  L192, L196), so a malformed input raises `AssertionError` rather than a typed finding.
- **The concurrent worktree was moving under me.** Findings are pinned to HEAD sha256 `5673405e…`; §3's four
  spot-checks against the 596-line worktree copy agree. A third revision would need re-running.
- **`/tmp` was at 100 % (48 MiB free)** during this review; my scratch was relocated to the lane's
  `.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2/` (on `/home`, 749 GiB free). No tool was installed or
  upgraded; no pacman transaction was run.
- I did not verify the *correctness* of the projection against the upstream generator beyond the four
  prereg-named witness mutants; that is the oracle item's scope, not mine.

## 9. Verdict rationale

The selftest is real, isolated, hand-anchored and write-contained: it kills the two prereg-named wrong
mutants (wrong-order A2/C1 at L438/L439; wrong-URL-only A3/S2 at L406/L410) plus 22 further behaviour
mutations, and its hand fixtures are independently re-derivable, not production-computed. It is not vacuous
overall and it is not tautological in its hand-fixture comparisons.

Against that: exit code 1 is asserted by **no** case; 15 behaviour mutants survive, including the two that
silently mis-categorise 543 and 338 leaves of the pinned output; the `expected_mutant` block of the URL-only
fixture and the per-step `expected_after_each_source_step` of the cascade fixture are persisted but never read;
the URL-field classifier is never exercised on the nested `eval.program_html[]`/`eval.reference_url` shapes that
dominate the frozen data; and the CLI child inherits the operator's environment. The prereg's "test findings and
exits checked" (L76-77) is only half-met: findings are checked, exits are checked only for 0 and 2.

These are gaps in the *selftest*, not proven defects in the projection's output at the pinned data — the
baseline output was not shown wrong by any surviving mutant except B22/B23 (which change reported categories,
not the projected objects) and B26/B27/B28/B29 (which corrupt reported metadata). Scoped to this item only.

VERDICT: PARTIAL
