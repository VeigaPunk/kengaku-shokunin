writer: KengakuR29-2.FReviewDiff-2

# FReviewDiff — diff()/leaf counting in `plans/config_projection.py` (structure detection, ordering, carrier invariant, decoded census)

Scope: the assigned area only — `diff()` and the leaf census it feeds in
`plans/config_projection.py` (lines 230–249 `diff`, 200–212 `pointer`/`template`, 214–227
`provenance`, 252–262 `string_values`, 266–339 `audit_text`). I attacked: structure-change
detection, dict/list ordering comparison, the changed-vs-carrier leaf invariant
(`leaf_change_unexplained`, lines 316–318), and the decoded remaining-token census including
keys (lines 307–308, 336–337).

Independence / source reading: **I did read the production source** `plans/config_projection.py`
in full (this item is a diff/leaf-counting review, not an oracle item). My independent leaf walk
was written from the prereg text (`plans/round-29-claims.md`), the pinned generator bytes
(`plans/fixtures/r29/generate_test_data.py`) and the pinned raw file only
(`scratch/falsify/FReviewDiff/oracle.py`), and was compared against the instrument's `--json`
**output**; it never imports the instrument.

Production mutation: none. Lane Git index, corpus, fixtures, SOURCES, SCORECARD and the candidate
were not touched. All experiments ran on `/tmp` copies (`/tmp/fr29d/cp.py`) or on my own scratch
dir `.ufo/waves/round-29/scratch/falsify/FReviewDiff/`.

Tooling: none installed or upgraded. Python 3.14.8 stdlib only (`python3 -V` → `Python 3.14.8`).
No pacman, no network, no REA device.

## 0. Baseline and independent re-derivation (pinned population)

Commands (run from lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`):

1. `python3 plans/config_projection.py --summary` → exit 0, last line `TOTAL findings=0 exit=0`.
2. `python3 plans/config_projection.py --json` → exit 0, 3,881,050 bytes.
3. `python3 plans/config_projection.py --selftest` → exit 0,
   `SELFTEST clean cases=20 six_tokens_and_non_url_field,units_not_pooled,...`.
4. Independent oracle `scratch/falsify/FReviewDiff/oracle.py` (my own leaf walk, six ordered text
   replacements, `json.loads`, parallel walk of every leaf) vs the instrument's `--json`.

My independent walk reproduces **every** leaf metric of the instrument exactly, for all three
frozen profiles: `parsed_task_count` 812; `string_leaf_count` 10869; `changed_leaf_count` 1416;
`changed_task_count` 812; `changed_leaves_with_multiple_occurrences` 13;
`changed_leaves_by_category` {non_url_field 61, url_field 1355};
`changed_leaves_by_path_template` {must_include[] 60, program_html[].url 338,
reference_answer_raw_annotation 1, reference_url 205, start_url 812};
`changed_leaves_by_token` {GITLAB 385, REDDIT 323, SHOPPING 275, SHOPPING_ADMIN 300, WIKIPEDIA 0,
MAP 133}; `remaining_known_tokens_text` and `remaining_known_tokens_decoded` all 0;
`projected_text_sha256` identical; per-task changed-leaf JSON pointers identical for all 812×3
task/profile pairs. `oracle-vs-instrument.txt` holds the comparison (0 mismatches after the
pointer-order artefact of my own comparator, which I corrected).

Differential fuzzing (my own random inputs, instrument vs my walker): 4000 cases
(`fuzz-diff-output.txt`) — 0 count mismatches, 0 pointer mismatches, 0 per-token census
mismatches, 0 structural-finding mismatches, 0 exceptions. 3000 text-mutation cases with JSON
escapes, duplicate keys and tokens in key position (`fuzz-census-output.txt`) — 0
serialized-text census mismatches, 0 decoded census mismatches, 0 missing/spurious
`known_token_remaining` findings, 0 exceptions.

So the instrument's leaf accounting is **numerically correct on the claimed scope**. The findings
below are defects in the same code that the pinned run does not reach, plus one live reporting
hazard and one defect exercised by an *adopted* hand fixture.

## F1 — `template()` raises IndexError on a valid JSON document (MEDIUM)

Location: `plans/config_projection.py:208`, inside `template()` (204–212):

```
            parts[-1] = parts[-1] + "[]" if parts else "[]"
```

The conditional guards the right-hand side only; the assignment target `parts[-1]` is still
evaluated, and on an empty `parts` list the store raises `IndexError`. `parts` is empty exactly
when the first element of `path[1:]` is a list index, i.e. when a *task* is itself a list
(path `(0, 0)`), because `path[0]` is the task index.

Observed (my probe, `/tmp/fr29d/probe.py` P1, input `[["__GITLAB__"]]`):

```
  RAISED IndexError: list assignment index out of range
  File "/tmp/fr29d/cp.py", line 271, in audit_text      occurrences = provenance(raw_text, spans)
  File "/tmp/fr29d/cp.py", line 225, in provenance       "path_template": template(span[2]) ...
  File "/tmp/fr29d/cp.py", line 208, in template         parts[-1] = parts[-1] + "[]" if parts else "[]"
```

End-to-end CLI consequence (my `/tmp` root, manifest re-pinned, raw = `[["__GITLAB__"]]`,
`cli-nested-list.json`): exit **2** with the finding

```
{"findings":[{"detail":"IndexError('list assignment index out of range')","id":"input_invalid"}], ...}
```

Two defects in one: (a) a valid JSON input is rejected as `input_invalid` (a
could-not-evaluate that is really a code bug, misattributed to the input), and (b) the same
expression is used again at `config_projection.py:314` in the changed-leaf loop — that second site
is never reached, because `provenance()` raises first (observed traceback above). Reachability on
the claimed scope: **not reachable** — every task in the pinned raw is a JSON object, so `path[1]`
is always a key string. Latent defect.

## F2 — leaf→token attribution is wrong under a later-token cascade (MEDIUM)

Location: `plans/config_projection.py:311` (`carried = [token for token in tokens if token in before]`),
used at 313–315 (`"tokens": carried`) and counted at 327–328 (`changed_leaves_by_token`,
`changed_tasks_by_token`).

`carried` is derived from the **original** leaf text, so the census credits a leaf to the token
that was present *before* the projection, not to the profile value that actually produced the
projected text. The six replacements are ordered, so a profile value that itself contains a later
token makes the final leaf text come from a different profile value than the one credited.

Observed on the **adopted hand fixture** `plans/fixtures/r29/hand/cascade-order.case.json`
(case_id `R29_ORDER_CASCADE_01`, values `GITLAB=__REDDIT__`, `REDDIT=__SHOPPING__`,
`SHOPPING=__SHOPPING_ADMIN__`, `SHOPPING_ADMIN=__WIKIPEDIA__`, `WIKIPEDIA=__MAP__`,
`MAP=https://map.invalid/order`) — `cascade-output.txt`:

```
applied_replacements: {"GITLAB": 1, "REDDIT": 1, "SHOPPING": 1, "SHOPPING_ADMIN": 1, "WIKIPEDIA": 1, "MAP": 1}
changed_leaf_count: 1  changed_leaves_by_token: {"__GITLAB__": 1, "__REDDIT__": 0, "__SHOPPING__": 0,
                       "__SHOPPING_ADMIN__": 0, "__WIKIPEDIA__": 0, "__MAP__": 0}
  leaf /0/start_url tokens=['__GITLAB__']
     original : '__GITLAB__/probe'
     projected: 'https://map.invalid/order/probe'
```

The final leaf text was produced by the **MAP** profile value after five cascading substitutions
(observed: the projected leaf text `https://map.invalid/order/probe` begins with the MAP value
`https://map.invalid/order`, and no other profile value is a prefix of it), yet the census credits
`__GITLAB__` (1) and every later token 0. [INFERENCE] The general mechanism — that the census
records "which token was present before" rather than "which profile value produced the projected
text" — follows from `carried` being computed from `before` at line 311; the six-step ordering in
the generator makes those two different whenever a value carries a token. The fixture's own
`expected_changed_string_leaf_count` exists but is never asserted by the selftest (the selftest
asserts only projected-text equality and per-step hit counts), so the mis-attribution is
unasserted by the adopted witness.

Reachability on the claimed scope: **not reachable** — all 18 profile values in
`plans/fixtures/r29/profiles.json` are token-free (verified: no `__*__` token in any of the six
values of any of the three profiles), so the pinned numbers are unaffected. The knowledge draft
discloses the cascade hazard operationally (`reject any value carrying ... a token string`), but
the instrument's own leaf output mis-attributes cascaded leaves without any disclosure in the
output. The prereg requires the cascade hand case to disclose non-equivalence; the *leaf
attribution* under cascade is not equivalent and is not disclosed.

## F3 — the `leaf_change_unexplained` invariant: one clause unreachable, the id mis-describes the other (MEDIUM)

Location: `plans/config_projection.py:309–318`.

```
309  by_task, unexplained = collections.defaultdict(list), 0
311      carried = [token for token in tokens if token in before]
312      unexplained += not carried
316  carriers = sum(1 for text in string_values(original) if any(token in text for token in tokens))
317  if unexplained or (not problems and carriers != len(changed)):
318      findings.append({"id": "leaf_change_unexplained", "profile": name, "unexplained": unexplained, "token_leaves": carriers, "changed": len(changed)})
```

(a) `unexplained` counts changed leaves whose **original** text contains none of the six tokens.
The only mutation mechanism in this instrument is literal token substitution on the serialized
text, so a leaf can only differ if its original decoded text contains a token literally (a token
hidden behind a JSON escape is not literally in the text and is therefore not replaced).
[INFERENCE] Hence `unexplained ≡ 0` for this projection family. Empirically: `unexplained` = 0 on
all three frozen profiles, and 0 in all 4000 + 3000 fuzz cases (`fuzz-diff-output.txt`:
`"unexplained_gt0": 0`); no case was found in which the clause is reachable.

(b) The reachable trigger I found is `carriers != len(changed)`, i.e. *a token-bearing leaf did
not change* — the opposite of the finding's name. Observed (probe P6, input
`[{"intent": "\u005f\u005fGITLAB__"}]`, escaped spelling):

```
findings: ["leaf_change_unexplained", "known_token_remaining"]
detail: {"changed": 0, "id": "leaf_change_unexplained", "profile": "distinct_origins", "token_leaves": 1, "unexplained": 0}
```

There is no unexplained leaf change at all (unexplained = 0, changed = 0); the id asserts one.
The same mislabeled finding appears when a profile value equals its own token (probe P8, value
`GITLAB=__GITLAB__`: `{"changed": 0, "id": "leaf_change_unexplained", ..., "token_leaves": 1,
"unexplained": 0}` plus `known_token_remaining`). A reader who greps for an "unexplained leaf
change" gets a false positive with a payload that contradicts the id.

(c) The invariant compares two views of the *same* parsed object (`carriers` from
`string_values(original)`, `changed` from the diff of the parsed pair). It therefore cannot
detect a text-level vs object-level divergence — see F4.

## F4 — text-level and object-level leaf views can disagree with no invariant firing (MEDIUM)

Location: `plans/config_projection.py:279–282` (text-level occurrence census), `145` (applied
replacements), `303` (`diff`), `309–318` (leaf census and invariant).

`json.loads` keeps the **last** of a duplicated object key, while the text-level census and the
six `str.replace` calls see every occurrence. Observed (probe P2, input
`[{"a": "__GITLAB__", "a": "__REDDIT__"}]`):

```
original_occurrences_by_token: {"__GITLAB__": 1, "__REDDIT__": 1, ...}
applied_replacements: {"GITLAB": 1, "REDDIT": 1, ...}
changed_leaves_by_token: {"__GITLAB__": 0, "__REDDIT__": 1, ...}
changed_leaf_count: 1   changed_task_count: 1
tasks_with_token: {"__GITLAB__": 1, "__REDDIT__": 1, ...}
findings: []
```

One `__GITLAB__` occurrence is counted as replaced in the text and is reported in
`original_occurrences_by_token` and `tasks_with_token`, yet **no leaf is attributed to it**
(`changed_leaves_by_token["__GITLAB__"] = 0`) and **no finding fires**, because both sides of the
`leaf_change_unexplained` test are computed on the duplicate-collapsed object.

Reachability on the claimed scope: **not reachable** — the pinned 812-task raw contains no
duplicate key (checked with an `object_pairs_hook` duplicate counter: `duplicate keys found: NONE`).
Latent defect, but it is exactly the class of mismatch the leaf invariant exists to catch.

## F5 — per-token leaf buckets are a non-disjoint partition; the summary prints no non-additivity note (LOW–MEDIUM, live on the task unit)

Location: `plans/config_projection.py:327` (`changed_leaves_by_token`), `328`
(`changed_tasks_by_token`), `281–282` (`tasks_with_token`, `tasks_with_any_token`), printed at
`379–380`.

A leaf carrying two different tokens is counted in both per-token buckets, so the buckets are not
a partition of the leaves and summing them over-counts. Observed (probe P5, input
`[{"intent": "__GITLAB__ and __REDDIT__"}]`):

```
changed_leaf_count: 1
changed_leaves_by_token: {"__GITLAB__": 1, "__REDDIT__": 1, ...}  (sum=2)
```

The same applies to `changed_tasks_by_token`. On the pinned data the *leaf* buckets happen to
coincide with the total (sum 1416 = `changed_leaf_count` 1416, because no pinned leaf carries two
distinct tokens — confirmed by my independent walk), but the *task* buckets are non-additive in
the live run and the summary prints both without a caveat:

```
changed_tasks_by_token sum = 834   changed_task_count = 812
tasks_with_token sum = 834         tasks_with_any_token = 812
```

The prereg requires `distinguish replacement occurrence counts, changed-leaf counts and task
counts; do not pool units`; the instrument's own `--summary` output offers no marker, while the
knowledge draft adds the caveat by hand (`not additive: sum 834, distinct 812`). Same-unit
pooling from the tool output alone overstates distinct tasks by 22.

## F6 — key-position changes are dropped from the leaf census while the occurrence census counts them (LOW)

Location: `plans/config_projection.py:306` (structure finding), `309–315` (leaf census),
`307–308` (decoded census).

Observed (probe P4, input `[{"__GITLAB__": 1}]`): the projection replaces the token inside the
**key**, so the projected object's key set differs → finding `projection_structure_changed`
(`paths: ["/0"]`) and `token_outside_string_value`; but

```
changed_leaf_count: 0   changed_task_count: 0
changed_leaves_by_token: all 0
population.tasks_with_token: {"__GITLAB__": 1, ...}   tasks_with_any_token: 1
```

The changed key's original/projected text is never reported, and the prereg requires per-task
`changed leaf paths with original/projected values`. The behaviour is intentional (the selftest
asserts it at line 411), but the divergence between the occurrence census (which counts the
key) and the leaf census (which does not) is not disclosed in the output. The decoded census
(lines 307–308) *does* include keys, so within one record the token census counts keys while the
leaf census does not.

## F7 — `pointer(())` is not a valid JSON pointer for the document root (LOW, informational)

Location: `plans/config_projection.py:200–201`. `pointer(())` returns `/` (a pointer to a member
named `""`), whereas RFC 6901 spells the root as the empty string. Unreachable in practice: the
root type cannot change under text substitution, so `diff()` never appends a root-level problem.
No observed effect; noted for completeness of the structure-change path.

## F8 — `applied_replacements` counts token occurrences found, not substitutions performed (LOW, informational)

Location: `plans/config_projection.py:145` (`"applied_replacements": text.count(token)`). With a
profile value equal to its own token (probe P8) the count is 1 while the projected text is
byte-identical to the input. The name overstates what was measured; the parallel field
`projected_text_sha256` does capture the real effect.

## Positive results (no defect found)

- `diff()` structure detection is complete for the reachable mutation class: type change
  (231), dict key-set **and key-order** change (234), list length change (241), scalar inequality
  (249). A 4000-case differential fuzz produced 0 disagreements with my independent walker on
  both the changed-leaf set and the structure findings.
- Dict comparison is order-sensitive (`list(original) != list(projected)`) and list comparison is
  positional (243–244); both are consistent with a text-substitution projection, where key and
  element order cannot change.
- The decoded remaining-token census (307–308) agrees exactly with my independent count of
  decoded values **and keys** in all 3000 escape/duplicate-key cases, and the
  `known_token_remaining` finding (336–337) fired in exactly the cases where either census was
  non-zero (0 missing, 0 spurious). The key-inclusive decoded census is the only path that sees a
  token hidden behind a JSON escape in key position (probe P3: text census 0, decoded census 1,
  finding raised) — that part of the design is correct.
- Every leaf metric the instrument publishes for the pinned 812×3 population is exactly
  reproduced by my independent walk from the prereg text, generator bytes and raw data.

## Residual risk and verification gaps

- F1, F4 and F6 are latent on the pinned inputs; they are reachable only by inputs the frozen
  manifest excludes. I did not construct a manifest-pinned root with a list-valued task or a
  duplicate key inside the lane (the manifest pin is fixed), so F1's CLI reproduction used a
  `/tmp` root with a re-pinned manifest copy of the script (`/tmp/fr29d/cp_cli.py`,
  MANIFEST_SHA256 patched) — the code path is identical, only the pinned digest differs.
- I did not test `string_spans()`'s manual scanner against non-JSON inputs (e.g. `NaN`,
  `Infinity`, which `json.loads` accepts but the scanner's `assert match` rejects at line 192);
  that is outside the assigned area and I report it only as an unverified observation.
- The upstream per-index file bytes (`would_be_file_sha256`, line 333) were not re-derived by
  writing the generator's `json.dump(item, f, indent=2)` output; that field is outside my area.
- The cascade defect F2 is evidenced on the adopted hand fixture; I did not attempt to rebind the
  frozen profiles to token-bearing values (out of scope, and it would invalidate the 2436 unit).

## Scoped verdict

On the claimed scope (2436 task/profile projections over the pinned raw and the three frozen
token-free profiles) the leaf census, structure detection, carrier comparison and both token
censuses are correct and independently reproduced. Outside that scope but inside the assigned
code, four concrete defects stand: a crash on a valid JSON shape (F1), a wrong leaf→token
attribution that the adopted cascade fixture exercises (F2), an invariant whose headline clause
is unreachable and whose id mis-describes its only reachable case (F3), and a text/object census
divergence the invariant cannot see (F4); plus a live non-additivity hazard in the printed
per-token buckets (F5). None of them changes a published pinned number.

VERDICT: PARTIAL

## Re-check at dbcecded (follow-up)

Writer: KengakuR29-2.FReviewDiff-2. Scope: re-check of my findings **F1, F3, F4, F7** against the
repaired instrument at lane master `dbcecded4a04247cf6fd12919327af973da10bdd`
(`plans/config_projection.py` sha256 `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142`).
Earlier bytes of this report are unchanged; the verdict line of the preceding section belongs to the
56fd949 review, and the final line of this file is the re-check verdict.

Read-only leaf: no lane, corpus, fixture, SOURCES, SCORECARD or candidate edit; no Git/JJ
operation beyond read-only `git log`/`git diff`/`git rev-parse`/`git status`; all experiments on
`/tmp/fr29d2` copies of the script, plus my own scratch dir
`.ufo/waves/round-29/scratch/falsify/FReviewDiff/`. My `/tmp/fr29d` and `/tmp/fr29d2` copies are
deleted at the end of this re-check. No tooling installed or upgraded (python3 3.14.8 stdlib only).

Repairs observed in `git diff 56fd949 dbcecded -- plans/config_projection.py`:
`template()` now appends `[]` when no name part precedes a list index; `pointer()` now emits the
empty string for the root; the carrier invariant is split into `leaf_change_unexplained` (only
when `unexplained > 0`, payload `count`) and a new `token_leaf_unchanged`; a new
`duplicate_json_key` finding plus `population.duplicate_object_keys` were added.

### F1 — `template()` on list-shaped tasks: REPAIRED (verified)

Repaired code: `template()` (now 236–244) appends `[]` instead of storing into `parts[-1]` of an
empty list. Re-check on a `/tmp` copy, input `[["__GITLAB__"]]`:

```
findings: []
changed_leaf_count: 1  changed_task_count: 1
leaf /0/0 tmpl='[]' cat=non_url_field tokens=['__GITLAB__']
```

Deeper nesting `[[["__REDDIT__"]]]` → leaf `/0/0/0`, template `[][]`; mixed input
`[["__GITLAB__"], {"z": "__MAP__", "a": 1}]` → leaves `/0/0` (`[]`) and `/1/z` (`z`), 0 findings.
End-to-end CLI on a `/tmp` root (re-pinned manifest, raw `[["__GITLAB__"], {"z": "__MAP__"}]`):
the previous `IndexError` / exit 2 / `input_invalid` is gone — the run now projects both tasks and
reports only the population findings that the probe input genuinely raises:

```
findings: [{"id": "input_population_mismatch"}, {"id": "projection_population_changed", ...}, {"id": "projection_count_invalid"}]
task0 changed_leaves: [{"json_pointer": "/0/0", "path_template": "[]", ...}]
task1 changed_leaves: [{"json_pointer": "/1/z", "path_template": "z", ...}]
```

(The probe input holds 2 tasks, not 812, so `input_population_mismatch` /
`projection_population_changed` / `projection_count_invalid` are correct for that input.) The
repaired selftest also pins this shape (`duplicate_keys_list_tasks_key_order`, asserting
`path_template == "[]"`). F1 is closed.

### F3 — carrier invariant: REPAIRED (verified)

The mislabelled finding no longer fires. Re-check, escaped-only token in a value
(`[{"intent": "\u005f\u005fGITLAB__"}]`), previously `leaf_change_unexplained` with
`unexplained: 0`:

```
findings: ["token_leaf_unchanged", "known_token_remaining"]
detail: {"changed": 0, "id": "token_leaf_unchanged", "profile": "distinct_origins", "token_leaves": 1}
```

Same for the degenerate profile value equal to its own token (`GITLAB=__GITLAB__`): findings are
`token_leaf_unchanged` + `known_token_remaining`, and the payload names the condition it reports
(a token-bearing leaf did not change: `token_leaves` 1, `changed` 0). `leaf_change_unexplained`
now fires only for `unexplained > 0` and carries `count` instead of the three-field payload.

Residual note (not a defect): the `unexplained > 0` branch is still unreachable in practice for
this projection family (substitution-only mutation ⇒ `unexplained ≡ 0`; 0 across 4000 + 3000
fuzz cases). It is now correctly named and payloaded, so it reads as a defensive check rather than
a false finding. F3 is closed.

### F4 — duplicate JSON key: REPAIRED (verified)

New finding `duplicate_json_key` with pointers and count, plus
`population.duplicate_object_keys`. Re-check of the exact input that previously produced no
finding at all (`[{"a": "__GITLAB__", "a": "__REDDIT__"}]`):

```
findings: ["duplicate_json_key"]
detail: {"count": 1, "id": "duplicate_json_key", "pointers": ["/0/a"]}
duplicate_object_keys: 1
changed_leaves_by_token: {"__GITLAB__": 0, "__REDDIT__": 1, ...}
```

The text/object divergence is now reported instead of silently absorbed. Precision check
(`dupkey.py`, 8 targeted cases + 400 randomised documents): every true duplicate inside one object
is reported exactly once with the right pointer (`/0/a`, `/0/x/a`, `/0/x/0/a`; one pointer for a
key repeated three times), the same key name in *different* objects is never reported
(`[{"a": 1}, {"a": 2}]` → 0 findings; 400 randomised documents → 0 false positives), and the
detection compares **decoded** member names, so `[{"a\u0062": 1, "ab": 2}]` is correctly reported
as one collision — `json.loads` collapses that object to `{'ab': 2}`. F4 is closed.

### F7 — pointer root: REPAIRED (verified)

`pointer(())` now returns `''` (the RFC 6901 root) instead of `'/'`; non-root pointers are
unchanged: `pointer((0,))` → `'/0'`, `pointer((0, 'a'))` → `'/0/a'`. F7 is closed.

### Regression check at dbcecded (my area)

- Pinned baseline: `python3 plans/config_projection.py --summary` → exit 0,
  `TOTAL findings=0 exit=0`, `POPULATION {"distinct_task_ids": 812, "input_task_count": 812,
  "profile_count": 3, "task_profile_projections": 2436, "tasks_with_any_token": 812}`,
  `ORIGINAL_OCCURRENCES_BY_TOKEN` unchanged (385/336/281/300/0/133), `OCCURRENCE_ROLES {"value":
  1435}`, `DUPLICATE_OBJECT_KEYS 0`, `INDEX {"unit": "input tasks",
  "index_equals_task_id_count": 812, "index_task_id_mismatches": 0}`.
- `python3 plans/config_projection.py --selftest` → exit 0, `SELFTEST clean cases=28` (was 20; the
  new cases include `duplicate_keys_list_tasks_key_order` and `verbatim_slash_and_path_category`).
- My independent leaf walk (unchanged oracle, `oracle.py`) vs the new `--json`: **0 mismatches**
  on every published leaf metric and on all 812×3 per-task changed-leaf pointer sets, for all
  three profiles: 812 parsed tasks, 10869 string leaves, 1416 changed leaves, 812 changed tasks,
  13 multi-occurrence leaves, category 1355/61, per-token 385/323/275/300/0/133, both remaining
  token censuses 0, identical `projected_text_sha256`. (My comparator now sorts both sides, so the
  earlier 438-index artefact of my own comparator is gone; the instrument never had it.)
- Differential fuzz against the repaired code: 4000 random documents → 0 count, 0 pointer,
  0 per-token census, 0 structural-finding mismatches, 0 exceptions; 3000 escape/duplicate-key
  documents → 0 serialized-text census mismatches, 0 decoded census mismatches, 0 missing and 0
  spurious `known_token_remaining` findings, 0 exceptions. The 616 `occ_vs_decoded_disagree`
  cases are the unchanged, documented text-literal vs decoded difference (an escaped token is
  invisible to the occurrence provenance census but visible to the decoded census).

### Residual notes for the coordinator (outside the four re-checked items)

- Two earlier findings of mine are disclosed in the repaired output but were not in this
  re-check's scope: the limitations list now states that per-token task counts are not additive
  and that a changed leaf's tokens are the six tokens literally present in its ORIGINAL text, and
  the summary line is renamed `TASKS_WITH_TOKEN_NOT_ADDITIVE` (my F5 reporting note and the F2
  attribution rule are now stated in the tool's own output). The cascade attribution itself
  (F2) is unchanged in the code.
- The public `--json` keys `index_mapping.index_equals_task_id` and `index_mapping.violations`
  were renamed to `index_equals_task_id_count` and `index_task_id_mismatches`; any other lane's
  checker that reads the old names needs the same rename.
- `string_spans()` now also accepts the non-standard literals `NaN`, `Infinity` and `-Infinity`
  (line 218 area), which `json.loads` accepts by default; I did not re-test that path beyond the
  pinned run, which contains none of them.

VERDICT: PASS
