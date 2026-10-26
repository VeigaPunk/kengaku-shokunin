Draft `corpus/README.md` edits for the round-40 C2 package (kengaku round 40, 2026-10-26).

## 1. Index row — `## What's here` table, after the `knowledge/tb2-git-leak-recovery-grader.md` row

| `knowledge/tb2-db-wal-recovery-grader.md` | A sixth Terminal-Bench 2.0 task grader read and executed: `db-wal-recovery` scores seven pytest functions that all open only `/app/recovered.json` — existence, a non-empty list, three field types, sorted ids, eleven ids with values `150`/`250` on ids 1-2 and the names `cherry`…`mango` on ids 3-11, unique ids, and a `>5`-row floor — so 22 of the 33 `id`/`name`/`value` cells are pinned and hand-typed JSON passes 7/7 without opening the database, "Fix the WAL file" is graded only through the export, one plain read-write `sqlite3` open destroys the encrypted log so the task's own oracle then fails 2 tests, a wrong XOR key leaves the five base rows, `True` passes as an int value, float ids `1.0`…`11.0` fail only the structure test, and an extra field passes; S119, S120; probe `plans/db_wal_probe.py`, receipt `evidence/round40/db-wal-probe.txt` |

## 2. Coverage bullet — `## Coverage map`, after the "(fifth task, repository-history class)" bullet

- **Terminal-Bench 2.0 task grader (sixth task, binary database file pair)**: covered at source-code depth and executed offline (round 40, 2026-10-26) — knowledge/tb2-db-wal-recovery-grader.md; S119, S120; probe `plans/db_wal_probe.py`, receipt `evidence/round40/db-wal-probe.txt`. A sixth instance of the same ground (6 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `db-wal-recovery` only: its whole score is seven pytest functions over one JSON export whose source of truth is a SQLite main database plus an XOR-encrypted write-ahead log, so the repair the instruction asks for is never read — `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0`. The passing vacuum is bounded by length, id multiset and the 22 pinned cells (`empty-list`, `truth-drop-id11`, `truth-plus-duplicate-id11`, `truth-wrong-path` fail); the unanswered surfaces are the database itself, the WAL, nine values, two names, extra keys and `True`-as-int. Not runtime task validity, not contamination measurement, not deployment config.

Both fragments were proven in a clone of the lane HEAD by `plans/pkg_gate.py` clause P8
(`index rows for knowledge/tb2-db-wal-recovery-grader.md=1`, the "every knowledge file is indexed"
equality, and the coverage bullet naming the entry and `evidence/round40/db-wal-probe.txt`).
