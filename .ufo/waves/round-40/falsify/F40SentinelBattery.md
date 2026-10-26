# F40SentinelBattery — security scan of `plans/battery40/*.py` and `.ufo/waves/round-40/claims/witness/*.py`

Round 40, WAVE 2 (FALSIFY). Target: the 7 battery modules + 3 pre-freeze witness modules, measured at
lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.

## 0. Measurement position (and one discrepancy)

Lane checkout is one commit **past** the named tip:

```
$ git -C …/kengaku-shokunin rev-parse HEAD          → c9c793ca33fab1cdaf1127c06ba31685c7db1325
$ git -C …/kengaku-shokunin log --oneline -5        → c9c793c round-40: wave-2 spec and dispatch (35 seats, policy v1)
                                                       ec1005a round-40: lesson, SCORECARD/LOG … ✓ the named tip
$ git diff --stat ec1005a… c9c793c -- plans/battery40 .ufo/waves/round-40/claims   → (empty)
```

`c9c793c` touches neither `plans/battery40/` nor the claims dir, so scanning at `ec1005a` (my scratch
clone) and at the working tree measures byte-identical targets. All numbers below come from the scratch
clone `$S/lane` at `ec1005a`, not from the lane.

**Method.** Fixtures are data plus a `build(ctx, d)` function; the counter executes them through
`round40_c1_verify.py --build-module <mod> --dest <fixture_root> --pristine <lane_clone>`
(`plans/round40_c1_verify.py:288-301`). Each of the 10 modules was run exactly once through that path,
inside the HOST-SAFETY wrapper, under `strace -f -e trace=openat,execve,connect`:

```
S=/fast/scratch/hyaku/kengaku-r40/F40SentinelBattery
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
         HOME=$S/root/home TMPDIR=$S/root/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  strace -f -e trace=openat,execve,connect -o $S/traces/<mod>.trace \
  /usr/bin/python3 $S/lane/plans/round40_c1_verify.py \
    --build-module $S/lane/plans/battery40/<mod>.py --dest $S/dests/bat_<mod> --pristine $S/pristine
```

All 10 modules: `rc=0`. 30 fixtures built (3+2+3+3+3+4+3 battery, 2+3+4 witness).
Receipts: `.ufo/waves/round-40/falsify/F40SentinelBattery/` (8 files; commands inline in each).

## 1. Headline: the landed modules are clean on every axis I was asked to attack

| axis | result | evidence |
|---|---|---|
| writes outside the fixture root | **0** | `write-census.txt` — every absolute write-intent `openat()` is under `$S/dests/<module>/…`, plus 171×`/dev/null`, 20×`/dev/tty`; grep for `/etc /usr /run /home /root /opt /var` returns empty |
| `~/.local/bin` | **unchanged** | `host-snapshot.txt` — 23033 → 23035 snapshot lines; `diff … \| grep -c '\.local/bin'` = **0** |
| network | **0** | `grep -c "connect(" → 0`, `socket( → 0` across all 10 traces. The two `https://raw.githubusercontent.com/…` (`a_bind.py:19`, `w_anchor.py:7`) are inert string data, never fetched |
| import-time side effects | **0** | dedicated import-only run per module under `strace -e openat`: zero write-intent opens, zero files created |
| subprocesses left running | **0 survivors** | 18 detached children, all `+++ exited with 0 +++` before the build child (`maintenance-census.txt`); `pgrep` after the runs finds only peers' processes |
| PATH/env | build child pinned | `Ctx.ENV` (`:238-242`) fixes `PATH` to a system-only list and `HOME=/nonexistent`; `/nonexistent` was never created |
| git config that executes code | **none** | no `core.hooksPath` / `core.fsmonitor` / `filter.*` / `pager` / `alias.*` / `sshCommand` key in any fixture `.git/config`; the closed subcommand list is `rev-parse, clone, add, commit, maintenance, init, checkout, branch, update-index` — no `config`, no `subcommand`, no `hook` |

That is the positive result the admission decision needs, and it is stronger than a code read: it is a
syscall trace of 30 builds.

## 2. Findings

### F1 (Medium) — the build child runs with the whole host writable, and no counter check observes a write outside the fixture root

`plans/round40_c1_verify.py:304`:

```
argv = [BWRAP, "--dev-bind", "/", "/", "--proc", "/proc", "--unshare-pid", "--die-with-parent", "--new-session"]
```

`--dev-bind / /` is a read-**write** bind of the entire filesystem. The three things that could notice a
misuse all stop at the fixture boundary:

- `fingerprint(d)` (`:310-317`) walks only the fixture directory;
- `path_ok(tok, d)` (`:326-330`) validates only the **argv tokens** the build returns, never what `build()` did;
- `SIDECHANNEL` (`:101-102`) is a 16-token substring denylist (`/proc`, `environ`, `hookspath`, `fork`, …) with **no** absolute-path term.

**Exploit path, measured.** A probe module whose only sin is one absolute-path `write_text` to a path outside
its fixture root, containing none of the 16 denylist tokens:

```
denylist hits: NONE -> sidechannel counter=0
PINS total=3 mismatched=0
FIXTURE z-outside-write tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)   rc=0
$ ls -l $S/escape/escaped.txt → -rw-r--r-- 1 vgpnk vgpnk 33 … /escape/escaped.txt
```

The write landed and every counter line still read clean (`escape-probe.txt`). Substituting
`/home/vgpnk/.local/bin/git` for that path is the wave-1 shim (`R40CritC1Counter.md` A2) reconstituted
inside the counter's own build phase, where the frozen predicate has no line to report it.

**Impact.** C1 admission genuinely rests on non-author review, exactly as the task states — the counter
cannot see a dishonest battery's writes. This corroborates `.ufo/waves/round-40/build/R40SentinelCounter.md`
("whole host fs writable") and supplies the receipt it lacked.

**Smallest remediation.** One line: `--ro-bind / /` instead of `--dev-bind / /`, plus
`--bind <dest> <dest>` and a `--tmpfs` for the build's TMPDIR. The build only writes inside `dest` and its
`git` children only write inside the clones it creates there.

### F2 (Medium) — `--shared` clone aliases every fixture's object store to the shared pristine, outside the fixture root

`Ctx.clone` (`:261-264`) runs `git clone -q --shared`. Each fixture therefore carries:

```
$ cat dests/bat_a_tok/f000/lane/.git/objects/info/alternates
/fast/…/F40SentinelBattery/pristine/.git/objects
$ grep -A1 'remote "origin"' dests/bat_a_tok/f000/lane/.git/config
  url = /fast/…/F40SentinelBattery/pristine
```

That path is outside every fixture root and outside `fingerprint()`'s walk. Receipt (`alternates-receipt.txt`):

```
$ echo "sentinel-forged" > forged.txt; git -C pristine hash-object -w forged.txt
b720c67f1d299f67fde4b12ba7605e8c04f1a98c
$ git -C dests/bat_a_tok/f000/lane cat-file -p b720c67f…
sentinel-forged
```

**Exploit path.** One module writes a blob (or, via `remote.origin.url`, a fetch or a `push`) into the
pristine; every sibling fixture — including ones in *other* modules of the same run — resolves it. That is
cross-module fixture forgery with **zero** writes inside any fixture dir, so `tampered=` cannot move, and
`fingerprint()` has nothing to compare.

**Impact.** The battery's isolation claim ("each fixture is its own repository") holds for worktrees, not
for object stores.

**Smallest remediation.** `git clone -q --no-hardlinks` (full copy) in `Ctx.clone`, or keep `--shared` and
add `git -C <dest> repack -a -d` + drop `objects/info/alternates` before returning.

### F3 (Low) — `fingerprint()` deliberately skips `.git/index`, which is the one file one fixture is read from

`:317`: `if rel.endswith(".git/index") or rel.endswith(".lock"): continue`

The carve-out is necessary — the tools themselves refresh the index — but it leaves the staged bytes
unverified, and `a_bind`'s third fixture reads exactly those bytes:
`{"fid": "a_bind-a17-index-bytes", … "build": build_a17}` returns `["--lane", …, "--evidence-ref", "index"]`
(`plans/battery40/a_bind.py:81-95,103-104`).

**Exploit path.** Anything that rewrites the index between `fingerprint()` and the tool's index read (a
leftover writer, see F4; or the tool's own refresh) changes what A17 evaluates while `tampered=0`.

**Impact.** Bounded: it can only move one fixture between `accept` and a non-`accept`, which the tool-run
model would still score as `wrong` rather than as tampering.

**Smallest remediation.** Fingerprint `git -C <fixture> ls-files -s` output (index content, not stat data)
per fixture alongside the tree hash.

### F4 (Low) — every `git add`/`commit` in a build spawns an unsynchronized detached writer into the fixture's `.git`

18 detached children across 4 modules (`a_bind` 2, `a_man` 2, `o_gate` 6, `w_order` 8):

```
execve("/usr/lib/git-core/git", ["git", "maintenance", "run", "--auto", "--quiet", "--detach"])
```

They write `.git/packed-refs.lock` → `.git/packed-refs.new` → rename (42 and 20 write-intent opens). All 18
exited 0 *before* the build child (`tail -2 bat_a_man.trace` shows `18 +++ exited with 0 +++` then
`4 +++ exited with 0 +++`), and `--unshare-pid --die-with-parent` bounds them, so there is no survivor today.

**Exploit path.** `--detach` means git does not wait. `fingerprint()` does not skip `packed-refs`. If a
fixture ever has real maintenance work, the child can outlive the build child and write `.git/packed-refs`
either before `fingerprint()` (invisible mutation) or after it (a spurious `TAMPERED` on a correct battery —
a flake in the frozen predicate). `a_man` and `o_gate` are the exposed shapes: their build's **last** action
is a `git commit`.

**Smallest remediation.** Pin it off in `Ctx.ENV` the way `Runner.env()` already pins
`core.fsmonitor`/`core.hooksPath` (`:365-367`): add `GIT_CONFIG_KEY_n=maintenance.auto`,
`GIT_CONFIG_VALUE_n=false` (or `gc.auto=0`).

## 3. Observations (no severity, no receipt of harm)

- **O1 — `Ctx.sh` does not carry the toplevel guard.** `sh` (`:254-259`) validates only `cwd`; the
  `rev-parse --show-toplevel` refusal lives in `git` (`:272-277`). A module calling
  `ctx.sh("git","-C","/elsewhere",…)` bypasses it. **No landed module calls `Ctx.sh`** (grep: zero hits in
  all 10 files), so this is inert — but it is the shortest path to F1's capability.
- **O2 — build-child env is weaker than the tool-run env.** `Ctx.ENV` (`:238-242`) omits the
  `core.fsmonitor`/`core.hooksPath` neutralizers that `Runner.env()` (`:365-367`) sets. No exposure today
  (fixtures are fresh `init`/`clone` repos with no hooks and no config inheritance, since
  `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` are both set), but the asymmetry is unnecessary.
- **O3 — the PATH exposure is in the *tool* run, not the build.** The build child's `PATH` is the constant
  `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` (`:106`), which does **not** contain
  `~/.local/bin` (measured: `False`). `Runner.env()` (`:362-363`) uses `os.environ["PATH"]`, which on this host
  does contain `/home/vgpnk/.local/bin`. That localizes wave-1 A2 to `Runner.run`, not to the battery.

## 4. Tooling

No installs, no upgrades: `bwrap`, `strace` and `python3` were already present and sufficient. No pacman
run, no user service, no background job left running.

VERDICT: battery-security-4-findings
