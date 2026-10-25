# R33FGateAnchorProse — unquoted anchor prose beyond checked spans

Seat: R33FGateAnchorProse (executor, leaf). Date: 2026-10-25. Lane: kengaku-shokunin.
Target: `plans/sources_adopt.py` anchor span parsing and quote validation
(`quoted_spans` at :289-301, `quote_check` at :442-558, `ANCHOR_COLUMN=5` at :276,
`QUOTE_SPAN_RE = re.compile(r'"([^"]+)"')` at :277).
Claim under test: build-wave report `.ufo/waves/round-33/build/R33C1KillRule.md` row 14 —
"Quote spans counted from the whole cell — only `"…"` spans are measured; unquoted anchor
prose is never checked against the capture" (UNCAUGHT, severity low).

## Method (all in /tmp; lane read-only)

- Sandbox `/tmp/r33-anchorprose`: copied `plans/sources_adopt.py`, the committed captures
  dir (`.ufo/waves/round-33/assimilation/captures/`, 5 UTF-8 files) and the committed
  `url-map.json`. No lane file was edited, committed, or staged; no tools installed.
- Baseline fixture: the landed S103/S104 rows extracted read-only from
  `corpus/SOURCES.md` (lines 118-119) into a quote file with the gate's own `HEADER`.
  Baseline gate run (CLI): `python3 sources_adopt.py --quote-file landed-rows.md
  --artifact captures --url-map url-map.json` → exit 0,
  `QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25 ...
  mismatch=0 unmapped=0 urlmap=url-map.json entries=3` — byte-identical to the committed
  receipt `assimilation/gate-receipts.txt:4`.
- Mutations: each variant rebuilds the S103 row with the **same 11 cells**, replacing only
  unquoted bytes of the anchor cell (quoting `"…"` spans kept byte-for-byte identical,
  asserted in-process). Rows were re-parsed and read back to prove the mutated anchor is
  what `quote_check` actually sees. Both in-process `quote_check` and the real CLI
  subprocess were exercised.

## Results

### Prose-only mutations (quoted spans untouched): gate result unchanged

| # | Mutation (unquoted anchor prose only) | Exit | stdout | report dict |
|---|---|---|---|---|
| M1 | every claimed line label retargeted: `main.py:58`→`main.py:1`, `:279`→`:9999`, `:280`→`:1`, `:218`→`:7`, `:234`→`:99999` | 0 | byte-identical | identical |
| M2 | anchor names a different captured file: `tasks/finalpool/ab-testing/evaluation/main.py:58` → `utils/evaluation/retry.py:58` | 0 | byte-identical | identical |
| M3 | prose asserts the *negation* of every captured fact ("signature default is 0.5; call site passes no tolerance; log check returns False; nothing is compared against expected_ratio.csv") | 0 | byte-identical | identical |
| M4 | 400 unquoted words absent from every capture prepended before the spans (cap is 25) | 0 | byte-identical | identical |
| M5 | per-span `(N words)` labels rewritten to false counts (`(11 words)`→`(200 words)`, etc.) | 0 | byte-identical | identical |
| M6 | claimed source commit SHA `9be8d8fe…` → `deadbeefdeadbeef…` | 0 | byte-identical | identical |
| M7 | `scope` cell (col 4) rewritten to a false claim | 0 | byte-identical | identical |
| M8 | `teaches` cell (col 6) rewritten to a false claim | 0 | byte-identical | identical |
| M9 | `source` cell title text (col 1) rewritten, URLs kept identical | 0 | byte-identical | identical |

CLI subprocess confirmation: baseline, M1, M3 all exit 0 and their stdout is **byte-identical**
(shared SHA-256 `8c159ccb6448626e…`). Readback confirmed each fixture file re-parses to
exactly 1 row, 0 malformed, and the anchor cell equals the mutated string with the same 5 spans.

### Exact boundary: when prose *is* read (structural characters only)

| Probe | change | Exit | reason |
|---|---|---|---|
| B1 | prose gains a balanced pair `"permissive"` (not in capture) | 7 | new span `permissive` absent → `absent=1` |
| B2 | prose gains one stray `"` | 4 | `unbalanced-quote` |
| B3 | prose gains a `|` | 4 | `columns=12` (row dropped) |
| B4 | prose gains `\|` | 4 | `escaped-pipe` |
| B5 | control: a *quoted* byte mutated (`tolerance_pct: float = 0.1` → `0.2` inside a span) | 7 | span absent → `absent=1`, `found=4` |

So prose is invisible only up to three structural characters: double-quote balance, `|`
separators, and escaped pipes. Any `"` pair in prose becomes a checked span; any stray `"`
or `|` turns the row malformed. Nothing else about prose is ever inspected.

### Coverage of the anchor cell (why this matters)

Landed rows, measured: S103 anchor cell = 513 bytes, quoted = 349, **unexamined = 164
(32.0%)**; S104 anchor cell = 426 bytes, quoted = 295, **unexamined = 131 (30.8%)**;
combined 31.4% of anchor bytes are never checked. The unexamined bytes carry exactly the
line labels (`:58`, `:279`, `:280`, `:218`, `:234`, `:41`, `:124`, `:131`), the file/commit
identity, and the `(N words)` annotations that anchor the entry to the source.

## Evidence retained

- `/tmp/r33-anchorprose/experiment.py`, `experiment.out` — full in-process matrix,
  exit codes, stdout equality, report-dict equality, coverage numbers, span-location lists.
- `/tmp/r33-anchorprose/qf-*.md` — each fixture; `landed-rows.md` baseline.
- `/tmp/r33-anchorprose/cli-{baseline,M1-line-labels-wrong,M3-opposite-claims}.{out,err}`
  — CLI subprocess runs, exit codes, SHA-256 of stdout.
- Source read: `quote_check` consumes only `row.cell(ANCHOR_COLUMN)` (plus
  `row.cell(SOURCE_COLUMN)` in `bind_failure`); no line label, section, file name, commit
  SHA, or word-count annotation in prose is ever compared to the artifact bytes.

## Verdict

**UNCAUGHT — claim substantiated by materialization.** Changing unquoted anchor
statements/line labels while leaving quoted spans intact does not change the quote gate
result: all six prose mutations exit 0 with byte-identical stdout and an identical report
dict, including a 400-word unquoted insertion (the 25-word cap is per *span*), a full
negation of the captured facts, and a wrong file/commit/line attribution. The gate's only
span-reading surface is `QUOTE_SPAN_RE`; the attack's only constraints are avoiding a stray
`"` or `|` in prose (B1-B4). This matches the kill-rule row 14 description exactly, and it
extends to `scope`/`teaches`/`source` prose (M7-M9), which the quote gate ignores entirely.
Severity judgment (low) is the build report's; the behavioral claim is confirmed.

## Riskl/notes

- No gate code was modified; all mutations live in /tmp fixtures. No lane file was touched;
  the only lane path written is this report.
- Not in scope: quote-in-wrong-section detection (row 1 of the kill-rule table, sibling
  seat), no-map vs url-map binding modes (sibling seat), receipt-vs-landed-bytes identity
  (row 3).
- No tools installed; used the system Python 3, cp, diff, sha256sum.
