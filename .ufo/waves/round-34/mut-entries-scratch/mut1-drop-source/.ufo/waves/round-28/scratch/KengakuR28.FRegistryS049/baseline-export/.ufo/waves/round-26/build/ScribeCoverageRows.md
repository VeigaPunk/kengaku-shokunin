# ScribeCoverageRows — round 26 (build wave, scribe)

Base observed: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (lane master, pre-registration commit).
Private clone: `/tmp/kengaku-r26-ScribeCoverageRows-4`, branch `r26-ScribeCoverageRows-4` at e0037a8.
Lane tree not written. Pre-existing lane change `M PROVINCE.md` belongs to another seat and was left alone.

## Behavior
Drafted the five requested `corpus/README.md` updates in the clone, formatted to the existing row shapes.
Every placeholder that depends on unlanded work is marked `**[PENDING: …]**` and must be resolved before admission.

| # | Item | Anchor in base README | Draft |
|---|---|---|---|
| 1 | Knowledge index row | after `:61` (attribution-interval-calibration) | `knowledge/grader-perturbation-audit.md`; Covers / Primary source columns; numbers PENDING |
| 2 | Lessons index row | after `:93` (round-25) | `lessons/round-26.md`; M39, M40, R26-E4, R26-E1–E3 |
| 3 | Round-26 additions table | after `:168` (round-25 additions) | `evidence/round26-sources/`, `evidence/round26-calibration/` |
| 4 | Coverage-map row | after `:229` (statistical reporting) | "Grader robustness / response-format invariance"; depth label PENDING |
| 5 | Frontier sub-bullet | after `:255` (round-25 Correction) | `*Partly discharged round 26 (2026-10-21):*`; verdicts PENDING; remaining frontier named |

Diff: `corpus/README.md` +11 lines, 0 deletions.

## Gates and admission conditions
- Q13 (claims §0): the knowledge row (#1), coverage row (#4) and frontier sub-bullet (#5) must land in the same commit as `corpus/knowledge/grader-perturbation-audit.md` and the wave-2 re-read reports it cites. Otherwise the row is a dangling index entry.
- Row #2 depends on `corpus/lessons/round-26.md` existing. At base it does not (verified: `ls corpus/lessons` has no round-26 file). M39/M40 names are taken from `plans/round-26-claims.md` §0 and must match the lesson the lesson scribe writes.
- Row #3: `evidence/round26-sources/` is an empty directory at base (git does not track it). Only `evidence/round26-calibration/round-start.txt` exists. Row text names after-state files as PENDING.
- Row #4 and #5 numbers and SOURCES ids (S### for this round) are not yet assigned; `corpus/SOURCES.md` has rows through S042 at base (42 rows, R26-E3).

## Gaps found (not drafted; outside the requested five)
1. `corpus/lessons/round-25-verifier-spotcheck.md` has no index row in `corpus/README.md` (only `round-24-verifier-spotcheck` is indexed). Round-25 lessons index is incomplete. Recommend a row in the same lessons table.
2. Plans table (`README.md` `### plans/`) has no rows for `plans/grader_perturb.py`, `plans/gate_timing_check.py`, or `plans/fixtures/r26/`. The `state_check.py` row says v2-era text (`--summary`, `--json`, `--selftest`); v3 P3 needs a PENDING note.
3. `QUALITY.md` is described in the supporting-files table as "Q1–Q8 … round 24"; Q13 (claims §0) will need that line updated when Q13 lands.
4. `evidence/round26-sources/` must be created with a `.gitkeep` or populated before it can be indexed as a committed dir.

## Checks
No instrument, grader, census or state_check run; per the item, only the draft was produced. The only commands run were read-only `ls`, `grep`, `git clone --no-hardlinks`, `git switch -c`, `git diff` and `sha256sum`.

## Installs / upgrades
None. (Tooling directive reviewed; nothing needed for a Markdown draft.)

## Files written
| file | sha256 |
|---|---|
| `/tmp/kengaku-r26-ScribeCoverageRows-4/corpus/README.md` (draft, clone) | `51e2a380718a55d9d02e6e3a823e3f8b64bd6538be675140cd79ca728de13b34` |
| `/tmp/kengaku-r26-ScribeCoverageRows-4-readme.patch` (git diff vs e0037a8) | `e7eb4359b1153bf36ba0f08f01772ce3c9be90a9bc8efdb4d74a957befcef7a8` |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/build/ScribeCoverageRows.md` (this report) | written by this file |

The integrator (KengakuR26-2) applies the patch to the lane only with the lane's commit that lands the C1 entry, Q13 gate and round-26 lesson.

VERDICT: five README drafts ready as a clone patch (+11 lines); rows #1, #2, #4, #5 are conditional on the C1 entry, lesson, and SOURCES ids landing in the same commit; two index gaps (round-25-verifier-spotcheck row, plans rows) flagged, not drafted.
