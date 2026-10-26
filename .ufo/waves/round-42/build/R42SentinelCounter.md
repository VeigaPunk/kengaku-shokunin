# R42SentinelCounter — security review of the round-42 C1 counter's sandboxes

Seat: `R42SentinelCounter` (sentinel, leaf). Scope: `plans/round42_c1_verify.py` `ro_sandbox`, `build_battery`,
`Runner.run` (incl. the tracer bound by `--ro-bind-data` at `/run/k42-tracer.py`) — can a build child or a tool run
(a) write outside its work/tmp/fixture dirs, (b) reach the network, (c) keep a process alive after the counter exits,
(d) read the hidden lane or variant store, (e) affect another module's fixtures; plus (f) which `.git/config` keys can
run a program during `ls-files`/`cat-file`/`rev-list`/`log`/`ls-tree`/`merge-base`. Nothing was edited; the lane's
`corpus/`, `plans/`, counters, tools and witness files were read only.

Envelope for every run below (verbatim, one line, `receipts/envelope.txt`):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

Q32: `date +%T` before `17:22:36`, after `17:36:51`; `ls -A /home/vgpnk/.local/bin | sha256sum`
`436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` both times (unchanged). Scratch
`/fast/scratch/hyaku/kengaku-r42/R42SentinelCounter` (round-root sentinel present), `TMPDIR` inside it. `bubblewrap
0.13.1`, `git 2.56.0`, `python 3.14.8`.

## Method

Four artifacts, all reproducible from the files copied next to this report:

1. `sandbox_probe.py` — the counter's own `ro_sandbox` (imported, not transcribed) + a payload: write sweep, network,
   `/dev`, `/proc`, `/run`, lane visibility, fd binding, process survival, cross-dir hardlink. Output `probe1.out`.
2. `probe2.py` — hide semantics (contents vs existence), build-mode lane hide, tracer visibility/detectability,
   `CapEff`, remount attempt, hardlink controls. Output `probe2.out`.
3. `probe_a.py` + `probe_b.py` — two minimal battery modules run through the **real counter**
   (`--lane <lane> --battery-dir … --only X7`); the build child's findings travel out in the fixture id, which the
   counter prints. Output `counterrun.out`.
4. `targeted.py` / `targeted2.py` — `.git/config` execution matrix for exactly the ten git invocations the two tools
   issue, under the counter's own tool-run env (`Runner.env`) and under the unpinned env. Outputs `targeted.out`,
   `targeted2.out`.

## Answer to (a)–(e), measured

| question | answer | evidence |
|---|---|---|
| write outside work/tmp/fixture | **No host write.** errno 30 (EROFS) for `/etc`, `/usr/local/bin`, `~/.local/bin`, `$HOME`, `/tmp`, another fixture, `/fast/scratch/…`, and the lane **in a tool run**. Writable only: the two `--bind` dirs plus the sandbox's own `/dev`, `/dev/shm`, `/run` tmpfs. | `probe1.out` `writes` map; `probe_b` `adirect=30` |
| reach the network | **No.** `1.1.1.1:443` → 101 (ENETUNREACH), loopback → 111 (refused), DNS → `gaierror`; `/run/user/1000/bus` absent. | `probe1.out` `net`, `dns`, `unix_runuser` |
| keep a process alive after exit | **No.** A build child and a tool child that spawn `sleep`-canaries leave nothing: `SURVIVORS none` after each sandbox exits, and `--unshare-pid` + `--die-with-parent` kill the namespace (`pids [1, 2]`, `/proc/1` = bwrap). | `probe1.out` `SURVIVORS`; `counterrun.out` `canary=10` + `no canary survivors` |
| read the hidden lane | **Builds: no** (`lane_listdir []`, counter unreadable). **Tool runs: yes** — full lane listing incl. `plans/round42_c1_verify.py` (`lane_counter_readable: true`); see V5. | `probe2.out` (`build-run-hide-lane`), `probe1.out` |
| read the variant store | **No.** `variants/` does not exist while builds run (`variants=NO`); in tool runs `variants`, `slots`, `bin`, `tracer` all listdir `[]`; the builder copy is unreadable (`bin_read=FileNotFoundError`); the `--ro-bind-data` fd does **not** leak (child has only fds 0,1,2 — no variant path). | `counterrun.out`, `probe2.out`, fd test in §"held" |
| affect another module's fixture | **Read yes, write no.** `aread=hello` succeeds; `link()` from the read-only mount → 18 (EXDEV), direct write → 30, `aread2=hello` unchanged. Control outside the sandbox shows the same hardlink **works** and mutates the source, so the block is the read-only mount, not the filesystem. | `counterrun.out` `probe_b` row; `probe2.out` `CONTROL-HARDLINK` / `hardlink2` |

Also held: caps are all zero inside the sandbox (`CapEff 0`, `CapBnd 0`) — `mount --bind` / `-o remount,rw` fail with
rc 32 "must be superuser", so a child cannot re-bind a read-only path writable; `/dev` is fresh with a private
`/dev/shm` (only the child's own file); `/proc` is the sandbox's own pid namespace.

## Findings

### V1 — HIGH — a fixture's `.git/config` runs a program inside the order tool's run

- **Fails:** the frozen docstring's "Both tools execute no fixture code (git plumbing only, hooks and fsmonitor
  disabled)" (round42_c1_verify.py:30; the isolation sentence is :59) and the repair-(a) property "nothing
  inside a run can read which variant it is" (round42_c1_verify.py:22). The un-neutralised key is
  `gpg.program` reached through `log.showSignature`.
- **Exploit path:** a `plans/battery42` module builds an order fixture repo whose `.git/config` carries
  `[log] showSignature = true` and `[gpg] program = <executable>`, and whose claims commit carries a `gpgsig`
  header (no gpg needed: `git hash-object -t commit -w --stdin --literally`). `order_check.py:97`
  (`add_commit` → `git.out("log", "--reverse", "--diff-filter=A", …)`) is executed twice per order fixture, so the
  program runs on the **reference and mutant** runs alike. `Runner.env` overrides only `core.fsmonitor` and
  `core.hooksPath` (round42_c1_verify.py:385-387).
- **Evidence:** `targeted.out` — `gpg+log.showSignature log --format=%H [B-runner] rc=0 exec=YES GPG
  --keyid-format=long --status-fd=1 …`; same for `[A-nopinned]` and for `include.path` (so the key can also be
  pulled in by config include); `rev-list` and `cat-file --batch` do not reach it. `probe2.out`: with the same
  `ro_sandbox`, `bin_read=FileNotFoundError` shows the counter's own directories are hidden, but `probe1.out`
  shows the lane is **not** hidden in a tool run (`lane_counter_readable: true`).
- **Impact:** (i) the counter's stated sandbox property is false for the order tool; (ii) fixture-supplied code runs
  with the run's capabilities: read the whole host read-only, read the unhidden lane (incl.
  `.ufo/waves/round-42/claims/witness/*`, the *pristine* `plans/order_check.py` and the counter itself), write only
  the run's work/tmp, print into the tool's stdout. Reading the live slot (`--ro-bind-data`, readable by the tool and
  its children) plus the lane's pristine file identifies the running variant — i.e. it defeats the purpose of repair
  (a) and the battery rule that forbids reading freeze material. [INFERENCE: the one-step diff is not executed here;
  each read it needs is measured.] (iii) The program cannot forge the 14 declared directions by itself: the only exit
  code it can force is 2 (kill its git parent → `SetupError`), and none of the 14 is `error`-direction — so this is a
  property break plus an information channel today, not yet a fabricated kill.
- **Smallest remediation:** pin the two keys in `Runner.env` (round42_c1_verify.py:380-387): bump `GIT_CONFIG_COUNT`
  to 4 and add `GIT_CONFIG_KEY_2=gpg.program GIT_CONFIG_VALUE_2=/bin/true`,
  `GIT_CONFIG_KEY_3=log.showSignature GIT_CONFIG_VALUE_3=false`.

### V2 — MEDIUM — build children can read the frozen counter (mutant table) through the builder copy

- **Fails:** `build_battery` writes the full counter source to `<scratch root>/bin/builder.py`
  (round42_c1_verify.py:475-476) while the build sandbox hides only `(lane,)` (round42_c1_verify.py:489). The lane
  hide is therefore defeated for the counter file itself, which carries the 14 `old -> new` pairs and the
  `SIDECHANNEL` list.
- **Evidence:** `counterrun.out` `FIXTURE … builder=MUTANTS35972 …` (readable, 35972 bytes, contains `MUTANTS`);
  `variants=NO` at build time (no variant leak), `slots=YES` (placeholders only).
- **Impact:** a battery module can be authored against the exact mutant table at build time from inside the
  sandbox, and any future decision to hide the counter from the battery is silently void. No host risk.
- **Smallest remediation:** add `root/"bin"` to the build's hide list and bind the builder read-only from a path
  outside the scratch root (e.g. a separate `mkdtemp` bound with `--ro-bind`).

### V3 — MEDIUM — `--tmpfs <lane>` is a *writable* empty directory at the lane's name

- **Fails:** `ro_sandbox` implements `hide` as `--tmpfs` (round42_c1_verify.py:304-305), and the build sandbox hides
  the lane that way (round42_c1_verify.py:489). A tmpfs mount point is writable, so the build child wrote at
  `<lane>/k42probe` (`laneW=WROTE`) where every other host path returned errno 30. The lane's *contents* are gone
  (measured: `lane=HIDDEN`, build-mode `lane_listdir []`), and the host lane is untouched (`ls` shows no such file;
  55 paths were already modified in the lane; this seat wrote no lane file).
- **Impact:** "the lane is absent" is false — it is a writable scratch directory at the lane's name; a build can
  plant arbitrary files there (e.g. a plausible `plans/anchor_digest_check.py`), and `os.path.isdir(lane)` is True,
  so any check that tests existence instead of contents is fooled. Contained (private tmpfs, no host mutation), but
  it is a surprising capability for a path the counter calls hidden.
- **Smallest remediation:** replace `--tmpfs <h>` for directories with `--ro-bind <empty dir> <h>` (one `mkdtemp`
  per sandbox), which keeps contents empty and makes writes fail with EROFS.

### V4 — LOW — the build child's git environment is not pinned for the two executable keys

- **Fails:** `Ctx.ENV` (round42_c1_verify.py:229) sets `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL` but not
  `core.fsmonitor`/`core.hooksPath`, so a fixture repo built by a module and then driven through `ctx.git(...)`
  re-executes a `core.fsmonitor` program on any index read.
- **Evidence:** `targeted.out` — `core.fsmonitor ls-files --cached [A-nopinned] exec=YES FSMON 2 …` vs `[B-runner]
  exec=no`; `probe_a` builds its repo through `ctx.git` under `Ctx.ENV`.
- **Impact:** self-execution only (the module authors the repo), fully contained by the build sandbox (caps 0, host
  read-only, rw only dest/tmp). It contradicts the "git config pinned" wording for builds; no boundary crossed.
- **Smallest remediation:** add the same two `GIT_CONFIG_*` overrides to `Ctx.ENV`.

### V5 — LOW — tool runs do not hide the lane

- **Fails:** `Runner.run`'s hide list is `variants, slots, bin, tracer` (round42_c1_verify.py:415-416); the lane is
  not in it (only the build path hides it). Measured: the run sees the whole lane (`lane_entries 16`,
  `lane_counter_readable true`), including the freeze witness directory the battery rules forbid reading.
- **Impact:** alone, none (the two frozen tools read only their argv repo), but it is the read half of V1's chain and
  it puts the freeze witness inside every run's reach.
- **Smallest remediation:** add the lane to `run()`'s hide list, with the same ro-empty-dir bind as V3.

### V6 — LOW — trace mode is detectable from inside a traced run (limit, fails closed)

- **Holds (fail-closed):** `TRACER_SLOT` is bound read-only and readable, and `sys.gettrace()` is non-None while the
  tool runs, so a tool (or fixture code, per V1) can tell the traced re-run from the untraced one — the attribution
  evidence run is not blind. It cannot forge attribution: the tracer overwrites its output file after the tool
  returns, and a missing/unwritable/faked file yields `lines = frozenset()` (round42_c1_verify.py:425-427), i.e.
  `UNATTRIBUTED` and a failed predicate. `os._exit` skips the writer entirely, also fail-closed.
- **Smallest remediation:** none required for soundness; if the asymmetry must go, pass the tracer source with
  `-c` instead of binding a file (argv is then the only tell, which `--ro-bind-data` already avoids).

### V7 — INFO — the `SIDECHANNEL` scan is source-only and trivially bypassed

- **Evidence:** `probe_a.py`/`probe_b.py` build `/home/…`, `/proc`, `/run`-shaped paths by concatenating literals yet
  the counter reports `BATTERY … sidechannel=0`. Fixture *content* is never scanned at all — V1's `.git/config` and
  the gpg program it names contain anything the author likes.
- **Impact:** the scan cannot bound what a run executes; it only bounds what the module's own source spells out.
  Matches the docstring's named limit ("the token scan is a heuristic").
- **Smallest remediation:** none in scope; keep human review, and treat V1's key list as the real control.

### V8 — INFO — `core.worktree` redirects the order tool's root outside the fixture

- **Evidence:** `targeted.out` — with `.git/config` `core.worktree = /etc`, `git rev-parse --show-toplevel` prints
  `/etc`; `order_check.py:155` adopts that output as `root`. `path_ok` (round42_c1_verify.py:343) validates only
  argv tokens against `d` and cannot see git's own root derivation.
- **Impact:** reads only (no exec, no write); a fixture using it lands as `wrong` or rc 2 — fails closed.
- **Smallest remediation:** none in the counter; the tools could prefer `Path(args.lane).resolve()` over the
  `rev-parse` output.

## (f) Which `.git/config` keys run a program during those six commands

Commands tested (exactly as issued): `ls-tree -r --name-only -z`, `ls-files --cached -z`, `cat-file --batch`,
`cat-file blob`, `cat-file -e`, `log --reverse --diff-filter=A --format=%H`, `rev-list --reverse`, `ls-tree -r <c>`,
`merge-base --is-ancestor`, `rev-parse --show-toplevel`; plus controls `log -p`, `ls-files --modified`, `diff`,
`cat-file --batch --filters`.

| key (fixture-controlled) | executes? with the runner env | executes? unpinned | note |
|---|---|---|---|
| `gpg.program` + `log.showSignature=true` on a `gpgsig` commit | **YES** on `log … --format=%H` | YES | V1; not overridden |
| `include.path` → the same two keys | **YES** | YES | include re-injects them |
| `core.fsmonitor=<cmd>` | no | **YES** on `ls-files --cached/--modified`, `status` | neutralised by `GIT_CONFIG_KEY_0` |
| `core.hooksPath` + `post-index-change`/`post-checkout` hooks | no | no (hook never fires for these commands) | neutralised anyway |
| `filter.<d>.clean/smudge/process` + `.gitattributes` | no | no | no content conversion on these commands; a `process` driver **hangs `git add`** during a module's own build (`targeted2.out` `filter setup git add rc=TIMEOUT`), which the counter's 1800 s build timeout turns into `SETUP` exit 2 |
| `diff.<d>.textconv`, `diff.external` + `.gitattributes` | no | no | no patch output is requested |
| `core.pager`, `pager.log` | no | no | stdout is a pipe, not a tty |
| `credential.helper = !cmd`, `core.sshCommand`, `core.gitProxy`, `url.*.insteadOf`, `protocol.ext.allow` | no | no | no transport is used |
| `core.alternateRefsCommand` | no | no | needs `--alternate-refs` |
| `core.worktree` | n/a (no exec) | n/a | V8 |

`targeted2.out`: 66 probe rows (6 config families × 11 commands), `exec=YES` count 0.

## Limits of this review

- Mutant *variants* were not re-audited; the frozen `MUTANTS` list was read only.
- One host (bwrap 0.13.1, git 2.56.0); other git builds may add exec keys (the fix in V1 should be a pinned
  `-c` set, not two literals).
- No hostile module was written that lies in wait across runs (nothing survives a run, measured), and no attempt was
  made to defeat `seccomp` (none is used — the sandbox relies on namespaces, mounts and zero capabilities).
- V1's variant-identification step is reasoned from two measured reads, not executed end to end.

## Receipts (all < 1 MiB, quoted not copied; in `build/R42SentinelCounter/`)

| file | sha256 |
|---|---|
| `probe1.out` | `e3721020f8d54d8a4bf3a66e0cdf59bb53cd6dfcef2046238f1a7dbf25e86829` |
| `probe2.out` | `4b40c3ad27b55239f7d1e5e4f03c6229e3fde1e3ccd67adfd759dc1f29361681` |
| `counterrun.out` | `6319b80b8580ae78595210705aee1a7a4221110fda7c6c3dc21f46cf1af94c93` |
| `targeted.out` | `cd6d2588d0107e51246e9125a7346f03a2e724fd6462f38fa74464ad8fba43e9` |
| `targeted2.out` | `270677aac22f306e9217a2ec4f219081cd918a0fbb82a5419be96b9407e25b8f` |
| `matrix.out` | `5a115d9d2362b5dad597289fc32bf28deba0fd9b14a2419b37e82ddaac745a8b` (12-case sweep aborted at case 5 — the `process` filter setup hang; superseded by `targeted*.out`) |
| `envelope.txt` | `d697d5a9c2563396aa296cdc53332da4edf53cec90d0e692b752fba294c31d4e` |
| `sandbox_probe.py` | `accebc68e2416f5d6c5da41210adfd3a2464523ed378187acc001701b46262d5` |
| `probe2.py` | `46e6faabcbbb94929d4f59abe9be969ccb1dce5a4ebaf894d4bc00d6f83c7b15` |
| `probe_a.py` | `d18a375a86b4e24e86f2293ebf70b4bbcbf0ed9638703efcd9e2895ee0d7113e` |
| `probe_b.py` | `64a9ed38a01dd08a4b1df9e23151424db4866c002d98ed9f96fd382722526ff0` |

No tool was installed or upgraded for this review; nothing outside my scratch and this report subdir was written.

VERDICT: c1-sandbox-findings-8-high-1
