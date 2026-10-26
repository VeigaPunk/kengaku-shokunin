# R39SentinelProbe — trusted-boundary review: `plans/git_leak_probe.py` and `plans/round39_c1_verify.py`

Round 39 wave 1, seat `R39SentinelProbe` (sentinel). Read-only on the lane; every experiment ran under
`S=/fast/scratch/hyaku/kengaku-r39/R39SentinelProbe` (removed at exit). Lane tip read: `7504738`
(`.git/HEAD`); `git -C <lane> status --porcelain` at the end of the seat showed only other seats' untracked
`round-39/` outputs — no tracked file modified by me.

Frozen inputs were never edited: I imported `plans/git_leak_probe.py` in-process only to reuse its own
`sandbox_argv` (`plans/git_leak_probe.py:191-203`), and every counter run was
`python3 plans/round39_c1_verify.py --lane . --battery-dir <my scratch module dir> --only M01 --work <scratch>`
(the documented development form, which prints `PREDICATE C1 n/a`).

Receipts (`R39SentinelProbe/`, beside this file): `probe-sandbox-evidence.txt`, `c1-child-evidence.txt`, `timeout-path.txt`, and the
three probe modules `probe_child.py`, `spec_exec.py`, `spec_tamper.py`.

**Threat model, stated up front.** The untrusted inputs are (a) the *captured* TB2 scripts (`challenge-setup.sh`,
`solve.sh`, `tests/test_outputs.py`) executed by the probe, and (b) `plans/battery39/*.py` executed by the C1
counter. (b) is authored in-lane by executor seats; the freeze already says "battery39 code review by a
non-author seat remains part of admission" (`plans/round-39-claims.md` §C1 Limits). The findings below do not
describe an outside attacker; they bound *what the frozen predicates prove*, which is what the calibration claim
rests on.

---

## 1. The four questions

| Question | C2 probe (frozen cases/recipes inside bwrap) | C1 counter (battery module in a child process) |
|---|---|---|
| write outside its scratch | **no** for the host; **yes** for the sandbox's own tmpfs root, `/tmp` and `/app` (bound to scratch), all without quota | **yes, unrestrained** — absolute host paths, and outside the fixture dir inside the counter's root (A1/B) |
| reach the network | **no** (`OSError:101` to `1.1.1.1:53`; no route to host loopback services) | **yes** (`1.1.1.1:53` REACHED) |
| read `~/.ssh` | **no** (`/home` does not exist in the sandbox root) | **yes** — `~/.ssh/id_ed25519` present and readable, 411 bytes (content not read) |
| read/write the lane's `.git` | **no** (lane path absent) | **yes** — `.git/HEAD` readable; `LOG.md` and `plans/round39_c1_verify.py` writable |
| leave processes behind | **no** — a `setsid`'d grandchild died with the pid namespace (A19) | **yes** — five `sleep 5311` survivors still running after the last run (E) |

Evidence id A* = `probe-sandbox-evidence.txt`, B/C/D = `c1-child-evidence.txt`.

---

## 2. Findings

### F1 (High, integrity of C1's isolation claim) — a battery module's child process is unsandboxed

`plans/round39_c1_verify.py:199-201` spawns the module child with no `env=`, no namespace, no `start_new_session`:

```
r = subprocess.run([sys.executable, …/round39_c1_verify.py, "--build-module", str(f), …],
                   cwd=str(dest), capture_output=True, text=True, timeout=900)
```

`build_module_child` (`:170-183`) then imports the module and calls its `build`, i.e. the module's top-level code
runs first. B (`c1-child-evidence.txt`) is a battery39-shaped module that contains **none** of the scanned tokens
(`/proc`, `ppid`, `cmdline`, `psutil`, `environ`: `round39_c1_verify.py:100`) and yet reports:

```
"home": "/home/vgpnk", "ssh_key_exists": true, "ssh_key_readable": true, "ssh_key_bytes": 411,
"lane_git_head_readable": true, "lane_file_writable": true, "counter_writable": true, "uid": 1000,
"wrote_absolute": "/fast/scratch/…/child-escape.txt", "net": "REACHED", "leftover_pid": 2616520
```

and the receipt prints `BATTERY fixtures=… sidechannel=0` (run D) while the same module's sibling did all of the
above. Sibling `spec_exec.py` also shows `sidechannel=0`.

Exploit path: a module that is *not* code-reviewed (or is reviewed only by the token heuristic) reads
`~/.ssh/id_ed25519`, the lane `.git`, and any host file, writes to the lane, and exfiltrates over the open
network — during the run that is supposed to measure the lane's calibration. It also leaves processes behind that
outlive the child, the counter, and (in this seat) every subsequent run (receipt E: `count=5` after the last
counter run; Table row "leave processes behind").

Impact: the predicate's `sidechannel=0` is *not* evidence of "no side channel"; it is evidence of five absent
substrings. The docstring's honest wording (`:42-43`) says "a heuristic", but the receipt line is what a reader
compares against the frozen predicate, and it reads as a clean bill.

Smallest remediation (next round; the counter is frozen now):
1. Give the child an explicit minimal env (as the C2 probe already does at `plans/git_leak_probe.py:212-213`).
2. `start_new_session=True` and kill the process group on exit/timeout.
3. Better: run the child under the existing bwrap recipe (`git_leak_probe.py:191-203`) with the lane read-only and
   `--unshare-net`, and drop the token scan to what it is (a lint).
Interim, this round: the non-author review of `plans/battery39/*` must read for `os.getenv`, `Path.home`,
`socket`, `subprocess`, `shutil`, `open(`, `--rerun`, `probe_cmd` — not run the token scan.

### F2 (High, soundness) — pinned inputs are checked once; a module can mutate one and the receipt still says `mismatched=0`

`mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]` (`:261`) is computed once, printed at
`:262`, and reused in `good = (not mism and …)` at `:386`. Nothing re-hashes the pins before the receipt is
printed, and `ctx.spec_path` — passed to **every** gate run (`:313`, `:334`, `:341`, `:364`) — is never hashed
after startup.

C (`c1-child-evidence.txt`): a module appends one newline to `plans/pkg-spec-r35.json` inside its `build`. The run
still prints:

```
PINS total=26 mismatched=0
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
spec-before=e085b43505c9848c8d19eb52c52fec1a3282dac3c5b436f59320e95e5c299fc4
spec-after =63a30c8f51f9debf22fd00c44c2673c686f24d69ffcf4e88b6521f06d178d2e8
```

Exploit path to a fabricated kill: module fixtures are built *before* the reference pass (`:313`) and never
rebuilt; the mutant pass reuses the same `built` dirs (`:361-364`). A leftover process from F1 (proven to survive)
can rewrite a fixture directory, or the frozen spec, *between* the reference pass and the mutant pass. The mutant
then produces a different clause set or exit code from a reference result computed against different bytes — a
direction difference with no behavioural difference. The only post-hoc defence is the gate-copy digest check
(`:369`), which covers neither fixture content nor `ctx.spec_path` nor the other 25 pinned inputs. The counter
file itself is not in `PINS`, and B reports `counter_writable: true`.

Impact: `killed=7 survived=0` is not compositional — it is sound only against modules that do not write and leave
no process. `M01`–`M07` survivors are meant to be *earned*; this path earns them.

Smallest remediation: re-hash `PINS` (and `ctx.spec_path`) immediately before printing `MUTANTS …` and before
`good`; hash each fixture directory before the reference pass and again before the mutant pass and count drift as
`invalid`. Also add `plans/round39_c1_verify.py` to a self-check (a run where `sha256(__file__)` changes is
`invalid`).

### F3 (High, capability, demonstrated) — the JSON hand-back is not a boundary: a fixture-supplied `--spec` makes the pinned gate execute code

`round39_c1_verify.py:293-297` validates only `argv[0] ∈ {package,d4-line,d5-line}` and that a `--spec` value
resolves inside the fixture dir. `--rerun` is not excluded, and `pkg_gate.py:308` runs P10 whenever it is present:

```
                          if (n != "P10" or args.rerun)]
```

P10 executes the command named by the spec (`pkg_gate.py:271-278`):

```
    probe = list(p.spec["probe_cmd"])
        cmd = [sys.executable] + probe
        cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe
        r = subprocess.run(cmd, cwd=str(p.root), capture_output=True, text=True, timeout=600)
```

A fixture may derive its own spec from a deep copy of `ctx.spec` (`plans/round-39-claims.md`, module contract), so
`probe_cmd = ["-c", <python>]` is legal. D (`c1-child-evidence.txt`), through the counter itself:

```
FIXTURE spec-exec expect=accept declared=- observed_rc=1 observed_defects=P1,P2,P3,P4,P5,P6,P7,P8,P9 WRONG
BATTERY fixtures=88 wrong=2 renamed_disagree=0 sidechannel=0
p10-exec.txt=P10 ran as uid=1000 cwd=…/w/k39-c1-bhbwip8e/fx/battery39-spec_exec/f000
```

`P10` is absent from the defect set: the gate *accepted* the rerun byte-compare after running arbitrary Python with
the counter's uid, inherited environment, cwd in the counter's temp root, and network. Two consequences:

1. A module can do everything F1 lists *without touching the filesystem in its own source* — the payload is a JSON
   string, so every token scan and most human greps pass.
2. P10 becomes self-certifying for any fixture that supplies `probe_cmd` + `receipt`; a fixture's `P10 ok` no
   longer means "the lane's probe reproduces".

Smallest remediation: reject `--rerun` in a battery-supplied argv (and, more generally, whitelist allowed argv
flags), or require the fixture spec to be byte-identical to the frozen one for a `package` argv. If P10 must stay
reachable, run the probe under the bwrap recipe too.

Side observation (same line, `pkg_gate.py:276`): with `biopython` absent from the host interpreter the gate fetches
`biopython==1.85` through `uv` with a version pin and no hash; the wheel is cached at
`/home/vgpnk/.cache/uv/sdists-v10/pypi/biopython/1.85/…/biopython-1.85-cp314-cp314-linux_x86_64.whl` (mtime
2026-10-25 16:25, i.e. not fetched by this seat). The gate is digest-pinned; its rerun dependency is not.

### F4 (Medium) — inherited environment, and grandchildren are never reaped

Neither `module_fixtures` (`:199-201`) nor `run_gate` (`:210-219`) passes `env=`, so every module child and every
gate invocation — including F3's payload — receives the operator's whole environment. Any token in it is one
`os.getenv` away (the token scan at `:100` looks for `environ`, not for `getenv`). `subprocess.run(timeout=900)`
kills only the direct child on timeout; the grandchildren from F1 survived every run
(`c1-child-evidence.txt`: four `sleep 5311` before the last run, five after).

Smallest remediation: `env={"PATH": …, "HOME": <scratch>, "LANG": "C.UTF-8"}`, `start_new_session=True`, and
`os.killpg` on timeout. The C2 probe already models the env half (`git_leak_probe.py:212-213`).

### F5 (Low, hardening; none of these defeated the probe's confinement) — C2 sandbox gaps

From A1–A19 (`probe-sandbox-evidence.txt`), all with the frozen `sandbox_argv` (`git_leak_probe.py:191-203`):

- uid 1000, `CapEff=0`, `NoNewPrivs=1`, `Seccomp:0` — no seccomp filter, but no capabilities either; `/etc` and
  `/usr` are read-only, `/proc/sys/kernel/hostname` is not writable.
- **No `--unshare-uts`**: `hostname` inside is `plazir27`, the host's name (A17 vs host `hostname`).
  **No `--unshare-cgroup`.**
- **`--ro-bind /etc /etc`** (`:197`) exposes host `/etc`: `sshd_config`, `ssh_config`, and a readable
  `/etc/machine-id` (A5). `/etc/shadow` is denied (A4). This is host-config and fingerprint exposure, not an escape.
- **No quota on either writable mount**: the bwrap root is a 16 GiB writable tmpfs and `/app` is the host NVMe
  (`/dev/nvme1n1p2`, 804 G, 542 G free, `noquota`) (A9, A14, A15, receipt E); an 8 MiB write to each succeeded at
  5.1 GB/s and 1.4 GB/s. The per-case timeout is 300 s (`:216`), which bounds but does not prevent filling `/fast`
  or exhausting RAM. The cases are
  frozen literals; the *executed* bytes are the pinned captures, so this needs a bad capture, not a bad case.

Cheap additions: `--unshare-uts`, `--unshare-cgroup`, `--tmpfs /tmp --size=…`, `--size` on the root, `--ro-bind
/etc/{passwd,group}`-style narrowing instead of all of `/etc`, and `--seccomp` only if a profile is maintained.

### F6 (Low, operability) — the probe crashes instead of failing on a slow case or a missing `--work` parent

`subprocess.run(…, timeout=300)` at `:216` sits in `run_case` with no `except TimeoutExpired`, and `main` has none
either. A copy of the frozen probe with **only** that constant changed (`timeout=0.001`) exits 1 with
`subprocess.TimeoutExpired` out of `main` — no `SETUP` line, no receipt, no per-case verdict
(`timeout-path.txt`; the `finally` cleanup does hold: the case root is removed). Separately, `--work` must already
exist: `tempfile.mkdtemp(…, dir=a.work)` at `:258` raised `FileNotFoundError` in my first attempt and produced the
same traceback shape. At 300 s, one `git gc` on a loaded host turns a 25-case measurement into a truncated run.

Smallest remediation: catch `TimeoutExpired` per case and report `CASE <id> timeout` as a non-verdict (or exit 2
with a `SETUP` line), and `mkdir(parents=True, exist_ok=True)` the `--work` dir.

---

## 3. What held (checked, not assumed)

- Captures are digest-checked **before** any case runs (`git_leak_probe.py:250-253`), and the harness is fed the
  frozen case strings, so no case text is interpolated from outside the frozen table.
- The case process gets exactly nine environment variables (A16), `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`; nothing from the operator's environment leaks in — the C1 counter does the
  opposite (F4).
- `/home`, `/root`, the lane, `/sys`, and the fleet root are absent from the sandbox root (A6, A8); `/` is bwrap's
  own tmpfs, so "writable `/`" is sandbox-internal.
- Network is a private namespace: `OSError:101` for an external connect, `ConnectionRefusedError:111` to the host's
  loopback sshd (A10, A11) — the host's loopback services are not reachable from a case.
- Process containment works: 5 pids, pid 1 is the bwrap argv itself, and a `setsid` grandchild is gone after exit
  (A12, A18, A19) — `--unshare-pid --die-with-parent` is doing its job. The C1 child is the one that leaks (F1).
- The gate's own tree stays honest under the counter: gate copies are digest-checked after every mutant
  (`round39_c1_verify.py:369`), and `run_gate` catches `TimeoutExpired` (`:215-216`), so a hanging gate is a
  non-result rather than a false accept.

## 4. Not tested / limits of this review

- I did not attempt a write to the real lane from a module: writability was established with `os.access` (B) and
  writes were confined to my scratch. A lane-destroying module is therefore *shown reachable*, not exercised.
- No 300 s timeout was run in production shape; F6 uses a copy of the probe with the timeout constant changed and
  nothing else (diff: only `:216`).
- No kernel/userns escape, no seccomp-bypass, no `io_uring`/`userfaultfd` class work; the sandbox review is a
  configuration and observed-behaviour review, not a fuzzer.
- The C2 sandbox was exercised with my own recipes at the frozen argv; the 25 frozen cases were not re-run (the
  receipt is another seat's).
- Host: bwrap 0.13.1 (not setuid, unprivileged userns enabled), Python 3.14, git 2.56.0 — F2/F3/F4's mechanics are
  plain `subprocess` semantics and should not be host-specific; the uid/capability numbers in F5 are host-specific.
- Tooling: nothing installed or upgraded this seat; no pacman transaction attempted.

VERDICT: sentinel-6-findings
