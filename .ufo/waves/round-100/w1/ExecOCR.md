# ExecOCR — R100-C1 positive-control OCR-version fidelity

## Hypothesis
The committed positive control (`corpus/evidence/round100/fdp-solution/`: placement.tsv, summary.csv,
per-invoice JSON sidecars from one offline run of the maintainer `solve.sh` heredoc) was produced with host
tesseract **5.5.3**, while `solve.sh` pins apt `tesseract-ocr=5.3.4-1build5`. The claim is that this version
mismatch undermines the positive control's fidelity. This seat re-ran the exact `solve.sh` heredoc
(`document_processor.py`, PEP 723 pins: numpy 2.3.2, opencv-python 4.11.0.86, pandas 2.3.2, pillow 11.3.0,
pymupdf 1.25.2, pytesseract 0.3.13, ...) offline under bubblewrap (`--unshare-all --clearenv`, no network)
on the 17 committed documents, once **per engine**, and graded each run's `/app` with the captured
`test_outputs.py` under the grader venv (pytest 8.4.1 / pandas 2.3.2 / pytest-json-ctrf 0.3.5).

## Method
- Extracted the heredoc exactly as RUN.md did (`awk` on `solve.sh`): the bytes are identical to the committed
  `fdp-solution/document_processor.py` (sha256 `db4f841e…c937a`, verified by `diff`).
- Engine A (host): `/usr/bin/tesseract` **5.5.3** (leptonica 1.87.0), `TESSDATA_PREFIX=/usr/share/tessdata`.
- Engine B (pinned): `tesseract` **5.3.4** (leptonica 1.83.1) via `micromamba create -c conda-forge
  tesseract=5.3.4` (conda-forge is the only offline-available channel for exactly 5.3.4; apt is paused and the
  box has no Ubuntu 5.3.4-1build5 binary). `TESSDATA_PREFIX` pointed at the conda env's own `share/tessdata`,
  so neither run read the host's 5.5.3 traineddata. Shadow `PATH` bound the requested binary only.
- Both runs processed all 17 documents, `rc=0`, "Found 10 invoices and 7 other documents" — matching the
  committed `run.log` line-for-line (extra `rc=0` trailer only).
- Grading: captured `test_outputs.py` under the grader venv inside bubblewrap (offline), 7/7 passed, reward rc=0,
  for **both** runs.

## Results — python-observable output is byte-identical across versions
| Comparison | placement.tsv | summary.csv | invoices-json (10) | grader |
|---|---|---|---|---|
| host 5.5.3 run vs committed `fdp-solution/` | `identical` (`diff` clean) | `identical` (sha256 `08724ad9…973b2`) | 10/10 `SAME` | 7/7, rc=0 |
| conda 5.3.4 run vs committed `fdp-solution/` | `identical` (`diff` clean) | `identical` (sha256 `08724ad9…973b2`) | 10/10 `SAME` | 7/7, rc=0 |
| host run vs conda run | byte-identical | byte-identical | all SAME | identical (pytest logs differ only in wall time) |

Receipts (names only; full bytes in `.ufo/waves/round-100/w1/ExecOCR/`):
`host553-{placement,summary,run,provenance,pytest}.log/exit`,
`conda534-{placement,summary,run,provenance,pytest}.log/exit`, `ocr_diff.txt`, `map_diff.py`.

## Crucial nuance — raw OCR text DOES differ; the pipeline erases it
`ocr_diff.txt` / `map_diff.py`: at the raw word level the two engines disagree on 11/11 invoice+other JPGs
sampled (e.g. `53lc58dr.jpg` account number `acct_1N8CpQGmFzQxIIDx` vs `…zQxlIDx`; `8mdd4v30.jpg` digits
`1079,80` vs `079,80`). The `eng.traineddata` also differs (host sha256 `daa0c97d…047` vs conda `7d4322bd…970b2`).
But the disagreements land on tokens the solver never extracts (classification signals, account strings,
header text). Every extracted `total_amount`/`vat_amount` — and hence every placement decision,
summary.csv value, and the `total` row 81315.2/5402.48 — is numerically identical, so the grader's
`test_summary_csv_content` passes under both engines.

## Verdicts
- **FALSIFIED (version-sensitivity of the positive control): the fidelity of `fdp-solution/` does NOT depend on
  the OCR-engine version.** Both engines reproduce the committed placement.tsv and summary.csv byte-for-byte, and
  the captured grader passes 7/7 on each run's `/app`. The committed 5.5.3-produced fixture therefore equals the
  output the 5.3.4-pinned solve.sh would have produced on these 17 documents.
- **CONFIRMED (raw-OCR divergence): engines 5.5.3 vs 5.3.4 make visibly different word-level recognition errors
  on the same documents**, but no error flips a classification or a captured amount for this document set. The
  equivalence is pipeline-level (estimator-free classification + regex amounts are insensitive to the differing
  tokens), not engine-level.

## Notes
- No production files edited; scratch clone not needed (used read-only captures + scratch sandboxes only).
- Recorded installs: `tesseract 5.3.4` via micromamba/conda-forge into scratch env `tess534` (channel: conda-forge
  official repo; reason: only source of exactly 5.3.4 offline; apt paused host-wide per pacman guard — no
  pacman transaction run). `uv venv` solve/grader venvs (uv 0.13.0, standard channels, numpy 2.3.2 etc. from PyPI).
- Residual risk: the equivalence is shown for these 17 documents with this traineddata pair; a different document
  whose decisive amount token is OCR-confusable could split the engines. That is the general OCR-version risk the
  positive control inherits and the lane's C1 predicate does not test — a round-101 routing candidate, not a
  round-100 kill (frozen predicates unchanged by this seat).

Report: .ufo/waves/round-100/w1/ExecOCR.md
