# R35ReopenPins — round 35 wave 1, executor seat

Task: independently re-open the six pinned terminal-bench-2 `protein-assembly` files at commit
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`, cmp against the frozen tb2-eval captures, and confirm the
round-34 `/tasks/`-prefixed URLs still 404.

## 1. Re-fetch (freshness)
Fetched 2026-10-25 16:41–16:42 (file mtimes) with `curl -fsSL` from
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/<path>`
into `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-35/build/R35ReopenPins/`.
All six fetches succeeded (no `FETCH_FAIL` lines).

| basename | pinned path | bytes |
|---|---|---|
| test_outputs.py | protein-assembly/tests/test_outputs.py | 3847 |
| test.sh | protein-assembly/tests/test.sh | 631 |
| instruction.md | protein-assembly/instruction.md | 2655 |
| task.toml | protein-assembly/task.toml | 973 |
| antibody.fasta | protein-assembly/environment/antibody.fasta | 475 |
| pdb_ids.txt | protein-assembly/environment/pdb_ids.txt | 100 |

## 2. cmp against tb2-eval captures
`cmp -s` each fetched file against `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round35/tb2-eval/<basename>`:
all six `rc=0`, `ANY_MISMATCH=0` → byte-identical, 6/6.

## 3. sha256sum
Fetched hashes (identical to the existing `tb2-eval/SHA256SUMS` capture manifest line-for-line):

```
44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582  test_outputs.py
9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5  test.sh
1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5  instruction.md
d714960681ec921a9247b382dfa0d8e97a9d13a3fe170a6ebd934ebe82398f24  task.toml
e0e13645b299470cb007f1daf13050010bf15cb7c22ff6042189ea1ca7a1c333  antibody.fasta
ea338c4e1a776a338d7d302e80ceaee6379c1c85a031448851c07b0f764358c2  pdb_ids.txt
```

## 4. Draft manifest + verification
Draft manifest written to `.ufo/waves/round-35/build/R35ReopenPins/SHA256SUMS` (sha256sum format, basenames, all six files).
Verification from the capture dir:
`cd corpus/evidence/round35/tb2-eval && sha256sum -c /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-35/build/R35ReopenPins/SHA256SUMS`
→ all six lines `OK` (test_outputs.py, test.sh, instruction.md, task.toml, antibody.fasta, pdb_ids.txt).

## 5. Round-34 `/tasks/`-prefixed URLs → 404
Round-34 source anchors used `.../2fd12b88…/tasks/protein-assembly/...` (see `.ufo/waves/round-34/build/R34EntryTB2/entry.md`
lines 1–3; defect recorded in `R34ReviewEntryTB2.md` and round-35 control `control-c1-skip.txt` V2). Re-checked all six
variants with `curl -s -o /dev/null -w '%{http_code}'`:

```
404  tasks/protein-assembly/tests/test_outputs.py
404  tasks/protein-assembly/tests/test.sh
404  tasks/protein-assembly/instruction.md
404  tasks/protein-assembly/task.toml
404  tasks/protein-assembly/environment/antibody.fasta
404  tasks/protein-assembly/environment/pdb_ids.txt
```

All six return 404, confirming the round-34 `/tasks/`-prefixed URLs remain dead and the root-level
`protein-assembly/` paths are the correct pinned locations.

## Risks / notes
- No lane files modified; only my seat's build dir (`R35ReopenPins/`) and report written.
- Evidence files in `tb2-eval/` also include a `SHA256SUMS` manifest; my draft manifest matches it exactly.
- Fetch timestamps per `ls -la` in scratch dir (16:41/16:42), same day as freeze claim.

VERDICT: reopen-6/6-manifest-ok
