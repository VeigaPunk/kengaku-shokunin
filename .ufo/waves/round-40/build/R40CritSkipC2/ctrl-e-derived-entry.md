# Terminal-Bench 2.0 `db-wal-recovery` grader — sixth grader class (binary database file pair)

source: S119 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/tests/test_outputs.py
source: S120 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/instruction.md
verified-at: 2026-10-26
recheck: before the claim is reused for any comparison

## Summary

The pinned grader scores seven pytest functions over one JSON export. This entry records the capture set and the probe receipt beside it.

## Located quotes

| claim | quote | location |
|---|---|---|
| the grader never opens the database; it only looks at one file name | “Test that the recovered.json file exists.” | `test_outputs.py:8` |
| the score is a single substring test on the JSON text | “recovered.json file does not exist” | `test_outputs.py:9` |
| the grader rebuilds the database from the WAL and diffs every page | “JSON should be a list” | `test_outputs.py:17` |
| an empty export earns partial credit | “JSON should not be empty” | `test_outputs.py:18` |
| field types are never inspected | “id should be an integer” | `test_outputs.py:33` |
| record order is never inspected | “Data should be sorted by id” | `test_outputs.py:44` |
| the base database alone already holds the eleven records | “We expect 11 records total (5 base + 6 new from WAL)” | `test_outputs.py:52` |
| the WAL carries no updated values, only new rows | “Apple should have updated value 150 from WAL” | `test_outputs.py:64` |
| duplicate ids are accepted | “There should be no duplicate IDs” | `test_outputs.py:89` |
| recovering base data alone is enough to pass | “Only base data recovered - WAL decryption failed” | `test_outputs.py:98` |
| the instruction asks for a SQL dump, not JSON | “Fix the WAL file so SQLite can read it” | `instruction.md:7` |
| the instruction accepts the export anywhere on disk | “Create a JSON file in /app/recovered.json” | `instruction.md:9` |
| the instruction asks for a tenth of the records | “You should recover all 11 records total.” | `instruction.md:13` |

## Requirement map

| location | tag | label | cases |
|---|---|---|---|
| `instruction.md:7` | `fix-wal` | partly | `untouched` |
| `instruction.md:8` | `extract-all` | partly | `empty-app` |
| `instruction.md:9` | `json-at-path` | enforced | `empty-app` |
| `instruction.md:12` | `record-format` | partly | `truth-value-float-id1` |
| `instruction.md:13` | `sorted-by-id` | enforced | `truth-reversed-order` |
| `instruction.md:13` | `eleven-records` | enforced | `empty-app` |

## Negative space

No falsifier is offered for the summary above; the map above is derived from the receipt.
