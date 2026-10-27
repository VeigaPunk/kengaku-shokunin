# R45RevengerOrder — why `lane_breach` sits before `repo_breach`, and what a filesystem-first chain costs

Seat R45RevengerOrder (revenger), kengaku round 45 wave 1 (build), hyaku run 9, 2026-10-26. Report only: no lane
file was edited, no frozen file touched, no counter/fixture/probe run outside the envelope.
Lane repo `kengaku-shokunin` (state at freeze `b4fcd351`; the files cited are the frozen round-42/43/44 counters and
the round-42/43/44/45 wave reports, all read-only).

Scope: `plans/round44_c1_verify.py:758-759` (`build_battery`'s fence chain) versus `plans/round43_c1_verify.py:691-692`,
traced back through `plans/round42_c1_verify.py` (which has no fence legs at all) and the wave reports
`R42CritC1Counter`, `R43SentinelCounter`, `R44SentinelFences`, `R44LabratLaneInclude`, `R44MutC1Fences`,
`R44MutC1Guards`, `R44PlanNext`.

## Axes (godspeed)

- **origin clarity** — can the chain's position be attributed to a written decision, or is it an inheritance?
- **behavioural delta** — does moving the pure-filesystem legs first change any admit/refuse decision?
- **cost delta** — does it change outside opens, hangs, or crashes (the three non-decision effects of a chain)?
- **obligations** — what must a fs-first fence carry that the old order carried implicitly?

## 1. Reconstructed contract (what the chain actually is)

`plans/round44_c1_verify.py:758-759`:

```
breach = argv_shape_breach(fx["tool"], argv) or lane_breach(d, argv) or repo_breach(d) or symlink_breach(d) \
    or (order_argv_breach(d, argv) if fx.get("tool") == "order" else None)
```

Five legs, short-circuited by `or`, evaluated once per fixture the module built. A leg returns a reason string
(refusal) or `None` (admit); the chain's value becomes `SETUP … escapes its directory: <reason>` (`:760-762`). The
legs differ in *what they look at*, and that is the only thing the position can matter to:

| leg | line | sees | side effects |
|---|---|---|---|
| `argv_shape_breach` | `:538` | argv tokens only (syntax) | none |
| `lane_breach` | `:573` | repo adopted from `--lane` by **git's own discovery, no ceiling** (`:586-592`) | spawns 2 unbounded `git` children |
| `repo_breach` | `:475` | `os.walk(d)` (no depth cap, `:486`), `.git` file/symlink (`:490-491`), alternates, `--local --no-includes` config, bounded `rev-parse`, `core.worktree` (`:505,:512,:517`) | spawns bounded `git` children (`pin_git`, ceiling `d.parent`) |
| `symlink_breach` | `:527` | `lstat` over `d` | none |
| `order_argv_breach` | `:556` | `--claims`/`--receipt` as blobs at HEAD of `--lane` | spawns 2 bounded `git` children |

Provenance of the position, in commit order:

- `bc856d8` (round-42 freeze): **no** fence legs exist; `grep -c breach plans/round42_c1_verify.py` = 1 (prose).
  The leg is born as a *finding*: `R42CritC1Counter.md:87` §V1b, `:102` "`order_check.main` trusts `git rev-parse
  --show-toplevel` (`order_check.py:152`) and resolves the argv".
- `02753f2` (round-43 freeze): the first three legs, **git before filesystem** — `round43_c1_verify.py:691-692`
  `repo_breach(d) or symlink_breach(d) or (order_argv_breach …)`.
- `5f16ed0` (round-44 freeze): `round44_c1_verify.py` is a new file; `argv_shape_breach` and `lane_breach` are
  prepended, producing the chain above at `:758`.

## 2. Was the ordering chosen to let discovery see what the tool sees? (the "named" origin)

**Partly, and the docstring's claim is not the reason.** Two separate statements have been fused:

1. **The method claim.** `lane_breach`'s docstring (`:573-578`): the repo "found by git's own discovery, with no
   ceiling below the host root, **exactly as the tool run discovers it** up to its scratch-root ceiling". This
   justifies *running git unbounded* inside that leg. It says nothing about where the leg sits in the chain.
2. **The ordering rationale.** `R43SentinelCounter.md:110-114` (§F2 "Smallest remediation"): "Do not enumerate a
   tree: derive the repos from the argv the fixture returned … **keep the walk only as a secondary sweep**". The
   round-44 author implemented that sentence literally *as an order*: the argv-derived leg (`lane_breach`, F2/F6)
   before the tree walk (`repo_breach`). F2 was HIGH ("`repo_breach` skips any repo deeper than three levels"),
   cause `round43_c1_verify.py:475` `if depth >= 3: dirs[:] = []`.

So the **named origin is `R43SentinelCounter` F2's "secondary sweep" split** — argv-derived view first, the
counter's own enumeration second — carried into `:758` at the round-44 freeze. It was *not* argued as
"discovery sees what the tool sees": the same report's F6 (`:205`) is about `PIN_CHECK_ENV`, and the counter's own
claim is falsified by the round-44 data-walk: `R44PlanNext.md:108-111` measures that the no-ceiling call is the
*opposite* of the tool's view ("the tool run's ceiling is the scratch root, so discovery from inside it cannot see
an ancestor repo") and calls it a defect that makes a non-repo `--lane` fixture "environment-dependent"
(`SETUP … --lane rev-parse --show-toplevel=…/repo is outside the fixture`, exit 2).

## 3. What the order was protecting, and what it cost (measured)

The chain is a monotone `or`: every leg runs until one fires, so **the position cannot change an admit/refuse
decision** — only (a) which reason is reported, (b) side effects, (c) exceptions. All three are documented:

**(a) Reason/credit — real and measured.** `R44MutC1Fences.md` rows: RB1 "`lane_breach`'s `--absolute-git-dir` half
fires first (f1 is double-covered)"; RB4 "`lane_breach`'s rev-parse follows the FIFO include and its own 30 s
timeout refuses"; RB5 "f2's escape is refused by `lane_breach` before `repo_breach` runs" → **survived**;
`R44MutC1Guards.md:78` "the round-44 hostile refusals for f1/f2/f4/f6 come from `lane_breach` (which runs before
`repo_breach`); `repo_breach`'s toplevel branch is never reached"; `:131-133` "…refused by `lane_breach` before
`repo_breach`; … (not constructible with the round-44 breach order — named as a limit)". The order made three of
`repo_breach`'s branches **undemonstrable** — a demonstration loss the order caused, not protected.

**(b) Side effects — the order's actual price, measured by the frozen round-45 control.** `claims/control-c1-fence-r44.txt`
(r44 fence as the fence, per-module `opens=` = successful outside opens):

```
REFUSAL f1_gitfile.py READ fixtures=1 admitted=0 hung=0 opens=6
REFUSAL f4_fifo.py READ fixtures=1 admitted=0 hung=0 opens=1
REFUSAL f6_above.py READ fixtures=1 admitted=0 hung=0 opens=3
REFUSAL f10_laneinclude.py READ fixtures=1 admitted=0 hung=0 opens=4
REFUSAL f2_deep.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f3_abbrev.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f5_alternates.py clean fixtures=1 admitted=0 hung=0 opens=0
CALIBRATION advertised=10 contradicted=7
```

The split is exactly along the chain: every `opens>0` refusal is one whose deciding leg **runs git discovery**
(`lane_breach`; and the include/worktree-config reads it drags in — `R44LabratLaneInclude.md:20-21` "lane_breach
therefore runs before `repo_breach`"; `:145-148` "the parent read the outside file? Yes … Is it before
`repo_breach` refuses the include? Yes"), while the three clean ones decided from **filesystem state or argv**
(alternates file, shape, local config value). f1 is the sharpest datum: `repo_breach`'s pure filesystem `.git`-FILE
check (`:490-491`) would have refused it with `opens=0`, but `lane_breach` refused it first with `opens=6`. The
order *selected the noisy detector when a silent one already existed downstream.*

**(c) Exceptions — the one ordering dependency the later design must keep.** `argv_shape_breach` first is not
decorative: `lane_breach` and `order_argv_breach` both parse `dict(zip(argv[0::2], argv[1::2]))` (`:578,:561`) and
`order_argv_breach` indexes `vals["--claims"]`/`vals["--receipt"]` (`:565`). Row AS1 in `R44MutC1Fences.md`: with
the shape leg off, f3 "REFUSED by accident — `SETUP '--claims'` (the `vals[opt]` KeyError in `order_argv_breach`),
not by the guard"; AS2: an unknown anchor token KeyErrors at `ANCHOR_OPTS[t]` (equivalent-null). A raise inside
`build_battery` becomes a `SETUP` exit 2, not a per-fixture refusal.

## 4. Does filesystem-first lose any behaviour the order was protecting? — measured, no

Probe `p_order.py` (below) built the f6 shape by hand (repo at `d.parent`, `d/sub/claims.md` committed) and called
the frozen legs directly, and replayed the abbreviated order argv through the frozen chain:

```
P1a unbounded  rev-parse --show-toplevel -> (0, '…/p1/par', '')
P1a ceiling=P  rev-parse --show-toplevel -> (128, '', 'fatal: not a git repository (or any of the parent directories): .git')
P1a ceiling=P  rev-parse --absolute-git-dir -> (128, '', 'fatal: not a git repository …')
P1b the fence legs on that fixture, both chain orders:
    repo_breach(d)   = None
    lane_breach(d,a) = '--lane rev-parse --show-toplevel=…/p1/par is outside the fixture'
    r44 order  (lane or repo) = '…is outside the fixture' | swapped (repo or lane) = '…is outside the fixture'
P2 shape-before-parse precondition, abbreviated order argv:
    argv_shape_breach(order, ab) = "order argv is not the contract shape ['--lane', '--claims', '--receipt']: …"
    order_argv_breach(ab) raises KeyError: '--claims'
P3 honest control: repo inside d, ceiling=d.parent:
    repo_breach(d) = None
```

- **f6 (repo above d).** `repo_breach` alone admits it (walk finds no `.git` under `d`); `lane_breach` refuses it.
  Swapping the two legs yields the **identical string** — the position is decision- and message-neutral for this
  class. What *does* preserve f6 under a fs-first fence is the round-45 rule "rc != 0 from a store/lane probe is a
  breach, never clean" (`plans/round-45-claims.md` §C1 design; `R44LabratLaneInclude.md:157` §5.3 "Treat a
  non-zero exit from any parent-side git as a breach"), because with `GIT_CEILING_DIRECTORIES=d.parent` the
  ancestor repo makes discovery fail `rc=128` (P1a) — under round 44 that `rc != 0` was silently "clean" at
  `:512`.
- **Honest side.** All 104 battery fixtures' `--lane` names a repo the fixture itself inits (`grep -rhn '"--lane"'`
  over `plans/battery42|43|44`: only `str(r)`, `str(repo)`, `"."`, each preceded by `ctx.init`), so the
  `rc != 0` = breach rule cannot refuse them on a valid discovery (`rc=0`, toplevel under `d`; P3). No honest
  fixture relies on an ancestor `.git`: `grep -rn "gitdir:|separate-git-dir|commondir|worktreeConfig|symlink"`
  over the three batteries returns nothing.
- **The legs a filesystem-first fence cannot replace.** f9 (`core.bare=true`, `rev-parse` exits non-zero) is
  invisible to `.git`-presence walks — `plans/refusals45/f9_nodescribe.py` docstring: "guards every check with
  `rc == 0` … THE round-45 fence treats `rc != 0` from any of its git probes as unverifiable". Its refusal
  therefore *requires* the git legs to still run second: pure-filesystem legs are additive, not a replacement.
  f7/f8 (`refusals45/f7_commondir.py`, `f8_worktreecfg.py`) conversely need a **text** scan of `.git/commondir` and
  `.git/config*` before any git call — the frozen round-45 design names both as filesystem legs.

## 5. Obligations the old order carried implicitly (for the fence author, wave 1)

1. **The syntax leg stays first.** `argv_shape_breach` must precede every argv-consuming leg, else an abbreviated
   order argv raises `KeyError('--claims')` (P2; AS1) instead of being refused — `build_battery` turns that into a
   `SETUP` (exit 2), and the round-45 counter counts it as not-clean. "Pure-filesystem legs first" must not be read
   as "argv reading may come before argv validation".
2. **A leg must return a string, never raise.** The chain's contract (`breach -> str | None`) is what makes
   reordering safe; a fs leg that raises on a malformed `.git/config` (f8's `[include]` text, continuation lines —
   `R44LabratLaneInclude.md:157` §5.1) converts a clean refusal into a crash.
3. **`rc != 0` = breach, not clean**, for the second-tier store/lane probes — the single change that preserves f6
   and f9 without any unbounded call.
4. **The argument for filesystem-first is the opens column, not the decision column** (`control-c1-fence-r44.txt`:
   f1 6→0, f6 3→0, f10 4→0). Any claim that the reorder changes verdicts would be false.

## 6. Divergences found (code vs. its own documents)

| # | where | what |
|---|---|---|
| D1 | `round44_c1_verify.py:573-578` | "no ceiling below the host root, exactly as the tool run discovers it" — the tool run *has* a scratch-root ceiling; `R44PlanNext.md:108-111` measures the deviation (refuses an honest non-repo `--lane` fixture when the scratch sits in a repo). |
| D2 | `:758` position vs `R43SentinelCounter.md:110-114` | F2 asked for argv-derivation *instead of* the walk; round 44 kept both and expressed the request as precedence, with no document arguing the position. |
| D3 | `R44MutC1Fences.md` RB5 / `R44MutC1Guards.md:78,131-133` | the order leaves `repo_breach`'s toplevel and containment branches unreachable for every round-44 hostile → those guards are undemonstrated (survived mutants), a demonstration defect the round-45 fs-first chain will *not* fix by itself (it adds masking pressure on the git legs from the other side). |
| D4 | `:565` `vals[opt]` | `order_argv_breach` cannot be called without a prior shape verdict; the dependency is implicit in the chain, not in the function. |

## 7. Limits of this evidence

- My probe called the frozen legs in-process on one hand-built fixture and replayed one abbreviated argv; it did
  not build any `refusals45` module (the counter's own builder is a frozen subprocess protocol — the round-45
  counter and its executors own that measurement). `repo_breach`/`lane_breach` were imported read-only; no lane
  file changed.
- Origin is attributed from the round-42/43/44 reports and the freeze commits; the round-44 freeze commit is an
  initial import of `round44_c1_verify.py`, so no intra-file reorder exists in git history to inspect — the
  position can only be attributed through `R43SentinelCounter` §F2 and the round-43 chain it replaced.
- "Behaviour lost" is answered over the classes the frozen fixtures cover (f1–f10, 104 honest). Hostile classes no
  battery builds (e.g. nested includes beyond depth 2, `R44LabratLaneInclude.md:163` limit) are unmeasured here.

## 8. Receipts

`R45RevengerOrder/receipts/p-order.txt` (probe output, 2124 B, sha256 `88e8a87f69429d19e95f57b3470cff144c2404f98afcfcedbca40400f4616381`),
`R45RevengerOrder/p_order.py` (probe source, 3587 B, sha256 `de72f772bcd40ec8e7d012ec4ce91ee5f59c36b33fb0eba9985d9c0293f90cb4`).

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45RevengerOrder/env /fast/scratch/hyaku/kengaku-r45/R45RevengerOrder/env --bind /fast/scratch/hyaku/kengaku-r45/R45RevengerOrder/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r45/R45RevengerOrder/p_order.py /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r45/R45RevengerOrder/p1
ENVELOPE start 23:28:35 cwd=/fast/scratch/hyaku/kengaku-r45/R45RevengerOrder
…
ENVELOPE end 23:28:37 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

All other numbers carry their command inline (`grep -c`, `git show 02753f2:…`, `git log -S`, `grep -rhn '"--lane"'`,
`sed -n` ranges), and the reports/controls cited are read-only files of the lane. Scratch
`/fast/scratch/hyaku/kengaku-r45/R45RevengerOrder` removed at end of seat via `plans/scratch_guard.py safe-rm`.
No tool was installed.

VERDICT: order-origin-r43sentinel-F2-secondary-sweep-behaviour-lost-no
