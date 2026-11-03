# QuoteGateBuild — proposed registry quote/meta counter and the S236/S237 rows (round 66, w1)

Date: 2026-11-03. Seat: executor, kengaku round-66 wave 1. Scope: **proposed files only** —
nothing was landed in `plans/` or `corpus/SOURCES.md`; no tracked lane file was modified.
Scratch `/fast/scratch/hyaku/kengaku-r66/QuoteGateBuild/` was removed before yield.
Tooling: nothing installed or upgraded; the counter is stdlib-only and ran on the host
`/usr/bin/python3` (3.14.8).

## Files written

- `proposed/round66_registry_check.py` — 14260 bytes, mode 755,
  sha256 `982b235d38af62b0f5428b646d653e53671f25db76d5f605ff8e9c958b66e914`
- `proposed/rows.md` — 1597 bytes, sha256 `ccb7245be377112280808fb75d2eb0d715b9f31c88cfb87c5f4f21b5a535eb9c`
- `red/rows-current.md` — the current S233 and S234 rows, extracted read-only from
  `corpus/SOURCES.md` with `grep -E '^\|[[:space:]]*S(233|234)[[:space:]]*\|'`
- `red/red-lesson.md` — synthetic lesson whose Gate carries the S233 composite quote
- `red/red-output.txt` — red-before commands, output and exit codes
- `red/live-checks.txt` — live negative checks against the real lane root, plus SETUP checks
- `green/green-lesson.md` — synthetic lesson with the two verbatim QUOTE lines
- `green/green-output.txt` — green commands, output and exit codes
- `green/columns.txt` — the `awk -F'|' NF==13` shape check
- `green/selftest.txt` — the 13-fixture selftest after the last code change
- `green/wordcounts.txt` — teaches word counts (16 and 18, limit 25) and file hashes

## Counter contract

`quote <lesson.md>` — reads the lesson's `## Gate` section (to the next level-1/2 heading) and
takes every line `QUOTE S### | <capture> | <verbatim text>`. The capture path is resolved
against the lane root and must stay inside `<root>/corpus/evidence/`; an absolute path or one
that resolves outside is refused, not read. The text must occur literally in the capture's
bytes (`needle.encode() in bytes`, the exact `grep -F` semantics). Every miss, malformed line,
empty text, missing capture or refused path prints `CHECK defect: quote <id> ...` and the run
exits 1. Fail-closed: a lesson with no `## Gate`, or a Gate with no QUOTE lines, is a finding
(no vacuous pass).

`meta <SOURCES.md> [ids ...]` — for every selected `S###` row (default: all), the `teaches`
cell must not contain `word bar`, `teaches is one benefit`, or `same source and capture`
(case-insensitive). The cell is located by the table header when a header row is present, else
at index 6 of the 11 real cells (0-based, leading empty cell dropped) — the 7th column, the
cell between `anchor` and `status`; the run prints `teaches_column=6`. A selected id that is
absent, a row with other than 11 cells, or a registry with no rows is a finding. Findings print
`CHECK defect: meta <id> phrase='...' ...` and exit 1.

`--selftest --work <dir>` — 13 fixtures under the scratch dir: a passing and a failing case for
each check, both refusal paths (outside-evidence and absolute), no-Gate, empty-Gate, header-less
fallback, bad row shape, and a missing selected id. Exits 0 only if all 13 assert true.

Root resolution: `--root`, else `$KENGAKU_ROOT`, else the script's parent directory (so the
counter needs no argument once it lives in `plans/`). Only `quote` requires a root with
`corpus/evidence/`; otherwise it is SETUP, exit 2. `meta` reads only the file it is given.

## Red-before (exit 1 required, observed)

Transcript: `red/red-output.txt`.

| command | exit | observed |
|---|---|---|
| `python3 <C> meta red/rows-current.md` | 1 | `CHECK defect: meta S234 phrase='word bar' ...`, `... 'teaches is one benefit' ...`, `... 'same source and capture' ...`; `CHECK meta rows=2 findings=3 teaches_column=6` |
| `python3 <C> quote red/red-lesson.md --root <L>` | 1 | `CHECK defect: quote S233 miss capture=corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt needle='sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h'` |
| `grep -c -F 'sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h' <capture>` | 1 | `0` — the composite quote is not a substring of the listing |

(`<C>` = the proposed counter; `<L>` = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.)

## Green (exit 0 required, observed)

Transcript: `green/green-output.txt`.

| command | exit | observed |
|---|---|---|
| `python3 <C> meta proposed/rows.md` | 0 | `CHECK meta rows=2 findings=0 teaches_column=6`, `CHECK ok meta` |
| `python3 <C> quote green/green-lesson.md --root <L>` | 0 | `QUOTE S236 ... result=FOUND`, `QUOTE S237 ... result=FOUND`, `CHECK quote quotes=2 misses=0`, `CHECK ok quote` |
| `python3 <C> meta proposed/rows.md S236 S237` | 0 | `CHECK meta rows=2 findings=0`, `CHECK ok meta` |
| `python3 <C> --selftest --work <S>/work` | 0 | `SELFTEST {...}` all 13 keys `True` (`green/selftest.txt`) |

## 11-column shape

Transcript: `green/columns.txt`.

`awk -F'|' '{printf "line %d NF=%d\n", NR, NF}' proposed/rows.md` → lines 1–4 all `NF=13`.
`awk -F'|' 'NF!=13 {...}' proposed/rows.md` → `ALL LINES 11-COLUMN (NF=13)`.
`rows_with_NF_13=4` (header, separator, S236, S237). No cell contains a `|`.

## The two rows verbatim (`proposed/rows.md`)

```
| S236 | SQLite amalgamation 3.54.1, sqlite.org download page — https://sqlite.org/2026/sqlite-amalgamation-3540100.zip (supersedes S233 anchor form) | code | A | offline instrument builds for db-state graders (R65-C1): the compile-input bytes the probe pins | corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt line 5: sqlite-amalgamation-3540100/sqlite3.c (9582521 bytes); zip sha256 0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9, 2990966 bytes | the amalgamation ships sqlite3.c at 9582521 bytes, the compile input a local gcov-instrumented sqlite3 build uses | mined | 2026-11-03 | 180d | corpus/lessons/round-66.md |
| S237 | Terminal-Bench 2.0 kv-store-grpc grader, tests/test_outputs.py at pin 2fd12b88 (supersedes S234 teaches form) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py | code | A | network-service grader offline execution (R64-C1): the grader's leg order and its handshake tolerance as the file states them | corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py:96 verbatim: assert result == 0, f"Port {port} is not listening - no real gRPC server is running"; seven legs in file order at :15-138; tolerance at :128 | seven legs execute in file order; the handshake accepts only grpc.RpcError as proof of a real gRPC server | mined | 2026-11-03 | 180d | corpus/lessons/round-66.md |
```

teaches word counts (whitespace tokens, limit 25): S236 16, S237 18 (`green/wordcounts.txt`).

## Live checks on the real lane root (`red/live-checks.txt`)

- `meta corpus/SOURCES.md` (default: all rows) → exit 1, `rows=227 findings=3`, and the only
  findings are S234's three phrases at line 250. This exercises the header-derived teaches
  index on the real table and shows all 227 rows have 11 cells (otherwise shape findings would
  appear), and that no other row trips a frozen phrase.
- A lesson quoting `corpus/SOURCES.md` → `CHECK defect: quote S990 refused capture outside
  corpus/evidence/`, exit 1.
- A lesson quoting a missing capture → `miss ... (capture file missing)`, exit 1.
- No subcommand → usage + `SETUP subcommand required`, exit 2; `--selftest` without `--work`
  → `SETUP --work required`, exit 2.

## Findings and limits (reported, not edited into any rule)

1. **`CORPUS.md` does not exist at the lane root** (and is not in `git ls-files`). The seat spec
   cites it for the SOURCES contract. The rows were drafted against the live registry header
   (`corpus/SOURCES.md:21`) and the existing contract-v1 rows, which are 11-column. This is a
   stale path in the spec, not a registry defect.
2. **"Column 6, counting the leading empty cell."** With the leading empty cell dropped, the
   teaches cell is index 6 of the 11 real cells (0-based) — the 7th column. The counter prints
   `teaches_column=6`, derives the index from the header when present, and falls back to 6. (In
   the raw `split('|')` that keeps the empty cell it is index 7; same cell.)
3. **Quote check is substring-only.** It does not enforce the ≤25-word limit, does not check
   that the quote sits at the anchor line the row names, and does not cross-check that the
   `QUOTE` id's registry row cites that capture. A quote that occurs anywhere in the capture
   passes. This is the specified check; the stronger binding remains the C1 probe's per-case
   junit binding.
4. **Meta check is phrase-based.** A reworded meta teaches cell ("one benefit inside the
   twenty-five-word limit") evades it. The three phrases are frozen; adding more is a rule
   change, not a seat edit.
5. **`used-by` target does not exist yet.** `corpus/lessons/round-66.md` is written later in
   this round. The rows must not land before the lesson cites them (CORPUS rule 4); the lesson
   must carry QUOTE lines for S236 and S237 in its `## Gate`.
6. **The round-65 lesson's Gate has no `QUOTE` lines** (it predates the format), so the counter's
   fail-closed rule would flag it. The format applies to the round-66 lesson.
7. **The rows are proposed only.** S233 and S234 remain in `corpus/SOURCES.md`; S236/S237 are
   new ids (no collision: `grep -cE '^\|[[:space:]]*S(235|236|237)[[:space:]]*\|'` → 0).
