# E6RowAudit23 — R54-C2 independent ledger-row audit

Re-executed all three frozen entry argv rows in shared clone `62e9bba5e4a0bed376890299aa6a09039db7e68e` under the counter's imported `hermetic_env`, with row-specific TMPDIR under seat scratch and a 600-second per-row cap. All three argv passed entry-mode checking, all three script paths exist in the clone, and all completed (0.1s each).

| row | declared | observed | evidence fragment match | verdict |
|---|---:|---:|---|---|
| round51-surfaces | 1 | 1 | false | NOT CONFIRMED |
| round52-c1 | 1 | 1 | true | CONFIRMED |
| round52-c2 | 0 | 0 | N/A (no fragment on green row) | CONFIRMED |

The round51-surfaces output starts `REV 62e9bba5e4a0bed376890299aa6a09039db7e68e`, not its declared evidence `REV 17f90355c3ec17dcf15f7980d83f1943ae428fe5`; its ending was `RESOLVE observed_present=12 floor=13 verdict=violated` / `PREDICATE R51-C1 fail`. Exit agrees, but evidence does not, so it is not confirmed. round52-c1's declared fragment `TASKS total=89 records=89 classified=88` appeared verbatim and its ending was `PREDICATE R52-C1-A5 pass`. round52-c2 exited 0 and ended `PREDICATE R52-C2 pass`.

Exact commands, environment method and output tails are in `E6RowAudit23/audit.md`; machine-readable verdicts and entry-mode/script checks are in `E6RowAudit23/audit.json`.

No tools installed or updated.

Report: `.ufo/waves/round-54/w1/E6RowAudit23.md`
