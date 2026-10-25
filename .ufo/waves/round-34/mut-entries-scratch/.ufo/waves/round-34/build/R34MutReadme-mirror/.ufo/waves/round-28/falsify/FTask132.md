# Round 28 C1 falsification — BUILD case132 (WebArena task_id 132)

Seat: `KengakuR28.FTask132` (author-side falsifier; leaf, no delegation). Scope: this one case only —
the pinned task 132 static task-spec and scorer path. Not a benchmark-wide verdict, not a runtime or
browser claim, not a C2 claim.

No installs or updates. No upstream code imported/evaluated/executed. No benchmark site or browser
contact. No REA MCP. No production writes: only this report and own scratch
(`.ufo/waves/round-28/scratch/KengakuR28.FTask132/`). One read-only CLI probe of the delivered audit
instrument (stdout to scratch) was run **after** independent derivation; it is not used as the source
of any count below.

## Inputs and integrity

| input | sha256 observed | note |
|---|---|---|
| `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` | equals assigned frozen candidate |
| `.ufo/waves/round-28/build/Task132.md` | `7e58517d4317e43742a9ddef4f7e8af4634bb0384583e5c06f58bac8b5d6e362` | case under test |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | matches `manifest.json` |
| `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | matches `manifest.json` |
| `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | matches `manifest.json` |
| `plans/fixtures/r28/webarena/selected-task-ids.json` | `[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]` | exact bytes read |

Method: stdlib `json` parse of the pinned raw file plus `awk` line reads of the pinned sources
(`python3` 3.14.8, `/usr/bin/python3`); no AST, no import of `evaluators.py`/`helper_functions.py`.

## Claim-by-claim verification (case text → observed bytes)

| case claim | observed | status |
|---|---|---|
| task 132 object at `test.raw.json` L4232–L4264 | `{` at 4232, `task_id: 132` at 4236, `}` at 4264 | confirmed |
| `intent_template` L4241 | `How many commits did {{user}} make to {{repo}} on {{date}}?` | confirmed |
| S061 quote L4247 | `"intent": "How many commits did kilian make to a11yproject on 3/5/2023?"` (11 words) | confirmed |
| `eval.eval_types` L4250–L4252 | `["string_match"]` | confirmed |
| `reference_answers` L4253–L4257 | `{"must_include": ["1"]}` | confirmed |
| `reference_answer_raw_annotation` `"1"`; `reference_url ""`; `program_html []`; `string_note ""` | L4261, L4258, L4259, L4260 | confirmed |
| sites/login/storage/start/geolocation/reset | `["gitlab"]`, `true`, `./.auth/gitlab_state.json`, `__GITLAB__`, `null`, `false` (L4233–4240, 4248) | confirmed |
| `intent_template_id: 322` L4263 | 4263 | confirmed |
| stratum `(["gitlab"], ["string_match"])`, n=43, minimum ID 132 | independent census: 43, min 132 | confirmed |
| 132 in `selected-task-ids.json` position 3 | third element | confirmed |
| siblings 205/134/303/135/207: template, question, reference | tpl 320/322/321/322/320; intents and refs `1/0/1/1/1` exactly as tabled | confirmed |
| 36 tasks mention `a11yproject`; 15 have `program_html` | 36; 15, IDs 390 391 392 416 417 446 450 568 578 658 668 805 806 809 811 exactly | confirmed |
| those 15 are comment/issue/MR/membership/profile edits; none `require_reset` | intents checked one by one; all `require_reset: false` | confirmed |
| `evaluator_router` L355–L374, `string_match`→`StringEvaluator()` L365–L366 | exact | confirmed |
| `EvaluatorComb.__call__` L341–L352 multiplies | `score *= cur_score` L351 | confirmed |
| `StringEvaluator.__call__` L123–L170; `get_last_action` L47–L56; `pred` L134 | exact | confirmed |
| `clean_answer` L79–L86 (strip, one quote pair, lowercase) | exact | confirmed |
| `must_include` L96–L111; L103–L109 token branch; L109 return | exact | confirmed |
| only key `must_include` L142–L149; `tokenize=(len(value) == 1)` L148 | exact | confirmed |
| unreached `fuzzy_match`/N/A/`ua_match` L150–L169; judges L146–L173, L176–L208 | exact | confirmed |
| `word_tokenize` import L13 | L13 | confirmed |
| helper import-time deps L1–L20 (`requests`, `browser_env.env_config`, `llms.providers.openai_utils`) | L6–L20 | confirmed |
| hash table prefixes/suffixes | all three consistent with full sha256 above | confirmed |

No source-line number, quote, task count, stratum size, position, or sibling field in `Task132.md` is
wrong.

### Decisive boundary and controls

Predicate for 132, read statically: `eval_types == ["string_match"]` routes one `StringEvaluator`;
`reference_answers` has one key `must_include` with a one-element list; hence `tokenize = (len(["1"]) ==
1) = True`; `clean_ref = "1"` has length 1; `word_tokenize("1")` is a single token. The token branch
(L103–L109) is therefore selected, and the score is 1.0 iff `"1"` is a member of
`word_tokenize(clean_answer(clean_answer(answer)))`; otherwise 0.0 (only one approach multiplies into
the initial 1.0).

- **Branch discriminator (decisive):** the answer `11` (and `10`). Token branch → 0.0; the substring
  branch (`clean_ref in clean_pred`, used whenever `tokenize` is false or the reference is not one
  character) would return 1.0 because `"1" in "11"`. The case's “`11` … fails” is exactly the
  observable that separates the branches; it is true only because Treebank-style tokenization keeps
  `11` as one token.
- **False-pass control:** `0 or 1` contains the standalone token `1` and passes, so “absence of other
  numbers or hedges” is genuinely unchecked, as the case states.
- **Population control that the branch is data-driven, not a default:** 78 pinned tasks carry
  multi-entry `must_include` lists (→ `tokenize=False`, substring branch); 31 tasks carry single
  one-character `must_include` references (→ token branch), including 132, 133, 134, 135, 205, 207.
  So 132's branch follows from its one-entry list, not a global scorer default.
- **Sibling control:** task 134 uses the same template (322) and operator with reference `0`;
  the `10`-vs-`0` relation mirrors 132's `11`-vs-`1` relation.

All of this is static source reasoning; NLTK was not executed (none is installed here), so the
tokenizer-dependent members remain inferences, as the case labels them.

## Findings

**F1 (non-material, evidence class).** `Task132.md:64` introduces “The following follow directly from
the code” and line 67 puts `11`/`10` failures there. That failure is contingent on the tokenizer not
splitting `11`/`10`; the report's own limitation (L109) promises `[INFERENCE]` for “NLTK behavior
beyond the single-character `"1"` token branch”. The decisive control is thus in the direct-code list
while its enabling assumption is unexecuted. The claim itself agrees with Treebank tokenization and
with the case's runtime-replay item 6 (L101); this is a labeling inconsistency, not a false claim.

**F2 (non-material, scope gloss).** `Task132.md:82,86` gloss tasks 205/207 as “all repos”. Their
intents contain no repo token, and `start_url` for 205–207 and 303–307 is
`__GITLAB__/a11yproject/a11yproject.com` (132/134/135 use `__GITLAB__`). “All repos” is one possible
reading, not source text. Consequently L88's “single Kilian commit in 2023” is stronger than the raw
bytes support; the defensible form is “a single Kilian commit to a11yproject in 2023”. Under the
project-scoped reading the sibling set is still consistent with 132 and with either M/D or D/M
handling of `3/5/2023`, so the case's verdict is unchanged.

**F3 (residual unknown, chain link).** The scorer reads whatever `config_file` it is handed at
evaluation time. The pinned snapshot contains only `config_files/test.raw.json`; no generated per-task
config is pinned, so preservation of the raw `eval` block into the eval-time config is assumed, not
observed. The case is explicitly scoped to the raw static spec, so this is an unlisted residual
dependency rather than a contradiction; it belongs on the runtime-evidence list (items 1–7 do not
mention it).

**F4 (instrument-side note, not a case claim).** The delivered instrument's per-task record for 132
emits `url_note: "GOLD in PRED"` although the raw task has no `url_note` key and no URL evaluator is
routed. The record also preserves the complete `raw_task` (absence visible), and the default mirrors
`evaluators.py:215` `configs["eval"].get("url_note", "GOLD in PRED")`. This does not affect
`Task132.md`, which correctly says no `url_match` check exists.

## Candidate case-specific language

The frozen candidate (`corpus/knowledge` canonical target path
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/webarena-task-spec-audit.md`, not yet
admitted; bytes under test are the `.ufo/waves/round-28/drafts/` file hashed above) mentions task 132
in only two places: the persisted-ID list (line 60) and the case-table row “`tokenized numeric
answer`” (line 70). That boundary description is supported by the source predicate above; the
candidate asserts nothing else about 132, so its case-specific language does not exceed source.

Candidate aggregate counters were independently reproduced from the pinned bytes (not from the
instrument): 812 tasks / 812 distinct IDs, IDs 0–811; 5 evaluator-type sets (325/66/282/10/129); 27
strata; selected16 exactly the persisted list; 651 page-content targets; string operators
exact_match 45 / must_include 176 / fuzzy_match 118; HTML operators 188 + 463; locator classes
full-page 105 / JavaScript 524 / helper 22; URL classes last 238 / navigation 338 / helper 75. All 16
named case-report files exist (`Task007/044/097/132/173/356/377/389/399/424/552/556/590/681/759/791.md`).
The candidate's “shopping site is omitted” holds (task 759 is `shopping_admin`, a distinct site).

## Not claimed

No browser action, site request, scorer execution, or benchmark score. Nothing here establishes task
132 as runtime-valid or invalid. `PARTIAL` in `Task132.md` for task-level validity remains the only
defensible verdict absent the runtime evidence it lists.

## Verdict

**VERDICT: PASS** — for BUILD case132 as a static task-spec/evaluator audit. Every source-line number,
quote, count, stratum claim and sibling field is byte-confirmed, and the intent→operator→target→
unchecked mapping is correct; the decisive token-branch control was identified and its population and
sibling controls confirmed. F1 and F2 are non-material wording/evidence-class caveats that L1 may fold
into an errata line if desired; F3 is a residual unknown; none changes any conclusion of the case.
No falsification of the candidate's case-132 language was found.
