# RevStringFuzzy — StringEvaluator fuzzy_match / N/A / ua_match contract review

- Writer/seat: KengakuR28.RevStringFuzzy-2 (reviewer, author-side; no outside closure)
- Scope: exactly `StringEvaluator` type-dependent branches (`exact_match`, `must_include`, `fuzzy_match` scalar `"N/A"` + `ua_match`, `fuzzy_match` list), judge dependence, and what the round-28 static task-spec audit can and cannot prove. Read-only; no upstream code executed, no benchmark sites contacted.
- Pinned inputs (hashes verified locally with `sha256sum`, all match `manifest.json`):
  - `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` sha256 `e23edb39…00c22`, url `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py`, opened 2026-10-21. Located quote (≤25w): `"fuzzy match: the answer is similar to the reference answer, using LLM judge"` (evaluators.py:75).
  - `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` sha256 `ec758da4…9e275`, same base url, opened 2026-10-21. Located quote: `"Check whether the prediction matches the reference with GPT4-turbo"` (helper_functions.py:147).
  - `plans/fixtures/r28/webarena/config_files/test.raw.json` sha256 `7b50386f…37652`, 812 tasks, opened 2026-10-21.
- Commands run (read-only, fixture-local): `python3` json counters over `test.raw.json`; `sha256sum` on the four pinned files. No installs, no network, no upstream execution, no builds/tests.

## 1. Source-anchored contract (evaluators.py, line-cited)

Entry: `evaluator_router` (lines 356–373) instantiates `StringEvaluator` iff `"string_match" ∈ eval.eval_types`; `EvaluatorComb` (340–352) multiplies every evaluator's score, so a `KeyError`/`AssertionError` inside `__call__` is a hard crash, not a 0.0 score — and is invisible to the task JSON.

`StringEvaluator.__call__` (123–170):

1. `pred = clean_answer(last_action["answer"])` (134): `KeyError` if the final Action has no `answer`; `clean_answer` (80–86) strips only a *matching outer quote pair* (`'…'` or `"…"`) then lowercases. Asymmetric `"abc'` is untouched; `'n/a'` cleans to `n/a`.
2. Iterates `configs["eval"]["reference_answers"].items()` (137). **Field-presence hazard:** `reference_answers: null` → `AttributeError` on `.items()`; `reference_answers: {}` or an *unknown* approach key → vacuous `score = 1.0` (match-case has no default). A task can "pass" with zero effective checks — the audit must flag both null and empty/unknown keys, not just presence.
3. `exact_match` (139–140): `value` must be a string usable by `clean_answer`; equality is on cleaned (lowercased, quote-stripped) forms. A non-str value crashes inside `clean_answer.strip()`.
4. `must_include` (142–149): `assert isinstance(value, list)` (143) — the `assert` **is** the schema check; non-list → `AssertionError`. Per-element `must_include` (98–111): `tokenize` is on **only when the list has exactly one element** (`tokenize=(len(value)==1)`), and even then only when `len(clean_ref)==1 and len(word_tokenize(clean_ref))==1` — i.e. tokenized comparison applies to single-*character* refs, a weaker gate than the comment's "single word" claim (101–102). Otherwise plain substring `clean_ref in clean_pred`. Note: a single-element list `["a"]` → tokenized; `["a","b"]` → substring per element.
5. `fuzzy_match` (150–169) — the type-dependent fork:
   - `value == "N/A"` (152): `score *= exact_match("N/A", pred)` — requires cleaned pred to equal `n/a` exactly. **If that fails, `score` is *reset*, not multiplied**: `score = 1.0 * self.ua_match(intent, ref=string_note, pred)` (159–163). A prior 0.0 from an earlier-iterated approach key would be overwritten to 1.0 by a passing judge call. Order-dependence: dict iteration is insertion order; a JSON with `{"fuzzy_match":"N/A","must_include":[…]}` could zero-score on `must_include` then resurrect via `ua_match`. (In the pinned corpus all 36 `"N/A"` tasks have `fuzzy_match` as sole key — dormant hazard, but the audit must record key order.) `configs["eval"]["string_note"]` is **only** read on this path → `KeyError` if absent; `configs["intent"]` → `KeyError` if absent.
   - non-`"N/A"` scalar: falls to `assert isinstance(value, list)` (165) → `AssertionError`. `"n/a"`, `"NA"`, `["N/A"]` treated differently — scalar match is **literal, case-sensitive**; list elements are never checked for `"N/A"`.
   - list (166–168): every element independently `fuzzy_match`ed and multiplied — all refs must be judged correct (conjunctive, not disjunctive).
6. Judge dependence (helper_functions.py):
   - `llm_fuzzy_match` (146–173): prompt built from `question=intent`, `reference`, `pred` (note reversed call order at evaluators.py:116 — `llm_fuzzy_match(pred, ref, intent)`); calls `generate_from_openai_chat_completion(model="gpt-4-1106-preview", temperature=0, max_tokens=768)`. Response parse is **substring-based**: `"partially correct" in response or "incorrect" in response` → 0.0 (169–170); else `assert "correct" in response` → 1.0 (172–173). Any other response (empty, refusal, `"unable to determine"`, API error string) → `AssertionError`.
   - `llm_ua_match` (176–208): `"different" in response` → 0.0 (204–205), else `assert "same"`. Substring hazard: a judge reply containing `"indifferent"` or `"not different"` is misclassified (0.0 for the former, assertion-false → 0.0 path for `"not different"` since it still contains `different`).

## 2. Corpus observations (test.raw.json, 812 tasks — counted, not executed)

- `eval_types` strata: `string_match` 325; `program_html` 282; `program_html+url_match` 129; `url_match` 66; `string_match+url_match` 10. (5 sets — matches F2.)
- Every `string_match` task (335 incl. the 10 mixed) has a non-null dict `reference_answers` — no `AttributeError` instance in-corpus.
- Approach keys observed: `must_include` only 172; `fuzzy_match` only 114; `exact_match` only 45; `fuzzy_match+must_include` 4 (tasks 34, 35, 267, 268 — all list-valued, so the score-reset hazard is dormant). No unknown approach keys.
- `fuzzy_match` shapes: literal `"N/A"` 36 tasks; list-of-str 82 tasks (145 string elements, none N/A-like). `must_include` always list-of-str (176 lists, 396 elements). `exact_match` always str (45).
- `string_note` present in **all 335** string_match tasks (empty string in non-N/A tasks, e.g. selected 132/97/173 `''`), so no `KeyError` on the N/A path in-corpus.
- Selected-16 coverage of this seat: 791 = `fuzzy_match:"N/A"` + `string_note:"the subreddit does not exist"` (the only N/A task in the sample); 173 = `fuzzy_match:["No, it is open"]`; 7 = `exact_match` str; 132/97 = `must_include` single-element lists `["1"]`, `["914km"]`. The remaining 11 selected tasks are `program_html`/`url_match` — outside this seat's scope.

## 3. Hand-expected cases for the audit instrument (miniature task dicts → expected audit verdict)

Schema (what the audit's per-task check must accept/flag — the `assert`s at evaluators.py:143/165 define the contract):

- S1 `{eval_types:["string_match"], reference_answers:{exact_match:"x"}, intent:"…"}` → VALID.
- S2 `reference_answers:{must_include:["a","b"]}` → VALID, flag `tokenize off` (len≠1); `{must_include:["a"]}` → VALID, tokenize eligible.
- S3 `reference_answers:{fuzzy_match:"N/A"}` **without** `string_note` → SCHEMA VIOLATION (runtime `KeyError` on the ua path); with `string_note` → VALID.
- S4 `fuzzy_match:"n/a"` or `fuzzy_match:"some scalar"` → SCHEMA VIOLATION (non-N/A scalar → `AssertionError`); `fuzzy_match:{"a":1}` → SCHEMA VIOLATION.
- S5 `reference_answers:{fuzzy_mtch:[…]}` (typo/unknown key) → SCHEMA VIOLATION flag, *not* silently valid: score is vacuously 1.0.
- S6 `reference_answers:{}` or `null` on a `string_match` task → flag (vacuous 1.0 / crash respectively). Conversely `reference_answers` present-but-unused on `program_html`-only tasks is *not* an error (282+129 tasks have `reference_answers` key with null value and no string_match).
- S7 `must_include` empty list `[]` → flag: loop body never runs, vacuous 1.0.
- S8 `string_match` task missing top-level `intent` → flag (`KeyError` on any `fuzzy_match` task; also judge-prompt input).
- S9 multi-approach dict — audit must emit **key order** so the N/A score-reset interaction (evaluators.py:155→159) is reviewable.

Semantic (score arithmetic the audit's case reports may state as pinned contract, clearly labeled static evidence not runtime truth):

- H1 `exact_match` ref `"Pittsburgh … United States"` (task 7) vs pred `"pittsburgh … united states"` → 1.0 (clean lowercases); vs pred missing one word → 0.0.
- H2 `must_include` ref `["914km"]` (task 97) vs pred `"914 km"` → 0.0 (substring, no normalization of whitespace).
- H3 N/A task 791: pred `"N/A"` → 1.0 via `exact_match`, `ua_match` never reached; pred `"I cannot: the subreddit does not exist"` → exact_match fails → `ua_match` called with ref=string_note; score = judge verdict only.
- H4 fuzzy list task 173 `["No, it is open"]`: pred `"it is still open"` → judge call, unparsed-but-plausible `correct` → 1.0; judge `partially correct` → 0.0.
- H5 judge-response edge: reply containing `"not different"` (ua_match) → 0.0 by substring; reply `"the answer is incorrect, mostly correct"` (fuzzy) → 0.0 since `incorrect` checked first; empty/refusal reply → `AssertionError` = task crash, distinct from 0.0.

## 4. What a static task-spec inventory cannot prove

1. Judge behavior: `llm_fuzzy_match`/`llm_ua_match` are external OpenAI calls (helper_functions.py:161–168, 196–203). Correctness, determinism under `temperature=0` (model-side nondeterminism, `gpt-4-1106-preview` deprecation), prompt effectiveness, and cost are all unprovable statically. The audit can only state that scoring for 118 tasks (114 fuzzy-only + 4 mixed) is *judge-mediated*, and 36 of those are `N/A`-gated judge calls.
2. Whether `last_action["answer"]` exists at runtime — depends on agent/harness producing a `stop` answer action; invisible to the JSON.
3. Ground truth of `string_note`/`fuzzy_match` refs (e.g. task 791 claims "the subreddit does not exist") — unverifiable without the sites; must remain an observation, never a task-validity verdict.
4. That a passing score implies task solvability, or a failing task is "invalid" — score arithmetic is defined; task *validity* is not derivable from field presence or schema conformance (per assignment: no validity counting from field presence).
5. Whether asserts ever fire in practice — depends on runtime flags (`python -O` strips the `isinstance` asserts, changing scalar-fuzzy behavior from `AssertionError` to per-char iteration garbage; audit should note, not execute).
6. Non-string_match evaluators' runtime dependencies (network helpers, page state) — outside this seat.
7. The `"N/A"` scalar comparison is case-sensitive/literal — statically provable; but no corpus element violates it, so the branch is exercised only by the hand cases.

## 5. Recommended required code/output checks for `benchmark_spec_audit.py`

- Per-task `string_match` schema check implementing the contract above (S1–S9): typed `reference_answers` dict; approach keys ∈ {exact_match(str), must_include(list[str]), fuzzy_match(str=="N/A" | list[str])}; `string_note`/`intent` required when `fuzzy_match=="N/A"` or any fuzzy; flag unknown keys, empty dicts/lists, non-str elements, `null` reference_answers on string_match tasks.
- Emit: per-approach task counts, `fuzzy_match` scalar-vs-list split, N/A task-id list, mixed-approach key orders, and the `tokenize`-eligibility subset (single-element must_include whose sole cleaned element is a single character — corpus count for the record).
- Exit code discipline per claims.md §C1: schema violations are instrument findings on the task spec, classified as benchmark observations vs instrument defects; never exit0-as-valid on malformed shapes, never invent benchmark FAILs.
- Selftest cases: include S3/S4/S5/S6/S9 and H3 (N/A + string_note gating) as hand-expected miniatures; include a `python -O`-independent schema check (the audit must not rely on assert semantics).
- Case report for task 791 must record the score-reset overwrite (`score = 1.0 * ua_match`, evaluators.py:159) and that the N/A fast path (pred `"N/A"` → 1.0) bypasses the judge entirely.

## 6. Limitations

Static-only review; judge semantics, runtime trajectory shape, and site ground truth unexamined by design. Corpus counts computed by read-only `json.load` + counters — no upstream module imported. The 16-task sample contains only one N/A task (791); N/A-branch generalization rests on the 36-task corpus count, not the sample. Q13-style structural evidence here is not endorsement of upstream scoring choices.

## Verdict

**PASS (scoped).** The pinned StringEvaluator contract is fully statically auditable for schema/branch conformance across all 812 tasks, and the corpus contains no violations of the fuzzy/N/A shape contract (36 `"N/A"` + 82 list tasks all well-typed; string_note/intent present on every string_match task). This verdict covers only the auditability and observed-schema conformance of the fuzzy_match/N/A/ua_match surface — it is not a claim that the 812 tasks are valid, that judge calls succeed, or that the round-28 C1 instrument itself is correct; those await the instrument, oracle, and task-case seats.
