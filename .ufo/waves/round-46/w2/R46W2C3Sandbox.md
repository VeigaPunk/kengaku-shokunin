# R46W2C3Sandbox — hostile-payload audit of the C3 probe's sandbox function

- **Item attacked:** R46W2C3Sandbox, wave 2 (falsify) of round 46. Subject: `plans/polyglot_c_py_probe.py` as landed.
- **Lane clone measured:** `git clone -q --no-local <lane> $S/lane && git -C $S/lane checkout -q 42d5043a…`;
  `git -C $S/lane rev-parse --show-toplevel` = `$S/lane`;
  `git -C $S/lane rev-parse HEAD` = `42d5043afac952fcb43bf4798757785dd258cf85` (repeated as `HEAD`/`TOP` in every receipt).
- **Subject digests:** `sha256sum plans/polyglot_c_py_probe.py` =
  `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26` (matches the stage-2 `PROBE_SHA256`
  prefix `67a8f4a6…` in the claims file); captured grader `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` =
  `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` (= probe `PINS`).
- **Method:** the landed function `sandbox_argv(cap, work)` (`plans/polyglot_c_py_probe.py:349-363`), the landed
  `ENV` and `harness()` (`:366-373`), and the landed `run_case()` are imported from the TIP clone and driven with
  hostile payloads. Nothing in the lane was edited; the driver is `R46W2C3Sandbox/sb.py`, receipts
  `R46W2C3Sandbox/r-*.txt`. Every run is bracketed by the wave-2 envelope; all nine receipts end
  `local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged`, `exit=0` (no `INVALID`).

| receipt | what it runs | ENVELOPE start / end |
|---|---|---|
| `r-multi.txt` | identity, mount table, `/proc/self/limits`, write-outside-`/app` matrix, `/etc` reads, symlink/`-p` escapes | `02:51:39` / `02:51:40` |
| `r-forks.txt` | 300 in-sandbox children, host `ps` accounting | `02:51:41` / `02:51:48` |
| `r-ram.txt` | 768 MiB to `/` + 256 MiB to `/tmp`, `/dev/tty`, `/pub` mutation | `02:51:49` / `02:51:50` |
| `r-out.txt` | 2 GiB of stdout into the probe's own capture | `02:51:51` / `02:51:53` |
| `r-daemon.txt` | `setsid` daemon survival after sandbox exit | `02:51:55` / `02:51:57` |
| `r-e2e.txt` | hostile `main.py.c` through `run_case(..., "grade")` (both runtimes) | `02:51:58` / `02:52:05` |
| `r-etc.txt` | host `/etc` disclosure + grader stall cost | `02:52:06` / `02:52:25` |
| `r-cases3.txt` | three hostile `main.py.c` programs (writer / network / fork+output) | `02:52:26` / `02:52:34` |
| `r-tmpfs.txt` | 1 GiB tmpfs in `/tmp`, 512 MiB into the host-backed `/app` | `02:52:35` / `02:52:37` |

Envelope argv is identical for every receipt except the scenario word (full line in each receipt):
`/home/vgpnk/…/.ufo/waves/round-46/claims/envelope.sh "$S/env" python3 "$S/sb.py" "$S/lane" "$S" <scenario>`.

## Axes

1. host filesystem containment (writes, reads, symlinks, `..`, `-p` parent fabrication)
2. network containment
3. process lifecycle (orphans, daemons, pid accounting)
4. resource governance (RAM, tasks, disk, CPU, output)
5. `HOME` / `~/.local` handling
6. information disclosure to graded code

## What the sandbox is, as measured

`/proc/self/status` inside (`r-multi.txt`): `Uid: 1000 1000 1000 1000`, `CapEff: 0000000000000000`,
`NoNewPrivs: 1`, `Seccomp: 0`, `Seccomp_filters: 0`, `NSpid: 4`. `id` = `uid=1000(vgpnk) gid=1000(vgpnk)
groups=1000(vgpnk),65534(nobody)`. Mount table of the sandbox (`/proc/self/mountinfo`, `r-multi.txt`):

| mount | flags | note |
|---|---|---|
| `/` | `rw` tmpfs (`/newroot`) | **writable sandbox root** — not stated, not read-only |
| `/usr`, `/etc` | `ro` | host btrfs `@/usr`, `@/etc` |
| `/proc`, `/dev`, `/tmp` | `/proc` procfs, `/dev` tmpfs + devtmpfs nodes, `/tmp` tmpfs `rw` | fresh per case |
| `/app` | `rw` **host xfs** `/dev/nvme1n1p2 … noquota` | bind of the run's `work/app` |
| `/tests` | `ro` | the run's `work/tests` |
| `/pub/*`, `/tpl/*`, `/seed.sh`, `/recipe.sh`, `/harness.py` | `ro` files under `--dir` parents | parents are in the rw root tmpfs |

`/proc/self/limits`: `Max processes 122865 122865`, `Max resident set unlimited unlimited`,
`Max cpu time unlimited unlimited`, `Max address space unlimited unlimited`,
`Max file size 274877906944 unlimited`, `Max core file size unlimited unlimited`.

## The three hostile `main.py.c` programs (task acceptance)

Each is a real polyglot built with the probe's own `poly()`, written by `emit()`, and graded by
`probe.run_case(CAP, root, case, "grade")` — i.e. executed by the captured grader (`python3 main.py.c N`, then
`gcc … -o cmain`, then `./cmain N`) inside the landed sandbox (`r-cases3.txt`).

| case | hostile behaviour | measured result |
|---|---|---|
| `hostile-writer` | writes `/etc/x`, `/usr/x`, `/tests/x`, `/pub/x`, `/home/vgpnk/.local/bin/x`, `/root/x`, `/w_root`, `/app/escape-ok` in both runtimes | `grades=[(0,'P'),(1,'F')]`, `LEFTOVERS 0`, `HOST-WRITES={'/etc/x': False, '/usr/x': False, '/root/x': False, '/w_root': False, '/app/escape-ok': False}` |
| `hostile-net` | `connect 1.1.1.1:80`, `bind 0.0.0.0:9000`, `getaddrinfo example.com`, C `connect`/`bind` | `grades=[(0,'P'),(1,'F')]`, host untouched |
| `hostile-forkout` | 400 children per runtime + 1 GiB stdout per runtime | `grades=[(1,'F'),(1,'F')]`, `peak_rss_mib=5762 peak_tasks=804 memavail_delta_mib=602`, `LEFTOVERS 0` |

Wire-level detail from the direct runs (same sandbox function, payload instead of recipe):
`WROTE /w_root`, `/pub/x`, `/tpl/x`, `/dev/x`, `/tmp/x`, `/app/../w_dotdot`, `/app/../../w_dotdot2`;
`DENIED /etc/hostile` and `/etc/passwd` and `/usr/x` and `/tests/x` (`Read-only file system`),
`DENIED /home/vgpnk/x` (`No such file or directory`), `/root/x` (ENOENT), `/sys/x` (ENOENT),
`/proc/sysrq-trigger` (`Permission denied`), `/proc/x` (ENOENT). Host-side re-check after the run:
`HOST /w_root exists=False … /home/vgpnk/.local/bin/x exists=False` (`r-multi.txt`).
`mkdir -p /home/vgpnk/.local/bin` prints `MKDIR` — `-p` fabricates the chain **inside the rw root tmpfs**, which is
why the host-side check is the one that decides; it is `False`.

## Findings

### G1 — root tmpfs is writable and unsized; RAM is the real limit (Medium; High if a recipe ever carries agent bytes)

`bwrap`'s new root is mounted `rw` (`816 … /newroot / rw … - tmpfs`), so `WROTE /w_root` succeeds and 768 MiB
written to `/` plus 256 MiB to `/tmp` dropped host `MemAvailable` by **1002 MiB** while the sandbox held it
(`r-ram.txt`: `BEFORE memavail_mib=19113` … `memavail_mib 18547628` … `WHILE-SANDBOX-HELD … delta_drop_mib=1002`).
`r-tmpfs.txt` shows the same via `/tmp` alone: `tmpfs_bytes 1073741824`, inside-sandbox `memavail_mib 18973548`
(= 18,528 MiB against a `BEFORE` of 19,568 MiB). `Max resident set unlimited`; no cgroup, no seccomp
(`Seccomp: 0`), no `--size` on either tmpfs. The probe's own capture adds the same class of blow-up: 2 GiB of
stdout was captured in 1.0 s, `parent_rss_mib 20 → 2073 (delta 2053)`, `SELF maxrss_mib=4122` (`r-out.txt`) —
`capture_output=True` at `plans/polyglot_c_py_probe.py:372` has no bound.
**Exploit path:** a graded `main.py.c` (or a recipe) writes to `/`, `/tmp` or stdout; the page cache/tmpfs is host
RAM, so the OOM killer picks a host victim while the probe sees only a failed case.
**Impact:** host OOM / probe kill; no host path is written.
**Smallest remediation:** `--remount-ro /` and `--tmpfs /tmp --size 268435456` (both offered by the installed
bubblewrap 0.13.1: `bwrap --help` lists `--remount-ro DEST` and `--size BYTES`), plus `resource.setrlimit(RLIMIT_AS, …)`
for the harness process and a size-capped replacement for `capture_output`.

### G2 — no task limit; children are host-visible tasks of uid 1000 (Medium)

`Max processes 122865 122865` is the host per-uid value inherited unchanged; bwrap 0.13.1 exposes no `--rlimit-*`
(`bwrap --help | grep -c rlimit` → `0`). Three hundred in-sandbox children produced
`HOSTPIDS baseline=2 during=305 delta=303`, `HOSTTASKS-OF-UID-1000 during=305`, and `HOSTPIDS after=2`
(`r-forks.txt`); the graded fork case peaked at `peak_tasks=804` (`r-cases3.txt`).
**Exploit path:** `main.py.c` forks; the pid namespace contains nothing — `RLIMIT_NPROC` is charged per real uid, not
per pidns, so the fan-out consumes the host user's process budget and starves every other process of uid 1000.
**Impact:** host-wide fork denial for the probing user; the sandbox itself is cleaned up correctly afterwards.
**Smallest remediation:** `RLIMIT_NPROC` (e.g. 256) in the harness process before it executes the grader.

### G3 — `/app` is the host filesystem, `noquota`, 256 GiB file-size ceiling (Medium)

`/app` mounts as `xfs /dev/nvme1n1p2 … noquota`; `df -h /app` from inside sees the host volume
(`804G 236G 568G 30%`). A 512 MiB file was written without resistance (`app_bytes 536870912`, `r-tmpfs.txt`), and
host `statvfs` free blocks fell by `192569344` bytes at the sampling instant (delayed allocation). `Max file size`
soft limit is `274877906944`.
**Exploit path:** a hostile file fills `/fast` with `dd`-style writes; the work dir is deleted afterwards, the 24
other seats' scratch on the same xfs is not.
**Impact:** shared-filesystem exhaustion; still no write outside the declared work dir.
**Smallest remediation:** `RLIMIT_FSIZE` (e.g. 64 MiB) for graded children, or put `/app` on a `--size`d tmpfs.

### G4 — time is bounded only by the probe's outer 1800 s, three times per case (Low–Medium)

The captured grader runs both runtimes with `capture_output=True, text=True, check=True` and **no** `timeout`
(`corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py:23-46`). A polyglot sleeping 3 s per runtime cost
`RUN_CASE_GRADE … seconds=18.1` (`r-etc.txt`), i.e. nine sleeps per grade with no inner timer. The only bound is
`timeout=1800` per `harness()` call (`plans/polyglot_c_py_probe.py:372`) and `run_case` makes three such calls
(recipe + two grades): 5400 s per case, 18 cases → **27 h** worst case [INFERENCE: arithmetic on those bounds].
**Impact:** a stalling file turns the probe into a multi-hour host CPU consumer; the run is not reproducible in a
bounded window.
**Smallest remediation:** `setrlimit(RLIMIT_CPU)` in the harness, or a timeout on the grader's two
`subprocess.run` calls (lane file, not this seat's scope).

### G5 — graded code reads host `/etc` and learns host paths (Low)

`READABLE /etc/machine-id 432d02b544a5459ebbff9c42ec68334d`, `/etc/hostname plazir27`, `/etc/passwd`,
`/etc/group`; `DENIED /etc/shadow`, `/etc/gshadow`, `/etc/sudoers`, `/etc/ssh/ssh_host_ed25519_key`,
`/etc/kernel/cmdline` (`r-etc.txt`). `READABLE /proc/self/cgroup 0::/user.slice/user-1000.slice/user@1000` and
`/proc/1/cmdline` (`/usr/bin/bwrap --unshare-net …`) — the bwrap argv leaks the host scratch path of the case.
**Impact:** fingerprints and host paths reachable by any graded byte; no credentials (all key files `0600` root and
denied by uid mismatch).
**Smallest remediation:** none worth the fragility (gcc/python need `ld.so.cache`, `nsswitch`, `passwd` for
`HOME`); record it as a named limit instead.

### G6 — observation, not a containment defect: side effects are invisible to the verdict

`hostile-writer` fails every escape attempt and still grades `P` on the first pass (`r-cases3.txt`,
`grades=[(0,'P'),(1,'F')]`), because the grader compares `stdout.strip()` and one `os.listdir`
(`test_outputs.py:17-46`) and never inspects side effects. A hostile solution that prints the right values is
indistinguishable from an honest one.

## What survives (no escape found)

- **Host filesystem:** of 20 write attempts (`r-multi.txt`) 11 were denied and 9 succeeded, and every success landed
  in sandbox-internal state — the `rw` root tmpfs (`/w_root`, `/pub/x`, `/tpl/x`, `/dev/x`, `/app/../w_dotdot`,
  `/app/../../w_dotdot2`, `/app/hl-escape`), `/tmp`, or the sanctioned `/app` work dir. No host path outside the
  work dir was written. `/etc`, `/usr`, `/tests` are `ro` (`Read-only
  file system`); `/home`, `/root`, `/sys` do not exist in the sandbox root (`No such file or directory`); no `/home`
  mount exists at all, so `~` is unreachable. Host-side re-check after the run: every target `False`. Symlink
  `/app/hl -> /home/vgpnk` resolves to the sandbox's own fabricated tree (`listdir /app/hl = ['.local']`, the chain
  `mkdir -p` created), and `/proc/1/root` reaches only the sandbox root. Forcing `HOME=/home/vgpnk` still fails.
- **Network:** `--unshare-net` holds. `connect 1.1.1.1:80` → `OSError 101` (ENETUNREACH); `getaddrinfo example.com`
  → `-3` (Temporary failure in name resolution); `AF_PACKET` → `EPERM 1` (no `CAP_NET_RAW`); only `lo` exists and
  is up (`connect 127.0.0.1:22` → `ConnectionRefusedError 111`), which is intra-sandbox only.
- **Process lifecycle:** `--unshare-pid --die-with-parent --new-session` tear the namespace down cleanly. A
  `setsid`'d `sleep 137` left `[]` on the host (`r-daemon.txt`); 404 and 804 graded children left `LEFTOVERS 0`
  and `HOSTPIDS after=2` (`r-cases3.txt`, `r-forks.txt`).
- **`HOME` / `~/.local`:** `HOME=/tmp`, `TMPDIR=/tmp` (`ENV`, `:366`); `$HOME/.local/bin` is a writable tmpfs path
  that dies with the sandbox, and the host `~/.local/bin` is untouched: 9/9 receipts show an identical
  `local_bin_content` digest, and `HOST /home/vgpnk/.local/bin/x exists=False`.
- **`/dev`:** no controlling terminal — `open("/dev/tty")` → `OSError 6` (ENXIO) after `--new-session`; `/dev/pts`
  is a fresh devpts.
- **Public copies:** the three `/pub` files are immutable from inside — `rename /pub/solve.sh` → `OSError 16`
  (EBUSY), append → `OSError 30` (EROFS), `pub-list` unchanged. Only the `--dir` parent accepts new entries, and it
  is a per-case tmpfs, so nothing persists across cases.

## Limits of this audit

- Measured on this host's bubblewrap 0.13.1 and kernel 7.2.11; a different bwrap build (e.g. one with `--rlimit-*`)
  would change G2's remediation, not the measurements.
- The fork bomb was run **bounded** (300 and 400 children) — an unbounded fan-out against `Max processes 122865` was
  not executed on the host (host-safety rule); the starvation claim is [INFERENCE] from the inherited limit plus the
  measured per-uid accounting.
- No `/sys`, no cgroup view was mounted, so host-wide memory pressure is measured as `MemAvailable`, not as
  per-sandbox accounting.
- The probe's 18 frozen receipt cases were not re-run (not this item's surface); all payloads here are new and none
  is a receipt case.

## Scratch

`S=/fast/scratch/hyaku/kengaku-r46/R46W2C3Sandbox`; receipts copied to
`.ufo/waves/round-46/w2/R46W2C3Sandbox/` and the scratch dir removed via `plans/scratch_guard.py safe-rm`.
No tool was installed or upgraded during this seat.

VERDICT: c3-sandbox-escapes-0
