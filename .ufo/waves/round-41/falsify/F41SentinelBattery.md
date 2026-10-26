# F41SentinelBattery — security review of the landed battery41 and its sandboxes

Seat: sentinel, wave 2 (falsify). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, working tip
`d7c7789` (assignment tip `3d0058f` is its parent; wave 2 adds only the spec/dispatch commit). Clean clone at
`/fast/scratch/hyaku/kengaku-r41/F41SentinelBattery/lane` (`rev-parse --show-toplevel` = itself, HEAD `d7c7789`).
Scratch `/fast/scratch/hyaku/kengaku-r41/F41SentinelBattery` (only my own; removed at the end). No tool installed
(nothing needed; pacman untouched). No write outside my report dir and scratch dir.

Freeze verified before and after every run:

```
$ cd $S/lane && sha256sum -c .../.ufo/waves/round-41/claims/frozen-digests.txt
plans/round-41-claims.md: OK   plans/round41_c1_verify.py: OK   plans/round41_c2_verify.py: OK
plans/constraints_probe.py: OK plans/pkg-spec-r41.json: OK      .../constraints-dry-cases-freeze.txt: OK
.../tb2-constraints-scheduling/SHA256SUMS: OK  plans/tip_receipts.py: OK  plans/sources_adopt.py: OK
plans/pkg_gate.py: OK  plans/order_check.py: OK                       (11/11 OK)
```

Every **counter** run below (all three, untraced and traced) executed inside the mandated envelope, `bwrap`
0.13.1, nesting verified (`nested-ok`). The targeted experiments in §3/§4 are bwrap invocations with the
counter's *own* flag set (`ro_sandbox`, which nests inside the envelope when driven by the counter) or with the
envelope itself; each is shown with its exact command. Envelope:

```
/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
```

## 1. Full counter re-run inside the envelope — the landing measurement reproduces

```
$ bwrap <envelope> /usr/bin/python3 plans/round41_c1_verify.py --lane . --work "$S/work" --jobs 8
PINS total=2 mismatched=0
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass                                                       rc=0
```

48 `FIXTURE … ok` lines, 23 `MUTANT … killed by=…` lines, zero `WRONG|SURVIVED|TAMPERED|NULL|SETUP` lines
(`receipts/counter-run.txt`, sha256 `28ff2d55…`). Runtime 16:14:16→16:14:22. Run twice more under `strace -f`
(same pass). Battery on disk: 7 modules, 48 fixtures, digests
`r_setup a693fc51 r_run 1ccb08aa r_ctl 2fcbbcb7 r_map 705a4b7c s_usage c9ca3abe s_modes 1023433b s_exit 5f57cec9`.

## 2. Containment: nothing appeared outside my scratch

| Check | Command | Result |
|---|---|---|
| host files changed | `find /home/vgpnk -xdev -newerct $S/stamp …` (prunes `.omp .cache .zcode .grokbot .local/state .config go`) | **0** |
| SysV IPC | `ipcs -a` before / after | **identical** (all three tables empty) |
| POSIX shm | `ls -la /dev/shm` | empty before and after |
| `/tmp`, `/run/user/1000` | `find /tmp /dev/shm /run/user/1000 -xdev -newerct $S/stamp` | no entries |
| shared PATH dir | `find ~/.local/bin -printf '%f %T@ %s\n' \| sort` before/after | **identical**, 101 entries |
| lane clone | `git -C $S/lane status --porcelain`; `PINS-AFTER` | clean; `mismatched=0` |
| counter scratch | `ls -A $S/work $S/work2 $S/work3` | 0 entries each (its `finally: rmtree` ran) |
| survivors | `pgrep -af k41-c1\|round41_c1_verify` | none of mine (matches shown belong to peer seats) |

Syscall-level (whole run under `strace -f`, 613,817 lines, `%file`+network+IPC classes):

* successful mutating syscalls with an **absolute** path outside my scratch: `symlinkat /proc/kcore` ×661 — one per
  `bwrap` launch, created inside bwrap's private `newroot`, invisible to the host. Nothing else.
  (`mkdir/rename/unlink/openat/chmod` all resolve under `$S`; the 20k relative `mkdirat/symlinkat/link` are bwrap's
  private-root setup.)
* network: `socket/connect` — every `AF_INET` (750) and `AF_INET6` (600) connect returned `ENETUNREACH`; **0**
  successful IP connects. `AF_UNIX` connects succeeded only to `/run/systemd/resolve/io.systemd.Resolve` (§4 F1).
* IPC: **zero** `shmget/msgget/semget` calls by any traced process (confirmed by the empty `ipcs` after).
* host reads made by the run are interpreter/sandbox overhead only, by prefix: `/usr/lib` ×152,746,
  `/usr/share` ×6,983, `/etc/ld.so.cache`, `/usr/bin`, `/proc/sys`, `/etc/passwd`, `/etc/localtime`,
  `/usr/pyvenv.cfg`, plus bwrap's `/newroot`, `/oldroot`.

## 3. The battery itself: no host write, network, socket, persistence, IPC, symlink or outside read

**Static (7 modules read in full, raw).** Only imports are `from __future__ import annotations` (5 modules) and none
at all in `r_setup`/`s_modes`. No `os`, `subprocess`, `socket`, `ctypes`, `urllib`, `pathlib`, `shutil`. No `/proc`,
`/home`, `/usr`, `/etc`, `/tmp` literal except one receipt *content* string (`scratch=/tmp/tmp8kq2zr41`, `r_run:77`),
no `HOME`, no `environ`, no `symlink`/`link`/`chmod`/`fork`/`setsid`/`daemon`. The only URLs are inert registry
cell text (`example.invalid`, plus the real TB2/GitHub URLs in `s_usage`) — `sources_adopt.py` parses URLs with
`URL_RE` and never fetches (no HTTP client import anywhere in it).

**Generated content is inert.** Generated probes (`built/…/plans/*.py`) contain, in total: `import sys` ×39,
`sys.stdout.write(...)` ×50+, `sys.exit(...)` ×10, and one `import tempfile` + `tempfile.mkdtemp()` (`r_run` T04).
No walk, no read, no `/proc`, no argv or file access.

**Rebuilt every module through the counter's own build child** (`--build-module`, inside a bwrap of the same flag
set) and scanned the trees: 1,038 files, **0** symlinks/FIFOs/devices/sockets, **0** references to `/home/vgpnk`,
`/fast/scratch` or `.local/bin`. The only absolute-path hits anywhere are git's stock `*.sample` hooks that
`git init` writes (never executed: tool runs set `core.hooksPath=/dev/null` and the build child's repos carry only the stock `*.sample` hooks).

**Registry files the battery writes** are plain fixture-local data, all under the fixture dir: `corpus/SOURCES.md`
and `corpus/SOURCES.append.md` (`s_usage`, `s_modes`), `.ufo/waves/round-41/SOURCES.append.md` (`s_exit`, relative
token resolved against `cwd` = the fixture dir). No row points `used-by`/`--entries` at a host path.

**The `Ctx` write API resists the symlink and absolute escapes it would be attacked with:**

```
$ python3 -c 'ctx.write(d/"link"/"PWNED", ...)'      # d/link -> /home/vgpnk/.local/bin
SYMLINK-WRITE=refused path outside the fixture root: /home/vgpnk/.local/bin/PWNED
ABS-WRITE=refused
SYMLINK-INIT=refused path outside the fixture root: /home/vgpnk/.local/bin
$ ls /home/vgpnk/.local/bin/PWNED /etc/PWNED-R41 → No such file or directory (both)
```

`_inside()` (`round41_c1_verify.py:256-261`) resolves before comparing, so a symlinked parent cannot be used by
`write`/`init`/`git`/`sh`. The build sandbox is then the second line of defence.

## 4. Findings

### F1 — MEDIUM — the sandbox leaves the host name service (and every `/run` AF_UNIX service) reachable; ordinary `git` uses it, and a battery module can too without tripping `SIDECHANNEL`

`ro_sandbox` (`round41_c1_verify.py:317-327`) passes `--unshare-pid --unshare-net` but no `--unshare-ipc` and no
`--tmpfs` for `/run`. `--unshare-net` isolates IP only; filesystem AF_UNIX sockets stay connectable under
`--ro-bind / /`. Observed inside the counter's *exact* flag set:

```
$ bwrap --ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent --new-session \
    /usr/bin/python3 -c 'socket.connect("/run/systemd/resolve/io.systemd.Resolve")'
VARLINK-CONNECT=ok
```

It is not merely reachable, it is used, 135 times in one counter run — `git clone -q --shared`, which
`tip_receipts.py:270` runs for every receipt re-run, resolves the local host name through nss-resolve:

```
266 execve("/usr/sbin/git", ["git", "clone", "-q", "--shared", …]) = 0
266 connect(6, {sa_family=AF_UNIX, sun_path="/run/systemd/resolve/io.systemd.Resolve"}, 42) = 0
266 connect(6, {sa_family=AF_INET, sin_port=htons(0), sin_addr=inet_addr("192.168.0.253")}, 16) = -1 ENETUNREACH
266 connect(6, {sa_family=AF_INET6, … "enp7s0"}, 28) = -1 ENETUNREACH
```

Minimal reproduction (env of `Runner.env()`; `AF_UNIX = 0`, all IP connects `ENETUNREACH`):

```
$ env -i PATH=… HOME=<empty> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
    bwrap --ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent --new-session \
          --bind $S $S /usr/bin/git clone -q --shared $S/clone_src $S/clone_dst
connect(AF_UNIX "/run/systemd/resolve/io.systemd.Resolve") = 0
```

**The scan does not see this class of use.** `SIDECHANNEL` (`:109`) is source text, lower-cased, matched against a
token list that has `socket`, `/proc`, `environ`, `fork`, `setsid` … but no `getent`, `resolv`, `nss`, `dbus`,
`systemctl`, `curl`, `clone`. Demonstrated in development mode with two throw-away modules of mine (never in the
lane):

```
blind   (build() runs ctx.sh("getent","hosts","localhost")) → BATTERY fixtures=1 wrong=0 … sidechannel=0
control (same shape + literal token `socket`)               → SIDECHANNEL …tokens=socket ; sidechannel=1
blind module's build child saw: getent rc=0 out=::1             localhost
```

Impact: (a) a name lookup performed by a *host* daemon is egress that `--unshare-net` does not stop — a module can
encode into a DNS label and the query leaves the machine (resolved does the lookup, not the sandbox); (b) any
host AF_UNIX service (session bus, agent sockets, systemd) is reachable, which is the escape path around every
`EROFS` result in §2; (c) both are invisible to the only automated anti-cheat C1 has. For *this* battery the only
user is the harness's own `git`; **no landed module uses it** — this is a counter/admission defect, not a landed
misbehaviour.

Smallest remediation: add `--unshare-ipc --tmpfs /run/systemd --tmpfs /run/dbus` to `ro_sandbox` (mask `/run`
beyond what the tools need), and add `getent|resolv|nss|dbus|systemctl|bus` to `SIDECHANNEL`.

### F2 — LOW — SysV IPC namespace is shared: an object created inside a sandbox outlives it on the host

Same missing `--unshare-ipc`. Confirmed once, then removed (host restored to the pre-run `ipcs`):

```
$ bwrap --ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent --new-session \
    python3 -c 'libc.shmget(0x4b343173, 4096, IPC_CREAT|0644)'
shmget-inside shmid= 3 errno= 0
$ ipcs -m                     # host, after the sandbox exited
0x4b343173 3          vgpnk      644        4096       0
$ ipcrm -m 3 ; ipcs -a | diff ipcs-before.txt -   → ipcs-restored-identical
```

The landed battery makes **zero** IPC syscalls (§2), so nothing leaked in the real run; the channel is open and a
`--jobs 8` keyed segment would also be a cross-run channel. Remediation: `--unshare-ipc` (one flag).

### F3 — INFO — `--work` is only checked for "not inside the lane"

`main()` (`:525-529`) refuses `--work` inside the lane but accepts any other host path, then `mkdtemp`s
`k41-c1-*` there and `rmtree`s it in `finally`. `--work /home/vgpnk/.local/bin` would create and delete a tree in a
shared PATH directory (the class of accident that made round 40's `git` shim memorable). Under the mandated
envelope it fails closed (`--ro-bind` makes `.local/bin` read-only), and I found no such path in the landed
battery or in the dispatch. Smallest remediation: also refuse `--work` under `$HOME` and any directory on `PATH`.

## 5. Answers to the assigned questions

| Question | Answer (evidence above) |
|---|---|
| host write by the battery/probe stubs/registries | none — 0 host files changed (ctime scan), 0 absolute-path mutations outside scratch in 613k trace lines; `Ctx` refuses symlink/absolute escapes |
| network use | no IP egress (`--unshare-net`, all connects `ENETUNREACH`, 0 successes); **AF_UNIX to host systemd-resolved succeeds and is used by `git` (F1)** — no battery module uses it, and the token scan would not see it |
| socket use | none in any module or generated probe; the sandbox itself leaves host sockets connectable (F1) |
| process persistence | none — per-run `work`/`tmp` empty, no surviving `bwrap`/probe of mine; `--unshare-pid`+`--die-with-parent`+`--new-session` |
| IPC | battery: none (0 IPC syscalls); sandbox: SysV IPC shared with the host (F2, demonstrated and cleaned) |
| symlink tricks | none in the battery; generated trees contain 0 symlinks; `Ctx.write/init` refuse a symlinked parent that resolves outside the fixture root |
| reads outside the fixture dir | battery modules read nothing (no read API, no constants pointing out); tool runs read only loader/locale/`/etc/passwd` and the fixture lane; the lane itself is `--ro-bind` read-only |
| full counter in the envelope, no file outside scratch | confirmed: `PREDICATE C1 pass`, rc=0, `find /home/vgpnk -newerct` → 0, `ipcs` identical, `/dev/shm`, `/tmp`, `/run/user/1000`, `~/.local/bin` untouched |

## 6. Reproduction

```bash
S=/fast/scratch/hyaku/kengaku-r41/<seat>; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
E=(bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
   --proc /proc --unshare-pid --die-with-parent)
touch "$S/stamp"; ipcs -a > "$S/ipcs-before.txt"
"${E[@]}" /usr/bin/python3 "$S/lane/plans/round41_c1_verify.py" --lane "$S/lane" --work "$S/work"   # §1
find /home/vgpnk -xdev -newerct "$S/stamp" … ; ipcs -a | diff "$S/ipcs-before.txt" -                   # §2
# §4 F1 — host resolved reachable inside the counter's own flags:
bwrap --ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent --new-session \
  python3 -c 'import socket;s=socket.socket(socket.AF_UNIX);s.connect("/run/systemd/resolve/io.systemd.Resolve")'
# §4 F1 — scan blind spot: module whose build runs ctx.sh("getent","hosts","localhost")
"${E[@]}" python3 "$S/lane/plans/round41_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat_blind2" \
  --only T01 --work "$S/wb" --jobs 2      # → FIXTURE … ok, BATTERY … sidechannel=0
# §4 F2 — then `ipcrm -m <id>` from the host and `ipcs` to restore
```

Receipts: `.ufo/waves/round-41/falsify/F41SentinelBattery/receipts/` (counter output, trace summaries, ipcs
before/after, `~/.local/bin` listings, host-ctime scan, git-resolve trace, blind-getent build output, `Ctx`
escape test, rebuilt-fixture scan).

VERDICT: battery-security-findings-3
