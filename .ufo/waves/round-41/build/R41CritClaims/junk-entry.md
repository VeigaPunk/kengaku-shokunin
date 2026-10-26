# Filler entry: Terminal-Bench 2.0 constraints-scheduling grader

source: S122 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py — filler, no reading.
source: S123 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md — filler, no reading.
verified-at: 2026-10-26
recheck: 180d — filler

## Summary

Filler entry: this file exists only to satisfy the machine gate. It states no finding and teaches nothing.

## Located quotes

| Claim supported | “Quote” | `capture:line` |
| --- | --- | --- |
| filler | “Find a 1-hour meeting slot for Alice, Bob, and Carol during January 15-19, 2024” | `instruction.md:1` |
| filler | “Create `/app/meeting_scheduled.ics` with a 1-hour "Team Planning Meeting" including all three attendees” | `instruction.md:10` |
| filler | “The meeting must not conflict with existing calendar entries and must satisfy ALL availability constraints.” | `instruction.md:12` |
| filler | “Treat the provided calendar files as read-only.” | `instruction.md:15` |
| filler | “Output file must be in valid ICS format” | `instruction.md:21` |
| filler | “All times must be in UTC format (YYYYMMDDTHHMMSSZ)” | `instruction.md:25` |
| filler | “def _hard_ok(t0: datetime, t1: datetime) -> bool:” | `test_outputs.py:58` |
| filler | “assert app_text == repo_path.read_text(), f"Input modified: {fname}"” | `test_outputs.py:93` |

## Requirement map

| Requirement | Tag | Label | Cases |
| --- | --- | --- | --- |
| `instruction.md:1` | `window` | enforced | `weekend-sat-20` |
| `instruction.md:10` | `output-file` | enforced | `nop` |
| `instruction.md:10` | `meeting-title` | enforced | `title-wrong` |
| `instruction.md:10` | `attendees` | enforced | `missing-carol` |
| `instruction.md:10` | `one-hour` | enforced | `duration-90min` |
| `instruction.md:12` | `hard-constraints` | partly | `bob-start-0900-wed`, `seconds-30` |
| `instruction.md:12` | `no-conflict` | enforced | `conflict-mon-1230`, `later-valid-wed-1105` |
| `instruction.md:15` | `inputs-readonly` | partly | `input-appended`, `input-crlf-rewrite` |
| `instruction.md:23` | `version-prodid` | enforced | `no-prodid-header` |
| `instruction.md:25` | `utc-format` | enforced | `tzid-form` |
| `instruction.md:27` | `earliest` | partly | `later-valid-thu-1100`, `decoy-first-vevent` |

## Negative space

This filler has no falsifier and claims no scope.
