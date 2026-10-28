# C1ScoutLaneHistory — lane history of the TB2 grader series

Scout, read-only. Novelty axis. No lane-tree edit, no git mutation, no tool install. No lsp server is mounted here; clause locations are file:line, then checked by a substring search.

## What I did

Read `plans/round-52-claims.md` (R52-C1 binds the population: 12 of 89 hand-read, no population instrument). Read all 12 `corpus/knowledge/tb2-*-grader.md` openings and the PROVINCE/authors'-question lines. Read `corpus/README.md` `## Frontier` (`:324-443`) and the round-28 leftover at `:513-515`. Read lesson H1s for rounds 35–46 and the frontier hits in `round-45-verifier-spotcheck.md` and `round-47-verifier-spotcheck.md`. Searched `corpus/lessons/round-3.md` and `round-4.md` for Frontier / tb2- / Terminal-Bench: no matches. Rounds 48–49 lessons rework the twelfth task; they do not name a thirteenth.

## Commands

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1ScoutLaneHistory/tmp \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutLaneHistory
```

Python over the lane tree (stdout and `clause-hits.txt`): glob `corpus/knowledge/tb2-*-grader.md`; print `corpus/README.md` lines 329–335, 428–433, 436, 441–443; record every line containing the open-clause needles and every `\d+ of 89 read`.

## Measured numbers

- Grader files: **12**. No thirteenth `tb2-*-grader.md`.
- `N of 89 read` occurrences in `corpus/README.md`: **10**, at lines 335 (3), 348 (4), 363 (5), 378 (6), 395 (7), 411 (8), 427 (9), 429 (10), 432 (11), 433 (12). The living count is **12 of 89** at `:433`.
- Substring `it stays open for the remaining TB2 task graders (12 of 89 read)` is on `:433` only.
- Tools installed: none.

## Open clauses a whole-benchmark triage would close

Living remainder, `corpus/README.md:433`, verbatim:

> it stays open for the remaining TB2 task graders (12 of 89 read)

Parent instrument gap, `corpus/README.md:329`, verbatim:

> the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately.

The triage is the graders conjunct of that sentence, and the "remaining TB2 task graders (12 of 89 read)" span. It does not close "task specs", "contamination", SWE-bench, or runtime task validity.

[INFERENCE] The frontier verb on the round-46 bullet is "reads and executes". R52-C1 (`plans/round-52-claims.md:72-85`) classifies grader bytes by marker. That closes the population gap the claims file names at `:28-30`. It does not turn the other 77 tasks into executed one-task readings.

Counts 3–11 of 89 are the same remainder at older landings, not extra open clauses. "4 of 89", "7 of 89" and "8 of 89" are line-wrapped (`:347-348`, `:394-395`, `:410-411`).

## Still open, and not closed by that triage

| file:line | verbatim |
|---|---|
| `corpus/README.md:433` | `for any SWE-bench Pro V2 grader beyond the round-31 one` |
| `corpus/README.md:433` | `and for runtime task validity (which `PROVINCE.md` refuses to this lane)` |
| `corpus/README.md:433` | `Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.` |
| `corpus/README.md:436` | `Still frontier: benchmark-maintainer releases on hidden-test governance (no private-split or hidden-test-governance release was opened this round), a runtime judge as the scoring artefact, and adoption of the card by any benchmark.` |
| `corpus/README.md:441` | `Independently sampled formats, instruction-exact parsing and future/generalized claims remain frontier.` |
| `corpus/README.md:442` | whole bullet, no discharge child: identity-verified endpoint; `:34113` absent |
| `corpus/README.md:443` | `the row stays frontier until the wiki path resolves again (round-13/16 receipts record it absent).` |

`corpus/README.md:514-515` still says TB2 primary specifications remain open. `:330` says round 29 supersedes the primary-specs half. The TB2 scoring-code remainder that is still live is `:433`.

Layout defect: the round-43 bullet is cut at `corpus/README.md:428` (`which `PROVINCE.md``). `:430-431` are the orphaned tail ("refuses to this lane). Not the task image…"). The living clause is `:433`.

## Discharged by the series

Parent: `corpus/README.md:329`. Before the twelve: round 29 checklist (`:330`, scoring code stays open), round 31 verifier execution (`:331`), round 33 one Toolathlon task (`:332`, leaves "Terminal-Bench 2.0's" open). Then one executed TB2 task per round, 35–46, each "for that one task only", count ending at 12 of 89. Round 35 lesson: "frontier rows advanced: 1 … for `protein-assembly` only" (`corpus/lessons/round-35.md:42-43`). Round 47 paid no frontier step (`corpus/lessons/round-47-verifier-spotcheck.md:67`). Rounds 48–49 stay on `polyglot-c-py`.

## Per-round question list

Full sourced quotes are in `frontier-open.md` (kept copy below). Short form, question then the entry line that answers it:

1. Round 35 `protein-assembly` — does `test_gblock` enforce named sources, or only amino-acid literals in the test? `tb2-protein-assembly-grader.md:11-14`. `cases=18 observed_pass=5 observed_fail=13 mismatches=0`.
2. Round 36 `regex-log` — is the artefact a data string, or a regex run on a 25-line log hard-coded in the test? `tb2-regex-log-grader.md:11-14`. `cases=24 observed_pass=8 observed_fail=16 mismatches=0`. Six of eight passes violate a stated requirement (`:21-25`).
3. Round 37 `configure-git-webserver` — does the score observe the git server, or a `TEST PASSED` substring over HTTP helper output? `tb2-git-webserver-grader.md:15-17`. `cases=22 observed_pass=9 observed_fail=13 mismatches=0`.
4. Round 38 `build-pmars` — does the grader observe a build, or presence, `ldd`, directory shape, and a stdout prefix? `tb2-build-pmars-grader.md:18`. `cases=22 observed_pass=7 observed_fail=15 mismatches=0`.
5. Round 39 `git-leak-recovery` — does the grader observe that a secret left the repo, or a flag literal plus selected git scans? `tb2-git-leak-recovery-grader.md:22-23`. `cases=25 observed_pass=13 observed_fail=12 mismatches=0`.
6. Round 40 `db-wal-recovery` — does any test open the database or the WAL, or only `/app/recovered.json`? `tb2-db-wal-recovery-grader.md:10-13`. `cases=28 observed_pass=8 observed_fail=20 mismatches=0`.
7. Round 41 `constraints-scheduling` — is the verdict a fixed answer, or a scheduling model embedded in the grader? `tb2-constraints-scheduling-grader.md:11-13`. `cases=25 observed_pass=6 observed_fail=19 mismatches=2`.
8. Round 42 `circuit-fibsqrt` — does the grader check the named function, or a simulator it compiles and runs on 28 fixed inputs? `tb2-circuit-fibsqrt-grader.md:13-16`. `cases=16 observed_pass=7 observed_fail=9 mismatches=0`.
9. Round 43 `feal-differential-cryptanalysis` — can an imported agent module pass with no cryptanalysis? `tb2-feal-differential-cryptanalysis-grader.md:22-24`. `cases=12 observed_pass=8 observed_fail=4 mismatches=0`.
10. Round 44 `feal-linear-cryptanalysis` — does the score require the attack, or 100 decimal constants somewhere in the file? `tb2-feal-linear-cryptanalysis-grader.md:24-26`. `cases=14 observed_pass=8 observed_fail=6 mismatches=0`.
11. Round 45 `password-recovery` — is the score line membership of one embedded constant? `tb2-password-recovery-grader.md:17-22`. `cases=16 observed_pass=5 observed_fail=11 mismatches=0`.
12. Round 46 `polyglot-c-py` — what is graded when one source file is executed by two toolchains and the grader compiles into the directory it just listed? `tb2-polyglot-c-py-grader.md:16-18`. `cases=18 observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`.

PROVINCE's question (validity, difficulty, solvability, or image/model/trajectory) is what these entries refuse. `tb2-protein-assembly-grader.md` has no "question" sentence. Details and line numbers: `frontier-open.md` last paragraph.

## Files

Kept (scratch removed after the copy, seat discipline):

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutLaneHistory/report.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutLaneHistory.md` (same findings)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutLaneHistory/frontier-open.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutLaneHistory/clause-hits.txt`

Written first under `/fast/scratch/hyaku/kengaku-r52/C1ScoutLaneHistory/` (`frontier-open.md`, `clause-hits.txt`), then copied here and the scratch tree removed.
