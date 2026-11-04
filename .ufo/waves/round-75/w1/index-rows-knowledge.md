# Proposed knowledge index rows

Axes: coverage (file indexing) and calibration (admission and provenance boundaries).

These are replacement-ready proposals, not instructions to append duplicates: the live README already contained all three table rows when inspected; none appears as a table row in `43255758:corpus/README.md`.

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/instrument-registry-derivation.md` | Row-derived instrument audits, AST declaration checks, and structural versus runtime limits; held candidate | admission: hold |
| `knowledge/registry-argv-and-flag-audit.md` | Registry command-line flag contracts and structural versus executable acceptance; held candidate | admission: hold |
| `knowledge/tb2-torch-tensor-parallel-offline.md` | Offline replay of the torch-tensor-parallelism grader, its five-case table, gloo execution and value-checking limits | S183 — pinned `torch-tensor-parallelism/tests/test_outputs.py`:18–25,43–211 at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; `corpus/evidence/round66/tensor/receipt.txt` |

A README row indexes `instrument-registry-derivation.md` and does not admit it.
A README row indexes `registry-argv-and-flag-audit.md` and does not admit it.
A README row indexes `tb2-torch-tensor-parallel-offline.md` and does not admit it.

The two held candidates cite S249 (`ast.html#ast.parse`, supporting `#ast.PyCF_ONLY_AST` and `#ast.walk`) and S250 (`argparse.html#name-or-flags`) respectively; their hold markers remain authoritative. The tensor source is S183, not the live README row's S235–S237.
