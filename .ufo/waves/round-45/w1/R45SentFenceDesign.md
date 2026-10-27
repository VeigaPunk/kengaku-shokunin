# R45SentFenceDesign — hostile vector census beyond f1–f10 (round 45, wave 1)

Seat: sentinel, leaf. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Nothing in the lane was written:
no edit to `plans/`, `corpus/`, `SCORECARD.md`, `LOG.md`, or `.ufo/waves/round-45/claims/`; every fixture,
clone-free git probe and strace run lived in `/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign` and every run was
bracketed by `claims/envelope.sh`. I wrote **no fence** (assignment: enumerate, no implementation); the probes are
fixture builders + git invocations only. No tool installed or upgraded.

Frozen inputs read only: `plans/round-45-claims.md`, `plans/round45_c1_verify.py` (docstring = the rule),
`plans/round44_c1_verify.py` (the five legs the r44 control fence composes), `plans/refusals45/f1–f10`,
`.ufo/waves/round-45/claims/control-c1-fence-r44.txt`, `.ufo/waves/round-44/wave/R44SentinelFences.md`.

## Method

Every row is measured in the same shape the counter uses: fixture dir `d = WORK/<id>/fx/f000`, a side tree
`WORK/<id>/fx/side` (outside `d`, inside the build scratch — the counter's own definition of "outside"), each git
call under `strace -f -qq -y -e trace=open,openat,openat2,creat,execve`, classified against `d` exactly as
`run_fence` does (`plans/round45_c1_verify.py:186-252`). Probe env is the counter's pinned-scope env
(`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `core.fsmonitor=false`, `core.hooksPath=/dev/null`,
`gpg.program=/bin/true`, `log.showSignature=false`, `HOME=/nonexistent`) — the r44 `GIT_PINS` a `pin_git`-shaped
leg carries — plus a no-pins variant where the difference matters. `git 2.56.0`, python 3.14, bwrap 0.13.1.

Frozen legs (labels used below), from the seat assignment's *Required design (frozen)* and the counter docstring
`:16-53`:

| label | frozen leg |
|---|---|
| W | walk every directory under `d` |
| G-FILE | a `.git` that is a **file** is refused, whatever it contains |
| G-SYM | a `.git` that is a **symlink** is refused |
| SYM | any symlink under `d` resolving outside `d` is refused |
| CD | any `.git/commondir` is refused |
| CW | `[include]` / `[includeIf]` / `extensions.worktreeConfig` text scan of any `.git/config*` |
| ALT | any `objects/info/alternates` is refused |
| ABOVE | a `.git` found above `d` (ancestors up to the module build root) is refused |
| GIT | bounded `pin_git` store/lane probe; `rc != 0` is a breach, never "clean" |

## Bottom line

**38 rows enumerated** (35 parse-reachable vectors, 1 vector blocked by environment only, 1 blocked by git, 1 not
a vector). **15 are caught by no frozen leg**; 5 are caught only if an implementation detail is right
(case-insensitive scan, section-aware line scan, pin env, toplevel comparison); 3 more are caught only if the
symlink leg is ordered **before** the config scan and the git legs; 12 are covered outright.

Four of the 15 uncovered are *calibration-relevant even though nothing is read outside* (rows 31–34): they make
the fence raise or block, and the counter counts a fence `ERROR` as an admitted fixture (`plans/round45_c1_verify.py:291`
`n_admit = sum(v in ("ADMIT", "ERROR") …)`) and a block as `HUNG` at 120 s (`:103`). Two more read outside while
the fence's path opens stay inside `d` (hardlinks), so the counter's metric is blind to them.

Severity of the 15 uncovered (exploit path, evidence and smallest remediation per class below):

| severity | rows | why |
|---|---|---|
| **HIGH** | 31–34 | admissible/`HUNG` contradiction with no git vector; deterministic; four one-line fixture edits |
| **HIGH** | 35 | outside store is read *inside* the order leg's own `cat-file`, which then returns `rc=0` |
| **HIGH** | 10, 11 | git executes an outside binary (textconv / `diff.external`) during a plausible "lane probe" |
| **HIGH** | 36 | `--lane <outside>` is admitted by a filesystem-only fence, and the r45 build contract no longer rejects it |
| **MEDIUM** | 9, 12, 15 | outside files read by `check-attr`/`status`/`ls-files`/`log`/`shortlog` if the fence runs them |
| **MEDIUM** | 27, 28 | content authored outside `d` is consumed with zero outside-path opens (metric-invisible) |
| **LOW/MEDIUM** | 20 | latent: needs a command run at the outside worktree (argv-shaped) |
| **LOW** | 16 | gated on `protocol.file.allow` coming from the fence's env (repo scope ignored) |

## The table

| # | vector | does git parse it? (command → proof) | frozen leg | verdict |
|---|---|---|---|---|
| 1 | `includeIf "gitdir:<d>/lane/"` + outside path | `git config --get user.email` → `OUTSIDE@invalid`, 1 outside open (`03/…--config-user-email.log:23`) | CW | covered |
| 2 | same with a **non-matching** `gitdir:` | not applied (`local@invalid`, 0 opens) but the text is present | CW (refuse on text, not on effect) | covered — a runtime-only refusal admits the fixture |
| 3 | `includeIf "onbranch:master"` + outside path | applied by `config --get`, `status`, `log`, `rev-parse` → `OUTSIDE@invalid`, 1 open each (`05/…`) | CW | covered |
| 4 | `[include] path = ../../../side/inc.cfg` (**relative**) | `git config --get user.email` → `RELOUTSIDE@invalid`; `openat(…, ".git/../../../side/inc.cfg") = 4` (`r6--relative-include.log:11`) | CW (refuse any `path` key, not only absolute ones) | covered |
| 5 | `[include] path = ~/inc-tilde.cfg` | expands to `$HOME`; with `HOME=/nonexistent` no read, with a writable HOME `TILDE-OUTSIDE@invalid` (`06`) | CW | covered |
| 6 | `[include] path = $HOME/…` / `${HOME}/…` | **not expanded**: `git config --get-all include.path` prints the literal (`07`) | — | not a vector |
| 7 | `[InClUdE]` **mixed case** | parsed: `config --get user.email` → `SPELL-OUTSIDE@invalid`, 1 outside open (`27c`) | CW **only if case-insensitive** | **conditional** — a case-sensitive scan refuses only after a git child read it = `READ` |
| 8 | `[include] path = X` on **one line** (header + key same line) | parsed: `SPELL-OUTSIDE@invalid`, 1 outside open (`27c`) | CW only if the scan is section-aware/token-based | **conditional** — a `^\s+path\s*=` scanner misses it |
| 9 | `core.attributesFile = <outside>` | `git check-attr -a`, `status --porcelain`, `ls-files -o` open `/fx/side/attrs` (`08`: 1, 3, 1 opens); `rev-parse` does not | none | **UNCOVERED** |
| 10 | row 9 + `diff.<d>.textconv = <outside>` | `git diff` opens `/fx/side/attrs` (7 lines) and **executes** `/fx/side/textconv.sh` twice, marker written (`25e`) | none | **UNCOVERED** (code execution outside `d`) |
| 11 | `[diff] external = <outside>` (no attributes file needed) | `git diff` → `execve("/fx/side/dext.sh", …)` (`r6--diff-external.log:21`) | none | **UNCOVERED** (code execution outside `d`) |
| 12 | `core.excludesFile = <outside>` | `status --porcelain`, `ls-files -o --exclude-standard` open it (`08`) | none | **UNCOVERED** |
| 13 | `core.hooksPath = <outside>` | with pins: 0 opens, no exec; without pins (`status`, `update-index --refresh`) → `execve("/fx/side/hooks/post-index-change")` (`09:96`) | GIT only via the r44 `GIT_PINS` env (`core.hooksPath=/dev/null`) | **conditional** — the counter's fence env has no pins (`:186`) |
| 14 | `core.fsmonitor = <outside script>` | without pins `status`/`update-index` → `execve("/fx/side/fsmon.sh")` (`09:27`); with pins `core.fsmonitor=false` wins | GIT only via pins | **conditional** |
| 15 | `mailmap.file = <outside>` | `git log --use-mailmap` opens it (1), `git shortlog -sne` opens it (2) (`10`) | none | **UNCOVERED** (no probe reads it today) |
| 16 | `.gitmodules url = file://<outside>` + gitlink | `submodule update --init` reads the outside store (6+ opens, `cloned=true`) **only** when the env sets `protocol.file.allow=always`; repo-scope `protocol.file.allow=always` is ignored (`fatal: transport 'file' not allowed`) (`11c`/`11e`) | none | **UNCOVERED**, transport-gated |
| 17 | `objects/info/alternates` **relative** entry | `cat-file -t <borrowed>` → `blob`, 2 outside opens (`12b`) | ALT (refuses any alternates file) | covered |
| 18 | `objects/info/alternates` is a **symlink** to an outside file | `cat-file -t` → `blob` (`29`) | SYM (before ALT/GIT) | covered |
| 19 | `.git/commondir` **relative** → outside store | `rev-parse --git-common-dir`, `cat-file` → `blob`, 6 outside opens (`13b`) | CD (refuse any commondir) | covered |
| 20 | `.git/worktrees/<n>/config.worktree` include outside; `gitdir` names an outside worktree | main-repo probes: 0 outside opens (`rev-parse`, `worktree list`, `config --get`); commands run **at the outside worktree** open `side/inc.cfg` and answer `WT-OUTSIDE@invalid` (`14b`) | CW's glob is `.git/config*` → **misses** `.git/worktrees/<n>/config.worktree` | **UNCOVERED** (latent; needs argv/worktree pointing outside) |
| 21 | `.git` **file** with a relative target `gitdir: ../../../side/gitdir` | accepted: `rev-parse --absolute-git-dir` = `/fx/side/gitdir-relative` (`16c`) | G-FILE | covered |
| 22 | `.git` file `gitdir : ` (space before colon), `gitdir:` no space, `GITDIR:`, leading newline | all `fatal: invalid gitfile format` (`16c`) | G-FILE (presence, no parsing) | covered |
| 23 | `.git` file with trailing spaces | `fatal: gitfile does not point to a valid repository` (`16c`) | G-FILE | covered |
| 24 | `.git` is a **symlink** to an outside git dir | followed: `rev-parse` rc=0, 3 outside opens; `os.walk` lists `.git` **in dirs**, and reading `lane/.git/config` resolves to `side/gitdir/config` (`17`, `17b`) | G-SYM/SYM **ordered before** CW | covered **only if ordered first** |
| 25 | `.git/config` itself a **symlink** outside | `config --get user.email` → `SYMLINK-CFG-OUTSIDE@invalid`, 2 outside opens (`18`) | SYM before CW | covered only if ordered |
| 26 | `.git/objects` (whole dir) a **symlink** to an outside store | `cat-file -t` → `blob`, 2 outside opens (`23`) | SYM before GIT | covered only if ordered |
| 27 | **hardlinked** object files | `cat-file -t` → `blob`; `st_nlink=2`; **0 outside opens** (`19`) | none | **UNCOVERED**, metric-invisible |
| 28 | **hardlinked** `.git/config` to an outside file | `config --get user.email` → `HARDLINK@invalid`; `st_nlink=2`; 0 outside opens (`36`) | none | **UNCOVERED**, metric-invisible |
| 29 | `core.worktree = ../../../side/wt` (**relative**) | git resolves against the **gitdir**: rc=0, `--show-toplevel` = `/fx/side/wt` (`02e`); r44's leg resolves against the **repo root** | GIT **if the store/lane probe compares `--show-toplevel`** | conditional — a gitdir-only probe misses it |
| 30 | `GIT_DIR` / `GIT_WORK_TREE` / `GIT_OBJECT_DIRECTORY` in env | redirects discovery: `GIT_DIR=<side>/store/.git git -C lane rev-parse` = 3 outside opens (`15`) | — | **not fixture-reachable**: `run_fence` passes a literal 5-key env (`:186`) — but any fence that forwards `os.environ` exposes it |
| 31 | `.git/config` replaced by a **FIFO** | `git rev-parse` **TIMEOUT** at 6 s; a plain `open('.git/config')` blocks past 5 s (`22b`) | none (f4 is a FIFO *include*, different file) | **UNCOVERED** → `HUNG` at 120 s |
| 32 | `.git/config` a **directory** | `read_text()` → `IsADirectoryError`; fence would exit `ERROR` (`26`) | none | **UNCOVERED** → counter counts `ERROR` as admitted |
| 33 | `.git/config` **chmod 000** | `PermissionError`; `git rev-parse` rc=128 (`26`) | none | **UNCOVERED** → `ERROR` → admitted |
| 34 | `.git/config` **invalid UTF-8** | `UnicodeDecodeError`; `git` itself still runs (`26`) | none | **UNCOVERED** → `ERROR` → admitted |
| 35 | `extensions.partialClone` + `remote.origin.promisor=true` + `remote.origin.url=file://<outside>` | `cat-file -t <absent blob>` → `blob` after **16 outside opens** of `<side>/store/.git/{HEAD,config,objects/…,pack}` (`21b`) | none | **UNCOVERED** — lazy fetch happens inside the store probe, before any `rc` check |
| 36 | argv token absolute **outside `d`** (`--lane /fx/side/outside-lane`) | `git -C <token> rev-parse` = outside; `round45_c1_verify.py:167` validates only `isinstance(t, str)` — the r44 `path_ok` guard is **absent** from the r45 build contract | none | **UNCOVERED** — fence must refuse any argv token that resolves outside `d`; counter-side contract gap |
| 37 | repo **above `d`** whose `.git/config` includes an outside file | bare `git -C d/lane config --get user.email` → `ABOVE-OUTSIDE@invalid`, toplevel = `fx`; with `GIT_CEILING_DIRECTORIES=fx` the same call returns rc=1 and the toplevel probe rc=128 (`31`) | ABOVE (filesystem) **and** GIT's ceiling + `rc != 0` rule | covered |
| 38 | `.git/HEAD` a symlink to an outside file | `fatal: not a git repository`; 0 outside opens (`35`) | (SYM would also fire) | not a vector |

## The five classes that matter most for wave-2 hostile authors

### A. Fence-crash layouts (rows 31–34) — cheapest contradictions, no git vector at all
`plans/round45_c1_verify.py:291` turns a fence exception into `LEAKED`:
`n_admit = sum(v in ("ADMIT", "ERROR") for …)`. So a fixture that makes the fence **raise** is a contradiction even
though it never reads outside `d`. Measured on one fixture each (same uid as the fence, inside the build sandbox):

```
26 note: {"config-as-dir":"IsADirectoryError","config-chmod0":"PermissionError",
          "git-on-chmod0":128,"config-nonutf8":"UnicodeDecodeError",
          "config-fifo":"fifo-nonblock-open-ok (plain read_text would block)"}
22b note: naive open = BLOCKED >5s ; git rev-parse rc=TIMEOUT
```

*Exploit path*: `.git/config` as FIFO / directory / mode 000 / non-UTF-8 bytes. A `CW` scan that calls
`path.read_text()` on `.git/config*` blocks (FIFO → `HUNG`, 120 s × every fixture) or raises (`ERROR` → admitted).
*Smallest remediation*: open every probed path `O_RDONLY|O_NONBLOCK|O_NOFOLLOW`, `fstat` and require `S_ISREG`
before reading, decode with `errors="replace"`, and wrap the whole `breach()` body so any `OSError` becomes a
refusal string, never an exception.

### B. Hardlinks (rows 27–28) — content from outside `d`, zero outside opens
```
19: cat-file -t <hardlinked blob> -> blob ; config --get user.email -> HARDLINK-CFG-OUTSIDE@invalid ; opens outside d = 0
36: config --get user.email -> HARDLINK@invalid ; st_nlink = 2 ; opens outside d = 0
19 note: nlink(config)=2 nlink(object)=2; inode-shared with outside file
```
The counter counts only opens whose *resolved path* is under the scratch outside `d`; a hardlink resolves inside
`d`. The fixture therefore hands the tool content it never built, and the metric cannot see it.
*Smallest remediation*: during `W`, refuse any regular file under `d` with `st_nlink > 1` (and any `.git/config`,
`.git/objects/**`, `.git/refs/**`, `.git/index` with `st_nlink > 1`); report the inode count in the reason.

### C. Promisor lazy fetch (row 35) — the store probe itself reads outside
```
21b cat-file-foreign-blob rc=0 out=16 :: 'blob'
paths: side/store/.git/HEAD, side/store/.git/config, side/store/.git/objects/b4/5230…, side/store/.git/objects/pack
```
`extensions.partialClone=origin` + `remote.origin.promisor=true` + `remote.origin.url=file:///…/side/store`
make `git cat-file -t <absent>` fetch the object from the outside store **and succeed**, so no `rc != 0` fires.
The r44 legs also admit it (`r44_legs 21b-promisor ADMIT`). It is triggered by the very call the order leg makes
(`cat-file -t HEAD:<claims>`), and it also opens the outside store's `config`.
*Smallest remediation*: refuse `extensions.partialClone` / any `remote.<n>.promisor=true` in the pre-git text scan
(same case-insensitive config reader as `CW`), and run every git child with `GIT_NO_LAZY_FETCH=1` and
`GIT_TERMINAL_PROMPT=0`.

### D. Attribute / diff / ignore / mailmap / hook execution family (rows 9–16)
Measured reads and executions of outside paths by commands a "lane probe" plausibly runs:

```
08: check-attr out=1, status out=3, ls-files-others out=1 (side/attrs, side/ign)
25e: openat(… lane>, "/fx/side/attrs") = 3, then execve("/fx/side/textconv.sh") ×2, marker=true
r6:  execve("/fx/side/dext.sh", ["…","a.txt","/tmp/git-blob-…"]) ; marker=true
09:  execve("/fx/side/fsmon.sh") and execve("/fx/side/hooks/post-index-change") under no-pins; 0 under GIT_PINS
10:  log --use-mailmap out=1 ; shortlog out=2
```
The frozen design pins only `core.fsmonitor`/`core.hooksPath`/`gpg.program`/`log.showSignature` (via the r44
`GIT_PINS` a `pin_git` brings) — and only if the fence actually adopts that env: the counter hands the fence a
5-key env (`:186`), so a fence that builds its own env from `os.environ` executes outside binaries.
*Smallest remediation*: keep every git child under a fixed env that adds `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_COUNT` pins for `core.fsmonitor=false`, `core.hooksPath=/dev/null`,
`gpg.program=/bin/true`, plus `GIT_NO_LAZY_FETCH=1`; and refuse repo config keys
`core.attributesFile|core.excludesFile|mailmap.(file|blob)|diff\.…(textconv|external)|filter\.…(clean|smudge)|core.pager|core.editor|sequence.editor`
in the same text scan (all are "read or execute something the fixture names").

### E. argv outside `d` (row 36) and the worktree-metadata glob (row 20)
`round45_c1_verify.py:167` accepts any string argv:
`and all(isinstance(t, str) for t in argv) and d.is_dir():` — the r44 `path_ok` guard is gone. A wave-2 module
can return `["--lane", "<absolute path outside d>", …]` and the counter will hand it to the fence. Nothing in
the frozen leg list resolves argv tokens, so a filesystem-only fence admits it (`r44_legs 24-argv-outside BREACH`,
but only because `lane_breach` runs — a leg the r45 fence is not required to carry).

Row 20 is the same shape one level down: `.git/worktrees/<n>/config.worktree` is outside `CW`'s `.git/config*`
glob, and the main-repo probes do not read it (0 opens), so it passes every leg while carrying a config file that
`git` applies when a command runs at the outside worktree (measured: `WT-OUTSIDE@invalid` at the outside worktree).
*Smallest remediation*: (a) refuse any argv token that, resolved against `d`, leaves `d`; (b) make `CW` a walk of
every file whose name is `config` or `config.worktree` under any `.git` in `d` (including `.git/worktrees/*/` and
`.git/modules/*/`), not a glob.

## Ordering requirements the design must state (rows 24–26)

The three symlink rows are only clean if `SYM`/`G-SYM` run **before** `CW` and **before** `GIT`:
`os.walk` lists a symlinked `.git` in `dirs` (`17b`, first probe), and `open("lane/.git/config")` resolves to
`side/gitdir/config` — a `CW` scan placed before the symlink leg turns a clean refusal into `READ`.

## Rows the frozen legs do catch, with the leg that catches them

Relative alternates (17) → ALT; symlinked alternates (18) → SYM; relative commondir (19) → CD; every `.git`-as-file
form (21–23) → G-FILE; includeInif/include/relative/tilde (1–5) → CW; repo above `d` (37) → ABOVE **and** the
ceiling: with `GIT_CEILING_DIRECTORIES=fx`, `git -C d/lane config --get user.email` returns rc=1 and
`rev-parse --show-toplevel` rc=128, so the `rc != 0` rule fires before any include is parsed.

`r44_legs` (the r44 fence applied to the same fixtures, `vectors3.json:r44_legs`) admits what the r45 design's new
filesystem legs are meant to catch: `13b commondir-relative ADMIT`, `14b worktrees ADMIT`, `19 hardlink ADMIT`,
`21b promisor ADMIT`, `26 config-as-dir ADMIT`, `26 nonutf8 ADMIT` — and breaches the
ones f1–f10 already cover (include forms, alternates, `.git`-as-file, symlinks, argv-outside via `lane_breach`).

## Wave-2 hostile module candidates (one line each, all measured here)

1. `.git/config` as FIFO (HUNG) and as directory / mode 000 / non-UTF-8 (ERROR→LEAKED). 2. `.git/config` hardlinked
to an outside file (metric-invisible). 3. Promisor remote + `cat-file` lazy fetch. 4. `.git/objects` hardlinked
objects. 5. `.git/worktrees/wt/config.worktree` include outside + argv at the outside worktree. 6. Mixed-case
`[InClUdE]` and one-line `[include] path = …`. 7. `core.attributesFile` + `diff.<d>.textconv` executed by a status
probe. 8. `[diff] external` outside with `git diff`. 9. argv token absolute outside `d` (counter accepts it).
10. `core.excludesFile`/`mailmap.file` outside read by status/log.

## Limits

* I did not build a fence, so every "frozen leg catches it" cell is a mapping from the frozen wording to measured
  git behaviour, not an execution of the future fence. Rows 7, 8, 13, 14, 29 are marked conditional for exactly
  that reason.
* `http-alternates`, `core.sshCommand`, `url.<base>.insteadOf`, `credential.helper`, GPT/SSH remotes: named but not
  measured — they need a transport and are not reachable by a read-only probe sequence (`rev-parse`, `config`,
  `cat-file`); rows 16/35 show the file-transport shape they share.
* `.git/HEAD` as symlink is refused by git itself (row 38); `.git/refs/*` symlinks were not separately measured
  (same `SYM` shape as row 25).
* Fixtures live only in scratch; only the JSON/log receipts and probe scripts are archived beside this report.
* PATH-dir digest drift: runs 1–5 (`23:29:29`–`23:36:12`) bracketed `c263b11afb1cccf6` unchanged; run 6
  (`23:37:19`–`23:37:20`) bracketed `e396f23e40a69201` unchanged. The digest changed **between** run 5 and run 6
  (another seat installed `~/.local/bin/OpenBot-0.51.1-x86_64.AppImage`, mtime 23:36) — not this seat; no run of
  mine had a within-run change, so no measurement is `INVALID`.

## Envelope lines (QUALITY Q32)

```
ENVELOPE start 23:29:29 cwd=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign
ENVELOPE end 23:29:43 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
ENVELOPE start 23:33:12 cwd=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign
ENVELOPE end 23:33:27 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
ENVELOPE start 23:34:47 cwd=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign
ENVELOPE end 23:34:50 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
ENVELOPE start 23:35:34 cwd=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign
ENVELOPE end 23:35:36 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
ENVELOPE start 23:36:10 cwd=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign
ENVELOPE end 23:36:12 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
ENVELOPE start 23:37:19 cwd=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign
ENVELOPE end 23:37:20 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```
Each run is `claims/envelope.sh "$S/env" /usr/bin/python3 "$S/probe_vectorsN.py"` (the bwrap line is the first line
of each archived `runN.log`).

## Reproduction (receipts archived in `.ufo/waves/round-45/w1/R45SentFenceDesign/`)

```
5707ff176ff30d7c9eb9d3b40bd701c1c27f81cac7bed6832c816947fc328755  probe_vectors.py
3708c8627cefb50d0efceb0f7d0fc605640c5e76540a8d3d0c6dec1fbed31d46  probe_vectors2.py
75e608aa7c17e4cf2b72be988d1c9c7591aa2bda1a67dddaaf33a3ba06b6e115  probe_vectors3.py
cb16f2403e12d7bcafb334b6d57765c8c0b02e76a5982cecb1e5dedd67feaa4c  probe_vectors4.py
249f99dd0c2c0bb59adf555b9a669b1e13ed373715b3c9b3e1c2f43ad80069e2  probe_vectors5.py
289f33ef849562019dc78833cde4916ca9e822af3b45c61e74e48209530cf950  probe_vectors6.py
940ec28f8380570eedbd0a28d3d79441aa07e328bf846d1fba9ef989d9bb501d  run1.log
212b806835a2cd5876ab7c89b12054315cc5ce110ee683828d3641da34134dfb  run2.log
eff1c7a99f7ff9b205032bf8dbb3cc88a4eedc296e9f3dcdc12950f08692aec4  run3.log
2f6275e441464eebd17ea1143a0ff46d3004c38af20ac648ef86dd917494b3a4  run4.log
a86ebc3cde9ff7d859b4bb7e7791c574685c5e26b6d2710810ea9a7dd7aade67  run5.log
f0750ab5d153948ff3b76b8eb9ca04c212d18e6d4c17eaeaedbdd723078888a7  run6.log
08f4b6607e5a9fc7f6af0a3ead5656fcf5f9a22146757ed4cbd49ea02e76ffd0  vectors.json
cc3424d10f72231805b8cdc9a1775dc21b3361bbd576f4a77de113552814b4af  vectors2.json
ce4a68b751bd7f0de7d90ab0546a0d80e729d1c9db4279a9896a58ccd463f116  vectors3.json
e3c81d1ed4611b7daecb9e2b427793b0cf9cfc63d42a095bfa8fb9388698aeb7  vectors4.json
0446e852a5e1b667c11afe92afa0fe809bfc74e5eb0505fbdad10c2d0c504176  vectors5.json
fdacce4a17617e6479afd1b97f356dc416f6b9f3d957d96e6f13567de749d8bd  vectors6.json
```
`vectorsN.json` holds every probe's argv, rc, stdout, outside-d opens, outside paths/execs and attempts;
`runN.log` holds the ENVELOPE lines and the one-line verdict per scenario. Trace logs stayed in scratch (1.7 MB)
and are quoted inline above; they were deleted with the scratch tree.
Re-running needs `S=/fast/scratch/hyaku/kengaku-r45/R45SentFenceDesign`, `mkdir -p "$S"; export TMPDIR="$S"`,
then the envelope command above; every fixture is rebuilt from nothing inside the bwrap run, and nothing is written
outside `$S`.

VERDICT: fence-design-vectors-38-uncovered-15
