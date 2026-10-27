source: S166 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py — the one pytest function that is this task's whole score: a pre-build listing assert, a grading-time gcc build, and three fixed-point stdout comparisons, lines 1-46, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-27
source: S167 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test.sh — the harness plumbing: uvx pytest 8.4.1 under a 3.13 interpreter, and the reward mapping from pytest's exit status, lines 1-29, same commit, accessed 2026-10-27
source: S168 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/instruction.md — the request the grader is mapped against, lines 1-9, same commit, accessed 2026-10-27
source: S169 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/solution/solve.sh — the task oracle: one heredoc writing a single file that is valid Python 3 and valid C at once, lines 1-57, same commit, accessed 2026-10-27
source: S170 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/environment/Dockerfile — the image recipe: ubuntu:24.04, WORKDIR /app, apt install gcc as the only tool, lines 1-6, same commit, accessed 2026-10-27
source: S171 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/task.toml — the authors' metadata: verifier and agent timeouts, the published image tag, internet allowed, lines 1-41, same commit, accessed 2026-10-27
source: S172 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/README.md — the authors' own README: the single-file rule, the two tools, the three graded test cases, lines 1-24, same commit, accessed 2026-10-27
verified-at: 2026-10-27
recheck: 180d — from the lane root run `(cd corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)` (eight files), re-fetch the seven pinned URLs above and compare with the pin table in `plans/pkg-spec-r46.json`, then re-run `python3 plans/polyglot_c_py_probe.py --lane .`; any capture digest, probe output or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `polyglot-c-py`

## Summary

`polyglot-c-py` asks for one source file, `/app/polyglot/main.py.c`, that is simultaneously valid Python 3
and valid C, and that prints the N-th Fibonacci number when run either way. Its grader is a **twelfth**
Terminal-Bench 2.0 exemplar in this lane and a grader class new to it: the graded artefact is an
**agent-authored source file executed by two toolchains at grading time**. One pytest function
(`test_fibonacci_polyglot`, `test_outputs.py:10`) scores the task and `tests/test.sh:25-28` turns its exit
status into a binary reward, so the whole score is three moves:

1. `polyglot_files = os.listdir("/app/polyglot")` then `assert polyglot_files == ["main.py.c"]`
   (`:17-18`) — an **exact list equality on the directory contents taken before any build**;
2. `subprocess.run(["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True)`
   (`:23-25`) — the grader compiles the graded file **into the directory it just asserted on**;
3. for each of three fixed points `(42, "267914296"), (10, "55"), (0, "0")` (`:27`), run
   `python3 /app/polyglot/main.py.c N` and `/app/polyglot/cmain N` with `check=True` and require
   `stdout.strip()` to equal the literal in both runtimes (`:31-46`).

Named against the lane's eleven executed exemplars, this is the **dual-runtime execution** class. The
closest neighbour is `circuit-fibsqrt` (round 41), which also compiles at grading time — but there the
compiled thing is the *task's own* simulator and the graded artefact is a data file (a gate list); here the
compiled thing **is** the graded artefact, and the same bytes must additionally run under a second language
runtime. The other ten are read-and-assert graders over text, JSON, git objects, an ICS file, an imported
module or a built binary's output; none of them executes the graded bytes as a program, and none of them
changes the graded directory in the middle of its own test. Every measured end state is recorded in the
receipt named by `plans/pkg-spec-r46.json` (`corpus/evidence/round46/polyglot-c-py-probe.txt`: `cases=18
observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`), first recorded after the stage-2
freeze `4fdeebaa` (QUALITY Q30); the sections below were drafted from the sources before that run and their
verdict cells filled from the receipt.

## Located quotes

Quotes are byte-exact from the round-46 captures (`corpus/evidence/round46/tb2-polyglot-c-py/`, identical to
the pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4` clause.
The package's registry rows, all tier A at that pin: S166 (`tests/test_outputs.py`), S167 (`tests/test.sh`),
S168 (`instruction.md`), S169 (`solution/solve.sh`), S170 (`environment/Dockerfile`), S171 (`task.toml`) and S172
(`README.md`); `.gitignore` is captured and pinned but carries no row.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| one file, named and located by the request | “Write me a single file in /app/polyglot/main.py.c which is a polyglot” | `instruction.md:1` |
| the Python invocation is a command line with N appended | “python3 /app/polyglot/main.py.c N” | `instruction.md:3` |
| the C invocation is a compile-then-run with the binary inside the graded directory | “gcc /app/polyglot/main.py.c -o /app/polyglot/cmain && /app/polyglot/cmain N” | `instruction.md:5` |
| both runtimes must print the Fibonacci value, and f(0)/f(1) are named | “Both of these should print to stdout the kth Fibonacci number, f(0) = 0, f(1) = 1, etc.” | `instruction.md:7` |
| the requester states a toolchain, not a constraint the grader checks | “I'm using python3 3.12.3 and gcc 13.2.0.” | `instruction.md:9` |
| the graded directory is listed before anything is built | “polyglot_files = os.listdir” | `test_outputs.py:17` |
| the listing assert is exact list equality against one name | “assert polyglot_files == [” | `test_outputs.py:18` |
| the same bytes are built by gcc, into the directory just asserted on | “"/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” | `test_outputs.py:24` |
| three fixed points, as literals in the test file | “test_cases = [(42,” | `test_outputs.py:27` |
| the Python leg is a subprocess the test runs itself | “["python3", "/app/polyglot/main.py.c", str(n)]” | `test_outputs.py:31` |
| only stdout is read, and it is stripped at both ends | “python_out = py_result.stdout.strip()” | `test_outputs.py:36` |
| both runtimes must match the same literal in one assertion | “assert python_out == expected and c_out == expected” | `test_outputs.py:44` |
| pytest itself runs under a 3.13 interpreter from uvx | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” | `test.sh:22` |
| reward 1 is written on pytest exit 0 | “echo 1 > /logs/verifier/reward.txt” | `test.sh:26` |
| internet is enabled in the environment | “allow_internet = true” | `task.toml:34` |
| the verifier timeout is 900 s | “timeout_sec = 900.0” | `task.toml:22` |
| the authors state the single-file requirement in their README | “Only `main.py.c` exists in `/app/polyglot/` (single file requirement)” | `README.md:21` |
| the authors publish the same three fixed points | “Test cases: f(0)=0, f(10)=55, f(42)=267914296” | `README.md:24` |
| the oracle writes its single file relative to the cwd | “cat <<'EOF' > polyglot/main.py.c” | `solve.sh:12` |
| gcc on ubuntu is the only tool the image installs | “RUN apt update -y && apt install -y gcc” | `Dockerfile:6` |

## Requirement map

Labels are **derived** from the receipt by the counter's `V7` rule: `enforced` iff every case whose `violates=` set
carries the tag is observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise. The
probe froze seven tags on five instruction lines; two of them (`both-print`, `toolchain`) are violated by no frozen
case, so no label can be derived for them — they are listed below as `not exercised`, and the counter's `V7` reports
them as a defect (round-46 lesson §Mistakes: the stage-2 pin never checked that every frozen tag has a violating case).

| Instruction line | Tag | Label | Receipt cases cited (violating) |
|---|---|---|---|
| `instruction.md:1` | `single-file` | partly | `nop`, `extra-file`, `leftover-cmain`, `regrade-same-state` |
| `instruction.md:3` | `python-run` | enforced | `c-only` |
| `instruction.md:5` | `c-build` | enforced | `python-only`, `dir-in-place` |
| instruction.md:7 | both-print | not exercised | no frozen case violates it |
| `instruction.md:7` | `fib-kth` | partly | `lookup-table`, `wrong-value`, `n-parsed-differently`, `empty-file` |
| `instruction.md:7` | `stdout-only` | enforced | `value-plus-line` |
| instruction.md:9 | toolchain | not exercised | no frozen case violates it |

- **1 (`single-file`, partly).** The listing at `test_outputs.py:17-18` is exact and taken once, before the build:
  a missing directory (`nop`), a second file (`extra-file`) or the binary `instruction.md:5` itself tells the agent to
  build (`leftover-cmain`) fail. `regrade-same-state` is the pass that makes the label `partly`: it is the oracle's
  state after one grading, so it violates the single-file rule only on its *second* grading, and its first grading
  passes (`regrade=DIFF:F`).
- **3 (`python-run`, enforced) and 5 (`c-build`, enforced).** Every `subprocess.run` carries `check=True`; a file
  valid in one language only dies at the other leg (`c-only` at the interpreter, `python-only` at gcc), and a
  directory named `main.py.c` passes the listing but not gcc (`dir-in-place`).
- **7 (`fib-kth`, partly).** "The kth Fibonacci number" is graded at exactly N in {42, 10, 0} (`:27`):
  `lookup-table`, which hardcodes the three literals, passes; `wrong-value`, `n-parsed-differently` and
  `empty-file` fail.
- **7 (`stdout-only`, enforced).** Only `stdout.strip()` is compared (`:36`, `:43`), so a second output line fails
  (`value-plus-line`) while symmetric padding (`trailing-ws`) and stderr (`stderr-noise`) pass — those two cases
  violate no tag and are recorded as the requirement's tolerances, not violations.
- **7 (`both-print`) and 9 (`toolchain`), not exercised.** No frozen case breaks only one runtime's print while
  keeping the other's, and no case changes the toolchain version: the probe uses the host's gcc and python3.

## Case table

The probe's 18 frozen cases, verdicts from the receipt. `Tests` is the single test function's letter
(`test_fibonacci_polyglot`); `Observed` is the receipt's verdict (each equals the frozen prediction:
`mismatches=0`).

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | F | fail | the image seed only: WORKDIR /app exists, /app/polyglot does not - os.listdir raises FileNotFoundError before any assert |
| `oracle-solve-sh` | P | pass | the task's published solution/solve.sh run verbatim with cwd /app (it creates polyglot/ relatively): a real polyglot whose Fibonacci loop both runtimes run |
| `lookup-table` | P | pass | a polyglot that hardcodes the three graded outputs, read out of the PUBLIC tests/test_outputs.py at recipe time and turned into a print table: the grader has exactly three fixed points and never inspects the source, so a lookup table is indistinguishable from computing |
| `python-only` | F | fail | valid Python that is not C (a plain import/def/raise program): python3 runs it, gcc fails with a parse error and check=True raises CalledProcessError |
| `c-only` | F | fail | valid C that is not Python (no # comment line, no Python expression): gcc builds it and it prints the right value, python3 aborts with a SyntaxError before the first expected value is compared |
| `extra-file` | F | fail | the oracle polyglot plus one unrelated file (NOTES.md) in /app/polyglot: the listing assert compares the whole list to ["main.py.c"], so a harmless extra file fails before gcc runs |
| `leftover-cmain` | F | fail | the oracle polyglot plus the binary that instruction.md:5 itself tells the agent to build (`gcc ... -o /app/polyglot/cmain && ./cmain N`): following the instruction leaves the second entry the grader's listing forbids - instruction and grader contradict each other |
| `wrong-value` | F | fail | a real polyglot whose f(42) is off by one (both runtimes print fib(n)+1 when N is 42): the value, not the shape, decides; the C loop also writes cmain, so the re-grade is what the listing sees |
| `trailing-ws` | P | pass | a correct polyglot that pads its output with leading and trailing spaces and blank lines in both runtimes: the grader compares stdout.strip(), which erases whitespace on both ends |
| `nonzero-exit` | F | fail | a correct polyglot that prints the right value and then exits non-zero (python sys.exit(3) / C return 3): the grader runs both runtimes with check=True, so a non-zero status fails a run whose stdout matched - the instruction never says the exit status must be 0 |
| `stderr-noise` | P | pass | a correct polyglot that also writes to stderr in both runtimes (python print(..., file=sys.stderr), C fprintf(stderr, ...)): the grader captures stderr and compares only stdout, so noise is invisible |
| `n-parsed-differently` | F | fail | a polyglot whose two sides read N differently - Python int(argv[1]), C the first digit only (argv[1][0]-'0') - so 42 and 10 disagree while 0 happens to match; no case proves both runtimes parsed N |
| `compile-warning` | P | pass | a correct polyglot carrying an explicit `#warning` line (a Python comment, a C preprocessing warning): gcc exits 0 with a diagnostic on stderr, and check=True only reads the exit status |
| `regrade-same-state` | P | pass | the oracle's end state, graded and then graded again: the first grade's own gcc writes /app/polyglot/cmain, so the same untouched state fails the second time - the grader is not idempotent (this row is the deliberate re-grade of oracle-solve-sh's state; the per-case `regrade` column is its measurement) |
| `empty-file` | F | fail | a zero-byte /app/polyglot/main.py.c: the listing passes, python3 prints nothing, and gcc links nothing with a main - both runtimes are wrong before any value is compared |
| `dir-in-place` | F | fail | a DIRECTORY at /app/polyglot/main.py.c: the listing is exactly ["main.py.c"] so the precondition passes, then gcc is handed a directory and check=True raises CalledProcessError |
| `crlf-source` | P | pass | a correct polyglot whose whole source uses CRLF line endings: CPython's tokenizer and gcc both accept CRLF, so the newline style of the source is invisible to this grader |
| `value-plus-line` | F | fail | a polyglot that prints the right value followed by a second line of output in both runtimes: strip() trims only the ends, so the compared string is two lines and no case fires the equality |

## Mechanism

One row per receipt case: the captured line that decides it and a verbatim fragment of that line.

| Case | Decisive line | “Quote” |
|---|---|---|
| `nop` | `test_outputs.py:17` | “polyglot_files = os.listdir("/app/polyglot")” |
| `oracle-solve-sh` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected, (” |
| `lookup-table` | `test_outputs.py:27` | “test_cases = [(42, "267914296"), (10, "55"), (0, "0")]” |
| `python-only` | `test_outputs.py:24` | “["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” |
| `c-only` | `test_outputs.py:30` | “py_result = subprocess.run(” |
| `extra-file` | `test_outputs.py:18` | “assert polyglot_files == ["main.py.c"], (” |
| `leftover-cmain` | `test_outputs.py:18` | “assert polyglot_files == ["main.py.c"], (” |
| `wrong-value` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected, (” |
| `trailing-ws` | `test_outputs.py:36` | “python_out = py_result.stdout.strip()” |
| `nonzero-exit` | `test_outputs.py:30` | “py_result = subprocess.run(” |
| `stderr-noise` | `test_outputs.py:36` | “python_out = py_result.stdout.strip()” |
| `n-parsed-differently` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected, (” |
| `compile-warning` | `test_outputs.py:24` | “["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” |
| `regrade-same-state` | `test_outputs.py:18` | “assert polyglot_files == ["main.py.c"], (” |
| `empty-file` | `test_outputs.py:24` | “["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” |
| `dir-in-place` | `test_outputs.py:24` | “["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” |
| `crlf-source` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected, (” |
| `value-plus-line` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected, (” |

## Findings, each tied to its receipt cases

1. **The graded directory is asserted before the grader mutates it, so the test is not idempotent (`regrade-same-state`
   P then F; every one of the 7 passing states fails a re-grade).** `:17-18` lists `/app/polyglot` and requires
   exactly `["main.py.c"]`; `:24` then compiles `-o /app/polyglot/cmain` into that directory. The receipt's
   `regrade cases=18 differ=7` is the measurement: each of the seven states that pass once (`oracle-solve-sh`,
   `lookup-table`, `trailing-ws`, `stderr-noise`, `compile-warning`, `regrade-same-state`, `crlf-source`) fails
   when graded a second time in the same tree (`regrade=DIFF:F`), while every failing state stays failing.
2. **The instruction's own command produces a failing state (`leftover-cmain` F).** `instruction.md:5` tells the
   agent to run `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain`; an agent that smoke-tests it and leaves the
   binary fails at `:18`.
3. **Three fixed points are not a Fibonacci definition (`lookup-table` P, `wrong-value` F, `n-parsed-differently` F).**
   `:27` pins `(42, "267914296"), (10, "55"), (0, "0")`; a polyglot that prints those three literals from a
   table passes, and the literals are public in the test file itself (`:27`) and in `README.md:24`, with
   `allow_internet = true` (`task.toml:34`).
4. **Each runtime must exit 0 as well as print (`nonzero-exit` F, `python-only` F, `c-only` F, `dir-in-place` F,
   `empty-file` F).** Every `subprocess.run` carries `check=True` (`:24`, `:34`, `:41`): a right value followed by a
   non-zero exit fails, a file valid in one language only fails at the other leg, and a directory named
   `main.py.c` passes the listing but not gcc.
5. **Only stripped stdout is compared (`trailing-ws` P, `stderr-noise` P, `value-plus-line` F).** `.strip()` at
   `:36`/`:43` trims the ends only, so padding and stderr are invisible and a second line is not.
6. **Toolchain tolerance (`compile-warning` P, `crlf-source` P).** A `#warning` leaves gcc's exit 0, and both
   CPython and gcc accept CRLF sources, so neither is a failure mode of this grader.
7. **The class is new to the lane: the graded bytes are executed, by two runtimes.** The other eleven exemplars
   decide from file contents, field values, git objects or a task-owned program's output; here the test builds
   and runs the agent's own source, and `circuit-fibsqrt` (round 41) — the closest neighbour — compiles the
   task's simulator, not the graded artefact.

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated, too easy, too hard or unsolvable
(no image run, no agent, no trajectory); that an agent would leave `cmain` behind (the `leftover-cmain`
case is a constructed end state); that the grader should hash the source, forbid a lookup table, check `f(1)`,
rebuild elsewhere or clean the directory (no such proposal is described or judged here); that the exact-list
assert is flaky (with exactly one expected element the comparison is order-free, and any two-element listing
fails regardless of order); or anything about how Harbor executes this verifier, retries it, or restores
`/app` between attempts.

Nor: **contamination** — `test_outputs.py:1-2`, `solve.sh:1` and `Dockerfile:1` carry the canary banner and
these captures exist for digest-pinned re-execution, not as a contamination measurement; **the image's
toolchain** — host `gcc` and `python3` stand in for the image's gcc 13.2.0 / python 3.12.3, and pytest is not
run (the harness reproduces the one test function's verdict); **`.gitignore`** — it is captured and pinned but
carries no SOURCES row: its 23 lines are repository boilerplate (`node_modules/`, `.env`, `dist.tar.gz`) with
no requirement attached, and no rule is read from it; **the oracle's correctness** — `solve.sh` runs as one
case's recipe and passes once, which says nothing about other images, other `gcc` versions or other points;
**prevalence** — one task, eighteen cases, no tracker sweep by this seat; **the instruction's intent** — whether
"a single file ... which is a polyglot" was meant to forbid a solution that leaves a build product next to it
is the authors' question, and the entry only records what the grader does.

**Falsifier.** This entry is falsified if (a) a re-fetch of the seven pinned URLs yields bytes whose SHA-256
differs from `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS`; (b) a fresh run of
`plans/polyglot_c_py_probe.py --lane .` prints a verdict other than the receipt's for any of the 18 cases, or a
`regrade` column other than the receipt's; (c) `test_outputs.py` is shown to list the directory after the gcc call,
to compare anything but stripped stdout, or to test any N other than 42, 10 and 0.

## Predictor

`predict(files, source) -> bool` is the counter's `V11` contract: `files` is `/app/polyglot`'s listing before
compilation, `source` the text of `main.py.c` (`None` when absent or not a regular file). True = the grader passes.
The grader executes the source, so no static reading is exact over arbitrary programs; this block reads the
polyglot shape the counter's held-out generator emits (a Python `emit(k)` table or recurrence and a C `printf`
body) and predicts the three fixed-point comparisons, the listing equality, the exit-status and stderr legs from
it. It was written by wave-1 seat `R46ExecC3Counter` (`v11-reference-predictor.py`) and is admitted here unchanged.

```python
import re

EXPECT = ((42, "267914296"), (10, "55"), (0, "0"))

def _py_values(text):
    head = text.split("if __name__ == ")[0]
    pairs = [(int(a), int(b)) for a, b in re.findall(r"if k == ([0-9]+):\n\s*return ([0-9]+)", head)]
    base = re.findall(r"\n    return ([0-9]+)", head)
    fallback = int(base[-1]) if base else None

    def get(k):
        for a, b in pairs:
            if a == k:
                return b
        return fallback

    return get

def _py_out(text, k, val):
    if "if __name__ == " not in text:
        return None
    call = text.split("if __name__ == ")[1]
    if "sys.stderr" in call:
        return None
    m = re.search(r'print\("([^"]*)" % emit\(k\)\)', call)
    if m:
        return m.group(1).replace("%d", str(val))
    if "emit(k)" in call:
        return str(val)
    return None

def _render(fmt, val):
    if "%llu" in fmt:
        out = fmt.replace("%llu", str(val))
    elif "%.1f" in fmt:
        out = fmt.replace("%.1f", str(val) + ".0")
    else:
        return None
    out = out.replace("\\n", "\n")
    return "\n".join(part.strip() for part in out.split("\n")).strip()

def _c_out(body, k):
    if "fprintf(stderr," in body:
        return None
    fb = re.search(r'else printf\("([^"]*)", (?:\(double\))?([0-9]+)', body)
    guarded = re.findall(r'if \(n == ([0-9]+)\)\s*printf\("([^"]*)", (?:\(double\))?([0-9]+)', body)
    if guarded:
        for g, fmt, val in guarded:
            if int(g) == k:
                return _render(fmt, int(val))
        return _render(fb.group(1), int(fb.group(2))) if fb else None
    seq = re.findall(r'printf\("([^"]*)", (?:\(double\))?([0-9]+)', body)
    if not seq:
        return None
    outs = [_render(f, int(v)) for f, v in seq]
    if None in outs:
        return None
    return "\n".join(outs)

def predict(files, source):
    if files != ["main.py.c"] or source is None:
        return False
    flat = source.replace("\r\n", "\n").replace("\r", "\n")
    if "def emit(k):" not in flat or "int main(" not in flat:
        return False
    values, body = _py_values(flat), flat.split("int main(")[1]
    for k, want in EXPECT:
        val = values(k)
        if val is None or _py_out(flat, k, val) != want:
            return False
        if _c_out(body, k) != want:
            return False
    return True
```

## Limits

- Host `gcc` and `python3` stand in for the image's gcc 13.2.0 / python 3.12.3 (`instruction.md:9`); pytest itself
  is not run — the probe reproduces the one test function's verdict, the only thing `tests/test.sh:25-28` rewards.
- The predictor reads the generator's polyglot template, not polyglots in general: it would mis-predict a valid
  polyglot of another shape. `V11` checks it against 60 fresh generated states per run and cannot refuse an
  open-coded reading of that template; non-author review of the block stays part of admission.
- Two frozen requirement tags (`both-print`, `toolchain`) are exercised by no case (see Requirement map), so the
  map's coverage of `instruction.md:7,9` is partial and the counter's `V7` reports it.
- No image was pulled and no agent ran; the non-idempotence finding is a property of the test, measured by
  grading the same tree twice, not an observation of Harbor's verifier.

## Errata (round 46, wave 2)

1. **Summary (`:35`) and Finding 7 overstate the class contrast.** "None of them executes the graded bytes as a
   program" is false for the round-43 exemplar `tb2-feal-differential-cryptanalysis-grader.md`, whose grader imports
   the agent-written Python module and calls its `attack` function. The narrower true statement: no earlier exemplar
   *compiles* the graded artefact or runs the same bytes under two language runtimes. Found by wave-2 seat
   `R46W2C3Entry` (`.ufo/waves/round-46/w2/R46W2C3Entry.md` finding 1).
2. **`instruction.md:7` names `f(1) = 1`, which no graded N and no frozen case exercises** (`R46W2C3Cases.md` defect
   1): the `fib-kth` row's `partly` label rests on N in {42, 10, 0} only.

