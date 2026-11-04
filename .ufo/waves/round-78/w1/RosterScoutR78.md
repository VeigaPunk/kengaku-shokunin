# RosterScoutR78 — per-surface reconnaissance of the executed-grader roster

Seat: `RosterScoutR78` (scout, leaf — no dispatch). Round 78, wave w1. Read-only.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, `git rev-parse master` = `f20a2f6f`
(freeze `2f9eeafb` is an ancestor; verified `git merge-base --is-ancestor 2f9eeafb master`).
Frozen claims read in full before any command: `plans/round-78-claims.md` (R78-C1, R78-C2).
Nothing was written outside this report; no scratch dir was needed (no fixture, no build).
No tool was installed or upgraded; pacman was not touched.

Reproducing commands (all read-only):

```
git -C …/kengaku-shokunin rev-parse master
python3 -c '<census/ledger parser>'            # §2/§3 numbers below
sha256sum corpus/evidence/round52/graders/<task>/tests/test_outputs.py
grep -n 'PREDICATE R[0-9]*-C[0-9]' corpus/evidence/round<NN>/…
git ls-files --error-unmatch <receipt>
```

---

## 1. What each round actually replayed offline

One row per round in the assigned list (57, 58, 59, 60, 61, 64–72), plus rounds 62 and 63,
which are not in the assigned list but are required by questions 2 and 3 (marked `adjacent`).
"Names the task" is the literal file:line whose bytes carry the TB2 task slug. All fourteen
assigned rounds replay **Terminal-Bench 2.0 at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`**
(the pin is named in `corpus/evidence/round62/tb2-tree-2fd12b88.json:sha` and in the probe
`TB2_PIN` constants, e.g. `plans/round57_c2_eigen_probe.py:49`).

| round | TB2 task replayed | file:line naming the task | receipt of record (predicate line) | note |
|---|---|---|---|---|
| 57 | `largest-eigenval` | `corpus/evidence/round57/tb2-eigenval/task.toml:5` `name = "terminal-bench/largest-eigenval"` | `round57/eigen-probe.txt:27` `PREDICATE R57-C2 pass` | 24-case timing/wall battery; class numeric-band/timing-wall, **not** one of the three C1 classes |
| 58 | `distribution-search` | `round58/tb2-distribution-search/task.toml:5` `name = "terminal-bench/distribution-search"`; also `round58/kl-oracle.md:3` | `round58/kl-probe.txt:15` `PREDICATE R58-C3 pass` | 12 cases / 48 legs; numeric-band |
| 59 | `openssl-selfsigned-cert` | `round59/tb2-openssl-selfsigned-cert/task.toml:5` `name = "terminal-bench/openssl-selfsigned-cert"` | `round59/openssl-probe.txt:17` `PREDICATE R59-C1 **fail**` | first run misses on 2 legs |
| 60 | `openssl-selfsigned-cert` (re-freeze) | same capture; instrument `plans/round59_c1_openssl_probe.py:2` | `round60/openssl-probe-refreeze.txt:15` `PREDICATE R59-C1 pass` | **of record for this task**; the `grep-manual/grep.html` in this round is a *manual* capture (S223), not a task |
| 61 | `cancel-async-tasks` | `plans/round61_c1_cancel_probe.py:2` ("``cancel-async-tasks`` grader"); capture `round61/tb2-cancel-async-tasks/tests/test_outputs.py:1` | `round61/cancel-async-probe.txt:15` `PREDICATE R61-C1 pass` | signal-delivery; the `whatwg-windows1252/` capture is source S227, not a task |
| 62 | — (no task replay) | — | `round62/class-survey.txt:23` `PREDICATE R62-C1 pass` | grader-class census only (see §3) |
| 63 | `pypi-server` (single `test_api` leg) | `plans/round63_c1_pypi_probe.py:2` ("``pypi-server`` grader") | run 1 `round63/check-receipt-run1.txt:2` `PREDICATE R63-C1 fail`; amended run `round63/pypi-probe-rerun.txt:9` `PREDICATE R63-C1 pass` | **verdict of record is MISS** (`plans/round-63-claims.md:158`, A1 item 1: no re-freeze, no narrowing); see §2 |
| 64 | `kv-store-grpc` | `round64/kvstore-probe.txt:1` `# R64-C1 receipt -- TB2 kv-store-grpc grader offline under bwrap` | `round64/kvstore-probe.txt:66` `PREDICATE R64-C1 pass` | post-hardening receipt of record; `round64/prehardening/` holds the superseded run |
| 65 | `sqlite-with-gcov` | `round65/sqlite-gcov-probe.txt:1` | `round65/sqlite-gcov-probe.txt:67` `PREDICATE R65-C1 pass` | of record; `replication-run2-receipt.txt:67` is the determinism rerun |
| 66 | `torch-tensor-parallelism` | `round66/tensor/receipt.txt:1` `path=…/graders/torch-tensor-parallelism/tests/test_outputs.py` | `round66/tensor/receipt.txt:47` `PREDICATE R66-C1 pass` | 5-case frozen vector table |
| 67 | `torch-pipeline-parallelism` | `round67/pipe/receipt.txt:1` and `:4` (`path=…/torch-pipeline-parallelism/…`) | `round67/pipe/receipt.txt` carries **no** `PREDICATE` line (17 lines, 6 `VECTOR … frozen=match`); the pass text is `round67/pipe/a1-mutants.txt:8` and `… --check-receipt` output | see discrepancy D1 |
| 68 | `pypi-server` (full grader) | `plans/round68_c1_pypi_finish.py:2`; receipt binds by `round68/pypi/receipt.txt:3` `GRADER sha256=82c635…` | `round68/pypi/receipt.txt:12` `PREDICATE R68-C1 pass` | **of record for the member** (supersedes 63) |
| 69 | `nginx-request-logging` | `round69/nginx/receipt-v2.txt:3` `GRADER …graders/nginx-request-logging/tests/test_outputs.py` | `round69/nginx/receipt-v2.txt:57` `PREDICATE R69-C1 **fail**` (leg-coverage `seen_f=6`) | miss; table re-frozen in 70 |
| 70 | `nginx-request-logging` (7-case re-freeze) | `round70/nginx/receipt.txt:4` | `round70/nginx/receipt.txt:78` `PREDICATE R70-C1 pass` (`LEG-COVERAGE legs=8 seen_p=8 seen_f=8`) | **of record for the member** |
| 71 | `hf-model-inference` | `plans/round71_c1_hf_probe.py:2`; receipt binds by `round71/hf/receipt.txt:2` `GRADER sha256=61a686…` | `round71/hf/receipt.txt:36` `PREDICATE R71-C1 pass` | **of record for the member** (counted from 71 in `SKILL.md:78`) |
| 72 | `hf-model-inference` (provenance + 9th case) | `plans/round72_c1_hf_probe.py:2` | `round72/hf/receipt.txt:40` `PREDICATE R72-C1 pass` | second passing replay of the same member; see D2 |

Observed: every assigned round replayed exactly one TB2 task, and no round in the list replayed a
member whose class is outside the round's topic. `executed17.lst` (17 tasks) intersects the twelve
members of the three C1 classes in **zero** names (checked by set intersection), so nothing in
rounds 1–56 pre-empts the C1 ledger.

Inference (stated as such): rounds 57–61 are grader-leg batteries rather than full-grader replays,
so their receipts are "replay of the grader's legs", not a container run — the same shape the C1
claim accepts for its `executed` rows.

---

## 2. Cross-check against `plans/grader-selected-members.json`

Ledger facts (re-derived, not imported): `schema=r78-selected-member-ledger/1`, **12 members /
13 member-class pairs / 7 executed / 5 unexecuted**, tracked at `2f9eeafb`
(`git log -1 -- plans/grader-selected-members.json`), sha256
`e268972164df734b7f6fc7ed95e86b56cbe0561584a2e44e60f8526149efb606`.

### 2a. The seven executed rows are real replays of the right grader

Each named receipt is tracked, exists, and its `GRADER` digest equals the stored grader bytes
(re-derived with `sha256sum`, all seven exact matches):

| member | ledger receipt | receipt GRADER sha | stored `round52/graders/<t>/tests/test_outputs.py` | verdict token |
|---|---|---|---|---|
| hf-model-inference | `round71/hf/receipt.txt` | `61a686d6…87857` | `61a686d6…87857` | `PREDICATE R71-C1 pass` (:36) |
| kv-store-grpc | `round64/kvstore-probe.txt` | `115de2e9…1b0e` | `115de2e9…1b0e` | `PREDICATE R64-C1 pass` (:66) |
| nginx-request-logging | `round70/nginx/receipt.txt` | `045cc716…4cda0` | `045cc716…4cda0` | `PREDICATE R70-C1 pass` (:78) |
| pypi-server | `round68/pypi/receipt.txt` | `82c63517…0be4c` | `82c63517…0be4c` | `PREDICATE R68-C1 pass` (:12) |
| sqlite-with-gcov | `round65/sqlite-gcov-probe.txt` | `b165f850…5a54` | `b165f850…5a54` | `PREDICATE R65-C1 pass` (:67) |
| torch-pipeline-parallelism | `round67/pipe/receipt.txt` | `23574246…8c64f` | `23574246…8c64f` | **no predicate line**; 6× `VECTOR … frozen=match` (`token=vectors`) |
| torch-tensor-parallelism | `round66/tensor/receipt.txt` | `4ae4285e…08290` | `4ae4285e…08290` | `PREDICATE R66-C1 pass` (:47) |

All seven are also **absent** from `executed17.lst` (correct: they post-date round 52).

### 2b. Are the seven rows the only offline replays of a member? **No.**

The seven rows are the only executed **members**, but not the only round-level replays. Counting
round-receipts that exercise a member of `network-service` / `process-environment` / `db-state`:

- **10 replays over 7 members**: 63 & 68 → `pypi-server`; 64 → `kv-store-grpc`; 65 →
  `sqlite-with-gcov`; 66 → `torch-tensor-parallelism`; 67 → `torch-pipeline-parallelism`;
  69 & 70 → `nginx-request-logging`; 71 & 72 → `hf-model-inference`.
- Extra **passing** receipts for already-counted members: `round63/pypi-probe-rerun.txt:9`
  (`PREDICATE R63-C1 pass` — but the claim's verdict of record for R63-C1 is **MISS**, A1 §1, so
  it may not be used as a member's evidence) and `round72/hf/receipt.txt:40` (`R72-C1 pass`).
- One extra **failing** receipt: `round69/nginx/receipt-v2.txt:57` (`R69-C1 fail`).

**Executed members the ledger omits: none.** The ledger's 12 keys are exactly the union of the
census's three member lists; every executed member is present, and `install-windows-3.11` carries
both classes in one row (hence 12 members / 13 pairs).

**Ledger reasons contradicted by an evidence file: none.** Each of the five typed reasons fires
in the stored grader bytes at a literal line, and no stored capture supplies the missing
prerequisite:

| member | reason | detector evidence in stored grader bytes | missing prerequisite stored? |
|---|---|---|---|
| filter-js-from-html | browser-required | `round52/graders/filter-js-from-html/tests/test_outputs.py:12` `from selenium import webdriver`; `:127` `driver = webdriver.Chrome(...)` | no (no chromedriver/chrome anywhere in repo; `find` empty) |
| git-multibranch | network-install-required | `…/git-multibranch/tests/test_outputs.py:12-13` `apt-get update` + `DEBIAN_FRONTEND=noninteractive apt-get install -y curl expect git openssh-client` (inside the `verify.sh` the grader writes at `:7`) | no |
| headless-terminal | candidate-library-required | `…/headless-terminal/tests/test_outputs.py:13` `from headless_terminal import HeadlessTerminal` (repeated `:18,32,57,84,99,120`) | no (`headless_terminal` appears only in this grader) |
| install-windows-3.11 | vm-required | `…/install-windows-3.11/tests/test_outputs.py:21` `pgrep qemu-system`; `:33` `/proc/{pid}/cmdline`; `:49` `/tmp/qemu-monitor.sock`; `:57` `:5901` listener | no (no qcow2/img in repo) |
| query-optimize | external-db-required | `…/query-optimize/tests/test_outputs.py:10-11` `/app/oewn.sqlite`, `/tests/golden.sql`; `:77-79` sha256 pin `89eab755…ad5a` over the DB | **no** (`find` for `oewn.sqlite`/`golden.sql` → empty) |

Counter cross-check (read-only, not imported): `plans/round78_c1_class_member_ledger.py:61-74`
carries exactly these five reason strings and a per-reason regex; the freezes' after-receipt
`corpus/evidence/round78/c1-after.txt` (untracked at read time, sibling seat) records
`UNIVERSE classes=3 members=12 pairs=13`, `LEDGER rows=12 executed=7 unexecuted=5`,
`DEFECTS n=0`, `TARGET … unaccounted=0 unbacked=0`, and `token=vectors` for
`torch-pipeline-parallelism` — i.e. the counter already takes the claim's "or a fully frozen
vector table" branch and does not rely on a predicate line in that receipt.

### 2c. What the ledger does *not* bind (scope observation, not a claim violation)

The counter validates an executed row by (i) receipt path exists and is tracked, (ii) the
`verdict_token` check over that receipt's bytes, (iii) `round ∈ 1..78`. It does **not** compare
the receipt's `GRADER sha256=` to the member's stored grader. I re-derived that binding by hand
(§2a) and all seven match, so the ledger is factually correct today; the gate alone would not
catch a member↔receipt swap that kept a passing predicate string. This is outside the frozen
predicate (which asks for a tracked receipt carrying the predicate/vector token), so it is
reported as a residual risk, not a defect.

---

## 3. Is `corpus/evidence/round62/class-survey.txt` still the right population source?

Observed (byte-level, `python3` parse of the raw file, not the tool-rendered line):

- `bytes=5528`, `sha256=ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613` —
  byte-identical to the round-62 landing claim ("sha ee30c698…5613, 5528 bytes",
  `git log -1 -- corpus/evidence/round62/class-survey.txt` = `629f1267`, 2026-11-02). File
  unchanged since; `DETERMINISM second-run-identical=True` (:22), `PREDICATE R62-C1 pass` (:23).
- `CLASS network-service count=8 members=…` is line **11** and parses to exactly:
  `filter-js-from-html, git-multibranch, headless-terminal, hf-model-inference,
  install-windows-3.11, kv-store-grpc, nginx-request-logging, pypi-server` — `count=8`,
  8 parsed names, no duplicates. `process-environment` (line 14) = 3 names;
  `db-state` (line 16) = 2 names.
- Set equality with the ledger is **exact in both directions**: zero census members absent from
  the ledger, zero ledger members absent from the census class; the only multi-class member is
  `install-windows-3.11`, giving the 13 pairs.
- The SKILL row implication (`SKILL.md:78`, `executed 4 of 8`) matches: the four named executed
  (`kv-store-grpc`, `pypi-server`, `nginx-request-logging`, `hf-model-inference`) plus the four
  remaining census names are exactly the eight. `SKILL.md:78` also carries the required
  `ledger=plans/grader-selected-members.json` pointer (checked on the raw 2055-byte line, not
  the truncated render).
- All eight network-service names exist in the pinned tree capture
  (`round62/tb2-tree-2fd12b88.json`, `sha=2fd12b88…`, 92 entries = 89 task dirs + 3 dotfiles):
  `missing from tree: []`.
- No later round re-issues a grader-class census. The `census-before/after.txt` files in rounds
  65–77 are **SOURCES** censuses (`kengaku W04 S040 duplicate url …` / `ROWS: 240`), a different
  population. Round 63's own claim cites the census as its universe source
  (`plans/round-63-claims.md`, R63-C1 line: "8 members, `corpus/evidence/round62/class-survey.txt:11`").

Verdict: **yes, still the right population source.** Its `EXECUTED-COVERAGE` line (:21,
`executed=17 … classes-uncovered=network-service,process-environment,db-state,container-image`)
is a round-52 snapshot by design — the census consumes `executed17.lst`
(`plans/round62_c1_class_survey.py:74`) — and is superseded for coverage accounting by the C1
ledger's `COVERAGE recomputed_*` line, while class *membership* (what C1 uses) is unaffected.

---

## 4. Discrepancies (4; none overturns the ledger's membership or reasons)

**D1 — `SKILL.md:81` prose vs the receipt's bytes (medium).** The `process-environment` row says
the receipt of record `corpus/evidence/round67/pipe/receipt.txt` carries `` `PREDICATE R67-C1
pass` ``. The committed file is 17 lines and contains no `PREDICATE` line; it carries six
`VECTOR <case> … frozen=match` lines. The pass text exists only in
`corpus/evidence/round67/pipe/a1-mutants.txt:8` (`base rc=0 CHECK ok cases=6 / PREDICATE R67-C1
pass`) and in the `--check-receipt` output (`.ufo/waves/round-67/w1/KnowledgeDraft/check-receipt-cited.txt:2`).
Claim-compatible via the "or a fully frozen vector table" branch, and the C1 counter already
records `token=vectors`; only the SKILL sentence over-claims the receipt's own bytes.
Reproduce: `grep -c PREDICATE corpus/evidence/round67/pipe/receipt.txt` → `0`.

**D2 — the ledger is a receipt-of-record map, not a replay register (low).** `round`/`receipt`
name one round per member, while three members were replayed more than once: `pypi-server`
(63 pass-under-amended-detector / **verdict of record MISS**, 68 pass), `nginx-request-logging`
(69 fail, 70 pass), `hf-model-inference` (71 pass, 72 pass). Reading the ledger as "the only
replay" would over-claim for 63 and under-record 72. Reproduce: `grep -rn 'PREDICATE R6[38]-C1'
corpus/evidence/round63 corpus/evidence/round68`, `grep -n 'PREDICATE R7[12]-C1'
corpus/evidence/round7{1,2}/hf/receipt.txt`.

**D3 — stale unexecuted lists still name all seven executed members (low; dated artifact).**
`corpus/evidence/round52/graders/unexec.lst` (69 lines) and `unexec72.lst` (72 lines) each contain
every one of the seven executed members (checked `grep -cx` = 1 for all seven). Provenance:
committed byte-as-is at the round-62 amendment `968f6ae7`, documented as round-52 population
bookkeeping in `corpus/knowledge/tb2-grader-class-census.md:21-27`; the census reads them
(`plans/round62_c1_class_survey.py:74`). Not a C1 defect, but it is the one committed evidence
file whose bytes contradict the ledger's `executed` rows, so nothing should cite `unexec*.lst` as
current coverage state.

**D4 — the population source does not self-name its pin (low; calibration/self-location).**
`round62/class-survey.txt` contains no `2fd12b88`; the pin appears only in the sibling capture
filename `round62/tb2-tree-2fd12b88.json`. A reader of the census bytes alone cannot tell which
upstream tree (89 dirs) it measured. This is the same class of gap R78-C2 is repairing for
round-77/78 receipts, one artifact older.

Adjacent observation (not counted): three of the seven ledger receipts do not name their task in
their own bytes — `round68/pypi/receipt.txt`, `round71/hf/receipt.txt`, `round72/hf/receipt.txt`
bind to the grader only through `GRADER sha256=` (which I verified matches) — and nine of the
fifteen replay receipts (§1) name no TB2 pin at all (`grep -c 2fd12b88` → 0 for 57, 58, 59, 60,
61, 66, 67, 71, 72; → 1 for 63, 64, 65, 68, 69, 70).

---

## 5. Remaining unknowns

- Whether the round-63 amended detector's pass (`pypi-probe-rerun.txt:9`) may ever stand is an
  open operator question (`.ufo/l0-questions.md`, `kengaku | round-63`); it does not affect the
  ledger, which uses round 68.
- Whether any *upstream* TB2 tree newer than pin `2fd12b88` changes the three class member sets.
  Not checkable from the lane's committed bytes; the ledger and census are both scoped to the
  frozen pin, and the claim declares the census as the universe.
- The C2 stamp-location surface is out of scope for this seat and was not audited.
- `corpus/evidence/round78/*` was untracked and being written by sibling seats while read; the
  `c1-after.txt` figures quoted in §2b are that live artifact, not a landed commit.

---

ROSTER: 7 executed / 5 unexecuted / 4 discrepancies
