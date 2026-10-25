# R32ReconPackage — read-only reconnaissance of the staged grader-semantics package

Seat: `L1Kengaku32.R32ReconPackage` (scout, leaf). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at baseline tip `f20a1097`. Staged package `/home/vgpnk/Projects/shokuknow/merge/kengaku/` opened read-only.
**Access date for every source opened here: 2026-10-25.** No writes outside this file and
`/tmp/r32-R32ReconPackage/`. No tool installs were needed (no pacman, no uv, nothing upgraded).

VERDICT: hazard

The package is usable but **not appendable as staged**: three independent blockers (H1 date mismatch against the
frozen predicate, H2 a duplicated `S093` id inside a 15-row collision set, H3 a load-bearing number that the
executed code contradicts), plus eleven content/format hazards (H4-H14). Detail in §d; per-claim evidence in §b.

---

## Fetch identity (every quote below resolves to one of these five captures)

| ref | URL | revision | bytes / lines | sha256 |
|---|---|---|---|---|
| **F1** | `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` | commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` | 14 138 B / 297 L | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` |
| **F2** | `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/utils/evaluation/retry.py` | same commit | 4 519 B / 109 L | `db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e` |
| **F3** | `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh` | commit `66f92766bba642462d4bbe5479e83f91f9211862` | 7 864 B / 234 L | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` |
| **F4** | `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md` | same commit | 6 858 B / 126 L | `dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f` |
| **F5** | `https://arxiv.org/abs/2412.05579v2` | arXiv `2412.05579v2` ("last revised 10 Dec 2024 (this version, v2)") | 43 661 B HTML | `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` |

All five returned HTTP 200 at the pins named in the frozen claims. Captures live under
`/tmp/r32-R32ReconPackage/` (≈75 KB total, 77 040 bytes). Two existence probes returned HTTP 200 at the same S093 pin:
`…/tests/parser.py` and `…/tests/config.json`.

---

## (a) The three `source:` lines, the load-bearing claims, and the exact staged rows

### a.1 The entry's triad — `knowledge/corpus/knowledge/benchmark-grader-semantics.md:2-6` (verbatim)

```
source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `# v2/tasks/…/tests/test.sh` and `# …/tests/parser.py` — commit `66f92766bba642462d4bbe5479e83f91f9211862`
source: S094 — https://github.com/hkust-nlp/Toolathlon — `# tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`
source: S097 — https://arxiv.org/abs/2412.05579 — `# Abstract` — arXiv 2412.05579v2
verified-at: 2026-10-23
recheck: 180d — re-run the Gate commands for S093, S094 and S097 against their pinned revisions (ran 2026-10-23)
```

Three distinct ids (`S093`, `S094`, `S097`) — matches the frozen predicate's "three distinct" clause.
`verified-at` is **2026-10-23**, not the `2026-10-25` the predicate requires (H1).

### a.2 Load-bearing claims (entry line → claim, abbreviated where the table in §b carries the quote)

| # | entry line(s) | claim |
|---|---|---|
| L1 | 16-17 | `tests/test.sh` performs a "two-stage environment reset" and then computes the reward from `tests/config.json` |
| L2 | 20-21 | `all_required = fail_to_pass \| pass_to_pass`; `success = all_required <= passed_tests` |
| L3 | 24 | `passed_tests` is the set of test names whose recorded status is `PASSED` |
| L4 | 25-26 | exit code 0 writes reward 1, non-zero writes reward 0 |
| L5 | 28-29 | the grader is conjunctive over the **union**, so fixing the bug while breaking a previously-passing test scores zero |
| L6 | 30-32 | the grade is binary, no partial credit, no per-test reporting — which makes the release gate's "642 / 642 resolved" figure interpretable |
| L7 | 34 | the numbered steps are "in the order the code performs it" |
| L8 | 36-40 | step 1: tracked test-code → `git checkout HEAD --`, untracked test-code → `rm -f`; test-code identified by the parent-dir set `tests/test/__tests__/spec/specs`, basename `conftest.py`, and the three regexes |
| L9 | 41-42 | step 2: paths the patch *creates* (`--- /dev/null` side) are removed; paths it *modifies* are restored to base |
| L10 | 43-44 | step 3: stale bytecode purged via `find … __pycache__ … -exec rm -rf {} +` and `find … '*.pyc' -delete` |
| L11 | 45 | step 4: `git apply` applies the test patch |
| L12 | 46-47 | step 5: the test list is parsed from `config.json`, the suite is run, the result set reduced to the containment test |
| L13 | 51-55 | the fixture-revert step runs over `git diff --name-only HEAD --` = tracked modifications only; a file the agent **created** under `testdata/ test_data/ fixtures/ fixture/ mocks/ mock/ __snapshots__/` is absent from that list and is also excluded from step 1's test-code removal |
| L14 | 57-60 | the README's claim that "agent edits to fixtures and snapshots are reverted" holds for tracked files only; a falsifiable limit on a maintainer statement |
| L15 | 64 | `…/evaluation/main.py` never calls a model |
| L16 | 66-69 | it reads a produced `record.csv`, compares it to `groundtruth_workspace/expected_ratio.csv` via `validate_record_data(actual_records, expected_records, tolerance_pct=0.1)`, failing on missing scenarios, extra scenarios, and any rate outside the **0.1-percentage-point** tolerance |
| L17 | 70 | asserts `check_storage_bucket_exists(...)` |
| L18 | 71-72 | asserts `check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time)` — no log-bucket writes between launch and evaluation |
| L19 | 73 | and finally `validate_task_completion(...)` |
| L20 | 75-76 | the grader is a state comparison with a stated numeric tolerance plus two side-effect checks; there is no judge prompt and no rubric in the scoring path |
| L21 | 80-83 | S097 organises the space into "Functionality, Methodology, Applications, Meta-evaluation, and Limitations"; meta-evaluation is the category the lane's judge-calibration work belongs to, kept distinct from methodology **on purpose** |
| L22 | 85-90 | a benchmark's grader should be described by kind; SWE-bench Pro V2 is a deterministic containment test with a binary reward, Toolathlon a state comparison with a tolerance, an LLM judge a third kind with its own meta-evaluation requirements |
| L23 | 92 | `ground:` cites Frontier §"Agentic benchmark task-spec audits" axes A and E and §"Judge calibration applied inward" |

### a.3 Staged row `S094` — `SOURCES.append.md:24` (11 columns, verbatim cells)

| column | cell |
|---|---|
| id | `S094` |
| source | `Toolathlon task evaluation script (evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon` |
| kind | `code` |
| tier | `A` |
| scope | `the executed scoring code for one Toolathlon task at a pinned commit: what is compared, against what, and with what tolerance, for the code's own behaviour` |
| anchor | ``commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb, tasks/finalpool/ab-testing/evaluation/main.py: "def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)" comparing a produced record.csv against groundtruth_workspace/expected_ratio.csv, plus check_abtesting_logging_bucket_clean() asserting no log bucket writes between launch and evaluation`` |
| teaches | `the benchmark scores by comparing a *produced artefact* against a ground-truth artefact with a stated numeric tolerance, and checks the absence of side-effect writes — a state-based deterministic grader with no judge model in the loop` |
| status | `mined` |
| opened | `2026-10-23` |
| recheck | `2026-10-23 — re-verify at the next upstream release (Gate S094 below)` |
| used-by | `corpus/knowledge/benchmark-grader-semantics.md` |

### a.4 Staged row `S097` — `SOURCES.append.md:27` (11 columns, verbatim cells)

| column | cell |
|---|---|
| id | `S097` |
| source | `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579` |
| kind | `paper` |
| tier | `B` |
| scope | `the survey's own five-part structure for LLM-as-a-judge evaluation — functionality, methodology, applications, meta-evaluation, limitations — for the preprint's own text; tier B under row 10 because it was a preprint at the time of opening` |
| anchor | `arXiv 2412.05579v2 (submitted 7 Dec 2024, last revised 10 Dec 2024), Abstract: "This paper presents a comprehensive survey of the LMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations."; Comments: "60 pages, comprehensive and continuously updated"` |
| teaches | `the field's own survey separates *meta-evaluation* — how a judge is itself evaluated — from methodology and applications, which is the separation a calibration protocol needs; the limitations section is where a lane should look for the known failure modes of judge-based scoring` |
| status | `mined` |
| opened | `2026-10-23` |
| recheck | `2026-10-23 — re-verify at the next revision (Gate S097 below)` |
| used-by | `corpus/knowledge/benchmark-grader-semantics.md` |

### a.5 Staged row `S093` — `SOURCES.append.md:23` (the third cited id, staged as an *append*)

| column | cell |
|---|---|
| id | `S093` |
| source | `SWE-bench Pro V2 task verifier files (test.sh, parser.py, config.json) — https://github.com/scaleapi/SWE-bench_Pro-os` |
| kind | `code` · tier `A` |
| scope | `the executed grading code for one SWE-bench Pro V2 task at a pinned commit: what is restored before grading and how the reward is computed, for the code's own behaviour` |
| anchor | `commit 66f92766…, v2/tasks/instance_internetarchive__openlibrary-…/tests/test.sh: "Resetting test-space to base state (full test-code surface)..." then "find . -name '__pycache__' -type d -prune -exec rm -rf {} +" and the reward block "all_required = fail_to_pass \| pass_to_pass" / "success = all_required <= passed_tests"` |
| teaches | `the grader is a binary set-containment over the union of fail_to_pass and pass_to_pass, and the environment is reset to base state first — but the fixture-restore step iterates tracked modifications only, so an agent-added untracked file under a fixture directory survives into grading` |
| status | `mined` · opened `2026-10-23` · recheck `2026-10-23 — re-verify at the next upstream release (Gate S093 below)` |
| used-by | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md` |

---

## (b) Quote support: what the staged rows actually carry

Legend: **[Q]** an anchored quote in the row's `anchor` cell · **[P]** paraphrase only, in `anchor`/`teaches`/`scope` ·
**[—]** nothing in any staged row · **source check** = what I found at the pin (F1/F3/F4/F5).

| # | staged-row support | source check at the pin |
|---|---|---|
| L1 "two-stage … reset" | **[P]** S093 scope "what is restored before grading" | **Understated, and the count is wrong**: F3 performs **three** reset passes before `git apply` — `/tmp/reset_list.txt` (F3:36-75), `/tmp/v5_paths.txt` (F3:80-95), `/tmp/v6_modified.txt` (F3:97-105). See H4. |
| L2 containment block | **[Q]** S093 anchor quotes both lines verbatim | F3:213 `all_required = fail_to_pass \| pass_to_pass`; F3:214 `success = all_required <= passed_tests`. Exact. |
| L3 `passed_tests` = `PASSED` names | **[—]** | F3:207-210 `passed_tests = set()` / `if test.get('status') == 'PASSED':` / `passed_tests.add(test.get('name',''))`. True, but needs its own quote. |
| L4 exit code → reward 1/0 | **[—]** | F3:11-22 `cleanup_and_reward()` — `if [ "${exit_code}" -eq 0 ]; then echo 1 > /logs/verifier/reward.txt else echo 0 …`; `trap cleanup_and_reward EXIT`. True, needs its own quote. |
| L5 conjunctive over the union | **[Q]** (derivable from L2's quote) + **[P]** S093 teaches "binary set-containment over the union" | F3:213-214 + F3:227 `missing = all_required - passed_tests`. True. |
| L6 binary, no partial credit | **[P]** S093 teaches "binary set-containment" | F3:203-231 — reward is one file, one bit; `RESULT: PASSED/FAILED` only. True. |
| L6 "642 / 642 resolved" | **[—]** in all three rows | The figure is real but lives in **S078** (`v2/GATE.md`), quoted in-lane at `corpus/knowledge/benchmark-task-validity-checklist.md:48-49`. F4:98 states `731 -> 642 tasks: 89 dropped after review`. The entry borrows a number from a row it does not cite — see H6. |
| L7 "in the order the code performs it" | **[—]** | **False as written**: the bytecode purge the entry numbers *step 3* is the **first** action of F3 (F3:29-30), executed before the test-code reset (F3:36+) and before the patch-path pass (F3:77+). See H4. |
| L8 step 1 classifier | **[P]** S093 anchor quotes the *banner* `"Resetting test-space to base state (full test-code surface)..."` (F3:33) | F3:37-56 verbatim: `CODE_DIRS = {'tests','test','__tests__','spec','specs'}`; `if any(s in DATA_DIRS for s in parents): return False`; `conftest.py`; `_test\.(go\|py\|js\|jsx\|ts\|tsx)$`; `^test_.*\.py$`; `\.(test\|spec)\.(js\|jsx\|ts\|tsx)$`. F3:71-72 `T) git checkout HEAD -- "$path"` / `U) rm -f -- "$path"`. All true; the row quote is only the banner. |
| L9 step 2 patch paths | **[—]** | F3:77-91: created paths removed (F3:77-78), then per path `if git ls-files --error-unmatch` → `git checkout HEAD --` else if in `v5_created.txt` → `rm -f`; comment F3:92 `# untracked files the patch merely MODIFIES are left alone (image-provided context)`. The entry's step 2 omits that third branch. |
| L10 bytecode purge | **[Q]** S093 anchor quotes the `__pycache__` command | F3:29 `find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null \|\| true`; F3:30 `find . -name '*.pyc' -delete …`. Exact modulo the trailing redirect. |
| L11 `git apply` | **[—]** | F3:108 `git apply --verbose /tests/test_patch.patch \|\| { echo "ERROR: Failed to apply test patch"; exit 1; }`. True. |
| L12 step 5 config parse + run | **[—]** | F3:164-166 `FAIL_TO_PASS=$(python3 -c "… json.load(open('/tests/config.json')).get('fail_to_pass', [])")`; F3:183-204; F3:233-234 `exit "${EVAL_EXIT_CODE}"`. True, but the list is `config.json`'s, not "the test patch's own recorded test list" (H14). |
| L13 the asymmetry | **[P]** S093 `teaches` states exactly this conclusion; **no quote** | **True against the code**: F3:97 `git diff --name-only HEAD -- > /tmp/v6_modified.txt`; F3:99-102 `case "$p" in *testdata/*\|*test_data/*\|*fixtures/*\|*fixture/*\|*mocks/*\|*mock/*\|*__snapshots__/*) … git checkout HEAD -- "$p"`; F3:38 `DATA_DIRS = {…}`; F3:41-42 data-dir paths are `return False` from `is_test_code`. A created fixture file is in neither list. **The row's anchor must gain the `git diff --name-only HEAD --` quote** (Q3). |
| L14 README sentence | **[—]** in S093/S094/S097 | The sentence exists verbatim at **F4:103-104**: `Verifier (all 642): hidden-test paths are restored or removed before the test patch is applied; agent edits to fixtures and snapshots are reverted; stale Python bytecode is purged; a leftover git index lock no longer makes restores fail silently.` The row for F4 is **S078**, not cited (H6). |
| L15 "never calls a model" | **[P]** S094 teaches "no judge model in the loop" | F1 imports (F1:1-12) are argparse/os/csv/json/subprocess/google-cloud-storage/logging/oauth2/api_core/pathlib/datetime plus `utils.evaluation.retry.grade_with_retry`; **F2** (the only local import) imports `time` and `typing` only (F2:35-36) and polls a `Callable` (F2:48-56). True. |
| L16 tolerance **0.1** | **[Q]** S094 anchor quotes the *signature default* `tolerance_pct: float = 0.1` (F1:58) | **Contradicted for the executed path**: F1:279 `# Validate with 0.05% tolerance`; F1:280 `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)`. The default at F1:58 is never used by `__main__`. See H3. |
| L16 record.csv vs expected_ratio.csv | **[Q]** S094 anchor names both artefacts | F1:15/25 `record.csv` fields `["scenario","A_conversion %","B_conversion %"]`; F1:55 `expected_file = os.path.join(groundtruth_workspace, "expected_ratio.csv")`. True. |
| L16 missing/extra scenarios | **[P]** (implied by "what is compared") | F1:63-72 `missing_scenarios` / `extra_scenarios` → `validation_errors`. True. |
| L17 `check_storage_bucket_exists` | **[—]** (S094 anchor names only `validate_record_data` and `check_abtesting_logging_bucket_clean`) | F1:125 `def check_storage_bucket_exists(bucket_prefix: str, project_id: str = "mcp-bench0606") -> bool`; F1:225-231 called, `if not bucket_exists: raise ValueError(...)`. True but unquoted; it returns a bool, it does not `assert`. |
| L18 logging-bucket check | **[Q]** S094 anchor quotes the function name and the "no log bucket writes between launch and evaluation" reading | F1:168 signature; F1:185-192 the launch/eval time window **is** applied (`log_filter += f' AND timestamp >= …'` / `<= …`); F1:207-212 any surviving entry → `return False`. **But** F1:217-218 `except Exception as e: … return True  # Don't fail evaluation if we can't check logs` — the check **fails open**. See H5. |
| L19 `validate_task_completion` | **[—]** | F1:220-237 `def validate_task_completion(...)` raising on either sub-check. True. |
| L20 no judge prompt / no rubric | **[P]** S094 teaches "no judge model in the loop" | No prompt/rubric string in F1 or F2; grading is `ValueError` + `exit(1)`. True. |
| L21 five perspectives | **[Q]** S097 anchor quotes the abstract sentence | F5 abstract: `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` **The staged quote drops one `L`** (`LMs-as-judges`; `grep -c "the LMs-as-judges"` on F5 = **0**, `the LLMs-as-judges` = 3). See H7. |
| L21 "on purpose" | **[P]** S097 teaches "separates … from methodology and applications" | F5's abstract asserts the five parts; "on purpose" is the entry's inference and is not in the preprint's abstract. Narrow it or mark it as the entry's reading. |
| L22 "third kind with its own meta-evaluation requirements" | **[—]** | Not in F5's abstract and not in any staged row. This is the entry's synthesis — legitimate as a frame, but Q4 (negative space) and Q3 (claim inside its quote) require it be labelled as the entry's own construction. |
| L23 `ground:` line | n/a | Names Frontier sections only; does **not** name the entry it extends (`benchmark-verifier-execution-model.md`) nor `benchmark-task-validity-checklist.md` — Q6 gap (H9). |

**Net:** of the 23 load-bearing claims, **6 rest on an anchored quote in a staged row** — L2, L5 (derivable from
L2's quote), L10, L16, L18, L21 — and three of those only partially or wrongly: L16 quotes the *signature default*
rather than the call, L18 quotes the function *name* and not the fail-open branch, L21's quote is byte-wrong.
**6 are paraphrase-only** (L1, L6, L8, L13, L15, L20). **10 carry no support in any staged row** (L3, L4, L7, L9,
L11, L12, L14, L17, L19, L22). One claim (L16's 0.1) is **contradicted** by the executed code, and one (L7's
ordering) is **wrong**.

---

## (c) The `S093` row in the live registry, and its `used-by` cell

`corpus/SOURCES.md:112` — the row already exists (round 31 landed it):

| column | live cell |
|---|---|
| id | `S093` |
| source | `SWE-bench Pro V2 task verifier files (tests/test.sh, parser.py, config.json) — https://github.com/scaleapi/SWE-bench_Pro-os` |
| kind / tier | `code` / `A` |
| scope | `the executed grading code for one SWE-bench Pro V2 task at a pinned commit — the test-space reset it performs itself, the paths that reset skips, and the log-scan parser behind its PASSED set` |
| anchor | `commit 66f92766bba642462d4bbe5479e83f91f9211862, v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh:33 "Resetting test-space to base state (full test-code surface)..." (8 words); :71 `` `T) git checkout HEAD -- "$path"` ``; :214 "success = all_required <= passed_tests" (5 words)` |
| teaches | `the task restores its own test-code surface from the container's git HEAD, so the harness upload is not the only reset path` |
| status | `mined` |
| opened | **`2026-10-25`** |
| recheck | `180d` |
| **used-by** | **`corpus/knowledge/benchmark-verifier-execution-model.md`** |

The `used-by` cell currently holds **exactly one** path and no more — `corpus/knowledge/benchmark-verifier-execution-model.md`
(raw cell repr: `'corpus/knowledge/benchmark-verifier-execution-model.md'`). It does **not** name
`benchmark-grader-semantics.md`. The frozen predicate's "S093's `used-by` gains the entry" is therefore still owed,
and the live row already satisfies `status=mined` / `opened=2026-10-25`.

The live row's anchor is **stronger** than the staged one: it pins `:33`, `:71`, `:214` — three locations I
re-resolved at the pin (F3:33, F3:71, F3:214 all match). The staged `S093` row (a.5) is the older, unpinned variant.

---

## (d) Hazards the entry must avoid

**H1 — date mismatch against the frozen predicate (blocking).** Entry `verified-at: 2026-10-23`
(`benchmark-grader-semantics.md:5`), recheck says "(ran 2026-10-23)" (`:6`); both staged rows carry `opened:
2026-10-23` (`SOURCES.append.md:24`, `:27`). The frozen predicate requires `verified-at: 2026-10-25` and
`opened=2026-10-25` on all three rows. Appending the rows verbatim and landing the entry as staged fails
`plans/adoption_check.py` on `rows_mined`/`opened` and on the entry's own provenance line. The honest repair is to
re-open all three sources this round (done here for S093/S094/S097 — see §b) and write `2026-10-25`; writing
`2026-10-25` without re-opening would be a false provenance claim.

**H2 — `S093` is duplicated (blocking).** `SOURCES.append.md` is a 175-row block whose ids collide with the live
registry on **15** ids: `S077, S078, S079, S080, S081, S082, S083, S084, S085, S086, S090, S091, S092, S093, S100`.
The package was computed against a 76-row registry (`MERGE-REPORT.md:9` "lane registry currently holds **76** rows";
`MERGE-REPORT.json` `"existing_rows": 76`), and its "already held" table (`MERGE-REPORT.md:85-91`) lists only
`S140 → S001`. Appending the file wholesale would write a second `S093` row with a stale scope, unpinned anchor and
`opened=2026-10-23`. Only `S094` and `S097` are genuinely new (`S094`/`S097` absent from `corpus/SOURCES.md`).

**H3 — a load-bearing number the executed code contradicts (blocking).** The entry states the tolerance is
`tolerance_pct=0.1` and "any conversion rate outside the 0.1-percentage-point tolerance" fails (`:67-69`). The
signature default is `0.1` (F1:58) — which is what the S094 anchor quotes — but `__main__` calls
`validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` (F1:280, comment F1:279). The entry
therefore reports **twice** the tolerance the run actually applies. This is exactly the Q10 (second-seat re-read of
locations and numbers) and Q3 (claim inside its quote) failure the bar names; the quote is real but supports the
default, not the behaviour. Repair: state `0.05` and quote F1:280, keeping F1:58 as the default.

**H4 — the reset order is wrong and the stage count understated.** Heading `:34` promises "the order the code
performs it", then numbers the bytecode purge **third** (`:43-44`). In F3 the purge is the first statement after the
`cd` (F3:29-30), before the reset list (F3:36+) and before the patch-path pass (F3:77+). The code also performs
**three** reset passes, not two (`:16`): test-code reset (`/tmp/reset_list.txt`), patch-path restore
(`/tmp/v5_paths.txt`), fixture restore (`/tmp/v6_modified.txt`). A reader following the entry's order would misdate
the purge relative to the reset.

**H5 — the logging check fails open, and the entry reads it as an assertion.** `:71-72` says the grader asserts
"no log-bucket writes between launch and evaluation". F1:217-218 returns **True** on any exception with the comment
`# Don't fail evaluation if we can't check logs`. The time window *is* implemented (F1:185-192, contra the stale
`# please add filter …` comment at F1:181) and any surviving entry fails the check (F1:207-212), so the reading is
right in the happy path — but the fail-open branch is a grader-integrity hole of the exact kind axes A/E exist to
record, and the entry claims to serve those axes. Precisely: if `project_id_from_creds and credentials` is falsy the
`if` body is skipped and the function falls off the end returning `None` (falsy → `validate_task_completion` raises,
fail-closed); the **only** fail-open is the `except Exception` branch at F1:217-218. Record that branch, or the entry's
"no log-bucket writes" reads stronger than the code.

**H6 — two borrowed numbers/quotes with no cited row.** "642 / 642 resolved" (`:31`) is anchored to **S078**
(`v2/GATE.md`), quoted in-lane at `corpus/knowledge/benchmark-task-validity-checklist.md:48-49`; the maintainer
sentence at `:57` is verbatim F4:103-104, also **S078**. Neither S078 nor the checklist entry is named. The frozen
predicate forbids a fourth `source:` line (exactly three ids), so the repair is an **inline** attribution
("S078, as quoted in `knowledge/benchmark-task-validity-checklist.md`"), not a new source line.

**H7 — the S097 anchor quote is off by one character.** Staged anchor: "…survey of the **LMs**-as-judges paradigm…"
(`SOURCES.append.md:27`). F5 reads "…survey of the **LLMs**-as-judges paradigm…" (`the LMs-as-judges` occurs **0**
times in F5; `the LLMs-as-judges` occurs 3 times). Under the C1 kill rule a byte-exact quote check refuses this row,
and with S093's round-31 quotes resolving, a refused S097 leaves exactly two survivors — one bad check away from the
"fewer than two survive" stop. Fix the anchor to `LLMs-as-judges` before appending.

**H8 — no negative space (Q4).** The entry never states what its three sources do not establish. It has, unstated:
one task's evaluation script of Toolathlon's 108 graders (S021 teaches 108 execution-verified tasks) and one of
SWE-bench Pro V2's 642 tasks; the fail-open branch was not exercised; no grader was run, only read; the survey's
five-part structure is a table of contents, not evidence that the separation is enforced anywhere. Nor is there a
falsifying observation. `QUALITY.md:36-41` requires both.

**H9 — "extends" is not named (Q6).** `QUALITY.md:50-55` requires the entry to name the existing entry or coverage
row it extends. The `ground:` line (`:92`) names Frontier bullets only. C1's own text says the entry "extends the
round-31 verifier-execution entry"; the staged text never names `benchmark-verifier-execution-model.md`, and it does
not name `benchmark-task-validity-checklist.md`, whose axis I ("ships an evaluation directory rather than a judge
prompt", `corpus/knowledge/benchmark-task-validity-checklist.md:42`) already carries the Toolathlon half of L20 via
**S080**. Without the naming, the Toolathlon section reads as new coverage of a surface the checklist already
touched — the adjacency a critic will attack.

**H10 — the `Gate` pointer dangles.** Both staged rows say "re-verify at the next upstream release (Gate S094
below)" (`SOURCES.append.md:24`, `:27`) and the entry's recheck says "re-run the Gate commands" (`:6`). The package
contains no gate block: `MERGE-REPORT.md` headings are only "What gets appended / Knowledge files to add / Rows whose
source the lane's registry already holds / `used-by` pointers corrected at packaging time / Adopt checklist", and
`MERGE-REPORT.json` contains the string "gate" **0** times and the strings `S093`/`S094`/`S097` **0** times. The gate
evidence lives in the lane's `SOURCES-PROPOSED.md`, which is not in this package. The recheck action must be restated
as the actual command (the three pinned fetches), or the row's recheck cell rewritten.

**H11 — do not append the staged `S093` row.** Beyond H2's id collision, its content is superseded: the live row's
scope adds the parser, its anchor pins `:33/:71/:214`, its `teaches` is the narrower round-31 claim, and its `opened`
is already `2026-10-25`. Adopting the staged variant would silently *downgrade* a landed row.

**H12 — format deltas, minor but checked by the lane's own readers.** (i) No `writer:` line; 6 of 40 lane entries
carry one (round-31 convention), so this is stylistic, not a bar item — but C1's own counter may expect it. (ii) The
S093 source line (`:2`) cites `tests/parser.py` with **no claim attached** anywhere in the body; `parser.py` does
exist at the pin (HTTP 200), so either add the PASSED-set parser claim (which is what the live S093 row's scope
names) or drop the file from the source line. (iii) The S093 location in the source line is elided (`v2/tasks/…/tests/test.sh`),
which is not a resolvable location under Q3; use the full task directory as the live row does.

**H13 — step 5's attribution.** `:46` says "The test patch's own recorded test list is parsed from `config.json`".
The lists are the **task's** `tests/config.json` `fail_to_pass`/`pass_to_pass` (F3:164-166, F3:183-184), read beside
the patch, not "recorded by" it. Small, but this entry's whole value is precision about which artefact carries what.

**H14 — cross-theme overlap to declare.** Two neighbours already hold part of this ground: `llm-judge-calibration.md`
(S009-S012) is the lane's judge-calibration entry, and L21/L22 claim S097 as *the frame* for it — the entry must say
what S097 adds to that entry (a published five-part taxonomy and a meta-evaluation category) and what it does not (no
correction, no protocol). Likewise S080 + checklist axis I vs the Toolathlon section (H9). Undeclared, these read as
duplicate coverage rather than extension, which is a Q6 and a C1-surface risk.

---

## (e) Neutral summary of what the entry teaches

The entry reads two benchmarks' grading code at pinned commits and classifies each grader by mechanism rather than
by reputation. SWE-bench Pro V2's `tests/test.sh` resets the test-code surface to the container's git HEAD, clears
patch-created paths, purges bytecode, applies the test patch, runs the suite, and then scores by set containment:
`all_required = fail_to_pass | pass_to_pass` must be a subset of the tests recorded `PASSED`, with the reward written
as a single bit from the script's exit code — so the grade is binary and conjunctive over the union, and a
previously-passing test broken by the fix costs the whole task. The entry's contribution on that side is a stated
limit: the fixture-revert pass iterates `git diff --name-only HEAD --`, i.e. tracked modifications only, and
fixture/snapshot directories are excluded from the test-code classifier, so an agent-*created* file under
`testdata/`, `fixtures/`, `mocks/` or `__snapshots__/` reaches grading — a precise, falsifiable qualification of the
maintainer's sentence that agent edits to fixtures and snapshots are reverted. On the Toolathlon side it reads one
task's `evaluation/main.py`: a produced `record.csv` is compared scenario-by-scenario against a ground-truth
`expected_ratio.csv` within a numeric tolerance, a storage bucket must exist, and a logging bucket must carry no
entries in the launch-to-evaluation window — a deterministic state comparison with no judge model in the scoring
path. The survey frame then places these two beside LLM-judge scoring: the field's own survey separates
meta-evaluation from methodology and applications, so a grader should be named as a containment test, a state
comparison, or a judge, because only the third kind needs the judge meta-evaluation protocol. Read as a whole the
entry is a taxonomy of grader kinds built from two executed graders plus one survey, with one sharp asymmetry on the
SWE-bench side; it is not a measurement, not a re-run, and not a validity claim about any task.

---

## Unresolved / not attempted (honest gaps)

- The entry's `tests/parser.py` is never read by me beyond an existence probe; the entry makes no claim from it, so
  nothing rests on that gap — but the source line advertises it (H12).
- I did not fetch `v2/GATE.md` to re-verify the "642 / 642" wording; I verified only that the lane already anchors
  that figure to S078 at `benchmark-task-validity-checklist.md:48-49`, which is sufficient to call it a citation gap
  (H6) rather than a fabrication.
- I did not read Toolathlon's `task_config.json` or `groundtruth_workspace/`, so I cannot say whether the ab-testing
  task's 0.05 tolerance is documented anywhere the entry could cite instead of the signature default.
- The other 172 staged rows were not audited; the collision count (15) is the whole of my claim about them.
- No tool was installed or upgraded for this seat; no pacman transaction was run.
