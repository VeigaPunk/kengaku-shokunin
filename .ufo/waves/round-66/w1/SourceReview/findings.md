# SourceReview — kengaku round-66 wave 1 (v1), seat findings

Date: 2026-11-03. Scope: independent re-open of the sources this round rests on. Read-only
in the lane except this seat dir and the seat report `.ufo/waves/round-66/w1/SourceReview.md`.
Scratch: `/fast/scratch/hyaku/kengaku-r66/SourceReview/` (deleted before yield; the zip went
with it). Raw check output copied to `W/SourceReview/quote-check.out` (bytes observed).
Tooling: nothing installed or upgraded.

## Check 1 — torch-tensor-parallelism grader at the pin (item 1) — PASS

Command:
`curl -sSfL -w 'HTTP-CODE %{http_code}\n' 'https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-tensor-parallelism/tests/test_outputs.py' -o "$S/torch-test_outputs.py" && sha256sum "$S/torch-test_outputs.py" && cmp "$S/torch-test_outputs.py" L/corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py && echo CMP-TORCH-IDENTICAL`

Observed: `HTTP-CODE 200`; sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`;
`CMP-TORCH-IDENTICAL` (cmp exit 0 — byte-identical to the committed capture).

Verdict: live bytes at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` equal the capture; sha
equals the F1 sha, the S183 row sha, and the C1 predicate's grader sha.

## Check 2 — kv-store-grpc grader at the pin (item 2) — PASS

Command: same shape as check 1 with `kv-store-grpc/tests/test_outputs.py` and capture
`L/corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py`.

Observed: `HTTP-CODE 200`; sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e`;
`CMP-KV-IDENTICAL` (cmp exit 0).

Verdict: identical to capture; sha equals the F1 S234 sha.

## Check 3 — SQLite amalgamation zip (item 3) — PASS

Command:
`curl -sSfL -w 'HTTP-CODE %{http_code}\n' 'https://sqlite.org/2026/sqlite-amalgamation-3540100.zip' -o "$S/sqlite-amalgamation-3540100.zip" && sha256sum ... && stat -c 'SIZE %s' ...`

Observed: `HTTP-CODE 200`; sha256 `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`
(matches the expected value exactly); `SIZE 2990966` (matches F1's 2990966 bytes).

Listing comparison — exactly what was compared: both `unzip -l` outputs (fresh run and committed
capture `sqlite-amalgamation-3540100.unzip-l.txt`) were reduced by removing (a) line 1, the
`Archive:` line (it embeds the fetching scratch path, `/fast/scratch/hyaku/…` in the capture vs
`/fast/scratch/hyaku/kengaku-r66/SourceReview/…` fresh), and (b) the trailing 2-line
timestamp-free summary (`---------                     -------` / ` 11588420                     5 files`).
Remaining 7 lines compared with `cmp`: the `Length Date Time Name` header, its dashes row, and the
5 entry lines (dir entry + sqlite3.c 9582521 + shell.c 1270623 + sqlite3.h 695729 + sqlite3ext.h
39547, all timestamped `2026-10-16 12:19` on both sides).

Command: `unzip -l "$S/sqlite-amalgamation-3540100.zip" > fresh.txt && tail -n +2 fresh.txt | head -n -2 > fresh-core.txt && tail -n +2 CAPTURE | head -n -2 > capture-core.txt && cmp fresh-core.txt capture-core.txt && echo UNZIP-L-CORE-IDENTICAL`

Observed: `UNZIP-L-CORE-IDENTICAL` (cmp exit 0).

## Check 4 — frozen located quotes (item 4) — PASS (3/3)

Method: quotes were extracted byte-for-byte from `plans/round-66-claims.md` (4th backtick field of
each quote bullet via `awk -F'`'`), not retyped; then `grep -F -c` in the named capture and
`printf '%s' | wc -w` for the word count. Exit codes recorded per check. Raw transcript:
`W/SourceReview/quote-check.out`.

| Quote source | Named capture | `grep -F -c` count | grep exit | words (≤25) | Verdict |
|---|---|---|---|---|---|
| S183 | `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py` | 1 | 0 | 7 | PASS |
| S233 | `corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt` | 1 | 0 | 1 | PASS |
| S234 | `corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py` | 1 | 0 | 16 | PASS |

Exact quote tokens grepped (as extracted from the claims file):
- S183: `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"`
- S233: `sqlite-amalgamation-3540100/sqlite3.c`
- S234: `assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`

Note on S233: the bullet renders `sqlite-amalgamation-3540100/sqlite3.c` (9582521 bytes); the
backticked token is the quote, `(9582521 bytes)` is annotation outside the backticks. The value
9582521 does appear verbatim in the compared listing line, so the annotation is also grounded.
Word-count convention: whitespace-split tokens (`wc -w`).

## Check 5 — S183 registry row vs capture sha (item 5) — PASS

Command: `grep -n 'S183' L/corpus/SOURCES.md; sha256sum L/corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py`

Observed: `corpus/SOURCES.md` line 198 (S183 row) records
`… git blob 6ac3c4b177ff89cebd868b3fba3a4700b960ca2b, 7171 bytes, sha256 4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290 …`;
`sha256sum` of the capture prints the identical value `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`.

Verdict: row sha256 == capture sha == live fetch sha. (Row status/used-by lifecycle — `queued`→`mined` — is the registry seat's scope; not judged here.)

## Disagreements / findings

None. All five checks pass: the live sources at the frozen pins match the committed captures byte
for byte, every frozen quote is verbatim-present in its named capture with word count ≤ 25, and
the S183 row's sha agrees with the capture and the live fetch. No rule, predicate, quote, or sha
in the frozen claims file disagrees with observed evidence.

## Residual risk / scope notes

- The capture's `Archive:` line carries the pre-freeze fetch path; excluded from comparison per
  item spec, no bearing on listing content.
- Check 4 verifies the three quote bullets only; the F1 prose claims (HTTP 200, byte sizes) were
  independently re-observed in checks 1–3 and agree.
- Scratch `/fast/scratch/hyaku/kengaku-r66/SourceReview/` (downloads, listing cores, quote script
  and output) was removed before yield; the raw check output was copied to
  `W/SourceReview/quote-check.out` first.
