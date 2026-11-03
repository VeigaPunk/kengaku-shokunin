# SecurityScan — round 67 w1 (R67-C1 sandbox and lane files)

Scope: read-only adversarial review of `plans/round67_c1_pipeline_probe.py` (`run_case` bwrap argv, `run()` lock handling, `check_receipt`), the six case files, and the committed round-67 source captures. No edits to the lane; no grader run; no listener on 12355. Sandbox experiments were run with a standalone bwrap argv (same flags as `run_case`) and a host listener on 127.0.0.1:23456. Every observed value below was produced by a command listed in `evidence.txt` in this seat dir.

Probe line numbers refer to `plans/round67_c1_pipeline_probe.py` (unchanged, sha256 `32bacf1d…b836` per the receipt's PROBE line).

## Must-fix

**M-1 — the results channel is writable by the code under test; a forged junit passes the predicate.**
- Where: `run_case` line 167 (`--bind <ctl> /ctl`, the only writable bind besides tmpfs `/tmp`); line 177 (`--junitxml=/ctl/junit.xml`); line 188 (`junit` read from the host side after bwrap exits); `check_receipt` derives the vector from the copied junit and nothing else (lines 241 onward).
- Mechanism: the candidate `pipeline_parallel.py` runs inside the same sandbox as pytest (its module is imported in the `mp.spawn` children). A process it starts can write `/ctl/junit.xml` after pytest has written its verdict and before the PID namespace is torn down.
- Reproduced (`forgery-demo.sh`, scratch only): the sandbox wrote `REAL-FAIL`, a daemon rewrote it to `FORGED-ALL-PASS` while the sandbox was still alive; the host read `FORGED-ALL-PASS` (`evidence.txt` E9). A forged file yields a VECTOR line that `--check-receipt` accepts, because the junit sha and the vector both come from the forged bytes.
- Scope of exposure: all six frozen cases are lane-authored. The committed junit failure causes match the frozen table: q3 `NotImplementedError: stub: pipeline schedule not implemented`; q5 `too many layers: 8`; q6 `mismatch at lm_head.bwd, microbatch 0, max diff=0.10`; q2/q4 failures at the expected tests (receipt.junit, observed with grep). This is consistent with genuine runs; it is not proof, since content alone cannot distinguish a forged junit.
- Impact: the probe's verdict on any candidate that is not lane-authored is not trustworthy. The R67-C1 counter is not invalidated for the six frozen cases (no kill rule triggered), but the receipt must not be described as an adversarial grader verdict.
- Fix: none available inside the frozen probe without changing its design (kill-rule discipline: not edited here). Required: a result channel that no candidate-spawned process can write after the verdict (for example, separate the candidate's process tree from pytest's writer, or run the verdict from a sandbox the candidate cannot reach). Until then, state the threat model in the round report: cases are lane-authored.

## Should-fix

**S-1 — no `--new-session`; the caller's stdin is inherited into the sandbox.**
- Where: argv lines 154–179 (no `--new-session`); `subprocess.run` line 180 passes no `stdin=`.
- Observed: `/proc/self/fd/0` inside the sandbox follows the caller's fd 0 (`evidence.txt` E4: a tty when the probe is run interactively, `/dev/null` here). On a tty the sandboxed code holds the controlling terminal, so TIOCSTI keystroke injection into the host shell is possible where the kernel permits it.
- Mitigation on this host: `/proc/sys/dev/tty/legacy_tiocsti` = `0` (E7), which disables TIOCSTI for unprivileged use. Not a guarantee on other hosts.
- Fix: add `"--new-session"` to argv and `stdin=subprocess.DEVNULL` to line 180.

**S-2 — `--unshare-ipc` and `--unshare-uts` are absent.**
- Where: argv lines 154–179.
- Observed: inside the sandbox the IPC and UTS namespace inodes equal the host's (`ipc:[4026531839]`, `uts:[4026531838]`; E5). SysV IPC and the hostname are shared with the host.
- Fix: add `"--unshare-ipc", "--unshare-uts", "--hostname", "sandbox"`. This also removes the host hostname from the junit XML (N-2).

## Nit

**N-1 — `/etc` is bound read-only in full.** Line 160 (`--ro-bind /etc /etc`). Observed: `/etc/shadow` is denied (EACCES, E2) but world-readable host configuration (`hosts`, `machine-id`, `resolv.conf`, ...) is visible to the candidate. Narrow to the files the runtime needs.

**N-2 — host identity in committed evidence.** Every `receipt.junit/*.xml` testsuite carries `hostname="plazir27"` (6 of 6 files; E10). Tracebacks in q2-none, q3-stub, q5-full-model and q6-unscaled-loss include the host venv path `/home/vgpnk/.local/share/kengaku-r67/venv-pipe/...` (E10). Not secrets; it is identity and layout. The receipt bytes are frozen. Fix for future runs: S-2 (`--hostname sandbox`).

**N-3 — the port lock and `port_busy()` check the wrong namespace.** Lines 65, 123–128, 204–207. The gloo listener on 12355 runs inside the sandbox's own network namespace (E3: a host listener on 127.0.0.1:23456 is `ECONNREFUSED` from inside). The lock is host-side coordination the spec requires, so keep it. `port_busy()` only produces a spurious `SETUP` exit 2 when a host process holds 12355; there is no security effect.

**N-4 — `/proc` is mounted read-write.** Mountinfo line for `/proc`: `rw,nosuid,nodev,noexec` (E1), the bwrap `--proc` default. Root-in-userns may write `/proc/sys` settings of its own network namespace. Not tested for host effect; no host effect observed in E1–E9.

**N-5 — grader sha is checked then bound by path.** Check at line 198, bind at line 169. Not atomic. `check_receipt` re-hashes the grader at receipt time (line 262). The case file is bound read-only, so `case_sha` cannot change during a run.

**N-6 — host-side XML parse of sandbox-written bytes.** `junit_outcomes` (line 110) parses `/ctl/junit.xml` on the host. Entity-expansion behaviour of the host expat was not tested [INFERENCE: current expat limits entity expansion].

## Verified (no finding)

- **Network unshared.** Inside the sandbox `ip -o addr` lists only `lo` (E3). `connect(1.1.1.1:443)` → `ENETUNREACH`; `connect(127.0.0.1:23456)` to a host listener → `ECONNREFUSED`; a host abstract unix socket → `ECONNREFUSED` (E3).
- **PID unshared.** Sandbox `getpid()` = 2; `/proc` lists 2 entries; PID 1 is the bwrap monitor (E4).
- **Read-only binds.** `/usr`, `/etc`, the venv, `/app` (case dir), `/tests/test_outputs.py` are `ro` in mountinfo. Writes to `/app`, the venv and `/etc` → `EROFS` (E1).
- **Writable binds.** Only `/ctl` (xfs, `rw`, the case's own ctl dir) and `/tmp` (tmpfs). The sandbox root is an ephemeral tmpfs (`/newroot`), so writes there never reach the host (E1).
- **No credential paths.** Inside the sandbox `/home/vgpnk/.ssh`, `.config`, `.netrc` do not exist. `/home/vgpnk` holds only `.local/share/kengaku-r67/venv-pipe` as bind scaffolding; `/fast/scratch` is not mounted except the ctl dir (E1).
- **`--clearenv`.** The sandbox environment is exactly `PATH, HOME, PYTHONDONTWRITEBYTECODE, PYTHONNOUSERSITE, HF_HUB_OFFLINE, TRANSFORMERS_OFFLINE, PWD, LC_CTYPE`. No token, secret or agent-socket variable (E1).
- **`/tmp` is tmpfs** (`stat -f -c %T /tmp` → `tmpfs`, E1).
- **Teardown on kill.** A daemon child of the sandbox stopped writing when bwrap was SIGKILLed: 11 bytes at +0.5 s and 11 at +2.0 s after the kill; no surviving bwrap process (E6). `--die-with-parent` and the PID namespace hold.
- **No fd leak from the probe.** `subprocess.run` (default `close_fds=True`) does not pass the parent's extra fds to the child (E8).
- **Case files have no secrets or network calls.** `grep -rnE 'token|secret|password|api[_-]?key|http'` over `cases/` returns four lines, all `embed_tokens` (q1-ref:39, q4-hooks-noop:39, q5-full-model:26, q6-unscaled-loss:37), a false positive. The probe returns no match (E11). `socket|urllib|requests|subprocess|os.system|eval|exec|http` over `cases/` → no match (exit 1, E12). The probe's `socket` (line 124, `port_busy`) and `subprocess` (line 180) uses are local and expected.
- **Source captures are only the grader and instruction.** `corpus/evidence/round67/sources/` holds two files: `torch-pipeline-parallelism-test_outputs.py` (6065 bytes, sha256 `23574246…64c8`) and `torch-pipeline-parallelism-instruction.md` (1885 bytes, sha256 `989bfcf0…dcd2`). Both are ASCII text. The grader is byte-identical to the round-52 capture (`cmp` identical) and to `corpus/evidence/round52/graders/SHA256SUMS` line 169. The instruction hash is the one the claims doc cites (S239). No URLs, no tokens; the only `embed_tokens` match is the grader's comment at line 143. The SHA256SUMS also lists `test.sh` (line 170, sha `cc9fd28b…`), which is not captured here and is not part of the frozen set (nit, not a finding).

## Verdict

No must-fix blocks the six frozen vectors: they are consistent with genuine runs (E9-style cause checks above) and the sandbox isolates network, PID and writable surface as designed. **M-1 must be stated, or fixed, before any receipt from this probe is cited as a verdict on a candidate that is not lane-authored.** S-1 and S-2 are one-line argv changes.
