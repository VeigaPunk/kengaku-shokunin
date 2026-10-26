source: S105 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py — `test_gblock`, lines 10–73, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-25
source: S106 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test.sh — reward mapping, lines 18–30, same commit, accessed 2026-10-25
source: S107 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/instruction.md — requirement bullets, lines 9–34, same commit, accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch the three pinned URLs, `sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS`, and re-run `plans/tb2_grader_probe.py`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `protein-assembly`

At terminal-bench-2 commit `2fd12b88`, the `protein-assembly` task's whole score is one pytest
function, `test_gblock`, mapped by `tests/test.sh` to a binary reward (1 if pytest exits 0, else
0). The grader never opens the task's reference inputs (`pdb_ids.txt`, `antibody.fasta`, the
plasmid, FPbase/PDB API results): the five expected subproteins are amino-acid **literals** in the
test file, and every instruction requirement that names a source (PDB sequence, FPbase spectra,
the antibody's antigen, the plasmid's DHFR) is enforced only through those literals. Offline
execution of the captured grader *function* on 18 lane-authored synthetic gBlocks — not a run of
Terminal-Bench, of the task image, or of any real submission (`plans/tb2_grader_probe.py`; receipt
`corpus/evidence/round35/tb2-grader-probe.txt`) matched every prediction written from the static
reading before the first run:

`cases=18 observed_pass=5 observed_fail=13 mismatches=0`

This entry extends `knowledge/benchmark-verifier-execution-model.md` (where a TB2 verifier runs;
S100 is the same repository at the same commit) and `knowledge/benchmark-grader-semantics.md` (one
Toolathlon grader read), and discharges, for this one task only, the `corpus/README.md` §Frontier
round-33 clause that left "Terminal-Bench 2.0's" scoring code open.

## Source labels

S105–S107 are the benchmark maintainers' own task files: primary for *what this grader checks*,
and a self-report for everything else (the comments' claims that one listed PDB protein matches
each requirement are the authors' statements, not verified here). The probe receipt is the lane's
own re-runnable gate output (tier A for its own scope: these 18 inputs under Biopython 1.85).

## What the grader checks (static reading, `test_outputs.py`)

| Step | Mechanism | Lines |
|---|---|---|
| File shape | `/app/gblock.txt` must exist; lines are `rstrip`ped; exactly one line; lower-cased | 13–21 |
| Alphabet, length | full match `[atcg]+`; at most 3000 nt | 22–23 |
| Translation | Biopython `Seq(gblock).translate()` over the whole gBlock | 27 |
| Expected parts | literals `flag_aa` (`DYKDDDDK`, the FLAG tag), `donor_aa`, `dhfr_aa`, `acceptor_aa`, `snap_aa`; located with `str.find` (first occurrence, −1 when absent) | 28–41 |
| Order | `flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx` | 42–44 |
| Boundaries | FLAG at index 0; SNAP ends at the last residue | 46, 60 |
| Linkers | each of the four gaps fully matches `[GS]+` and has 5–20 residues | 47–59 |
| GC | every full 50-nt window has 15–35 G/C (30–70%), checked by a sliding count | 65–73 |
| Reward | pytest exit 0 → `echo 1`, else `echo 0` into `/logs/verifier/reward.txt` | `test.sh` 26–30 |

## Instruction requirement → enforcing assertion (executed, 18 cases)

Each row is one probe case; "observed" and the first failing assertion are copied from the receipt.

| Instruction requirement (S107) | Probe case | Observed | First failing assertion |
|---|---|---|---|
| all bullets satisfied | `valid-balanced` (FLAG–GGGGS–donor–GGGGS–DHFR–GGGGS–acceptor–GGGGS–SNAP, 2586 nt) | pass | — |
| file holds only the sequence | `uppercase`, `no-trailing-newline` | pass, pass | — (case is lowered; a final newline is stripped) |
| no empty lines | `trailing-empty-line` | fail | line count |
| no start codon; drop N-terminal Met | `start-codon-prefixed` | fail | FLAG not at index 0 |
| no stop codon | `stop-codon-appended` | fail | SNAP does not end the protein |
| linkers 5–20 aa | `linker-4aa`, `linker-21aa`; `linker-20aa` | fail, fail; pass | linker length (upper bound inclusive) |
| only GS linkers | `linker-non-gs` (`GGAGS`) | fail | linker alphabet |
| "GS linkers" | `linker-g-only` (`GGGGG`) | **pass** | — the grader does not distinguish a G-only linker |
| no linker at N / C terminus | `n-terminal-linker`, `c-terminal-linker` | fail, fail | FLAG start / SNAP end |
| subprotein order | `donor-acceptor-swapped` | fail | order |
| donor matches its PDB sequence | `donor-one-substitution` | fail | **order** (the mutated donor is not found, `find` returns −1) |
| do not repeat a protein (stated for the antibody binder; the probe repeats the donor) | `donor-repeated` | fail | **length cap** (3378 nt) fires before any linker check |
| a DNA sequence | `non-acgt-base` | fail | alphabet |
| GC 30–70% per 50-nt window | `gc-window-high` (first 40 DHFR residues on max-GC codons) | fail | GC window |

Three findings follow from the executed table, each bounded to this grader at this commit:

1. **A G-only linker passes.** `[GS]+` admits `GGGGG`; whether that is a "GS linker" is not
   decided by the grader. A solution with G-only linkers scores 1.
2. **The 3000-nt cap never decides an otherwise-passing gBlock.** With the literal lengths 8, 259,
   158, 235 and 182 residues and four linkers of at most 20, the longest gBlock that passes every
   other assertion is 3 × (842 + 80) = 2766 nt (`max_passing_nt=2766` in the receipt). The cap only
   changes *which* assertion fails first (the repeated-donor case), never the reward.
3. **Failure messages misattribute.** A one-residue error in a subprotein fails with the *order*
   message, because `find` returns −1. A trajectory analysis that reads the assertion text as the
   cause would be wrong; the binary reward is unaffected.

Requirements the 18 cases do **not** exercise (wave-1 review `R35RevProbePred`): the antibody-binder
bullet (the grader expects the 8-residue FLAG epitope literal; no variant or repeat of it is probed),
the DHFR-from-`plasmid.gb` bullet (no DHFR substitution case), and the FPbase spectral bullet (enforced
only through the donor/acceptor literals, unprobeable offline). PDB identity is probed for the donor
only. The predictions were committed in the freeze (`11d64530`) before the receipt first landed; that
ordering, not a byte inside the receipt, is the evidence that they were written before the run.

## Negative space

This entry does **not** establish: that the literals are the correct PDB/FPbase/antibody answers
(the grader's comments say so; nothing here checks them against `pdb_ids.txt`, the APIs or
`antibody.fasta`); biological correctness or expression of any gBlock; Harbor's runtime execution of
this test (see `benchmark-verifier-execution-model.md` for where verifiers run); any model's
performance or any trajectory; task validity in the PROVINCE sense; or anything about the other 88
TB2 tasks. The probe runs the captured file under Biopython 1.85 (the version `test.sh` pins) on
the lane's host Python, not inside the task image.

**Falsifier:** this entry is falsified if a re-fetch of the three pinned URLs yields bytes whose
SHA-256 differs from `corpus/evidence/round35/tb2-eval/SHA256SUMS`, or if a fresh run of
`plans/tb2_grader_probe.py` against the captured grader prints a summary line different from the
one quoted above (for example, `linker-g-only` observed `fail`).

## Located quotes

Quotes are byte-exact from the round-35 captures (`corpus/evidence/round35/tb2-eval/`, identical to
the pinned raw files), each ≤25 words.

| Claim supported | Quote | Location |
|---|---|---|
| grader reads one fixed path | “gblock_path = Path("/app/gblock.txt")” | `test_outputs.py:13` |
| trailing whitespace is stripped per line | “lines = [line.rstrip() for line in f]” | `test_outputs.py:16` |
| exactly one line | “assert len(lines) == 1, "Invalid number of lines in gblock.txt."” | `test_outputs.py:19` |
| case-insensitive | “gblock = lines[0].lower()” | `test_outputs.py:21` |
| length cap | “assert len(gblock) <= 3000, "gBlock must be at most 3000 nucleotides."” | `test_outputs.py:23` |
| literals replace lookups (authors' rationale) | “We can directly check that the gBlock contains specific sequences since only one protein” | `test_outputs.py:25` |
| whole-gBlock translation | “gblock_aa = str(Seq(gblock).translate())” | `test_outputs.py:27` |
| antibody binder literal is the FLAG tag | “flag_aa = "DYKDDDDK"” | `test_outputs.py:28` |
| first-occurrence search | “donor_idx = gblock_aa.find(donor_aa)” | `test_outputs.py:38` |
| order assertion | “assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (” | `test_outputs.py:42` |
| FLAG starts the protein | “assert flag_idx == 0, "Start of gBlock must match flag protein."” | `test_outputs.py:46` |
| linker alphabet | “assert re.fullmatch(r"[GS]+", linker), (” | `test_outputs.py:54` |
| linker length | “assert 5 <= len(linker) <= 20, (” | `test_outputs.py:57` |
| SNAP ends the protein | “assert snap_idx + len(snap_aa) == len(gblock_aa), (” | `test_outputs.py:60` |
| GC window bound | “assert 15 <= gc <= 35, (” | `test_outputs.py:71` |
| pinned grader dependency | “-w biopython==1.85 \” | `test.sh:21` |
| binary reward on pass | “echo 1 > /logs/verifier/reward.txt” | `test.sh:27` |
| binary reward on fail | “echo 0 > /logs/verifier/reward.txt” | `test.sh:29` |
| no empty lines | “of the gBlock and nothing else. No empty lines.” | `instruction.md:11` |
| linker length requirement | “The GS linkers between different subproteins should be between 5 and 20 amino acids long.” | `instruction.md:29` |
| GC requirement | “The GC content should be between 30 and 70% in any given 50 nucleotide window encoding the” | `instruction.md:30` |
| required order | “The order of the subproteins from N to C terminus should be: antibody binder - donor - dhfr -” | `instruction.md:33` |

## Errata (appended round 35, falsify wave, 2026-10-25)

The findings above stay as written; these corrections narrow them (seat reports under
`.ufo/waves/round-35/falsify/`, each re-run through the probe's own `run_grader` on the pinned grader).

- **Finding 2, number wrong by 2 nt.** The longest passing gBlock is **2768 nt**, not 2766: the
  translation drops a trailing partial codon, so 1–2 extra bases after the SNAP stop-less end still
  pass (`F35MaxNt.md`: `append=2 nt=2768 observed=pass`; `append=3` fails). The receipt's
  `max_passing_nt=2766` is the full-codon maximum. The conclusion stands: no passing gBlock reaches
  the 3000-nt cap. New acceptance this exposes: a gBlock whose length is not a multiple of 3 passes.
- **Finding 1, narrowed.** G-only linkers pass at every length 5–20 in every gap *when the construct
  also meets the GC windows*; with all four linkers at 20 G-only residues no GC-safe encoding was
  found in 3000 deterministic seeds (`F35GOnlyLinker.md`), so "a solution with G-only linkers scores
  1" holds only for constructs that satisfy the other assertions.
- **Finding 3, narrowed.** The order message holds for one-residue errors in the donor, DHFR,
  acceptor and SNAP literals (26 rows), but a one-residue error in the first subprotein (the FLAG
  literal) fails with `Start of gBlock must match flag protein.`: `flag_idx = -1` still satisfies the
  order chain, and the next assertion fires (`F35GOnlyLinker.md`).
- **Probe case `non-acgt-base` is confounded** as well as `donor-repeated`: the `n` sits in linker 1,
  so it also breaks the linker alphabet; the alphabet assertion fires first (`F35IndepWindows.md`).
- **Table header overstates.** "Instruction requirement → enforcing assertion (executed, 18 cases)"
  maps cleanly only for file shape, linker alphabet and length, start/stop codons, terminal linkers
  and order; donor PDB identity, N-terminal Met, the 3000-nt cap and the GC rule (high side only) are
  partial or confounded, and three bullets are not exercised (listed above) (`F35CritC1.md` F3).
