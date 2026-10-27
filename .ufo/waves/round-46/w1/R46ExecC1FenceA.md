# R46ExecC1FenceA — C1 variant A (allowlist) fence

Seat: executor, wave 1. Base: `plans/fixture_fence.py` @ `64ba8385` (digest `ac65c032…5eda6`, identical at the
stage-1 freeze tip `fd4129eb`). Delivered: `fixture_fence.py` in this seat's subdir, sha256
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`, 574 lines, stdlib only
(`os`, `pathlib`, `re`, `stat`), contract `breach(d, argv, tool) -> str|None` unchanged. Tested only with
`plans/round45_c1_verify.py` and the `R45Ho*` modules; no draft of `plans/round46_c1_verify.py` was run or opened,
and nothing under `.ufo/waves/round-46/w1/` was opened except this seat's own subdir. No tool installed.

## Design (variant A — refuse unless proven plain)

Round 45 named attack classes (`commondir`, `alternates`, `[include]` text) and nine held-out modules spelled the
same escapes differently. Variant A inverts the burden: classify every byte the decision depends on, refuse the rest.

1. `d` itself: `lstat`, no follow; must be a real directory.
2. argv: the tool's exact option shape (`order` = 3 exact pairs, `anchor` = exact option set). Every value is a
   **lexical** path check — no NUL, no CR/LF, no `{...}` placeholder, `os.path.normpath` containment in `d`; no
   `resolve()`, so nothing behind a symlink is ever consulted.
3. one `os.walk` of `d` (`followlinks=False`): any symlink, FIFO, socket, device or second hard link refuses; every
   `.git` that is a real directory is collected, a `.git` file refuses. Caps: 200 000 entries, 64 repos.
4. each store is classified entry by entry against what `git init` + commits writes: `HEAD`, `ORIG_HEAD`,
   `COMMIT_EDITMSG`, `config`, `description`, `hooks/` (`*.sample` only), `index`, `info/exclude` only,
   `logs/` (`HEAD` or `refs/heads|tags/<safe>`), `objects/` (2-hex dirs of 38-hex regular single-link files,
   `info/` must be empty, `pack/` only pack-file suffixes), `refs/heads|tags` (40-hex, `..`-free names),
   `packed-refs` (strict line grammar). Anything else in `.git` refuses — `commondir`, `gitdir`, `modules`,
   `worktrees`, `config.worktree`, `alternates`, `FETCH_HEAD`, `shallow` are all "not a plain-init entry".
5. `config` is parsed line by line: any `\r`, any byte ≥ 0x80 (BOM), any section but `[core]`, any key outside
   `{repositoryformatversion=0, filemode, bare=false, logallrefupdates, ignorecase, precomposeunicode, symlinks}`,
   and any line the parser does not fully classify refuses. This is what closes the CR/BOM/`includeIf`/
   `attributesFile`/`worktreeConfig` family without naming any of them.
6. `--lane` must be one of the collected repositories.
7. **no git child is started.** Measured, every git subcommand resolves the worktree path component-wise and
   `newfstatat`s `d`'s ancestors — paths under the build scratch outside `d` (below). The store classification is
   the proof; `--show-toplevel`/`--git-common-dir` have nothing left to add because the redirects they would catch
   are refused by name.

## Evidence

All runs through the frozen envelope (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh
"$S/env" …`), scratch `S=/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceA`, `--shared` clone verified
`git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`. Receipts in `R46ExecC1FenceA/`.

### 1. Round-45 counter — `PREDICATE C1 pass` (`final-counter.out`)

```
ENVELOPE start 02:04:43 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceA
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 02:05:03 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Command: `envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/w" --jobs 8`.
Per-module refusal reasons (same receipt), one per held-out class:

```
f1 `.git is a file (gitdir redirect)` · f2 `config line b'worktree = …' is not a plain key=value`
f3 `order argv is not the contract shape` · f4/f10 `config section [include] is not allowlisted`
f5 `objects/info/alternates present` · f6 `--lane …/sub is not a repository inside the fixture`
f7 `commondir is not a plain-init entry` · f8 `config section [extensions] is not allowlisted`
f9 `config core.bare must be false`   — every one `opens=0`
```

### 2. Held-out modules under the r45 driver (`final-heldout.out`; `drive_heldout.py`)

Driver imports the counter's own `build_module`/`run_fence` (builder + bwrap + strace), fence copy from the clone.

| module | fixtures | admitted | read | hung | outside opens | verdict |
|---|---|---|---|---|---|---|
| h1_cr_include.py | 2 | 0 | 0 | 0 | 0 | clean |
| h2_includeif_cond.py | 9 | 0 | 0 | 0 | 0 | clean |
| h3_bom_symlink.py | 4 | 0 | 0 | 0 | 0 | clean |
| h4_controls.py (control) | 3 | 0 | 0 | 0 | 0 | clean |
| link_hostiles.py | 5 | 0 | 0 | 0 | 0 | clean |
| argv_env.py | 3 | 0 | 0 | 0 | 0 | clean |
| g1_cdrel.py | 1 | 0 | 0 | 0 | 0 | clean |
| g2_gitfile.py | 1 | 0 | 0 | 0 | 0 | clean |
| g3_wtmeta.py | 1 | 0 | 0 | 0 | 0 | clean |
| g4_cdrel_hidden.py | 1 | 0 | 0 | 0 | 0 | clean |
| configkeys.py | 1 | 0 | 0 | 0 | 0 | clean |

`HELDOUT modules=10 clean=10 leaked=0 read=0 hung=0`, `CONTROLS modules=1 verdicts=['clean']`.

Refusing leg per module: h1/h2 bare CR in `config`; h3 BOM (2) and bare CR (2); link_hostiles `.git/objects`
symlink, `.git` symlink, worktree `claims.md` symlink, object hardlink (`more than one hard link`), `inc2` symlink;
argv_env placeholder / NUL / shape; g1 `commondir`; g2 `.git` file; g3 `worktrees`; g4 `modules`; configkeys
`attributesFile` line. h4's three plain `[includeIf "…"]` controls: `section header … is not plain`.

### 3. Self-audit, 12 fixtures authored by this seat (`final-selfattack.out`, `selfattack.py`)

`SELFATTACK fixtures=12 admitted=0`. Each is a plain repo plus one non-plain shape:

```
sa-info-commitgraph   BREACH  objects/info/commit-graph present (object-store redirect)
sa-core-subsection    BREACH  section header b'[core "x"]' is not plain
sa-symbolic-ref       BREACH  heads/side is not a 40-hex ref
sa-head-escape        BREACH  .git/HEAD is not a plain branch HEAD
sa-packed-escape      BREACH  .git carries a ref name git does not write
sa-index-symlink      BREACH  .git/index is a symlink
sa-hook-real          BREACH  pre-commit is not a hook sample
sa-bare-truthy        BREACH  config core.bare must be false
sa-nlink-worktree     BREACH  lane/claims.md has more than one hard link
sa-dir-symlink-out    BREACH  lane/linked is a symlink
sa-objects-direct-file BREACH .git/objects/notadirectory is not a directory
sa-logs-escape-name   BREACH  outside has a name git does not write
```

Two of these were **found by the audit and fixed**, not merely re-tested: `packed-refs` still used the loose
`REF_PATH` (no `..` rule) and `logs/` accepted any `refs/…` shape — both now share `_ref_name_ok`/exact log paths.

### 4. No outside-`d` path, measured over the whole file-syscall set (`final-paths.out`, `drive_paths.py`)

Same sandbox and fixtures, `strace -f -y -e trace=%file` (open + stat + access + readlink + execve), counting every
path under the build scratch root outside `d`:

```
AUDIT honest   battery42/a_class.py  verdict='ADMIT'  outside_path_refs=14  {'4 newfstatat':6,'4 openat':4,'4 mkdir':1}
AUDIT honest   battery43/o_excuse.py verdict='ADMIT'  outside_path_refs=14  {'4 newfstatat':6,'4 openat':4,'4 mkdir':1}
AUDIT refusal  f10_laneinclude.py    verdict='BREACH' outside_path_refs=14  {'4 newfstatat':6,'4 openat':4,'4 mkdir':1}
AUDIT refusal  f5_alternates.py      verdict='BREACH' outside_path_refs=14  {'4 newfstatat':6,'4 openat':4,'4 mkdir':1}
```
Every one of them is pid 4 (the counter's harness) and names only `harness.py`, `fence/fixture_fence.py`, the
`__pycache__` probe and the EROFS `mkdir` — the counter's own B3 exception; `outside-path pids: ['4']`. With the
git legs removed the git children (previously pids 5–9, `6 newfstatat` each) are gone entirely.

### 5. Why the git legs are gone (measurement, `gitleg.sh` / `gitleg2.sh`)

Four legs, `-C <repo>`: `rev-parse --show-toplevel`, `--absolute-git-dir`, `--git-common-dir`,
`cat-file -t HEAD:<path>` — each `anc_stats` includes `"…/layout"`, `d`'s parent. Same with `cd <repo>` and no `-C`
(`--show-toplevel`, `--git-common-dir`): git resolves the worktree component-wise and stats every ancestor of `d`.
Under the frozen round-46 counter's B3/B5 legs ("any open outside `d` under the whole scratch root counts … stat-family
… count like opens") a git-calling fence registers outside-`d` reads on **every** fixture, honest ones included — so
the fence cannot both call git and advertise that it names nothing outside `d`. Flag for the L1/stage-2: this
measurement constrains the new counter as much as the fence.

## Limits (named, not hidden)

1. `.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*`, `pack/*` are admitted by name + size, contents not
   validated. The tool run behind the fence reads none of them for a path; a future reader would have to.
2. `git` is never executed (deviation from the base's legs, argued above). Cost: a store that satisfies the
   allowlist but that git itself would reject (e.g. an object file with a valid name and no content) is admitted;
   the downstream tool's own git then fails, outside the fence's contract.
3. Narrowing beyond today's honest batteries — all measured 104/104, but each would need an L1 decision if a future
   honest fixture adopts it: `objects/info` must be empty (no `git gc`/`commit-graph`), no `refs/remotes|notes|bisect`,
   no `FETCH_HEAD`/`MERGE_HEAD`/mid-merge or mid-rebase state, no linked worktrees, no hardlinked files (so no
   `git clone --local` shape), and only `[core]` in `.git/config` (a fixture that stores `user.email` in config is
   refused; the builder pins identity by env, which is why nothing honest trips it).
4. TOCTOU: the proof is only a proof because the run is read-only (`bwrap --ro-bind / /`). Outside such a sandbox
   the fence is a check, not a lock.
5. No child process, no io_uring, no writes: the round-45 bypass families B1 (log erasure), B4 (stdout verdict),
   B6 (blocked opens), B7 (io_uring) have no surface here — the fence never owns the log, never prints the verdict
   and never starts a process.
6. Cost: one `scandir`+`stat` per entry, whole `config` read (cap 1 MiB), every ref name read (cap 200 B each).
   `ENTRY_CAP` 200 000 keeps a pathological tree bounded; measured wall time for the full 114-fixture counter is
   ~20 s on this host.

## Risks for the L1

- Landing is a whole-file replacement of `plans/fixture_fence.py`; no other lane file was touched, the round-45
  counter passes at the clone tip (no-harm), and the file's digest must be what stage 2 pins if the new counter pins
  the fence (it should not — the fence is the work).
- The r46 counter's REFUSALS set is `plans/refusals46/` (f1–f10 + converted held-out). Every shape it names is
  refused here with `opens=0`; the converted `R45Ho*` shapes were run directly (table §2).
- Wave-2 sealed modules: the classes that survive this design are the named limits (§Limits 1–3), not path escapes.

## Host safety / cleanup

No tool installed (nothing needed; `strace 7.2`, `bwrap 0.13.1`, `python3 3.14.8` already present). Every
measurement ran through the round-46 envelope; each receipt ends
`exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. No write outside
`$S`, this seat's subdir and the lane clone under `$S`. Scratch removed with
`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46ExecC1FenceA "$S"` after the receipts
were copied here.

VERDICT: fenceA-r45-pass-yes-heldout-refused-10/10
