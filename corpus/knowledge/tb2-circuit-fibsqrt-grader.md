source: S125 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/test_outputs.py — the three pytest functions that are this task's whole score, lines 1-147, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S126 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/instruction.md — the request the grader is mapped against, lines 1-13, same commit, accessed 2026-10-26
source: S127 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/sim.c — the simulator the grader compiles at grading time and that executes the agent's gate list, lines 1-353, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round42/tb2-circuit-fibsqrt && sha256sum -c SHA256SUMS)` (green as written), re-fetch the three pinned URLs and compare with the pin table in `plans/pkg-spec-r42.json`, then re-run `python3 plans/fibsqrt_probe.py --lane .`; any capture digest, PROBE output or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `circuit-fibsqrt`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `circuit-fibsqrt` task is scored by **three** pytest functions in
`tests/test_outputs.py` — `test_gates_file_exists` (`:7-11`), `test_gates_file_size` (`:14-23`) and `test_sqrt_fib`
(`:56-147`) — and the reward is one bit from the pytest exit status (`test.sh:25-29`). The agent never submits code:
the graded artefact is a **data file**, `/app/gates.txt`, a list of gate assignments, and the verdict comes from a
**simulator the grader compiles itself** at grading time (`gcc -O3 /tests/sim.c -o sim`, `test_outputs.py:66`) and
then runs as `/app/sim N` for 28 fixed `N` (`:73-102`, `:119`), comparing stdout with `fibonacci(isqrt(N)) % 2**32`
(`:115-116`, `:134`). The largest graded input is 48401 = 220²+1. The task's own instruction calls the gate file
`<32,000` lines and names 208 and 20000 as examples (`instruction.md:11-13`); neither example is in the graded table.

On the 16 frozen end states of this round's probe, the grader reproduced the frozen prediction on all 16
(`cases=16 observed_pass=7 observed_fail=9 mismatches=0`) and graded every end state a second time with no
difference (`regrade cases=16 differ=0`). Four results organise the rest of this entry.

(1) **A 1195-line lookup table for exactly the 28 graded inputs scores 3 of 3 (`lookup-28`, `PPP`)** and prints 0 for
the instruction's own examples 208 and 20000 — it carries `violates=example-208,example-20000` and is observed
`pass`. Adding both examples back (`lookup-28-plus-examples`, `PPP`) also passes and still violates
`output-function`: the score distinguishes a table of answers from *the function* in no way at all.

(2) **The line budget is counted on lines, not gates.** Blank-line padding to 31999 lines passes 3 of 3
(`lookup-28-padded-31999`, `PPP`); padding to 32000 fails **only** the size test (`lookup-28-padded-32000`, `PFP`),
because the simulator skips every line that does not scan as a gate (`sim.c:113-114`) while `test_outputs.py:21`
sums every line of the file.

(3) **The file's line order is not graded, and "the last 32 lines" is not what is printed.** Reversing every line
(`lookup-28-reversed-lines`, `PPP`) and interleaving `# note` lines (`lookup-28-comment-lines`, `PPP`) both pass:
`sim.c` tracks the highest signal index it has seen (`:117-118`) and prints the 32 highest-**indexed** signals
(`:340-347`), so `instruction.md:9`'s "the last 32 lines" describes an intended layout the grader does not check.

(4) **One trailing space per line is fatal, CRLF is free.** `lookup-28-trailing-space` is `PPF` — the copy branch
requires a space-free right-hand side (`sim.c:126-127`), so a spaced copy line is silently dropped instead of
rejected; `lookup-28-crlf` is `PPP`. Two further measured facts that cut the other way: the grader's own compile
overwrites an agent-planted `/app/sim` (`fake-sim-script`, `PPF`), and a directory in place of the gate file is an
uncaught `IsADirectoryError` inside the size test (`gates-is-directory`, `PFF`).

This entry extends the lane's executed TB2 grader sample (`tb2-constraints-scheduling-grader.md`,
`tb2-protein-assembly-grader.md`, `tb2-regex-log-grader.md`, `tb2-git-webserver-grader.md`,
`tb2-build-pmars-grader.md`, `tb2-git-leak-recovery-grader.md`, `tb2-db-wal-recovery-grader.md`). The edge class it
adds is **not** a new verdict channel: existence, a line count and per-value equality are old. What is new to the
sample is that the graded artefact is not read by the grader at all — it is **executed** by a C program the grader
compiles from its own read-only copy, so the semantics that decide the verdict are a 353-line simulator
(`sim.c`) plus a 28-row table, and the passing condition is a property of that simulator's parse, not of the
instruction's description of the format. It **narrows** the `corpus/README.md` §Frontier "Terminal-Bench 2.0's"
clause for this one task only; the clause stays open for the remaining TB2 task graders (8 of 89 read at
`2fd12b88`).

## Source labels

S125 and S127 are the benchmark maintainers' own scoring code: primary for *what this grader checks* and for the
simulator's parse and print semantics. S126 is the maintainers' own request and is primary only for *what is asked*;
every claim about what is graded is drawn from S125/S127, never from S126, and the map below records exactly where
the two disagree. `task.toml` (captured, not a registry row) is the authors' metadata: `difficulty = "hard"`
(`:15`), `expert_time_estimate_min = 960.0` (`:18`), `junior_time_estimate_min = 2400.0` (`:19`), the verifier and
agent timeouts of 3600 s (`:22`, `:25`), `docker_image = "alexgshaw/circuit-fibsqrt:20251031"` (`:29`) and
`allow_internet = true` (`:34`) — read only, never exercised. `test.sh` and `Dockerfile` are captures of the
harness: `Dockerfile:3` is `WORKDIR /app`, `Dockerfile:9-10` copy `tests/sim.c` and the example `gates.txt` into
`/app`, and `test.sh:18-29` is the reward mapping. The captured `gates.txt` is the shipped example circuit (33 lines:
`out0 = out0` … `out31 = out31` then `out32 = 0`); it prints `N/2`, which is what `instruction.md:10` says it does,
and it is the seeded state of the `nop` case. The captured `solve.sh` is the task oracle, **own reading, tier C** —
not a registry row: it runs as the `oracle-solve-sh` case's recipe inside the sandbox and no finding rests on its
logic. The `README.md` capture is the task's own prose, read once for its example claims, not a row. The probe
receipt (`corpus/evidence/round42/fibsqrt-probe.txt`) is the lane's own re-runnable gate output, tier A for its own
scope: these 16 end states against these captures, under host `python3`, host `/usr/bin/gcc` and the captured
grader.

Disclosure: the 16 case predictions and their `violates=` tags were written from a static reading of
`tests/test_outputs.py`, `tests/sim.c` and `instruction.md` **before the first recorded run** and frozen in
`corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt` (digest pinned in `plans/pkg-spec-r42.json`). Three of the
16 (`nop`, `oracle-solve-sh`, `lookup-28`) had been graded on this host by the round-41 planning seat
(`.ufo/waves/round-41/build/R41PlanNext.md` §3.2: nop 2/3, oracle 3/3, a 28-value lookup 3/3); those three
re-observe prior results and the other 13 were never graded before the freeze. Every case carries
`predicted_tests=` and `predicted=`; no prediction was edited after the run, and none needed to be.

## What is graded (static reading of test_outputs.py AND sim.c)

| Step | Mechanism | Lines |
|---|---|---|
| Entry point | `uvx -p 3.13` + `pytest==8.4.1` + `pytest-json-ctrf==0.3.5` over `/tests/test_outputs.py`; all three functions are collected in file order | `test.sh:18-22` |
| Reward | the shell maps the pytest exit status to `/logs/verifier/reward.txt`: `1` on 0, `0` otherwise — one bit, no partial credit | `test.sh:25-29` |
| Initial state | `WORKDIR /app`; `COPY tests/sim.c /app` and `COPY gates.txt /app` seed the simulator source and the 33-line example circuit; no `sim` binary and no grading state exists yet | `Dockerfile:3`, `:9-10` |
| Existence | `Path("/app/gates.txt").exists()` — an absolute path, independent of the cwd | `test_outputs.py:9-11` |
| Size | `open(gate_path, 'r')` then `sum(1 for line in f)`; assert `line_count < 32000` — every line counts, blank or not | `test_outputs.py:20-23` |
| Value | `subprocess.run(["gcc", "-O3", "/tests/sim.c", "-o", "sim"])` in the cwd; then, per value, `subprocess.run(["/app/sim", str(n)])` and `int(stdout.strip())` compared with `fibonacci(isqrt(n)) % 2**32`; `all_passed` must stay true | `test_outputs.py:65-70`, `:113-137`, `:147` |
| Table | 28 values: 1, 4, 8, 12, 41, 42, 107, 220, 209, 366, then x², x²−1, x²+1 for x in 12, 41, 42, 107, 220, 209; maximum 48401 | `test_outputs.py:73-102` |
| Simulator load | `parse_gates("gates.txt")` — a bare relative name, resolved against the process cwd, which the harness fixes at `/app` | `sim.c:101`, `:319` |
| Simulator parse | per line `sscanf(line, "out%d = %[^\n]", &out_idx, op)`; a line that does not yield two fields is `continue`d; `num_signals = out_idx + 1` whenever the index is higher | `sim.c:108-119` |
| Gate forms | exact `0` / `1`; `outN` with no space anywhere (copy); `~outN` (NOT); `outA <&,|,^> outB` parsed by `sscanf(op, "out%d %c out%d", …)` and dropped if that fails — there is no final `else` and no error | `sim.c:122-182` |
| Input | signals 0-31 are seeded from `argv[1]` with `strtoul`; stdin is never read; seed loop is bounded by `i < 32 && i < num_signals` | `sim.c:322-331` |
| Run | 32000 fixed steps of an event-driven simulation over a heap of indices; a dependent is re-queued when its source changes | `sim.c:212-303`, `:335-338` |
| Print | if `num_signals >= 32`, bit `i` of the result is `values[num_signals - 32 + i]`, printed as one unsigned decimal line | `sim.c:340-347` |

Five structural consequences follow from the reading alone:

- **The graded set is 28 points, not a function.** Nothing in the three tests evaluates the circuit at an `N` outside
  the frozen table, and nothing compares it with the instruction's examples. `lookup-28` is the measurement.
- **The size bound and the simulator's capacity are different numbers.** `test_outputs.py:23` bounds *lines* at 31999;
  `sim.c:5` bounds *signals* at `MAX_SIGNALS 32000`, and the parse writes `gates[out_idx]` without checking
  `out_idx < MAX_SIGNALS` (`sim.c:117-118`), so a line naming a signal at or above 32000 is an out-of-bounds write
  in the grader's own process. No receipt case exercises that shape; it is a code reading, not a measurement.
- **"Last 32 lines" is never computed.** `num_signals` is the highest index *mentioned*, not a line count, and blank,
  comment and unparsable lines never move it. Reversed and comment-interleaved files are `PPP`.
- **The value channel is `/app/sim`, the compile channel is `./sim`.** The two names coincide only because the
  harness cwd is `/app`; the compile is what makes the graded binary the grader's, not the agent's.
- **`strcmp`/`strstr` on the raw `op` slice makes whitespace significant.** `%[^\n]` keeps everything after the
  first ` = ` to the end of the line, including trailing spaces and a CR, so the exact-match forms (`0`, `1`) and the
  space-free copy test are both sensitive to bytes the instruction never mentions.

## Located quotes

Quotes are byte-exact from the round-42 captures (`corpus/evidence/round42/tb2-circuit-fibsqrt/`, identical to the
pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4` clause. Straight
double quotes inside a quote are the file's bytes.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the graded artefact is a line-per-gate data file | “each line of the file /app/gates.txt should contain a line of the form” | `instruction.md:1` |
| the request says the inputs arrive on stdin | “Initially, the first 32 lines are defined by the binary representation of stdin.” | `instruction.md:8` |
| the request says the file's last 32 lines are the outputs | “After 32000 steps, the last 32 lines are converted to an integer and printed to stdout.” | `instruction.md:9` |
| the line bound is part of the request | “Create a /app/gates.txt file with <32,000 lines” | `instruction.md:11` |
| the request's own example is a value the grader never runs | “As an example, running /app/sim 208 should output 377” | `instruction.md:12` |
| existence is an absolute-path assertion | “assert gate_path.exists(), f"File {gate_path} does not exist"” | `test_outputs.py:11` |
| the size test counts every line of the file | “line_count = sum(1 for line in f)” | `test_outputs.py:21` |
| the bound is strict and counted over all lines | “assert line_count < 32000, f"gates.txt has {line_count} lines, but must have fewer than 32,000 lines"” | `test_outputs.py:23` |
| the grader compiles its own simulator into the cwd | “["gcc", "-O3", "/tests/sim.c", "-o", "sim"], capture_output=True, text=True” | `test_outputs.py:66` |
| the expected value is fib of the integer square root | “fib_n = fibonacci(isqrt(n))” | `test_outputs.py:115` |
| the modulus is applied by the grader, not by the circuit | “fib_n_mod = fib_n % (2**32)  # Take modulo 2^32” | `test_outputs.py:116` |
| the graded channel is an absolute /app/sim invocation per value | “result = subprocess.run(["/app/sim", str(n)], capture_output=True, text=True)” | `test_outputs.py:119` |
| the verdict is one all-or-nothing boolean | “print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")” | `test_outputs.py:145` |
| the simulator's signal table is a compile-time bound | “#define MAX_SIGNALS 32000” | `sim.c:5` |
| the gate list is opened by a bare name, so the cwd decides which file | “FILE *f = fopen(filename, "r");” | `sim.c:101` |
| an unparsable line is skipped, never an error | “if (sscanf(line, "out%d = %[^\n]", &out_idx, op) != 2) {” | `sim.c:113` |
| the signal count is the highest index seen, not the line count | “num_signals = out_idx + 1;” | `sim.c:118` |
| a copy line is one whose right-hand side has no space | “} else if (strncmp(op, "out", 3) == 0 && !strstr(op, " ")) {” | `sim.c:126` |
| the copy branch states its own space rule | “// Copy operation (no spaces means simple copy)” | `sim.c:127` |
| binary gates are parsed by sscanf and silently dropped when it fails | “if (sscanf(op, "out%d %c out%d", &src1, &op_char, &src2) == 3) {” | `sim.c:156` |
| the input integer comes from argv, never stdin | “input_value = (unsigned int)strtoul(argv[1], NULL, 0);” | `sim.c:324` |
| only the first 32 signals are seeded from the input | “for (int i = 0; i < 32 && i < num_signals; i++) {” | `sim.c:329` |
| the simulation is a fixed 32000-step loop | “for (int step = 0; step < 32000; step++) {  // Full simulation” | `sim.c:335` |
| the printed value is the 32-signal window ending at the highest index | “if (values[num_signals - 32 + i]) {” | `sim.c:343` |

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the round-42
counter `V7` applies, computed over **all** violating cases and not from one convenient witness. The frozen table
carries seven tags on five instruction lines; every tag has at least one violating case. Two tags are single-witness
(`line-form`, `last-32-lines`) and both are `unenforced`; two are `enforced` (`gates-file`, twice-witnessed;
`line-limit`, single-witness); three are wide and `partly` (`output-function` 15 cases, `example-208` and
`example-20000` 14 cases each).

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:1` | `line-form` | unenforced | `lookup-28-comment-lines` |
| `instruction.md:9` | `last-32-lines` | unenforced | `lookup-28-reversed-lines` |
| `instruction.md:11` | `gates-file` | enforced | `no-gates-file`, `gates-is-directory` |
| `instruction.md:11` | `line-limit` | enforced | `lookup-28-padded-32000` |
| `instruction.md:11` | `output-function` | partly | `nop`, `no-gates-file`, `empty-gates-file`, `lookup-28`, `lookup-27-drop-48401`, `lookup-28-plus-examples`, `lookup-28-bitflip-41`, `lookup-28-padded-31999`, `lookup-28-padded-32000`, `lookup-28-comment-lines`, `lookup-28-reversed-lines`, `lookup-28-crlf`, `lookup-28-trailing-space`, `fake-sim-script`, `gates-is-directory` |
| `instruction.md:12` | `example-208` | partly | `nop`, `no-gates-file`, `empty-gates-file`, `lookup-28`, `lookup-27-drop-48401`, `lookup-28-bitflip-41`, `lookup-28-padded-31999`, `lookup-28-padded-32000`, `lookup-28-comment-lines`, `lookup-28-reversed-lines`, `lookup-28-crlf`, `lookup-28-trailing-space`, `fake-sim-script`, `gates-is-directory` |
| `instruction.md:13` | `example-20000` | partly | `nop`, `no-gates-file`, `empty-gates-file`, `lookup-28`, `lookup-27-drop-48401`, `lookup-28-bitflip-41`, `lookup-28-padded-31999`, `lookup-28-padded-32000`, `lookup-28-comment-lines`, `lookup-28-reversed-lines`, `lookup-28-crlf`, `lookup-28-trailing-space`, `fake-sim-script`, `gates-is-directory` |

Two tags are enforced and five are not. The per-line reading:

- **1 (`line-form`, `unenforced`).** The request says each line "should contain a line of the form" of the seven gate
  shapes, and every gate line of `lookup-28` is preceded by a `# note` line that is none of them; the case is `PPP`.
  The simulator skips the comment lines (`sim.c:113-114`), so the request's line-form sentence is a style rule the
  grader cannot see. This is the only tag on `instruction.md:1`, and it is the receipt's cleanest
  requirement/assertion divergence on the format axis.
- **9 (`last-32-lines`, `unenforced`).** The only violating case is the reversed file and it passes, because the print
  window is indexed off `num_signals` (`sim.c:343`) rather than off the file's tail. The tag is honest — a reversed
  file really does violate "the last 32 lines are converted" — and the label records that the grader does not
  implement the sentence.
- **11 (`gates-file`, `enforced`).** Both violating cases fail: removing the file fails all three tests; a directory
  in its place passes the existence test and raises inside the size test. The tag covers the existence/readability
  requirement and is the one requirement whose failure is total.
- **11 (`line-limit`, `enforced`).** The single witness is the 32000-line pad, which fails exactly the size test
  (`PFP`). Note what the label does **not** say: the limit is enforced on lines, and blank lines are counted, so the
  sentence "fewer than 32,000 lines" is enforced literally while the gate budget it appears to express is not
  enforced at all.
- **11/12/13 (`output-function`, `example-208`, `example-20000`, all `partly`).** All three tags carry passing
  violators, and the passing violators are the same family: any lookup-table circuit violates "outputs
  fib(isqrt(N))" and each named example while passing 3 of 3. The label `partly` is exactly right — the grader tests
  28 points, so these sentences are enforced at 28 points and unenforced everywhere else. `lookup-28-plus-examples`
  is the sharpest instance: it stops violating the two example sentences (it answers 208 and 20000 correctly) and
  still violates `output-function`, and it passes. So the difference between "the two examples" and "the function" is
  one tag, visible only in the frozen table, with no verdict difference.

`instruction.md:8` (stdin) and `instruction.md:10` (the example prints `argv[1]/2`) carry **no** frozen tag and
therefore no row. Neither is a requirement the agent must satisfy, and the receipt's `oracle-solve-sh` (`PPP`) shows
the task's own solution uses the argv channel; the stdin sentence is simply wrong about the graded interface
(finding 10).

### Contestable tags

The `violates=` tags are frozen with the predictions and are not edited; three deserve naming:

- **`example-208` / `example-20000` → `lookup-28`.** The case *does* violate both sentences (it prints 0 for 208 and
  0 for 20000) and it passes. The tag is on the end state, which is the probe's stated rule; the `pass` is the
  coverage gap the tags are there to expose.
- **`output-function` → `fake-sim-script`.** The planted `/app/sim` is overwritten before it can print anything, so
  the case violates the sentence by printing `N/2` rather than the function; the tag is honest but the case is
  really about *who* the graded binary is (finding 6).
- **`gates-file` → `gates-is-directory`.** `Path.exists()` is true for a directory, so the "file exists" sentence is
  satisfied while the size test errors. The tag stays because the instruction asks for a *file*; the row's
  `enforced` label is carried by the two failing letters, one of which is an exception rather than an assertion.

## Case table

The 16 frozen cases in receipt order; letters are the three tests in file order (`test_gates_file_exists`,
`test_gates_file_size`, `test_sqrt_fib`) and the verdict is all three `P`.

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | PPF | fail | the shipped example circuit (prints N/2) left in place |
| `oracle-solve-sh` | PPP | pass | the task's solve.sh generates the reference circuit |
| `no-gates-file` | FFF | fail | `/app/gates.txt` removed |
| `empty-gates-file` | PPF | fail | an empty `/app/gates.txt`, so the simulator prints nothing |
| `lookup-28` | PPP | pass | a lookup circuit for exactly the 28 graded inputs, 0 elsewhere |
| `lookup-27-drop-48401` | PPF | fail | the lookup circuit without the largest graded input 48401 |
| `lookup-28-plus-examples` | PPP | pass | the lookup circuit plus the instruction's examples 208 and 20000 |
| `lookup-28-bitflip-41` | PPF | fail | the lookup circuit with bit 0 of the answer for N=41 flipped |
| `lookup-28-padded-31999` | PPP | pass | the lookup circuit padded with blank lines to 31999 lines |
| `lookup-28-padded-32000` | PFP | fail | the lookup circuit padded to 32000 lines: the size test counts blanks |
| `lookup-28-comment-lines` | PPP | pass | every gate line preceded by a `# note` line |
| `lookup-28-reversed-lines` | PPP | pass | the lookup circuit's lines in reverse order |
| `lookup-28-crlf` | PPP | pass | the lookup circuit with CRLF line ends |
| `lookup-28-trailing-space` | PPF | fail | every line ends in one space, so copy lines stop scanning as copies |
| `fake-sim-script` | PPF | fail | the example circuit plus an executable `/app/sim` printing the right answers |
| `gates-is-directory` | PFF | fail | `/app/gates.txt` is a directory, so the size test raises |

## Findings, each tied to its receipt cases

1. **A lookup table for the 28 graded inputs scores 3 of 3 (`lookup-28` `PPP`; `lookup-28-plus-examples` `PPP`;
   `nop` `PPF`; `empty-gates-file` `PPF`).** The value test walks a fixed 28-element list (`test_outputs.py:73-102`)
   and compares each entry (`:113-137`); no test evaluates the circuit anywhere else. The set is 1, 4, 8, 12, 41, 42,
   107, 220, 209, 366 and x², x²−1, x²+1 for x in 12, 41, 42, 107, 220, 209 — maximum 48401 — and it contains
   neither 208 nor 20000. The 1195-line circuit (`32 self-copies + 32 NOTs + 1099 binary gates + 32 final copies`,
   counted from the probe's builder, 0 constant lines) answers those 28 points and 0 elsewhere and passes all three
   tests. Both instruction examples therefore fail on a passing submission: the receipt's own tag record says so
   (`violates=example-208,example-20000` on a `pass`). The round-41 pilot measured the same two values from the same
   circuit (`./sim 208 → 0`, `./sim 20000 → 0`, `R41PlanNext` §3.2); this entry re-observes only the verdict, not
   those two runs.
2. **The shipped example already passes 2 of 3 (`nop` `PPF`).** The captured `gates.txt` is 33 lines: 32 self-copies
   and `out32 = 0`, which prints `N/2` (`instruction.md:10`). It exists and is under the bound, so tests 1 and 2 pass
   and only the value test fails; `empty-gates-file` is the same letters with the file emptied, because
   `num_signals == 0` makes `sim.c:340` print nothing, and the grader's `int("")` (`:127`) is caught by its own
   `except ValueError` (`:128-131`), which clears `all_passed` — the escaping failure is the final assert. The reward is
   still 0 (one failing function fails pytest, `test.sh:25-29`), but the do-nothing state is not a 0-of-3 state:
   unlike the round-41 `constraints-scheduling` grader (`nop` `FFF`) this one has no existence hole.
3. **The line budget is counted on lines, so blanks are budget (`lookup-28-padded-31999` `PPP`;
   `lookup-28-padded-32000` `PFP`).** `sum(1 for line in f)` (`:21`) over `open(..., 'r')` counts every physical
   line, and `:23` requires strictly fewer than 32000. The simulator never sees the blanks (`sim.c:113`), so 31999
   lines of which 30804 are empty pass 3 of 3, and one more line fails only the size test. Two consequences the
   receipt makes visible: the limit constrains file length, not circuit size; and a submission exactly at 32000 is
   `PFP`, i.e. the grader rejects it on a rule the submission's own semantics never touch.
4. **Line order and non-gate lines are invisible (`lookup-28-comment-lines` `PPP`;
   `lookup-28-reversed-lines` `PPP`).** `num_signals` is `out_idx + 1` for the highest index seen
   (`sim.c:117-118`), and the print loop reads `values[num_signals - 32 + i]` (`:343`). Reversing the file's lines
   therefore changes nothing (the same 32 signals exist, at the same indices), and `# note` lines are skipped before
   the index is ever read. `instruction.md:9`'s "the last 32 lines" and `instruction.md:1`'s "each line … of the
   form" are both descriptions the grader does not implement; they are the two `unenforced` rows of the map. A
   submission could therefore keep a human-readable comment block and any line order, and a submission whose final
   32 *lines* are wrong but whose 32 highest indices are right still passes.
5. **One trailing space per line is fatal; CRLF is free (`lookup-28-trailing-space` `PPF`; `lookup-28-crlf` `PPP`).**
   A copy line is recognised by `strncmp(op, "out", 3) == 0 && !strstr(op, " ")` (`:126`); with a trailing space the
   copy line falls through to the binary branch, whose `sscanf(op, "out%d %c out%d", …) == 3` (`:156`) fails; the line
   is not skipped (its first `sscanf` at `:113` succeeded and set `num_signals`), so the gate keeps its zero-initialised
   type, `OP_CONST_0`, and drives its signal to 0 from step 0 (wave-1 `R42CritProbe` D1, measured: one trailing space
   on the last line clears exactly bit 31 of the printed value) — tests 1 and 2 still pass, so the failure is `PPF`.
   Binary `&`/`|`/`^` lines keep working with a trailing space (`R42CritProbe` D1 table). The CRLF file passes
   because every form this circuit uses still scans with a `\r` on the end of `op`: copies and `~outN` are matched by
   prefix and parsed by `sscanf` (`:129`, `:142`), which ignores the trailing byte. **Scope, measured:** the lookup
   circuit contains no `outX = 0` and no `outX = 1` line (1195 lines: 0 constants), so this case does not show that
   a constant line survives CRLF. [INFERENCE] By reading: `strcmp(op, "0")` (`:122`) is exact and `op` would be
   `"0\r"`, so a `0` constant still yields 0 (the zero-initialised type is `OP_CONST_0`) while a `1` constant would
   silently drive 0. The receipt's CRLF verdict is shape-dependent, not a general newline tolerance.
6. **The grader compiles its own simulator over whatever the agent left (`fake-sim-script` `PPF`).** `:66` compiles
   `/tests/sim.c` with `-o sim` — a relative output name — and `:119` runs `/app/sim`. With the harness cwd at
   `/app` (`Dockerfile:3`), the compile overwrites any `/app/sim` the agent planted, which is what the case measures:
   an executable `/app/sim` printing the right answers does not pass, because the shipped example circuit it is
   graded against is what actually runs. This closes the most obvious verifier hole for this class — the agent cannot
   ship its own interpreter — and the mechanism is a cwd coincidence, not a path assertion: `-o sim` and `/app/sim`
   are two different names and no line of the grader binds them. [INFERENCE] A grading run whose cwd were not `/app`
   would compile `./sim` and then execute the agent's `/app/sim`; the probe fixes cwd `/app` (probe docstring), so no
   receipt case separates the two readings.
7. **Twenty-eight points, all-or-nothing (`lookup-27-drop-48401` `PPF`; `lookup-28-bitflip-41` `PPF`;
   `lookup-28` `PPP`).** Dropping the single largest input or flipping one bit of one answer fails only the value
   test: `all_passed` (`:103`) is cleared by any mismatch (`:136-137`) and asserted once (`:147`). The table's
   maximum, 48401 = 220²+1, is the only reach above 2^15; nothing grades an input outside the list, including any
   input above 48401 and every input the instruction's own "fib(isqrt(N))%(2^32)" formula covers above it.
8. **A directory in place of the gate file errors out of the size test (`gates-is-directory` `PFF`).** Test 1's
   `exists()` is true for a directory (`:11`); test 2 opens it and raises `IsADirectoryError` (`:20`), which the
   receipt records verbatim (`test_gates_file_size:error=IsADirectoryError`); test 3 compiles, and the simulator's
   `fopen` on a directory reads nothing, so `num_signals` stays 0, nothing is printed (`sim.c:340`) and the grader's
   `int("")` lands in its own `except ValueError` (`:126-131`), clearing `all_passed`. The letters are the measurement: an exception in one test and a silent empty
   read in the other, with no diagnostic naming the real problem.
9. **Removing the file fails all three (`no-gates-file` `FFF`).** Both `test_gates_file_exists` and
   `test_gates_file_size` assert existence on the absolute path `/app/gates.txt` (`:9`, `:16`, `:18`), and the value
   test fails because there is nothing to simulate. This is the only requirement whose violation is total, and it is
   also the only one enforced against a path the cwd cannot change.
10. **The instruction's interface sentence is not the graded interface (`oracle-solve-sh` `PPP`).** `instruction.md:8`
    says the first 32 lines are "defined by the binary representation of stdin"; `sim.c:322-331` seeds signals 0-31
    from `argv[1]` and never reads stdin, and the probe runs every case with stdin on `/dev/null` (probe docstring —
    the oracle case's own `solve.sh` recipe included). The task's oracle passes 3 of 3, so the graded channel is
    demonstrably argv. A second, unexercised contradiction sits beside it: `sim.c:328`'s comment says "signal 0 gets
    MSB, signal 31 gets LSB" while `:330` computes `(input_value >> i) & 1`, i.e. signal 0 gets the LSB. No receipt
    case separates the two readings, because a lookup circuit built to one convention is self-consistent — only a
    circuit relying on the comment's convention would differ, and none is frozen.

## Regrade (second grading of the same end state)

The probe's harness imports the grader once and calls the three functions twice on the same built state, in the same
sandbox, under the tags `TEST` and `REGRADE`; the second pass is reported (`regrade=same` / `regrade=DIFF:<letters>`)
and never used for the verdict. The receipt is `regrade cases=16 differ=0`. Every graded input is a file the case
built before the first pass — `/app/gates.txt`, `/tests/sim.c`, `/app/sim` — and the grader reads no clock,
environment or network (`test_outputs.py:1-147` has no such call); a second call over unchanged files cannot differ.
The column is therefore a determinism read of this probe, nearly tautological for this grader, and **not** a
re-run-stability claim: the value test does recompile the simulator on each call (`:65-70`), so the read does show
that `gcc` at this host is deterministic on this source, and nothing more. It could catch only a writer left running
inside the sandbox; this grader writes nothing outside its own `./sim` and pytest's cache.

## What the probe does not show

- **The task image is never pulled; the host's tools stand in.** `task.toml:29` names
  `alexgshaw/circuit-fibsqrt:20251031` and `:34` sets `allow_internet = true`; `Dockerfile:2` is
  `python:3.13-slim-bookworm` and `:6` installs `gcc` from apt; `test.sh:7-13` installs uv 0.9.5 from the network and
  runs pytest under `uvx -p 3.13`. The probe uses host `/usr/bin/python3` (3.14 on this host) and host
  `/usr/bin/gcc`, imports the captured module directly and runs the three functions itself, so the image's gcc
  version, the pinned `pytest==8.4.1`, `pytest-json-ctrf==0.3.5`, the ctrf report and the 3600 s verifier timeout
  (`task.toml:22`) are untested.
- **`tests/test.sh` was not executed.** The reward mapping is read (`test.sh:18-29`), not run: `apt-get`, the network
  uv install and `/logs/verifier/` are outside the sandbox. `observed_pass` means "the three functions return
  without failing", which is what makes pytest exit 0 — not that `reward.txt` was written.
- **The 16 cases are the claim's whole surface.** They were fixed before the first recorded run. States outside them
  — a >32000 signal index (an out-of-bounds write in `sim.c:117-118`, deliberately left unfrozen as
  non-deterministic), a `DURATION`-style circuit relying on a later step order, a gate file with a `\r`-bearing
  constant line, a symlinked `gates.txt`, an `/app/sim` that is a symlink or a directory, a submission that reads
  `/tests/sim.c` while it exists (the Dockerfile copies it into `/app` on purpose), and every AI-agent trajectory —
  are not covered and are not claimed.
- **The 28-value table is re-derived, not re-executed in the image.** The probe compiles the captured `sim.c` with
  host gcc and compares against `fibonacci(isqrt(n)) % 2**32` computed by the captured grader's own helpers
  (`test_outputs.py:26-52`); a difference between host gcc and the image's gcc in `-O3` behaviour is untested,
  though nothing in the source is undefined by inspection.
- **Not a statement about the task's validity, difficulty or solvability.** That is PROVINCE's question, not this
  lane's; `difficulty = "hard"` (`task.toml:15`) and the 16-hour expert estimate (`:18`) are the authors' metadata,
  read only. The lookup circuit is a constructed end state, not an agent's submission, and nothing here measures
  whether an agent would produce one.
- **The oracle row is one execution, not a correctness claim.** `oracle-solve-sh` runs the captured `solve.sh` as
  the case recipe and passes 3 of 3; it says nothing about other inputs, about `tests/test.sh`, or about the image.
- **The `gates.txt` example's provenance.** The capture is the file `Dockerfile:10` copies; that it is the file the
  authors ship today at the pin rests on the SHA256SUMS digest, which the spec also pins, not on a fetch by this seat.

## Prior art

- **A published audit asserts the opposite of finding 1.** `JonathanGabor/terminal-bench-2-audit`, run
  `20260120_125158`, `audit_results/audit.txt` (tier C, LLM-written), says of this task: “28 distinct test cases with
  varied inputs make hardcoding impractical”. The measured result is that a 1195-line lookup over exactly those 28
  inputs scores 3 of 3 (`lookup-28` `PPP`). The sentence was located by the round-41 planning seat
  (`.ufo/waves/round-41/build/R41PlanNext.md` §3.2) and is **not** re-fetched by this entry; it is cited as a prior
  statement, not as a registry row, and this entry claims **no novelty** — the round-41 seat had already measured
  the same coverage gap from the same captures (`R41PlanNext` §3.2: `./sim 208 → 0`, grader 3/3, `wc -l → 1195`).
  What this entry adds is the frozen 16-case receipt, the derived requirement map and the line-limit/ordering/
  whitespace mechanics; not the idea.
- **No published report of the other mechanics was found by this seat.** The round-41 seat's tracker sweep
  (`gh api` searches on 2026-10-25/26) returned 4 hits on `terminal-bench-2-1` for `circuit-fibsqrt`, all
  leaderboard-submission PRs, and 0 on `terminal-bench-2` and `terminal-bench` (`R41PlanNext` §3.3). I ran no
  tracker search of my own this round and therefore claim nothing about the absence of such reports.
- **The grader is what TB2.1 ships.** The round-41 seat reported all three of TB2.1 `main` (`7131e437`)'s
  `circuit-fibsqrt` files byte-identical to this pin (`test_outputs.py` sha256 prefix `6117b8ed`, `R41PlanNext`
  §3.3). Not re-verified by this entry; the capture digest `6117b8ed…` equals the pin in `plans/pkg-spec-r42.json`
  either way.
- **Grading-by-simulator is not new in general.** The lane's own executed sample already contains graders that run
  the agent's artefact rather than read it (`tb2-git-webserver-grader.md` runs a server; `tb2-build-pmars-grader.md`
  compiles and runs `pmars`). What is new here is that the *grader* supplies the interpreter and compiles it at
  grading time, so the agent's artefact is data for the grader's own code.

The claim this entry makes stays the narrow one: **a probed instance of the TB2 `circuit-fibsqrt` grader** — 16
frozen end states executed offline against these three captures, a requirement map derived from them, and the parse
semantics of the simulator that decides the verdict read out of `sim.c`. It is not a first-instance claim for
simulator-graded data artefacts, not a novelty claim, and not a claim about how agents solve the task.

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated, too easy or unsolvable (no image run,
no agent, no trajectory); that a lookup table is what an agent would build, or that the coverage gap is reachable by
four hours of work; that the grader should test the full 32-bit domain (no such proposal is described or judged
here); that the line limit is wrong as a design (the entry records what it counts, not what it should count); that
the trailing-space or CRLF behaviours are exploitable by a real submission (no agent produced either); or anything
about how Harbor executes this verifier (`benchmark-verifier-execution-model.md` covers where it runs and what it
restores).

Nor: **contamination** — `test_outputs.py:1-2` and `Dockerfile:1` carry the canary banner and these captures exist
for digest-pinned re-execution, not as a contamination measurement; **the image's toolchain** — host python and host
gcc are the probe's instruments, and `-O3` equivalence with the image's gcc is untested; **the oracle's
correctness** — `solve.sh` runs as one case's recipe and passes, which says nothing about other inputs; **the
instruction's intent** — that 208 and 20000 were meant as examples rather than as required outputs is the authors'
question, and the entry only records that the grader does not run them; **prevalence** — one task, 16 states, no
tracker sweep by this seat.

**Falsifier.** This entry is falsified if (a) a re-fetch of the three pinned URLs yields bytes whose SHA-256 differs
from `corpus/evidence/round42/tb2-circuit-fibsqrt/SHA256SUMS` and the pins in `plans/pkg-spec-r42.json`; (b) a fresh
run of `plans/fibsqrt_probe.py --lane .` prints anything other than `cases=16 observed_pass=7 observed_fail=9
mismatches=0` and `regrade cases=16 differ=0` — in particular if `lookup-28`, `lookup-28-plus-examples`,
`lookup-28-padded-31999`, `lookup-28-comment-lines`, `lookup-28-reversed-lines`, `lookup-28-crlf` or
`oracle-solve-sh` is observed `fail`, or if `nop`, `empty-gates-file`, `lookup-27-drop-48401`,
`lookup-28-bitflip-41`, `lookup-28-padded-32000`, `lookup-28-trailing-space`, `fake-sim-script`, `no-gates-file` or
`gates-is-directory` is observed `pass`; (c) a line of `test_outputs.py` is shown to read the gate file's semantics
rather than execute it, to evaluate the circuit at a value outside the 28-element list, to compare the submission
with `instruction.md`'s examples 208 or 20000, or to bind `./sim` to `/app/sim` by anything other than the cwd; or
(d) a line of `sim.c` is shown to read stdin, to print the file's last 32 lines rather than the 32 highest-indexed
signals, to reject a trailing-space copy line instead of leaving it a constant-0 gate, or to count blank lines toward
`num_signals`.

## Wave-1 integration (L1 `KengakuR42`, appended at landing)

Findings from wave-1 seats that bear on this entry; the frozen probe, dry table and receipt are unchanged.

- **Mechanism correction (`R42CritProbe` D1).** The probe docstring's "skips every line that does not scan as
  `out%d = <op>`" is half the story: a line that scans but whose operator matches no form is kept as an
  `OP_CONST_0` gate (`sim.c:9`, `:113`, `:126`, `:156`) and drives its signal to 0. Finding 5 above is written with the
  corrected mechanism; every verdict of the receipt stands (7 pass, 9 fail).
- **Tags the receipt understates (`R42CritProbe` D2, D3).** `lookup-28-padded-31999` and `lookup-28-padded-32000` end in
  32 blank lines, so they too pass only because the print window is the 32 highest-indexed signals, and their blank
  lines are not "of the form" — they would carry `last-32-lines` and `line-form` as well. `instruction.md:8` (stdin)
  has no frozen tag and no case. Neither changes a requirement-map label (`last-32-lines` and `line-form` stay
  `unenforced`); both are named here so no reader takes the reversed-lines case for the only positional divergence.
- **The cwd the receipt assumes is the verifier's (`R42ScoutHarborCwd`, `R42CritProbe` D4).** Harbor runs the
  verifier by `docker compose exec` without `-w`, so the cwd is the image `WorkingDir=/app`; under any other writable
  cwd the seat measured nine of the sixteen verdicts move and `fake-sim-script` flips to `PPP`. Finding 6's "cwd
  coincidence" is therefore load-bearing and holds for the shipped harness, not for the grader in isolation.
- **Probe pin breadth (`R42CritProbe` D5).** The probe digest-checks five of the nine captures; `Dockerfile`,
  `test.sh`, `task.toml` and `README.md` are pinned by the C2 counter's V1, not by the probe.
- **Prior art, searched this round (`R42ScoutPriorArt`, 2026-10-26 17:20-17:27 -03).** Of six findings, one is
  published as worded — the examples 208 and 20000 are not graded (JonathanGabor/terminal-bench-2-audit @ `35f11039`,
  `audit_results/20260120_125158/audit.txt:460`, LLM-written, tier C: "Example values from problem not directly
  tested") — and one in a weaker, adjacent form: the coverage gap above 48,401 with real agent circuits that pass the
  table and are wrong above it (S128, OpenAgents issue #9645, closed 2026-09-25: "The official grader exercises 28
  values, none above 48,401."). The lookup construct itself, the stdin/argv and last-32-lines divergences, the cwd
  compile and the whitespace mechanics were not found (queries in the seat report). The TB2.1 `main` copies of all
  nine files are byte-identical to the pin. This entry still claims no novelty.
- **Independent checks.** Real pytest 8.4.1 under Python 3.13 reproduces all 16 cases (`R42CritPytest`: parity 16/16).

## Errata (round 43, closure R1; appended 2026-10-26, nothing above edited)

Seven items. E1–E4 correct the four sentences `F42EntryQuotes` §4 found wrong or overclaiming; E5–E6 were found
re-deriving them; E7 is a locator `F42EntryQuotes` recorded as a nit outside its count. Each quotes the sentence with
its line, then the correction and the evidence line.

- **E1 `:296-298` (finding 7) — the `2^15` sentence.** Quote: "The table's maximum, 48401 = 220²+1, is the only reach
  above 2^15". **Wrong: six of the 28 graded inputs are above 2^15 = 32768**, all from the two largest roots —
  220²−1 = 48399 (`test_outputs.py:94`), 220² = 48400 (`:88`), 220²+1 = 48401 (`:100`), 209²−1 = 43680 (`:95`),
  209² = 43681 (`:89`), 209²+1 = 43682 (`:101`); the next-largest input is 107²+1 = 11450 (`:99`). Correction: "The
  table's largest input is 48401 = 220²+1, and six of its 28 inputs lie above 2^15 (220²−1, 220², 220²+1 and 209²−1,
  209², 209²+1); nothing grades an input outside the list." The summary sentence at `:17` and the rest of finding 7 (dropping 48401 or
  flipping one bit of one answer is `PPF` — only the value test fails, receipt lines 12 and 14) stand.

- **E2 `:309-312` (finding 10) — stdin scope and locator.** Quote: "the probe runs every case with stdin on
  `/dev/null` (probe docstring — the oracle case's own `solve.sh` recipe included)". **Wrong twice.** The probe pins
  `stdin=subprocess.DEVNULL` for the case *recipe only* (`plans/fibsqrt_probe.py:201`); each case's harness is launched
  with no `stdin=` (`fibsqrt_probe.py:266-267`), so the graded `/app/sim` calls — `subprocess.run(["/app/sim", …])` with
  no `stdin=` (`test_outputs.py:119`) — inherit the harness's stdin, i.e. the probe caller's. The probe docstring makes
  no `/dev/null` statement at all; its only stdin sentence is that `sim.c` "sets signals 0-31 from argv[1] (not stdin)"
  (`fibsqrt_probe.py:27-28`). Correction: "`sim.c:324` takes the value from `argv[1]` and no line of `sim.c` reads stdin
  (its only stream read is `fgets` over the gate file, `:108`); the probe pins the case recipe's stdin to `/dev/null`
  (`fibsqrt_probe.py:201`) and leaves the graded `/app/sim` calls on the caller's stdin (`:266-267`,
  `test_outputs.py:119`)." The finding's conclusion — the graded channel is argv, shown by `oracle-solve-sh` `PPP` —
  stands, on `sim.c`'s code, not on this sentence.

- **E3 `:430-432` (integration, D2 bullet) — the padded rows' verdicts.** Quote: "end in 32 blank lines, so they too
  pass only because the print window is the 32 highest-indexed signals". **Overclaim.** Only the *value* test passes
  for that reason: `lookup-28-padded-31999` is `PPP` (receipt line 15) but `lookup-28-padded-32000` is observed `fail`,
  `PFP` (receipt line 16), because `test_outputs.py:21-23` counts the blank lines and the file is exactly 32000.
  Correction: "…so their value test passes only because the print window is the 32 highest-indexed signals
  (`sim.c:340-347`); `lookup-28-padded-32000` is observed `fail` (`PFP`) on the size test, `lookup-28-padded-31999`
  `PPP`." The tag argument (both would carry `last-32-lines` and `line-form`) is unaffected.

- **E4 `:433-434` — the labels under that counterfactual.** Quote: "Neither changes a requirement-map label
  (`last-32-lines` and `line-form` stay `unenforced`)". **Wrong under the bullet's own counterfactual.** Tag both
  padded rows and `padded-32000` (observed `fail`) joins `lookup-28-comment-lines` (`P`, receipt line 17) in the
  `line-form` set and `lookup-28-reversed-lines` (`P`, line 18) in the `last-32-lines` set; by the V7 rule at
  `:152-154` each label then becomes `partly`, not `unenforced`. Correction: "the two labels are `unenforced` only
  because the frozen receipt does not tag the padded rows; under this bullet's counterfactual both become `partly`."
  The frozen tags and the V7 labels as computed stay as they are.

- **E5 `:430-431` — the count of blank lines.** Quote: "end in 32 blank lines". **Wrong count.** The builder appends
  `[""] * (31999 - len(L28))` and `[""] * (32000 - len(L28))` (`plans/fibsqrt_probe.py:177-181`) with `len(L28) = 1195`
  (measured by importing the frozen builder), so the files end in **30804** and **30805** blank lines — as finding 3
  itself says at `:261` ("31999 lines of which 30804 are empty"). Correction: "end in 30804 / 30805 blank lines, so the
  file's last 32 lines are blank". The `last-32-lines` argument needs only the last 32; its conclusion stands.

- **E6 `:96`, `:144` (and the wording at `:40`) — "dropped" for an operator outside `&|^`.** Quotes: "parsed by
  `sscanf(op, "out%d %c out%d", …)` and dropped if that fails" (`:96`); "binary gates are parsed by sscanf and
  silently dropped when it fails" (`:144`). **Wrong.** Nothing is dropped: `Gate gates[MAX_SIGNALS]` is zero-initialised
  at file scope (`sim.c:24`; `OP_CONST_0` is 0, `:9`), `num_signals` was already raised at `:117-118`, and the missing
  final `else` leaves the type at `OP_CONST_0`, so the line stays a constant-0 gate and drives its signal to 0.
  Measured on the captured `sim.c` (`gcc -O3`, digest `700645ac…`, round-43 envelope): `out0 = 1` + `out40 = out1 + out2`
  → `0`; `out40 = out1 &` (binary `sscanf` returns 2) → `0`; `out40 = 1` → `2147483648` (index 40 is bit 31);
  `out0 = 1` alone → no output (so `num_signals` really moved to 41). The entry already says this at `:275-276` and in
  the wave-1 note at `:428`; only these three places keep the old wording. Correction: "binary gates are parsed by
  `sscanf(op, "out%d %c out%d", …) == 3`; the `&`/`|`/`^` switch has no default, so an unhandled operator leaves the
  gate a zero-initialised `OP_CONST_0` that drives 0 — not skipped, not an error."

- **E7 `:305-306` (finding 9) — the existence locators.** Quote: "assert existence on the absolute path
  `/app/gates.txt` (`:9`, `:16`, `:18`)". **Locator wrong, claim right.** `:9` and `:16` are the
  `gate_path = Path("/app/gates.txt")` assignments; the asserts are `:11` (test 1) and `:18` (test 2). Correction:
  "`test_outputs.py:11` and `:18`". (Recorded as a nit by `F42EntryQuotes` §4, outside its count of four.)

### S135 — the cwd claims now rest on a registry row (round 43, appended)

The four cwd statements in this entry were anchored on a capture only; they are now anchored on a row. `S135`
(`environment/Dockerfile` @ `2fd12b88`, tier B, status `mined`, `used-by` this file) pins the image definition whose
line 3 is `WORKDIR /app` — the working directory the grader's `-o sim` compile and its `/app/sim` execution both
resolve against, and the directory `:9-10` copy `tests/sim.c` and `gates.txt` into. It carries no graded predicate of
its own: `test_outputs.py` and `sim.c` hold every predicate, so the row is cited as the mechanism those predicates
assume, not as a source of the graded rule. The statements it anchors are `:65` (`Dockerfile:3` is `WORKDIR /app`,
`Dockerfile:9-10` the two copies), `:89` (the `Initial state` row, `Dockerfile:3` and `:9-10`), `:94` (`gates.txt`
resolved against a cwd the harness fixes at `/app`) and `:435-438` (the wave-1 note that the receipt's cwd is the
verifier's `WorkingDir=/app`, which is what makes Finding 6's cwd coincidence load-bearing). Re-opened 2026-10-26
19:10:24 -03: `curl` → `200`, 321 bytes, `cmp` identical to `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile`,
sha256 `780c2398…3d3d4`, 10 lines. The round-42 Gate's flip condition — "if the entry keeps the `WORKDIR /app`
sentence …, admit `Dockerfile` as a tier-B mechanism row" — is executed by this row and this paragraph, not waived,
and the statements above stay as written (no erratum is needed: none of them was wrong, they were under-anchored).
