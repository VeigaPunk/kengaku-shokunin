# FFullEntry — Q10 complete second-seat re-read (round-28 WebArena task-spec audit)

- Scope: full candidate re-read, all three pinned primary sources reopened, every numeric
  claim and source location independently re-derived before comparison to the lane instrument.
- Draft bytes read: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
  SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (12405 bytes) —
  matches the frozen hash in the wave context exactly.
- Canonical candidate path (not yet admitted): `corpus/knowledge/webarena-task-spec-audit.md`.
- Writer: KengakuR28 (distinct seat). This is an author-side falsification re-read; no draft edits.

## Per-source verification

### S061 — config_files/test.raw.json (sha256 7b50386f…, 880776 B, 29604 lines)
Independently re-parsed (stdlib json only; no production/oracle imports):
- 812 tasks, 812 distinct IDs, contiguous 0–811, zero missing/duplicate/unexpected. MATCH.
- Evaluator-type sets (sorted labels): string_match 325, program_html 282, url_match 66,
  string_match+url_match 10, program_html+url_match 129 (ordered form `url_match,program_html` ×129;
  draft correctly notes sorted-label grouping vs ordered preservation). MATCH.
- Site/evaluator strata: 27. Re-derived selection (sorted site-set, sorted eval-type-set,
  lexicographic stratum sort, per-stratum minimum task_id, first 16) yields exactly
  389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399 — identical to
  selected-task-ids.json and the draft's persisted list. MATCH.
- "shopping site is omitted": literal site label `shopping` (universe: gitlab 204, map 128,
  reddit 129, shopping 192, shopping_admin 184, wikipedia 23) is absent from all 16 tasks'
  sites; `shopping_admin` present only via task 759. MATCH (substring caution resolved).
- String operator task counts: exact_match 45, must_include 176, fuzzy_match 118
  (approach combos: em45, mi172, fm114, fm+mi4, None477). Coexistence caveat true (4 tasks
  carry fuzzy+must_include). MATCH.
- program_html targets 651; required_contents operators exact_match 188 + must_include 463
  (no target carries both — consistent with the source's elif). MATCH.
- Locator classes: full-page 105, JavaScript 524, helper(func:) 22 (sums to 651). MATCH.
- Target URL classes: last 238, navigation 338, helper(func) 75 (sums to 651). MATCH.
- Schema findings 0: no unknown eval_types, no url_match task missing reference_url;
  url_note only "GOLD in PRED" (196) or absent (9). MATCH. (Note: 477 tasks have
  reference_answers=null — only non-string_match tasks; not a schema defect, not claimed.)
- All 36 `fuzzy_match == "N/A"` tasks hold only the fuzzy_match approach — draft's
  RevStringFuzzy claim verified against population. MATCH.
- task0 eval block spans source lines 18–28 as cited. MATCH.
- Case facts: T590 intent "1/16/2023…1/30/2023" vs targets "Jan 16, 2030"/"Jan 30, 2030" —
  date-key disagreement verbatim in authored bytes. T97 must_include `914km` vs raw
  annotation `914 km`. T356/T759 locators `[name="route_from"` / `[name="route_to"` and
  T424 `[id="sidebar_content"` each contain an unclosed attribute-selector bracket
  (1 `[`, 0 `]`). T173 fuzzy_match → llm judge; T791 fuzzy "N/A" exact/fallback with
  string_note "the subreddit does not exist". All MATCH.
- Sample vector: across the 16 tasks — 0 func: target URLs, 0 func: locators, 0 prep_actions,
  0 ` |OR| ` must_include entries. Draft's stated omissions confirmed. (Population still
  holds 75 helper URLs / 22 helper locators / 10 prep targets / 5 OR entries — correctly
  framed as an unclosed coverage gap.)

### S062 — evaluation_harness/evaluators.py (sha256 e23edb39…, 374 lines)
Re-opened every cited range:
- StringEvaluator 71–170; clean_answer 80–86 (strip, one outer quote pair, lowercase);
  routed pre-clean of pred at 134 → normalization applied twice; non-idempotent
  (e.g. `''a''` → `a` vs `'a'`). MATCH.
- must_include 98–111 tokenize branch (flag AND len(clean_ref)==1 AND
  len(word_tokenize(clean_ref))==1); call site 142–149 sets tokenize=(len(value)==1). MATCH —
  minor wording note below.
- fuzzy_match→llm_fuzzy_match 150–169; N/A branch 152–163: exact first, then
  `score = 1.0 * ua_match(...)` at 159 — assignment override, not product. MATCH.
- URLEvaluator 173–241: rstrip("/") 189; netloc+path base 195; split " |OR| " 213;
  GOLD-in-PRED substring 220–227; pooled queries defaultdict(set) 204–209 checked
  per-key any-of-values 229–235 — query values genuinely pooled across alternatives,
  not paired per base path; scheme/fragment ignored. MATCH.
- HTMLContentEvaluator 244–333: exact_match elif must_include order 305–312; func: URL
  eval 263–266; `url != "last"` → goto + sleep(3) 271–273; JS locator exception → ""
  288–294; func: locator eval unguarded 296–299; unknown locator ValueError 300–301;
  html.unescape 303. MATCH.
- EvaluatorComb 336–352 ordered product; router 355–374 preserves declared eval_types order.
  MATCH.

### S063 — evaluation_harness/helper_functions.py (sha256 ec758da4…, 221 lines)
- llm_fuzzy_match 146–173 and llm_ua_match 176–208, both model="gpt-4-1106-preview",
  temperature=0; unexpected replies hit `assert` (172/207) rather than returning a score —
  draft's "can reach assertions rather than a normal score" MATCH. Exact-N/A bypasses the
  judge (S062:152–155). Dynamic helper functions exist as text
  (shopping/reddit/gitlab helpers 23–143) — inspected as text only, as claimed.

## Command comparison
`PYTHONDONTWRITEBYTECODE=1 python3 plans/benchmark_spec_audit.py --summary` and `--json`:
EVAL_TYPE_SETS, SITE_SETS, STRING_OPERATORS, HTML_OPERATORS, LOCATOR_CLASSES,
target_url_classes {helper75,last238,navigation338}, TOTAL task_count=812, strata=27,
selected_count=16, program_html_targets=651, findings=0, selected IDs — all identical to
my independent derivation above. Receipt `corpus/evidence/round28-calibration/audit-summary.txt`
matches the live output. `build-acceptance/audit-current.stdout` referenced by the draft
exists under `.ufo/waves/round-28/build/build-acceptance/`. Selftest "21 cases exit 0" and
oracle agreement are stated consistently with wave context (selftest not re-run by this seat;
not required for the re-read).

## Non-numeric contract checks
- LIMIT/honesty framing consistent with source facts: hosted judges unverified, static-only,
  no bypass/runtime claims; falsifier list is concrete and testable.
- Calibration/scope paragraph consistent with claims file (novelty7/calibration8, distinct
  populations, no combined improvement).
- All 16 `build/TaskNNN.md` reports and `Rev*.md` references exist at the cited paths.

## Findings (residual, non-blocking)
1. Line 31: "tokenization only when its tokenize flag is true AND the cleaned reference is
   one character" lists necessary conditions but omits the third conjunct in S062:103–107
   (`len(word_tokenize(clean_ref)) == 1`). Sourced lines are correct and the statement is
   not false as written; an exhaustive reading would mention the single-token guard.
2. Line 40: "other URLs navigate" — literally, after func: URL evaluation a func URL
   returning "last" would not navigate (S062:271 tests the evaluated string). No pinned
   task exercises this; statement is effectively true for the population.
3. Upstream commit date 2025-11-26 is not derivable from fixture bytes (no commit metadata
   pinned); consistent with manifest/receipt text, flagged as unverifiable-bytes only.

## VERDICT: PASS
Every location, number, sample fact, and contract claim in the draft is supported by the
pinned sources at the cited lines; independent census and `--summary`/`--json` agree on all
counters including the 16 selected IDs. Findings 1–3 are precision footnotes, not
corrections. This report is explicit Q13 support at actual admission for these exact bytes
(SHA256 77e19d5b…); any candidate byte change requires same-identity re-read.

## Dated re-read 2026-10-21 — corrected candidate frozen v2 (requested by KengakuR28)

The v1 sections above are preserved unchanged; they concern historical candidate `77e19d5b…`. This section covers only the post-falsification v2 bytes.

- Canonical candidate (not admitted; `corpus/knowledge/webarena-task-spec-audit.md` does not exist at check time): `corpus/knowledge/webarena-task-spec-audit.md`.
- Current draft, read in full (163 lines): `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, 14419 bytes, SHA256 `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182`. Re-hashed unchanged after all checks. Matches `candidate_sha256` in `.ufo/waves/round-28/candidate-freeze-v2.json` (freeze file SHA256 `7bfa6b5b013acbb5828dcfc6147e1e2eb0006e05e481520d3c833a3ac58dd259`; supersedes v1 `77e19d5b…`).
- Instrument bytes match the freeze: `plans/benchmark_spec_audit.py` `b7524c2f…`, `plans/registry_check.py` `fc388c33…`, `plans/state_check.py` `5db1eb78…`.

### Sources reopened (2026-10-21; scratch copies in `.ufo/waves/round-28/scratch/FFullEntry/`)

| source | opened bytes / page | located evidence re-derived | result |
|---|---|---|---|
| S061/S068 | `config_files/test.raw.json` at dce04686 via curl: SHA256 `7b50386f…`, 880776 B, identical to pinned manifest | line 16 `"intent": "What is the top-1 best-selling product in 2022",`; line 18 `"eval": {`; line 19 `"eval_types": [` (2 whitespace words); lines 22–24 `reference_answers`; line 26 `program_html`; line 29 `},` closing eval, so eval 18–29; task index 0 has task_id 0 | supported |
| S062 | `evaluation_harness/evaluators.py` at dce04686 via curl: SHA256 `e23edb39…`, 13264 B, identical | StringEvaluator clean 80–86, exact 90–94, must_include 98–111 with tokenize guard 103–107, call site 142–149, fuzzy 150–169, N/A 152–163, routed pre-clean 134; URL 173–241 (clean 187–190, OR split 213, base/query pooling 199–210 and 229–235, default `GOLD in PRED` 215); HTML 244–333 (unescape 303, `last` branch 271–273, JS except 292–294, helper 296–299, exact before must_include 305–332); composite product 351, comb 348–352, router 361–374 | supported |
| S063 | `evaluation_harness/helper_functions.py` at dce04686 via curl: SHA256 `ec758da4…`, 7565 B, identical | llm_fuzzy_match 146–173 (model 162, keywords 169–173, assert 172); llm_ua_match 176–208 (model 197, keywords 204–208, assert 207); dynamic helpers 23–143 | supported |
| LICENSE | `LICENSE` at dce04686 via curl: SHA256 `c71d239d…`, 11357 B, identical; header "Apache License Version 2.0, January 2004" | Apache-2.0 retained as claimed | supported |
| S005 | openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/, dated February 23, 2026 | "## Background", second bullet: "Many task statements were underspecified, which could lead to multiple valid interpretations - while the tests only covered a specific one." verbatim; len(split) = 21 | supported; OpenAI self-report |
| S006 | openai.com/index/separating-signal-from-noise-coding-evaluations/, dated July 8, 2026 | "## Methodology", paragraph after the workflow image: "An initial automated filter reviews the instructions given to the model, attempts by the model to solve the task, and the tests" verbatim; len(split) = 22; source continues "used to grade these attempts" | supported; OpenAI self-report |
| S069 | evaluators.py line 159 `score = 1.0 * self.ua_match(` (5 whitespace words); line 351 `score *= cur_score`; N/A branch 152–163 | assignment at 159 and multiplicative composite at 351 both match | supported |

Supplemental read-only lookups (not among the five named URLs; used only for the date claims in F2–F3): GitHub API commit/tags/releases for web-arena-x/webarena, and arXiv 2307.13854 abstract page. No benchmark site, browser action, upstream execution or import was used.

### Revised numbers and counts

| claim in v2 | independent derivation | result |
|---|---|---|
| 67 selftests | `final-acceptance/audit-selftest.stdout` has one line, `SELFTEST clean cases=67`; 67 names parsed, 67 distinct, last name `cli_manifest_pin`; `commands.json` exit 0. A fresh `--selftest` run (`PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3`) gave stdout byte-identical to the receipt, SHA256 `c3d54a97…`, exit 0. Mutations run only in `tempfile.TemporaryDirectory` copies (`benchmark_spec_audit.py` lines 366–401). | supported |
| 21 build selftest cases | `build-acceptance/audit-selftest.stdout`: `SELFTEST clean cases=21`, SHA256 `305ef8e4…` (historical build receipt) | supported |
| URL 205 = 196 + 9 | url_match tasks: 66 + 10 + 129 = 205. Explicit `url_note` 196, all `GOLD in PRED`; absent 9, defaulted to `GOLD in PRED` (S062:215). Instrument `url_rules {GOLD in PRED: 205}`, `url_note_origin {explicit: 196, defaulted: 9}`; oracle agrees. | supported |
| S068 anchors | see the S061/S068 row | supported |
| S069 anchors | see the S069 row | supported |
| counts unchanged | 812 tasks, 812 distinct IDs 0–811; eval-type sets 325/282/66/10/129; 27 strata; 16 selected = 389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399; string operators 45/176/118; 651 targets with 188 exact and 463 must_include; locators 105/524/22; target URLs 238 last/338 navigation/75 helper; schema findings 0; JSON `raw_task` equals the parsed raw task for 812/812 | unchanged |

Reproduction: `--json` SHA256 `ad53df24…` equals `final-acceptance/audit-current.stdout`. `--summary` text equals `audit-summary-final.txt` except that the receipt carries a wrapper line `exit=0`. `plans/fixtures/r28/benchmark_oracle.py` stdout SHA256 `13a1bc20…` equals the receipt; its 16 metric keys equal the instrument's, and its selected IDs equal the instrument's, so "agrees on every metric and selected ID" holds.

Receipt digests: `candidate-freeze-v2.json` `7bfa6b5b…`; `final-acceptance/acceptance.json` `a76eb360…` (checks 11, failed 0, corrected invariant); `final-acceptance/admission-source-links.json` `dee129b6…` (red exit 1 with 7 `admission_used_by_missing`; green exit 0; `actual_admission_present: false`); `final-acceptance-run.txt` `a9f86601…`; `build-acceptance-run.txt` `7e36d61d…`, the initial red run (`AssertionError: historical per-ID verdict changed`, exit 1), retained. I did not rerun `acceptance.py`.

### Findings (corrections requested; no production or candidate edits made)

- F1 (precision, draft lines 27–28): "Only fixture login-state path strings occur in the task data; no account/token/cookie values … were opened." Scan results: login-state fields are `storage_state` path strings (684 non-null, five distinct `./.auth/*.json` paths, 128 null) and `require_login` booleans (812 true). No `password`, `passwd`, `api_key` or `Bearer` strings occur; `token`, `cookie` and `secret` appear only as page wording ("Get me my RSS feed token", "Enable Cookies", page title "Secret"). Account usernames occur as ordinary task text (`byteblaze` 164 times, `MarvelsGrantMan136` 5 times). Correction: say login-state fields hold only storage_state path strings and boolean flags, that no credential, token or cookie values occur, and that account usernames appear as task text.
- F2 (sourcing and date, draft lines 16–17 "including the 2023-07-25 release"): unsourced. `corpus/SOURCES.md` and the candidate cite no URL or row for this date. Public evidence: GitHub tags are v0.1.0 (published 2023-08-23) and v0.2.0 (published 2023-10-21); commit `b454f2dc…`, titled "release commit", has committer date 2023-07-25T10:30:29Z; arXiv 2307.13854 v1 reads "Submitted on 25 Jul 2023". Correction: register and cite one specific source, naming it accurately (commit or arXiv v1 date), or drop the date. Do not describe it as a tagged release.
- F3 (sourcing, draft lines 15–16 "committed2025-11-26"): the value is verified, but no URL supports it in the header or in any row. The GitHub API commit record for dce04686 gives author and committer date 2025-11-26T21:15:59Z (`https://api.github.com/repos/web-arena-x/webarena/commits/dce04686a56253aefba7b18a4fa0937cf1dc987b`). Correction: add that URL to the header or to the S061 row.
- F4 (precision, draft line 45): "HTML targets using `last` do not navigate." The source tests the evaluated target URL after func: substitution against the literal "last" (S062:263–273). Correction: "targets whose evaluated URL equals `last`." Count-neutral; not measured.
- Resolved from v1: v1 Finding 1 (missing tokenize conjunct) is now stated in v2 line 36. v1 Finding 3 (date not derivable from fixture bytes) is now verified by F3. v1 Finding 2 persists as F4.
- Not re-derived here: qualitative routing sentences (lines 160–162) and process statements.

### VERDICT: PARTIAL

Every revised number (67 selftests, 21 build cases, URL 205 = 196 + 9, unchanged counts), every S061/S068, S062/S069 and S063 location and quote, and both S005/S006 quotes are supported by the reopened bytes. The verdict is PARTIAL, not PASS, because F1–F3 need correction and F4 needs wording. No numeric or location error was found, so this is not FAIL. While the verdict is PARTIAL, this section gives no Q13 support. Canonical `corpus/knowledge/webarena-task-spec-audit.md` stays unadmitted. Any correction changes the digest, and the corrected bytes need a same-identity re-read.

Installs or updates during this check: none.

## Final full-entry judgment 2026-10-21 — candidate frozen v3 (requested by KengakuR28)

The earlier sections are preserved unchanged. They cover historical v1 `77e19d5b…` and v2 `3eb2afe5…`. This section judges only the v3 bytes.

- Final candidate bytes: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, 14731 bytes, 167 newline-terminated lines. SHA256 `1cda3cdf7937d236af2d7f6e9834dbb64690040ad4bef7fa9394112bf2369615`; SHA1 `6e945dbaf07f7a858455f5026b6b3aa6e7c450e7`.
- Canonical candidate (not admitted; `corpus/knowledge/webarena-task-spec-audit.md` is absent at check time): `corpus/knowledge/webarena-task-spec-audit.md`.
- `candidate-freeze-v3.json` records `candidate_sha256` `1cda3cdf…`, supersedes v2 `3eb2afe5…`, and pins the same three instrument digests.
- Digest note: the IRC message gave `cda3cdf7937d236af2d7f6e9834dbb64690040ad4bef7fa9394112bf2369615`, labelled SHA1. That string has 63 hex digits and omits the leading `1`. The correct SHA256 is `1cda3cdf…`, and the true SHA1 is `6e945dba…`.

### Bounded delta against v2 (exact, not inferred)

- In a scratch copy (`scratch/FFullEntry/v2-reconstructed.md`), I reverted exactly three v3 blocks to their v2 wording: lines 17–21 (scope and commit date), lines 29–32 (login/account sentence), and lines 48–49 (`last` sentence). The result has SHA256 `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182` and 14419 bytes, which equals the frozen v2 digest. The unified diff from v3 to v2 has four hunks and nothing else.
- Every other byte of v3 is therefore identical to the v2 bytes covered by the complete v2 reread. Those v2 checks carry forward.

### Requested corrections, checked against sources

| finding | v3 wording | check | result |
|---|---|---|---|
| F1 login/account | "Fixture login-state paths and public usernames occur as authored task data; no authentication-secret values, cookies or contents of auth-state files were opened." | storage_state paths: 684 non-null (5 distinct), 128 null; require_login true for 812. Usernames occur as task text (`byteblaze` 164 times, `MarvelsGrantMan136` 5 times). Credential scan of the raw JSON and the opened .py fixtures found no literal password, token, cookie or secret value. Matches are intent or page text ("RSS feed token", "Enable Cookies", page title "Secret") and code that reads `ACCOUNTS[...]["password"]` or builds Bearer headers at runtime. No auth-state file was opened. | supported |
| F2 July release | "including earlier paper-era snapshots and WebArena-Verified" | No "2023-07-25", "07-25" or "July" remains in v3. The only "2023" is Task590 intent text ("January2023"). | supported |
| F3 commit API | URL `https://api.github.com/repos/web-arena-x/webarena/commits/dce04686a56253aefba7b18a4fa0937cf1dc987b`; field `.commit.committer.date` = `2025-11-26T21:15:59Z` | Fetched 2026-10-21 to scratch `commit.json` (SHA256 `c47ee922ea0e8a349776fc1e6216b7afc7e5c8499c6347c6233da6c10e1b73da`). The sha is dce04686…; `commit.committer.date` and `commit.author.date` are both `2025-11-26T21:15:59Z`. The path matches the JSON structure. | supported |
| F4 `last` | "When the resolved target_url equals `last`, the page-content check does not navigate; otherwise it navigates and sleeps a fixed interval, conditional on no propagated runtime error." | evaluators.py 263–266 (func: substitution) and 271–273 (`if target_url != "last": page.goto(...); time.sleep(3)`). There is no try around goto in HTMLContentEvaluator, so a goto error propagates and skips the sleep. | supported |

### Instruments and counters unchanged

- SHA256 digests match the freeze: `plans/benchmark_spec_audit.py` `b7524c2f…`; `plans/registry_check.py` `fc388c33…`; `plans/state_check.py` `5db1eb78…`.
- Fixture SHA256 digests match the manifest: test.raw.json `7b50386f…`; evaluators.py `e23edb39…`; helper_functions.py `ec758da4…`; LICENSE `c71d239d…`.
- `--json` run with bytecode disabled: SHA256 `ad53df24…`, equal to `final-acceptance/audit-current.stdout`. `--summary` equals `audit-summary-final.txt` except the wrapper line `exit=0`.
- `final-acceptance/acceptance.json` SHA256 `a76eb360…`, unchanged.

### Remaining location claims, checked this pass

- `corpus/README.md` has `## Frontier` at line 253. The entry "Agentic benchmark task-spec audits" is at line 258, under that heading. Supported.
- `plans/round-28-claims.md` lines 8–9: C1 novelty axis 7 and C2 calibration 8. Supported as "novelty7 and calibration8".
- The routing paragraph (v3 lines 164–165) matches `corpus/lessons/round-28.md` lines 82–84 (kengaku, chousa, tameshi, kotoba, kake). Supported as a qualitative routing statement.

### Non-blocking notes (they do not change the verdict)

- N1, typography: about 36 word–number joins have no space, e.g. `committed2025-11-26` (line 16), `as2025-11-26T21:15:59Z` (line 21), `task0 intent16 … eval18–29` (line 1), `URL173`, `HTML244` and `UA146` (line 1), `passed21`, `executes67` and `exit0` (lines 130, 146), `string_match325`, `temperature0`, `January2023` and `name2030` (line 86), `IDs0–811` (line 114), `page105` (line 120), `at134`, `first16`, `novelty7` and `calibration8`. Values are unaffected. Fixing them changes the bytes and needs a same-identity re-read.
- N2, registry bookkeeping: the commit-API URL is cited in the body but is not yet in the header source list or `corpus/SOURCES.md`. Before admission, L1 should add a row or S061 cell citing that URL and scratch SHA256 `c47ee922…`. This is registry-only and does not change candidate bytes.

### VERDICT: PASS (candidate SHA256 1cda3cdf7937d236af2d7f6e9834dbb64690040ad4bef7fa9394112bf2369615)

Every location, number and claim in v3 is supported by the reopened sources and receipts. The delta against v2 is exact and limited to the three requested blocks. Instruments, fixtures and counters are unchanged. Earlier verdicts stay historical: v1 PASS was for `77e19d5b…`, and v2 PARTIAL was for `3eb2afe5…`.

Admission conditions: copy these exact bytes, and register the commit-API URL (N2) without editing candidate bytes. Any byte change, including the typography fixes in N1, voids this PASS and needs a same-identity re-read.

Installs or updates during this check: none.

## Final same-identity judgment 2026-10-21 — candidate frozen v4 (requested by KengakuR28)

Earlier sections stay unchanged. v1 (`77e19d5b…`), v2 (`3eb2afe5…`) and v3 (`1cda3cdf…`) are historical. This section judges only the v4 bytes.

- Judged bytes: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, 14594 bytes, 167 lines. SHA256 `50589759b82b26a7199d157035c852260ab1b10b59815f7b57e7534eccfd2ead`; SHA1 `12a9f59096d70be72861e5d7f181dea6e389f6c1`. This matches the IRC value (64 hex digits, checked), `candidate_sha256` in `candidate-freeze-v4.json` (which supersedes v3 `1cda3cdf…`), and the scope note.
- Canonical candidate: `corpus/knowledge/webarena-task-spec-audit.md` is now present, 14594 bytes, written 12:31:16 after freeze v4 (12:27:55). It is `cmp`-identical to the draft and has the same SHA256, so this PASS covers the canonical bytes. The earlier "absent" notes were correct only for their check times. `corpus/README.md` and `corpus/lessons/round-28.md` now mention the file; that index and lesson bookkeeping is outside this Q10 judgment and was not checked.
- Freeze v4 instrument digests match the live files: `benchmark_spec_audit.py` `b7524c2f…`, `registry_check.py` `fc388c33…`, `state_check.py` `5db1eb78…`.

### Bounded delta v3→v4 (exact)

- v3 was rebuilt from the verified v2 scratch copy plus the three v3 blocks, and its SHA256 `1cda3cdf…` was reproduced exactly. A unified diff against live v4 has five hunks, and 153 of 167 lines are unchanged.
- Hunk 1, v4 lines 15–19 (v3 15–21): the commit date `committed2025-11-26` and the commit-API sentence are removed. The header names only the snapshot `dce04686…`. No `2025` token remains in the draft.
- Hunk 2, v4 lines 107–108: the repaired summary is named as `corpus/evidence/round28-calibration/audit-summary-final.txt`.
- Hunk 3, v4 lines 126–128: operation and error-phase text is now "hand-read annotations, not automatically checked by the AST or validated merely by the source hash".
- Hunk 4, v4 line 130: `passed 21` and `executes 67` (spacing only).
- Hunk 5, v4 lines 137–139: "no vacuity advisories"; vacuity, shadowed-key and dead-field classification is stated as outside the instrument.

### Checks on the changed claims

- Header: the commit SHA `dce04686a56253aefba7b18a4fa0937cf1dc987b` equals the fixture manifest's `upstream_revision` and the fetched commit record. The only 2023 token is authored Task590 intent text ("January2023"). No `07-25`, `July` or `api.github` string remains. Supported.
- Receipt: `audit-summary-final.txt` exists (SHA256 `8019499e…`). Its counters match `--summary` output except the wrapper line `exit=0`. Supported.
- Annotations: the `scorer_contract` operation and failure-phase texts are literal strings in the instrument. The AST is used only for dispatch and for the statement lines 351 and 159. The manifest hash check covers source bytes only. Supported.
- Vacuity: the instrument produces no vacuity or advisory output. "vacuity" appears only in a LIMIT line and in native-vacuity selftest names that expect no findings. All 812 tasks are `SCHEMA_COMPATIBLE`. Supported.
- Counts: `audit-selftest.stdout` reports `cases=67` (SHA256 `c3d54a97…`, unchanged). The build receipt reports 21. The C2 registry receipt reports `cases=15`, which the candidate does not cite.

### Previously unchecked v2 sentences, now checked

- "malformed eval-type projections retain the raw value and label invalid histogram buckets": eval-type histograms use bucket `<INVALID>` (instrument lines 87–88), flag histograms use the `invalid:` prefix (line 70), and per-task records keep the raw `eval_types` (line 157). Supported.
- "raw and effective URL-note fields distinguish presence from defaulting": per-task `url_note`, `url_note_present` and `effective_url_rule` exist, and `url_note_origin` is {explicit 196, defaulted 9}. Supported.
- "No dormant branch is called validated": the instrument and JSON contain no positive validated label. "success" appears only in limitation text and authored intent strings. Supported.

### Counters, fixtures and instruments unchanged

- `--json` (bytecode off): SHA256 `ad53df24…`, matching the receipt.
- `--summary` matches `audit-summary-final.txt` except the wrapper line.
- Fixture SHA256 digests match the manifest: test.raw.json `7b50386f…`, evaluators.py `e23edb39…`, helper_functions.py `ec758da4…`, LICENSE `c71d239d…`.
- The F1 login sentence (v4 lines 27–30, formerly 29–32) and the F4 `last` sentence (v4 lines 46–47, formerly 48–49) are unchanged.

### Non-blocking notes

- N1, typography: 32 word–number joins remain (27 lowercase, 5 uppercase). Examples: `exit0` (lines 130, 146), `string_match325`, `temperature0` (38), `January2023` and `name2030` (84), `IDs0` (113), `page105` (119), `at134` (36), `first16` (66), `novelty7` and `calibration8` (161–162), `URL173`, `HTML244`, `UA146`, and `task0 intent16 … eval18–29` (line 1). Values are unaffected. Any fix changes the bytes and needs a same-identity re-read.
- N2, closed: the commit-date and API assertion was removed, so no registry row is needed for it.

### VERDICT: PASS (candidate SHA256 50589759b82b26a7199d157035c852260ab1b10b59815f7b57e7534eccfd2ead)

Every location, number and claim in v4 is supported by the reopened sources and receipts. The v3→v4 delta is exact and limited to the five hunks above. The previously unchecked v2 sentences now check out, and the instruments, fixtures and counters are unchanged. This PASS gives Q13 support at actual admission only for these exact bytes; presence alone is not endorsement. The canonical copy is identical. Any byte change, including the N1 fixes, voids this PASS and needs a same-identity re-read.

Installs or updates during this check: none.
