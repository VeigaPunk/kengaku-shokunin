# R46ExecC1Modules — refusals46: round-45 held-out modules converted to the refusal-module contract

Seat: executor, kengaku round 46 wave 1 (hyaku run 9). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Base measured: `64ba8385ea10af1b78d367dcb242b92d97062af7` (round-45 closure tip). Claims read in full before any
work: `plans/round-46-claims.md` (C1 bullet (c) is my assignment). Round-45 routing read:
`corpus/lessons/round-45-verifier-spotcheck.md`.

## 0. Order rule and scope compliance

- I wrote no fence and no counter. I did not open `plans/round46_c1_verify.py` or anything under
  `.ufo/waves/round-46/w1/<other seat>` except my own; I read only the round-45 a3w1 held-out modules and their
  reports, `plans/refusals45/`, `plans/fixture_fence.py` @ base and the two pinned counters.
- No SEALED module was read. No repaired fence was scored by anything (none exists yet).
- Lane writes: none. `git -C <lane> status --porcelain` shows only other seats' round-46 wave scaffolding
  (`?? .ufo/waves/round-46/w1/`, `w1.ready`, spec dumps); no `corpus/`, `plans/` or tracked file changed by me.
  My only writes are `/.ufo/waves/round-46/w1/R46ExecC1Modules/` (this report, `driver.py`, `receipts/`,
  `refusals46/`) and my scratch dir.

## 1. Contract mirrored

I mirrored `plans/refusals45/f7_commondir.py` (three-fixture, two tools), `f1_gitfile.py` (single `build`) and
`f10_laneinclude.py` (single `build`, outside artefact at `d.parent`), and the builder's own reader
(`plans/round44_c1_verify.py` `Ctx` / `build_module_child`): `FIXTURES = [{"fid", "tool", "expect", "defects",
"build"}]`, `build(ctx, d) -> list[str]` returning the argv tail, every outside artefact created under
`pathlib.Path(d).parent` (the module build root `Ctx` permits), `tool` ∈ {`order`, `anchor`}. No module imports
anything, and no module reads its own `expect`/`defects` (they are carried verbatim from the source module and are
inert for the round-45 counter; a future `round46_c1_verify.py` may decide what they mean).

## 2. Deliverable

`refusals46/` — complete directory, 20 modules + `SHA256SUMS` (manifest of the 20 `f*.py`, relative names):

| file | bytes sha256 |
|---|---|
| `f1_gitfile.py` … `f10_laneinclude.py` | byte copies of `plans/refusals45/`, sha256 equality confirmed per file |
| `f11_cr_include.py` – `f20_attributes_file.py` | 10 new, `SHA256SUMS` |
| `SHA256SUMS` | `sha256sum f*.py | LC_ALL=C sort -k2` |
| `driver.py` (seat dir) | `fab7ac86867f96b03307c9a6158775bba37df856d0226c7019364cc222c7a8ec` |

Byte-copy proof (`plans/refusals45/` vs `refusals46/`), ten lines `EQUAL fN_*.py`:

```text
58ab580f84f84b4bd5e536418e7580874ae7ecf1717585628712e800feaf5111  f10_laneinclude.py
bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d  f1_gitfile.py
027972c63696dd16e147b70002a532bf754ef5bd4f31956ae4510efd8ddcb734  f2_deep.py
05a43c051053d131fc11a0f7625c0b28fc0ca1a8c5d9c5302fca5f21062ead48  f3_abbrev.py
6ba6a730192d056f60e1accfb1a31f30e2133296b56537ff6047d0da6817d043  f4_fifo.py
8d56f2f7d4c1e8dd5951d87e1d5e5443fa45721fc1da1a61abcd11320061eab4  f5_alternates.py
e9a599e400952eb203123205754f7993a37c83de9ddc881521bbcaa4df4608df  f6_above.py
c828c1010e38e17812374e8d5383d4fb04e8e37d0ad38915f46723b726eaa0f3  f7_commondir.py
e9483e36db55a98abdc3f9b93964fe96d4cda4e714d2be831696db6a245af364  f8_worktreecfg.py
b85ca5c6f95ac535ee762323cf0461a27e15820fd93c994d58df5ccb2ca557d2  f9_nodescribe.py
EQUAL f10_laneinclude.py
EQUAL f1_gitfile.py
EQUAL f2_deep.py
EQUAL f3_abbrev.py
EQUAL f4_fifo.py
EQUAL f5_alternates.py
EQUAL f6_above.py
EQUAL f7_commondir.py
EQUAL f8_worktreecfg.py
EQUAL f9_nodescribe.py
```

## 3. Conversion table — module → source report → base verdict → opens

Every verdict below is produced by the round-45 counter's **own** machinery on a `--shared` clone at
`64ba8385` (`git -C "$S/lane" rev-parse HEAD` = `64ba8385ea10af1b78d367dcb242b92d97062af7`; toplevel =
`$S/lane`): `plans/round45_c1_verify.py` `build_module(k44, lane, root, f)` (round-44 builder sandbox) +
`run_fence(k44, lane, root, fence_copy, fx, n)` (read-only sandbox, `strace -f -y`, counter's open classifier),
fence copy sha256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` = `plans/fixture_fence.py`
at base (= the digest the round-45 reports measured). Per-module rule is the counter's own (`main()` lines
289–296): any `ADMIT`/`ERROR` → LEAKED, else HUNG, else READ if an outside open happened, else clean.

| new module | source (round-45 a3w1) | class (one per file) | base verdict | fixtures | outside opens |
|---|---|---|---|---|---|
| `f11_cr_include.py` | `R45HoIncludeIf/h1_cr_include.py` + `h3_bom_symlink.py` (`h3-cr-include-anchor`, same class, anchor tool) | bare `\r` before `[include]` | **LEAKED** | 3 | 17 (7/7/3) |
| `f12_includeif_cond.py` | `R45HoIncludeIf/h2_includeif_cond.py` | `\r`-prefixed `[includeIf "<cond>"]` | **LEAKED** | 9 | 36 |
| `f13_bom_include.py` | `R45HoIncludeIf/h3_bom_symlink.py` (BOM fixtures) | UTF-8 BOM at byte 0 of `.git/config` | **LEAKED** | 2 | 12 (7/5) |
| `f14_gitdir_include_symlink.py` | `R45HoIncludeIf/h3_bom_symlink.py` (symlink fixture) | include target symlink inside the pruned `.git` | **LEAKED** | 1 | 7 |
| `f15_objects_symlink_out.py` | `R45HoSymlinks/link_hostiles.py` | `.git/objects` symlinked out of `d` | **LEAKED** | 1 | 8 |
| `f16_objects_hardlink_out.py` | `R45HoSymlinks/link_hostiles.py` | object store hardlinked out of `d` | **LEAKED** | 1 | 0 |
| `f17_argv_nul.py` | `R45HoArgvEnv/argv_env.py` | `--lane` value with embedded NUL (fence raises `ValueError`) | **LEAKED** (`ERROR`) | 1 | 0 |
| `f18_wtmeta_out.py` | `R45HoCommondir2/modules/g3_wtmeta.py` | linked-worktree metadata pointing outside `d` | **LEAKED** | 1 | 0 |
| `f19_commondir_hidden.py` | `R45HoCommondir2/modules/g4_cdrel_hidden.py` | relative `.git/commondir` hidden below a pruned `.git` | **LEAKED** | 1 | 32 |
| `f20_attributes_file.py` | `R45HoConfigKeys/configkeys.py` | `core.attributesFile` pointing outside `d` | **LEAKED** | 1 | 0 |

Totals: **10 new modules, 21 fixtures, 10 LEAKED, 0 READ, 0 clean, 0 hung, 0 build errors.** No kept module is
READ-only: on all three reading modules the same fixture was also ADMITted, so the counter's rule reports LEAKED
(the opens column preserves the read evidence: `f11`, `f12`, `f13`, `f14`, `f15`, `f19` = 112 outside opens).

### 3.1 Held-out fixtures/materials dropped, and why

The keep rule is "LEAKED or READ under the base fence". Dropped, each refused with 0 outside opens at base:

| dropped | source | base observation |
|---|---|---|
| `h4_controls.py` (3 fixtures) | `R45HoIncludeIf` | `BREACH … lane/.git/config carries an include`, opens=0 |
| `link-git-symlink-in`, `link-claims-symlink-out`, `link-include-chain-in` | `R45HoSymlinks` | `BREACH`, opens=0/0/0 |
| `argv-placeholder-lane-escape`, `argv-extra-token` | `R45HoArgvEnv` | `BREACH`, opens=0 |
| `g1_cdrel.py`, `g2_gitfile.py` | `R45HoCommondir2/modules` | `BREACH` (`commondir` / `.git` file), opens=0 |

Split rationale: `R45HoSymlinks/link_hostiles.py` is one driver over five fixtures in three classes (store
symlink out / store hardlink out / three refusals) — split into `f15`/`f16`, refusals dropped. `h3_bom_symlink.py`
states two independent `_INCLUDE_RE`/walk evasions (BOM, `.git`-internal symlink target) — split into
`f13`/`f14`. `h1_cr_include.py` and the CR-anchor fixture of `h3` are the same class (CR-prefixed include, two
tools), so they share `f11` rather than lose the anchor-leg coverage. `argv_env.py`'s surviving fixture is a
single class (argv value that crashes the fence) → `f17`.

## 4. The round-45 counter run over the whole dir

`--refusals` is **not** a flag of `plans/round45_c1_verify.py` (its `main()` takes `--lane`, `--work`, `--jobs`
only; the refusal dir is the constant `REFUSAL_REL = "plans/refusals45"`, `REFUSAL_TOTAL = 10`). So, as the item
instructs, I ran it on a second `--shared` clone (`$S/lane2`, toplevel `$S/lane2`, HEAD `64ba8385`) whose
`plans/refusals45/` was emptied and refilled with `refusals46/` (20 modules; f1–f10 still byte-identical, so
`PINS` for the ten refusal paths still match) and whose `REFUSAL_TOTAL` I edited `10 → 20` (single line, `:100`).

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/env2 /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/env2 --bind /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/env2/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/lane2/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/lane2 --work /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/w2 --jobs 8
ENVELOPE start 01:52:15 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
REFUSALS total=20 clean=10 leaked=10 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=20 contradicted=10
PREDICATE C1 fail
ENVELOPE end 01:52:21 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Exit 1 is the expected before-value: the base fence contradicts 10 of the 20 modules. The HONEST leg stays
104/104 admitted, so adding the ten modules does not disturb the honest floor.

## 5. Per-module proof run (receipt `receipts/driver-run.out`)

`driver.py LANE ROOT MODDIR` — imports the clone's `plans/round44_c1_verify.py` and `plans/round45_c1_verify.py`
unchanged, writes `HARNESS` + a fence byte-copy, then one `build_module`/`run_fence` pair per module.

```text
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/env /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/env --bind /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC1Modules/driver.py /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/lane /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/w1/root /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC1Modules/refusals46
ENVELOPE start 01:51:49 cwd=/home/vgpnk/Projects/shokunin
LANE /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules/lane HEAD 64ba8385ea10af1b78d367dcb242b92d97062af7
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
FENCE-COPY sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
MODULES 20
FENCE-RUN f11_cr_include.py h1-cr-include-lf ADMIT opens=7
FENCE-RUN f11_cr_include.py h1-cr-include-crlf ADMIT opens=7
FENCE-RUN f11_cr_include.py h3-cr-include-anchor ADMIT opens=3
FENCE-RUN f12_includeif_cond.py h2-inclif-onbranch ADMIT opens=5
FENCE-RUN f12_includeif_cond.py h2-inclif-onbranch-nomatch ADMIT opens=0
FENCE-RUN f12_includeif_cond.py h2-inclif-gitdir-exact ADMIT opens=7
FENCE-RUN f12_includeif_cond.py h2-inclif-gitdir-glob ADMIT opens=7
FENCE-RUN f12_includeif_cond.py h2-inclif-gitdir-i ADMIT opens=7
FENCE-RUN f12_includeif_cond.py h2-inclif-gitdir-star ADMIT opens=7
FENCE-RUN f12_includeif_cond.py h2-inclif-gitdir-nomatch ADMIT opens=0
FENCE-RUN f12_includeif_cond.py h2-inclif-hasconfig ADMIT opens=0
FENCE-RUN f12_includeif_cond.py h2-inclif-onbranch-anchor ADMIT opens=3
FENCE-RUN f13_bom_include.py h3-bom-include ADMIT opens=7
FENCE-RUN f13_bom_include.py h3-bom-includeif ADMIT opens=5
FENCE-RUN f14_gitdir_include_symlink.py h3-cr-include-symlink ADMIT opens=7
FENCE-RUN f15_objects_symlink_out.py link-objects-symlink-out ADMIT opens=8
FENCE-RUN f16_objects_hardlink_out.py link-objects-hardlink-out ADMIT opens=0
FENCE-RUN f17_argv_nul.py argv-nul-lane ERROR opens=0 -- ValueError: lstat: embedded null character in path
FENCE-RUN f18_wtmeta_out.py g3-wtmeta-out ADMIT opens=0
FENCE-RUN f19_commondir_hidden.py g4-cd-hidden ADMIT opens=32
FENCE-RUN f20_attributes_file.py config-core-attributes-file-outside ADMIT opens=0
MODULE f11_cr_include.py LEAKED fixtures=3 admitted=3 hung=0 opens=17
MODULE f12_includeif_cond.py LEAKED fixtures=9 admitted=9 hung=0 opens=36
MODULE f13_bom_include.py LEAKED fixtures=2 admitted=2 hung=0 opens=12
MODULE f14_gitdir_include_symlink.py LEAKED fixtures=1 admitted=1 hung=0 opens=7
MODULE f15_objects_symlink_out.py LEAKED fixtures=1 admitted=1 hung=0 opens=8
MODULE f16_objects_hardlink_out.py LEAKED fixtures=1 admitted=1 hung=0 opens=0
MODULE f17_argv_nul.py LEAKED fixtures=1 admitted=1 hung=0 opens=0
MODULE f18_wtmeta_out.py LEAKED fixtures=1 admitted=1 hung=0 opens=0
MODULE f19_commondir_hidden.py LEAKED fixtures=1 admitted=1 hung=0 opens=32
MODULE f20_attributes_file.py LEAKED fixtures=1 admitted=1 hung=0 opens=0
MODULE f1_gitfile.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f2_deep.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f3_abbrev.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f4_fifo.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f5_alternates.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f6_above.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f7_commondir.py clean fixtures=3 admitted=0 hung=0 opens=0
MODULE f8_worktreecfg.py clean fixtures=2 admitted=0 hung=0 opens=0
MODULE f9_nodescribe.py clean fixtures=1 admitted=0 hung=0 opens=0
MODULE f10_laneinclude.py clean fixtures=1 admitted=0 hung=0 opens=0
ENVELOPE end 01:51:54 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

(The `FENCE-RUN f1`–`f10` `BREACH` lines are in the receipt; omitted here only to keep the block readable — the
ten `MODULE … clean` lines above are the verdicts.) Reproduction of the round-45 numbers is exact where the
fixture set is unchanged: h2 9/9 ADMIT with the same per-fixture opens, g4 `opens=32`, hardlink `opens=0`,
NUL `ERROR`. The base fence's silence on `h3-cr-include-symlink` (`opens=7`) also reproduces.

## 6. Receipts (all in this seat's dir, all < 1 MiB)

| file | bytes | sha256 |
|---|---|---|
| `receipts/driver-run.out` | 5493 | `f5497f14ab410cb1d17d2cc1545f7924ba960b3786564e86274c34edb2b3581b` |
| `receipts/r45-counter-refusals46.out` | 14253 | `5372a21edb7216f68dad88b8b7bc8d1ae7703f4b6e0da49c73e449b33f6d6e2f` |
| `driver.py` | 3290 | `fab7ac86867f96b03307c9a6158775bba37df856d0226c7019364cc222c7a8ec` |
| `refusals46/SHA256SUMS` | manifest of the 20 modules | — |

No tool was installed or upgraded (none needed); no pacman transaction was run.

## 7. Risks, limits, and what the L1 must decide

1. **ERROR counts as LEAKED only under the round-45 rule.** `f17` makes the base fence raise `ValueError:
   lstat: embedded null character in path`; `run_fence` returns `ERROR`, and the counter's `n_admit` counts
   `ERROR` with `ADMIT`. If `round46_c1_verify.py` treats a fence exception as a harness fault rather than a
   defect, `f17` becomes invisible to the predicate. It is a real defect either way (the fence's contract says
   `str | None`, never an exception) and should be counted; the stage-2 counter text must say which.
2. **`f16` (hardlink) leaks no open.** It is a store-identity leak (the ADMIT is the defect; 0 outside opens).
   Same for `f18` (worktree metadata) and `f20` (`core.attributesFile`): a counter that only counts outside
   opens will not see them; the ADMIT legs must stay in the predicate.
3. **`f18` and `f20` are robustness gaps against the letter of the advertisement** rather than proven reads
   during the decision (round-45's own reading: `R45HoCommondir2.md` §5 "reported, not judged";
   `R45HoConfigKeys.md`: git honours the external attributes file when queried). Kept because both are ADMITs
   under the base fence; the L1 may downgrade their weight.
4. **Split choices are mine and reversible.** `f11` carries the anchor variant from `h3`; if the L1 prefers one
   file per source module, splitting `f11` into `f11` (h1) + a separate anchor file is mechanical (the fixture
   list is the only thing that changes). Likewise `f13`/`f14` split `h3`'s two evasions.
5. **Freshness of the numbers.** All ten new modules were authored this wave from files that the base fence
   ADMITs; they are not sealed held-out modules for a repaired fence (they are its known-before set). A repaired
   fence that passes `refusals46` has not thereby passed anything held out.
6. **`expect`/`defects` are inert** for the round-45 counter and were copied verbatim from the sources (e.g.
   `f16` says `expect: accept`, which is the observed base behaviour, not the wanted one). If
   `round46_c1_verify.py` reads them, its semantics must be fixed at stage 2, not assumed.

## 8. Scratch

`S=/fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules` (two `--shared` clones, two envelope dirs, two work roots).
Removed with the mandated guard after the receipts were copied:

```text
$ python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46ExecC1Modules /fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules
DELETE path=/fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules resolved=/fast/scratch/hyaku/kengaku-r46/R46ExecC1Modules bytes=1100865196 size=1.0GiB
rc=0
```

Round root and other seats' dirs untouched (`ls /fast/scratch/hyaku/kengaku-r46/` → `L1 R46ExecC1Counter
R46ExecC1FenceA R46ExecC1FenceB R46ExecC1FenceC`).

VERDICT: refusals46-modules-20-base-leaked-10-read-0
