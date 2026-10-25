# Round 27 — ExecRevertHarness

- **Scope:** implemented the pre-registered separability check from `plans/round-27-claims.md:132-138` in the private clone only.
- **Clone:** `/tmp/kengaku-r27-ExecRevertHarness`, based at `11a7fc8c64dc5d634331be24ccf5936f84a11f03`; frozen base resolved as `b5719440e5eee46c1886fddbdf7bdc1624829454`.
- **File written in clone:** `plans/fixtures/r27/revert_test.sh` — SHA-256 `b2f5821e730a603973fe25599498f5e112d6a9500317ee2938cc5b2913234607`.
- **Behavior:** accepts `REPO C1_REV C2_REV [BASE_REV]`; creates disposable Git exports under `/tmp`, combines C1 claim paths from C1_REV and C2 paths plus new R27-E correction rows from C2_REV, then restores each claim's paths from BASE in the relevant export only. Re-runs both `--summary` counters; compares full stdout and exit status against the combined export. Exit 0 means both summaries/statuses are unchanged; exit 1 means a counter moved; exit 2 means invalid input or incomplete counter output. C2's permitted counter exits 0/1 follow `state_check.py`'s exit map.
- **Synthetic verification:** independent C1/C2 commits from the same dummy base in `/tmp/kengaku-r27-synthetic-ia9us_0f/repo`.
- Command: `/tmp/kengaku-r27-ExecRevertHarness/plans/fixtures/r27/revert_test.sh /tmp/kengaku-r27-synthetic-ia9us_0f/repo 10e5307040a5292c72c461e86f8fc1110fc290cf b08a92258fb88011f58bdc6f979f8dc7d0019c4a 3e833c359c0fb7b25f5bf4ade87f073d60ae9829` — exit **0**.
- Captured output:
  - `C2 baseline: assertions=5 match=5 mismatch=0 superseded=1 offline_unverifiable=0`
  - `C2 after C1 revert: assertions=5 match=5 mismatch=0 superseded=1 offline_unverifiable=0`
  - `C2 comparison=UNCHANGED`
  - `C1 baseline: TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=0 policies_with_flips=0`
  - `C1 after C2 revert: TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=0 policies_with_flips=0`
  - `C1 comparison=UNCHANGED`; `RESULT=UNCHANGED`; stderr empty.
- **Risks/blockers:** only the required synthetic pair was available for execution; the round-27 C1/C2 revisions and real counter outputs were not present in the pinned clone. No live lane files, Git index, or jj state were written.
- **Installs:** none.

VERDICT: Implemented and synthetic independence case passed; real-round execution awaits integrated C1/C2 revisions.