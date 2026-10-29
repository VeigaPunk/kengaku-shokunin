# C1MutCounter: mutation table for `plans/round53_c1_triage.py` (wave 1, seat C1MutCounter)

Base file: `plans/round53_c1_triage.py` at `1373b6c` (claims commit `a34838f`, sha256 `1ba1a800…931bf`). Line numbers refer to that file.

Column `frozen suite` = the frozen 22-case `--selftest`. Column `+kill cases` = the same file plus the 47 cases in `survivor-kill-cases.diff`. `killed` = selftest exit code changes or the `cases=… failures=…` line changes (or the selftest raises). Null mutant N00 is not killed under either suite.

| id | group | line | mutation (old → new) | what it is | frozen suite | +kill cases | real-tree probe (visible on current tree) |
|---|---|---|---|---|---|---|---|
| P01 | PINS | 81 | `== cfg["POP_SHA"]` → `!= cfg["POP_SHA"]` | pop digest comparison inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (48 FAIL) | y |
| P02 | PINS | 82 | `== cfg["PIN_TREE_SHA"]` → `!= cfg["PIN_TREE_SHA"]` | pin-tree digest comparison inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P03 | PINS | 83 | `== cfg["TESTS_INDEX_SHA"]` → `!= cfg["TESTS_INDEX_SHA"]` | tests-index digest comparison inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P04 | PINS | 86 | `if pop_ok and pin_ok:` → `if pop_ok or pin_ok:` | population walk gated by OR | n | n (equivalent) | — |
| P05 | PINS | 94 | `if p == cfg["EXCLUDED_PATH"]:` → `if p != cfg["EXCLUDED_PATH"]:` | excluded path test inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P06 | PINS | 95 | `(not f.exists())` → `(f.exists())` | excluded capture must be absent: clause dropped | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P07 | PINS | 97 | `if not f.is_file():` → `if f.is_file():` | absent capture counter inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P08 | PINS | 99 | `== blobs.get(p):` → `!= blobs.get(p):` | blob-SHA1 match inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (46 FAIL) | y |
| P09 | PINS | 106 | ` and absent == 0` → (deleted) | absent==0 clause dropped (equivalent given blob_bad/match) | n | n (equivalent) | — |
| P10 | PINS | 106 | `match == cfg["CAPTURES_EXPECTED"]` → `match >= cfg["CAPTURES_EXPECTED"]` | captures equality relaxed to >= (equivalent given files==EXPECTED+1) | n | n (equivalent) | — |
| P11 | PINS | 106 | `pop_ok and pin_ok and idx_ok and` → `pop_ok and pin_ok and` | tests-index digest clause dropped from PINS verdict | n | y — ext-tests-index-digest (1 FAIL) | n |
| P12 | PINS | 107 | `exc_ok and ` → (deleted) | excluded-blob clause dropped from PINS verdict | n | y — ext-excluded-capture-present (1 FAIL) | n |
| P13 | PINS | 107 | `+ 1)` → `+ 0)` | population count off by one (EXPECTED+0) | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (46 FAIL) | — |
| F01 | FREEZE | 131 | `sha256_file(clf) == d.get` → `sha256_file(clf) != d.get` | classifier digest comparison inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (7 FAIL) | — |
| F02 | FREEZE | 134 | `if c_fz and c_lab and c_fz != c_lab:` → `if c_fz and c_lab and c_fz == c_lab:` | freeze-before-labels order test inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (6 FAIL) | n |
| F03 | FREEZE | 135 | `)[0] == 0` → `)[0] != 0` | is-ancestor test inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (8 FAIL) | — |
| F04 | FREEZE | 135 | `order = git(lane, "merge-base", "--is-ancestor", c_fz, c_lab)[0] == 0` → `order = True` | ancestry check dropped | n | y — ext-freeze-after-labels (2 FAIL) | n |
| F05 | FREEZE | 137 | `ok = sha_ok and order and` → `ok = sha_ok and` | freeze ordering clause dropped from FREEZE verdict | n | y — ext-freeze-leg-order-clause (1 FAIL) | — |
| F06 | FREEZE | 137 | ` and bool(info["authors"])` → (deleted) | non-empty author_seats clause dropped (equivalent: verdict gates on authors at L374) | n | y — ext-freeze-leg-empty-authors (1 FAIL) | — |
| L01 | LABELS | 150 | `len(set(r["labelers"])) != 2` → `len(set(r["labelers"])) < 2` | two-distinct-labelers test relaxed to <2 | n | y — ext-labelers-three-distinct (1 FAIL) | — |
| L02 | LABELS | 152 | ` or set(r["labelers"]) & authors` → (deleted) | labeler-is-author rejection branch deleted | y — forged-labeler-is-author | y — forged-labeler-is-author (1 FAIL) | — |
| L03 | LABELS | 152 | ` or any(x not in ("Y", "N", "U") for x in r["labels"])` → (deleted) | label-domain rejection branch deleted | n | y — ext-label-domain-X (2 FAIL) | — |
| L04 | LABELS | 156 | `if a == b and a in ("Y", "N"):` → `if a in ("Y", "N"):` | agreement requirement dropped: disagreeing pair decided | n | y — ext-label-disagree-contested (3 FAIL) | — |
| L05 | LABELS | 150 | `(not isinstance(r, dict) or ` → `(` | missing-row (non-dict) rejection branch deleted | n | y — traceback (0 FAIL) | — |
| L06 | LABELS | 150 | `not isinstance(r.get("labelers"), list) or ` → (deleted) | labelers-is-list rejection branch deleted | n | y — ext-labelers-not-a-list (1 FAIL) | — |
| O01 | ORACLE | 198 | `if (v2[t] == "P1") != (y == "Y")` → `if (v2[t] == "P1") == (y == "Y")` | v2 disagreement count inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (10 FAIL) | — |
| O02 | ORACLE | 199 | `if (r52[t] == "P1") != (y == "Y")` → `if (r52[t] == "P1") == (y == "Y")` | r52 control disagreement count inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (10 FAIL) | — |
| O03 | ORACLE | 203 | `dis52 >= CONTROL_RATIO * max(dis, 1)` → `dis52 > CONTROL_RATIO * max(dis, 1)` | control ratio >= relaxed to > | y — genuine-fixture-passes | y — genuine-fixture-passes (6 FAIL) | — |
| O04 | ORACLE | 203 | ` and dis52 >= CONTROL_MIN` → (deleted) | control minimum clause dropped | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (2 FAIL) | — |
| O05 | ORACLE | 204 | `and not extra and` → `and` | extra label-row clause dropped | n | y — ext-extra-label-row (1 FAIL) | — |
| O06 | ORACLE | 204 | `and not uncl and` → `and` | unclassified=0 clause dropped | n | y — ext-scale-unclassified-10 (1 FAIL) | — |
| O07 | ORACLE | 204 | `ok = (n == cfg["TESTS_TOTAL"] and not bad and` → `ok = (n == cfg["TESTS_TOTAL"] and` | bad-label-row clause dropped | n | y — ext-scale-bad-label-row (1 FAIL) | — |
| O08 | ORACLE | 204 | `n == cfg["TESTS_TOTAL"] and ` → (deleted) | tests-count clause dropped (equivalent given TESTS_INDEX_SHA pin) | n | y — ext-tests-total-mismatch (1 FAIL) | — |
| O09 | ORACLE | 205 | `and dis <= lim` → `and dis < lim` | disagreement limit <= relaxed to < (boundary) | n | y — ext-scale-disagree-at-limit-3 (1 FAIL) | — |
| O10 | ORACLE | 205 | `len(contested) <= ORACLE_MAX_CONTESTED * n` → `len(contested) < ORACLE_MAX_CONTESTED * n` | contested limit <= relaxed to < (boundary) | n | y — ext-scale-contested-at-limit-15 (1 FAIL) | — |
| O11 | ORACLE | 205 | `and ctl_ok)` → `)` | ORACLE-CONTROL clause dropped from verdict | n | y — ext-oracle-control-clause-in-leg (2 FAIL) | — |
| O12 | ORACLE | 202 | `lim = ORACLE_MAX_DISAGREE * max(1, len(decided))` → `lim = ORACLE_MAX_DISAGREE * max(1, len(ids))` | disagreement denominator: decided -> all tests | n | y — ext-scale-disagree-3-of-85-decided (1 FAIL) | — |
| K01 | CONFIRM | 266 | `if r.get("confirmed") is not True:` → `if not r.get("confirmed"):` | confirmed weakened from `is not True` to falsy | y — forged-confirmed-string | y — forged-confirmed-string (1 FAIL) | — |
| K02 | CONFIRM | 270 | `elif r["task"] not in cand or tid not in {x["id"] for x in cand[r["task"]]}:` → `elif False:` | never-read / v2-P1 candidacy check deleted | n | y — ext-candidate-v2-P0-rejected (3 FAIL) | — |
| K03 | CONFIRM | 272 | `elif r["task"] in seen_tasks:` → `elif False:` | duplicate-task rejection deleted | n | y — ext-duplicate-task-row (1 FAIL) | — |
| K04 | CONFIRM | 274 | `< QUOTE_MIN_CHARS or norm(r["quote"]) not in span:` → `< QUOTE_MIN_CHARS:` | quote-inside-test-span check deleted | y — forged-quote-outside-span | y — forged-quote-outside-span (1 FAIL) | — |
| K05 | CONFIRM | 274 | `< QUOTE_MIN_CHARS or` → `<= QUOTE_MIN_CHARS or` | quote length >= 20 relaxed to > 20 (boundary) | n | y — ext-quote-exactly-20-chars (1 FAIL) | n |
| K06 | CONFIRM | 276 | ` or r["reader"].startswith("KengakuR53")` → (deleted) | KengakuR53 reader rejection deleted | n | y — ext-reader-KengakuR53-prefix (1 FAIL) | — |
| K07 | CONFIRM | 278 | ` or r["reader"] not in str(rep)` → (deleted) | reader-name-in-report-path check deleted | n | y — ext-reader-not-in-report-path (1 FAIL) | — |
| K08 | CONFIRM | 280 | `elif r["task"] not in rep.read_text(encoding="utf-8", errors="replace"):` → `elif False:` | report-names-task check deleted | y — forged-report-names-other-task | y — forged-report-names-other-task (1 FAIL) | — |
| K09 | CONFIRM | 265 | `src[t["lineno"] - 1:t["end_lineno"]]` → `src[t["lineno"]:t["end_lineno"]]` | test span drops its def line | n | y — ext-quote-spans-def-line (1 FAIL) | — |
| K10 | CONFIRM | 268 | `elif t is None or t["task"] != r.get("task"):` → `elif t is None:` | test_id/task consistency check deleted (reason text changes only) | n | y — ext-task-testid-mismatch (1 FAIL) | — |
| K11 | CONFIRM | 289 | `ok = len(good) >= cfg["CONFIRM_MIN"]` → `ok = len(good) > cfg["CONFIRM_MIN"]` | CONFIRM minimum >= relaxed to > (cfg-level, fixture overrides) | y — genuine-fixture-passes | y — genuine-fixture-passes (6 FAIL) | n |
| A01 | PRIOR-ART | 324 | `if task not in confirmed:` → `if False:` | task-confirmed check deleted in prior-art | n | y — ext-prior-art-unconfirmed-task-row (1 FAIL) | — |
| A02 | PRIOR-ART | 326 | `elif v not in ("phenomenon-new", "phenomenon-known"):` → `elif False:` | verdict-domain check deleted | n | y — ext-prior-art-bad-verdict (1 FAIL) | — |
| A03 | PRIOR-ART | 328 | ` or "example.org" in r["url"]` → (deleted) | example.org rejection deleted (sole-check route) | y — forged-prior-art-example | y — forged-prior-art-example (1 FAIL) | — |
| A04 | PRIOR-ART | 328 | `elif not re.match(r"https?://[^/\s]+\.[^/\s]+/", str(r.get("url", "")) + "/") or` → `elif` | URL shape check deleted | n | y — ext-prior-art-url-not-a-url (2 FAIL) | — |
| A05 | PRIOR-ART | 335 | `8 <= len(q.split()) <= 25` → `7 <= len(q.split()) <= 25` | quote word-count lower bound 8 -> 7 | n | y — ext-quote-7-words-rejected (1 FAIL) | — |
| A06 | PRIOR-ART | 335 | `8 <= len(q.split()) <= 25` → `8 < len(q.split()) <= 25` | quote word-count lower bound <= swapped to < (8 excluded) | n | y — ext-quote-8-words-accepted (1 FAIL) | — |
| A07 | PRIOR-ART | 335 | `len(q.split()) <= 25` → `len(q.split()) <= 26` | quote word-count upper bound 25 -> 26 | n | y — ext-quote-26-words-rejected (1 FAIL) | — |
| A08 | PRIOR-ART | 335 | ` or q not in norm(text):` → `:` | quote-in-archive check deleted | y — forged-prior-art-quote | y — forged-prior-art-quote (1 FAIL) | — |
| A09 | PRIOR-ART | 337 | ` and task not in text:` → `:` | known-row: task-name-in-fetch alternative deleted | n | y — ext-known-names-task-not-tests (1 FAIL) | — |
| A10 | PRIOR-ART | 337 | `elif v == "phenomenon-known" and not any(n in text for n in tests_of.get(task, [])) and task not in text:` → `elif False:` | known-row naming check deleted | n | y — ext-known-names-neither-rejected (1 FAIL) | — |
| A11 | PRIOR-ART | 341 | `if not isinstance(sw, list) or len(sw) < 2:` → `if not isinstance(sw, list) or len(sw) < 1:` | new-row sweep minimum 2 -> 1 | n | y — ext-new-one-sweep-rejected (1 FAIL) | — |
| A12 | PRIOR-ART | 346 | `if st is None or task in st or any(` → `if st is None or any(` | sweep: task-name check deleted | n | y — ext-sweep-names-task-rejected (1 FAIL) | — |
| A13 | PRIOR-ART | 346 | ` or any(n in st for n in tests_of.get(task, [])):` → `:` | sweep: test-name check deleted | n | y — ext-sweep-names-test-rejected (1 FAIL) | — |
| A14 | PRIOR-ART | 314 | `if not str(r.get(key, "")).startswith(f"{RUN_DIR}/fetched/") or not f.is_file():` → `if not f.is_file():` | fetch-path-under-fetched/ check deleted | n | y — ext-fetch-outside-fetched-dir (1 FAIL) | — |
| A15 | PRIOR-ART | 316 | `if sha256_file(f) != r.get(key + "_sha256"):` → `if sha256_file(f) == r.get(key + "_sha256"):` | fetch digest comparison inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (15 FAIL) | — |
| A16 | PRIOR-ART | 358 | `and new >= 1 and not rej` → `and new >= 0 and not rej` | new>=1 score rule relaxed to >=0 | y — known-only-fails-score-rule | y — known-only-fails-score-rule (1 FAIL) | — |
| A17 | PRIOR-ART | 358 | ` and not rej` → (deleted) | one-rejected-row rule deleted | n | y — ext-prior-art-unconfirmed-task-row (4 FAIL) | — |
| A18 | PRIOR-ART | 358 | `bool(confirmed) and ` → (deleted) | non-empty confirmed clause dropped (equivalent: rej/covered gates) | n | n (equivalent) | — |
| C01 | CONST | 29 | `0230b68c666c` → `0230b68d666c` | POP_SHA first digits (CFG; selftest overrides cfg) | n | y — ext-frozen-constants (1 FAIL) | y |
| C02 | CONST | 32 | `TESTS_TOTAL = 305` → `TESTS_TOTAL = 306` | TESTS_TOTAL 305->306 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C03 | CONST | 33 | `CAPTURES_EXPECTED = 183` → `CAPTURES_EXPECTED = 182` | CAPTURES_EXPECTED 183->182 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C04 | CONST | 37 | `ORACLE_MAX_DISAGREE = 0.03` → `ORACLE_MAX_DISAGREE = 0.5` | ORACLE_MAX_DISAGREE 0.03->0.5 | n | y — ext-scale-disagree-over-limit-4 (3 FAIL) | n |
| C05 | CONST | 38 | `ORACLE_MAX_CONTESTED = 0.15` → `ORACLE_MAX_CONTESTED = 0.5` | ORACLE_MAX_CONTESTED 0.15->0.5 | n | y — ext-scale-contested-over-limit-16 (2 FAIL) | n |
| C06 | CONST | 39 | `CONTROL_RATIO = 2` → `CONTROL_RATIO = 1` | CONTROL_RATIO 2->1 | n | y — ext-scale-control-ratio-1-vs-2 (2 FAIL) | n |
| C07 | CONST | 40 | `CONTROL_MIN = 10` → `CONTROL_MIN = 11` | CONTROL_MIN 10->11 (selftest rebinds to 1 except one case) | n | y — ext-scale-control-min-at-10 (2 FAIL) | n |
| C08 | CONST | 41 | `CONFIRM_MIN = 3` → `CONFIRM_MIN = 2` | CONFIRM_MIN 3->2 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C09 | CONST | 42 | `URL_MIN = 3` → `URL_MIN = 2` | URL_MIN 3->2 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C10 | CONST | 43 | `QUOTE_MIN_CHARS = 20` → `QUOTE_MIN_CHARS = 19` | QUOTE_MIN_CHARS 20->19 | n | y — ext-quote-19-chars-rejected (2 FAIL) | n |
| C11 | CONST | 43 | `QUOTE_MIN_CHARS = 20` → `QUOTE_MIN_CHARS = 21` | QUOTE_MIN_CHARS 20->21 | n | y — ext-quote-exactly-20-chars (2 FAIL) | n |
| C12 | CONST | 35 | `EXCLUDED_BLOB = "3269e74e` → `EXCLUDED_BLOB = "3269e74f` | EXCLUDED_BLOB first digits (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | y |
| K12 | CONFIRM | 240 | ` and not seen_before(t["task"], texts)` → (deleted) | never-read check: task-seen-in-base-texts exclusion deleted | n | y — ext-candidate-seen-in-base-excluded (1 FAIL) | — |
| K13 | CONFIRM | 240 | ` and t["task"] not in r52_conf` → (deleted) | never-read check: round-52-confirmed exclusion deleted | n | y — ext-candidate-r52-confirmed-excluded (1 FAIL) | — |
| A19 | PRIOR-ART | 339 | `elif v == "phenomenon-new":` → `elif False:` | whole sweep check (phenomenon-new) deleted | y — forged-new-without-sweep | y — forged-new-without-sweep (4 FAIL) | — |

Mutants: 81 (plus null N00: not killed by either suite). Killed by frozen suite: 25. Killed by frozen suite + kill cases: 77. Survivors after kill cases: P04, P09, P10, A18 (all verdict-equivalent, see report).
