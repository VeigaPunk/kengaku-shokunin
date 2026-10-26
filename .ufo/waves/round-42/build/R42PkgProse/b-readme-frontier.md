# Block (b) — corpus/README.md `## Frontier`: round-42 TB2 sub-bullet, narrowed to "8 of 89 read"

Draft only. INSERT after `corpus/README.md:359` (the last line of the round-41 sub-bullet, `behaviour.`), before
`:360` (`- **Contamination transparency cards**`). Two-space sub-bullet indent, shape copied from
`corpus/README.md:343-359`. It stays inside the `## Frontier` section, so it satisfies V9(d)
(`plans/round42_c2_verify.py:310-312` requires `circuit-fibsqrt` anywhere in that section).

```markdown
  - *Partly discharged round 42 (2026-10-26):* `knowledge/tb2-circuit-fibsqrt-grader.md` reads and executes an
    eighth Terminal-Bench 2.0 task's scoring code (`circuit-fibsqrt/tests/test_outputs.py` with `tests/sim.c` @
    `2fd12b88`; S125, S126, S127) against its `instruction.md`, probe `plans/fibsqrt_probe.py`, receipt
    `corpus/evidence/round42/fibsqrt-probe.txt`. The graded state is a class the lane had not executed before: a
    program in a data format — `/app/gates.txt` is a gate list that the task's own simulator executes, and the
    grader compiles that simulator itself (`gcc -O3 /tests/sim.c -o sim` in the cwd, `test_outputs.py:65-67`) before
    running `/app/sim N` for 28 fixed inputs (largest 48401 = 220²+1, `:73-102`) and comparing stdout with
    `fib(isqrt(N)) % 2**32` (`:115-117`). So the three tests are existence (`:7-11`), `sum(1 for line in f) < 32000`
    (`:14-23`) and those 28 outputs (`:56-147`): a 1195-line lookup table for exactly the 28 graded inputs passes
    3 of 3 (`lookup-28`, receipt:11) while printing 0 for `instruction.md:12-13`'s own examples 208 and 20000, blank
    padding to 31999 lines passes and 32000 fails only the size test (`receipt:15-16`), comment lines, reversed line
    order and CRLF pass (`receipt:17-19`), one trailing space per line fails (`receipt:20`), a planted executable
    `/app/sim` is overwritten by the grader's compile (`receipt:21`), and a directory named `gates.txt` passes
    existence and fails the rest (`receipt:22`) — `cases=16 observed_pass=7 observed_fail=9 mismatches=0`,
    `regrade cases=16 differ=0` (`receipt:23-24`). The "Terminal-Bench 2.0's" clause is **narrowed for that one task
    only**; it stays open for the remaining TB2 task graders (8 of 89 read), for any SWE-bench Pro V2 grader beyond
    the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image
    (never pulled) or a harness run (the task's own `solve.sh` is executed as one case and observed pass), not
    contamination, not model or agent behaviour.
```

Citation audit for this block: every number is `fibsqrt-probe.txt:11-24` as marked, or `test_outputs.py` lines
(`:7-11`, `:14-23`, `:56-147`, `:65-67`, `:73-102`, `:115-117`) in `corpus/evidence/round42/tb2-circuit-fibsqrt/`.
"8 of 89 read" follows the claims file's own narrowing (`plans/round-42-claims.md` §C2: eighth grader class) and the
round-41 sub-bullet's "7 of 89".
