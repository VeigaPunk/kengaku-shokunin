# R49C1HoPaths — benign repository layout dispositions

Axes: **calibration** (R49-C1). Scope: disposition of benign repository nesting and symlinked worktree layouts only. No candidate fence, admission, or C1/C2 verdict is claimed.

## Freeze and measured tree

The required stage-1 freeze existed in the committed lane tree before measurement. Its commit is `9d2900af41e4d1fc6022eff99010436fde6dbd93` (2026-10-28 09:14:40 -0300), parent `3a548330c4899c6c5df34168a44a59f66828ce74`; it contains `plans/round-49-claims.md` (167 lines), `plans/fixture_fence.py`, and `plans/round46_c1_verify.py`. The measurement clone's `HEAD` and top-level were respectively that exact freeze revision and `/fast/scratch/hyaku/kengaku-r49/R49C1HoPaths/lane`. The measured fence is the base fence at that commit, SHA-256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`. The imported counter was `plans/round46_c1_verify.py`, SHA-256 `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`; its pinned round-44 builder digest matched. This was a **disposition-only probe**, not a full/frozen counter score.

## Commands and observed outputs

Setup and freeze checks:

- `mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C1HoPaths && cd /fast/scratch/hyaku/kengaku-r49/R49C1HoPaths && export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1HoPaths && git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin lane && git -C lane checkout --quiet 9d2900af41e4d1fc6022eff99010436fde6dbd93 && git -C lane rev-parse HEAD && git -C lane rev-parse --show-toplevel` →
  ```
  9d2900af41e4d1fc6022eff99010436fde6dbd93
  /fast/scratch/hyaku/kengaku-r49/R49C1HoPaths/lane
  ```
- `git -C lane show 9d2900af41e4d1fc6022eff99010436fde6dbd93:plans/round-49-claims.md | wc -l && git -C lane ls-tree -r 9d2900af41e4d1fc6022eff99010436fde6dbd93 --name-only | grep -E '^plans/(fixture_fence.py|round46_c1_verify.py|round-49-claims.md)$' && git -C lane show -s --format='%H%n%P%n%ci%n%s' 9d2900af41e4d1fc6022eff99010436fde6dbd93 && git -C lane status --porcelain` →
  ```
  167
  plans/fixture_fence.py
  plans/round-49-claims.md
  plans/round46_c1_verify.py
  9d2900af41e4d1fc6022eff99010436fde6dbd93
  3a548330c4899c6c5df34168a44a59f66828ce74
  2026-10-28 09:14:40 -0300
  round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
  ```
  `git status --porcelain` emitted no lines.
- Tool availability/version command: `command -v bwrap strace git python3; strace --version | head -1; bwrap --version; git --version; python3 --version` → `/usr/bin/bwrap`, `/usr/bin/strace`, `/usr/bin/git`, `/usr/bin/python3`; `strace -- version 7.2`, `bubblewrap 0.13.1`, `git version 2.56.0`, `Python 3.14.8`.
- `python3 build_test.py` built all 15 scratch-only fixtures successfully (`BUILT <fid> argv=...` for each); no build errors.

Disposition command: `python3 measure.py`. It rechecked the clone revision/top-level, checked the imported builder's pinned digest, used the base fence and the round-46 counter's existing `build_module`/`run_fence` sandbox and trace machinery, and emitted the following verbatim rows:

```text
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
COUNTER sha256=ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508 PINS-k44=match
FENCE sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
DISPOSITION fid=nested-outer verdict=ADMIT touches=0 calls=569 reason='ADMIT'
DISPOSITION fid=nested-inner verdict=ADMIT touches=0 calls=569 reason='ADMIT'
DISPOSITION fid=nested-siblings verdict=ADMIT touches=0 calls=558 reason='ADMIT'
DISPOSITION fid=nested-three-level verdict=ADMIT touches=0 calls=641 reason='ADMIT'
DISPOSITION fid=symlink-relative-tracked verdict=BREACH touches=0 calls=436 reason='BREACH repo/link.txt is a symlink'
DISPOSITION fid=symlink-absolute-tracked-in-d verdict=BREACH touches=0 calls=436 reason='BREACH repo/link.txt is a symlink'
DISPOSITION fid=symlink-directory-tracked verdict=BREACH touches=0 calls=433 reason='BREACH repo/shortcut is a symlink'
DISPOSITION fid=symlink-broken-tracked verdict=BREACH touches=0 calls=434 reason='BREACH repo/dangling is a symlink'
DISPOSITION fid=symlink-untracked verdict=BREACH touches=0 calls=436 reason='BREACH repo/new-link is a symlink'
DISPOSITION fid=symlink-to-nested-repo verdict=BREACH touches=0 calls=438 reason='BREACH repo/alias is a symlink'
DISPOSITION fid=fixture-root-is-repo verdict=ADMIT touches=0 calls=488 reason='ADMIT'
DISPOSITION fid=plain-worktree-layout verdict=BREACH touches=0 calls=432 reason='BREACH linked/.git is a file (gitdir redirect), not a directory'
DISPOSITION fid=separate-git-dir-contained verdict=BREACH touches=0 calls=527 reason='BREACH worktree/.git is a file (gitdir redirect), not a directory'
DISPOSITION fid=nested-separate-git-dir-contained verdict=BREACH touches=0 calls=441 reason='BREACH outer/vendor/sub/.git is a file (gitdir redirect), not a directory'
DISPOSITION fid=many-contained-repositories verdict=BREACH touches=0 calls=686 reason='BREACH fixture holds more than 64 repos'
SUMMARY ADMIT=5 BREACH=10 ERROR=0 HUNG=0 fixtures=15
```

## Counterexample and judgment

The strongest benign counterexample is a committed symlink in `repo/link.txt` pointing to `repo/target.txt`, with both link and target inside `d`: the base fence returns `BREACH repo/link.txt is a symlink`, with zero outside touches. The same blanket refusal applies to an absolute symlink whose target is inside `d`, directory and dangling tracked links, an untracked worktree symlink, and a link to another in-`d` nested repo. Separately, ordinary nested repositories (outer/inner, siblings, three levels) and a repo rooted at `d` are admitted with zero touches. Native linked-worktree and `--separate-git-dir` layouts whose metadata/store remain within `d` are refused at the `.git` redirect file; the probe confirms the lexical refusal but does not independently prove the behavior of every possible redirect target.

This is evidence of calibration-relevant over-refusal for ordinary nested layouts with contained worktree symlinks and Git's in-tree redirected worktree metadata. It does **not** justify allowing symlinks or redirect files indiscriminately: external targets remain a boundary risk. Smallest safe correction to consider: preserve refusal for targets that cannot be proven inside `d`, but distinguish contained worktree symlinks and in-`d` `.git` redirect targets, validating the target store rather than rejecting solely on entry type. The >64-repository refusal is an explicit cap/pathological-layout tradeoff and is not counted here as a demonstrated calibration defect.

## Sources and limits

Access date: 2026-10-28. Only local sources were opened; no external URL/source was used. URLs below are local file URLs, with located quotes (each ≤25 words):

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` — “an honest fixture whose store sits on a mount boundary inside `d` is admitted iff every byte the decision reads is inside `d`.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` — “Any future C1 admission attempt needs the mutation floor committed with receipts.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48.md` — “The candidate's ≥12-mutant kill battery was never reported”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` — “one walk of `d` proves the tree has no symlink and no special file anywhere”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` — “a fence that refuses everything, or anything with a git repo, fails here.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py` — “`build(ctx, d)` fills the EMPTY directory `d` and returns the tool argv tail as a list of str.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/modules/novel48/n10_empty_repo.py` — “a fence that refuses it refuses the state a fixture starts in before its first commit.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1HonestInv.md` — “No score/counter/probe was run in this review.”

Limits: these are scratch-authored layout probes, not a frozen population or C1 counter run; no repairs were tested. All observed `BREACH` verdicts in this set had `touches=0`. No external symlink-target fixture was scored, so this report makes no claim about how a corrected boundary policy should treat one. The measured tracked tree was clean at the freeze revision; Python created only ignored `plans/__pycache__` in the scratch clone. Tooling: no tools installed or upgraded.

VERDICT: The base fence admits the ordinary nested repository layouts tested, but over-refuses contained symlinked worktree files and contained Git redirect layouts. Calibration concern evidenced; disposition only; no R49-C1/R49-C2 admission claim.
