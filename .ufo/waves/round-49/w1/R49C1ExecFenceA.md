# R49C1ExecFenceA — fence repair variant A re-applied at the round-49 freeze (scratch candidate, re-measured)

Axes named: **calibration** (R49-C1, the axis this seat is judged on), with the containment constraint it is
measured against — zero traced access outside `d` on every leg. No other axis is touched: no lane file, counter,
plan, population, corpus entry or scorecard byte was changed, no commit/jj call was made, and no tool was
installed or updated.

Scope: the seat's named item only — apply the §7 unified diff of `.ufo/waves/round-48/w1/R48C1ExecFenceA.md` to
`plans/fixture_fence.py` @ `9d2900af41e4d1fc6022eff99010436fde6dbd93`, re-verify the candidate sha256
`b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`, and run the 120-fixture honest48
population + 20 refusals46 modules + 12 sealed46 modules through a development harness that reuses the round-46
counter's builders and strace envelope, printing per-leg rollups only. **No predicate was printed and no
R49-C1/C2 admission is claimed.**

## 1. Freeze and measurement boundary

Verified before any measurement, read-only, on the lane:

```
$ git -C <lane> rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128
$ git -C <lane> merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD ; echo $?
0                                  # ANCESTOR-OK
$ git -C <lane> log -1 --format='%H %ci %an' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 kengaku-shokunin
$ git -C <lane> log --oneline 9d2900af..HEAD
af88aab round-49: w1 v2 wave spec + dispatch evidence (64 seats, 40 attack, policy v2 accepted)
$ git -C <lane> show 9d2900af:plans/round-49-claims.md | sha256sum
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  -
$ sha256sum <clone>/plans/round-49-claims.md
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  <clone>/plans/round-49-claims.md
$ git -C <lane> show 9d2900af:plans/fixture_fence.py | sha256sum
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  -
$ git -C <lane> rev-parse 9d2900af:plans/fixture_fence.py
a2b128ae007bf47d3aefdeda6321ae118c7e5958
```

So the stage-1 freeze is committed in the lane tree at `9d2900af`, is an ancestor of the wave head, carries the
`## Freeze amendments` / `None yet` shape, and was committed at **2026-10-28T09:14:40-03:00**, i.e. **before**
the measurements below (`date -Iseconds` at measurement time: `2026-10-28T09:21:37-03:00`; receipt mtimes
`09:21:00` candidate, `09:21:10` base). The fence blob at the freeze is byte-identical to the round-48 base fence
(`05d5fe03…aad5e`, blob `a2b128ae…`), so the §7 diff — written against `a543d920` — applies to `9d2900af`
without any intervening change to the file it patches.

**Stage 2 does not exist.** `plans/honest49/`, `plans/sealed49/`, `plans/mutants49/c1-mutants.json` and
`plans/round49_c1_verify.py` are absent at `9d2900af` (and at the wave head); no `<P>`, `<H>`, `<S>`, `<B>`,
`<M>` literal is pinned and no v3 counter file exists. A scored run of `plans/round49_c1_verify.py` is therefore
impossible, and I made none. Every number below comes from a development harness that prints **rollups only**,
never a `PREDICATE` line, and that imports the round-44 builder and the round-46 envelope **from the clone at the
frozen base** rather than re-implementing them.

## 2. The diff applies cleanly and the candidate sha256 is reproduced — no drift

```
$ git clone --shared -q <lane> lane && git -C lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
$ git -C lane rev-parse HEAD        /  git -C lane rev-parse --show-toplevel  /  git -C lane status --porcelain
9d2900af41e4d1fc6022eff99010436fde6dbd93
/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceA/lane
0 lines
$ git -C lane apply --verbose $TMPDIR/fence_a.diff
Checking patch plans/fixture_fence.py...
Applied patch plans/fixture_fence.py cleanly.
$ sha256sum lane/plans/fixture_fence.py ; wc -l lane/plans/fixture_fence.py
b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52  lane/plans/fixture_fence.py
810 lane/plans/fixture_fence.py
$ cp lane/plans/fixture_fence.py fence_a.py && git -C lane checkout -q -- plans/fixture_fence.py
$ git -C lane status --porcelain | wc -l
0
```

The unified diff was extracted **programmatically** from the round-48 report's single ` ```diff ` fence
(`re.findall(r'^```diff\n(.*?)^```$', text, re.S|re.M)` → 1 block, 690 lines) so no line was retyped.

- **Drift: none.** The applied result is exactly `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`
  (810 lines) — the pinned candidate digest, reproduced byte-for-byte at the round-49 freeze rather than at
  `a543d920`.
- Transcribed to `.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py`, sha256 `b687b1d9…0ca52`, 810 lines.
- Base copy for the before-value: `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

## 3. Harness (dev only, no predicate)

`dev_harness.py` (scratch, deleted with the scratch tree; its whole logic is described here) does exactly this:

1. `load(<clone>/plans/round44_c1_verify.py)` and `load(<clone>/plans/round46_c1_verify.py)` — the counters
   **as committed at the frozen base**; nothing is copied, patched or re-implemented.
2. `k46.pin_issues(lane, refdir, sealdir, False)` → `PINS total=65 mismatched=0` (all 65 round-46 pins, i.e.
   the round-44 builder plus every battery/refusals46/sealed46 module, match the frozen base tree).
3. Writes `k46.HARNESS` and a byte copy of the fence under test into `<root>/ctl/`, then builds every module
   with **`k46.build_module(k44, …)`** (round-44 bwrap build sandbox, memfd builder slot, per-run tokens,
   24-child padding) and shuffles the build order, the run order and all fleet tokens.
4. Runs every fixture with **`k46.run_fence(k44, …)`**: `strace -f -qq -y -s 256 -e trace=<TRACE_SET>` outside
   a `k44.ro_sandbox` that hides the lane and the ctl dir, log written outside `d`, `os.closerange(3, 1024)`
   inside the fence process, verdict carried by exit status 10/11, touches counted by `k46.analyse` against the
   scratch root only (B1/B3/B4/B5/B6 legs).
5. Prints `BUILD`, `FENCE-RUN`, `ROLLUP`, `REFUSALS`, `SEALED`, `HONEST` lines. **It never prints `PREDICATE`,
   never computes a pass/fail, and its `HONEST`/`REFUSALS`/`SEALED` lines are plain counters with no floor
   literal attached.** No `<H>`/`<S>`/`<M>` literal is invented here.

## 4. Exact commands run

```
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceA
W=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/modules

python3 dev_harness.py --fence $TMPDIR/fence_a.py \
    --honest-extra $W/r46novel --honest-extra $W/novel48 \
    --refusals $TMPDIR/lane/plans/refusals46 --sealed $TMPDIR/lane/plans/sealed46 \
    --work $TMPDIR/work/cand --jobs 10 --out $TMPDIR/receipts/candidate.txt

python3 dev_harness.py --fence $TMPDIR/fence_base.py \
    --honest-extra $W/r46novel --honest-extra $W/novel48 \
    --refusals $TMPDIR/lane/plans/refusals46 --sealed $TMPDIR/lane/plans/sealed46 \
    --work $TMPDIR/work/base --jobs 10 --out $TMPDIR/receipts/base.txt
```

Population: honest = 22 battery modules (`plans/battery42|43|44`) + 9 `r46novel` + 7 `novel48` = **38 modules,
120 fixtures**; hostile = 20 `refusals46` modules (34 fixtures) + 12 `sealed46` modules (15 fixtures).
`JOBS total=169 workers=10` on both runs. No scored counter, gate or probe was run over claimed work.

## 5. Observed outputs (verbatim)

### 5.1 Candidate `b687b1d9…0ca52` — the repair

```
LANE /fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceA/lane
FENCE source=/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceA/fence_a.py sha256=b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52
PINS total=65 mismatched=0
MODULES refusal total=20
MODULES sealed total=12
MODULES honest total=38
JOBS total=169 workers=10
ROLLUP honest/battery42 modules=5 fixtures=29 admit=29 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/battery43 modules=7 fixtures=42 admit=42 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/battery44 modules=10 fixtures=33 admit=33 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/novel48 modules=7 fixtures=7 admit=7 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/r46novel modules=9 fixtures=9 admit=9 refuse=0 error=0 hung=0 touched=0
ROLLUP refusal modules=20 fixtures=34 admit=0 refuse=34 error=0 hung=0 touched=0
ROLLUP sealed modules=12 fixtures=15 admit=0 refuse=15 error=0 hung=0 touched=0
ROLLUP honest modules=38 fixtures=120 admit=120 refuse=0 error=0 hung=0 touched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 error=0 hung=0 touched=0 build_errors=0
```

Every one of the 169 `FENCE-RUN` rows carried `touches=0`; `build_errors=0` and `hung=0` on every leg; no row
printed `LOG-TAMPER`. The 16 novel honest fixtures (the classes the base refuses) all admit:

```
FENCE-RUN honest novel48/n10_empty_repo.py n10-empty-repo ADMIT touches=0 calls=470 -- ADMIT
FENCE-RUN honest novel48/n11_multibranch.py n11-multibranch ADMIT touches=0 calls=577 -- ADMIT
FENCE-RUN honest novel48/n12_local_config_user.py n12-local-config-user ADMIT touches=0 calls=492 -- ADMIT
FENCE-RUN honest novel48/n13_remote_origin.py n13-remote-origin ADMIT touches=0 calls=492 -- ADMIT
FENCE-RUN honest novel48/n14_stash_entry.py n14-stash-entry ADMIT touches=0 calls=509 -- ADMIT
FENCE-RUN honest novel48/n15_commit_graph.py n15-commit-graph ADMIT touches=0 calls=504 -- ADMIT
FENCE-RUN honest novel48/n16_notes_ref.py n16-notes-ref ADMIT touches=0 calls=508 -- ADMIT
FENCE-RUN honest r46novel/n01_packed_refs.py n01-packed-refs ADMIT touches=0 calls=504 -- ADMIT
FENCE-RUN honest r46novel/n02_annotated_tag.py n02-annotated-tag ADMIT touches=0 calls=497 -- ADMIT
FENCE-RUN honest r46novel/n03_detached_head.py n03-detached-head ADMIT touches=0 calls=501 -- ADMIT
FENCE-RUN honest r46novel/n04_merge_commit.py n04-merge-commit ADMIT touches=0 calls=523 -- ADMIT
FENCE-RUN honest r46novel/n05_gitignore.py n05-gitignore ADMIT touches=0 calls=496 -- ADMIT
FENCE-RUN honest r46novel/n06_linear_30.py n06-linear-30 ADMIT touches=0 calls=711 -- ADMIT
FENCE-RUN honest r46novel/n07_reflog_gc.py n07-reflog-gc ADMIT touches=0 calls=492 -- ADMIT
FENCE-RUN honest r46novel/n08_tag_detached.py n08-tag-detached ADMIT touches=0 calls=506 -- ADMIT
FENCE-RUN honest r46novel/n09_ignored_untracked.py n09-ignored-untracked ADMIT touches=0 calls=497 -- ADMIT
```

### 5.2 Candidate — all 49 hostile fixtures refused, `touches=0` (containment after the allowlist extension)

```
refusal refusals46/f10_laneinclude.py f10-lane-include-regular BREACH touches=0 calls=468 -- BREACH lane/.git/config section [include] is not allowlisted
refusal refusals46/f11_cr_include.py h1-cr-include-crlf BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f11_cr_include.py h1-cr-include-lf BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f11_cr_include.py h3-cr-include-anchor BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-gitdir-exact BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-gitdir-glob BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-gitdir-i BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-gitdir-nomatch BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-gitdir-star BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-hasconfig BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-onbranch-anchor BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-onbranch BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f12_includeif_cond.py h2-inclif-onbranch-nomatch BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f13_bom_include.py h3-bom-include BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a non-ASCII byte
refusal refusals46/f13_bom_include.py h3-bom-includeif BREACH touches=0 calls=468 -- BREACH lane/.git/config carries a non-ASCII byte
refusal refusals46/f14_gitdir_include_symlink.py h3-cr-include-symlink BREACH touches=0 calls=469 -- BREACH lane/.git/config carries a bare CR
refusal refusals46/f15_objects_symlink_out.py link-objects-symlink-out BREACH touches=0 calls=447 -- BREACH lane/.git/objects is a symlink
refusal refusals46/f16_objects_hardlink_out.py link-objects-hardlink-out BREACH touches=0 calls=482 -- BREACH 05/6b827f2bdbcacbd8fddc955f4ffc599f5f811c has more than one hard link
refusal refusals46/f17_argv_nul.py argv-nul-lane BREACH touches=0 calls=427 -- BREACH --lane value carries a NUL byte
refusal refusals46/f18_wtmeta_out.py g3-wtmeta-out BREACH touches=0 calls=469 -- BREACH repo/.git/worktrees is not a plain-init entry
refusal refusals46/f19_commondir_hidden.py g4-cd-hidden BREACH touches=0 calls=469 -- BREACH repo/.git/modules is not a plain-init entry
refusal refusals46/f1_gitfile.py f1-gitdir-outside BREACH touches=0 calls=431 -- BREACH .git is a file (gitdir redirect), not a directory
refusal refusals46/f20_attributes_file.py config-core-attributes-file-outside BREACH touches=0 calls=468 -- BREACH lane/.git/config key core.attributesfile is not allowlisted
refusal refusals46/f2_deep.py f2-deep-worktree BREACH touches=0 calls=455 -- BREACH x/y/z/r/.git/config key core.worktree is not allowlisted
refusal refusals46/f3_abbrev.py f3-abbrev-tree-claims BREACH touches=0 calls=427 -- BREACH order argv is not the contract shape ['--lane', '--claims', '--receipt']
refusal refusals46/f4_fifo.py f4-fifo-include BREACH touches=0 calls=446 -- BREACH lane/.git/config section [include] is not allowlisted
refusal refusals46/f5_alternates.py f5-alternates-outside BREACH touches=0 calls=484 -- BREACH alternates is not a plain object-info entry (object-store redirect)
refusal refusals46/f6_above.py f6-repo-above-d BREACH touches=0 calls=433 -- BREACH --lane '<SCRATCH>/work/cand/…/f000/sub' is not a repository inside the fixture
refusal refusals46/f7_commondir.py f7-cd-accept BREACH touches=0 calls=436 -- BREACH lane/.git/commondir is not a plain-init entry
refusal refusals46/f7_commondir.py f7-cd-anchor BREACH touches=0 calls=436 -- BREACH lane/.git/commondir is not a plain-init entry
refusal refusals46/f7_commondir.py f7-cd-reject BREACH touches=0 calls=436 -- BREACH lane/.git/commondir is not a plain-init entry
refusal refusals46/f8_worktreecfg.py f8-wtcfg-a BREACH touches=0 calls=469 -- BREACH lane/.git/config section [extensions] is not allowlisted
refusal refusals46/f8_worktreecfg.py f8-wtcfg-b BREACH touches=0 calls=469 -- BREACH lane/.git/config section [extensions] is not allowlisted
refusal refusals46/f9_nodescribe.py f9-bare-repo BREACH touches=0 calls=468 -- BREACH lane/.git/config core.bare must be false
sealed sealed46/a_newline_anchor.py newline-anchor-accept BREACH touches=0 calls=427 -- BREACH --lane value carries a newline
sealed sealed46/a_newline_anchor.py newline-anchor-reject BREACH touches=0 calls=427 -- BREACH --lane value carries a newline
sealed sealed46/a_phantom_anchor.py phantom-anchor-accept BREACH touches=0 calls=429 -- BREACH --lane 'missing-lane' does not exist inside the fixture
sealed sealed46/a_phantom_anchor.py phantom-anchor-reject BREACH touches=0 calls=429 -- BREACH --lane 'missing-lane' does not exist inside the fixture
sealed sealed46/a_phantom_order.py phantom-order-accept BREACH touches=0 calls=430 -- BREACH --lane 'lane-file' is not a directory
sealed sealed46/a_phantom_order.py phantom-order-reject BREACH touches=0 calls=430 -- BREACH --lane 'lane-file' is not a directory
sealed sealed46/c_core_attributes_path.py sealed-core-attributes-path BREACH touches=0 calls=468 -- BREACH lane/.git/config key core.attributesfile is not allowlisted
sealed sealed46/c_excludes_file.py sealed-core-excludes-file BREACH touches=0 calls=468 -- BREACH lane/.git/config key core.excludesfile is not allowlisted
sealed sealed46/c_url_rewrite.py sealed-url-insteadof-path BREACH touches=0 calls=468 -- BREACH lane/.git/config section [url "file:///outside/"] is not allowlisted
sealed sealed46/p_info_redirect.py sealed-info-redirect BREACH touches=0 calls=530 -- BREACH info is a symlink
sealed sealed46/p_pack_redirect.py sealed-pack-redirect BREACH touches=0 calls=500 -- BREACH pack is a symlink
sealed sealed46/p_refs_redirect.py sealed-refs-redirect BREACH touches=0 calls=468 -- BREACH lane/.git/refs is a symlink
sealed sealed46/s_objects_link.py seal-objects-link BREACH touches=0 calls=468 -- BREACH lane/.git/objects is a symlink
sealed sealed46/s_packed_refs.py seal-packed-refs-link BREACH touches=0 calls=469 -- BREACH lane/.git/packed-refs is a symlink
sealed sealed46/s_refs_link.py seal-refs-link BREACH touches=0 calls=468 -- BREACH lane/.git/refs is a symlink
```

37 refusal rows + 12 sealed rows = 34 + 15 = 49 fixtures; every one `BREACH` with `touches=0`. The refusal
*reasons* are the base fence's own messages (allowlist / CR / non-ASCII / symlink / hardlink / argv-shape), i.e.
the extended allowlist did not have to weaken a single hostile detection to reach 120/120 honest admissions.
(The `f6-repo-above-d` message embeds the run's scratch path; redacted as `<SCRATCH>` here.)

### 5.3 Base fence `05d5fe03…aad5e` on the identical population — before value (harness self-check)

```
FENCE source=/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceA/fence_base.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
PINS total=65 mismatched=0
ROLLUP honest/battery42 modules=5 fixtures=29 admit=29 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/battery43 modules=7 fixtures=42 admit=42 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/battery44 modules=10 fixtures=33 admit=33 refuse=0 error=0 hung=0 touched=0
ROLLUP honest/novel48 modules=7 fixtures=7 admit=2 refuse=5 error=0 hung=0 touched=0
ROLLUP honest/r46novel modules=9 fixtures=9 admit=6 refuse=3 error=0 hung=0 touched=0
ROLLUP refusal modules=20 fixtures=34 admit=0 refuse=34 error=0 hung=0 touched=0
ROLLUP sealed modules=12 fixtures=15 admit=0 refuse=15 error=0 hung=0 touched=0
ROLLUP honest modules=38 fixtures=120 admit=112 refuse=8 error=0 hung=0 touched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 error=0 hung=0 touched=0 build_errors=0
```

The 8 base honest refusals, verbatim:

```
FENCE-RUN honest novel48/n16_notes_ref.py n16-notes-ref BREACH touches=0 calls=472 -- BREACH refs/notes has a name git does not write
FENCE-RUN honest r46novel/n07_reflog_gc.py n07-reflog-gc BREACH touches=0 calls=467 -- BREACH repo/.git/info/refs is not git's exclude file
FENCE-RUN honest r46novel/n03_detached_head.py n03-detached-head BREACH touches=0 calls=446 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest novel48/n13_remote_origin.py n13-remote-origin BREACH touches=0 calls=447 -- BREACH repo/.git/config section header b'[remote "origin"]' is not plain
FENCE-RUN honest novel48/n15_commit_graph.py n15-commit-graph BREACH touches=0 calls=496 -- BREACH repo/.git/objects/info/commit-graph present (object-store redirect)
FENCE-RUN honest novel48/n14_stash_entry.py n14-stash-entry BREACH touches=0 calls=474 -- BREACH refs/stash has a name git does not write
FENCE-RUN honest novel48/n12_local_config_user.py n12-local-config-user BREACH touches=0 calls=447 -- BREACH repo/.git/config section [user] is not allowlisted
FENCE-RUN honest r46novel/n08_tag_detached.py n08-tag-detached BREACH touches=0 calls=446 -- BREACH repo/.git/HEAD is not a plain branch HEAD
```

This reproduces the round-48 measured before value exactly — `HONEST fixtures=120 admitted=112 refused=8`
(`w1/R48C1ExecCounter.md`, scratch `REV a543d920…`) — on the same 8 fixtures and with the same refusal causes.
That is the harness self-check: my envelope and builders reproduce the known base figure, so the candidate's
120/120 is measured by an instrument whose before value is already corroborated, not by a new one.

### 5.4 Delta (candidate − base), the axis-relevant quantity

| leg | base | candidate | delta |
|---|---|---|---|
| honest fixtures admitted | 112 / 120 | **120 / 120** | +8 (the 8 over-refusals repaired) |
| honest `touched` | 0 | 0 | 0 (no new outside access) |
| refusals46 clean | 20 / 20 | 20 / 20 | 0 (no detection lost) |
| sealed46 clean | 12 / 12 | 12 / 12 | 0 (no detection lost) |
| build errors / hangs | 0 / 0 | 0 / 0 | 0 |

Both directions are measured on the *same* 169 jobs with the same tokens/shuffle scheme, so the only variable is
the fence bytes.

## 6. Revision measured

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
```

Clone at the frozen base, clean (`git -C lane status --porcelain` → 0 lines before and after every run); the
fence under test is the scratch candidate named by sha256 in §2, never a lane file. `TREE-BYTES` does not apply
(the clone was uncommitted-clean throughout). Host facts: git 2.56.0, Python 3.14.8, bubblewrap 0.13.1,
strace 7.2, `/fast` device 66309, 32 CPUs, all fixtures and the scratch root on `/fast` (`/tmp` unused). Wall
time: candidate 09:20:58→09:21:00, base 09:21:08→09:21:10 (local).

## 7. Limits (named, not hidden)

1. **This is not a C1 verdict.** No v3 counter, no pinned `<H>`/`<S>`/`<M>` literal, no `plans/honest49/` or
   `plans/sealed49/` population exists at stage 2; the item's own rule forbids a scored counter run, and none was
   made. The numbers above are development-harness rollups; stage 2 must re-measure on the pinned counter and a
   clean clone of the landing tip.
2. **The mutation leg is untouched by this seat.** `<M>` fence mutants (`plans/mutants49/c1-mutants.json`) are a
   separate wave-1 deliverable; this report says nothing about the mutation floor and must not be read as
   evidence for it. The round-48 routed defect 4 stays open until that battery runs with receipts.
3. **The honest population measured is the round-48 frozen 120**, not the stage-2 population the claims freeze
   extends with "the novel honest classes authored by wave-1 seats this round against the *base* fence
   description". Those new classes are not in `w1/R48C1ExecHonest/modules/`, so they could not be included; if
   any of them names an in-`d` linked worktree, an in-`d` `objects/info/alternates` target, or a clone inside
   `d`, variant A refuses it by design (round-48 report §8 limits 2–3) and the honest leg would go red.
4. **Same-filesystem bind mounts below `d` are admitted** (`st_dev` equal, no in-`d` discriminator). Cross-device
   mounts are refused. This is a property of the candidate as written, inherited unchanged from the round-48
   measurement; the round-49 mount-boundary wording ("admitted iff every byte the decision reads is inside `d`")
   is satisfied, the stricter "the store is not a bind of something else" reading is not.
5. **Instrument limits inherited unchanged** from the round-46 envelope: host paths outside the scratch root are
   not counted, `io_uring` SQE opens are untraced, a directory `stat`'s `st_nlink` channel is nulled by padding.
   The claim measured is "no traced access outside `d` under the scratch root", not "no syscall to any path".
6. **`sealed49/` does not exist**, so the held-out class authored against the *landed* fence is not tested here;
   a hostile shape aimed at the newly allowlisted surface (`info/refs` rows, `commit-graph` magic, `[remote]`
   values, `refs/stash`) is exercised only by the round-48 negative probes, not by this run.
7. **`[remote "<n>"] url` is admitted as an inert declaration** even if it names a path or host outside `d`; the
   fence reads no byte of it and the gated tools run no fetch. If stage 2 makes remote URLs policy-hostile, that
   is a predicate change, not a seat decision, and this variant would need the `url` charset narrowed.
8. **Two fixtures' `calls=` differ by ±1–2 between this run and round 48** (`n13`, `n14`, `n16`, battery rows):
   strace call counts include scheduler-dependent noise; verdicts, `touches` and rollups are stable across both
   runs and both fences' before value reproduces exactly.

## 8. Files, scratch and lane state

- Transcribed deliverable: `.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py` (sha256 `b687b1d9…0ca52`,
  810 lines) — byte-identical to the applied candidate.
- This report: `.ufo/waves/round-49/w1/R49C1ExecFenceA.md`.
- Lane: **no production file written** (`plans/`, `corpus/`, `SCORECARD.md`, `LOG.md` untouched), no commit, no
  push, no mutating git/jj call; the clone at `9d2900af` was used read-only and restored to clean after the
  patch check (`git -C lane status --porcelain` → 0 lines). Lane worktree shows only the wave tree the L1
  dispatched: `?? .ufo/waves/round-49/w1/`, `?? .ufo/waves/round-49/w1.ready.dispatched`.
- Scratch `/fast/scratch/hyaku/kengaku-r49/R49C1ExecFenceA` (+ `TMPDIR`) held the clone, `fence_a.py`,
  `fence_base.py`, `fence_a.diff`, `dev_harness.py`, `work/` and `receipts/`; **it was removed before yield**
  (receipts transcribed verbatim into §5 first). No `/tmp` artefact is cited; no tool was installed or updated.
- Suggested post-integration checks for the main agent (not run here): pin `b687b1d9…0ca52` in stage 2 and run
  the v3 counter on a clean clone of the landing tip; confirm `PINS`, `REFUSALS 20/20`, `SEALED <S>/<S>`,
  `HONEST <H>/<H>` and the mutant floor; re-run the base fence as the before-control (expect `HONEST … refused≥8`
  on the extended population).

## 9. Sources opened (access date 2026-10-28; local URLs only, no external URL opened)

| source | located quote (≤25 words) |
|---|---|
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` §C1 | “HONEST fixtures=<H> admitted=<H> refused=0 read=0 hung=0 build_errors=0” |
| `…/.ufo/waves/round-48/w1/R48C1ExecFenceA.md` §7 | “Candidate source (full unified diff, applies to `plans/fixture_fence.py` @ `a543d920`)” |
| `…/.ufo/waves/round-48/w1/R48C1ExecFenceA.md` §3 | “candidate: battery 104/104 r46novel 9/9 novel48 7/7 my nc1–nc9 18/18” |
| `…/.ufo/waves/round-48/w1/R48C1ExecFenceA.md` §6 | “REV a543d92083557dd9b33ee674e9b99b03411f80af” |
| `…/corpus/lessons/round-48-verifier-spotcheck.md` §5 defect 4 | “the candidate's ≥12-mutant kill battery was never reported” |
| `…/corpus/lessons/round-48-verifier-spotcheck.md` §2 (R48-C1) | “the base fence over-refuses 8 honest fixtures” |
| `…/.ufo/waves/round-48/w1/R48C1ExecHonest/README.md` | “120 | 85 `anchor`, 35 `order`; 0 duplicate `fid`” |
| `…/plans/round46_c1_verify.py` (`run_fence` docstring) | “One fence decision in a read-only sandbox under a host `strace -f -y`” |
| `…/plans/round44_c1_verify.py` (`build_module_child` docstring) | “Child entry (inside bwrap): build every fixture of one module into dest/fNNN, print JSON only.” |
| `…/plans/fixture_fence.py` @`9d2900af` (module docstring) | “`--lane` must be one of the collected repositories.” |
| `file:///home/vgpnk/.omp/agent/RULES.md` | “Record every install or update … in your report or handoff” — no tool was installed or updated |

VERDICT: **variant A re-applied at the round-49 freeze with NO DRIFT — the §7 diff applies cleanly to
`plans/fixture_fence.py` @ `9d2900af` and reproduces the pinned candidate sha256 `b687b1d9…0ca52` (810 lines),
transcribed to `.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py`; on the frozen 120-fixture honest48
population + 20 refusals46 + 12 sealed46 modules (169 jobs, `PINS total=65 mismatched=0`) the candidate measures
`HONEST fixtures=120 admitted=120 refused=0 touched=0`, `REFUSALS total=20 clean=20`, `SEALED total=12 clean=12`,
`build_errors=0 hung=0`, while the base fence on the identical population measures the known before value
`admitted=112 refused=8` on the same 8 fixtures; NO scored counter/probe run (stage-2 freeze absent), NO predicate
printed, and NO R49-C1/C2 admission claimed.** The mutation floor (`<M>`, routed defect 4) remains unmeasured by
this seat.
