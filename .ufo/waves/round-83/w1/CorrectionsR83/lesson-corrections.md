## Corrections (R82-V1–R82-V8; 2026-11-04 UTC)

These are dated corrections to the filed round-82 record, not edits to the historical round-82 lesson, report, LOG or SCORECARD. Round-83 report timestamps use UTC with `Z`. A correction paragraph states the repair obligation and its evidence; it does not by itself establish that the current-tree gate passed. Source universe: `corpus/lessons/round-82-verifier-spotcheck.md` at base `614f00559c75155ec100e945b3e8257b14fb7496`, section 6, lines 161, 168, 173, 178, 182, 187, 192 and 195.

### R82-V1

Correction: `S262=4 S263=2`. The S262 quote “echo 1 > /logs/verifier/reward.txt” has 4 whitespace-split tokens; S263's “-w requests==2.32.4” has 2. This explicitly supersedes the round-82 Gate annotations at `corpus/lessons/round-82.md:25,30` and the repeated report Sources & frontier annotations (6 and 1 respectively). S268 supersedes S262 and S269 supersedes S263; frozen S262/S263 cells remain unchanged. The substantive check extracts the quote and count from each NEW supersede row and recomputes them, rather than accepting corrected numbers in prose alone.

### R82-V2

Correction: `W04=27`, not the report's after-count of 26. The outside spotcheck re-derived 27 at `a44b2f083ee8b4115aea64598646f4bd9e3c1470`; S266 duplicates S261's URL. The repair evidence is `corpus/evidence/round83/r82-census-after.txt`, retaining the full historical census, COMMAND, that REV and EXIT 0; count its W04 output lines. This supersedes the round-82 report line 151 after-count, without relabeling the before census (26). The README's former round82 “census before/after” description was unsupported by a committed after receipt; the round83 receipt supplies the missing historical after evidence. This paragraph is not a claim that this scribe ran the census.

### R82-V3

Correction: `affected=6 unrecovered=2 recovered=4`, replacing “Five seats died” in the filed LOG/SCORECARD narrative. The six affected identities are `SweepGateR82`, `SweepHarvestR82`, `ReviewerR82`, `CriticR82`, `MutationR82` and `RegistryCounterR82`. Two did not recover a structured result: `SweepGateR82` (empty output) and `RegistryCounterR82` (nonempty unstructured transcript). Four recovered: `SweepHarvestR82`, `ReviewerR82`, `CriticR82`, `MutationR82`. The machine-readable receipt `corpus/evidence/round83/r82-seat-counts.json` binds the source bytes and separately records final outputs: seats=12, final_terminal=10, final_empty=1, final_unstructured=1. A terminal result means its output parses as a JSON object, not that its substantive claims were verified. Historical provider interruptions and recoveries are grounded in the outside spotcheck's six-name list and filed narrative, NOT inferred from final terminal/empty classifications.

### R82-V4

Correction: `82fe89d5` (full `82fe89d5dd29fa4c1bb8d85399d9e43442d1b862`) is the addition commit for BOTH `plans/round82_c2_closure_debt.py` and `plans/round82_c2_checks.py`. This supersedes the round-82 report's Landed changes attribution and `LOG.md:3172` attribution to `c804dd41`. Re-derive with `git log --diff-filter=A` over these paths or inspect their membership in the pinned addition commit. The filed report and LOG remain unchanged; this new lesson entry is the correction.

### R82-V5

Correction: `three-cell README rows` index `lessons/round-82.md`, `lessons/round-81-verifier-spotcheck.md` and `lessons/round-82-verifier-spotcheck.md`. The round-81 outside spotcheck row formerly omitted its third cell, and round82's lesson was not indexed despite the report's SHONEN box 3 claim. The README fragment replaces that malformed row and appends the two absent rows in the lessons table, not under Knowledge. The repair check parses rendered table cells and exact entry paths; a mention in an evidence bullet is not an index row.

### R82-V6

Correction: `S265 and S266` must be enumerated separately in this round's Gate with URL or own-work source locator, access date and located ≤25-word quote, explicitly correcting their omission from the round-82 Gate. Their old placement under Corrections alone did not satisfy the per-new-row Gate rule. S270 supersedes S264 as a rejected row whose teaches cell has `supersedes S264 — REJECTED: ...; flip: ...`; it rejects the pinned absent locator, not the existence of harness packaging generally. Old S264 immutable cells are preserved. The companion Gate fragment below records the existing S265/S266 access evidence, not a fresh fetch by this scribe.

### R82-V7

Correction: `seven of ten new registry rows declare selftests`, NOT ten of ten. Mechanical extraction of the ten round82 additions' eight-cell SKILL registry rows yields three `none declared` exceptions: `round37-c1-attribution`, `round80-c1-remint`, `round82-c2-checks`. The other seven are `log-appendonly`, `round66-registry-check`, `round81-log-summary-probe`, `round81-vulnerable-secret-probe`, `round82-c3-sweep`, `round82-c1-plans-registry`, `round82-c2-closure-debt`. This supersedes round82 SHONEN box 1's pointer that each new row carries a self-test. Registry declaration is not evidence of selftest execution or success, and stale historical battery cardinalities are not silently updated here.

### R82-V8

Correction: `07:24-03:00=10:24Z`. Round82's `RegistryCounterR82 (died ~07:24Z)` used a local -03:00 wall-clock value with a Z suffix; the intended approximate instant is ~10:24Z, not ~07:24Z. The launch `06:26:48-03:00` is `09:26:48Z`. All round83 report timestamps use UTC (`Z`); explicit historical local offsets remain visible when quoted. The historical report remains byte-identical, rather than having its time label rewritten.

## Gate supplement — historical S265/S266 omission correction

This explicitly corrects the round-82 Gate omission; it does not create or re-admit these rows and does not assert a new network access.

- **S265 — own-work supersede of S260.** Source locator `corpus/evidence/round81/log-summary-date-ranges-probe.txt` (no external URL; own-work source). Recorded access date **2026-11-04 UTC**. Located quote at **line 1**: “# tb2 log-summary-date-ranges grader probe (round 81)” (**7** whitespace-split tokens). Receipt stamp occupies lines 2–14, `OBSERVATIONS_BEGIN` is line 15 and CASE observations begin at line 16. This enumerates the supersede row previously left outside the Gate.
- **S266 — supersede of S261.** URL `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md`; companion URL `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/vulnerable-secret/instruction.md`. Recorded accesses **2026-11-04T08:26:13Z**, re-fetch **2026-11-04T09:47Z**, HTTP 200 (historical S266 record). Located quotes: first document **line 9**, “Write a CSV file /app/summary.csv with the following structure (including the header):” (**12** tokens); companion **line 1**, exact substring “The goal is to extract this secret key” (**8** tokens). This deliberately stops before the backticked path rather than silently dropping Markdown bytes from a longer quote. Each quote is ≤25 words. SourcesR83 separately supplies fresh round83 access receipts in `SourcesR83/Gate.proposed.md`; those are peer evidence, not fetches performed by this scribe.

## Mistakes — outside-captured record debt

| ID | Class | Evidence | Captured by | Fix and falsifier |
|---|---|---|---|---|
| R82-V1 | Repeated annotation arithmetic error; previous repair scan too narrow | S262/S263 quotes recompute 4/2, not 6/1; filed Gate repeats the errors | Outside spotcheck §6:161; NOT a round82 self-catch | Append S268/S269 supersede rows and dated correction; extract NEW-row quote/count and recompute |
| R82-V2 | Unreceipted after-state and wrong count | Historical tip census has 27 W04, report says 26; only before receipt retained | Outside spotcheck §6:168 | Retain full COMMAND/REV/EXIT after capture at historical tip; count its W04 lines |
| R82-V3 | Narrative cardinality and status conflation | “Five” conflicts with six named identities; final outputs are 10 terminal/1 empty/1 unstructured | Outside spotcheck §6:173 | Separate affected=6, unrecovered=2, recovered=4 from final classifications; bind machine receipt to source SHA |
| R82-V4 | Commit attribution error | Both C2 tools' addition history points to 82fe89d5, not c804dd41 | Outside spotcheck §6:178 | New dated correction; re-derive addition commit from Git history |
| R82-V5 | Missing index and malformed rendered row | Round82 lesson absent; round81 outside row has two cells in three-column table | Outside spotcheck §6:182 | Three valid index rows with exact paths; parse cells rather than accepting prose mentions |
| R82-V6 | Gate incompleteness and rejected-row contract drift | S265/S266 outside Gate; S264 teaches lacks combined REJECTED/flip shape | Outside spotcheck §6:187 | Enumerate historical access/located quotes in Gate; append rejected S270 supersede; keep old immutable cells |
| R82-V7 | Declaration overclaim | Ten new rows, seven selftest declarations, three none-declared exceptions | Outside spotcheck §6:192 | Derive ten cells mechanically; name exceptions; do not equate declaration with execution |
| R82-V8 | Time-zone unit error | Approximate local 07:24 mislabeled Z; launch was 09:26:48Z | Outside spotcheck §6:195 | Explicit 07:24-03:00=10:24Z correction and UTC convention; preserve historical report |
