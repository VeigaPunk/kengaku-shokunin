# R2 report-order falsification

## Evidence

- Frozen claim `plans/round-32-claims.md:65-66` defines R2 as the round-32 report existing after the last lane commit and citing the final lane tip. The repair discipline is explicit at `:77-80`: R2 is repaired by landing this round's report after lane commits.
- The build draft `.ufo/waves/round-32/build/R32DraftReport.md:17-19` has a `**Landed round work `<LANE-TIP>`**` line and says the report commit lands after the last lane commit and cites `<LANE-TIP>`. Lines 68-73 assign `<LANE-TIP>` to lane-work commits and `<REPORT-COMMIT>` to the report itself. So the skeleton carries the required slot, not an actual landed hash yet.
- Counter implementation `plans/round32_defects.py:86-98`: R2 fails if the report path does not exist; then it obtains tip using `git -C <lane> rev-parse master`; then requires that exact hash string to occur in report bytes.
- Read-only current tip command returned `6084cd3492c6aef10fd66afc36ffc00e79ace94a` (`master`). This is the freeze-receipt commit, not evidence of the eventual final lane tip.
- The fleet report path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-32/kengaku.md` does not exist at inspection (`test -f` exit 1). Therefore simulating R2 now yields failure on report absence; moreover, the draft placeholder `<LANE-TIP>` does not contain current tip `6084cd3492c6aef10fd66afc36ffc00e79ace94a`.

## Required sequence to make R2 green

Finish and commit every lane change first, including final lane evidence/lesson/report references; record the resulting `master` tip. Only then materialize the fleet report with that exact full tip in its `Landed lane tip` line and commit the report separately, after the lane commit. Do not add or amend lane commits afterward: that would move `master` and invalidate the cited tip. Run the R2 check against the landed report and final lane state.

The draft's current placeholder is a valid skeleton slot but not a passing report. Current R2 status: report missing and exact tip absent from the skeleton.

VERDICT: defect
