# R49C1HoStore — benign Git metadata counterexamples

Axes: **calibration** (classification of honest in-`d` metadata versus expected refusal); **evidence integrity** (freeze gate and trace boundaries). This seat does not judge/admit C1 or C2.

## Freeze gate

Commands:
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `commit`
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %an %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 kengaku-shokunin round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)`
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD && echo ANCESTOR-OF-HEAD` → `ANCESTOR-OF-HEAD`
- At that frozen commit, `plans/round-49-claims.md` says: “Stage 1 (this commit): the predicate sentence, the counter contract and its deltas, the controls that must fail, and the kill rule” (§Freeze shape).

Stage 1 exists and predates my fixture measurements. The v3 stage-2 counter/population/pins are not in this commit; **no scored counter/probe was run**. I ran only an isolated developmental `breach()` inspection on the base fence, not a C1 score or admission test.

## Counterexample and exact receipts

Base source: `plans/fixture_fence.py` at the frozen base, SHA256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`. Its `_tree` refuses every `.git` file; `_store` permits only the plain-init allowlist and rejects `commondir` and any nonempty `objects/info` (including `alternates`). These are shape refusals without resolving whether the target is inside `d`.

Scratch clone: `git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`, then checkout `9d2900af41e4d1fc6022eff99010436fde6dbd93`. `git rev-parse HEAD` → that exact revision; `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C1HoStore/lane`.

Constructed functional honest Git metadata under each fixture `d`:
- linked worktree via `git worktree add d/wt HEAD`: `git -C d/wt rev-parse --show-toplevel` returned `d/wt`; `--git-dir` returned `d/repo/.git/worktrees/wt`; `--git-common-dir` returned `d/repo/.git`. The `.git` pointer and `commondir` target are in `d`.
- separate gitdir via `git init --separate-git-dir d/store d/wt`: `d/wt/.git` says `gitdir: <d>/store`; `git -C d/wt rev-parse --git-dir` returned `<d>/store`; config is plain `[core]` and store is inside `d`.
- alternate object store: a native `git init` clone fixture with `d/clone/.git/objects/info/alternates` naming `d/main/.git/objects`; `git -C d/clone rev-parse --show-toplevel` returned `d/clone`; `git -C d/clone fsck` resolved the borrowed object (reported `dangling commit …`). Both stores are inside `d`.
- common-dir fixture: `.git/commondir` content `../../store/common`; `git -C d/repo rev-parse --git-common-dir` returned `<d>/store/common`; repository commit succeeded.

Base fence driver was run under `/usr/bin/strace -f -y` with the counter's open/stat/readlink/exec trace family, cwd=`d`, per-run logs in scratch `logs/`. Exact observed classifications (return code 10 = breach; independent touch analyzer applied B5 directory-stat exclusion; all were 0 outside touches):
```
h1_linked_worktree lane=repo: BREACH wt/.git is a file (gitdir redirect), not a directory; OUTSIDE-TOUCHES 0
h1_linked_worktree lane=wt: BREACH wt/.git is a file (gitdir redirect), not a directory; OUTSIDE-TOUCHES 0
h2_separate_gitdir lane=wt: BREACH wt/.git is a file (gitdir redirect), not a directory; OUTSIDE-TOUCHES 0
h3b_alternates_no_remote lane=clone: BREACH clone/.git/objects/info/alternates present (object-store redirect); OUTSIDE-TOUCHES 0
h4_commondir_inside lane=repo: BREACH repo/.git/commondir is not a plain-init entry; OUTSIDE-TOUCHES 0
```
An additional `git clone --shared` run was refused earlier at its ordinary `[remote "origin"]` config section before reaching alternates; h3b isolates the alternate condition without remote config. The trace initially displayed one `readlink(<scratch root>) = -1 EINVAL`; it is a directory, hence B5's directory-stat exception; corrected analyzer output for all runs is zero outside touches. These are base-fence developmental observations only, not stage-2 receipts.

Expected-refusal counterparts were also built: external gitfile/store, alternates pointing to `<scratch>/outside-store/objects`, and external common-dir. Base results respectively refused at `.git is a file`, `objects/info/alternates present`, and `.git/commondir is not a plain-init entry`; zero outside touches. This demonstrates that blanket shape rejection produces the same outcome for in-`d` and out-of-`d` target cases, rather than implementing the frozen boundary distinction.

Routed hostile examples corroborate the pairing: `plans/refusals46/f5_alternates.py` explicitly says its object store is “outside d”; `f7_commondir.py` builds its store “BESIDE d”; `f1_gitfile.py` puts its gitdir beside `d`; `f18_wtmeta_out.py` puts the linked-worktree checkout outside `d`. Those are correct refusal cases. The benign counterparts above differ only in target containment. Also, round-48's measured honest results already classify non-plain Git-produced states as over-refusals: `R48C1ExecCounter.md:109-116` records 8 honest BREACHes (detached HEAD, reflog/GC, user/remote config, stash, commit-graph, notes) with `touches=0`; thus plain-init shape is not the operative honesty test.

## Smallest safe correction

Do not equate metadata indirection with escape. In the repair and stage-2 honest population, include paired in-`d`/out-of-`d` cases for (1) `.git` gitfile/separate gitdir and linked-worktree metadata, (2) `objects/info/alternates`, and (3) `commondir`. Resolve each pointer according to Git's actual base directory, then admit only if every resolved store/checkout/config/object/ref path stays within `d`; retain the hostile counterparts so blanket admission fails. Do not admit merely because a path is lexically below `d` before resolving `..`, or because Git reports a worktree top-level inside `d` while its common store is external. The existing frozen kill rule remains unchanged.

## Commands, limits, provenance

Exact fixture commands are represented by the scratch scripts `ctl/build.sh`, `ctl/run.sh`, and `ctl/run2.sh`; driver invocation was `/usr/bin/strace -f -y -e trace=<open/stat/readlink/execve family> -o <scratch-log> python3 <scratch>/ctl/drive.py <d> anchor '["--lane","<absolute lane>"]'`, with cwd=`d`. Fixture Git mutations ran only in `/fast/scratch/hyaku/kengaku-r49/R49C1HoStore/fix/...`; scratch clone and fixtures were not committed. No tests/tools installed. No external source opened (no URL/quote applicable). Limitation: custom trace analyzer is an approximation and these are not the frozen v3 counter; output cannot satisfy stage-2 scoring. The initial h4 helper left a transient `MERGE_RR` from failed setup; it was removed before the final h4 run. A relative separate-gitdir attempt resolved outside `d` because the command's relative path used the shell cwd; it was discarded, not used as evidence.

Scratch was removed before yield: `rm -rf /fast/scratch/hyaku/kengaku-r49/R49C1HoStore`; verify with `test ! -e /fast/scratch/hyaku/kengaku-r49/R49C1HoStore`.

VERDICT: **calibration counterexample confirmed against the base fence** — benign, Git-functional in-`d` gitfile/worktree, alternates, and commondir cases are refused without outside touches, while the corresponding outside-target classes are expected refusals. Not a C1 score or admission decision.
