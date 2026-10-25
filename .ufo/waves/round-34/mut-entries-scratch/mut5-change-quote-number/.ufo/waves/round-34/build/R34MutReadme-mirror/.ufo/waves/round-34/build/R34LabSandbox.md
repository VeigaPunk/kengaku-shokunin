# R34LabSandbox — bounded probe: sandbox mirror fidelity

Seat: lab-sandbox (leaf). Wave: round-34 build (hyaku run 7). Date: 2026-10-25.

## Hypothesis
`git archive` export of the lane tip reproduces identical counter outcomes on the clean
tree (the harness's clean-mirror requirement is sound).

## Method
1. Archive HEAD (`adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`) of lane
   `/home/vgpnk/Projects/shokunin/kengaku-shokunin` to `$(mktemp -d)`.
2. Run `python3 plans/round33_defects.py --lane .` on the tip (cwd = lane) and
   `python3 <lane>/plans/round33_defects.py --lane $SB` on the sandbox; diff outputs/exit codes.
3. Cross-check with a real `git clone` mirror (same HEAD).
4. Absence probe for the round-34 tools (`plans/round34_c1_verify.py`,
   `plans/round34_defects.py`, `plans/round34_mutate.py`) on the worktree, on HEAD
   (`git cat-file -e`), and in the archive sandbox.
5. Locate path-dependence in `plans/round33_defects.py` (N3/N4 target resolution).

No tool installations were performed (probe uses stock git/tar/python3/find/diff); nothing
to record under the tooling directive.

## Results

### 1. Archive mirror breaks N1 — counter outcomes do NOT match
Archive export: 8789 files, exactly matching the HEAD tree count (`git ls-tree -r
--name-only HEAD | wc -l` = 8789).

Tip run (cwd = lane, `--lane .`):
```
TIP_EXIT=0
checks=6 defects=0
```

Sandbox run (`--lane /tmp/lab-sandbox.InxWGi`):
```
SB_EXIT=1
DEFECT N1 round32-wave-tree-committed: git ls-files failed: fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
checks=6 defects=1
```

`diff` of the two transcripts: `1c1,3` — not identical. **The hypothesis is falsified
for archive mirrors.** Root cause: N1 (`check_n1`, plans/round33_defects.py:68-88) runs
`git -C $LANE ls-files -- .ufo/waves/round-32/`; a `git archive` export is not a git repo
(no `.git`), so the porcelain call fails and the sandbox trip red on the *clean* tree.

### 2. Clone mirror holds
Real `git clone -q` of the same HEAD (adaf25d) reproduces byte-identical output:
```
CLONE_EXIT=0
OUTPUTS_IDENTICAL (tip vs clone)
checks=6 defects=0
```
So the clean-mirror requirement is sound only when the mirror preserves git metadata; a
plain archive export is not a valid mirror for git-dependent checks.

### 3. Path-dependence: N3/N4 are FLEET-absolute (partially fleet-dependent)
`plans/round33_defects.py:40-42`:
```
FLEET = Path("/home/vgpnk/Projects/shokunin")
R31_REPORT = FLEET / ".ufo/reports/round-31/kengaku.md"
R32_REPORT = FLEET / ".ufo/reports/round-32/kengaku.md"
```
N3/N4 default to these paths regardless of `--lane` (check_n3/check_n4 signatures,
lines 100-120). Evidence: on the archive sandbox (which contains no `.ufo/reports/` at
the fleet root), N3/N4 passed — they never read sandbox content; they resolve against the
real fleet repo. Both fleet reports exist (ls: round-31/kengaku.md 21552 B, round-32/
kengaku.md 6702 B), so outcomes are deterministic and equal across tip/sandbox/clone —
but `--lane` semantics are partially fleet-dependent: N1/N2/N5/N6 are pure functions of
the lane tree; N3/N4 are functions of fleet state.

### 4. Absence probes match the frozen do-nothing controls
Worktree (`python3` open failure, exit 2 each):
```
c1_run_exit=2    # plans/round34_c1_verify.py
defects_run_exit=2  # plans/round34_defects.py
mutate_run_exit=2   # plans/round34_mutate.py
```
HEAD (`git cat-file -e` fails, exit 128 each):
```
catfile_c1_exit=128
catfile_defects_exit=128
catfile_mutate_exit=128
```
Archive sandbox file probe: `ABSENT plans/round34_c1_verify.py`,
`ABSENT plans/round34_defects.py`, `ABSENT plans/round34_mutate.py`,
`PRESENT plans/round33_defects.py`. This matches the frozen C1/C2 controls
(round-34-claims.md §C1 control, §C2 do-nothing control: `cat-file -e` fails, exit 128).

## Findings
- Archive-mirror fidelity **breaks** for N1 (git-dependent check): exit 1 + `DEFECT N1`
  on the clean tree vs tip `checks=6 defects=0` exit 0.
- Clone-mirror fidelity **holds** (byte-identical, exit 0).
- N3/N4 are FLEET-absolute → `--lane` semantics partially fleet-dependent; not sandbox-visible.
- Round-34 counter/tool absence is confirmed on all three surfaces, consistent with the
  freeze-phase do-nothing controls.
- Advisory (for L1/harness, not built here): a clean-mirror harness must either (a)
  mirror with git metadata (clone, or archive + `git init` + commit + tracked registration),
  or (b) make git-dependent checks (N1-class) tolerate a non-repo lane; a bare `git archive`
  tree is not a faithful counter substrate.

VERDICT: lab-sandbox (fidelity breaks for git-archive mirrors — N1 needs git metadata, so
the archive clean tree trips `DEFECT N1` exit 1 vs tip `checks=6 defects=0` exit 0; clone
mirror reproduces identically; N3/N4 are FLEET-absolute/fleet-dependent; absence probes for
round34 tools match freeze controls).
