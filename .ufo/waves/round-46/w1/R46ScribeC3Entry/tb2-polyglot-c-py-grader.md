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
receipt named by `plans/pkg-spec-r46.json`; this entry is written before that receipt exists (QUALITY Q30),
so its case table carries `TBD` verdicts and the L1 fills them from the receipt after the stage-2 freeze.

## Located quotes

Quotes are byte-exact from the round-46 captures (`corpus/evidence/round46/tb2-polyglot-c-py/`, identical to
the pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4` clause.

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

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the
counter's `V7` applies, computed over **all** violating cases. Seven frozen tags on four instruction lines.

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:1` | `single-file` | enforced | `nop`, `empty-dir`, `extra-file`, `precompiled-cmain`, `dotfile`, `wrong-name`, `dir-at-source` |
| `instruction.md:1` | `path` | enforced | `nop`, `wrong-name` |
| `instruction.md:3` | `python-run` | enforced | `nop`, `empty-dir`, `c-only`, `exit-nonzero` |
| `instruction.md:5` | `c-compile` | enforced | `nop`, `empty-dir`, `dir-at-source`, `python-only` |
| `instruction.md:5` | `c-run` | enforced | `nop`, `empty-dir`, `c-only`, `exit-nonzero` |
| `instruction.md:7` | `stdout` | enforced | `extra-stdout` |
| `instruction.md:7` | `fib` | partly | `fib-wrong`, `lookup-print` |

**Draft status of the label column.** Those seven labels are the draft's *predictions* from the frozen case
set below, not receipt-derived values: no graded case of this task has run in this round (QUALITY Q30). The
L1 MUST recompute each label from the receipt with the `V7` rule at stage 2 and change any cell that
disagrees; `fib` is the cell most likely to move, because it is the only one whose case set contains a
predicted pass (`lookup-print`).

The per-line reading (the package's SOURCES rows are S166, S167, S168, S169, S170, S171 and S172, all tier A):

- **1 (`single-file`, `path`, both `enforced`).** The pre-build listing is the only structural gate, and it is
  exact: a second file of any kind (`extra-file`, `precompiled-cmain`, `dotfile`) or a different name
  (`wrong-name`) fails before anything is compiled or executed. It is an exact **list** equality, so the
  check is on the set of names, taken once, before the test itself writes `cmain` there. `dir-at-source` is
  the edge the equality does not see: a *directory* named `main.py.c` satisfies `== ["main.py.c"]`, and only
  the `gcc` call at `:24` rejects it.
- **3, 5 (`python-run`, `c-compile`, `c-run`, all `enforced`).** Each graded point is run twice with
  `check=True`, so a non-zero exit in either runtime fails the test even when the printed value is right
  (`exit-nonzero`), and a file that is valid in one language only dies at the other leg (`python-only` at the
  compile, `c-only` at the interpreter). The instruction's own second command is the compile leg — the test
  re-runs it rather than reading a binary the agent left behind.
- **7 (`stdout`, `enforced`).** `stdout` is the only channel read and it is `.strip()`ped at both ends
  (`:36`, `:43`), so surrounding whitespace is forgiven (`padded-stdout`) while a second line is not
  (`extra-stdout`): `strip()` removes leading and trailing whitespace only, never an interior newline. stderr
  is captured and never compared (`stderr-noise`).
- **7 (`fib`, `partly`).** "The kth Fibonacci number" is graded at exactly three points; `f(1)`, named in the
  instruction, is never exercised, and no other N is. A polyglot that carries a table of the three expected
  literals and prints anything for every other N passes (`lookup-print`), so the requirement holds at the
  three points and nowhere else. The label is `partly` rather than `unenforced` because a wrong-value polyglot
  does fail (`fib-wrong`).
- **9 (no tag).** The toolchain sentence is not a graded requirement: the test calls bare `python3` and `gcc`
  and never reads a version. `environment/Dockerfile:2-6` fixes neither version explicitly — it takes
  Ubuntu 24.04's defaults (which are the two versions named) and `task.toml:29` pins the tag
  `alexgshaw/polyglot-c-py:20251031`. `tests/test.sh:19` runs pytest under a *different* interpreter
  (`-p 3.13`) from the one the test invokes.

## Case table

The frozen case set: sixteen end states. `Tests` is the captured test's single letter (`test_fibonacci_polyglot`); the file carries one test function,
so no end state reaches a second test and no `-` appears. `Observed` is `TBD` for every row — no graded case of this task has been executed in this
round (QUALITY Q30); the L1 fills each cell from `corpus/evidence/round46/polyglot-c-py-probe.txt` after the
stage-2 freeze and must then make this table byte-equal to the receipt's `CASE` lines (`V9`). The `Tests`
letter is the probe's *prediction* and is the value the receipt is expected to confirm.

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | F | TBD | `/app/polyglot` does not exist — `os.listdir` raises `FileNotFoundError` before any assert |
| `empty-dir` | F | TBD | `/app/polyglot` exists and is empty: `[] != ["main.py.c"]` |
| `oracle-solve-sh` | P | TBD | the task's own `solve.sh` heredoc, run from `/app`: one polyglot file, nothing else in the directory |
| `extra-file` | F | TBD | the oracle source plus an unrelated `notes.txt` in the same directory |
| `precompiled-cmain` | F | TBD | the oracle source plus the `cmain` binary left by the agent's own smoke test of `instruction.md:5` |
| `dotfile` | F | TBD | the oracle source plus `.main.py.c.swp` — `os.listdir` returns dotfiles |
| `wrong-name` | F | TBD | the correct source saved as `main.py`; the directory holds exactly one, wrongly named, entry |
| `dir-at-source` | F | TBD | a *directory* named `main.py.c` containing the real source: the listing equality passes, `gcc` on a directory fails |
| `python-only` | F | TBD | a valid Python Fibonacci program with no C part: the Python leg would pass, the gcc build fails |
| `c-only` | F | TBD | a valid C Fibonacci program with no Python part: the gcc build passes, `python3` fails to parse it |
| `lookup-print` | P | TBD | a valid polyglot that prints 267914296 / 55 / 0 from a table keyed on argv and anything else for any other N |
| `stderr-noise` | P | TBD | the oracle source plus a diagnostic banner on stderr in both runtimes |
| `exit-nonzero` | F | TBD | the oracle source printing the right value and then exiting 1 in both runtimes (`check=True`) |
| `extra-stdout` | F | TBD | the oracle source printing the right value and one further line in both runtimes |
| `padded-stdout` | P | TBD | the oracle source printing the value padded with leading and trailing spaces |
| `fib-wrong` | F | TBD | a valid polyglot whose recurrence is broken (prints N instead of f(N)) in both runtimes |

## Mechanism

One row per frozen case, with the captured line that decides it and a verbatim fragment of that line. These
are the draft's predicted decisive lines; `V10` compares them with the receipt's cases and the L1 corrects any
row the receipt contradicts. The Findings section says, case by case, why that line decides it.

| Case | Decisive line | “Quote” |
|---|---|---|
| `nop` | `test_outputs.py:17` | “polyglot_files = os.listdir” |
| `empty-dir` | `test_outputs.py:18` | “assert polyglot_files == [” |
| `oracle-solve-sh` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected” |
| `extra-file` | `test_outputs.py:18` | “assert polyglot_files == [” |
| `precompiled-cmain` | `test_outputs.py:18` | “assert polyglot_files == [” |
| `dotfile` | `test_outputs.py:18` | “assert polyglot_files == [” |
| `wrong-name` | `test_outputs.py:18` | “assert polyglot_files == [” |
| `dir-at-source` | `test_outputs.py:24` | “"/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” |
| `python-only` | `test_outputs.py:24` | “"/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True” |
| `c-only` | `test_outputs.py:31` | “["python3", "/app/polyglot/main.py.c", str(n)]” |
| `lookup-print` | `test_outputs.py:27` | “test_cases = [(42,” |
| `stderr-noise` | `test_outputs.py:36` | “python_out = py_result.stdout.strip()” |
| `exit-nonzero` | `test_outputs.py:31` | “["python3", "/app/polyglot/main.py.c", str(n)]” |
| `extra-stdout` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected” |
| `padded-stdout` | `test_outputs.py:36` | “python_out = py_result.stdout.strip()” |
| `fib-wrong` | `test_outputs.py:44` | “assert python_out == expected and c_out == expected” |

## Findings

1. **The graded directory is asserted before the grader mutates it (`nop`, `empty-dir`, `extra-file`,
   `precompiled-cmain`, `dotfile`, `wrong-name`; `F`).** `:17` lists `/app/polyglot` once and `:18` compares
   the result to a one-element list. Any other entry — a stray note, a dotfile, or a build product — fails the
   test before a compiler runs, and a missing directory fails at `:17` itself with `FileNotFoundError`
   rather than at an assertion.
2. **The instruction's own command produces the state that fails (`precompiled-cmain` `F`).**
   `instruction.md:5` tells the agent to run `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain`. That writes
   `cmain` into the directory whose listing is asserted, so an agent that smoke-tests the published command
   exactly as written and leaves the binary behind fails the grader — the same shape as round 45's
   `under-varsea` (the oracle's own advice landing one directory off). The passing state requires either a
   build outside `/app/polyglot` or a cleanup step the instruction never mentions.
3. **The listing check does not distinguish a directory from a file (`dir-at-source` `F`).**
   `os.listdir` returns bare names, so `["main.py.c"]` is satisfied by a directory of that name containing the
   real source; the only thing that rejects it is the `check=True` `gcc` call at `:24`. The check is
   "no other *name*", never "a readable file".
4. **The test is not idempotent (`oracle-solve-sh` passes once; a second run fails).** `:24` compiles `-o
   /app/polyglot/cmain` into the directory that `:18` asserted one statement earlier. The first invocation in
   a fresh container sees the listed state and passes; any re-grade in the same container re-reads the
   directory with `cmain` present and dies at `:18`. Nothing in `tests/test.sh` re-creates `/app/polyglot`, so
   the harness's single pytest run is what makes the task gradable at all.
5. **Both runtimes must clear their exit status as well as their output (`exit-nonzero`, `python-only`,
   `c-only`; `F`).** Every `subprocess.run` carries `check=True` (`:24`, `:34`, `:41`), so a correct print
   followed by `exit 1` fails, and a source that is valid in one language only fails at the other leg. The
   grader reads *both* toolchains from the same bytes: there is no partial credit and no per-runtime score.
6. **Only stdout is compared, and it is stripped (`stderr-noise` `P`, `padded-stdout` `P`, `extra-stdout`
   `F`).** `capture_output=True` collects both streams but only `.stdout.strip()` reaches the assertion
   (`:36`, `:43`), so stderr noise and symmetric padding are invisible, while a second output line is not —
   `strip()` trims the ends of the whole string, never an interior newline.
7. **Three fixed points are not a Fibonacci definition (`lookup-print` `P`, `fib-wrong` `F`).** `:27` pins
   `(42, "267914296"), (10, "55"), (0, "0")` and `:29` iterates exactly those. A polyglot carrying a table of
   three literals passes while printing anything for every other N, so `f(1)` — which the instruction names
   explicitly — is never exercised, and the instruction's recurrence is enforced only at three points. The
   three literals are also published in the test file and in `README.md:24`, and `task.toml:34` allows
   internet, so the expected outputs are readable without computing anything.
8. **The class is new because execution, not reading, is the predicate.** The ten read-and-assert exemplars
   decide from file contents, field values, git objects or program output collected by the test; here the test
   *builds and runs* the graded artefact, and the same bytes must survive a second language runtime. And
   unlike `circuit-fibsqrt` (which compiles the task's own simulator and reads a data file), the compiled
   object here is the agent's own source — so the compile leg is itself a graded requirement (`c-compile`),
   not instrumentation.

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated, too easy, too hard or unsolvable
(no image run, no agent, no trajectory); that an agent would leave `cmain` behind (the `precompiled-cmain`
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
**prevalence** — one task, sixteen cases, no tracker sweep by this seat; **the instruction's intent** — whether
"a single file ... which is a polyglot" was meant to forbid a solution that leaves a build product next to it
is the authors' question, and the entry only records what the grader does.

**Falsifier.** This entry is falsified if (a) a re-fetch of the seven pinned URLs yields bytes whose SHA-256
differs from `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS` and the pins in
`plans/pkg-spec-r46.json`; (b) a fresh run of `plans/polyglot_c_py_probe.py --lane .` prints a case verdict
other than the `Tests` letters in the case table above — in particular if `oracle-solve-sh`, `lookup-print`,
`stderr-noise` or `padded-stdout` is observed `fail`, or if `nop`, `empty-dir`, `extra-file`,
`precompiled-cmain`, `dotfile`, `wrong-name`, `dir-at-source`, `python-only`, `c-only`, `exit-nonzero`,
`extra-stdout` or `fib-wrong` is observed `pass`; (c) `test_outputs.py` is shown to assert the directory
listing by anything other than `== ["main.py.c"]` at `:18`, to build with anything other than `gcc` into
`/app/polyglot/cmain` at `:24`, or to compare anything other than stripped stdout against
`[(42, "267914296"), (10, "55"), (0, "0")]` at `:27`; (d) `tests/test.sh` is shown to compute the reward from
anything other than the pytest exit status; (e) `task.toml` is shown to have `allow_internet = false` at the
pinned commit; or (f) the pre-build listing assert at `:18` is shown to fire *after* the `gcc` call at `:24`
in this capture, which would remove the `precompiled-cmain` finding.

## Predictor

The grader's rule, as far as one source file's text decides it: the graded state is the **directory listing
taken before any build** plus the **bytes of the single file**, and the verdict is `pass` iff the listing is
exactly one entry named `main.py.c` and those bytes are both a Python 3 program and a C translation unit of
the canonical overlapping shape. `listing` is the sequence `os.listdir("/app/polyglot")` returns at test
entry, or `None` when the directory is absent; `source` is the text of `/app/polyglot/main.py.c`, or `None`
when it cannot be read. True = the grader passes that end state.

```python
def predict(listing, source):
    if listing is None or source is None:
        return False
    names = list(listing)
    if len(names) != 1 or names[0] != "main.py.c":
        return False
    text = source.replace("\r\n", "\n")
    if "\r" in text or not text.strip():
        return False
    if "#include" not in text or "int main(" not in text or "printf(" not in text:
        return False
    if "def " not in text or "argv" not in text:
        return False
    return True
```

Three things the block decides and one it does not. It decides the listing leg exactly (`len != 1` or a
different name is a fail, and an absent directory is a fail); the "second language runtime" leg as a
structural question — a bundle that lacks a C-visible entry point and a `printf` cannot compile, and one that
lacks a Python-visible `def` and an argument read cannot run under `python3`; and the newline encoding: a
source whose only terminators are bare carriage returns is a single logical line to the C preprocessor, so it
is predicted `fail` rather than assumed equivalent to `\r\n` (which both runtimes accept, and which is
normalised away before the substring checks). It does **not** decide arithmetic: a valid polyglot that
computes the wrong value is predicted `pass` and graded `fail`. That state is outside this predictor's
declared domain and is carried by the case table (`fib-wrong`, `lookup-print`) instead.

## Limits

- Host `gcc` and `python3` stand in for the image's gcc 13.2.0 / python 3.12.3; pytest itself is not run —
  the harness reproduces the one test function's verdict, the only thing `tests/test.sh:25-28` rewards.
- The predictor's domain is `(listing x polyglot-or-not)`: three predicted-pass sources may differ only in
  whitespace, newline encoding and stderr noise, not in arithmetic. The held-out states must be drawn from
  that domain; a semantic mutant in the held-out set is a counter defect, not a predictor defect.
- `V11` cannot refuse an open-coded two-branch decision that reproduces the grader's verdict on the drawn
  states without performing the reading; non-author review of the admitted block stays part of admission (the
  same limit round-45's entry names for its own `V11`).
- The `lookup-print` and `fib-wrong` constructions are described, not yet built: their verdicts become facts
  only in the probe receipt.
- `plans/pkg_gate.py` runs at its round-45 digest against this package; re-running the verifier twice in one
  container is not attempted here, so finding 4 is read off `:18` vs `:24` and not executed.
