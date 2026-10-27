# R48C1ExecFenceA — R48-C1 fence over-refusal repair, variant A (scratch candidate)

Axes named: **calibration** (R48-C1, the axis I am judged on), with the containment constraint it is measured
against — zero traced access outside `d`. No other axis is touched: no lane file, counter, plan or scorecard byte
was changed, and no tool was installed or updated.

Scope: the seat's named item only — extend the round-46 variant-A allowlist so the nine round-46 novel honest
classes are admitted while all 20 `plans/refusals46/` + 12 `plans/sealed46/` modules stay refused with
`touches=0`; honour the `w2/R46W2C1Intent.md` mount-point boundary; per-fixture receipts on a scratch clone.
I claim no C1/C2 admission and wrote no predicate line.

## 1. Freeze and measurement boundary (why there is no scored run)

Verified before any measurement, read-only, on the lane:

```
$ git -C <lane> log -1 --format='%H %cI %s' -- plans/round-48-claims.md
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
$ sha256sum plans/round-48-claims.md                    # worktree copy of the clone at that revision
87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672  plans/round-48-claims.md
$ git show a543d920:plans/round-48-claims.md | sha256sum
87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672  -
$ git cat-file -e a543d920:plans/round48_c1_verify.py ; echo $?    / test -e plans/round48_c1_verify.py
stage2-counter: ABSENT at a543d920 / worktree counter: absent
$ tail -3 plans/round-48-claims.md
## Freeze amendments
None yet. Stage 2 fills literals and pins only.
```

So the stage-1 freeze exists in the committed lane tree, is the revision I measured, and predates it; **stage 2
(the v3 counter file, its pins, the frozen population literals and the before-control receipts) does not exist**.
A scored run of `plans/round48_c1_verify.py` is therefore impossible, and I made none: every number below comes
from a development harness that reuses the round-46 counter's own builder and strace envelope and prints **no**
`PREDICATE` line. Nothing was re-frozen, weakened or re-labelled; no scored counter, gate or probe was run over
claimed work.

## 2. What the candidate changes (allowlist deltas, nothing removed)

Base fence: `plans/fixture_fence.py` @ `a543d920`, sha256 `05d5fe03…aad5e` (575 lines). Candidate:
`fence_a.py` in this seat's scratch, sha256
`b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` (810 lines), full diff in §7.

Measured refusal causes at base on ordinary `git init` states, and the repair for each:

| # | base refusal (measured, §5.3) | repair |
|---|---|---|
| 1 | `lane/.git/HEAD is not a plain branch HEAD` — detached HEAD | `HEAD` accepts `ref: refs/heads/…` **or** one 40-hex sha (`HEAD_HEX`), nothing else |
| 2 | `lane/.git/info/refs is not git's exclude file` — `git gc`/`pack-refs`/`update-server-info` | new `_info()`: `exclude` (as before) + `refs` validated line by line as `sha\tref` with optional `^{}` peel |
| 3 | `repo/.git/objects/info/commit-graph present (object-store redirect)` | new `_obj_info()`: `packs` (`P <name>.pack` rows), `commit-graph` (magic `CGPH`), `commit-graphs/` (`graph-<8..64 hex>.graph` with magic, `commit-graph-chain` of 40-hex rows). `alternates`, `http-alternates` and every other name stay refused |
| 4 | `repo/.git/config section [user] is not allowlisted` | `_config` rewritten: `[core]` keys as before plus `autocrlf`/`safecrlf`; `[user] name|email`, `[init] defaultBranch` as printable text; `[remote "<n>"]` (`url`/`fetch`/`tagopt`) and `[branch "<n>"]` (`remote`/`merge`) as inert declarations, subsection name validated by `_sub_name_ok` |
| 5 | `refs/stash has a name git does not write` | `_refs`: `refs/{heads,tags,notes}/…` plus `refs/stash` as a plain 40-hex file |
| 6 | `refs/notes has a name git does not write` | same; reflogs: `_log_name_ok` + `_logs` accept `refs/{heads,tags,notes}/…` and `refs/stash` |
| 7 | never refused (worktree shapes) | no change: annotated tags, merge commits, `.gitignore`, 30-commit linear, ignored untracked files were already admitted by the walk; they appear in the receipts only as coverage of the nine classes |

Mount boundary (`w2/R46W2C1Intent.md`): `_entries()` now carries `st_dev`; the walk and every store classifier
refuse any directory/file whose device differs from `d`'s (`… crosses a mount boundary (device N != M)`), so a
store backed by another device is refused instead of classified. Same-device bind mounts are **not**
distinguishable with reads inside `d` (named limit, §8) — refusing on device identity is the only in-`d` proof.

Nothing that redirects a read was added: `[include]`, `[includeIf]`, `[url "<base>"] insteadOf`, `core.attributes*`,
`core.excludes*`, `core.hooksPath`, `core.fsmonitor`, `core.worktree`, `[extensions]`, `.git/commondir`,
`.git/config.worktree`, `.git` gitdir files, `objects/info/alternates|http-alternates`, `refs/remotes` all remain
refused (§5.4, §5.5).

## 3. Functional consequence

Admitted (0 outside touches) | refused (0 outside touches)

```
candidate:  battery 104/104  r46novel 9/9   novel48 7/7   my nc1–nc9 18/18   | refusals 34 fixtures / 20 modules
                                                                             | sealed   15 fixtures / 12 modules
base:       battery 104/104  r46novel 6/9   novel48 2/7   my nc1–nc9 11/18   | refusals 34/34, sealed 15/15 (identical)
```

The round-46 novel classes were reproduced twice: my own `nc1–nc9` (18 fixtures, §5.1) and the wave-1 frozen
population's `r46novel` (9, `R48C1ExecHonest`). Both are fully admitted by the candidate and partly refused at base.

## 4. Exact commands (all in this seat's scratch; TMPDIR exported to it)

```
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1ExecFenceA && export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1ExecFenceA
git clone --shared -q <lane> $TMPDIR/lane && git -C $TMPDIR/lane checkout -q a543d92083557dd9b33ee674e9b99b03411f80af
git -C $TMPDIR/lane rev-parse HEAD                     # a543d92083557dd9b33ee674e9b99b03411f80af
git -C $TMPDIR/lane rev-parse --show-toplevel          # /fast/scratch/hyaku/kengaku-r48/R48C1ExecFenceA/lane
python3 $TMPDIR/probe.py --lane $TMPDIR/lane --fence $TMPDIR/fence_a.py \
    --honest $TMPDIR/honest --honest <wave>/R48C1ExecHonest/modules/r46novel \
    --honest <wave>/R48C1ExecHonest/modules/novel48 --battery \
    --refusals $TMPDIR/lane/plans/refusals46 --sealed $TMPDIR/lane/plans/sealed46 \
    --work $TMPDIR/work --jobs 8 --out $TMPDIR/receipts/final_candidate.txt
# same line with --fence $TMPDIR/lane/plans/fixture_fence.py → receipts/final_base.txt
python3 $TMPDIR/neg.py $TMPDIR/fence_a.py                 # 26 direct breach() probes, no strace
python3 $TMPDIR/shapecheck.py $TMPDIR/fence_a.py          # 6 ordinary/extra shapes
unshare -rm sh -c "cd $TMPDIR && python3 mountprobe.py $TMPDIR/fence_a.py"   # bind mounts in a private mntns
```

`probe.py` loads `plans/round44_c1_verify.py` and `plans/round46_c1_verify.py` **from the clone** and calls their
own `build_module()` and `run_fence()`/`analyse()`; it prints `FENCE-RUN`/`ROLLUP` lines only and no predicate.
The candidate receipt holds 187 `FENCE-RUN` rows = 34 novel honest (18 + 9 + 7) + 104 battery + 34 refusal
fixtures + 15 sealed fixtures, each with its verdict, `touches=` and traced-call count.

Every fixture is built by the round-44 builder inside the counter's bwrap sandbox and judged by the round-46
envelope: `strace -f -y` outside the sandbox, log outside `d`, fd>2 closed, exit status carries the verdict,
touches counted under the scratch root only (B3/B5/B6).

## 5. Observed outputs (verbatim)

### 5.1 Population rollups — candidate (fence sha256 `b687b1d9…0ca52`)

```
ROLLUP honest modules=9 fixtures=18 admit=18 refuse=0 error=0 hung=0 touched=0
ROLLUP honest1 modules=9 fixtures=9 admit=9 refuse=0 error=0 hung=0 touched=0
ROLLUP honest2 modules=7 fixtures=7 admit=7 refuse=0 error=0 hung=0 touched=0
ROLLUP battery modules=22 fixtures=104 admit=104 refuse=0 error=0 hung=0 touched=0
ROLLUP refusal modules=20 fixtures=34 admit=0 refuse=34 error=0 hung=0 touched=0
ROLLUP sealed modules=12 fixtures=15 admit=0 refuse=15 error=0 hung=0 touched=0
```

`honest` = my nc1–nc9 (18 fixtures), `honest1` = population `r46novel`, `honest2` = population `novel48`.

### 5.2 Same harness, base fence (sha256 `05d5fe03…aad5e`) — before value

```
ROLLUP honest modules=9 fixtures=18 admit=11 refuse=7 error=0 hung=0 touched=0
ROLLUP honest1 modules=9 fixtures=9 admit=6 refuse=3 error=0 hung=0 touched=0
ROLLUP honest2 modules=7 fixtures=7 admit=2 refuse=5 error=0 hung=0 touched=0
ROLLUP battery modules=22 fixtures=104 admit=104 refuse=0 error=0 hung=0 touched=0
ROLLUP refusal modules=20 fixtures=34 admit=0 refuse=34 error=0 hung=0 touched=0
ROLLUP sealed modules=12 fixtures=15 admit=0 refuse=15 error=0 hung=0 touched=0
```

### 5.3 Base-fence refusals of ordinary states (the defect, measured verbatim)

```
FENCE-RUN honest  honest/nc3_detached_head.py nc3-detached-at-tip BREACH touches=0 calls=468 -- BREACH lane/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest  honest/nc3_detached_head.py nc3-detached-behind BREACH touches=0 calls=457 -- BREACH lane/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest  honest/nc8_annotated_detached.py nc8-tag-detached BREACH touches=0 calls=468 -- BREACH lane/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest  honest/nc8_annotated_detached.py nc8-tag-packed-detached BREACH touches=0 calls=469 -- BREACH lane/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest  honest/nc1_packed_refs.py nc1-gc-packed BREACH touches=0 calls=491 -- BREACH lane/.git/info/refs is not git's exclude file
FENCE-RUN honest  honest/nc7_reflog_gc.py nc7-reflog-gc BREACH touches=0 calls=491 -- BREACH lane/.git/info/refs is not git's exclude file
FENCE-RUN honest  honest/nc7_reflog_gc.py nc7-reflog-gc-logs BREACH touches=0 calls=491 -- BREACH lane/.git/info/refs is not git's exclude file
FENCE-RUN honest1 r46novel/n03_detached_head.py n03-detached-head BREACH touches=0 calls=445 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest1 r46novel/n07_reflog_gc.py n07-reflog-gc BREACH touches=0 calls=466 -- BREACH repo/.git/info/refs is not git's exclude file
FENCE-RUN honest1 r46novel/n08_tag_detached.py n08-tag-detached BREACH touches=0 calls=445 -- BREACH repo/.git/HEAD is not a plain branch HEAD
FENCE-RUN honest2 novel48/n12_local_config_user.py n12-local-config-user BREACH touches=0 calls=446 -- BREACH repo/.git/config section [user] is not allowlisted
FENCE-RUN honest2 novel48/n13_remote_origin.py n13-remote-origin BREACH touches=0 calls=446 -- BREACH repo/.git/config section header b'[remote "origin"]' is not plain
FENCE-RUN honest2 novel48/n14_stash_entry.py n14-stash-entry BREACH touches=0 calls=473 -- BREACH refs/stash has a name git does not write
FENCE-RUN honest2 novel48/n15_commit_graph.py n15-commit-graph BREACH touches=0 calls=495 -- BREACH repo/.git/objects/info/commit-graph present (object-store redirect)
FENCE-RUN honest2 novel48/n16_notes_ref.py n16-notes-ref BREACH touches=0 calls=471 -- BREACH refs/notes has a name git does not write
```

All 15 are ordinary git states with `touches=0`: the base fence over-refused them, which is the round-46 defect
(`w2/R46W2C1HoHonest.md`) reproduced on the frozen population.

### 5.4 Per-fixture receipts — candidate, 34 honest fixtures (all admitted, zero outside touches)

```
FENCE-RUN honest2 novel48/n13_remote_origin.py n13-remote-origin ADMIT touches=0 calls=491 -- ADMIT
FENCE-RUN honest1 r46novel/n03_detached_head.py n03-detached-head ADMIT touches=0 calls=500 -- ADMIT
FENCE-RUN honest2 novel48/n10_empty_repo.py n10-empty-repo ADMIT touches=0 calls=469 -- ADMIT
FENCE-RUN honest honest/nc3_detached_head.py nc3-detached-at-tip ADMIT touches=0 calls=543 -- ADMIT
FENCE-RUN honest honest/nc7_reflog_gc.py nc7-reflog-gc ADMIT touches=0 calls=514 -- ADMIT
FENCE-RUN honest honest/nc5_gitignore.py nc5-gitignore-root ADMIT touches=0 calls=547 -- ADMIT
FENCE-RUN honest honest/nc9_ignored_untracked.py nc9-ignored-file ADMIT touches=0 calls=548 -- ADMIT
FENCE-RUN honest1 r46novel/n01_packed_refs.py n01-packed-refs ADMIT touches=0 calls=503 -- ADMIT
FENCE-RUN honest honest/nc1_packed_refs.py nc1-gc-packed ADMIT touches=0 calls=514 -- ADMIT
FENCE-RUN honest honest/nc7_reflog_gc.py nc7-reflog-gc-logs ADMIT touches=0 calls=518 -- ADMIT
FENCE-RUN honest honest/nc2_annotated_tag.py nc2-two-annotated-tags ADMIT touches=0 calls=553 -- ADMIT
FENCE-RUN honest honest/nc6_long_linear.py nc6-linear-30-tagged ADMIT touches=0 calls=977 -- ADMIT
FENCE-RUN honest honest/nc8_annotated_detached.py nc8-tag-packed-detached ADMIT touches=0 calls=546 -- ADMIT
FENCE-RUN honest2 novel48/n14_stash_entry.py n14-stash-entry ADMIT touches=0 calls=508 -- ADMIT
FENCE-RUN honest honest/nc5_gitignore.py nc5-gitignore-nested ADMIT touches=0 calls=560 -- ADMIT
FENCE-RUN honest2 novel48/n16_notes_ref.py n16-notes-ref ADMIT touches=0 calls=507 -- ADMIT
FENCE-RUN honest honest/nc8_annotated_detached.py nc8-tag-detached ADMIT touches=0 calls=548 -- ADMIT
FENCE-RUN honest honest/nc4_merge_commit.py nc4-merge-second ADMIT touches=0 calls=562 -- ADMIT
FENCE-RUN honest honest/nc2_annotated_tag.py nc2-annotated-tag ADMIT touches=0 calls=548 -- ADMIT
FENCE-RUN honest1 r46novel/n02_annotated_tag.py n02-annotated-tag ADMIT touches=0 calls=496 -- ADMIT
FENCE-RUN honest1 r46novel/n04_merge_commit.py n04-merge-commit ADMIT touches=0 calls=522 -- ADMIT
FENCE-RUN honest honest/nc1_packed_refs.py nc1-pack-refs-only ADMIT touches=0 calls=547 -- ADMIT
FENCE-RUN honest honest/nc3_detached_head.py nc3-detached-behind ADMIT touches=0 calls=533 -- ADMIT
FENCE-RUN honest honest/nc9_ignored_untracked.py nc9-ignored-dir ADMIT touches=0 calls=559 -- ADMIT
FENCE-RUN honest1 r46novel/n06_linear_30.py n06-linear-30 ADMIT touches=0 calls=710 -- ADMIT
FENCE-RUN honest1 r46novel/n08_tag_detached.py n08-tag-detached ADMIT touches=0 calls=505 -- ADMIT
FENCE-RUN honest1 r46novel/n05_gitignore.py n05-gitignore ADMIT touches=0 calls=495 -- ADMIT
FENCE-RUN honest2 novel48/n15_commit_graph.py n15-commit-graph ADMIT touches=0 calls=503 -- ADMIT
FENCE-RUN honest2 novel48/n11_multibranch.py n11-multibranch ADMIT touches=0 calls=576 -- ADMIT
FENCE-RUN honest1 r46novel/n09_ignored_untracked.py n09-ignored-untracked ADMIT touches=0 calls=496 -- ADMIT
FENCE-RUN honest2 novel48/n12_local_config_user.py n12-local-config-user ADMIT touches=0 calls=491 -- ADMIT
FENCE-RUN honest honest/nc4_merge_commit.py nc4-merge-no-ff ADMIT touches=0 calls=562 -- ADMIT
FENCE-RUN honest1 r46novel/n07_reflog_gc.py n07-reflog-gc ADMIT touches=0 calls=491 -- ADMIT
FENCE-RUN honest honest/nc6_long_linear.py nc6-linear-30 ADMIT touches=0 calls=972 -- ADMIT
```

### 5.5 Per-fixture receipts — candidate, 49 hostile fixtures (all refused, zero outside touches)

```
refusals46/f10_laneinclude.py f10-lane-include-regular BREACH touches=0
refusals46/f11_cr_include.py h1-cr-include-crlf BREACH touches=0
refusals46/f11_cr_include.py h1-cr-include-lf BREACH touches=0
refusals46/f11_cr_include.py h3-cr-include-anchor BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-gitdir-exact BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-gitdir-glob BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-gitdir-i BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-gitdir-nomatch BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-gitdir-star BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-hasconfig BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-onbranch BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-onbranch-anchor BREACH touches=0
refusals46/f12_includeif_cond.py h2-inclif-onbranch-nomatch BREACH touches=0
refusals46/f13_bom_include.py h3-bom-include BREACH touches=0
refusals46/f13_bom_include.py h3-bom-includeif BREACH touches=0
refusals46/f14_gitdir_include_symlink.py h3-cr-include-symlink BREACH touches=0
refusals46/f15_objects_symlink_out.py link-objects-symlink-out BREACH touches=0
refusals46/f16_objects_hardlink_out.py link-objects-hardlink-out BREACH touches=0
refusals46/f17_argv_nul.py argv-nul-lane BREACH touches=0
refusals46/f18_wtmeta_out.py g3-wtmeta-out BREACH touches=0
refusals46/f19_commondir_hidden.py g4-cd-hidden BREACH touches=0
refusals46/f1_gitfile.py f1-gitdir-outside BREACH touches=0
refusals46/f20_attributes_file.py config-core-attributes-file-outside BREACH touches=0
refusals46/f2_deep.py f2-deep-worktree BREACH touches=0
refusals46/f3_abbrev.py f3-abbrev-tree-claims BREACH touches=0
refusals46/f4_fifo.py f4-fifo-include BREACH touches=0
refusals46/f5_alternates.py f5-alternates-outside BREACH touches=0
refusals46/f6_above.py f6-repo-above-d BREACH touches=0
refusals46/f7_commondir.py f7-cd-accept BREACH touches=0
refusals46/f7_commondir.py f7-cd-anchor BREACH touches=0
refusals46/f7_commondir.py f7-cd-reject BREACH touches=0
refusals46/f8_worktreecfg.py f8-wtcfg-a BREACH touches=0
refusals46/f8_worktreecfg.py f8-wtcfg-b BREACH touches=0
refusals46/f9_nodescribe.py f9-bare-repo BREACH touches=0
sealed46/a_newline_anchor.py newline-anchor-accept BREACH touches=0
sealed46/a_newline_anchor.py newline-anchor-reject BREACH touches=0
sealed46/a_phantom_anchor.py phantom-anchor-accept BREACH touches=0
sealed46/a_phantom_anchor.py phantom-anchor-reject BREACH touches=0
sealed46/a_phantom_order.py phantom-order-accept BREACH touches=0
sealed46/a_phantom_order.py phantom-order-reject BREACH touches=0
sealed46/c_core_attributes_path.py sealed-core-attributes-path BREACH touches=0
sealed46/c_excludes_file.py sealed-core-excludes-file BREACH touches=0
sealed46/c_url_rewrite.py sealed-url-insteadof-path BREACH touches=0
sealed46/p_info_redirect.py sealed-info-redirect BREACH touches=0
sealed46/p_pack_redirect.py sealed-pack-redirect BREACH touches=0
sealed46/p_refs_redirect.py sealed-refs-redirect BREACH touches=0
sealed46/s_objects_link.py seal-objects-link BREACH touches=0
sealed46/s_packed_refs.py seal-packed-refs-link BREACH touches=0
sealed46/s_refs_link.py seal-refs-link BREACH touches=0
```

### 5.6 Negative probes of the newly allowlisted surface (`neg.py`, 26 cases, direct `breach()`)

Each case builds a valid repo and mutates one tolerated shape into an escape; `NEG-SUMMARY cases=26 unexpected=0`:

```
NEG info/refs symlinked out of d: REFUSED -- ../../../negcases/info_refs_symlinked_out_of_d/f/lane/.git/info/refs is a symlink
NEG info/refs carrying a line git does not serve: REFUSED -- ../../../negcases/info_refs_carrying_a_line_git_does_not_serve/f/lane/.git/info/refs carries a line git does not serve
NEG info/attributes present: REFUSED -- ../../../negcases/info_attributes_present/f/lane/.git/info/attributes is not a plain `.git/info` entry
NEG objects/info/alternates to a store beside d: REFUSED -- ../../../../negcases/objects_info_alternates_to_a_store_beside_d/f/lane/.git/objects/info/alternates is not a plain object-info entry (object-store redirect)
NEG objects/info/http-alternates to a neighbour: REFUSED -- ../../../../negcases/objects_info_http-alternates_to_a_neighbour/f/lane/.git/objects/info/http-alternates is not a plain object-info entry (object-store redirect)
NEG objects/info/packs symlinked out of d: REFUSED -- ../../../../negcases/objects_info_packs_symlinked_out_of_d/f/lane/.git/objects/info/packs is a symlink
NEG objects/info/packs carrying a hostile row: REFUSED -- ../../../../negcases/objects_info_packs_carrying_a_hostile_row/f/lane/.git/objects/info/packs carries a row git does not write
NEG commit-graph without the CGPH magic: REFUSED -- ../../../../negcases/commit-graph_without_the_CGPH_magic/f/lane/.git/objects/info/commit-graph is not a commit-graph file
NEG commit-graph symlinked to a neighbour copy: REFUSED -- ../../../../negcases/commit-graph_symlinked_to_a_neighbour_copy/f/lane/.git/objects/info/commit-graph is a symlink
NEG commit-graphs/graph symlinked out of d: REFUSED -- ../../../../../negcases/commit-graphs_graph_symlinked_out_of_d/f/lane/.git/objects/info/commit-graphs/graph-0123456789abcdef0123456789abcdef01234567.graph is a symlink
NEG HEAD to a tag line, not a branch or a sha: REFUSED -- lane/.git/HEAD is not a branch line or a detached sha
NEG HEAD carrying a sha and a newline escape: REFUSED -- lane/.git/HEAD is not a branch line or a detached sha
NEG objects/info/info redirect file (unlisted name): REFUSED -- ../../../../negcases/objects_info_info_redirect_file_(unlisted_name)/f/lane/.git/objects/info/objects is not a plain object-info entry (object-store redirect)
NEG config [include] section: REFUSED -- lane/.git/config section [include] is not allowlisted
NEG config [includeIf "gitdir:..."] section: REFUSED -- lane/.git/config section [includeif "gitdir:/home/"] is not allowlisted
NEG config [url "<base>"] insteadOf rewrite: REFUSED -- lane/.git/config section [url "https://example.invalid/"] is not allowlisted
NEG config core.excludesFile outside: REFUSED -- lane/.git/config key core.excludesfile is not allowlisted
NEG config core.attributesFile outside: REFUSED -- lane/.git/config key core.attributesfile is not allowlisted
NEG config core.hooksPath outside: REFUSED -- lane/.git/config key core.hookspath is not allowlisted
NEG config [user] value carrying a backslash escape: REFUSED -- lane/.git/config user.name carries a value the parser cannot classify
NEG config [remote] with a subsection git does not write: REFUSED -- lane/.git/config section header b'[remote "../../outside"]' is not plain
NEG config [extensions] worktreeConfig: REFUSED -- lane/.git/config section [extensions] is not allowlisted
NEG refs/stash carrying junk instead of a sha: REFUSED -- lane/.git/refs/stash is not a 40-hex ref
NEG refs/notes/commits symlinked out of d: REFUSED -- ../../../negcases/refs_notes_commits_symlinked_out_of_d/f/lane/.git/refs/notes/commits is a symlink
NEG logs/refs/stash as a directory: REFUSED -- ../../../negcases/logs_refs_stash_as_a_directory/f/lane/.git/logs/refs/stash has a name git does not write
NEG control plain-init repo: ADMITTED
NEG-SUMMARY cases=26 unexpected=0
```

### 5.7 Extra ordinary shapes (`shapecheck.py`)

```
SHAPE S1 split commit-graph: ADMIT -- admitted
SHAPE S2 repack bitmap: ADMIT -- admitted
SHAPE S3 update-server-info: ADMIT -- admitted
SHAPE S4 annotated tag + gc: ADMIT -- admitted
SHAPE S5 gc then commit: ADMIT -- admitted
SHAPE S6 clone inside d: REFUSE -- ../../../shapecases/S6/f/clone/.git/logs/refs/remotes has a name git does not write
SHAPE-SUMMARY cases=6 unexpected=0
```

### 5.8 Mount boundary (`mountprobe.py`, run under `unshare -rm` with real bind mounts)

```
MOUNT M1 cross-device store (objects/info): REFUSED -- dev 66309->33; ../../../mountcases/M1/f/lane/.git/objects/info crosses a mount boundary
MOUNT M2 cross-device worktree (lane/data): REFUSED -- dev 66309->33; lane/data crosses a mount boundary (device 33 != 66309)
MOUNT M3 same-fs bind worktree (lane/data): ADMITTED -- dev 66309->66309; admitted
MOUNT M4 same-fs bind store (objects/info): ADMITTED -- dev 66309->66309; admitted
```

## 6. Revision measured

```
REV a543d92083557dd9b33ee674e9b99b03411f80af
```

That is the lane tree the clone was checked out at and from which the builder/envelope were imported; the fence
under test is the scratch candidate named by sha256 in §2 (never a lane file). Host facts: git 2.56.0, Python
3.14.8, `/usr/bin/bwrap`, `/usr/bin/strace`, all fixtures on `/fast` (device 66309); the mount probe used `/dev/shm`
(device 33) as the cross-device donor.

## 7. Candidate source (full unified diff, applies to `plans/fixture_fence.py` @ `a543d920`)

```diff
--- a/plans/fixture_fence.py
+++ b/plans/fixture_fence.py
@@ -19,14 +19,17 @@
   1. `d` itself must be a real directory (lstat, never followed).
   2. argv must be the tool's exact option shape; every value must be a path that stays inside `d` lexically
      (no `..`, no absolute escape, no NUL, no `{...}` placeholder we cannot resolve).
-  3. one walk of `d` proves the tree has no symlink and no special file anywhere, and collects every directory
-     holding a real `.git` directory (a `.git` file is refused).
-  4. each collected store is classified entry by entry against a plain-init allowlist: `HEAD`, `ORIG_HEAD`,
-     `COMMIT_EDITMSG`, `config`, `description`, `hooks/` (`*.sample` only), `index`, `info/exclude` only
-     (so no `alternates`), `logs/`, `objects/` (2-hex/38-hex loose objects, empty `info/`, pack files only),
-     `refs/heads|tags` (40-hex refs), `packed-refs`. `config` is parsed line by line against a `[core]` key
-     allowlist; any CR, any non-ASCII byte, any section or key not listed, or any line the parser does not
-     fully understand is refused. This is what closes the CR/BOM/includeIf/attributesFile/worktree family.
+  3. one walk of `d` proves the tree has no symlink, no special file and no multi-link file anywhere, that no
+     entry crosses a device boundary (mount point), and collects every directory holding a real `.git`
+     directory (a `.git` file is refused).
+  4. each collected store is classified entry by entry against a plain-init allowlist: `HEAD` (a
+     `refs/heads` branch line or a detached 40-hex sha), `ORIG_HEAD`, `COMMIT_EDITMSG`, `config`, `description`,
+     `hooks/` (`*.sample` only), `index`, `info/` (`exclude` and the `refs` file update-server-info writes only,
+     so no `alternates`), `logs/`, `objects/` (2-hex/38-hex loose objects, pack files only, and an `info/`
+     holding only `packs` / `commit-graph` / `commit-graphs/`), `refs/heads|tags` (40-hex refs),
+     `packed-refs` (with peeled lines). `config` is parsed line by line against a `[core]` key allowlist; any
+     CR, any non-ASCII byte, any section or key not listed, or any line the parser does not fully understand is
+     refused. This is what closes the CR/BOM/includeIf/attributesFile/worktree family.
   5. `--lane` must be one of the collected repositories.
   6. no git child is started at all: measured, every git subcommand resolves the fixture path component-wise
      and stats `d`'s ancestors (paths under the build scratch outside `d`), which the advertisement and the
@@ -36,6 +39,34 @@
 (the measured residue is only the interpreter importing the harness and this module, before `breach` runs).
 `.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*` and pack files are admitted by name and size without
 content validation: the tool run behind this fence reads none of them for a path (named limit).
+
+Round 48 repair (fixture-fence honest over-refusal, `w2/R46W2C1HoHonest.md`): the round-46 allowlist refused
+ordinary `git init` repository states. This variant keeps the allowlist and extends it to the shapes git itself
+writes for the nine novel honest classes, and to nothing else:
+
+  - detached HEAD: `HEAD` may be a symbolic `refs/heads` line OR one 40-hex sha (git's own detached write);
+  - packed refs / `gc`: `.git/info/refs` (update-server-info: `sha\tref`, optional `^{}` peel), and under
+    `.git/objects/info/`: `packs` (`P <pack>.pack` lines), `commit-graph` (magic `CGPH`) and
+    `commit-graphs/` (`graph-<hex>.graph` with magic, `commit-graph-chain` of 40-hex lines). `alternates`,
+    `http-alternates`, `objects/info/*` redirects and `.git/info/*` names not listed here stay refused.
+  - annotated tags, merge commits, `.gitignore`, long linear histories and ignored untracked files are worktree
+    and object shapes the walk already classifies; they were only ever refused through the two rules above.
+  - the round-48 honest population's further ordinary states: `.git/config` may carry `[user] name|email`,
+    `[init] defaultBranch` (printable text) and the inert declaration sections `[remote "<name>"]`
+    (`url`/`fetch`/`tagopt`) and `[branch "<name>"]` (`remote`/`merge`), plus `core.autocrlf`/`core.safecrlf`;
+    `refs/notes/...`, `refs/stash`, and their reflogs are ordinary ref namespaces. No section or key that
+    redirects a read is added: `[include]`, `[includeIf]`, `[url "<base>"]` (`insteadOf`), `core.attributesFile`,
+    `core.excludesFile`, `core.hooksPath`, `core.fsmonitor`, `core.worktree`, `extensions.worktreeConfig`,
+    `.git/commondir`, `.git/config.worktree`, `objects/info/alternates|http-alternates` stay refused, and so do
+    `.git` gitdir files and `refs/remotes` (a clone is not a plain-init state).
+
+Mount-point boundary (`w2/R46W2C1Intent.md`): every directory and file the decision visits, and every store
+entry it classifies, must live on the same device as `d`; a store whose tree crosses a device boundary is
+refused (`mount boundary`), because the fence cannot prove those bytes are the fixture's. Named limit: a bind
+mount of the SAME filesystem below `d` is lexically indistinguishable from a plain directory without reading
+outside `d` (e.g. `/proc/self/mountinfo`), which the advertisement forbids; for such a fixture the fence's
+guarantee is the one it advertises — every path it names, stats or opens is inside `d`, and the store it
+classifies has the plain-init shape.
 """
 import os
 import pathlib
@@ -53,8 +84,16 @@
 
 HEX40 = re.compile(rb"\A[0-9a-f]{40}(?:\n)?\Z")
 HEAD_REF = re.compile(rb"\Aref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*\n\Z")
+HEAD_HEX = re.compile(rb"\A[0-9a-f]{40}\n\Z")
+INFO_REFS = re.compile(rb"\A[0-9a-f]{40}\t([A-Za-z0-9_][A-Za-z0-9._/-]*)(\^\{\})?\n\Z")
+PACKS_ROW = re.compile(rb"\AP ([A-Za-z0-9_][A-Za-z0-9._-]*\.pack)\n\Z")
+GRAPH_NAME = re.compile(r"\Agraph-[0-9a-f]{8,64}\.graph\Z", re.ASCII)
+CHAIN_ROW = re.compile(rb"\A[0-9a-f]{40}(?: [0-9]+)?\n\Z")
+CG_MAGIC = b"CGPH"
 SECTION_LINE = re.compile(rb"\A\[([A-Za-z][A-Za-z0-9.-]*)\]\Z")
-KEY_LINE = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)(?:[ \t]*=[ \t]*([A-Za-z0-9._-]*))?\Z")
+SECTION_SUB = re.compile(rb'\A\[([A-Za-z][A-Za-z0-9.-]*) "([A-Za-z0-9_@:+-][A-Za-z0-9._/@:+-]{0,239})"\]\Z')
+KEY_NAME = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)\Z")
+VALUE_TEXT = re.compile(rb"\A[\x20-\x5b\x5d-\x7e]{0,1024}\Z")
 OBJ_DIR = re.compile(r"\A[0-9a-f]{2}\Z", re.ASCII)
 OBJ_FILE = re.compile(r"\A[0-9a-f]{38}\Z", re.ASCII)
 PACK_FILE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\.(?:pack|idx|rev|keep|bitmap|mtimes)\Z", re.ASCII)
@@ -64,7 +103,9 @@
 GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
            "logs", "objects", "refs", "packed-refs"}
 GIT_DIRS = {"hooks", "info", "logs", "objects", "refs"}
-CFG_SECTIONS = {"core"}
+REF_NAMESPACES = ("heads", "tags", "notes")     # directories under `refs/` git writes
+CFG_SECTIONS = {"core", "user", "init"}
+CFG_SUB_SECTIONS = {"remote", "branch"}         # inert declarations: URLs and refspecs, no reads
 CFG_KEYS = {
     ("core", "repositoryformatversion"): "0",
     ("core", "filemode"): "bool",
@@ -73,9 +114,16 @@
     ("core", "ignorecase"): "bool",
     ("core", "precomposeunicode"): "bool",
     ("core", "symlinks"): "bool",
+    ("core", "autocrlf"): "autocrlf",
+    ("core", "safecrlf"): "safecrlf",
 }
+CFG_TEXT = {("user", "name"), ("user", "email"), ("init", "defaultbranch")}
+CFG_SUB_KEYS = {("remote", "url"), ("remote", "fetch"), ("remote", "tagopt"),
+                ("branch", "remote"), ("branch", "merge")}
 BOOL = {"true", "yes", "on", "1", "false", "no", "off", "0"}
 FALSEY = {"false", "no", "off", "0"}
+AUTOCRLF = {"true", "false", "input"}
+SAFECRLF = {"true", "false", "warn"}
 
 
 # ---------- small path helpers (lexical only: no resolve, no follow) ----------
@@ -98,13 +146,13 @@
 
 
 def _entries(p):
-    """[(name, mode, size, nlink)] of one directory, lstat-style. None when it cannot be read."""
+    """[(name, mode, size, nlink, dev)] of one directory, lstat-style. None when it cannot be read."""
     out = []
     try:
         with os.scandir(str(p)) as it:
             for e in it:
                 st = e.stat(follow_symlinks=False)
-                out.append((e.name, st.st_mode, st.st_size, st.st_nlink))
+                out.append((e.name, st.st_mode, st.st_size, st.st_nlink, st.st_dev))
     except OSError:
         return None
     return sorted(out)
@@ -176,9 +224,9 @@
 # ---------- fact 3: the whole tree ----------
 
 
-def _tree(d):
-    """Return (repos, reason): every directory holding a real `.git` dir, after refusing symlinks and
-    special files anywhere in the fixture."""
+def _tree(d, ddev):
+    """Return (repos, reason): every directory holding a real `.git` dir, after refusing symlinks, special
+    files, multi-link files and device boundaries anywhere in the fixture."""
     repos, seen = [], 0
     for top, dirs, files in os.walk(str(d), followlinks=False):
         seen += len(dirs) + len(files)
@@ -189,13 +237,15 @@
         for name in dirs:
             p = t / name
             try:
-                mode = os.lstat(p).st_mode
+                st = os.lstat(p)
             except OSError:
                 return None, f"{_rel(p, d)} cannot be lstat'ed"
-            if stat.S_ISLNK(mode):
+            if stat.S_ISLNK(st.st_mode):
                 return None, f"{_rel(p, d)} is a symlink"
-            if not stat.S_ISDIR(mode):
+            if not stat.S_ISDIR(st.st_mode):
                 return None, f"{_rel(p, d)} is not a directory"
+            if st.st_dev != ddev:
+                return None, f"{_rel(p, d)} crosses a mount boundary (device {st.st_dev} != {ddev})"
             if name == ".git":
                 repos.append(t)
                 continue
@@ -204,17 +254,19 @@
         for name in files:
             p = t / name
             try:
-                mode = os.lstat(p).st_mode
+                st = os.lstat(p)
             except OSError:
                 return None, f"{_rel(p, d)} cannot be lstat'ed"
-            if stat.S_ISLNK(mode):
+            if stat.S_ISLNK(st.st_mode):
                 return None, f"{_rel(p, d)} is a symlink"
             if name == ".git":
                 return None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"
-            if not stat.S_ISREG(mode):
+            if not stat.S_ISREG(st.st_mode):
                 return None, f"{_rel(p, d)} is a special file"
-            if os.lstat(p).st_nlink > 1:
+            if st.st_nlink > 1:
                 return None, f"{_rel(p, d)} has more than one hard link"
+            if st.st_dev != ddev:
+                return None, f"{_rel(p, d)} crosses a mount boundary (device {st.st_dev} != {ddev})"
     if len(repos) > REPO_CAP:
         return None, f"fixture holds more than {REPO_CAP} repos"
     return repos, None
@@ -223,8 +275,64 @@
 # ---------- fact 4: the store, classified against the plain-init allowlist ----------
 
 
+def _sub_name_ok(name):
+    """A remote or branch subsection name git itself would write: no empty, dot or dot-dot component."""
+    if name.startswith("-") or name.endswith(".lock"):
+        return False
+    return all(part and part not in (".", "..") for part in name.split("/"))
+
+
+def _config_value(label, sect, sub, key, val, has):
+    """Classify one config value against the key's kind. `has` is whether the line carried `=`."""
+    where = f"{sect}.{sub}.{key}" if sub is not None else f"{sect}.{key}"
+    if sub is not None:
+        if (sect, key) not in CFG_SUB_KEYS:
+            return f"{label}/config key [{sect} \"{sub}\"] {key} is not allowlisted"
+        if not has or not val:
+            return f"{label}/config key {where} needs a value"
+        if VALUE_TEXT.match(val) is None:
+            return f"{label}/config {where} carries a value the parser cannot classify"
+        return None
+    need = CFG_KEYS.get((sect, key))
+    if need is None:
+        if (sect, key) in CFG_TEXT:
+            if not has:
+                return f"{label}/config key {where} needs a value"
+            if VALUE_TEXT.match(val) is None:
+                return f"{label}/config {where} carries a value the parser cannot classify"
+            return None
+        return f"{label}/config key {where} is not allowlisted"
+    if not has:
+        if need != "bool":
+            return f"{label}/config key {where} needs a value"
+        return None
+    low = val.decode("ascii").lower()
+    if need == "bool":
+        if low not in BOOL:
+            return f"{label}/config {where}={low!r} is not a boolean"
+    elif need == "false":
+        if low not in FALSEY:
+            return f"{label}/config {where} must be false"
+    elif need == "0":
+        if low not in ("0", ""):
+            return f"{label}/config {where} must be 0"
+    elif need == "autocrlf":
+        if low not in AUTOCRLF:
+            return f"{label}/config {where}={low!r} is not true|false|input"
+    elif need == "safecrlf":
+        if low not in SAFECRLF:
+            return f"{label}/config {where}={low!r} is not true|false|warn"
+    return None
+
+
 def _config(p, label):
-    """Parse `.git/config` strictly. Anything the parser does not fully classify is refused."""
+    """Parse `.git/config` strictly. Anything the parser does not fully classify is refused.
+
+    Sections: `[core]`, `[user]`, `[init]` and the inert declaration sections `[remote "<name>"]` /
+    `[branch "<name>"]`. A redirect section or key (`[include]`, `[includeIf]`, `[url "<base>"]`,
+    `core.attributesFile`, `core.excludesFile`, `core.hooksPath`, `core.worktree`, `core.fsmonitor`) is not in
+    the tables above and is refused; a value is printable ASCII with no backslash, quote, CR, NUL or non-ASCII.
+    """
     raw = _read(p, CONFIG_CAP)
     if raw is None:
         return f"{label}/config unreadable"
@@ -236,79 +344,88 @@
         return f"{label}/config carries a bare CR"
     if any(b >= 0x80 for b in raw):
         return f"{label}/config carries a non-ASCII byte"
-    sect = ""
+    sect, sub = "", None
     for line in raw.split(b"\n"):
-        s = line.lstrip(b" \t")
+        s = line.strip(b" \t")
         if not s:
             continue
         if s[:1] in (b"#", b";"):
             continue
         if s.startswith(b"["):
             m = SECTION_LINE.match(s)
-            if m is None:
-                return f"{label}/config section header {s[:40]!r} is not plain"
-            sect = m.group(1).decode("ascii").lower()
-            if sect not in CFG_SECTIONS:
-                return f"{label}/config section [{sect}] is not allowlisted"
-            continue
-        m = KEY_LINE.match(s)
+            if m is not None:
+                sect = m.group(1).decode("ascii").lower()
+                sub = None
+                if sect not in CFG_SECTIONS:
+                    return f"{label}/config section [{sect}] is not allowlisted"
+                continue
+            m = SECTION_SUB.match(s)
+            if m is not None:
+                sect = m.group(1).decode("ascii").lower()
+                sub = m.group(2).decode("ascii")
+                if sect not in CFG_SUB_SECTIONS:
+                    return f"{label}/config section [{sect} \"{sub}\"] is not allowlisted"
+                if not _sub_name_ok(sub):
+                    return f"{label}/config section [{sect} \"{sub}\"] has a name git does not write"
+                continue
+            return f"{label}/config section header {s[:40]!r} is not plain"
+        key_raw, eq, val_raw = s.partition(b"=")
+        key_raw = key_raw.strip(b" \t")
+        m = KEY_NAME.match(key_raw)
         if m is None:
             return f"{label}/config line {s[:40]!r} is not a plain key=value"
-        key = m.group(1).decode("ascii").lower()
-        need = CFG_KEYS.get((sect, key))
-        if need is None:
-            return f"{label}/config key {sect}.{key} is not allowlisted"
-        if m.group(2) is None:
-            if need != "bool":
-                return f"{label}/config key {sect}.{key} needs a value"
-            continue
-        val = m.group(2).decode("ascii").lower()
-        if need == "bool":
-            if val not in BOOL:
-                return f"{label}/config {sect}.{key}={val!r} is not a boolean"
-        elif need == "false":
-            if val not in FALSEY:
-                return f"{label}/config {sect}.{key} must be false"
-        elif need == "0":
-            if val not in ("0", ""):
-                return f"{label}/config {sect}.{key} must be 0"
+        why = _config_value(label, sect, sub, m.group(1).decode("ascii").lower(),
+                            val_raw.strip(b" \t") if eq else b"", bool(eq))
+        if why:
+            return why
     return None
 
 
-def _refs(p, label):
+def _refs(p, label, ddev):
     ents = _entries(p)
     if ents is None:
         return f"{label} unreadable"
-    for name, mode, _s, _n in ents:
+    for name, mode, _s, n, dev in ents:
         q = p / name
         if stat.S_ISLNK(mode):
             return f"{_rel(q, label)} is a symlink"
-        if _linked(mode, _n):
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
+        if _linked(mode, n):
             return f"{_rel(q, label)} has more than one hard link"
-        if name not in ("heads", "tags"):
-            return f"{label}/{name} is not refs/heads or refs/tags"
+        if name == "stash":                       # `git stash push` writes the ref as a plain file
+            if not stat.S_ISREG(mode):
+                return f"{label}/stash is not a regular file"
+            body = _read(q, 200)
+            if body is None or HEX40.match(body) is None:
+                return f"{label}/stash is not a 40-hex ref"
+            continue
+        if name not in REF_NAMESPACES:
+            return f"{label}/{name} is not a ref namespace git writes"
         if not stat.S_ISDIR(mode):
             return f"{label}/{name} is not a directory"
-        why = _ref_tree(q, label)
+        why = _ref_tree(q, label, ddev)
         if why:
             return why
     return None
 
 
-def _ref_tree(p, label):
+def _ref_tree(p, label, ddev):
     ents = _entries(p)
     if ents is None:
         return f"{_rel(p, label)} unreadable"
-    for name, mode, _s, _n in ents:
+    for name, mode, _s, _n, dev in ents:
         q = p / name
         if stat.S_ISLNK(mode):
             return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
         if _linked(mode, _n):
             return f"{_rel(q, label)} has more than one hard link"
         if stat.S_ISDIR(mode):
             if not _ref_name_ok(name):
                 return f"{_rel(q, label)} has a name git does not write"
-            why = _ref_tree(q, label)
+            why = _ref_tree(q, label, ddev)
             if why:
                 return why
             continue
@@ -324,30 +441,32 @@
     return None
 
 
-def _objects(p, label):
+def _objects(p, label, ddev):
     ents = _entries(p)
     if ents is None:
         return f"{label} unreadable"
-    for name, mode, _s, _n in ents:
+    for name, mode, _s, _n, dev in ents:
         q = p / name
         if stat.S_ISLNK(mode):
             return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
         if not stat.S_ISDIR(mode):
             return f"{label}/{name} is not a directory"
         if name == "info":
-            inner = _entries(q)
-            if inner is None:
-                return f"{label}/info unreadable"
-            if inner:
-                return f"{label}/info/{inner[0][0]} present (object-store redirect)"
+            why = _obj_info(q, f"{label}/info", ddev)
+            if why:
+                return why
             continue
         if name == "pack":
             inner = _entries(q)
             if inner is None:
                 return f"{label}/pack unreadable"
-            for pname, pmode, _ps, _pn in inner:
+            for pname, pmode, _ps, _pn, pdev in inner:
                 if stat.S_ISLNK(pmode):
                     return f"{label}/pack/{pname} is a symlink"
+                if pdev != ddev:
+                    return f"{label}/pack/{pname} crosses a mount boundary"
                 if not stat.S_ISREG(pmode) or not PACK_FILE.match(pname):
                     return f"{label}/pack/{pname} is not a pack file"
                 if _linked(pmode, _pn):
@@ -358,10 +477,12 @@
         inner = _entries(q)
         if inner is None:
             return f"{_rel(q, label)} unreadable"
-        for oname, omode, _os_, _on in inner:
+        for oname, omode, _os_, _on, odev in inner:
             qq = q / oname
             if stat.S_ISLNK(omode):
                 return f"{_rel(qq, label)} is a symlink"
+            if odev != ddev:
+                return f"{_rel(qq, label)} crosses a mount boundary"
             if not stat.S_ISREG(omode) or not OBJ_FILE.match(oname):
                 return f"{_rel(qq, label)} is not a loose object"
             if _linked(omode, _on):
@@ -369,31 +490,111 @@
     return None
 
 
+def _graph_dir(p, label, ddev):
+    """`.git/objects/info/commit-graphs/`: git's own split-commit-graph names, each a graph file."""
+    ents = _entries(p)
+    if ents is None:
+        return f"{label} unreadable"
+    for name, mode, size, n, dev in ents:
+        q = p / name
+        if stat.S_ISLNK(mode):
+            return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
+        if not stat.S_ISREG(mode):
+            return f"{_rel(q, label)} is not a plain file"
+        if _linked(mode, n):
+            return f"{_rel(q, label)} has more than one hard link"
+        if name == "commit-graph-chain":
+            if size > TEXT_CAP:
+                return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
+            raw = _read(q, TEXT_CAP)
+            if raw is None:
+                return f"{_rel(q, label)} unreadable"
+            for line in raw.split(b"\n"):
+                if line and CHAIN_ROW.match(line + b"\n") is None:
+                    return f"{_rel(q, label)} carries a row git does not write"
+            continue
+        if GRAPH_NAME.match(name) is None:
+            return f"{_rel(q, label)} is not a graph file name"
+        head = _read(q, 8)
+        if head is None or len(head) < 8 or not head.startswith(CG_MAGIC):
+            return f"{_rel(q, label)} is not a commit-graph file"
+    return None
+
+
+def _obj_info(p, label, ddev):
+    """`.git/objects/info/`: only git's own `packs`, `commit-graph` and `commit-graphs/` shapes.
+
+    Anything that can redirect the object store (`alternates`, `http-alternates`, ...) stays refused.
+    """
+    ents = _entries(p)
+    if ents is None:
+        return f"{label} unreadable"
+    for name, mode, size, n, dev in ents:
+        q = p / name
+        if stat.S_ISLNK(mode):
+            return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
+        if not stat.S_ISREG(mode) and not (name == "commit-graphs" and stat.S_ISDIR(mode)):
+            return f"{_rel(q, label)} is not a plain file"
+        if _linked(mode, n):
+            return f"{_rel(q, label)} has more than one hard link"
+        if name == "packs":
+            if size > TEXT_CAP:
+                return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
+            raw = _read(q, TEXT_CAP)
+            if raw is None:
+                return f"{_rel(q, label)} unreadable"
+            for line in raw.split(b"\n"):
+                if line and PACKS_ROW.match(line + b"\n") is None:
+                    return f"{_rel(q, label)} carries a row git does not write"
+            continue
+        if name == "commit-graph":
+            if size > CONFIG_CAP:
+                return f"{_rel(q, label)} exceeds {CONFIG_CAP} bytes"
+            head = _read(q, 8)
+            if head is None or len(head) < 8 or not head.startswith(CG_MAGIC):
+                return f"{_rel(q, label)} is not a commit-graph file"
+            continue
+        if name == "commit-graphs":
+            why = _graph_dir(q, f"{label}/commit-graphs", ddev)
+            if why:
+                return why
+            continue
+        return f"{_rel(q, label)} is not a plain object-info entry (object-store redirect)"
+    return None
+
+
 def _log_name_ok(rel):
-    """A reflog lives at `HEAD` or under `refs/heads|refs/tags` with git's own name shape."""
-    if rel == "HEAD":
+    """A reflog lives at `HEAD`, at `refs/stash`, or under git's ref namespaces with git's own name shape."""
+    if rel in ("HEAD", "refs/stash"):
         return True
-    m = re.fullmatch(r"refs/(?:heads|tags)/(.+)", rel, re.ASCII)
+    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", rel, re.ASCII)
     if not m:
         return False
     return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))
 
 
-def _logs(p, label, prefix=""):
+def _logs(p, label, ddev, prefix=""):
     ents = _entries(p)
     if ents is None:
         return f"{label} unreadable"
-    for name, mode, size, n in ents:
+    for name, mode, size, n, dev in ents:
         q = p / name
         rel = prefix + name
         if stat.S_ISLNK(mode):
             return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
         if _linked(mode, n):
             return f"{_rel(q, label)} has more than one hard link"
         if stat.S_ISDIR(mode):
-            if not (rel in ("refs", "refs/heads", "refs/tags") or _log_name_ok(rel)):
+            if not (rel in ("refs", "refs/heads", "refs/tags", "refs/notes")
+                    or (_log_name_ok(rel) and rel != "refs/stash")):
                 return f"{_rel(q, label)} has a name git does not write"
-            why = _logs(q, label, rel + "/")
+            why = _logs(q, label, ddev, rel + "/")
             if why:
                 return why
             continue
@@ -406,14 +607,16 @@
     return None
 
 
-def _hooks(p, label):
+def _hooks(p, label, ddev):
     ents = _entries(p)
     if ents is None:
         return f"{label} unreadable"
-    for name, mode, _s, _n in ents:
+    for name, mode, _s, _n, dev in ents:
         q = p / name
         if stat.S_ISLNK(mode):
             return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
         if not stat.S_ISREG(mode) or not name.endswith(".sample"):
             return f"{_rel(q, label)} is not a hook sample"
         if _linked(mode, _n):
@@ -421,6 +624,40 @@
     return None
 
 
+def _info(p, label, ddev):
+    """`.git/info/`: git's `exclude`, and the `refs` file `git gc`'s update-server-info writes.
+
+    `info/attributes` and every other name stay refused: the allowlist is the point.
+    """
+    ents = _entries(p)
+    if ents is None:
+        return f"{label} unreadable"
+    for name, mode, size, n, dev in ents:
+        q = p / name
+        if stat.S_ISLNK(mode):
+            return f"{_rel(q, label)} is a symlink"
+        if dev != ddev:
+            return f"{_rel(q, label)} crosses a mount boundary"
+        if not stat.S_ISREG(mode):
+            return f"{_rel(q, label)} is not a plain file"
+        if _linked(mode, n):
+            return f"{_rel(q, label)} has more than one hard link"
+        if name == "exclude":
+            continue
+        if name == "refs":
+            if size > TEXT_CAP:
+                return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
+            raw = _read(q, TEXT_CAP)
+            if raw is None:
+                return f"{_rel(q, label)} unreadable"
+            for line in raw.split(b"\n"):
+                if line and INFO_REFS.match(line + b"\n") is None:
+                    return f"{_rel(q, label)} carries a line git does not serve"
+            continue
+        return f"{_rel(q, label)} is not a plain `.git/info` entry"
+    return None
+
+
 def _packed(p, label):
     raw = _read(p, CONFIG_CAP)
     if raw is None:
@@ -450,16 +687,18 @@
     return None
 
 
-def _store(gd, label):
+def _store(gd, label, ddev):
     """Classify one `.git` directory, entry by entry, against what `git init` + commits writes."""
     ents = _entries(gd)
     if ents is None:
         return f"{label} unreadable"
     have = set()
-    for name, mode, size, n in ents:
+    for name, mode, size, n, dev in ents:
         q = gd / name
         if stat.S_ISLNK(mode):
             return f"{label}/{name} is a symlink"
+        if dev != ddev:
+            return f"{label}/{name} crosses a mount boundary"
         if name not in GIT_TOP:
             return f"{label}/{name} is not a plain-init entry"
         have.add(name)
@@ -473,8 +712,8 @@
             return f"{label}/{name} has more than one hard link"
         if name == "HEAD":
             body = _read(q, 200)
-            if body is None or HEAD_REF.match(body) is None:
-                return f"{label}/HEAD is not a plain branch HEAD"
+            if body is None or (HEAD_REF.match(body) is None and HEAD_HEX.match(body) is None):
+                return f"{label}/HEAD is not a branch line or a detached sha"
         elif name == "ORIG_HEAD":
             body = _read(q, 200)
             if body is None or HEX40.match(body) is None:
@@ -500,26 +739,21 @@
         if req not in have:
             return f"{label} has no {req}"
     if "hooks" in have:
-        why = _hooks(gd / "hooks", f"{label}/hooks")
+        why = _hooks(gd / "hooks", f"{label}/hooks", ddev)
         if why:
             return why
     if "info" in have:
-        inner = _entries(gd / "info")
-        if inner is None:
-            return f"{label}/info unreadable"
-        for name, mode, _s, _n in inner:
-            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode) or name != "exclude":
-                return f"{label}/info/{name} is not git's exclude file"
-            if _linked(mode, _n):
-                return f"{label}/info/{name} has more than one hard link"
+        why = _info(gd / "info", f"{label}/info", ddev)
+        if why:
+            return why
     if "logs" in have:
-        why = _logs(gd / "logs", f"{label}/logs")
+        why = _logs(gd / "logs", f"{label}/logs", ddev)
         if why:
             return why
-    why = _objects(gd / "objects", f"{label}/objects")
+    why = _objects(gd / "objects", f"{label}/objects", ddev)
     if why:
         return why
-    why = _refs(gd / "refs", f"{label}/refs")
+    why = _refs(gd / "refs", f"{label}/refs", ddev)
     if why:
         return why
     return None
@@ -548,14 +782,15 @@
     if not stat.S_ISDIR(st.st_mode):
         return "fixture dir is not a directory"
     d = pathlib.Path(_norm(dpath))
+    ddev = st.st_dev
     vals, why = _argv(d, tool, argv)
     if why:
         return why
-    repos, why = _tree(d)
+    repos, why = _tree(d, ddev)
     if why:
         return why
     for repo in repos:
-        why = _store(repo / ".git", f"{_rel(repo / '.git', d)}")
+        why = _store(repo / ".git", f"{_rel(repo / '.git', d)}", ddev)
         if why:
             return why
     lane_tok = vals.get("--lane")
```

## 8. Limits and risks (named, not hidden)

1. **Same-filesystem bind mounts are not detectable inside `d`.** `M3`/`M4` (§5.8) are admitted: a bind mount of
   the same device below `d` is lexically identical to a plain directory, and the only in-`d` signal
   (`st_dev`) is equal. Detecting it needs `/proc/self/mountinfo`, i.e. a read outside `d` the advertisement
   forbids. For such a fixture the guarantee is the advertised one: every path the decision names/stats/opens is
   inside `d`, and the classified store has the plain-init shape. Cross-device mounts are refused (`M1`, `M2`).
2. **In-`d` linked worktrees and in-`d` alternates stay refused** (`.git` gitdir file, `.git/commondir`,
   `objects/info/alternates`). `w1/R48C1HoStore.md` proposes them as honest classes; they are *not* in the frozen
   wave-1 population file, and admitting them needs target resolution plus a two-store model (variant-B work).
   If stage 2 freezes such a class as HONEST, this variant fails the honest leg on it — the L1 must either not
   freeze that class or land a variant that models the indirection.
3. **A local `git clone` inside `d` stays refused** (`refs/remotes` and `[remote]` alone is not enough; the
   population has no clone). Named rather than silently allowed.
4. **`[remote "<n>"] url` may name a path or host outside `d`** and is admitted as an inert declaration
   (`git remote add` writes exactly that; the fence reads no byte of it, and the gated tools run no fetch). If the
   L1 judges remote URLs hostile by policy, the value charset for `url` must be narrowed to URL syntax — a frozen
   predicate change, not a seat decision.
5. **Config values are validated by charset, not by grammar**: printable ASCII without backslash, quote, CR, NUL
   or non-ASCII, ≤1024 bytes, for text keys and subsection values. Git's quoted/escaped value form is refused
   (conservative allowlist, not a parse of every legal syntax).
6. **`objects/pack/multi-pack-index` is refused** (`git gc` on this host does not write it; a repo with
   `gc.writeMultiPackIndex=true` and a gc would be over-refused). Not in the frozen population.
7. **Instrument limits inherited unchanged** from the round-46 envelope: host paths outside the scratch root are
   not counted (so `/etc`, `/proc`, `/sys` reads by a fence are invisible), `io_uring` SQE opens are untraced, a
   directory stat's `st_nlink` channel is nulled by padding rather than measured. My measurement therefore proves
   "no traced access outside `d` under the scratch root", not "no syscall to any absolute path".
8. **No scored run exists** (§1), so nothing here is a C1 verdict; the candidate must be re-measured by the stage-2
   pinned counter on a clean clone of the landing tip.

## 9. Files, scratch, and handoff

- Lane: **no file written, no commit, no mutating git/jj call**; clone at `a543d920` used read-only; lane tree
  untouched (`git -C lane status --porcelain` → 0 lines before and after every run).
- Scratch (removed before yield, receipts transcribed above): `fence_a.py` (candidate), `probe.py`, `neg.py`,
  `shapecheck.py`, `mountprobe.py`, `honest/nc1…nc9` (18 fixtures), `lane/` (shared clone), `receipts/`.
- Handoff: land the §7 diff as `plans/fixture_fence.py`; the stage-2 pin is then the candidate sha256
  `b687b1d9…0ca52`. Suggested post-integration checks for the main agent: the pinned
  `plans/round48_c1_verify.py` on a clean clone (HONEST must be the pinned population, REFUSALS 20/20,
  SEALED `<S>`/`<S>`, `CALIBRATION advertised=<20+S> contradicted=0`), plus the frozen pre-receipt controls
  (base fence must fail with `HONEST … refused≥9`).

## 10. Sources opened (access date 2026-10-27; local URLs, no external URL was opened)

| source | located quote (≤25 words) |
|---|---|
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` §C1 | “C1 passes iff the counter prints `PINS total=<P> mismatched=0`”; also “a fixture admitted with `touches=0` is reported as `BENIGN-ADMIT`” |
| `…/corpus/lessons/round-46-verifier-spotcheck.md` (routed defects 1) | “repair over-refusal (9/9 novel honest controls refused) and broaden positive controls” |
| `…/.ufo/waves/round-46/w2/R46W2C1HoHonest.md` | “all nine are newly named modules in the counter's `--sealed` override” |
| `…/.ufo/waves/round-46/w2/R46W2C1Intent.md` (finding, medium) | “lexical containment is not backing-store containment” |
| `…/plans/fixture_fence.py` @`a543d920` (`_config` docstring) | “Parse `.git/config` strictly. Anything the parser does not fully classify is refused.” |
| `…/plans/round46_c1_verify.py` (rule f) | “a touch is any path under the scratch root that is neither `d` nor under the harness directory” |
| `…/plans/round44_c1_verify.py` (`Ctx` docstring) | “What a battery build() may use. Runs only inside the build child.” |
| `…/.ufo/waves/round-48/w1/R48C1ExecHonest/README.md` + `population.txt` | “total | **120** | 85 `anchor`, 35 `order`; 0 duplicate `fid`” |
| `…/.ufo/waves/round-48/w1/R48C1ExecHonest/modules/novel48/n1{0..6}*.py` | “`git remote add origin <url>` is what every repository with a remote carries” (n13) |
| `…/.ufo/waves/round-48/w1/R48C1HoStore.md` | “The current fence's `_tree` rejects any `.git` file as “gitdir redirect”” |
| `…/.ufo/waves/round-48/w1/R48C1HoConfig.md` | “`user.name`/`user.email` name no path, run no program and redirect nothing outside `d`” |
| `…/plans/refusals46/f7_commondir.py` | “a hand-written `.git/commondir` sends refs, objects and config to a store built BESIDE d” |
| `…/plans/refusals46/f15_objects_symlink_out.py` | “`.git/objects` is renamed out of `d` … and replaced by a symlink back to it” |
| `…/plans/sealed46/p_info_redirect.py` | “Hostile filesystem-shape module: object-info directory redirected outside the fixture.” |
| `…/plans/sealed46/s_packed_refs.py` | “packed-refs … symlink_to(outside / "packed-refs")” (module body) |
| `file:///home/vgpnk/.omp/agent/RULES.md` | “Record every install or update … in your report or handoff” — no tool was installed or updated |

VERDICT: **variant A candidate complete and measured — 34/34 novel honest fixtures (18 mine + 16 from the frozen
wave-1 population) admitted with `touches=0`, 104/104 standing battery admitted, 20/20 refusals46 + 12/12 sealed46
modules refused with `touches=0`, 26/26 negative probes of the new surface refused, cross-device mounts refused,
same-device mounts named as a limit; NO scored counter run (stage-2 freeze absent at `a543d920`), no admission
claimed.**
