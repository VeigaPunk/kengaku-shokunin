# R38SentinelProbe — trust boundaries of the round-38 build (probe + C1 counter)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `fc1174f5` clone. Scratch: `/fast/scratch/hyaku/kengaku-r38/R38SentinelProbe`
(clone + fixtures only; deleted at the end). No lane write, no lane git index touched, no mutating jj, no pacman
(nothing installed; `uv 0.9.x` and `bwrap` were already present).

Axes exercised: **A** sandbox containment of `plans/build_pmars_probe.py`; **B** privilege/env/network envelope of
battery38 fixture code under `plans/round38_c1_verify.py`; **C** path containment in both; **D** process lifecycle;
**E** reproducibility of each claim (command + output cited).

Frozen surfaces were read, never written: `plans/build_pmars_probe.py`, `plans/round38_c1_verify.py`,
`plans/pkg_gate.py`, `plans/pkg-spec-r38.json`, the captures and the dry table.

---

## 1. What holds (tested, not assumed)

All four positive controls below were run against a clone; receipts in `./R38SentinelProbe/`.

1. **The per-case bwrap sandbox contains the graded code.** I imported the frozen probe and called
   `run_case(cap, root, case, script=<hostile harness>)` — the harness ran as pid-side of `bwrap` and reported
   (`./R38SentinelProbe/rec_isolation.py`, output `./R38SentinelProbe/proof-isolation.txt`):

   ```
   etc_shadow = ERR PermissionError: [Errno 13] Permission denied: '/etc/shadow'
   home_list = ERR FileNotFoundError: [Errno 2] No such file or directory: '/home'
   lane_git_config = ERR FileNotFoundError: ... '/home/vgpnk/Projects/s...
   write_app = ERR OSError: [Errno 30] Read-only file system: '/app/pwn'
   write_usr_local_bin = ERR OSError: [Errno 30] Read-only file system: '/usr/local/bin/pwn'
   write_etc = ERR OSError: [Errno 30] Read-only file system: '/etc/pwn'
   write_tmp = 1
   net_connect = ERR OSError: [Errno 101] Network is unreachable
   dns = ERR gaierror: [Errno -3] Temporary failure in name resolution
   host_pid1 = 'bwrap'     proc_entries = 63     root_list = ['app','bin','dev','etc','harness.py','lib','lib64','proc','sbin','tests','tmp','usr']
   ```

   So: no `~/.ssh`, no lane `.git`, no host writable path, no network, no host pid visibility, `/etc/shadow`
   denied. The child env is scrubbed — `ENV ['HOME','LANG','LC_ALL','PATH','PWD','PYTHONDONTWRITEBYTECODE','PYTHONUTF8']`,
   `SSH_AUTH_SOCK` absent, agent socket `FileNotFoundError` (`build_pmars_probe.py:266-268` passes an explicit `env=`).

2. **The probe leaves no processes behind.** A harness that spawned `setsid sleep 400` left none after the case
   returned (`SURVIVORS []`); killing `bwrap` from the outside (the `timeout=180` path) also left none
   (`SURVIVORS_AFTER_TIMEOUT []`, `BWRAP_SURVIVORS []`) — the pid namespace dies with `bwrap`.

3. **The probe's scratch is its own.** `--smoke` on a fresh `--work` left `residue: <empty>`; only the
   documented `SMOKE out=Results: 12 34 78` line, rc 0.

4. **The counter's `--spec` containment rule holds.** A fixture returning `--spec /etc/hostname`, and a fixture
   whose spec is a symlink inside `d` to `/etc/hostname`, both produce
   `SETUP fixture SENX-abs-spec returned a forbidden argv` / `... SENX-link-spec ...`, exit 2
   (`round38_c1_verify.py:241-245`). The rule that a fixture may only own a spec *inside its own dir* is enforced.

---

## 2. Findings

### F1 — HIGH — a battery38 fixture reaches arbitrary host code with the reviewer's secrets and network; the side-channel scan does not see it

**Exploit path (performed end to end through the real counter).**
A single module in the battery dir returns a `package` argv that carries `--rerun` and its *own* spec:

```python
spec = dict(ctx.spec); spec["probe_cmd"] = ["pwn.py", "--arg1"]      # any argv
(d/"pwn.py").write_text(...)                                          # written at build time, not scanned
return ["package", "--root", str(d), "--rerun", "--spec", str(d/"spec.json")]
```

`--spec` sits inside `d`, so `round38_c1_verify.py:241-245` accepts it. Gate P10 then executes that argv
verbatim: `probe = list(p.spec["probe_cmd"])` (`pkg_gate.py:271`), `cmd = [sys.executable] + probe`
(`:274`), `r = subprocess.run(cmd, cwd=str(p.root), ...)` (`:278`) — no `env=`, no sandbox, cwd = the fixture dir.
The counter scans only `<battery>/ *.py` text for five tokens (`round38_c1_verify.py:162-171`) — the spec is JSON
and `pwn.py` is written inside `d`, so nothing is flagged.

**Evidence.** `python3 plans/round38_c1_verify.py --lane lane --battery-dir bat38 --only N15 --work w`
(receipt `./R38SentinelProbe/c1-only-N15.out`, module `./R38SentinelProbe/sens_p10.py`, canary
`./R38SentinelProbe/canary-fixture-spec-probe.json`):

```
FIXTURE SEN10-p10-probe-spec-exec expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N15 P10 mirror killed by=SEN10-p10-probe-spec-exec -- a byte-equal fresh run passes P10
PREDICATE C1 n/a (non-default battery or mutant subset)        (exit 0)
```

The canary the gate-executed `probe_cmd` wrote **into the lane clone** (`plans/CANARY-SEN10.json`) reports:

```
"uid": 1000
"cwd": ".../w/k38-c1-1vq3u3rj/fx/f064"
"env_keys": [... "OPENAI_CODEX_TOKEN", "OP_SERVICE_ACCOUNT_TOKEN", "OPKEY_VAULT", "OP_ACCOUNT",
              "XAI_OAUTH_TOKEN", "SSH_AUTH_SOCK", "GPG_TTY", "NOTIFY_SOCKET", "XDG_RUNTIME_DIR" ...]
"home_ssh_present": true
"net": "reachable"
```

(Values were never read or printed; only the inherited key names.)

**Impact.** `plans/battery38/*.py` is this round's work product and is **not** in `PINS`. Any module — a peer's
bug, a copy-paste of someone else's fixture, or a hostile one — gets, at the moment the reviewer runs the
predicate, the reviewer's full environment (agent/1Password/GPG handles), outbound network, `~/.ssh`, and write
access to the lane. The counter still prints `sidechannel=0`, `wrong=0` and an attributed kill. The claims'
limit sentence (“the side-channel scan is a token heuristic … code review by a non-author seat remains part of
admission”) is confirmed as necessary but insufficient: the *spec* is an unexamined execution channel.

**Smallest remediation.** The counter and gate are frozen, so containment must be external this round: run
`round38_c1_verify.py` under `bwrap --unshare-net --clearenv --ro-bind <lane> /lane --tmpfs /tmp` (or at minimum
`env -i PATH=… TMPDIR=$S`) so a fixture inherits no secret and cannot reach the network or the lane; and in
non-author review, diff every fixture's returned argv for `--rerun` plus the `probe_cmd` of any spec it writes,
requiring `probe_cmd[0]` to be the frozen probe path. If a later round unfreezes the counter: scan `*.json` and
require `probe_cmd` to stay inside the fixture dir.

### F2 — HIGH — the same vector mutates the lane/its index (gate has no write protection)

P10 runs the fixture's `probe_cmd` with `cwd=p.root` and the inherited environment (`pkg_gate.py:278`); nothing
stops it from being `["-c", "import subprocess; subprocess.run(['git','-C','<lane>','checkout','--','.'])"].`
My benign canary already wrote a file into the lane clone from that child (F1). **Impact:** “nothing frozen may
change” rests on reviewer discipline, not on the mechanism, at counter time. **Remediation:** the same external
`--ro-bind <lane>` wrapper as F1 (lane repo must be mounted read-only while a counter runs).

### F3 — MEDIUM — the gate reads outside `--root` through unguarded spec paths

Only `Package.capture()` guards a spec-derived path (`pkg_gate.py:105`: `".." not in rel.parts`). `entry`,
`readme` (`:70-71`), `sources`, `receipt` (`:118`) and `capture_dir` (`:153`, then a full directory walk at
`:178`) have no such guard, and `pathlib` lets an absolute value win. Demonstrated with the frozen gate:

```
spec["receipt"] = "/home/vgpnk/.ssh/known_hosts"; spec["receipt_sha256"] = sha256(that file)
$ python3 plans/pkg_gate.py package --root travroot --spec travspec.json
P2 ok receipt_sha256=pinned                       (rc 1, P1 DEFECT for the empty root)
```

**Impact:** read-only. A fixture-owned spec turns the gate into a path-existence/content oracle over host files
(fixtures can read directly anyway, so this is a boundary defect, not an escalation). **Remediation:** reuse the
line-105 guard for every spec path, and reject absolute values, in the next unfrozen gate revision.

### F4 — MEDIUM (latent) — `stage_app()` has no path containment: a case can write outside the scratch

`p = root / rel` then `p.mkdir(parents=True)` / `p.write_bytes(b"")`
(`build_pmars_probe.py:228-236`). With a case row whose relpath is `"../../../../../../fast/scratch/.../ESC2.txt"`
I created `/fast/fast/scratch/hyaku/kengaku-r38/R38SentinelProbe/ESC2.txt` **as the invoking user, outside any
scratch** (`EXISTS True`; removed afterwards, `CLEANED`; receipt `./R38SentinelProbe/proof-traversal.txt`
re-runs it in-tree: `WROTE_OUTSIDE_ROOT True`). Today unreachable: `CASES` is a frozen constant and the
probe digest is pinned by the C2 counter (`PROBE_SHA256`, V5), so abuse requires editing a pinned file — detected,
not prevented. **Remediation:** `p = (root / rel).resolve(); if not p.is_relative_to(root.resolve()): raise`, and
the same check for `build_art`'s `dest`.

### F5 — LOW — crash paths bypass the documented exit convention

`subprocess.run(..., timeout=180)` in `run_case` (`:267`) and `tempfile.mkdtemp(dir=a.work)` in `main`
(`:308`) are unguarded: a hung case raises `TimeoutExpired`, a missing `--work` raises `FileNotFoundError`; both
exit **1** with a traceback instead of `2 = usage/setup`, and the “did not yield four test verdicts” diagnostic is
skipped. Observed: `python3 plans/build_pmars_probe.py --lane lane --work nope/deeper` → `EXIT=1` +
`FileNotFoundError: ... nope/deeper/k38-bpm-mw2k7v5g`. The C1 counter behaves identically for a missing `--work`
(`run_gate`'s `timeout=900` is caught, `round38_c1_verify.py:181`, but `mkdtemp` at `:236` is not).
**Remediation:** `mkdir(parents=True, exist_ok=True)` on `--work`, and catch `TimeoutExpired` → return `2` with a
`SETUP case <id> timed out` line.

### F6 — LOW — the probe binds all of `/etc`

`--ro-bind /etc /etc` (`build_pmars_probe.py:245`) exposes every world-readable host config to the graded code
(`/etc/machine-id`, `passwd`/`group`, `ssh_config`, resolver). No secret is reachable on this host — `/etc/shadow`
is `0600 root:root` (denied in the sandbox) and `/etc/ssh` holds only `moduli`, `ssh_config*`, `sshd_config*` —
but it is broader than the grader needs. **Remediation (optional):** bind only `passwd, group, nsswitch.conf,
resolv.conf, hosts, ld.so.cache, alternatives, ssl` once the probe is unfrozen.

### F7 — LOW — P10's `uv run` fallback is a network package-resolution on every counter run

`Bio` is not importable on this host (`python3 -c "import Bio"` → `ModuleNotFoundError`), so the gate takes
`cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe` (`pkg_gate.py:276`) for
every P10 that runs — including C2's V2 (`--rerun`, `--root lane`) and any `--rerun` fixture. That is a host
process with the inherited env and network (verified reachable, F1). biopython 1.85 is in `~/.cache/uv`, so the
common path is cache-served, but uv still performs index resolution unless told not to.
**Remediation:** install biopython into the running interpreter (or export `UV_OFFLINE=1` for counter runs) and
record it in the round's tool log.

### F8 — LOW — the counter's gate timeout leaves grandchildren alive

`run_gate` uses `subprocess.run(..., timeout=900)` (`round38_c1_verify.py:181`); Python kills only the direct
child. Reproduced with the same call shape on the real gate and a P10 `probe_cmd` that spawns and sleeps:

```
GATE_KILLED_AT 4.0 s
SURVIVORS ['173800 uv run --no-project --with biopython==1.85 python3 -c import subprocess,time;subpro...',
           "173810 python3 -c import subprocess,time;subprocess.Popen(['setsid','sleep','300','SENLEFT"])"]
```

(cleaned: `pgrep -af SENLEFT` → `NO_LEFTOVERS`.) Contrast §1.2: the *probe's* subtree is killed correctly because
`bwrap` owns a pid namespace; the gate side has none. **Impact:** a fixture can park long-lived processes (up to
the gate's 600 s probe timeout) across 22 mutant attempts. **Remediation:** `start_new_session=True` plus
`os.killpg` on timeout in the counter (next revision), or `--die-with-parent`-style wrapping of gate runs.

---

## 3. Limits of this review

- Everything was measured under the reviewing user's own `PATH`/`TMPDIR`; I did not test a malicious
  *non-author* module beyond the demonstration fixture, and did not send anything off-host (the network test was a
  single TCP connect to `1.1.1.1:80` from inside the gate child and a DNS failure inside the probe sandbox).
- F1/F2 are consequences of design stated in the frozen counter (“a battery38 fixture MAY own its spec”); I judge
  the mechanism, not intent.
- `/etc` and `ldd` are the host's (as the probe's docstring already states); shell differences were not re-measured.
- No installs, no pacman, no host service touched. Scratch `$S` removed; the only host artefact ever created
  outside it (`/fast/fast/...`, F4) was removed and verified (`ls: cannot access '/fast/fast'`).

VERDICT: sentinel-8-findings
