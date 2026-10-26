# R41SentinelProbe — sandbox review of `plans/constraints_probe.py`

Seat: sentinel (leaf, no subagents). Scope: the bwrap sandbox in `plans/constraints_probe.py` — the task's
`solve.sh` and the TB2 grader run inside it. Question set: can a case recipe or the grader **write outside `/app`
and `/tmp`**, **reach the network**, or **leave a process**? Plus: run the probe once and diff against the frozen
receipt.

Everything below was produced under the mandated envelope, and every fixture/probe write stayed inside
`/fast/scratch/hyaku/kengaku-r41/R41SentinelProbe` plus this report dir. The lane was never written; my clone is
`git status --porcelain`-clean.

## 0. Packet

| item | value |
|---|---|
| lane clone | `git -C "$S/lane" rev-parse HEAD` → `fc79f2a49be0221e138b3885fa0d83bc43b31a42`; toplevel `$S/lane` (asserted) |
| module under review | `plans/constraints_probe.py` sha256 `8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7242` (`probe-module-sha256.txt`) |
| host bwrap | `/usr/bin/bwrap` `-rwxr-xr-x root root` (NOT setuid), `bubblewrap 0.13.1`, `kernel.unprivileged_userns_clone=1` |
| envelope | `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent …` |
| scratch | `/fast/scratch/hyaku/kengaku-r41/R41SentinelProbe` (removed at end; receipts below) |

Evidence files in this directory: `probe-run.txt`, `probe-sha256.txt`, `probe-diff.txt`, `probe-module-sha256.txt`,
`sandbox-round2.txt` (mounts/caps/secrets/write matrix), `sandbox-leak.txt` (teardown), `sandbox-stdin-symlink.txt`
(stdin + `--bind` symlink), `probe-hardened2.txt` / `probe-hardened2-diff.txt` (remediation), `probe-hardened.txt`
(failed first remediation attempt), `bwrap-flag-notes.txt`. Drivers: `scripts/*.py` (they import the frozen module
read-only and call its own `sandbox_argv`; the frozen file is never edited).

## 1. Answers to the three asked questions

| axis | answer | evidence |
|---|---|---|
| write outside `/app` and `/tmp` | **No host-persistent write exists.** Exactly one host-backed mount is writable: `/app` (the per-case scratch dir). Everything else writable is a private tmpfs discarded at exit. | mounts + write matrix, §2/§4 |
| reach the network | **No.** `--unshare-net`; external connect `OSError [Errno 101] Network is unreachable`, `127.0.0.1:22` refused, DNS `gaierror -3`. No `/run`, `/var` → no `docker.sock`. | `sandbox-round2.txt` |
| leave a process | **No.** A `setsid`-double-forked grandchild is visible from the parent namespace while the sandbox runs, and is gone after both a `SIGKILL` of bwrap (the `timeout=300` path) and a normal exit; no zombies. | `sandbox-leak.txt` |

No HIGH or MEDIUM finding on these three axes. Five LOW hardening findings follow (§3), each with a validated
remediation (§5).

## 2. The bind list as frozen

`plans/constraints_probe.py:241-252`:

```
--unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session
--ro-bind /usr /usr      (+ /bin,/sbin,/lib,/lib64 recreated as symlinks when the host has them)
--ro-bind /etc /etc      --proc /proc  --dev /dev  --tmpfs /tmp
--bind <work>/app /app   --dir /cap
--ro-bind <cap>/test_outputs.py /cap/test_outputs.py   --ro-bind <cap>/solve.sh /cap/solve.sh
--ro-bind <work>/recipe.sh /recipe.sh  --ro-bind <work>/harness.py /harness.py  --chdir /app
```

Mount table observed from inside (`sandbox-round2.txt`):

```
tmpfs /        rw,nosuid,nodev,uid=1000,gid=1000
/dev/mapper/root /usr btrfs ro,...   /dev/mapper/root /etc btrfs ro,...
proc /proc     rw,nosuid,nodev,noexec
tmpfs /dev     rw,nosuid,nodev,mode=755,uid=1000 | devpts /dev/pts | tmpfs /tmp rw,nosuid,nodev
/dev/nvme1n1p2 /app xfs rw,nosuid,nodev,noatime
```

`/` is a root tmpfs owned by uid 1000, so `/cap`, `/`, `/dev`, `/dev/shm` accept writes — all ephemeral. `/usr` and
`/etc` are read-only btrfs binds (`EROFS`, errno 30 on write). `/home`, `/root`, `/run`, `/var`, `/fast`, `/sys` are
**absent**: `VISIBLE /home False`, and a direct read of the lane fails (`head: cannot open
'/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/constraints_probe.py': No such file or directory`).

## 3. Findings

### F1 — LOW — the sandbox inherits the probe's stdin
- **Exploit path:** `run_case` builds `subprocess.run(..., env=env, capture_output=True, …)` with no `stdin=`
  (`plans/constraints_probe.py:269-270`), so fd 0 of bwrap — and therefore of the recipe and of the in-process
  grader — is the probe's own stdin. `HARNESS_PY` gives the recipe `stdin=subprocess.DEVNULL`, but the imported
  grader still reads fd 0 directly.
- **Evidence:** harness that does `sys.stdin.read(64)`, driven by the frozen `sandbox_argv` with `input="SECRET-PARENT-STDIN\n"`:
  `WITH_PIPE_STDIN rc=0 out=STDIN_READ 'SECRET-PARENT-STDIN\n'` (`sandbox-stdin-symlink.txt`).
- **Impact:** third-party code (TB2 `solve.sh`/`test_outputs.py`, pinned but external) can read or drain whatever a
  caller attaches to the probe's stdin — a receipt file, a pipe from another tool, a terminal fragment. It can also
  block forever on a tty read instead of seeing EOF.
- **Smallest remediation:** `stdin=subprocess.DEVNULL` on the `subprocess.run` in `run_case` (the harness already
  does this for the recipe).

### F2 — LOW (same-user only) — `--bind` follows a symlinked `/app` source
- **Exploit path:** `--bind str(work / "app") /app` resolves the *source* path; if `work/app` is a symlink, its
  target is mounted read-write at `/app`. The window is between `app.mkdir()` and the bwrap call.
- **Evidence:** with `work/app` a symlink to `work/target` and an unchanged frozen `sandbox_argv`, the sandbox's
  `open("/app/hostmark","w")` landed in the host dir: `TARGET_GOT_WRITE True`, `SYMLINK_BIND rc=0`
  (`sandbox-stdin-symlink.txt`).
- **Impact:** limited — the dir is a `tempfile.mkdtemp` with mode 0700 under the probe's own `--work`, so the
  attacker must already be the same user with write access to that dir before the bind. It is not reachable from
  the recipe or the grader, which run after the bind. It matters as a pattern: a writable host bind whose source is
  not verified is the one path that can widen into an arbitrary host write.
- **Smallest remediation:** `p = pathlib.Path(os.path.realpath(work / "app"))` plus `assert not p.is_symlink()`
  (or bind `os.open(..., O_DIRECTORY|O_NOFOLLOW)` by fd) before constructing the argv.

### F3 — LOW — host identity is disclosed to untrusted code
- **Exploit path:** no `--unshare-uts`, and the whole host `/etc` is bind-mounted, so the recipe/grader can read
  the host's hostname and `/etc/machine-id`.
- **Evidence:** `HOSTNAME plazir27`, `MACHINEID 432d02b544a5459ebbff9c42ec68334d`, `USERS root:x:0:0::/root:/usr/bin/bash`
  (`sandbox-round2.txt`). `/etc/shadow` is correctly refused: `SHADOW PermissionError13`.
- **Impact:** host fingerprinting/stability-correlation from third-party task code; no write and no secret leak.
- **Smallest remediation:** `--unshare-uts --hostname k41probe`, and replace the whole-`/etc` bind with the entries
  the run actually needs (`ld.so.cache`, `passwd`/`group`, `nsswitch.conf`, locale, timezone) — `machine-id` has no
  consumer here.

### F4 — LOW (defence in depth) — nested user namespaces are permitted inside the sandbox
- **Exploit path:** bwrap is not setuid, so it runs in a user namespace; with no `--unshare-user`/`--disable-userns`
  the sandboxed process can create further user+mount namespaces.
- **Evidence:** `NESTED_USERNS (0, '')`, `NESTED_USERNS_MOUNT (0, '')` (`sandbox-round2.txt`).
- **Impact:** none reachable today — the process has `CapEff 0000000000000000`, `NoNewPrivs 1`, and no
  host-writable path other than `/app`, so a nested namespace can only re-mount its own view. It does keep the
  userns/overlayfs kernel attack surface available to untrusted code.
- **Smallest remediation:** `--unshare-user --disable-userns` (bwrap quotes: `--disable-userns requires
  --unshare-user`, `bwrap-flag-notes.txt`); validated in §5.

### F5 — LOW — no resource bounds beyond the 300 s timeout
- **Exploit path:** a recipe or grader can fork-bomb or stream unbounded output; the sandbox has no pid/memory cap
  and the parent buffers both pipes (`capture_output=True`).
- **Evidence:** `Seccomp: 0`, no pids/memory cgroup in the mount table, `timeout=300`
  (`plans/constraints_probe.py:270`), no output cap; the harness itself is silent by design.
- **Impact:** host RAM/PID pressure for up to 300 s per case, and parent-side memory growth proportional to
  grader output. Bounded to the probe's own process tree and terminated by the timeout; the executed artifacts are
  sha256-pinned before any run (`PINS`, `constraints_probe.py:66-72`, checked at `:305-308`), so this needs either a
  pinned-capture compromise or a future unpinned case.
- **Smallest remediation:** read the pipes with a byte cap (or `stdout`/`stderr` to a size-limited temp file) and
  lower the per-case timeout; a pids cap needs a cgroup outside bwrap and is out of scope for this file.

### Observations (not counted as findings)
- `/cap` is writable as a directory (`WRITE /cap/x OK`); only the two pinned files are read-only mounts. Nothing
  persists — `/cap` lives in the root tmpfs — so "read-only `/cap`" is a file-level property, not a directory one.
- The verdict channel is the grader's own stdout, parsed by the harness. Containment does not protect the receipt
  from a grader whose bytes are not the pinned ones; the sha256 `PINS` check before execution does.
- A hard crash of the probe (SIGKILL of the parent) skips `run_case`'s `finally: shutil.rmtree(work)`, leaving
  per-case dirs under `--work`. Residue only; exit paths tested here leave `$S/w7`, `$S/w8` empty.

## 4. What holds (positive controls)

| property | observed |
|---|---|
| identity | `uid=1000(vgpnk)`, `CapEff: 0000000000000000`, `NoNewPrivs: 1` |
| setuid binaries visible in `/usr` | present with the SUID bit but owners unmapped (`-rwsr-xr-x 1 65534 65534 … /usr/bin/sudo`); `sudo` refuses: `The "no new privileges" flag is set, which prevents sudo from running as root` |
| host `/proc` | not visible: `PID1 /usr/bin/bwrap …`, `NPROC 2` |
| lane | not visible (`/home` absent; lane file read fails) |
| network | `Network is unreachable`; loopback refused; DNS `gaierror -3` |
| secret files | `/etc/shadow` `PermissionError13`; no docker socket |
| terminal | `--new-session` → no controlling tty, `/dev/tty` open `OSError [Errno 6]` |
| write outside `/app`,`/tmp` | `/usr/x` `OSError 30`, `/etc/x` `OSError 30`; the rest are devtmpfs/tmpfs writes |
| teardown | grandchild `7 4 /bin/sh /tmp/k41canary` while running → `(none)` after `SIGKILL` of bwrap and after normal exit; `ZOMBIES: (none)` |

## 5. Remediation validated (no relaxation of the receipt)

Wrapping `sandbox_argv` in memory only (frozen file untouched) with `--unshare-user --disable-userns
--unshare-uts --hostname k41sandbox` and re-running the whole probe:

```
$ python3 scripts/probe_remediation.py "$S/lane" "$S/w8" '--unshare-user|--disable-userns|--unshare-uts|--hostname|k41sandbox'
HARDENED2 OUTPUT IDENTICAL     (diff vs corpus/evidence/round41/constraints-probe.txt empty)
MAIN_RC 0 ; cases=25 observed_pass=6 observed_fail=19 mismatches=2 ; regrade cases=25 differ=0
```
and inside the hardened sandbox: `hostname` → `k41sandbox`, `unshare -U` / `unshare -Urm` → `unshare failed: No
space left on device` (nested userns blocked). The first attempt without `--unshare-user` is kept as evidence that
the flag has a precondition (`probe-hardened.txt`: `SETUP case nop did not yield three test verdicts twice (rc=1)`).

## 6. Acceptance: the probe run vs the frozen receipt

```
$ cd "$S/lane" && bwrap <envelope> python3 -B plans/constraints_probe.py --lane . --work "$S/w" > probe-run.txt
probe rc=0
$ diff -u corpus/evidence/round41/constraints-probe.txt probe-run.txt   → no output (byte-equal)
c5aa674277f9b9473de4c0884629c577f2b6467d8b73c3a90eec33b24b7701da  …/corpus/evidence/round41/constraints-probe.txt
c5aa674277f9b9473de4c0884629c577f2b6467d8b73c3a90eec33b24b7701da  …/build/R41SentinelProbe/probe-run.txt
```
33 lines; tail: `regrade cases=25 differ=0` / `cases=25 observed_pass=6 observed_fail=19 mismatches=2`. The
receipt is reproduced exactly on this host and lane state, including the two pilot mismatches.

## 7. Limits

- Host-specific: bwrap 0.13.1 non-setuid, unprivileged userns enabled, `/bin`,`/sbin`,`/lib`,`/lib64` present as
  symlinks. A setuid bwrap, `kernel.unprivileged_userns_clone=0`, or a non-symlinked `/lib64` changes the failure
  modes (the last one already surfaces as `bwrap: execvp /usr/bin/bash: No such file or directory`).
- Kernel-level sandbox escapes (userns/btrfs bugs) are out of scope; F4 is a surface, not a demonstrated escape.
- Resource-exhaustion constructs were **not** executed (host safety); F5 is argued from the flags and the mount
  table.
- The C1 counter's own sandbox (`round41_c1_verify.py`) and the gate (`pkg_gate.py`) are not reviewed here.
- Operational note: `/fast/scratch/hyaku/kengaku-r41` was recreated at 15:42 mid-seat, deleting my clone and two
  driver scripts; I re-cloned (`fc79f2a4`) and re-ran every measurement above. Receipts were written to this
  report dir before scratch removal, and scratch is now deleted.

VERDICT: probe-sandbox-findings-5
