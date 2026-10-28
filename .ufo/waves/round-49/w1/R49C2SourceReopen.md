# R49C2SourceReopen — reviewer report (round 49, wave 1)

Seat: R49C2SourceReopen (reviewer), serving R49-C2 (coverage). Judged on: coverage.
Item: re-open S166 (pinned `tests/test_outputs.py`) this round and verify the cited predicate against the
committed capture; record URL, access date, <=25-word located quote.

## Axes

Coverage (primary) — whether S166's claimed evidence still grounds the C2 package's fixed-point case table at
the frozen pin. Calibration secondary: the pinned digest must still bind the committed capture byte-for-byte.

## Freeze precondition (verified before any fetch)

- Stage-1 freeze `9d2900af41e4d1fc6022eff99010436fde6dbd93` exists in the lane
  (`git -C <lane> cat-file -t` → `commit`) and predates the measurement:
  committer time `2026-10-28T09:14:40-03:00`; this seat's clock at measurement `2026-10-28T12:20:46Z`
  (= 09:20:46 -03:00) and at report write ~09:2x -03:00 — all measurements post-date the freeze.
- Work was done read-only in a `--shared --no-checkout` clone at the frozen base:
  `/fast/scratch/hyaku/kengaku-r49/R49C2SourceReopen/lane`, `rev-parse --show-toplevel` confirmed,
  `HEAD == 9d2900af41e4d1fc6022eff99010436fde6dbd93`. No scored counter/probe run was executed by this seat
  (item is a source re-open only); no lane file was written outside this report.

## S166 locator (from committed `corpus/SOURCES.md:181`, tree `9d2900af`)

- URL: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`
- Pinned sha256: `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`
  (also line 8 of `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS`)
- Cited predicates in the SOURCES row: `:18` `assert polyglot_files == ["main.py.c"], (` ; `:27`
  `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` ; `:44`
  `assert python_out == expected and c_out == expected, (` — plus the description "an exact directory
  listing, one gcc compile, then python3 and C stdout equality on three fixed sizes".

## Commands run (verbatim) and observed output

In `/fast/scratch/hyaku/kengaku-r49/R49C2SourceReopen` with `TMPDIR` exported there:

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
→ 9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims

git clone --shared --no-checkout <lane> lane && git -C lane checkout -q 9d2900af...
→ rev-parse --show-toplevel: /fast/scratch/hyaku/kengaku-r49/R49C2SourceReopen/lane ; HEAD: 9d2900af41e4d1fc6022eff99010436fde6dbd93

(cd lane/corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)
→ gitignore: OK / README.md: OK / Dockerfile: OK / instruction.md: OK / solve.sh: OK / task.toml: OK / test.sh: OK / test_outputs.py: OK   (8/8 OK)

sha256sum lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
→ b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec

curl -fsSL --retry 2 -o s166_live_test_outputs.py <URL>
→ fetched 1564 bytes ; access at 2026-10-28T12:20:46Z

sha256sum s166_live_test_outputs.py
→ b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec

cmp s166_live_test_outputs.py lane/.../test_outputs.py
→ BYTE-EQUAL (cmp silent, exit 0)

sed -n '18p;27p;44p' s166_live_test_outputs.py
→     assert polyglot_files == ["main.py.c"], (
    test_cases = [(42, "267914296"), (10, "55"), (0, "0")]
        assert python_out == expected and c_out == expected, (
```

REV of measured tree: `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` (committed clone; no uncommitted bytes —
no `TREE-BYTES` needed). The fetched live bytes are external evidence, not lane content.

## Re-open result

- **Re-fetch at the pinned URL today** (access date 2026-10-28, 12:20:46Z) yields 1564 bytes,
  sha256 `b94a7a98…ddec` — **byte-equal** to the committed capture at the frozen base, matching the claims
  file's expectation (`plans/round-49-claims.md:143`: "reopened … sha256 `b94a7a98…`, byte-equal to the
  committed capture"). No capture drift; the falsifier (a) in the grader entry is NOT triggered.
- **Cited predicate verified verbatim against committed capture:** all three quotes in the S166 row appear
  byte-exact at their cited lines (18, 27, 44) of the committed `test_outputs.py` (46 lines total,
  `test_outputs.py:1-46` as cited). The description clause also holds: `os.listdir("/app/polyglot")` at :17
  precedes the `gcc … -o /app/polyglot/cmain` compile at :23-25, and the only comparisons are
  `stdout.strip()` equalities to the three fixed literals at :44.

## Source record (required fields)

- URL: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`
- Access date: 2026-10-28 (re-fetch 12:20:46Z)
- Located quote (≤25 words, `test_outputs.py:27`, 8 words): **“test_cases = [(42, "267914296"), (10, "55"), (0, "0")]”**

## Limits

- Single-seat re-open of S166 only; S167–S172 were not re-fetched by this seat (not in item scope).
- The fixed points are literals in the public test file; this re-open confirms the pin and predicates, not
  grader soundness (already covered by the grader entry's limits/errata).
- No scored counter/probe run executed — none required for this item; no admission claimed for R49-C1/R49-C2.
- Scratch tree `/fast/scratch/hyaku/kengaku-r49/R49C2SourceReopen` removed after this report was written
  (clone + fetched bytes deleted; only this report persists).

## VERDICT

S166 re-opened 2026-10-28: pinned URL live, bytes byte-equal to committed capture (sha256 `b94a7a98…`),
cited predicates verbatim at :18/:27/:44 — VERIFIED, supports the C2 sourced basis; no drift.
