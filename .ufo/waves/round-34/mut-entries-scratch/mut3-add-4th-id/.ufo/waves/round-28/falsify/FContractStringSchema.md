# FContractStringSchema — falsification of the active string-schema audit (round 28, author-side)

Seat: KengakuR28.FContractStringSchema. Author-side falsifier, not outside evidence. Read-only over production; every
probe, mutant and output lives under `.ufo/waves/round-28/scratch/FContractStringSchema/`. Bytecode disabled
(`python3 -B`, `sys.dont_write_bytecode`), no `__pycache__` left. No upstream code imported or executed, no network,
no browser. Tools installed/updated: none.

## Identities attacked

| object | path | sha256 |
|---|---|---|
| frozen candidate (draft) | `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches assignment) |
| audit instrument | `plans/benchmark_spec_audit.py` | `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8` |
| pinned raw tasks (S061) | `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (equals manifest) |

The canonical candidate path `corpus/knowledge/webarena-task-spec-audit.md` is not admitted. This report attacks the
frozen draft bytes above plus the instrument. Hand expectations come from the pinned scorer
`evaluation_harness/evaluators.py` (S062) lines 80–170 (StringEvaluator) and 355–374 (router). Those lines were read
as text only.

## 1. Independent census of the pinned string population: SUPPORTED

Command: `python3 -B census.py` (stdlib only, no import of the production audit or `benchmark_oracle.py`). Output is in
`census.out`, and `json.loads` used an `object_pairs_hook` to detect duplicate keys.

- 812 tasks. No duplicate JSON object keys anywhere and no NaN/Infinity constants, so last-wins `json` loading
  hides nothing and the "complete raw task" preservation claim holds for these bytes.
- Every `eval_types` value is a non-empty list of known strings. There are no duplicate or unknown eval_types.
- 335 tasks have string_match active, and each has a dict `reference_answers` (325 + 10 matches the candidate's
  evaluator-type-set row). All 477 nonactive tasks have an explicit `reference_answers: null`. No task lacks the key,
  and no nonactive task carries a non-null (dormant) reference.
- Operator occurrences are exact_match 45, must_include 176 and fuzzy_match 118, matching candidate line 104. The
  ordered tuples are exact 45, must 172, fuzzy 114 and must,fuzzy 4.
- Value shapes: exact_match is always a str, must_include is always a list of str, and fuzzy_match is either the
  string "N/A" (36 tasks) or a list of str (82 tasks). No list is empty, and no element is blank or quote-only.
- All 36 N/A tasks have a nonempty str `string_note`, and none combines N/A with another operator. This confirms the
  candidate's line 47 ("all N/A tasks in the pinned population use only that approach"). The other 299 active tasks
  carry `string_note: ""`, which the scorer never reads.
- Page-content side check (`html_vacuity.out`): 651 targets. None has an empty `must_include` list or an empty or
  quote-only OR-alternative, and none has both exact_match and must_include.

## 2. Miniature hand-expected probes against `audit_tasks`: 30 of 36 agree, 6 disagree

Command: `python3 -B probe.py <lane>/plans/benchmark_spec_audit.py > probe-production.json`. It reports
`MISMATCH 6 V01_must_empty_list,V02_fuzzy_empty_list,V03_must_empty_string,V04_must_blank_string,V05_must_quote_pair,E06_eval_types_nonstr_masks`.

Cases that agree with hand expectations:

- exact_match with an int or list value, must_include as a str, must_include or fuzzy_match lists containing an
  int, fuzzy "n/a", and a fuzzy dict all give `string_operator_invalid`.
- A missing or None `string_note` under N/A gives `string_note_invalid`.
- `reference_answers` that is None, a list, absent, or `{}` gives `reference_answers_invalid`.
- An unknown operator, alone or mixed, gives `string_operator_invalid`. The scorer's `match` has no `case _`, so an
  unknown operator would silently score 1.0, and the audit correctly flags it.
- Duplicate eval_types give `duplicate_eval_type`. Unknown types, including a case variant and an unknown type
  alongside string_match, give `unknown_eval_type`. An empty, str-valued or absent `eval_types` gives
  `eval_types_invalid`.
- When string_match is inactive, malformed references are not flagged. That is correct, because the scorer never
  reads them.
- **Nonactive None is preserved.** In N01 the record has `reference_answers: None` and `reference_approach_order: None`.

### Finding F1: vacuous string predicates are classified inconsistently (latent instrument defect)

The audit applies an emptiness rule (`or not refs`, line 90) that flags `{}`. Under the pinned scorer, `{}` returns
1.0 for every prediction (loop at :137 does nothing). The audit also flags an unknown operator alone, which
likewise yields 1.0. However, the following shapes give the same always-1.0 outcome and are reported as
**`SCHEMA_COMPATIBLE` with no finding**:

| probe | reference_answers | why it scores 1.0 for every prediction |
|---|---|---|
| V01 | `{"must_include": []}` | loop at :144 runs zero times |
| V02 | `{"fuzzy_match": []}` | loop at :166 runs zero times, so no judge call |
| V03 | `{"must_include": [""]}` | `"" in clean_pred` is always true (:111) |
| V04 | `{"must_include": ["   "]}` | `clean_answer` strips the reference to `""` (:81) |
| V05 | `{"must_include": ["\"\""]}` | `clean_answer` strips the quote pair to `""` (:84–85) |

Impact: the pinned population has **zero** instances (section 1), so no measured counter changes and "schema
findings 0" stays true for these bytes. The defect is the instrument's own validity rule contradicting itself:
it flags vacuity in some forms and certifies it in others. It would misreport a mutated or alternate population.

Smallest repair (not applied): in the string-operator loop, add a `string_reference_vacuous` finding when a valid
`must_include`/`fuzzy_match` list is empty, or when any `must_include` element is empty after strip and one
outer-quote-pair strip. Pinned impact is 0 findings. The alternative is to drop the emptiness half of line 90 and
state that vacuity is out of scope. Either way, one rule should apply to every vacuous form.

### Finding F2: a non-str eval_types element masks string findings and pollutes the histogram (minor, fail-closed)

In E06, `eval_types=["string_match", 5]` with `reference_answers={"exact_match": 3}` reports only
`eval_types_invalid`. Line 76 resets `kinds = []`, so the string branch is skipped and the malformed reference is
never reported. The same reset happens in E04, E05 and E07. Each of those writes `eval_types: []` into the derived
record, which overwrites the malformed value (only `raw_task` keeps it), and each adds an unlabeled `""` key to the
`eval_type_sets` and `eval_type_orders` histograms. The task is still marked FAILED, so this does not unsoundly
certify anything. Pinned impact is 0.

Smallest repair: when `kinds` is a list, keep its str members for the downstream branch checks
(`kinds = [k for k in kinds if isinstance(k, str)]`). Label the invalid histogram bucket explicitly, for example
`<invalid>`, instead of `""`.

### Finding F3: an absent `reference_answers` is recorded as a fabricated `{}` (minor provenance defect)

In N03 and A13, the derived record shows `reference_answers: {}` and `reference_approach_order: []` when the key is
absent. That is indistinguishable from an explicit `{}` (A14) and misstates the raw input. The cause is line 88's
`.get("reference_answers", {})`. Pinned impact is 0, because all 812 tasks carry the key.

Smallest repair: `.get("reference_answers")`. The active-branch check already rejects None.

## 3. Mutation adequacy: all 11 string/eval-type mutants survive the 21-case selftest

Command: `python3 -B mutants.py` (`mutants.json`, `mutants.summary`). The script writes each mutant to
`scratch/.../mut/`, runs that mutant's own `--selftest` with `--root <lane>` (its CLI subcases use the selftest's
own temporary fixture copy), and runs the probe battery. The unmodified production selftest was not rerun.

| mutant | selftest | killed by probe | identical output on pinned 812 (`pinned_equivalence.out`) |
|---|---|---|---|
| M01 drop duplicate_eval_type | exit0, 21 clean | E01, E09 | yes |
| M02 exact_match accepts any type | exit0 | A02, A03 | yes |
| M03 must_include element types unchecked | exit0 | A05 | yes |
| M04 fuzzy list element types unchecked | exit0 | A17 | yes |
| M05 accept empty `{}` refs | exit0 | A13, A14 | yes |
| M06 coerce None refs to `{}` | exit0 | record check N01 | no (477 nonactive records change) |
| M07 accept empty eval_types | exit0 | E05 | yes |
| M08 N/A note presence only | exit0 | A09 | yes |
| M09 drop reference_approach_order | exit0 | record check A01 | no |
| M10 skip unknown type when string_match present | exit0 | E02 | yes |
| M11 accept list-shaped refs | exit0 | A12 | yes |

Finding F4 (test adequacy): none of the active-string or eval-type validation branches the target names
(malformed operator/value shapes, empty or list refs, the N/A note type, duplicate eval_types, an unknown type next
to string_match, nonactive None preservation, approach order) is protected by the 21-case selftest. Nine of the
11 deletions also give byte-identical audit output on the pinned population. For those nine branches, the
measured "schema findings 0" therefore rests on code reading, not on a failure-capable test. The candidate's
selftest sentence (line 115) does not claim string-shape coverage, so it is not false. The preregistered controls
(unknown type, duplicate ID, snapshot) are present. Also, `plans/fixtures/r28/acceptance.py` never references
`audit_tasks`.

Smallest repair: copy the A02–A17, E01/E02/E05/E09 and N01 cases from `probe.py` into `selftest()`, with record
assertions for N01 (`reference_answers is None`, `reference_approach_order is None`) and for A01's approach order.
Together they kill all 11 mutants (demonstrated above). The selftest case count would then change from 21, which is
a candidate number for L1 to decide on.

## Impacted axes

- Coverage/constructs 7: the C1 measured string counters, nonactive None preservation, the N/A-only claim and the
  0 schema findings are all independently reproduced. F1–F3 are latent instrument defects with zero pinned impact,
  so no candidate number is wrong.
- Calibration 8: not touched by this seat.
- F4 weakens the failure-capability evidence behind "schema findings 0" for nine validation branches. It is not a
  measured-value error.

## Verdict

These are findings, not repairs; L1 resolves them. The candidate's string-schema numbers and the preservation of
nonactive `None` are fully supported. The instrument's active-string validation is not completely supported:
there are 6 hand-expected mismatches (F1, F2), a fabricated-`{}` provenance defect (F3), and 11 of 11 surviving
mutants (F4).

VERDICT: PARTIAL

---

## v2 bounded re-read and re-probe (appended after Amendment 2; v1 above preserved)

v1 section bytes (sha256 of the whole file before this append): `8b593fdaf057b2fb1629c12257c5a8cf2abd1c13218e274014cb504098e64e35`.

The authorities for this section are Amendment 2 (`plans/round-28-claims.md`), `.ufo/waves/round-28/candidate-freeze-v2.json`
and `corpus/evidence/round28-calibration/final-acceptance/`. The old 21-case output is not used as authority.
Production was read-only. All new artifacts are in the scratch directory: `probe_v2.py`, `probe-v2-production.json`,
`mutants_v2.py`, `mutants_v2.out`, `mutants_v2.json`, `mut_v2/` and `pinned_records_v2.out`. No bytecode was left
behind, nothing was installed, and no upstream code ran.

| object | sha256 | matches freeze-v2 |
|---|---|---|
| candidate draft | `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182` | yes |
| `plans/benchmark_spec_audit.py` | `b7524c2f316f5ba850bd901c932811ca55cd4adff264242488f3842def5cca36` | yes |
| receipt `audit-selftest.stdout` | reports `SELFTEST clean cases=67` | — |

### Disposition of the v1 findings under the v2 scope

- **F1 (vacuity inconsistency): resolved by scope, not by code.** The v2 audit drops the `or not refs` rule, so
  `{}` is accepted along with `[]`, blank and quote-only references. Amendment 2 and candidate lines 118 and 133–135
  declare the tool an "expected-field schema inventory, not ... a vacuity detector". Selftest cases
  `empty_refs_native_vacuity`, `include_empty_native_vacuity`, `fuzzy_empty_native_vacuity`,
  `blank_reference_native_vacuity` and `html_empty_native_vacuity` lock that scope in. One rule now covers all
  forms, so the v1 contradiction is gone. Unknown operators and malformed types still fail, which is consistent
  because they fail the declared shape check, not a vacuity check.
- **F2 (masking and unlabeled bucket): repaired.** Line 79 keeps the string members of a malformed list. The
  record's `eval_types` is now the raw value. Both histograms use `<INVALID>`, and invalid lists stay out of the
  strata.
- **F3 (invented `{}`): repaired.** `refs = evaluation.get("reference_answers")`, plus a new
  `reference_answers_present` field.
- **F4 (test adequacy): mostly closed, with a residual** (see the mutant section below).

### Scope-aware probes: 41 of 41 pass on the current audit

Command: `python3 -B probe_v2.py <lane>/plans/benchmark_spec_audit.py`, which reports `CASES 41 MISMATCH 0`. Each
case checks the finding set, the derived record fields and metrics, and that `raw_task` is preserved. New cases
beyond v1:

- E10: a mixed list with a duplicate and a non-str member gives
  `eval_types_invalid + duplicate_eval_type + string_operator_invalid`.
- E11: an unhashable member next to an unknown type gives `eval_types_invalid + unknown_eval_type`, and the raw
  list is kept.
- E12: a mixed list with valid references is still counted in `string_operators`.
- E13: a mixed list with absent references gives `reference_answers_invalid` and `present=False`.
- A18: a scalar `reference_answers` is invalid.
- N05: when `eval` is not an object, the record keeps `reference_answers None`, `present False` and
  `eval_types None`.
- Nonactive `None` and malformed nonactive references are still preserved unflagged (N01–N03).

Pinned population on the current bytes (`mutants_v2.out`, `pinned_records_v2.out`):

- 0 findings. String operators are exact_match 45, must_include 176 and fuzzy_match 118. The evaluator-type sets
  are unchanged, and the 16 selected IDs are unchanged.
- 477 nonactive records keep `reference_answers None`, and 0 records have `present=False`.
- For all 812 records, `reference_approach_order` equals the raw key order, and `eval_types` and `raw_task` equal
  the raw values. Candidate line 120 ("preserves each complete raw task and explicit reference-approach order")
  holds.

### Mutants against the 67-case selftest: 13 of 20 killed

Command: `python3 -B mutants_v2.py`. I re-anchored the v1 mutants to the v2 text. M05 is inverted to M05r ("reject
`{}`") because accepting `{}` is now the declared behavior. I also added nine controls (R01–R09) for the named
repairs.

The selftest kills M01–M07, M05r, R01, R02, R04, R05, R06 and R08, which covers every repair KengakuR28 named:
missing references not invented, the mixed raw value kept, string members checked, the invalid set bucket, and
`{}` accepted.

Survivors (the selftest exits 0; my probe kills each one):

| survivor | behavior left unpinned | output on pinned 812 |
|---|---|---|
| M08 | an N/A `string_note` that is present but not a str (None) is accepted | identical |
| M09 | `reference_approach_order` is dropped to None | **differs**, but neither the selftest nor acceptance (metrics/selection projections only) checks it |
| M10 | an unknown type is suppressed when string_match is also declared | identical |
| M11 | a list or scalar `reference_answers` is accepted when string_match is active (only None is pinned) | identical |
| R03 | the `eval_type_orders` invalid bucket loses its `<INVALID>` label (only `eval_type_sets` is asserted) | identical |
| R07 | invalid-type tasks are admitted into strata and selection | identical |
| R09 | a duplicate inside a mixed-type list goes unflagged | identical |

These are regression-permanence gaps, not current defects. The current code handles each case correctly (41/41),
and the candidate does not claim the 67 cases cover every branch (lines 126–127 list categories only). M09 is the
most material one, because it is the only survivor that changes pinned JSON and it corresponds to a stated
candidate property (line 120) that no automated check verifies.

Smallest bounded repair (optional, no production patch here): add seven selftest cases. They are
`{"fuzzy_match":"N/A"}` with `string_note=None`; `eval_types=["string_match","bogus"]`; `reference_answers=["a"]`;
an assertion that `hand_exact` gives `reference_approach_order == ["exact_match"]`; an assertion that
`eval_type_orders == {"<INVALID>": 1}` for the mixed case; `selected_task_ids == []` for the mixed case; and
`["string_match","string_match",None]` expecting `duplicate_eval_type`. Each line kills one survivor. The selftest
count would go from 67 to about 72, which is L1's decision.

### v2 verdict (scope-aware)

Under the declared v2 scope (expected-field schema inventory, vacuity out of scope), the current audit's
active-string, nonactive-`None`, duplicate/unknown eval-type and malformed-shape behavior matches every
hand-expected observation. The pinned measurements and the record-fidelity claim reproduce. The v1 findings F1–F3
are resolved, F1 by explicit scope and F2–F3 in code. What remains is the seven-mutant test-permanence
residual above, which is advisory and not a falsified claim.

VERDICT (v2): PASS — advisory residual: 7 of 20 string/eval-type mutants survive the 67-case selftest; M09
(approach order) is unguarded by any automated check.
