source: S342–S347, https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/financial-document-processor/tests/test_outputs.py:66; companion files and quotes in corpus/lessons/round-100.md §Gate
verified-at: 2026-11-06 (round 100; measured T dbe0cefa607cf57f7f58346fce64bcc127144ca0)
recheck: on-release

# A hash-set grader checks where documents went, not what the summary says about them

The captured `financial-document-processor` grader (Terminal-Bench 2.0 at `2fd12b88`) gives an agent 17
JPG/PDF files under randomized names and asks it to OCR them, move the 10 invoices to `/app/invoices/`
and the 7 others to `/app/other/`, and write `/app/invoices/summary.csv` with each invoice's total and
VAT plus a final `total` row. Its seven tests identify every document by **sha512** (the reason the
lane ledger classes it `crypto-credential`): two tests compare the SET of sha512 digests found in each
output directory with a hard-coded set; one checks the CSV header and row count; one checks the CSV
values; one checks `/app/documents` is empty.

The replay runs the captured file unchanged under real `pytest.main` with an observe-only hook, in
python 3.13 / pytest 8.4.1 / pandas 2.3.2 / pytest-json-ctrf 0.3.5 (the `test.sh` uvx pins; numpy
unpinned and stamped), offline in bubblewrap. Each case starts from the image state (17 documents in
`/app/documents`, staged under their captured names: the grader never reads a name, S346/S347) and is
edited deterministically. Fifteen cases × eight legs reproduce their P0 mechanism predictions
(`plans/round100-cases.json`, `corpus/evidence/round100/fdp-probe.txt`). Legs: `dirs, invoices_moved,
others_moved, summary_exists, summary_structure, summary_content, documents_empty, reward`.

| case | observed | interpretation |
|---|---|---|
| C01 maintainer OCR solution's placement + summary (one offline run) | P×7, 1 | positive control: host tesseract 5.5.3 in place of the pinned 5.3.4 still classified 10/7 and read all ten totals and five VAT values exactly (`corpus/evidence/round100/fdp-solution/`) |
| C02 nothing done | F,E,E,F,E,E,F, 0 (E = FileNotFoundError) | no work is rejected |
| C03 summary = header + 11 copies of the `total` row | P×7, 1 | **gap**: no invoice row is required; `total` is a valid key and 11 rows meet the count |
| C04 summary = ten copies of one invoice's row + `total` | P×7, 1 | **gap**: rows need not be distinct or cover the ten invoices |
| C05 an extra `notes.json` in `/app/invoices` | P×7, 1 | `.json` is excluded by suffix (the reference solution writes a JSON sidecar per invoice) |
| C06 an extra `notes.txt` in `/app/invoices` | invoices_moved F, 0 | any other extra file enters the hash set |
| C07 copies of all 17 documents kept in `/app/documents/keep/` | P×7, 1 | **gap**: only top-level files count, so the instruction's "empty" directory is not enforced |
| C08 a second copy of one invoice under another name | P×7, 1 | **gap**: the set collapses duplicates (18 files graded as 17) |
| C09 one invoice misfiled as other, summary 9 + total | P,F,F,P,F,F,P, 0 | mechanism negative: both hash sets and both CSV checks catch a misfile |
| C10 empty VAT written as 0 | P×7, 1 | documented tolerance (instruction: "0 or empty") |
| C11 one total +0.009 | P×7, 1 | inside the strict `< 0.01` band |
| C12 one total +0.01 | summary_content F, 0 | |Δ| = 0.0100000000002 in float: the band edge is exclusive |
| C13 no summary.csv | P,F,P,F,E,E,P, 0 | a missing summary also fails the invoice-placement test (its expected set contains the literal `summary.csv`) |
| C14 columns ordered filename,vat_amount,total_amount | summary_structure F, 0 | the header test is order-sensitive while the content test reads columns by name |
| C15 UTF-8 BOM before the header | summary_structure F, 0 | `csv.DictReader` keeps the BOM in the first field name; pandas' C parser strips it (content passes) |

## What this teaches about grading

- **A set comparison over content digests is the right identity check and the wrong count check.**
  sha512 sets make the grader immune to the randomized names (S347) and to renames, but blind to
  duplicates (C08) — the same multiplicity blindness as round 98's per-line membership and round 99's
  DAG edge sets (`knowledge/tb2-regex-chess-grader.md`, `knowledge/tb2-bn-fit-modify-grader.md`).
- **Lookup-by-key validation is not coverage.** Every summary row must name a known key with matching
  values, but nothing requires every key to appear once (C03, C04). The README's "Correct summation in
  the final 'total' row" (S349, rejected) is not what the bytes check: the total row is a hard-coded
  lookup, never a sum, and its position is free.
- **Two readers of one CSV disagree on format.** `csv.DictReader` (order- and BOM-sensitive) and
  `pandas.read_csv` (by name, BOM-stripping) split C14/C15 into structure-fail/content-pass.
- **A "directory is empty" contract implemented as "no top-level files"** admits retained copies (C07).

## Limits

- The positive control is one run of the maintainer's classifier with host tesseract 5.5.3 (the script
  pins apt `tesseract-ocr=5.3.4-1build5`); the probe stages that run's committed placement and summary
  and does not re-run OCR. Its exact match with the grader's hard-coded table is the evidence that the
  fixture is faithful.
- The replay does not run the harness image (`alexgshaw/financial-document-processor:20251031`, S348)
  and makes no claim about any submitted agent solution.
