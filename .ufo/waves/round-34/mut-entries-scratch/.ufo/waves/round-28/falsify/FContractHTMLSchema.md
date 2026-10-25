# FContractHTMLSchema — HTML required-contents / target-schema falsification (author-side)

Seat: KengakuR28.FContractHTMLSchema (critic). Author-side evidence only, not outside non-author evidence.
Scope: C1 instrument `plans/benchmark_spec_audit.py` HTML branch (lines 109–146) vs pinned
`evaluation_harness/evaluators.py` HTMLContentEvaluator 244–333 and StringEvaluator 79–111.

## Identities re-read

| artifact | SHA256 |
|---|---|
| frozen candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | 77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8 (matches assignment) |
| `plans/benchmark_spec_audit.py` | f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8 |
| pinned `config_files/test.raw.json` | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |
| pinned `evaluation_harness/evaluators.py` | e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22 |

Canonical candidate path `corpus/knowledge/webarena-task-spec-audit.md` does not exist yet (not admitted), as expected.
No upstream code was imported or executed. No tool installs/updates. Bytecode disabled (`-B`, `PYTHONDONTWRITEBYTECODE=1`);
no `__pycache__` was created under `plans/` or `.ufo/`. All writes are under `scratch/FContractHTMLSchema/` plus this report.

## 1. Measured HTML counters — reproduced (supports candidate)

Independent census `scratch/FContractHTMLSchema/census.py` (reads only test.raw.json; imports no production code),
output `census.out.json`; target URL / selection check `selection_witness.out`:

| observable | candidate | independent |
|---|---|---|
| routed page-content targets | 651 | 651 |
| effective operators exact / include | 188 / 463 | 188 / 463 |
| `required_contents` key sets | — | `{exact_match}` 188, `{must_include}` 463, both 0, empty 0, extra keys 0 |
| value types | — | exact: str ×188; include: list[str] ×463; 0 empty lists, 0 blank items, 0 blank OR alternatives, 0 blank exact refs |
| target key sets | — | `{url,locator,required_contents}` 641; `+prep_actions` 10; no other keys |
| `prep_actions` | — | 10 targets (tasks 699–703, ×2), all `list[str]` length 1, all on JavaScript locators |
| locator classes | 105 / 524 / 22 | 105 / 524 / 22 |
| target URL classes | 238 / 338 / 75 | 238 / 338 / 75 |
| `program_html` key present but not routed | — | 401 tasks, all `[]`; 0 routed-but-missing |
| selected16 ∩ OR / prep / helper tasks | “omitted” | ∅ / ∅ / ∅ (OR tasks 431,750,751,755,756) |

Production `--summary` (scratch receipt `production.summary.out`) prints the same HTML_OPERATORS and LOCATOR_CLASSES values, plus `TOTAL … program_html_targets=651 findings=0 exit=0`.
Precedence: line 137 mirrors upstream `if "exact_match" … elif "must_include"` (evaluators.py:305/312), and is correct.

## 2. Counterexample — HTML detectors are unwitnessed: six deletion/reversal mutants survive

Command (scratch copies only, `TMPDIR` set to scratch, `--root` = lane root read-only):
`python3 -B scratch/FContractHTMLSchema/mut/<M>.py --root <lane> --selftest` and `… --summary`.

| mutant (single textual edit to a scratch copy) | selftest | pinned summary |
|---|---|---|
| M1 precedence flip: `must_include` checked before `exact_match` | exit0, `cases=21` | identical, exit0 |
| M2 `html_operator_value_invalid` → `pass` | exit0, 21 | identical, exit0 |
| M3 `prep_actions_invalid` → `pass` | exit0, 21 | identical, exit0 |
| M4 `required_contents_invalid` removed | exit0, 21 | identical, exit0 |
| M5 `html_operator_unsupported` → `pass` | exit0, 21 | identical, exit0 |
| M6 `program_html_invalid` → `pass` | exit0, 21 | identical, exit0 |

Receipts: `scratch/FContractHTMLSchema/mut/*.selftest.out` and `*.summary.out`.
The selftest's HTML cases (hand_html, hand_javascript_locator, hand_helper_locator, malformed_helper_url,
unknown_locator, invalid_locator_keeps_target_count) only cover the locator and URL branches.
None of them covers operator precedence, value types, non-dict `required_contents`, unsupported operators,
an empty or missing `program_html`, or `prep_actions`. The pinned population has 0 instances of every such shape.
The line-136 comment “exact_match takes precedence” is therefore witnessed by neither the selftest nor the data.
The candidate's falsifier “a recorded operator contradicts the source branch” (draft line 131) is not armed for HTML. M1 reverses the branch and is undetectable.

## 3. Counterexample — silently accepted shapes that the pinned scorer handles differently

Miniature probes against production `audit_tasks` (read-only import). Receipt: `scratch/FContractHTMLSchema/mutants.out.jsonl`.
Upstream behavior was hand-derived from the source lines cited.

| shape | audit | hand-derived pinned scorer behavior |
|---|---|---|
| `{"exact_match":"a","must_include":["b"]}` | no finding; counted exact only | elif: must_include silently dead (305/312) |
| `{"must_include":["a"],"fuzzy_match":["b"]}` | no finding | extra key silently ignored |
| `{"must_include": []}` | no finding | loop never runs → target vacuously 1.0 (315) |
| `{"must_include": [""]}`, `["x \|OR\| "]`, `["x \|OR\|  "]` | no finding | `"" in pred` → vacuous 1.0 (316–326, 99–111) |
| `{"exact_match": ""}` | no finding | matches the locator-failure `""` (290–294) |
| target extra key `prep_action` (typo) | no finding | ignored |
| `program_html: []` | `program_html_invalid` | vacuous 1.0, no crash |

This is internally inconsistent. An empty target list is a finding, but an empty `must_include` list (the same vacuity one level down) is not.
A blank URL `|OR|` alternative is a finding (`reference_url_empty_alternative`), but a blank HTML `|OR|` alternative is not.

`prep_actions` checking is stricter than the scorer and is not branch-aware. Non-list or non-str shapes are flagged even though upstream swallows them (283–287, no crash).
`prep_actions` on a helper locator, which upstream never reads, is still flagged as invalid. On a full-page locator it is accepted silently, so dead prep there is not reported.
All 10 pinned instances are valid and on JavaScript locators, so no measured value changes.

## 4. Dropped build requirement without disposition

`.ufo/waves/round-28/build/RevHTMLRequired.md` §3.1 specified hand cases S1–S6, S8, S11 and S12, including `shadowed_operator`, `dead_prep_actions` and `vacuous_ref` advisories.
§5 R6/R7 required them as CLI selftest fixtures.
`rg -uu -l --glob '!**/scratch/**' -e 'vacuous_ref|dead_prep|shadowed_operator|must_include_non_list|exact_match_non_string'`
over the lane (excluding this report) matches only the build reports `build/RevHTMLRequired.md` and `build/RevStringInclude.md`.
It matches nothing in the instrument, the claims, the lessons or the candidate.
Lessons mention RevHTMLRequired only at line 114 (the OR-quirk retraction) and line 140 (the seat count).
Lessons line 128 records integration of the RevHTMLLocator and RevRouterMix findings only. No acceptance, rejection or deferral of the RevHTMLRequired schema cases is recorded.
This is an unrecorded scope reduction of a build-seat requirement.

## Impacted axes

- coverage/constructs7: the measured counters stand. The instrument's HTML contract checks are untested code, and the “operator contradicts source” falsifier is unarmed.
- calibration8: no number changes. The `selftest21` wording could be read as covering the HTML schema, but it covers locator and URL cases only.
- No task-validity, runtime, or score claim is affected. The pinned population contains 0 instances of every surviving shape.

## Smallest safe correction (for L1; no production patch made)

Choose one:
1. **Instrument (preferred, about 10 lines in `selftest`)**: add probes for
   - both operators present (assert `html_operators == {"exact_match": 1}`, which kills M1);
   - `{"exact_match": 1}` and `{"must_include": "x"}`, each expecting `html_operator_value_invalid` (kills M2);
   - `required_contents: []` (kills M4);
   - `{"fuzzy_match": ["x"]}` (kills M5);
   - `program_html: []` (kills M6);
   - `prep_actions: "x"` on a JavaScript locator (kills M3).

   Optionally, emit advisory-only counters (not exit-affecting findings) for `shadowed_operator`, `ignored_required_contents_keys`, `vacuous_html_ref` (empty list, blank item or blank `|OR|` alternative) and `dead_prep_actions`. All are pinned 0, so the measured counters stay unchanged.
2. **Candidate text only**: state that selftest21 witnesses the HTML locator and URL branches but not operator precedence, value types or `prep_actions`. Also state that vacuous or shadowed HTML predicates are not detected, and that the pinned count of each was independently found to be 0. Record a disposition for RevHTMLRequired S1–S6/S8/S12 in the lessons.

Either correction changes bytes and needs a same-identity reread. Neither alters 651 / 188 / 463 / 105 / 524 / 22 / 238 / 338 / 75.

VERDICT: PARTIAL. All HTML measured counters and the precedence reading are independently supported. However, the instrument's HTML schema detectors (precedence, value types, `required_contents`, unsupported operators, empty targets, `prep_actions`) survive deletion or reversal under selftest21 and the pinned summary. Vacuous and shadowed predicates are accepted silently, and RevHTMLRequired's specified cases were dropped without a recorded disposition.

---

## Repair re-probe (v2) — appended 2026-10-21; v1 above preserved unchanged

Requested by KengakuR28 over IRC. The re-probe is restricted to the six v1 mutants, with hand expectations adapted to the scope now disclosed:
- empty predicate containers are compatible with the scorer's native vacuity and are not certified as meaningful predicates;
- `prep_actions` is validated only on the JavaScript-locator branch that consumes it.

The work was finite scratch checks only, with no production edits and no installs.

### Identities

| artifact | SHA256 | matches `candidate-freeze-v2.json` |
|---|---|---|
| candidate v2 `drafts/webarena-task-spec-audit.md` | 3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182 | yes |
| `plans/benchmark_spec_audit.py` | b7524c2f316f5ba850bd901c932811ca55cd4adff264242488f3842def5cca36 | yes |
| pinned `test.raw.json` / `evaluators.py` | 7b50386f…37652 / e23edb39…00c22 | unchanged from v1 |
| `final-acceptance/audit-selftest.stdout` | c3d54a97…2f045 | byte-identical to my fresh production `--selftest` output (`cases=67`, exit0) |

The canonical `corpus/knowledge/webarena-task-spec-audit.md` is still absent, which is consistent with the freeze scope.
The pre-existing `plans/__pycache__` and `plans/fixtures/r26/__pycache__` (mtimes 03:51–08:54) predate this seat's first scratch file (11:29), so this seat did not create them.

### Mutant re-run

The mutants were regenerated from the v2 bytes in `scratch/FContractHTMLSchema/v2/mut/`; each anchor occurs exactly once.
For every mutant, the pinned `--summary` output is identical to production (after dropping the LIMIT lines): exit0, 651 targets, HTML operators 188/463, locator classes 105/524/22.

| mutant | adapted hand expectation | selftest67 result |
|---|---|---|
| M1 precedence flip | the shadow case `{"exact_match":"x","must_include":3}` must stay clean (the exact branch never reads the include value) | **killed**: exit1 at `html_exact_shadows_include` |
| M2 drop `html_operator_value_invalid` | `{"exact_match":3}` must be a finding (beartype `ref: str`) | **killed**: `html_exact_bad_type` |
| M3 drop `prep_actions_invalid` | JavaScript locator with `prep_actions: [3]` must be a finding | **killed**: `html_bad_prep_actions` |
| M3b (adapted) drop the JavaScript-branch guard | unread `prep_actions: 3` on a full-page locator must be clean | **killed**: `html_unread_prep_actions` |
| M4 drop `required_contents_invalid` | `required_contents: null` must be a finding | **killed**: `required_contents_null` |
| M5 drop `html_operator_unsupported` | `{"unknown":"x"}` must be a finding (ValueError, evaluators.py:329–332) | **killed**: `html_unknown_operator` |
| M6 drop `program_html_invalid` | `program_html: null` must be a finding | **killed**: `html_nonlist_targets` |
| M6b (adapted) re-reject empty target lists | `program_html: []` must be clean (native vacuity; disclosed) | **killed**: `html_empty_native_vacuity` |

All six v1 survivors and both scope-adapted inverses are now killed, each by its named hand-expected control.
The pinned summary remains blind to all of them because the data has 0 instances. That is expected: the selftest, not the population, is the witness.

### Disclosure check against the v1 findings

| v1 finding | how it is now handled |
|---|---|
| v1 §3 (silent vacuous/shadowed shapes) | Disclosed in candidate v2, lines 118 and 133–135 (vacuity advisories are not a complete feature; schema compatibility can coexist with a vacuous native predicate). Selftest pins `include_empty_native_vacuity`, `blank_reference_native_vacuity` and `html_empty_native_vacuity` as deliberate clean outcomes. |
| v1 §4 (no disposition for RevHTMLRequired) | Lessons M76 (line 167) and line 184 record it: hand-expected cases added; no full vacuity/dead-field classifier is claimed. |
| `prep_actions` over-strictness | Resolved: findings fire only on the consuming JavaScript branch. |

### Residual (outside the six, non-blocking)

The extra probe X1 changes the HTML `must_include` check from `isinstance(value, list) and all(isinstance(v, str) …)` to `isinstance(value, list)`. It **survives**: selftest67 exit0, pinned summary identical.
No selftest row uses an HTML `must_include` list containing a non-string element. The string-side equivalent, `include_nonstr_element`, does exist.
Hand-derived pinned behavior: `{"must_include": ["x", 3]}` crashes the scorer with `AttributeError` on `content.split` (evaluators.py:316).
The pinned population has 0 such elements (census v1: include values are list[str] ×463), so no measured value or candidate sentence is affected.
The probe X2 (dropping the exact-match type check) is killed by `html_exact_bad_type`.

Smallest repair (optional, one row): add `("html_include_bad_element", {"url": "last", "locator": "", "required_contents": {"must_include": ["x", 3]}}, ["html_operator_value_invalid"])` to the HTML table in `selftest`.

Receipts: `scratch/FContractHTMLSchema/v2/{production.selftest.out, production.summary.out, mut/*.selftest.out, mut/*.summary.out}`.

REPAIR VERDICT: PASS for the scoped repair. All six v1 mutants and both scope-adapted variants are killed by named hand-expected controls in selftest67. The receipt equals the fresh run, the counters are unchanged, and vacuity and the RevHTMLRequired disposition are disclosed. One non-blocking residual remains: the HTML `must_include` element-type mutant (X1), with 0 instances in the pinned population.
