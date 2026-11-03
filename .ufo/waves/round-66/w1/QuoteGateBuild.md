# QuoteGateBuild — kengaku round-66 wave 1 (v1), seat findings

Date: 2026-11-03. Scope: build the frontier mistake-fix counter and draft the two superseding
registry rows, proposed files only. Nothing landed in `plans/` or `corpus/SOURCES.md`; no
tracked lane file was modified. Seat dir `W/QuoteGateBuild/` holds every proposed file and
receipt; the full transcript is `W/QuoteGateBuild/report.md`. Scratch
`/fast/scratch/hyaku/kengaku-r66/QuoteGateBuild/` (selftest fixtures and live-check lessons) was
removed before yield. Tooling: nothing installed or upgraded (stdlib-only counter, host
`/usr/bin/python3` 3.14.8).

`<C>` = `W/QuoteGateBuild/proposed/round66_registry_check.py` (14260 bytes, sha256
`982b235d38af62b0f5428b646d653e53671f25db76d5f605ff8e9c958b66e914`).
`<L>` = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Check 1 — counter selftest, 13 fixtures — PASS

Command: `python3 <C> --selftest --work <S>/work` → exit 0.
Observed: `SELFTEST {...}` with all 13 keys `True`: passing and failing cases for `quote` and
`meta`, both refusal paths (outside-evidence, absolute), no-Gate, empty-Gate, header-less
teaches fallback, bad row shape, missing selected id. Fixtures were created under the scratch
dir and removed in `finally`. Receipt: `green/selftest.txt`.

## Check 2 — red-before: `meta` on the current S233/S234 rows — PASS (refused)

Command: `python3 <C> meta W/QuoteGateBuild/red/rows-current.md` → exit 1.
Observed: `CHECK defect: meta S234 phrase='word bar' ...`, `... 'teaches is one benefit' ...`,
`... 'same source and capture' ...`; `CHECK meta rows=2 findings=3 teaches_column=6`.
The rows were extracted read-only from `corpus/SOURCES.md` with
`grep -E '^\|[[:space:]]*S(233|234)[[:space:]]*\|'` into `red/rows-current.md`. Receipt:
`red/red-output.txt`.

## Check 3 — red-before: `quote` on the S233 composite quote — PASS (refused)

Command: `python3 <C> quote W/QuoteGateBuild/red/red-lesson.md --root <L>` → exit 1.
Observed: `CHECK defect: quote S233 miss capture=corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt needle='sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h'`;
independent `grep -c -F` of the same needle in the capture → `0`, exit 1. The composite quote is
a summary of four listing lines, not a listing line. Receipt: `red/red-output.txt`.

## Check 4 — green: `meta` on the proposed S236/S237 rows — PASS

Command: `python3 <C> meta W/QuoteGateBuild/proposed/rows.md` → exit 0.
Observed: `CHECK meta rows=2 findings=0 teaches_column=6`, `CHECK ok meta`. With explicit ids
(`meta ... S236 S237`) the same exit 0. Receipt: `green/green-output.txt`.

## Check 5 — green: `quote` on the two verbatim lines — PASS

Command: `python3 <C> quote W/QuoteGateBuild/green/green-lesson.md --root <L>` → exit 0.
Observed:
`QUOTE S236 capture=corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt result=FOUND needle='sqlite-amalgamation-3540100/sqlite3.c'`
and `QUOTE S237 ... kv-store-grpc-test_outputs.py result=FOUND needle='assert result == 0, f"Port {port} is not listening - no real gRPC server is running"'`;
`CHECK quote quotes=2 misses=0`, `CHECK ok quote`. Receipt: `green/green-output.txt`.

## Check 6 — 11-column shape — PASS

Command: `awk -F'|' '{printf "line %d NF=%d\n", NR, NF}' W/QuoteGateBuild/proposed/rows.md` and
`awk -F'|' 'NF!=13 {...}' ...` → `line 1..4 NF=13`; `ALL LINES 11-COLUMN (NF=13)`;
`rows_with_NF_13=4` (header, separator, S236, S237). No cell contains `|`. Receipt:
`green/columns.txt`.

## Check 7 — live registry calibration — PASS

Command: `python3 <C> meta <L>/corpus/SOURCES.md` (default: all rows) → exit 1.
Observed: `CHECK meta rows=227 findings=3 teaches_column=6`; the only findings are S234's three
frozen phrases at line 250. This proves the header-derived teaches index on the real table, that
all 227 rows parse as 11 cells, and that no other row trips a frozen phrase. Receipt:
`red/live-checks.txt`.

## Check 8 — live refusals and SETUP — PASS

- `quote` with capture `corpus/SOURCES.md` → `refused capture outside corpus/evidence/`, exit 1.
- `quote` with a missing capture → `miss ... (capture file missing)`, exit 1.
- no subcommand → usage + `SETUP subcommand required`, exit 2.
- `--selftest` without `--work` → `SETUP --work required`, exit 2.
Receipt: `red/live-checks.txt`.

## Rows (proposed, verbatim)

```
| S236 | SQLite amalgamation 3.54.1, sqlite.org download page — https://sqlite.org/2026/sqlite-amalgamation-3540100.zip (supersedes S233 anchor form) | code | A | offline instrument builds for db-state graders (R65-C1): the compile-input bytes the probe pins | corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt line 5: sqlite-amalgamation-3540100/sqlite3.c (9582521 bytes); zip sha256 0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9, 2990966 bytes | the amalgamation ships sqlite3.c at 9582521 bytes, the compile input a local gcov-instrumented sqlite3 build uses | mined | 2026-11-03 | 180d | corpus/lessons/round-66.md |
| S237 | Terminal-Bench 2.0 kv-store-grpc grader, tests/test_outputs.py at pin 2fd12b88 (supersedes S234 teaches form) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py | code | A | network-service grader offline execution (R64-C1): the grader's leg order and its handshake tolerance as the file states them | corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py:96 verbatim: assert result == 0, f"Port {port} is not listening - no real gRPC server is running"; seven legs in file order at :15-138; tolerance at :128 | seven legs execute in file order; the handshake accepts only grpc.RpcError as proof of a real gRPC server | mined | 2026-11-03 | 180d | corpus/lessons/round-66.md |
```

teaches word counts: S236 16, S237 18 (limit 25; `green/wordcounts.txt`). `rows.md` sha256
`ccb7245be377112280808fb75d2eb0d715b9f31c88cfb87c5f4f21b5a535eb9c`.

## Findings and limits (reported, no rule edited)

1. **`CORPUS.md` is absent at the lane root** and is not in `git ls-files`; the seat spec's
   path for the SOURCES contract is stale. Rows were drafted against the live 11-column header
   (`corpus/SOURCES.md:21`) and the existing contract-v1 rows.
2. **"Column 6, counting the leading empty cell"**: with the leading empty cell dropped, the
   teaches cell is index 6 of the 11 real cells (0-based) — the 7th column; the counter prints
   `teaches_column=6` and prefers the header. In the raw `split('|')` that keeps the empty cell
   it is index 7; same cell.
3. **Quote check is substring-only**: it does not enforce the ≤25-word limit, does not bind the
   quote to the anchor line the row names, and does not cross-check that the QUOTE id's row
   cites that capture. A quote present anywhere in the capture passes. This is the specified
   check; the C1 probe's per-case junit binding remains the stronger gate.
4. **Meta check is phrase-based**: a reworded meta cell evades the three frozen phrases.
5. **`used-by` target `corpus/lessons/round-66.md` does not exist yet**; the rows must not land
   before the lesson cites them (CORPUS rule 4), and the lesson's `## Gate` must carry the
   S236/S237 QUOTE lines.
6. **Round-65's lesson Gate has no QUOTE lines** (the format is new this round), so the
   counter's fail-closed rule would flag it; the format applies to the round-66 lesson.
7. **Nothing landed**: S233/S234 remain in the registry; S236/S237 are new ids (no collision;
   `grep -cE '^\|[[:space:]]*S(235|236|237)[[:space:]]*\|'` → 0). From `plans/` the counter
   needs no `--root`; until then `quote` requires `--root <L>`.
