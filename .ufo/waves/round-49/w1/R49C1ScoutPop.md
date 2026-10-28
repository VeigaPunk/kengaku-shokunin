# R49C1ScoutPop — additional Git repository states survey

## Axes and scope

- **Calibration** (R49-C1 only): identify additional ordinary Git repository states the frozen honest population does not enumerate, and rank fence admission. This is source/evidence survey only; no claim of R49-C1 or R49-C2 admission.
- **Measured revision:** `9d2900af41e4d1fc6022eff99010436fde6dbd93` (stage-1 freeze). `git cat-file -t` returned `commit`; `git log -1 --format='%H %cI %s'` returned `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`. The clone was checked out at this exact commit before inspection. No scored counter/probe executed.

## Findings and ranked recommendations

Rank is for a fence advertised as admitting an ordinary in-tree `.git` store with no external reads, not for expanding the specific strict plain-init contract. “Admit” means classification is explicit and remains wholly internal; where Git permits an external redirect or executable behavior, continue refusing that configuration/path.

| Rank | Additional state absent from the described 120-fixture population | Host observation / Git docs | Recommendation |
|---|---|---|---|
| 1 | `refs/stash`, `logs/refs/stash`, stash commits (though R48 n14 already covers one stash) | R48 honest report explicitly says novel48 n14 is one stash push; stash docs say latest is stored at `refs/stash` and older entries in its reflog. Multiple stash entries / stash with untracked content are still additional shapes. | **Admit**, as validated refs/reflogs and in-tree objects. The namespace is ordinary local ref data, not a redirect. The frozen fence currently refuses `refs/stash` because `_refs` only accepts `heads`/`tags`; it also rejects the stash reflog. |
| 2 | `.git/info/refs`, `.git/objects/info/packs`, `.git/objects/info/commit-graph`, pack `.rev`/`.mtimes`, multi-pack-index | Locally observed after `git update-server-info` / `git gc` / repack / `git multi-pack-index write`; `gitrepository-layout` documents info/refs and objects/info/packs as dumb-transport indexes, and says commit-graph may be an ancillary index (git-gc docs). | **Admit**, after exact format/size/symlink checks: these are metadata/index files inside the store; they are not object-store redirects. Current code rejects nonempty `.git/info` except `exclude`, rejects nonempty `objects/info` except currently empty `info`, and has no `multi-pack-index` filename allowance. Preserve refusal of `objects/info/alternates` and `http-alternates`, which are redirects. |
| 3 | Refs under `refs/replace/` | `git replace` docs say it creates refs in `refs/replace/`; the layout docs identify replacement refs. Host `git replace` generated that ref path. Replacement refs affect object interpretation by default. | **Conditional admit**, only if caller semantics tolerate replacement objects and the store proves replacement targets/objects remain inside `d`; otherwise refuse intentionally and disclose this stricter scope. For the current “plain init + commits” advertised contract, this is not a plain-init state, so refusal is consistent. |
| 4 | Shallow-clone boundary `.git/shallow` | A local `git clone --depth 1 file://…` produced `.git/shallow`; layout docs say it is maintained by shallow-clone machinery. | **Refuse for this fence**: not produced by plain init + commits, changes ancestry interpretation, and cannot be validated by existing normal-ref rules without a format-specific parser. It is an honest clone state only under a broader contract. |
| 5 | SHA-256 init and reftable init (`[extensions] objectformat=sha256`, `[extensions] refstorage=reftable`, `.git/reftable/*`) | Host `git init --object-format=sha256` and `git init --ref-format=reftable` generated these. `git-init` docs list both options and both formats; layout format-version docs require extension-aware readers. | **Refuse under current fence; high-priority future compatibility class** if “ordinary git init on this host” is the intended contract. Current 40-hex validators, loose-object path rules, refs-file layout, and config allowlist cannot prove these formats. They are valid initialized repos, so a universal plain-init claim must either support them or narrow its stated accepted formats. |
| 6 | `info/grafts` | Created by explicit local graft-file write; docs call it fake ancestry and outdated/deprecated. | **Refuse**. Not created by plain init, deprecated, changes ancestry interpretation, and needs dedicated parsing. Prefer replace refs if history replacement is deliberately supported. |
| 7 | Fetch/submodule state: `FETCH_HEAD`, `refs/remotes/*`, `[remote]` / `[branch]` / `[submodule]` config, `.git/modules/*`, worktree `.git` gitfile and `.gitmodules` | Host fetch/submodule probe produced these. Layout docs state a `.git` gitfile points to the real repository; `modules` contains submodule repos; git-init docs describe `--separate-git-dir` as a gitfile. | **Mixed:** simple inert `[remote]` / `[branch]` data and `FETCH_HEAD` can be admitted only with strict syntax/value bounds and no follow-up network behavior. **Refuse** gitfiles, `.git/modules`, worktrees/commondir, and external URLs/paths for this fence: they redirect repo discovery or introduce additional repositories. `.gitmodules` is a worktree file, not a Git-store entry, but submodule initialization creates a gitfile and modules tree. |
| 8 | In-progress operation/bisect/rebase/merge state (`MERGE_HEAD`, `MERGE_MSG`, `AUTO_MERGE`, `BISECT_*`, `refs/bisect/*`, `refs/rewritten/*`) | Host-created by merge conflict/bisect/rebase attempts; layout docs distinguish `refs/bisect`, `refs/rewritten`, and other refs. | **Refuse by default** for a plain-init fence: these represent active operations or command-specific state, not ordinary init/commit state; parser semantics and supported Git versions vary. Could add discrete, format-pinned benign cases only if the desired contract expands. |
| 9 | `.git/rr-cache/` and empty `.git/MERGE_RR` when global `rerere.enabled=true` | Host Git 2.56.0 with global rerere enabled created both on a one-commit repo. Under the R48 builder’s environment (`GIT_CONFIG_GLOBAL=/dev/null`) this did not reproduce; global `git config --global --list` showed `rerere.enabled=true`. | **Admit only when classified as inert, bounded rerere state** if this host-global-config variation is in scope. Do not weaken an isolated counter based on this host-global probe: the fixture builder explicitly disables global config, and these files were absent there. This is configuration-dependent, not a state guaranteed by plain init. |
| 10 | `git describe` names | `git describe --tags` emitted a name based on reachable tags; it wrote no new `.git` state in the host probe. Existing n02/n08 population includes annotated tags. | No additional store-state admission needed. Keep tag/ref data already validated; `describe` is an inspection command, not persistent repository state. |
| 11 | `core.*` written by fresh `git init` on this host | `git version 2.56.0`; fresh `git init -b master` config was exactly `[core] repositoryformatversion = 0`, `filemode = true`, `bare = false`, `logallrefupdates = true`. Those keys are covered by the existing config allowlist. SHA-256/reftable add `[extensions]` and format version 1, not more core keys. | No missing default `core.*` key found on this host. Maintain allowlist for the observed four defaults; test other platforms separately before treating `ignorecase`, `precomposeunicode`, or `symlinks` values as host requirements. |

### Coverage distinctions

The frozen population is not simply “120 plain init fixtures.” The claims freeze describes 104 battery fixtures plus 16 novel honest classes. The R48 honest report’s novel classes already cover one stash entry, local user config, remote origin, commit-graph, notes, multibranch, empty repo, detached HEAD, packed refs, tags, merge commit, reflog-GC, and ignored untracked content. Therefore this survey treats stash as an uncovered *variant* (multiple entries / untracked stash), not a wholly absent class. Its n15 commit-graph case does not establish coverage for every `objects/info` index, pack extension, or multipack index format.

## Git-doc evidence

Access date for all URLs below: **2026-10-28**. Quotes are verbatim and each is at most 25 words.

- `https://git-scm.com/docs/gitrepository-layout` — “refs/replace/*<obj-sha1>* records the SHA-1 of the object that replaces *<obj-sha1>*.” (located section `refs/replace`).
- `https://git-scm.com/docs/gitrepository-layout` — “This file records fake commit ancestry information” (located section `info/grafts`).
- `https://git-scm.com/docs/gitrepository-layout` — “This is similar to info/grafts but is internally used and maintained by shallow clone mechanism.” (located section `shallow`).
- `https://git-scm.com/docs/gitrepository-layout` — “This file records paths to alternate object stores that this object store borrows objects from” (located section `objects/info/alternates`).
- `https://git-scm.com/docs/gitrepository-layout` — “This file helps dumb transports discover what refs are available in this repository.” (located section `info/refs`).
- `https://git-scm.com/docs/gitrepository-layout` — “Additional information about the object store is recorded in this directory.” (located section `objects/info`).
- `https://git-scm.com/docs/gitrepository-layout` — “A plain text file .git at the root of your working tree, containing gitdir: <path> to point at the real directory” (located repository-flavours note).
- `https://git-scm.com/docs/gitrepository-layout` — “Contains the git-repositories of the submodules.” (located section `modules`).
- `https://git-scm.com/docs/git-stash` — “The latest stash you created is stored in refs/stash; older stashes are found in the reflog of this reference” (located DESCRIPTION).
- `https://git-scm.com/docs/git-replace` — “Adds a replace reference in refs/replace/ namespace.” (located DESCRIPTION).
- `https://git-scm.com/docs/git-init` — “The valid values are: files for loose files with packed-refs. This is the default. reftable for the reftable format.” (located `--ref-format`).
- `https://git-scm.com/docs/git-init` — “The valid values are sha1 and (if enabled) sha256. sha1 is the default.” (located `--object-format`).
- `https://git-scm.com/docs/git-describe` — “The command finds the most recent tag that is reachable from a commit.” (located DESCRIPTION).
- `https://git-scm.com/docs/git-gc` — “May also update ancillary indexes such as the commit-graph.” (located DESCRIPTION).

## Commands and observed outputs

Commands were run from the unique scratch tree `/fast/scratch/hyaku/kengaku-r49/R49C1ScoutPop`; a shared clone was checked out at the frozen base. Git-state probes were created only in scratch directories. No counter, gated probe, or score run was made.

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
$ git --version
git version 2.56.0
$ cat fresh/.git/config
[core]
\trepositoryformatversion = 0
\tfilemode = true
\tbare = false
\tlogallrefupdates = true
$ git init --object-format=sha256 -q -b main r8; cat r8/.git/config
[extensions]
\tobjectformat = sha256
[core]
\trepositoryformatversion = 1
\tfilemode = true
\tbare = false
\tlogallrefupdates = true
$ git init --ref-format=reftable -q -b main r9; find r9/.git -mindepth 1 | grep reftable
r9/.git/reftable
r9/.git/reftable/0x000000000001-0x000000000001-fedde177.ref
r9/.git/reftable/tables.list
$ git clone --depth 1 file://… r4; test -f r4/.git/shallow && echo shallow
shallow
$ git -C rB fetch -q origin; cat rB/.git/FETCH_HEAD
786a11aeb135a47c4d8dca55c8b727e200ff5db4\tnot-for-merge\tbranch 'master' of file:///fast/scratch/hyaku/kengaku-r49/R49C1ScoutPop/probe/rB/../rBsrc
$ git -C rC worktree add ../rC-wt HEAD; cat rC/.git/worktrees/rC-wt/commondir
../..
$ git -C rE multi-pack-index write; find rE/.git -name 'multi-pack*'
rE/.git/objects/pack/multi-pack-index
$ git config --global --list | grep rerere
rerere.enabled=true
```

The isolated builder’s environment was observed directly in `plans/round44_c1_verify.py`: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, and four controlled `GIT_CONFIG_KEY_n` values. Thus my global `rerere.enabled=true` explains the local extra `MERGE_RR`/`rr-cache` output and is not evidence that the frozen builder population included those entries.

## Limits

- No tests or scored runs were performed; no claim predicate, fence-mutant, or C1/C2 admission was evaluated.
- Empirical probes cover Git 2.56.0 on this Linux host only. They are not a cross-version/platform survey.
- Git docs establish meanings and formats, not fence safety; proposed admits still require counter-backed format classification and hostile tests.
- `git describe` was observationally non-mutating in the tested fixture; that does not prove every wrapper/configuration is side-effect-free.
- Full integration/callsite/LSP tracing was not relevant: this is a Git-format survey, not an exported code contract.
- Scratch cleanup is verified below.

VERDICT: **Survey complete; recommendations only.** Additional states make clear that “plain init” must be version/platform/configuration bounded. Keep redirects and external stores refused; consider bounded, explicit admission for benign local metadata and indexes. No R49-C1/R49-C2 admission claim.
Cleanup after copying findings into this report:

```text
$ rm -rf /fast/scratch/hyaku/kengaku-r49/R49C1ScoutPop && if test ! -e /fast/scratch/hyaku/kengaku-r49/R49C1ScoutPop; then printf 'scratch_removed=yes\n'; else printf 'scratch_removed=no\n'; fi
scratch_removed=yes
```
