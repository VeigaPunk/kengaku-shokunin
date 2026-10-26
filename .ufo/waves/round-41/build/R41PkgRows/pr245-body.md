# TB2.1 PR #245 capture — harbor-framework/terminal-bench-2-1
# fetched 2026-10-26T18:38:28Z via gh api repos/harbor-framework/terminal-bench-2-1/pulls/245
# state=closed merged=false created_at=2026-10-05T02:41:13Z closed_at=2026-10-08T19:02:36Z author=camirian base=main base_sha=7131e4375048a0e408a8fb404b5f499d726b695b comments=0 review_comments=0

# Draft Terminal-Bench 2.1 contribution

**Status:** local draft only; do not submit without owner authorization.

**Recommended surface:** Pull request to `harbor-framework/terminal-bench-2-1`, changing only `tasks/constraints-scheduling`.

**Current upstream state checked 2026-10-04:** public `main` is `7131e4375048a0e408a8fb404b5f499d726b695b`, the same base as the local patch. The current grader still obtains the target VEVENT for the structure test, but the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar. GitHub tracker search returned no matching bug report; the two results for `constraints-scheduling` were unrelated leaderboard-submission PRs. The repository has active Issues and Pull Requests. [Tracker search](https://github.com/harbor-framework/terminal-bench-2-1/issues?q=is%3Aissue+constraints-scheduling) found no matching bug report; the two task-name matches were leaderboard-submission PRs. The README notice that community submissions are closed applies to benchmark leaderboard submissions, not code-fix PRs.

## Proposed title

Bind constraints-scheduling checks to the requested VEVENT

## Proposed PR description

The `constraints-scheduling` verifier can reward an invalid requested meeting when an unrelated VEVENT appears first in the output calendar. The structure check identifies `Team Planning Meeting` by its summary and attendees, but the constraint and earliest-slot checks read the first DTSTART from the full calendar. This lets the unrelated event provide the time evidence for a different target event.

A minimal reproduction uses the supplied task calendars and two output VEVENTs:

1. `Context Event`, Jan 17, 2024 11:00–12:00 UTC, with no required attendees.
2. `Team Planning Meeting`, Jan 17, 2024 09:00–10:00 UTC, with Alice, Bob, and Carol as attendees.

The requested meeting violates Bob's no-meetings-before-10:00 constraint. With the context event first, the current verifier passes all three checks. With the requested meeting first, the verifier fails. With the invalid target alone, it fails. A valid requested meeting at 11:00–12:00 passes in both versions.

The cause is inconsistent event binding: the structure test reads fields from the selected VEVENT, while later checks read the first DTSTART from the calendar. The proposed fix selects exactly one title-matching VEVENT and obtains DTSTART and DTEND from that event for every target-specific check. Conflict checks still compare that interval against every immutable input calendar. Multiple matching target events fail closed.

The patch adds 55 adversarial calendar fixtures, each of which runs all three native verifier checks. Cases cover event order, decoys, duplicate and ambiguous targets, field binding, scheduling constraints, supported iCalendar syntax, and malformed structures. The patch also adds the suite to the existing `tests/test.sh` invocation.

Local verification: `python3 -m pytest tasks/constraints-scheduling/tests/test_event_binding_adversarial.py -q` passes all 55 cases; Python compilation and `git diff --check` pass. I did not run `tests/test.sh` because it installs curl and uv from the network. The patch does not add dependencies.

The parser implements the task's UTC VEVENT subset. It accepts CRLF, folded lines, case-insensitive property names, attendee parameters, and explicit UTC value parameters. It does not claim full RFC 5545 validation; balanced non-target components are opaque. The duplicate-target policy is explicit because the task does not define how to resolve multiple requested meetings.

This report concerns one task's verifier behavior. It does not measure prevalence across Terminal-Bench, establish that an evaluated model exploited the issue, or support a conclusion about leaderboard validity.

## Patch contents

Local branch `local/continuous-loop-repair`, commit `ca2256b`:

- `tasks/constraints-scheduling/tests/test_outputs.py`
- `tasks/constraints-scheduling/tests/test_event_binding_adversarial.py`
- `tasks/constraints-scheduling/tests/test.sh`
- `tasks/constraints-scheduling/SPECIFICATION.md` (bounded task-contract note)

Expected maintainer effort: inspect a focused test-helper change, run one task test script, and decide whether the fail-closed multiple-target policy matches repository expectations. No library choice or runtime dependency is involved.

**External action required:** owner authorization to open this PR. No upstream issue, PR, or comment has been created.

