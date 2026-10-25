# FContractEntry — Q10 complete second-seat re-read (full entry)

Seat: KengakuR28.FContractEntry. Scope: complete entry-level re-read of the frozen
candidate, reopening all three pinned primary sources and re-deriving every number and
source-backed interpretation independently (own code at
`.ufo/waves/round-28/scratch/FContractEntry/census.py`, output `census.out`; no
production/oracle imports, `-B` bytecode disabled, read-only over production).

- Frozen draft actually read: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
- SHA256 of exact bytes read: `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`
  — byte-identical to the digest pinned in `candidate-freeze.json` and the lesson.
- Canonical candidate path (not yet admitted): `corpus/knowledge/webarena-task-spec-audit.md`
- Fixture digests re-hashed, all match `plans/fixtures/r28/webarena/manifest.json`:
  test.raw.json `7b50386f…7652`, evaluators.py `e23edb39…00c22`,
  helper_functions.py `ec758da4…e275`, LICENSE `c71d239d…0ab4`.

## Per-source table

| row | URL (pinned revision dce04686a56253aefba7b18a4fa0937cf1dc987b) | accessed | located quote (≤25 words) | candidate pins verified |
|---|---|---|---|---|
| S061 | raw.githubusercontent.com/web-arena-x/webarena/dce04686…/config_files/test.raw.json | 2026-10-21 | `"eval_types": [ "string_match" ]` — task0 eval object | header pin `task0:18–28` covers every field of the task0 eval object (18 `eval`, 19–21 eval_types, 22–24 reference_answers, 25–28 remaining fields); the object's `}` sits at line29, one line outside the pin — cosmetic only |
| S062 | raw.githubusercontent.com/web-arena-x/webarena/dce04686…/evaluation_harness/evaluators.py | 2026-10-21 | `score *= cur_score` — EvaluatorComb:351 | `StringEvaluator:71–170`, `URLEvaluator:173–241`, `HTMLContentEvaluator:244–333`, `EvaluatorComb/evaluator_router:336–374` all exact |
| S063 | raw.githubusercontent.com/web-arena-x/webarena/dce04686…/evaluation_harness/helper_functions.py | 2026-10-21 | `if "partially correct" in response or "incorrect" in response:` — llm_fuzzy_match:169 | pin `fuzzy/UA:146–208` covers `llm_fuzzy_match` (146–173) and `llm_ua_match` (176–208) exactly |

## Predicate claims re-derived against S062/S063 (all confirmed)

- `clean_answer` (80–86): strip → at most one outer quote pair if first==last quote char →
  lower. `exact_match` (90–94) equality of two cleaned operands; routed path pre-cleans
  `last_action["answer"]` at134 so normalization is applied twice. Non-idempotent: e.g.
  raw answer `"'a'"` — direct `exact_match` yields `'a'` vs routed `a` — claim confirmed.
- `must_include` (98–111): substring containment on cleaned strings; tokenized branch
  needs `tokenize` flag AND `len(clean_ref)==1` AND `len(word_tokenize(clean_ref))==1`;
  flag passed as `len(value)==1` at148 (single-element must_include list).
- `fuzzy_match` (150–169): non-N/A values asserted list, each element → `llm_fuzzy_match`
  (S063:146–173). N/A path (152–163): exact `"N/A"` first; on `score!=1`, line159
  *assigns* `1.0*ua_match(...)` against `string_note` — overwrites any earlier
  accumulated in-evaluator score, as claimed. Census: all 36 `fuzzy_match=="N/A"` tasks
  have `reference_answers == {"fuzzy_match"}` only, so the overwrite is unreachable in
  this population — claim "all N/A tasks use only that approach" confirmed.
- `URLEvaluator` (187–239): `clean_url` rstrips `/`; `parse_url` keeps `netloc+path`
  (scheme, fragment, params ignored); `reference_url.split(" |OR| ")`; `base_score` is
  `any(ref_base_path in pred_base_path)` — substring containment of reference netloc+path
  inside predicted netloc+path; per-key query score requires some pooled reference value
  in `parse_qs(pred.query)`; query values pooled across alternatives via
  `defaultdict(set)` (199–210), not paired per-alternative. Non-"GOLD in PRED"
  `url_note` raises ValueError (238–239). Population: only 7 `reference_url`s use the
  OR delimiter (task 681 among selected16, literal ` |OR| ` confirmed); every `url_note`
  present is exactly `GOLD in PRED` (196 tasks; 9 url_match tasks omit the key).
- `HTMLContentEvaluator` (258–333): `url=="last"` → no navigation; otherwise
  `page.goto(url)` + fixed `time.sleep(3)`; `func:` URLs eval-resolved (263–266).
  Empty locator → `page.content()`; `document.`/`[...document.` → `page.evaluate` with
  errors → `""` (288–294); `func:` locators eval'd with no try/except — errors
  propagate, the "different paths" claim confirmed. `html.unescape` at303; `if
  exact_match … elif must_include` (305–327) → effective single operator per target,
  exact_match precedence; ` |OR| ` alternatives inside must_include entries (316).
- `EvaluatorComb` (348–352) multiplies in declared `eval_types` order built by the
  router (361–370); unknown type → ValueError (371–372). Order is observably
  significant: all 129 `program_html+url_match` tasks declare `["url_match","program_html"]`
  (non-sorted order exists in the data), and HTML navigation mutates `page.url` that
  URLEvaluator reads — the draft's "preserve order" warning is grounded, not rhetorical.
- S063 (146–208): both judges call `gpt-4-1106-preview`, temperature0; unexpected
  responses fall through to `assert` (172, 207), not a graceful score. "Exact N/A
  bypasses the reason judge" — ua_match only runs when exact N/A fails. `func:` strings
  treated as text throughout; no eval/import of upstream code performed.

## Numbers re-derived independently (before instrument comparison)

| metric | my derivation | draft | match |
|---|---|---|---|
| raw tasks / distinct IDs | 812 / 812, IDs 0–811, 0 missing, 0 dup | 812/812 | ✓ |
| evaluator-type sets | string_match 325, program_html 282, url_match 66, string_match+url_match 10, program_html+url_match 129 | identical | ✓ |
| strata / selected | 27 / [389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399] | 27/16, same list | ✓ (byte-equal to selected-task-ids.json) |
| string operator task counts | exact_match 45, must_include 176, fuzzy_match 118 (4 tasks carry fuzzy+must_include → coexistence claim confirmed) | identical | ✓ |
| page-content targets / effective ops | 651 / exact_match 188 + must_include 463, no dual-key, no other-key targets | identical | ✓ |
| locator classes | full-page 105, JavaScript 524, helper 22, 0 unclassified | identical | ✓ |
| target URL classes | last 238, navigation 338, helper(func) 75 | identical | ✓ |
| schema anomalies under declared contract | 0 (all eval_types/​locators/​rc-keys/​url_notes in enum; no `func`-without-colon URLs) | 0 | ✓ |
| `shopping` site among selected16 | none (only shopping_admin in task759) | "shopping omitted" | ✓ |
| selected-case coverage gaps | 0/16 have func-url, func-locator, prep_actions, or ` |OR| ` required_contents (only 5/10/65/14 tasks population-wide) | all three gaps claimed | ✓ |
| N/A tasks | 36, all single-approach, all with non-empty `string_note` | implied by case claims | ✓ |

`python3 -B plans/benchmark_spec_audit.py --summary` (lane-owned, allowed): exit0,
every emitted counter equal to my derivation. `--selftest`: exit0, 21 named cases as
claimed. Cited receipts exist (`corpus/evidence/round28-calibration/audit-summary.txt`,
`build-acceptance/audit-current.stdout`), as do all 16 Task*.md and Rev*.md build
reports named in the table.

## Case-audit claims spot-verified in raw spec bytes

- Task590: intent `1/16/2023–1/30/2023`; program_html must_include `Jan 16, 2030` /
  `Jan 30, 2030` — authored-text mismatch confirmed, runtime invalidity correctly not
  asserted.
- Task97: graded must_include `914km` vs raw annotation `914 km`; must_include is pure
  substring — claim confirmed.
- Task356/759/424: locators `[name="route_from"`, `[name="route_to"`,
  `[id="sidebar_content"` — unclosed attribute-selector brackets confirmed; draft
  correctly declines to infer browser rejection.
- Task173: `fuzzy_match: ["No, it is open"]` → llm_fuzzy_match judge dependency.
  Task791: `fuzzy_match: "N/A"` + `string_note` → exact-N/A then ua_match fallback.
  Both "remote-judge-dependent branches" confirmed.
- Boundary labels verified per task: 389 comment must_include, 132 single-element
  must_include `["1"]` → tokenized numeric answer, 44 URL-only, 552 literal URL list in
  required contents, 681 literal ` |OR| ` reference_url + cross-site literals, 556
  README must_includes, 7 long exact_match address, 377 literal query URL, 759 route
  input fields, 424 sidebar text, 399 bio exact_match.

## Observations (non-blocking precision notes, not unsupported claims)

1. must_include tokenization: draft states the flag and one-character-reference
   conditions; the source has a third conjunct `len(word_tokenize(clean_ref))==1`
   (S062:103–107). For a single character this is practically redundant; the draft's
   stated conditions are necessary but not strictly sufficient. Cosmetic.
2. URL containment direction is implicit in the table row ("netloc+path substring
   containment"); source direction is reference-in-prediction (`GOLD in PRED`).
   Requires reader inference; not wrong.
3. S061 header pin `task0:18–28` excludes the eval object's closing `}` at line29.
4. `clean_url`/`rstrip("/")` strips all trailing slashes; draft's "strips trailing
   slash" is directionally exact, singular by phrasing only.

No location, number, or claim was found unsupported. Every scorer operator/branch
statement traces to the reopened pinned lines; every table value re-derives
independently; every named receipt/report path exists; honest limitations (static
only, no judge/browser truth, nonrepresentative sample, oracle authored by same
writer) are all stated in-band.

## VERDICT: PASS

Findings are re-read evidence, not repairs. L1 resolves admission; any byte change to
the candidate requires a same-identity re-read of the new digest.

---

## v2 re-read (2026-10-21), IRC from KengakuR28: draft 3eb2afe5…, supersedes the v1 VERDICT for v2 bytes only

Scope: complete re-read of the v2 frozen draft (all 163 lines), Amendment 2, the corrected lesson, the S005/S006 primary pages, and final-acceptance receipts. The v1 section above is preserved unchanged; its PASS applies only to v1 bytes 77e19d5b…. No production, draft, freeze, or source-registry edits were made. Scratch: .ufo/waves/round-28/scratch/FContractEntry/v2/.

### Identity and pins

- Draft read: .ufo/waves/round-28/drafts/webarena-task-spec-audit.md. SHA256 of exact bytes read: 3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182. This equals candidate_sha256 in candidate-freeze-v2.json.
- The IRC named freeze-v2.json; the actual file is .ufo/waves/round-28/candidate-freeze-v2.json (sha256 7bfa6b5b013acbb5828dcfc6147e1e2eb0006e05e481520d3c833a3ac58dd259). It supersedes candidate-freeze.json (sha256 bf5990dcdc0897875b09ca8616be1061ea7ed171a0151278e3dfb6304bad1618, v1 candidate 77e19d5b…).
- Canonical candidate path: corpus/knowledge/webarena-task-spec-audit.md. Absent, so nothing is admitted; the freeze scope agrees.
- Instrument digests match freeze v2: plans/benchmark_spec_audit.py, plans/registry_check.py, plans/state_check.py (full hashes in the table below).
- Pinned fixtures re-hashed against plans/fixtures/r28/webarena/manifest.json (sha256 c78b1478…, equal to the script's MANIFEST_SHA256 constant): test.raw.json, evaluators.py, helper_functions.py match; LICENSE is Apache License 2.0 (header confirmed).

### Source anchors checked this round

- S061/S068, test.raw.json: intent line 16 ✓; eval object 18–29 ✓ (line 18 "eval": {, line 29 },); eval_types 19–21 ✓; reference_answers 22–24 ✓; program_html 26 ✓. S068 corrects S061's 18–21 anchor as stated.
- S062, evaluators.py (own ast probe, not a production import): StringEvaluator 71–170 ✓, URLEvaluator 173–241 ✓, HTMLContentEvaluator 244–333 ✓, EvaluatorComb 336–352 ✓, evaluator_router 356–374 ✓ (decorator at 355).
- S069 statement lines: composite product "score *= cur_score" at 351 ✓ (the only augmented multiply inside EvaluatorComb); N/A assignment "score = 1.0 * self.ua_match(" at 159 ✓ (the only assignment to score whose right side calls ua_match); N/A branch 152–163 ✓.
- S063, helper_functions.py: llm_fuzzy_match 146–173 ✓; llm_ua_match 176–208 ✓; judge model calls at 162 and 197 ✓; keyword-to-return/assert at 169–172 and 204–207 ✓.
- Probe: .ufo/waves/round-28/scratch/FContractEntry/v2/ast_anchor_probe.py and ast_anchor_probe.out. Dispatch derived independently: string_match to StringEvaluator, url_match to URLEvaluator, program_html to HTMLContentEvaluator.

### S005 / S006 primary pages (reopened 2026-10-21)

- S005, openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ (dated February 23, 2026): the quote "Many task statements were underspecified, which could lead to multiple valid interpretations - while the tests only covered a specific one." is a bullet under "## Background" ✓. The same section says experts reviewed 1,699 SWE-bench problems, which supports the in-kind audit-precedent wording.
- S006, openai.com/index/separating-signal-from-noise-coding-evaluations/ (dated July 8, 2026): the quote "An initial automated filter reviews the instructions given to the model, attempts by the model to solve the task, and the tests" is in "## Methodology" ✓.
- Both are self-reports, as the draft says.

### Dates in the v2 entry (new precision check)

- "committed 2025-11-26": the GitHub commit record for dce04686a56253aefba7b18a4fa0937cf1dc987b gives author and committer date 2025-11-26T21:15:59Z ✓ (api.github.com commit JSON, reopened this round).
- "2023-07-25 paper-era release": arXiv 2307.13854 reads "Published: 2023-07-25" ✓ (arXiv v1 publication date).

### Numbers and receipts

- The v1 census (scratch census.py and census.out) still reproduces every v1 count. New v2 counts from the raw JSON: url_match tasks 205 = 196 with a url_note key + 9 without; effective rule GOLD in PRED for all 205 ✓.
- Lane audit --json re-run into scratch (read-only): sha256 ad53df24… is byte-identical to final-acceptance/audit-current.stdout and audit-without-c2.stdout ✓.
- Oracle: final-acceptance/audit-alternate.stdout metrics (16 keys) and selected IDs equal the production JSON exactly (programmatic check) ✓. Its writer field is KengakuR28, as the draft says.
- Selftest: final-acceptance/audit-selftest.stdout reads "SELFTEST clean cases=67". I counted 67 names, all unique. They include precedence (html_exact_shadows_include), retained-verified-byte (verified_bytes_retained_config_files/test.raw.json and verified_bytes_retained_evaluation_harness/evaluators.py), and missing-input (cli_missing_input) controls. commands.json records exit 0. I did not re-run selftest (not assigned); the 67 figure rests on the receipt.
- Raw preservation: all 812 records' raw_task equal the input objects ✓. reference_approach_order equals raw key order for all 812 ✓. The receipt's reference_answers dict is key-sorted for tasks 34, 35, 267, 268, so the explicit order lives only in reference_approach_order; the draft's wording is accurate.
- Task 247: raw reference_url "Valorie doesn't have a email in the system" with string_match only; the record keeps the value, effective_url_rule is null, status SCHEMA_COMPATIBLE ✓.
- Credential scan of raw JSON: token, cookie, and secret hits are task intent, page title, and heading text only (lines 8184–8186, 15500–15618). storage_state values are path strings or null ✓.
- Execution boundary: no exec, eval, compile, importlib, or __import__ in plans/benchmark_spec_audit.py (grep exit 1). subprocess only re-runs the script itself (sys.executable plus Path(__file__)) for selftest CLI cases against a scratch copy ✓.

### Hand-read vs AST annotation boundary

- AST-derived in production: dispatch, composition and N/A line numbers, and contract anchors. The selftest asserts dispatch and line lists against hand-written expected constants.
- Literal strings, not hashed and not checked by any code path: "authority", composition.operation, na_fallback.operation, and all failure_phases text (benchmark_spec_audit.py:192).
- I checked every failure-phase sentence against the pinned source. Unknown eval type raises ValueError at the router (372). Unknown URL rule raises ValueError (239). Unknown locator or operator raises ValueError (301, 330–332). A JavaScript locator exception yields empty text, "not necessarily score zero", which is correct because exact_match against an empty reference passes. Dynamic helper and navigation errors are not absorbed: the func: call at 299 and page.goto at 272 sit outside the try at 288–294 ✓.

### Vacuity limits and raw projections

- The instrument emits no vacuity advisories: "advis" occurs zero times in the script and in the receipt. Vacuity-shaped inputs pass with findings: [] (cases empty_refs_native_vacuity, include_empty_native_vacuity, fuzzy_empty_native_vacuity, blank_reference_native_vacuity, html_empty_native_vacuity, html_exact_shadows_include).
- Malformed projections: invalid eval-type sets go to a "<INVALID>" histogram bucket, and the raw eval_types stays in each record. URL-note provenance: url_note (raw), url_note_present, effective_url_rule ✓.

### Errata to v1 (above, not edited)

- E1 (incorrect in v1): the non-idempotence witness "'a'" is wrong. Direct exact_match and routed both return 1.0. The correct witness is raw ''a'' against reference a: direct 0.0, routed 1.0; clean(clean(x)) is a while clean(x) is 'a'. Scratch: v2/idempotence_probe.py and idempotence_probe.out. The v2 draft's claim is correct and needs no witness.
- E2 (superseded): v1's note that the S061 anchor 18–28 misses line 29 is resolved; v2 cites 18–29 ✓.
- E3 (resolved): v1's note on the missing third tokenization conjunct is resolved; v2 line 36 includes it ✓.

### Findings for L1 (concrete corrections; no number changes)

- F1 (wording, draft lines 133–135): "Vacuity advisories (…) are not a complete feature of this instrument" describes an advisory feature that does not exist. Suggested: "The instrument emits no vacuity advisories: empty predicate containers, blank reference values and shadowed extra keys are accepted without findings."
- F2 (wording, lines 122–124): "hand-read, source-hash-bound annotations" overstates. Only the input bytes are hash-verified (manifest check plus top-level source_sha256). The annotation text is literal and unchecked. Suggested: "hand-written literal annotations, reviewed against the manifest-pinned revision; the text is neither hashed nor AST-checked."
- F3 (receipt, lines 102–106): no repaired-package --summary receipt exists in final-acceptance. The only summary receipt, corpus/evidence/round28-calibration/audit-summary.txt, predates the repair and lacks the new LIMIT line and the URL_RULES and URL_NOTE_ORIGIN lines. The current --summary run exits 0 (scratch v2/audit-summary-rerun.txt). Add a final-acceptance summary receipt or qualify the sentence.
- F4 (source registration, lines 15–16): "committed 2025-11-26" is correct, but no registry row carries an opened quote for the commit date. Register the GitHub commit record as an opened row with a new source number, or cite it.
- F5 (source registration and wording, lines 16–17): "2023-07-25 paper-era release" is correct as the arXiv v1 publication date, but "release" is a gloss and no registry row exists. Register the arXiv abstract page, or write "arXiv v1 publication date 2023-07-25".
- F6 (optional, line 49): add the witness ''a'' against reference a (direct 0.0, routed 1.0) so the non-idempotence sentence is checkable.

Everything else reproduced: numbers, selection, anchors, quotes, S068/S069 lines, the S005/S006 quotes, the 196+9 split, the 67 cases, and the receipt and report paths. All exist except the canonical entry, which is correctly absent.

### Receipt and freeze hashes (for L1 to pin; freeze-v2 not edited)

+| artifact | sha256 |
|---|---|
| draft v2 (read) | 3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182 |
| candidate-freeze-v2.json | 7bfa6b5b013acbb5828dcfc6147e1e2eb0006e05e481520d3c833a3ac58dd259 |
| candidate-freeze.json (v1) | bf5990dcdc0897875b09ca8616be1061ea7ed171a0151278e3dfb6304bad1618 |
| plans/benchmark_spec_audit.py | b7524c2f316f5ba850bd901c932811ca55cd4adff264242488f3842def5cca36 |
| plans/registry_check.py | fc388c332d4e37f8f0f7118d15a0baed8d86cd99b345ab9255e2b9dc6bd7379b |
| plans/state_check.py | 5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c |
| fixture manifest.json | c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd |
| fixture selected-task-ids.json | 5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a |
| fixture test.raw.json | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |
| fixture evaluators.py | e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22 |
| fixture helper_functions.py | ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275 |
| fixture LICENSE | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |
| final-acceptance/acceptance.json | a76eb360351cb182e53a18cfbbe0a11a13a7b1a0bbc5447538069df4558b0256 |
| final-acceptance/commands.json | 96e61c4dbdd1c0493adbcb87d42907bc69198b6500ddbfb8e0d90f9b0dd5ac5b |
| final-acceptance/audit-current.stdout | ad53df24c06e58d9db3bd36dadf058d963fbe45ebc19684998e6b588b2879a93 |
| final-acceptance/audit-without-c2.stdout | ad53df24c06e58d9db3bd36dadf058d963fbe45ebc19684998e6b588b2879a93 |
| final-acceptance/audit-selftest.stdout | c3d54a97b46c6c86b2b52c7f27baa8c44482af7ec8c4d45b4805561dad52f045 |
| final-acceptance/audit-alternate.stdout | 13a1bc20a207e7d70684edaffe26dfa90e9afeaef3be787733564fcfe98c6385 |
| final-acceptance/admission-source-links.json | dee129b6e3987fcc8cd9023649d665f75d17eb14efd2840af6420a2e862fbe07 |
| final-acceptance/historical-state-current.stdout | 46670654146294ca4a1a1f2a0c2dc3299e84d6cb921e96b59d8de11fb9f3ff19 |
| final-acceptance/registry-current.stdout (also registry-s038-only-delta-green.stdout) | f6f53dc28d406a37bf1cccdcae13ff9dc42b845b2185b4b84138f167b968250b |
| final-acceptance/registry-baseline-red.stdout | a507723c10a97b41a0d02a2e880b6b80854cdebfb0b66217f572aa403ce049ba |
| final-acceptance/registry-s050-only-red.stdout | f024acd01bc6d84e6fb36c4e789c81af560df83235d2157b58bdc646928ab02b |
| final-acceptance/registry-only-delta.json | 081e176ec42b9d08f271a99babd82aca31036b18e22adc6ba691b5b6b6cc6263 |
| build audit-summary.txt (pre-repair) | 686cbcf9edfff5d67b15e0e0e7c2685f2ae53021d497f06a40cceec82b898bb1 |
| scratch v2/audit-json-rerun.stdout | ad53df24c06e58d9db3bd36dadf058d963fbe45ebc19684998e6b588b2879a93 |
| scratch v2/audit-summary-rerun.txt | dbbffbe818e1f5ada791a2777c78df2f2d4b637c62f454a2fa44dd527e036972 |
| scratch v2/ast_anchor_probe.out | 67856a6e13d44bb37ee5a127fe7306e5b9f41423af38733540940f5e313905d6 |
| scratch v2/idempotence_probe.out | 7b26198343dfcc96c054dfc522641608dc3663b03e4b5aa78fed33bb83d68cc4 |
| scratch census.out (v1) | fb2c6728f6cc205947b620726e8a45db944795d2207285650379c4000f77078a |

### VERDICT (v2 draft, sha256 3eb2afe5…)

VERDICT: PARTIAL. Numbers, anchors, quotes, digests, and the 67-case and 196+9 counts reproduce. Corrections F1–F5 are required before PASS (F6 optional). Any changed candidate bytes need a same-identity re-read of the new digest. Tool installs: none. Production edits: none. Canonical path corpus/knowledge/webarena-task-spec-audit.md remains absent.

---

## v3 final re-read (2026-10-21), IRC from KengakuR28: draft 1cda3cdf…, supersedes the v2 VERDICT for v3 bytes only

Scope: complete re-read of the exact v3 bytes (all 167 lines), the four FFullEntry precision fixes named in the IRC, status of v2 findings F1–F6 on these bytes, and the pins and counters the writer named. Targeted checks only; no new broad probes. Earlier sections (v1 for 77e19d5b…, v2 for 3eb2afe5…) are preserved. Cosmetic note: line 205 (v2 receipt table header) carries an append-syntax "+" character; it is left unedited to preserve earlier sections.

### Identity (exact bytes)

- Draft read in full: .ufo/waves/round-28/drafts/webarena-task-spec-audit.md, 167 lines.
- SHA256 of exact bytes read: 1cda3cdf7937d236af2d7f6e9834dbb64690040ad4bef7fa9394112bf2369615. This equals candidate_sha256 in .ufo/waves/round-28/candidate-freeze-v3.json and the on-disk file.
- The IRC's digest (cda3cdf7937d236af2d7f6e9834dbb64690040ad4bef7fa9394112bf2369615, labelled "SHA1") has 63 hex characters. It is the correct value with its leading "1" dropped. The algorithm is SHA-256 (64 hex), so 1cda3cdf… is the pin.
- candidate-freeze-v3.json: sha256 b384799abda6973aa7e2eb86600412f5a18dc7b2827a5cc9c954a5eae1452bfe; prior_candidate_sha256 3eb2afe5… (v2); scope "Final wording-only correction to v2; instruments and all measured counters unchanged; current exact-byte re-read required."
- Canonical candidate path: corpus/knowledge/webarena-task-spec-audit.md. ABSENT on disk; this verdict does not admit it.

### Code hashes and counters (unchanged, verified)

- plans/benchmark_spec_audit.py b7524c2f… ✓; plans/registry_check.py fc388c33… ✓; plans/state_check.py 5db1eb78… ✓. Each matches freeze v3 and final-acceptance/acceptance.json.
- C1 selftest: final-acceptance/audit-selftest.stdout header "SELFTEST clean cases=67" with 67 unique names ✓ (not re-run).
- C2 selftest: final-acceptance/registry-selftest.stdout header "SELFTEST clean cases=15" ✓ (not re-run).
- Build C1 selftest: build-acceptance/audit-selftest.stdout header "SELFTEST clean cases=21" ✓ (supports "passed21").

### The four FFullEntry precision fixes (v3 text checked)

- Fix 1, public usernames and no auth secrets (lines 29–32): "Fixture login-state paths and public usernames occur as authored task data; no authentication-secret values, cookies or contents of auth-state files were opened." RESOLVED. Usernames are present in the raw task data: 169 lines match byteblaze or MarvelsGrantMan136 (for example tasks 173, 399, 552). The v2 credential scan found no credential values.
- Fix 2, no July release assertion (lines 16–17): the text now reads "including earlier paper-era snapshots and WebArena-Verified" and asserts no date. grep for July or 2023 finds only "January2023" (Task590's intent, line 86). RESOLVED; this also closes v2 F5.
- Fix 3, exact commit API citation (lines 18–21): cites https://api.github.com/repos/web-arena-x/webarena/commits/dce04686a56253aefba7b18a4fa0937cf1dc987b and field `.commit.committer.date` = 2025-11-26T21:15:59Z. Verified against the reopened API record, where author and committer dates are identical. RESOLVED at candidate-text level. Registration remains open: corpus/SOURCES.md has zero rows naming api.github.com, so L1 must add an opened-source row before admission (v2 F4).
- Fix 4, resolved URL equals last (lines 48–49): "When the resolved target_url equals `last`, the page-content check does not navigate; otherwise it navigates and sleeps a fixed interval, conditional on no propagated runtime error." RESOLVED. Source S062 lines 261–273: target_url is resolved first (the func: branch evaluates the string and replaces __last_url__ with page.url), then `if target_url != "last": page.goto(target_url); time.sleep(3)`. Exceptions from eval or goto propagate, so the sleep is conditional on no error.
- Changed regions versus v2 (by section comparison): lines 15–21, 29–32, and 48–49 only. The draft grew from 163 to 167 lines through those insertions; all other sections match the v2 read.

### Re-verification on the v3 bytes

- Source anchors S061/S068, S062/S069, S063 and their line claims: text unchanged; verified in the v2 section and in ast_anchor_probe.out.
- S005/S006 quotes and pages: text unchanged. Line 1 raw URLs match the reopened pages: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ and https://openai.com/index/separating-signal-from-noise-coding-evaluations/.
- Numbers (lines 112–122: 812/812, 651 targets, 205 = 196 explicit + 9 defaulted, 67 cases) and the non-idempotence sentence (lines 53–54): unchanged and verified. The corrected witness is in the v2 section.

### Status of v2 findings on the v3 bytes

- F1 vacuity wording (v3 lines 137–139): OPEN. The text still reads "Vacuity advisories (…) are not a complete feature of this instrument." The instrument emits no vacuity advisories ("advis" occurs zero times in the script and receipt); vacuity-shaped inputs pass with findings: [].
- F2 "source-hash-bound annotations" (v3 line 127): OPEN. Only the input bytes are hash-verified; the annotation strings are literal and unchecked.
- F3 repaired --summary receipt (v3 lines 106–110): OPEN. final-acceptance has no summary receipt; the only summary receipt, corpus/evidence/round28-calibration/audit-summary.txt, predates the repair.
- F4 commit-date citation: candidate text RESOLVED; registry row OPEN before admission (see Fix 3).
- F5 July or 2023-07-25 release: RESOLVED (assertion removed).
- F6 optional witness (v3 lines 53–54): OPEN, optional, not required.
- F7 glued tokens (new, typographic, non-blocking): "committed2025-11-26" (line 16), "as2025-11-26T21:15:59Z" (line 21, new text), "string_match325" (line 115), "passed21" and "executes67" (line 130). Values are unaffected; spacing should be restored.
- F8 clarity (new, optional): "conditional on no propagated runtime error" (line 49) can be read as making navigation itself depend on no error. Source-accurate phrasing: "otherwise it calls page.goto and, only if that raises no error, sleeps a fixed interval; errors propagate."

### Proposed wording for the open items (for L1 or the writer)

- F1: "The instrument emits no vacuity advisories. Empty predicate containers, blank reference values and shadowed extra keys are accepted without findings; empty string-reference maps and empty HTML target lists are not labeled semantic successes or defects."
- F2: replace "hand-read, source-hash-bound annotations" with "hand-written literal annotations, reviewed against the manifest-pinned revision; the input bytes are hash-verified (top-level source_sha256), but the annotation text is neither hashed nor AST-checked."
- F3: add final-acceptance/audit-summary.stdout from a --summary run on the admitted tree, or state explicitly that only the --json receipt exists for the repaired package.

### Receipt and freeze hashes (additions; the v2 table above remains valid)

+| artifact | sha256 |
|---|---|
| draft v3 (read) | 1cda3cdf7937d236af2d7f6e9834dbb64690040ad4bef7fa9394112bf2369615 |
| candidate-freeze-v3.json | b384799abda6973aa7e2eb86600412f5a18dc7b2827a5cc9c954a5eae1452bfe |
| final-acceptance/registry-selftest.stdout | 06700d9ae79af2cd11dd2f25850daaae3ee4f5491a70101bd381c8a6e8da0d38 |
| final-acceptance/audit-selftest.stdout | c3d54a97b46c6c86b2b52c7f27baa8c44482af7ec8c4d45b4805561dad52f045 |

### VERDICT (v3 draft, sha256 1cda3cdf…)

VERDICT: PARTIAL. All four FFullEntry precision fixes are resolved and verified, and every number, anchor, quote, pin, and counter reproduces on these exact bytes. Three items remain open on these bytes: F1 (vacuity "advisories" wording), F2 ("source-hash-bound" wording), and F3 (no repaired --summary receipt). Non-blocking: F4 registry row before admission, F6 witness, F7 spacing, F8 clarity. PASS requires F1–F3 corrected and a same-identity re-read of the resulting digest. Canonical path corpus/knowledge/webarena-task-spec-audit.md remains absent. Tool installs: none. Production edits: none.

---

## v4 same-identity judgment (2026-10-21), IRC from KengakuR28: draft 50589759…, supersedes the v3 VERDICT for v4 bytes only

Scope: same-identity full-entry judgment on the exact v4 bytes, using the complete reread of all 167 lines plus the four narrow deltas named in the IRC (F1 vacuity wording, F2 annotation status, F3 repaired summary receipt, commit-date removal). Targeted reads, greps, and hashes only; no new probes and no scope change. Earlier sections (v1 for 77e19d5b…, v2 for 3eb2afe5…, v3 for 1cda3cdf…) are preserved: the first 305 lines of this file hash to 2743a3ad… both before and after this append.

### Identity

- Draft read in full: .ufo/waves/round-28/drafts/webarena-task-spec-audit.md, 167 lines. SHA256 of exact bytes read: 50589759b82b26a7199d157035c852260ab1b10b59815f7b57e7534eccfd2ead. This matches the IRC digest exactly (64 hex).
- candidate-freeze-v4.json: sha256 f691c4a1df1377faea70255939b4b5722a39c5abb215c776a76c846453ab23c4. Its candidate_sha256 equals the draft digest; prior_candidate_sha256 is 1cda3cdf… (v3); scope "Final precision corrections … Instruments/counters unchanged."
- Canonical candidate path: corpus/knowledge/webarena-task-spec-audit.md. ABSENT on disk (verified). This verdict does not admit the entry; Q13 support exists only at actual admission.

### Instruments and counters (unchanged, verified)

- plans/benchmark_spec_audit.py b7524c2f…; plans/registry_check.py fc388c33…; plans/state_check.py 5db1eb78…. All match freeze v4.
- C1 selftest: final-acceptance/audit-selftest.stdout reads "cases=67" (not re-run). C2 selftest: final-acceptance/registry-selftest.stdout reads "cases=15" (not re-run). Build C1 selftest: build-acceptance/audit-selftest.stdout reads "cases=21".

### The narrow deltas

- F1, vacuity wording (lines 137–141): now reads "The instrument emits no vacuity advisories." Verified: "advis" occurs zero times in the script and receipts; vacuity-shaped inputs pass with findings: []. The added sentence "Vacuity, shadowed-key and dead-field semantic classification are outside this instrument." holds: the script contains no "dead" token, and shadowed keys appear only as a test-case name. RESOLVED.
- F2, annotation status (lines 125–128): now reads "Operation/error-phase descriptions are hand-read annotations, not automatically checked by the AST or validated merely by the source hash." Verified: the operation and failure-phase strings are literal (plans/benchmark_spec_audit.py:192) and no code path checks them; dispatch and composition/N-A line numbers are AST-derived. RESOLVED.
- F3, repaired summary receipt (lines 104–109): the draft names corpus/evidence/round28-calibration/audit-summary-final.txt for the repaired --summary. The file exists (1513 bytes; sha256 8019499ee1d19f440f55b1516981e9d8f44d51ba85fc35c2db7c7be63a4102de). It is line-identical to a post-repair --summary run (scratch v2/audit-summary-rerun.txt, sha256 dbbffbe8…) except for the harness trailer (blank line and "exit=0"). It carries the repaired LIMIT line and the URL_RULES and URL_NOTE_ORIGIN lines, and TOTAL reads findings=0 exit=0. RESOLVED.
- Commit date and API citation: removed entirely. Residual scan of the draft: 0 hits for 2025-11-26, 0 for api.github, 0 for "committed". The only 2023 token is January2023 in Task590's intent (line 84); no July date assertion remains. RESOLVED; the earlier F4 and F5 items are moot.

### Full-entry re-verification on the v4 bytes

- Source header (line 1, raw): S061/S068 and S062/S069 anchors, S063 anchors, and the S005 and S006 URLs are unchanged. Both S005 and S006 URLs match the reopened pages.
- Anchors and quotes: S062 StringEvaluator 71–170, URLEvaluator 173–241, HTMLContentEvaluator 244–333, comb/router 336–374; S063 fuzzy/UA 146–208; S069 product line 351 and N/A line 159; S005 Background and S006 Methodology quotes. Unchanged from the verified v3 reread and checked against the pinned bytes (ast_anchor_probe.out).
- Public-username and no-secret sentence (lines 28–30) and resolved-URL-equals-last sentence (lines 46–47): unchanged and verified (public usernames in 169 raw task-data lines; source lines 261–273).
- Numbers table (lines 113–121): 812/812; 27/16; 651 targets with 188 exact and 463 must_include; 105/524/22 locators; 238/338/75 URL classes; 205 GOLD in PRED = 196 explicit + 9 defaulted; 0 schema findings. Unchanged and re-derived in v1 and v2.
- Selection, Task247, case-report paths, and receipt paths: unchanged. Every cited path exists except the canonical entry, which is correctly absent.

### Non-blocking residuals (optional; no claim is changed by them)

- F6 (lines 51–52): no witness for the non-idempotence sentence. Optional; the corrected witness ''a'' against reference a (direct 0.0, routed 1.0) would make it checkable.
- F7 (typography): line 130 now reads "passed 21" and "executes 67" (fixed). Compact label-number cells remain in the table (for example string_match325, helper22, last238 at lines 114–120). Values are unaffected.
- F8 (clarity, line 47): "conditional on no propagated runtime error" is source-accurate. An error from an earlier target or from goto propagates out of the loop, so the sleep and later targets run only when no error has propagated. Optional rewording.

### Findings

- Blocking: none.
- Admission notes for L1 (not verdict inputs): the canonical entry is created only at admission. Registry rows S062, S063, S068, and S069 cite the same anchors. S061's row keeps its superseded 18–21 anchor by design, since S068 supersedes it. No commit-date source is needed.

### Receipt and freeze hashes (v4 additions)

+| artifact | sha256 |
|---|---|
| draft v4 (read) | 50589759b82b26a7199d157035c852260ab1b10b59815f7b57e7534eccfd2ead |
| candidate-freeze-v4.json | f691c4a1df1377faea70255939b4b5722a39c5abb215c776a76c846453ab23c4 |
| corpus/evidence/round28-calibration/audit-summary-final.txt | 8019499ee1d19f440f55b1516981e9d8f44d51ba85fc35c2db7c7be63a4102de |
| scratch v2/audit-summary-rerun.txt (same lines, no trailer) | dbbffbe818e1f5ada791a2777c78df2f2d4b637c62f454a2fa44dd527e036972 |

### VERDICT (v4 draft, sha256 50589759…)

VERDICT: PASS.

Scope of the verdict: the exact v4 bytes above. Every location, number, quote, pin, counter, and receipt path in the entry is supported. F1, F2, F3, and the commit-date item are resolved as stated. The residuals F6–F8 are optional and non-blocking. This is a judgment on the candidate bytes, not an admission or endorsement: the canonical path corpus/knowledge/webarena-task-spec-audit.md remains absent, and Q13 support exists only at actual admission. Any later byte change needs a same-identity re-read of the new digest. Tool installs: none. Production edits: none.
