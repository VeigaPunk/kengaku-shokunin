# R48C2SourceReopen — S166 re-open (R48-C2 sourced basis)

seat: R48C2SourceReopen (reviewer, leaf — no subagent dispatch)
lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin
axes named: coverage (R48-C2); calibration not touched. C1/C2 admission not claimed.

## Item

Re-open S166 (pinned `tests/test_outputs.py`) this round and verify the cited predicate
against the committed capture; record URL, access date, <=25-word located quote.

## Freeze verification (pre-measurement gate)

- Stage-1 freeze commit: `a543d92083557dd9b33ee674e9b99b03411f80af` (2026-10-27T06:53:29-03:00,
  "round-48: stage-1 freeze of C1 ... and C2 ... claims"). Frozen base per seat spec = this commit.
- `git ls-tree HEAD plans/round-48-claims.md` at that commit → blob present;
  `git log -1 --format='%H %cI %s' -- plans/round-48-claims.md` → the file's introducing commit is
  a543d920 itself. The C2 "Sourced basis (§2b)" line (S166 re-open with URL/access date/quote)
  is present in the committed file at the frozen base.
- Freeze predates measurement: freeze commit 2026-10-27T06:53:29-03:00; my live fetch at
  2026-10-27T11:33:27Z (14:33 -03:00) is strictly later.
- No scored counter/probe execution was made or attempted (this item is a source re-open only);
  no C2 ordering constraint is implicated. Read-only against a scratch clone of the frozen base;
  no production file, claim, counter, or control was edited.

## Commands run (exact)

```
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2SourceReopen
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q a543d92083557dd9b33ee674e9b99b03411f80af   # rev-parse --show-toplevel == $D verified
git -C lane ls-tree HEAD plans/round-48-claims.md
git -C lane log -1 --format='%H %cI %s' -- plans/round-48-claims.md
grep -n 'assert polyglot_files == \["main.py.c"\]' lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
grep -n 'test_cases = \[(42' lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
grep -n 'assert python_out == expected and c_out == expected' lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
wc -l lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
sha256sum lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
grep test_outputs lane/corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS
curl -fsSL -o live_test_outputs.py "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py"
sha256sum live_test_outputs.py lane/.../test_outputs.py && cmp live_test_outputs.py lane/.../test_outputs.py
```

## Observed outputs (verbatim evidence)

- REV a543d92083557dd9b33ee674e9b99b03411f80af (clone HEAD; freeze commit 2026-10-27T06:53:29-03:00)
- `sha256sum` committed capture: `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py`
- `SHA256SUMS` row: `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  test_outputs.py`
- live fetch: same sha256; `cmp` → `BYTES-IDENTICAL`
- located quotes present in committed capture at cited lines:
  - `18:    assert polyglot_files == ["main.py.c"], (`
  - `27:    test_cases = [(42, "267914296"), (10, "55"), (0, "0")]`
  - `44:        assert python_out == expected and c_out == expected, (`
  - `46 lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` (range :1-46 exact)
- S166 row (corpus/SOURCES.md @ frozen base) cites pin 2fd12b88..., range 1-46, the three quotes
  at :18/:27/:44, and sha256 b94a7a98... — all confirmed against committed bytes.
- Grader entry `corpus/knowledge/tb2-polyglot-c-py-grader.md` registry map quotes at lines
  17/18/24/27/31/36/44 also verified present in the capture.

## Source record (per claims §2b / seat item)

- URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py
- Access date: 2026-10-27 (fetch 2026-10-27T11:33:27Z; freeze commit 06:53:29-03:00 same day, earlier)
- Located quote (<=25 words), `test_outputs.py:27` at the pin:
  "test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]" (8 words)
- Secondary located quote, `test_outputs.py:44`:
  "assert python_out == expected and c_out == expected, (" (9 words)

## Predicate verification result

The cited predicate holds against the committed capture:
1. Exact-directory precondition — capture lines 17-20 assert `os.listdir("/app/polyglot") == ["main.py.c"]` before any build.
2. Two toolchains on one file — gcc build of `/app/polyglot/main.py.c` (lines 22-24) and python3 execution of the same path (lines 28-35), plus the built C binary (lines 37-43).
3. Three fixed points — line 27 literals `[(42, "267914296"), (10, "55"), (0, "0")]`.
4. Dual-equality scoring assert — line 44.
Committed capture, SHA256SUMS entry, S166 cited sha256, and the reopened live source are all byte-identical at the pinned commit.

## Limits

- Live source reached from this host via curl; no fetch-side content negotiation (raw URL returns the blob as stored). Reproducibility anchor is the pin + sha256, not the network.
- Scope limited to the S166 re-open item; no C2 counter/probe run, no stage-2 input pins inspected beyond what the freeze file names.
- Round-46 spotcheck (`corpus/lessons/round-46-verifier-spotcheck.md`) reopened the same source on 2026-10-27 with the same quote at line 27; this seat independently re-verifies byte-identity rather than reusing that receipt.

## VERDICT

S166 REOPEN PASS — predicate verified against committed capture at REV a543d92083557dd9b33ee674e9b99b03411f80af; live pinned source byte-identical (sha256 b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec); URL/access date/located quotes recorded. No defect found; no freeze predicate, control, or kill rule altered.
