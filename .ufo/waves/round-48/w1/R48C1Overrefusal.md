# R48C1Overrefusal — calibration critic

Axes named: **calibration** (primary); coverage/novelty are not judged. Item: novel honest repository-state fixtures, representativeness of the frozen honest leg, and the base/do-nothing fence's ability to reach the C1 target.

## Freeze / measurement boundary

I cloned the lane into the authorized scratch root and checked out `a543d92083557dd9b33ee674e9b99b03411f80af`. Output: `HEAD=a543d92083557dd9b33ee674e9b99b03411f80af`; top-level `/fast/scratch/hyaku/kengaku-r48/R48C1Overrefusal/lane`. `git log` shows the claims-file commit at `a543d920`, timestamp `2026-10-27 06:53:29 -0300`; the claims say `Freeze amendments: None yet. Stage 2 fills literals and pins only.` `plans/round48_c1_verify.py` is absent at this frozen revision. Thus the stage-1 claim is committed and predates this review, but the stage-2 v3 counter/population pins do not yet exist. **No counter/probe/scored execution was run.** I did not run claimed work or treat these fixture recipes as a score/receipt.

Exact inspection commands run (all from the scratch clone unless stated):
- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`
- `git checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`
- `git rev-parse HEAD`; `git rev-parse --show-toplevel`; `git log --format='%H %ci %s' -3`
- `git log --format='%H %ci %s' --oneline -1 -- plans/round-48-claims.md`
- `git show HEAD:plans/round-48-claims.md | tail -5`
- `git ls-tree HEAD plans/ | grep -E 'round48_c1_verify|fixture_fence'`
Observed key lines: `a543d920... 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze...`; `None yet. Stage 2 fills literals and pins only.`; only `plans/fixture_fence.py` was listed. The working lane itself was at `bf783c1...` with untracked wave material, so I used only the frozen clone.

## Novel honest fixture recipes authored

Scratch-only module sources were authored at `novel/novel_refs.py` and `novel/novel_states.py` under the unique scratch root; these use the round-44 `Ctx` builder contract and are candidates for stage-2 population inclusion (not committed, not measured). They cover:

- shallow and full local clones (remote config/refs), replace refs, notes refs, stash refs/reflogs;
- annotated tag plus `pack-refs --all --prune` (peeled packed refs);
- linked worktree, tracked symlink, bare clone, core.autocrlf config, fresh unborn init;
- submodule add/deinit/removal residue; archive-export/import shape;
- interrupted rebase, conflicted merge, in-progress cherry-pick, commit-graph, multi-pack-index;
- reproductions by description of detached HEAD, 30-commit history, merge commit, and ignored-file states from the round-46 nine.

These are recipe-level proposals only: there are no observed per-fixture fence verdicts. In particular, the archive-export helper models a plain re-imported tree; it does not retain an actual `git archive` payload, so that fixture should not be treated as a demonstrated export control. The submodule helper uses `check=False` for submodule setup and could silently fail to create the intended residue; it needs a builder receipt/structural assertion before inclusion. Several fixtures intentionally make a sharp test: the base allowlist explicitly permits peeled packed-ref lines, so peeled tags may be admitted even though the r46 narrative names annotated/packed tags among refused classes. This tension requires execution against the committed base fence before stage 2, not inference from class labels.

## Representativeness and do-nothing analysis

The round-48 frozen population is 104 battery-built fixtures + the nine round-46 classes + wave-1 critic classes. The round-46 report describes those nine as plain `git init` states (packed refs, tags, detached HEAD, merge, ignore/history/reflog variants). The base fence source explicitly defines a *plain-init allowlist*: `_store` admits only `GIT_TOP`, `refs/heads|tags`, narrow `[core]` config, and empty `objects/info`; `_tree` rejects any symlink and `.git` file. Therefore the named new shapes—clone remotes, `refs/replace`, notes/stash refs, shallow metadata, worktree metadata/files, object metadata, common config options, and tracked symlinks—exercise distinct unrepresented on-disk forms. The frozen nine by themselves are not representative of ordinary cloned/modern/in-progress repositories. Stage 2 should include the successful recipes and preserve the distinction between ordinary repo metadata and outside-path behavior; otherwise an honest refusal rate can remain misleadingly low-dimensional.

Do-nothing: the unchanged base fence cannot meet the frozen C1 honest target if the nine round-46 fixtures are included: stage-1 explicitly freezes the base-fence control as failing with at least nine honest refusals, and the r46 report says `9/9 were refused`. An admit-all fence cannot meet the whole target because C1 also requires all refusal/sealed hostile modules clean; refuse-all cannot meet HONEST. These are contract/evidence deductions, not new executions. I did not run the v3 counter or claim that any fence variant passed a scored predicate.

## Sources opened

Access date: 2026-10-27.
- `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` — not opened by this seat; no quote claimed.
- Local `plans/round-48-claims.md` at frozen revision — quote: “honest population frozen at stage 2” (six words).
- Local `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` — quote: “all nine were refused” (five words).

## Limits

No stage-2 counter, exact frozen population, or pins existed at the frozen base; no scored run was made. The authored fixture modules remain unvalidated and scratch-only, including the noted archive/submodule construction limitations. The direct conclusion about representativeness is source-structure-based; novel fixture outcomes against the base fence remain unknown. No tool installs/updates.

VERDICT: **calibration critique — frozen nine alone are not representative; do-nothing/base fence cannot meet the C1 honest target; stage-2 scored determination blocked until stage-2 freeze exists.**