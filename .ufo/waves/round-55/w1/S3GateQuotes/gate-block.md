Gate block for the two new SOURCES rows (seat S3GateQuotes, 2026-10-30; splice target:
`corpus/lessons/round-55.md` `## Gate` table). Quotes verified verbatim at the pinned raw URLs
(pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`); sha256 pins re-hashed this seat, all three
match the lesson (`a540714e…f286` test_outputs.py, `6ba25be4…9ce7a` instruction.md,
`4770437e…c334` test.sh, the last byte-identical to S109's regex-log runner).

| row | URL and location | access date | located quote (at most 25 words) | decision |
|---|---|---|---|---|
| S201 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py — tests/test_outputs.py:25 | 2026-10-30 | `assert sorted(move) == sorted(["g2g4", "e2e4"])` | admit A — executed scoring predicate for the code's own behaviour |
| S202 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md — instruction.md:1 | 2026-10-30 | `If there are multiple winning moves, print them all, one per line.` | admit A — maintainer requirement the grader is mapped against |

Flip check: the runner row was dropped as duplicate of S109 (byte-identical test.sh, sha256
`4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`) — no status/recheck/used-by
cell of any existing row changed.
