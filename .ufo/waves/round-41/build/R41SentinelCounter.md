# R41SentinelCounter — security review of the round-41 C1 sandboxes

Seat: sentinel (`R41SentinelCounter`), wave 1. Lane under review:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (clone HEAD `fc79f2a4`), counter
`plans/round41_c1_verify.py` (`ro_sandbox` 317-327, `build_battery` 462-503, `Runner.run` 400-428), freeze
control `.ufo/waves/round-41/claims/control-c1-hostile.txt` + `claims/hostile/h_host_writes.py`.

Every battery, counter and fixture run below was executed inside the orchestrator envelope
(`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent`); the counter nested its own sandboxes inside it. Scratch only under
`/fast/scratch/hyaku/kengaku-r41/R41SentinelCounter{,2}` (removed). No tool installed (pacman paused; nothing
needed). No write outside my report dir and scratch dir; timestamps checked, none found.

Method: I wrote my own probe modules (one per vector) and drove them through the frozen counter in development
mode (`--battery-dir … --only T01`), plus a harness that reproduces `Runner.run`'s argv from the counter's own
`ro_sandbox()`/`Runner.env()` and prints the stub's stdout (so the sandbox outcome is observed, not inferred).
The witness modules and `plans/battery41` were not read or used.

## 1. What holds (tested, per vector)

Tool run (`Runner.run`, argv line 419: `ro_sandbox(writable=(work, tmp), ro_binds=((variant, slot),))`), probe
stub reporting from inside:

```
w_fixture_dir=OSError(Read-only file system)   w_work=allowed   w_tmp=allowed
w_slot=OSError(Read-only file system)          w_variants=OSError(Read-only file system)
w_other_fixture=OSError(Read-only file system) w_canon_lane=OSError(Read-only file system)
w_clone_lane=OSError(Read-only file system)    w_scratch_sibling=OSError(Read-only file system)
w_cache=OSError(Read-only file system)         w_tmp_dir=OSError(Read-only file system)
net_connect=OSError(Network is unreachable)    proc_pids=2  proc1_comm=bwrap
```

Build child (`build_battery`, line 482, `hide=(lane,)`), reporting through `fid`:

```
w_cache=OSError(Read-only file system)  w_scratch_sibling=OSError(Read-only file system)
w_tmp=OSError(Read-only file system)    w_dest=allowed
w_root_bin=OSError(Read-only file system)  w_root_fx_sibling=OSError(Read-only file system)
w_btmp_sibling=OSError(Read-only file system)
w_lane_at_hidden_path=FileNotFoundError  r_lane_at_hidden_path=FileNotFoundError
r_canon_lane=allowed                    net_connect=OSError(Network is unreachable)
proc_pids=2  proc1_comm=bwrap
```

* Filesystem writes outside `work`/`tmp`/`d` are refused everywhere, including `/tmp`, `$HOME/.cache`, the
  counter's own `bin`/`variants`/`slots`, the fixture dir, sibling fixtures and scratch siblings — `EROFS`.
* `--unshare-pid` + a fresh `--proc` hides host processes (2 procs, PID 1 `bwrap`).
* Process lifetime: none survives. A detached grandchild (closed fds) dies when the probe exits
  (`CASE-hold-stdout elapsed=0.01s`); 25 tool runs each spawning a 900 s sleeper leave `no survivor`; a
  `TimeoutExpired` kill leaves `SURVIVOR-AFTER-TIMEOUT: none`; killing the counter with `SIGKILL` mid-run leaves
  `AFTER slot: none / AFTER probe sleep: none / AFTER bwrap: none`. `--die-with-parent` plus the PID namespace
  do their job.
* Work/tmp are removed per run (`ls -la "$S/w"` → empty), variants re-hashed, pins re-hashed.

## 2. Findings

### F1 — HIGH — the mutant under test is readable from inside every tool run (predicate integrity)

Exploit path: a probe stub walks its own cwd (`<root>/work/wNNNNNN/run/tip-receipts-*/tip`) for an ancestor that
contains `slots/` and `variants/`, then reads `variants/<mid>.py` and `slots/receipts.py`. The file set also names
the phase (`ref-*`, `null-*`, `<mid>`). A fixture can therefore answer on *identity*, not behaviour — e.g. emit
the declared difference only when `variants/T01.py` exists — and the kill is still "attributed" by the counter.

Evidence, end-to-end through the frozen counter (module sets its receipt to the observed line):

```
FIXTURE root-from-cwd tool=receipts expect=accept declared=… observed_rc=0 observed=… ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
```
with the stub printing `variants=ref-receipts.py,ref-sources.py|readref=read|readslot=read|wvar=denied`.
Direct sandbox check with a mutant file present: `variants=T01.py,ref-receipts.py`, `read-variant=read`,
`read-slot=read`. `sidechannel=0` is the point: nothing in `SIDECHANNEL` (line 109) is needed, so the only
automated anti-cheat the counter has does not see it.

Impact: the calibration count (`MUTANTS total=23 killed=23`) can be satisfied without demonstrating any advertised
behaviour. Counter lines that fail: 419 (only `work`/`tmp` bound writable, but the rest of `root` stays *readable*)
and 595 (`mv.write_text` leaves the variant on a reachable path). The claims' named limit ("a kill records a result
difference in the declared direction, not the fixture's intent") covers *intent* but not this *mechanical* channel.

Smallest remediation: pass the variant to the sandbox by content instead of by path — `--ro-bind-data <fd> <slot>`
(bwrap 0.13.1 has it; verified via `bwrap --help`) — so the mutant never exists at a readable path; keep
`root/"variants"` off disk for the tool runs, or add it to `hide` (419/482). Cheaper stopgap:
`hide=(lane, root/"variants")` plus a copy of the variant staged at `root/slots/<mid>.py` masked after the bind.

### F2 — HIGH — `--unshare-net` does not stop AF_UNIX; host sockets stay reachable and unmasked

Exploit path: `--unshare-net` (line 318) isolates only the network namespace. Any unix socket visible under
`--ro-bind / /` is still connectable, and the counter masks nothing except the lane. Observed, with the counter's
exact flag set (`--ro-bind / / --unshare-pid --unshare-net --die-with-parent`):

```
UNIX-CONNECT-OK
LISTENER-GOT b'hello-from-sandb'
```

and the sockets are present in a counter-shaped sandbox even under the wave envelope:

```
envelope sees:                     srw-rw-rw- 1 nobody nobody 0 /run/dbus/system_bus_socket
counter-shaped inner sandbox sees: srw-rw-rw- 1 nobody nobody 0 /run/dbus/system_bus_socket
```

`/run/user/1000/bus` and the user's agent sockets (`/run/user/1000/gnupg`, ssh-agent, editor sockets) are masked
only by the *envelope*, not by the counter: `ro_sandbox` adds no `--tmpfs` for `/run`, and a run of the frozen
predicate without the envelope exposes them (host stat: `srw-rw-rw- /run/user/1000/bus`).

Impact: a build module or probe stub can speak to host services as the user without any filesystem write — the
session bus can start a user unit (`org.freedesktop.systemd1`) which then runs *outside* the sandbox, and
agent/keyring sockets are reachable. That is an escape path around every EROFS result above, and it contradicts
the docstring's implicit "no network, no write" framing (lines 60-63).

Smallest remediation: add `--unshare-ipc` and mask the socket trees — `--tmpfs /run/user/<uid>` and
`--tmpfs /run/dbus` (or a minimal `--tmpfs /run` with the few paths a tool needs), in `ro_sandbox` (317-327).

### F3 — MEDIUM — SysV IPC is not unshared: host objects outlive every sandbox and the counter

`ro_sandbox` passes `--unshare-pid --unshare-net` only (line 318). A segment created inside the counter-shaped
sandbox survives on the host:

```
inside:  Shared memory id: 1
after:   0x08b65213  1  vgpnk  644  4096  0
```

(cleaned with `ipcrm -m 1`; `ipcs -m` empty afterwards). Semaphores (`ipcmk -S`) behave the same.

Impact: (a) host residue that no `finally: shutil.rmtree` reaches, so "keep state on the host after the counter
exits" is possible — unbounded `shmget` can exhaust `kernel.shmall` for the user's other processes; (b) a keyed
segment is a cross-run channel between the 8 concurrent runs of one counter (`--jobs 8`), which the per-run
work/tmp isolation is meant to prevent.

Smallest remediation: `--unshare-ipc` in `ro_sandbox` (one flag; peer lanes such as `R41ExecNoHarm`'s round-37
runner already pass it).

### F4 — MEDIUM — `path_ok` checks absolute tokens only, so relative argv escapes the fixture dir

`path_ok` (349-356) returns `True` for anything that is not `/`-rooted and not a `{WORK}` token; the contract at
497 therefore accepts `../` chains. Observed with a two-fixture module whose first fixture is graded against its
sibling's lane:

```
FIXTURE relative-escape tool=receipts expect=accept declared=skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command observed_rc=0 observed=skip:… ok
FIXTURE lane-holder     … ok
```

The absolute control is refused as designed: `SETUP fixture 'absolute-escape' of bat3/m_abs_escape.py breaks the
contract`, `counter_rc=2`.

Impact: a fixture is not hermetic — it can grade a sibling fixture's lane (so its `defects` come from another
fixture's state) and, with a long enough `../`, reach any host path, e.g. the real lane, whose committed probe
scripts `tip_receipts` will then clone and execute. The counter's stated contract ("Every absolute argv path must
lie inside d") is technically true but has no force against the relative spelling, and a relative chain contains
no `SIDECHANNEL` token.

Smallest remediation: resolve every token, not just absolute ones: `p = (d / tok).resolve(); if not
p.is_relative_to(d.resolve()): return False`, keeping the `{WORK}` branch first.

### F5 — LOW — lane hiding is per-path, and the frozen measurement protocol defeats it

`hide=(lane,)` (482) masks exactly the resolved `--lane`. With `--lane` = the canonical lane the hostile control
prints the committed values; with `--lane` = a clean clone — the frozen predicate's own protocol, "measured on a
clean clone of the landing tip" — the same control prints `lane_read=allowed`:

```
FIXTURE h-host-writes.build_write=OSError.lane_read=FileNotFoundError … ok      (--lane canonical)
FIXTURE h-host-writes.build_write=OSError.lane_read=allowed        … ok        (--lane <clone>)
```

The claims' named limit covers the read ("a module can still read other copies of the tools elsewhere on the
read-only host (no network, no write)"), but `control-c1-hostile.txt` reads as though the lane were hidden.
Same class: a tool run never hides anything (419 has no `hide`), so `r_canon_lane_counter=allowed` and
`r_clone_lane_counter=allowed`.

Remediation: none required beyond wording; if a hard boundary is wanted, hide every copy of the lane the counter
can find, not just `--lane`.

### F6 — LOW — `fingerprint()` reads every fixture file whole, twice

`fingerprint` (329-346) does `content = hashlib.sha256(fh.read()).hexdigest()` (344) for every regular file, before
the runs and again after them, in the unsandboxed counter process. In the counter process itself, measured:

```
fingerprint_256MiB seconds=0.17 peak_rss_kb=282420 digest=bb82e7b1852f
second_pass seconds=0.17
```

Impact: fixture size maps 1:1 to counter RSS (a 10 GiB fixture file ≈ 10 GiB peak) — a module can OOM the counter
that is grading it, with nothing but `ctx.write`. Availability of the calibration run, not host integrity.

Smallest remediation: `hashlib.file_digest(open(p, "rb"), "sha256")` (streams) and skip/cap files above a size
limit.

### F7 — INFO — the hostile control proves three of its four claims, but only one is an assertion

Reproduced in full against the canonical lane (numbers match `claims/control-c1-hostile.txt`):

```
SIDECHANNEL hostile/h_host_writes.py tokens=/home/
FIXTURE h-host-writes.build_write=OSError.lane_read=FileNotFoundError tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/r/foo-probe.txt observed_rc=0 observed=control:differ,equal:corpus/evidence/r/foo-probe.txt ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=1
MUTANTS total=23 killed=1 survived=22 invalid=0 null_detected=0
ADVERTISED direct=21 indirect=2 none=0
ls: cannot access '/home/vgpnk/k41-hostile-*': No such file or directory
```

* `build_write=OSError` ✓ — but the marker is under the *invoking user's* home, while the build child's `HOME`
  is `/nonexistent` (line 485); the denial is the read-only `/` bind, not `$HOME`. Wording only.
* `lane_read=FileNotFoundError` ✓ in canonical mode, false in clone mode (F5).
* probe-stub write denied ✓ **and asserted**: `h_host_writes.py:42` declares `equal:` on a receipt whose content
  is `write=denied`, so a successful write prints `write=allowed` → `differ` → `WRONG`. This is the solid one.
* `build_write` and `lane_read` are *reported* only: the module stuffs them into `fid` (`h_host_writes.py:38`),
  and `fid` is printed at 567/617 and never compared to anything. If either bound failed, the FIXTURE line would
  still print `ok`; only the external `ls` and a human reading the string catch it.

Remediation: raise inside `build()` on the bad outcome (e.g. `if w == "allowed": raise SystemExit(3)`) so a
regression is visible as a build failure, with `fid` left as the record.

## 3. Answers to the assigned questions

| Question | Answer |
|---|---|
| build child writes outside work/tmp/fixture | no — EROFS on every target tried, incl. `/tmp`, `$HOME/.cache`, scratch siblings, `root/bin`, sibling `fx`/`btmp` |
| tool run writes outside work/tmp/fixture | no — EROFS on fixture dir, slot, variants, sibling fixture, both lanes, scratch, `/tmp`, `$HOME/.cache` |
| reach the network | IP: no (`Network is unreachable`); **AF_UNIX: yes (F2)** |
| keep a process alive after the counter exits | no — normal exit, `TimeoutExpired`, and counter `SIGKILL` all leave nothing; **but SysV IPC objects do outlive it (F3)** |
| read the hidden lane | at the hidden path: no (build), `FileNotFoundError`; other copies: yes (build and tool run); a tool run hides nothing (F5) |
| affect another module's fixtures | no writes (EROFS); **reads yes**, and the module's own scratch root is reachable from a probe's cwd (**F1**) |

## 4. Environment note

`/fast/scratch/hyaku/kengaku-r41/R41SentinelCounter` (my first scratch dir, holding the probe modules and clones)
disappeared between 15:41 and 15:42 while other seat dirs under the same parent survived; `ls -ld` on the host
reports it absent. Nothing in my harness removed it (all my deletions were `rm -rf` of named subdirectories). All
evidence above was captured before and after the loss; it was rebuilt as `…/R41SentinelCounter2` and re-verified.
Not a counter finding; flagged because peer scratch dirs share that parent.

## 5. Reproduction

```bash
S=/fast/scratch/hyaku/kengaku-r41/<seat>; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
E=(bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
   --proc /proc --unshare-pid --die-with-parent)
# F1 (variant readable, token-clean): module with a stub that walks cwd ancestors for slots/+variants/
"${E[@]}" /usr/bin/python3 "$S/lane/plans/round41_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat7" \
   --only T01 --work "$S/w" --jobs 2          # → FIXTURE root-from-cwd … ok ; sidechannel=0
# F2 (AF_UNIX): listener on a scratch socket, then inside the counter's own flag set:
bwrap --ro-bind / / --unshare-pid --unshare-net --die-with-parent /usr/bin/python3 -c 'connect+send'
# F3 (SysV IPC): bwrap <counter flags> /bin/sh -c 'ipcmk -M 4096'; then host: ipcs -m
# F4 (relative argv): module returning ["--lane", "../f001/lane", "--list"] → FIXTURE … ok
# F5 (lane hiding): the committed hostile module with --lane canonical vs --lane "$S/lane"
# F6 (fingerprint cost): import the counter, write a 256 MiB file, call fingerprint()
```

VERDICT: c1-sandbox-findings-7-high-2
