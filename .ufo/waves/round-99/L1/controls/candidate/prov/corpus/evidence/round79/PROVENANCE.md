# Row-scoped provenance bindings (round79; round 99, R99-C2)

Built by `plans/round99_provenance_build.py` from the frozen population in
`plans/round99_c2_rowscoped_bind.py`: SOURCES rows whose only anchor-digest finding was
`anchor-unbound` although their sha256 equals bytes committed in this directory. Each line
binds one row id to that capture through the frozen gate's provenance-row rule. Three
columns and no URL, so no line can re-bind another row through the gate's provenance-URL
fallback (round-98 lesson M4). The sha256 column is the committed capture's digest, equal
to the row's anchor token.

| row | file here | sha256 |
|---|---|---|
| S180 | `sources/tb2-readme.md` | `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364` |
