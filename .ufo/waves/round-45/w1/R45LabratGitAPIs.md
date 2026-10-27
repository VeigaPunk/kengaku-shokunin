# R45LabratGitAPIs — git's actual behaviour, measured (round 45 wave 1, build)

Seat: `R45LabratGitAPIs` (executor/labrat, leaf). Lane repo (read-only to me):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Scratch:
`/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs` (deleted at the end; see §12).
No lane file was written; no git/jj mutation ran in the lane; nothing was installed
(tooling authorization: nothing needed — `git 2.56.0`, `/usr/bin/strace`, `/usr/bin/bwrap` were already present).

**Purpose.** Answer the seven questions the L1 sent for `plans/fixture_fence.py` — in scratch, never the lane — and state,
for each measured behaviour, **which fence leg it demands**. The fence contract under test (`plans/round45_c1_verify.py`
counter docstring): `breach(d, argv, tool) -> str | None`, judged over the 10 frozen `plans/refusals45/` modules
(`clean` = refused **and** no successful/never-returned open outside `d`) and the 104 honest fixtures of battery42+43+44
(all `ADMIT`, zero outside opens).

## 0. Envelope ledger (QUALITY Q32) — every probe ran under `claims/envelope.sh`

`envelope.sh` gives `--ro-bind /home/vgpnk /home/vgpnk`, so `/home/vgpnk/.local/bin` is read-only for every run, and it
prints a **content** digest of that directory before/after. All 14 runs: `before == after`, `exit=0`, no `INVALID`.

| run | probe | ENVELOPE start | ENVELOPE end (digest) |
|---|---|---|---|
| 1 | `probe.sh` (P1–P11) | 23:27:09 | 23:27:11 exit=0 `c263b11afb1cccf6` → `c263b11afb1cccf6` unchanged |
| 2 | `probe2.sh` (Q1–Q10) | 23:28:18 | 23:28:21 exit=0 `c263b11afb1cccf6` unchanged |
| 3 | `probe3.sh` (R1–R7) | 23:29:57 | 23:30:14 exit=0 `c263b11afb1cccf6` unchanged |
| 4 | `probe4.sh` (R8–R15) | 23:31:19 | 23:31:21 exit=0 `c263b11afb1cccf6` unchanged |
| 5 | `probe5.sh` (S1–S5) | 23:32:12 | 23:32:14 exit=0 `c263b11afb1cccf6` unchanged |
| 6 | `probe6.sh` (T1–T6) | 23:32:50 | 23:33:02 exit=0 `c263b11afb1cccf6` unchanged |
| 7 | `probe7.sh` (U1–U4) | 23:33:58 | 23:34:00 exit=0 `c263b11afb1cccf6` unchanged |
| 8 | `probe8.sh` (V1–V4) | 23:34:46 | 23:34:48 exit=0 `c263b11afb1cccf6` unchanged |
| 9 | `probe9.sh` (W1–W5) | 23:37:16 | 23:37:18 exit=0 `e396f23e40a69201` unchanged |
| 10 | `probe10.sh` (X1–X5) | 23:38:20 | 23:38:21 exit=0 `e396f23e40a69201` unchanged |
| 11 | `probe11.sh` (Y1–Y5) | 23:39:17 | 23:39:19 exit=0 `e396f23e40a69201` unchanged |
| 12 | `probe12.sh` (Z1–Z4) | 23:41:10 | 23:41:11 exit=0 `e396f23e40a69201` unchanged |
| 13 | `probe13.sh` (A1–A6) | 23:42:35 | 23:42:37 exit=0 `e396f23e40a69201` unchanged |
| 14 | `probe14.sh` (S1–S6, counter-rule simulation) | 23:44:47 | 23:44:49 exit=0 `e396f23e40a69201` unchanged |

**Out-of-band observation (host safety).** The digest itself changed **between** run 8 and run 9, from
`c263b11afb1cccf6` to `e396f23e40a69201`. It was not my runs (each bracket is unchanged) and not my writes (I never
touched a PATH directory). Cause, by mtime: `find /home/vgpnk/.local/bin -newermt '2026-10-26 23:30'` →
`2026-10-26+23:36:46 f OpenBot-0.51.1-x86_64.AppImage` (a new appimage landed, 296 MB, at 23:36:46, i.e. between the two
runs). **No measurement below is invalidated** — every envelope bracket is `unchanged` — but the L1 should know another
seat/process was writing that directory mid-wave.

## 1. Does `git config --local --no-includes` skip `[include]` while `rev-parse` still parses it?

**Answer: `--no-includes` does NOT prevent the include target from being opened.** It suppresses the *values* of the
include from the config set, but git's **repository setup read** of `.git/config` (which happens before the subcommand's
own `--no-includes` read) follows includes and opens the target. `rev-parse` opens it too — as does every other git call.

P1 (`probe-out.txt`), repo whose `.git/config` carries `[include] path = …/p1/out1.cfg`:

```
--- p1 config --local --no-includes --get-regexp ^include(if)?\.
include.path /fast/scratch/.../probe/p1/out1.cfg            [rc=0]
--- p1 config --local --no-includes --get-regexp
OPENED .../p1/out1.cfg : YES
    33    openat(AT_FDCWD<.../p1/d>, "/…/p1/out1.cfg", O_RDONLY) = 4
--- p1 rev-parse --show-toplevel
OPENED .../p1/out1.cfg : YES
--- p1 status --porcelain
OPENED .../p1/out1.cfg : YES
```

R1 isolates **who** opens it — the same command run with a non-repo cwd does not open anything:

```
--- r1 (A) NON-repo cwd + --file copy --no-includes --list   → OPENED : NO
--- r1 (C) repo cwd     + --file copy --no-includes --list   → OPENED : YES
```

V3 shows every subcommand does it (`rev-parse --show-toplevel`, `--absolute-git-dir`, `--git-common-dir`,
`config --local --no-includes --get-regexp`, `status --porcelain`, `cat-file -t HEAD`, `log --oneline -1`, and even
`GIT_DIR=<repo>/.git` with an outside cwd: all `FIRED (target opened)`). Q3 confirms `--no-includes` keeps the *values*
out (`user.email` → no such value) while the file is still opened.

Also measured: `git config --file <path>` does **not** follow includes unless `--includes` is passed (X1:
`--file standalone --list` → `not opened`; `--file standalone --includes --list` → `OPENED`, and it printed
`user.email=OUTSIDE-X1@invalid`).

**Demands:** the include/`includeIf` **static text scan leg must run before any git call** in that repo. There is no git
flag that makes the call safe. (This is exactly the mechanism behind the frozen control's f4/f10 `READ` verdicts.)

## 2. Does `extensions.worktreeConfig=true` + `config.worktree` reach `rev-parse` / status?

**Answer: yes — and `--local` scope cannot see it, so a git-based include check misses it entirely.**

P2/Q7/R12/U4, repo with `extensions.worktreeConfig true` and `.git/config.worktree` = `[include] path = …/out.cfg`:

```
--- p2 config --local --no-includes --get-regexp include      [rc=1]      ← blind
--- p2 config --worktree --get-regexp include
include.path /…/p2/out2.cfg                                   [rc=0]
--- p2 config --list --show-origin
file:.git/config.worktree	include.path=/…/p2/out2.cfg
file:/…/p2/out2.cfg	user.email=OUTSIDE-P2@invalid      ← the include WAS followed
--- p2 rev-parse --show-toplevel   → OPENED /…/p2/out2.cfg : YES
--- p2 status --porcelain          → OPENED /…/p2/out2.cfg : YES
```

W3 bounds the trigger: with `.git/config.worktree` present but **without** the extension, the file is ignored —
`config --list --show-origin` lists only `.git/config`, `--worktree` returns `[rc=1]`, and `rev-parse` opens nothing.
W3b: extension set with no `config.worktree` file → nothing read, no error.

**Demands:** the static scan must cover **`.git/config*` (all of them)**, and must refuse `extensions.worktreeConfig`
and/or a `config.worktree` carrying `[include*]` — a `git config --local --no-includes '^include(if)?\.'` leg cannot
(the round-44 fence's exact hole → f8 `LEAKED`).

## 3. Does a relative `commondir` resolve against the git dir?

**Answer: yes — against the **git dir** (the directory holding the `commondir` file), not the cwd and not the work-tree
root.** Both `storeA` and `../storeA` were tested against a decoy at cwd level.

Q1 (`probe2-out.txt`), `d/.git/commondir` = `../storeA`, decoys at `<d>/storeA` (bare) and `<cwd>/storeA` (bare):

```
--- q1 rev-parse --git-common-dir
/…/q1/d/storeA                                   ← git dir ../storeA == <d>/storeA
--- q1 config --local --list --show-origin
file:/…/q1/d/storeA/config  core.bare=true       ← the common dir's config is the repo config
--- q1 git-dir storeA marker   → IN-GITDIR-STORE
--- q1 cwd storeA marker       → IN-CWD-STORE
```

R5 (`storeA`, no `..`) → `--git-common-dir` = `<d>/.git/storeA`; Y5 repeats it. R10: a relative commondir that resolves
nowhere (`../../outside/store.git` from `d/lane/.git`) makes git fail — `fatal: Invalid path '…/r10/d/outside'`,
`[rc=128]` — i.e. git resolves it against the git dir and then refuses a non-existent store.

**Demands:** a commondir leg must (a) refuse `.git/commondir` outright (the frozen design says exactly that: "no
module-built repo needs one"), and (b) if it ever resolves one, resolve it **against the git dir**, never the work tree.

## 4. Does `GIT_CEILING_DIRECTORIES` stop discovery above a directory that is itself a repo's parent?

**Answer: yes, and the semantics are "the ceiling directory itself is not entered"** — so a repo **at** the ceiling is
invisible. Ceilings must be **absolute**; relative entries are silently ineffective.

P4, repo at `P`, cwd `P/sub/d`:

```
--- no ceiling                                  → /…/p4/P                      [rc=0]
--- ceiling=P  (the repo root itself)           → fatal: not a git repository  [rc=128]
--- ceiling=P/sub                               → fatal: not a git repository  [rc=128]
--- ceiling=P/sub/d (the cwd itself)            → /…/p4/P                      [rc=0]
--- ceiling=D4 (parent of the repo root)        → /…/p4/P                      [rc=0]
--- ceiling=/                                   → /…/p4/P                      [rc=0]
--- ceiling="P" RELATIVE from cwd P/sub/d       → /…/p4/P                      [rc=0]  ← ignored
--- multi-entry "A:B" (one entry = Q)           → fatal: not a git repository  [rc=128]
--- ceiling="P/" (trailing slash)               → fatal: not a git repository  [rc=128]
```

R3 (the f6 shape: repo **at** `d.parent`), with strace:

```
--- r3 NO ceiling: does it open d.parent/.git/config ?      → OPENED : YES
--- r3 ceiling=d.parent: does it open d.parent/.git/config ?→ OPENED : NO  (rc=128)
--- r3 ceiling=d.parent, git -C <d.parent> cat-file …       → OPENED : YES  ← -C names the repo, ceiling irrelevant
```

Two consequences: a ceilinged probe is **safe but blind** (it cannot see the ancestor repo — rc=128, indistinguishable
from "no repo"), and an **unbounded** probe sees it but **reads its config** (an outside open). The ceiling also does not
protect the repo's *own* include: X2 shows the include target opened with `ceiling=d.parent` too.

**Demands:** the "`.git` **above** d" leg must be a **pure filesystem stat walk** of d's ancestors, and every git probe
must carry an **absolute** ceiling at `d.parent`. Never ask git to detect the ancestor repo.

## 5. Does an `[includeIf "gitdir:…"]` trigger on a fixture path?

**Answer: yes — and the pattern language makes several forms trigger for a fixture's own git dir.** Matching follows
git-config(1): the pattern is a glob against the **git dir path**; a relative pattern gets `**/` prepended; a trailing
`/` gets `**` appended; a leading `./` means "relative to the directory of the config file".

Q2/R6/Y2 (absolute):

```
pattern = /…/lane/.git     (exact, no trailing slash) → FIRED
pattern = /…/lane/.git/    (trailing slash)           → not fired
pattern = /…/lane/.git*    (glob)                     → not fired
```

R6/R11 (relative, one pattern per fresh repo):

```
pattern = lane/.git   → FIRED      (git-config(1): becomes **/lane/.git → matches anywhere)
pattern = lane/.git/  → not fired  (becomes **/lane/.git/** — the git dir itself has no trailing component)
pattern = lane        → not fired
pattern = lane/       → FIRED
pattern = ./lane/.git → not fired  (./ = the config file's directory, i.e. the .git dir itself)
pattern = ../lane/.git→ not fired
```

S1: the relative form fires regardless of cwd (four different cwds, same repo). Two distinct reasons a probe shows "not
fired": (a) the cwd was **not a repository** at all, so no config was read — X3 c1/c3/c5, Y1 `b_cwd`, where git prints
`fatal: not a git repository`; (b) the pattern itself does not glob-match, e.g. Y1 `b_tp` `../repo/.git` from a cwd
*inside* the repo — `**/../repo/.git` is not normalised, so it never matches. Only (b) is information about the pattern.

Also: `[includeIf "onbranch:master"]` fires and opens its target (S2), so the static scan must key on the **section
name**, not on a particular condition keyword. T3: `config --local --no-includes` opens the includeIf target as well.
Z3: the includeIf key is at least *listed* by `--local --no-includes --get-regexp '^include(if)?\.'` as
`includeif.gitdir:<pattern>.path` — but only after the file is already open.

**Demands:** refuse **any** `[include]`/`[includeIf]` section in any `.git/config*` by text scan; do not try to evaluate
the pattern.

## 6. Does `rev-parse --git-common-dir` resolve a commondir?

**Answer: yes, and it is the one probe that exposes the f7 shape** — while `--show-toplevel` and `--absolute-git-dir`
stay inside `d`.

P6/Q8/R9, `d/lane/.git/commondir` = absolute path to an outside store:

```
--- p6 rev-parse --git-common-dir        → /…/p6/store/.git      (the outside store)
--- p6 rev-parse --absolute-git-dir      → /…/p6/d/lane/.git      (inside d)
--- p6 rev-parse --show-toplevel         → /…/p6/d/lane           (inside d)
--- p6 rev-parse --git-dir               → .git                   (RELATIVE)
--- r9 rev-parse --absolute-git-dir      → OPENED /…/store/.git/config : YES
--- r9 rev-parse --show-toplevel         → OPENED /…/store/.git/config : YES
--- r9 config --local --list --show-origin → file:/…/store/.git/config core.bare=false
```

Two traps measured: **(a)** with no commondir, `--git-common-dir` and `--git-dir` print a **relative** `.git`
(X4/Y3/R4) — use `--path-format=absolute` (X4 gives the absolute form); **(b)** every git call on a commondir repo
**opens the outside store's config** (R9), so detection must be static.

Bonus: a legitimate linked worktree puts `commondir` at `.git/worktrees/<name>/commondir` (content `../..`), **never**
at `.git/commondir` (Z1) — so "refuse `.git/commondir`" does not refuse honest worktrees, while "refuse any file named
commondir" would.

## 7. Extra measurements the leg design needs

**rc != 0 semantics (f9 shape).** P7/U2: `core.bare=true` → `--show-toplevel` `[rc=128]` ("this operation must be run in
a work tree"), but `--absolute-git-dir` `[rc=0]` (`<d>/.git`), `--git-common-dir` `[rc=0]` (`.git`),
`--is-inside-work-tree` `[rc=0]` false. An empty `.git` dir or a plain dir → **all** probes `[rc=128]` "not a git
repository" (R14/U2). So the rule "rc != 0 from a store/lane probe is a breach" needs the pairing: *`--absolute-git-dir`
rc=0 with anything else rc!=0* = "repo exists, git cannot describe it" = breach; *all rc!=0* = not a repo (the tool's
own setup error, not the fence's business).

**core.worktree.** P8/R13: absolute outside value → `--show-toplevel` answers the **outside** path (inside-d toplevel is
not enough); **relative** value → *every* git call fails `[rc=128]` `fatal: cannot chdir to '../wt'` — including
`config --local --no-includes --get core.worktree` (V4/W2), so a git-based read of core.worktree can return nothing.
Base of a relative value: W2b `../wt` from `<d>/.git` → `<d>/wt` (git dir base). V4 shows the raw text
(`worktree = ../wt`) is always readable.

**FIFO include (f4).** R2: with `.git/config` including a FIFO, `timeout 5 git config --local --no-includes --get-regexp`
→ `[rc=124]`, and `git rev-parse --show-toplevel` → `[rc=124]`; a **ceiling does not help** (T5 `[rc=124]`). From a
non-repo cwd with `--file <copy>` the same reads return rc=0 (no block). So the block is the setup read.

**`.git` as a FILE / SYMLINK (f1).** R8: `.git` containing `gitdir: <outside store>` → `--absolute-git-dir` = the outside
store and the outside store's `.git/config` is **opened** by rev-parse (YES). W1: `.git` as a **symlink** to an outside
git dir → identical, and `os.path.isdir('.git')` is `True` while `os.path.islink` is `True` — a mode test must use
`lstat`/`islink`, never `is_dir` alone.

**alternates (f5).** P10/Q4: `objects/info/alternates` → a plain `rev-parse` attempts `openat(<alternate>/objects/info/alternates)`
(outside `d`; `ENOENT` in the probe, so it is a failed open and the counter ignores failed opens). A successful open of
the alternate store is possible once objects are needed. Static refusal is the cheap leg.

**Which filesystem calls count as an "open" for the counter.** A1–A6 (probe13) + probe14 simulation of
`round45_c1_verify.py`'s own `OPEN_RE`/`DONE_RE`/scratch rule:

```
--- a1 python os.stat(outside.txt) + os.stat(outside/.git)   → newfstatat only, no openat of the target
--- a2 python read_text(outside.txt)  → openat(…, "/…/outside.txt", O_RDONLY|O_CLOEXEC) = 3   ← COUNTS
--- a3 python os.listdir(outside dir) → openat(…, "/…/probe13", O_RDONLY|…|O_DIRECTORY) = 3    ← COUNTS
--- a5 python Path.resolve(outside)   → newfstatat / readlink only
--- a6 python islink + resolve        → newfstatat(SYMLINK_NOFOLLOW) / readlink only
```

## 8. Counter-rule simulation on a realistic `root/fx` layout (probe14)

`root/fx/mod/f000` = an ancestor repo, `d` = `root/fx/mod/f000/d`, an include target at
`root/fx/mod/f000/inc.cfg` (all under the counter's scratch, all outside `d`). The counter's own counting rule applied
verbatim:

| candidate fence strategy | `outside_opens` |
|---|---|
| **stat-only** ancestor walk (`.git` stat per ancestor) | **0** |
| `os.listdir` per ancestor | **3** (the ancestor dirs themselves are opened) |
| `git -C d rev-parse --show-toplevel` **with** `ceiling=d.parent` | **0** |
| `git -C d rev-parse --show-toplevel` **without** a ceiling | **3** (first: `…/f000/.git/HEAD`) |
| `git -C d/lane rev-parse --show-toplevel`, no ceiling | **3** |
| text scan of `.git/config*` for `[include` | **0** |
| `git config --local --no-includes --get-regexp '^include(if)?\.'` | **2** (first: `…/inc.cfg`) |
| `git rev-parse --show-toplevel` in the same include repo | **1** |
| `git --git-dir=d/lane/.git --work-tree=d/lane rev-parse` | **1** |

The stat-only walk did find the ancestor (`ancestor_git=…/f000/.git`), and git's own answer from the same `d` is
`…/f000` — i.e. the tool would adopt a repo above `d`, which is why the fence must refuse it.

## 9. Behaviour inventory → fence legs

`B<n>` = behaviour measured above (evidence in the receipts); `L<n>` = the leg it demands.

| # | behaviour (probe) | leg demanded |
|---|---|---|
| B1 | any git call with cwd/`--git-dir` in a repo reads that repo's `.git/config` **and follows its includes** (P1,Q3,R1,V3,S5,S5b,S6) | L4, **L12 (ordering)** |
| B2 | `--no-includes` drops include *values* but not the **open**; it still lists the `include.path` key (P1,Q3,Z4) | L4 (no git-based include detector) |
| B3 | `git config --file X` ignores includes unless `--includes`; with `--includes` it opens them (X1) | L4 |
| B4 | the include open only happens with repo context (cwd or `GIT_DIR`), not from a plain `--file` read (R1,S3) | L4 |
| B5 | a FIFO include blocks **every** git call in the repo (rc=124), ceiling irrelevant (R2,T5) | L4 before L9, L9 timeout |
| B6 | relative `include.path` resolves against the **.git dir** (`../x` ⇒ `.git/../x`, still inside `d`) (T1,T2,Y4) | L4, L7 |
| B7 | `includeIf gitdir:` fires for an absolute exact git-dir path (no trailing slash); trailing slash does not (Q2,Y2,R6) | L4 (refuse any includeIf) |
| B8 | relative `gitdir:` patterns get `**/` prepended ⇒ match a fixture anywhere; `./` is relative to the config file's dir (R6,R11,S1,X3,Y1) | L4 |
| B9 | `includeIf onbranch:` also fires and opens (S2) | L4 |
| B10 | `extensions.worktreeConfig=true` + `.git/config.worktree` include is followed by rev-parse/status but is **invisible** to `--local` (P2,Q7,R12,U4) | L3 |
| B11 | without the extension the worktree config is ignored entirely (W3,W3b) | L3 |
| B12 | relative `commondir` resolves against the **git dir**; a dead target ⇒ rc=128 `Invalid path` (Q1,R5,Y5,R10) | L2 |
| B13 | `--git-common-dir` resolves a commondir to the outside store while `--show-toplevel`/`--absolute-git-dir` stay in `d` (P6,Q8,R9) | L2, L10 |
| B14 | a linked worktree's `commondir` is at `.git/worktrees/<n>/commondir`, not `.git/commondir` (Z1) | L2 (narrow key) |
| B15 | plain `--git-dir`/`--git-common-dir` print a **relative** `.git`; `--path-format=absolute` gives the absolute path (X4,Y3,R4) | L10, L11 |
| B16 | `GIT_CEILING_DIRECTORIES` excludes the ceiling dir itself ⇒ a repo **at** the ceiling is invisible (P4,U3,R3) | L8, L9 |
| B17 | ceilings must be absolute; relative entries are ignored; multi-entry and trailing slash work (P4,U3) | L9 |
| B18 | without a ceiling, discovery from `d` ascends into the ancestor repo **and opens its config** (R3,Q5,probe14) | L8 |
| B19 | a bare repo answers `--absolute-git-dir` rc=0 but `--show-toplevel` rc=128; an empty/absent repo answers rc=128 everywhere (P7,U2,R14) | L11 |
| B20 | absolute `core.worktree` outside `d` is what `--show-toplevel` answers; a **relative** one fails every git call rc=128, including the config read (P8,R13,V4,W2,W2b) | L7, L11 |
| B21 | `.git` as a FILE (`gitdir:`) or SYMLINK to an outside git dir ⇒ `--absolute-git-dir`/`--git-common-dir` = outside store, and its config is opened; `isdir` is True for the symlink (P9,R8,W1) | L1 |
| B22 | `objects/info/alternates` makes git attempt an open under the alternate store (P10,Q4) | L5 |
| B23 | stat/`resolve`/`islink` are `newfstatat`/`readlink` (not counted); `read_text` and `listdir` are `openat` (counted) (A1–A6) | L8 (stat-only), L12 |

**Legs (k = 12):**

- **L1** pure-fs: walk `d`; a `.git` that is a **file** or a **symlink** ⇒ refuse (B21). Mode test via `lstat`.
- **L2** pure-fs: a `.git/commondir` **file** ⇒ refuse (B12–B14).
- **L3** pure-fs: `extensions.worktreeConfig` in `.git/config`, or a `.git/config.worktree` carrying an include ⇒ refuse (B10,B11).
- **L4** pure-fs: **text** scan of every `.git/config*` for `[include` / `[includeIf` ⇒ refuse (B1–B9; the only safe detector, and the only one that cannot block on a FIFO).
- **L5** pure-fs: `.git/objects/info/alternates` present ⇒ refuse (B22).
- **L6** pure-fs: any symlink under `d` resolving outside `d` ⇒ refuse (B21).
- **L7** pure-fs: `core.worktree` from the **text**, resolved against the git dir, must be `d` (B20,B6).
- **L8** pure-fs: **stat-only** walk of `d`'s ancestors for `.git` (file or dir) up to the module build root ⇒ refuse (B16,B18,B23).
- **L9** git-call: bounded `pin_git` — **absolute** ceiling at `d.parent`, timeout, no stdin, never a named path outside `d` (B16,B17,B5).
- **L10** git-call: `rev-parse --path-format=absolute --git-common-dir` must be inside `d` (B13,B15).
- **L11** git-call: `--absolute-git-dir` inside `d`; `--show-toplevel` inside `d` **when `--absolute-git-dir` succeeded**; rc!=0 in that pairing = breach (B19,B20).
- **L12** ordering: **every** L1–L8 leg before the first git call, and the first refusing leg ends the decision (B1,B23; probe14 shows the difference is 0 vs 1–3 outside opens).

## 10. What this explains about the seven frozen contradictions (`control-c1-fence-r44.txt`)

| module | frozen verdict | mechanism measured here |
|---|---|---|
| f7 commondir | `LEAKED` | B13: r44 checks only `--show-toplevel`/`--absolute-git-dir`; both stay in `d`; `--git-common-dir` (the tell) is never asked |
| f8 worktreecfg | `LEAKED` | B10: `--local --no-includes --get-regexp '^include(if)?\.'` is blind to the worktree-scoped include (rc=1) |
| f9 nodescribe | `LEAKED` | B19: every check is guarded `rc == 0`; a bare repo's `--show-toplevel` rc=128 reads as "nothing to see" |
| f1 gitfile | `READ` (opens=6) | B21: `lane_breach` runs git **before** `repo_breach`'s "`.git` is a file" test; the setup read opens the outside store's config |
| f6 above-d | `READ` (opens=3) | B18/B16: unbounded lane discovery opens the ancestor's `.git/config`; a ceiling would have hidden the repo entirely |
| f10 lane-include | `READ` (opens=4) | B1/B2: the include is detected, but only after the setup read opened it |
| f4 fifo | `READ` (opens=1) | B5: r44's `pin_git` blocks on the FIFO (its 30 s timeout yields "git hung"), and the never-returned open of the FIFO counts |

The single ordering fix (L12) plus the six static legs cover all seven without touching the honest set. Measured over
`plans/battery42|43|44`: no `core.bare`, no `--bare`, no `commondir`, no `include.path`, no `separate-git-dir`, no
`alternates`, no `git worktree add`, no `extensions.worktreeConfig`, no `config.worktree` — the only `bare` hits are the
word in prose and one fixture directory named `d/"bare"` (a normal repo, `battery43/o_alt.py:122`). Every repo is built
at `d` or `d/<sub>`: `ctx.init(...)` appears 82× as `d` (20) or `d/<name>` (62), never above `d` (including
`battery43/a_alt.py:30` `ctx.init(d / sub)`, whose `sub` is only `""` or `"repo"`).

## 11. Risks / open questions for the L1 (not decided here)

1. **Bound of the ancestor walk (L8).** The fence receives only `d`, `argv`, `tool` — it cannot know the module build
   root. Measured: in the counter's layout (`plans/round45_c1_verify.py:build_module`, `dest = root/fx/<module>`,
   `d = dest/fNNN`) the ancestor repo used by f6 sits at **exactly `d.parent`** (`ctx.init(pathlib.Path(d).parent)`).
   So the minimum bound is `d.parent`, and a fixed small depth cap (or a stop at the first ancestor that is not
   writable / not scratch-owned) is the fence author's call. Walking to `/` risks refusing every honest fixture if the
   build root ever sits inside a repo (the counter already forbids `--work` inside the lane, so today it does not).
   Stat-only is required either way (B23).
2. **`.git`-as-file refusal also refuses legitimate linked worktrees** (B21/Z1). No honest fixture uses one, but the held-
   out attack set may test an honest worktree — the L1 may prefer "refuse `.git` file whose `gitdir:` target is outside
   `d`" over "refuse any `.git` file". Both refuse f1; the narrow form is the safer calibration.
3. **`rc != 0` is not a blanket breach** (B19): plain non-repo dirs answer rc=128 to everything, and honest fixtures whose
   lane is not a repo would be wrongly refused. The pairing in L11 is the discriminator I could measure.
4. **`--git-common-dir` needs `--path-format=absolute`** (B15) or the comparison is against a relative `.git`.
5. **`config.worktree` without the extension is inert** (B11): refusing the file's mere presence is stricter than git's
   behaviour but cannot hurt the honest set (no honest fixture has one).

## 12. Cleanup

Scratch `/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs` (probe trees `probe*` + strace logs) was removed with the
project guard **after** the receipts were copied:

```
$ python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45LabratGitAPIs "$S"
DELETE path=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs resolved=…/R45LabratGitAPIs bytes=3956345 size=3.8MiB
$ ls -d /fast/scratch/hyaku/kengaku-r45/.ROUND-ROOT-SENTINEL   → present (untouched)
```

`probe13.sh` (A1–A6) is reproduced in the receipts directory because it was deleted with the scratch tree otherwise.

## 13. Receipts (in `.ufo/waves/round-45/w1/R45LabratGitAPIs/receipts/`)

| file | sha256 |
|---|---|
| `probe-out.txt` (P1–P11) | `db4697c5f1d392480756b83d99dc14ec5cdf87a13f5f81432e2f35dcf232fd8d` |
| `probe2-out.txt` (Q1–Q10) | `8be91f31a12042a1c63f772c755697d813a1430567ec58a40b3e3a4319e26154` |
| `probe3-out.txt` (R1–R7) | `75b707acc1e466ba2d2a0b9fdb90ad21dcf250abe9b8f7294c926fcf817c479a` |
| `probe4-out.txt` (R8–R15) | `8ec0efb1e6824aa7b06bb94e514320e8e66176bcad39dab848fa4fe6ab1bf799` |
| `probe5-out.txt` (S1–S5) | `a4ec14c27b77f72f6cc511afd66db7d14f23e1e35f3c755b62c6c490295f0418` |
| `probe6-out.txt` (T1–T6) | `4b69427b3ad10534a4aeda9e960492775e180e3bc6afa51b2fc7e42565c18161` |
| `probe7-out.txt` (U1–U4) | `c0bc3d5ab87726688d10754812311da0c0135e3009031d5f3f3f50e1c4794495` |
| `probe8-out.txt` (V1–V4) | `b70a99d80124b38524cf11fd87667708c7b14c8a49de794cccee38d4da055f65` |
| `probe9-out.txt` (W1–W5) | `b5d2ada6b81242b9cd7535265a5d15e8ff9aefa50c3da03057794f00b8e0cc1c` |
| `probe10-out.txt` (X1–X5) | `eb30ae357db5eb2658db02194bda8c5edc55057a4ea8652e94d4cadc5b092954` |
| `probe11-out.txt` (Y1–Y5) | `52cb077a00ac418ad2336a2256612cb6aa0c0cced9ef1e9bd63a8f3c5ab24708` |
| `probe12-out.txt` (Z1–Z4) | `af77de4bbd75bf8ea08c99254dd91e24bfed550c9814cd94da39af5ee3b9fd17` |
| `probe13-trimmed.txt` (A1–A6; full 228 K trace sha256 `df8aae4ee8ac2eb335706d66ac7519e9f26208c30df9b4d0ebe85069c3222345`) | in-file header |
| `probe14.sh` + `count.py` + `listdir.py` (counter-rule simulation) | scripts; output quoted in §8 |

All probe scripts (`probe.sh`, `probe2.sh` … `probe14.sh`, plus probe14's helpers `count.py`/`listdir.py`) are in the same
directory, so each table row above can be re-run verbatim with
`claims/envelope.sh <scratch> bash <script>`.

VERDICT: git-behaviours-verified-23-leg-mapped-12
