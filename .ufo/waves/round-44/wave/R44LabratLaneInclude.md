# R44LabratLaneInclude — does `lane_breach` make the counter read a file outside `d`?

Seat: executor/labrat, round 44 (hyaku run 9, 2026-10-26). Report only: no lane file was edited, no frozen file touched.
Lane clone at `/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude/lane` (tip `5e3d3aa06c6b7000929ac3e62563a39159c4501f`).
The counter under test is byte-identical to the freeze commit (`git -C <clone> diff --stat 5f16ed04…..HEAD -- plans/round44_c1_verify.py`
→ empty; sha256 `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad`).

## VERDICT (one line, at the end)

`VERDICT: lane-breach-reads-outside-confirmed` — the parent process opens a file outside `d`.

## 1. Hypothesis and mechanism, read from the frozen source

`build_battery` evaluates the fixture fences in this order (`plans/round44_c1_verify.py:758`):

```
breach = argv_shape_breach(...) or lane_breach(d, argv) or repo_breach(d) or symlink_breach(d) or (order_argv_breach ...)
```

`lane_breach` therefore runs **before** `repo_breach`, which is the leg that refuses an `include.path`
(`:502-506`). `lane_breach` body (`:573-595`) runs git with the pinned environment and no include suppression:

```
:585  for args in (("rev-parse", "--show-toplevel"), ("rev-parse", "--absolute-git-dir")):
:588      r = subprocess.run(["git", "-C", str(lane), *args], ..., env=PIN_CHECK_ENV, ...)
:592      if r.returncode == 0 and not pathlib.Path(r.stdout.strip()).resolve().is_relative_to(d):
```

The refusal at `:592` is *post hoc*: git has already discovered the repo and parsed `.git/config`, include directives
included, before the counter compares `stdout`. `PIN_CHECK_ENV` (`GIT_PINS`, `:137-144`) pins `core.fsmonitor`,
`core.hooksPath`, `gpg.program`, `log.showSignature` — nothing that disables `include.path`. The `lane_breach` docstring
(`:573-578`) states the discovery is run "with no ceiling below the host root", so no `GIT_CEILING_DIRECTORIES` either.

The F5 claim in `repo_breach`'s docstring (`:482-483`) is the invariant under test: "any include.path is refused
outright, so no file outside `d` is parsed". Measured falsified: refused, yes; unparsed, no.

## 2. Isolated mechanism check (no counter)

`git -C repo rev-parse --show-toplevel` with `.git/config` carrying `[include] path = <outside file>`:
`strace -f -e trace=openat` shows exactly one successful open of the outside file
(`openat(AT_FDCWD, ".../outside/inc_wt.cfg", O_RDONLY) = 4`), and `git -C repo config core.worktree` prints the value
taken from that include. `git -C repo config --local --no-includes core.worktree` prints nothing (rc=1) — the flag does
suppress includes for the *command's own* config read. Noted also: a `core.worktree` supplied by an include is **not**
honoured by `rev-parse --show-toplevel` (setup reads repo keys before includes), so the include cannot move the printed
toplevel; a `core.worktree` in the *local* file is honoured. This is why the leak is a read, not an output oracle.

## 3. Counter runs (all inside the round-44 envelope, strace on the counter)

Every run: `python3 <clone>/plans/round44_c1_verify.py --lane <clone> --battery-dir <probe module dir> --work <scratch>`,
`PINS total=2 mismatched=0` in every run. Probe module sources are in this seat's subdir; `build()` creates the repo with
`ctx.init`, writes the include line with `ctx.git(repo, "config", "include.path", <outside>)`, returns `["--lane","repo"]`.

### Probe A — benign include outside `d` (module `inc_benign.py`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/env …/env --bind …/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- strace -f -qq -e trace=openat,execve -s 200 -o …/w/strace_a.txt python3 …/lane/plans/round44_c1_verify.py --lane …/lane --battery-dir …/bat_a --work …/w
ENVELOPE start 20:35:07 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
SETUP fixture 'probe-include-benign' of bat_a/inc_benign.py escapes its directory: repo/.git/config carries an include
ENVELOPE end 20:35:08 exit=2 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The outside file is **opened four times by the parent's own git children**, all with a real fd (`= 4`). Attribution is
by pid: pid 4 is the counter (python3, the strace root), pid 5 is the build `bwrap` (reaped by pid 4 at strace line 560,
*before* the leak), pids 11/12/13 are direct children of pid 4 (`SIGCHLD … si_pid=11/12/13` inside pid 4's stream):

| strace line | pid | argv (abridged) | open of the outside file |
|---|---|---|---|
| 564 | 11 | `git -C …/f000/repo rev-parse --show-toplevel` | line 586 `openat(…/outside/inc_benign.cfg, O_RDONLY) = 4` |
| 591 | 12 | `git -C …/f000/repo rev-parse --absolute-git-dir` | line 613 `… = 4` |
| 620 | 13 | `git -C …/f000/repo config --local --no-includes --get-regexp '^include(if)?\.'` | lines 642 and 645 `… = 4` |

pids 11 and 12 are exactly `lane_breach`'s two calls (`:585`), which run before `repo_breach` refuses. pid 13 is
`repo_breach`'s *own* include detector (`:502`) — **`--no-includes` does not stop the read**: repo discovery parses
`.git/config` with includes on, so the defense opens the outside file twice more before reporting "carries an include".
The fixture is refused as designed, but only after four parent-side reads of a file outside `d` (the build writes the directive; it reads nothing outside).

### Probe C — control: include of a path that does not exist (module `inc_absent.py`)

```
ENVELOPE start 20:36:10 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
SETUP fixture 'probe-include-absent' of bat_c/inc_absent.py escapes its directory: repo/.git/config carries an include
ENVELOPE end 20:36:12 exit=2 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

No `openat` of `absent.cfg` at all (only the build's `git config include.path` execve) — an attempted-and-failed path
leaves no read; the leak in probe A is a genuine open, not a name-resolution artefact. Refusal still fires because
`repo_breach` matches the *directive*, not the target.

### Probe G — nested include pointing at the lane's own `.git/config` (module `inc_nested.py`)

```
ENVELOPE start 20:36:17 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
SETUP fixture 'probe-include-nested' of bat_g/inc_nested.py escapes its directory: repo/.git/config carries an include
ENVELOPE end 20:36:18 exit=2 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The scratch include contains `[include] path = /home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/config`. The parent
reads **both** files: pids 11/12/13 each `openat(…/outside/inc_nested.cfg, O_RDONLY) = 4` followed by
`openat("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/config", O_RDONLY) = 5` (strace lines 586/587, 614/615,
644/645, 648/649). So a fixture can steer the counter's parent process into the read-only home — the same lane tree the
tool sandboxes hide (F42C1Hardened R3). Severity: read-only; the counter does not print the file's contents, so this is
an arbitrary-read primitive, not an exfiltration channel (probe A's `core.worktree` test shows rev-parse ignores
include-supplied repo keys).

### Probe E — include pointing at a FIFO outside `d` (module `inc_fifo.py`)

```
ENVELOPE start 20:36:10 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
SETUP fixture 'probe-include-fifo' of bat_e/inc_fifo.py escapes its directory: --lane git hung
ENVELOPE end 20:36:42 exit=2 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
real	0m33.150s
```

pid 11's `openat(…/outside/fifo.cfg, O_RDONLY) = ?` (unresolved — the syscall is still blocked when strace reports);
F4's 30 s parent timeout fires and the fixture is refused with `--lane git hung`. Consequence: **each** include-to-FIFO
fixture costs the parent 30 s of wall time before refusal (measured 33.15 s end-to-end for the whole counter run). F4
bounds it; it does not prevent the stall.

### Probe D — side effect of the same hole: unparseable include target makes the fence fail open (module `inc_bad.py`)

```
ENVELOPE start 20:36:13 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE probe-include-badconfig tool=anchor expect=reject declared=- observed_rc=2 observed=- WRONG
MUTANT U5 anchor silence SURVIVED exhibits=none  … (5 mutants survive; development mode, one fixture)
BATTERY fixtures=1 wrong=1 tampered=0 sidechannel=0
MUTANTS total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:36:15 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

With the include target `this is not a git config line`, no `SETUP` line is printed: the fixture is **admitted** with the
include still in `.git/config`, and the outside file is opened six times (pids 11/12/13 and three tool-run gits 14/15/16).
Mechanism: every parent-side git call dies on the bad include, so `repo_breach` reaches its detector with `rc != 0`
(`:503-506` skips the check), the two `rev-parse` legs are skipped (`:512` `got[0] == 0` false), `core.worktree` reads
empty (`:517-522`) and the fence returns `None`. The refusal in probes A/C/G depends on git *succeeding*; when it fails,
F5/R4 fail open rather than closed. (Alerting on `rc != 0` — instead of skipping — closes this half.)

## 4. Answers to the assigned question

1. **Does the parent read the outside file?** Yes. Probe A: 4 parent-side `openat` with fd 4, from `lane_breach`'s two
   `rev-parse` calls and `repo_breach`'s `--no-includes` call, all direct children of the counter, after the build
   sandbox exited. Probe G: additionally a lane file under the read-only home.
2. **Is it before `repo_breach` refuses the include?** Yes: `lane_breach` is earlier in the `or` chain (`:758`) and its
   own two calls leak first (pids 11, 12); `repo_breach` then leaks twice more while detecting the directive.
3. **Can the fixture do worse than a read?** No write observed: the parent-side git gets `PIN_CHECK_ENV` (no
   `core.fsmonitor`, `core.hooksPath=/dev/null`, `gpg.program=/bin/true`), `stdin=/dev/null`, 30 s timeout; the only
   controllable side effects measured are (a) arbitrary readable-file open, (b) a 30 s per-fixture stall via FIFO,
   (c) the fail-open admission in probe D.

## 5. Recommended fix (advisory: frozen files untouched, L1 integrates)

1. Refuse the directive **before** any git call: read `.git/config` as text in `lane_breach`/`repo_breach` (stripping
   continuation lines) and reject `include`/`includeIf` there; then no parent-side git needs `--no-includes` at all.
2. Alternatively run the parent-side discovery inside the same restrictive sandbox as a tool run — bind only `d`
   (plus `/usr`, `/etc/ld.so.cache`), never `--ro-bind / /` — so an include outside `d` is unopenable regardless of
   flags. `git config --no-includes` alone is measurably insufficient (probe A pid 13).
3. Treat a non-zero exit from any parent-side git as a breach ("cannot vet the fixture"), not as "no defect".
4. Keep F4's 30 s bound; the FIFO probe shows it is load-bearing.

## 6. Limits of this seat's evidence

- Host git 2.56.0, python 3.14.8; the frozen counter is run unmodified from a shared clone; development mode
  (`--battery-dir`), so `PREDICATE C1 n/a` in every run — none of this is a calibration claim.
- Instrumentation is `strace -f`; the `atime` cross-check is unusable here because `/fast` is mounted `noatime`
  (measured atime 2000-01-01 unchanged after probe A).
- Probe G's target is the lane's `.git/config` (a parseable file); a non-parseable sensitive file would hit probe D's
  fail-open path instead. Nested includes beyond depth 2 were not probed.
- No dependency on the pre-freeze witness module; nothing outside scratch/report was written. No packages installed
  (strace/gcc already present); no pacman transaction.

## 7. Scratch and receipts

Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude` removed at the end with
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44LabratLaneInclude "$S"`.
Receipts in `.ufo/waves/round-44/wave/R44LabratLaneInclude/`: `probe-a-strace.txt` (68127 B), `probe-g-strace.txt`
(68677 B), `probe-e-strace.txt` (61909 B), `probe-a-run.txt`, `decisive-excerpts.txt` (line-numbered deciders),
and the five probe module sources.

VERDICT: lane-breach-reads-outside-confirmed
