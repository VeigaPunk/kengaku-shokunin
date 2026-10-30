# CN2CrossSource — scoped findings (round 55, wave 1)

Cross-source dataset: the 13 executed TB2 task graders (rounds 35–46 + r55 chess-best-move).
Full deliverable: `w1/CN2CrossSource/class-table.md` (13-row table + routing); seat log:
`w1/CN2CrossSource/report.md`.

## Class table (compressed)

| # | task (round) | graded artefact | operation | partial credit | receipt cases |
|---|---|---|---|---|---|
| 1 | protein-assembly (r35) | DNA text file, translated in-process | literal (5 AA literals, positional chain) | none | 18: 5P/13F, mm=0 |
| 2 | regex-log (r36) | regex file run in-process vs hard-coded log | literal (full-list equality, 9 dates) | none | 24: 8P/16F, mm=0 |
| 3 | configure-git-webserver (r37) | live HTTP service state via helper | literal (substring `TEST PASSED`) | none | 22: 9P/13F, mm=0 |
| 4 | build-pmars (r38) | build provenance (binary + source shape) | ldd-scan (+presence, output regex, dir shape) | none | 22: 7P/15F, mm=0 |
| 5 | git-leak-recovery (r39) | repo history + flag + work-tree checksum | chain-compare (5 git probes + checksum) | none | 25: 13P/12F, mm=0 |
| 6 | db-wal-recovery (r40) | JSON export of DB+WAL | literal (per-cell, 22/33 pinned) | none | 28: 8P/20F, mm=0 |
| 7 | constraints-scheduling (r41) | one-event ICS read by regexes | chain-compare (grader-carried constraint model + earliest scan) | none | 25: 6P/19F, mm=2 (carried pilot) |
| 8 | circuit-fibsqrt (r42) | gate list executed by grader-compiled simulator | chain-compare (28-value chain vs fib(isqrt) table) | none | 16: 7P/9F, mm=0 |
| 9 | feal-differential (r43) | agent Python module imported in-process | literal (one equality get_keys()[5]==stolen) | none | 12: 8P/4F, mm=0 |
| 10 | feal-linear (r44) | text file, read whole | membership (F1: 100 literal substrings) | none | 14: 8P/6F, mm=0 |
| 11 | password-recovery (r45) | line file of guesses | membership (F1: one literal whole-line) | none | 16: 5P/11F, mm=0 |
| 12 | polyglot-c-py (r46) | source file run by two toolchains | chain-compare (dual-runtime, 3 fixed points × 2 runtimes) | none | 18: 7P/11F, mm=0; regrade differ=7 |
| 13 | chess-best-move (r55) | token file `move.txt` | **multiset** (sorted full-multiset over split tokens) | none | 12: 5P/7F, mm=0 |

Totals: 269 cases; partial credit uniformly none (pytest exit → single reward bit in all 13).

## Where chess-best-move sits

The strict pole of the lane's constant-compare family. Against the two membership rows: same
content `g2g4 e2e4 h7h5` → feal-linear P, password-recovery P, chess F (extras fail); duplicates
flip chess to F where membership stays P; r45's headline `decoys-1000` P is exactly chess's
`extra-decoy-move` F. Shared with r45: order-freeness, newline/whitespace tolerance, case
sensitivity. New in combination (C4ClassNovelty ruling: NOVEL, combinatorial — no single axis
is new): order-free AND multiplicity-exact AND exact-count AND any-whitespace-token split over a
bare agent-written token file. Repo sweep: no other captured grader decides by
sorted/Counter equality (db-wal's `ids == sorted(ids)` enforces order on structured JSON — the
opposite use). Also the simplest grader in the set (one file, one assert, one literal pair) and
13th of 89 frontier tasks.

## Routing recommendation

**Fleet-level pattern → kotoba (primary).** The cross-source pattern is the
instruction-vs-grader gap operationalized: all 13 entries carry receipt-derived requirement
maps, and 12/13 headline cases pass while violating stated instruction requirements
(canned-shape, literals-never-open-db, lookup-28, decoy-first-vevent, token-in-body,
input-crlf-rewrite). Gaps run both directions (instructions assert shapes graders never check:
fibsqrt "last 32 lines", feal-linear's unstated decimal format, chess "one per line" as token
discipline only). Kotoba owns instruction/prompt/output-contract craft; the transferable rule
is "an advertised requirement without a violating test state is unenforced" plus the two
instructive traps: example literals graded as attempts (chess `h1h8`), and answer constants
published inside test files (F1 family).

**Not tameshi as primary:** tameshi already owns the probe method these entries exercised
(frozen predictions, hermetic suites, regrade legs) — kengaku applied its doctrine; nothing new
to transfer. Optional secondary copy: this class table as a fixture-discrimination taxonomy
(extras-decoys discriminate multiset from membership; format decoys discriminate literal-rows).

## Anomalies reported (sibling-owned, not fixed)

- constraints-scheduling receipt mismatches=2 (carried r40 pilot errors, disclosed).
- polyglot-c-py receipt regrade differ=7 (only non-differ=0 regrade in the dataset).
- chess entry's Q13/Q14 second-seat re-read still pending (R3) at read time.
