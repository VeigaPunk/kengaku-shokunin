# Round 65 — README index rows to append (LessonDraft, 2026-11-03)

Two rows to append to `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md`. Both are
byte-exact as written; the L1 lands them at the round-65 landing. Nothing else in `corpus/README.md`
is touched by this seat.

---

## Row 1 — the round-65 lesson (lesson-index row)

**Placement:** in the `## Round29 supporting artifacts (2026-10-21; knowledge admission deferred)`
table (`| Path | Covers |`), immediately AFTER the existing `| `lessons/round-64.md` | … |` row
(currently `corpus/README.md` line 552). The round-64 lesson row is the shape precedent: two
cells, `| `lessons/round-65.md` | <Covers> |`, no third cell.

**Append exactly this one line:**

```
| `lessons/round-65.md` | Gate (S232 sqlite-with-gcov grader admit tier A, S233 SQLite amalgamation 3.54.1 admit tier A, S234 kv-store-grpc grader superseding S230 admit tier A; no rejections of admitted rows; reject-equivalents: query-optimize blocked by its 1.05x timing threshold and pinned 250 MB-class database, torch-pipeline-parallelism blocked by absent cp314 torch wheels), the four R65-C2 dated append-only corrections (S234 superseding row, round-64 `R64-ERRATUM-65` block, SCORECARD addendum-classified block, QUALITY Q47), a no-bind observation and the four C2 before-counters at 0; verdict: [L1 fills the C1/C2 verdicts] |
```

**L1 note on the trailing cell:** the `[L1 fills the C1/C2 verdicts]` text is the placeholder the
round-64 row also carries in spirit (its verdict clause is written at landing). The L1 replaces it
with the measured verdict, e.g. `verdict: C1 predicate met (capability enters, coverage held at the
L0 cap), C2 predicate met (calibration held at the ceiling)` — or the honest miss wording, if either
claim misses. Do not leave the bracket text in the landed file.

---

## Row 2 — the new round-65 knowledge entry (knowledge-index row)

**Placement:** in the `## What's here` table (`| Entry | Covers | Primary source |`), immediately AFTER
the existing `| `knowledge/tb2-kv-store-grpc-offline.md` | … |` row (currently `corpus/README.md`
line 91).

**Append exactly this one line (3-cell form, matching the table header and the 60-row majority of
this table):**

```
| `knowledge/tb2-sqlite-gcov-offline.md` | The first offline replay of a db-state TB2 grader (`sqlite-with-gcov`, S232; the SQLite amalgamation build input, S233): `plans/round65_c1_sqlite_probe.py` runs the grader's three legs in bwrap against a lane-built gcov-instrumented `sqlite3` compiled in place from the pinned amalgamation and staged on PATH with the host binary masked, against a frozen five-case × three-leg table (G1 P/P/P, G2 F/F/F, G3 P/P/F, G4 P/P/F, G5 P/P/F); the receipt of record `corpus/evidence/round65/sqlite-gcov-probe.txt` re-derives the frozen five vectors and the three located message fragments (`sqlite3 not found in PATH`, `No .gcno files found`, `No .gcda files found`). The class row flips; `query-optimize` stays recipe-unexecuted on its timing-threshold design. Provenance trio opens the entry (trio gate green). | S232 (grader at pin `2fd12b88`), S233 (SQLite amalgamation 3.54.1); probe `plans/round65_c1_sqlite_probe.py`, receipt of record `corpus/evidence/round65/sqlite-gcov-probe.txt` |
```

**L1 note on the trailing cell:** the third cell names the sources, the probe and the receipt of
record — the same shape as the `knowledge/tb2-cancel-async-tasks-grader.md` row (the last 3-cell
knowledge row). The L1 fills in the measured predicate string inside the Covers cell (the round-64
row carries the literal `PREDICATE R64-C1 pass`); the text above deliberately states only what is
already frozen or already measured (the five frozen vectors, the three captured fragments) and no
predicate verdict, so that the L1 can paste the measured string without rewriting the row.

**Alternative if the L1 prefers the 2-cell shape of the two most recent knowledge rows.** The
round-63 (`corpus/README.md` line 90) and round-64 (line 91) knowledge rows shipped with the third
column empty, so the table renders a 2-cell row for them; if the L1 wants the new row to match that
exact shape instead, append this line (byte-exact) and drop the 3-cell version:

```
| `knowledge/tb2-sqlite-gcov-offline.md` | The first offline replay of a db-state TB2 grader (`sqlite-with-gcov`, S232; the SQLite amalgamation build input, S233): `plans/round65_c1_sqlite_probe.py` runs the grader's three legs in bwrap against a lane-built gcov-instrumented `sqlite3` compiled in place from the pinned amalgamation and staged on PATH with the host binary masked, against a frozen five-case × three-leg table (G1 P/P/P, G2 F/F/F, G3 P/P/F, G4 P/P/F, G5 P/P/F); the receipt of record `corpus/evidence/round65/sqlite-gcov-probe.txt` re-derives the frozen five vectors and the three located message fragments (`sqlite3 not found in PATH`, `No .gcno files found`, `No .gcda files found`). The class row flips; `query-optimize` stays recipe-unexecuted on its timing-threshold design. Provenance trio opens the entry (trio gate green). |
```

Choose ONE of the two forms, not both — the entry must have exactly one index row.

---

## Optional (not one of the two required rows) — round-65 evidence bullets

The round-64 landing also appended two bullet lines under the `### Round-63 evidence (2026-11-03)`
section (`corpus/README.md` lines 599–600) naming the round's evidence dir and its wave dir. If the
L1 wants the same parity for round 65, append these two bullets under the same section (they are not
part of the two required index rows and may be skipped):

```
- `corpus/evidence/round65/` — `sqlite-gcov-probe.txt` (receipt of record for the frozen R65-C1 predicate: the five case vectors equal the frozen five, `PREDICATE R65-C1 pass`), the pre-freeze control captures `g1-capture.txt` (P/P/P, masked, coverage build on PATH), `g2-capture.txt` (F/F/F, masked, `sqlite3 not found in PATH`), `g4-capture.txt` (P/P/F, `No .gcno files found`) and `g5-capture.txt` (P/P/F, unmasked host binary answering legs 1-2, `No .gcda files found`), `grader-import-scan.txt` (stdlib-only import scan and the grader's test-function order) and `c2-before-counters.txt` (the four R65-C2 counters at 0 at base `12a62551`).
- `.ufo/waves/round-65/w1/` — the wave evidence: each seat's report and receipts (`GraderRecon`, `ProbeBuild`, `ErrataBuild`, `KnowledgeDraft`, `LessonDraft`, `SiblingOverlap`, `FreezeReview`, `SourceReview`, `ClaimFalsifier`, `ProbeMutate`, `SecurityScan`, `ControlOrigin`), the amalgamation zip and the download page capture, and the drafts that were integrated.
```

Paths in the bullets are lane-root-based (`corpus/…`, `.ufo/…`) — the form QUALITY Q47 requires
(the round-64 spot-check §7.3 defect 3). Do not write a fleet-root-relative or absolute path here.

---

## Provenance of every quoted value in these rows

| value | observed by this seat, command |
|---|---|
| five frozen vectors G1 P/P/P, G2 F/F/F, G3 P/P/F, G4 P/P/F, G5 P/P/F | `plans/round-65-claims.md` §"Frozen vectors" (read at this seat) |
| `sqlite3 not found in PATH` (G2 leg 2) | `corpus/evidence/round65/g2-capture.txt` |
| `No .gcno files found` (G4 leg 3) | `corpus/evidence/round65/g4-capture.txt` |
| `No .gcda files found` (G5 leg 3) | `corpus/evidence/round65/g5-capture.txt` |
| receipt of record path `corpus/evidence/round65/sqlite-gcov-probe.txt` | named in `plans/round-65-claims.md` (predicate + counting command) |
| probe path `plans/round65_c1_sqlite_probe.py` | named in `plans/round-65-claims.md` |
| S232 / S233 / S234 ids, URLs, tiers, statuses | `corpus/SOURCES.md` rows 248–250 (read at this seat) |
| `query-optimize` timing threshold `1.05 × golden median` and `/app/oewn.sqlite` | `corpus/evidence/round52/graders/query-optimize/tests/test_outputs.py` lines 10, 142 (`grep -n '1.05\|golden\|median'` at this seat) |
| `db-state` members `query-optimize,sqlite-with-gcov` | `corpus/evidence/round62/class-survey.txt` line 16 |
| `process-environment` members incl. `torch-pipeline-parallelism` | `corpus/evidence/round62/class-survey.txt` line 14 |
