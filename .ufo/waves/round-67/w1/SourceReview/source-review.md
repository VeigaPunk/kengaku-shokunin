# Round 67 w1 — SourceReview: second-seat re-read of S238 and S239

Seat: SourceReview (leaf member, read-only on L; network used only for the two pinned URLs).
Date of re-read: 2026-11-03. Lane root: /home/vgpnk/Projects/shokunin/kengaku-shokunin.

## Verdicts (one per row)

| row | verdict | defect |
|---|---|---|
| S238 | **pass** | none. Fetch HTTP 200; sha256 matches SHA256SUMS line 169 and the capture; all quotes and line citations resolve (see table below). Tightness note only: the AFAB quote is cited as range `:154-157`; the string itself sits on `:157` (the range contains it, so it passes). |
| S239 | **pass** | none. Fetch HTTP 200; sha256 equals `989bfcf0c54baf6c8cdc391743dbb2f9e858c5779dd85112536875d4d1b2dcd2`; both quotes resolve at the cited lines. |

## Step 1 — registry rows (`grep -n '^| S23[89]' corpus/SOURCES.md`, rows read raw at 253-254)

Both rows have 11 cells, matching the 11-column header at `corpus/SOURCES.md:21` (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`). Status `mined` is one of the table's existing values (210 rows `mined`, 8 `queued`, 13 `rejected`). `opened` is `2026-11-03` (well-formed, matches the claims doc F1). `recheck` is `180d`, a value used by 159 rows. `used-by` is `plans/round-67-claims.md` on both rows.

## Step 2 — pinned URL re-fetch and hashes

Command (run in scratch `/fast/scratch/hyaku/kengaku-r67/SourceReview`):
```
curl -s -m 30 -o grader.py -w 'S238 http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/tests/test_outputs.py
curl -s -m 30 -o instruction.md -w 'S239 http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/instruction.md
sha256sum grader.py instruction.md
```
Output:
```
S238 http=200 bytes=6065 url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/tests/test_outputs.py
S239 http=200 bytes=1885 url=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-pipeline-parallelism/instruction.md
23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f  grader.py
989bfcf0c54baf6c8cdc391743dbb2f9e858c5779dd85112536875d4d1b2dcd2  instruction.md
```

Comparison against the pinned values:
```
sed -n '169p' corpus/evidence/round52/graders/SHA256SUMS
23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f  ./torch-pipeline-parallelism/tests/test_outputs.py
```
- Grader fetched sha256 = SHA256SUMS line 169 sha256 → **match**.
- Instruction fetched sha256 = `989bfcf0…d2` → **match**.
- Capture sha256 (`corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py`) = `23574246…64f`; capture sha256 (`…-instruction.md`) = `989bfcf0…d2`.
- `cmp grader.py <capture>` → identical (`GRADER_IDENTICAL`); `cmp instruction.md <capture>` → identical (`INSTR_IDENTICAL`).

Fetched bodies copied into this seat dir as receipts: `fetched-test_outputs.py`, `fetched-instruction.md`.

## Step 3 — quotes and line citations

Command: `grep -nF '<quote>' <capture>` and `sed -n` on the cited lines.

| row | claim | command | result | verdict |
|---|---|---|---|---|
| S238 | `AFAB violation: found forward after backward at {key}` in range `:154-157` | `grep -nF 'AFAB violation: found forward after backward at {key}' …test_outputs.py` | `157:                f"AFAB violation: found forward after backward at {key}"` rc=0 | match (line 157 ∈ 154-157) |
| S238 | `def test_no_hooks_in_pipeline_parallel` at `:31` | `grep -n 'def test_no_hooks_in_pipeline_parallel' …` | `31:def test_no_hooks_in_pipeline_parallel():` rc=0 | match |
| S238 | `exists` at `:19` | `grep -n 'def test_' …` | `19:def test_pipeline_parallel_exists():` | match |
| S238 | parametrised world sizes `:171-172` | `sed -n '171,172p' …` | `@pytest.mark.parametrize("world_size", [1, 2])` / `def test_pipeline_parallel(world_size):` | match |
| S239 | `Run forward passes for all microbatches first, then run backward passes.` at `:18` | `grep -nF '…' instruction.md` | `18:Run forward passes for all microbatches first, then run backward passes. ` rc=0 | match |
| S239 | `You must not use hooks inside your implementation.` at `:31` | `grep -nF '…' instruction.md` | `31:This comparison is done using hooks inside the test. You must not use hooks inside your implementation.` rc=0 | match (substring of line 31) |

Each quote matches verbatim and each cited line contains it.

## Step 4 — word counts (≤ 25 words each)

Command: `printf '%s' '<quote>' | wc -w`
- S238 AFAB quote: 8 words.
- S239 `Run forward passes…`: 11 words.
- S239 `You must not use hooks…`: 8 words.
All ≤ 25 → pass.

Status and recheck cells: S238 and S239 both `mined` / `2026-11-03` / `180d` / `plans/round-67-claims.md`, all well-formed against the schema.

## Notes (no defect)

- S238 anchor cites the AFAB quote as a range `:154-157` marked "verbatim". The quoted string is on `:157`. A tighter cite (`:157`) would be preferred but is not a defect; the range contains the line.
- The S238 "teaches" cell says the AFAB and hook rules are "dictionary-order and literal checks". This matches the capture: the AFAB check at `:152-157` compares `.fwd`/`.bwd` key order, and `no_hooks` is a literal check. Not re-derived here beyond the quotes.
- Nothing in L was written by this seat; no git command was run.

## Commands run (exit codes as observed)

1. `cat plans/round-67-claims.md` — rc 0 (output truncated by tool at predicate line; the claims-doc frozen text was otherwise read).
2. `grep -n '^| S23[89]' corpus/SOURCES.md` — rc 0.
3. `mkdir -p` seat and scratch dirs — rc 0.
4. `_read corpus/SOURCES.md:253-254:raw` — rows read raw.
5. `curl … tests/test_outputs.py` and `curl … instruction.md` — HTTP 200 both; `sha256sum` — rc 0.
6. `sed -n '169p' corpus/evidence/round52/graders/SHA256SUMS` — rc 0.
7. `sha256sum` on the two capture files — rc 0.
8. `cmp` grader and instruction vs captures — rc 0 both.
9. `grep -nF` quotes in the captures — rc 0 for all four quote greps; `grep -n 'def test_'`, `sed -n` on cited ranges — rc 0.
10. `wc -w` on quotes — rc 0.
11. `awk`/`grep` on the table for cell counts, status, recheck, opened — rc 0.
