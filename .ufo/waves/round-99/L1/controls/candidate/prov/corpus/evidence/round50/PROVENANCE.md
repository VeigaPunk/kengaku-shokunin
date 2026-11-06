# Row-scoped provenance bindings (round50; round 99, R99-C2)

Built by `plans/round99_provenance_build.py` from the frozen population in
`plans/round99_c2_rowscoped_bind.py`: SOURCES rows whose only anchor-digest finding was
`anchor-unbound` although their sha256 equals bytes committed in this directory. Each line
binds one row id to that capture through the frozen gate's provenance-row rule. Three
columns and no URL, so no line can re-bind another row through the gate's provenance-URL
fallback (round-98 lesson M4). The sha256 column is the committed capture's digest, equal
to the row's anchor token.

| row | file here | sha256 |
|---|---|---|
| S173 | `gitrepository-layout.adoc` | `39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439` |
| S174 | `git-init.adoc` | `123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95` |
| S175 | `git-worktree.adoc` | `ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc` |
| S176 | `git-replace.adoc` | `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631` |
| S177 | `git-fetch.adoc` | `fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e` |
