# F42C1Hardened — a hardened copy of the round-42 C1 counter, one hostile module per repair

Seat `F42C1Hardened` (executor, leaf; no subagent, no `task`/`agent`/workpool call, no `proc://` job — the one
full-battery run was a single shell-level `async` invocation of one bwrap command, finished in 3 s).
Target: `plans/round42_c1_verify.py` (`sha256 559fca0c…c6649`) and the four wave-1 remediations it owes
(`R42SentinelCounter` V1/V2/V3, `R42CritC1Counter` V1b). The frozen counter, the two tools, `plans/battery42`
and every other lane file were read only. Everything I wrote lives in
`.ufo/waves/round-42/falsify/F42C1Hardened/` and my scratch `/fast/scratch/hyaku/kengaku-r42/F42C1Hardened`
(578 MB, clone + receipts kept for re-measurement).

Clone rule: `git clone -q --no-local …/kengaku-shokunin $S/lane && git -C $S/lane checkout -q 508434ad55c7…`;
`git -C $S/lane rev-parse --show-toplevel` → `$S/lane`; `git -C $S/lane status --porcelain` is 0 lines before
and after every run (the hostile lane write of §2 R3 lands in a sandbox-only mount; measured below).

## 1. The artifact

`…/falsify/F42C1Hardened/round42_c1_verify.py`, 42 489 B (42 478 decoded chars),
`sha256 c443b8de76b5fc77fe87cec08f7703c5228cc1f8b6b2ab3f6cf06ff4728b9a13`,
18 hunks, +152 −29 against the frozen file (35 983 B), both digested in `receipts/segment-compare.txt`. The frozen file is
untouched.

Segment-compare (byte-exact slices, `receipts/segment-compare.txt`):

| segment | bytes | sha256 (frozen = copy) |
|---|---|---|
| `MUTANTS` table | 6 672 | `2a6cf60f0dc6f7fb9e22db20c7406172c7b1fce13eb1bf651253da496e85b356` |
| `TOTAL` + `FLOORS` | 45 | `94447cc94497c9fa570d97ae7b567ba262ae4f6604db930608e3ac9d5c7df9bd` |
| predicate block (`tampered` → `PREDICATE C1`) | 1 809 | `6c900f1f0dd45843c876e2d73c7e511512d32a41038bc26576535062182e3475` |
| `exhibits` (kill rule) | 656 | `1e8fbdfe43ae1f87c6da0b07a389f3cdc3c72bc971b81d0079f047b977b15fa0` |
| `seen_directions` | 388 | `086fe9bf58e185e70f05fbba31ca92b969708d9bbb3fc744de64e2335cdf0725` |
| `PINS`/`TOOLS`/`BATTERY_REL` | 1 132 | `4bde6850d6ebd31691ca0b79febccd1a050c626f83f1b8f9b633d83244759ac5` |
| `SIDECHANNEL` + direction/rc tables | 794 | `dbb7d043b226eeb218cf0e410b41fedc3fc6363ccfd8118a06139ad8db0fff70` |

Mutant list, predicate and floors are therefore untouched; so are the pins and the kill rule. Every change
sits in the build/run plumbing, and each carries an `F42C1Hardened R#` comment naming the wave-1 finding.

## 2. The four repairs, one hostile module each

Each module is a normal `battery42`-contract module: `FIXTURES = [{"fid","tool","expect","defects","build"}]`,
built from nothing through `ctx.init`/`ctx.write`/`ctx.git`. Each was run through the frozen counter and through
the copy in dev mode (`--battery-dir <one module> --only XO1`, one fixture, so a single run is ~1 s), inside the
mandated envelope. "Green" = the exploit's effect is measured; "red" = the copy neutralises it.

| repair | wave-1 finding | copy site | hostile module | frozen (green) | copy (red) |
|---|---|---|---|---|---|
| R1 pin gpg keys | `R42SentinelCounter` V1 (HIGH) | `GIT_PINS` `:127`, `Runner.env` `:492`, `Ctx.__init__` `:258` | `battery/h1_gpgexec.py` | `observed_rc=2 … WRONG` | `observed_rc=0 … ok` |
| R2 hide `root/bin` | `R42SentinelCounter` V2 (MED) | `builder_source()` `:414`, `build_battery` `:576-607`, `Runner.hidden()` `:487` | `battery/h2_builderleak.py` | `h2-builder-LEAK-35983b-builder.py:35972` | `h2-builder-CLEAN-3908b` |
| R3 read-only hide | `R42SentinelCounter` V3/V5 (MED/LOW) | `ro_sandbox` `:324-332`, `hide_list()` `:394` | `battery/h3_lanewrite.py` | `h3-lane-WROTE-hidden` | `h3-lane-ERR30-hidden` |
| R4 reject repo escape | `R42CritC1Counter` V1b (WORKS) | `repo_breach()` `:440`, called at `:627` | `battery/h4_worktree.py` | `observed_rc=0 … ok` | `SETUP … escapes its directory …` |

### R1 — a fixture's `.git/config` could run a program (`receipts/matrix.txt`)

Frozen: `Runner.env` pins `GIT_CONFIG_COUNT=2` (frozen `:384-386`), so `gpg.program` + `log.showSignature`
from a fixture repo reached `add_commit`'s `git log --reverse --diff-filter=A --format=%H`
(`plans/order_check.py:97`). `h1_gpgexec` builds a clean freeze/receipt history, rewrites HEAD as an identical
tree carrying a `gpgsig` header (`git hash-object --literally`), and points `gpg.program` at a script that
kills its git parent. Frozen counter:

```
FIXTURE h1-gpg-program-executes tool=order expect=accept declared=- observed_rc=2 observed=- WRONG
```

The copy pins `gpg.program=/bin/true`, `log.showSignature=false` (plus `core.fsmonitor`, `core.hooksPath`) as
`GIT_CONFIG_KEY_n`, i.e. at command-line precedence above repo config and above `include.path` re-injection,
for **both** the tool run and the build child:

```
FIXTURE h1-gpg-program-executes tool=order expect=accept declared=- observed_rc=0 observed=- ok
```

Control bracket: the same build with `gpg.program=/bin/true` and the same fake signature is rc 0 on the frozen
counter too (`c1-gpg-benign-program`), and the killing program with no signed commit is rc 0
(`c1-gpg-unsigned`) — so the frozen rc=2 is the program executing, not the fixture's history
(`receipts/controls.txt`).

### R2 — the build child could read the whole counter (`receipts/matrix.txt`)

Frozen `build_battery` wrote `builder.write_text(pathlib.Path(__file__).read_text())` into
`<scratch>/bin/builder.py` (frozen `:473-476`) while hiding only the lane (`:489`); the child executes that file,
so it reads the 14 `old -> new` pairs and the `SIDECHANNEL` list. `h2_builderleak` reads `sys.argv[0]`, the
`.py` files beside it, and every `.py` under the scratch root, then carries the finding in the fixture id:

```
frozen  FIXTURE h2-builder-LEAK-35983b-builder.py:35972 …       (35 983 B = the frozen counter, written whole)
copy    FIXTURE h2-builder-CLEAN-3908b …                        (3 908 B, and nothing else in the root)
```

The copy never writes the counter into the scratch root: the child entry point is a generated minimal builder
(`Ctx`, `load`, `build_module_child`, `PATH`, `GIT_PINS`, sliced out of the copy with `ast` — so it cannot
drift), bound by `--ro-bind-data` (memfd) at `/run/k42-builder.py`; the old `root/bin` is hidden if present and
never created; module copies moved to `root/mods`.

### R3 — the lane hide was a writable tmpfs (`receipts/matrix.txt`)

Frozen `ro_sandbox` implemented `hide` as `--tmpfs <path>` (frozen `:305`); a tmpfs mount point is a writable
empty directory at the hidden name. `h3_lanewrite` writes one file at the lane path and looks for the lane's
counter:

```
frozen  FIXTURE h3-lane-WROTE-hidden …      (write succeeded at <lane>/k42probe-F42C1Hardened; contents hidden)
copy    FIXTURE h3-lane-ERR30-hidden …      (EROFS; the name is no longer writable)
```

The copy binds one empty read-only directory over each hide target (`ro_sandbox(..., empty=)`), and adds the
lane to the tool runs' hide set as well (`Runner.hidden()` `:487`). `hide_list()` dedupes and drops nested
targets: bwrap cannot create a `--ro-bind-data` destination inside a directory an earlier hide has emptied —
that failure is what moved the variant slot from `root/slots/<tool>.py` to the fixed `/run/k42-slot.py`, and
the trace run's attribution still works (the full battery attributes all 14 kills, §3). The lane clone's
`git status --porcelain` is empty after every run: the frozen run's write stayed in its private tmpfs.

### R4 — a fixture repo could point the tool outside `d` (`receipts/matrix.txt`)

`path_ok` checks argv tokens only; `order_check.main` adopts `git rev-parse --show-toplevel` as its root
(`plans/order_check.py:152`), so `core.worktree=<host repo outside d>` makes the tool measure a history the
counter never sees. `h4_worktree` builds a decoy whose own claims blob carries `gate: P10 ok fresh probe output
byte-equal` (order rc 1 on its own), a clean host repo under `d.parent`, and the redirect:

```
frozen  FIXTURE h4-worktree-redirect tool=order expect=accept declared=- observed_rc=0 observed=- ok
copy    SETUP fixture 'h4-worktree-redirect' of bat-h4_worktree/h4_worktree.py escapes its directory:
        lane/rev-parse --show-toplevel=/fast/scratch/…/k42-c1-b4hcyu69/fx/h4_worktree/host        (exit 2)
```

`repo_breach(d)` walks every `.git` under `d` (depth ≤ 3) after the module builds and refuses the fixture when
`rev-parse --show-toplevel` resolves elsewhere or `core.worktree` is set to anything but the repo itself; the
calls run in the parent with the pinned env (`PIN_CHECK_ENV`), outside the module's process. Bracket: without
the redirect the same decoy is `observed_rc=1 ok` (declared reject) on **both** counters
(`c4-decoy-no-redirect`, `receipts/controls.txt`) — the frozen accept can only come from the redirect.

## 3. Landed `battery42` through the copy — still 14/14, matrix identical

`python3 <copy> --lane $S/lane --work $S/work-full-copy --jobs 8` inside the envelope
(`receipts/full-copy.txt`, 29 fixtures, exit 0):

```
BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=9/9 order=5/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```

Per-mutant matrix (all fourteen lines, verbatim from `receipts/full-copy.txt`):

```
MUTANT X1  anchor rc-mirror  killed by=a_route-x1-provenance-table   attributed=L318 hits=2
MUTANT X3  anchor rc-mirror  killed by=a_route-x3-provenance-url     attributed=L343 hits=2
MUTANT X6  anchor silence    killed by=a_class-x6-sibling-digest     attributed=L527 hits=2
MUTANT X7  anchor silence    killed by=a_class-x7-fabricated-token   attributed=L535 hits=6
MUTANT X9  anchor rc-silence killed by=a_row-x9-short-no-token       attributed=L477 hits=2
MUTANT X12 anchor rc-mirror  killed by=a_route-x12-slashless-toml    attributed=L256 hits=2
MUTANT X13 anchor rc-silence killed by=a_row-x13-staged-capture      attributed=L570 hits=2
MUTANT X14 anchor silence    killed by=a_class-x14-uppercase-token   attributed=L458 hits=2
MUTANT X15 anchor rc-silence killed by=a_row-x15-sibling-digest      attributed=L455 hits=2
MUTANT XO1 order rc-silence  killed by=o_clause-freeze-single        attributed=L183 hits=2
MUTANT XO3 order rc-silence  killed by=o_clause-receipt-withdrawn    attributed=L188 hits=2
MUTANT XO5 order rc-mirror   killed by=o_scan-xo5-post-receipt-verdicts attributed=L117 hits=2
MUTANT XO6 order rc-mirror   killed by=o_scan-xo6-pass-verdict-row   attributed=L53  hits=2
MUTANT XO7 order rc-silence  killed by=o_scan-xo7-timeout-rows       attributed=L55  hits=2
```

Control with the same clone and envelope (frozen counter, `receipts/full-frozen.txt`):
`diff` of the two outputs is empty — the copy reproduces the landed measurement **byte for byte**, including
the `killed by=` fixture ids and `hits=` counts, which also equal the C1 block of
`.ufo/waves/round-42/integrate/measure-final.txt` (14/14, anchor 9/9, order 5/5, `PREDICATE C1 pass`).
The repairs are therefore additive: they remove the four vectors without moving a single number of the claim.

## 4. What this copy does *not* close (named, not implied)

- **R2 is about this counter's own source in the scratch root.** The build child still reads the whole
  read-only host, and other counter copies live there. My first `h2` build walked from `/` by accident and
  found `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34LegacyGaps-files/run_checks.py`
  (11 803 B, a `MUTANTS` table) — the freeze's named limit ("a module can still read other copies … elsewhere"),
  measured. The walk is now bounded to the scratch root (`len(here.parents) >= 3`), which is what R2 claims.
- **R1 pins four keys, not the key space.** The Sentinel's command matrix is the control; a future key on a
  future git may still reach an exec. A pinned `-c` set on every `git` invocation would be stricter than
  env pins, but that is a change to the tools, not the counter.
- **R4 is a build-time contract check.** It covers `rev-parse --show-toplevel` and `core.worktree` for repos
  under `d` (depth ≤ 3). It does not touch the other `R42CritC1Counter` escapes: symlinked captures/row
  sources that resolve outside `d` (V2b), an order fixture whose `--claims`/`--receipt` is a **tree** rather
  than a blob (the XO1/XO3 substitutes), or the X13 staged-manifest shape (three of the fourteen wave-1 kills).
  Those are battery-shape or kill-rule questions the freeze reserves for the non-author review; this seat did
  not widen the mutant list or the predicate.
- **`sidechannel` stays a source-only print.** `h1_gpgexec` must spell `chmod` and `$PPID` to run its program,
  so the counter prints `SIDECHANNEL … tokens=ppid,chmod` and runs it anyway (`sidechannel=1`); `h4_worktree`
  spells `core.worktree` (`tokens=core.`). Neither token went away by respelling — the scan is not a control,
  as the freeze says.
- Hiding now makes a hidden name *unwritable* but still **existent**: an `os.path.isdir(lane)`-style check is
  still fooled. R3 closes the write, not the existence.

## 5. Rider the L1 should look at (not my lane)

`.ufo/waves/round-42/integrate/measure-final.txt` closes with
`ENVELOPE end 17:52:40 exit=0 local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED`
— i.e. the Q32 digest moved during the landing measurement, whose own envelope binds `/home/vgpnk` read-only.
My own pairs are stable (`8cf5b151…` at 18:09:02/18:09:06, 18:10:35/18:10:38, 18:11:05/18:11:09,
18:12:13/18:12:37, 18:13:02/18:13:02 and 18:15:04/18:15:05). [INFERENCE] the digests are taken outside that
envelope, so a concurrent host process changed `~/.local/bin` mid-measurement; either way the landing receipt
cannot claim an unchanged PATH listing.

## 6. Envelope and Q32

Every counter/battery run above (frozen, copy, hostile, control, full) ran inside:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

`/home/vgpnk` was **not** made read-only as a whole (the counter's own nested sandboxes do that for builds and
tool runs), so `uv`/cache paths keep working. `ls -A /home/vgpnk/.local/bin | sha256sum` =
`8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` before and after every batch
(`receipts/envelope.txt`). Nothing was installed or upgraded; no pacman transaction was run.

## 7. Receipts (`…/falsify/F42C1Hardened/`, all < 1 MiB, sha256)

| file | sha256 |
|---|---|
| `round42_c1_verify.py` (hardened copy) | `c443b8de76b5fc77fe87cec08f7703c5228cc1f8b6b2ab3f6cf06ff4728b9a13` |
| `battery/h1_gpgexec.py` | `f434e4c5b45f8b1a2e29ba0bda4e0ed8b542bc2e155d8f312cb4a82c6cc96612` |
| `battery/h2_builderleak.py` | `3a94d3fe7ff27913a857c2e649a8611f4667f21557e4c4a0c400dd723d492fc4` |
| `battery/h3_lanewrite.py` | `d936e7942f1c7296ccd3b8b7e5a8b2768c1d8da7fa73b8c8554635469ddd045e` |
| `battery/h4_worktree.py` | `5f0003688c13d9cf93d232a9007d19970613003d8b73e0b6472c2a28094baed9` |
| `receipts/envelope.txt` | `f3725e1b92657649fa3bf311e94af4502430bf75016cdedfb5d5fbf16cb5d2c2` |
| `receipts/matrix.txt` | `ae6c78df54ac769ff524622e56816d8356e5d893abac8c8181bc35addd9fdc94` |
| `receipts/controls.txt` | `c775d1246f082aba048ee349ae8bcf2d6aa724ed19ac119e2d1b8aae7ada5007` |
| `receipts/full-copy.txt` | `a1afe348299da2626256ea52f90164a7c320bcd7b53a42b2c71f3fb7ade652d2` |
| `receipts/full-frozen.txt` | `6f6b3abe66448632132f33114251fdbd57d81dccf0a03dd81adacc266651e2d4` |
| `receipts/segment-compare.txt` | `3329ee7a4c09621c8232bf1089611058a7fa04ee47a90b5cd07aed8c747530ee` |
| `receipts/c1_gpg_controls.py` | `b1e7401922b09d98235bc348d85be051b19ce9124a8957b26d65810f19995391` |
| `receipts/c4_worktree_control.py` | `e438856d40465899fa17c302dce2a2ca26d085a1e6f25d65d593b00a44698bed` |

Reproduce: clone `508434ad5…` to `$S/lane`, then
`bwrap … python3 <copy> --lane $S/lane --work $S/w --jobs 8` (§3) and
`bwrap … python3 <frozen|copied> --lane $S/lane --battery-dir $S/bat-<module> --only XO1 --work $S/w2 …` (§2).
Toolchain: `bubblewrap 0.13.1`, `git 2.56.0`, `python 3.14.8`.

VERDICT: hardened-copy-battery42-14/14-repairs-biting-4/4
