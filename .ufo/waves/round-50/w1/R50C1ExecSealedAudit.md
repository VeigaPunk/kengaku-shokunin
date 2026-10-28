# R50C1ExecSealedAudit — contract audit of the wave-1 blind sealed modules

Seat: `R50C1ExecSealedAudit` (executor), serving **R50-C1** (novelty). Read-only against the lane; nothing
committed, no production file touched, no claim of C1/C2 admission made.

```
REV 5c56819f7964f4af19c960de08a49cd8f95781ce            # lane tip at measurement (read-only)
MEASURED-AT 3b02d573d58cc6d2e0d27ef92ac0815354912252    # git clone --shared, all counters/fences loaded from here
FREEZE-ANCESTOR FREEZE_ANCESTOR_OK                      # git merge-base --is-ancestor 3b02d57… HEAD
FENCE-BYTE 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e   # plans/fixture_fence.py @ 3b02d57
COUNTER    f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76   # plans/round50_c1_verify.py
POPULATION b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69   # plans/honest50/population.txt
BUILDER    35e3de6059e4676133291c615fdac7b04342e7c43827ec1e70ac09f83267a70b   # digest declared in the claims doc
WINDOW     14:22–14:41 America/Argentina/Buenos_Aires, 2026-10-28
```

All four digests match the values frozen in `plans/round-50-claims.md`; the fork-point check printed
`FREEZE_ANCESTOR_OK`. The live lane working tree is **not** what was measured: at 14:36–14:38 other seats wrote
an uncommitted `plans/fixture_fence.py` (`57adce4a598e1ca8…`) and an uncommitted `plans/sealed50/`. The audit
loads the fence, counter, population builder and round-44 builder from the clone at `3b02d57`, i.e. the base
fence `05d5fe03…`, because that is the only tree the frozen predicate binds. The untracked wave modules and the
untracked `plans/sealed50/` are read from the live tree (they exist nowhere else).

## Axes named

1. **Contract conformance** — every module is consumable by `plans/round50_c1_verify.py`: `FIXTURES` list, rows
   carrying `fid/tool/expect/defects/build`, `build(ctx, d)` returning the argv tail as `list[str]`, fixture dir
   surviving the build, per-module unique fids, no bare absolute path literal in the module source.
2. **Identity reproducibility** — three builds at the *same* absolute root must give one canonical identity
   (`.git/index` masked by the population builder's own `tree_identity`); a fourth at a *different* root reports
   whether the fixture embeds its absolute build root.
3. **Scope integrity** — no duplicate `fid` across the audited set or against the 32 frozen r46 fids; no module
   name or fid visible from another seat's report, in particular from the fence writers'.

Non-axes (deliberately not measured): whether a *correct* repair must refuse each fixture (soundness of the
hostility argument), outside-`d` reads (that property belongs to `plans/round46_c1_verify.py`), and any verdict
about the in-flight repaired fence.

## Instrument and its negative controls

`R50C1ExecSealedAudit/audit_sealed.py` (185 lines, scratch-authored, copied into this receipt dir) imports the
lane's own `plans/honest50/build_honest_population.py` and `plans/round44_c1_verify.py`, builds every fixture of
every module into `--work` (never `/tmp`), and reports one row set per axis. It was calibrated *before* looking
at any blind module:

* **Negative controls** (six scratch modules, one defect each; `controls-negative.txt`):
  `FIXTURES[{0}] missing expect,defects,build` → `contract-ok … NO`; a `time_ns()`-stamped fixture →
  `nondeterministic`; two modules sharing `ctl-dup-fid` → two `duplicate-fid` rows; a source literal
  `/tmp/ctl-abs-marker` → `absolute path literal in source`; a fid named in a report → `name-leaks`;
  `SEALED50-CANDIDATES 0/6`.
* **Positive control on the frozen population** (`calibration-sealed46.txt`): the 12 modules of
  `plans/sealed46/` → `contract-ok 12/12`, `nondeterministic none`, `duplicate-fid none`, `name-leaks none`,
  3 root-dependent (`c_core_attributes_path`, `c_excludes_file`, `s_packed_refs` — all three write an absolute
  `str(outside)` into config or a symlink). So the instrument does not fail a fixture merely for being hostile;
  it fails only the four measured properties.

## Scope A — the wave-1 blind modules (primary item)

Six of the eight blind critic seats delivered by the end of the window: `C1CritBlind1,3,4,5,6` and
`R50C1CritBlind2` (`*/sealed/`), 12 modules, 17 digestible fixtures. `C1CritBlind7` and `C1CritBlind8` were
dispatched (`w1-dispatch.json` tasks 58 and 59) but had produced no directory and no report by the last
observation at 14:40:01; nothing of theirs is in this audit.

```
== CONTRACT-OK ==
contract-ok b1_replace_ref_target_outside_store.py yes
contract-ok b2_fetch_head_hardlink_out.py yes
contract-ok s50_alternates_dotdot_abs.py yes
contract-ok s50_gitfile_symlink_chain.py yes
contract-ok s6_gitfile_rel_objects_link.py yes
contract-ok s6_second_store_mount.py yes
contract-ok c4_gitfile_delimiter.py NO
contract-ok c4_gitfile_store_include.py yes
contract-ok x1_commondir_escape.py yes
contract-ok x2_gitfile_alternates_escape.py yes
contract-ok h_alternates_chain.py yes
contract-ok h_wt_commondir_out.py yes
== NONDETERMINISTIC ==
nondeterministic c4_gitfile_delimiter.py
== IDENTITY-ROOT-DEPENDENT ==
root-dependent s50_alternates_dotdot_abs.py fids=s50-alternates-dotdot-abs,s50-alternates-dotdot-abs:lane/.git/objects/info/alternates
root-dependent s6_second_store_mount.py fids=seal6-second-store-outside,seal6-second-store-outside:other/.git
root-dependent x1_commondir_escape.py fids=x1-cd-abs,x1-cd-abs:lane/.git/commondir
root-dependent x2_gitfile_alternates_escape.py fids=x2-alt-abs,x2-alt-abs:store/objects/info/alternates
== DUPLICATE-FID ==
duplicate-fid none
== NAME-LEAKS ==
name-leaks b1_replace_ref_target_outside_store.py …/w1/R50C1CritBlind5.md seat=R50C1CritBlind5.md needle=b1_replace_ref_target_outside_store
name-leaks s50_alternates_dotdot_abs.py …/w1/R50C1CritBlind5.md seat=R50C1CritBlind5.md needle=s50_alternates_dotdot_abs
name-leaks s50_alternates_dotdot_abs.py …/w1/C1ExecRepair/receipt-blind50-crosscheck.txt seat=C1ExecRepair needle=s50_alternates_dotdot_abs
name-leaks s50_alternates_dotdot_abs.py …/w1/C1ExecRepair/receipt-blind50-crosscheck.txt seat=C1ExecRepair needle=s50-alternates-dotdot-abs
name-leaks s50_gitfile_symlink_chain.py …/w1/C1ExecRepair/receipt-blind50-crosscheck.txt seat=C1ExecRepair needle=s50-gitfile-symlink-chain
name-leaks s50_gitfile_symlink_chain.py …/w1/C1ExecRepair/receipt-blind50-crosscheck.txt seat=C1ExecRepair needle=s50_gitfile_symlink_chain
SEALED50-CANDIDATES 8/12 b2_fetch_head_hardlink_out.py s6_gitfile_rel_objects_link.py s6_second_store_mount.py c4_gitfile_store_include.py x1_commondir_escape.py x2_gitfile_alternates_escape.py h_alternates_chain.py h_wt_commondir_out.py
```

Per-fixture evidence (identity digest, mask set, base-fence verdict; `audit-blind.json` has all 17 rows):

| module | fid | tool | expect | base `05d5fe03` | masked | det |
|---|---|---|---|---|---|---|
| b1_replace_ref_target_outside_store | b1-replace-target-outside-store | anchor | reject | BREACH | `lane/.git/index` | yes |
| b2_fetch_head_hardlink_out | b2-fetch-head-hardlink-out | anchor | reject | BREACH | `lane/.git/index` | yes |
| s50_alternates_dotdot_abs | s50-alternates-dotdot-abs | order | error | BREACH | `lane/.git/index` | yes |
| s50_gitfile_symlink_chain | s50-gitfile-symlink-chain | order | error | BREACH | *(none — no index exists)* | yes |
| s6_gitfile_rel_objects_link | seal6-gitfile-up-outside / -up-inside-link / -submodule-store-link | order | reject | BREACH ×3 | `sub/store/index`; `main/.git/index` | yes |
| s6_second_store_mount | seal6-second-store-outside / -twin | order | reject | BREACH ×2 | `lane/.git/index`, `other/.git/index` | yes |
| c4_gitfile_delimiter | b4a-gitfile-nul-two-stores | anchor | accept | *(no digest: build raises)* | — | — |
| c4_gitfile_delimiter | b4a-gitfile-newline-two-pointers | anchor | accept | BREACH | *(none)* | **no** |
| c4_gitfile_store_include | b4b-gitfile-store-include | anchor | accept | BREACH | `store/index` | yes |
| x1_commondir_escape | x1-cd-abs / x1-cd-rel | anchor | error | BREACH ×2 | `lane/.git/index` | yes |
| x2_gitfile_alternates_escape | x2-alt-abs / x2-alt-rel | anchor | error | BREACH ×2 | `store/index` | yes |
| h_alternates_chain | bl5-alternates-chain-out | anchor | breach | BREACH | `lane/.git/index`, `mid/.git/index` | yes |
| h_wt_commondir_out | bl5-wt-commondir-out | anchor | breach | BREACH | `wtadmin/index` | yes |

All 17 digestible fixtures are `BREACH` on the base fence — the assemble gate's "must be refused by the base
fence" condition holds for every row, and none of the 17 fids collides with the 32 frozen r46 fids.

## Scope B — the assembled `plans/sealed50/` as it stands (uncommitted, other seats' output)

Eighteen modules, 21 fixtures: the 8 blind modules above plus 10 hostile variants `s50_01…s50_10`. All 21 are
`BREACH` on the base fence; `duplicate-fid none`.

```
== CONTRACT-OK ==   (18 rows; two NO)
contract-ok c4_gitfile_delimiter.py NO          # build: ValueError: lstat: embedded null character in path
contract-ok s50_01_stray_symlink.py NO          # absolute path literal in source: /etc/hostname
…16 × yes (b1, b2, c4_gitfile_store_include, s50_02…s50_10, s50_alternates_dotdot_abs,
           s50_gitfile_symlink_chain, s6_gitfile_rel_objects_link, s6_second_store_mount)
== NONDETERMINISTIC ==
nondeterministic c4_gitfile_delimiter.py
== IDENTITY-ROOT-DEPENDENT ==
root-dependent s50_alternates_dotdot_abs.py, s6_second_store_mount.py
== DUPLICATE-FID ==
duplicate-fid none
== NAME-LEAKS ==
name-leaks none
SEALED50-CANDIDATES 16/18 …
```

## Defects (measured, with the exact pointer)

**D1 — blocking: a fixture in `plans/sealed50/` crashes the frozen population builder.** Module
`c4_gitfile_delimiter.py` (lane copy sha256 `95429f872677b32c…`, identical to
`w1/C1CritBlind4/sealed/`), fixture `b4a-gitfile-nul-two-stores`, writes a `.git` FILE whose body is
`gitdir: ../../side/store2\x00../store\n`. `plans/honest50/build_honest_population.py:83` `gitfile_index_paths`
matches it with the single-line `GITFILE` regex and calls `(p.parent / m.group(1)).resolve()`:

```
File "…/plans/honest50/build_honest_population.py", line 167, in tree_identity
    extra = gitfile_index_paths(root)
File "…/plans/honest50/build_honest_population.py", line 98, in gitfile_index_paths
    target = (p.parent / m.group(1)).resolve()
ValueError: lstat: embedded null character in path
```

`plans/round50_c1_verify.py` `build_all` catches that as a build failure, and its SEALED `leg()` sets
`ok = False` when `nfail != 0`; the module would print `SEALED … build_errors=1` and kill the predicate. Note
the defect is file-scoped: the same module's other fixture digests fine. Two remedies exist and both are the
L1's call — drop/exclude the module, or repair the builder under the open-window rule ("a leg that cannot
run") with a NUL guard at line 98 (inert for the frozen population: no honest fixture has a NUL gitfile, so the
population pin `b5197f94…` cannot move).

**D2 — the mask rule is narrower than the gitfile state space.** `GITFILE` is single-line-anchored
(`\Agitdir:[ \t]*(.+?)[ \t]*\n?\Z`), so a multi-line gitfile gets no store index added to `extra` and git's stat
cache enters the identity. Measured on `b4a-gitfile-newline-two-pointers`, six rebuilds at distinct roots:

```
r0 tree=ab9ccc8ffb9456f6 store_index=66b3d6d3509b
r1 tree=89324278efbb36aa store_index=f8d9cb61f7e5
r2 tree=6085c4e2b9dbf4a3 store_index=6b92a3e3548e
r3 tree=fd2fec24bc36fb31 store_index=84e90ba76417
r4 tree=2fa9b42eb96fecce store_index=d739d9908929
r5 tree=63de879cada13796 store_index=bf849b395a86
tree digests equal: False   store/index equal: False
```

(`store/index` is 209 bytes in every build; two rebuilds at the *same* path also differed,
`095bb1662a6bcee3` vs `dc3c11b5ffe9fc78`.) The fixture is a real git state and a plausible blind row; it simply
cannot be identity-pinned under the frozen builder. Same family as D1: the open-window repair is one rule —
resolve a gitfile's store index for every line-oriented reading, and refuse to resolve a path containing NUL.

**D3 — a committed row hardcodes a host path.** `plans/sealed50/s50_01_stray_symlink.py` does
`os.symlink("/etc/hostname", d / "outside-link")`. The fixture's shape then depends on a file outside the
scratch root that the claims explicitly say is not observed ("host paths outside the scratch root are not
observed"), and the row would be unbuildable-meaningful on a host without `/etc/hostname`. The witnessed
property (a symlink outside every store, pointing outside `d`) is reachable with a target inside the build root,
e.g. `d.parent / "outside-target"`. Reported as `contract-ok … NO` for that reason only.

**D4 — name cross-check: the blind set is readable from two reports.** (i) `w1/R50C1CritBlind5.md` lines 311,
340, 343 name `s50_alternates_dotdot_abs.py` (seat `R50C1CritBlind1`) and `b1_replace_ref_target_outside_store.py`
(seat `R50C1CritBlind3`) — one blind critic read two other blind seats' modules, which is
`R50C1RevBlindIndependence`'s claim, but it is also a name leak by my item's definition. (ii) The fence writer
`R50C1ExecRepair` ran its candidate against `C1CritBlind1/sealed/` and recorded the outcome in
`w1/C1ExecRepair/receipt-blind50-crosscheck.txt` (14:39), naming both Blind1 modules and their sha256 and the
BREACH reasons. Timestamps put the candidate fence (`fence_candidate.py`, mtime 14:36, sha256
`9baedf1379b6de5c…`) *before* that crosscheck, so there is no evidence the candidate was tuned on those two
modules — but the sealed rows are now visible to a fence writer, which is what the item asks me to report.
No other seat's report names any blind module, and no lane file (`SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`,
`LOG.md`, `plans/*.md`, `corpus/lessons/*.md`) does.

**D5 — the assembled copy of one module is stale.** `plans/sealed50/s6_second_store_mount.py` is
`f2425983cc13e91d…` while `w1/C1CritBlind6/sealed/s6_second_store_mount.py` is `cfb0005ddfe5011c…`; the delta is
semantic (`outside = d.parent / "s6-store-second"` → `d.parent / f"{d.name}-evil"`, a prefix-twin that a
`startswith` containment test admits). The other 7 blind copies are byte-identical to their wave originals
(`34354116…`, `6a15228b…`, `95429f87…`, `3c99e89b…`, `9fe77895…`, `70705f02…`, `efe4ad43…`).

**D6 — junk in the row directory.** `plans/sealed50/__pycache__/` exists; the counter globs `*.py` so it is
inert, but it must not be committed.

## The count that may enter `plans/sealed50/`

| set | modules | fixtures | base fence | contract+identity+fid+leak clean | **may enter** |
|---|---|---|---|---|---|
| wave-1 blind modules (6 seats) | 12 | 17 | 17/17 BREACH | 8 | **8** |
| assembled `plans/sealed50/` now | 18 | 21 | 21/21 BREACH | 16 | **16** |

Both clear the frozen literals (`SEALED50_MIN = 6`, and `SEALED ≥ 18` total with the 12 frozen r46 modules —
18 + 16 = 34). The eight clean blind modules are
`b2_fetch_head_hardlink_out, s6_gitfile_rel_objects_link, s6_second_store_mount, c4_gitfile_store_include,
x1_commondir_escape, x2_gitfile_alternates_escape, h_alternates_chain, h_wt_commondir_out`; the four that are
not clean are `c4_gitfile_delimiter` (D1+D2), `s50_alternates_dotdot_abs` and `s50_gitfile_symlink_chain` (D4),
`b1_replace_ref_target_outside_store` (D4). In the assembled directory the same rows apply plus `s50_01`
(D3): 16 of 18 clean.

**D1 makes the count moot until it is settled**: `c4_gitfile_delimiter.py` is *currently in* `plans/sealed50/`,
so a scored run of the frozen counter on that tree prints `SEALED … build_errors=1` and
`PREDICATE R50-C1 fail`, independent of how many clean rows exist.

## Commands run (verbatim, in order)

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD
git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
sha256sum plans/fixture_fence.py plans/round50_c1_verify.py plans/honest50/population.txt
python3 audit_sealed.py --lane $S/lane --work $S/w-ctl --modules $S/controls/m --leak-scan $S/controls/fence-writer-report.md
python3 audit_sealed.py --lane $S/lane --work $S/w-cal2 --modules $S/lane/plans/sealed46 --json $S/cal-sealed46.json
python3 audit_sealed.py --lane $S/lane --work $S/w-final --modules <6 × w1/*sealed dirs> \
  --leak-scan "<w1>/*.md" "<w1>/*.txt" "<w1>/*/*.md" "<w1>/*/*.txt" SCORECARD.md SHONEN.md PROVINCE.md LOG.md \
  "plans/*.md" "corpus/lessons/*.md" --json audit-blind.json
python3 audit_sealed.py --lane $S/lane --work $S/w-final2 --modules <lane>/plans/sealed50 --json audit-sealed50.json
```
(`$S = /fast/scratch/hyaku/kengaku-r50/R50C1ExecSealedAudit`, `TMPDIR=$S`; the scratch tree including the
577 MB `--shared` clone was removed before this report was yielded. Receipts retained here:
`R50C1ExecSealedAudit/{audit_sealed.py, controls-negative.txt, calibration-sealed46.txt, audit-blind.txt,
audit-blind.json, audit-sealed50.txt, audit-sealed50.json}`. `python3 plans/round50_c1_verify.py` was **not**
re-run by this seat: its result is not part of this item, and the tree it would score is the in-flight,
uncommitted one.)

## Limits

* Blind7 and Blind8 delivered nothing in the observation window; the blind population measured is 6 seats / 12
  modules. A later arrival must be audited the same way before assembly.
* The audit judges consumability, identity and name visibility — not whether each fixture's refusal is
  *required* by the fence's predicate, and not whether any fixture triggers an outside-`d` read (that is the
  round-46 counter's property, not re-scored here).
* Identity is the frozen builder's `tree_identity`: `.git/index`, each gitfile-named store index and per-worktree
  indexes are masked; a symlink *directory* target is hashed only by its mode, not by its text — which is why
  three modules that escape through directory symlinks read `root_independent=True`.
* The "same root" determinism probe rewrites the fixture at one absolute path three times; a stat cache that the
  mask misses (D2) still shows, but an absolute build path can only be seen by the cross-root build, which is
  reported separately (`IDENTITY-ROOT-DEPENDENT`, 4 of 12 blind modules, 3 of 12 frozen modules).
* The fence under test throughout is the frozen base fence `05d5fe03…` in the clone at `3b02d57`. No statement
  is made about the in-flight repaired fence (`57adce4a…` in the live tree, or any scratch candidate).

## VERDICT

`contract-ok` 11/12 wave-1 blind modules (16/18 in the assembled directory) · `nondeterministic`
`c4_gitfile_delimiter` (D2: mask gap on a multi-line gitfile, 6/6 distinct digests) · `duplicate-fid` none
(neither within either set nor against the 32 frozen r46 fids) · `name-leaks` two modules reachable from reports
(D4: `R50C1CritBlind5.md` for Blind1/Blind3 modules; `C1ExecRepair/receipt-blind50-crosscheck.txt` for Blind1's
two modules) · **may enter `plans/sealed50/`: 8 of 12 blind modules, 16 of 18 assembled modules**, both above the
frozen `SEALED50_MIN = 6` — **but only after D1 is settled**, because `c4_gitfile_delimiter.py` is in the
assembled directory now and its NUL fixture crashes the frozen population builder, which costs
`SEALED build_errors=1` and fails the predicate. Scratch tree removed; no lane file written outside this report
and its receipt directory.
