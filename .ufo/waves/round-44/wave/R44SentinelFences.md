# R44SentinelFences — attacking the round-44 store fences F1–F6

Seat R44SentinelFences (sentinel, leaf), kengaku round 44 wave (build + attack, v2). Scope as assigned: the five
fence functions of `plans/round44_c1_verify.py` (`pin_git` :462, `repo_breach` :475, `argv_shape_breach` :538,
`order_argv_breach` :556, `lane_breach` :573), compared against `plans/round43_c1_verify.py` and
`.ufo/waves/round-43/build/R43SentinelCounter.md`, plus the build-time refusals they feed (:758). Frozen files
read only; the counter and both tools are unmodified (every run prints `PINS total=2 mismatched=0`,
`PINS-AFTER mismatched=0`). Every fixture was built in my scratch `/fast/scratch/hyaku/kengaku-r44/R44SentinelFences`
from nothing (`git init` inside the counter's own sandbox); the lane used for the counter is my shared clone and
`git -C <clone> rev-parse --show-toplevel` printed that clone. No vector names a real host path as a target; the
one absolute-target probe (C below) names only that clone's own `.git`, read-only. Every run below is bracketed by
`claims/envelope.sh` (PATH-dir content digest `328be01808ba022f` before and after every run — unchanged, so no
measurement is invalid). Nothing installed or upgraded.

## Bottom line

Three of the six repairs are bypassed as controls. All three bypasses are **admitted modules** (`no SETUP`, no
`wrong`): the fences' literal rules hold while the property they exist to enforce — *the measured repository lives
inside `d`* — does not.

| Repair | Verdict | One-line reason |
|---|---|---|
| F1 `.git` is a directory, `--absolute-git-dir` inside `d` | **bypassed** | a hand-written `.git/commondir` keeps both answers inside `d` and sends refs/objects/config elsewhere (V1) |
| F2 no depth cap | holds | repo nine levels down with an outside worktree refused (N1) |
| F3 exact argv shape | holds | `--claim` abbreviation refused before any git call (N2) |
| F4 30 s timeout, no stdin | holds | FIFO include blocked one call, refusal after 33 s wall, nothing hung (N3) |
| F5 `--no-includes`, include and alternates refused | **bypassed** | the second repo config file is invisible to both config calls, so an include outside `d` is parsed by every other git call (V2); with a commondir the "local" config and the alternates check are looked for in the wrong tree (V1) |
| F6 repo discovered from `--lane` inside `d` | **bypassed** | toplevel and git dir answer inside `d`; the store they delegate to is outside (V1) |

A fourth, smaller class: every store check is guarded by `rc == 0`, so a repository git refuses to describe is
reported as *no breach* rather than *unverifiable* (V3).

## V1 — HIGH — `.git/commondir` delegates the store outside `d`; both fences pass, both tools decide from it

**Line:** `plans/round44_c1_verify.py:475-524` (`repo_breach` inspects `.git` itself, `objects/info/alternates`,
the local config and two `rev-parse` answers; it never resolves git's *common* dir); `:573-595` (`lane_breach`
asks the same two questions). Git's linked-worktree mechanism (`$GIT_DIR/commondir`) is unchecked.

**Exploit path.** Build a repo whose git dir is `d/lane/.git` — a real directory, so F1's file/symlink refusals do
not fire — and write `commondir` naming a repository built *beside* `d`. `rev-parse --show-toplevel` answers
`d/lane` and `--absolute-git-dir` answers `d/lane/.git`; HEAD, refs, objects and config are then read from the
outside store. No symlink, no alternates file, no include in the inspected config. The build path needs no sandbox
escape: the build child's root *is* `d`'s parent (`round44_c1_verify.py:276` `self._root = ...`, writable bind at
`:734` `writable=(dest, tmp)`), so `ctx.init(d.parent/...)` is inside the sandbox's writable set — the same shape
round 44's own `claims/hostile/f5_alternates.py` and `f6_above.py` already use.

**Admitted modules** (`b_commondir.py`, copied beside this report; `:28` order fixtures, `:55` anchor fixture):

```
$ python3 plans/round44_c1_verify.py --lane "$S/lane" --battery-dir "$S/bat_main" --only U5,U14c --work "$S/w8"
PINS total=2 mismatched=0
FIXTURE cd-accept tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE cd-reject tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE cd-anchor tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE wtcfg-include-outside tool=order expect=accept declared=- observed_rc=0 observed=- ok
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=0 survived=2 ... PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE start 20:46:49 ... ENVELOPE end 20:46:51 exit=1 local_bin_content_before=328be01808ba022f
  after=328be01808ba022f unchanged
```

`cd-accept` and `cd-reject` have the **same `d` shape** — `d/lane` holding only `.git/HEAD` and `.git/commondir` —
and opposite verdicts, decided solely by which outside store the commondir names. `cd-anchor` runs the anchor tool
with no `--lane` at all, so `lane_breach` never runs; `repo_breach` walks `d`, finds the git dir, and passes it.

**What the counters' own calls and the tools read (hand-built, same shape, `probe4.py`):**

```
"to": [0, ".../p4/fx/mod/f000/lane", ""]                       # rev-parse --show-toplevel  -> inside d
"gd": [0, ".../p4/fx/mod/f000/lane/.git", ""]                  # rev-parse --absolute-git-dir -> inside d
"log": [0, "e60f4d69... receipt\n3a65620f... claims", ""]      # both commits live outside d
"ls_tree": [0, ".ufo/waves/round-42/claims/round-42-claims.md\ncorpus/evidence/round42/receipt.txt", ""]
"cat": [0, "blob", ""]                                         # cat-file -t HEAD:receipt (order_argv_breach's call)
"store_config_via_parent_shape": [0, "STORE-MARKER@invalid", ""]  # config --local --no-includes --get user.email
"d_lane_files": ["lane/.git", "lane/.git/HEAD", "lane/.git/commondir"]
"order_check": [0, "ORDER claims=... freeze=3a65620f... \nORDER receipt=... \nORDER ok no claims file ...", ""]
ENVELOPE end 20:43:55 exit=0 ... unchanged
```

So the store fence's own `config --local --no-includes --get` and `cat-file` calls answer from a config and an
object store outside `d`, and the tool's verdict (`ORDER ok`, `rows=0 tokens=0 defects=0` for the anchor fixture,
`probe7.py`) is computed from them.

**An absolute commondir reaches any git dir on the host** — `probe5.py` §c, target = this clone's `.git`:

```
"c_commondir_absolute": {"show_toplevel": [0, ".../f003/lane"], "absolute_git_dir": [0, ".../f003/lane/.git"],
 "common_dir": [0, "/fast/scratch/hyaku/kengaku-r44/R44SentinelFences/lane/.git"],
 "cat_file_lane_head": [0, "blob"], "log_head": [0, "round-44: v2 wave spec + validated dispatch (68 seats)"]}
ENVELOPE end 20:42:32 exit=0 ... unchanged
```

**Impact.** F1/F5/F6's stated rules all hold and the store is still outside `d`: a fixture can serve its whole
history, its config and its blobs from a directory it did not build in `d`, share one store between fixtures (all
fixtures of a module share `dest`), or point the parent process at any repository on the host. `wrong=0` stops
implying the scenario lived in `d`.

**Smallest remediation.** After `--absolute-git-dir`, also require `rev-parse --git-common-dir` (and
`--git-path objects`) to resolve inside `d`, and refuse a `.git/commondir` file outright — the module contract
builds every repo in `d`, so no fixture needs one. Then the alternates/include checks must run against the resolved
common dir, not against `repo/.git`.

## V2 — MEDIUM — the second repo config file carries an include outside `d`; both fence config calls miss it

**Line:** `plans/round44_c1_verify.py:502` and `:517` — `config --local --no-includes`; `--local` reads
`.git/config` only, so a repository with `extensions.worktreeConfig` enabled has a second config file
(`.git/config.worktree`) that neither call sees, while every other git call (including the fence's own `rev-parse`
at `:513`) parses it and follows its includes.

**Exploit path.** `git config extensions.worktreeConfig true`, then `.git/config.worktree` =
`[include]\n path = <file outside d>`. Admitted module `b_wtcfg.py` (beside this report):

```
$ ... --battery-dir "$S/bat_main" --only U5,U14c   (same run as V1)
FIXTURE wtcfg-include-outside tool=order expect=accept declared=- observed_rc=0 observed=- ok
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
ENVELOPE end 20:46:51 exit=1 ... unchanged
```

**The fence calls miss it and every other git call parses it** (`probe5.py` §a/§a2, `probe6.py` §2; PIN-check env,
same argv shape the counter uses):

```
"a_second_config": {"fence_scan": [1, "", ""], "fence_worktree": [1, "", ""],
  "any_parse": [0, "OUTSIDE-MARKER@invalid", ""], "lane_rev_parse": [0, ".../f000/lane", ""]}
"a2_second_config_worktree": {"fence_scan": [1, "", ""],
  "rev_parse": [0, ".../fx/mod/outside-wt", ""]}        # value exists only in the outside include
ENVELOPE end 20:42:32 exit=0 ... unchanged
```

`a2` is the decisive row: `rev-parse --show-toplevel` prints a worktree path that is written **only** in the
included file outside `d`, so that file was parsed by the fence's own call while `fence_scan` returned `rc=1`
empty. The same include is parsed by `order_argv_breach`'s `cat-file -t` and by the tool run.

**Impact.** F5's sentence "no file outside `d` is parsed" is false: an outside file is parsed by every parent-side
git call except the two config calls, and any config key not in the four R1 pins can be injected into the parent's
git decisions (a key that changes an answer — `core.worktree`, `core.bare` — is caught or falls into V3; harmless
read-channel keys are not). It is a leak of outside-`d` state into the counter's own process, and it makes the
fixture's behaviour depend on a file the fence never inspected.

**Smallest remediation.** Read the repository config scope completely instead of one file: e.g.
`git config --list --show-origin --show-scope` and refuse any origin outside `d` plus any repo-scoped `include*`
key, or refuse `extensions.worktreeConfig` outright when `.git/config.worktree` exists.

## V3 — LOW/MEDIUM — a repository git refuses to describe is reported as *no breach*

**Line:** `plans/round44_c1_verify.py:505`, `:512`, `:520` and `lane_breach:592` — every check is guarded by
`rc == 0`; a non-zero return code is treated as "nothing to see" instead of "unverifiable".

**Exploit path (a):** `.git/config` includes a file outside `d` that is not valid config. All fence-shaped calls
abort, so every check is skipped; the fixture is admitted and the tool's own setup fails (exit 2, a declared
`expect=error`), so `wrong=0`.

```
$ ... --battery-dir "$S/bat_fail" --only U14c --work "$S/w3"
FIXTURE broken-include-admitted tool=order expect=error declared=- observed_rc=2 observed=- ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
ENVELOPE end 20:44:10 exit=1 ... unchanged   (real 0m3.109s)
```

The outside file was nevertheless **opened and parsed** — the same calls with the same env (`probe6.py` §1):

```
"malformed_include": {
 "rev_parse": [128, "", "fatal: bad config line 1 in file .../p6/fx/mod/broken.cfg"],
 "absolute_git_dir": [128, "", "fatal: bad config line 1 in file .../p6/fx/mod/broken.cfg"],
 "config_scan": [128, "", "fatal: bad config line 1 in file .../p6/fx/mod/broken.cfg"]}
ENVELOPE end 20:44:32 exit=0 ... unchanged
```

**Exploit path (b):** a bare-shaped config (`core.bare=true`) gives `rev-parse --show-toplevel` = 128,
`--absolute-git-dir` inside `d`, config scan = 1 (`probe6.py` §3) — again admitted, tool exit 2.

**Impact.** The fence's verdict "no breach" covers two very different states: a repository it proved clean and a
repository it could not read at all. A fixture can therefore be admitted with an arbitrary config while the
outside-`d` file it names has already been parsed.

**Smallest remediation.** Treat `rc != 0` from any of these calls as a SETUP refusal ("unverifiable repository"),
not as a pass.

## Attacked and holding (negative controls, same envelope)

N1 (F2, no depth cap) — repo nine levels down, worktree outside `d` (`b_neg_depth.py`):

```
SETUP fixture 'deep-nine' ... escapes its directory: --lane rev-parse --show-toplevel=.../b_neg_depth/outside-wt
  is outside the fixture
ENVELOPE start 20:46:16 ... ENVELOPE end 20:46:17 exit=2 ... unchanged
```

N2 (F3, exact argv) — `--claim` abbreviation naming a directory at HEAD (`b_neg_shape.py`):

```
SETUP fixture 'abbrev-claim' ... escapes its directory: order argv is not the contract shape
  ['--lane', '--claims', '--receipt']: ['--lane', '.../f000/lane', '--claim', 'plans/round-7-claims.md', ...]
ENVELOPE start 20:46:19 ... ENVELOPE end 20:46:20 exit=2 ... unchanged
```

N3 (F4, 30 s timeout) — two fixtures whose `.git/config` includes a FIFO **outside `d`** (`b_fifo.py`). The
argv fence runs first, follows the include, and blocks; the refusal costs one 30 s timeout and the run ends:

```
SETUP fixture 'fifo-a' of bat_fifo/b_fifo.py escapes its directory: --lane git hung
ENVELOPE start 20:44:31 ... ENVELOPE end 20:45:02 exit=2 ... unchanged
real 0m32.990s
```

F4 therefore holds (a hang is a refusal, not a stall): the fenced pass is bounded at ~30 s because `build_battery`
stops at the first refused fixture.

## Checked and clean (no finding)

| Vector | Measurement |
|---|---|
| symlink escape / `.git` symlink | `symlink_breach:527` + `repo_breach:498` refuse both; no variant found that is adopted |
| `.git` as a FILE, FIFO, or dangling entry | refused (`:490`); `probe3.py` confirms the hand-built escape needs a directory |
| case-varied `[Include] Path` key | still listed by `--get-regexp` (`probe2.py` §b, `include.path ... outside.cfg`) — no bypass |
| relative vs absolute commondir | relative is resolved against the git dir; both forms reach outside `d` (V1) — no additional finding |
| `core.worktree` outside `d` (direct config) | caught: `--lane rev-parse --show-toplevel=…/no-such-wt is outside the fixture`, SETUP exit 2 (20:42:04 run) |
| `core.worktree` from an include (primary config) | git does **not** honour it for `rev-parse` (`probe6.py` §2: still `.../lane`, `worktree_read` rc 1) |
| `K44_SPAN`, tracer env, `R1` pins | unchanged from round 43; not touched by any vector here |

## Limits

The threat model is a `plans/battery44` author, not the pinned tools; every vector needs a fixture. I did not test
cross-`--work` state, a hostile `TMPDIR`, jj state, or anything needing a different uid. V1's absolute-target
variant was measured only against my own clone (no real host path was named as a target); the generalization to
"any absolute git dir" is direct (`probe5.py` §c resolved the path and printed the clone's tip subject), not
separately measured against a third-party repo. The `commondir` file is not in `SIDECHANNEL`; a module can build
it and still pass the token scan, and my `b_commondir.py` did (`sidechannel=0`).

## Reproduction

Beside this report: `b_commondir.py` (`sha256 ce078146…`), `b_wtcfg.py` (`d72314ff…`), `b_incfail.py` (`7d39caf2…`),
`b_fifo.py` (`a39b8531…`), `b_neg_depth.py` (`d4a76e0f…`), `b_neg_shape.py` (`b13487df…`), `probe4.py`
(`cdff3742…`), `probe5.py` (`94b63269…`), `probe6.py` (`7054d2a5…`), `probe7.py` (`6872cada…`). Each needs
`S=/fast/scratch/hyaku/kengaku-r44/R44SentinelFences`, a `"$S/lane"` clone of the lane, and the envelope:
`claims/envelope.sh "$S/env" python3 "$S/lane/plans/round44_c1_verify.py" --lane "$S/lane"
--battery-dir "$S/<dir>" --only U5,U14c --work "$S/w"`.

Envelope log (start–end, exit, PATH-digest before/after — all `unchanged`): probe1 20:36:23–20:36:24 exit=0;
probe2 20:36:22–20:36:24 exit=0; probe3 20:37:34–20:37:36 exit=0; probe4 20:43:54–20:43:55 exit=0; probe5
20:42:31–20:42:32 exit=0; probe6 20:44:31–20:44:32 exit=0; probe7 20:46:28–20:46:30 exit=0; counter
(bat) 20:42:04–20:42:06 exit=2; counter (bat_main) 20:43:54–20:43:56 exit=1; counter (bat_fail) 20:44:08–20:44:10
exit=1; counter (bat_fifo) 20:44:31–20:45:02 exit=2; counter (bat_main, final) 20:46:49–20:46:51 exit=1; N1
20:46:16–20:46:17 exit=2; N2 20:46:19–20:46:20 exit=2. All digests `328be01808ba022f` unchanged.

VERDICT: fence-bypasses-3-of-6
