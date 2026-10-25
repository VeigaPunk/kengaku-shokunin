# R33ReconPackage — read-only reconnaissance of the staged grader-semantics package (round 33)

Seat: `R33ReconPackage` (scout, leaf). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Staged package `/home/vgpnk/Projects/shokuknow/merge/kengaku/` opened **read-only**; nothing was
written into that repo, into the fleet repo `/home/vgpnk/Projects/shokunin`, or into any sibling lane.
**Access date for every source opened here: 2026-10-25.** Scratch: `/tmp/r33-r33reconpackage/`
(≈ 240 KB). No tool was installed or upgraded (curl + python3 stdlib only; PACMAN is paused host-wide).

VERDICT: package-read

---

## 0. State note the L1 must read first (the lane moved under this seat)

The lane tip when this seat opened was `f0b20ae` (freeze) / `c227e486`; **the C1 repair landed while
this seat was running**, at commit `2b4cef2` *"round-33: renumbered assimilation (S103/S104),
routed-defect closure N1-N6, catalog re-probe receipts"* (tip now `2b4cef2`, parent `7895588`).
So the "live registry" in §c is reported **both** as it stood at the freeze commits
(`f0b20aea` + `c227e486`, 95 rows, ids ≤ S102) and as it stands now at `2b4cef2` (97 rows).
Everything in §a/§b is the **staged package as it exists on disk**, unchanged since it was staged —
the package was never edited by this lane.

## 0.1 Fetch identity (every quote below resolves to one of these)

| ref | URL | revision | bytes | sha256 |
|---|---|---|---|---|
| **F1** | `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` | commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` | 14 138 B / 297 L | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` |
| **F2** | `https://arxiv.org/abs/2412.05579` | v2 — "[Submitted on 7 Dec 2024 (v1), last revised 10 Dec 2024 (this version, v2)]" | 43 647 B HTML | `851b03db6bf5ae74ac7abe0512a0d12be97c8d7b6f99916e7e09356ae67b043d` |

F1's digest is **byte-identical** to the lane's committed capture
`.ufo/waves/round-33/assimilation/captures/toolathlon-ab-testing-evaluation-main.py`
(14 138 B, sha256 `3bad26b6…`) — independently re-fetched, same bytes.
F2's digest differs from the lane's committed capture `arxiv-2412.05579v2-abs.html`
(43 661 B, sha256 `44195c5f…`) by arXiv's per-request HTML variation; the quoted span is
byte-exact in **both** copies (checked separately, below), so the quote location holds either way.

---

## (a) The staged entry, its three `source:` lines, its load-bearing claims, and the staged rows

### a.1 The staged entry's three `source:` lines — verbatim

`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-grader-semantics.md`
(96 lines, 5 254 B, sha256 `032fe69ae594bc761bfe5f626ecbb526ed032d1bb580f283abaa650d4ef94b8e`),
lines **2-6**:

```
source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `# v2/tasks/…/tests/test.sh` and `# …/tests/parser.py` — commit `66f92766bba642462d4bbe5479e83f91f9211862`
source: S094 — https://github.com/hkust-nlp/Toolathlon — `# tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`
source: S097 — https://arxiv.org/abs/2412.05579 — `# Abstract` — arXiv 2412.05579v2
verified-at: 2026-10-23
recheck: 180d — re-run the Gate commands for S093, S094 and S097 against their pinned revisions (ran 2026-10-23)
```

Three distinct ids (`S093`, `S094`, `S097`). `verified-at:` is **2026-10-23**, two days before the
frozen predicate's `2026-10-25` — the same date mismatch the round-32 seat recorded.

### a.2 Load-bearing claims of the staged entry (line → claim)

SWE-bench Pro V2 half (lines 14-60):

| # | staged lines | claim |
|---|---|---|
| L1 | 16-17 | `tests/test.sh` performs a **"two-stage environment reset"** and then computes the reward from `tests/config.json` |
| L2 | 20-21 | the reward block `all_required = fail_to_pass \| pass_to_pass` / `success = all_required <= passed_tests` |
| L3 | 24 | `passed_tests` is the set of test names whose recorded status is `PASSED` |
| L4 | 25-26 | exit code 0 writes reward 1, non-zero writes reward 0 |
| L5 | 28-29 | the grader is **conjunctive over the union**, so a task that fixes the bug but breaks a previously-passing test scores zero |
| L6 | 30-32 | the grade is binary, no partial credit — "which is what makes the release gate's **"642 / 642 resolved"** figure interpretable" |
| L7 | 34-47 | the reset happens "**in the order the code performs it**", in five numbered steps: (1) tracked test-code `git checkout HEAD --` / untracked `rm -f` with the path classifier; (2) patch-created paths removed, patch-modified paths restored; (3) stale bytecode purged; (4) `git apply`; (5) list parsed from `config.json`, suite run, result reduced to the containment test |
| L8 | 51-55 | the fixture-revert step runs over `git diff --name-only HEAD --` = **tracked modifications only**; an agent-**created** file under `testdata/ test_data/ fixtures/ fixture/ mocks/ mock/ __snapshots__/` is in neither that list nor step 1's test-code removal |
| L9 | 57-60 | the README's claim that **"agent edits to fixtures and snapshots are reverted"** holds for tracked files only — "a precise, falsifiable limit on a maintainer statement" |

Toolathlon half (lines 62-76):

| # | staged lines | claim |
|---|---|---|
| L10 | 64 | `tasks/finalpool/ab-testing/evaluation/main.py` **never calls a model** |
| L11 | 66-69 | it reads a produced `record.csv`, compares it to `groundtruth_workspace/expected_ratio.csv` via `validate_record_data(actual_records, expected_records, tolerance_pct=0.1)`, failing on missing scenarios, extra scenarios, and any conversion rate **outside the 0.1-percentage-point tolerance** |
| L12 | 70 | asserts `check_storage_bucket_exists(...)` |
| L13 | 71-72 | asserts `check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time)` — "no log-bucket writes between launch and evaluation" |
| L14 | 73 | and finally `validate_task_completion(...)` |
| L15 | 75-76 | the grader is a **state comparison with a stated numeric tolerance, plus two side-effect checks**; "there is no judge prompt and no rubric in the scoring path" |

Survey half (lines 78-92):

| # | staged lines | claim |
|---|---|---|
| L16 | 80-83 | S097 organises the space into "Functionality, Methodology, Applications, **Meta-evaluation**, and **Limitations**"; meta-evaluation is "the category the lane's judge-calibration work belongs to", "kept distinct from methodology **on purpose**" |
| L17 | 85-90 | the practical consequence: a benchmark's grader should be described by kind; SWE-bench Pro V2 = deterministic containment test, Toolathlon = state comparison with a tolerance, an LLM judge = a third kind; "Treating the first two as if they were the third is the error the **survey's structure is designed to prevent**" |
| L18 | 92 | `ground:` Frontier §"Agentic benchmark task-spec audits" axes A and E + §"Judge calibration applied inward" |

Structural absences in the staged entry (no line): **no negative space** (no "what this does not
establish"), **no falsifier**, **no naming of the entry it extends** (`benchmark-verifier-execution-model.md`),
**no `writer:` line**.

### a.3 Staged row `S094` — `SOURCES.append.md:24` — all 11 cells verbatim

| column | cell (verbatim) |
|---|---|
| id | `S094` |
| source | `Toolathlon task evaluation script (evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon` |
| kind | `code` |
| tier | `A` |
| scope | `the executed scoring code for one Toolathlon task at a pinned commit: what is compared, against what, and with what tolerance, for the code's own behaviour` |
| anchor | `commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb, tasks/finalpool/ab-testing/evaluation/main.py: "def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)" comparing a produced record.csv against groundtruth_workspace/expected_ratio.csv, plus check_abtesting_logging_bucket_clean() asserting no log bucket writes between launch and evaluation` |
| teaches | `the benchmark scores by comparing a *produced artefact* against a ground-truth artefact with a stated numeric tolerance, and checks the absence of side-effect writes — a state-based deterministic grader with no judge model in the loop` |
| status | `mined` |
| opened | `2026-10-23` |
| recheck | `2026-10-23 — re-verify at the next upstream release (Gate S094 below)` |
| used-by | `corpus/knowledge/benchmark-grader-semantics.md` |

### a.4 Staged row `S097` — `SOURCES.append.md:27` — all 11 cells verbatim

| column | cell (verbatim) |
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

### a.5 Staged row `S093` — `SOURCES.append.md:23` (the entry's third cited id; **malformed**)

| column | cell (verbatim) |
|---|---|
| id | `S093` |
| source | `SWE-bench Pro V2 task verifier files (test.sh, parser.py, config.json) — https://github.com/scaleapi/SWE-bench_Pro-os` |
| kind | `code` |
| tier | `A` |
| scope | `the executed grading code for one SWE-bench Pro V2 task at a pinned commit: what is restored before grading and how the reward is computed, for the code's own behaviour` |
| anchor | `commit 66f92766bba642462d4bbe5479e83f91f9211862, v2/tasks/instance_internetarchive__openlibrary-…/tests/test.sh: "Resetting test-space to base state (full test-code surface)..." then "find . -name '__pycache__' -type d -prune -exec rm -rf {} +" and the reward block "all_required = fail_to_pass \| pass_to_pass" / "success = all_required <= passed_tests"` |
| teaches | `the grader is a binary set-containment over the union of fail_to_pass and pass_to_pass, and the environment is reset to base state first — but the fixture-restore step iterates tracked modifications only, so an agent-added untracked file under a fixture directory survives into grading` |
| status | `mined` |
| opened | `2026-10-23` |
| recheck | `2026-10-23 — re-verify at the next upstream release (Gate S093 below)` |
| used-by | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md` |

**This row parses to 12 cells, not 11** — the escaped-pipe handling inside the quoted reward block
splits it. Same defect in staged `S101` (`SOURCES.append.md:31`, **15 cells** — the `git apply --3way`
/ `patch --fuzz=3` docstring lines carry raw pipes). A naive `split('|')` append of the package would
write two malformed rows into the registry.

---

## (b) Quote support: what the staged rows carry, and what carries nothing

Legend — **[Q]** an anchored quote exists in a staged row's `anchor` cell · **[P]** paraphrase only
(staged row states the conclusion in `scope`/`teaches`/`anchor` prose) · **[—]** no staged-row support
at all · **pin check** = what I verified at F1/F2 or in the lane's committed capture
`swebench-pro-tests-test.sh` (sha256 `b6f26eec…`).

| # | staged-row support | pin check |
|---|---|---|
| L1 "two-stage environment reset" | **[P]** S093 scope "what is restored before grading" | **contradicted**: F3 shows **three** reset passes (`/tmp/reset_list.txt` :34-74, `/tmp/v5_paths.txt` :77-94, `/tmp/v6_modified.txt` :97-105), and the bytecode purge at **:29-30 runs before** all of them — so "two-stage" and the staged step order are both wrong |
| L2 reward block | **[Q]** S093 anchor quotes both lines | exact: `test.sh:213` `all_required = fail_to_pass \| pass_to_pass`; `:214` `success = all_required <= passed_tests` |
| L3 `PASSED` name set | **[—]** | true at `test.sh:207-210`; needs its own quote |
| L4 exit code → reward 1/0 | **[—]** | true at `test.sh:12-22` (`cleanup_and_reward`, `trap … EXIT`) |
| L5 conjunctive over the union | **[Q]** (derivable from L2's quote) + **[P]** S093 teaches "binary set-containment over the union" | exact |
| L6 binary grade | **[P]** S093 teaches "binary set-containment" | true |
| L6 "642 / 642 resolved" | **[—]** in all three staged rows | the figure is **S078's** (`v2/GATE.md`); the staged entry borrows it without citing S078 — unanchored number / cross-theme bleed |
| L7 five ordered steps | **[Q]** only step 3's command (S093 anchor quotes the `__pycache__` find); steps 1, 2, 4, 5 **[—]** | step 1 classifier `test.sh:37-55`; step 2 `:77-94`; step 4 `:108`; step 5 `:164-166`, `:183-204`; and the **order is wrong** (purge at :29-30 precedes the reset at :33) |
| L8 asymmetry (tracked-only fixture revert) | **[P]** S093 `teaches` states the conclusion exactly; **no quote** | true: `test.sh:97` `git diff --name-only HEAD -- > /tmp/v6_modified.txt`; `:100-102` the `*fixtures/*` case; `:38` `DATA_DIRS`; `:43-44` data-dir paths return `False` from `is_test_code` |
| L9 README quote "agent edits to fixtures and snapshots are reverted" | **[—]** in all three staged rows | the sentence is **S078's** README (`v2/README.md`), not any cited row — unanchored quote / cross-theme bleed |
| L10 "never calls a model" | **[P]** S094 teaches "no judge model in the loop" | true for F1: case-insensitive scan for `prompt\|judge\|model\|openai\|chat\|gpt\|llm\|claude\|anthropic` → **0 hits**; imports are stdlib + `google.cloud.storage/logging` + `oauth2.service_account` + `api_core.exceptions` + `utils.evaluation.retry` |
| L11 tolerance **0.1** | **[Q]** S094 anchor quotes the *signature default* | **contradicted for the executed path**: F1:279 `# Validate with 0.05% tolerance`; F1:280 `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)`. The staged anchor's quoted **call form** `validate_record_data(actual_records, expected_records, tolerance_pct=0.1)` **does not occur in the file** (checked byte-wise: absent). `:58` is the signature default only |
| L11 record.csv vs expected_ratio.csv | **[Q]** S094 anchor names both artefacts | true: F1:55 `expected_file = os.path.join(groundtruth_workspace, "expected_ratio.csv")`; F1:268/274 the agent's `record.csv` and the groundtruth workspace |
| L11 missing/extra scenarios | **[P]** (implied by "what is compared") | true: F1:66-72 `missing_scenarios` / `extra_scenarios` → `validation_errors`; `:98-100` `raise ValueError(f"Record validation failed:\n{error_msg}")` |
| L12 `check_storage_bucket_exists` | **[—]** (S094 anchor names only `validate_record_data` and `check_abtesting_logging_bucket_clean`) | true but unquoted: F1:125 `def check_storage_bucket_exists(bucket_prefix: str, project_id: str = "mcp-bench0606") -> bool`; `:225` the call. It returns a bool — the caller raises; the entry's "asserts" is loose |
| L13 logging-bucket check | **[Q]** S094 anchor names the function and its reading | **the "asserting" framing is wrong on three paths**: F1:213-214 clean → `True`; **:216-218** caught exception → `return True  # Don't fail evaluation if we can't check logs` (**fail open**); **:176 → :214** with absent credentials the `if project_id_from_creds and credentials:` body is skipped, the try block ends, the function returns **implicit `None`** (falsy) → F1:234-235 `if not check_abtesting_logging_bucket_clean(...)` → `raise ValueError(...)` (**fail closed**). A fourth path: `:171-172` reads `../groundtruth_workspace/log_bucket_name.txt` **before** the `try` → an unhandled `FileNotFoundError` aborts the run |
| L14 `validate_task_completion` | **[—]** | true: F1:220-237; it raises on either sub-check. Note it runs **before** the record comparison in `__main__` (F1:262 `grade_with_retry(_check_completion)` then `:269+` the record check) — the staged list order (L13 then L14 then record) inverts the real order |
| L15 no judge prompt / no rubric | **[P]** S094 teaches "no judge model in the loop" | true (same scan as L10); grading is `ValueError` + `exit(1)` |
| L16 five perspectives | **[Q]** S097 anchor quotes the abstract sentence | **the staged quote is not byte-exact**: it reads `the LMs-as-judges paradigm` (**one** L). In F2 the string `LLMs-as-judges` occurs 9× and a standalone `LMs-as-judges` occurs **0×**; the full staged sentence is absent from both F2 and the lane's capture. The corrected two-L sentence **is** byte-exact in both copies (20 whitespace-words) |
| L16 "on purpose" / "the category the lane's judge-calibration work belongs to" | **[P]** S097 teaches "separates … from methodology and applications" | inference, not in the abstract |
| L17 grader-kind taxonomy, "the error the survey's structure is designed to prevent" | **[—]** | **nothing in the staged rows or the source**: the abstract never mentions deterministic graders or benchmark graders; it lists five perspectives of LLMs-as-judges. The attribution is the entry's own construction presented as the survey's design |
| L18 `ground:` | n/a | names Frontier sections only; names neither the entry it re-derives nor `benchmark-task-validity-checklist.md` |

**Net:** of the 18 load-bearing claims, **6 rest on an anchored quote** in a staged row
(L2, L5, L10/L11/L13's artefact names, L16) — and **two of those six are defective**: L11's quote is the
unused *default*, L16's quote is **off by one character** (one `L`). **7 are paraphrase-only**
(L1, L6, L8, L12→not quoted, L15, L16-inference, L18). **7 carry no staged-row support**
(L3, L4, L7's steps 1/2/4/5, L9, L14, L17, and L1's "two-stage"). **Three claims are contradicted by the
pinned bytes** (L1's stage count and step order, L11's 0.1 tolerance, L13's "asserts") and one quote is
**not byte-exact at the pin** (L16's `LMs-as-judges`).

---

## (c) The live registry: refusal rows S094/S097/S101/S102, and S093

### c.1 The four round-32 refusal rows (they stand unchanged; quoted `teaches` cells)

`corpus/SOURCES.md` lines 114-117 — identical at the freeze commits (`f0b20aea`, `c227e486`) and at
`2b4cef2`. All four `teaches` cells read, verbatim:

```
REJECTED: duplicate id; flip: a future candidate must use a new id and pass the source gate
```

Their `source` cells (the refusal reasons), verbatim:

- **S094** (line 114): `supersedes S094 — duplicate staged row refused after registry collision; staged wording misstated the executed tolerance and log-check behavior; use the corrected pinned task source description at the existing S094 row.`
- **S097** (line 115): `supersedes S097 — duplicate staged row refused after registry collision; staged anchor omitted one L in “LLMs-as-judges”; use the existing byte-verified S097 row.`
- **S101** (line 116): `supersedes S101 — duplicate staged row refused after registry collision; this id already identifies the SWE-bench locked replay agent. Use the existing S101 row; no catalog row admitted.`
- **S102** (line 117): `supersedes S102 — duplicate staged row refused after registry collision; this id already identifies the SWE-bench release map. Use the existing S102 row; no catalog row admitted.`

All four carry `kind=docs`, `tier=B`, `status=rejected`, `opened=2026-10-25`, `recheck=180d`,
`used-by=—`. (The `S101`/`S102` texts say "this id already identifies …"; note that in the live
registry the *only* rows carrying those ids are these four rejection rows themselves — the ids
S101/S102 in the staged package are different documents (SWE-bench `patch_replay.py`, Toolathlon
`EVAL_SERVICE_README.md`/`eval_server.py`/`evaluator.py`). The refusal rows are accurate about the
refusal but their "already identifies" clause is a package-id statement, not a live-registry row.)

### c.2 S093 — live cells at the freeze and now

| cell | at freeze `f0b20aea` / `c227e486` | at `2b4cef2` (now) |
|---|---|---|
| id | `S093` | `S093` |
| source | `SWE-bench Pro V2 task verifier files (tests/test.sh, parser.py, config.json) — https://github.com/scaleapi/SWE-bench_Pro-os` | unchanged |
| kind / tier | `code` / `A` | unchanged |
| scope | `the executed grading code for one SWE-bench Pro V2 task at a pinned commit — the test-space reset it performs itself, the paths that reset skips, and the log-scan parser behind its PASSED set` | unchanged |
| anchor | `commit 66f92766bba642462d4bbe5479e83f91f9211862, v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh:33 "Resetting test-space to base state (full test-code surface)..." (8 words); :71 \`T) git checkout HEAD -- "$path"\`; :214 "success = all_required <= passed_tests" (5 words)` | unchanged |
| teaches | `the task restores its own test-code surface from the container's git HEAD, so the harness upload is not the only reset path` | unchanged |
| **status** | `mined` | `mined` |
| **opened** | `2026-10-25` | `2026-10-25` |
| recheck | `180d` | `180d` |
| **used-by** | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md` | unchanged |

**Finding for the L1:** S093's `used-by` **already named `benchmark-grader-semantics.md` at the freeze
commits** — it was added by round 32's commit `bcd2a6c`, which committed the (then-refused) draft
*and* its pointer. So C1's "S093's `used-by` gains the entry" clause was **already satisfied at
freeze** and needed no new registry edit; the r32 recon report's observation that the cell held only
`benchmark-verifier-execution-model.md` described the pre-`bcd2a6c` baseline. `git diff f0b20ae..2b4cef2
-- corpus/SOURCES.md` touches **only** the two added rows S103/S104 — S093's row is byte-identical.

### c.3 The registry as it now stands (`2b4cef2`)

97 S-rows, ids ≤ S104, no duplicate ids, no malformed rows, 15 W04 (same count and same rows as the
frozen `census-before.txt`), 0 E03/E04 — I re-implemented the census' url/scope rules over the
committed file to check this. The two rows added by `2b4cef2` (verbatim):

- **S103** (line 118) — `source`: `Toolathlon task evaluation script (evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon` · `kind` `code` · `tier` `A` · `scope`: `the executed scoring code for one Toolathlon task at a pinned commit: what is compared, against what, and with the tolerance actually invoked` · `anchor`: `commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb, tasks/finalpool/ab-testing/evaluation/main.py: "def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:" (:58, signature default) invoked as "validate_record_data(actual_records, expected_records, tolerance_pct=0.05)" (:280) — the executed tolerance is 0.05; plus check_abtesting_logging_bucket_clean() whose caught exceptions return True (fail open) while absent credentials fall through to implicit None (fail closed)` · `teaches`: `the benchmark scores by comparing a produced artefact against a ground-truth artefact with a stated numeric tolerance, and its log-bucket check mixes fail-open exceptions with fail-closed credential absence` · `status` `mined` · `opened` `2026-10-25` · `recheck` `180d` · `used-by` `corpus/knowledge/benchmark-grader-semantics.md`
- **S104** (line 119) — `source`: `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579` · `kind` `paper` · `tier` `B` · `scope`: `the survey's own five-part structure for LLM-as-a-judge evaluation — Functionality, Methodology, Applications, Meta-evaluation, Limitations — for the preprint's own text; tier B because it is a preprint` · `anchor`: `arXiv 2412.05579v2 (submitted 7 Dec 2024, last revised 10 Dec 2024), Abstract: "This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." (20 words); Comments: "60 pages, comprehensive and continuously updated"` · `teaches`: `the field's own survey separates meta-evaluation — how a judge itself is scored — from methodology, so judge-based scoring owns a distinct validation protocol` · `status` `mined` · `opened` `2026-10-25` · `recheck` `180d` · `used-by` `corpus/knowledge/benchmark-grader-semantics.md`

The live entry (`corpus/knowledge/benchmark-grader-semantics.md` at `2b4cef2`) now carries exactly three
`source:` lines — `S093`, `S103`, `S104` — with `verified-at: 2026-10-25`, and exactly one index row in
`corpus/README.md` (line 67).

---

## (d) Hazards

**H1 — the staged tolerance number is wrong and the staged quote supports it (round-32 falsify seat
`FxTolerance`, confirmed).** Staged entry lines 67 and 69 state the operative tolerance as
`tolerance_pct=0.1` / "0.1-percentage-point tolerance", and the staged S094 anchor quotes the
*signature default* (`tolerance_pct: float = 0.1)`). The executed call is
`validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` at F1:280, with
`# Validate with 0.05% tolerance` at F1:279; the staged call form with `0.1` **does not occur in the
file**. The staged row reports **twice** the tolerance the run applies. **Status: repaired** — the live
S103 anchor and the live entry now quote both `:58` (default) and `:280` (executed) and state 0.05.

**H2 — the staged log-check reading is wrong in both directions (round-32 falsify seat `FxFailOpen`,
confirmed by execution against the pinned bytes).** The staged S094 anchor and staged entry line 71-72
say the grader **asserts** "no log bucket writes between launch and evaluation". F1 shows three
outcomes: clean → `True` (:213-214); caught exception → `True` (:216-218, **fail open**, comment
`# Don't fail evaluation if we can't check logs`); absent credentials → the `:176` branch is skipped,
the function returns **implicit `None`**, `not None` → `raise ValueError` at :234-235 (**fail
closed**). A fourth path (:171-172, groundtruth file read before the `try`) aborts the run outright.
The staged row's "asserting" wording supports none of these. **Status: repaired** — the live S103
anchor states the fail-open/fail-closed mix explicitly and the live entry separates them in §S103 and
in "What this does not establish".

**H3 — the staged S097 quote is off by one character (round-32 refusal row S097).** Staged anchor
reads `the LMs-as-judges paradigm` (one `L`). In F2 `LLMs-as-judges` occurs 9×, a standalone
`LMs-as-judges` occurs 0×; the staged sentence is absent from F2 and from the lane's own capture. The
corrected two-L sentence is byte-exact in both copies. **Status: repaired** — live S104's anchor
carries `LLMs-as-judges` and the live entry quotes it at 20 words.

**H4 — two borrowed numbers/quotes with no cited row (cross-theme bleed; still live in the *staged*
text, removed from the landed entry).** Staged line 31-32 borrows the release gate's
`"642 / 642 resolved"` figure, which belongs to **S078** (`v2/GATE.md`); staged line 57 quotes the
maintainer sentence "agent edits to fixtures and snapshots are reverted", which also belongs to
**S078** (`v2/README.md`). Neither S078 nor the checklist entry is among the three cited ids, and the
frozen predicate forbids a fourth `source:` line — so the repair must be an inline attribution, not a
new citation. **Status: removed** — the landed entry's S093 half is a labelled restatement
("restated, not repeated") and no longer carries the 642 figure or the README sentence.

**H5 — the staged reset ordering and stage count are wrong (stale claim; the r32 seat already
recorded it).** Staged line 16 says "two-stage environment reset" and staged lines 34-47 promise "the
order the code performs it" while numbering the bytecode purge **third**; in `test.sh` the purge is
`:29-30`, *before* the reset banner at `:33`, and there are three reset passes. **Status: removed** —
the landed entry drops the derivation entirely.

**H6 — the staged survey attribution over-claims (r32 seats `FxS097Frame` sub-claim 3 and
`FxEntryTruth` §1.4/§2.1-2, confirmed).** Staged lines 85-90 present the deterministic-vs-LLM-judge
dichotomy as "the error the survey's structure is designed to prevent"; the survey's abstract names
five perspectives of LLMs-as-judges and never mentions deterministic graders. The staged entry also
lacks the negative-space and falsifier sections the landed entry now has, and does not name the
round-31 entry it re-derives. **Status: repaired** — the landed entry says "That classification is
this entry's own framing; the abstract itself only separates the parts", and adds
"What this does not establish" + "Falsifier".

**H7 — staged provenance dates are two days stale.** Staged `verified-at: 2026-10-23`, recheck
"(ran 2026-10-23)", and `opened: 2026-10-23` on all three staged rows; the frozen predicate requires
`verified-at: 2026-10-25` and `opened=2026-10-25`. **Status: repaired** — the landed entry and the
live S103/S104 rows all read `2026-10-25`.

**H8 — two staged rows are structurally malformed and must never be appended as-is.** Staged `S093`
(12 cells) and staged `S101` (15 cells) contain raw `|` inside quoted code, so a `split('|')` append
writes broken rows. (Both ids are refused/absent-by-design anyway; the hazard is for any future
assimilation of this package.) **Status: not applicable to the landed rows** — S103/S104 are 11 cells
each and the registry has 0 malformed rows.

**H9 — the staged package's `Gate` pointers dangle.** Staged recheck cells say "(Gate S094 below)",
"(Gate S097 below)", "(Gate S093 below)" and the staged entry's recheck says "re-run the Gate
commands" — but the package contains **no** `## Gate` block: `MERGE-REPORT.md` headings are only
"What gets appended / Knowledge files to add / Rows whose source the lane's registry already holds /
`used-by` pointers corrected at packaging time / Adopt checklist", and `MERGE-REPORT.json` contains
the strings `gate`, `Gate`, `S093`, `S094`, `S097` **0 times** each. **Status: repaired** — the live
rows' recheck cell reads `180d` and the live entry names the actual action.

**H10 — RESIDUAL DEFECT the L1 still owns: the landed entry's word-count labels are wrong.** In the
landed entry (`corpus/knowledge/benchmark-grader-semantics.md`, lines 41-42):

```
> `# Validate with 0.05% tolerance` — 4 words, `main.py:279`
> `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` — 5 words, `main.py:280`
```

Actual whitespace-word counts: `# Validate with 0.05% tolerance` = **5** words (not 4);
`validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` = **3** words (not 5).
The lane's own committed gate receipt
`.ufo/waves/round-33/assimilation/gate-receipts.txt` records the same two spans as
`ok S103 words=11` and `ok S103 words=3` — i.e. **the receipt and the entry disagree**. The r32 seat
`FxEntryTruth` §2 item 5 had already flagged these two spans as mislabelled (it recorded the `:279`
comment as "4 words" against an actual 5, and the `:280` call as "4 words" against an actual 3); the
round-33 landing re-worded the second label to "5 words" but did not correct either count. The
signature quote (11 words) and the arXiv quote (20 words) are correct. Fixing the two numbers needs
no new source and no new row; it is a one-line-per-quote correction inside the entry.

**H11 — RESIDUAL: the live S103 anchor compresses two distinct error paths into one clause.** The
anchor says "check_abtesting_logging_bucket_clean() whose caught exceptions return True (fail open)
while absent credentials fall through to implicit None (fail closed)". That is accurate, but it does
not mention the **third** reachable path — F1:171-172 reads
`../groundtruth_workspace/log_bucket_name.txt` **before** the `try`, so a missing ground-truth file
raises an unhandled `FileNotFoundError` that aborts the whole evaluation (not a grader pass and not
a grader fail, but a run abort). The landed entry's §S103 likewise names only the clean path, the
exception path and the credential path. Not a false statement; a completeness gap on the exact axis
(Q3/Q4) the entry claims to serve.

**H12 — RESIDUAL: the landed S102 refusal text names a document the live registry does not hold.**
The live S102 row's `source` cell says "this id already identifies the SWE-bench release map", but the
live registry's release-gate row is **S078** ("SWE-bench Pro V2 release notes and release gate"), and
the staged package's S102 is the *Toolathlon* evaluation service
(`EVAL_SERVICE_README.md`, `eval_server.py`, `utils/evaluation/evaluator.py`). The refusal itself is
correct (the row is a rejection record and the staged catalog row is not appended), but the
"already identifies" clause names the wrong subject. The r33 frozen claim says the four refusal rows
"stand unchanged", so **do not edit it** — record it as a known stale clause instead.

**H13 — adjacency worth one line in the lesson: the staged package's S094/S097 rows were *correct in
their `used-by`* (`corpus/knowledge/benchmark-grader-semantics.md`) and wrong in their numbers; the
round-32 refusal therefore did not need to reject the *theme*, only the ids and the two misstatements.
The landed S103/S104 keep that same `used-by`, so the entry is now cited by three mined rows and the
round-32 draft's debt is discharged.**

---

## Evidence discipline

- Bytes fetched this seat: F1 and F2 above, both re-verified against the lane's committed captures
  by digest and by byte-containment of every quoted span.
- Nothing was written outside `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-33/build/R33ReconPackage.md`
  and the scratch dir `/tmp/r33-r33reconpackage/`.
- No tool was installed or upgraded; no pacman transaction was run (host-wide pause).
- Checks **not** run by this seat (main agent's job): `plans/round33_defects.py`,
  `plans/catalog_probe.py --verify`, `plans/adoption_check.py`, `plans/round33_c1_verify.py`,
  `scripts/sources-census.sh`. The census figures in §c.3 come from my own re-implementation of that
  script's url/scope rules over the committed `corpus/SOURCES.md`, not from the script itself.
