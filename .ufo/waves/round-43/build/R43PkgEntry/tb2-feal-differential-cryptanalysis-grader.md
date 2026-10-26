source: S129 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/test_outputs.py — the one pytest function that is this task's whole score, lines 1-30, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S130 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/instruction.md — the request the grader is mapped against, lines 1-6, same commit, accessed 2026-10-26
source: S131 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/feal_module.c — the CPython wrapper that exports `encrypt`, `get_keys` and `create_random_keys`, lines 1-68, same commit, accessed 2026-10-26
source: S132 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/feal.c — the C FEAL implementation whose key schedule and four-round cipher the extension wraps, lines 1-99, same commit, accessed 2026-10-26
source: S133 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/test.sh — the harness's reward mapping, lines 1-29, same commit, accessed 2026-10-26
source: S134 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/README.md — the authors' own README for this task, lines 1-34, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round43/tb2-feal-differential-cryptanalysis && sha256sum -c SHA256SUMS)` (twelve files), re-fetch the six pinned URLs and compare with the pin table in `plans/pkg-spec-r43.json`, then re-run `python3 plans/feal_probe.py --lane .`; any capture digest, probe output or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `feal-differential-cryptanalysis`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `feal-differential-cryptanalysis` task is scored by **one** pytest
function, `test_feal_differential_cryptanalysis_attack` (`tests/test_outputs.py:7-30`), and the reward is one bit
mapped from the pytest exit status (`test.sh:22`, `:25-29`). The graded artefact is an **agent-authored Python
module**, `/app/attack.py`, that the grader **imports into its own interpreter** (`test_outputs.py:22-24`) beside
the reference C extension `feal_in_c`, whose public `get_keys()` returns the six 32-bit round keys
(`feal_module.c:25-43`, `:51`). The single value assertion is `feal_in_c.get_keys()[5] == stolen`
(`test_outputs.py:30`), where `stolen` is whatever `attack.attack(feal_in_c.encrypt)` returned (`:29`).

**The class, worded narrowly.** This is module import plus an in-process call: the agent's module runs inside the
grader's process, receives the grader's own `encrypt` function as an argument, and can reach every other public
name of the same interpreter — including the module that holds the answer. The lane already executes an
agent-authored artefact in-process in `knowledge/tb2-regex-log-grader.md` (an agent-supplied regex is compiled and
applied inside the scoring process); what this entry adds is the import-and-call shape, not "agent code in
process". No novelty is claimed here.

On the 12 frozen end states of this round's probe, the grader reproduced the frozen prediction on all 12
(`cases=12 observed_pass=8 observed_fail=4 mismatches=0`) and graded every end state a second time with no
difference (`regrade cases=12 differ=0`). Four results organise the rest of the entry.

(1) **The answer is a public function of a module the agent's code can import, and five cheats that never recover
the key pass.** `cheat-import-get_keys` (`P`) returns `get_keys()[5]`; `cheat-patch-get_keys` (`P`) rebinds
`get_keys` before the assert reads it; `cheat-sysmodules-shadow` (`P`) installs a fake `feal_in_c` in `sys.modules`
at `import attack` time, which is *before* the grader's own `import feal_in_c`; `cheat-always-equal` (`P`) returns
an object whose `__eq__` is always true; `cheat-exit-zero` (`P`) ends the grader process with `os._exit(0)` before
the assert. None of them performs cryptanalysis.

(2) **Nothing times the call.** `attack.attack(...)` at `test_outputs.py:29` is a plain Python call; the only bound
is the verifier timeout of 1800 s (`task.toml:22`). A reference attack followed by a 45 s sleep
(`slow-oracle-45s`, `P`) passes although `instruction.md:3` asks for "less than 30 seconds" and `README.md:35`
claims the test "Confirms the attack completes within the time limit".

(3) **The key schedule is clock-seeded and 16 bits wide per key.** `create_random_keys()` calls `srand(time(NULL))`
once per process (`feal.c:60-62`) and then `key[i] = (rand() & 0xFFFF) * 1234567` (`:65-66`);
`test_outputs.py:27` calls it inside the grading process. An agent that replays libc's `srand`/`rand` over a short
clock window and checks candidates against `encrypt_fn` passes (`cheat-clock-seed`, `P`, flagged `host=libc-rand`).

(4) **Three shapes that do the task correctly still fail the one assertion.** Returning 0 (`wrong-key`, `F`), the
reference result plus one (`oracle-off-by-one`, `F`) and the reference result as a decimal string (`return-str`,
`F`) each fail only the equality at `:30`; the task's own `solve.sh` passes (`oracle-solve-sh`, `P`). The
do-nothing state is `F` for a different reason: no `/app/attack.py` (`nop`, `F`, `ModuleNotFoundError` at
`:24`).

## Source labels

S129, S131, S132 and S133 are the benchmark maintainers' own scoring code: primary for *what this grader checks*,
for the extension's exported surface and key schedule, and for the reward mapping. S130 is the maintainers' own
request and is primary only for *what is asked*; every claim about what is graded is drawn from S129/S131/S132/S133,
never from S130, and the requirement map below records exactly where the two disagree. S134 is the authors' prose
about the task (`:5` overview, `:21` the 30 s attack limit, `:31-35` its own description of the verification) and is
read as the authors' claim, then checked against the code: `:35`'s "Confirms the attack completes within the time
limit" is **not** something `test_outputs.py` does.

`task.toml` (captured, not a registry row) is the authors' metadata: `difficulty = "hard"` (`:15`),
`expert_time_estimate_min = 480.0` (`:18`), `junior_time_estimate_min = 19200.0` (`:19`), verifier and agent
timeouts of 1800 s (`:22`, `:25`), `docker_image = "alexgshaw/feal-differential-cryptanalysis:20251031"` (`:29`),
1 CPU and 2048 MB (`:30-31`), and `allow_internet = true` (`:34`) — read only, never exercised. `Dockerfile`
(8 lines) is the image recipe: `WORKDIR /app` (`:4`), `pip install setuptools==80.9.0` (`:6`) and `COPY feal.py ./`
(`:8`); the captured `feal.py` is the 89-line Python implementation the agent is given, with the same cipher and a
`random.randint`-based `create_random_keys` (`:24-29`). The captured `solve.sh` is the task oracle, **own reading,
tier C** — not a registry row: it runs as the `oracle-solve-sh` case's recipe inside the sandbox and no finding
rests on its internal logic beyond the fact that the recipe returns a value the assert accepts. `setup.py` (12
lines) names the extension's sources (`:4`). The probe receipt (`corpus/evidence/round43/feal-probe.txt`) is the
lane's own re-runnable gate output, tier A for its own scope: these 12 end states against these captures, under
host `python3`, host `gcc` and the captured grader.

Disclosure: the 12 case predictions and their `violates=` tags were written from a static reading of
`tests/test_outputs.py`, `tests/feal.c`, `tests/feal_module.c`, `tests/test.sh` and `instruction.md` **before the
first recorded run** and frozen in `corpus/evidence/round43/feal-dry-cases-freeze.txt` (digest pinned in
`plans/pkg-spec-r43.json`). Six of the 12 (`nop`, `oracle-solve-sh`, `wrong-key`, `cheat-import-get_keys`,
`cheat-clock-seed`, `slow-oracle-45s`) had been graded on this host by the round-42 wave-1 planning seat
(`.ufo/waves/round-42/build/R42PlanNext/feal/feal_run1.txt`) with an unfrozen in-process harness; those six
re-observe prior results and the other six (`oracle-off-by-one`, `return-str`, `cheat-always-equal`,
`cheat-sysmodules-shadow`, `cheat-patch-get_keys`, `cheat-exit-zero`) were never graded before the freeze. Every
case carries `predicted_tests=` and `predicted=`; no prediction was edited after the run, and none needed to be.

## What is graded (static reading of test_outputs.py, feal.c, feal_module.c, setup.py, test.sh)

| Step | Mechanism | Lines |
|---|---|---|
| Entry point | `uvx -p 3.13` with `pytest==8.4.1`, `setuptools==80.9.0` and `pytest-json-ctrf==0.3.5`, then `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -v -rA`; one function is collected | `test.sh:17-22` |
| Reward | the shell maps the pytest exit status to `/logs/verifier/reward.txt`: `1` on 0, `0` otherwise — one bit, no partial credit | `test.sh:25-29` |
| Initial state | `WORKDIR /app`; `pip install setuptools==80.9.0`; `COPY feal.py ./` — the agent starts with the Python cipher and no `attack.py` | `Dockerfile:4`, `:6`, `:8` |
| Extension build | at grading time the test shells out: `(cd /tests && python setup.py build_ext --inplace)`, i.e. it compiles the captured `feal_module.c` + `feal.c` into `/tests` | `test_outputs.py:20`, `setup.py:4` |
| Import path | `sys.path.append("/app")` then `sys.path.append("/tests")`: `/tests` is searched first, so `feal_in_c` resolves to the freshly built extension, while `attack` exists only in `/app` | `test_outputs.py:22-23` |
| Module imports | `import attack` (the agent's module, its top-level code runs here) and then `import feal_in_c` (the reference extension) into the same interpreter | `test_outputs.py:24-25` |
| Key generation | `feal_in_c.create_random_keys()`: `srand(time(NULL))` once per process, then six `rand() & 0xFFFF` seeds, each multiplied by `1234567` | `test_outputs.py:27`, `feal.c:56-68` |
| The call | `stolen = attack.attack(feal_in_c.encrypt)` — the agent's function is handed the extension's `encrypt` as an ordinary Python callable; no subprocess, no timer | `test_outputs.py:29` |
| The assertion | `assert feal_in_c.get_keys()[5] == stolen` — the sixth round key, compared with whatever `attack` returned | `test_outputs.py:30` |
| The answer's surface | `get_keys` is exported as `METH_NOARGS` and returns all six keys as a list; `encrypt` is the only other operation | `feal_module.c:25-43`, `:47-53` |
| Cipher shape | four Feistel rounds; round `r` mixes with `key[r + 2]`, so `key[5]` enters the last round; `key[5]` is the graded value | `feal.c:83-88`, `feal.c:30-53` |

Five structural consequences follow from the reading alone.

- **The graded module and the answer live in the same interpreter.** `attack.attack` is called in the pytest
  process, after `feal_in_c.create_random_keys()` has written the six keys into a C global
  (`feal.c:6`, `:56-68`) that `get_keys` returns (`feal_module.c:26`, `:51`). Nothing separates the agent's
  namespace from the grader's: `import feal_in_c` inside `attack()` is an ordinary import of a module already on
  `sys.path` (`test_outputs.py:23`).
- **The import order is attack first, reference second.** `import attack` at `:24` runs the agent's module-level
  code before `import feal_in_c` at `:25`, so a module-level `sys.modules["feal_in_c"]` assignment is what `:25`
  binds.
- **The comparison is not type-checked.** `==` between an `int` and an arbitrary object falls back to the object's
  `__eq__` when `int.__eq__` returns `NotImplemented`; the assert at `:30` has no `isinstance` guard and no
  `type(...)` test. The instruction's "uint32 value" (`instruction.md:3`) is prose, not a graded type.
- **`get_keys` is looked up at assert time, not captured.** The binding at `:30` happens after `attack()` returned,
  so an `attack()` that rebinds `feal_in_c.get_keys` changes both sides of the comparison.
- **Exit status is the verdict, so leaving early is a pass.** `test.sh:25` reads `$?`; a process that exits 0
  without printing a verdict line is a pass for the probe too (receipt tag `exit=no-verdict-line`). Nothing bounds
  the call (`:29` is untimed), and the only ceiling is `task.toml:22`'s 1800 s verifier timeout.

## Located quotes

Quotes are byte-exact from the round-43 captures (`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`,
identical to the pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4`
clause. Straight double quotes inside a quote are the file's bytes.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the request is a chosen-plaintext key recovery | “Implement a chosen plaintext attack that recovers the value of key[5]” | `instruction.md:1` |
| the graded artefact is a Python module at an absolute path | “Your attack should be implemented in /app/attack.py” | `instruction.md:3` |
| the requested return type is a uint32 | “should return the uint32 value of key[5]” | `instruction.md:3` |
| the request states a 30-second budget | “Your attack should run in less than 30 seconds.” | `instruction.md:3` |
| each round key is derived from a 16-bit seed | “(Each of the 6 round keys is derived from a 16 bit seed.” | `instruction.md:4` |
| the extension is built by the test at grading time | “setup.py build_ext --inplace” | `test_outputs.py:20` |
| the agent's function receives the reference encrypt as an argument | “stolen = attack.attack(feal_in_c.encrypt)” | `test_outputs.py:29` |
| the whole value check is one equality against key index 5 | “assert feal_in_c.get_keys()[5] == stolen” | `test_outputs.py:30` |
| a key byte seed is the low 16 bits of rand() | “uint32_t x = rand() & 0xFFFF;” | `feal.c:65` |
| each key is a 16-bit seed times 1234567 | “key[i] = (x * 1234567) & 0xFFFFFFFF;” | `feal.c:66` |
| the last round mixes with key index 5 | “uint32_t mixed = f_function(right ^ key[round_num + 2]);” | `feal.c:84` |
| get_keys is a plain no-argument wrapper | “static PyObject* py_get_keys(PyObject* self, PyObject* args) {” | `feal_module.c:25` |
| get_keys is exported in the module's method table | “"get_keys", py_get_keys, METH_NOARGS” | `feal_module.c:51` |
| pytest runs the single captured test file | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -v -rA” | `test.sh:22` |
| the reward is the pytest exit status | “if [ $? -eq 0 ]; then” | `test.sh:25` |
| the extension is built from two captured C files | “"feal_in_c", sources=["feal_module.c", "feal.c"], include_dirs=["."]” | `setup.py:4` |
| the authors claim the test enforces the time limit | “Confirms the attack completes within the time limit” | `README.md:35` |
| setuptools is pinned in the image | “RUN pip install setuptools==80.9.0” | `Dockerfile:6` |

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the counter's
`V7` applies, computed over **all** violating cases and not from one convenient witness. The frozen table carries
five tags on two instruction lines; every tag has at least one violating case. Two tags are single-witness and both
are `unenforced` (`chosen-plaintext`, `time-30s`); one is single-witness and `enforced` (`attack-file`); two are
`partly` (`recover-key5` 7 cases, `return-uint32` 2 cases).

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:1` | `chosen-plaintext` | unenforced | `cheat-import-get_keys`, `cheat-always-equal`, `cheat-sysmodules-shadow`, `cheat-patch-get_keys`, `cheat-exit-zero`, `cheat-clock-seed` |
| `instruction.md:1` | `recover-key5` | partly | `nop`, `wrong-key`, `oracle-off-by-one`, `cheat-always-equal`, `cheat-sysmodules-shadow`, `cheat-patch-get_keys`, `cheat-exit-zero` |
| `instruction.md:3` | `attack-file` | enforced | `nop` |
| `instruction.md:3` | `return-uint32` | partly | `return-str`, `cheat-always-equal` |
| `instruction.md:3` | `time-30s` | unenforced | `slow-oracle-45s` |

The per-line reading:

- **1 (`chosen-plaintext`, `unenforced`).** The request asks for a "chosen plaintext attack", and six cases that
  do no differential cryptanalysis pass: the five cheats plus the clock replay. This is the widest gap in the
  receipt and the one the class names: the grader hands `attack()` the encryption oracle and the answer's public
  accessor in the same namespace, and then asks only whether one integer equals another.
- **1 (`recover-key5`, `partly`).** Three failing cases violate the sentence honestly (0, oracle+1, and the
  always-equal object that never names an int); four passing cases violate it just as honestly (the import,
  shadow, patch and exit cheats). The label `partly` records that the grader checks *a* value for key 5, not that
  the value was recovered by the requested method.
- **3 (`attack-file`, `enforced`).** The only violating case is `nop`, and it fails: with no `/app/attack.py`,
  `import attack` at `:24` raises `ModuleNotFoundError` inside the test. This is the one requirement whose
  violation is total, and it is enforced by the import itself, not by an existence check on a path.
- **3 (`return-uint32`, `partly`).** `return-str` returns the right key as a decimal string and fails, because
  `int == str` is False with no coercion; `cheat-always-equal` returns a non-int object with an always-true `__eq__`
  and passes. The type sentence is therefore enforced against a wrong *value* but not against a non-integer
  carrier, which is exactly the difference between "uint32" as prose and as an assertion.
- **3 (`time-30s`, `unenforced`).** The only witness sleeps 45 s after the correct answer and passes; nothing in
  `test_outputs.py` measures time. `README.md:35`'s sentence about the time limit is the authors' claim, and the
  receipt is the measurement against it.

### Contestable tags

The `violates=` tags are frozen with the predictions and are not edited; three deserve naming.

- **`chosen-plaintext` → `cheat-clock-seed`.** The case does call `encrypt_fn`, but as a check oracle over
  candidate keys, not as the differential chosen-plaintext pairs `instruction.md:4` describes. The tag is honest
  about the sentence and the `pass` is the coverage fact.
- **`recover-key5` → `cheat-exit-zero`.** The process dies before the assert, so the case never demonstrates a
  wrong value; the tag records that the requirement is not *seen* to be met, which is why a process-level exit is a
  coverage hole rather than a value error.
- **`return-uint32` → `cheat-always-equal`.** The returned object is not a uint32 at all; the tag is on the type
  sentence, and the pass is the reflected-`__eq__` mechanism, not a type hole in `int`.

## Case table

The 12 frozen cases in receipt order; the letter is the one test (`test_feal_differential_cryptanalysis_attack`)
and the verdict is that letter.

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | F | fail | no `/app/attack.py`, only the shipped `feal.py`, so the grader's import fails |
| `oracle-solve-sh` | P | pass | the task's `solve.sh` writes the reference differential attack |
| `wrong-key` | F | fail | `attack()` returns 0 |
| `oracle-off-by-one` | F | fail | the reference attack's result plus one |
| `return-str` | F | fail | the reference attack's result returned as a decimal string |
| `cheat-import-get_keys` | P | pass | `attack()` imports the reference module and returns `get_keys()[5]` |
| `cheat-always-equal` | P | pass | `attack()` returns an object whose `__eq__` is always True (no key, no int) |
| `cheat-sysmodules-shadow` | P | pass | importing `attack` installs a fake `feal_in_c` in `sys.modules`; `attack()` returns 0 |
| `cheat-patch-get_keys` | P | pass | `attack()` rebinds `feal_in_c.get_keys` to a constant and returns it |
| `cheat-exit-zero` | P | pass | `attack()` ends the grader process with `os._exit(0)` before the assert |
| `cheat-clock-seed` | P | pass | `attack()` replays the libc `srand(time(NULL))` schedule and checks candidates against `encrypt_fn` |
| `slow-oracle-45s` | P | pass | the reference attack followed by a 45 s sleep |

## Mechanism

One row per receipt case, in receipt order: the captured line that decides the case and a verbatim fragment of it.
The Findings section says, case by case, why that line decides it.

| Case | Decisive line | “Quote” |
|---|---|---|
| `nop` | `test_outputs.py:24` | “import attack” |
| `oracle-solve-sh` | `solve.sh:90` | “if (c1l ^ c2l) == 0x02000000:” |
| `wrong-key` | `test_outputs.py:30` | “assert feal_in_c.get_keys()[5] == stolen” |
| `oracle-off-by-one` | `test_outputs.py:30` | “feal_in_c.get_keys()[5] == stolen” |
| `return-str` | `test_outputs.py:30` | “assert feal_in_c.get_keys()[5]” |
| `cheat-import-get_keys` | `feal_module.c:51` | “"get_keys", py_get_keys, METH_NOARGS” |
| `cheat-always-equal` | `test_outputs.py:30` | “get_keys()[5] == stolen” |
| `cheat-sysmodules-shadow` | `test_outputs.py:25` | “import feal_in_c” |
| `cheat-patch-get_keys` | `test_outputs.py:29` | “stolen = attack.attack(feal_in_c.encrypt)” |
| `cheat-exit-zero` | `test.sh:25` | “if [ $? -eq 0 ]; then” |
| `cheat-clock-seed` | `feal.c:66` | “key[i] = (x * 1234567) & 0xFFFFFFFF;” |
| `slow-oracle-45s` | `task.toml:22` | “timeout_sec = 1800.0” |

## Findings, each tied to its receipt cases

1. **The module the grader requires is the module whose absence is the do-nothing failure (`nop` `F`).**
   `test_outputs.py:24` is `import attack`; with only the shipped `/app/feal.py` present, the import raises
   `ModuleNotFoundError` inside the pytest function and the harness exits 1 with no verdict line. Nothing checks
   `Path("/app/attack.py").exists()` first, so the failure is an import error rather than an assertion — the
   receipt records it verbatim (`ModuleNotFoundError -- no /app/attack.py (the shipped feal.py only)`). The
   Mechanism row points at `:24` because that is the line that decides: the graded artefact is loaded by name from
   `/app`, which `:22` puts first on `sys.path`.
2. **The task's own attack passes (`oracle-solve-sh` `P`).** `solve.sh` writes `/app/attack.py`; its inner loop
   filters 16-bit seed candidates by the differential condition at `solve.sh:90` and returns
   `(candidates[0]*1234567) & 0xFFFFFFFF`. The case is `P` because the recipe's output satisfies `:30`. This is a
   sanity anchor for the probe, not a claim that the oracle is correct on other key draws; the Mechanism row cites
   the filter line as the decisive step of the shipped approach.
3. **Returning any wrong integer fails exactly one comparison (`wrong-key` `F`; `oracle-off-by-one` `F`).** Both
   cases call `attack()` successfully and return an `int`; `:30` compares it with `get_keys()[5]` and raises
   `AssertionError`. There is one test, so the whole reward is that one equality. The difference between the two
   cases is only the arithmetic (`0` versus the correct value plus one), which is what makes the pair a value
   channel check rather than a shape check.
4. **A correct value in the wrong type fails, because `==` is not coercing (`return-str` `F`).** The case returns
   the reference result as `str`. `int.__eq__(str)` returns `NotImplemented` and `str.__eq__(int)` is `False`; the
   assert fails. This is the only receipt evidence that `instruction.md:3`'s "uint32" is enforced at all: the
   sentence is enforced against a wrong carrier of the right number, while the reflective `__eq__` below shows it
   is not enforced against a wrong type that claims equality.
5. **The answer is importable from the graded module (`cheat-import-get_keys` `P`).** `attack()` does
   `import feal_in_c` and returns `get_keys()[5]`. The extension is already built into `/tests` by `:20` and
   `/tests` is on `sys.path` from `:23`, so the import inside the agent's function resolves to the reference
   module; the assert compares the key with itself. The Mechanism row cites `feal_module.c:51`, the method-table
   entry that makes `get_keys` public; without that export the case could not exist.
6. **`int == object` dispatches to the object's `__eq__` (`cheat-always-equal` `P`).** `attack()` returns an
   `Anything()` whose `__eq__` returns `True`; the assert's left operand is an `int`, whose `__eq__` returns
   `NotImplemented` for an unrelated type, so Python calls the right operand's `__eq__` and the assertion passes.
   The decisive line is `:30` itself: there is no `isinstance(stolen, int)` and no `type(stolen) is int` anywhere in
   the test, so the claimed return type is only prose.
7. **The import order lets the agent's module own `feal_in_c` (`cheat-sysmodules-shadow` `P`).** `import attack` at
   `:24` runs before `import feal_in_c` at `:25`; the case's module-level code assigns
   `sys.modules["feal_in_c"] = _fake`, so the grader's second import binds the fake, `create_random_keys()` is a
   no-op, `get_keys()` is `[0,0,0,0,0,0]` and `attack()` returns 0 — the assert compares 0 with 0. The Mechanism
   row cites `:25` because that is the line the shadowing defeats; `:24` is the line that permits it.
8. **The accessor is resolved after the call (`cheat-patch-get_keys` `P`).** `attack()` rebinds
   `feal_in_c.get_keys` to a lambda returning seven at index 5 and returns 7; `:30`'s `feal_in_c.get_keys` is a
   fresh attribute lookup performed after `:29` returned, so both sides are 7. The Mechanism row cites `:29`
   (where the agent's code gets to run against the live module); `:30` is the line whose late binding makes the
   rebinding effective.
9. **The verdict is a process exit status, so a process can win by leaving (`cheat-exit-zero` `P`).**
   `attack()` calls `os._exit(0)`; the harness dies before the assert and `test.sh:25` writes reward 1 because
   `$?` is 0. The probe's own harness follows the same rule, tagging the case `exit=no-verdict-line`, and pytest
   would also have exited 0. The Mechanism row cites `test.sh:25` because that is the line that turns "no verdict"
   into a pass.
10. **The key schedule is replayable from the clock (`cheat-clock-seed` `P`, `host=libc-rand`).**
    `create_random_keys()` seeds libc once per process with `time(NULL)` (`feal.c:60-62`) and builds each key as
    `(rand() & 0xFFFF) * 1234567` (`:65-66`); `test_outputs.py:27` runs it in the same process. The case tries
    `srand(now + dt)` for ten offsets, derives six keys, and accepts the schedule whose `encrypt` reproduces
    `encrypt_fn` on three plaintexts. The Mechanism row cites `:66`, the multiplication that makes each key a
    function of a 16-bit draw; that is what bounds the replay. The verdict is a host fact: it depends on the host
    C library's `rand()` sequence (glibc here, Debian bookworm glibc in the image).
11. **Nothing times the call (`slow-oracle-45s` `P`).** `:29` is a plain call; the case returns the correct key
    after `time.sleep(45)` and the assert still passes. The only ceiling in the captured material is
    `task.toml:22`'s `timeout_sec = 1800.0` for the verifier, which is 60 times the requested budget and does not
    fail the case — it would only kill a much slower process. The Mechanism row cites that line because it is the
    only time bound the grader's environment actually carries.
12. **The last round is where key index 5 is used, which is why index 5 is the graded one (`oracle-solve-sh` `P`
    and `wrong-key` `F` together).** `:30` reads index 5; `feal.c:84`'s `key[round_num + 2]` uses index 5 in the
    fourth round (`round_num == 3`), and `feal.c:76-77` whiten with indices 0 and 1. The differential attack in
    `solve.sh` recovers exactly that round key by the characteristic at `solve.sh:90`. The Mechanism row for the
    oracle cites that filter line; finding 3's pair is what shows the index, not the value's provenance, is what
    the assert reads.

## Regrade (second grading of the same end state)

The probe's harness is imported once per grading process and calls the one test function twice: the `grade` run and
a second, **fresh harness process** over the same built state, under the tags `TEST` and `REGRADE`; the second pass
is reported (`regrade=same` / `regrade=DIFF:<letter>`) and never used for the verdict. The receipt is
`regrade cases=12 differ=0`. Two properties matter for reading it. The end state is fixed between the passes —
`/app`, `/tests` and the built `feal_in_c` extension are the same files — so the second process re-imports the same
code. But `create_random_keys()` runs again in the second process and re-seeds from `time(NULL)`, so the two passes
are two independent key draws, not two evaluations of one key. `regrade=same` on the eight passing cases therefore
says the attack or cheat still passes on a second key draw (for `oracle-solve-sh` that is a real, if narrow,
re-execution), and on the four failing cases it says the failure is not a fluke of one draw. It is a determinism
read of this probe, not a general re-run-stability claim: the clock-seed case depends on the host libc, and two runs
seconds apart can see the same or adjacent seeds.

## What the probe does not show

- **The task image is never pulled; the host's tools stand in.** `task.toml:29` names
  `alexgshaw/feal-differential-cryptanalysis:20251031`; `Dockerfile:2` is `python:3.13-slim-bookworm`; `test.sh:4-9`
  installs `gcc`, `curl` and uv 0.9.5 from the network and `:17-22` runs pytest under `uvx -p 3.13`. The probe uses
  host `/usr/bin/python3` (3.14 on this host), host `/usr/bin/gcc` and the host's setuptools, imports the captured
  module directly and calls the one test function itself, so the image's gcc version, the pinned
  `pytest==8.4.1`, `setuptools==80.9.0`, `pytest-json-ctrf==0.3.5`, the ctrf report and the 1800 s verifier timeout
  (`task.toml:22`) are untested.
- **`tests/test.sh` was not executed.** The reward mapping is read (`test.sh:17-29`), not run: `apt-get`, the
  network uv install and `/logs/verifier/` are outside the sandbox. `observed_pass` means "the test function
  returned without raising", which is what makes pytest exit 0 — not that `reward.txt` was written.
- **Real pytest was not run.** The harness maps the one test function's outcome onto pytest's exit status,
  including the `os._exit(0)` path. Pytest's own collection, import errors and `pytest-json-ctrf` behaviour are
  therefore untested here; a pytest-parity re-run is a wave-1 item on this round's list, and this entry does not
  claim it happened.
- **The 12 cases are the claim's whole surface.** They were fixed before the first recorded run. States outside
  them — an `attack()` that reads `/tests/feal.c` or `/tests/test_outputs.py` while they exist, an attack that
  subclasses the returned int, a cheat that patches `feal_in_c.encrypt` rather than `get_keys`, a process that
  writes the ctrf file itself, a harness whose cwd differs, and every AI-agent trajectory — are not covered and
  are not claimed.
- **`cheat-clock-seed` is a host fact.** Its verdict rests on the host C library's `rand()` sequence and on
  `time(NULL)` moving by no more than the replay window; the receipt flags it `host=libc-rand`. On a different
  libc, or a clock that jumps, the shaped cheat can fail, and that would not contradict any other case.
- **No separation between "the module imported" and "the module behaves".** The probe writes `/app/attack.py`
  verbatim and grades; it does not model how an agent would arrive at one, and it does not measure whether the
  instruction is solvable within its stated 30 s by any method other than the shipped `solve.sh`.
- **Not a statement about the task's validity, difficulty or solvability.** That is PROVINCE's question, not this
  lane's; `difficulty = "hard"` (`task.toml:15`) and the 8-hour expert estimate (`:18`) are the authors' metadata,
  read only. Nothing here measures whether a real agent would take any of the shortcuts.
- **The captures' provenance.** The twelve files were fetched at `2fd12b88` by the L1 on 2026-10-26 and pinned in
  `SHA256SUMS` and in `plans/pkg-spec-r43.json`; that they are the files the authors ship today rests on those
  digests, not on a fetch by this seat.

## Prior art

**SLOT: L1 fills this section from `R43ScoutPriorArt` (round-43 wave 1).** This seat ran no tracker search and
therefore asserts nothing about the absence or presence of published reports on this grader. What is claimed
without novelty is only the class sentence in the Summary: an agent-authored Python module imported into the
grader's own interpreter beside the reference extension whose `get_keys()` holds the answer, with the pytest exit
status as the verdict. The lane's own `knowledge/tb2-regex-log-grader.md` already executes an agent-authored regex
in-process, so the import-and-call shape is an extension of an existing class, not a first instance. Every finding
above rests on the frozen 12-case receipt, not on any prior statement.

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated, too easy or unsolvable (no image run,
no agent, no trajectory); that an agent would write any of the five cheats (they are constructed modules, not
observed behaviour); that the grader should sandbox the agent's module, time the call, or type-check the return (no
such proposal is described or judged here); that the 30 s sentence is wrong as a design (the entry records that
nothing measures it, not what should); or anything about how Harbor executes this verifier
(`benchmark-verifier-execution-model.md` covers where it runs and what it restores).

Nor: **contamination** — `test_outputs.py:1-2` and `Dockerfile:1` carry the canary banner and these captures exist
for digest-pinned re-execution, not as a contamination measurement; **the image's toolchain** — host python, host
gcc and host setuptools are the probe's instruments, and parity with `uvx -p 3.13` and Debian gcc is untested;
**the oracle's correctness** — `solve.sh` runs as one case's recipe and passes on two key draws, which says nothing
about other draws or other inputs; **prevalence** — one task, 12 states, no tracker sweep by this seat; **the
instruction's intent** — whether "chosen plaintext attack" was meant to exclude an oracle-checking replay is the
authors' question, and the entry only records that the grader cannot tell the difference.

**Falsifier.** This entry is falsified if (a) a re-fetch of the six pinned URLs yields bytes whose SHA-256 differs
from `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/SHA256SUMS` and the pins in
`plans/pkg-spec-r43.json`; (b) a fresh run of `plans/feal_probe.py --lane .` prints anything other than
`cases=12 observed_pass=8 observed_fail=4 mismatches=0` and `regrade cases=12 differ=0` — in particular if
`oracle-solve-sh`, `cheat-import-get_keys`, `cheat-always-equal`, `cheat-sysmodules-shadow`,
`cheat-patch-get_keys`, `cheat-exit-zero`, `cheat-clock-seed` or `slow-oracle-45s` is observed `fail`, or if `nop`,
`wrong-key`, `oracle-off-by-one` or `return-str` is observed `pass`; (c) a line of `test_outputs.py` is shown to
type-check `stolen`, to run `attack()` in a subprocess, to measure the call's duration, to read `get_keys` before
`attack` runs, or to import `feal_in_c` before `attack`; (d) `feal_module.c` is shown not to export `get_keys`, or
to export it in a form that cannot be called with no arguments; (e) `test.sh` is shown to compute the reward from
anything other than the pytest exit status; or (f) `feal.c` is shown to seed the key schedule from something other
than `time(NULL)` or to use more than 16 bits per key seed.
