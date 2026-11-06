# Path-matched provenance bindings (round58; round 100, R100-C2)

Built by `plans/round100_provenance_build.py` from the frozen population in
`plans/round100_c2_rowcensus_bind.py`: SOURCES rows whose anchor digest equals the committed
copy, in this directory, of the very upstream file the row's pinned URL names, but which the
frozen gate bound to another file (or to nothing). Each line binds one row id to that copy
through the gate's provenance-row rule. Three cells and no URL. The sha256 cell is the
committed copy's digest, equal to the row's anchor token; the upstream file was re-fetched
live on 2026-11-06 and still hashed to it (`.ufo/waves/round-100/L1/c2-live-refetch.txt`).

| row | file here | sha256 |
|---|---|---|
| S211 | `tb2-distribution-search/solution/solve.sh` | `19daaee18d534f36679854b0ba5727290df389ee023ebb67846cb89579d38bbe` |
