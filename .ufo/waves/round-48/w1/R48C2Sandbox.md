# R48C2Sandbox — probe isolation / host-safety review

## Axes

- **Probe isolation integrity:** host paths and writes remain outside the sandbox.
- **Host-safety:** scratch and lane boundaries remain respected.
- **Bypass surface:** whether a hostile case can escape via path/symlink or unbounded resources.
- **Frozen-contract / ordering:** no full or scored probe/counter execution before stage 2.

## Evidence and commands

Measured revision: `REV a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze; `git log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af` printed `a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`). Scratch clone top-level was `/fast/scratch/hyaku/kengaku-r48/R48C2Sandbox/lane`, `HEAD` matched that revision, and status had 0 lines.

Commands run:

- `git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`
- `git -C lane checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`
- `python3 plans/polyglot_c_py_probe.py --lane . --dry` — printed all seven tags, 18 cases, `cases=18 predicted_pass=7 predicted_fail=11`; dry-only, no sandbox/case execution.
- `python3 plans/polyglot_c_py_probe.py --lane . --stage-check` — all 18 cases matched expected file shape; final output `stagecheck cases=18 failed=0`. This mode writes/builds only inside the disposable bwrap `/app`; it performs Python `compile()` and `gcc -fsyntax-only`, not imports, grader invocation, linking, or candidate execution.
- Scratch-only bwrap boundary attempt, mirroring probe mounts: a symlink in sandbox `/app/escape` targeted a host-side sentinel path under the seat scratch; writing through it failed (`/usr/bin/bash: line 1: /app/escape: No such file or directory`), exit 0 for the negative-control assertions, host sentinel remained exactly `HOST_SENTINEL`, and `/tmp` write was private. No lane or host file was modified.

Source files inspected (local lane snapshot):
- `plans/polyglot_c_py_probe.py`: sandbox argv uses `--unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session`, read-only `/usr` and `/etc`, private `/tmp`, writable per-case `/app`, read-only `/tests`, `/pub`, `/tpl`, fixed `PATH`, and a 1800-second subprocess timeout. Located quote (16 words): “/app is a fresh writable directory: the task image has `WORKDIR /app`” (probe docstring, lines 17–20).
- `plans/round46_c3_verify.py`: identified the counter’s bwrap predictor harness and its separate fixed `SANDBOX_ENV`; no counter was run.
- `plans/order_check.py`: inspected the frozen receipt/order guard; did not run it.
- `plans/pkg-spec-r46.json`: pins the upstream source URL `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`. This URL was not fetched during this review. The local probe’s located description of the pinned grader is: “`os.listdir("/app/polyglot")` must equal `["main.py.c"]` exactly” (12 words; probe docstring, lines 25–27). Local evidence inspection date: 2026-10-27.
- Required governing source `plans/round-48-claims.md` and routed source `corpus/lessons/round-46-verifier-spotcheck.md` were read first; stage-1 claim says no C2 probe before stage 2 and permits only `--dry`/stage-check beforehand.

## Review

**Positive:** the examined mount layout and scratch bypass control deny a direct symlink path from writable `/app` to a host path; `/tmp` is a private tmpfs. Stage-check completed on the frozen scratch clone only. The C2 stage-2 counter is absent at the measured revision, so no scored run was attempted. No package probe `grade` mode or counter execution was run.

**Counterexample / remaining host-safety gap:** sandboxing is filesystem/network/process-namespace isolation, not resource isolation. The probe gives each bwrap run a 1800-second timeout, but the argv and environment expose no CPU, memory, process-count, or writable-byte quota. A hostile executable/case can consume host CPU/memory or fill the scratch filesystem through `/app` until the timeout/space exhaustion. The scratch path being an NVMe volume does not enforce a per-run quota. I deliberately did not execute a resource-exhaustion attack.

**Impacted axes:** host-safety and probe isolation integrity (availability); coverage only insofar as the probe can fail from shared-host exhaustion. This does not falsify the observed path/network isolation or the frozen C2 predicate, but it is a genuine containment tradeoff if probe inputs become attacker-controlled.

**Smallest safe correction:** if hostile execution is in scope, run bwrap beneath a per-process resource controller with explicit memory, CPU-time, pids, and scratch-byte limits, plus a shorter wall timeout; preserve the frozen case table, predicates, P10 ordering, and input pins. Alternatively explicitly scope the trust boundary to trusted frozen recipes/package bytes, in which case no predicate change is needed. Do not run the full probe before stage 2.

## Limits

No full probe execution, scored counter, order-check execution, network request, mutation test, or resource-exhaustion attempt. The bwrap attack was a minimal scratch-only host-path/private-tmp control, not a comprehensive sandbox escape assessment. I installed or updated no tools.

VERDICT: **No direct host-path escape reproduced in the permitted scratch control; resource-exhaustion containment remains unbounded and untested. C2 claim admission not assessed.**
