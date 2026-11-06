# Row-scoped provenance bindings (round93; round 99, R99-C2)

Built by `plans/round99_provenance_build.py` from the frozen population in
`plans/round99_c2_rowscoped_bind.py`: SOURCES rows whose only anchor-digest finding was
`anchor-unbound` although their sha256 equals bytes committed in this directory. Each line
binds one row id to that capture through the frozen gate's provenance-row rule. Three
columns and no URL, so no line can re-bind another row through the gate's provenance-URL
fallback (round-98 lesson M4). The sha256 column is the committed capture's digest, equal
to the row's anchor token.

| row | file here | sha256 |
|---|---|---|
| S293 | `graders/schemelike-metacircular-eval/tests/test/01-factorial.scm` | `2623000a742c63d50ae1851854826247caee129c7d1613be6c7131d21f26a6ad` |
