# SentinelR86 — isolation and confidentiality review of the round-86 evidence path

Seat: `SentinelR86` (leaf, read-only). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen claims read in full: `plans/round-86-claims.md` @ `61b0e074a44259c8c022aa2fda257182a0708346`
(BASE `88651a72ef112ed9f5361e1c8c197babec691f96`). No frozen element was edited; nothing was
committed, staged or written outside `.ufo/waves/round-86/w1/SentinelR86/` and (now deleted)
`/fast/scratch/hyaku/kengaku-r86/SentinelR86/`.

**Verdict: FINDINGS — 5, none of which voids R86-C1 or R86-C2 as measured.**
Both counters reproduce their frozen targets at the lane tip and their frozen BASE values at BASE,
and no instrument byte changed after the tip run. Every finding is about *what the instruments
would accept*, not about what this round's delivered bytes say.

---

## 0. The state I measured

| fact | value |
|---|---|
| lane tip at review start | `ab9da0d4` (`round-86: wave evidence — seat reports as they land …`) |
| lane tip at review end | `a571044c` (L1 landed `4d2a0ee8`, `a571044c` while I reviewed) |
| freeze revision | `61b0e074a44259c8c022aa2fda257182a0708346` |
| instrument freeze | `316811fa604eeef1d157bdbf62b5595891dc015a` |
| BASE | `88651a72ef112ed9f5361e1c8c197babec691f96` |
| receipt `LANE_TIP` | `bfda0472d5c163b2b5d2bbf22557f60a940de180` — an ancestor of `61b0e074`, `ab9da0d4` and `a571044c` |

**Instrument-byte integrity (the "voids both claims" condition): clean.**
`hashes.txt`, first 16 hex of sha256, at freeze / `ab9da0d4` / `master` / worktree:

```
plans/round86_raman_probe.py                  09731b3ebcf44485 09731b3ebcf44485 09731b3ebcf44485 09731b3ebcf44485
plans/round86_c1_replay.py                    04f6ec2ae8d2e4e5 04f6ec2ae8d2e4e5 04f6ec2ae8d2e4e5 04f6ec2ae8d2e4e5
plans/round86_c2_repin.py                     a3fbf5064c1c8470 a3fbf5064c1c8470 a3fbf5064c1c8470 a3fbf5064c1c8470
plans/round86-cases.json                      f8aa21f3b3f6ccf9 f8aa21f3b3f6ccf9 f8aa21f3b3f6ccf9 f8aa21f3b3f6ccf9
corpus/evidence/round86/raman-fitting-probe.txt 192932b28a24efda 192932b28a24efda 192932b28a24efda 192932b28a24efda
probe sha256 = 09731b3ebcf4448546184b39d21d9a28016693af935a20f7efddec5cff209cde == TRUSTED_TOOL_SHA
```

**Claim reproduction at the current tip** (`counters.txt`):

```
### C1 rev master (a571044c)
TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0
PREDICATE R86-C1 pass
rc=0
### C1 BASE
DEFECT L1-receipt missing corpus/evidence/round86/raman-fitting-probe.txt
DEFECT L2-stamp
DEFECT L3-tip
DEFECT L4-table missing plans/round86-cases.json@rev 88651a72ef11
DEFECT L5-vectors
DEFECT L6-reproduce no tool plans/round86_raman_probe.py@rev 88651a72ef11
DEFECT L7-ledger status=unexecuted,round=None,receipt=None,subject=None,verdict=None
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=7
PREDICATE R86-C1 fail
rc=1
### C2 rev master
TARGET derived_line=151 shonen_pointer=PROVINCE.md:151 pin_line=151 state_mismatches=0 selftest=pass defects=0
PREDICATE R86-C2 pass
rc=0
### C2 BASE
DEFECT P2-shonen pointer=PROVINCE.md:129 derived=PROVINCE.md:151
DEFECT P3-pin line=129 derived=151
DEFECT P4-state mismatches=1
TARGET derived_line=151 shonen_pointer=PROVINCE.md:129 pin_line=129 state_mismatches=1 selftest=pass defects=3
PREDICATE R86-C2 fail
rc=1
```

The committed receipt's observation block is byte-identical to a fresh probe run at the current tip
(`probe-run.txt` vs the committed file; `diff` of the two `OBSERVATIONS_*` blocks is empty):

```
# tb2 raman-fitting grader probe
...
LANE_TIP a571044c1ea7c243791330607c5b90b6afce9a15      # fresh run; committed says bfda0472d5c163…
WORKTREE dirty
...
CASE exact predicted=P/P/P observed=P/P/P
... (8 CASE lines identical) ...
cases=8 legs=24 mismatches=0
PREDICATE R86-PROBE pass
EXIT 0   (rc=0)
```

---

## 1. Isolation

### 1.1 Every bwrap flag the probe uses, verbatim

`plans/round86_raman_probe.py:169-182` (`sandbox_argv`), as actually executed in my run
(`sandbox_probe.out`, argv printed from the module's own function):

```
/usr/bin/bwrap
  --unshare-all --die-with-parent --new-session
  --ro-bind /usr /usr
  --ro-bind /etc /etc
  --symlink usr/bin /bin   --symlink usr/bin /sbin
  --symlink usr/lib /lib   --symlink usr/lib /lib64
  --proc /proc
  --dev /dev
  --bind <case>/app /app          # writable bind of a fresh per-case scratch dir
  --dir /tests                    # empty writable dir in the sandbox
  --ro-bind <capture> /tests/test_outputs.py
  --ro-bind <case>/harness.py /harness.py
  --clearenv --setenv PATH /usr/bin --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --chdir /app /usr/bin/python3 -I -B /harness.py
```

Flag-by-flag: `--unshare-all` = user, ipc, pid, net, uts, cgroup namespaces;
`--die-with-parent` kills the sandbox if the probe dies; `--new-session` detaches the tty (no
terminal signal path); the two `--ro-bind`s are the *only* host trees; `--symlink` reproduces the
host's merged-`/usr` layout; `--proc`/`--dev` are fresh mounts, not the host's; `--bind …/app /app`
is a writable scratch bind; `--dir /tests` is an empty in-sandbox dir; the two `--ro-bind`s stage
the pinned capture and the harness read-only; `--clearenv` + three `--setenv`s; `--chdir /app`.
In production the capture source is the staged copy under the work dir (`replay`, probe:211-220);
in my argv capture I passed the lane path, which is the *same bytes* and read-only either way.

### 1.2 What the case harness can and cannot reach — observed, not inferred

Command: `python3 sandbox_probe.py` (builds argv with the probe's own `sandbox_argv`, then swaps the
tail for `/bin/sh -c …`; full output `sandbox_probe.out`):

```
uid: uid=1000(vgpnk) gid=1000(vgpnk) groups=1000(vgpnk),65534(nobody)
--- env:
LANG=C.UTF-8
LC_ALL=C.UTF-8
PATH=/usr/bin
PWD=/app
SHLVL=1
_=/usr/bin/env
--- root listing:
app  bin  dev  etc  harness.py  lib  lib64  proc  sbin  tests  usr
--- app:            (empty, then receives only what the case stages)
--- tests:          test_outputs.py
--- home?           ls: cannot access '/home': No such file or directory
--- lane path?      ls: cannot access '/home/vgpnk': No such file or directory
--- tmp?            ls: cannot access '/tmp': No such file or directory
--- shadow:         head: cannot open '/etc/shadow' for reading: Permission denied
--- proc netdev:    Inter-|… only "lo" with 0/0 counters
--- status:         CapInh/Prm/Eff/Bnd/Amb = 0000…, NoNewPrivs: 1, Seccomp: 0
--- write /app:     wrote-app
--- write /usr:     Read-only file system
--- write /etc:     Read-only file system
--- write /:        wrote-root            (/ is bwrap's own tmpfs; nothing persists)
--- parent pid:     4 numeric /proc entries (own pid namespace)
net:  ifaces [(1, 'lo')]   routes  (empty)
host /app/from-sandbox.txt exists: False
case app after: ['from-sandbox.txt']
```

Reachability summary:

| target | reachable? | why |
|---|---|---|
| host `/app` | **no** | `/app` is a fresh bind of a per-case scratch dir; the host has no `/app` at all |
| network | **no** | `--unshare-all` includes `--unshare-net`; only `lo` exists and `/proc/net/route` lists no routes |
| lane tree (`/home/vgpnk/...`) | **no** | the sandbox root is bwrap's own tmpfs; `/home` is not mounted |
| `$HOME`, `USER`, `TMPDIR`, `PYTHONPATH`, cookies/tokens in env | **no** | `--clearenv` leaves `PATH/LANG/LC_ALL` only (observed `env` above) |
| credentials | **no** | uid 1000 with an all-zero capability set; `/etc/shadow` denied |
| host `/usr` | **yes, read-only** | `--ro-bind /usr /usr` (interpreter and site-packages) |
| host `/etc` | **yes, read-only** | `--ro-bind /etc /etc`; `/etc/machine-id` was readable (value not reproduced here) |
| host `/proc`, `/dev` | fresh, isolated | `--proc`, `--dev` create new instances; pid namespace shows 4 pids |
| writes outside its own `/app` | **no persistent write** | `/usr`,`/etc` read-only; `/` is an ephemeral tmpfs; `/tests` exists only per case |

### 1.3 Proof the host `/app` is unchanged

`ls -ld /app` before and after a probe run (`app-before.txt`, `app-after.txt`):

```
ls: cannot access '/app': No such file or directory      # before
ls: cannot access '/app': No such file or directory      # after
```

`/app` does not exist on this host, so there is no content hash to take; the sandbox's `/app` is
proved to be the scratch bind (write inside → `case app after: ['from-sandbox.txt']`, host
`/app/from-sandbox.txt exists: False`).

### 1.4 No file outside the work dir is written

Command pair around one probe run (window in `window.txt`, diff in `find.diff`, snapshots in
`find-before.txt.gz` / `find-after.txt.gz` with hashes in `find-snapshots.sha256`):

```
find $LANE -xdev -printf '%p\t%s\t%T@\n' | LC_ALL=C sort   # before: 41398 entries
python3 -I -B $LANE/plans/round86_raman_probe.py --lane $LANE --work $SCRATCH/probe-work2   # rc=0
find $LANE -xdev -printf '%p\t%s\t%T@\n' | LC_ALL=C sort   # after:  41398 entries
diff
2c2
< …/kengaku-shokunin/.git   220  1793848424.2933243720
---
> …/kengaku-shokunin/.git   220  1793848521.8966033080
```

Exactly one changed line: the `.git` **directory mtime**. No file was created, deleted or modified
(entry count identical; `.git/index` hashed `8a2bf850…` both before and after that run — it was later rewritten at 00:11:25 by L1's own integration commit, outside my window). The cause is
the probe's own `worktree_state()` (`git status --porcelain`, probe:109-114), which takes and
releases `.git/index.lock`. That is git's index refresh, not a probe write, and it leaves no file
behind — but it is a write *to the lane* by the measuring instrument, so it is recorded here. The
probe's own writes are `tempfile.TemporaryDirectory(dir=work)` and, with `--receipt`, one path the
caller names; neither is used by `L6` (the counter never passes `--receipt`, so the reproduction
cannot overwrite the receipt it compares).

### 1.5 What the sandbox deliberately does not restrict (feeds F5)

`--ro-bind /etc /etc` and `--ro-bind /usr /usr` give the graded code read access to every
world-readable host file in those trees, and to the host's site-packages
(`/usr/lib/python3.14/site-packages` appears on the sandbox `sys.path`). `Seccomp: 0`, no
`--rlimit-*`, no cgroup limit: a misbehaving capture can burn host CPU/RAM until the 60 s
per-case timeout (`run_case`, probe:185-209) reaps it. For a *byte-pinned* capture this is
defence-in-depth, not a live hole.

---

## 2. Confidentiality

### 2.1 Do the instruments read credentials, env vars, cookies, tokens, network or `$HOME`?

No. Three independent checks:

1. `grep -nE 'os\.environ|getenv|Path.home|expanduser|HOME|PWD|USER' plans/round86_raman_probe.py plans/round86_c1_replay.py plans/round86_c2_repin.py` → **no match**. No instrument
   reads an environment variable, `$HOME` or the user database directly.
2. `grep -nE 'socket|urllib|http|requests|ftplib|smtplib|ssl\.|URL'` over the same three files →
   one match only, `plans/round86_raman_probe.py:124: return ssl.OPENSSL_VERSION` — a library
   version string, no network I/O. Nothing in any instrument opens a socket.
3. Any absolute host path or user name: `grep -nE 'vgpnk|/home/|/root/'` → **no match**. The
   instruments are path-portable; the only absolute paths in evidence are the ones the caller passes
   (`--lane`, `--work`).

The four greps and their raw output are in `confidentiality.txt`.

Toolchain reads are deliberate and benign: `platform.python_version()` (probe:263) and
`openssl version` (probe:116-126) with `env={"PATH": "/usr/bin"}`. Credential stores
(`~/.ssh`, `~/.aws`, `~/.netrc`, keyrings, browser cookie DBs) are never opened, named or inferred.

### 2.2 `c1_replay.py`'s stripped `env`: verified, and what it does not cover

Every child *instrument* is launched with a scrubbed environment:

```
365:  env={"PATH": "/usr/bin", "TMPDIR": str(work)}      # L6: the probe re-run
565:  env={"PATH": "/usr/bin", "TMPDIR": str(work)}      # mutant: unmutated counter
570:  env={"PATH": "/usr/bin", "TMPDIR": str(work)}      # mutant: mutated counter
652:  env={"PATH": "/usr/bin", "TMPDIR": str(work)}      # freeze fail-closed selftest
c2: 118/128/291  env={"PATH": "/usr/bin", "PYTHONDONTWRITEBYTECODE": "1"}   # state_check runs
probe: 118, 196, 271, 309, 316  env={"PATH": "/usr/bin"[,"TMPDIR"]}
```

So no `HOME`, no `GIT_*`, no `PYTHON*`, no token-bearing variable reaches a child instrument. This is
correct and it is what makes the `L6` reproduction independent of the caller's shell.

**What it does not cover (F4):**

* `c1_replay.py:91-92` — `git()`: `subprocess.run(["git", "-C", lane, *args])` with **no `env=`**.
* `c1_replay.py:128-132` — `git archive` and `tar -x` with **no `env=`**.
* `c2_repin.py:53-54, 64, 68` — the same three classes of call.
* `round86_raman_probe.py:96-98` — `git_out()`, same omission. In `L6` the probe inherits the
  scrubbed env, so this is clean *inside* the counter; when the probe is run directly (as the
  receipt's `COMMAND` shows) its `git` children inherit the operator's environment.

The counter's own process environment is not scrubbed, and `git -C <lane>` is overridden by
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY`/`GIT_ALTERNATE_OBJECT_DIRECTORIES`/
`GIT_CONFIG*`. Demonstration (`gitdir.txt`), with a throwaway fixture repo created as
`D=$(mktemp -d -p $SCRATCH)` + `git -C "$D" init -q` and its toplevel asserted equal to `$D`
before the one commit:

```
plain      : a571044c1ea7c243791330607c5b90b6afce9a15      # git -C $LANE rev-parse master
GIT_DIR    : 242ba5c115bc94d1b233183ef95c88293a210984      # GIT_DIR=$D/.git git -C $LANE rev-parse master
frozen table visible under GIT_DIR:
fatal: path 'plans/round86-cases.json' exists on disk, but not in 'master'
counter with GIT_DIR set:
DEFECT SETUP archive-failed 242ba5c115bc
PREDICATE R86-C1 fail   (rc=2)
```

The counter measured the *foreign* repo's `master` and then failed closed only because that repo
lacked `plans/`. A foreign repo that carries the same paths (e.g. a clone at an older master) would
be measured instead of `--lane`, and `--lane` would not notice. `tar` likewise inherits
`TAR_OPTIONS`. Severity LOW: it requires control of the counting shell's environment; the round's
own runs are unaffected.

### 2.3 Does the receipt leak anything beyond a work path?

`grep -nEi 'token|secret|passw|credential|cookie|bearer|@|https?://' corpus/evidence/round86/raman-fitting-probe.txt` → **no match**. The receipt contains exactly:

* the member name and the capture path (repo-relative), and three sha256 digests of repo content;
* `HOST_PYTHON Python 3.14.8`, `HOST_OPENSSL OpenSSL 3.6.5 29 Sep 2026 (Library: …)` — toolchain
  versions, not host identifiers;
* `LANE_TIP bfda0472…`, `WORKTREE dirty` — repo state;
* `COMMAND python3 plans/round86_raman_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r86/L1/probe2`
  — the only work path, pointing at L1's scratch directory (an absolute path under `/fast`, not a
  `/tmp` citation, no user secret).

No environment values, no user name, no hostname, no credential, no URL. **Nothing beyond a work
path.** (The one host-identifying byte the sandbox *can* read, `/etc/machine-id`, is not read by any
instrument and does not appear in the receipt.)

---

## 3. Integrity

### 3.1 Can a candidate-controlled file at `/app/results.json` influence the verdict beyond the eight frozen cases?

**No.** There is no read of a host or candidate `results.json` anywhere on the path:

```
grep -n 'results\.json|"/app"|/app/'  →  probe:4 (docstring), probe:176 (--bind … /app),
                                          probe:181 (--chdir /app), probe:192 (write_text)
```

`/app/results.json` is only ever *written* by `run_case` (probe:185-209) from `case["results"]`,
which comes from `plans/round86-cases.json`. That table is pinned three times over:

* `L4-table` compares the table bytes at the measured rev with the bytes read at `FREEZE_REV`
  (counter:226-236, `frozen_table` counter:192-206) — the frozen side is never the measured tree;
* the probe pins `FROZEN_TABLE_SHA` whenever the canonical table is present (probe:142), so a
  drifted table cannot be replayed even if `L4` were bypassed (that redundancy is declared in the
  counter at `DECLARED_REDUNDANT = {"no-table-binding"}`);
* `load_inputs` also re-checks `member`, `subject_sha`, the leg tuple, the case count, case order
  and every `predicted` vector against `FROZEN_CASES` (probe:143-167).

If the canonical table is missing the sha check is skipped, but the fallback path is the *same*
`plans/round86-cases.json` (the module's sibling), so a missing table is a `no-table` setup defect,
not a bypass. A `results` payload may carry arbitrary extra keys (`extra-schema-keys` case), and
cannot move the verdict outside the eight frozen `(id, predicted)` pairs.

### 3.2 Can the graded module import anything from the candidate's staged tree?

**No.** `import_probe.out` — the probe's own argv, with a harness that prints `sys.path`, cwd and
three import attempts (a module and a `results.py` staged in `/app`, and `test_outputs` in `/tests`):

```
{"sys_path": ["/usr/lib/python314.zip", "/usr/lib/python3.14", "/usr/lib/python3.14/lib-dynload",
              "/usr/lib/python3.14/site-packages"],
 "cwd": "/app",
 "import_appmod": "ModuleNotFoundError: No module named 'appmod'",
 "import_results": "ModuleNotFoundError: No module named 'results'",
 "import_test_outputs": "ModuleNotFoundError: No module named 'test_outputs'",
 "python": "3.14.8", "isolated": 1}
```

`-I` (isolated: implies `-E -s -P`) keeps the script directory, the cwd and user site-packages off
`sys.path`; `--chdir /app` only sets the cwd; `runpy.run_path` on a plain `.py` file does not touch
`sys.path`. So the graded module cannot shadow a stdlib/3rd-party import with a file from `/app`, and
cannot import `/tests`. It *can* import the host's site-packages (`/usr` is ro-bound) — intended, and
see F5.

### 3.3 The observation channel is shared with the graded code (F3)

`run_case` launches one process: the harness imports the capture with `runpy.run_path`, calls the
`test_` functions and prints one JSON blob; the probe parses `proc.stdout`. The module executes in
that same process *before* the harness prints, so it can print the payload itself and leave with
`os._exit(0)`, and the probe will accept it (`channel_probe.out`, calling the probe's own
`run_case` with a capture that prints a JSON blob and calls `os._exit(0)`):

```
accepted payload: {"tests": [["test_result_file_exists", "P", ""], ["test_G_Peak", "P", ""], ["test_2D_Peak", "P", ""]]}
observed vector the probe would record: P/P/P
```

Nothing binds an observation to the harness's own execution: the vector is whatever the process
printed. The only control is the byte pin — `load_inputs` refuses any capture whose sha256 is not
`SUBJECT_SHA` (probe:133), and `L8-subject` re-checks the same digest from the measured tree. For
this member the capture is a real TB2 grader with no module-level output, so the surface is closed by
the pin; it is reported because "the sandbox observed it" is weaker than it sounds.

### 3.4 `L6` is reproduction, not authentication — what a lane writer can forge (F2)

`L6` re-runs the tool *from the measured tree* (`tree.root / TOOL`, counter:350-380). That is safe
against a drifted tool because `L2` requires `sha256(tool_in_tree) == stamp.TOOL_SHA ==
TRUSTED_TOOL_SHA` (counter:303-308). But everything the receipt *says* is derivable, and `L6`
therefore confirms determinism, not execution: the observation block is a pure function of the
pinned capture and the pinned table.

Demonstration (`forge.txt`): take the delivered receipt, change only `LANE_TIP` to **BASE**
(`88651a72…`, a real ancestor of the measured tip), and also falsify `HOST_PYTHON`, `WORKTREE` and
`COMMAND`; keep the digests and vectors:

```
LANE_TIP 88651a72ef112ed9f5361e1c8c197babec691f96
WORKTREE clean
HOST_PYTHON Python 0.0.0
COMMAND none
...
TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0
PREDICATE R86-C1 pass      (rc=0)
```

Per-leg, for an adversary who can write (and commit) the lane tree:

| leg | refuses | does not refuse |
|---|---|---|
| `L1-receipt` | absent receipt | — |
| `L2-stamp` | a tool whose sha ≠ trusted; `MEMBER`/`SUBJECT_*`/`CASE_TABLE_SHA`/`TOOL` mismatch; `EXIT != 0` | `HOST_PYTHON`, `HOST_OPENSSL`, `WORKTREE`, `COMMAND` are **presence-only** (never compared) |
| `L3-tip` | an unresolvable commit, or one not in this history | **any** ancestor of the measured rev — including BASE, a tree that predates the tool and table the receipt claims |
| `L4-table` | any table byte drift (plus the probe's own sha pin) | — |
| `L5-vectors` | a predicted vector that is not frozen, or observed ≠ predicted | a *hand-computed* observed vector — it is deterministic |
| `L6-reproduce` | a tool that does not reproduce the block | a receipt minted from the table without ever running the sandbox |
| `L7-ledger` | a missing/incorrect row | the row is itself just data |
| `L8-subject` | capture bytes ≠ `SUBJECT_SHA` | — |

So: **an adversary with lane-write can forge the whole receipt, including a false `LANE_TIP`
provenance, and no leg refuses it.** No leg is *unconditionally* refusing for a receipt whose
`LANE_TIP` names a real ancestor and whose digests are recomputed from the tree. The round's honest
limit concedes the tip-named case; it does not concede the ancestor slack, and the
`--control-forged-receipt` control (`0`×40) only models "names a commit that does not exist", which
no realistic forger would choose. This does not make C1 false — the capture/table/tool pins and the
BASE/tip contrast are real — it bounds what "located" and "executed" can mean.

### 3.5 C2's `P4-state` / `P5-selftest` run an instrument outside the measured tree (F1)

`c2_repin.py:114-128`:

```python
def state_summary(root, lane):
    script = (lane / STATE) if (lane / STATE).is_file() else (root / STATE)
def state_selftest(root, lane):
    script = (lane / STATE) if (lane / STATE).is_file() else (root / STATE)
```

With the frozen counting command (`--lane . --rev <REV>`), `lane` is the **worktree** and `root` is
the extracted revision, so P4/P5 execute `./plans/state_check.py` — a possibly *uncommitted* file —
against the measured tree. Unlike C1's `L6` (which runs the tree's tool and pins its sha via `L2`),
nothing binds the executed instrument to the measured revision.

Demonstration (`p4.txt`), on a scratch clone of the lane (clone toplevel asserted):

```
### measured tree's own instrument:
MISMATCH: P2b.axis.novelty.anchor.1:626 — {"anchor": ":162", …}
MISMATCH: P3d.axis.novelty.anchor.1.pin:626 — {…}
VERDICT: FAIL — at least one frozen assertion mismatches
### real worktree instrument ae87f5834831bdaf
DEFECT P4-state mismatches=2
TARGET … state_mismatches=2 … defects=1
PREDICATE R86-C2 fail      (rc=1)
### stubbed worktree instrument 6d91738fc407de2b (uncommitted; HEAD has ae87f5834831bdaf)
TARGET … state_mismatches=0 … defects=0
PREDICATE R86-C2 pass      (rc=0)
```

A three-line, **uncommitted** replacement of `plans/state_check.py` that prints `VERDICT: PASS` and
exits 0 flips `state_mismatches` from 2 to 0 and the predicate from fail to pass for a *fixed*
measured tree whose own instrument says FAIL. At the delivered tip this changes nothing (worktree
and revision instruments are byte-identical, `ae87f583…`), so the round's claim stands — but the
counted quantity "the number of `MISMATCH:` lines printed by `plans/state_check.py --summary` over
the measured tree" is, as implemented, a property of the lane worktree, not of the measured tree.
`P5-selftest` inherits the same weakness (a stubbed instrument trivially exits 0).

---

## 4. Findings

All five touch `plans/round86_*.py`, which is production and read-only to this seat: they are
routed, not fixed here. F1 is the one that can change a verdict for a committed revision; F2–F5
bound what the claims' words can mean and tighten the sandbox and the counters' subprocess hygiene.

### F1 — MEDIUM — C2 counts `state_mismatches` with an instrument taken from the lane worktree, not the measured tree
*Leg / file:* `plans/round86_c2_repin.py:114-128` (`state_summary`, `state_selftest`), used by
`P4-state` and `P5-selftest`.
*Exploit path:* any writer to `plans/state_check.py` in the lane worktree (any seat, any dirty
state) changes `state_mismatches` and the `P4`/`P5` verdicts for **any** measured revision, including
a committed one, without touching the revision under measurement.
*Evidence:* `p4.txt` (2 → 0, fail → pass, same `--root`).
*Impact:* the claim's own definition of `P4` reads `plans/state_check.py --summary --root <tree>`,
and the round-85 lesson ("a stale frozen pin may not be silently rewritten") rests on `P4` reading
the *measured* instrument. Delivered tip unaffected (bytes identical at `a571044c`).
*Smallest remediation:* in `state_summary`/`state_selftest`, prefer `root / STATE` when a root tree
is measured (`--rev`), and treat a worktree/revision byte difference as a `DEFECT SETUP`; or add a
`P0` that asserts `sha256(lane/plans/state_check.py) == sha256(root/plans/state_check.py)`.

### F2 — LOW — `L3-tip` accepts any ancestor, the stamp's host/metadata fields are presence-only, and the forged-receipt control is a straw man
*Leg / file:* `plans/round86_c1_replay.py:316-331` (`L3`), `:289-317` (`L2`), `:449-478`
(`--control-forged-receipt`).
*Exploit path:* mint a receipt from the frozen table (the block is deterministic), recompute
`SUBJECT_SHA`/`CASE_TABLE_SHA`/`TOOL_SHA` from the tree, set `LANE_TIP` to any ancestor — e.g. BASE,
a revision that predates the tool and the table. All eight legs pass (`defects=0`).
*Evidence:* `forge.txt`.
*Impact:* the receipt's `LANE_TIP` is not evidence of the tree it was minted at, and
`HOST_*`/`WORKTREE`/`COMMAND` carry no weight; "located" means "a receipt with correct digests
exists", "executed" means "the pinned tool reproduces the block". This is narrower than the claims'
sentence "`L2` and `L3` are what a receipt copied in from elsewhere cannot satisfy" reads — true only
for a foreign history.
*Smallest remediation:* make `L3` require the declared tip to *carry* the artefacts it claims
(`git cat-file -e <tip>:plans/round86_raman_probe.py` and `<tip>:<RECEIPT>`), or require `declared ==
tree.tip` for rev trees; and re-point `--control-forged-receipt` at a real ancestor with re-minted
digests (the current `0`×40 fixture tests a case no forger would choose).

### F3 — LOW — the case observation is not integrity-separated from the graded code
*Leg / file:* `plans/round86_raman_probe.py:60-74` (`HARNESS`), `:185-209` (`run_case`).
*Exploit path:* a capture that prints a forged `{"tests": [[name, letter, …], …]}` blob and calls
`os._exit(0)` decides the observed vector for that case; `run_case` accepts it (`P/P/P` in the demo).
*Evidence:* `channel_probe.out`.
*Impact:* nil for this member — `load_inputs` (probe:133) and `L8-subject` pin the capture to
`SUBJECT_SHA`, and the pinned grader has no module-level output. The surface matters for the claim's
wording: the sandbox "observes" only what one shared stdout carries.
*Smallest remediation:* none in-process — the harness and the graded code share one address space
and one stdout, so the pin on the capture is the real control. The cheapest honest fix is to say so
in the receipt grammar (an observation is trusted only to the extent `SUBJECT_SHA` is) rather than to
present the sandbox as the thing that observed it.

### F4 — LOW — the counters' own `git`/`tar` children inherit the ambient environment
*Leg / file:* `plans/round86_c1_replay.py:91-92,128-132`; `plans/round86_c2_repin.py:53-54,64,68`;
`plans/round86_raman_probe.py:96-98`.
*Exploit path:* with `GIT_DIR` exported, `git -C <lane> rev-parse master`/`cat-file`/`archive` read a
different repository, so `--lane` does not pin the repo; the foreign repo's revision is measured and
`--lane` is ignored. `TAR_OPTIONS` is honoured by `tar -x` in the same way.
*Evidence:* `gitdir.txt` (plain `a571044c` vs `GIT_DIR` `242ba5c1`; the counter then measured
`242ba5c1` and failed closed only because the foreign tree lacked `plans/`).
*Impact:* verdict-controlling only for an adversary who controls the counting shell's environment;
none of this round's runs did.
*Smallest remediation:* pass `env={"PATH": "/usr/bin"}` to every `git`/`tar` invocation in the three
instruments (as the child-instrument launches already do), which also removes `~/.config/git/config`
from git's resolution.

### F5 — LOW — the sandbox exposes host `/etc` and `/usr` read-only, and has no resource ceilings
*Leg / file:* `plans/round86_raman_probe.py:170-172` (`--ro-bind /usr /usr`, `--ro-bind /etc /etc`),
`:185-209` (60 s timeout only).
*Exploit path:* the graded code can read every world-readable host file under `/usr` and `/etc`
(`/etc/machine-id` confirmed readable; `/etc/shadow` confirmed denied as uid 1000) and can import any
host site-package; `Seccomp: 0`, no `--rlimit-*`, no cgroup, so a runaway capture consumes host
resources until the timeout.
*Evidence:* `sandbox_probe.out`.
*Impact:* confidentiality of `/etc`/`/usr` is not protected by the sandbox; no credential store is in
those trees, so this is breadth, not leakage. The capture is byte-pinned, so there is no live
attacker in this round.
*Smallest remediation:* bind only what the grader needs (`/usr/lib/python3.14` + `lib-dynload`, or a
`--tmpfs /etc` with a minimal `passwd`), and add `--rlimit-nproc`/`--rlimit-as`.

**Informational (not counted):**
*I1.* `--freeze <rev>` (`c1:667`) lets a caller make `L4` compare the measured table with itself; only
the probe's own `FROZEN_TABLE_SHA` remains. The frozen counting command does not pass it — keep it
that way, or make `--freeze` refuse a revision at/after `FREEZE_REV`.
*I2.* With no `--rev`, `c1_replay.py` measures `fixture_tree(lane)` (`main`, last branch), i.e. the
*dirty worktree*, while the kill rule counts only "the measured committed revision". The counting
command passes `--rev`; a run without it is not the claim's measurement.
*I3.* `L2`'s stamp parser (`STAMP_RE`, counter:63, last-wins dict) would silently accept duplicate stamp keys;
immaterial next to F2's full-forgery surface, but exact-match-on-count would be cheaper than a
later surprise.

---

## 5. What this review does not establish

* I did not re-derive the eight predicted vectors from the TB2 grader by hand; I confirmed that the
  pinned tool reproduces them and that the frozen table pins them. Whether the vectors *are* the
  grader's true behaviour is the capture's business (`corpus/evidence/round52/...`), not mine.
* I did not run Terminal-Bench, the task image or an agent; nothing here speaks to model behaviour.
* I did not attempt to break out of bubblewrap beyond the reads/writes listed in §1.2 (no exploit
  development, per seat bounds); the absence of a breakout is an observation about a stock bwrap
  0.13.1 with `--unshare-all`, not a proof of kernel-level isolation.
* I did not measure the sibling seats' evidence paths; the surface is the three instruments and the
  one receipt named by my ticket.
* My lane-tree write-window evidence (§1.4) is a single 40 s window at `ab9da0d4`; later windows are
  confounded by L1's concurrent integration commits (`HEAD` moved to `a571044c` during the review),
  so I did not re-take it.

## 6. Evidence index (this directory)

| file | content |
|---|---|
| `probe-run.txt` | full probe stamp + observations at tip `a571044c`, rc=0 |
| `hashes.txt` | instrument/tool/table/receipt sha256 at freeze, `ab9da0d4`, `master`, worktree; receipt ancestry; block identity |
| `confidentiality.txt` | the four greps behind §2: no env/`$HOME` read, no host path/user name, no network client, no secret token in the receipt |
| `counters.txt` | C1 and C2 at tip and at BASE |
| `sandbox_probe.out` | full bwrap argv from `sandbox_argv`, and the observed reachability dump |
| `import_probe.out` | `sys.path`, cwd, and the three failed imports |
| `channel_probe.out` | forged observation accepted by `run_case` |
| `forge.txt` | receipt with `LANE_TIP`=BASE + falsified host fields reaching the target |
| `p4.txt` | C2 `P4` decided by a worktree instrument (2 → 0, fail → pass) |
| `gitdir.txt` | `GIT_DIR` redirection of the counter's git reads |
| `app-before.txt`, `app-after.txt` | `ls -ld /app` before/after a probe run |
| `find-before.txt.gz`, `find-after.txt.gz`, `find.diff`, `find-snapshots.sha256`, `window.txt` | lane snapshot pair (41 398 entries), the one-line diff, hashes, window timestamps |
| `sandbox_probe.py`, `import_probe.py`, `channel_probe.py` | the three demonstration drivers; each imports the probe module from the lane and builds argv with its own `sandbox_argv` (their scratch work dirs under `/fast/scratch/hyaku/kengaku-r86/SentinelR86/` were deleted after the runs) |

Scratch (`/fast/scratch/hyaku/kengaku-r86/SentinelR86/`) was deleted after these receipts were
copied here. No tool was installed or upgraded for this seat. No network fetch was made.
