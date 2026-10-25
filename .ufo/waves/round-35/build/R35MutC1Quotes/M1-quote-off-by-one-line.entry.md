source: S105 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py
source: S106 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test.sh
source: S107 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/instruction.md
verified-at: 2026-10-25
recheck: on-release

# TB2 protein-assembly grader (minimal V3 fixture entry)

Pinned Terminal-Bench 2.0 protein-assembly grader sources admitted with an executed offline probe
(plans/tb2_grader_probe.py, 18 frozen cases): the grader tests the gblock file's shape, DNA-only
content, length cap, subprotein order and identity, GS-linker constraints, and GC windows.

Probe receipt summary (carried verbatim):
cases=18 observed_pass=5 observed_fail=13 mismatches=0

## Negative space

This entry is falsifiable: flipping any quoted source line or quote string makes the located-quotes
check fail, and removing the probe's mismatch line breaks the receipt check.

## Located quotes

| claim | “quote” | `file:line` |
| --- | --- | --- |
| Invalid-line-count | “Invalid number of lines in gblock.txt.” | `test_outputs.py:20` |
| Base-pair-content | “gBlock must contain only A, T, C, G.” | `test_outputs.py:22` |
| Length-cap | “gBlock must be at most 3000 nucleotides.” | `test_outputs.py:23` |
| Subprotein-order | “Fusion protein must be in the order flag - donor - dhfr - acceptor - snap” | `test_outputs.py:42-44` |
| N-term-start | “Start of gBlock must match flag protein.” | `test_outputs.py:46` |
| Linker-composition | “Linker must only contain G and S amino acids.” | `test_outputs.py:54-56` |
| Linker-length | “Linker must be between 5 and 20 amino acids long.” | `test_outputs.py:57-59` |
| C-term-end | “End of gBlock must match snap protein.” | `test_outputs.py:60-62` |
| GC-window | “GC content must be between 30 and 70% in all 50 nucleotide windows.” | `test_outputs.py:66-68` |
| Workdir-requirement | “Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script.” | `test.sh:14` |
| File-shape | “of the gBlock and nothing else. No empty lines.” | `instruction.md:11` |
| Order-spec | “The order of the subproteins from N to C terminus should be: antibody binder - donor - dhfr -” | `instruction.md:33` |
