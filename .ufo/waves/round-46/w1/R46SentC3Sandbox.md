# R46SentC3Sandbox — design review of the C3 polyglot probe's sandbox, before it runs

Seat `R46SentC3Sandbox` (sentinel, leaf), round 46 wave 1, 2026-10-27. Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. I read `plans/round-46-claims.md` in full first, plus the
round-45 closure (`corpus/lessons/round-45-verifier-spotcheck.md` §2, §5) and `corpus/QUALITY.md` Q32 (`:626-643`).

**What this review audits.** The C3 draft probe *as it stands in wave 1*, not a frozen file:
`.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py`, sha256 `67a8f4a68fcdf190…`, 526 lines, mtime 02:11.
Its own input pin matches the captured grader I ran against (`test_outputs.py` sha256 `b94a7a9882decd81…` =
`PINS["test_outputs.py"]`). Nothing here imports that grader or executes a case: the payload is a **hostile polyglot
`main.py.c` this seat wrote**, executed only inside bwrap sandboxes this seat built (the task's own instruction).

**Nothing in the lane was edited by this seat.** All artifacts are in `.ufo/waves/round-46/w1/R46SentC3Sandbox/`
(this dir) and the scratch dir, which was removed at the end.

## 1. Axes and moves (godspeed)

Axes: **host safety (writes)**, **host safety (resource DoS)**, **operability (does the hardening still compile and run
the task's own toolchain)**, **coverage (does the review answer the six questions the item asks)**. Moves kept are the
ones that improved at least one axis and harmed none: every claim below is a measured run under the round-46 envelope
(receipts `receipts.txt`); the two "read the code" claims are marked as such.

Method: take the draft's *own* `sandbox_argv()` and `ENV` (imported from the peer's file, md5-stable, no write into
its directory), run one hostile payload through them, then run the same payload through the same argv plus the flags
this seat recommends. The payload is a real C/Python polyglot (so the **same bytes** are executed by both runtimes,
which is the task's subject) with modes: `safe` (writes outside /app, network, forks, limit dump), `forks`, `mem`,
`fill`, `bigout`, `cpu`.

## 2. Runs (envelope, Q32)

All runs: `claims/envelope.sh <scratch>/env-<tag> <command…>`; the full ENVELOPE line, start/end time and
`local_bin_content_before/after` for all 14 runs are in `receipts.txt`. Digest drift `ff187bb5…`→`7747d38e…` happened
**between** envelopes [2] and [3] (another seat's install), never inside one; every run is internally `unchanged`.

| # | run | command (abridged) | envelope start→end | digest |
|---|---|---|---|---|
| 1 | draft matrix | `python3 runner.py --variant draft` | 02:19:06→02:19:25 exit=0 | `ff187bb5…` unchanged |
| 2 | hard v1 | `--variant hard` (rlimits + uts + clearenv + sized /app) | 02:19:42→02:20:01 exit=0 | `ff187bb5…` unchanged |
| 3 | output cap | `--variant hard --stop-after 65536 --only bigout` | 02:20:38→02:20:53 exit=0 | `7747d38e…` unchanged |
| 4 | envelope access | `os.access` on 11 host paths (no writes) | 02:21:05→02:21:08 exit=0 | `7747d38e…` unchanged |
| 5 | stub-Bio, wrong | PYTHONPATH set after start (no effect) | 02:21:42→02:21:44 exit=1 | `7747d38e…` unchanged |
| 6 | stub-Bio, right | `env PYTHONPATH=…/stubbio python3 -c <branch>` | 02:22:02→02:22:04 exit=0 | `7747d38e…` unchanged |
| 7 | tmpfs/remount | `--size 8M --tmpfs`; `--remount-ro /` | 02:22:53→02:22:54 exit=0 | `7747d38e…` unchanged |
| 8 | hard v2 | v1 + `--remount-ro /` last | 02:23:42→02:23:57 exit=0 | `7747d38e…` unchanged |
| 9 | unshare-all | `--unshare-all --hostname` | 02:25:02→02:25:03 exit=0 | `7747d38e…` unchanged |
| 10 | env + /pub | payload env dump; /pub,/tests writes | 02:26:01→02:26:03 exit=0 | `7747d38e…` unchanged |
| 11 | /dev, /dev/shm | statvfs + writes with no extra flags | 02:26:48→02:26:49 exit=0 | `7747d38e…` unchanged |
| 12 | /dev ro, shm sized | `--size 8M --tmpfs /dev/shm --remount-ro /dev` | 02:27:11→02:27:12 exit=0 | `7747d38e…` unchanged |
| 13 | final matrix | all recommended flags, both runtimes | 02:27:33→02:27:48 exit=0 | `7747d38e…` unchanged |
| 14 | tight bounds | `R46_AS=256 R46_NPROC=16`, modes safe/mem/forks | 02:28:50→02:28:53 exit=0 | `7747d38e…` unchanged |

No run wrote to `~/.local/bin`, `/usr`, `/etc` or `$HOME`; the envelope's `unchanged` digest brackets every one.

## 3. The audited invocation, exactly

`polyglot_c_py_probe.py:347-362` (the whole sandbox):

```
bwrap --unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session
      --ro-bind /usr /usr  [--symlink /bin,/sbin,/lib,/lib64 → usr/…]
      --ro-bind /etc /etc  --proc /proc  --dev /dev  --tmpfs /tmp
      --bind <work>/app /app  --ro-bind <work>/tests /tests  --dir /pub  --dir /tpl
      --ro-bind <cap>/{instruction.md,test_outputs.py,solve.sh} /pub/<name>
      --ro-bind <work>/{template.txt,seed.sh,recipe.sh,harness.py} /…  --chdir /app
```
with `ENV = {PATH, HOME:/tmp, TMPDIR:/tmp, LANG, LC_ALL, PYTHONUTF8, PYTHONDONTWRITEBYTECODE}` (`:366-367`),
`harness()` = `subprocess.run(…, env=ENV, capture_output=True, text=True, timeout=1800)` (`:370-373`), and
`run_case()` = seed/recipe leg + **two** grade legs, i.e. three sandbox invocations per case (`:376-394`).

Measured inside it (`draft.txt`, both runtimes identical):

```
LIMIT CPU soft=-1 hard=-1          # RLIMIT_CPU: no limit
LIMIT NPROC soft=122865            # = the host's max_user_processes
LIMIT FSIZE soft=274877906944      # inherited from the ancestor, ~256 GiB
LIMIT AS soft=-1 hard=-1           # no address-space limit
LIMIT CORE soft=-1 hard=-1         # cores enabled (host core_pattern is piped to systemd-coredump)
LIMIT NOFILE soft=524288
POLY lang=PY|C mode=safe uid=1000 host=plazir27 ncpu=32
```

So the mount geometry is right and the **bounds are absent**: the sandbox is a name-space fence with no resource
fence at all.

## 4. Measured containment (no escapes in either variant)

| surface | target | draft | final (recommended) |
|---|---|---|---|
| intended rw bind | `/app/inside.txt` | ok | ok (now a 64 MiB tmpfs) |
| private tmp | `/tmp/tmp-ok.txt` | ok | ok (8 MiB tmpfs) |
| host home | `/home/vgpnk/…/w1/R46SentC3Sandbox/ESCAPE-home.txt` | `ENOENT` | `ENOENT` |
| host root home | `/root/ESCAPE-root.txt` | `ENOENT` | `ENOENT` |
| host scratch | `/fast/scratch/…/markers/ESCAPE-fast.txt` | `ENOENT` | `ENOENT` |
| config | `/etc/ESCAPE-etc.txt`, `/usr/ESCAPE-usr.txt` | `EROFS` (30) | `EROFS` |
| root tmpfs | `/ESCAPE-root-tmpfs.txt`, `../ESCAPE-dotdot.txt` | **ok** (writable) | `EROFS` |
| proc root | `/proc/1/root/ESCAPE-proc1.txt` | **ok** (= sandbox root) | `EROFS` |
| network | `1.1.1.1:80` / `127.0.0.1:22` | `ENETUNREACH`(101) / `ECONNREFUSED`(111) | same |
| fingerprint | `gethostname()` | **`plazir27`** (host), `ncpu=32` | `k46sent`, `ncpu=32` |
| host artifacts | `app_bytes` left on the host after a case | **24,891** (cmain+inside.txt) / 7,483 (py) | **0** |

**Escapes: 0 in both.** The difference is not reach but *bounds*: the draft leaves writable, unsized surfaces and
leaves compiled artifacts on the host.

## 5. Risk table — draft vs the measured mitigation

| # | Risk | Draft (measured) | Recommended flags (measured) |
|---|---|---|---|
| R1 | network reach | `ENETUNREACH`, `ECONNREFUSED` | `--unshare-all` (or `--unshare-net`) → same |
| R2 | host `/home`, `/root` visible | `ENOENT`, not bound | `--clearenv --setenv HOME=/tmp` + no home bind → `ENOENT` |
| R3 | host `/fast`, host `/tmp` visible | `ENOENT` (not bound) | same |
| R4 | `/etc`, `/usr` writable | `EROFS` | same (keep the ro-binds) |
| R5 | root tmpfs writable, huge | **writable**; `statvfs /` = 3,965,224×4096 = **15.1 GiB** | `--remount-ro /` **last** → `EROFS` |
| R6 | `/dev` + `/dev/shm` writable, ~15 GiB each | **writable** (`/dev/x`, `/dev/shm/x` ok) | `--dev /dev --size 8M --tmpfs /dev/shm --remount-ro /dev` → `/dev/x` `EROFS`, `/dev/null` still writable, shm `ENOSPC` at 8,388,608 |
| R7 | fork bomb | 96 forks: **96 ok, 0 fail** | `--nproc=48`: 43 ok / 53 `EAGAIN`; `--nproc=16`: 11 ok / 85 `EAGAIN` |
| R8 | CPU spin / infinite loop | `RLIMIT_CPU=-1`; only the harness's 1800 s ends it | `--cpu=5` → kernel SIGKILL, rc=137 at ~5.3 s |
| R9 | process memory blowup | 512 MiB malloc **ok** | `--as=512M` → `MemoryError`/`ENOMEM`; `--as=256M` also compiles gcc |
| R10 | disk fill through the `/app` host bind | 5,242,880 B written into `/fast` scratch | `--size 64M --tmpfs /app` + `--fsize=1M` → stop at 1,048,576 (py `EFBIG` 27, C `SIGXFSZ` rc=153) |
| R11 | unbounded stdout buffering | 8,388,874 B emitted; `capture_output=True` on both sides holds it in RAM | reader **stops** at 64 KiB → writer blocks, 64 KiB kept, killed (rc=-9, `timed_out=True`) |
| R12 | host fingerprint / env inheritance | `host=plazir27`; env passed only as a `subprocess(env=)` kwarg | `--unshare-uts --hostname k46sent --clearenv --setenv …` → `host=k46sent`, exactly **8** env vars, `HOME=/tmp`, `PATH` head `/usr/local/sbin` |
| R13 | wrapper runs the probe **outside** bwrap | `import Bio` → `ModuleNotFoundError` ⇒ frozen gate runs `uv run --with biopython==1.85` (`pkg_gate.py:273-276`), resolved as `/home/vgpnk/.local/bin/uv` | `PYTHONPATH=<scratch>/stubbio` with a one-line `Bio/__init__.py` → branch takes `[sys.executable] + probe` (measured `BRANCH /usr/bin/python3`) |

R5/R6 are why the root tmpfs matters: `--remount-ro /` alone leaves `/dev` and `/dev/shm` writable (measured in run
[11] before the fix), and the *only* way to bound them is the sized `--tmpfs /dev/shm` plus `--remount-ro /dev`.

## 6. The round-45 "HOME escape", and what actually applies

**6.1 The citation does not resolve.** The item and `SCORECARD.md:2014-2015` name
`w1/R45SentinelC2Sandbox.md` ("a probe run escapes the seat sandbox's HOME (`/root/.local` writes …)").
Measured: `ls .ufo/waves/round-45/w1/R45SentinelC2Sandbox.md` → `No such file or directory`;
`git log --all -- '.ufo/waves/round-45/w1/R45SentinelC2Sandbox.md'` → empty; the string first appears in
`4290d64` (the round-45 SCORECARD section), and `.ufo/` is tracked (15,653 files), so absence is meaningful. The
lane's only `/root/.local` string is round-37's `R37DockerOracle.md:160` (`installing to /root/.local/bin`, inside a
Docker container). `w2/R45ExecNoHarm.md:124` quote the same SCORECARD phrase.

**6.2 What the round-45 sandbox seat actually recorded.** `.ufo/waves/round-45/w1/R45SentC2Sandbox.md:56` (row E2)
records `ls /home /root /sys /var /run` → `No such file or directory` ×5, and `:74` answers "Q `/home` bound? No."
with `/root` ENOENT; `:44` says the seat "never wrote to any PATH directory or `$HOME`". So the *recorded* sandbox had
no `/root` at all, and the escape as cited is unreproducible from any lane artefact. My own payload reproduces the
same result twice (`/root` and `/home` ENOENT, §4) — for both runtimes.

**6.3 The class is nonetheless live for C3, in toolchain form.** A `$HOME` write in a probe run comes from a *tool*,
not from the payload: `uv` installs a managed CPython under `~/.local`/`~/.cache` and executes it on the host. Round 45
measured exactly that for the previous package (`a3w1/R45SentC2Grader.md` F1: `uv run --with biopython==1.85` executed
outside bwrap, 143 MB of `~/.cache` per run). For this round it is **live, not hypothetical**: host `python3` is
3.14.8, `python3 -c "import Bio"` → `ModuleNotFoundError`, and `which uv` → `/home/vgpnk/.local/bin/uv` (run [4]), so
the frozen gate's `c_rerun` takes the `uv` branch for C3's V2 leg. Under the round-46 envelope that is contained by
the home ro-bind and the `~/.cache` overlay; **outside** it (a counter run without the envelope) it installs into
`$HOME`. The measured fix (run [6]) keeps the frozen gate untouched: `PYTHONPATH` at a two-line stub makes `import Bio`
succeed, the probe then runs under `sys.executable`, and nothing leaves bwrap.

## 7. Recommended invocation (the answer to "what must it unshare/bind")

The final variant in `runner.py` (`harden()`), dumped verbatim to `final-argv.txt`, with `<work>` as the case dir:

```
/usr/bin/prlimit --nproc=16 --cpu=5 --fsize=1048576 --core=0 --as=268435456 --nofile=512 -- \
/usr/bin/bwrap --unshare-all --die-with-parent --new-session --hostname k46sent \
  --ro-bind /usr /usr  [--symlink usr/bin /bin, /sbin; usr/lib /lib, /lib64]
  --ro-bind /etc /etc --proc /proc --dev /dev \
  --size 8388608  --tmpfs /dev/shm  --remount-ro /dev \
  --size 8388608  --tmpfs /tmp \
  --size 67108864 --tmpfs /app  --ro-bind <work>/main.py.c /app/main.py.c \
  --ro-bind <work>/tests /tests  --dir /pub  --ro-bind <cap>/{instruction.md,test_outputs.py,solve.sh} /pub/ \
  --ro-bind <work>/{seed.sh,recipe.sh,harness.py} /… \
  --clearenv --setenv PATH=… --setenv HOME=/tmp --setenv TMPDIR=/tmp --setenv LANG/LC_ALL=C.UTF-8 \
  --setenv PYTHONUTF8=1 --setenv PYTHONDONTWRITEBYTECODE=1 \
  --remount-ro /  \
  --chdir /app /usr/bin/python3 /harness.py <mode>
```

plus, in the *runner*: `subprocess.Popen(…, start_new_session=True)`, a **wall-clock timeout of ~60 s** with
`os.killpg(…, SIGKILL)`, and a stdout reader that stops at a 1 MiB cap. Two ordering facts, both measured:

* `--size N` sizes **the next** `--tmpfs` (`bwrap --help`: "Set size of next argument (only for --tmpfs)"); putting
  `--size` after the mount silently leaves the tmpfs unbounded.
* `--remount-ro /` must be the **last mount option**. Placing it before another bind fails hard:
  `bwrap: Can't create file /run.sh: Read-only file system` (measured, exit 1 for all 12 rows of that attempt).

`--unshare-all` was measured separately (run [9]): `hostname=k46all`, `/proc/self/cgroup` = `0::/` (fresh cgroup ns,
no host path leak), 8 namespaces, root `EROFS`. It is a superset of the explicit `--unshare-net/pid/ipc` + `--unshare-uts`
I used in `harden()`; either is fine, `--unshare-all` is harder to under-specify later.

**Aggregate bound arithmetic.** Writable surfaces after the fix: `/tmp` 8 MiB + `/app` 64 MiB + `/dev/shm` 8 MiB =
80 MiB of tmpfs per sandbox, `/` and `/dev` read-only, no host bind. Process memory is bounded per process by
`--as`, so the aggregate is `nproc × as`: 48×512 MiB = 24 GiB is **above** this host's 17 GiB available (measured
`free -g`), 16×256 MiB = 4 GiB is comfortably below — and 16/256 still compiles the polyglot with gcc 16.2.1 (run [14],
`POLY lang=C` printed, no compiler error). Pick `nproc × as` below available RAM; do not rely on `--nproc` alone.

## 8. Findings (severity · exploit path · evidence · impact · smallest remediation)

**F1 — HIGH (safety + reproducibility): the wrapper executes unpinned remote code outside the sandbox.**
Exploit path: any C3 counter run on a host whose `python3` cannot `import Bio` → `plans/pkg_gate.py:273-276` resolves
`uv` from `PATH` (`/home/vgpnk/.local/bin/uv`, measured) and runs `uv run --with biopython==1.85 python3 <probe>` as
`vgpnk`, outside bwrap, fetching a wheel set **and a managed CPython** from PyPI, then executes the probe with it.
Evidence: run [4] (`BIO host=ModuleNotFoundError`, `WHICH uv /home/vgpnk/.local/bin/uv`); the same path measured on the
round-45 package (`.ufo/waves/round-45/a3w1/R45SentC2Grader.md` F1, 143 MB in `~/.cache`). Impact: a replaced PyPI
artefact executes on the verifying host and can rewrite the receipt the gate then compares byte-for-byte; V2 is
network-dependent, so the claim is not reproducible offline. Remediation (measured, run [6]): give the gate subprocess
`PYTHONPATH=<scratch>/stubbio` with `Bio/__init__.py` = `version = "1.85"`; the frozen gate then uses
`[sys.executable] + probe` and the probe (stdlib-only) runs under `/usr/bin/python3`.

**F2 — HIGH (DoS): no resource limits at all.** `RLIMIT_CPU=-1`, `NPROC=122865`, `AS=-1`, `CORE=-1`, `FSIZE` ≈ 256 GiB
(dumped from inside the draft sandbox, both runtimes). Measured concrete effects: 96/96 forks succeed; a 512 MiB
touched allocation succeeds; 5 MiB written into the host `/app` bind; a spin loop is bounded only by the harness's
1800 s. Impact: a fork/alloc loop inside one case converts to host-wide pid/memory pressure (a new pid namespace still
consumes host pids; there is no pids or memory cgroup). Remediation: `prlimit --nproc/--cpu/--fsize/--as/--core` on
the bwrap argv as in §7, with `nproc × as` under available RAM.

**F3 — MEDIUM (DoS): stdout is unbounded on both sides.** The captured grader uses `capture_output=True` with no
timeout on the payload (`test_outputs.py:30-42`), and the probe's `harness()` buffers the whole sandbox output
(`:372`). Measured: 8,388,874 B of payload stdout delivered into the parent's memory; a 10 GiB emitter costs 10 GiB of
sandbox-python RSS (arithmetic on the measured 8.4 MB, not a run). Remediation: keep a cap in the *reader* and stop
reading at the cap, then `killpg` (measured, run [3]: 64 KiB kept, writer blocked, rc=-9).

**F4 — MEDIUM (DoS): three writable, unsized tmpfs.** The root tmpfs is writable (`/ESCAPE-root-tmpfs.txt` ok) and so
are `/dev` and `/dev/shm`; `statvfs` reports 3,965,224 blocks (15.1 GiB) for `/` and the same for `/dev/shm`, and
`/dev/x`, `/dev/shm/x` both wrote. Impact: ~15 GiB of RAM per surface, ×3, from one hostile case. Remediation measured:
`--remount-ro /` last, `--size 8M --tmpfs /dev/shm`, `--remount-ro /dev` (§7); `/dev/null` still writable.

**F5 — MEDIUM (operability): 1800 s × 3 legs per case.** `harness()` `timeout=1800` (`:372`) and `run_case()` runs it
three times (`:393`), so a single looping payload can consume 90 minutes; the task's own verifier timeout is 900 s
(`task.toml`), i.e. the sandbox is 6× more permissive than the bench. Remediation: 60 s per invocation + `SIGKILL`
the group; measured kill path in R8/R11.

**F6 — LOW (host residue): the `/app` host bind leaves case artefacts on the host.** Measured `app_bytes` after one
case: 24,891 (C leg: `cmain` + `inside.txt`) and 7,483 (py leg) on the draft; **0** after `--tmpfs /app`. Impact: a
host disk write path and untracked files under `--work` (which the probe deletes, but a crash leaves them).
Remediation: `--tmpfs /app` (measured; nothing in the receipt is read back from `/app`).

**F7 — LOW (fingerprint): hostname, cpu count, `/etc` ro-bind.** `gethostname()` = `plazir27`, `ncpu=32`,
`/etc/machine-id` readable (round-45 §7.5 still applies). Remediation: `--unshare-uts --hostname k46sent` (measured
`host=k46sent`); the cpu count is not maskable without cpuset cgroups and is harmless for this grader.

**F8 — LOW: `/pub`'s directory is writable** (round-45 §7.4 recurrence: `--dir /pub` lands on the rw root tmpfs).
Measured after `--remount-ro /`: `/pub/planted.txt` → `EROFS` while `/pub/f.txt` stays readable and `/tests/*` is
`EROFS`. Remediation: the remount also closes this; no separate change needed.

**F9 — LOW (environment): the envelope is a recorder, not a sandbox.** Measured with `os.access` only (no writes):
inside the envelope `/fast` and `/tmp` are writable, `~/.cache` is the scratch overlay, `$HOME`, `~/.local` and
`~/.local/bin` are not (`False`), `/usr`, `/etc`, `/root` are `False` (mode bits; writing there would need a
world-writable host dir). Consequence: anything the probe runs **outside** its own bwrap inherits `/fast` and `/tmp`
writes — the reason F1's `uv` path must be closed rather than merely bracketed.

**F10 — LOW (provenance): the cited round-45 HOME escape does not exist as a seat report.** Evidence §6.1. Impact:
the item's premise and `SCORECARD.md:2014-2015` attribute an unreproducible escape to a file that was never written,
while the actual seat `R45SentC2Sandbox` measured `/home` and `/root` ENOENT. Remediation: the L1 appends a correction
line naming `w1/R45SentC2Sandbox.md` (and the `/root/.local` string's only lane occurrence, round-37's Docker note),
or drops the row.

**F11 — INFO: core dumps are not disabled.** Host `core_pattern` is
`|/usr/lib/systemd/systemd-coredump … %h %d %F %I` and the draft's `RLIMIT_CORE` is unlimited [INFERENCE for the dump
path itself: I did not crash a payload with cores enabled, so as not to write under `/var`]. `--core=0` makes the
kernel skip the handler; measured inside the final sandbox (`LIMIT CORE soft=0 hard=0`).

**F12 — INFO: mountinfo discloses host source paths.** `--ro-bind <work>/…` exposes the scratch path in
`/proc/self/mountinfo` as read-only strings (round-45 §7.6). The probe's receipt prints only `TEST`/`STAGE`/`CASE`
lines, so payload output never reaches it; no action needed beyond knowing it.

**F13 — INFO: post-run host handling of `/app` must not follow symlinks.** A payload can plant `/app/x -> /etc/passwd`
(dangling inside the sandbox). `shutil.rmtree(work)` unlinks symlinks and is safe; a future `cp -r`/`tar -h` of a case
dir would not be. Keep `rmtree`, or use `--tmpfs /app` and there is nothing to remove.

## 9. Limits of this audit

* One bwrap (0.13.1, not setuid, unprivileged userns on), one gcc (16.2.1) and one python3 (3.14.8) on this host; the
  claim's own limit (host toolchain standing in for gcc 13.2.0 / python 3.12.3) still applies to any verdict the probe
  produces.
* No cgroup was used (no `systemd-run`, no `MemoryMax`): the memory residual is bounded by `nproc × as`, not proven
  under a cgroup. No seccomp filter was written (`--seccomp` exists and is unused); `RLIMIT_NPROC` is the fork bound.
* No 1800 s run: the long window is code evidence (`:372`), the kill behaviour was measured at 8 s.
* The payload's own 8.4 MB output is a sample; the scaling to GiB is arithmetic.
* `/app` as tmpfs changes nothing the receipt reads (verified: `app_files=[]` after every final run), but if a future
  case needs to inspect an artefact *after* the sandbox, it must print it inside instead of reading the bind.
* The audited probe is a **draft** (sha `67a8f4a6…`); if the author amends `sandbox_argv`, re-check §7 against the new
  bytes. Neither the probe nor the grader was executed as a case by this seat, and no sealed module was read.

## 10. Evidence files (this dir) and digests

`draft.txt` (draft-variant matrix, 9.3 KB), `final.txt` (final matrix, 8.0 KB), `hard2.txt` (intermediate v2, 8.1 KB),
`hard-stop.txt` (cap-and-kill, 1.6 KB), `tight.txt` (nproc=16 / as=256M, 2.6 KB), `final-argv.txt` (the measured
invocation, 1.8 KB), `receipts.txt` (all 14 ENVELOPE pairs), and the drafts themselves: `main.py.c` (hostile polyglot,
7,482 B, sha256 `eab42012ebfbffdc…`), `runner.py` (draft runner + `harden()`, sha256 `d18f8a0c1e7f459f…`),
`test_remount.sh`, `test_env_pub.sh`. Every file is < 10 KB; no corpus/plans tree, lane mirror or clone was copied.
Scratch `/fast/scratch/hyaku/kengaku-r46/R46SentC3Sandbox` was removed with `plans/scratch_guard.py safe-rm`.

## 11. Addendum — the author's amended draft (post-review, 02:33)

The probe author applied all six changes and reported the new digest `a96e4226…` (30,238 B, from `67a8f4a6…`), with
`--dry` byte-identical to the freeze file and no case or prediction changed. Sections 3–7 above were measured on the
earlier bytes; the amendment keeps every flag I asked for and adds one structural change that I want on the record,
because it is *forced* by R10 and changes the probe's semantics:

* **One bwrap invocation for four phases.** With `/app` a tmpfs, a per-leg sandbox would reset `/app` between the two
  grade legs and silently destroy the non-idempotence observation the `regrade` column exists for (`leftover-cmain`).
  So seed + recipe + leg1 + leg2 now run in one sandbox over one sized `/app`. That is correct, and it is the right
  reading of my §7: the mitigation moves the persistence into the tmpfs instead of the host bind. Three consequences
  the docstring should state, none of them a defect:
  1. **Phase isolation is gone.** An orphan left by `seed.sh`/`recipe.sh` survives into the grade legs (bounded by
     `--nproc=48` and `--die-with-parent`, and both recipes are the probe's own frozen text, so the exposure is small);
     a future per-case recipe authored by an agent would need the pid namespace reset per phase.
  2. **One 60 s budget now covers four phases.** A leg-1 timeout kills the invocation, so leg 2 never runs and the
     receipt shows `regrade=-`, not `same`. The `letters()`/`regrade_tag()` mapping already renders `-`, so this is a
     disclosure, not a code change.
  3. **The payload's `capture_output=True` residue is now bounded by `--as`.** With `test_outputs.py:30-42` frozen,
     a huge emitter still allocates inside the sandbox python, but `--as=512M` turns host pressure into a `MemoryError`
     inside the harness → no verdict line and an ambiguous `exit=…-no-verdict-line` note. That is the correct trade
     (the alternative is editing a frozen capture), and it belongs in the limits paragraph as a measured limit.
* **`--fsize=1M` is rejected by `prlimit`; bare bytes are required.** The author's deviation is right and my own draft
  used bare bytes (`--fsize=1048576`, `--as=536870912`); `prlimit` does not parse suffixes. Anyone copying §7 should
  copy the numeric form.
* **Their `/dev/shm` reading is better than mine.** They measured a 9 MiB write stopping at `EFBIG`/1,048,576 (the
  `--fsize` cap biting before `ENOSPC`); my run [12] measured `ENOSPC` at 8,388,608 only because that test used
  `--fsize=64M`. Same bound, different first-firing limit — cite the one that matches the flags in the argv.

* **Terminal revision.** The shipped draft is `22b7779e6ccbea5f…` (31,355 B), superseding the `a96e4226…` named above;
  the author reports it as docstring/sandbox only, with the freeze table pinned at `99adfea6…` unchanged and
  `--stage-check` 18/18 after each revision. Static check on the terminal bytes (read only, nothing executed here):
  `PRLIMIT` prefix with bare byte counts (`:105-108`), `--unshare-all --hostname polyglot-sandbox` (`:382-383`),
  `--size 8388608 --tmpfs /dev/shm --remount-ro /dev` and sized `/tmp` (32 MiB) + `/app` (64 MiB) (`:388-389`),
  `--clearenv` + `--setenv` (`:395-397`), `--remount-ro /` **after every bind** (`:398`), and a `CAP_BYTES = 1 << 20`
  store with `TIMEOUT` kill (`:111,403-419`) — i.e. all of §7 is present, in the order §7 requires.
  One refinement to R11: their reader *keeps draining* and stores at most 1 MiB, where mine *stops reading*; both
  bound parent memory at the cap, but draining leaves the payload's own write behaviour untouched (a blocked writer
  could change what a case observes) and relies on `RLIMIT_CPU` + the wall kill, which are in the same argv. Either is
  acceptable; do not read R11 as prescribing the stop-and-block shape only.

Nothing in this addendum changes the risk count or the verdict; the audited bytes in §3–§7 remain the pre-amendment
draft; a re-review of the shipped `22b7779e…` against §7 needs only the three disclosures above.

VERDICT: polyglot-sandbox-risks-13-mitigated-in-draft-13
