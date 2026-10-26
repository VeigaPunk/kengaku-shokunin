# Excerpts (copied 2026-10-26 16:2x -03; sources fetched in the same session)

## JonathanGabor/terminal-bench-2-audit — audit_results/20260120_125158/audit.txt (lines 649-671)

### Test 3: `test_earliest_tiebreakers_and_carol_buffer`
This test validates:
- **Earliest slot at minute granularity**: Exhaustively checks every minute from Jan 15 9:00 AM to scheduled time to ensure no earlier valid slot exists
- **Monday avoidance tie-breaker**: If same-time candidates exist on both Monday and other weekdays, Monday should be avoided
- **Morning preference assertion**: Directly checks that scheduled hour is 9-11 (assumes dataset has valid morning slot)
- **Carol's 15-min buffer**: Checks both directions for late-ending meetings

### Strengths
1. **Exhaustive earliest-slot verification** - minute-by-minute checking is very rigorous
2. **Input integrity protection** - hash verification prevents cheating by modifying inputs
3. **Complete constraint coverage** - all hard constraints are explicitly tested
4. **Tie-breaker validation** - Monday avoidance and morning preference are verified

### Potential Weaknesses
1. The morning preference assertion (`9 <= sched.hour < 12`) is somewhat hardcoded to the expected dataset outcome
2. Carol's buffer check for late-ending meetings (4:45 PM+) would never apply to the team meeting itself since Alice's constraint caps it at 2 PM
3. Bob's "informational only" afternoon preference is correctly excluded, but this is a minor consideration

### Could an Incorrect Solution Pass?
Very unlikely. The minute-by-minute exhaustive search for earlier slots makes it nearly impossible for a solution to pass unless it correctly:
- Parses all calendars
- Implements all constraints correctly
- Finds the truly earliest valid slot
- Applies tie-breakers appropriately

Coverage rating: 4

## TB2.1 PR #245 — body and diff (gh api)

Body (lines 17-31):
> A minimal reproduction uses the supplied task calendars and two output VEVENTs:
> 1. `Context Event`, Jan 17, 2024 11:00–12:00 UTC, with no required attendees.
> 2. `Team Planning Meeting`, Jan 17, 2024 09:00–10:00 UTC, with Alice, Bob, and Carol as attendees.
> The requested meeting violates Bob's no-meetings-before-10:00 constraint. With the context event first, the current verifier passes all three checks. With the requested meeting first, the verifier fails. With the invalid target alone, it fails.

Diff (lines 33-36):
> +- An unrelated VEVENT remains permitted. Do not change input integrity, conflict,
> +availability, or earliest-time rules while repairing event binding.

Diff (line 292) — integrity block appears only as unchanged context:
>      # Integrity check: ensure calendars under /app match pristine inputs

## Python docs — docs.python.org/3/library/functions.html (newline parameter)

> When reading input from the stream, if newline is None, universal newlines mode is enabled. Lines in the input can end in '\n', '\r', or '\r\n', and these are translated into '\n' before being returned to the caller.

## Lane receipt lines quoted

corpus/evidence/round41/constraints-probe.txt:13
> CASE bob-start-0900-wed predicted=fail observed=fail tests=PFP ... the earliest test passes because no valid slot precedes it (pilot)

:31
> CASE input-crlf-rewrite predicted=pass observed=pass tests=PPP ... all three input calendars rewritten with CRLF line ends, the right slot booked
