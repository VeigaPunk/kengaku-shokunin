# Seat R35IndepGrader — independent grader checker (kengaku r35 wave 1)

## Deliverable

`.ufo/waves/round-35/build/R35IndepGrader/indep.py` — an independent re-implementation of
the pinned Terminal-Bench 2.0 `protein-assembly` grader (`corpus/evidence/round35/tb2-eval/test_outputs.py`,
sha256 `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582`, pin
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`).

Independence properties:
- **Own translation table**: hard-coded standard genetic code (NCBI table 1); no Biopython import.
  Validated differentially against `Bio.Seq.Seq.translate()` on 2018 sequences (18 case contents +
  2000 random DNA, lengths ≡ 0 mod 3, stops included): `checked=2018 divergences=0`.
- **Own window loop**: rolling G/C count over every 50-nt window (15..35), implemented from scratch.
- **Own assertion dispatch**: mirrors the grader's assertion order and exact messages (lines count →
  alphabet → length → fusion order → flag start → linker chars/length per pair → C terminus → GC
  windows), including `.find()` semantics (returns −1) and the `rstrip()` per-line normalization.
- Does NOT import the grader; does NOT import the probe's `run_grader`; has no Biopython dependency.
- Case contents ARE generated from the probe's frozen table (`build_cases`/`components` imported from
  `plans/tb2_grader_probe.py`). The five AA reference constants are extracted independently from the
  grader source and verified equal to the probe's extraction (guard exits 2 on divergence — not triggered).

## Method

1. Read the frozen claims (`plans/round-35-claims.md`) and the probe receipt
   (`corpus/evidence/round35/tb2-grader-probe.txt`, 18 rows + totals line).
2. Read the pinned grader source (`test_outputs.py`) and re-implement its assertions as above.
3. Run `python3 .ufo/waves/round-35/build/R35IndepGrader/indep.py`; for each of the 18 cases compare
   my pass/fail and first failing assertion message against the receipt's `observed=`/`assertion=`
   fields. Any disagreement (different pass/fail OR different assertion message) is a finding.
4. Cross-check freshness: ran the **real** pinned grader (probe `run_grader`, Biopython 1.85 via
   `uv run --no-project --with biopython==1.85`) on the same 18 contents — observed output is
   byte-identical in `observed=`/`assertion=` to the committed receipt, so the receipt is not stale
   (scratch harness `.ufo/waves/round-35/build/R35IndepGrader/k35_live_grader.py`).

## Result (run: `python3 .../build/R35IndepGrader/indep.py`, exit 0)

```
cases=18 observed_pass=5 observed_fail=13 disagreements=0
```

All 18 rows `match=yes` (pass/fail AND first failing assertion class identical to the receipt):

| case | indep | receipt assertion (first failing) |
|---|---|---|
| valid-balanced | pass | – |
| uppercase | pass | – |
| no-trailing-newline | pass | – |
| trailing-empty-line | fail | Invalid number of lines in gblock.txt. |
| start-codon-prefixed | fail | Start of gBlock must match flag protein. |
| stop-codon-appended | fail | End of gBlock must match snap protein. |
| linker-4aa | fail | Linker must be between 5 and 20 amino acids long. |
| linker-21aa | fail | Linker must be between 5 and 20 amino acids long. |
| linker-20aa | pass | – |
| linker-non-gs | fail | Linker must only contain G and S amino acids. |
| linker-g-only | pass | – |
| n-terminal-linker | fail | Start of gBlock must match flag protein. |
| c-terminal-linker | fail | End of gBlock must match snap protein. |
| donor-acceptor-swapped | fail | Fusion protein must be in the order flag - donor - dhfr - acceptor - snap |
| donor-one-substitution | fail | Fusion protein must be in the order flag - donor - dhfr - acceptor - snap |
| donor-repeated | fail | gBlock must be at most 3000 nucleotides. |
| non-acgt-base | fail | gBlock must contain only A, T, C, G. |
| gc-window-high | fail | GC content must be between 30 and 70% in all 50 nucleotide windows. |

Note: `donor-one-substitution` correctly lands on the **order** assertion (mutant donor → `.find()`
= −1 → `flag_idx < donor_idx` false), matching the receipt.

## Exact commands & outputs

- `python3 .ufo/waves/round-35/build/R35IndepGrader/indep.py` → exit 0, `cases=18 observed_pass=5
  observed_fail=13 disagreements=0` (full transcript in `.ufo/waves/round-35/build/R35IndepGrader/indep.out`).
- `uv run --no-project --with biopython==1.85 python3 .../k35_diff_tables.py` → `checked=2018 divergences=0`.
- `uv run --no-project --with biopython==1.85 python3 .../k35_live_grader.py` → `live_cases=18`, all
  18 rows identical to receipt (fresh run of the real grader).

## Risks / notes

- Independent checker is validated only against the frozen receipt (and a fresh run of the real
  grader); it does not certify the grader itself.
- No lane files were modified; only the seat build dir was written. No tools installed (stdlib only).

VERDICT: indep-agree-18/18
