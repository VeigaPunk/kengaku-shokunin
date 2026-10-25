# R35MutLedgerD1D2 — attack `plans/defect_ledger.py` checks `r34_d1` / `r34_d2` (C2 calibration, wave 1)

Seat: executor (leaf). Scope: only the two D1/D2 checks, in a disposable fixture clone in `/tmp`
(never the live lane; live lane untouched — HEAD remained `11d64530179b78e33ba6074fc77d63d36ee7ac31`,
no command wrote to the lane). No tools installed (used existing `git`/`python3`); no labrat spawned.

## Axis framing (godspeed)

- Axis 1 — D1 working-tree observable: does `r34_d1` catch untracked round-34 wave/plan paths, and
  does its `--exclude-standard` correctly skip ignored files?
- Axis 2 — D2 tip observable: does `r34_d2` read the committed branch tip (ls-tree), not the
  working tree?
- Both improve on every cheap mutation; no hazards (all mutations confined to the clone).

## Fixture baseline (clone, sparse, at master = freeze commit)

```
D=$(mktemp -d /tmp/k35-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus/ /plans/ /SCORECARD.md \
  /.ufo/waves/round-34/assimilation/ /.ufo/waves/round-34/build/*.md
git -C "$D/lane" checkout -q master
```
`toplevel=/tmp/k35-sPtH/lane` (verified `== $D/lane` before any write), `HEAD=11d64530179b78e33ba6074fc77d63d36ee7ac31`
(the freeze commit).

Baseline run (`python3 plans/defect_ledger.py --lane "$D/lane"`):
```
R34-D1 status=open observed=pass agree=NO untracked=0
R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
rows=5 closed=0 observed_pass=1 mismatches=1
PREDICATE C2 fail
EXIT=1
```
Baseline clone: D1 green (no untracked), D2 red (109413 committed mirror paths at `refs/heads/master`).

## Mutants

### A1 — untracked file under `./ufo/waves/round-34/` → D1 must FAIL (caught)
```
echo "mutant-A1" > "$L/.ufo/waves/round-34/UNTRAKCED_MUTANT.txt"
git -C "$L" status --porcelain | grep UNTRAKCED
?? .ufo/waves/round-34/UNTRAKCED_MUTANT.txt
R34-D1 status=open observed=fail agree=yes untracked=1
```
D1 flipped green→red with `untracked=1`. Removed after capture.

### C1 — ignored `__pycache__` file under the wave → D1 must stay green (documented, no flip)
```
mkdir -p "$L/.ufo/waves/round-34/__pycache__"; echo pyc > "$L/.ufo/waves/round-34/__pycache__/mutant.pyc"
git -C "$L" check-ignore -v .ufo/waves/round-34/__pycache__/mutant.pyc
.gitignore:2:__pycache__/	.ufo/waves/round-34/__pycache__/mutant.pyc
git -C "$L" status --porcelain | grep pycache   # (empty — not shown as untracked)
R34-D1 status=open observed=pass agree=NO untracked=0
```
`__pycache__/` (lane `.gitignore:2`) matches → file invisible to `ls-files --others --exclude-standard`;
D1 unchanged. Note: a *non-ignored* untracked file is exactly A1; `--exclude-standard` is what keeps
ignored files inert. Removed after capture.

### A2 — untracked `plans/round34_mutate.py` (spot-check D1 path) → D1 must FAIL (caught)
```
echo mutant-A2 > "$L/plans/round34_mutate.py"
git -C "$L" status --porcelain | grep round34_mutate
?? plans/round34_mutate.py
R34-D1 status=open observed=fail agree=yes untracked=1
```
D1 flipped green→red. Removed after capture.

### B1 — delete all mirror files on disk WITHOUT committing → D2 must stay RED (documented: reads tip)
Sparse checkout extended to materialize the three mirror roots:
```
git -C "$L" sparse-checkout set --no-cone /corpus/ /plans/ /SCORECARD.md \
  /.ufo/waves/round-34/assimilation/ /.ufo/waves/round-34/build/*.md \
  /.ufo/waves/round-34/mut-entries-scratch/ \
  /.ufo/waves/round-34/build/R34MutRegistry/mirror/ \
  /.ufo/waves/round-34/build/R34MutRegistry/mut/
scratch=106323   mirror=515   mut=2575     # files materialized; worktree clean
rm -rf "$L/.ufo/waves/round-34/mut-entries-scratch" \
       "$L/.ufo/waves/round-34/build/R34MutRegistry/mirror" \
       "$L/.ufo/waves/round-34/build/R34MutRegistry/mut"
git -C "$L" status --porcelain | awk '{print $1}' | sort | uniq -c
109413 D
R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
```
All 109413 mirror files deleted from the working tree; D2 still red with identical
`committed_mirror_paths=109413` — confirmed the check reads the committed branch tip
(`git ls-tree -r --name-only refs/heads/master …`), not the working tree.
(D1 also stayed green: deleting tracked files creates no untracked entries.)

### B2 — fixture commit (identity `fixture <fixture@invalid>`) removing the mirrors → D2 must go GREEN (caught)
```
git -C "$L" config user.name fixture
git -C "$L" config user.email fixture@invalid
git -C "$L" add -A
git -C "$L" commit -q -m "fixture: remove round-34 mirror scratch (D2 mutation)"
git -C "$L" rev-parse HEAD
c1918329aa05cd6a63101937676f0374f3c98977
R34-D2 status=open observed=pass agree=NO committed_mirror_paths=0
git -C "$L" ls-tree -r --name-only HEAD -- .ufo/waves/round-34/mut-entries-scratch \
  .ufo/waves/round-34/build/R34MutRegistry/mirror .ufo/waves/round-34/build/R34MutRegistry/mut | wc -l
0
```
D2 flipped red→green only once the removal was committed; the worktree-only delete (B1) never
moved it. Commit happened only in the fixture clone (`git -C "$D/lane"`); lane refs untouched.

## Result tally

| Mutation | Check | Expected | Observed | Outcome |
|---|---|---|---|---|
| A1 untracked file under `.ufo/waves/round-34/` | D1 | fail | `untracked=1` fail | caught |
| A2 untracked `plans/round34_mutate.py` | D1 | fail | `untracked=1` fail | caught |
| B2 fixture commit removing mirrors | D2 | pass | `committed_mirror_paths=0` pass | caught |
| C1 ignored `__pycache__` (control, no flip) | D1 | stay green | `untracked=0` green | documented |
| B1 worktree-only delete (control, no flip) | D2 | stay red | `committed_mirror_paths=109413` red | documented |

Flip-mutants: 3/3 caught. Both no-flip controls behave as specified: `--exclude-standard` excludes
ignored files (C1), and D2 is branch-tip-committed, not working-tree (B1).

Cleanup: `rm -rf /tmp/k35-sPtH` (and the temp var file) per fixture rule.

## Risks / notes

- The `--shared` clone shares the object store; the B2 fixture commit's objects (tree/blob edits of
  109413 deletions) were written to the shared object database, but no ref or index in the lane was
  touched and no commit was pushed; the clone was deleted. Lane HEAD/status unchanged.
- Not in scope: D3/D4/D5 checks (they remain red in the clone at the freeze tip; the live lane has
  uncommitted repairs, e.g. ` M .ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS`, which
  are the L1's integration surface, not this seat's).

VERDICT: d1d2-mutants-3/3
