# TB2 protein-assembly expected-artifact capture

Pinned source: `harbor-framework/terminal-bench-2` commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, task `protein-assembly`. Captures are under `.ufo/waves/round-34/assimilation/captures/tb2-eval/`.

Evidence:

- Fetch command: `mkdir -p .../assimilation/captures/tb2-eval && for f in environment/antibody.fasta environment/pdb_ids.txt task.toml instruction.md; do curl -fsSL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/$f -o .../$(basename $f) || exit; done`. Completed successfully for all four files.
- Byte-size command: `wc -c antibody.fasta pdb_ids.txt task.toml instruction.md`; output: `475 antibody.fasta`, `100 pdb_ids.txt`, `973 task.toml`, `2655 instruction.md` (total 4203).
- SHA command: `sha256sum antibody.fasta pdb_ids.txt task.toml instruction.md`; output:
  - `e0e13645b299470cb007f1daf13050010bf15cb7c22ff6042189ea1ca7a1c333  antibody.fasta`
  - `ea338c4e1a776a338d7d302e80ceaee6379c1c85a031448851c07b0f764358c2  pdb_ids.txt`
  - `d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24  task.toml`
  - `1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5  instruction.md`
  These were written to `SHA256SUMS` in the capture directory.
- `task.toml` lines 1, 15–22: `schema_version = "1.1"`; difficulty `hard`, category `scientific-computing`; expert estimate `60.0` minutes; junior estimate `300.0` minutes; verifier timeout `1800.0` seconds.
- `instruction.md` lines 7–11 specify the deliverable `/app/gblock.txt`, containing only the gBlock sequence and no empty lines.
- Count command: `awk '/^>/{n++} END{print "FASTA records=" n}' antibody.fasta && awk 'NF{n++} END{print "PDB ids=" n}' pdb_ids.txt`; output `FASTA records=2` and `PDB ids=20`.

VERDICT: tb2-env-captured (4 files)
