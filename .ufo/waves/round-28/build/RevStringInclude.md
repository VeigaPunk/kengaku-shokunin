# RevStringInclude — StringEvaluator `must_include` (tokenize branch + list conjunction) scorer contract + audit cases

- **Seat / writer:** `KengakuR28.RevStringInclude-2` (reviewer leaf, author-side; no subagents dispatched)
- **Date:** 2026-10-21
- **Scope:** Review exactly the pinned WebArena `StringEvaluator.must_include` primitive — the `tokenize` conditional branch, the `reference_answers.must_include` list conjunction in `StringEvaluator.__call__`, and the exact length conditions governing each — plus `clean_answer` and the `reference_answers` match-dispatch that feeds it. Produce a source-anchored scorer contract plus concrete hand-expected schema/semantic cases for the C1 audit (`plans/benchmark_spec_audit.py`). Static source/JSON analysis only; no upstream code executed or imported.
- **Source opening (access date 2026-10-21, ≤25-word located quotes below):**
  - S062 `evaluation_harness/evaluators.py`, pinned upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b` — quote (lines 104–107, verbatim): *“tokenize and len(clean_ref) == 1 and len(word_tokenize(clean_ref)) == 1”* — scope: the tokenize-branch predicate only.
  - S061 `config_files/test.raw.json`, same revision — quote (task 132, `reference_answers`): *“{"must_include": ["1"]}”* — scope: illustrative tokenize-eligible reference sampling.
  - S063 `evaluation_harness/helper_functions.py`, same revision — quote (lines 215–217): *“if "different" in response: return 0.0 … else: assert "same" in response”* — scope: `llm_ua_match` return contract reached by the `fuzzy_match=="N/A"` arm.
- **Snapshot integrity (observed):** `sha256sum` of the manifest-listed files reproduces `plans/fixtures/r28/webarena/manifest.json` exactly (`test.raw.json` 7b50386f…37652, `evaluators.py` e23edb39…0c22, `helper_functions.py` ec758da4…e275). All counting below ran on this verified input.
- **Tools used:** preinstalled `python3` (stdlib `json`, `collections`, `re`) and `sha256sum`/`grep` for read-only counting over the frozen snapshot; no installs, no pacman, no network, no benchmark sites contacted. NLTK/beartype/playwright are **not installed** on this host — `evaluators.py` could not be imported here; every semantic claim below is a hand-derivation from the pinned text, and every NLTK-dependent expectation is marked instrument-conditional rather than asserted.
- **Limitation:** every count is a static census of the pinned snapshot: scorer-contract evidence, not runtime/browser truth, and not a task-validity verdict.

---

## 1. Scorer contract (source-anchored, evaluators.py @ dce04686)

### 1.0 Upstream routing and the pred pipeline

1. `evaluator_router` (evaluators.py:356–374) instantiates `StringEvaluator()` only for the literal `eval_types` member `"string_match"` (line 366). Tasks lacking `"string_match"` in `eval_types` never reach `must_include` at all — a routing fact, not a field-presence fact.
2. `StringEvaluator.__call__` (lines 123–170): `pred = self.clean_answer(last_action["answer"])` where `last_action = trajectory[-1]` via `get_last_action` (lines 44–55, comment `is_bearable(trajectory[-1], Action)`). A `trajectory` whose last element is not an action, or whose `answer` key is missing, crashes (KeyError/no typed fallback) — there is no score-0 path for malformed trajectories.
3. `score = 1.0`; the loop iterates `configs["eval"]["reference_answers"].items()` **in JSON insertion order** and multiplies per-approach sub-scores (line 136).
4. `EvaluatorComb` multiplies across routed evaluators (lines 340–352), so `string_match` ANDs with any `url_match`/`program_html` co-routing.

### 1.1 `clean_answer` (lines 80–87) — applied to ref and pred, and applied TWICE to pred

- Bare single char `"` **does** match the conditions: `'"'` both starts and ends with `"`, so `clean('"')` = `''` (same for `'`). An agent answering literally `"` produces the empty pred, which then fails every non-empty ref and passes every vacuous one.

- `clean_answer` is **not idempotent**: `clean(clean('"a"'))` = `clean("'a'")` = `a`, while `clean('"a"')` = `'a'`. This matters because `__call__` already cleaned `pred` at line 132, and `must_include` cleans it again at line 100 — the prediction is effectively double-cleaned while the reference is single-cleaned. `pred='"done"'` → `clean` → `'done'` → `clean` → `done`.
- Bare single char `"` (one quote) does not match the 2-char `startswith/endswith` conditions — wait, it does: `'"'` both starts and ends with `"`, so `clean('"')` = `''`. Same for `'`. An agent answering literally `"` produces the empty pred, which then fails every non-empty ref and passes every vacuous one.
- Interior whitespace and punctuation are preserved verbatim; only the two extremes are trimmed and only one quote layer is removed.
- Case-folding is `.lower()` — ASCII plus Unicode lowercase; there is no `.casefold()` and no diacritic/punctuation normalization.

### 1.2 `must_include` primitive (lines 98–112) — the tokenize conditional, exactly

```python
def must_include(ref: str, pred: str, tokenize: bool = False) -> float:
    clean_ref  = clean_answer(ref)    # line 99
    clean_pred = clean_answer(pred)   # line 100
    if (tokenize                      # line 104
        and len(clean_ref) == 1       # line 105  — cleaned-reference length
        and len(word_tokenize(clean_ref)) == 1):   # line 106 — near-dead guard
        tok_pred = word_tokenize(clean_pred)       # line 108
        return float(clean_ref in tok_pred)        # line 109 — exact TOKEN membership
    else:
        return float(clean_ref in clean_pred)      # line 111 — plain SUBSTRING
```

- **Two disjoint length conditions, and they are NOT the same variable**: `tokenize` (the flag) is set by the *list* length at the call site (`len(value) == 1`, line 148); the branch additionally requires the *cleaned ref* to be a single character (`len(clean_ref) == 1`). A length-1 list whose ref is multi-char (e.g. `["914km"]`, task 97) takes `tokenize=True` into the call and still falls through to **substring**.
- **The `len(word_tokenize(clean_ref)) == 1` guard is near-dead**: for a 1-character string, NLTK `word_tokenize` returns a 1-element list in every expected case (digits, letters, punctuation). It exists to exclude pathological single chars; it does not extend the branch to multi-char refs. An audit MUST NOT model this arm as "any single-token ref" — the `len(clean_ref)==1` clause already killed that reading.
- **Tokenize branch = exact token membership**, `clean_ref in word_tokenize(clean_pred)`: `'1' in ['q1']` is False, `'1' in ['10']` is False, `'1' in ['1','0']` is False. This is the stated "prevent false positive (e.g, 0)" motivation (comment lines 102–103): without it, ref `"0"` substring-matches inside `"10"`, `"305"`, `"v0.1"`.
- **Substring branch = `clean_ref in clean_pred`**, plain case-insensitive containment: no word boundaries, interior-whitespace-sensitive, `"914km" in "914 km"` is False (task 97 hazard: `reference_answer_raw_annotation` is `"914 km"` — with a space — while the checked ref is `"914km"`).
- **Vacuous truth:** `"" in x` is `True` for every `x`, including `""`. A ref that cleans to `""` (`""`, `"''"`, `'""'`) is an unconditional pass; corpus count 0 (§2).
- `beartype` enforces `ref: str, pred: str` — non-string refs raise at call time, not score 0.

### 1.3 The `__call__` conjunction (lines 136–150)

```python
case "must_include":                       # line 142
    assert isinstance(value, list)         # line 143 — crash, not score 0
    for must_value in value:               # line 144
        score *= self.must_include(        # line 145
            ref=must_value, pred=pred,
            tokenize=(len(value) == 1),    # line 148 — LIST-length conditional
        )
```

- **AND across list elements:** the loop multiplies each element's 0/1 into `score`; any failure ⇒ task score 0.0. There is **no `|OR|` splitting on this path** — the split lives only in `HTMLContentEvaluator` (lines 316–326). Literal `" |OR| "` inside a `reference_answers.must_include` ref is matched literally (task 386's `"65 |OR| 3"` is the sole observed instance — a probable authoring transplant from the program_html convention; surfaced as an observation, not adjudicated as a defect).
- **`tokenize` is a per-list flag, not per-ref**: `(len(value)==1)` — length-1 lists pass `tokenize=True` for their single ref; lists of ≥2 refs pass `tokenize=False` for every element. Consequence: the single-char protection exists **only** in length-1 lists; a digit ref inside a multi-element list would lose it. Observed corpus: all 31 cleaned-single-char refs sit in length-1 lists, so the branch covers exactly the intended population — but this is a corpus fact, not a contract guarantee.
- **`assert`, not a finding:** a non-list `must_include` value raises `AssertionError` (unscorable crash). Under `python -O` the assert is stripped and a bare string would iterate per-character as refs — a deployment-mode hazard; corpus count 0.
- **`reference_answers` must be a dict** for `string_match`-routed tasks: `.items()` at line 137 raises `AttributeError` on `null`. Observed corpus invariant: `reference_answers` is a dict **iff** `"string_match"` ∈ `eval_types` (dict 335 = string_match-routed 335; null 477 = all non-string_match tasks). Key is present in all 812 eval blocks.
- **Unknown `reference_answers` keys are silently ignored**: the `match` has no default arm, so `{"must_includ": [...]}` yields score 1.0 for the string_match component — a silent pass the audit must flag.

### 1.4 Order-sensitive edge (documented, corpus-dead)

In the `fuzzy_match` arm, when `value == "N/A"` and `exact_match("N/A", pred)` fails, the code executes `score = 1.0 * self.ua_match(...)` (line 159) — an **overwrite**, not a multiply: any earlier approach's failure (e.g. a failed `must_include` earlier in dict order) would be resurrected by `ua_match`'s result. In the observed corpus every `fuzzy_match:"N/A"` task is single-key (36 tasks, all `("fuzzy_match",)`), and all 4 multi-key tasks (34/35/267/268) carry list-valued fuzzy refs with `must_include` first — so the overwrite is reachable in source but dead at this pin. The audit should still model the overwrite faithfully rather than "fix" it, and should report per-task reference_answers key order.

---

## 2. Observed population facts (static census, verified hashes; denominators explicit)

Population: 812 raw tasks. Facts the new audit must reproduce exactly (scratch copy: `.ufo/waves/round-28/scratch/KengakuR28.RevStringInclude-2/must_include_census.json`):

| # | Fact | Value |
|---|------|-------|
| R1 | tasks with `reference_answers` key present | 812 (always present) |
| R2 | `reference_answers` = dict / `null` | 335 / 477 |
| R3 | dict `reference_answers` ⇔ `"string_match"` ∈ `eval_types` | exact correspondence (335/335; no null-RA string_match task, no dict-RA non-string_match task) |
| R4 | `reference_answers` operator sets | `{must_include}` 172, `{fuzzy_match}` 114, `{exact_match}` 45, `{must_include,fuzzy_match}` 4 |
| R5 | tasks using `must_include` | 176 |
| R6 | `must_include` non-list values / non-string items / empty lists | 0 / 0 / 0 |
| R7 | `must_include` list-length histogram | 1:98, 2:36, 3:13, 4:6, 5:6, 6:10, 7:1, 8:1, 9:1, 10:1, 11:1, 14:2 |
| R8 | lists where `tokenize=True` is passed (len==1) | 98 |
| R9 | lists where the tokenize branch actually fires (len-1 list **and** cleaned ref is 1 char) | **31** — task IDs 11,12,13,14,15,27,28,29,30,31,77,79,128,132,133,134,135,136,144,205,206,207,292,303,305,306,319,329,346,348,787; every firing ref is a single digit `0/1/2/5/6/9` |
| R10 | single-char cleaned refs inside multi-element lists (unprotected) | 0 |
| R11 | `must_include` refs containing literal `" |OR| "` | 1 — task 386 `"65 |OR| 3"` (length-1 list; tokenize passed, ref len>1 ⇒ substring of the literal incl. `|OR|`) |
| R12 | `must_include` items altered by `clean_answer` (trim/quote/case-fold) | 238 — dominated by case-folding; none clean to `""` |
| R13 | `fuzzy_match` value shapes | bare `"N/A"` 36 (all single-key, all with non-empty `string_note`); list-of-refs 82; no other shapes |
| R14 | multi-key `reference_answers` order | tasks 34,35,267,268 — `must_include` first, `fuzzy_match` second; fuzzy values are lists ⇒ N/A-overwrite arm not reached |
| R15 | selected-16 `must_include` exposure | **132** (`["1"]`, len-1 + 1-char ⇒ tokenize branch fires), **97** (`["914km"]`, len-1 + multi-char ⇒ `tokenize=True` passed but substring executes); 791 exercises `fuzzy_match:"N/A"`+`ua_match`; 173 exercises list `fuzzy_match`; 7 exercises `exact_match`; remaining 11 selected IDs route no `string_match` |

**R9 is the load-bearing fact for this slice:** the `tokenize` branch is exercised by exactly 31 of 812 tasks, all digit refs, all in length-1 lists — and task 132 is in the frozen 16. The audit's tokenize-eligibility stratum must be computed as `len(value)==1 ∧ len(clean(ref))==1` (a *candidate* stratum; actual firing is NLTK-conditional, §4).

---

## 3. Concrete hand-expected cases for the new audit

### 3.1 Schema/static cases (miniature tasks; hand-expected finding/exit per §1 contract)

| Case | Miniature `eval` fragment | Expected audit result |
|---|---|---|
| S1 | `"eval_types": ["string_match"], "reference_answers": null` | `ra_null_for_string_match` finding (runtime `.items()` AttributeError, line 137); pin count 0 |
| S2 | `"reference_answers": {"must_include": "0"}` (scalar) | `mi_non_list` finding (AssertionError at line 143; under `-O`, per-char iteration); pin count 0 |
| S3 | `"must_include": [0]` (non-string item) | `mi_item_non_string` (beartype `ref: str`); pin count 0 |
| S4 | `"must_include": []` | `mi_empty_list` advisory — vacuous full pass for that approach; pin count 0 |
| S5 | `"must_include": ["a", 3]` mixed | same `mi_item_non_string` class |
| S6 | `"reference_answers": {"must_includ": ["x"]}` | `ra_unknown_key` finding — **silent pass** (no match default, line 137–168); MUST be exit-1-capable |
| S7 | `"reference_answers": {}` on string_match | `ra_empty` advisory — score 1.0; pin count 0 |
| S8 | `"must_include": ["''"]` or `[""]` | `vacuous_ref` advisory (`"" in x` always True, §1.2); pin count 0 |
| S9 | `["0"]` (len-1, 1-char digit) | `tokenize_candidate` stratum — audit must report branch candidacy AND flag that firing is NLTK-conditional; 31 pin instances (R9) |
| S10 | `["0", "x"]` (1-char ref in multi list) | `tokenize_disabled` finding — tokenize=False (§1.3); `"0"` raw-substring matches `"10"`/`"305"`; pin count 0 |
| S11 | `["10"]` (len-1, multi-char) | `tokenize_ineligible` — `tokenize=True` passed but `len(clean_ref)==1` fails ⇒ substring; matches inside `"110"`/`"100"`; 67 len-1 non-firing lists in pin incl. task 97 `"914km"` |
| S12 | ref containing `" |OR| "` | `or_token_in_ra` advisory — literal match on this path; pin instance task 386 only |
| S13 | multi-key `{"must_include": [...], "fuzzy_match": "N/A"}` | `na_overwrite_risk` finding — ua_match overwrites prior score (line 159, §1.4); pin count 0, all 4 multi-keys are list-fuzzy |
| S14 | snapshot hash ≠ manifest | instrument exit 2 `snapshot_tampered` before any counting (prereg line 15) |
| S15 | `fuzzy_match` scalar other than `"N/A"` (e.g. `"yes"`) | `fuzzy_scalar_non_na` finding — assert at line 165; pin count 0 |

### 3.2 Semantic micro-model cases (pure reimplementation vs. hand-computed expectations; never import upstream)

Model: `pred = clean(clean(last_action["answer"]))` (double-clean via line 132 + line 100); per ref, `score *= tok-or-substr(ref, pred)`.

| Case | last_action answer | `must_include` value | Expected |
|---|---|---|---|
| M1 | `"the answer is 1"` | `["1"]` | **1.0** — tokenize arm, `['1'] ⊆ tokens` (NLTK-conditional expectation; canonical punkt tokens `[the,answer,is,1]`); without tokenize this same case = 0.0 — this is THE discriminator case |
| M2 | `"the answer is 10"` | `["1"]` | **0.0** under tokenize arm; would be 1.0 under substring — encodes the false-positive motivation |
| M3 | `"Q1 revenue"` | `["1"]` | **0.0** under tokenize (`'1' ∉ ['q1']`); substring would give 1.0 |
| M4 | `"score: 1,000"` | `["1"]` | **0.0** (punkt keeps `'1,000'` one token); documents NLTK-version sensitivity — mark instrument-conditional |
| M5 | `"It costs 10 dollars"` | `["0"]` | **0.0** tokenize vs **1.0** substring — pair with M2 as the branch-boundary pair |
| M6 | `"Yes, done"` | `["yes", "done"]` | 1.0 (AND, both substrings) |
| M7 | `"Yes"` | `["yes", "done"]` | 0.0 (one conjunct fails) |
| M8 | `"cart"` | `["art"]` | **1.0** — substring has no word-boundary protection when len>1 or list len>1 |
| M9 | `"Foo  bar"` (two spaces) | `["foo bar"]` | **0.0** — interior whitespace sensitive |
| M10 | answer `'914 km'` | `["914km"]` | **0.0** — task 97's exact hazard (annotation `"914 km"`, ref `"914km"`) |
| M11 | answer `'"done"'` (double-quoted in a quoted string) | `["done"]` | 1.0 — pred is double-cleaned: `'"done"'`→`'done'`→`done`; reimplementation must reproduce the DOUBLE clean to stay same-identity |
| M12 | answer `"` (a lone quote char) | `["done"]` | 0.0 — pred cleans to `""` (one quote layer strips to empty) |
| M13 | answer `"done"` | `["''"]` → cleans to `""` | 1.0 — vacuous ref always passes (pair with S8) |
| M14 | answer `"The rating is 65 or 3"` | `["65 \|OR\| 3"]` | **0.0** — literal `|OR|` on this path (task 386); only the exact literal string `"65 |OR| 3"` (case-folded) scores 1.0 |
| M15 | answer `"DONE!"` | `["done"]` | 1.0 — case-fold both sides; `done!` still contains `done` (trailing punctuation OK for substring) |

### 3.3 Selected-ID expectations

- **Task 132** (gitlab, `string_match`, `must_include ["1"]`, intent "How many commits did kilian make to a11yproject on 3/5/2023?"): case report must state the tokenize branch **fires** (len-1 list, 1-char ref) — correct answer `"1"` passes, `"10"`/`"Q1"` fail; expected M1/M2/M3 behavior. Static fact: tokenize-candidate; firing is NLTK-conditional.
- **Task 97** (map, `string_match`, `must_include ["914km"]`): `tokenize=True` passed, ref len 5 ⇒ substring executes; `"914 km"` fails — surface the annotation-vs-ref whitespace divergence as observation, not FAIL.
- **Task 791** (`fuzzy_match:"N/A"`, `string_note:"the subreddit does not exist"`): exercises the N/A exact-match arm + `ua_match` fallback; both LLM-dependent arms are unverifiable statically.
- **Tasks 173, 7**: list-`fuzzy_match` and `exact_match` arms respectively — `must_include` absent; report as adjacent-arm coverage only.
- Remaining 11 selected IDs: no `string_match` routing ⇒ `must_include` is dead configuration for them; state "not scorer-active," never count field presence.

## 4. What a static task-spec inventory cannot prove (explicit non-claims)

1. **NLTK `word_tokenize` behavior** — the audit cannot execute it (no import, no punkt data, not installed on this host). The 31 tokenize-candidate tasks are a *candidate* stratum; whether each ref actually takes the token branch, and every M1–M5 expectation, is instrument-conditional on the pinned NLTK version and tokenizer data.
2. **LLM-judgment outcomes** — `llm_fuzzy_match`/`llm_ua_match` call GPT-4-turbo (helper_functions.py:143–221); 114+82 list-fuzzy and 36 N/A tasks have no static truth for the fuzzy arm.
3. **Runtime trajectory shape** — whether `trajectory[-1]` is an `Action` carrying a string `answer`; crashes vs scores are runtime-only.
4. **Semantic correctness** — substring/token match passing says nothing about whether the ref is *discriminating* or the task *achievable* (task 97 `"914km"`, task 386 `"65 |OR| 3"` are divergences to surface, not adjudicate). No validity counting from field presence (R3's null-vs-dict strata are schema facts, not task quality).
5. **Deployment flags** — `python -O` strips the `isinstance` asserts (line 143,165), changing non-list/non-string behavior from crash to silent per-char iteration; unverifiable statically.
6. **Import graph availability** — `evaluators.py` imports `browser_env.*`, `llms.providers.openai_utils`, playwright, beartype, nltk — all outside the pinned snapshot; presence/absence of these at deployment is outside C1 evidence.
7. **Dict-order reliance** — insertion order is JSON-parse-order dependent; harmless at this pin (R14) but the audit must record order, not assume it.
8. **Whether `|OR|` in task 386 was intended** — plausible transplant of the program_html convention; static analysis surfaces it, cannot prove authoring intent or benchmark invalidity.

## 5. Recommended checks for `benchmark_spec_audit.py` (`string_match`/`must_include` slice)

- **B1 hash-gate first:** verify manifest sha256s before counting; mismatch ⇒ exit 2 `snapshot_tampered` (prereg line 15).
- **B2 AST-contract extraction:** via `ast.parse` (never import) extract — (a) `must_include` default `tokenize=False` (line 98); (b) the exact branch predicate `tokenize ∧ len(clean_ref)==1 ∧ len(word_tokenize(clean_ref))==1` (lines 104–107); (c) call-site flag `tokenize=(len(value)==1)` (line 148); (d) `assert isinstance(value, list)` (line 143); (e) no `|OR|` split inside `StringEvaluator.__call__` (the split exists only at lines 316–326 in `HTMLContentEvaluator`); (f) `match` arms `{exact_match, must_include, fuzzy_match}` with **no default** (lines 139–168); (g) the `score = 1.0 * self.ua_match(...)` overwrite (line 159).
- **B3 per-task schema checks:** R1–R14 census exactly (operator sets, list-length histogram, tokenize-candidate stratum defined as `len(list)==1 ∧ ∃ref: len(clean(ref))==1`, OR-token refs, clean-altered refs, null-vs-dict RA by eval_types).
- **B4 findings vocabulary (stable names):** `ra_null_for_string_match`, `mi_non_list`, `mi_item_non_string`, `mi_empty_list`, `vacuous_ref`, `ra_unknown_key`, `ra_empty`, `tokenize_candidate`, `tokenize_disabled`, `tokenize_ineligible`, `or_token_in_ra`, `na_overwrite_risk`, `fuzzy_scalar_non_na`.
- **B5 micro-model selftest:** §3.2 M1–M15 as a pure-stdlib reimplementation scored against hand expectations; M1–M5 must carry an `nltk_conditional` marker, and the tokenizer side may be modeled with a documented minimal stub (digit/letter/punct splitting) whose divergence from real NLTK is listed as a selftest limitation — never by importing nltk or upstream.
- **B6 oracle separation:** the independent oracle writer re-derives §3.1 expected findings and R1–R14 counts without reading the production implementation (prereg line 21).
- **B7 exit discipline:** schema findings ⇒ exit 1; tampered/missing input ⇒ exit 2 stable codes; summary carries scope + §4 non-claims verbatim.
- **B8 case-report fields:** for tasks 132/97/791 (and 173/7) record intent, exact operator list, list lengths, `tokenize` flag actually passed, whether the branch predicate is met, what remains unchecked (NLTK, LLM, trajectory), source location.
- **B9 must not:** import/execute upstream code or nltk; issue network/browser actions; treat `|OR|` as valid in `reference_answers`; model tokenize as per-ref or as "single-token ref"; count task validity from field presence; convert the task-97/386 divergences into benchmark FAILs.

## 6. Verdict

**PASS (scoped)** — for the reviewed slice only: `StringEvaluator.must_include`'s tokenize branch, its list-length conditional, and the `reference_answers` conjunction are fully traceable to `evaluators.py` @ dce04686 (§1, exact line anchors), the pinned population reproduces consistent aggregates on hash-verified input (§2, incl. the sharp R9: 31 tokenize-candidate tasks, all single-digit refs in len-1 lists, incl. selected task 132), and §3 supplies concrete hand-expected schema/semantic cases sufficient to build and self-test this audit slice without executing upstream code. Two same-identity corners must be reproduced, not cleaned: pred is **double-cleaned** (M11/M12), and the `fuzzy_match:"N/A"` arm **overwrites** rather than multiplies prior score (§1.4, corpus-dead). Residual risks: (a) all 31 tokenize-branch semantics are NLTK-conditional — the audit reports candidacy, not firing truth; (b) unknown RA keys are silent passes — audit must catch what the scorer cannot; (c) `-O`-stripped asserts change failure mode from crash to silent iteration; (d) this verdict covers the `must_include`/string-match contract slice only — it is not a blanket round PASS, not browser truth, and not a task-validity judgment.

---
report-by: KengakuR28.RevStringInclude-2 — seat review, author-side advice, not outside non-author closure. Paths relative to lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Sources: `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` (S062), `plans/fixtures/r28/webarena/config_files/test.raw.json` (S061), `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` (S063), opened 2026-10-21 at pinned revision dce04686a56253aefba7b18a4fa0937cf1dc987b. Scratch evidence: `.ufo/waves/round-28/scratch/KengakuR28.RevStringInclude-2/must_include_census.json`.
