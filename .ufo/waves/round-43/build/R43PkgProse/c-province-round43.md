# block c — PROVINCE.md, append after `:568` (end of the round-42 routing paragraph)

One unwrapped `**Core addition:**` line names both `feal-differential-cryptanalysis` and
`tb2-feal-differential-cryptanalysis-grader.md` (C2 V9(c)); the routing clause at the end names the two unowned
domains with the exact sweep.

## Round43 partial frontier admission (2026-10-26)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader — `feal-differential-cryptanalysis/tests/test_outputs.py` with `tests/feal_module.c`, `tests/feal.c` and `tests/test.sh` at terminal-bench-2 `2fd12b88` — over 12 frozen end states, via `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (S129, S130, S131, S132, S133, S134), `plans/feal_probe.py` and receipt `corpus/evidence/round43/feal-probe.txt` (`cases=12 observed_pass=8 observed_fail=4 mismatches=0`; `regrade cases=12 differ=0`).

The graded state is a class new to this lane: not a fixed artefact read by an assertion, not a model computed inside
the test, and not a program in a data format executed by a grader-compiled interpreter, but an **agent-authored
Python module the grader imports into its own interpreter and calls**. One test function does everything
(`test_outputs.py:7-30`): it builds the task's C extension in `/tests` through a shell (`python setup.py
build_ext --inplace`, `:20`, output printed and never asserted), appends `/app` and then `/tests` to `sys.path`
(`:22-23`), imports the agent's `attack` and then the reference `feal_in_c` (`:24-25`), seeds the C keys
(`:27 create_random_keys()`), hands the C `encrypt` to the module (`:29 stolen = attack.attack(feal_in_c.encrypt)`)
and compares the answer with `feal_in_c.get_keys()[5]` (`:30`). `tests/test.sh:17-25` runs that one test under
`uvx -p 3.13` with pytest 8.4.1 and writes `/logs/verifier/reward.txt` from pytest's exit status, so an exit before
the assertion is a pass. The extension exports `get_keys()` as a six-element list of the live `uint32_t key[6]`
(`feal_module.c:25-43`, `:51`), `create_random_keys()` seeds libc once per process (`srand(time(NULL))`, a static
`seeded` flag) and derives each key as `(rand() & 0xFFFF) * 1234567` (`feal.c:56-67`) — a 16-bit seed per round key,
which `instruction.md:4-6` states as a hint and which is also a clock read an attack can replay through libc.

Observed on the 12 frozen cases: eight pass and four fail, with no prediction mismatch (`cases=12
observed_pass=8 observed_fail=4 mismatches=0`, receipt:23) and a second, same-process grading of each end state
agreeing case by case (`regrade cases=12 differ=0`, receipt:22). The four failures are the shapes that return nothing
or the wrong value: no `/app/attack.py` at all (`nop`, a `ModuleNotFoundError` at `test_outputs.py:24`, receipt:10),
`attack()` returning 0 (`wrong-key`, receipt:12), the reference attack's result plus one (`oracle-off-by-one`,
receipt:13) and that result returned as a decimal string (`return-str`, receipt:14). The eight passes split into the
task's own oracle (`oracle-solve-sh`, the `solve.sh` differential attack, receipt:11) and **six passes that never
recover a key**: returning `feal_in_c.get_keys()[5]` (`cheat-import-get_keys`, receipt:15), returning an object whose
`__eq__` is always True (`cheat-always-equal`, receipt:16 — `int.__eq__` returns `NotImplemented` for a non-int and
the reflected comparison decides the assert), installing a fake `feal_in_c` in `sys.modules` at import time
(`cheat-sysmodules-shadow`, receipt:17), rebinding `feal_in_c.get_keys` before the assert reads it
(`cheat-patch-get_keys`, receipt:18), `os._exit(0)` inside `attack()` before the assertion ever runs
(`cheat-exit-zero`, `exit=no-verdict-line`, receipt:19), and replaying the C key schedule from the current time
through libc and checking candidates against the passed `encrypt` (`cheat-clock-seed`, `host=libc-rand`,
receipt:20) — plus a ninth pass that is the reference attack followed by a 45 s sleep (`slow-oracle-45s`, receipt:21).
Nothing measures that sleep: `instruction.md:3` asks for under 30 s and `README.md:35` says the test "Confirms the
attack completes within the time limit", but `test_outputs.py:29` does not time the call and the only time bound in
the capture is `task.toml:22`'s 1800 s verifier timeout. It records how that captured grader answers those synthetic
states only: it does not run Terminal-Bench, the task image (`task.toml:29` names
`alexgshaw/feal-differential-cryptanalysis:20251031`; `allow_internet = true` at `:34`; the image is never pulled) or a
harness (`tests/test.sh`'s `uvx -p 3.13`/pytest path and its `/logs/verifier/reward.txt` write are read, not run),
does not validate or certify the task, measure difficulty, gameability or contamination, and does not speak for the
remaining 80 TB2 task graders (89 carry `tests/test.sh`; 9 are read). Limits: host python3 3.14, host gcc and host
setuptools stand in for the image's python 3.13 under `uvx`, Debian gcc and setuptools 80.9.0; pytest is not run — the
harness maps the one test function onto pytest's exit status, so a pytest-parity check is an open item; recipes run
unprivileged rather than as root; each case stages its own `/app` and `/tests`, so no case observes the image's tree;
the cases are constructed modules, not agents. Disclosed ordering: before the freeze the probe ran only `--dry` and
`--stage-check` (`stagecheck cases=12 failed=0`, `.ufo/waves/round-43/claims/c2-stage-check.txt`), and round-42 wave-1
seat `R42PlanNext` had graded seven shapes on this host with an unfrozen in-process harness
(`.ufo/waves/round-42/build/R42PlanNext/feal/feal_run1.txt`); six of these twelve cases re-observe those shapes (`nop`,
`oracle-solve-sh`, `wrong-key`, `cheat-import-get_keys`, `cheat-clock-seed`, `slow-oracle-45s`) and
`oracle-off-by-one`, `return-str`, `cheat-always-equal`, `cheat-sysmodules-shadow`, `cheat-patch-get_keys` and
`cheat-exit-zero` were never graded before the freeze (`plans/round-43-claims.md` §C2).

Round-43 routing (from the `R43PkgProse` draft; L1 confirms). This lane owns what the captured grader checks and what
passes it — nothing else. **Two findings are unowned: whether a differential attack on this FEAL-like variant is
correct or strong enough to recover `key[5]` inside 30 seconds (cryptanalysis technique), and Python import-system
semantics as a subject — `sys.path` search order, `sys.modules` substitution, the reflected-comparison fallback of
`int.__eq__`, extension-module shadowing — beyond the single verdict they decide here.** Named sweeps, 2026-10-26 from
`/home/vgpnk/Projects/shokunin`: `for pat in "cryptanalys" "cipher" "differential cryptanalysis" "sys.modules" "import
system" "importlib" "python semantics" "interpreter semantics"; do grep -ril "$pat" --include=PROVINCE.md
*/PROVINCE.md; done` returns **0 files for every pattern**, and `grep -rin "cryptanalys\|block cipher\|differential
cryptanalysis" --include=SKILL.md */SKILL.md` and `grep -rin "sys.modules\|import system\|import machinery"
--include=SKILL.md */SKILL.md` both return **no hits**; the only near-misses are `kotodama-shokunin/SKILL.md:24` ("a
cipher of English", a conlang sense), `kaidoku-shokunin/SKILL.md:893` (pcap encryption hiding layers) and
`chousa-shokunin/SKILL.md:116` (`importlib` leaving `__pycache__` beside a harness's candidate — a side note about its
own tool, not a domain declaration). So any finding of that kind routes to the orchestrator rather than being absorbed
here, and no sibling is credited with owning it. Advising an agent how to attack this cipher, and prior-art pricing of
differential cryptanalysis on FEAL, are likewise not this lane's: the task's own `solve.sh` is executed as one case
and observed pass, nothing more. Terminal-Bench's task, image and oracle stay the benchmark's; the round35-42
paragraphs above stay as written, and this paragraph narrows only their "remaining TB2 tasks" clause for this one task.
