- **Terminal-Bench 2.0 task grader (sixth task, database-file-pair class)**: covered at source-code depth and executed offline (round 40, 2026-10-26) — knowledge/tb2-db-wal-recovery-grader.md; S119, S120; probe `plans/db_wal_probe.py`, receipt `evidence/round40/db-wal-probe.txt`. A sixth instance of the same ground (6 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `db-wal-recovery` only: its whole score is seven pytest functions over one JSON export at `/app/recovered.json` whose source of truth is a SQLite main database plus an XOR-encrypted write-ahead log; the untouched initial state scores 0 of 7 while hand-typed JSON that never opens the database scores 7 of 7, because only 22 of the 33 id/name/value cells are pinned (the eleven ids, the values of ids 1-2, the names of ids 3-11); a wrong-key XOR and a plain read-write open both fail exactly the completeness and WAL tests, and a genuinely repaired WAL with no export scores 0 of 7 — so "Fix the WAL file" is only partly enforced, and path, order and the eleven-record count are the clauses the frozen case set enforces. The class "a grader that reads only an export can be satisfied by a hand-typed export" is a probed instance here; the entry claims that instance only.

<!-- COMPANION BLOCK (optional, same surface: corpus/README.md §Open gaps, "Agentic benchmark task-spec audits" chronology, insert after the round-39 entry at :309-321). Trim or drop if the L1 keeps the chronology one-entry-per-round only. -->

  - *Partly discharged round 40 (2026-10-26):* `knowledge/tb2-db-wal-recovery-grader.md` reads and executes a
    sixth Terminal-Bench 2.0 task's scoring code (`db-wal-recovery/tests/test_outputs.py` @ `2fd12b88`; S119,
    S120) against its `instruction.md`, probe `plans/db_wal_probe.py`, receipt
    `corpus/evidence/round40/db-wal-probe.txt`. The graded state is a class the lane had not executed before:
    a JSON export at `/app/recovered.json` whose source of truth is a binary database file pair — `main.db` plus
    an XOR-encrypted `main.db-wal` — scored by a path existence check, one `json.load`, a field-type pass, id
    sortedness, eleven ids in order, a duplicate check and a WAL test that re-reads two of the same cells, so the
    untouched initial state scores 0 of 7 while hand-typed JSON that never opens the database scores 7 of 7
    (only 22 of the 33 id/name/value cells are pinned), a wrong-key XOR and a plain read-write open both fail
    exactly the completeness and WAL tests, and a genuinely repaired WAL with no export scores 0 of 7
    (`cases=28 observed_pass=8 observed_fail=20 mismatches=0`). The "Terminal-Bench 2.0's" clause is **narrowed
    for that one task only**; it stays open for the remaining TB2 task graders (6 of 89 read), for any SWE-bench
    Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this
    lane). Not the task image (never pulled) or a harness run (the task's own `solve.sh` is executed as one case
    and observed pass), not contamination, not model or agent behaviour.
