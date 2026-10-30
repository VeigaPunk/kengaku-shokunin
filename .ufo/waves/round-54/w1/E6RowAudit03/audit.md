# R54-C2 independent entry-row audit

Source clone tip: `62e9bba5e4a0bed376890299aa6a09039db7e68e`.
All commands ran in the shared clone with the exact ledger argv, `cwd` at clone root, `env=hermetic_env(<seat scratch>/run/tmp-<row>)` imported from the frozen counter, and a 600-second per-command timeout. All scripts existed; no argv contained `--selftest`, `--help`, `-h`, `--dry`, or `--version`. These rows declare no evidence fragment (all are green), so fragment-match is N/A, not a missing-evidence finding.

## Commands and results

1. `python3 plans/config_projection.py --summary` — declared 0; observed 0; CONFIRMED. Output tail: `PROFILE path_prefix changed_leaves_by_category={"non_url_field": 61, "url_field": 1355}` (full final diagnostics were emitted; no required fragment).
2. `python3 plans/constraints_probe.py --lane .` — declared 0; observed 0; CONFIRMED. Output tail included `CASE seconds-30 predicted=fail observed=fail tests=PFF predicted_tests=PPF match=NO regrade=same ...`; registry explicitly defines these prediction mismatches as summary output, not exit failures.
3. `python3 corpus/evidence/round13-coverage/coverage_census.py` — declared 0; observed 0; CONFIRMED. Output tail listed `corpus/evidence/round54` and instrumentation denominator 12; no required fragment.

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| config-projection | 0 | 0 | N/A | CONFIRMED |
| constraints-probe | 0 | 0 | N/A | CONFIRMED |
| coverage-census | 0 | 0 | N/A | CONFIRMED |
