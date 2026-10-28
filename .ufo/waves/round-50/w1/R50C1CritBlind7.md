# R50C1CritBlind7 — two more blind hostile modules against the repaired fence

Seat: `R50C1CritBlind7` (critic, novelty) · wave `round-50/w1` · item: author TWO blind hostile modules under
`C1CritBlind7/sealed/` — (i) a store directory that is a SYMLINK to the real store inside `d`, (ii) a gitfile
naming a store reached through a SYMLINKED PARENT inside `d`.

REV 8acd0f830452198706c21af8bc52d611c0f29177 (lane tip at measurement; freeze `3b02d573…` verified an ancestor:
`git -C <lane> merge-base --is-ancestor 3b02d57… HEAD` → rc 0)
FENCE measured `plans/fixture_fence.py` sha256 `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`
COUNTER `plans/round50_c1_verify.py` sha256 `850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999`
POPULATION pin `b5197f94…3fae69` (126 rows) · host git 2.56.0, python 3.14.8.
VERDICT **deliver** (both modules refused at the tip fence, for the symlink leg, with a unique kill direction).

## Axes named

| axis | why it is the axis | move | outcome |
|---|---|---|---|
| A1 hostile-shape novelty — a kill direction no landed module has | C1 is claimed on *novelty*; a sealed module that only re-catches what `s50_01`/`s50_gitfile_symlink_chain`/`s6_gitfile_rel_objects_link` already catch adds no discriminating power | two inside-`d` symlink shapes (final component / intermediate component) | **improved**: each has a kill direction that neither the 20 sealed nor the 20 refusals modules have (measured below) |
| A2 fence-policy consistency — refused for the intended reason, not incidentally | a module refused because its repo is broken or its argv is malformed is not evidence about the symlink leg | paired controls: the same fixtures with the symlink replaced by a real directory | **improved**: controls ADMIT, hostile twins BREACH; refusal text names the symlink entry; both repos live (`rev-parse HEAD` rc 0) |
| A3 integration cost — counter leg clean, no collateral | a new sealed module that breaks the HONEST leg or fails to build sinks the round's scored run | built through the lane's own builder; counter run with both modules present | **improved**: `HONEST 126/126`, `SEALED total=22 clean=22 leaked=0`, `PREDICATE R50-C1 pass` |

## Deliverables (in this wave dir)

| file | sha256 | shape |
|---|---|---|
| `C1CritBlind7/sealed/b7_symlink_store_inside_d.py` | `93697a6e48f73b472cd53eff9f431ef23af1b3e09d84f877c28d4f057c782c17` | `d/wt/.git` = `gitdir: ../store`; `d/store` is a **symlink → `realstore`**; `d/realstore/` is the plain store; two commits. Fid `b7a-gitfile-store-symlink-inside-d`, tool `order`, argv `--lane wt --claims … --receipt …` |
| `C1CritBlind7/sealed/b7_symlink_parent_in_gitfile.py` | `67fca824aa9f97ecca87a1ed28c81e7e32ec2ee14dc62ca00652b9ddc0387be9` | `d/lane/.git` = `gitdir: ../alias/gitstore`; **`d/alias` is a symlink → `rho/hold`**; `d/rho/hold/gitstore/` is a real plain store; two commits. Fid `b7b-gitfile-symlinked-parent-inside-d`, tool `order`, argv `--lane lane --claims … --receipt …` |

Probes and receipts: `C1CritBlind7/probes/` (driver, paired controls, three scratch mutant fences),
`C1CritBlind7/receipts/` (all verbatim runs, `identity.json`, `module.sha256`, `rev.txt`).

Shape of the two fixtures (both are the honest `n21_separate_gitdir` gitfile text; the only difference is the
symlink):

```
b7a:  d/wt/.git -> "gitdir: ../store"     d/store -> realstore (symlink)   d/realstore/  (plain store)
b7b:  d/lane/.git -> "gitdir: ../alias/gitstore"   d/alias -> rho/hold (symlink)   d/rho/hold/gitstore/ (plain store)
```

## What was run (commands, exact)

Fixture clone: `git clone --shared <lane> $S/lane` then `git -C $S/lane checkout 3b02d57…` **once** (freeze tree,
never measured), and the measured tip tree produced **without a checkout**:
`git -C $S/lane archive 8acd0f8… | tar -x -C $S/tip`. The lane checkout was only read (`git log`, `sha256sum`);
`git -C <lane> status --porcelain` after the seat's work shows only the wave's own untracked report dir.

1. Decision per fixture, out of process, through the counter's own frozen harness text
   (`round50_c1_verify.HARNESS`), cwd = fixture dir, `-I`, `HOME=/nonexistent`, verdict as exit status —
   `python3 probes/drive.py --lane $S/tip --modules … --work $S/workN`
2. Counter's own legs with both modules dropped into a scratch copy of `plans/sealed50/`:
   `python3 plans/round50_c1_verify.py --lane . --skip-mutants --allow-dirty --work $S/tmp/cw1`
   (the tip tree is an archive extract, so `REV unknown`, `TREE dirty=0`; `--allow-dirty` was required for that
   reason only — the lane itself was never dirtied).
3. Kill-direction witnesses: three scratch mutant fences in `probes/` run through the same counter with
   `--fence`.

## Observed (verbatim)

### Both modules refused at the tip fence; paired controls admitted

`receipts/delivered-files-tip-fence.txt` (delivered files, `PYTHONDONTWRITEBYTECODE=1`):

```
FENCE …/tip/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
MODULE b7_symlink_store_inside_d.py sha256=93697a6e48f73b472cd53eff9f431ef23af1b3e09d84f877c28d4f057c782c17
b7a-gitfile-store-symlink-inside-d    verdict=BREACH reason='BREACH store is a symlink'  symlinks=['store'] gitdir_inside_d=True head_rc=0 tree=5929fddf9322712a
MODULE b7_symlink_parent_in_gitfile.py sha256=67fca824aa9f97ecca87a1ed28c81e7e32ec2ee14dc62ca00652b9ddc0387be9
b7b-gitfile-symlinked-parent-inside-d verdict=BREACH reason='BREACH alias is a symlink'  symlinks=['alias'] gitdir_inside_d=True head_rc=0 tree=9c307a21bba7ee65
MODULE ctl_b7_twins.py sha256=0ee89bf5…
ctl-b7a-real-store   verdict=ADMIT reason='ADMIT' symlinks=[] gitdir_inside_d=True head_rc=0
ctl-b7b-real-parent  verdict=ADMIT reason='ADMIT' symlinks=[] gitdir_inside_d=True head_rc=0
```

Refusal-leg attribution (direct call, `fence._tree(d, dev)`): `f000 tree_reason= 'alias is a symlink'` and
`f000 tree_reason= 'store is a symlink'` — i.e. the **fixture walk** (docstring structure item 3, "no symlink
anywhere") refuses, before the gitfile target is resolved and before any store entry is classified. That is the
intended leg: the gitfile text is inside `d` lexically and the resolved gitdir is inside `d`
(`gitdir_inside_d=True` for both), so *containment cannot be the reason* — only the symlink can.

Materiality (the refusal cannot be excused as "the repo was broken"): through the symlinked store,
`git -C <lane> rev-parse --absolute-git-dir` succeeds (`…/realstore`, `…/rho/hold/gitstore`) and
`rev-parse --verify HEAD` answers `68f76e622abe5894625f0a8a8cb11fc8040e0046` / `8b631df5ddf3fc458cab718d7bbd0dd3ba9de6b1`
(rc 0) for b7a / b7b. The gitfile text is written by the same `git init --separate-git-dir` invocation the honest
`n21` class uses; only the symlink is added.

Reproducibility: two independent builds give identical identities — b7a `5929fddf…`, b7b `9c307a21…`
(`receipts/blind-modules-tip-fence.txt` vs `receipts/blind-modules-tip-fence-repeat.txt`, IDENTICAL), and the
volatile `index` of the gitfile-named store is masked by the builder's own `gitfile_index_paths` rule.

### Counter legs with both modules in `plans/sealed50/` (scratch copy of the tip tree)

`receipts/counter-tip-fence-with-b7-modules.txt`:

```
REV unknown
TREE dirty=0
FENCE …/tip/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=22 clean=22 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

So the delivered modules are counted clean by the counter's own SEALED leg (20 landed + 2 = 22, floor
`SEALED50_MIN=6`, claim's stated `≥18`), and the HONEST and REFUSALS legs are unchanged.

### Kill directions witnessed (scratch mutant fences of the tip fence, `--fence`)

| mutant (probe file) | change | SEALED leg | who is admitted |
|---|---|---|---|
| `mutant_resolve_admit.py` (`…c8654f`) | tree walk **skips** symlinks instead of refusing | `total=22 clean=18 leaked=4` | b7a, b7b, `s50_01_stray_symlink`, `s50_gitfile_symlink_chain` |
| `mutant_contain_all.py` (`…695abff`) | tree walk **resolves** a symlink and admits it when the target stays inside `d` (dirs and files) — the coherent "admit `n21`/`n20` by resolution" repair | `total=22 clean=20 leaked=2` | **only b7a and b7b**; every refusal module and every other sealed module stays refused |
| `mutant_contain_final_lstat.py` (`…097f10e`) | as above **plus** `os.path.islink()` on the resolved store directory | `total=22 clean=21 leaked=1` | **only b7b** (the final component `gitstore` is real; only its parent `alias` is the symlink) |

All three runs keep `HONEST 126/126`, `REFUSALS 20/20 clean`, `SEALED total=12 clean=12`, and end
`PREDICATE R50-C1 fail` on the leak — i.e. the modules fire inside the round's frozen predicate currency. The
row-2 result is the novelty evidence: with the natural repair shape, **no landed module catches the fixture**; the
two delivered modules are the only ones that do. Row 3 is why the item asked for two modules and not one: b7a is
caught by "the store must not be a symlink", b7b is not — the pair separates "store *is* a symlink" from "store is
*reached through* a symlink", and the fence's invariant refuses both.

Candidate mutant rows for `plans/mutants50/` (if the mutant owner wants them; Q38 witnessed, not assumed):
`receipts/mutant-candidate-resolve-admit.diff`, `…-mutant_contain_all.diff`,
`…-mutant_contain_final_lstat.diff`. Each is an inline `-p1` diff against `plans/fixture_fence.py@57adce4a`, and
each row's kill direction is the table above (the admitted fixtures are named in the receipts).

## Distinctness from the landed sealed/refusal set (measured, not asserted)

- `s50_01_stray_symlink`: symlink **outside any store**, target outside `d` — skipped entirely by the
  containment mutant only because it is a *file* symlink; in the coherent `contain_all` mutant it is refused
  (target outside `d`), so it does not witness my shape.
- `s50_gitfile_symlink_chain`: gitfile → two-symlink chain ending **outside `d`**; refused by containment.
- `s6_gitfile_rel_objects_link` (`seal6-gitfile-up-inside-link`, `…-submodule-store-link`): gitfile target is a
  real directory, the escape is a symlinked `objects` / `modules/sub` pointing **outside `d`**.
- No landed module (20 sealed + 20 refusals) is admitted by `mutant_contain_all` — measured, `leaked=0` for them.

## Limits (named)

- These modules pin the fence's **advertised invariant** ("no symlink anywhere in `d`", docstring item 3), not the
  outside-`d` read property: an admission by the `contain_all` mutant does **not** make a tool read outside `d`
  (the resolved store is inside `d`). The hostile set is therefore a policy witness; the outside-`d` read
  measurement stays with `plans/round46_c1_verify.py` and is not re-scored here.
- Corollary for the honest set: the 126-fixture population is symlink-free by construction
  (`structural_audit`), so a future widening that admits inside-`d` symlinks would pass every honest fixture and
  make these two modules false positives. Their bite depends on the invariant staying as written; if the lane
  ever decides symlinks are admissible, these modules must be withdrawn in the same commit, not silently kept.
- Both fixtures are hand-forged states (gitfile text is git's `--separate-git-dir` shape, the symlink is the
  agent's addition) — that is the definition of the sealed set, not a git-written honest state.
- Both refusals land on the **walk**, so the modules do not independently exercise the store-classification leg;
  a fence that refuses at the walk and would also mis-classify the store is not distinguished by them.
- Counter receipt was produced on an archive extract of `8acd0f8` (`REV unknown`, `--allow-dirty`), not on a
  clone of the landing tip; the lane checkout was never dirtied (`status --porcelain` shows only the wave dir).
  The frozen predicate run itself remains the L1's S3 receipt.
- No tool install or upgrade was needed for this seat (`pacman` untouched, nothing added to `~/.local/bin`).
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind7` was removed after the receipts were copied here;
  nothing of the seat's work remains outside this wave dir.

## Handoff for the L1 (integration, not done by this seat)

1. Copy `C1CritBlind7/sealed/b7_symlink_store_inside_d.py` and `…/b7_symlink_parent_in_gitfile.py` into
   `plans/sealed50/` (files are lane-ready: builder contract `build(ctx, d) -> argv`, `FIXTURES` list, no lane
   path baked in, no `/tmp` string; `--work` is the counter's).
2. Do **not** copy `probes/ctl_b7_twins.py` into `plans/sealed50/`: it is the paired control and is expected to be
   ADMITTED; landing it there would fail the SEALED leg by design.
3. After landing, the SEALED leg becomes `total=22` (both dirs) with `clean=22` on the current fence; re-run the
   scored predicate on a clean clone as the S3 receipt.
4. If the mutant battery is re-derived, the three `receipts/mutant-candidate-*.diff` rows carry witnessed kill
   directions; the Q38 witness for each is the `SEALED-MISS` line set in the matching receipt.
