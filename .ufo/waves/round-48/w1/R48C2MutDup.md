# R48C2MutDup — frozen-case count-drift mutation

Axes: **coverage** (R48-C2). Mutation target: duplicate or remove one frozen case; test whether the frozen counter inventory detects count drift.

## Evidence opened
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — accessed 2026-10-27. Located quote, §C2: “`plans/round48_c2_verify.py` (written in wave 1, pinned at stage 2)” (line 92).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — accessed 2026-10-27. Located quote, §Claim re-checks: “V7 lacks violating cases for `both-print` and `toolchain`” (line 21; source text line truncated in reader display, quote fragment appears in other committed wave evidence). This records the relevant prior count/inventory defect context.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1-spec.json` — accessed 2026-10-27. Located quote, R48C2MutDup item: “duplicate or remove one frozen case; test whether the counter inventory catches count drift.”
- `file:///home/vgpnk/.omp/agent/RULES.md` — accessed 2026-10-27. Located quote: “Record every install or update — tool, version, channel, reason — in your report or handoff.” No tools were installed or updated.

## Commands and observed output
Commands run:
1. `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2MutDup` and `export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C2MutDup`.
2. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`.
3. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show --no-patch --format='%H %s' a543d92083557dd9b33ee674e9b99b03411f80af` → `a543d92083557dd9b33ee674e9b99b03411f80af round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`.
4. `git -C ... show a543d920...:plans/round-48-claims.md | wc -c` → `12587`.
5. Scratch-only shared clone and checkout: `git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r48/R48C2MutDup/lane`; asserted `git -C "$D/lane" rev-parse --show-toplevel` exactly equaled `$D/lane`; then detached checkout at `a543d92083557dd9b33ee674e9b99b03411f80af`.
6. Observed in scratch clone:
```
TOP=/fast/scratch/hyaku/kengaku-r48/R48C2MutDup/lane
REV=a543d92083557dd9b33ee674e9b99b03411f80af
FREEZE_BLOB=3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5
C2_COUNTER=fatal: path 'plans/round48_c2_verify.py' does not exist in 'a543d92083557dd9b33ee674e9b99b03411f80af'
CASE_TABLE=
TREE_STATUS=
```
The stage-1 claims blob is therefore present at the frozen revision; the C2 stage-2 counter is absent there. The frozen case table exists at that revision (empty output from `cat-file -e` indicates the existence check succeeded). The stage-1 contract explicitly places the counter pins, frozen populations/cases and before-control receipts at stage 2 before scored work; the count-drift detector is not present in the committed base.

## Mutation result / boundary
No case was duplicated or removed and no counter/probe/dry/stage-check execution was run. The required detector for this item is the stage-2-frozen `python3 plans/round48_c2_verify.py --lane .`; it does not exist in the committed stage-1 tree, and the case population/table is to be amended/frozen at stage 2. Running an improvised or absent detector would not test the frozen inventory and would violate the requirement that the measurement follow the freeze. This is a **blocked/inconclusive mutation**, not a survived or killed mutant.

REV measured for presence check: `a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze). No scored measurement exists. Scratch clone was removed by the registered cleanup trap before report writing.

Limits: no conclusion about whether the eventual stage-2 counter detects duplication/removal/count drift. The current lane checkout is `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`, not the task's frozen base; all fixture-tree inspection was done only in the scratch clone at the specified base. No admission claim is made.
Scratch cleanup follow-up: the first post-command existence check found the scratch root still present (with `lane/`); removed it explicitly with `rm -rf /fast/scratch/hyaku/kengaku-r48/R48C2MutDup`, then confirmed `SCRATCH_REMOVED=yes`.
VERDICT: INCONCLUSIVE — stage-2 counter/freeze prerequisite absent; no mutation run authorized.
