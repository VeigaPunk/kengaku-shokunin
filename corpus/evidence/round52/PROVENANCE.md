# Path-matched provenance bindings (round52; round 100, R100-C2)

Built by `plans/round100_provenance_build.py` from the frozen population in
`plans/round100_c2_rowcensus_bind.py`: SOURCES rows whose anchor digest equals the committed
copy, in this directory, of the very upstream file the row's pinned URL names, but which the
frozen gate bound to another file (or to nothing). Each line binds one row id to that copy
through the gate's provenance-row rule. Three cells and no URL. The sha256 cell is the
committed copy's digest, equal to the row's anchor token; the upstream file was re-fetched
live on 2026-11-06 and still hashed to it (`.ufo/waves/round-100/L1/c2-live-refetch.txt`).

| row | file here | sha256 |
|---|---|---|
| S210 | `graders/distribution-search/tests/test_outputs.py` | `02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed` |
| S219 | `graders/openssl-selfsigned-cert/tests/test_outputs.py` | `90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d` |
| S228 | `graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` |
| S232 | `graders/sqlite-with-gcov/tests/test_outputs.py` | `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` |
| S279 | `graders/merge-diff-arc-agi-task/tests/test_outputs.py` | `2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149` |
| S281 | `graders/modernize-scientific-stack/tests/test_outputs.py` | `0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977` |
