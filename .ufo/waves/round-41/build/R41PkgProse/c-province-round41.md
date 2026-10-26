# Block (c) — PROVINCE.md: round-41 paragraph, surface named, routing clause stated

Draft only. L1 applies. Append at the end of `PROVINCE.md` (after existing line 468, the last
line of the round-40 adjacency paragraph) as a new `##` section plus its adjacency paragraph.
Shape is copied from `## Round40 partial frontier admission (2026-10-26)` (lines 419-468): core
addition → observed → what it does not do + limits → adjacency/routing, and it narrows only
the previous rounds' "remaining TB2 tasks" clause for this one task.

Numbers: `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (`corpus/evidence/round41/
constraints-probe.txt:33`), `regrade cases=25 differ=0` (`:32`), `stagecheck cases=25 failed=0`
(`.ufo/waves/round-41/claims/c2-stage-check.txt`, quoted in `plans/round-41-claims.md` §C2).

## Paste (append at end of file)

```
## Round41 partial frontier admission (2026-10-26)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`constraints-scheduling/tests/test_outputs.py` at terminal-bench-2 `2fd12b88` — over 25 frozen end states, via
`corpus/knowledge/tb2-constraints-scheduling-grader.md` (S122, S123), `plans/constraints_probe.py` and receipt
`corpus/evidence/round41/constraints-probe.txt` (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`;
`regrade cases=25 differ=0`, a same-process second grading of each un-rebuilt end state, not a second run). The
graded state is a class new to this lane: an artefact at `/app/meeting_scheduled.ics` whose verdict is *computed*
by a scheduling model embedded in the test file — `_hard_ok` (`test_outputs.py:58-83`), `_overlap` (`:46-55`) and
a minute-granularity earliest-slot scan (`:158-167`) — over three sha256-pinned input calendars (digests in the
receipt header, `:2-4`); the ICS itself is read with regexes (`:40-43`), never with an ICS parser. Each case seeds
`/app` as the task Dockerfile does (`Dockerfile:14`), runs a frozen recipe under `bash -euo pipefail` (only the
oracle case has a non-empty recipe), then imports the captured module and calls its three test functions in file
order in a per-case bubblewrap sandbox: private network/pid/ipc namespaces, `/usr` and `/etc` read-only, private
`/tmp`, a fresh `/app`, `/cap` holding only the two executed captures, `HOME=/tmp`
(`plans/constraints_probe.py:10-21`). The grader is bound at `/cap/test_outputs.py`, so the
`Path(__file__).resolve().parent.parent / "inputs"` the integrity check looks for is absent and the sha256 branch
runs, as in the task image. Observed: the untouched/no-output state fails all three tests (`nop`, receipt:7) and
the task's own `solve.sh` passes 3 of 3 (`oracle-solve-sh`, receipt:8); a hand-typed Wednesday 11:00 file passes 3
of 3 without reading any calendar (`literal-correct-slot`, receipt:9), so the calendars are not load-bearing; a
first `VEVENT` decoy at Wednesday 11:00 with the attendee meeting at Friday 15:00 passes 3 of 3
(`decoy-first-vevent`, receipt:14), because tests 2 and 3 take the first `DTSTART:` of the whole file
(`:135`, `:151`) while only test 1 locates the meeting block (`:106-118`); the earliest test passes slots that are
themselves invalid when no valid slot precedes them (`bob-start-0900-wed` and `wed-1059-overlaps-alice`, both
`PFP`, receipt:13,23); rewriting all three input calendars with CRLF line ends passes 3 of 3
(`input-crlf-rewrite`, receipt:31) although `instruction.md:17-18` states "Any modification will cause the tests to
fail", because the integrity check compares decoded text (universal newlines, `:88-96`) and hashes that text on the
sha256 branch; `DTEND` is read only by the structure test, so a 90-minute meeting fails only test 1 (`FPP`,
receipt:15); and three RFC 5545-valid output forms fail — a folded `ATTENDEE` line (`FPP`, receipt:25), an explicit
`DTSTART;VALUE=DATE-TIME:` (`FFF`, receipt:26) and lowercase property names (`FPP`, receipt:30) — while a CRLF
output passes 3 of 3 (receipt:24). Two pilot prediction mismatches are carried verbatim and not corrected
(`later-valid-wed-1105`, receipt:10; `seconds-30`, receipt:18); 16 of the 25 cases are the round-40 planning seat's
pilot, disclosed at freeze (`plans/round-41-claims.md` §C2). It records how that captured grader answers those
synthetic states only: it does not run Terminal-Bench, the task image (`task.toml:30` names
`alexgshaw/constraints-scheduling:20251031`; `allow_internet = true` at `:35`; the image is never pulled) or a
harness (`tests/test.sh`'s `uvx -p 3.13`/pytest path and its `/logs/verifier/reward.txt` write are read, not run,
`test.sh:18-22,25-29`), does not validate or certify the task, measure difficulty, gameability or contamination,
judge whether these three assertions are the right ones, or speak for the remaining 82 TB2 task graders (89 carry
`tests/test.sh`; 7 are read). Limits: host python3 stands in for the image's `uvx -p 3.13` pytest, the image is
never pulled, recipes run unprivileged rather than as root, and each case stages its own `/app`, so no case observes
the image's tree; the ground-truth valid-slot table is hand-read from the three captured calendars, not from the
grader (`plans/constraints_probe.py:27-31`: the only valid starts are Wed 11:00 and Thu 11:00, earliest Wed 11:00).
Disclosed ordering: before the freeze the probe ran only `--dry` and `--stage-check` (`stagecheck cases=25 failed=0`,
`.ufo/waves/round-41/claims/c2-stage-check.txt`; the grader module is never imported in stage mode); the receipt is
the first recorded run. Adjacent: sandboxed child execution stays fleet prior art (the round-38 block above);
capture and citation method stay chousa's; prompt and skill wording stays kotoba's; the task's own `solve.sh` stays
the benchmark's, executed as one case and observed pass. The round35/36/37/38/39/40 paragraphs above stay as
written; this paragraph narrows only their "remaining TB2 tasks" clause for this one task.

Round-41 routing (`R41PkgProse` draft; L1 confirms). This lane owns what the captured grader checks and what passes
it — nothing else. **What a correct 1-hour slot is under these constraints, and RFC 5545 / iCalendar conformance,
are unowned.** Named check, 2026-10-26 15:41: `grep -rln "RFC 5545\|iCalendar\|calendar scheduling\|ICS file"
--include=PROVINCE.md --include=SKILL.md --include=*.md /home/vgpnk/Projects/shokunin` returns no lane but this one,
and the only sibling hits for `cron|scheduling|calendar` in a PROVINCE are `kaidoku-shokunin/PROVINCE.md:259` (a
"shared calendar date" used to date supersessions) and `lore-shokunin/PROVINCE.md:28`, which routes invented
calendar/era design to kotodama (`kotodama-shokunin/corpus/knowledge/culture-material/calendar-festival-systems.md`)
and recorded dates to lore — fictional calendars, not meeting scheduling or ICS conformance. So any finding of that
kind routes to the orchestrator rather than being absorbed here, and no sibling is credited with owning it.
Terminal-Bench's own task, image and oracle stay the benchmark's; the destructive-integrity finding above is about
this lane's captured grader only.
```

## Notes for L1

- S124 (TB2.1 PR #245) is **not** in this paragraph on purpose: the claims say it is to be opened live in
  wave 1, and `corpus/SOURCES.md` has no S124 row at draft time. The paragraph names TB2.1 PR #245 only in
  block (a1)/(b) as prior art, which is what the claims call it.
- "82 remaining" = 89 − 7 read. Rounds 35-40 said 83 after six; that text is untouched.
- `Dockerfile:14` is the single `COPY inputs/ /app/` line in this capture (the round-40 capture had a two-line
  comment+COPY pair; this one does not).
