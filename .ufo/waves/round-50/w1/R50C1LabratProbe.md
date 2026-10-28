# R50C1LabratProbe — is the gitfile escape real? (measured under strace)

Seat: `R50C1LabratProbe` (executor, round 50 wave w1) · serves **R50-C1 (novelty)**
Item: one falsifiable probe — with cwd in `d`, `GIT_CEILING_DIRECTORIES` set at `d`, and `d/.git` a gitfile
naming a store outside `d`, does **git itself** resolve and READ that store? Report the syscalls that leave `d`.

**Answer: yes, unconditionally.** git 2.56.0 dereferences the pointer and reads config, HEAD, refs, packed-refs,
commondir, index and loose objects outside `d`; the ceiling setting does not change one byte of that behaviour.
The honest/hostile pairs differ **only** in where the pointer resolves, and the resolved target is what a
containment leg sees (measured against the landed S2 fence, §7).

`REV lane_tip_at_start=c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 · lane_tip_at_end=d6f2fce (S3 repair 6db0279)`
`REV base_tip=71f5f5f77591d8c3d19297ee9785436da45209e4 · freeze=3b02d573d58cc6d2e0d27ef92ac0815354912252 (ancestor of both tips, verified before measuring)`
`REV fence_frozen=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e · fence_at_lane_tip=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`
`REV git=2.56.0 · strace=7.2 · host=linux 7.2.11-arch1-1 · population_pin=b5197f94… (unchanged, not re-derived here)`

## 1. Axes

- **novelty** (the axis C1 claims): the lane had no committed measurement of *what git does* with an out-of-`d`
  pointer. The fence's own docstring reasons about refusing the shape by name; this probe measures the
  mechanism, so the repair's containment rule is grounded in git's observed resolution instead of assumption.
- **harm check**: no production file touched (write scope: this report only), so no other axis moves.

## 2. Fixtures (all built in scratch; every git write asserted `rev-parse --show-toplevel` == its dir)

`<S>` below = `/fast/scratch/hyaku/kengaku-r50/R50C1LabratProbe` (removed at yield). Two scratch-only drivers
were used: `<S>/probe.py` (build nine fixtures, strace each command, classify paths) and `<S>/driver.py`
(fence verdicts + resolved-pointer discriminator). Both were deleted with the scratch tree, so no digest is
claimable here; their construction is fully specified by the recipe and analysis rule below.

| id | documented state | mechanism | pointer line (verbatim) | target |
|---|---|---|---|---|
| **A** | `git init --separate-git-dir=<store>` | `d/.git` FILE, absolute | `gitdir: <S>/work/cases/A-abs-gitfile/store.git` | **outside d** |
| **B** | same, gitfile rewritten relative | `d/.git` FILE, `..` only | `gitdir: ../store.git` | **outside d** |
| **H** | same, pointer literal entirely inside d | `d/.git` FILE, `d/lnk` symlink | `gitdir: lnk` | **outside d** |
| **E** | `git worktree add` | `d/.git` FILE + `commondir` | `gitdir: …/main/.git/worktrees/d` | **outside d** (`--git-common-dir=…/main/.git`) |
| **D** | `objects/info/alternates` | real `.git` in d, absolute entry | `<S>/…/alt/.git/objects` | **outside d** |
| **D2** | same, relative entry | relative, no absolute path anywhere | `../../../../altstore/.git/objects` | **outside d** |
| C | honest class **n21** echo (`gitdir: ../store`, store in d) | `d/.git` FILE | `gitdir: <S>/…/d/.gitstore` | inside d |
| F | honest class **n22** echo (`../../../main/.git/objects`) | alternates, relative | `../../../main/.git/objects` | inside d |
| G | discovery control: no `.git` in `d`, repo at `d`'s parent | — | — | parent's repo |

C and F are shaped exactly like the lane's own honest builders — `plans/honest50/modules/novel50/n21_separate_gitdir.py`
(`gitdir: ../store`, store at `d/store`) and `n22_alternates_in_d.py` (`../../../main/.git/objects` from
`lane/.git/objects`) — so the pairs differ **only** in the resolved target, which is the point.

Construction recipe (per case, inside `<S>`, env per command, never exported):

    env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null XDG_CONFIG_HOME=<S>/nohome/.config \
        HOME=<S>/nohome GIT_AUTHOR_NAME=p GIT_AUTHOR_EMAIL=p@x GIT_COMMITTER_NAME=p GIT_COMMITTER_EMAIL=p@x \
        git init -q --initial-branch=main --separate-git-dir=<abs store> <d>     # A / B
    # then: config probe.marker, commit a marker blob, delete the worktree copy (blob then exists only in the store)
    printf 'gitdir: ../store.git\n' > B/d/.git        # B   (H: ln -s <store> d/lnk; printf 'gitdir: lnk\n' > d/.git)
    git -C main worktree add -q d -b wtprobe           # E
    printf '<abs alt objects>\n' > d/.git/objects/info/alternates                    # D
    printf '../../../../altstore/.git/objects\n' > d/lane/.git/objects/info/alternates  # D2

## 3. Exact commands run (measurement)

    # ancestry + digests, before any measurement
    git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 3b02d573… 71f5f5f7…   # rc=0
    sha256sum plans/fixture_fence.py plans/honest50/population.txt

    # read-only lane clone at the freeze (never the live checkout)
    git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin <S>/lane
    git -C <S>/lane checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252     # rev-parse HEAD == 3b02d57…
    sha256sum <S>/lane/plans/fixture_fence.py                                  # 05d5fe03… (frozen)

    # the probe: build 9 fixtures, run 6 read-only git commands per fixture under strace,
    # twice per fixture (GIT_CEILING_DIRECTORIES=d and =parent(d)), cwd inside the fixture's repo
    python3 <S>/probe.py --work <S>/work          # per command:
    #   strace -f -y -qq -s 4096 -e trace=%file -o traces/<case>__<variant>__<i>_<cmd>.log git <cmd>
    #   cmds: rev-parse --git-dir | rev-parse --show-toplevel | config --get probe.marker |
    #         cat-file -p HEAD:marker.txt | log --oneline -1 | status --porcelain
    #   env: GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null XDG_CONFIG_HOME=<S>/nohome/.config HOME=<S>/nohome
    #        GIT_OPTIONAL_LOCKS=0 GIT_TERMINAL_PROMPT=0 PATH=/usr/local/bin:/usr/bin:/bin

    # fence verdicts: frozen fence imported from the clone, breach(d, argv, "order") called directly
    python3 <S>/driver.py <S>/work <S>/lane
    # landed S2 fence read as a blob from the clone (no checkout, no lane write), same call
    git -C <S>/lane show 6db0279…:plans/fixture_fence.py > <S>/fence_s2.py
    python3 - <<'EOF'                        # importlib-load fence_s2.py, breach(d, ["--lane", rel, …], "order") per case
    EOF                                     # output quoted in §7

Every git fixture call used `git -C "$D"`/`cwd=$D` after asserting the toplevel; no pacman, no installs
(git 2.56.0 and strace 7.2 already present; PACMAN GUARD respected).

## 4. Measured: file syscalls whose resolved path leaves `d`

Analysis rule (applied to every `trace=%file` line of all 114 logs): for each syscall take every quoted path;
resolve a relative path against the `dirfd` strace prints with `-y` (`N</dir>` / `AT_FDCWD</dir>`), and for
`open`/`openat` prefer the **returned fd decoration** (`= 3</abs/path>`), which is the kernel's resolved target;
`normpath` the result. Classify as `in-d` (path == `d` or under `d/`), `outside-store` (the declared outside
store, or any other path under `d`'s parent that is not `d`), else `other` (git runtime: `/usr`, `/etc`, …), which
is counted but not listed. `writes` = the argument string carries `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC`.

`distinct` = distinct absolute paths outside `d` touched; `syscalls` = every `%file` syscall line naming one;
`open_ok` = `openat` calls that succeeded on an outside path; `writes` = opens with `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC`.

    case                    ceiling          distinct syscalls open_ok open_fail write
    A-abs-gitfile           ceiling=d              41      233      54        24     0
    A-abs-gitfile           ceiling=parent(d)       41      233      54        24     0
    B-rel-gitfile           ceiling=d              44      233      54        24     0
    B-rel-gitfile           ceiling=parent(d)       44      233      54        24     0
    H-symlink-in-d          ceiling=d              40      221      54        24     0
    H-symlink-in-d          ceiling=parent(d)       40      221      54        24     0
    E-linked-worktree       ceiling=d              46      378      75        25     0
    E-linked-worktree       ceiling=parent(d)       46      378      75        25     0
    D-alternates-out        ceiling=d              14       79      15        16     0
    D-alternates-out        ceiling=parent(d)       14       79      15        16     0
    D2-rel-alternates-out   ceiling=d              14       79      15        16     0
    D2-rel-alternates-out   ceiling=parent(d)       14       79      15        16     0
    C-in-d-gitfile          ceiling=d               1       24       0         0     0
    C-in-d-gitfile          ceiling=parent(d)        1       24       0         0     0
    F-alternates-in-d       ceiling=d               1       24       0         0     0
    F-alternates-in-d       ceiling=parent(d)        1       24       0         0     0
    G-discovery             ceiling=d              45      252      55        26     0
    G-discovery             ceiling=parent(d)        1        7       0         0     0
    G-discovery             ceiling=unset          45      246      55        26     0

Set identity of outside paths between the two ceiling settings (§5): **identical for every gitfile/alternates/
worktree case** (A 36, B 38, H 34, E 40, D 14, D2 14, C 1, F 1 — same sets). Only the discovery control differs.

For the honest controls C and F the single outside path is one `newfstatat` of `d`'s **parent directory** — the
ancestor stat the fence docstring already lists as accepted residue — and **zero** content opens. So the
discriminator is not "does git touch anything outside d" (it stats ancestors always) but "does git **open** a
file outside d".

## 5. The ceiling does not bound pointer resolution (verbatim)

    $ cd <S>/work/cases/G-discovery/d
    $ env GIT_CEILING_DIRECTORIES=<S>/work/cases/G-discovery/d git rev-parse --git-dir
    <S>/work/cases/G-discovery/.git                                    # ceiling == cwd does not bound discovery
    rc=0
    $ env GIT_CEILING_DIRECTORIES=<S>/work/cases/G-discovery git rev-parse --git-dir
    fatal: not a git repository (or any of the parent directories): .git
    rc=128                                                             # ceiling at d's PARENT does bound discovery
    $ env -u GIT_CEILING_DIRECTORIES git rev-parse --git-dir
    <S>/work/cases/G-discovery/.git
    rc=0

git(1) states the reason (`GIT_CEILING_DIRECTORIES`): "a list of directories that Git should not chdir up into
while looking for a repository directory … **It will not exclude the current working directory** or a GIT_DIR
set on the command line or in the environment." The ceiling is a *discovery* bound; a `.git` **file** found at
`d` is not discovery, it is a pointer, and dereferencing it is not a chdir up. Measured: with the strictest
ceiling (`d`'s parent, which makes discovery fail outright) every gitfile/alternates case produces the same
outside-read set as with `ceiling=d` — A 54 successful opens, B 54, H 54, E 75, D 15, D2 15, unchanged.
Corroboration: the lane's own builder already pins `GIT_CEILING_DIRECTORIES=str(root.parent)`
(`plans/round44_c1_verify.py:278`), so this is the setting the honest population is built under — and it does
not stop a pointer from leaving `d`.

## 6. Verbatim syscalls that leave `d` (pid prefix stripped; `<S>` substituted; otherwise unedited)

Absolute gitfile, store outside (A) — `cat-file`:

    openat(AT_FDCWD<<S>/work/cases/A-abs-gitfile/d>, "<S>/work/cases/A-abs-gitfile/store.git/HEAD", O_RDONLY) = 3<<S>/work/cases/A-abs-gitfile/store.git/HEAD>
    openat(AT_FDCWD<<S>/work/cases/A-abs-gitfile/d>, "<S>/work/cases/A-abs-gitfile/store.git/config", O_RDONLY) = 3<<S>/work/cases/A-abs-gitfile/store.git/config>
    openat(AT_FDCWD<<S>/work/cases/A-abs-gitfile/d>, "<S>/work/cases/A-abs-gitfile/store.git/refs/heads/main", O_RDONLY) = 3<<S>/…/store.git/refs/heads/main>
    openat(AT_FDCWD<<S>/work/cases/A-abs-gitfile/d>, "<S>/work/cases/A-abs-gitfile/store.git/objects/d4/a8f0693cc9…", O_RDONLY|O_CLOEXEC) = 3<…>

Relative gitfile (B) — git passes the **unresolved literal** and the kernel resolves it outside:

    openat(AT_FDCWD<<S>/work/cases/B-rel-gitfile/d>, "<S>/work/cases/B-rel-gitfile/d/../store.git/HEAD", O_RDONLY) = 3<<S>/work/cases/B-rel-gitfile/store.git/HEAD>
    access("<S>/work/cases/B-rel-gitfile/d/../store.git/objects", X_OK) = 0
    openat(AT_FDCWD<<S>/work/cases/B-rel-gitfile/d>, "<S>/work/cases/B-rel-gitfile/store.git/config", O_RDONLY) = 3<<S>/work/cases/B-rel-gitfile/store.git/config>

Symlink inside `d`, literal pointer entirely inside `d` (H) — the sharpest line of the probe:

    openat(AT_FDCWD<<S>/work/cases/H-symlink-in-d/d>, "<S>/work/cases/H-symlink-in-d/d/lnk/HEAD", O_RDONLY) = 3<<S>/work/cases/H-symlink-in-d/store.git/HEAD>
    readlink("<S>/work/cases/H-symlink-in-d/d/lnk", "<S>/work/cases/H-symlink-in-d/store.git", 85) = 84
    openat(AT_FDCWD<<S>/work/cases/H-symlink-in-d/d>, "<S>/work/cases/H-symlink-in-d/store.git/config", O_RDONLY) = 3<<S>/work/cases/H-symlink-in-d/store.git/config>

Linked worktree, common dir outside (E) — `config`:

    newfstatat(AT_FDCWD<<S>/work/cases/E-linked-worktree/d>, "<S>/work/cases/E-linked-worktree/main/.git/worktrees/d/commondir", {st_mode=S_IFREG|0644, st_size=6, ...}, AT_SYMLINK_NOFOLLOW) = 0
    openat(AT_FDCWD<<S>/work/cases/E-linked-worktree/d>, "<S>/work/cases/E-linked-worktree/main/.git/worktrees/d/commondir", O_RDONLY) = 3<<S>/…/main/.git/worktrees/d/commondir>
    openat(AT_FDCWD<<S>/work/cases/E-linked-worktree/d>, "<S>/work/cases/E-linked-worktree/main/.git/config", O_RDONLY) = 3<<S>/work/cases/E-linked-worktree/main/.git/config>

Relative alternates landing outside (D2) vs the honest in-`d` shape (F), same `cat-file`:

    openat(AT_FDCWD<<S>/work/cases/D2-rel-alternates-out/d/lane>, "<S>/work/cases/D2-rel-alternates-out/altstore/.git/objects/34/98db8794aee390e7e541b503df5e3833aeccae", O_RDONLY|O_CLOEXEC) = 3<…/altstore/.git/objects/34/98db8794…>
    openat(AT_FDCWD<<S>/work/cases/F-alternates-in-d/d/lane>,        "<S>/work/cases/F-alternates-in-d/d/main/.git/objects/34/98db8794aee390e7e541b503df5e3833aeccae", O_RDONLY|O_CLOEXEC) = 3<…/d/main/.git/objects/34/98db8794…>

Content, not just metadata (marker strings exist only outside `d`; `cat-file`/`config` read them through the
pointer; `marker_in_d=none` for A/B/H/D/D2/C/F — for E the checked-out worktree file carries the blob text, so
E's content proof is its **config** marker, which exists only in `…/main/.git/config` outside `d`):
`config --get probe.marker` → `probe.outside.cfg.7f3a91` (A, B, H),
`probe.outside.maincfg.7f3a91` (E); `cat-file -p HEAD:marker.txt` → `STORE_ONLY_BLOB_7f3a91` (A, B, H, D, D2, E).
For C and F the same blob (`cat-file` above) resolves **inside** `d` — that is the whole difference.

**Zero writes outside `d` in all 9 cases × 2 ceiling settings** (`writes=0`); the escape is read-only
(path disclosure / object disclosure), matching the fence's threat model.

## 7. What this grounds for the S2 repair — and one supplementary check

Three failure modes of a name-based rule, each measured:

1. **Prefix test on the literal** fails on B: **30 of 233** outside syscalls carry a path string that starts
   with `d` + `/` (`…/d/../store.git/HEAD`) and resolve outside. git emits *both* forms in one run (literal and
   resolved), so a trace-prefix check returns "inside" for ~1 in 8 outside syscalls.
2. **Lexical containment of the pointer** fails on H: `gitdir: lnk` is inside `d`, has no `..`, no absolute
   path, and the fd target is `<S>/…/store.git/HEAD`. Only `realpath()` (which follows the symlink) sees it.
3. **One resolution base for all pointers** fails on D2 vs B: a gitfile's path is relative to the **gitfile's
   directory**; an alternates entry is relative to the **objects directory** (`lane/.git/objects`). D2's
   `../../../../altstore/.git/objects` is exactly one `..` further than F's `../../../main/.git/objects`, whose
   store is in `d` — same bytes shape, opposite verdict.

Supplementary (adjacent to the item, no claim on the repair's own evidence): the landed S2 fence
(`plans/fixture_fence.py` = `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`, read as a blob
from the clone at `6db0279`), run on these nine fixtures through its own `breach()`:

    A-abs-gitfile            lane=.     REFUSE: ../store.git resolves outside the fixture
    B-rel-gitfile            lane=.     REFUSE: ../store.git resolves outside the fixture
    H-symlink-in-d           lane=.     REFUSE: lnk is a symlink
    E-linked-worktree        lane=.     REFUSE: ../main/.git/worktrees/d resolves outside the fixture
    D-alternates-out         lane=.     REFUSE: .git/objects/info/alternates names a store outside the fixture
    D2-rel-alternates-out    lane=lane  REFUSE: lane/.git/objects/info/alternates names a store outside the fixture
    C-in-d-gitfile           lane=.     ADMIT
    F-alternates-in-d        lane=lane  ADMIT
    G-discovery              lane=.     REFUSE: --lane '.' is not a repository inside the fixture

i.e. on the measured escape set the landed containment leg separates honest from hostile exactly where the
probe says the discriminator sits, and it does so without a git child. The frozen base fence
(`05d5fe03…`, imported from the clone at `3b02d57`) refuses all nine, including C and F, by name
(`.git is a file (gitdir redirect), not a directory` / `.git/objects/info/alternates present (object-store
redirect)`) — the over-refusal C1 has to repair.

Probe defect found and fixed in my own fixture env (recorded so nobody repeats it): a builder that inherits the
host environment picks up `XDG_CONFIG_HOME=/home/vgpnk/.config`, whose `rerere.enabled=true` makes `git commit`
write `MERGE_RR` + `rr-cache/` into every store, which is *not* a plain-init entry. First pass of the S2 check
therefore refused C/F for `MERGE_RR is not a plain-init entry`. Fix: `GIT_CONFIG_GLOBAL=/dev/null` and
`XDG_CONFIG_HOME` pointing into scratch, per command. The lane's own builder already sets both
(`plans/round44_c1_verify.py:270-271`), so the frozen population is not affected; only my probe was.

## 8. Limits

- One host, one git (`2.56.0`). Pointer-following behaviour is old and documented, but the syscall *shapes*
  (which files are probed in what order, e.g. `MERGE_HEAD`, `rebase-apply`, `commondir`) are version-specific.
- Not observed: `io_uring`, `mmap`-only reads (all reads here are `openat`+`read` on the traced tree), paths
  reached through already-open fds created before `execve`, or reads performed by a helper the trace filter
  would attribute to another process (none occurred: every command was a single `git`).
- Two ceiling values plus unset; no bind mounts, no chroot/namespace sandbox. `GIT_DIR`/`--git-dir` on the
  command line was never used (git(1) excludes those from the ceiling too, and the fence's argv shape forbids it).
- C and F are faithful echoes of the lane's `n21`/`n22` builder shapes, not byte-identical to the pinned
  population rows; fixture identity belongs to `plans/honest50/population.txt` and was not re-derived here.
- No claim is made about the S2 fence's admission decisions beyond the nine fixtures listed; that evidence
  belongs to the C1 scored run and the seats that own it.
- The probe measures reads; it does not evaluate whether a *repaired* fence reproduces git's resolution for
  every pointer kind (`commondir`, `refs/replace`, `FETCH_HEAD` were not probed — they are not gitfile pointers).

## 9. Risks / blockers

- **Risk for S2 (informational):** a containment leg that normalises lexically (`normpath`) instead of resolving
  (`realpath`) passes A/B/D/D2 but fails H and any symlinked intermediate; a leg that resolves but uses `d` as
  the base for an alternates entry fails D2-in-reverse (a hostile relative alternates under the honest shape).
- No blocker. Lane was read-only for this seat; the only lane writes are other seats' (uncommitted-at-start
  `57adce4a…` fence, now committed at `6db0279`).

## 10. Retained evidence and cleanup

- All evidence a reader needs is quoted in this report (counts, verbatim syscall lines, fence verdicts, ceiling
  transcript). Per-command strace logs (114 files), `work/probe-summary.json`, `work/final-table.txt`,
  `work/driver-summary.json`, `work/s2-verdicts.txt` lived under `<S>/work`.
- Scratch removed before yield: `rm -rf /fast/scratch/hyaku/kengaku-r50/R50C1LabratProbe` (verified absent).
  No file in the lane, no sibling repo, no `/tmp` residue; nothing committed, pushed or stashed.

**VERDICT: escape confirmed real (git, not theory).** With cwd in `d` and `GIT_CEILING_DIRECTORIES` bounding
discovery, git 2.56.0 resolves a `.git` gitfile, a `commondir`, and an `objects/info/alternates` entry that name
a store outside `d`, and reads it: 54/54/54/75/15/15 successful outside-`d` opens for A/B/H/E/D/D2, 0 writes,
6/6 commands rc=0 per escaping case, marker content returned from outside `d`. The honest echoes (C, F) produce
zero outside-`d` opens — the discriminator is the **resolved target**, not the literal, not the ceiling. The
repair must therefore resolve every pointer from git's own base and check containment on the resolved path;
refusing the shape by name (base fence) over-refuses, and trusting the literal admits the escape.
