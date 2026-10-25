Axes: calibration (primary; Q13 enforces evidence timing). Review scope: preregistration wording and checker contract.

## Findings — high

- **The specified checker is existence-only and can be satisfied by a placeholder or empty file.** `plans/round-26-claims.md:20-24` requires cited report paths and the proposed interface tests whether a path “exists in that commit's tree”; it sets no minimum content, required review fields, or report-role/roster match. A zero-byte blob or arbitrary `.md` at an accepted path therefore qualifies. Current `corpus/QUALITY.md:97-104` repeats the tree-presence rule; it does not close this gap.
- **An own/unassigned/first-wave report can be mistaken for a second-seat report.** The interface accepts `.ufo/waves/round-N/<wave>/<Seat>.md` or a bare `<Seat>.md` resolvable under wave dirs, but specifies no canonical second-seat roster lookup or ambiguity rejection (`plans/round-26-claims.md:20-24`). Q10 says the seat must differ from the entry writer (`corpus/QUALITY.md:75-78`); current Q13 text also says this (`corpus/QUALITY.md:99`), but the checker interface does not define how to establish either identity. Thus that prose is not an enforceable guard as specified.

## 8ea41f9 red case

- The expected red is well-founded: the landed Gate cell says “by wave-2 seats” (`corpus/lessons/round-25.md:29`); the contemporaneous closure says the Gate landed at 21:44:48 -03 and the first wave-2 report appeared at 21:49:53 -03 (`corpus/lessons/round-25-verifier-spotcheck.md:36-39`). `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e 8ea41f9:.ufo/waves/round-25/falsify/RevQ11R12R13.md` → fatal, exit 128; `git ls-tree -r --name-only 8ea41f9 -- .ufo/waves/round-25` listed build reports only. The generic-only Gate row has no qualifying second-seat path, so the preregistered rule should reject it (`plans/round-26-claims.md:23-24`).
- **Not runtime-verified:** `plans/gate_timing_check.py` was absent when inspected (read returned “Path … not found”); the red-before result is an acceptance criterion, not an observed checker run.

## Tighten wording and checks

Replace “a report path that exists” with: “For every admitted Gate row, list at least one unique repo-relative path to a Q10 re-read report by an assigned second-seat reviewer. The path MUST resolve unambiguously to that round's canonical second-seat/falsify roster in the admitting commit; the reviewer identity MUST differ from the entry writer. Generic wave/seat references are never evidence. Each report MUST be a non-empty regular tracked file with a structured Q10 block naming the candidate, the sources/quote locations and numbers re-read, and the reviewer’s confirm/correct result.”

Checker: read only the requested commit tree; parse each admit row; reject generic-only support, bare/ambiguous/absolute/traversal paths, paths outside the roster, writer identity matches, non-regular or zero-byte blobs, and missing/mismatched Q10 blocks. Require the report’s candidate/source/location fields to cover the Gate’s Q10 claims. Add red fixtures for generic-only 8ea41f9, empty blob, arbitrary placeholder, writer’s report, and unassigned/first-wave path; green fixture for a valid roster-matched report. Human review remains necessary to judge whether the stated re-read was genuine; file checks cannot prove it.

## Verification gaps

- LSP unavailable: `read xd://lsp` returned “No such tool” (no LSP device mounted); no grep was used as semantic proof. No checker/tests were run because the checker file is absent.
- Installs/updates: none.

VERDICT: PARTIAL — the design catches the specific 8ea41f9 timing defect by specification, but permits placeholder/empty and potentially non-independent reports; enforce roster, identity, and content constraints before relying on it.