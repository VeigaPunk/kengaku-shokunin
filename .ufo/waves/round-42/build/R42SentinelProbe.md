# R42SentinelProbe — sandbox review of `plans/fibsqrt_probe.py`

Seat: `R42SentinelProbe` (sentinel, leaf, no subagents). Round 42 wave 1, item *R42SentinelProbe*.
Surface: the per-case bubblewrap sandbox `plans/fibsqrt_probe.py` builds — its bind list, `--die-with-parent`,
and whether **a case recipe, a `gates.txt` or the grader** can write outside `/app` and `/tmp`, reach the
network, or leave a process — plus one re-run of the probe compared byte-for-byte with the frozen receipt.

Lane clone: `git clone -q --shared …/kengaku-shokunin $S/lane`; `git -C "$S/lane" rev-parse --show-toplevel`
= `/fast/scratch/hyaku/kengaku-r42/R42SentinelProbe/lane`; HEAD `fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`.
Nothing frozen was edited: `plans/`, `corpus/evidence/round42/` were opened read-only from the clone; my only
writes are `$S` (scratch) and `.ufo/waves/round-42/build/R42SentinelProbe/`.

## Method

The sandbox was **not re-derived by hand**: each harness below imports the frozen module from the clone and calls
its own `sandbox_argv(cap, work)`, so every run used the exact bind list the probe uses, with only `/harness.py`
swapped for an introspection harness. Attacks ran *inside* that sandbox, which is the only way to answer the
question from local evidence. Host-side checks were run after each sandbox exited.

Envelope for every run (QUALITY Q32), receipt in `evidence-envelope.txt`:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

`before date 17:26:31  bin 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`
`after  date 17:27:08  bin 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`
(the real-probe run had its own pair: `17:23:05` → `17:24:06`, same digest both sides). `~/.local/bin` was
never written; no PATH directory was touched.

The bind list under test (`sandbox_argv`, printed by reuse, `evidence-introspect.txt` line 1):

```
bwrap --unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session
      --ro-bind /usr /usr  --symlink usr/bin /bin  --symlink usr/bin /sbin
      --symlink usr/lib /lib  --symlink usr/lib /lib64  --ro-bind /etc /etc
      --proc /proc  --dev /dev  --tmpfs /tmp  --bind <work>/app /app
      --dir /tests --dir /cap
      --ro-bind <cap>/test_outputs.py /tests/test_outputs.py
      --ro-bind <cap>/sim.c /tests/sim.c
      --ro-bind <cap>/solve.sh /cap/solve.sh
      --ro-bind <work>/recipe.sh /recipe.sh  --ro-bind <work>/harness.py /harness.py
      --chdir /app
```

There is **no `--bind /`**: the sandbox root is bwrap's own tmpfs, populated only by the entries above. That one
structural fact is what makes the findings below containable, and it is why the sandbox is materially tighter
than the orchestrator envelope (which must expose the whole host).

## Answer

**No write outside `/app` and `/tmp`, no network, no surviving process.** Interior evidence
(`evidence-introspect.txt`), one line each, all from inside the sandbox:

| probe | result |
|---|---|
| `sorted(os.listdir("/"))` | `app bin cap dev etc harness.py lib lib64 proc recipe.sh sbin tests tmp usr` |
| `write /etc/zz_probe` | `OSError:[Errno 30] Read-only file system` |
| `write /usr/bin/zz_probe` | `OSError:[Errno 30] Read-only file system` |
| `write /home/vgpnk/zz_probe` · `/root` · `/fast/scratch/...` · `/.local/bin` | `FileNotFoundError` (path does not exist in the namespace) |
| `write /proc/sys/kernel/core_pattern` | `PermissionError:[Errno 13]` |
| `write /app/zz_probe` · `/tmp/zz_probe` | `WROTE` in both |
| `socket.create_connection(("1.1.1.1", 53))` | `OSError:[Errno 101] Network is unreachable`; `/proc/net/dev` = `["lo"]` only |
| `/proc` pid entries | `["1", "2"]` — own pid namespace only |
| `uid / uid_map / CapEff / CapBnd / NoNewPrivs` | `1000` / `1000 0 1` / `0000…0000` / `0000…0000` / `1` |
| `see /home`, `/home/vgpnk/Projects`, `/fast`, `/sys` | `false` for all four |

`CapEff=0` with `NoNewPrivs=1` means the ro-bound `/usr` cannot be abused for setuid escalation, and
`/usr/bin/bwrap` is not setuid here (`-rwxr-xr-x root root`, 84464 bytes).

## Verified controls

- **C1 — filesystem.** Only `/app` (a host directory under the probe's `--work` root, deleted afterwards) and
  `/tmp` (fresh tmpfs) are writable; the root listing above is the complete set of names. A write "inside `/app`"
  is a host write by design, into `$S/w/k42-fsp-*/app`, and `evidence-attacks.txt` D shows the `--work` root
  empty after the real run: `entries: []`.
- **C2 — network.** `--unshare-net`; loopback only; connect → `ENETUNREACH`. No path to any host or LAN service.
- **C3 — process containment.** A guest `setsid` daemon that writes a marker 20 s after spawn
  (`Zq42SentinelLeak`) produced `LEAK_IMMEDIATE no` and `LEAK_AFTER_28s no`; `pgrep -af Zq42SentinelLeak` on the
  host → none. Killing the bwrap pid at a 4 s timeout (the shape of the probe's `timeout=1800`) left
  `pgrep -af Zq42TimeoutProbe` → `''`, rc=1. `--unshare-pid` + `--die-with-parent` + `--new-session` hold: the
  namespace init dying kills everything, and `--new-session` removes the TIOCSTI keystroke path.
- **C4 — executed-code integrity.** `PINS` are checked before any case (`main`), and the three executed captures
  are mount points: append to `/tests/test_outputs.py`, `/tests/sim.c`, `/cap/solve.sh` → `EROFS`; unlink
  `test_outputs.py` → `Errno 16 Device or resource busy`; host digests unchanged after the attacks
  (`6117b8ed…`, `700645ac…`, `a4ffab41…`). A cwd-local `/app/gcc` does **not** shadow the toolchain —
  `PATH` has no `.` and `shutil.which("gcc")` = `/usr/sbin/gcc`, resolved binary `gcc (GCC) 16.2.1` — and the
  probe's `env` is a closed 6-key dict (`PATH/HOME/LANG/LC_ALL/PYTHONUTF8/PYTHONDONTWRITEBYTECODE`), so no host
  secret environment enters the sandbox (`evidence-integrity.txt`). `PYTHONDONTWRITEBYTECODE=1` also keeps the
  grader's import from writing `__pycache__` into the ro `/tests`.
- **C5 — the one host-side "follow" path.** `/app` is a *writable bind of a host directory*, so a guest can plant
  a symlink there pointing at any host path. The host then `shutil.rmtree`s it. Test: guest planted
  `/app/link_dir → $S/victim` and `/app/link_file → $S/victim/keep.txt` (`PLANTED True True`); after the host
  `rmtree`, `victim/keep.txt` still exists with content `'must survive\n'`. `rmtree` unlinks the link, does not
  follow it — the only plausible write-outside path is closed.

## Findings

**F1 — LOW — no resource limits inside the sandbox (defence in depth).**
*Exploit path:* a hostile recipe or a grader bug forks or allocates without bound; `--unshare-pid` hides PIDs
from the host but does not cap them, `/tmp` is an uncapped tmpfs, `--bind …/app` writes straight to host storage,
and the sandbox carries no `--rlimit-*` and no cgroup (`/sys` is absent from the root listing). A fork bomb can
reach the host's `pid_max` in seconds; the only backstop is `subprocess.run(..., timeout=1800)` on the bwrap pid.
*Evidence:* the bind list quoted above contains no `--rlimit`; `/sys` not in the root listing; `CapEff=0` (so no
cgroup delegation either). *Impact:* host-wide PID/memory starvation for up to 30 min. *Reachability today:*
none — the 16 frozen recipes are `:\n` except the pinned oracle, so this is latent. I did not demonstrate it
(that would damage the host). *Smallest remediation:* when the probe is next edited, add
`--rlimit-nproc=256 --rlimit-as=8589934592` before `--unshare-net` and `--tmpfs`'s `--size`; record as a named
limit until then.

**F2 — LOW — `sim.c` is not memory-safe on `gates.txt` (contained).**
*Exploit path:* `parse_gates` never range-checks the parsed indices —
`if (out_idx >= num_signals) { num_signals = out_idx + 1; }` then `gates[out_idx]` (`sim.c:109-117`), and the
same for `src` on the copy/NOT paths (`sim.c:129,142`), where `dependents[src]` is a `32000×10000` BSS array.
A `gates.txt` line is therefore a write primitive into the simulator's globals.
*Evidence* (`evidence-attacks.txt` A, compiled `gcc -O3 /tests/sim.c` in `/app` as the grader does):
`out99999 = 0` → `RUN rc=-11` (SIGSEGV); `out5 = out999999` → `RUN rc=-11`; `out-5 = 0` → `RUN rc=0` (silent
out-of-bounds write before `gates[]`); a 4000-char line → `rc=0` (the `fgets(line, sizeof line)` bound saves
`char op[256]`, so no stack overflow there).
*Impact:* no escape — the blast radius is the namespace C1–C3 measured (no host path, no network, uid 1000,
CapEff 0, NoNewPrivs 1), so in-sandbox RCE gains `/app`, `/tmp` and a 30-min-bounded process. The real cost is
*soundness*: a gates-file that crashes `sim` yields `test_sqrt_fib F` in the probe output, indistinguishable from
a wrong circuit, and the probe's error path cannot tell them apart. *Reachability today:* none — every `gates.txt`
is fixture-frozen. *Smallest remediation:* `sim.c` is a pinned upstream capture (editing it would break
`PINS`/S8), so the remedy is a recorded limit plus, in the probe, a case-level distinction if a future untrusted
gates-file is ever graded.

**F3 — INFORMATIONAL — UTS not unshared; host `/etc` is exposed read-only.**
*Evidence:* `HOSTNAME plazir27` from inside (`evidence-attacks.txt` A) — the guest sees the host hostname; the
root listing shows `etc` and `os.listdir("/etc")` = 186 entries, with `machine-id`, `hostname`, `passwd`, `hosts`
readable and `shadow`, `resolv.conf` not (`R_OK false`, `evidence-integrity.txt`). This is also a *fidelity* note:
the grader reads the host's `/etc`, not the task image's. *Impact:* host identity disclosure to code that is
already pinned and trusted; no secret (`shadow`, ssh host keys unreadable by uid 1000). *Smallest remediation:*
add `--unshare-uts`, and bind only the files the toolchain needs (`/etc/ld.so.cache`, `/etc/ld.so.conf*`,
`/etc/nsswitch.conf`, `/etc/passwd`, `/etc/group`, `/etc/localtime`) instead of all of `/etc`.

## Receipt — probe re-run

```
cd $S && bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  /usr/bin/python3 $S/lane/plans/fibsqrt_probe.py --lane $S/lane --work $S/w
rc=0            17:23:05 → 17:24:06   (61.05 s wall)
24 lines, stderr empty
sha256 probe-out.txt   2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a
sha256 frozen receipt  2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a
cmp → BYTE-EQUAL
tail: regrade cases=16 differ=0 / cases=16 observed_pass=7 observed_fail=9 mismatches=0
```

Every one of the 16 case verdicts reproduces, including the `regrade=` column, so the frozen receipt is
reproducible on this host exactly as committed.

## Limits of this review

- Kernel-level containment only: no attempt at a bwrap/kernel exploit, and none is in scope for a local review;
  the verdict rests on the namespace shape measured above.
- `/etc`, `gcc` and `python3` are the host's, not the task image's (already a named limit of the probe), so the
  exposure in F3 is the host's, not Debian bookworm's.
- F1's fork-bomb/OOM path was reasoned from the missing limits, not executed (host-safety rule).
- Two guests showed `proc_pids ["1","2"]`; I did not enumerate pid-2's identity, so "only sandbox pids" is
  bounded by the listing, not by a full `/proc` walk.

## Files

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42SentinelProbe/`:
`probe-out.txt` (`2a54ca8a…`), `evidence-envelope.txt` (`e65d9eba…`), `evidence-introspect.txt` (`eb6a517e…`),
`evidence-attacks.txt` (`cdb3e4a4…`), `evidence-integrity.txt` (`eee77f63…`). Harnesses (scratch, not copied):
`sbxprobe.py`, `memprobe.py`, `integrity.py` under `$S`. No tool was installed.

VERDICT: probe-sandbox-findings-3-rerun-equal
