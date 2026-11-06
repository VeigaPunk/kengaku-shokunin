# Row-scoped provenance bindings (round92; round 99, R99-C2)

Built by `plans/round99_provenance_build.py` from the frozen population in
`plans/round99_c2_rowscoped_bind.py`: SOURCES rows whose only anchor-digest finding was
`anchor-unbound` although their sha256 equals bytes committed in this directory. Each line
binds one row id to that capture through the frozen gate's provenance-row rule. Three
columns and no URL, so no line can re-bind another row through the gate's provenance-URL
fallback (round-98 lesson M4). The sha256 column is the committed capture's digest, equal
to the row's anchor token.

| row | file here | sha256 |
|---|---|---|
| S285 | `graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl` | `8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de` |
