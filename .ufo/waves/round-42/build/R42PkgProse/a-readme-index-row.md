# Block (a) — corpus/README.md: knowledge index row + coverage-map bullet

Draft only. Two paste blocks. Nothing outside the fenced blocks is content; the anchor comments are
instructions to the L1, not text to paste.

## a1. Knowledge index row — INSERT after `corpus/README.md:74` (the round-41 row), before `:75` (`| \`lessons/round-1.md\` …`)

Shape copied from `corpus/README.md:74`: one row, one physical line, no `|` inside a cell, fifth column =
`S…` rows plus the pin, then probe and receipt.

```markdown
| `knowledge/tb2-circuit-fibsqrt-grader.md` | An eighth Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `circuit-fibsqrt` grades a **data artefact** — a gate list at `/app/gates.txt` — by compiling the task's own simulator at grading time (`gcc -O3 /tests/sim.c -o sim` in the cwd, `test_outputs.py:65-67`) and running `/app/sim N` on 28 fixed inputs (largest 48401, `:73-102`), so the whole score is existence, a `< 32000` line count and 28 printed words: a 1195-line lookup circuit covering exactly those 28 inputs passes 3/3 (`lookup-28`) while printing 0 for the instruction's own examples 208 and 20000, blank padding to 31999 lines still passes but 32000 fails only the size test, `#` comment lines, full line reversal and CRLF all pass, one trailing space per line fails, a planted executable `/app/sim` is overwritten by the grader's own compile, and a directory named `gates.txt` passes the existence test and fails the other two (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`; `regrade cases=16 differ=0`) | S125, S126, S127 (terminal-bench-2 @ 2fd12b88); probe `plans/fibsqrt_probe.py`, receipt `evidence/round42/fibsqrt-probe.txt` |
```

Every number above: `cases=16 observed_pass=7 observed_fail=9 mismatches=0` = `corpus/evidence/round42/fibsqrt-probe.txt:24`;
`regrade cases=16 differ=0` = `:23`; `lookup-28` `PPP` = `:11`; `lookup-28-padded-31999` `PPP` = `:15`;
`lookup-28-padded-32000` `PFP` = `:16`; `-comment-lines`/`-reversed-lines`/`-crlf` `PPP` = `:17-19`;
`-trailing-space` `PPF` = `:20`; `fake-sim-script` `PPF` = `:21`; `gates-is-directory` `PFF` = `:22`;
1195 lines = the dry table's `gates_lines=1195` (`fibsqrt-dry-cases-freeze.txt:10`); 28 inputs and largest 48401 =
`test_outputs.py:73-102`; `< 32000` = `test_outputs.py:23`; compile line = `test_outputs.py:65-67`.

## a2. Coverage-map bullet — INSERT after `corpus/README.md:269` (the "seventh task, embedded-scheduling-model class" bullet), before `## Open gaps` at `:270`

Shape copied from `corpus/README.md:263-269`: `- **Title (nth task, class)**: covered at source-code depth and
executed offline (round N, date) — entry; S-rows; probe, receipt. A nth instance of the same ground (n of the 89 TB2
task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `task` only: …`

```markdown
- **Terminal-Bench 2.0 task grader (eighth task, grader-compiled-simulator class)**: covered at source-code depth and executed offline (round 42, 2026-10-26) — knowledge/tb2-circuit-fibsqrt-grader.md; S125, S126, S127; probe `plans/fibsqrt_probe.py`, receipt `evidence/round42/fibsqrt-probe.txt`. An eighth instance of the same ground (8 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `circuit-fibsqrt` only: the graded artefact is a program in a data format — `/app/gates.txt`, a gate list that the task's own `sim.c` interprets — and the grader compiles that interpreter itself (`gcc -O3 /tests/sim.c -o sim` in the cwd, `test_outputs.py:65-67`) before running `/app/sim N` over 28 fixed inputs (`:73-102`, largest 48401 = 220²+1), so the whole score is `Path("/app/gates.txt").exists()`, `sum(1 for line in f) < 32000` and 28 stdout integers compared with `fib(isqrt(N)) % 2**32` (`:7-11`, `:14-23`, `:115-117`). Neither the instruction nor the tests constrain the circuit: a 1195-line lookup table for exactly the 28 graded inputs passes 3 of 3 (`lookup-28`, receipt:11) although `instruction.md:12-13` says `sim 208` gives 377 and `sim 20000` gives 1407432322 and that file prints 0 for both; dropping the largest graded input fails only the output test (`lookup-27-drop-48401`, `PPF`, receipt:12) and one flipped bit at N=41 likewise (`lookup-28-bitflip-41`, receipt:14); blank padding to 31999 lines passes (`lookup-28-padded-31999`, receipt:15) while 32000 fails only the size test (`lookup-28-padded-32000`, `PFP`, receipt:16); `#` comment lines, full line reversal and CRLF all pass (`receipt:17-19`) because `sim.c` builds a dependency graph and skips every line that does not scan as `out%d = <op>` (`sim.c:113-115`), while one trailing space per line fails the output test (`receipt:20`) because the captured operator keeps the space and the copy branch requires `!strstr(op, " ")` (`sim.c:113`, `:126`); a planted executable `/app/sim` printing the right answers is overwritten by the grader's compile into the cwd (`fake-sim-script`, `PPF`, receipt:21); and a directory at `/app/gates.txt` passes existence, raises `IsADirectoryError` in the size test and fails the output test (`gates-is-directory`, `PFF`, receipt:22, which names `test_gates_file_size:error=IsADirectoryError`). `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0` (receipt:23-24).
```
