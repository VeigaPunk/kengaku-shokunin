ATTACKS: Round-25 calibration/state instruments under a network-less namespace

- Executed from a pristine `git archive 8ea41f9ed` copy at `/tmp/k25w2-SentinelNetns/archive`; each invocation used `unshare -rn strace -f -c -e trace=%network,%process`.
- `python3 plans/attrib_calibration.py --summary`: exit 0; `TOTAL ... scored_trials=92 correct=92 incorrect=0 ... mismatches=0`; strace recorded 1 `execve` (the instrument) and no `%network` syscalls.
- `python3 plans/attrib_calibration.py --selftest`: exit 0; `selftest: 14 checks, 0 failed`; strace recorded 7 `wait4`, 7 `clone3`, 8 `execve` (instrument plus seven fixture CLI runs), and no `%network` syscalls.
- `python3 plans/state_check.py --summary`: exit 0; `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3`; `VERDICT: PASS — all comparable frozen assertions match`; strace recorded 2 `vfork`, 2 `wait4`, 27 `execve` calls (24 errors), and no `%network` syscalls.
- `python3 plans/state_check.py --selftest`: exit 0; `[selftest] ALL PASS (...)`; strace recorded only the initial `execve`, with no subprocess or `%network` syscalls.
- `plans/state_check.py:170-180` hardcodes the only allowed commands: `("python3", "grader.py")` and `("python3", "plans/attrib_probe.py", "freeze-check", "--frozen", "plans/attrib-r23-frozen.md")`. `:305-325` rejects non-allowlisted vectors and calls `subprocess.run(command, cwd=self.root, ...)`; `shell` is omitted, so Python's default `shell=False` applies. The two child processes observed in summary tracing match these two allowed invocations.
- `plans/attrib_calibration.py:825-828` also uses an argv list for its selftest CLI probes; its seven subprocess runs match the trace counts.
- No installs or updates.

VERDICT: SURVIVES — all four requested runs exited 0; the traced invocations made no network syscalls, and state-check subprocess execution is allowlisted and shell-free.