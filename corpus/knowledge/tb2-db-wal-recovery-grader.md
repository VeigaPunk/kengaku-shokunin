source: S119 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/tests/test_outputs.py — the seven pytest functions that are this task's whole score, lines 1-107, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S120 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/instruction.md — the request the grader is mapped against, lines 1-14, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS)` (green as written), re-fetch the two pinned URLs, and re-run `plans/db_wal_probe.py --lane .`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `db-wal-recovery`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `db-wal-recovery` task is scored by **seven** pytest functions in
`tests/test_outputs.py`, all seven required for the reward bit, and **every one of them opens only
`/app/recovered.json`** (`:9`, `:14`, `:23`, `:40`, `:49`, `:85`, `:94`) — the database and the encrypted
write-ahead log are read by no test. The functions check: the file exists (`:9`); it parses as a non-empty JSON
list (`:17-18`); each item is a dict carrying `id`, `name`, `value` with `int`/`str`/`int` types (`:27-35`); the
`id`s arrive sorted (`:44`); there are exactly eleven, with ids `1..11`, values `150` and `250` on ids 1-2 and the
names `cherry`…`mango` on ids 3-11 (`:53-80`); the ids are unique (`:89`); and — the test named for the WAL — there
are more than five rows plus the same two cells (`:98-107`). `tests/test.sh:25-29` maps the pytest exit status to
`/logs/verifier/reward.txt`: `1` on 0, `0` otherwise, one bit, no partial credit.

The graded state is therefore **a JSON export of a table**, and the task's stated first step — "Fix the WAL file"
(`instruction.md:7`) — is graded only through the rows that export happens to contain. Offline execution of the
captured grader over 28 frozen cases (`plans/db_wal_probe.py`; receipt `corpus/evidence/round40/db-wal-probe.txt`)
reproduced every prediction:

`cases=28 observed_pass=8 observed_fail=20 mismatches=0`

with a second call of the same seven functions on the same end state, in the same process, agreeing on all 28
(`regrade cases=28 differ=0`; a determinism read of the probe, not re-run stability — see §Regrade). The headline case is
`literals-never-open-db`: hand-typed JSON — the right ids, the two pinned values, zeroes elsewhere, the database
never opened — passes **7 of 7**, and so does `literals-names-1-2-wrong`, which gets the two names the grader does
not pin wrong. Only 22 of the 33 `id`/`name`/`value` cells are pinned at all, and nothing reads the WAL: a state
that fixes the WAL in place and writes no export scores 0 of 7 (`decrypt-in-place-no-json`), while the task's own
`solve.sh` after one careless read-write `sqlite3` open scores 4 of 7 (`plain-read-then-solve`).

This entry extends `knowledge/benchmark-grader-semantics.md` and
`knowledge/benchmark-verifier-execution-model.md` (S100 is the same repository at the same commit) and the five
earlier TB2 grader entries (`tb2-protein-assembly-grader.md`, `tb2-regex-log-grader.md`,
`tb2-git-webserver-grader.md`, `tb2-build-pmars-grader.md`, `tb2-git-leak-recovery-grader.md`). It records one edge
class new to the lane's **executed** grader sample: the graded artefact is a **JSON export whose source of truth is
a binary database file pair** — a SQLite main database plus an XOR-encrypted write-ahead log — so the score is a
comparison against a table the agent is expected to recover, with the recovery step itself unobserved. It is not a
new verdict channel (list length, set equality, per-cell equality and type gates are all old) and not a new
reading. It **narrows** the `corpus/README.md` §Frontier "Terminal-Bench 2.0's" clause for this one task only; the
clause stays open for the remaining TB2 task graders (6 of 89 read at `2fd12b88`).

## Source labels

S119 and S120 are the benchmark maintainers' own task files: primary for *what this grader checks* and for the
requirement text the map is drawn against, and a self-report for everything else. `task.toml` (captured, not a
registry row) is the authors' own metadata, read only for the declared image (`:29`), the verifier and agent
timeouts (`:22`, `:25`) and the internet policy (`:34`). The captured `solve.sh` oracle is **own reading, tier C** —
not a registry row; the probe executes it once, as the `oracle-solve-sh` case's recipe inside the sandbox, and no
finding rests on its correctness. The `Dockerfile` is a capture of the maintainers' own environment build, read for
the shape of the initial state. The probe receipt is the lane's own re-runnable gate output (tier A for its own
scope: these 28 states against these captures under host sqlite3 3.54.0, python3 and xxd).

Disclosure: the case predictions were written from a static reading of `tests/test_outputs.py` and `instruction.md`
**before the first recorded run**, and the frozen case table
(`corpus/evidence/round40/db-wal-dry-cases-freeze.txt`) carries them; seven predictions copy the round-39 planning
seat's pilot observations on this host (`untouched`, `oracle-solve-sh`, `base-only-ro`, `literals-never-open-db`,
`literals-names-1-2-wrong`, `literals-id3-name-wrong`, `truth-value-float-id1`; named in the probe docstring), and
`plain-read-then-solve` rests on that seat's measurement that a plain read-write open deletes the encrypted WAL
rather than on a prior grading of its own. See the limits section.

## What is graded (static reading)

| Step | Mechanism | Lines |
|---|---|---|
| Entry point | `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA` under `uvx -p 3.13`, `pytest==8.4.1`, `pytest-json-ctrf==0.3.5`; all seven functions are collected | `test.sh:18-22` |
| Reward | the shell maps the pytest exit status to `/logs/verifier/reward.txt`: `1` on 0, `0` otherwise — one bit, no partial credit | `test.sh:25-29` |
| Export presence | `os.path.exists("/app/recovered.json")` — existence only, no content | `test_outputs.py:9` |
| Export shape | `json.load`; `isinstance(data, list)`; `len(data) > 0` | `test_outputs.py:14-18` |
| Record shape | every item a `dict` whose keys are a superset of `{"id", "name", "value"}`, with `id` `int`, `name` `str`, `value` `int` | `test_outputs.py:27-35` |
| Order | `ids == sorted(ids)` over the export's own ids | `test_outputs.py:43-44` |
| Completeness | `len(data) == 11`; `ids == list(range(1, 12))`; `id 1 → value 150`, `id 2 → value 250`; names `cherry`, `date`, `elderberry` on ids 3-5 and `fig`…`mango` on ids 6-11 | `test_outputs.py:53-80` |
| Uniqueness | `len(ids) == len(set(ids))` | `test_outputs.py:88-89` |
| "WAL decrypted" | `len(data) > 5`; if id 1 is present its value is 150; if id 6 is present its name is `fig` | `test_outputs.py:98-107` |

Five structural consequences follow from the reading alone:

- **The export is the only state under test.** No function opens `/app/main.db` or `/app/main.db-wal`; requirement
  1 of the instruction ("Fix the WAL file so SQLite can read it", `:7`) has no assertion of its own, and the test
  named `test_wal_was_decrypted` reads the same export and asserts only a row count and two cells (`:98-107`).
- **22 of the 33 `id`/`name`/`value` cells are pinned.** The eleven `id`s are structural (`:53`, `:57-58`), the
  values of ids 1-2 are literals (`:64-67`), the names of ids 3-11 are literals (`:70-80`). Free: the names of ids
  1-2 and the values of ids 3-11 — nine of them — so most numeric content of the recovered table is unconstrained.
- **Types are checked once, in one direction.** `isinstance(item["id"], int)` rejects `1.0` while every equality
  test accepts it (`1.0 == 1`); `isinstance(item["value"], int)` accepts `True`; the key check is
  `required_fields.issubset(item.keys())` (`:30`), so extra keys are free.
- **Order is checked twice, cheaply.** `test_recovered_data_sorted` compares the export's ids to their own sort
  (`:44`) and completeness compares them to `1..11` (`:58`), so both are satisfied by the sequence `1..11` and
  neither restricts anything else.
- **The empty and near-empty states are vacuously clean on three tests.** `[]` passes existence, structure and
  uniqueness (`PFPPFPF` in the receipt), so only length and order-carrying tests do the work.

## Located quotes

Quotes are byte-exact from the round-40 captures (`corpus/evidence/round40/tb2-db-wal-recovery/`, identical to the
pinned raw files at `2fd12b88`), each 3-25 words, verified line by line with `sed -n '<n>p'` and by the gate's
`P4` clause. Straight double quotes inside a quote are the file's bytes.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the first test's whole assertion is existence | “assert os.path.exists("/app/recovered.json"), "recovered.json file does not exist"” | `test_outputs.py:9` |
| the second test's stated scope is JSON validity | “Test that the recovered.json file is valid JSON.” | `test_outputs.py:13` |
| the top-level shape demanded is a list | “assert isinstance(data, list), "JSON should be a list"” | `test_outputs.py:17` |
| required keys are the three field names | “required_fields = {"id", "name", "value"}” | `test_outputs.py:27` |
| the id type gate is the only one of its kind | “assert isinstance(item["id"], int), "id should be an integer"” | `test_outputs.py:33` |
| the record count is a literal eleven | “assert len(data) == 11, f"Expected 11 records, got {len(data)}"” | `test_outputs.py:53` |
| the id sequence is pinned to 1..11 | “assert ids == expected_ids, f"Expected ids {expected_ids}, got {ids}"” | `test_outputs.py:58` |
| id 1's value is a literal from the WAL | “assert id_to_item[1]["value"] == 150, "Apple should have updated value 150 from WAL"” | `test_outputs.py:64` |
| id 11's name is a literal from the WAL | “assert id_to_item[11]["name"] == "mango", "Record 11 should be 'mango' from WAL"” | `test_outputs.py:80` |
| the WAL test is a row-count floor over the export | “assert len(data) > 5, "Only base data recovered - WAL decryption failed"” | `test_outputs.py:98` |
| the initial state is described as a five-row view | “access the database, SQLite may only show the base data (5 records) instead” | `instruction.md:3` |
| requirement 1 is the repair the grader never reads | “Fix the WAL file so SQLite can read it” | `instruction.md:7` |
| requirement 2 is the all-rows extraction | “Extract ALL data from the database (including WAL changes)” | `instruction.md:8` |
| requirement 3 fixes the graded path and format | “Create a JSON file in /app/recovered.json” | `instruction.md:9` |
| the record format is shown by example, not specified | “[{"id": 1, "name": "item1", "value": X}, {"id": 2, "name": "item2", "value": Y}, ...]” | `instruction.md:12` |
| order and count are stated once as prose | “sorted by id. You should recover all 11 records total. You'll be tested on the specific” | `instruction.md:13` |

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the round-40
counter `V7` applies, computed over **all** violating cases. The frozen table carries six tags on four instruction
lines (`:7`, `:8`, `:9`, `:12`, `:13`); all six have at least one violating case. Three of the 28 receipt cases carry
no tag (`oracle-solve-sh`, `decrypt-then-extract`, `decrypt-checkpoint-truncate`). The wide tag is `fix-wal` (23
cases), then `extract-all` (15), `eleven-records` (10), `record-format` (8), `json-at-path` (5) and `sorted-by-id`
(1).

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:7` | `fix-wal` | partly | `literals-never-open-db`, `literals-names-1-2-wrong`, `base-only-ro`, `xor-wrong-key` |
| `instruction.md:8` | `extract-all` | partly | `literals-never-open-db`, `truth-value-id3-wrong`, `truth-bool-value-id5`, `truth-drop-id11` |
| `instruction.md:9` | `json-at-path` | enforced | `empty-app`, `decrypt-in-place-no-json`, `truth-trailing-garbage`, `truth-wrong-path` |
| `instruction.md:12` | `record-format` | partly | `truth-extra-field`, `truth-bool-value-id5`, `truth-wrapped-object`, `truth-ids-as-floats` |
| `instruction.md:13` | `sorted-by-id` | enforced | `truth-reversed-order` |
| `instruction.md:13` | `eleven-records` | enforced | `untouched`, `base-only-ro`, `empty-list`, `truth-drop-id11` |

Three lines are enforced and three are not. The per-line reading:

- **7 (fix the WAL).** `partly`: five violating cases are observed `pass` — `literals-never-open-db`,
  `literals-names-1-2-wrong` (hand-typed exports), `truth-extra-field`, `truth-value-id3-wrong`,
  `truth-bool-value-id5` — and eighteen are observed `fail`, all of them for export-content reasons. Nothing in
  the grader reads the log: `decrypt-in-place-no-json` fixes the WAL and scores `FFFFFFF`, `base-only-ro` leaves it
  encrypted and scores `PPPPFPF`. The label is `partly` because the frozen rule counts those passing violators,
  and the label is not evidence that the repair is checked at all: zero of the seven tests read `/app/main.db-wal`,
  every failing `fix-wal` case fails on another tag's grounds, and the passing repair routes (`oracle-solve-sh`,
  `decrypt-then-extract`, `decrypt-checkpoint-truncate`) end with a 0-byte WAL and the rows checkpointed into
  `main.db` — none ends with a repaired WAL file (`R40CritProbe` §2 D2/D3). Here the derived label and the headline
  ("the repair is never checked") disagree in wording; the headline is the measured statement.
- **8 (extract all data).** `partly`: four violating cases are observed `pass` — `literals-never-open-db`,
  `literals-names-1-2-wrong`, `truth-value-id3-wrong` and `truth-bool-value-id5`, all of which claim an export that
  was typed or lightly edited rather than extracted — and eleven are observed `fail` (`empty-list`,
  `truth-drop-id11`, the base-only row sets, and the hand-typed cases with a wrong name or a non-integer cell). The
  mechanism that makes both directions possible is the pin surface: nine values and two names are unconstrained, so
  "extracted" and "invented" are indistinguishable outside those 22 cells.
- **9 (create the JSON at the given path).** `enforced`: `empty-app`, `decrypt-in-place-no-json`,
  `truth-trailing-garbage` and `truth-wrong-path` all fail, and the path is asserted literally (`:9`); the trailing
  garbage case fails six of seven (`PFFFFFF`, a parsed-prefix-free `JSONDecodeError`), the wrong-path case all
  seven.
- **12 (the record format).** `partly`: `truth-extra-field` and `truth-bool-value-id5` pass — extra keys are free
  (`:30`) and `True` is an `int` (`:35`) — while `truth-wrapped-object` (`PFFFFFF`), `truth-ids-as-strings`
  (`PPFFFPP`), `truth-ids-as-floats` (`PPFPPPP`), `truth-value-string-id4` and `truth-name-null-id1` fail. The
  format is enforced against the example's three keys and their types, not against its text.
- **13 (sorted by id, eleven records).** Two tags, two `enforced` labels. `sorted-by-id` has one violating case and
  it fails (`truth-reversed-order`, `PPPFFPP`). `eleven-records` has ten violating cases and all ten fail
  (`empty-app`, `untouched`, `base-only-ro`, `plain-read-then-solve`, `xor-wrong-key`, `decrypt-in-place-no-json`,
  `truth-plus-duplicate-id11`, `truth-dup-id10-no-id11`, `empty-list`, `truth-drop-id11`).

### Contestable tags

The `violates=` tags are frozen with the predictions and are not edited; two are wide and one is narrow:

- **`fix-wal` → `decrypt-in-place-no-json`.** The case *does* fix the WAL, and still carries the tag, so the tag
  reads "the graded export does not evidence a fix" rather than "the WAL is still broken". Under the frozen rule
  the label is `partly` either way (four of the five passing violators are literal exports, not WAL states).
- **`extract-all` → `truth-*` cases.** Every case built from `mk.py`'s truth table is tagged as not extracting from
  the database. That is the probe's reading (the recipe never opens it), not a line of the grader; the entry uses it
  only to keep the two directions visible in the map.
- **`sorted-by-id` → `truth-reversed-order`.** One case carries the whole `enforced` label. It fails on two tests
  (`:44` and `:58`), so the label would survive either; no other case violates the tag.
- **The tag rule is content-based for `extract-all`.** The probe docstring states an end-state rule ("its end state
  does not do what the instruction asks"); for `fix-wal` the end state decides it, but for `extract-all` nothing in
  an end state distinguishes an extracted export from a typed one, so the operative rule is "the export's data are
  not the database's data" (`truth-extra-field` carries correct data and is not tagged `extract-all`;
  `truth-bool-value-id5` is). Tag policy is also uneven (`empty-app` omits `fix-wal`; `truth-trailing-garbage`
  carries `json-at-path` but not `record-format`). `R40CritProbe` §3 recomputed every label under each contestable
  edit: only two edits move a label (dropping `fix-wal` from its passing violators; dropping `record-format` from
  `truth-extra-field` and `truth-bool-value-id5`), and both would claim enforcement against a passing violating case.

## Findings, each tied to its receipt cases

1. **A do-nothing agent scores 0 of 7 (`untouched`, `FFFFFFF`; `empty-app`, `FFFFFFF`).** Unlike the
   repository-history grader of round 39 (whose untouched state passes 4 of 5), this grader's first function is a
   file-existence check (`:9`), so the task's initial state fails everything. The negative control `empty-app` is
   the same letters from an empty `/app`, and the receipt shows each function's exception class
   (`FileNotFoundError` on all seven).
2. **Hand-typed JSON passes 7 of 7 without opening the database (`literals-never-open-db`, `PPPPPPP`;
   `literals-names-1-2-wrong`, `PPPPPPP`).** The probe's `mk.py` writes the export from the probe's own `TRUTH`
   table (computed once from the two captured files and written into the probe), not from the database; the recipes
   never call `sqlite3`. `literals-never-open-db` is not a correct export: nine of its eleven values are `0`
   (`[150, 250, 0, …]`). The second case also gets both unpinned names wrong and loses nothing. Outside the frozen
   table, wave-1 critic `R40CritProbe` ran the exact `truth` export at `/app/recovered.json` (7 × P, both database
   files left byte-identical to the seeds) and the same export with `main.db` and `main.db-wal` deleted first
   (7 × P): neither file needs to exist (`.ufo/waves/round-40/build/R40CritProbe.md` §2 D4).
3. **Only 22 of 33 cells are pinned (`literals-names-1-2-wrong` `PPPPPPP`, `truth-value-id3-wrong` `PPPPPPP`,
   `truth-bool-value-id5` `PPPPPPP`).** `truth-value-id3-wrong` changes id 3's value from 300 to 301 and passes all
   seven; `truth-bool-value-id5` writes `true` for id 5 and passes, because `isinstance(True, int)` holds (`:35`) and
   the value is not compared. The nine values of ids 3-11 are free, and so are the names of ids 1-2.
4. **"Fix the WAL file" is graded only through the export (`decrypt-in-place-no-json`, `FFFFFFF`;
   `decrypt-then-extract`, `PPPPPPP`; `decrypt-checkpoint-truncate`, `PPPPPPP`).** A state that decrypts the log in
   place and writes no export fails all seven; two different correct repair routes pass only because they also write
   the export. No function in the file names `main.db` or `main.db-wal`.
5. **One plain read-write open destroys the log, and the task's own oracle then fails two tests
   (`plain-read-then-solve`, `PPPPFPF`; `base-only-ro`, `PPPPFPF`; `xor-wrong-key`, `PPPPFPF`).** All three end
   states produce the same five base rows and the same letters: tests 5 (completeness) and 7 (`test_wal_was_decrypted`)
   fail. In `plain-read-then-solve` the read-write `sqlite3` open deletes the 16,512-byte encrypted WAL; `solve.sh`'s
   read-only query then leaves a 0-byte `main.db-wal`, and its decryptor XORs 0 bytes (`R40CritProbe` §2 D6: the end
   state holds a 0-byte WAL, not no WAL). The destructive read is published in the oracle itself — `solve.sh:8`
   opens the database read-only "to avoid WAL interaction" — and by the benchmark's own repository (§Prior art,
   S121), so the trap is a property of the task's environment and recipe, not of the grader.
6. **A wrong decryption key is not diagnosed (`xor-wrong-key`, `PPPPFPF`).** XORing with 0x43 leaves the WAL header
   magic invalid (`367e0783`, neither `0x377f0682` nor `0x377f0683`), and the case's read-write extraction then
   discards the log: after the recipe no `/app/main.db-wal` exists. The case is therefore confounded — the five rows
   come from the key and from the destructive read together; `R40CritProbe` (§2 D5, not a frozen case) ran the same
   wrong key with a read-only extraction, which keeps the wrong-key WAL intact and still yields five rows. The grader
   has no "the WAL is still encrypted" signal; the only evidence it produces is the missing six rows, the same
   signal a deleted log gives (finding 5).
7. **The type gate splits id type from id value (`truth-ids-as-floats`, `PPFPPPP`; `truth-ids-as-strings`,
   `PPFFFPP`; `truth-value-float-id1`, `PPFPPPP`).** `1.0` fails only `test_recovered_data_structure` (`:33`) and
   passes sorted, completeness and uniqueness by numeric equality; `"1"` fails structure (`:33`), and also sorted and
   completeness because the lexicographic order of `"1"…"11"` is not `1..11`; `150.0` fails structure (`:35`). A
   `True` value passes (finding 3).
8. **Structural checks are strict where they exist and blind where they do not (`truth-wrapped-object`,
   `PFFFFFF`; `truth-trailing-garbage`, `PFFFFFF`; `truth-wrong-path`, `FFFFFFF`; `empty-list`, `PFPPFPF`;
   `truth-plus-duplicate-id11`, `PPPPFFP`; `truth-dup-id10-no-id11`, `PPPPFFP`).** Wrapping the list in
   `{"items": [...]}` passes existence and then raises `TypeError` in the sorted and uniqueness tests; trailing
   garbage raises `JSONDecodeError` in six functions; the wrong path fails all seven; `[]` passes three tests
   vacuously; a duplicated id 11 and an 11-record set ending in a second id 10 both fail completeness and
   uniqueness, which is the one place the id multiset is checked exactly.
9. **An extra key is free (`truth-extra-field`, `PPPPPPP`).** `required_fields.issubset(item.keys())` (`:30`)
   admits `{"id", "name", "value", "note"}`; the entry records the acceptance, not a format preference.

## Regrade (second grading of the same end state)

The harness imports the grader once and calls the seven functions twice in the same process on the same built
state (`plans/db_wal_probe.py` `HARNESS_PY`, `for tag in ("TEST", "REGRADE")`); the second pass is reported, never
used for the verdict: `regrade cases=28 differ=0`. Because every function only re-opens `/app/recovered.json`
(`:14`, `:23`, `:40`, `:49`, `:85`, `:94`) and reads no clock, environment or network, a second read of an unchanged
file cannot differ: the column is a determinism read of this probe, nearly tautological for this grader, and **not**
re-run stability (`R40CritProbe` §2 D1). It could only catch a writer left running inside the sandbox.

The stability question itself (`considerthese/2026-10-26.md` proposal 3) was measured separately by wave-1 seat
`R40RegradeSweep` (`.ufo/waves/round-40/build/R40RegradeSweep.md`): for the five earlier TB2 graders, one
oracle-equivalent and two failing end states each were built once in the lane's own probe sandboxes and graded twice
without rebuilding — 15 of 15 verdicts the same, but two of the five graders mutate the graded state while grading
(`configure-git-webserver` writes `git_test.exp` and `~/.ssh/config`; `git-leak-recovery` writes `.git/lost-found/`
entries on its failing states), invisibly to their own assertions. The `polyglot-c-py` second-grading failure
(`R39PlanNext.md` §4) remains the only verdict flip observed.

## What the probe does not show

- **The task image is never pulled; the host's tools stand in.** `Dockerfile:3` says `FROM ubuntu:24.04` and `:5-10`
  installs `python3`, `sqlite3` and `xxd` from apt; the probe uses host sqlite3 **3.54.0** (`sqlite3 --version`,
  2026-10-09 build), host python3 and host `xxd`. The image's own sqlite version was not fetched — no image pull, and
  `https://packages.ubuntu.com/noble/sqlite3` answered HTTP 500 on 2026-10-26 — so every version-specific behaviour
  of that build is untested here: in particular whether its sqlite deletes an undecryptable WAL on a read-write open
  with the same trigger as 3.54.0 (finding 5), and its WAL recovery arithmetic. The probe ran no case under the
  image's packages.
- **The setup runs unprivileged.** `Dockerfile:14-15` copies `main.db` and `main.db-wal.encrypted` as root and
  `Dockerfile:12` sets `WORKDIR /app`; the probe seeds `/app` as the probing user inside `bwrap`, so ownership,
  modes and the absence of the image's `python3-pip` differ. The task declares `docker_image =
  "alexgshaw/db-wal-recovery:20251031"` (`task.toml:29`) and `allow_internet = true` (`:34`); neither was exercised.
- **`tests/test.sh` was not executed.** The reward mapping is read (`test.sh:18-29`), not run: `uvx`, apt, the
  network install of uv 0.9.5 and `/logs/verifier/` are outside the sandbox; the probe calls the seven test
  functions itself. `observed_pass` means "pytest would exit 0", not "reward.txt was written".
- **Seven predictions are pilot copies and one rests on an ungraded measurement.** `untouched`, `oracle-solve-sh`,
  `base-only-ro`, `literals-never-open-db`, `literals-names-1-2-wrong`, `literals-id3-name-wrong` and
  `truth-value-float-id1` copy the round-39 planning seat's observations; `plain-read-then-solve`'s prediction
  copies that seat's measurement that a plain read destroys the WAL, and its grading had not been run before this
  probe's first run.
- **The oracle row is one execution, not a correctness claim.** `oracle-solve-sh` runs the captured `solve.sh` as a
  case recipe and passes 7 of 7; it says nothing about other states, about `tests/test.sh`, or about the image.
- **The 28 cases are the claim's whole surface.** They were fixed before the first recorded run. States outside
  them — a WAL in a different journal mode, `-wal`/`-shm` presence differences, a checkpointed-but-not-truncated
  log, a base database already carrying the WAL's rows, other XOR keys or a multi-byte key, extra tables, a
  `recovered.json` written by a symlink, a JSON file with duplicate keys, and every AI-agent trajectory — are not
  covered and are not claimed.
- **Not a statement about the task's validity, difficulty or solvability.** That is PROVINCE's question, not this
  lane's; `difficulty = "medium"` (`task.toml:15`) and the 45/240-minute time estimates are the authors' metadata,
  read only.

## Prior art

Opened 2026-10-26 by wave-1 scout `R40ScoutPriorArt` (captures and `SHA256SUMS` in
`.ufo/waves/round-40/build/R40ScoutPriorArt/`); the L1 re-opened the strongest one (S121) the same day.

- **The destructive-read trap is published, by the benchmark's own repository.** S121: Terminal-Bench 2.1 pull
  request #3 (opened 2026-05-21, open and unmerged at access) says, §Reasoning: “Opening the database with a normal
  read-write SQLite connection can truncate or remove that file before the agent has inspected it” — and moves the
  encrypted file off the live `-wal` name. It changes neither `instruction.md` nor `tests/`, so the grader findings
  above (1-4, 7-9) are untouched by it. A terminal-bench issue #2218 comment (2026-10-12) records a leaderboard run
  in which “The agent's own SQLite probe removed the task's WAL”; harbor issue #3607 (2026-10-10) records agents on
  this task searching the filesystem for an intact copy of the WAL. Finding 5 is therefore a probed instance of a
  published defect, not a discovery.
- **The mechanism, from SQLite's own documents.** `https://www.sqlite.org/wal.html` §4: “Usually, the WAL file is
  deleted automatically when the last connection to the database closes.” `fileformat2.html` §4.1 gives the two
  valid header magics; the XOR-0x42 file starts `753d44c0`. The chain “invalid magic → no valid frames → the closing
  connection deletes the file” is an inference across these pages and `src/wal.c`, observed in this probe, not
  stated in one sentence upstream — so no SOURCES row is taken for it.
- **The grader's permissiveness is not reported as a defect.** The one audit that touches it
  (`JonathanGabor/terminal-bench-2-audit` `audit.txt:782` @ `35f11039`: “Not all values are verified”) rates the suite
  strong and runs no case; no issue or PR in terminal-bench-2, terminal-bench-2-1, harbor or terminal-bench names
  the 22/33 pin surface, the hand-typed pass or the unchecked repair step (search commands in the seat report;
  a text search, not proof of absence).
- **TB2.1 carries the same task bytes.** `tests/test_outputs.py`, `instruction.md` and `environment/Dockerfile` on
  terminal-bench-2-1 `main` hash to the lane's pinned captures (`R40ScoutPriorArt` §3; `R40ScoutUpstream`: no drift
  at terminal-bench-2 `main` either).

The claim this entry makes stays the narrow one: **a probed instance of the TB2 `db-wal-recovery` grader** — 28
frozen states executed offline against these captures. It is not a first-instance claim for SQLite, WAL recovery or
export-based grading, not a novelty claim, and not a claim about how agents solve the task.

source-note: S121 https://github.com/harbor-framework/terminal-bench-2-1/pull/3 (tier B, cited by §Prior art only).

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated or too easy (no image run, no agent, no
trajectory); that reading only the export is the *wrong* assertion for this task (the authors' choice, described,
not judged); that any agent can or would reach a passing invented export in a real run — nothing here is a
gameability, solver-strategy or reward-hacking-in-the-wild claim; that the 0x42 key is the only key or that the
recovery route the oracle takes is the intended one; anything about how Harbor executes this verifier
(`benchmark-verifier-execution-model.md` covers where it runs and what it restores); or anything about the other 83
TB2 task graders at `2fd12b88`.

Nor: **contamination** — `test_outputs.py:1-2` carries the canary banner and this capture exists for
digest-pinned re-execution, not as a contamination measurement; **the image's sqlite** — host sqlite 3.54.0 is the
probe's instrument; **the oracle's correctness** — `solve.sh` runs as one case's recipe and passes, which says
nothing about other states; **the destructive-read trap's generality** — it is observed on this host's sqlite and
published in the oracle's own comment, and no other sqlite build was tested; **deployment or packaging guidance** —
the repair route is the maintainers' instruction, not a configuration this lane recommends.

**Falsifier.** This entry is falsified if (a) a re-fetch of the two pinned URLs yields bytes whose SHA-256 differs
from `corpus/evidence/round40/tb2-db-wal-recovery/SHA256SUMS`; (b) a fresh run of `plans/db_wal_probe.py --lane .`
prints anything other than `cases=28 observed_pass=8 observed_fail=20 mismatches=0` and
`regrade cases=28 differ=0` — in particular if any of `oracle-solve-sh`, `decrypt-then-extract`,
`decrypt-checkpoint-truncate`, `literals-never-open-db`, `literals-names-1-2-wrong`, `truth-extra-field`,
`truth-value-id3-wrong` or `truth-bool-value-id5` is observed `fail`, or if any of `untouched`, `empty-app`,
`base-only-ro`, `plain-read-then-solve`, `xor-wrong-key`, `decrypt-in-place-no-json`, `empty-list`,
`truth-drop-id11`, `truth-wrapped-object`, `truth-wrong-path`, `truth-trailing-garbage`, `truth-reversed-order`,
`truth-plus-duplicate-id11`, `truth-dup-id10-no-id11`, `truth-ids-as-strings`, `truth-ids-as-floats`,
`truth-value-float-id1`, `truth-name-null-id1`, `truth-value-string-id4` or `literals-id3-name-wrong` is observed
`pass`; (c) a line of `test_outputs.py` is shown to open `/app/main.db`, `/app/main.db-wal` or any file other than
`/app/recovered.json`, or to compare more than the 22 pinned cells of the export; or (d) the captured grader applied
to the `literals-never-open-db` state raises `AssertionError` in any of the seven functions, or the captured grader
applied to the `decrypt-in-place-no-json` state passes any function.

## Errata (round 40, wave 2)

Appended after the falsify wave (`.ufo/waves/round-40/falsify/F40CritOverclaim.md` F1-F14, `F40EntryQuotes.md` D1-D6);
the text above stands as written. Receipt, dry table, probe and requirement-map labels are unaffected (V7 re-derives every
label; `F40MapControl` 10/10 red controls).

- Summary, “`solve.sh` after one careless read-write `sqlite3` open scores 4 of 7”: it scores **5 of 7**
  (`plain-read-then-solve` `PPPPFPF`, completeness and the WAL test fail).
- Summary, “every one of them opens only `/app/recovered.json`”: six open it; `test_recovered_json_exists` only checks
  existence (`:9`). The same holds for the README index row and S119's teaches cell (“read only the exported JSON”).
- Source labels, “the probe executes it once”: `solve.sh` runs in **two** cases — `oracle-solve-sh` and
  `plain-read-then-solve` (`plans/db_wal_probe.py:172,177`); “runs as one case's recipe” in the limits sections means the
  oracle row only.
- Structural consequences and finding 8, “`[]` passes … three tests”: it passes **four** — existence, structure, sortedness
  and uniqueness (`PFPPFPF`) — so only the three length-carrying tests do the work.
- Requirement map, “six tags on four instruction lines”: **five** lines (`:7`, `:8`, `:9`, `:12`, `:13`).
- Line 7 paragraph, “eighteen are observed `fail`, all of them for export-content reasons”: seventeen fail on export content,
  `untouched` on a missing export.
- Line 9 paragraph: the `enforced` witnesses are five — add `untouched` (`FFFFFFF`).
- Line 12 paragraph: the failing `record-format` cases are six — add `truth-value-float-id1` (`PPFPPPP`).
- Contestable tags, “four of the five passing violators are literal exports”: **all five** are `mk.py` exports.
- Finding 1, “`FileNotFoundError` on all seven”: on six; the existence test fails its own `AssertionError`, which the harness
  prints as a bare `F`.
- Finding 5, “`solve.sh:8` opens the database read-only”: line 8 is the comment, line 10 the `mode=ro` query
  (`solve.sh:8-10`); the oracle records the hazard, it does not perform the destructive read.
- Finding 7, “`"1"` … fails sorted and completeness because the lexicographic order …”: only `sorted` (`:44`) fails by
  lexicographic order; completeness fails because string ids never equal the int sequence `1..11` (`:57-58`).
- Outside this file (same corrections, recorded here rather than rewritten in place): `PROVINCE.md` round-40 paragraph,
  “the repair step … is reachable only through that export” → is graded only through that export, and no export content
  evidences it; `corpus/README.md` index row, “a plain read-write open destroys the encrypted log” holds on the probe's host
  sqlite 3.54.0 (the image's build is untested; `R40CritSqlite` found an older Python-bundled SQLite behaves the same), and
  “a wrong XOR key leaves the five base rows” → a wrong XOR key followed by a read-write extraction; `SKILL.md`
  round-40 section, `json-at-path`'s witnesses are `receipt:6,7,14,26,27` (not `receipt:28`, `empty-list`), and `partly` on
  `fix-wal` is a co-tagging artefact — no test reads the WAL.
- §Prior art (`F40CritPriorArt` D1-D3, sources opened by that seat 2026-10-26, captures under
  `.ufo/waves/round-40/falsify/F40CritPriorArt/` with `SHA256SUMS`): the audit quote sits at
  `audit_results/20260120_125158/audit.txt:782-784`; “The one audit that touches it” → **two** public audits touch it (the
  second, `kimjune01/terminal-bench-audit` `results/verdicts-2.1.jsonl:91-95`, finds no task-specific defect); and the
  permissiveness is reported **in the wild** by `dzhioev/bro` issue #659 (2026-09-18, five trials): agents “invented the six
  missing rows” and “The verifier caught it only because the two updates in the lost WAL were unguessable” — i.e. the grade
  turned on ids 1-2's values, as finding 3 predicts. The narrowed negative: no opened source states the 22-of-33 count or
  executes a from-scratch export against the grader; the entry's findings are a probed, counted instance of a reported
  weakness, not a discovery.
