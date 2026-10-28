# Seat C1ExecClassifier — R52-C1 grader-vacuity classifier (round 52, wave 1, build)

Lane `kengaku-shokunin` · base tip `30801b479e3418c11089b8586178b6960216f364` · seat role: executor
Scope: implement the **frozen** §C1 classifier and run it over the frozen population. No lane-tree
source file, state file, template, script or MANIFEST file was written by this seat; the only
writes outside my scratch dir are this report and the artefacts listed in §7.

Timeline note (measured, because the instrument changed under me during the wave):
`2026-10-28T17:01:05` wave dispatch → `17:02:18` `plans/round52_c1_grader_audit.py` modified in
the working tree → `17:02:56` the L1 committed it as `07ea208 round-52: amendment A1 (per-test
classification + hardened CONFIRMED leg) with disclosure receipt` (claims file §"Amendment A1"
appended, receipt at `.ufo/waves/round-52/claims/a1-observation.txt`). My module was verified
against **all three** versions of the instrument (frozen HEAD, the 336-line interim, the committed
373-line A1) — the V-class rules are identical in all of them, so the deliverable is valid either
way. §5 reports what the change means and what still does not hold.

---

## 1. What I did

1. Read `plans/round-52-claims.md` (full) and `plans/round52_c1_grader_audit.py` (full) before
   writing any code.
2. Implemented the frozen classifier as a standalone module `classify.py`, mirroring the counter's
   `classify()` exactly (marker regexes, `def test_` count, branch order, `primary_grader()`).
3. Proved the mirror exact against **every** version of the counter over **all 184 captured byte
   streams** (0 mismatches each run).
4. Fetched the frozen population myself as a fallback (the fetch seat's captures dir was still
   empty when I started) and verified every file byte-exact against the pinned upstream tree.
5. Ran the classifier over the fetch seat's delivered captures (authoritative set) and over my own
   independent fetch; the two runs are identical task-for-task.
6. Ran the counter itself against a scratch lane populated with the delivered captures, to measure
   what the predicate actually prints. That surfaced the findings in §5.

## 2. The deliverable

`classify.py` — standalone module, stdlib only.

```
python3 classify.py --captures DIR [--population PATH] [--out records.json] [--notes notes.json]
                     [--emit-sums SHA256SUMS] [--histogram] [--parity] [--selftest]
```

* reads the frozen population (`plans/round52-tasks.json`, default) and a captures dir;
* resolves each task's **primary grader** exactly as the counter does (`tests/test_outputs.py`,
  preferring the non-`environment/` copy, same sort key);
* emits one JSON record per task: `task`, `grader` (population path), `sha256`, `bytes`, the four
  features (`presence`, `content`, `behaviour`, `test_functions`), `class`, `candidate` (V1/V4),
  `status`, `reason`;
* capture lookup: primary layout `<captures>/<population-path>` (the fetch seat's layout); fallback
  `<captures>/<population-path with "/"→"_">` (not needed on the delivered set).

**Frozen rules applied, unchanged** (claims §C1 table; branch order V1 → V2 → V3 → V4 → V0, first
match wins): V1 = presence marker and no content marker and no behaviour marker; V2 = behaviour
marker; V3 = content marker; V4 = no marker class and ≤ 2 `def test_` lines; V0 = otherwise.
Marker vocabulary copied verbatim from the counter. `V1`/`V4` = triage queue.
I did **not** change any rule, including after the A1 amendment (see §5/F2).

## 3. Measured results (run over the fetch seat's delivered captures)

Captures dir: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders`
(184 files, `<population-path>` layout).

```
POPULATION tasks=89 records=89 classified=89
CAPTURES dir=.../C1ExecFetchGraders/artifacts/graders capture_files_expected=184
CLASS V1=2 V4=0 V2=53 V3=32 V0=2
CANDIDATES total=2
  CANDIDATE pytorch-model-recovery   class=V1 grader=pytorch-model-recovery/tests/test_outputs.py   tests=5
  CANDIDATE torch-tensor-parallelism class=V1 grader=torch-tensor-parallelism/tests/test_outputs.py tests=3
UNDECIDABLE total=0
```

**Class histogram (89 tasks): `V1=2 · V2=53 · V3=32 · V4=0 · V0=2`** (in the counter's print order:
V1, V4, V2, V3, V0 → V1=2, V4=0, V2=53, V3=32, V0=2). The committed counter prints exactly the
same `CLASS` line over the same captures, so my classifier and the instrument agree on every task.

**Per-task records file:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecClassifier/artifacts/records.json`
(89 records; `notes.json` holds the rule-edge notes; `SHA256SUMS` the digests of the 184 captures;
`per-test-classes.json` the A1 per-test annotation computed with the counter's own functions).

### Undecidable rule cases

**None.** All 89 frozen tasks were decided: 0 captures absent, 0 tasks without a `test_outputs.py`,
0 undecodable byte streams. The rules were edge-loaded anyway; the four edge notes are in
`artifacts/notes.json`:

| task | class | why the rules land there |
|---|---|---|
| `pytorch-model-recovery` | V1 | presence marker hits only — 2 hits (`exists(` at lines 88 and 108), **0** content hits, **0** behaviour hits; 5 `def test_` lines (V4 unreachable: V1 wins first) |
| `torch-tensor-parallelism` | V1 | 1 presence hit (`exists(` at line 25), 0 content hits, 0 behaviour hits; 3 `def test_` lines |
| `distribution-search` | V0 | no marker class applies, but 4 `def test_` lines ⇒ the ≤2 test-function branch (V4) does not apply |
| `largest-eigenval` | V0 | no marker class applies, 3 `def test_` lines ⇒ V4 does not apply |

Located quotes (V1 candidates, presence-only):
* `pytorch-model-recovery/tests/test_outputs.py:108` — `assert hello_path.exists(), f"File {hello_path} does not exist"` (and `:88` — `assert weights_path.exists(), f"File {weights_path} does not exist"`)
* `torch-tensor-parallelism/tests/test_outputs.py:25` — `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"`

Neither V1 candidate is among the lane's 12 hand-read graders (`corpus/knowledge/tb2-*-grader.md`:
build-pmars, circuit-fibsqrt, constraints-scheduling, db-wal-recovery,
feal-differential-cryptanalysis, feal-linear-cryptanalysis, git-leak-recovery, git-webserver,
password-recovery, polyglot-c-py, protein-assembly, regex-log), so both are candidates for the
"never read by this lane" clause of the claim (subject to the independent second reader, not my
seat).

### Rule-vs-reality caveat (observation, not a rule change)

The V1 label is a property of the **frozen marker vocabulary**, not of the grader's real strength.
`pytorch-model-recovery` loads the model and compares state dicts (`torch`), and
`torch-tensor-parallelism` drives `torch.distributed`/`multiprocessing` — but the frozen
`BEHAVIOUR`/`CONTENT` vocabularies have no token for `torch.load`, `torch.`, `dist.` or `mp.`, so
both files land in V1 with 0 content/behaviour hits. The L1's own A1 receipt says the same thing
about these two files ("the file-level label V1 … is FALSE of those graders as a whole"). I did not
change any rule; the finding is that the *file-level* V1 label is a misdescription of these two
graders, which is exactly why the amendment moves the unit to the test function.

## 4. Fidelity evidence for the mirror

* `python3 classify.py --selftest` → `SELFTEST cases=9 failures=0` (the counter's 4 fixture bodies
  + 5 branch-order edges I added: presence+content→V3, presence+behaviour→V2, behaviour+content→V2,
  no-marker+3 tests→V0, no-marker+2 tests→V4).
* Parity over all 184 captured byte streams, three runs, `mismatches=0` each:
  * vs the **freeze-commit** instrument (`1315234`; sha256
    `dbdf24bafaf90c2f2fa4a0374e8af24c015d6cef442c89f4df39eb5e9b22c3ab`, 291 lines);
  * vs the 336-line working-tree interim;
  * vs the **committed A1** instrument (sha256
    `e43ff9e7cd2242ce62b561fbae67e41cb478be156d03ffc412972cdf7593e6be`, 373 lines).
* AST comparison of the counter versions: `classify`, `primary_grader`, `sha256_bytes`, `PRESENCE`,
  `CONTENT`, `BEHAVIOUR`, `TESTFN`, `CLASS_ORDER` — **IDENTICAL**. A1 does not touch the V-class
  rules; it adds a per-test layer and changes the candidate flag.

### Cross-check with the fetch seat (two independent fetches)

My fallback fetch (184 files from `raw.githubusercontent.com` at the pin) and the fetch seat's
delivered captures agree byte-for-byte: path sets equal, **0 digest mismatches**, 477374 bytes on
both sides. Every one of my 184 files also matches the upstream tree's **git blob sha1** and size
at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (184/184 byte-exact; manifest in
`artifacts/fetch-manifest.json`). My records over the two capture sets are identical task-for-task
(89/89 same grader path, sha256, bytes, class).

## 5. Findings (measured, with evidence)

### F1 — BLOCKING for leg 1: the counter's CAPTURES leg cannot pass as written

`collect()` increments `present` **once per task** (one primary grader per task) but compares it
to `pop["capture_file_count"]` = **184** — a count of *capture files*. `present` can therefore
never exceed 89, so `present == expected` is false for any data and the predicate's leg 1
("`CAPTURES expected=184 present=184 mismatched=0`") always fails ⇒ the kill rule fires ⇒ R52-C1
would be reported as an honest stop even with perfect captures.

Measured with the fetch seat's complete, digest-matched captures in a scratch lane
(`artifacts/counter-current-on-fetch-captures.txt`, and identically in
`artifacts/counter-committed-on-fetch-captures.txt` for the pre-A1 instrument):

```
TASKS total=89 records=89 classified=89
CAPTURES expected=184 present=89 mismatched=0
```

184/184 files were present and `mismatched=0`; `present=89` is the per-task counter. The defect is
present in the pre-A1 frozen instrument **and** in the committed A1 instrument, so it is not an
artefact of A1. It is a defect in the **frozen instrument**, not in the data. Fixing it is the L1's
call (amend before the scored after-run, or land a new round); the claims' PROTOCOL forbids an
in-place rewrite of a frozen rule, and I did not touch the lane tree.

### F2 — the instrument was amended mid-wave; the amendment is disclosed, the V-rules are untouched

* dispatch marker `.ufo/waves/round-52/w1.ready.dispatched` → `2026-10-28T17:01:05`
* counter modified `17:02:18`, committed `17:02:56` as `07ea208` (post-freeze: the freeze commit is
  `1315234`), with a disclosure receipt
  (`.ufo/waves/round-52/claims/a1-observation.txt`) and an appended claims section
  (`plans/round-52-claims.md` §"Amendment A1 — 2026-10-28, before the scored after-run (disclosed)").
* what A1 changes: the classification **unit** moves from the grader file to the test function
  (`split_tests`/`classify_test`, classes P0–P3, same marker vocabulary, mechanical split at
  `^def test_<name>(`); the candidate flag becomes `bool(p1) or cls in ("V1","V4")`; the CONFIRMED
  leg gains two stricter checks (the task must have an instrument record and be a vacuity
  candidate; the located quote must appear **verbatim** in the captured grader bytes).
* measured effect on the delivered captures: `TESTCLASS presence_only_tests=33
  tasks_with_presence_only=27`, `CANDIDATES total=29` (against 2 under the frozen file-level rule).
* what A1 does **not** change (verified by AST diff): `classify()`, `primary_grader()`,
  `sha256_bytes()`, and the constants `PRESENCE`, `CONTENT`, `BEHAVIOUR`, `TESTFN`, `CLASS_ORDER`.
  My module is therefore exact against the frozen rules *and* against the amended instrument.
* Note for the label seat: A1 changed the **candidate unit**, but `labels_agreement()` still
  compares blind labels against the **file-level** class (`CLASS_ORDER` = V1..V0). The LABELS leg
  is therefore a file-level agreement figure, while the CONFIRMED leg is a per-test unit. Worth
  stating explicitly in the lesson so the two figures are not read as one.

### F3 — the counter's "already read by this lane" guard does not fire

`lane_read_tasks()` extracts the hand-read task names with

```python
m = re.search(r"task `([a-z0-9-]+)`", text) or re.search(r"\b([a-z0-9-]+)\b task", text)
```

but the knowledge entries phrase it as `# Terminal-Bench 2.0 task grader, read and executed:
`build-pmars`` (`corpus/knowledge/tb2-build-pmars-grader.md:6`; the front-matter `source:` line at
`:1` contains "…that are this task's whole score…"). Neither regex matches; the second alternative
matches the tokens `0` (from "2.0 task") and `this` (from "this task's").

Measured: `lane_read_tasks(lane)` returns `{'0', 'this'}` — 2 bogus strings instead of the 12
hand-read task names. Consequence: the "never read by this lane before this round" restriction on
the CONFIRMED-new leg is **not enforced** by the instrument (a confirmation for any task would
count as new). This is still true in the committed A1 instrument (the function is unchanged there).
Substantively the two V1 candidates are genuinely un-read — I checked the 12 knowledge file names
by hand — so the claim survives for them, but the guard itself is broken.

### F4 — the A1 receipt's population statistics are not reproducible from the committed instrument

The A1 disclosure receipt states: "Per test function (the A1 unit): 308 test functions across the
89 graders, of which **54 are presence-only (P1)** and **42 of the 89 tasks** carry at least one",
and "The L1's own scan of all 89 graders measured 54 presence-only test functions across 42 tasks".

Measured with the committed A1 counter's own `classify_test()`/`split_tests()` over the delivered
captures (`artifacts/per-test-classes.json`, and the counter's own printed line
`TESTCLASS presence_only_tests=33 tasks_with_presence_only=27`):

* 89 primary graders: **308** test functions (agrees), **P1 = 33**, tasks with ≥1 P1 = **27**;
  per-test totals P3=167, P2=88, P1=33, P0=20;
* over all 94 captured `test_outputs.py` files (a different population): 322 test functions,
  P1=34, 28 files with ≥1 P1 — also not 54/42.

So the 308-test-function total and the file-level class histogram are reproducible, but the
**54 presence-only tests / 42 tasks** figures are not reproduced by the committed instrument or by
the wider capture population. I am not claiming the receipt is wrong about what the L1 saw — only
that the numbers a reader would take from it do not match the instrument that is meant to measure
them. Wave 2's falsify seats should check this explicitly.

A second receipt figure does not check out either: the receipt lists
`pytorch-model-recovery/tests/test_outputs.py` as "**9249 B**". The pinned file is **5591 B**
(sha256 `5d4d57c43e6913bf…`, byte-exact vs the upstream blob at the pin — see
`artifacts/fetch-manifest.json`); 9249 B is the size of `adaptive-rejection-sampler`'s
`tests/test_outputs.py`. The receipt's other two sizes do check out
(`bn-fit-modify/tests/test_outputs.py` = 5892 B, sha256 `364069f893e336a0…`).

### F5 — the amended candidate population differs from the frozen one (facts, no judgement)

Under the frozen claims text, CANDIDATES = V1 ∪ V4 = **2** tasks. Under the committed A1
instrument, CANDIDATES = 29 tasks (27 with ≥1 P1 test, plus the 2 file-level V1 tasks). The
per-test P1 test names for the 27 are in `artifacts/per-test-classes.json`. The claim's CONFIRMED
threshold is unchanged (`≥ 2`), but the queue a reader sees is now 29 tasks wide, so the triage
queue in the lesson should say which population it is reporting.

## 6. Exact commands run (read-only outside my scratch dir)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1ExecClassifier/tmp
cd /fast/scratch/hyaku/kengaku-r52/C1ExecClassifier
TMPDIR=$PWD/tmp python3 fetch_local.py --out $PWD/graders        # fallback fetch, 184 files
python3 classify.py --selftest
python3 classify.py --captures graders --parity                            # vs committed A1 counter
python3 classify.py --lane lanehead --captures graders --parity            # vs committed HEAD counter
python3 classify.py --captures graders --out records.json --notes notes.json --emit-sums SHA256SUMS
python3 classify.py --captures <C1ExecFetchGraders>/artifacts/graders \
        --out records_fetchseat.json --notes notes_fetchseat.json
# lane inspection (read-only):
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
git log --oneline -3 ; git status --porcelain ; git show --stat 07ea208
git show HEAD:plans/round52_c1_grader_audit.py > /fast/scratch/.../counter_head.py
python3 plans/round52_c1_grader_audit.py --lane /fast/scratch/.../fakelane2   # both instrument versions
```

No mutating git/jj command was run anywhere; no install transaction was needed (stdlib Python
3.14.8 and `curl` 8.23.0 were already present), so the tooling-record entry is empty.

## 7. Files produced (absolute paths)

Deliverable + receipts (kept out of scratch so they survive cleanup), all under
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecClassifier/`:

* `artifacts/classify.py` — the frozen classifier (also at
  `/fast/scratch/hyaku/kengaku-r52/C1ExecClassifier/classify.py` before cleanup)
* `artifacts/records.json` — 89 per-task records (task, grader, sha256, bytes, 4 features, class, candidate)
* `artifacts/notes.json` — the four rule-edge notes
* `artifacts/per-test-classes.json` — A1 per-test annotation, computed with the committed counter's own functions
* `artifacts/SHA256SUMS` — sha256sum-format digests of the 184 captures (paths relative to the graders root)
* `artifacts/fetch-manifest.json` — my fallback fetch receipt: per-file size, sha256, git blob sha1 vs the pinned tree (184/184 byte-exact)
* `artifacts/selftest.txt`, `artifacts/parity-vs-frozen-1315234.txt` (vs the freeze-commit instrument),
  `artifacts/parity-vs-committed-a1.txt` (vs the committed A1 instrument) — both `PARITY files=184 mismatches=0`
* `artifacts/counter-committed-on-fetch-captures.txt`, `artifacts/counter-worktree-on-fetch-captures.txt`,
  `artifacts/counter-current-on-fetch-captures.txt` — the counter's own output on the delivered captures (F1, F2, F4 evidence)
* `report.md` — this report (a copy also at `.ufo/waves/round-52/w1/C1ExecClassifier.md`)

Scratch dir `/fast/scratch/hyaku/kengaku-r52/C1ExecClassifier/` was removed after the artefacts above
were copied out.

## 8. Hand-off to the L1

1. **F1 blocks admission** of R52-C1 as written: `present` counts tasks, `expected` counts files.
   Measured `present=89` vs `expected=184` with a complete, digest-matched capture set. L1 decision
   needed (amend before the scored after-run, or land a new round).
2. **F2** — A1 is disclosed and committed; the V-class rules my classifier implements are unchanged
   by it (AST-verified), so the classifier stays valid. Decide which CANDIDATES population the
   lesson reports (2 frozen vs 29 amended) and state that the LABELS leg is still file-level while
   the CONFIRMED leg is per-test.
3. **F3** — `lane_read_tasks()` returns `{'0','this'}`; the "never read by this lane" guard does not
   fire. The two V1 candidates are nevertheless genuinely un-read.
4. **F4** — the A1 receipt's 54 P1 tests / 42 tasks do not reproduce from the committed instrument
   (33 / 27). Wave 2 should check this explicitly.
5. Ready for the second-reader / labrat seats: the presence-only quotes are
   `pytorch-model-recovery` (`:88`, `:108`) and `torch-tensor-parallelism` (`:25`); the per-test P1
   list for all 27 candidate tasks is in `artifacts/per-test-classes.json`.
6. **Blinding note:** `artifacts/records.json` and `artifacts/per-test-classes.json` are the
   classifier's output and must not be shown to the blind-label seat before it labels, or the LABELS
   agreement figure is contaminated (I warned that seat accordingly).
