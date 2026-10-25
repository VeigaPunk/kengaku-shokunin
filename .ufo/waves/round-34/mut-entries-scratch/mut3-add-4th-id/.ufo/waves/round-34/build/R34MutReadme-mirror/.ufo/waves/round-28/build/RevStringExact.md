# RevStringExact — StringEvaluator clean_answer / exact_match contract review

- Seat: `KengakuR28.RevStringExact-2` (reviewer, leaf)
- Date: 2026-10-21
- Scope (assigned): `StringEvaluator.clean_answer` + `exact_match` only — normalize-vs-task-contract truth,
  hand-expected schema/semantic cases, static-inventory limits. `must_include`/`fuzzy_match`/`ua_match`
  internals and URL/contract-evaluator deep review belong to sibling seats; I flag overlap points without
  claiming them.
- Pinned inputs (all paths under `plans/fixtures/r28/webarena/`):
  - `evaluation_harness/evaluators.py` sha256 `e23edb39…` — matches `manifest.json` (verified by me via `sha256sum`).
  - `config_files/test.raw.json` sha256 `7b50386f…` — matches manifest.
  - `helper_functions.py` (read; llm_* bodies out of my scope).
- Upstream revision `dce04686a56253aefba7b18a4fa0937cf1dc987b` per manifest. No upstream code executed,
  imported, or eval'd; all census numbers from my own JSON parsing, all clean_answer expectations
  hand-derived by reading the pinned source.

---

## 1. Source-anchored contract (evaluators.py line refs)

### 1.1 `clean_answer` (lines 80–86)
```
answer.strip()
if startswith("'") and endswith("'"): answer[1:-1]
elif startswith('"') and endswith('"'): answer[1:-1]
return answer.lower()
```
Contract, precisely:
- **Strip**: `str.strip()` — removes leading/trailing Python-whitespace *including* `\t`, `\n`, `\r`,
  and Unicode spaces such as `\xa0` (NBSP) and `\u2000–\u200a`. Internal whitespace untouched.
- **Dequote**: at most ONE matched quote pair, and only when the *first and last* characters of the
  already-stripped string are the same quote kind. `if/elif` → single quotes take precedence;
  a `'"…\'` mixed pair is never stripped. Whitespace *inside* quotes is never stripped.
- **Lower**: `str.lower()` — Unicode-aware but NOT `casefold()`; no accent/NFKD normalization.
  `'Norén' → 'norén'`; `'\u0130'` (Turkish İ) → `'i\u0307'` ≠ `'i'`; `'ß' → 'ß'` ≠ `'ss'`.
- **Idempotent? NO.** `clean("' x '") = "' x'"` ≠ `clean("' x'") = "x'"` (second call strips the
  outer pair). This non-idempotence is load-bearing for §2.1.

### 1.2 `exact_match` (lines 90–94)
`float(clean_answer(pred) == clean_answer(ref))` — binary {0.0, 1.0}; symmetric; cleans BOTH sides,
so a *malformed reference* is silently normalized too (untrimmed/quoted refs pass more answers than
the literal bytes suggest — see §4.2).

### 1.3 Routed `StringEvaluator.__call__` (lines 123–170)
- Opens `config_file`, `pred = clean_answer(last_action["answer"])` — **pred is pre-cleaned once
  before the loop**; each approach call then cleans it AGAIN. Effective pred semantics =
  `clean∘clean`; ref semantics = `clean`. Asymmetric pass-count vs direct `exact_match(ref, raw_pred)`.
- Multiplies `score` over every key in `configs["eval"]["reference_answers"].items()` — AND
  composition; order irrelevant since each factor is 0 or 1.
- `match approach:` has NO default case — **unknown reference_answers keys are silently ignored**
  (score unaffected). Instrument must flag them, scorer does not.
- `fuzzy_match == "N/A"` gate is a **case-sensitive literal on the RAW config value** (`if value ==
  "N/A"` line 152): raw `"n/a"` falls into the list branch → `assert isinstance(value, list)` fails →
  crash, not a score. Cross-cutting fact relevant to fuzzy seat; recorded here because it constrains
  schema checks (§5).
- N/A recovery (lines 155–163): exact 'n/a' failure → `ua_match(ref=configs["eval"]["string_note"])` —
  a missing `string_note` key is `KeyError`, not 0.

### 1.4 Second consumer — `HTMLContentEvaluator` (lines 305–310)
`required_contents.exact_match` → `StringEvaluator.exact_match(ref=rc, pred=selected_element)`.
Differences from string path:
- pred = `str(page.evaluate(…))` (line 289) then `html.unescape` (line 303) — **single-cleaned**
  (no `__call__` pre-clean), and entity-decoded. So `program_html` exact_match is MORE lenient on
  entities and LESS lenient on nested/space-inside-quote preds than the routed string path.
- `str()` coercion: JS `null` → `'None'` → cleans to `'none'` (truthy bypass of the `if not
  selected_element` guard at 290); JS `true` → `'True'` → `'true'`; numbers → Python repr
  (`1.0` ≠ `'1'`). A hypothetical rc ref `'none'` would score 1.0 on a locator returning null —
  none exists in the corpus (checked, §3), but the hazard class is real.
- `must_include` under `required_contents` splits each string on `" |OR| "` (line 316) —
  **the `|OR|` alternation exists ONLY in program_html**, not in `reference_answers.must_include`.

### 1.5 Dispatch (`evaluator_router` lines 356–374)
`eval_types` unknown → `ValueError`. `eval_types` is the ONLY gate; `reference_answers` content is
never validated. `EvaluatorComb` multiplies evaluator scores — `['string_match','url_match']` tasks
AND the string and URL checks (10 tasks: 5 exact_match + 5 fuzzy_match).

---

## 2. Normalize vs task-contract truth

### 2.1 Divergence: direct `exact_match` vs routed `__call__` (double-clean asymmetry)
Because clean is non-idempotent, `exact_match(ref, raw_pred)` and the routed path differ:
| ref | raw pred | `exact_match` direct | routed `__call__` (pred pre-cleaned) |
|---|---|---|---|
| `'x'` | `"' x '"` (space inside quotes) | 0.0 | 1.0 |
| `'x'` | `"''x''"` (nested quotes) | 0.0 | 1.0 |
Any test harness driving `exact_match` directly (as selftests likely will) must pin WHICH semantics
it expects; the production path is double-clean.

### 2.2 What the task contract actually is
"exact match" in WebArena is **byte-equality after (strip, dequote×1, lower)** — a normalization
that forgives case, outer whitespace, and one quote wrapper, and nothing else. It is NOT semantic
equivalence: synonyms, unit spacing, punctuation, accents, and reformatting all fail. Whether that
strictness is a defect is a *task-validity* judgment a static audit cannot make; what the audit CAN
state per task is the exact forgiven/unforgiven transformation set.

### 2.3 Selected-16 tasks touching this contract
Only task **7** exercises `reference_answers.exact_match` (map site): ref
`'Pittsburgh International Airport, Southern Beltway, Findlay Township, Allegheny County, 15231,
United States'`. Pred `'pittsburgh international airport, …, united states'` passes; dropping a
comma, `'Pittsburgh International Airport (PIT), …'` insertion, or `'`s around the string pass, but
any word/address-component deviation fails. Task **399** exercises `required_contents.exact_match`
('I am a robot', `.user-bio__biography` outerText). Tasks **356/759** use rc-exact_match `'1'` on
`selectedIndex` — i.e., stringified JS number equality. Tasks **132/97** are `must_include`
(string path), **173/791** fuzzy — outside my exact scope but share `clean_answer`.

---

## 3. Corpus census (my parse of test.raw.json; 812 tasks)

- `eval_types` sets: `string_match` only 325; `program_html` only 282; `program_html+url_match` 129;
  `url_match` only 66; `string_match+url_match` 10. Total distinct sets 5.
- `reference_answers` key sets: `exact_match` 45 (40 string-only + 5 with url_match); `must_include`
  172; `fuzzy_match` 114 (109+5); `must_include+fuzzy_match` 4; absent/empty 477 (all program_html/
  url_match-only tasks — consistent, not a defect).
- `required_contents` key sets across all program_html targets: `exact_match` 188, `must_include`
  463 — the 2-key union is complete; `exact_match` under program_html is actually the LARGER
  exact_match surface (188 vs 45).
- All 45 `reference_answers.exact_match` values are clean strings: no untrimmed, quoted, empty, or
  non-str values; 19 are already-lowercase. Two non-ASCII refs: task 0 `'Quest Lumaflex™ Band'`
  and task 311 `'Erik Linder-Norén'` — predictions must reproduce the accents modulo case.
- `program_html` rc-exact_match values that are str()-coercion-adjacent: `'0'` (≥5 stock/selectedIndex
  tasks), `'true'` (task 521 checkbox `.checked`) — benign since JS 'True'→'true' matches, but
  `None`/`'none'` hazard stands; no `'none'` ref exists today.
- **Task 386 anomaly** (finding F1): `must_include: ["65 |OR| 3"]` with raw annotation "Around 3.1
  stars". `|OR|` alternation is honored ONLY in program_html must_include (line 316), never in
  `reference_answers.must_include` (lines 142–149 treat it as a literal). The literal-cleaned
  substring `'65 |or| 3'` must appear for a pass — spec/intent mismatch evidence worth surfacing in
  the audit's benchmark-observation class (my scope boundary: recorded, not adjudicated).
- Single-char `must_include` refs triggering the nltk `word_tokenize` path (tokenize=True when
  len(list)==1 and cleaned ref is one char): 31 tasks incl. **132** (`'1'`). Static audit must note
  these carry an nltk punkt dependency and different semantics (token membership vs substring).
- All 36 `fuzzy_match:"N/A"` tasks carry a non-empty `string_note` — the ua_match fallback is
  wired; no `KeyError` exposure in corpus as shipped.
- No unknown `reference_answers` keys, no non-list `must_include`, no non-list `fuzzy_match`
  (other than the `'N/A'` literal) in the shipped 812 — clean baseline for the instrument's
  schema checks.

---

## 4. Hand-expected cases for the new audit instrument

Notation: `EM(ref, pred)` = `StringEvaluator.exact_match`; `R` = routed `__call__` effective result
(pred pre-cleaned). All expected values derived by hand from lines 80–94 — NOT executed upstream.

### 4.1 Semantic cases (single-clean `EM`)
| # | ref | pred | expected | teaches |
|---|-----|------|----------|---------|
| S1 | `Yes` | `yes` | 1.0 | case forgiven |
| S2 | `Yes` | `Yes.` | 0.0 | trailing punctuation NOT forgiven |
| S3 | `Yes` | `Yes\n` | 1.0 | outer whitespace forgiven |
| S4 | `748m` | `748 m` | 0.0 | internal whitespace NOT forgiven (tasks 363–367 class) |
| S5 | `Yes` | `"yes"` | 1.0 | one matched quote pair forgiven |
| S6 | `Yes` | `"yes'` | 0.0 | mismatched quote pair not stripped |
| S7 | `x` | `' x '` | 0.0 | whitespace inside quotes survives strip |
| S8 | `N/A` | `n/a` | 1.0 | N/A exact gate is case-insensitive at comparison (but see §1.3 raw-value gate) |
| S9 | `Erik Linder-Norén` | `erik linder-norén` | 1.0 | lower() handles accents symmetrically |
| S10 | `Erik Linder-Norén` | `Erik Linder-Noren` | 0.0 | no accent/NFKD folding |
| S11 | `a` | `İ` (U+0130) | — | `clean('İ')='i\u0307'` ≠ `'a'`; use `ref='i'` pred='İ' → 0.0, casefold would have passed |
| S12 | `ss` | `ß` | 0.0 | no casefold expansion |
| S13 | `a b` | `a\u00a0b` | 0.0 | internal NBSP survives |
| S14 | `a` | `a\u00a0` | 1.0 | trailing NBSP stripped by strip() |
| S15 | `x` | `''` | 0.0 | `''`→strip→`''`→dequote→`''`→`''`; ref `''` vs pred `''` → 1.0 (empty==empty edge) |
| S16 | `Quest Lumaflex™ Band` | `quest lumaflex™ band` | 1.0 | ™ lower-invariant; task 0 shape |
| S17 | `1.7km` | `1.70km` | 0.0 | numeric formatting strictness |

### 4.2 Schema / instrument-detection cases
| # | scenario | expected instrument outcome |
|---|----------|------------------------------|
| K1 | `eval_types` contains `string_match`, `reference_answers` absent | flag: scorer `KeyError` crash class (not score 0) |
| K2 | `string_match` with `reference_answers: {}` | flag: **vacuous pass** — loop never runs, returns 1.0 |
| K3 | `reference_answers` key ∉ {exact_match, must_include, fuzzy_match} | flag: silently ignored by `match` (no default arm) |
| K4 | `exact_match` value non-str (e.g. `1`, `true`, `["x"]`) | flag: `clean_answer`/`beartype` TypeError crash class |
| K5 | `fuzzy_match` value a bare string other than literal `"N/A"` (e.g. `"n/a"`, `"NA"`) | flag: `assert isinstance(list)` crash class |
| K6 | `fuzzy_match == "N/A"` and `string_note` key missing/empty | flag: potential `KeyError`/vacuous-ua_match |
| K7 | `must_include` non-list, or list with non-str items | flag: assertion/TypeError crash class |
| K8 | ref `≠ clean_answer(ref)` (untrimmed, quoted, uppercase-internal anomalies that normalize onto another ref) | report cleaned-vs-raw pairs; duplicates-after-cleaning |
| K9 | `string_match` + `url_match` both declared | note multiplicative AND across evaluators (10 tasks) |
| K10 | `required_contents` key ∉ {exact_match, must_include} | flag: `ValueError` at line 329 |
| K11 | `required_contents.exact_match` ∈ {'none','null'} | flag: `str(None)`→'None'→'none' collision hazard |
| K12 | `must_include` ref containing ` |OR| ` | flag: literal-vs-alternation divergence (task 386 is the live exemplar) |

---

## 5. What a static task-spec inventory CANNOT prove (explicit limits)

1. **Reference correctness.** Nothing in the spec proves `'Pittsburgh International Airport, …'`
   is the right answer to task 7's intent — only live-site ground truth at task-authoring time
   (which may have drifted) could. Static audit records contract strictness, never answer truth.
2. **Field presence ≠ task validity.** A well-formed `reference_answers` block guarantees the scorer
   runs a comparison; it does not guarantee the comparison is meaningful, achievable, or the only
   acceptable answer (e.g., `|OR|` task 386, alternate-valid airports/spellings).
3. **`last_action["answer"]` provenance.** `browser_env` is outside the snapshot; whether stop
   actions always carry a string `answer` (vs missing/None → `KeyError`/beartype) is unverifiable
   statically.
4. **Runtime dependencies.** `nltk.word_tokenize` behavior (punkt data present? token boundaries?),
   `beartype` version semantics, `page.evaluate` stringification for exotic JS return types.
5. **LLM-path outcomes.** `llm_fuzzy_match`/`llm_ua_match` make network calls (helper_functions.py
   imports openai provider) — nondeterministic; static audit can only describe the call sites.
6. **`eval(func)` expansions.** 75 `func:` URLs / 22 `func:` locators evaluate Python against live
   page/site state (`shopping_get_latest_order_url` etc.); reachability and returned values are
   unverifiable offline, and the `eval` itself is a code-exec surface to document, not run.
7. **Drift between sites and spec.** `__GITLAB__`/`__REDDIT__`/`__MAP__` template substitution
   correctness and whether target elements exist live.
8. **The double-clean semantic** (§2.1) can be *stated* statically, but which behavior the harness
   actually exhibits end-to-end depends on trajectory construction — instrument should treat
   routed-semantics as primary truth and flag direct-call divergences as test-harness hazards.

---

## 6. Required code/output checks for `benchmark_spec_audit.py` (recommendations)

Code checks (instrument correctness):
- MUST verify snapshot sha256 against `manifest.json` before counting (already prereg'd — re-affirm).
- MUST schema-validate every `reference_answers`/`required_contents` block against the operator set
  the pinned scorer actually implements (K1–K12 classes); emit instrument-level findings distinct
  from benchmark observations.
- MUST NOT import/execute upstream; a pure-Python reimplementation of `clean_answer` for the
  hand-expected table is acceptable if the file documents it as a reimplementation and the
  divergence risk (my §4 rows pin the behavior).
- Selftests should cover: vacuous-pass empty dict, silent unknown key, `|OR|` literal in string
  path, single-clean vs double-clean divergence (S7), NBSP internal (S13), `''` empty edge (S15),
  `str(None)` collision class (K11), crash-class vs score-0 classification.
- Case report for task 7 must record: forgiven transforms {case, outer ws, one quote pair},
  unforgiven {punctuation, internal ws, accents, reordering}; same-shape note for 399/356/759
  rc-exact_match.

Output checks (what the emitted audit must contain):
- Per-task: raw ref, cleaned ref (reimplementation), operator, crash-class vs score-class
  disposition, denominators; aggregate: the §3 censuses (45/188 exact_match surfaces, 31
  single-char tokenize tasks (listed §3), 10 ANDed tasks) as reproducible JSON.
- MUST classify findings as `instrument_defect` vs `benchmark_observation` vs `cannot_determine`;
  unpassable-spec suspicions (task 386) are observations with evidence, not verdicts.
- MUST NOT emit "N tasks are valid/invalid" counts derived from field presence alone (explicitly
  prohibited; presence is schema conformance only).
- MUST state the routed (double-clean) truth wherever `__call__` behavior is reported.

---

## 7. Cross-seat overlap notes (record, don't claim)
- RevStringInclude: `must_include` tokenize path (lines 98–111), `|OR|` semantics split — I census
  (31 tasks, task 386) but leave verdicts to that seat.
- RevStringFuzzy: fuzzy/N-A gate + `ua_match`/`string_note` wiring — I census (36 N/A tasks, all
  noted) but leave LLM-path review to that seat.
- RevURLContract: `|OR|` in `reference_url` (line 213) is real alternation — different surface from
  task 386's literal.

## 8. Verification performed / limitations
- Verified: manifest sha256 of evaluators.py + test.raw.json match; every census count from my own
  JSON parse of the pinned file; all contract claims cited to line ranges I read directly.
- Not verified: anything requiring execution (no upstream code run, per contract); `browser_env`
  action schema; live LLM helpers; correctness of any reference answer.
- Commands observed by me: `sha256sum` on the two files; stdlib `json` parses of test.raw.json.
- Tool installs: none (no installs/updates performed; pacman paused per directive).

## 9. Verdict — scoped
**PASS (scoped to StringEvaluator clean_answer/exact_match contract surface).**
The pinned scorer contract is fully traceable and consistent with its own code: `clean_answer` =
strip → optional single matched-dequote → lower, applied asymmetrically (pred double-cleaned via
routed `__call__`, ref single-cleaned); `exact_match` is byte-equality under that normalization and
admits no semantic slack. The corpus is schema-clean for this surface (no malformed refs, no unknown
keys, no missing string_note), so the audit has a stable baseline to inventory. Material facts the
audit must carry: the double-clean divergence, `|OR|` literal-vs-alternation mismatch (task 386),
`str(None)`-collision hazard class, vacuous-pass on empty `reference_answers`, and the hard boundary
that static spec review cannot establish task validity or reference correctness — this is a PASS for
contract traceability and inventory completeness within my seat's slice, not a round-level verdict.
