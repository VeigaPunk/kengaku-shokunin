# Path-matched provenance bindings (round94; round 100, R100-C2)

Built by `plans/round100_provenance_build.py` from the frozen population in
`plans/round100_c2_rowcensus_bind.py`: SOURCES rows whose anchor digest equals the committed
copy, in this directory, of the very upstream file the row's pinned URL names, but which the
frozen gate bound to another file (or to nothing). Each line binds one row id to that copy
through the gate's provenance-row rule. Three cells and no URL. The sha256 cell is the
committed copy's digest, equal to the row's anchor token; the upstream file was re-fetched
live on 2026-11-06 and still hashed to it (`.ufo/waves/round-100/L1/c2-live-refetch.txt`).

| row | file here | sha256 |
|---|---|---|
| S298 | `graders/write-compressor/tests/original-decomp.c` | `7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a` |
| S300 | `graders/write-compressor/solution/solve.sh` | `01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409` |
