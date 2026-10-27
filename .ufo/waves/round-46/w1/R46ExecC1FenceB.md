# R46ExecC1FenceB — repaired `plans/fixture_fence.py`, variant B (no git; store parsed from its own bytes)

Seat: executor, kengaku round 46 wave 1 (`/skill:godspeed`). Lane measured through a `git clone -q --shared` at
`/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceB/lane` (`git -C … rev-parse --show-toplevel` printed that path,
HEAD `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`, fence at base `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`
= round-45 landed bytes). The lane itself was never written, no jj/git command ran there, no commit was made anywhere.

**Deliverable (for the L1 to land):** `.ufo/waves/round-46/w1/R46ExecC1FenceB/fixture_fence.py`,
sha256 `8537a9e846e7e88b128d3f239c7ed9d3c9bf500e41a1be5b1f2d026951f14794`, 919 lines, stdlib only
(`hashlib, os, pathlib, posixpath, re, stat, zlib`), no `subprocess`, no `git`, no writes, no stdout.

## 1. Headline

| measurement | command | observed |
|---|---|---|
| round-45 C1 counter, my clone | `envelope.sh "$S/env4" python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/w6" --jobs 8` | `PINS total=33 mismatched=0`, `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=10 contradicted=0`, **`PREDICATE C1 pass`**, exit 0 |
| 5 round-45 held-out families, 11 modules, 31 fixtures | the five `R45Ho*` drivers, pointed at the clone (§3) | **31/31 fixtures `BREACH`, 0 admitted, 0 outside opens, 0 hung**; every module `clean` |
| whole-`%file` trace (B5 channel: stat/readlink/access/execve) | `filetrace_probe.py` on 9 fixtures | `classes=execve,newfstatat,open,openat,readlink`, `outside=0` on every fixture |
| order leg at HEAD (`--claims`/`--receipt`) | `claims_probe.py` | tree-at-HEAD → `BREACH`; blob → `ADMIT`; absent receipt → `ADMIT`; packed-only store → `BREACH` (`order`) / `ADMIT` (`anchor`) |

Full counter receipt: `receipts-r45-counter.out` (sha256 `e53d921390ed45bcec455afacf304dbb7a0a2585503146f347682535fe49d724`).
Its brackets:

```
ENVELOPE start 02:08:09 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceB
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=8537a9e846e7e88b128d3f239c7ed9d3c9bf500e41a1be5b1f2d026951f14794
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 02:08:23 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

All four refusal rows print `opens=0` and all 104 honest rows print `ADMIT opens=0` (receipt lines
`REFUSAL …` / `FENCE-RUN honest …`). `local_bin_content_before=after` on every envelope, so no measurement is
`INVALID`. Only the frozen round-45 counter and the `R45Ho*` drivers were used; no draft of
`plans/round46_c1_verify.py` was opened or run, and nothing under `.ufo/waves/round-46/w1/` other than this seat's
own directory was read.

## 2. What the fence does (and why each round-45 bypass is closed)

Contract unchanged — `breach(d, argv, tool) -> str | None`, refusal = one line, `None` = admit. The design inverts
round 45's rule (`R45CriticPredicate`, per-module verdicts in `corpus/lessons/round-45-verifier-spotcheck.md` §2:
a denylist fence stayed unprovable while 8 of 10 held-out modules were admitted): **admit only what the fence can
parse itself and prove inert; refuse every other shape.** It never spawns a process, so nothing exists that could
open an include file, adopt a repo above `d`, or erase a strace log.

| rule | where | what it closes |
|---|---|---|
| no child process at all; no write, no stdout | whole module (`import` list, no `subprocess`) | B1 log erasure, B4 stdout spoof, B7 io_uring (no such syscall is issued), and f4/f10's include target is never opened |
| every stat/readlink/scandir is on a path built from `d` downward; symlinks are refused unfollowed | `_listdir` `fixture_fence.py:165` | R45HoSymlinks `objects`-symlink-out, `link-claims-symlink-out`, h3's `.git/inc.cfg` link; B3/B5 host and module-source reads |
| any regular file with `st_nlink != 1` is refused | `fixture_fence.py:187` | R45HoSymlinks `link-objects-hardlink-out` (the round-45 "coverage, not defect" survivor) |
| argv: exact option shape, plain tokens (no NUL/control/brace/leading `-`), values normalised **lexically** into `d` | `_argv` `:220`, `_lexical` `:136` | f3 abbreviations, R45HoArgvEnv's `{WORK}/../../outside`, embedded NUL (base raised `ValueError`, counted as admission) and extra tokens |
| `--lane` **must be a store root the fence validated** (a tool without `--lane` falls back to cwd = `d`, so `d` must be one too) | `breach` `:868` | f6 "repo above `d`": git discovery stops at the first `.git` walking up, so a validated root cannot discover above `d` — and the fence never needs an outside `lstat` to say so |
| `.git` entries from a closed inert set (`_STORE_DIRS`/`_STORE_FILES` `:87`); `commondir`, `modules`, `worktrees`, `config.*`, `branches/*`, `shallow`, grafts are simply not in it | `_store` `:751` | f7 commondir, R45HoCommondir2 g1/g3/g4 (hidden `modules/escape/.git/commondir` refused at `modules`), f8's `config.worktree`, f1 `/` g2 `.git`-file |
| `.git/config`: no BOM, no CR, no NUL, strict `[section]`/`[section "sub"]` + `key = value` grammar, no escapes, no dotted sections, and a **closed key table** (`_INERT_KEYS` `:72`) of keys that can name neither a path nor a program; subsections only `branch` | `_config` `:398` | f2 `core.worktree`, f4/f10 `[include]`, f8 `extensions.worktreeConfig`, f9 `core.bare=true`, R45HoConfigKeys `core.attributesFile`, every R45HoIncludeIf CR/BOM/`includeIf`/mixed-case variant, and any yet-unwritten key (allowlist, not denylist) |
| objects: loose files only in `objects/<2hex>/<38hex>`, each inflated and its `<kind> <size>` header checked against the payload; `objects/info` limited to `packs`/`commit-graph`; pack indexes parsed (v2 fanout + sorted id table) | `_loose` `:304`, `_pack_idx` `:345`, `_pack` `:372` | f5 `objects/info/alternates`; objects that are not objects |
| refs: only `refs/heads/**` and `refs/tags/**`, ref-name grammar, `ref:` chains hop-limited, every loose ref / `packed-refs` / `info/refs` id present in this store; HEAD resolves through `packed-refs` | `_refs` `:496`, `_packed_refs` `:528`, `_info_refs` `:557`, `_head_oid` `:717` | `refs/replace`, graft-by-ref, a packed branch pretending to be unborn |
| `.git/index`: `DIRC`, **v2 only**, every entry path proven repo-relative without `..`, trailer sha1 over the file, extension blocks that exactly consume it | `_index` `:452` | index shapes the fence cannot parse (split index, v4) |
| `order`: `--claims`/`--receipt` must be lane-relative and are resolved through HEAD's commit/tree objects read out of this store; a tree or gitlink at HEAD is refused, an absent path admitted | `_head_path` `:840` | the base's `cat-file -t HEAD:<path>` leg, without a git child |
| budgets: `FILES_CAP=20000` reads / `BYTES_CAP=64 MiB` per decision, `ENTRY_CAP`, `DEPTH_CAP=64`, `REPO_CAP=64`, `REF_HOPS=8` | `:64`, `:262` | a pathological fixture being answered late instead of refused (a `HUNG` fence is not a clean refusal) |
| any unexpected exception → refusal (`fail closed`) | `breach` `:868` | the counter counts `ERROR` as admission, so nothing may escape |

Q39 (the round-46 counter hides fixture names with a per-run token): no decision reads the fixture's name, its
parent's name, an absolute path prefix, a sibling count or the build order. `d`'s path appears only in reason
strings and as the equality key for `--lane`; the shape rules are name-free.

## 3. Per-held-out-module table (round-45 `R45Ho*`, run under the round-45 counter machinery)

Drivers: `R45HoArgvEnv/probe.py`, `R45HoCommondir2/driver.py`, `R45HoConfigKeys/probe.py` and the patched copy of
`R45HoSymlinks/run_probe.py` were given the clone as `LANE` (the symlinks probe hard-codes the lane, so it was
byte-copied to scratch with only that constant replaced); `R45HoIncludeIf` had no surviving driver, so
`includeif_driver.py` was written locally from the same prompt's contract (`build_module` + `run_fence`, the
round-45 detector). Every run: `envelope.sh "$S/env4" …`.

| family | module | fixtures | refused | admitted | outside opens | module verdict |
|---|---|---|---|---|---|---|
| R45HoIncludeIf | `h1_cr_include.py` | 2 | 2 | 0 | 0 | clean |
| R45HoIncludeIf | `h2_includeif_cond.py` | 9 | 9 | 0 | 0 | clean |
| R45HoIncludeIf | `h3_bom_symlink.py` | 4 | 4 | 0 | 0 | clean |
| R45HoIncludeIf | `h4_controls.py` | 3 | 3 | 0 | 0 | clean |
| R45HoSymlinks | `link_hostiles.py` | 5 | 5 | 0 | 0 | clean |
| R45HoArgvEnv | `argv_env.py` | 3 | 3 | 0 | 0 | clean |
| R45HoCommondir2 | `g1_cdrel.py` | 1 | 1 | 0 | 0 | clean |
| R45HoCommondir2 | `g2_gitfile.py` | 1 | 1 | 0 | 0 | clean |
| R45HoCommondir2 | `g3_wtmeta.py` | 1 | 1 | 0 | 0 | clean |
| R45HoCommondir2 | `g4_cdrel_hidden.py` | 1 | 1 | 0 | 0 | clean |
| R45HoConfigKeys | `configkeys.py` | 1 | 1 | 0 | 0 | clean |
| **total** | **11 modules** | **31** | **31** | **0** | **0** | **clean=11** |

Reasons actually printed (one line each, abridged to the first clause):

```
h1-cr-include-lf / -crlf, h2-inclif-* (all 9)   lane/config carries a carriage return
h3-bom-include / -bom-includeif                  lane/config starts with a byte-order mark
h3-cr-include-symlink                            lane/.git/inc.cfg is a symlink; the fence cannot prove it stays inside
h4-plain-inclif-onbranch / -gitdir-anchor        lane/config carries a [includeif "…"] subsection the fence does not admit
link-objects-symlink-out                         lane/.git/objects is a symlink; the fence cannot prove it stays inside
link-git-symlink-in / link-claims-symlink-out    lane/.git | lane/claims.md is a symlink; …stays inside
link-objects-hardlink-out                        lane/.git/objects/05/6b827f2… has 2 hard links; …none outside
link-include-chain-in                            inc1 is a symlink; …stays inside
argv-placeholder-lane-escape / argv-nul-lane     --lane value '{WORK}/../../outside' | 'lane\x00/…' is not a plain token
argv-extra-token                                 order argv is not the contract shape ['--lane','--claims','--receipt']
g1-cd-rel                                        repo/.git/commondir is a store entry the fence cannot prove inert
g2-gitfile-pad                                   lane/.git is a file (gitdir redirect), not a directory
g3-wtmeta-out                                    repo/.git/worktrees is a store entry the fence cannot prove inert
g4-cd-hidden                                     repo/.git/modules is a store entry the fence cannot prove inert
config-core-attributes-file-outside              lane/config sets [core] attributesfile, which cannot be proven inert
```

Receipts: `receipts-heldout-includeif.out` (`e5bec2b3…`), `…-symlinks.out` (`40591192…`), `…-argvenv.out`
(`7278566e…`), `…-commondir2.out` (`db1bc57c…`), `…-configkeys.out` (`b180122c…`). The config-key probe's own
`git check-attr` control still prints `marker: hostile: outside` — i.e. the fixture really does point git at a file
outside `d`, and the fence now refuses it without reading that file.

## 4. Extra design probes (not part of either counter)

**a. B5 channel, whole `%file` syscall set.** `filetrace_probe.py` traces `%file` (open/openat/newfstatat/stat/
readlink/access/getxattr/…/execve) in the round-45 sandbox and counts successful calls whose resolved path is under
the build scratch but outside `d`. Receipt `receipts-filetrace.out` (`2877215d…`):

```
FILETRACE a_class-x6-sibling-digest  verdict=ADMIT   successful=425 classes=execve,newfstatat,open,openat,readlink outside=0
FILETRACE a_class-x6-stale-manifest  verdict=ADMIT   successful=463 … outside=0
… (6 honest a_class fixtures, all ADMIT, outside=0)
FILETRACE f10-lane-include-regular   verdict=BREACH  successful=311 … outside=0
FILETRACE f2-deep-worktree           verdict=BREACH  successful=302 … outside=0
FILETRACE g4-cd-hidden               verdict=BREACH  successful=310 … outside=0
```

So the round-45 B5 objection ("stat/readlink/getxattr are never traced") is met by construction here: across
`newfstatat`, `readlink`, `open`, `openat` and `execve`, zero successes touch a scratch path outside `d` — including
f10, whose include target is a regular file beside `d`.

**b. The order leg.** `claims_probe.py`, receipt `receipts-claims-leg.out` (`7460dd8f…`):

```
CLAIMS-RUN ct-tree     tool=order  BREACH opens=0 -- --claims plans/round-7-claims.md is a tree at HEAD, not a blob
CLAIMS-RUN ct-blob     tool=order  ADMIT  opens=0
CLAIMS-RUN ct-absent   tool=order  ADMIT  opens=0
CLAIMS-RUN ct-packed   tool=order  BREACH opens=0 -- --claims: lane holds 674d04b0f0eb in a pack the fence does not decode
CLAIMS-RUN ct-packed-a tool=anchor ADMIT  opens=0
```

`ct-tree` is the case the round-44/45 fence answered with `git cat-file`; it is now answered from the store's own
commit/tree objects. The packed pair documents the limit in §5: a packed store is *validated* (idx parsed, refs
resolve) and admitted for `anchor`, but a `--claims` path that lives only inside the pack is **refused**, not
guessed.

## 5. Design limits (stated, not hidden)

1. **Packed objects are opaque.** `.pack` members are name-checked and paired with a parsed v2 `.idx`, but their
   payloads are never decoded. Any decision that needs an object body (order's claims path at HEAD) is refused when
   that object is packed. Consequence: `anchor` + packed store admits; `order` + packed store refuses when the
   claims path resolves through HEAD. The 104 honest fixtures are all loose.
2. **A `.git` above `d` is not detected** — detecting it needs an `lstat` outside `d`, which this variant forbids.
   It is made irrelevant instead: only a store root the fence validated can be the tool's repo (f6 stays refused).
   A tool that discovered a repo through some *other* argument than `--lane` would be outside the contract.
3. **Hard links are refused wholesale** (`st_nlink != 1`). This is deliberately over-strict: a second name on the
   inode cannot be proven inside `d`. A legitimate `git clone --local`-shaped fixture would be refused.
4. **Over-refusal is the design cost, and it is bounded to shapes the batteries do not build:** worktrees,
   `.git` files, submodules, symlinks, hardlinks, packed-only stores, index v3/v4/split-index, `extensions.*`,
   any config key outside the table (`remote.*`, `core.excludesFile`, `core.hooksPath`, `core.fsmonitor`, …), a
   sha256 object format, more than one refs subtree. Everything outside the 104 honest constructions is refused by
   default; that is the point of variant B.
5. **`info/refs`** is admitted only in `update-server-info` shape (`<oid>\t<ref>`, ids held here); anything else in
   `info/` is refused.
6. **`logs/`** is shape-checked (two object ids per line), not interpreted; `description`, `COMMIT_EDITMSG`,
   `ORIG_HEAD`, `*_HEAD`, `*_MSG` are size- and NUL-checked text. None of these can name a path.
7. **Bind mounts and overlay quirks** inside `d` are invisible to `lstat`; the counter's bwrap (`ro_sandbox`) locks
   mounts, so a module cannot produce one.
8. **Budgets** (`20000` reads / `64 MiB`) are per decision and reset at entry: a fixture that would need more is
   refused as pathological rather than answered late.
9. `_SPENT` (the budget) is module state, reset at each `breach` entry — safe because the contract is one decision
   per process; a caller that re-entered `breach` concurrently would share the budget (fail-closed, not fail-open).

## 6. Risks and blockers

- No blockers. No tool installed or upgraded (nothing was needed: python3 3.14, bwrap, strace present); no pacman
  transaction; `~/.local/bin` digest `ff187bb5c98aa6b5` unchanged in all 9 envelope runs.
- Risk to the round-46 counter's REFUSALS leg: the frozen claims say its refuse set is "every round-45 held-out
  module … converted to the module contract", i.e. the 31 fixtures above plus f1–f10. All 31 + all 10 refuse here
  with zero outside opens, including the two cases round 45 counted as survivors (`g4` hidden commondir, hardlink).
- Risk to SEALED (wave-1 modules I must not read): a sealed module can only win by finding a shape my allowlist
  admits. The allowlist is: plain files/dirs with one link, a store with the six inert subdirectories, a config in
  the key table, loose objects that inflate, refs that resolve inside the store, an index v2 that parses. Each of
  those is checked by content, not by name, so a name-keyed or path-keyed survivor is unlikely; a *parser
  disagreement* with git (e.g. a config construct my grammar accepts and git reads as an include) is the residual
  class — my parser is stricter than git's (no escapes, no dotted sections, no inline comments, no subsections
  outside `branch`), so any such construct is refused rather than admitted.
- Fidelity note for the L1: my `order` leg is stricter than the base's — absolute or `..`-escaping `--claims` /
  `--receipt` values are refused instead of being handed to `git cat-file` (which failed open). No honest battery
  fixture uses one (all 104 pass, and the values in `plans/battery4*/o_*.py` are lane-relative).

## 7. Scratch and hygiene

`python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46ExecC1FenceB /fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceB`
→ `DELETE path=/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceB resolved=… bytes=561770008 size=535.7MiB`;
peer scratch dirs untouched. Receipts kept in this seat's subdir (each < 12 KiB, none over 1 MiB):
`receipts-r45-counter.out`, `receipts-heldout-{includeif,symlinks,argvenv,commondir2,configkeys}.out`,
`receipts-claims-leg.out`, `receipts-filetrace.out`. No corpus/, plans/ or lane file was written; the fence exists
only in the clone that measured it and in this seat's directory.

VERDICT: fenceB-r45-pass-yes-heldout-refused-11/11
