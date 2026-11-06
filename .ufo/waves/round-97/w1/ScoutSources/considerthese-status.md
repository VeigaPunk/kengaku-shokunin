# considerthese 2026-11-05 — implementation status at T (round 97, f1083da6)

Proposal file: `considerthese/2026-11-05.md` (23 lines; landed `70eb8cac`; window r60–r91,
read at `cd0c116`). The file itself says "proposals only, nothing acted on". Checked at T for
whether any proposal has since landed, and whether it is still relevant. No file was changed.

| # | proposal (short) | status at T | evidence |
|---|---|---|---|
| 1 | cap calibration at 8 when any routed finding is older than two rounds; cap printed by the gate, not typed | **unimplemented** | `SCORECARD.md:4467` r96 calibration "held at ceiling 10"; `plans/round-97-claims.md` R97-C2 "calibration (held at ceiling 10)"; no cap emission in `plans/round97*.py` (only `CAPDIR`/`capture=` matches); `plans/round9*_burndown.py` compute `oldest_pending` but print no cap |
| 2 | root-of-trust manifest of checker shas verified outside the lane (CI cheapest) | **unimplemented** | `.github/` absent (`test -d .github` → absent); `git ls-files` has no trust-root manifest (only round-28 scratch fixtures and `round-52/w1/C1CritTrustBoundary.md`); trust root still the in-lane pin ledgers (`counter-pins-r90.json`, `counter-pins-r91.json`) |
| 3 | SKILL.md byte budget gate + generated one-page STATUS | **unimplemented** | `SKILL.md` 364,893 B at T (356 KB when proposed); no `STATUS.md` at repo root; no `st_size`/`getsize` check on SKILL/SCORECARD/LOG in `plans/*.py` (`plans/state_check.py` checks headings only) |
| 4 | one round in five on an outward question; report instrument vs domain rounds separately | **unimplemented** | no "instrument round"/"domain round" count in `SCORECARD.md`, `LOG.md`, `SKILL.md`; round 97 is instrument-only (C1 replay + C2 calibration, 7 `R97-C` references in the claims) |
| 5 | ask the operator to rule on the coverage L0 cap (retire / re-scope / lifting condition) | **unimplemented, still relevant** | `SCORECARD.md:670` "coverage is capped at 7 by the unresolvable-surface clause pending the operator's coverage-cap ruling"; `plans/round-97-claims.md` "held at its L0 cap 7"; no ruling in `LOG.md`; cap has stood since round 25 (2026-10-20) |

Relevance at T: 1, 2 and 4 are instrument-governance proposals that the round-97 shape (two
instrument claims, no domain claim) leaves untouched; 3 is measurable and still true (SKILL.md
grew 8 KB since the proposal); 5 is the one with a live scoring consequence (coverage held at 7
since round 25 while the ledger moved to 41 executed of 88 at T).
