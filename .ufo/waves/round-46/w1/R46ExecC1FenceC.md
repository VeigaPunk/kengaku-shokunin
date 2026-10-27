# R46ExecC1FenceC — repaired fixture fence (round 46, C1, wave 1, variant C: isolated git)

Seat: executor `R46ExecC1FenceC`. Lane clone (shared): `/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceC/lane`
at `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f` (`git -C "$S/lane" rev-parse HEAD`), whose
`plans/fixture_fence.py` was the round-45 landed fence `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`
— i.e. the file at base `64ba8385` unchanged. I edited **only** the clone's `plans/fixture_fence.py` and wrote
inside `.ufo/waves/round-46/w1/R46ExecC1FenceC/`. No lane file outside my report dir was touched, no tool was
installed, no pacman transaction, no counter of round 46 was read or run, nothing under
`.ufo/waves/round-46/w1/` outside my own subdir was opened.

Deliverable: **`fixture_fence.py`** (sha256 `13e5a4c9e4f91dccb9cc7df2f88a9c1f2b7bfd72963ac4a40996a6c1ce4bd528`),
in this seat's dir, ready for the L1 to land at `plans/fixture_fence.py`. Contract unchanged:
`breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None`, stdlib only, one-line reason strings.

## 1. Headline

| measurement | result |
|---|---|
| round-45 counter on the clone (`plans/round45_c1_verify.py --lane . --jobs 8`) | `PINS total=33 mismatched=0`, `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=10 contradicted=0`, **`PREDICATE C1 pass`**, exit 0 |
| round-45 held-out modules (11 files / 31 fixtures), frozen r45 driver path | **11/11 clean** — 31/31 `BREACH opens=0`, 0 admitted, 0 hung |
| round-46 B5 pre-emption (`strace -e trace=%file` over 148 fixtures: honest 104, refusals 13, held-out 31) | `TRACED fixtures=148 with_outside_path_touch=0` — no `open*/stat*/access/readlink/getxattr/chdir` on **any** path under the scratch root other than `d` itself |
| name independence (built fixtures copied to `secrets.token_hex(8)` dirs, fence re-run) | 11/11 verdicts identical (4 refusal-side BREACH, 7 honest ADMIT) |
| 8 extra hostile/honest shapes I wrote (not in the frozen set) | 7 refused as designed, 1 admitted by design (a legitimate shape, to prove no over-refusal) |

Every run below carries its `ENVELOPE` lines. All envelopes: `exit=0 local_bin_content_before=ff187bb5c98aa6b5
after=ff187bb5c98aa6b5 unchanged` (no `INVALID`).

## 2. Design (variant C — isolated git, refuse what cannot be proven safe)

The base fence's failure is structural: it is a denylist of attack shapes over a *walk it prunes* (`.git`), so
anything below a `.git` dir, any config syntax its regex misses (`\r`, BOM), and any repo git can describe
while its store lives elsewhere gets through (round-45 closure §5; `R45Ho*` verdicts). The repaired fence
inverts that:

1. **Static pass, no child process, nothing outside `d`.** Argv must be the tool's exact contract shape — for
   `order` the literal six tokens; for `anchor` exact option tokens, each valued option carrying a value; no
   token may hold a NUL or a `{...}` placeholder; every path value must resolve **lexically** inside `d`
   (normpath only: no `stat`, no `resolve()`, so no outside access even to decide containment). Then one walk
   of the **whole** tree with `.git` directories descended into (the base fence pruned them — that is how
   `g4`'s hidden `commondir` survived). It refuses, before git is reached:
   - a `.git` **file** (gitdir redirect) or a `.git` **symlink** (even one pointing inside `d`: unprovable);
   - a `.git` nested inside a git dir, and `worktrees/` or `modules/` under a git dir (linked-worktree and
     submodule metadata — `g3`, `g4`);
   - any `commondir`, `gitdir`, `alternates` or `http-alternates` file in any store (git dir or bare store);
   - any config file (`config*`) whose text carries an `include`/`includeIf` section, a `path =` key, or a
     path-bearing key (`core.attributesfile`, `core.excludesfile`, `core.hookspath`, `core.fsmonitor`,
     `core.bare` true, `extensions.worktreeConfig`, `core.worktree` not equal to the repo);
   - any symlink whose target chain leaves `d` (followed by `readlink` only, hop-capped), any FIFO/socket/
     device/special file, any store file with an extra hard link (the hardlink-borrowed store);
   - a bare store is judged like a git dir (its own `config`, `commondir`, `alternates`), so no config escapes
     the scan by not sitting under `.git`.
   Config text is BOM-stripped and `\r`/`\r\n` normalised before the scan — that is what closes `h1`/`h3`
   (a bare CR before `[include]`, and a BOM at byte 0).
2. **Git pass, only after the static pass, only inside a mount namespace that contains `d` (bound at the
   constant alias `/fixture`), the read-only system tree and nothing else.** Any reference to a path outside
   `d` cannot resolve, so git fails and `rc != 0` is a refusal (`f6`, repo above `d`, is exactly this). Legs:
   `rev-parse --show-toplevel --absolute-git-dir --git-common-dir` (the **common dir** is what the base fence
   never asked — `g4`'s escape), each translated back and required inside `d`; `config --local --no-includes
   --get core.worktree`; for `order`, `cat-file -t HEAD:<claims>` and `HEAD:<receipt>` must not be a tree.
3. **Nothing is trusted because a name looked hostile.** The fence reads no fixture name, no sibling, no
   module name, no counter name; it never imports the counter; it keys on nothing but bytes inside `d` and on
   git's answer from inside the namespace.

### 2a. Variant C specifics and the one measured trap

Nested namespaces **do** work inside the counter's own `ro_sandbox` (this had to be tested first):

```
OUTER rc= 0 stdout= /fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceC/nt2/fx/fixture stderr=
HOST-NESTED rc= 0 stdout= /fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceC/nt2/fx/fixture stderr=
ESCAPE rc= 128 stderr= fatal: not a git repository (or any parent up to mount point .../nt2/fx)
ENVELOPE start 02:09:48 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:09:52 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```
(`tools/nested_test.py`; the third line is a `commondir` escape: inside the alias-only namespace git cannot
see the outside store at all.)

The trap: **how `d` is bound decides whether the fence touches the scratch root outside `d`.** With an
absolute bind source (`--ro-bind <d> /fixture`) bubblewrap canonicalises `d`'s parent components and emits
three `readlink` calls on paths outside `d` — under a round-46 counter's B5 rule (stat/readlink/access on such
paths count like opens) that alone would mark every honest fixture `read`.

```
VARIANT D-usr-only rc=0 offenders=0
VARIANT E-bind-d-true rc=0 offenders=3
     5     readlink(".../sv2r", 0x...) = -1 EINVAL      # d's ancestors: scratch root, fx, module dir
VARIANT I-src-dot-cwd-d rc=0 out='/fixture\n/fixture/.git\n.git' offenders=0   # relative source "." , cwd = d
VARIANT J-src-basename-cwd-parent rc=0 offenders=2                              # relative, but cwd = d.parent
VARIANT H-plain-git rc=128 offenders=9                                          # no namespace: git stats d.parent
```
So the fence binds the **relative** source `"."` (the child's cwd is `d`) at `/fixture`. With that, the whole
process tree's `%file` trace over 148 fixtures shows **zero** paths under the scratch root other than `d`
(§1, `receipts/FINAL-trace.out`). Incidentally variant H is why the isolation is needed at all: plain git
stats `d.parent`, `d.parent/.git`, `d.parent/HEAD` — outside opens/stat that the base fence caused.

## 3. Round-45 counter on the clone (frozen counter, unchanged)

Command:
```
envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/wF" --jobs 8
```
Output (complete predicate block; `receipts/FINAL-counter.out`, sha256 `fba76431…153d329`):
```
ENVELOPE start 02:07:35 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=13e5a4c9e4f91dccb9cc7df2f88a9c1f2b7bfd72963ac4a40996a6c1ce4bd528
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 02:07:51 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```
All 10 refusals and all 104 honest fixtures report `opens=0`; the 104 honest fixtures are all `ADMIT`
(grep: `FENCE-RUN honest` rows with anything but `ADMIT opens=0` → 0).

Refusal reasons (one per module, from the same receipt):
| module | reason |
|---|---|
| f1_gitfile | `.git is a file (gitdir redirect), not a directory` |
| f2_deep | `x/y/z/r/.git/config sets core.worktree=<outside>` |
| f3_abbrev | `order argv is not the contract shape [...]` |
| f4_fifo | `lane/.git/config carries a [include] section` |
| f5_alternates | `lane/.git/objects/info/alternates is an alternates file` |
| f6_above | `sub: git cannot describe the fixture (rc=128)` (inside the namespace there is no repo above `d`) |
| f7_commondir (3 fixtures) | `lane/.git/commondir is a store/worktree redirect` |
| f8_worktreecfg (2) | `lane/.git/config enables extensions.worktreeConfig` |
| f9_nodescribe | `lane/.git/config sets core.bare` |
| f10_laneinclude | `lane/.git/config carries a [include] section` |

## 4. Held-out module table (round-45 `R45Ho*` modules, frozen counter path)

Two layers of evidence, both under the envelope, both on the clone:

- **"Original" drivers** — each seat's own driver, pointed at the clone. `R45HoCommondir2/driver.py`,
  `R45HoArgvEnv/probe.py`, `R45HoConfigKeys/probe.py` take the lane as argv and ran unchanged;
  `R45HoSymlinks/run_probe.py` hardcodes the lane path, so its **scratch copy** with the single line
  `lane = pathlib.Path("…/R46ExecC1FenceC/lane").resolve()` replaced is in `tools/run_probe_lane_clone.py`
  (`diff`: one line). Receipt: `receipts/FINAL-original-drivers.out` (`633aa5b1…2ccc3`).
- **One uniform table** — `tools/heldout_driver.py` calls the frozen `c1.build_module` / `c1.run_fence`
  exactly as the counter's `main()` does, over all 11 module files at once. Receipt:
  `receipts/FINAL-heldout.out` (`9bb7238d…487f23`).

| # | held-out module | fixtures | base fence (round 45) | repaired fence | reason (first fixture) |
|---|---|---|---|---|---|
| 1 | `R45HoIncludeIf/h1_cr_include.py` | 2 | admitted+read | **clean** 2/2 BREACH | `lane/.git/config carries a [include] section` (bare CR normalised) |
| 2 | `R45HoIncludeIf/h2_includeif_cond.py` | 9 | admitted+read | **clean** 9/9 | `… carries a [includeif] section` |
| 3 | `R45HoIncludeIf/h3_bom_symlink.py` | 4 | admitted+read | **clean** 4/4 | `… carries a [include] section` (BOM stripped) |
| 4 | `R45HoIncludeIf/h4_controls.py` (control) | 3 | clean | **clean** 3/3 | `… carries a [includeif] section` |
| 5 | `R45HoSymlinks/link_hostiles.py` | 5 | admitted 2, read 1 | **clean** 5/5 | `symlink lane/.git/objects -> … leaves the fixture`; `.git is a symlink`; `symlink lane/claims.md -> …`; `…/objects/05/6b827f2b… has extra hard links`; `… carries a [include] section` |
| 6 | `R45HoArgvEnv/argv_env.py` | 3 | admitted 1 (ERROR) | **clean** 3/3 | placeholder token; `argv token carries a NUL byte`; argv shape |
| 7 | `R45HoCommondir2/modules/g1_cdrel.py` | 1 | clean | **clean** 1/1 | `repo/.git/commondir is a store/worktree redirect` |
| 8 | `R45HoCommondir2/modules/g2_gitfile.py` | 1 | clean | **clean** 1/1 | `lane/.git is a file (gitdir redirect), not a directory` |
| 9 | `R45HoCommondir2/modules/g3_wtmeta.py` | 1 | **admitted** | **clean** 1/1 | `repo/.git/worktrees is linked-worktree/submodule metadata` |
| 10 | `R45HoCommondir2/modules/g4_cdrel_hidden.py` | 1 | **admitted+read (32 opens)** | **clean** 1/1 | `repo/.git/modules is linked-worktree/submodule metadata` |
| 11 | `R45HoConfigKeys/configkeys.py` | 1 | **admitted** | **clean** 1/1 | `lane/.git/config sets core.attributesfile` |

Totals: **11/11 modules clean, 31/31 fixtures refused, `opens=0` on every row, 0 hung, 0 build errors.** The
round-45 counter's module rule (`n_admit = ADMIT or ERROR`) never fires: there is no `ERROR` row — the NUL
argv case that the base fence raised as an uncaught `ValueError` is now a refusal.

Round-45 base values are quoted from the seats' own verdict lines: `includeif-modules-3-admitted-3-read-3`,
`argvenv-modules-1-admitted-1-read-0`, `commondir2-modules-4-admitted-2-read-1`,
`link-modules-5-admitted-2-read-1`, `configkey-modules-1-admitted-1-read-0`.

Note on `R45HoConfigKeys/probe.py`: after the decision it runs `git check-attr` on the fixture and still
prints `TOOL_CHECK_ATTR rc=0 stdout=marker: hostile: outside`. That line is the probe's own host-side check
that *git* honours the outside `attributesFile`; it is not a fence measurement. It confirms the fixture is a
real defect when admitted, and the fence now refuses it before any git child exists.

## 5. Round-46 B5/B3 pre-emption (my own measurement — NOT the round-46 counter)

The round-46 counter may not be run against repaired work before the stage-2 pin, so I measured the classes it
freezes with the round-45 builder/runner plus an extended trace filter (`-e trace=%file` = every syscall that
takes a path: open*, stat*, access, readlink*, getxattr, chdir, execve, mount, mkdir, …), classifying any
path under the scratch root that is not `d` and is not the harness/fence copy:

```
envelope.sh "$S/env" /usr/bin/python3 tools/trace_probe.py "$S/lane" "$S/tpF" <104 honest + 10 refusal + 11 held-out module files>
TRACED fixtures=148 with_outside_path_touch=0
ENVELOPE start 02:08:09 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:08:50 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```
(`receipts/FINAL-trace.out` `30b1939c…2c54d`.) 148 = 104 honest + 13 refusal fixtures + 31 held-out fixtures.
So the fence's decision is invisible to a B3/B5-style count: it does not open, stat, access or readlink a
single path under the build scratch outside `d`. (The earlier, first-cut fence bound `d` by absolute path and
would have failed exactly this — see §2a; that is why the bind source is relative.)

Verdict is never parsed from stdout (B4 is a counter-side defect, but the fence no longer prints anything at
all: `breach` returns a string, the harness prints it, and only the counter's own parsing is at stake). The
fence does not unlink or touch any log (B1 is out of its reach by construction), and it uses no io_uring (B7:
not used, so not a channel this fence opens).

## 6. Generalization checks (my own, outside the frozen set)

`tools/extras.py` (8 fixtures; receipt `receipts/FINAL-extras.out` `7286674b…b9e1a3f`):

| fixture | intent | result |
|---|---|---|
| bare store at `d/store` with `[include]` in its own `config` | config outside any `.git` | **BREACH** (`store/config sets core.bare` — the bare store's own `core.bare` is refused before the include) |
| `.git/objects/info/http-alternates` | second alternates channel | **BREACH** (`is an alternates file`) |
| `core.worktree = .` | legitimate key, self-consistent? | **BREACH** (`worktree top level is lane/.git, not the repo directory`) — git resolves `.` against the **git dir**, so the repo is genuinely self-inconsistent; refusing is correct, and honest fixtures never set it |
| second real repo nested in the first one's worktree | must NOT over-refuse | **ADMIT** |
| `core.worktree = <d.parent>/wt` | redirect | **BREACH** (static config scan) |
| `d/lane/.git` symlink to a git dir **inside** `d` | unprovable link | **BREACH** (`.git is a symlink, not a git dir`) |
| `alternates` to a store **inside** `d` | borrowed store | **BREACH** (`is an alternates file`) |
| `.git/config.worktree` with an `[include]` whose target is **inside** `d` | include, local target | **BREACH** (`… carries a [include] section`) |

The extras module's own roll-up therefore prints `LEAKED fixtures=8 admitted=1` — the single admit is the
deliberate piggy-backed honest shape, not a leakage.

Name independence (`tools/name_random.py`, receipt `receipts/FINAL-name-random.out` `965171e7…766cb9`): 11
built fixtures copied to `secrets.token_hex(8)`/`secrets.token_hex(8)` paths — 4 refusal-side keep their
BREACH (same reason strings), 7 honest keep their ADMIT. Nothing in the decision depends on a fixture,
sibling, module or build-order name.

## 7. Limits (named, not hidden)

1. **Nested unprivileged namespaces are a hard dependency.** Variant C needs `bwrap` to create a mount/pid/net
   namespace *inside* the counter's sandbox. Measured working here (bubblewrap 0.13.1, strace 7.2,
   python 3.14.8, kernel 7.2.11-arch1-1). If a future sandbox forbids them, every repo probe fails and the
   fence **refuses every fixture with a repo** — fail-safe, but the HONEST leg would then fail loudly instead
   of the fence silently admitting.
2. **Fixed executable paths** `/usr/bin/bwrap`, `/usr/bin/git` (the round-45 counter already requires
   `/usr/bin/bwrap`). A host without either refuses every fixture.
3. **Conservative refusals beyond the honest set**: any `include`/`includeIf` (even with a local target), any
   `core.worktree` that git does not confirm as the repo, any `alternates`/`commondir`/`gitdir`/`worktrees`/
   `modules`, any symlinked `.git`, any store file with `st_nlink > 1`, any bare store inside the fixture, any
   config key in the path-bearing set. The 104 honest fixtures of `plans/battery42|43|44` are all admitted;
   a module that legitimately needs one of these shapes would have to be judged by the L1 as a false refusal.
4. **The config scan is not git's parser.** It normalises BOM/CR/CRLF and looks for the section/key shapes;
   it refuses rather than emulating git's condition evaluation (`includeIf` conditions, `path=` escapes).
   Escapes inside values are therefore not evaluated — the whole include surface is refused instead.
5. **The git pass proves discovery, not tool execution.** It answers the round-45 advertisement ("git store,
   discovered repos and argv stay inside `d`"); it does not run `plans/order_check.py` or
   `plans/anchor_digest_check.py`. A fixture whose *tool run* would leave `d` (e.g. reading a `$HOME` file) is
   out of this contract, and was out of the base contract too.
6. **io_uring is not used by this fence**, so the B7 channel is not one it opens; if a future hostile module
   forced the fence to submit io_uring SQEs (it does not), the trace filter would miss them.
7. **Time**: 104 honest + 13 refusal fixtures in ~16 s wall at `--jobs 8`; each fixture costs ≤ 4
   `bwrap+git` calls at a 20 s timeout each, inside the counter's 120 s per-fixture cap.

## 8. Envelope lines (all runs)

```
ENVELOPE start 02:07:35 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:07:51 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged   # counter
ENVELOPE start 02:07:54 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:08:04 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged   # held-out (11 modules)
ENVELOPE start 02:08:09 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 02:08:50 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged   # %file trace, 148 fixtures
ENVELOPE start 02:09:04 / end 02:09:07 exit=0 … unchanged   # Commondir2 driver
ENVELOPE start 02:09:10 / end 02:09:13 exit=0 … unchanged   # ArgvEnv probe
ENVELOPE start 02:09:15 / end 02:09:18 exit=0 … unchanged   # ConfigKeys probe
ENVELOPE start 02:09:20 / end 02:09:23 exit=0 … unchanged   # Symlinks run_probe (clone-patched copy)
ENVELOPE start 02:09:26 / end 02:09:30 exit=0 … unchanged   # extras
ENVELOPE start 02:09:32 / end 02:09:36 exit=0 … unchanged   # name random
ENVELOPE start 02:09:48 / end 02:09:52 exit=0 … unchanged   # nesting + bind variants
ENVELOPE start 02:09:58 / end 02:10:02 exit=0 … unchanged   # absolute-source readlinks
```

## 9. Files in this seat's dir

| file | bytes | sha256 |
|---|---|---|
| `fixture_fence.py` (the deliverable) | 18879 | `13e5a4c9e4f91dccb9cc7df2f88a9c1f2b7bfd72963ac4a40996a6c1ce4bd528` |
| `receipts/FINAL-counter.out` | 11599 | `fba764319e8e3c65757a79660c496edb5181472367946c5afb77e1e11153d329` |
| `receipts/FINAL-heldout.out` | 10172 | `9bb7238d6f37b380a382209945e0f02b2c0e461f617a017d0d2c01b48c487f23` |
| `receipts/FINAL-trace.out` | 4338 | `30b1939c10c03660e9e8d5e47e7adcb56dc41b0ef188e74b56f248cc3e72c54d` |
| `receipts/FINAL-original-drivers.out` | 5641 | `633aa5b1ff09d95f3c5e4f6a2283580e7d5bc2397f649d10b752cad45f72ccc3` |
| `receipts/FINAL-extras.out` | 2273 | `7286674bd6e370e3f11ea7208f16ded61c8942ba99c87089e7e83fd86b9e1a3f` |
| `receipts/FINAL-name-random.out` | 2536 | `965171e74c876bae344abc09576546848651238a2b612e0a2e54e8262b766cb9` |
| `receipts/FINAL-nesting-and-bind.out` | 1664 | `2aca9294564f150ef3d12419152f4fbc9d5ef7e8ba398d86a0abcaa2743230d3` |
| `receipts/FINAL-absolute-source-readlinks.out` | 4246 | `1b00ef1b91a8e5ca04c877f03cffb391fe8832eaf50bf40cf57f3cdfe5039889` |
| `tools/heldout_driver.py` | 1885 | `110a8c423d5a8fef4e299ce1fcf6960ae9bb8294952d318982adfe144adc25b6` |
| `tools/trace_probe.py` | 3274 | `c30732eafa857bb48aaa82fda7222a83a311e490f54c0c1dee4f5e1ad57b5ccf` |
| `tools/extras.py` | 4284 | `54e4b5e7efb5c3e595f328364f6543b26c600c4a8ac489a2dd5f13956a42a7da` |
| `tools/name_random.py` | 1417 | `8a01f604e08d027c480f4602e3ff305bda8dcc7b0c4eb6f38abe8fcf8b17cdbe` |
| `tools/nested_test.py` | 2655 | `85b529e29b30026fd67092f37a7c5308ce98d82a16f0fdb51a2310d9a7b022aa` |
| `tools/sv2.py`, `tools/sv3.py` | 3138 / 2569 | `a65f5516…07af89` / `0c074a37…65ca` |
| `tools/run_probe_lane_clone.py` | 1475 | `1f3b8e4a5de68c0d9607f06a52eece87c54422a700cceac3adda1e81276711f0` |

No receipt is over 1 MiB; no lane tree, corpus tree or clone was copied here. Scratch
`/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceC` is removed with the mandated guard after this report is
written.

## 10. For the L1

- Land `fixture_fence.py` as `plans/fixture_fence.py` and re-run `plans/round45_c1_verify.py --lane . --jobs 8`
  on the landing tip (expect the exact block in §3).
- The fence is a *behaviour* change only: same module path, same `breach(d, argv, tool)` contract, stdlib only.
  `plans/refusals46/` conversions of the `R45Ho*` modules should now be refused by the reason strings in §4.
- Two things I could not test and did not: any round-46 counter draft (§C1 order rule), and `plans/sealed46/`
  modules (they do not exist yet and no fence-writing seat may read them). The design intends to answer them
  structurally: everything git touches after the static pass is confined to `d`, and anything whose store or
  config the fence cannot prove local is refused before git runs.

VERDICT: fenceC-r45-pass-yes-heldout-refused-11/11
