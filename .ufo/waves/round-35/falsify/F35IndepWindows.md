# F35IndepWindows — falsify · C1 probe construction (round 35 wave 2)

Seat: F35IndepWindows (executor, leaf). Target: `plans/tb2_grader_probe.py` `build_cases`
(18 case contents) used by C1 coverage. Lane tip `dfee6fff631ebc5f623ba4506e5c7992a215401c`,
freeze `11d64530`.

## Method (independence axes)

1. **Translation (a)** — own explicit 64-codon standard genetic table written in the verifier
   (`verify_cases.py`, `MY_CODONS`), not imported from the probe's `CODONS`. Cross-checked
   against Biopython 1.85: **0 mismatches** across all 64 codons + ambiguous-codon samples
   (`codon_table_mismatches_vs_Biopython=0`).
2. **GC (b)** — min/max G/C over every full 50-nt window computed independently (`window_stats`).
3. **Requirement isolation (c)** — each case re-evaluated against the full grader assertion set
   (lines / alphabet / length / order / FLAG@0 / linker `[GS]+` / linker length 5–20 / SNAP end /
   GC windows). `violated` = every requirement broken by that content (not just the first-failing
   assertion); compared with the case label's claim (`expected`). `firstfail` replicates the
   grader's assertion order and matches the committed receipt messages on all 18 rows.

Command (run in scratch dir; repo only read):

```
uv run --no-project --with biopython==1.85 python3 verify_cases.py
```

## Result — 18 cases independently re-derived

| case | nt | aa | gc (min,max) | nbad | violated | expected | isolated |
|---|---|---|---|---|---|---|---|
| valid-balanced | 2586 | 862 | 19,30 | 0 | [] | [] | yes |
| uppercase | 2586 | 862 | 19,30 | 0 | [] | [] | yes |
| no-trailing-newline | 2586 | 862 | 19,30 | 0 | [] | [] | yes |
| trailing-empty-line | 2586 | 862 | 19,30 | 0 | [lines] | [lines] | yes |
| start-codon-prefixed | 2589 | 863 | 19,30 | 0 | [flag0] | [flag0] | yes |
| stop-codon-appended | 2589 | 863 | 19,30 | 0 | [snapend] | [snapend] | yes |
| linker-4aa | 2583 | 861 | 19,30 | 0 | [linklen] | [linklen] | yes |
| linker-21aa | 2634 | 878 | 19,31 | 0 | [linklen] | [linklen] | yes |
| linker-20aa | 2631 | 877 | 19,31 | 0 | [] | [] | yes |
| linker-non-gs | 2586 | 862 | 19,30 | 0 | [linkGS] | [linkGS] | yes |
| linker-g-only | 2586 | 862 | 19,30 | 0 | [] | [] | yes |
| n-terminal-linker | 2601 | 867 | 19,30 | 0 | [flag0] | [flag0] | yes |
| c-terminal-linker | 2601 | 867 | 19,30 | 0 | [snapend] | [snapend] | yes |
| donor-acceptor-swapped | 2586 | 862 | 20,30 | 0 | [order] | [order] | yes |
| donor-one-substitution | 2586 | 862 | 19,30 | 0 | [order] | [order] | yes (artifact noted) |
| donor-repeated | 3378 | 1126 | 19,30 | 0 | [length, linkGS, linklen] | [length] | **no** |
| non-acgt-base | 2586 | 862 | 19,30 | 0 | [alphabet, linkGS] | [alphabet] | **no** |
| gc-window-high | 2586 | 862 | 19,36 | 6 | [gcwin] | [gcwin] | yes |

All 18 `firstfail` messages reproduce the committed receipt
(`corpus/evidence/round35/tb2-grader-probe.txt`) exactly, and 16/18 have the claimed single
violation. Two findings.

## Findings

### F1 — `donor-repeated` failure is confounded by 2nd/3rd violations (`plans/tb2_grader_probe.py:112`)
Content: `back_translate(fusion([flag, donor, donor, dhfr, acceptor, snap], L + ["GGGGS"]))`.
The duplicated donor copy sits between the first donor and DHFR, i.e. inside the gap the grader
treats as the donor→DHFR linker. Independent evaluation:
`violated=[length, linkGS, linklen]`, while the case label claims only `do not repeat a protein`
(length cap). The first-failing assertion is the length cap
(`gBlock must be at most 3000 nucleotides.` — receipt line 18), masking that the same content also
fails the linker-alphabet and linker-length assertions (the "gap" is 269 aa of non-`[GS]+`
sequence). The failure is not attributable to the length cap alone: raising the cap would leave the
case failing on `[GS]+`.

### F2 — `non-acgt-base` failure is confounded by a second violation (`plans/tb2_grader_probe.py:113`)
Content: `valid[:30] + "n" + valid[31:]`. Position 30 (0-based) is the first base of codon 10 —
linker 1's third residue — so the `n` codon translates to `X`, breaking that linker's `[GS]+`
alphabet. Independent evaluation: `violated=[alphabet, linkGS]`, label claims only `gBlock is a
DNA sequence`. First-failing assertion is the alphabet regex
(`gBlock must contain only A, T, C, G.` — receipt line 19), masking the aa-level `X`. A fix that
only changed the offending letter's alphabet class (e.g. `n`→`a` without knowing the original base
at 30) would restore the codon and heal the linker, but as constructed the case exercises two
requirements, not one.

No other case shows a second violation (incl. `donor-one-substitution`: the only extra failure is
the grader's well-known *order-message artifact* — the substitution breaks the donor literal's
`find` → `donor_idx=-1` → order assertion fires; no *requirement* other than "donor matches its
PDB sequence" is violated; already documented in `knowledge/tb2-protein-assembly-grader.md` §
finding 3).

## C1 counter (context)

```
$ uv run --no-project --with biopython==1.85 python3 plans/round35_c1_verify.py --lane .
V1 ok … V6 ok
checks=6 defects=0
PREDICATE C1 pass
```

## Tooling record
- No installs performed. `uv 0.13.0` already present; Biopython **1.85** run via ephemeral
  `uv run --no-project --with biopython==1.85` (official uv channel; no pacman transaction; host
  Python 3.14.8). Scratch: `.ufo/waves/round-35/falsify/F35IndepWindows/` (`verify_cases.py`,
  `tb2_grader_probe.py` copy for bytecode-free import).

VERDICT: cases-isolated-16/18
