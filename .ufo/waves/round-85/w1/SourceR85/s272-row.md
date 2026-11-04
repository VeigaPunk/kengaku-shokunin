# SourceR85 — proposed `corpus/SOURCES.md` row S272 (sqlite-db-truncate pinned grader)

Seat `SourceR85`, kengaku round 85, wave 1, 2026-11-04. Drafted by the source seat; **not** applied to
`corpus/SOURCES.md` (production files are read-only to this seat; the L1 owns the landing).

## The proposed row (ONE row, 11 cells, copy-paste ready)

```
| S272 | Terminal-Bench 2.0 sqlite-db-truncate pinned grader — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py | code | A | member replay only: this pinned grader's acceptance predicate; not a solved-task or model claim | test_outputs.py:8-31; :31 quote `assert score > 6, "Did not load data correctly"` (9 whitespace-split words); accessed 2026-11-04; live 1097 B sha256 8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881 equals the round-52 capture | the grader loads /app/recover.json at :22, builds (word, value) sets from the hardcoded eight-row soln list at :8-17 and from the data at :24-25, and asserts the intersection exceeds six at :31, so scores 7 and 8 pass while 6 fails | mined | 2026-11-04 | 2027-01-18 | corpus/lessons/round-85.md |
```

## Cell-by-cell provenance

| cell | value | why |
|---|---|---|
| id | `S272` | the id the frozen claim names (`plans/round-85-claims.md` §R85-C1 "Sourced claim") |
| source | title + the pinned raw URL | the one URL this seat fetched (HTTP 200) |
| kind | `code` | the subject is source code (the enum in SOURCES contract v1 §Shape) |
| tier | `A` | primary and authoritative for its scope: the upstream source at a pinned revision |
| scope | `member replay only: this pinned grader's acceptance predicate; not a solved-task or model claim` | the claim's own wording; the row supports member replay only |
| anchor | `test_outputs.py:8-31; :31 quote …` + access date + live bytes + sha256 | the located quote, its line, the access date, and the byte digest |
| teaches | one grounded benefit | what the grader's bytes actually say, with its own line numbers |
| status | `mined` | cited by `corpus/lessons/round-85.md` in `used-by` |
| opened | `2026-11-04` | the date this seat opened the source |
| recheck | `2027-01-18` | ISO date, matching the recheck cadence the sibling pinned-grader rows S261–S271 carry for the same pin |
| used-by | `corpus/lessons/round-85.md` | the round-85 lesson that admits it |

## The quote, its line, and its word count

Quote (verbatim from the fetched bytes, which are byte-identical to the committed capture):

```
assert score > 6, "Did not load data correctly"
```

- **Located at line 31** of `test_outputs.py` (1-based, `str.splitlines()`); line 30 is the blank
  line before it.
- **Word count: 9**, counted as `len(quote.split())` — the same counter
  `plans/sources_adopt.py` `words()` and `plans/round30_defects.py` `words()` use, i.e. the
  `wc -w` convention. The nine tokens are
  `['assert', 'score', '>', '6,', '"Did', 'not', 'load', 'data', 'correctly"']`.
- The quote is **9 words**, comfortably inside the ≤25-word cap of SOURCES contract v1 rule 1 and
  QUALITY Q3.
- The quote is a byte-exact substring of the capture line 31 (`q in lines[n-1]`).

## Schema conformance (checked mechanically)

- Exactly 11 cells; 12 `|` separators; **no literal `|` and no escaped `\|` inside any cell**
  (`plans/sources_adopt.py` `split_cells()` refuses both).
- `status` ∈ {queued, mined, rejected}; `recheck` matches `^\d{4}-\d{2}-\d{2}$`.
- `kind` ∈ the contract enum; `tier` = A with `kind` = code (not `community`, so no tier inflation).
- `used-by` path `corpus/lessons/round-85.md` exists on disk in the lane (census E11 clean).
- The row sits inside the `## Registry` section (census E12 clean).

Gate runs (all in scratch, lane read-only):

| gate | result |
|---|---|
| `plans/sources_adopt.py --quote-file … --artifact <capture> --url-map …` | `QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 mismatch=0 unmapped=0` → exit 0 |
| `plans/sources_adopt.py --registry <base> --package <row> --admit-ids S272 --access-date 2026-11-04 --recheck 2027-01-18 --entries corpus/lessons/round-85.md` | `registry=263 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0` → exit 0 |
| `scripts/sources-census.sh validate --file <registry with this row>` | no E-code attributable to this row; the E-code set is byte-identical to the same run on the registry without it |
| `plans/anchor_line_check.py --lane <fixture with this row>` | `ANCHORLINE rows=1 cited=1 captured=1 defective=0 live=0 cells=0` → exit 0 |

## Fetch and comparison receipts

- Fetch: `curl` against the pinned raw URL, written only under this seat's scratch →
  **HTTP 200**, **1097 bytes**, sha256
  `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`.
- Comparison against `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`:
  `cmp` exit 0 → **byte-identical**; the capture is git-tracked and is listed in
  `corpus/evidence/round52/graders/SHA256SUMS` with the same digest.
- The live digest therefore equals the frozen claim's subject pin
  (`plans/round-85-claims.md` §R85-C1) and the committed receipt's `SUBJECT_SHA`
  (`corpus/evidence/round85/sqlite-db-truncate-probe.txt`).

Full command transcript: `receipts.txt` in this directory.

## Note for the L1 — the row already landed in this round differs from this draft

A row with this id was already committed to `corpus/SOURCES.md` at `e7b44805` (round-85 lesson
commit), and `corpus/lessons/round-85.md` carries a matching Gate row. That landed row states
`:30` and `(6 whitespace-split words)`. The bytes say **line 31** and **9 whitespace-split words**
(`len(quote.split()) == 9`); line 30 is blank. Under the SOURCES contract v1 rule 2 (append-only;
a correction is a new superseding row) this is corrected by a new row whose `teaches` opens
`supersedes S272 —`, not by editing the landed row. This seat does not touch production files; the
correction is reported to the L1 and recorded in `findings.md`.
