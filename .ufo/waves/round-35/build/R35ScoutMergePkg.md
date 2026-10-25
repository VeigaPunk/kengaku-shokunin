# R35ScoutMergePkg — merge/kengaku package screen (round 35, wave 1)

Seat: scout (read-only). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Screened source (read-only, never written): `/home/vgpnk/Projects/shokuknow/merge/kengaku/`
(`MERGE-REPORT.md`, `MERGE-REPORT.json`, `SOURCES.append.md`, `knowledge/corpus/knowledge/*.md`),
plus the upstream lane's own artefacts under `/home/vgpnk/Projects/shokuknow/lanes/kengaku/`.

**Theme screened (one, matching C1):** *benchmark grader / verifier semantics measured by
reading and executing pinned upstream grader code* — i.e. the staged entries that read a
benchmark's grading code at a pinned commit and, where claimed, execute it offline.
21 of the package's 65 knowledge entries fall in this theme; the other 44 (CJK governance,
contamination cards, BenchmarkCards, OSF preregistration, GENIAC/post5G programme pages) are
**held** — out of C1's theme and out of PROVINCE's "benchmark grader audits" clause, and none
of them is cited by anything round 35 admits.

Axis notes (Godspeed): the cheap axis was *id/entry collision* (measurable offline, no
network); the expensive axis was *number re-derivation* (re-fetch the pinned tree, re-run the
upstream probe). I ran the cheap axis first and it alone already decided most entries; the
expensive axis was spent only on the one entry that survived it.

---

## 1. Structural facts about the package (cheap axis, offline)

| Fact | Command | Output |
|---|---|---|
| Package knowledge entries | `ls merge/kengaku/knowledge/corpus/knowledge/*.md \| wc -l` | `65` |
| Package staged rows | `grep -cE '^\| *S[0-9]{3,} *\|' merge/kengaku/SOURCES.append.md` | `175` |
| Live lane registry rows | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` | `100` (ids S001–S107) |
| **Id collisions staged vs live** | python set-intersection of the two id sets | **24** (`S077–S086, S090–S094, S097, S100–S107`) |
| Staged rows that would overwrite a live row | same | S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S090,S091,S092,S093,S094,S097,S100,S101,S102,S103,S104,S105,S106,S107 |
| Package rows the lane's own gate calls malformed | `python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package merge/kengaku/SOURCES.append.md` | `registry=100 staged=173 collisions=22 malformed=2 duplicates=0 defects=167 prose=167`; malformed `S093:escaped-pipe`, `S101:escaped-pipe`; exit 3 |
| Knowledge files whose **filename** collides with a live lane entry | `for f in pkg/knowledge/*.md; do [ -e corpus/knowledge/$(basename $f) ] && echo COLLIDE; done` | `benchmark-grader-semantics.md`, `benchmark-task-validity-checklist.md`, `benchmark-verifier-execution-model.md`, `contamination-transparency-card.md` |
| Package rows pointing **outside** the lane | `grep -c shokuknow corpus/SOURCES.md` (live) vs staged S114/S130/S144 locators `lanes/kengaku/roundN/...` | live: **0** rows reference the source repo; staged own-work rows use a path relative to the *source* repo root, unresolvable from this lane |

**The package's own numbers are stale.** `MERGE-REPORT.md:14` and `MERGE-REPORT.json` say
`lane registry currently holds **76** rows; `first_id S077`. The live registry holds **100**
rows ending at S107 — and S105/S106/S107 are *round 35's own* C1 rows (the TB2
`protein-assembly` grader trio). The package's S105/S106/S107 are **different documents**
(GENIAC phase-1 results, 中文信息学报 survey, Toolathlon `deploy_containers.sh`). Appending
the package's S105–S107 to the live registry **breaks the frozen C1 predicate** — measured in
a scratch clone of the lane at `6ac9611`:

```
$ python3 plans/round35_c1_verify.py --lane .      # after appending staged S105,S106,S107
V1 ok / V2 DEFECT S105 present 2 times / V3 ok / V4 ok / V5 ok / V6 DEFECT census exit 1
checks=6 defects=2
PREDICATE C1 fail
```

So the package must not be appended wholesale. This is the single most actionable finding
for the L1.

## 2. C1-collision constraint on landing any package content (measured)

C1's counter `plans/round35_c1_verify.py` V4 requires **committed knowledge files == index
rows == 42** (docstring V4; `plans/round35_c1_verify.py:154`). Consequences, all measured in
the scratch clone:

* Copying the package's 65 knowledge files in and committing → `V4 DEFECT knowledge files=103
  index rows=43 (want 42/42)` → `PREDICATE C1 fail`. (The 65 file copy alone, uncommitted, is
  invisible to V4 because V4 counts `git ls-files`.)
* Adding **one** new knowledge file **plus** its README index row → `V4 DEFECT knowledge
  files=103 index rows=43` → `PREDICATE C1 fail`.
* **Amending an existing entry in place** (no new file, no new index row) → `checks=6 defects=0`,
  `PREDICATE C1 pass`.

**Therefore the only C1-safe landing shape for package content is a dated amendment inside an
already-indexed knowledge file** (which is also what the package's own adopt checklist §5/§6
prescribes). A new knowledge file cannot land in round 35 without re-baselining C1's V4,
which the frozen predicate forbids.

Second constraint, also measured: a new registry row must go **inside** the `## Registry`
section (`corpus/SOURCES.md:19`–`:123`); appended after `## Paths` the census returns
`E12 <id> row outside Registry section` ×144 and exits 1. And a staged row's prose `recheck`
cell fails the census (`E09 recheck=2026-10-23 — …`) unless normalised to a cadence.

## 3. Admit-candidate / refuse verdicts (theme: grader & verifier semantics)

### ADMIT-CANDIDATE A1 — `grader-predicate-input-types.md` (staged rows S143 + S144)

The round-7 fixture probe: it re-calls 16 pinned Toolathlon comparison functions with
fixtures of their *real* input types and reports `discriminates: 16 of 16`.

* **Reproduced.** I re-ran the upstream probe script read-only against the pinned commit
  `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`:

  ```
  $ python3 /home/vgpnk/Projects/shokuknow/lanes/kengaku/round7/toolathlon-grader-fixture-probe.py \
        --fetch --src-dir /tmp/k35-scout-mgr/src
  ...
  ## Counts
  - discriminates: 16 of 16
  ```
  and diffed the fresh result table against the staged `round7/toolathlon-grader-fixture-probe.md`
  table: **16 rows both sides, 0 textual differences** (identical task/function/verdict/detail
  for all 16).
* **Why it is new ground for C1.** C1 executed one TB2 task grader; this executes a *second*
  benchmark's grader comparison functions with the same instrument shape (offline, pinned,
  one-unit perturbation, no task run, no workspace). It also directly answers the round-33
  frontier clause "for Toolathlon" beyond the single `ab-testing` task.
* **Flip condition (all four needed).**
  1. **Own-work locator must be re-homed.** S144's locator is `lanes/kengaku/round7/toolathlon-grader-fixture-probe.md`,
     a path relative to the *source* repo; the live lane has 0 rows pointing outside itself
     (`grep -c shokuknow corpus/SOURCES.md` → `0`). Copy the artefact + a fresh lane-side
     receipt into the lane (e.g. `corpus/evidence/round35/…`) and re-point the row.
  2. **S143 is a live-collision risk only if reused as-is** — it is *not* in the live registry
     (live ids end S107 with S105–S107 = C1's rows), so S143/S144 are free ids; they must
     still be renumbered by the L1's adoption plan rather than assumed.
  3. **The entry must be a dated amendment**, not a new file (§2 above).
  4. `recheck` for the own-work rows must be a cadence/ISO date, and `opened` must be
     `2026-10-25` — the staged rows carry `opened: 2026-10-23`, which the lane's own gate
     refuses (`missing: S114:not-opened-this-round`) unless the caller re-opens and attests.
     Verified gate path: `--scope-to-admit --attest-opened --recheck 180d` emits a 4-row block;
     inserted inside `## Registry` the census returns **exit 0** and C1 stays
     `checks=6 defects=0 / PREDICATE C1 pass`.

### ADMIT-CANDIDATE A2 — the dated probe-amendment lineage (13 staged entries, one cluster)

`grader-fixture-coverage.md` (S155), `grader-fixture-probe-stage3.md` (S170,S171),
`spreadsheet-grader-fixtures.md` (S180,S181,S182), `grader-candidate-coverage.md` (S189),
`grader-candidate-reconstruction.md` (S197), `grader-candidate-coverage-r13.md`
(S212–S216), `-r14.md` (S232–S235), `-r15.md` (S240), `grader-sheet-checks-real-pandas-r16.md`
(S245–S248). These are the round-8…round-16 amendments to A1: the coverage recount
(26 of 26 measured; 15 named unmeasured; then 7 of 7, then 11 of 11), the pandas-host
blocker, and the final r16 finding that the three `nvidia-market` sheet checks cannot be
exercised even with a real pandas because the import chain reaches the `openai-agents` SDK.

* **Why admit as one cluster, not 13 entries.** They are one claim told thirteen times
  (the candidate-set coverage figure and its successive corrections); the package's own adopt
  checklist §5/§6 folds dated amendments into the held file.
* **Partial re-derivation.** Of the seven upstream probe scripts in the source repo
  (`round7/8/9/10/13/14/16`), I re-ran round 7 (16/16, exact). Rounds 11, 12 and 15 have **no
  script** — they are recounts/reconstructions over cached trees and reasoning, so their
  numbers are not independently re-runnable as staged.
* **Flip condition.**
  1. Land as dated amendment sections of the **same** entry as A1 (no new file).
  2. Every own-work locator must be re-homed into the lane with a lane-side receipt, as in A1.1.
  3. The scriptless rounds (11/12/15) must either be re-derived with a shipped script or be
     labelled as lane-own-work recounts whose recheck is `on-commit`.
  4. Rows must be renumbered around the live S001–S107 block and the census `E09`/`E12`
     constraints honoured (§2).

### REFUSE R1 — `toolathlon-grader-contract-2026-10-23.md` (S114) — *the package's flagship*

It is the one entry whose numbers are load-bearing for a whole-corpus claim ("there is no
single grader contract"; "the independent reference is usually optional"; "the tolerance is
mostly implicit"). **Its numbers do not reproduce from the pinned tree.**

| Staged claim | Re-derivation at `9be8d8fe` | Verdict |
|---|---|---|
| "109 task directories under `tasks/finalpool` were listed"; "108 of 109 directories contain a grader; the 109th (`task_conflict.json`) is a task-configuration file" | GitHub trees API at the pinned commit: `tasks/finalpool` has **109 direct children = 108 trees + 1 blob** (`task_conflict.json` is a *file*, not a 109th directory) | denominator mis-described |
| "graders declaring `--groundtruth_workspace`: **100** of 108"; per-task table: 14 True / 86 False / **8 absent** | AST parse of all 108 graders: **107** declare the option (only `price-comparison` does not); 14 `required=True` ✔; **89** explicit `required=False`; 4 with no `required=` kwarg | **does not reproduce** — the "absent 8" bucket wrongly includes 3 graders that declare `required=False` explicitly (`huggingface-upload`, `travel-expense-reimbursement`, `woocommerce-new-welcome`) and 4 that declare it without `required=` |
| per-task "grader bytes" column | GitHub blob `size` vs staged: **57 of 108 rows differ**, every one *smaller* (deltas 2–2836 B); 51 match exactly | **does not reproduce** |
| "Only five graders declare a numeric tolerance default at all: 0.01 (three graders), 0.1 (one), 1e-6 (one)" | AST argparse defaults found: `--numerical_tolerance=1e-06`, `--reading_tolerance=0.01`, `--time_tolerance=60` → **three argparse defaults in two graders**; 0.01 appears as a *function* default in 2 graders (`llm-training-dataset`, `machine-operating`) — the staged prose's "0.01 in three graders" is unsupported, and the staged artefact's own per-task table lists only 3 graders with a tolerance default (it contradicts its own prose) | **does not reproduce** |
| "graders referencing a tolerance parameter: 16" | `grep -l tolerance` over the 108 fetched files → **16** | reproduces ✔ |
| recheck: "re-derive the denominator from the pinned tree and **re-run the tabulation script**" | `find lanes/kengaku -name '*.py'` → 7 probe scripts, **no tabulation script exists** | the row's own recheck instruction is **not executable** |

The 108-grader denominator and the `required=True = 14` do reproduce (both exactly), and the
64 "delegates to a task-local checker" count is internally consistent with its own per-task
table (64 yes / 44 no over 108). But three of its five headline counts and its byte column do
not, and its recheck names a script that does not exist.

* **Flip condition.** Re-derive the whole table with a **shipped** tabulation script
  (`plans/…` in the lane, not only in the source repo), land that script + its output in the
  lane, correct the `--groundtruth_workspace` classification (107 declaring, 89 explicit
  `required=False`, 4 unspecified, 1 without the option) and the tolerance-default claims,
  drop or fix the byte column, and then re-present as a dated amendment (not a new file).
  Until then its two headline findings ("there is no single grader contract", "the reference
  is usually optional") are **plausible but unverified**, and the third ("the tolerance is
  mostly implicit") is contradicted by its own table.

### REFUSE R2 — `toolathlon-grader-behaviour-probe-2026-10-23.md` (S130)

The round-6 generic-shape probe. Its summary table denominates everything by **38 candidates**
("isolated and callable 13 | 38", "… not callable with any of the seven shapes 23 | 38",
"exec failed 1 | 38"), but its own per-candidate record has **37 rows**
(23 `no-callable-shape` + 13 `ok` + 1 `exec-failed` = 37), and 13 + 23 + 1 = 37 ≠ 38.
The four discriminating functions and the nine "uninformative" ones are internally consistent
with the 13 `ok` rows, so the defect is the denominator, not the per-function table.

* **Flip condition.** Either state 37 (with the 38th candidate named or the claim dropped), or
  land as an amendment *folded into* A1 — which is required anyway, since A1's own text says
  the round-6 negative results "were artefacts of its argument shapes". Admitting R2 as a
  standalone entry would put a retracted result in front of a reader.

### REFUSE R3 — `benchmark-grader-semantics.md` (staged S093/S094/S097)

Filename-collides with the live entry `corpus/knowledge/benchmark-grader-semantics.md`
(round 33). The live file is the **richer** version: located quotes with line numbers
(`main.py:58`, `:279`, `:280`), the renumbered ids **S103** (Toolathlon `ab-testing`) and
**S104** (LLMs-as-Judges), and the executed-vs-default tolerance distinction
("`0.05` is 0.05 percentage points", the `0.1` default is *not* executed). The staged copy
cites **S094 and S097**, which the live registry carries as **rejected** supersede rows
(`corpus/SOURCES.md` S094/S097 = "duplicate staged row refused after registry collision") —
i.e. the staged file would re-introduce the exact ids the lane already refused, and it drops
the located-quote table. Overwriting the live file with it would also break C1's V3/V4 shape
expectations.

* **Flip condition.** Do not overwrite. If any part of the staged text is wanted, carry it as
  a *dated amendment section appended to* the live file, with the row ids renumbered to the
  live S103/S104 scheme, and only the content the live file lacks.

### REFUSE R4 — `benchmark-verifier-execution-model.md` (staged S092/S093/S100)

Filename-collides with the live round-31 entry, which is the richer, quote-anchored version
(`verifier_mode.py:18-21`, `:24-25`, `:31`; `Verifier.verify`; `bundled_tests`). The staged
copy is an earlier draft of the same entry (its own `used-by` points at the same path). No
new ground. *Flip: only as a dated amendment with located quotes the live file lacks.*

### REFUSE R5 — `benchmark-task-validity-checklist.md` (staged S020/S077–S080/S090)

Filename-collides with the live round-29 attempt-2 entry, which **already supersedes** the
staged package's numbers: the live file records "89 task directories and 89 `task.toml` files"
and states plainly that it "corrects the staged package, whose two cells read 92 top-level
task directories and 109 task directories" (`corpus/knowledge/benchmark-task-validity-checklist.md:79-88`).
The staged copy is the *uncorrected* draft; adopting it would re-import the 92/109 error the
lane already fixed. *Flip: none for the staged text as-is.*

### REFUSE R6 — `contamination-transparency-card.md` (staged S077/S081–S086)

Filename-collides with the live round-30 entry, which is the quote-anchored version
(≤25-word located quotes with the extraction quirks named per source). Adopting the staged
copy would drop the quote table. Also out of C1's theme (contamination, not grader
semantics). *Flip: only as a dated amendment with the live quotes retained.*

### REFUSE R7 — `terminal-bench-release-identity.md` (staged S092/S100)

Same entry round 34 already refused (Q6 duplicate). Re-checked here: the live S100 row
already carries the release-identity and task-count anchor ("92 top-level entries — 89
directories plus .gitignore, LICENSE and README.md"), and the live checklist already holds
the 89-vs-92 resolution (R5). The staged file adds no new ground. Its one extra claim —
"the repository carries **no** git tags" — I verified independently and it is *true*
(`GET /repos/laude-institute/terminal-bench-2/tags` → **0 tags**; `harbor-framework/terminal-bench`
→ v3.0.0 `2b0442c`, v4.0.0 `452bf30`), but that fact is not about grader semantics and is
not needed by C1. *Flip: only if the L1 wants a one-line append to the live S100 anchor.*

### REFUSE R8 — `benchmark-grader-integrity-models-2026-10-23.md` (S101/S102/S107) and `-2026-10-23b.md` (S094/S108)

Both cite ids the live registry carries as **rejected** supersede rows: S101 ("this id already
identifies the SWE-bench locked replay agent"), S102, and S094. The `-b` file also cites S094
directly. The -b file's own claim (grader semantics are task-parameterised, not a benchmark
property) is *partly* the same claim as R1's tabulation and would be redundant once R1 is
re-derived. *Flip: renumber to fresh ids and fold into A1/R1's amendment, never overwrite.*

### Adjacent-topic notes (not verdicts, but they will bite the L1)

* `judge-meta-evaluation-2026-10-23.md` cites **S103** for the survey, but the live S103 is the
  Toolathlon `ab-testing` script and the survey is live **S104** — the same id/URL mismatch
  round 34 flagged, in a new file. `judge-meta-evaluation-2026-10-23b.md` cites **S110**
  (GENIAC phase-2 results page) for a judge-calibration claim. Both are judge-theme, not C1's
  theme: held, but flag them before any adoption.
* `judge-calibration-thresholds.md` cites S009/S012/S078/S081/S087 — four of those ids are
  live (S009,S012,S081,S087) and S078 is in the collision block.

## 4. Comparison with round 34's screen

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/build/R34ReconPackage.md`
screened **6** entries and refused **all 6**; verdict line
`VERDICT: recon-package (6 screened; 0 admitted, 6 refused as staged)`.

| Round-34 entry | Round-34 verdict | Round-35 re-check | Change |
|---|---|---|---|
| `terminal-bench-release-identity.md` | refuse (Q6 duplicate) | R7 refuse | **same**, and now backed by an independent tag check |
| `toolathlon-grader-contract-2026-10-23.md` | refuse (Q1/Q2: no live source row for S114) | R1 refuse | **stronger ground**: the id problem persists *and* the row's own counts do not reproduce |
| `judge-meta-evaluation-2026-10-23.md` | refuse (Q3: cites S103 for survey §6) | held (adjacent topic) | **same defect, new file**: still cites S103 for the survey |
| `benchmark-grader-integrity-models-2026-10-23b.md` | refuse (Q1/Q2 + id collision) | R8 refuse | same, plus S094/S108 still collide |
| `cjk-benchmark-governance-2026-10-23c.md` | refuse (Q1/Q2) | held (out of theme) | unchanged |
| `cjk-dataset-documentation-standard-2026-10-23.md` | refuse (Q2/Q3) | held (out of theme) | unchanged |

Net delta: round 34 screened 6 of 65 and found 0 admits; round 35 screens 21 of 65 in C1's
theme and finds **2 admit-candidates** (both the executed-fixture-probe family, which round 34
never reached because it only saw the *static* tabulation) against **8 refuses**. The two
admit-candidates are admitted *conditionally* — as dated amendments into an existing entry,
with own-work artefacts re-homed into the lane — because C1's V4 (42/42) forbids new
knowledge files this round and the package's 24 id collisions forbid a wholesale append.

## 5. Falsifier ledger (every number above, with its command)

1. Package rows/entries: `grep -cE '^\| *S[0-9]{3,} *\|' merge/kengaku/SOURCES.append.md` → 175; `ls merge/kengaku/knowledge/corpus/knowledge/*.md | wc -l` → 65.
2. Live rows: `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 100; ids via `re.finditer(r'^\|\s*(S\d{3,})\s*\|', …, re.M)`.
3. Collisions = 24: set-intersection of the two id lists; staged ids ≤ S107 = 31.
4. Gate output `registry=100 staged=173 collisions=22 malformed=2 defects=167 prose=167`, exit 3: `python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`.
5. Filename collisions = 4: loop over the package's `knowledge/` names against `corpus/knowledge/`.
6. Live rows referencing the source repo = 0: `grep -c shokuknow corpus/SOURCES.md`.
7. C1 red on staged S105–S107: scratch clone `/tmp/k35-*/lane` at `6ac9611`, appended the 3 staged rows to `corpus/SOURCES.md`, `python3 plans/round35_c1_verify.py --lane .` → `V2 DEFECT S105 present 2 times`, `V6 DEFECT census exit 1`, `checks=6 defects=2`, `PREDICATE C1 fail`.
8. C1 baseline green in the same clone before the mutation: `checks=6 defects=0`, `PREDICATE C1 pass`.
9. C1 red on a new knowledge file + index row: same clone, one new `corpus/knowledge/*.md` + one README index row, committed → `V4 DEFECT knowledge files=103 index rows=43 (want 42/42)`, `checks=6 defects=1`, `PREDICATE C1 fail`.
10. C1 green on an in-place amendment: same clone, `## Dated amendment` appended to `corpus/knowledge/benchmark-grader-semantics.md`, committed → `checks=6 defects=0`, `PREDICATE C1 pass`.
11. Census `E12` on rows appended after `## Paths`: 144 × `E12 <id> row outside Registry section`, `--file` exit 1.
12. Census `E09` on prose recheck cells: 144 × `E09 S1xx recheck=2026-10-23 — …`, exit 1.
13. Census exit 0 for the gate-produced block: `sources_adopt.py … --scope-to-admit --attest-opened --recheck 180d --out block.md` → `wrote … rows=4`; inserted inside `## Registry` → `census validate --file` exit **0**, C1 `checks=6 defects=0`.
14. Round-7 probe re-run: `python3 lanes/kengaku/round7/toolathlon-grader-fixture-probe.py --fetch --src-dir /tmp/k35-scout-mgr/src` → exit 0, `## Counts - discriminates: 16 of 16`; table diff vs the staged artefact → 16/16 rows, **0 textual differences**.
15. R1 re-derivation: 108 graders fetched from `raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe…/tasks/finalpool/<task>/evaluation/main.py`; trees API for the 109-children split (108 trees + 1 blob `tasks/finalpool/task_conflict.json`); `ast` walk for `add_argument('--groundtruth_workspace')` → 107 declaring, 14 `required=True`, 89 `required=False`, 4 unspecified, 1 without the option; blob `size` vs staged bytes → 57/108 differ, all staged smaller (2–2836 B); argparse tolerance defaults → 3 (`1e-06`, `0.01`, `60`); `grep -l tolerance` → 16 files.
16. R2 denominator: `round6/toolathlon-grader-behaviour-probe.md` per-candidate table → 37 data rows (23 + 13 + 1); summary denominators → 38; 13 + 23 + 1 = 37.
17. R7 tag check: `GET /repos/laude-institute/terminal-bench-2/tags` → 0 tags; `GET /repos/harbor-framework/terminal-bench/tags` → v3.0.0 `2b0442c`, v4.0.0 `452bf30`.
18. Live registry rows cited as rejected: `corpus/SOURCES.md` S094, S097, S101, S102 (status `rejected`).

## 6. What I did not check (limits)

* 44 of the 65 staged entries (CJK governance, contamination cards, BenchmarkCards, OSF
  preregistration, GENIAC/post5G programme pages, model cards) are **held**: out of C1's
  theme, not screened, not verified, no verdict implied. The round-34 screen refused two of
  them on source-row grounds; that reasoning is untouched by this seat.
* Only round 7 of the seven upstream probe scripts was re-run. Rounds 8/9/10/13/14/16 were not
  re-executed (each needs its own fixture set and a pandas/openai-agents environment); their
  staged numbers are **unverified here**, not refuted.
* No package row was appended, no lane file was modified, no git/jj mutating command was run
  in the lane. All clone experiments were in `/tmp` scratch clones; the source repo was read
  only (`ls`, `cat`, `git cat-file -e HEAD:<path>`, `git log`).
* The R1 byte-column discrepancy is unexplained; I did not search the upstream history for a
  commit whose blob sizes match the staged column.

VERDICT: package-2-admit-8-refuse
