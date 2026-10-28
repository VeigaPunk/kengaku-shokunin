# R50C1CritMount — mount-boundary hostile/honest pair (R50-C1 critic seat)

**Seat:** R50C1CritMount (critic, leaf) · **Item:** attempt the mount-boundary pair the r49 critic named
(`.ufo/waves/round-46/w2/R46W2C1Intent.md`): can a mount point be created inside a fixture without root
(bind mount in a user namespace, `unshare -rm`)? Report the observed capability and, if impossible, the exact
refusal text; state what the repair must do when the device check fires.
**Axes named:** novelty (assigned — the C1 instrument/repair's decision surface), with two incidental axes:
*fence-intent fidelity* (does the advertised containment proof cover mount boundaries) and *counter integrity*
(can module code reach the fence's mount namespace). No calibration work.

**Revisions measured (REV lines).**

    REV freeze            3b02d573d58cc6d2e0d27ef92ac0815354912252   (ancestor of tip: OK)
    REV lane tip @start   8acd0f830452198706c21af8bc52d611c0f29177
    REV lane tip @end     297e17927ba9342a87ba27a48cc5270a001de7cb
    REV repair commit     6db0279e2506c1788b26c2586b4d2d774228c6a9  ("S3 fence repair …")  ancestor of tip: OK
    REV base fence        plans/fixture_fence.py @ freeze sha256 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
    REV repair fence      plans/fixture_fence.py @ 6db0279 / tip sha256 57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
    REV counter           plans/round50_c1_verify.py @ tip  sha256 850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999
    REV population pin    b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  (recomputed in the shared clone: matched)

All measurements against a `git clone --shared` of the lane checked out at the freeze commit
(`/fast/scratch/hyaku/kengaku-r50/R50C1CritMount/lane`), plus a read-only copy of the repair fence extracted from
the lane's own history (`git -C lane show 6db0279:plans/fixture_fence.py > fence_repair.py`). No lane file was
written, no mutating git command was run in the lane.

---

## 1. Capability: a mount point inside a fixture, without root — YES, three measured channels

Host: `7.2.11-arch1-1`, git 2.56.0, util-linux 2.42.4, `uid=1000(vgpnk)`, `CapEff=0000000000000000`
(`grep CapEff /proc/self/status`). User namespaces enabled: `/proc/sys/kernel/unprivileged_userns_clone = 1`,
`/proc/sys/user/max_user_namespaces = 122865`.

**Channel A — `unshare -rm` (subprocess).** Works; inside the namespace `euid=0`, `uid_map = "0 1000 1"`. Both
mount kinds succeed on a directory inside the fixture tree:

    $ unshare -rm sh -c 'mount -t tmpfs tmpfs $S/mnt/t && stat -c "%d %n" $S/mnt/t $S/mnt/p'
    TMPFS_MOUNT_OK
    88 /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/mnt/t
    66309 /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/mnt/p
    $ unshare -rm sh -c 'mount --bind $S/mnt/p $S/mnt/t/tgt && stat -c "%d %n" $S/mnt/p $S/mnt/t/tgt'
    BIND_OK
    66309 /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/mnt/p
    66309 /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/mnt/t/tgt

**Channel B — in-process `unshare(2)` + raw `mount(2)`.** This is the channel a module needs, because it changes
the namespace of the *fence's own process* rather than a child's. No root, **no uid map at all**:

    ctypes: unshare(CLONE_NEWUSER) -> rc 0 ; unshare(CLONE_NEWNS) -> rc 0 ; euid 65534 ; uid_map "" (0 bytes)
    libc.mount("tmpfs", "<d>", "tmpfs", 0, "size=8m") -> rc 0   (mountinfo: 728 723 0:88 / <d> rw,relatime - tmpfs tmpfs)
    libc.mount(outside_dir, "<d>", NULL, MS_BIND, NULL)          -> rc 0
    libc.mount(outside_plain_repo, "<d>", NULL, MS_BIND, NULL)   -> rc 0   (probe7, see §3)

Refusals on the variants that do *not* work, verbatim (rc 32 in both cases):

    # plain user, no namespace at all
    $ mount --bind reach/a reach/b
    mount: /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/reach/b: must be superuser to use mount.
           dmesg(1) may have more information after failed mount system call.
    rc=32

    # `-r` without `-m`: userns yes, mount ns still owned by the initial userns
    $ unshare -r sh -c 'mount --bind reach/a reach/b'
    mount: /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/reach/b: permission denied.
           dmesg(1) may have more information after failed mount system call.
    rc=32

    # in-process, after unshare(CLONE_NEWUSER)+unshare(CLONE_NEWNS) but with an EMPTY uid_map:
    # util-linux refuses in userspace before the syscall (euid renders 65534)
    $ mount -t tmpfs tmpfs <d>
    mount: /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/probe5/d: must be superuser to use mount.
    # ...while libc.mount(2) with the same arguments succeeds. A module must call the syscall.

**Channel C — FUSE (setuid helper), capability chain measured, no driver installed.** `/dev/fuse` is
`crw-rw-rw-` (world-writable) and `os.open("/dev/fuse", O_RDWR)` succeeds; `/usr/bin/fusermount3` is
`-rwsr-xr-x root root`. `fusermount3` mounts in the **caller's** mount namespace, so a FUSE mount would be
parent-visible (unlike channels A/B in a child), but no FUSE filesystem driver is installed on this host
(`bindfs`, `fuse-overlayfs`, `squashfuse` all missing), so no FUSE mount could be demonstrated. Named residual,
not measured.

## 2. The pair, measured on the fence under test (freeze) and on the repair (S3)

Driver: `mntprobe2.py` / `mntprobe3.py` under `unshare -rm --propagation private`, in-process `breach(d, argv,
tool)` calls for both fences. Fixtures hand-built (plain `git init` + commits, git env isolated per command with
`GIT_CONFIG_GLOBAL=/dev/null` — the host global config sets `rerere.enabled=true`, which writes
`.git/MERGE_RR`/`.git/rr-cache` and otherwise masks every verdict with
`.git/MERGE_RR is not a plain-init entry`). Control S0 (plain repo, no mount) is `ADMIT` for both fences, so the
only difference in each row is the mount.

| # | fixture state | st_dev | base fence (05d5fe03) | repair fence (57adce4a) |
|---|---|---|---|---|
| S0 | plain repo, no mount (control) | 66309 | ADMIT | ADMIT |
| S1 | bind of an in-`d` dir onto `d/sub` (honest shape, same device) | 66309 | ADMIT | ADMIT |
| S2 | bind of an **outside plain store** onto `d/sub` | 66309 | ADMIT | **ADMIT** |
| S3 | tmpfs at `d/sub` holding a plain store | 88 ≠ 66309 | ADMIT | BREACH `sub crosses a mount boundary (device 88 != 66309)` |
| S4 | tmpfs at `d/sub`, no store | 88 | ADMIT | BREACH `sub crosses a mount boundary (device 88 != 66309)` |
| S5 | `n21` gitfile `wt/.git -> ../store`, store = tmpfs mount at `d/store` | 88 | BREACH `wt/.git is a file (gitdir redirect), not a directory` | BREACH `store crosses a mount boundary (device 88 != 66309)` |
| S6 | `n21` gitfile, store = bind of an outside store (same device) | 66309 | BREACH `wt/.git is a file (gitdir redirect), not a directory` | **ADMIT** |
| S7 | `objects/info/alternates` → tmpfs objects dir outside `d` | 88 | BREACH `.git/objects/info/alternates present (object-store redirect)` | BREACH `.git/objects/info/alternates names a store outside the fixture` |
| S8 | `objects/info/alternates` → bind of an outside objects dir placed at `d/obj` | 66309 | BREACH (same as S7) | **ADMIT** |
| S10 | tmpfs at `d/.git/objects` (walk never descends `.git`) | 88 | ADMIT | BREACH `.git/objects crosses a mount boundary` |
| S11 | alternates points at a tmpfs mount at `d/.git/objects/pack` | 88 | BREACH (alternates) | BREACH `../../probe3/s11/.git/objects/pack crosses a mount boundary` |
| S12 | tmpfs mounted **at `d`** and a plain repo built on it (original `d` invisible) | 88 uniform | **ADMIT** | **ADMIT** |

Reading of the table:

- At the freeze the fence has **no device notion at all** (`grep -c 'st_dev\|mountinfo\|mount boundary'
  plans/fixture_fence.py @ freeze` → `0`). The r46 intent finding is unrepaired there: S2, S3, S4, S8, S10 and
  S12 are all admitted, including a fixture whose entire `.git` store lives on a tmpfs mount.
- The repair's device check is fail-closed where it fires (S3, S4, S5, S10, S11) and it reaches mount points
  *inside* `.git`, which the tree walk never descends (S10), and an alternates target that is lexically inside
  `d` (S11).
- The repair's device check is **silent** for every same-device bind (S2, S6, S8, P6C below) and for any mount
  **at `d` itself** (S12: `ddev` is taken from `lstat(d)`, so a mount at `d` is uniform and invisible).

## 3. Reachability: the bind that defeats the check *is* reachable, without root, on the counter's own model

Two visibility facts measured first (probe `mntprobe.py`/E3–E4, plain user, no namespace):

    # a `unshare -rm` subprocess mount is invisible to the parent
    parent_before 66309 ; IN_NS_BOUND ; in_ns 66309 ; parent_after 66309 ; parent mountinfo: 0 lines
    # and it cannot push a mount into the parent's namespace
    $ unshare -rm sh -c 'nsenter -t 1 -m -- mount --bind …'
    nsenter: reassociate to namespaces failed: Operation not permitted   (rc=1)

So a module that shells out to `unshare -rm` cannot reach the fence. But **`plans/round50_c1_verify.py` runs the
module's `build()` in the counter's own process** (`build_all` → `hb.build_once(...)`, line 142) and then spawns
the fence in a child that **inherits the counter's mount namespace** (`verdicts()`: `subprocess.run([sys.executable,
"-I", harness, fence, dir, tool, json(argv)], cwd=dir, env=scrubbed)`). Channel B therefore lands in the fence's
namespace. Measured end-to-end with the counter's own harness text (probe `mntprobe7.py`):

    C1_control_plain_no_mount  base {rc 11 ADMIT}  repair {rc 11 ADMIT}
    C2_control_empty_no_mount  base {rc 10 BREACH "--lane '.' is not a repository inside the fixture"}  repair {rc 10 BREACH …}
    counter_unshare_NEWUSER rc 0 ; counter_unshare_NEWNS rc 0 ; euid 65534 ; uid_map_bytes 0
    attack_bind_rc 0 ; st_dev_d 66309 ; d_listing [".git", "a.txt"]     # d was EMPTY before the bind
    A_attack_bind_outside_repo_at_d  base {rc 11 ADMIT}  repair {rc 11 ADMIT}
    mountinfo (parent, inherited by the child):
      728 723 259:5 /scratch/hyaku/kengaku-r50/R50C1CritMount/probe7/outside
            /fast/scratch/hyaku/kengaku-r50/R50C1CritMount/probe7/a_empty rw,nosuid,nodev,noatime … - xfs /dev/nvme1n1p2

i.e. an **empty** fixture directory is turned, by a bind mount of an outside plain-init repo, into an admitted
fixture whose store bytes live outside `d`, on the same device, **against the repaired fence with the device
check**, with no root. The same trick in-process without a subprocess (`mntprobe6.py`, A/B/C) shows the fence
reads the mount's bytes (`P6A`: binding an empty outside dir at an honest `d` makes both fences refuse
`--lane '.' is not a repository inside the fixture`) and admits the outside store (`P6B`) at `d` and below `d`
(`P6C`).

## 4. What the repair must do when the device check fires

Grounded in the measurements above, the fail-closed device check that exists at `57adce4a` is right in shape and
must keep exactly these properties; each one is a requirement the next repair must not lose:

1. **Refuse and stop.** Return the one-line reason immediately, before classifying that path or its children, and
   never fall back to admit. Measured: every firing path returns `None`-admitting nowhere (S3/S4/S5/S10/S11 print a
   single-line refusal and no partial classification).
2. **Reference device = `lstat(d).st_dev`, captured once** (`ddev = st.st_dev` in `breach`). Not the parent's, not
   the harness's, not `$TMPDIR`'s: a scratch or work tree that is itself a mount (counter on `/fast/scratch`, lane
   on another device) must stay admissible. Measured: honest controls stay `ADMIT` under this rule.
3. **Every stat the decision makes, before content is read.** Walked directories and files outside `.git`; every
   store entry inside `.git` (`objects/`, `objects/pack/`, `objects/info/commit-graphs/`, `logs/`, `hooks/`,
   `refs/`); and every pointer target it follows — gitfile target, `commondir`, worktree store, alternates target
   and each alternates hop — *at the target*, not only at the lexical parent. Measured: S10 (`d/.git/objects`) and
   S11 (`d/.git/objects/pack`) are caught although the tree walk never descends `.git`.
4. **The alternates resolver must carry `ddev` itself.** `_alternates(path, objects, depth, seen)` at `57adce4a`
   has no `ddev` parameter; S11 was caught only incidentally, because `_objects` device-checks the target's parent
   entry. Smallest correction: thread `ddev` into `_alternates` and return
   `f"{_rel(target, _ROOT)} crosses a mount boundary"` when `os.lstat(target).st_dev != ddev`, so the check does
   not depend on which parent happened to be classified first.
5. **Refuse, do not sanitize.** No "skip the entry and keep classifying" and no "treat as empty": membership of one
   subtree is not evidence about its contents (S10: the store's objects directory is wholly foreign).
6. **Do not claim the check closes the mount class.** It cannot. Same-device binds (S2, S6, S8, `P6B`, `P6C`) and
   any mount **at `d`** (S12) are invisible to a `st_dev` comparison, and `/proc/self/mountinfo` is outside the
   fence's advertised syscall set. The docstring's named limit currently names only "a bind mount of the SAME
   filesystem below `d`"; it must be widened to *any mount whose subtree under `d` is single-device — a same-
   device bind below `d`, and any mount at `d` itself (bind, tmpfs, FUSE, overlay)*.
7. **The reachable form must be closed in the counter, not in the fence.** Because `build()` runs in the counter
   process and the harness child inherits its mount namespace (§3), the only thing that closes S2/S6/S8/P6B at the
   predicate level is: build module code out of the counter's namespace (a build harness child, or
   `unshare(CLONE_NEWNS)` around each build), and/or have the counter — which *is* allowed to read `/proc` —
   refuse a fixture where `mountinfo` shows a mountpoint at or below `d`. Both are counter-side; neither is
   a fence property.
8. **Over-refusal must be named.** The check refuses a plain-init repo that merely *contains* a mount: S4 (tmpfs
   at `d/sub`, no store at all) and S10 (`d/.git/objects` on tmpfs) are both refused although their git store is
   otherwise plain. Neither is in the frozen 126-fixture population, so the predicate is unaffected today; if the
   population is ever extended with "store on tmpfs" or "a scratch mount inside the worktree", those honest rows
   will be over-refused. Record it as a designed refusal.

## 5. Unfalsifiability of the check inside the frozen predicate (novelty finding)

The S3 repair adds a decision path that **no leg of the frozen predicate can exercise and no frozen mutant can
witness**:

- No honest fixture can hold a mount (the builder creates none), and refusals/sealed are module-shape modules
  (`grep -rl 'mount\|unshare' plans/honest50/modules plans/battery4* plans/refusals46 plans/sealed46` → no hits at
  freeze). A clean clone has no way to create one.
- The r49 candidate battery carried the row that deletes the walk device check
  (`c1-mut-03-drop-file-mountbound`, whose own text says "may SURVIVE on hosts without that fixture class"). The
  re-derived `plans/mutants50/c1-mutants.json` at the tip has 15 rows and a `dropped_unwitnessed` list of 7
  (`c50-10, c50-11, c50-12, c50-13, c50-20, c50-22, c50-24`) — **no mount-boundary row appears in either list**.
  So the check was neither kept with a witnessed kill nor recorded as dropped: it is now an invariant whose
  removal no part of the instrument would notice.

Smallest safe corrections (in order of cost):

1. Add one `dropped_unwitnessed` entry for the device-check mutant, with the reason "no leg can create a mount
   point; witnessed only by this seat's namespace receipts". Costs one row; restores the battery's own convention
   (Q38: a frozen mutant's kill direction is witnessed, not assumed).
2. Add the widened named limit (§4.6) to the fence docstring and to the round's "Named limits" so the claim does
   not read the device check as containment of the mount class.
3. If the mount class is to be scored at all, it must be scored by a counter leg that can *run under
   `unshare -rm`* and a fixture prepared by the counter, not by the fence; otherwise keep it out of the predicate
   and cite this report as its receipt.

## 6. Limits of this seat

- One host, one kernel (`7.2.11-arch1-1`), one git (2.56.0). `unprivileged_userns_clone=1` is the enabling
  condition; a host with it at 0 admits only channels B-with-uid-map (untested here) and C.
- FUSE was not demonstrated (no driver installed), so a parent-visible, setuid-assisted mount remains a named
  residual rather than a measured one.
- Verdicts were taken on hand-built fixtures that reproduce the population's plain-init shape (`S0` control
  `ADMIT`), not on the 126-fixture population; the fast leg was not re-run (measured state was given, and the
  population pin was recomputed and matched).
- The identity pin (`tree_sha256`) was not exercised end-to-end; §3 shows it *would* be measured through the bind
  (`d_listing` shows the outside tree at `d`), which is the false-provenance direction, but no counter run was
  made to confirm the pin comparing the forged tree as "inside `d`".
- No lane file was edited, no commit/stash/checkout in the lane, no pacman transaction, no tool installed.

## 7. Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C1CritMount` (NVMe), `TMPDIR` exported inside each command.
All mounts created during the probes were inside a private mount namespace (`unshare -rm --propagation private`,
or in-process `unshare(CLONE_NEWNS)`); verified after every probe with
`grep <scratch> /proc/self/mountinfo` → `NONE` (host namespace clean, no residual mount). Scratch tree removed
before yield; no `/tmp` or `/fast/scratch` residue from this seat.

**VERDICT:** mount-point creation inside a fixture without root is **possible** (`unshare -rm` → euid 0,
uid_map `0 1000 1`, tmpfs and bind both succeed; in-process `unshare(CLONE_NEWUSER)`+`CLONE_NEWNS`+`mount(2)`
succeeds even with an empty uid map); the r46 pair is therefore testable, and it is **reachable on the round-50
counter's execution model** (build in-process, harness child inherits the mount namespace): an empty fixture
becomes an admitted fixture whose store lives outside `d`, against the repaired fence, because the bind is
same-device and the device check is silent. The repair's device check is correct where it fires (fail-closed,
covers `.git` internals and alternates targets) but cannot close same-device binds or a mount at `d`; the
frozen predicate exercises it on **no leg and no mutant** (the mount-boundary mutant appears in neither the 15
rows nor `dropped_unwitnessed`). Base fence at the freeze has no device check at all (S2/S3/S4/S8/S10/S12 ADMIT).
