# Block (d) — SKILL.md section 'Simulator-executed data-artefact TB2 grader — round 42'

Draft only. APPEND at end of `SKILL.md` (after `:1140`, the last line of the round-41 section's closing sentence
"advice, not a statement about RFC 5545 conformance in general, and not a statement about any agent's behaviour.").
Heading level and shape copied from `SKILL.md:1059-1140` (`## … TB2 grader — round 41` + `### Decision table — what
the grader reads, and what passes it`).

```markdown
## Simulator-executed data-artefact TB2 grader — round 42

Before citing the pinned TB2 `circuit-fibsqrt` scorer, run `python3 plans/fibsqrt_probe.py --lane .` and read its
summary line: exit `0` means only that all 16 cases produced three test verdicts twice each — a prediction mismatch
does not change the exit code, it is printed on the summary line (`plans/fibsqrt_probe.py:358-360`), and exit `2` is
a setup failure — a duplicate or malformed case id, an unknown tag, a malformed prediction, a graded list that is not
28 long, a capture missing or not at its pinned digest, `/usr/bin/bwrap`, `/usr/bin/python3`, `/usr/bin/bash` or
`/usr/bin/gcc` not executable (`:70-71`), a `--work`
directory that cannot be created, or a case that did not yield three verdicts twice (a recipe error is never a
verdict) (`plans/fibsqrt_probe.py:288-293,308-318,344`). `--dry` prints the frozen case table with no sandbox and
`--stage-check` builds each case's end state and prints only stage exit codes, the grader never imported
(`plans/fibsqrt_probe.py:4-7`), so neither is evidence. The receipt's summary
(`corpus/evidence/round42/fibsqrt-probe.txt:24`) reads `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, and a
second, same-process grading of each un-rebuilt end state agrees case by case (`regrade cases=16 differ=0`, `:23`) — a
determinism read of the probe, not re-run stability.

The class is new: the graded artefact is a **program in a data format**, and the interpreter that executes it is
owned by the grader. `/app/gates.txt` is a list of `outX = …` gate lines (`instruction.md:1-7`); test 3 compiles the
task's own simulator at grading time (`gcc -O3 /tests/sim.c -o sim`, `tests/test_outputs.py:65-67`) in the cwd
(`Dockerfile:3` `WORKDIR /app`, and `tests/test.sh:13-16` refuses `/`), so `./sim` and the `/app/sim` it then runs
(`:119`) are the same file, and the `/app/sim.c` the Dockerfile ships for the agent (`Dockerfile:8-9`) is never the
compiled source. The simulator reads `gates.txt` **relative to its cwd** (`sim.c:319`, `fopen` `:101`), builds a
dependency graph from every line that scans as `out%d = <op>` and silently skips the rest (`sim.c:113-115`), sets
signals 0-31 from `strtoul(argv[1], …)` (`:324`, bit `i` of the argument into signal `i`, `:330`), runs exactly 32000
synchronous steps (`:335`), and prints bits 0-31 of the 32 **highest-indexed** signals (`:342-345`) — three points
where `instruction.md:8-9` says stdin, "the last 32 lines" and an unnamed bit order.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `Path("/app/gates.txt").exists()` (`test_outputs.py:7-11`) | anything that exists, including a **directory** — `gates-is-directory` passes test 1 and fails tests 2-3 (`PFF`) | `is_file()`, not `exists()`; the size test is what rejects a directory, and it does so by raising | `gates-is-directory` (receipt:22), `no-gates-file` (`FFF`, receipt:9) |
| `sum(1 for line in f) < 32000` over the whole file (`:14-23`) | exactly 31999 lines, blank padding included (`lookup-28-padded-31999` `PPP`); 32000 fails **only** this test (`lookup-28-padded-32000` `PFP`) | count every line yourself, blanks and comments included; `sim.c` ignores both, so the budget buys nothing | `lookup-28-padded-31999` (receipt:15), `lookup-28-padded-32000` (receipt:16) |
| `gcc -O3 /tests/sim.c -o sim`, then `/app/sim N` (`:65-67`, `:119`) | the grader's own compile: a planted executable `/app/sim` printing the right answers is overwritten and `fake-sim-script` fails the output test (`PPF`) | which file the binary came from, and that `/app/sim.c` (shipped for the agent, `Dockerfile:9`) has no effect | `fake-sim-script` (receipt:21), `oracle-solve-sh` (`PPP`, receipt:8) |
| 28 fixed inputs — `1,4,8,12,41,42,107,220,209,366` and `x²`, `x²-1`, `x²+1` for x in `12,41,42,107,220,209`; largest 48401 (`:73-102`) | a circuit right on exactly those 28 and 0 elsewhere: `lookup-28` is `PPP` at 1195 lines and prints 0 for the instruction's own examples 208 and 20000 | the 28 inputs, not the instruction's examples: test 3 never calls `sim 208` or `sim 20000` | `lookup-28` (receipt:11), `lookup-28-plus-examples` (`PPP`, receipt:13), `lookup-27-drop-48401` (`PPF`, receipt:12) |
| `fibonacci(isqrt(n)) % 2**32` computed **in the test file** (`:26-53`, `:115-117`) — no reference data exists | the exact integer; one flipped answer bit at N=41 fails the output test (`lookup-28-bitflip-41`, `PPF`) | recompute `fib` and `isqrt` yourself; both are in the grader, so the oracle is the grader's own arithmetic | `lookup-28-bitflip-41` (receipt:14) |
| `gates.txt` opened cwd-relative (`sim.c:319`, `:101`) and every non-scanning line skipped (`:113-115`) | line order, `#` comment lines and CRLF are free: `lookup-28-reversed-lines`, `-comment-lines`, `-crlf` all `PPP` (`instruction.md:1`'s "each line … a line of the form" is not checked) | that the file is a dependency graph over signal indices: nothing else in the file is read, and the physical last lines mean nothing | `lookup-28-comment-lines` (receipt:17), `lookup-28-reversed-lines` (receipt:18), `lookup-28-crlf` (receipt:19) |
| the `out%d = %[^\n]` capture keeps trailing whitespace, and the copy branch needs `strncmp(op, "out", 3) == 0 && !strstr(op, " ")` (`sim.c:113`, `:126`) | one trailing space on every line makes every copy line a no-op (the unparsed gate keeps type `OP_CONST_0`, `sim.c:9`, `:259`) and the printed word 0 — `lookup-28-trailing-space` is `PPF` | strip the line before deciding it scans; an invisible byte flips the score | `lookup-28-trailing-space` (receipt:20) |
| `strtoul(argv[1])` (`:324`), `values[i] = (input_value >> i) & 1` (`:330`), 32000 steps (`:335`), result bits taken from `values[num_signals-32 + i]` (`:340-347`, bit `i` set at `:343-344`) | the printed word is the 32 **highest-indexed** signals, not the file's last 32 lines: the shipped 33-line example (`out0 = out0` … `out31 = out31`, `out32 = 0`, `gates.txt:1-33`) prints `argv[1] >> 1`, which is `instruction.md:10`'s `argv[1]/2` | the index arithmetic and the argument, not the prose: `instruction.md:8` says stdin and `:9` says "the last 32 lines" | `nop` (`PPF`, receipt:7 — the shipped example, only the output test failing), `lookup-28-reversed-lines` (receipt:18) |
| nothing — the circuit as logic | a table, not an implementation: `lookup-28` passes 3/3 (`PPP`) for a function it does not compute | whether the file *computes* `fib ∘ isqrt` at all; only 28 outputs are ever observed | `lookup-28` (receipt:11), `lookup-28-plus-examples` (receipt:13) |
| stdout parsed with `int(result.stdout.strip())` (`:127`) and `returncode != 0` read as a failed case (`:121-124`) | a file with fewer than 32 distinct signal indices prints nothing (`sim.c:340`) — `int('')` raises and the case fails: `empty-gates-file` `PPF`; a missing file makes `sim` exit 1 (`sim.c:103-104`) and fails all three (`no-gates-file` `FFF`) | that "no output" and "wrong output" are the same verdict, and that the parse is unconditional | `empty-gates-file` (receipt:10), `no-gates-file` (receipt:9) |
| the task's own oracle and the do-nothing baseline | `oracle-solve-sh` is `PPP` (receipt:8) — the task's `solve.sh`, 444 lines, generates the reference circuit — and `nop` is `PPF` (receipt:7): the shipped example already passes 2 of 3 | run both first: this grader starts at 2 of 3 on its own initial state, unlike round 41's | `oracle-solve-sh` (receipt:8), `nop` (receipt:7) |

What a green means here: in the probe's staged state `/app/gates.txt` was a gate list under the line cap whose
circuit, run by the grader's own compiled `sim.c` over the 28 fixed inputs, printed `fib(isqrt(N)) % 2**32` — on
states the probe built, not states an agent built. What it does not mean: that the circuit computes anything
(`receipt:11`), that the instruction's own examples work (`receipt:11`), that lines are read in order or at all
(`receipt:17-19`), that a runtime `/app/sim` matters (`receipt:21`), that the file is a regular file (`receipt:22`),
or that the simulator behaves as `instruction.md:8-9` says (code read, `sim.c:324,342-345`).

Of the seven frozen instruction tags (`TAG` lines `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt:1-7`), the
round-42 counter's V7 rule (`plans/round42_c2_verify.py`, label rule: label = the observed verdicts of every receipt
case whose `violates=` carries the tag; all fail → `enforced`, all pass → `unenforced`, mixed → `partly`) gives,
counted from the receipt: `line-form` (`instruction.md:1`) `unenforced` — 1 case, 1 observed pass
(`lookup-28-comment-lines`); `last-32-lines` (`:9`) `unenforced` — 1, 1 (`lookup-28-reversed-lines`); `gates-file`
(`:11`) `enforced` — 2, 0; `line-limit` (`:11`) `enforced` — 1, 0; `output-function` (`:11`) `partly` — 15, 6 passes;
`example-208` (`:12`) `partly` — 14, 5; `example-20000` (`:13`) `partly` — 14, 5. `enforced` is a property of the
frozen case set only: `gates-file` and `line-limit` rest on one or two witnesses, and `line-form`/`last-32-lines` mean
"the only frozen case that violates it is observed pass", not "an agent may not violate it". The three `partly` tags
are `partly` for the same reason: `lookup-28` and its padding/comment/reversal/CRLF variants pass while printing 0
for 208 and 20000. The entry's `## Requirement map` carries one row per tag in the counter's row shape
(`| \`instruction.md:<L>\` | \`<tag>\` | <label> | case-id, … |`), and V7 re-derives all seven labels from the receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:29` names
`alexgshaw/circuit-fibsqrt:20251031`; `allow_internet = true` at `:34`; `Dockerfile:2` builds on
`python:3.13-slim-bookworm`) or a harness. Host python3 and host gcc stand in for the image's python 3.13 and Debian
bookworm gcc (`tests/test.sh:18-22` runs pytest under `uvx -p 3.13`, which needs the network; its
`/logs/verifier/reward.txt` write is `:25-29`); recipes run as the probing user rather than root; each case stages its
own `/app` and `/tests`, so no case observes the image's tree; and `/tests/sim.c` is the captured file, so the compile
is the image's recipe, not the image's compiler. The 28-value table and the line cap are read from the captured
grader, not from the instruction alone. Three of the 16 cases (`nop`, `oracle-solve-sh`, `lookup-28`) re-observe
shapes the round-41 wave-1 seat graded on this host before the freeze, disclosed at freeze; the other 13 were never
graded before it, and `mismatches=0` means every frozen prediction held, none was edited. A property of this capture
at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver advice, not a statement about
digital-logic design or C semantics in general, and not a statement about any agent's behaviour.
```

Citation audit for this block: receipt numbers are `fibsqrt-probe.txt:7-24` as marked on each row; the tag lines and
their frozen locations are `fibsqrt-dry-cases-freeze.txt:1-7`; the labels and per-tag case counts (1/1, 1/1, 2/0,
1/0, 15/6, 14/5, 14/5) were derived from the receipt's `violates=` and `observed=` fields with the V7 rule
(derivation command in the seat report §2); simulator, grader, harness, Dockerfile and task.toml lines are in
`corpus/evidence/round42/tb2-circuit-fibsqrt/`; probe line numbers are `plans/fibsqrt_probe.py`.
