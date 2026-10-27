# R45ExecHarnessRO — run_fence sandbox confinement review (kengaku r45 wave 1, 2026-10-26)

Seat: R45ExecHarnessRO (reviewer, leaf). Judged on: calibration, safety.
Target: verify that `run_fence`'s sandbox in `plans/round45_c1_verify.py` really is read-only and isolated,
by instrumenting probe fences and running each through the counter's real FENCE-RUN path in a clone.

## Method

- Lane clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane`,
  `git -C $S/lane rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO/lane` (verified before any write).
  Clone HEAD `05b02e2b7894a9c83219685f2374905e11c1beda` (2026-10-26 23:27:18 -0300, "round-45: first recorded probe run");
  freeze commit `b4fcd35141…` is an ancestor (merge-base check). `plans/fixture_fence.py` absent in the clone (frozen state intact).
- Scratch: `S=/fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO`, `TMPDIR=$S`, probe roots `k45probe-kqeuc33j` (run 1) and
  `k45probe2-iqv4viqi` (run 2) under it.
- Driver: imports the clone's `plans/round45_c1_verify.py` and calls its `run_fence` **verbatim** (same bwrap+strace+counting
  code the predicate is judged with); fixtures built by the counter's own `build_module` (round-44 builder, imported unchanged).
  `PINS total=33 mismatched=0` in both runs. `FENCE_TIMEOUT=120`, `STRACE=/usr/bin/strace`.
- Probes: 14 per-leg fences (run 2; run 1 used 6 multi-leg fences whose reasons were truncated by run_fence's 120-char cap —
  per-leg fences fix that). Each fence is exec'd by the counter's HARNESS (`plans/round45_c1_verify.py:108-117`) with cwd=d,
  under `k44.ro_sandbox(writable=(logdir,), hide=(lane,), empty=root/empty)` + `strace -f -qq -y -e trace=open,openat,openat2,creat`
  (`plans/round45_c1_verify.py:178-183`); sandbox construction is `plans/round44_c1_verify.py:341-362` (`--ro-bind / /`,
  `--unshare-pid --unshare-net --unshare-ipc --tmpfs /run --die-with-parent --new-session`, hidden targets ro-bind an empty dir).
- `lsp`: no lsp server/device is available in this session; analysis is source read + strace evidence (recorded per role rules).

## Run 2 (clean envelope — the counted measurement)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO/env /fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO/env --bind /fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 -u /fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO/driver2.py
ENVELOPE start 23:45:27 cwd=/fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO
ENVELOPE end 23:47:30 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

Fence fixture: `refusals45/f1_gitfile.py` fid `f1-gitdir-outside` (tool order); sleep probe on `f2_deep.py` fid `f2-deep-worktree`.
All lines from `run2-driver.out.txt` (sha256 5614ab49bdd18fdb…); strace logs under `run2-strace/`.

| # | probe fence | verdict | opens | reason (verbatim) |
|---|---|---|---|---|
| 1 | w_d | BREACH | 0 | `w-into-d errno=30 Read-only file system` |
| 2 | w_parent | BREACH | 0 | `w-parent errno=30 Read-only file system` |
| 3 | w_grandparent | BREACH | 0 | `w-grandparent errno=30 Read-only file system` |
| 4 | mkdir_parent | BREACH | 0 | `mkdir-parent errno=30 Read-only file system` |
| 5 | shadow_read | BREACH | 0 | `shadow-read errno=13 Permission denied` |
| 6 | shadow_write | BREACH | 0 | `shadow-write errno=13 Permission denied` |
| 7 | tmp_write | BREACH | 0 | `tmp-write errno=30 Read-only file system` |
| 8 | hostname_read | BREACH | 0 | `hostname-read ok len=9` |
| 9 | admit_outside | **ADMIT** | **3** | (None returned deliberately) |
| 10 | git_version | BREACH | 0 | `git-version rc=0 out=git version 2.56.0` |
| 11 | git_init_parent | BREACH | 0 | `git-init-parent rc=1 err=/fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO/k45probe2-iqv4viqi/fx` |
| 12 | git_init_tmp | BREACH | 0 | `git-init-tmp rc=128 err=fatal: cannot change to '/tmp/k45_git_target': No such file or directo` |
| 13 | git_lane | BREACH | 0 | `git-lane rc=128 err=Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not s` |
| 14 | sleep | **HUNG** | 0 | (240 s sleep > FENCE_TIMEOUT) |

`LEAK-SCAN[...] none` after every leg and at final (in-envelope /proc scan for `harness.py|fixture_fence|probe_|k45probe|strace`).

### Strace-counted evidence (paste of the deciding lines)

- (a) write into d — `run2-strace/f00001.txt:94`:
  `openat(AT_FDCWD<…/fx/refusals45-f1_gitfile/f000>, "…/fx/refusals45-f1_gitfile/f000/x.txt", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = -1 EROFS (Read-only file system)`
- (b) write/mkdir into the fixture's parent and grandparent — same `-1 EROFS` on `…/fx/refusals45-f1_gitfile/x.txt` and
  `…/fx/x.txt` (`f00002.txt`, `f00003.txt`; mkdir leg `f00004.txt`, errno 30 returned to the fence).
- (c) /etc/shadow — read and append both refused `errno=13 Permission denied` (uid 1000; `f00005.txt`, `f00006.txt`).
- (d) deliberate outside open + ADMIT — **counted, opens=3** (`f00009.txt:94-96`):
  `openat(…, "…/k45probe2-iqv4viqi/btmp", O_RDONLY|O_CLOEXEC|O_DIRECTORY) = 3<…/btmp>`
  `openat(…, "…/fx/refusals45-f1_gitfile", O_RDONLY|O_CLOEXEC|O_DIRECTORY) = 3<…/fx/refusals45-f1_gitfile>`
  `openat(…, "…/fx/refusals45-f1_gitfile", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3<…/fx/refusals45-f1_gitfile>`
  (the third is `os.scandir`'s own open of the parent). A deliberate outside open is counted (read>0) while the fence ADMITs.
- git exec — `f00010-13.txt`: git 2.56.0 execs and runs (rc=0 `--version`); `git -C <fixture parent> init` rc=1 with stderr
  beginning at the fixture-parent path (git's mkdir-failure shape `<path>/.git: <errno text>`; shape reproduced host-side:
  `git -C /sys init` → `/sys/.git: Permission denied` — tail text beyond the 70-char fence cap is [INFERENCE]);
  `git -C /tmp/k45_git_target init` rc=128 `fatal: cannot change to '/tmp/k45_git_target': No such file or directo…` —
  the fence could not even create the target dir (tmpfs /tmp is read-only inside);
  `git -C <lane> rev-parse --show-toplevel` rc=128 `Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not s…` —
  the lane is hidden by the empty ro-bind, its `.git` undiscoverable. Zero counted opens on all four git legs.
- sleep past FENCE_TIMEOUT — verdict `HUNG opens=0` at 120 s (wall 23:45:27→23:47:30 for the whole run). The surviving partial
  log `run2-strace/f00014-hung.log` (93 lines: 85 successful startup/stdlib opens, 8 ENOENT, **0 EROFS, 0 writes**) ends at the
  fence-source read, then silence — the fence sat inside the sandbox doing nothing but sleeping until the kill.

## Run 1 (envelope INVALID — reported per protocol, does not count)

```
ENVELOPE start 23:36:09 cwd=/fast/scratch/hyaku/kengaku-r45/R45ExecHarnessRO
ENVELOPE end 23:38:11 exit=0 local_bin_content_before=c263b11afb1cccf6 after=e396f23e40a69201 CHANGED
ENVELOPE measurement INVALID (PATH dir content changed while it ran)
```

Exit 4 per envelope contract. Cause: a concurrent host writer changed `~/.local/bin` content during the 122 s run — this seat
installed nothing (no pacman/uv/npm calls made); other seats' authorized tool installs are the plausible writer [INFERENCE].
Run 1's six probes produced the same verdicts as run 2 (`run1-driver.out.txt`, sha256 9c494fe6d5164174…): BREACH×3 (w_d,
w_parent, shadow — errno 30/13 identical), ADMIT opens=3 (admit_outside), git legs rc 0/1/128/128, HUNG opens=0. One aborted
attempt between the runs (missing `$S/stracekeep2`, FileNotFoundError in run_fence's keep-copy at `:225`) executed no probe and
is a seat setup error, disclosed here.

## Findings

Confinement verdict components (details 1-7 hold; 8-9 are scope/gap observations):

1. **Read-only holds everywhere tested**: writes into d, the fixture parent, the grandparent, and /tmp all fail EROFS
   (errno 30); mkdir fails identically. The only writable path in the fence sandbox is the strace log dir.
2. **Host secrets unreachable**: /etc/shadow read and write refused (errno 13, uid 1000).
3. **Deliberate scratch-outside opens are counted**: ADMIT + opens=3 (btmp dir, fixture parent ×2) — the counter's READ
   detection works on an admitting fence; in `main()`'s classification an ADMIT dominates (REFUSAL module → LEAKED,
   `plans/round45_c1_verify.py:259-263`) and an honest fixture with opens>0 counts into `read` (`:271-273`).
4. **git exec cannot write or discover**: init at any outside target fails (rc=1/128); the hidden lane's repo is invisible
   (discovery stops at the filesystem boundary); no counted opens.
5. **Timeout path is clean**: sleep(240) > FENCE_TIMEOUT=120 → HUNG, opens=0, no process leak (in-envelope LEAK-SCAN none;
   host-side pgrep after the run showed only other lanes' `mado-r48` stracers, none of mine).
6. **Failed opens are not counted** (DONE_RE skips `=-1`/`E*` results, `:105,199-201`): observed on git's
   `<parent>/.git/config = -1 ENOENT` (`f00011.txt:128`) — correct per the frozen "successful or never-returned open" rule.
7. **Never-returned opens are counted** (pending-branch `:216-222`): the f4-fifo READ control in the frozen claims depends on
   it; code path read and confirmed present (not re-executed here — the frozen control already exercises it).
8. **Scope observation (frozen, not a break)**: opens outside the build scratch are neither blocked nor counted —
   `/etc/hostname` read succeeded (`len=9`, opens=0), and every fence run reads ~90 host files (python stdlib, ld.so.cache,
   /proc/self/maps). The counter's opens rule is scratch-scoped by the frozen docstring (`:190` scratch = `<root>/fx`,
   `<root>/btmp`); write-isolation is bwrap's EROFS, which held. A fence can read readable host data without a READ verdict.
9. **Evidence-preservation gap (minor)**: the HUNG path (`:189`) returns before the keep-copy (`:223-226`) and before log
   parsing, so a fence that opens outside paths and *then* hangs is recorded HUNG opens=0 with its partial strace log left only
   in the scratch root, which `main()` deletes in `finally` (`:329`). Observed here only because I kept the probe root.

## Receipts (all under `.ufo/waves/round-45/w1/R45ExecHarnessRO/`, none >1 MiB, total 652K)

`run1-driver.out.txt` 9c494fe6d5164174…; `run1-driver.py.txt` 8c8eec41c7ca7064…; `run1-strace/f00001-5.txt`
(bcfbea8e…, ac2ed1ec…, 88c7fa90…, 324b77d5…, e2779942…); `run2-driver.out.txt` 5614ab49bdd18fdb…; `run2-driver.py.txt`
6760498a6d891de0…; `run2-strace/f00001-13.txt` (07890efb…, 9b5885e8…, 3bb9fd08…, 95a6d03d…, 4264c1f2…, d58b5810…,
8e3d2b81…, db519099…, 87cae951…, 747458c2…, 7db00d05…, d9488666…, a60c7167…); `run2-strace/f00014-hung.log` 4fd0bc6f91d7afd8….

No lane file was edited; the clone and probe roots live only in my scratch (deleted below). No tool was installed by this seat.

VERDICT: harness-confinement-holds-yes-details-9
