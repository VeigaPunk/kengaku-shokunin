# R49C1HonestInv — honest-population inventory (C1)

**Axis:** calibration. **VERDICT:** base fence over-refuses honest fixtures; 8/120 on the frozen r48 denominator, and 11/124 in the current r49 honest-population preview. This is a diagnostic/control result only: no R49-C1 admission claimed.

## Freeze and scope

The required stage-1 freeze exists in the committed lane tree: `9d2900af41e4d1fc6022eff99010436fde6dbd93`, committed `2026-10-28T09:14:40-03:00`, before measurement. It is an ancestor of lane HEAD `af88aab193e6034cb9b386472064e3c18fa90128` (`2026-10-28T09:18:20-03:00`). I cloned the lane at the freeze into `/fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane`; the clone top-level check returned that exact directory. No stage-2 counter/population freeze exists in the committed tree. Therefore the v2 counter run below is a re-measurement of the base-fence control, not scoring of claimed work.

## Population and fixture semantics

Independently rebuilt the carried population from the frozen tree and the r49 honest-seat modules. Builder receipt: `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `POPULATION population.txt sha256=ddf74c56c0165ef541772feab61991fcf77c8442f4db3859b2269bd1d8adbee0 fixtures=124`; `COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 novel49=4`; `CHECKS all-ok`; `PREDICATE POPULATION ok`. All 124 builds were deterministic; repository audits reported no symlink, special file, or hardlink, all discovered gitdirs inside each fixture, and `fsck_rc=0`, top-level checks true. The 16 carried r46/r48 modules were byte-identical to the r48 `modules.sha256` manifest. The reconstructed 120 carried fixture identity digests matched the frozen r48 `population.txt` row-by-row (normalized to tree digest, fid, and tool; the source-path column necessarily differs in the r49 candidate layout).

The v2 base-fence counter independently exercised the 104 pinned battery fixtures plus the 16 frozen r48 novel fixtures, preserving the 120 denominator. Verbatim result:

```text
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
TREE dirty=2
PINS total=82 mismatched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0
HONEST-POP battery=104 novel=16 expected_novel=16 novel_modules=16
BENIGN total=112
CALIBRATION advertised=32 contradicted=0
REASON tree-dirty=2,honest-not-admitted
PREDICATE R48-C1 fail
```

Thus 0/104 battery fixtures and 8/16 r48 novel fixtures were refused; no outside-root touches were recorded in the counter's FENCE-RUN lines for these eight. Refused honest fixtures and reasons (verbatim):

```text
n14-stash-entry — BREACH refs/stash has a name git does not write
n12-local-config-user — BREACH repo/.git/config section [user] is not allowlisted
n16-notes-ref — BREACH refs/notes has a name git does not write
n03-detached-head — BREACH repo/.git/HEAD is not a plain branch HEAD
n15-commit-graph — BREACH repo/.git/objects/info/commit-graph present (object-store redirect)
n07-reflog-gc — BREACH repo/.git/info/refs is not git's exclude file
n08-tag-detached — BREACH repo/.git/HEAD is not a plain branch HEAD
n13-remote-origin — BREACH repo/.git/config section header b'[remote "origin"]' is not plain
```

Each corresponding fixture builder uses ordinary local git operations only: `git stash push`, `git config --local user.*`, `git notes add`, checkout to an existing commit, `git commit-graph write --reachable`, `git reflog expire`/`git gc`, and `git remote add origin` without fetching. Their claimed bytes are inside the fixture; their refusal reasons are allowlist limits, not external access. The other eight novel48 fixtures were admitted. The 104 battery's own `expect=accept|reject` classifies the fixture contents/tool result, not whether the fence should admit the fixture; all 104 are structurally contained and admitted by the fence.

The four new classes currently delivered in the r49 wave directory were independently built and checked against the base fence. Their builders describe ordinary, in-bound states: `n17` local `refs/replace`; `n18` shallow fetch from sibling `../src` inside `d`; `n19` template-less `git init`; `n20` internal linked worktree with relative gitdir metadata. All were deterministic, `fsck_rc=0`, with gitdirs inside `d`, and strace showed zero outside-`d` touches. Results:

```text
n17-replace-ref BREACH repo/.git/refs/replace is not refs/heads or refs/tags
n18-shallow-fetch BREACH repo/.git/FETCH_HEAD is not a plain-init entry
n19-template-less-init ADMIT
n20-linked-worktree BREACH wt/.git is a file (gitdir redirect), not a directory
```

The preview population therefore has 11 refusals / 124 fixtures (8 carried refusals + n17, n18, n20), while the frozen denominator remains 120 for the before measurement; I do not remove refused rows or substitute a reduced denominator.

## Exact commands run

Commands below were run from the per-seat scratch directory unless absolute paths are shown. The quoted outputs above came from these commands.

```sh
git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git show -s --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane
git -C /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
git rev-parse --show-toplevel
sha256sum plans/fixture_fence.py plans/round44_c1_verify.py plans/round46_c1_verify.py .ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py
python3 /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/honest49snap/build_honest_population.py --lane /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane --modules /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/honest49snap/modules --out /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/honest49-out --work /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv --assert-base --jobs 8
bash /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane/.ufo/waves/round-46/claims/envelope.sh /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/env/base-fence python3 plans/round48_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/w/base-fence --jobs 8
python3 /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/breach_driver.py /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/honest49snap/modules/novel49/*.py
python3 /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/trace_one.py /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/lane /fast/scratch/hyaku/kengaku-r49/R49C1HonestInv/honest49snap/modules/novel49/n17_replace_ref.py
# trace_one.py was likewise run for n18_shallow_fetch.py, n19_template_less_init.py, n20_linked_worktree.py
```

R48 v2 counter digest was `8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f`, matching its r48 control report; frozen base digests also matched the builder's pinned fence, k44 builder, and r46 counter. The counter exited 1 as expected for this base-fence control, and the envelope reported unchanged PATH-dir content. The population builder exited 0.

## Limits and provenance

The 124-row expansion is a stage-2 preview from the wave-1 honest seat, not a committed/pinned stage-2 population; its denominator and module pins are not yet frozen. The counter measures the base fence against the carried 120 frozen rows only; the four new classes were directly evaluated against the same base fence, not run through a stage-2 v3 counter. Direct class strace checked the r49 classes; carried-class outside-touch counts come from the v2 counter receipt. This does not establish universal filesystem safety or any repaired-fence behavior. No external sources were opened (no URL/access-date/quote applies). No tools installed or upgraded.
