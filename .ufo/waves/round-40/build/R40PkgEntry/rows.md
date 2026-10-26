Draft registry rows for `corpus/SOURCES.md` (kengaku round 40, C2). Append after S118 in the
`## Registry` table; the lane working tree already carries these two rows uncommitted (`git diff
corpus/SOURCES.md` = +2 lines), so integration is idempotent — keep one copy. Eleven cells, column
order from the header `| id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by |`.

| S119 | Terminal-Bench 2.0 db-wal-recovery task grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit: seven pytest functions over /app/recovered.json, as this capture shows it | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-107, :98 “assert len(data) > 5, "Only base data recovered - WAL decryption failed"” (12 words); sha256 88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49 | seven pytest functions read only the exported JSON: existence, a non-empty list, field types, id order, eleven ids with two pinned values and nine pinned names, unique ids, and more than five rows | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-db-wal-recovery-grader.md |
| S120 | Terminal-Bench 2.0 db-wal-recovery task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/instruction.md | docs | A | the request this one task states to the agent at a pinned commit, as the maintainer's own specification the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1-14, :7 “Fix the WAL file so SQLite can read it” (9 words); sha256 5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26 | three asks: repair the encrypted write-ahead log so SQLite reads it, extract all eleven records including WAL changes, and write them sorted by id as a JSON list at /app/recovered.json | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-db-wal-recovery-grader.md |

Checks a reviewer can re-run: `scripts/sources-census.sh validate --file corpus/SOURCES.md` (green once
the entry file exists — E11 `used-by` is what the entry satisfies); each anchor cell carries exactly one
`sha256 <64 hex>` token equal to `plans/pkg-spec-r40.json`'s pin for that row; both anchor quotes are
verbatim at `corpus/evidence/round40/tb2-db-wal-recovery/{test_outputs.py:98,instruction.md:7}`.
