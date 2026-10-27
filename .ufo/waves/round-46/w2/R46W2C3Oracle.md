# R46W2C3Oracle — independent replication of the C3 polyglot-c-py probe verdicts

Seat: R46W2C3Oracle (executor, leaf). Round 46 wave 2 (falsify, v1). Target of attack: the landed claim
**C3 (coverage)** at lane tip `42d5043afac952fcb43bf4798757785dd258cf85` — specifically the case table in
`corpus/evidence/round46/polyglot-c-py-probe.txt` for the four states named in this seat's assignment.

## 1. Provenance (closure D3)

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" \
  && git -C "$S/lane" checkout -q 42d5043afac952fcb43bf4798757785dd258cf85
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/lane
$ git -C "$S/lane" rev-parse HEAD
42d5043afac952fcb43bf4798757785dd258cf85
```

The `LANE_CLONE_TOP` / `LANE_CLONE_HEAD` pair is echoed into the header of every receipt below (D3: a receipt
names the revision it measured).

**Artifact identity.** The grader and the oracle were copied byte-for-byte out of the lane clone; their digests
equal both `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS` and the digest header of the probe receipt:

```
$ sha256sum "$S/run/test_outputs.py" "$S/run/solve.sh"
b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  .../run/test_outputs.py
e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0  .../run/solve.sh
```

`corpus/evidence/round46/polyglot-c-py-probe.txt:8` states `# capture test_outputs.py sha256=b94a7a98…`; match.
The full capture set (Dockerfile, README.md, instruction.md, solve.sh, task.toml, test.sh, test_outputs.py)
also matched its `SHA256SUMS` byte-for-byte:

```
$ sha256sum corpus/evidence/round46/tb2-polyglot-c-py/*
2eb537f2… Dockerfile  591e27f9… README.md  a44b38ea… SHA256SUMS  9a8dd8d9… gitignore
a57c0c0e… instruction.md  e768453a… solve.sh  d31b9f60… task.toml  4770437e… test.sh  b94a7a98… test_outputs.py
```

**Independence.** `plans/polyglot_c_py_probe.py` was **not** opened by this seat. The harness
(`R46W2C3Oracle/harness/grade.py`, 138 lines) was written from the captured grader's own text only — the four
things the grader does, read at
`corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py:17,24,27,36,43`:
`os.listdir("/app/polyglot") == ["main.py.c"]`; `gcc main.py.c -o cmain` (`check=True`); for
`(42,"267914296")`, `(10,"55")`, `(0,"0")` both `python3 … N` and `./cmain N` `stdout.strip()` equal the
expected value (`check=True`).

## 2. Method

* Each state is a real directory mounted at `/app` in a scratch-rooted `bwrap` mini root (so `/app` is
  writable inside while `/home/vgpnk/.local/bin` stays read-only), executed as the command of the mandated
  envelope. The grader runs **byte-identical** (`importlib` load of `/work/test_outputs.py`) against
  `/app/polyglot`; no path in the grader was rewritten.
* `harness/run_case.sh` (sandbox + provenance) and `harness/grade.py` (state construction + grading) are the
  complete instrument; both are retained in this seat's report dir, byte-identical to the files the runs used
  (`sha256 ab1ba71c…` and `f4a6d5a2…` respectively, re-checked against the scratch copies).
* State recipes: `build` = `bash solve.sh` verbatim with cwd `/app` (creates `polyglot/` relatively); the three
  remaining states are byte copies of that build, plus one edit each.
* `oracle` grades the built state once, then re-grades the same untouched state (the receipt's `regrade`
  column). `lookup` writes this seat's own lookup-table polyglot. `extra` adds `NOTES.md`. `leftover` runs the
  build line that `instruction.md:5` itself prescribes, `gcc main.py.c -o /app/polyglot/cmain`.

## 3. Results — 4/4 verdicts agree with the probe receipt

| # | state | my observed verdict | probe receipt row (`corpus/evidence/round46/polyglot-c-py-probe.txt`, cited by line) | agree |
|---|---|---|---|---|
| 1 | oracle `solve.sh` output | **pass** (re-grade: **fail**) | `:10` `oracle-solve-sh … observed=pass … regrade=DIFF:F` | yes |
| 2 | lookup table for 42/10/0 | **pass** | `:11` `lookup-table predicted=pass observed=pass` | yes |
| 3 | oracle + `NOTES.md` | **fail** — `AssertionError: Expected only main.py.c, found: ['main.py.c', 'NOTES.md']` | `:14` `extra-file predicted=fail observed=fail` | yes |
| 4 | oracle + `cmain` (built per `instruction.md:5`) | **fail** — `AssertionError: Expected only main.py.c, found: ['main.py.c', 'cmain']` | `:15` `leftover-cmain predicted=fail observed=fail` | yes |

### 3.1 Case 1 — oracle state passes, and the same state fails on re-grade

```
{"case": "oracle", "grade1": {"error": null, "verdict": "pass"},
 "grade2_same_state": {"error": "AssertionError: Expected only main.py.c, found: ['main.py.c', 'cmain']", "verdict": "fail"},
 "outputs_after_grade1": {"0": {"c": "0", "c_rc": 0, "py": "0", "py_rc": 0},
                          "10": {"c": "55", "c_rc": 0, "py": "55", "py_rc": 0},
                          "42": {"c": "267914296", "c_rc": 0, "py": "267914296", "py_rc": 0}},
 "state_after_grade1": ["main.py.c", "cmain"], "state_after_grade2": ["main.py.c", "cmain"],
 "state_before": ["main.py.c"]}
```

Every number the receipt asserts for this row is reproduced on my side: both runtimes print the three expected
values with rc 0, and the first grade's own `gcc … -o /app/polyglot/cmain` is visible in
`state_after_grade1` **before** my own output probe ran. The re-grade fails on the listing assert, i.e. the
receipt's `regrade=DIFF:F` for this row survives (`polyglot-c-py-probe.txt`, `oracle-solve-sh` row: "the
per-case `regrade` column is its measurement" appears on the `regrade-same-state` row).

### 3.2 Case 2 — a lookup table is indistinguishable from a computation

My polyglot (`receipts/lookup-main.py.c`, sha256
`91cdec6ba2d382eeea0cd25425759e97208b09e9accd4701d1784cef5d1d2567`) contains **no Fibonacci loop**: the
Python side is `TABLE = {"42": "267914296", "10": "55", "0": "0"}` and the C side is three `strcmp` branches.
It passes.

```
{"case": "lookup", "grade1": {"error": null, "verdict": "pass"},
 "outputs_after": {"0": {"c": "0", "c_rc": 0, "py": "0", "py_rc": 0},
                   "10": {"c": "55", "c_rc": 0, "py": "55", "py_rc": 0},
                   "42": {"c": "267914296", "c_rc": 0, "py": "267914296", "py_rc": 0}},
 "state_before": ["<OSError:FileNotFoundError>"], "state_before_grade": ["main.py.c"],
 "state_after": ["main.py.c", "cmain"]}
```

Confirms the class wording independently: "the grader has exactly three fixed points and never inspects the
source" (`polyglot-c-py-probe.txt`, `lookup-table` row). The state before my write raised
`FileNotFoundError` on `os.listdir` — the same shape the receipt records for its `nop` row (`:9`, `error=FileNotFoundError`), so the seed
behaviour (empty `/app`) also matches.

### 3.3 Case 3 — an extra file fails **before** gcc runs

```
{"case": "extra", "grade1": {"error": "AssertionError: Expected only main.py.c, found: ['main.py.c', 'NOTES.md']", "verdict": "fail"},
 "state_before": ["main.py.c"], "state_before_grade": ["main.py.c", "NOTES.md"],
 "state_after": ["main.py.c", "NOTES.md"]}
```

`state_after` equals `state_before_grade`: no `cmain` appeared, so the listing assert fired before the compile
— the receipt's causal clause "fails before gcc runs" is reproduced, not merely the fail verdict.

### 3.4 Case 4 — following `instruction.md` produces a state the grader forbids

```
{"case": "leftover", "gcc_cmain_rc": 0, "grade1": {"error": "AssertionError: Expected only main.py.c, found: ['main.py.c', 'cmain']", "verdict": "fail"},
 "state_before": ["main.py.c"], "state_before_grade": ["main.py.c", "cmain"]}
```

`instruction.md:5` tells the agent `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain && /app/polyglot/cmain N`;
`test_outputs.py:17-19` requires `os.listdir("/app/polyglot") == ["main.py.c"]`. A state that does exactly what
the instruction says fails the grader: the instruction/grader contradiction the receipt reports is real on my
instrument too.

## 4. Extra corroboration (free, same runs)

* Host toolchain differs from the image and did not change any verdict: `Python 3.14.8 / gcc (GCC) 16.2.1`
  vs the image's `python3 3.12.3 / gcc 13.2.0` (`instruction.md`). Both the published solution and my table
  polyglot compile with only `warning: missing terminating " character` on the closing `"""` line and exit 0 —
  `check=True` reads the exit status, matching the receipt's `compile-warning` mechanism.
* The receipt's 18-row tally (`cases=18 observed_pass=7 observed_fail=11 mismatches=0`) is not re-derived here:
  this seat's assignment is the four states above. All four agree; no disagreement was found to report.

## 5. Limits

* `pytest` is not installed on the host and was deliberately not installed (writing `~/.local/bin` is
  forbidden). The harness therefore calls the captured test function directly (`grade.py:run_grader`); pytest's
  only role in `test.sh` is to collect and call that same function, so the verdict semantics are identical, but
  this is a harness step I did not execute.
* Four of the eighteen receipt rows were attacked; the other fourteen were not re-run.
* `importlib` execution of the grader is byte-identical to the capture (digest above), but I execute it as
  `python3 /work/grade.py`, not as `uvx -p 3.13 … pytest` (`test.sh`).
* Scratch `/fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle` is deleted after copying receipts; the retained
  evidence is `receipts/{build,oracle,lookup,extra,leftover}.txt`, `receipts/{oracle,lookup}-main.py.c` and
  `harness/{grade.py,run_case.sh}` in this report directory.

## 6. Retained evidence (envelope receipts, verbatim)

Each run below is the mandated envelope; every `ENVELOPE end` line shows
`local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged` and `exit=0` — no `INVALID`, no
exit 4.

### build (`receipts/build.txt`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-build /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-build --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-build/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/run/run_case.sh build
ENVELOPE start 02:47:46 cwd=/home/vgpnk/Projects/shokunin
LANE_CLONE_HEAD 42d5043afac952fcb43bf4798757785dd258cf85
{"case": "build", "solve_rc": 0, "solve_stderr": "", "state_before": ["<OSError:FileNotFoundError>"], "state_built": ["main.py.c"]}
ENVELOPE end 02:47:47 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

### oracle (`receipts/oracle.txt`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-oracle /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-oracle --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-oracle/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/run/run_case.sh oracle
ENVELOPE start 02:47:57 cwd=/home/vgpnk/Projects/shokunin
LANE_CLONE_HEAD 42d5043afac952fcb43bf4798757785dd258cf85
{"case": "oracle", "grade1": {"error": null, "verdict": "pass"}, "grade2_same_state": {"error": "AssertionError: Expected only main.py.c, found: ['main.py.c', 'cmain']", "verdict": "fail"}, "outputs_after_grade1": {"0": {"c": "0", "c_rc": 0, "py": "0", "py_rc": 0}, "10": {"c": "55", "c_rc": 0, "py": "55", "py_rc": 0}, "42": {"c": "267914296", "c_rc": 0, "py": "267914296", "py_rc": 0}}, "state_after_grade1": ["main.py.c", "cmain"], "state_after_grade2": ["main.py.c", "cmain"], "state_before": ["main.py.c"]}
ENVELOPE end 02:47:59 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

### lookup (`receipts/lookup.txt`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-lookup /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-lookup --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-lookup/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/run/run_case.sh lookup
ENVELOPE start 02:47:57 cwd=/home/vgpnk/Projects/shokunin
LANE_CLONE_HEAD 42d5043afac952fcb43bf4798757785dd258cf85
{"case": "lookup", "grade1": {"error": null, "verdict": "pass"}, "outputs_after": {"0": {"c": "0", "c_rc": 0, "py": "0", "py_rc": 0}, "10": {"c": "55", "c_rc": 0, "py": "55", "py_rc": 0}, "42": {"c": "267914296", "c_rc": 0, "py": "267914296", "py_rc": 0}}, "state_after": ["main.py.c", "cmain"], "state_before": ["<OSError:FileNotFoundError>"], "state_before_grade": ["main.py.c"]}
ENVELOPE end 02:47:59 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

### extra (`receipts/extra.txt`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-extra /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-extra --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-extra/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/run/run_case.sh extra
ENVELOPE start 02:47:57 cwd=/home/vgpnk/Projects/shokunin
LANE_CLONE_HEAD 42d5043afac952fcb43bf4798757785dd258cf85
{"case": "extra", "grade1": {"error": "AssertionError: Expected only main.py.c, found: ['main.py.c', 'NOTES.md']", "verdict": "fail"}, "state_after": ["main.py.c", "NOTES.md"], "state_before": ["main.py.c"], "state_before_grade": ["main.py.c", "NOTES.md"]}
ENVELOPE end 02:47:59 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

### leftover (`receipts/leftover.txt`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-leftover /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-leftover --bind /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/env-leftover/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle/run/run_case.sh leftover
ENVELOPE start 02:47:57 cwd=/home/vgpnk/Projects/shokunin
LANE_CLONE_HEAD 42d5043afac952fcb43bf4798757785dd258cf85
{"case": "leftover", "gcc_cmain_rc": 0, "gcc_cmain_stderr": "/app/polyglot/main.py.c:44:15: warning: missing terminating \" character\n   44 | #define ert \"\"\"\n      |               ^", "grade1": {"error": "AssertionError: Expected only main.py.c, found: ['main.py.c', 'cmain']", "verdict": "fail"}, "state_after": ["main.py.c", "cmain"], "state_before": ["main.py.c"], "state_before_grade": ["main.py.c", "cmain"]}
ENVELOPE end 02:47:59 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

## 7. What survives the attack

Nothing in the four rows I attacked is contradicted: an independent harness, an independent polyglot recipe,
and a different sandbox construction reproduce all four verdicts plus the oracle row's re-grade observation.
C3's probe table is not falsified on these states. No tracked lane file was touched: after the seat's work,
`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain` lists only untracked
`.ufo/waves/round-46/w2*` entries (the L1's dispatch files plus this seat's report dir); no tool was installed
and no mutating git/jj command was run anywhere.

VERDICT: c3-independent-verdicts-agree-4/4
