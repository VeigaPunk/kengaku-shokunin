## Database-recovery TB2 grader — round 40

Before citing the pinned TB2 `db-wal-recovery` scorer, run `python3 plans/db_wal_probe.py --lane .` and read its
summary line: exit `0` means only that all 28 cases produced seven test verdicts twice each, exit `2` a setup
failure (a capture not at its pinned digest, `/usr/bin/bwrap` not executable, a `--work` directory that cannot be
created, a case that did not yield seven verdicts twice, or a recipe that exited non-zero — a recipe error is never
a verdict) (`plans/db_wal_probe.py:1-20,314-364`). `--dry` prints the frozen case table with no sandbox and
`--stage-check` builds each case's end state and prints only stage exit codes, the grader never imported
(`plans/db_wal_probe.py:3-10`), so neither is evidence. The receipt's summary
(`corpus/evidence/round40/db-wal-probe.txt:35`) reads `cases=28 observed_pass=8 observed_fail=20 mismatches=0`,
and its second grading of the same, un-rebuilt end states agrees case by case (`regrade cases=28 differ=0`, `:34`).
The class differs from rounds 35–39: the graded state is one JSON export at `/app/recovered.json` whose source of
truth is a binary database file pair — `main.db` plus an XOR-encrypted `main.db-wal` — and the whole score is seven
pytest functions over that export (`corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py:7-107`); the probe
seeds `/app` as the task Dockerfile does (`Dockerfile:14-15`), runs a frozen recipe under `bash -euo pipefail`,
then imports the captured module and calls the seven functions in file order inside a per-case bubblewrap sandbox
(`plans/db_wal_probe.py:10-20`), so `tests/test.sh`'s `uvx`/pytest path and its `/logs/verifier/reward.txt` write
(`test.sh:18-29`) are read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `os.path.exists("/app/recovered.json")` and nothing else (`test_outputs.py:7-9`) | any file at that path, including one that is not JSON: `truth-trailing-garbage` passes test 1 and fails the other six (`PFFFFFF`) | parse the file before crediting it; test 1 is a path test, not a recovery test | `truth-trailing-garbage` (receipt:26) |
| `json.load` of the whole file plus `isinstance(data, list)` and `len(data) > 0` (`:12-18`) | a list of any content — `empty-list` clears tests 1, 3, 4 and 6 (`PFPPFPF`) | that "valid JSON" means one parse of one file; a JSON object raises `TypeError` in tests 4 and 6 instead of asserting (`truth-wrapped-object`, `PFFFFFF`) | `empty-list` (receipt:28), `truth-wrapped-object` (receipt:23) |
| `required_fields.issubset(item.keys())` over `{"id","name","value"}` (`:27-32`) | extra keys are free: `truth-extra-field` adds a `note` to every record and passes 7/7 | the exact key set, when the instruction's `[{"id":…,"name":…,"value":…}]` line is meant as the format | `truth-extra-field` (receipt:22) |
| `isinstance(item["id"], int)`, `["value"], int`, `["name"], str` (`:33-35`) | `True` passes as an int (`truth-bool-value-id5`, 7/7); floats fail only here (`truth-value-float-id1` and `truth-ids-as-floats` are `PPFPPPP`, because `1.0 == 1` still clears tests 4-6) | `type(x) is int` and `not isinstance(x, bool)` if the export must be machine-readable, not merely JSON-shaped | `truth-bool-value-id5` (receipt:31), `truth-value-float-id1` (receipt:18), `truth-ids-as-floats` (receipt:25) |
| `ids == sorted(ids)` (`:43-44`) | monotone ids of any length and with duplicates: `empty-list` passes it (`PFPPFPF`), as do `truth-plus-duplicate-id11` and `truth-dup-id10-no-id11` (`PPPPFFP`) | set equality against `1..11`; sortedness is neither completeness nor uniqueness | `truth-reversed-order` (receipt:19), `truth-plus-duplicate-id11` (receipt:20) |
| `len(data) == 11` then `ids == list(range(1, 12))` (`:53-58`) | eleven ids in order, and nothing about where they came from: `literals-never-open-db` types them by hand and is 7/7 | open the database yourself; an eleven-id list is not evidence of a WAL read | `literals-never-open-db` (receipt:15), `truth-drop-id11` (receipt:29), `empty-list` (receipt:28) |
| `len(ids) == len(set(ids))` (`:83-89`) | nothing extra — it cannot fail alone, since both duplicate states already fail the count and id-equality assertions (`PPPPFFP`) | that this assertion is redundant: "no duplicate ids" is enforced only through test 5's count and id list | `truth-plus-duplicate-id11` (receipt:20), `truth-dup-id10-no-id11` (receipt:21) |
| `id_to_item[1]["value"] == 150` and `id_to_item[2]["value"] == 250` (`:64-67`) | 2 of the 33 id/name/value cells: values of ids 3-11 are never read — `truth-value-id3-wrong` writes `301` for id 3 and passes 7/7 | compare the whole exported table with the decrypted rows, not the two cells the grader sampled | `truth-value-id3-wrong` (receipt:30), `literals-never-open-db` (receipt:15) |
| `id_to_item[3..11]["name"] == cherry…mango` (`:70-80`) | 9 more of those cells: names of ids 1-2 are never read (`literals-names-1-2-wrong`, 7/7) while id 3's name is (`literals-id3-name-wrong`, `PPPPFPP`) | the whole name column; the gate is asymmetric between ids 1-2 and 3-11 | `literals-names-1-2-wrong` (receipt:16), `literals-id3-name-wrong` (receipt:17) |
| `test_wal_was_decrypted`: `len(data) > 5`, then two `if`-guarded re-reads of id 1's value and id 6's name (`:92-107`) | a state that never touched `/app/main.db-wal` — `literals-never-open-db` passes it — and `truth-ids-as-strings` passes it on an export whose keys are strings, because `1 in id_to_item` is false (`PPFFFPP`) | stat, `xxd -l 32` and read-only-open the WAL and the database; the test named for decryption reads only the export and skips when a key is missing | `literals-never-open-db` (receipt:15), `truth-ids-as-strings` (receipt:24), `decrypt-in-place-no-json` (receipt:14) |
| nothing — the WAL and the database themselves | the inverse of a green: a genuinely repaired WAL with no export is `FFFFFFF` (`decrypt-in-place-no-json`) | that the graded artefact is the export alone, so "Fix the WAL file so SQLite can read it" (`instruction.md:7`) has no assertion behind it | `decrypt-in-place-no-json` (receipt:14) |
| nothing — a wrong-key XOR over the WAL (key 0x43 instead of 0x42) | the 5 base rows: `xor-wrong-key` is `PPPPFPF`, failing only completeness and the WAL test — 5 of 7 assertions are satisfied by an untouched database | check the WAL magic (`37 7f 06 82`) yourself; those two failures are the only signal that the WAL was ignored | `xor-wrong-key` (receipt:11), `base-only-ro` (receipt:9) |
| nothing — a plain read-write open before the repair | the same shape: `plain-read-then-solve` is `PPPPFPF`, because the first open deleted the undecryptable WAL and the task's own `solve.sh` then had nothing to decrypt | back the WAL up before any open and read via `file:…?mode=ro` (the oracle's own comment, `solve.sh:8-10`); the destructive first read is invisible to every assertion | `plain-read-then-solve` (receipt:10) |
| nothing — do-nothing baselines and the task's own oracle | `empty-app` and `untouched` are both `FFFFFFF` (the image ships no `recovered.json`), `oracle-solve-sh` is 7/7, and `decrypt-then-extract` and `decrypt-checkpoint-truncate` are both 7/7 | run all five first: unlike round 39's grader this one starts at 0 of 7, and it cannot tell a WAL-applied read from a checkpointed-truncated one | `empty-app` (receipt:6), `untouched` (receipt:7), `oracle-solve-sh` (receipt:8), `decrypt-then-extract` (receipt:12), `decrypt-checkpoint-truncate` (receipt:13) |

What a green means here: in the probe's staged state, `/app/recovered.json` parsed as a list of eleven dicts with
integer `id`/`value` and string `name`, ids `1..11` in order, id 1's value `150`, id 2's value `250`, and the names
`cherry…mango` for ids 3-11 — on states the probe built, not states an agent built. What it does not mean: that the
WAL was repaired (a hand-typed export scores 7/7, `receipt:15`), that the database was read at all, that the values
of ids 3-11 or the names of ids 1-2 are the ones in the database (`receipt:16,30`), that values are integers rather
than booleans (`receipt:31`), that the record has no extra fields (`receipt:22`), or that an agent's first open did
not destroy the WAL it was asked to fix (`receipt:10`).

Of the six frozen instruction tags (`plans/db_wal_probe.py` `TAGS`; frozen lines in
`corpus/evidence/round40/db-wal-dry-cases-freeze.txt:1-6`), the round-40 counter's V7 rule
(`plans/round40_c2_verify.py:209-214`; label = the observed verdicts of every receipt case whose `violates=` carries
the tag) gives: `fix-wal` (`instruction.md:7`) `partly` — 23 cases, 5 observed pass; `extract-all` (`:8`) `partly` —
15 cases, 4 observed pass; `json-at-path` (`:9`) `enforced` — 5 cases, 0 observed pass; `record-format` (`:12`)
`partly` — 8 cases, 2 observed pass; `sorted-by-id` (`:13`) `enforced` — 1 case, 0 observed pass; `eleven-records`
(`:13`) `enforced` — 10 cases, 0 observed pass. `enforced` here is a property of the frozen case set only: one of
`eleven-records`' ten witnesses is the empty-`/app` baseline (`receipt:6`) and two are the untouched and base-only
states (`receipt:7,9`), so the label means "every frozen case that violates it is observed fail", not "no
improving agent can violate it". `sorted-by-id` rests on a single witness (`truth-reversed-order`, `receipt:19`),
and `json-at-path` on five that include the empty-list and non-JSON states (`receipt:28,26`). The entry's
`## Requirement map` carries one row per tag in the counter's row shape, and V7 re-derives all six labels from the
receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:29` names
`alexgshaw/db-wal-recovery:20251031`; `allow_internet = true` at `:34`; `Dockerfile:3` builds it on `ubuntu:24.04`)
or a harness, and `tests/test.sh`'s `uvx`/pytest path and its `/logs/verifier/reward.txt` write (`test.sh:18-29`)
are read, not run. Host sqlite3 3.54.0, python3 and xxd stand in for the image's Ubuntu 24.04 packages, recipes run
as the probing user rather than root, and each case stages its own `/app`, so no case observes the image's tree. The
ground-truth table the recipes copy (eleven rows, values `100*id` except id 1 → `150` and id 2 → `250`) is computed
from the two captured files under XOR key `0x42`, not from the grader (`plans/db_wal_probe.py:25-29`). The
destructive-read behaviour is published in the oracle's own comment (`solve.sh:8`), so the cases that depend on it
probe an already-documented property.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, not a statement about SQLite's WAL semantics or about any agent's behaviour.
