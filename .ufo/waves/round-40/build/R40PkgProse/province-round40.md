## Round40 partial frontier admission (2026-10-26)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`db-wal-recovery/tests/test_outputs.py` at terminal-bench-2 `2fd12b88` — over 28 frozen synthetic end states,
via `corpus/knowledge/tb2-db-wal-recovery-grader.md` (S119, S120), `plans/db_wal_probe.py` and receipt
`corpus/evidence/round40/db-wal-probe.txt` (`cases=28 observed_pass=8 observed_fail=20 mismatches=0`;
`regrade cases=28 differ=0` on the same end states). The graded state is a class new to this lane: one JSON
export at `/app/recovered.json` whose source of truth is a binary database file pair — `main.db` plus an
XOR-encrypted write-ahead log — so the instruction's repair step ("Fix the WAL file so SQLite can read it",
`instruction.md:7`) is reachable only through that export, and the whole score is seven pytest functions over it
(`test_outputs.py:7-107`). Each case seeds `/app` as the task Dockerfile does (`Dockerfile:14-15`), runs a frozen
recipe under `bash -euo pipefail`, then imports the captured module and calls its seven test functions in file
order in a per-case bubblewrap sandbox: private network/pid/ipc namespaces, `/usr` and `/etc` read-only, private
`/tmp`, a fresh `/app`, `/cap` holding only the two executed captures, `HOME=/tmp`
(`plans/db_wal_probe.py:10-20`). Observed: the untouched initial state scores 0 of 7 (`untouched`, receipt:7) and
the task's own `solve.sh` 7 of 7 (`oracle-solve-sh`, receipt:8); hand-typed JSON that never opens the database
also scores 7 of 7 (`literals-never-open-db`, receipt:15), because the grader pins only 22 of the 33
id/name/value cells — the eleven ids, the values of ids 1-2 and the names of ids 3-11 (`test_outputs.py:53-80`) —
and reads neither `main.db` nor `main.db-wal`; a wrong-key XOR leaves the 5 base rows and fails exactly the
completeness and WAL tests (`xor-wrong-key`, receipt:11, `PPPPFPF`), the same 2-of-7 shape a plain read-write open
produces, after which the task's own oracle fails them too (`plain-read-then-solve`, receipt:10); a genuinely
repaired WAL with no export scores 0 of 7 (`decrypt-in-place-no-json`, receipt:14). It records how that captured
grader answers those synthetic states only: it does not run Terminal-Bench, the task image (`task.toml:29` names
`alexgshaw/db-wal-recovery:20251031`; the image is never pulled) or a harness (`tests/test.sh`'s `uvx`/pytest path
and its `/logs/verifier/reward.txt` write are read, not run, `test.sh:18-29`), does not validate or certify the
task, measure difficulty, gameability or contamination, judge whether these seven assertions are the right ones,
or speak for the remaining 83 TB2 task graders (89 carry `tests/test.sh`; 6 are read). Limits: host sqlite3 3.54.0,
python3 and xxd stand in for the image's Ubuntu 24.04 packages; recipes run unprivileged rather than as root; each
case stages its own `/app`, so no case observes the image's tree; the ground-truth table is computed from the two
captured files (XOR key 0x42), not from the grader; the destructive-read behaviour is published in the oracle's
own comment (`solve.sh:8`, "read-only to avoid WAL interaction") and the entry claims a probed instance of it, not
a discovery. Disclosed ordering: before the freeze the probe ran only `--dry` and `--stage-check`
(`stagecheck cases=28 failed=0`, `.ufo/waves/round-40/claims/c2-stage-check.txt`; the grader is never imported in
stage mode); the receipt is the first recorded run. Adjacent: sandboxed child execution stays fleet prior art (the
round-38 prior-art block above); capture and citation method stay chousa's; prompt and skill wording stays
kotoba's; how to repair or purge a SQLite database deployed in WAL mode belongs to the sibling lanes that own
storage operations, not to this one; deployment configuration and runtime task validity are refused. What SQLite
actually stores in a WAL, and what a given open mode does to it, is read here only through this grader's assertions
— any such finding routes rather than being absorbed. The round35/36/37/38/39 paragraphs above stay as written;
this paragraph narrows only their "remaining TB2 tasks" clause for this one task.
