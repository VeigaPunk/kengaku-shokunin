# R45LabratControls — hand replay of the r44-fence control (before-state for C1)

Seat: R45LabratControls (reviewer, leaf). 2026-10-26. Scope: independently verify the frozen before-state
count **contradicted=7** in `claims/control-c1-fence-r44.txt` WITHOUT the round-45 counter: rebuild the
refusal fixtures in scratch with the module builders, run the round-44 fence's five functions
(`plans/round44_c1_verify.py`) under my own `strace -f -y`, and confirm each leak/read per the receipt.
All 10 modules replayed (the 7 contradicted + the 3 clean), 13 fixtures.

## Method

1. Scratch `S=/fast/scratch/hyaku/kengaku-r45/R45LabratControls` (all paths below shown with the constant
   prefix `/fast/scratch/hyaku/kengaku-r45/R45LabratControls` abbreviated `<S>`).
2. Fixtures built with the counter's own builders: `build_one.py` imports `round44_c1_verify` and uses its
   `Ctx`/`load` exactly as `build_module_child` does (`Ctx.ENV` pins, `GIT_CEILING_DIRECTORIES`), so builder
   semantics are byte-identical to `build_battery`'s build child. `PYTHONDONTWRITEBYTECODE=1` + `-B`;
   after the runs `git status --porcelain plans/` in the lane is empty and no `__pycache__` was created.
3. Fence replayed by `fence_one.py`: composition copied verbatim from `round44_c1_verify.py:738-740` —
   `argv_shape_breach(tool, argv) or lane_breach(d, argv) or repo_breach(d) or symlink_breach(d)
   or (order_argv_breach(d, argv) if tool == "order" else None)`. One envelope-wrapped
   `strace -f -y -s 512` python child per fixture; its trace is the fence run.
4. Opens counted per the r45 C1 rule: successful or never-returned `open/openat` of a path under the
   module build scratch outside the fixture dir `d` (`count_opens.py`; successful opens carry the
   `-y`-decoded fd path `= N</path>`; a blocked open stays `<unfinished ...>`).
   Fence refusal verdicts (`FENCE-VERDICT`) and outside-open counts were computed independently of the
   receipt, then compared.
5. Every build/fence run wrapped in
   `.ufo/waves/round-45/claims/envelope.sh "$S/env" <cmd>` (home read-only bwrap, `~/.local/bin`
   content digest before/after).

## Instrument integrity

- `plans/round44_c1_verify.py` sha256 `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad`
  — equals the pin in `plans/round45_c1_verify.py:66`.
- `plans/refusals45/*.py`, `envelope.sh` digests recorded in `<R>/sha256sums.txt`
  (`<R>` = `.ufo/waves/round-45/w1/R45LabratControls`).
- Tools: git 2.56.0, Python 3.14.8, strace 7.2, /usr/bin/bwrap. No tools installed (none needed).

## Envelope records (QUALITY Q32)

Build runs: one envelope per module, 23:36:33–23:37:06, all `exit=0`.

- **f5 build run 1 (23:36:48) INVALID and re-run once, both reported:** during it
  `local_bin_content_before=c263b11afb1cccf6 after=e396f23e40a69201 CHANGED` → envelope exited 4. The
  digest shift persisted for all later runs (`e396f23e40a69201`), i.e. `~/.local/bin` content changed
  host-wide mid-loop (a concurrent seat's tool install; my process cannot write it — the envelope ro-binds
  `/home/vgpnk`). f5 build re-run 23:38:26–23:38:28: `exit=0 ... before=e396f23e40a69201
  after=e396f23e40a69201 unchanged`.
- Fence runs: 13 envelopes, 23:38:47–23:40:01, all `exit=0`, all `unchanged` (start/end lines per fixture
  are in `<R>/<fid>.verdict.txt`; no `CHANGED`/`INVALID` in any). f4 ran 23:39:01→23:39:33 (the fence's own
  30 s `GIT_TIMEOUT` hang — expected, see below). Representative line:
  `ENVELOPE end 23:39:33 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged`.

## Results — my replay vs the frozen receipt

Receipt `claims/control-c1-fence-r44.txt` rows in parentheses. "clean" = refused with zero outside opens.

| module | fixture | my verdict | my opens | receipt | match |
|---|---|---|---|---|---|
| f1_gitfile | f1-gitdir-outside | BREACH `--lane rev-parse --absolute-git-dir=<S>/fx/f1_gitfile/side/gitdir is outside the fixture` | 4+2=6 | BREACH opens=6, same message | YES |
| f4_fifo | f4-fifo-include | BREACH `--lane git hung` | 1 never-returned | BREACH opens=1, `--lane git hung` | YES |
| f6_above | f6-repo-above-d | BREACH `--lane rev-parse --show-toplevel=<S>/fx/f6_above is outside the fixture` | 3 | BREACH opens=3, same message | YES |
| f7_commondir | f7-cd-accept / cd-reject / cd-anchor | ADMIT ×3 | 40 / 40 / 15 | ADMIT opens=40/40/15 | YES |
| f8_worktreecfg | f8-wtcfg-a / wtcfg-b | ADMIT ×2 | 8 / 8 | ADMIT opens=8/8 | YES |
| f9_nodescribe | f9-bare-repo | ADMIT | 0 | ADMIT opens=0 | YES |
| f10_laneinclude | f10-lane-include-regular | BREACH `lane/.git/config carries an include` | 4 | BREACH opens=4, same message | YES |
| f2_deep | f2-deep-worktree | BREACH (`--lane ... /wt is outside`) | 0 | clean opens=0 | YES |
| f3_abbrev | f3-abbrev-tree-claims | BREACH (argv shape) | 0 | clean opens=0 | YES |
| f5_alternates | f5-alternates-outside | BREACH (alternates) | 0 | clean opens=0 | YES |

Totals: REFUSALS total=10 clean=3 leaked=3 read=4 hung=0 build_errors=0 → **CALIBRATION
advertised=10 contradicted=7**, identical to the receipt line for line. Per-fixture receipts:
`<R>/<fid>.verdict.txt` (FENCE-VERDICT + ENVELOPE lines) and `<R>/<fid>.outside.txt` (the outside-`d`
openat lines, pid-tagged). Full traces deleted with scratch; sha256+line counts in
`<R>/traces-manifest/traces.sha256.txt`.

## Syscall evidence per contradicted module (quoted from `<R>/*.outside.txt`; pid = traced process)

- **f1 (READ opens=6):** `d/.git` is a gitdir FILE → `lane_breach` runs before any refusal. Its two git
  children (pid 5 `rev-parse --show-toplevel`, pid 6 `rev-parse --absolute-git-dir`) each opened the
  outside store: `<S>/fx/f1_gitfile/side/gitdir/HEAD` and `.../side/gitdir/config` (3 per child) —
  `openat(AT_FDCWD<...f000>, "<S>/fx/f1_gitfile/side/gitdir/config", O_RDONLY) = 3<...>` — then
  `--absolute-git-dir` answered outside `d` and the fence refused. Refused, yet read.
- **f4 (READ opens=1, hung):** pid 5: `openat(AT_FDCWD<.../f000/lane>, "<S>/fx/f4_fifo/fifo.cfg",
  O_RDONLY <unfinished ...>` — the FIFO include target opened by the first `lane_breach` rev-parse and
  never returned; python's `GIT_TIMEOUT=30` killed it (envelope window 32 s), `lane_breach` returned
  `--lane git hung`. The never-returned open is the leak-while-deciding.
- **f6 (READ opens=3):** `--lane d/sub`, repo discovered ABOVE d. pid 5:
  `openat(..., "<S>/fx/f6_above/.git/HEAD", O_RDONLY) = 3<...>`, then `.git/config` ×2 (pids 5,6) read
  from the repo above `d`; pid 6's `--show-toplevel` then answered `<S>/fx/f6_above` → refused, after the
  outside store was read.
- **f7 (LEAKED, opens 40/40/15):** `.git` is a real dir; `.git/commondir` redirects the store beside d.
  `--absolute-git-dir` still answers `<S>/fx/f7_commondir/f000/lane/.git` (inside d) and `--show-toplevel`
  answers `lane`, so every leg passes → ADMIT, while the fence's git children read the outside store
  through commondir: per order fixture 40 opens of `<S>/fx/f7_commondir/storeA/.git/config` (18),
  `refs/heads/master`, `refs/`, `objects/pack` and loose objects (pid 11/12 samples:
  `openat(..., "<S>/fx/f7_commondir/storeA/.git/objects/42/68d1a342..., O_RDONLY|O_CLOEXEC) = 3<...>`) —
  including `order_argv_breach`'s `cat-file` blob reads. The advertised refusal never happens.
- **f8 (LEAKED, opens 8/8):** `extensions.worktreeConfig=true`, include in `.git/config.worktree` names
  `<S>/fx/f8_worktreecfg/outside-a.cfg`. Every git child that parses config with includes opened the
  outside file (pids 5–12, one each, = lane_breach rev-parses, repo_breach rev-parses, order_argv
  cat-files), e.g. `openat(..., "<S>/fx/f8_worktreecfg/outside-a.cfg", O_RDONLY) = 4<...>`; the
  `--local --no-includes` include-scan does NOT open it and finds no include in `.git/config` itself, so
  no leg refuses → ADMIT while the include target is parsed by the fence's own process tree.
- **f9 (LEAKED, opens=0):** `core.bare=true` → `rev-parse --show-toplevel` exits non-zero, and the r44
  fence treats `rc != 0` as "nothing to check" (`if got[0] == 0:` guards); `--absolute-git-dir` answers
  inside `d`. ADMIT with zero outside opens — the silent admission (`refuse-to-describe` reads as clean).
- **f10 (READ opens=4):** pids 5/6 = the two `lane_breach` rev-parses, each
  `access("<S>/fx/f10_laneinclude/inc10.cfg", R_OK) = 0` then
  `openat(..., "<S>/fx/f10_laneinclude/inc10.cfg", O_RDONLY) = 4<...>` and
  `read(4<...inc10.cfg>, "[user]\n\temail = OUTSIDE-READ@invalid\n", 4096) = 37`. pid 7 = `repo_breach`'s
  include-scan `git config --local --no-includes --get-regexp ^include(if)?\.`: its startup config parse
  opened the include target twice BEFORE the `--no-includes` query, which then wrote
  `"include.path <S>/fx/f10_laneinclude/inc10.cfg\n"` to the pipe → refused by `repo_breach` ("carries an
  include") after 4 successful outside opens. Decided only by reading outside `d`.

## Deviations and residual risk

- My build used the counter's `Ctx`/`load` under the envelope, not the counter's full `ro_sandbox`
  (hide-list, memfd builder). Builders write only through `Ctx._inside` (fixture-root guard), so fixture
  trees are built by the same code path; I did not byte-compare against the L1 control run's fixtures
  (not available to me) — residual risk negligible for fence behaviour, since every verdict re-derives
  from the built tree at run time.
- Open counts are exact-match on this host (git 2.56.0, strace 7.2) — every count equals the receipt
  (6/1/3/40/40/15/8/8/0/4). On a different git version counts could shift without changing any verdict.
- f1/f6 refusal messages carry my scratch paths where the receipt carries L1's — shape and leg identical.
- Not in scope, not re-verified: `HONEST fixtures=104 admitted=104`, the other three controls
  (`nothing`, `admit_all`, `refuse_all`, `static_only`), and the round-45 counter itself (not yet written).

## Conclusion

The frozen before-state reproduces exactly by hand: f7/f8/f9 leak, f1/f6/f10/f4 are refused only after
their own process tree opens (or blocks on) a path outside the fixture directory, f2/f3/f5 refuse clean
— `contradicted=7` of the 10 advertised refusals, `PREDICATE C1 fail`. The round-45 fence requirements
(pure-filesystem legs first, `rc != 0` = breach, no outside open while deciding) are each grounded in a
specific observed failure above.

Report: .ufo/waves/round-45/w1/R45LabratControls.md

VERDICT: before-state-confirmed-7/7
