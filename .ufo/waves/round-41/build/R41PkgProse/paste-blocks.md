# R41PkgProse — paste order for L1

Four blocks, four target files, five insertion points (block (a) is two rows in one file).
Each paste block is the first fenced block of its draft file; block (a) has two, in order.

| # | target | anchor | paste source |
|---|---|---|---|
| a1 | `corpus/README.md` | after existing line 73 (round-40 index row), as new line 74 | `a-readme-index-and-coverage.md`, first fence |
| a2 | `corpus/README.md` | after existing line 267 (round-40 coverage bullet), as new line 268 | `a-readme-index-and-coverage.md`, second fence |
| b  | `corpus/README.md` | after existing line 340 (round-40 §Frontier sub-bullet), before line 341 | `b-frontier-tb2-subbullet.md` |
| c  | `PROVINCE.md` | append after existing line 468 | `c-province-round41.md` |
| d  | `SKILL.md` | append after existing line 1030 | `d-skill-scheduling-section.md` |

Line numbers are the pre-insertion state measured at 2026-10-26 15:39 (`wc -l`:
`corpus/README.md` 499, `PROVINCE.md` 468, `SKILL.md` 1030). Apply top-down per file
(README: a1 → a2 → b) and the later anchors shift by the number of lines already added.

Nothing here edits an existing line. Round-35..40 text stays byte-identical, including every
"N of 89 read" count, because each count is true of the round that wrote it; only the round-41
sub-bullet says 7.

Numbers used, all from `corpus/evidence/round41/constraints-probe.txt`:
`cases=25 observed_pass=6 observed_fail=19 mismatches=2` (`:33`), `regrade cases=25 differ=0`
(`:32`), case cites `receipt:<line>` throughout.
