# Row-scoped provenance bindings (round95; round 99, R99-C2)

Built by `plans/round99_provenance_build.py` from the frozen population in
`plans/round99_c2_rowscoped_bind.py`: SOURCES rows whose only anchor-digest finding was
`anchor-unbound` although their sha256 equals bytes committed in this directory. Each line
binds one row id to that capture through the frozen gate's provenance-row rule. Three
columns and no URL, so no line can re-bind another row through the gate's provenance-URL
fallback (round-98 lesson M4). The sha256 column is the committed capture's digest, equal
to the row's anchor token.

| row | file here | sha256 |
|---|---|---|
| S306 | `graders/fix-code-vulnerability/upstream-bottle/bottle.py` | `abf643683b4870e07500f8a035d1a076d4bf0bbf98eb2fb5180fbc3ef8fad802` |
