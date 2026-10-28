# Lane history of the Terminal-Bench 2.0 grader series

Seat `C1ScoutLaneHistory`. Read-only. Base text is the lane tree as read on 2026-10-28 (claims pin the base tip `30801b479e3418c11089b8586178b6960216f364`). No lsp server is mounted in this seat; locations are file:line from the files themselves, confirmed by a substring search (`clause-hits.txt` in this directory).

Population check: `corpus/knowledge/tb2-*-grader.md` is 12 files. No thirteenth.

## Living open clauses a whole-benchmark grader triage would close

The series restates one remainder and raises the count. The living wording is the round-46 sentence. Counts "3 of 89" through "11 of 89" are the same remainder at older landings, not ten extra open clauses. "4 of 89", "7 of 89" and "8 of 89" are line-wrapped, so the contiguous phrase below exists on one line only for the counts the substring search hit (3, 5, 6, 9, 10, 11, 12).

### A. Unread TB2 graders — living sentence

`corpus/README.md:433` (round-46 bullet). Verbatim span:

> it stays open for the remaining TB2 task graders (12 of 89 read)

The sentence that contains it, same line:

> The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (12 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).

A Terminal-Bench 2.0 whole-benchmark triage addresses only the span "the remaining TB2 task graders (12 of 89 read)".

[INFERENCE] That is the clause `plans/round-52-claims.md:28-30` names: the lane has read 12 of 89 task graders by hand, one per round since round 35, and has no instrument that audits a benchmark's graders as a population. The frontier's own discharge verb on this bullet is "reads and executes". The frozen R52-C1 rules (`plans/round-52-claims.md:72-85`) classify primary-grader bytes by marker (V0–V4). They do not execute the other 77 graders. A static population audit closes the unread-population gap. It does not, on the frontier's verb, turn those 77 tasks into executed one-task readings of the rounds-35–46 kind.

Same line, still open, and not closed by a TB2 grader triage:

> for any SWE-bench Pro V2 grader beyond the round-31 one

> and for runtime task validity (which `PROVINCE.md` refuses to this lane)

> Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.

(`corpus/README.md:433`; the exclusion sentence is the continuation on that line.)

### B. Missing audit instrument — parent why, graders conjunct

`corpus/README.md:329`. Verbatim span:

> the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately.

A grader triage is an instrument for the graders conjunct. It does not close "task specs" or "contamination" in that sentence. The rest of the bullet (S005/S006 why, and the next-instrument sentence naming Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro primary specs) is the parent item the series has been narrowing, not a second remainder the triage retires.

## Still open, outside what this triage closes

These are still open in `## Frontier`. A TB2 grader-population triage does not discharge them.

| file:line | verbatim still-open wording |
|---|---|
| `corpus/README.md:433` | `for any SWE-bench Pro V2 grader beyond the round-31 one` |
| `corpus/README.md:433` | `and for runtime task validity (which `PROVINCE.md` refuses to this lane)` |
| `corpus/README.md:433` | `Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.` |
| `corpus/README.md:436` | `Still frontier: benchmark-maintainer releases on hidden-test governance (no private-split or hidden-test-governance release was opened this round), a runtime judge as the scoring artefact, and adoption of the card by any benchmark.` |
| `corpus/README.md:441` | `Independently sampled formats, instruction-exact parsing and future/generalized claims remain frontier.` |
| `corpus/README.md:442` | whole bullet, no partly-discharged child: `Identity-verified endpoint for novelty probes` — `:34113` absent, so no new live capability/novelty probe can run; next instrument is an identity-verified endpoint plus `plans/probe-battery-TEMPLATE.md` |
| `corpus/README.md:443` | `the row stays frontier until the wiki path resolves again (round-13/16 receipts record it absent).` |

`corpus/README.md:514-515` still says "Terminal-Bench2.0, Toolathlon and SWE-bench Pro primary specifications, generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open." That paragraph is the round-28 supporting-artifact note. `corpus/README.md:330` says the round-29 checklist "supersedes the `primary specs` half" for those three sources. The scoring-code remainder of TB2 is the living sentence at `:433`, not this older paragraph.

`corpus/README.md:330` also still contains "their scoring code was not read and stays open". Later bullets discharge pieces of it (verifier execution at `:331`, one Toolathlon task at `:332`, twelve TB2 tasks at `:333-433`). The TB2 piece that remains is `:433`.

The same six-word phrase "their scoring code was not read and stays open" also occurs at `corpus/README.md:295`, which is the coverage map, outside `## Frontier`.

## What the series discharged

Parent item: `corpus/README.md:329`, "Agentic benchmark task-spec audits".

Before the twelve hand-reads:

| round | file:line | what was discharged | what that bullet left open |
|---|---|---|---|
| 29 attempt 2 | `corpus/README.md:330` | per-benchmark task-validity checklist from maintainer artefacts of TB2, SWE-bench Pro V2, Toolathlon-Verified; supersedes the "primary specs" half | "their scoring code was not read and stays open; contamination-transparency cards, runtime task validity and hosted judges remain open." |
| 31 | `corpus/README.md:331` | "their scoring code was not read and stays open" for **verifier execution** at Harbor `6099b8cf` | other benchmarks' scoring code; runtime task validity; Toolathlon. TB2 axis-E filled for verifier execution context, not a task-level scoring-code audit (the bullet says the round-34 clarification) |
| 33 | `corpus/README.md:332` | "and for Toolathlon" for one task's scoring code (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) | "Terminal-Bench 2.0's" scoring code; any SWE-bench Pro V2 grader beyond the round-31 one; runtime task validity |

The twelve hand-reads then narrow "Terminal-Bench 2.0's", one task each. Each bullet says the clause is discharged or narrowed **for that one task only**.

| round | task | knowledge file | lesson H1 | frontier count left open |
|---|---|---|---|---|
| 35 | `protein-assembly` | `tb2-protein-assembly-grader.md` | `corpus/lessons/round-35.md:1` | "the other TB2 tasks" (`README:333`) |
| 36 | `regex-log` | `tb2-regex-log-grader.md` | `corpus/lessons/round-36.md:1` | "the other TB2 tasks" (`README:334`); `tests/test.sh` read, not run |
| 37 | `configure-git-webserver` | `tb2-git-webserver-grader.md` | `corpus/lessons/round-37.md:1` | 3 of 89 (`README:335`) |
| 38 | `build-pmars` | `tb2-build-pmars-grader.md` | `corpus/lessons/round-38.md:1` | 4 of 89 (`README:347-348`, line-wrapped) |
| 39 | `git-leak-recovery` | `tb2-git-leak-recovery-grader.md` | `corpus/lessons/round-39.md:1` | 5 of 89 (`README:363`) |
| 40 | `db-wal-recovery` | `tb2-db-wal-recovery-grader.md` | `corpus/lessons/round-40.md:1` | 6 of 89 (`README:378`) |
| 41 | `constraints-scheduling` | `tb2-constraints-scheduling-grader.md` | `corpus/lessons/round-41.md:1` | 7 of 89 (`README:394-395`, line-wrapped) |
| 42 | `circuit-fibsqrt` | `tb2-circuit-fibsqrt-grader.md` | `corpus/lessons/round-42.md:1` | 8 of 89 (`README:410-411`, line-wrapped) |
| 43 | `feal-differential-cryptanalysis` | `tb2-feal-differential-cryptanalysis-grader.md` | `corpus/lessons/round-43.md:1` | 9 of 89 (`README:427`); the bullet is cut mid-sentence at `:428` |
| 44 | `feal-linear-cryptanalysis` | `tb2-feal-linear-cryptanalysis-grader.md` | `corpus/lessons/round-44.md:1` | 10 of 89 (`README:429`) |
| 45 | `password-recovery` | `tb2-password-recovery-grader.md` | `corpus/lessons/round-45.md:1` | 11 of 89 (`README:432`); spot-check re-measured max 10 → `11 of 89 read` at `corpus/lessons/round-45-verifier-spotcheck.md:80` |
| 46 | `polyglot-c-py` | `tb2-polyglot-c-py-grader.md` | `corpus/lessons/round-46.md:1` | **12 of 89 (`README:433`) — living** |

Round 35's lesson records the first advance: "frontier rows advanced: 1 (README §Frontier task-spec item, "Terminal-Bench 2.0's" scoring-code clause, for `protein-assembly` only)." (`corpus/lessons/round-35.md:42-43`).

After round 46 the series stops. There is no thirteenth `tb2-*-grader.md`. `corpus/README.md:434` is blank and `:435` starts the next frontier item (contamination cards). No later `## Frontier` sub-bullet raises the count.

- Round 47 has no `corpus/lessons/round-47.md`. The spot-check says the frontier step was unpaid: "r47 ran a start census but no end census, no lesson, no `## Mistakes`, no sourced claim." (`corpus/lessons/round-47-verifier-spotcheck.md:67`).
- Round 48's lesson is a fence repair and a second attempt to admit the twelfth task (`polyglot-c-py`), and it says neither claim reached a committed stage-2 freeze (`corpus/lessons/round-48.md:1-5`).
- Round 49's lesson is the same twelfth task plus the fence (`corpus/lessons/round-49.md:1`). It does not name a new TB2 task.

`corpus/lessons/round-3.md` and `corpus/lessons/round-4.md` do not contain "Frontier", "tb2-", or "Terminal-Bench". They are early telemetry and endpoint-drift lessons, not this series. Rounds 30–34 lessons in the `round-3*` set are assimilation, quote gates, and the round-34 honest stop; the first hand-read TB2 task grader in `## Frontier` is round 35.

## Layout defect in the frontier list

`corpus/README.md:428` ends the round-43 bullet in the middle of the sentence:

> for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md`

`corpus/README.md:429` is the whole round-44 bullet. `corpus/README.md:430-431` are the orphaned tail:

> refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent

> behaviour.

The living open clause is `:433`, not the broken round-43 bullet.

## Per-round question list

Each question is the one that entry's opening answers. The quoted sentence is the entry's. "PROVINCE's question" in these entries is the question they refuse: task validity, difficulty, or solvability.

1. **Round 35 — `protein-assembly`.** Question: does `test_gblock` enforce the instruction's named sources, or only amino-acid literals in the test file? Quote, `corpus/knowledge/tb2-protein-assembly-grader.md:11-14`: "The grader never opens the task's reference inputs (`pdb_ids.txt`, `antibody.fasta`, the plasmid, FPbase/PDB API results): the five expected subproteins are amino-acid **literals** in the test file, and every instruction requirement that names a source (PDB sequence, FPbase spectra, the antibody's antigen, the plasmid's DHFR) is enforced only through those literals." Receipt in the entry: `cases=18 observed_pass=5 observed_fail=13 mismatches=0` (`:20`). Lesson: `corpus/lessons/round-35.md:1`.

2. **Round 36 — `regex-log`.** Question: is the graded artefact a data string the agent writes, or a regex the grader runs against a log hard-coded in the test, and do stated requirements survive that surface? Quote, `corpus/knowledge/tb2-regex-log-grader.md:11-14`: "The graded artefact is not a data string the agent writes: it is a **regex pattern file** (`/app/regex.txt`) that the grader reads, strips, compiles and runs with `re.findall(..., re.MULTILINE)` against a **25-line log hard-coded in the test file**, then compares the full match list to nine literal expected dates." Follow-on, `:21-25`: six of eight passing cases violate a stated or structural requirement and still score 1. Receipt: `cases=24 observed_pass=8 observed_fail=16 mismatches=0` (`:19`). Lesson: `corpus/lessons/round-36.md:1`.

3. **Round 37 — `configure-git-webserver`.** Question: does the score observe the git server the instruction asks for, or a `TEST PASSED` substring over helper stdout? Quote, `corpus/knowledge/tb2-git-webserver-grader.md:15-17`: "The state the verdict is computed from is, as this capture shows it, two HTTP responses from a service on `:8080`; the git server the instruction asks for is touched only by a helper step whose exit status no line of the helper reads." Receipt: `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (`:25`). Lesson: `corpus/lessons/round-37.md:1`.

4. **Round 38 — `build-pmars`.** Question: does the grader observe a build, or presence, an `ldd` string, directory shape, and a stdout prefix? Quote, `corpus/knowledge/tb2-build-pmars-grader.md:18-19`: "Nothing in those four functions builds anything, opens a Debian package, or inspects where the binary came from." Headline case in the same summary, `:26-29`: a 21-line C program, an empty `debian/` directory and a zero-byte `src/dummy.c` pass all four tests. Receipt: `cases=22 observed_pass=7 observed_fail=15 mismatches=0` (`:24`). Lesson: `corpus/lessons/round-38.md:1`.

5. **Round 39 — `git-leak-recovery`.** Question: does the grader observe that a secret left the repository, or a flag literal plus selected git text scans? Quote, `corpus/knowledge/tb2-git-leak-recovery-grader.md:22-23`: "The graded state is therefore **a repository's refs and object-store text plus one flag file plus a work-tree checksum** — nothing about how the secret was recovered, and nothing about the blobs under an unreachable commit." Headline, `:30-31`: writing the literal alone passes 5/5 while the secret commit stays. Receipt: `cases=25 observed_pass=13 observed_fail=12 mismatches=0` (`:27`). Lesson: `corpus/lessons/round-39.md:1`.

6. **Round 40 — `db-wal-recovery`.** Question: does any test read the database or the WAL, or only `/app/recovered.json`? Quote, `corpus/knowledge/tb2-db-wal-recovery-grader.md:10-13`: "the `db-wal-recovery` task is scored by **seven** pytest functions in `tests/test_outputs.py`, all seven required for the reward bit, and **every one of them opens only `/app/recovered.json`**". Headline, `:28-30`: hand-typed JSON that never opens the database passes 7 of 7. Receipt: `cases=28 observed_pass=8 observed_fail=20 mismatches=0` (`:25`). Lesson: `corpus/lessons/round-40.md:1`.

7. **Round 41 — `constraints-scheduling`.** Question: is the verdict a comparison to a fixed answer, or a scheduling model embedded in the grader? Quote, `corpus/knowledge/tb2-constraints-scheduling-grader.md:11-13`: "the verdict is not a comparison against a reference answer: it is **computed by a scheduling model embedded in the grader**". Receipt: `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (`:29`). Lesson: `corpus/lessons/round-41.md:1`.

8. **Round 42 — `circuit-fibsqrt`.** Question: does the grader check the function the instruction names, or a simulator the grader compiles and runs on 28 fixed inputs? Quote, `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:13-16`: "The agent never submits code: the graded artefact is a **data file**, `/app/gates.txt`, a list of gate assignments, and the verdict comes from a **simulator the grader compiles itself** at grading time". Finding (1), `:24-26`: a lookup table for exactly the 28 graded inputs scores 3 of 3 and prints 0 for the instruction's own examples 208 and 20000. Receipt: `cases=16 observed_pass=7 observed_fail=9 mismatches=0` (`:21`). Lesson: `corpus/lessons/round-42.md:1`.

9. **Round 43 — `feal-differential-cryptanalysis`.** Question: when the grader imports the agent's module and calls it, can a pass occur with no cryptanalysis? Quote, `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:22-24`: "This is module import plus an in-process call: the agent's module runs inside the grader's process, receives the grader's own `encrypt` function as an argument, and can reach every other public name of the same interpreter — including the module that holds the answer." Finding (1), `:33-34`: five cheats that never recover the key pass, and `:38` "None of them performs cryptanalysis." Receipt: `cases=12 observed_pass=8 observed_fail=4 mismatches=0` (`:30`). Lesson: `corpus/lessons/round-43.md:1`.

10. **Round 44 — `feal-linear-cryptanalysis`.** Question: does the score require the attack, or only that 100 decimal constants occur somewhere in an agent-written file? Quote, `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md:24-26`: "Constant-compare on a text file: the grader never imports or executes anything the agent wrote, and it never parses the file — it asks, for each of 100 expected values, whether those digits occur anywhere in the bytes." Finding (1), `:36-39`: three attack-free passes come from public pin files. Receipt: `cases=14 observed_pass=8 observed_fail=6 mismatches=0` (`:33`). Lesson: `corpus/lessons/round-44.md:1`.

11. **Round 45 — `password-recovery`.** Question: is this a second constant-compare, decided by line membership of one embedded constant? Quote, `corpus/knowledge/tb2-password-recovery-grader.md:17-22`: "Its grader is the second exemplar of the **F1 constant-compare family** this lane has executed (after `feal-linear-cryptanalysis`, round 44): the score reduces to an existence check plus exact **line membership** of one hard-coded 23-character constant, `"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses`". Receipt: `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0` (`:24`). Lesson: `corpus/lessons/round-45.md:1`.

12. **Round 46 — `polyglot-c-py`.** Question: what is graded when one source file is executed by two toolchains, and the grader compiles into the directory it just listed? Quote, `corpus/knowledge/tb2-polyglot-c-py-grader.md:16-18`: "Its grader is a **twelfth** Terminal-Bench 2.0 exemplar in this lane and a grader class new to it: the graded artefact is an **agent-authored source file executed by two toolchains at grading time**." The three moves are an exact directory listing, then `gcc` writing `cmain` into that directory, then stdout equality at three fixed inputs (`:22-28`). Receipt: `cases=18 observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7` (`:37-38`). Lesson: `corpus/lessons/round-46.md:1`.

Shared limit, not a thirteenth question. Ten of the twelve entries say validity, difficulty, and solvability are PROVINCE's question. Example: `corpus/knowledge/tb2-build-pmars-grader.md:287` "Not a statement about the task's validity, difficulty or solvability. That is PROVINCE's question, not this". The same sentence is in `tb2-circuit-fibsqrt-grader.md:352`, `tb2-constraints-scheduling-grader.md:322`, `tb2-db-wal-recovery-grader.md:290`, `tb2-feal-differential-cryptanalysis-grader.md:351`, `tb2-feal-linear-cryptanalysis-grader.md:354`, `tb2-git-leak-recovery-grader.md:287`. `tb2-git-webserver-grader.md:225` and `tb2-regex-log-grader.md:211` name PROVINCE's question as image, model, and trajectory. `tb2-password-recovery-grader.md:176-177`: whether "recover the PASSWORD" was meant to exclude reading the published test file "is the authors' question, and the entry only records that the grader cannot tell the difference." `tb2-polyglot-c-py-grader.md:205-207`: whether "a single file ... which is a polyglot" was meant to forbid a solution that leaves a build product next to it "is the authors' question, and the entry only records what the grader does." `tb2-feal-differential-cryptanalysis-grader.md:402` and `tb2-feal-linear-cryptanalysis-grader.md:391-392` use the same "authors' question" shape for the attack the instruction names. `tb2-protein-assembly-grader.md` has no "question" sentence.
