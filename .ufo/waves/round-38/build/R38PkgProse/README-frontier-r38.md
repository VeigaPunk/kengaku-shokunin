Paste targets in `corpus/README.md`. Three blocks, in file order. (b1) is the item the seat was asked
for; (b2) and (b3) are what `plans/pkg_gate.py` P8 actually checks (`c_readme`, `plans/pkg_gate.py:233-256`):
one index row for the entry citing every registry row, and one coverage bullet that starts with "- " and
names both the entry and the receipt path. They are included here so the same paste lands a gate-clean
README; the entry author or L1 may replace the wording, not the required tokens.

### b1 — §Frontier sub-bullet (after the `*Partly discharged round 37 (2026-10-26):*` line, before the next `- **` item)

  - *Partly discharged round 38 (2026-10-26):* `knowledge/tb2-build-pmars-grader.md` reads and executes a
    fourth Terminal-Bench 2.0 task's scoring code (`build-pmars/tests/test_outputs.py` @ `2fd12b88`; S115,
    S116) against its `instruction.md`, probe `plans/build_pmars_probe.py`, receipt
    `corpus/evidence/round38/build-pmars-probe.txt`. The graded state is a class the lane had not executed
    before: a built executable plus a source tree, scored by `Path.exists()`, an `ldd` stdout string scan,
    directory shape and a `re.match` prefix on program stdout, with no rebuild anywhere — so a canned
    21-line C program with an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four
    tests, a `dlopen()`ed libX11 is invisible to the `ldd` scan, `Results: 12 34 78 forged` passes the
    prefix match, a binary that exits 3 passes, a canned script earlier on `PATH` answers the behaviour
    checks while `ldd` reads the silent installed file, `debian` may be a regular file, and a directory
    named `src/sim.c` counts as C source (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`). The
    "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining
    TB2 task graders (4 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for
    runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image, the oracle or a
    harness run, not contamination, not model or agent behaviour.

### b2 — coverage bullet (in the coverage list that ends with the round-37 `configure-git-webserver` bullet, `corpus/README.md:261`)

- **Terminal-Bench 2.0 task grader (fourth task, one new executed edge class)**: covered at source-code depth and executed offline (round 38, 2026-10-26) — knowledge/tb2-build-pmars-grader.md; S115, S116; probe `plans/build_pmars_probe.py`, receipt `evidence/round38/build-pmars-probe.txt`. A fourth instance of the same ground (4 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `build-pmars` only: the graded state is a built executable plus a source tree reached by `Path("/app").glob("pmars-*")`, `src.glob("*.c")` and `debian.exists()` (`tests/test_outputs.py:62-85`), and the behaviour checks are a `re.match` prefix on the last battle line and a `\d{5}` address count over debugger stdout (`:31-46`); the `ldd` scan is a substring test on four library names (`:53-57`). One new edge class in the executed sample: the artefact is a compiled binary whose provenance is inferred from directory shape, not shown. Headline passing states: a canned C program with an empty `debian/` dir and a zero-byte `src/dummy.c` (`canned-shape`), a `dlopen()`ed libX11 (`canned-x11-dlopen`), `Results: 12 34 78 forged` (`results-trailing-text`), exit 3 (`canned-exit-nonzero`), a `PATH`-earlier script beside a silent installed binary (`path-split`), `debian` as a regular file (`debian-is-file`), a directory named `src/sim.c` (`c-is-dir`). Not the remaining 85 TB2 tasks, not the task image, the oracle or a harness run, not task validity, difficulty or quality, not contamination, not agent behaviour.

### b3 — knowledge index row (after the `knowledge/tb2-git-webserver-grader.md` row, `corpus/README.md:70`)

| `knowledge/tb2-build-pmars-grader.md` | A fourth Terminal-Bench 2.0 task grader read and executed: `build-pmars`'s four tests score a binary at `/usr/local/bin/pmars` plus a `/app/pmars-*` tree by existence, an `ldd` stdout scan for four X11 library names, `debian/` and `src/*.c` presence, a `re.match` prefix on `Results: \d+ \d+ \d+` and a `\d{5}` debugger-address count — so a canned C program with an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four, and a `dlopen()`ed libX11 is invisible to `ldd`; a 22-case offline probe stages each state in its own bubblewrap sandbox (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`) | S115, S116 (terminal-bench-2 @ 2fd12b88) |

### Gate tokens these must keep (P8, `plans/pkg_gate.py:233-256`)

- one index row whose first cell is `` `knowledge/tb2-build-pmars-grader.md` `` and whose text contains
  both `S115` and `S116` (b3);
- one line starting exactly `- ` that contains `tb2-build-pmars-grader.md` and
  `evidence/round38/build-pmars-probe.txt` (b2 does; b1 is indented under §Frontier and does not satisfy
  this check);
- the set of `knowledge/*.md` files in the lane equals the set of index rows (so b3 must land with the
  entry file in the same commit).
