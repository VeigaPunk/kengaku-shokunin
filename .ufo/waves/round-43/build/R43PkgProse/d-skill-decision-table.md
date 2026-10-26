# block d — SKILL.md, append after `:1204` (end of the round-42 `Simulator-executed data-artefact TB2 grader` section)

## In-process module-import TB2 grader — round 43

Before citing the pinned TB2 `feal-differential-cryptanalysis` scorer, run `python3 plans/feal_probe.py --lane .` and
read its summary line: exit `0` means only that all 12 cases produced two verdicts each — a prediction mismatch does
not change the exit code, it is printed as `match=NO` on the case line and counted in `mismatches=`; exit `1` is a
`--stage-check` failure; exit `2` is a setup failure (duplicate or malformed case id, unknown tag, malformed
prediction, a capture missing or off its pinned digest, `/usr/bin/bwrap`, `python3`, `bash` or `gcc` not executable,
an uncreatable `--work`, or a case whose recipe exited non-zero). `--dry` and `--stage-check` are not evidence. The
receipt's summary (`corpus/evidence/round43/feal-probe.txt:23`) reads `cases=12 observed_pass=8 observed_fail=4
mismatches=0`, and grading each end state a second time in the same process agrees case by case (`regrade cases=12
differ=0`, `:22`).

The class is new: the graded artefact is an **agent-authored Python module imported into the grader's own
interpreter**. One test function does everything (`tests/test_outputs.py:7-30`): it shells out to build the task's C
extension in `/tests` (`print(os.popen("(cd /tests && python setup.py build_ext --inplace)").read())`, `:20`),
appends `/app` and then `/tests` to `sys.path` (`:22-23`), runs `import attack` (`:24`) and `import feal_in_c` (`:25`),
calls `feal_in_c.create_random_keys()` (`:27`), hands the C `encrypt` to the module (`:29 stolen =
attack.attack(feal_in_c.encrypt)`) and asserts `feal_in_c.get_keys()[5] == stolen` (`:30`). `tests/test.sh:17-25` runs
that one test under `uvx -p 3.13` (pytest 8.4.1, setuptools 80.9.0) and writes `/logs/verifier/reward.txt` from
pytest's exit status — so the module runs in the same interpreter and process as the reference extension, and
`get_keys()` returns the live `uint32_t key[6]` as a six-element list (`tests/feal_module.c:25-43`, method table `:51`).
`create_random_keys()` seeds libc once per process (`srand(time(NULL))` behind a static flag) and derives each key as
`(rand() & 0xFFFF) * 1234567` (`tests/feal.c:56-67`): six 16-bit seeds, which `instruction.md:4-6` states as a hint and
which also makes the key schedule a clock read.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `sys.path.append("/app")`, then `"/tests"`, then `import attack` (`test_outputs.py:22-24`) | a module that imports the reference implementation and returns its key: `cheat-import-get_keys` passes (`P`) | which module answered; whether the attack did any work | `cheat-import-get_keys` (receipt:15) |
| `feal_in_c.get_keys()[5] == stolen` with `stolen` any object (`:30`) | an object whose `__eq__` returns True passes: `int.__eq__` returns `NotImplemented` for a non-int and the reflected comparison decides the assert (`cheat-always-equal`, `P`) | that the returned value *is* the int — `type(stolen) is int`, or a comparison in the other direction | `cheat-always-equal` (receipt:16) |
| `import attack` runs **before** `import feal_in_c` (`:24-25`) | a module that installs a fake `feal_in_c` in `sys.modules` at import time is what `:25` binds, and every later call goes to the fake (`cheat-sysmodules-shadow`, `P`) | import order and module identity; a private name for the reference, or a fresh subprocess | `cheat-sysmodules-shadow` (receipt:17) |
| the reference module is looked up again **after** `attack()` returns (`:29-30`) | rebinding `feal_in_c.get_keys` to return a constant before returning that constant passes (`cheat-patch-get_keys`, `P`) | attribute identity before and after the call | `cheat-patch-get_keys` (receipt:18) |
| pytest's exit status as the whole verdict (`test.sh:22`, `:25`) | `os._exit(0)` inside `attack()` ends the grader process with status 0, `test.sh` writes reward 1, and the assertion never runs (`cheat-exit-zero`, `P`, `exit=no-verdict-line`) | that a verdict line exists at all — `test.sh:25` writes the reward from the exit status alone, so a process that exits before pytest reports is indistinguishable from a pass | `cheat-exit-zero` (receipt:19) |
| the SAME interpreter's libc rand state, seeded once per process (`feal.c:56-67`) | replaying `srand(time(NULL))` through libc with the current time and filtering candidates against the passed `encrypt` reproduces `key[5]` (`cheat-clock-seed`, `P`, `host=libc-rand`) | whether the "attack" is a clock read; the real entropy is 16 bits per round key | `cheat-clock-seed` (receipt:20) |
| `stolen = attack.attack(feal_in_c.encrypt)` — the call is never timed (`:29`) | the reference attack plus a 45 s sleep passes (`slow-oracle-45s`, `P`) although `instruction.md:3` asks under 30 s; the only bound in the capture is `task.toml:22`'s 1800 s verifier timeout | a wall-clock measurement inside the test; `README.md:35` claims the test confirms the limit and it does not | `slow-oracle-45s` (receipt:21), `README.md:35`, `task.toml:22` |
| the argument is the C `encrypt` bound to the six C keys (`:29`; `feal_module.c:12-22`) | the analysis must target the passed function: the shipped `/app/feal.py` keeps its own `random`-seeded keys (`feal.py:24-29`) and is not the grading cipher; the oracle's differential attack passes (`oracle-solve-sh`, `P`) | which ciphertexts came from — the passed `encrypt_fn`, not the `/app` copy | `oracle-solve-sh` (receipt:11) |
| `import attack` with no `/app/attack.py` (`:24`) | the test errors out (`ModuleNotFoundError`): `nop` fails (`F`), and the shipped `feal.py` alone is not an attack module | that a module exists at `/app/attack.py` with an `attack` callable | `nop` (receipt:10) |
| the asserted value and its type (`:30`) | a wrong int (`wrong-key`), the oracle's result plus one (`oracle-off-by-one`) and the oracle's result as a decimal string (`return-str`) all fail (`F`) | the exact integer; `uint32`, not a string | `wrong-key` (receipt:12), `oracle-off-by-one` (receipt:13), `return-str` (receipt:14) |
| the build at `:20` — printed, never asserted | no case witnesses a build failure: a broken build surfaces only as an `ImportError` at `:25` | the build's stderr; that `setup.py:3-5` names the captured sources | code read only (`test_outputs.py:20`, `setup.py:3-5`) |

V7 labels derived from the receipt (frozen tag lines,
`corpus/evidence/round43/feal-dry-cases-freeze.txt:1-5`: `chosen-plaintext` `instruction.md:1`, `recover-key5` `:1`,
`attack-file` `:3`, `return-uint32` `:3`, `time-30s` `:3`): `attack-file` **enforced** (1 case, 0 pass — `nop`);
`recover-key5` **partly** (7 cases, 4 pass — the three failing key cases plus `cheat-always-equal`,
`cheat-sysmodules-shadow`, `cheat-patch-get_keys`, `cheat-exit-zero`); `return-uint32` **partly** (2 cases, 1 pass —
`return-str` fails, `cheat-always-equal` passes); `chosen-plaintext` **unenforced** (6 cases, 6 pass);
`time-30s` **unenforced** (1 case, 1 pass — `slow-oracle-45s`). Every label is a property of this frozen 12-case set
only, not a reading of the instruction prose.

Limits: the probe never runs the task image (`task.toml:29`, `allow_internet = true` at `:34`, never pulled) or a
harness; host python3, host gcc and host setuptools stand in for the image's python 3.13 under `uvx`, Debian gcc and
setuptools 80.9.0; pytest itself is not run — the harness maps the one test function onto pytest's exit status, so
pytest parity is unverified; recipes run unprivileged; each case stages its own `/app` and `/tests`; the cases are
constructed modules, not agents. `cheat-clock-seed` is a host fact (`host=libc-rand`): the replay works because the
grader's own process seeded libc moments earlier. A property of this capture at `2fd12b88`; not a task-validity,
difficulty or gameability verdict, not solver advice, not a statement about differential cryptanalysis, the FEAL
cipher or Python's import system in general, and not a statement about any agent's behaviour. (Draft `R43PkgProse`
block d; the L1 condenses at integration.)
