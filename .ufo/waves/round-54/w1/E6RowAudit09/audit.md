# R54-C2 independent entry-row audit

Source lane tip observed before the shared clone: `62e9bba5e4a0bed376890299aa6a09039db7e68e`. The scratch clone top-level was `/fast/scratch/hyaku/kengaku-r54/E6RowAudit09/lane`. Each command ran there with Python `subprocess.run(..., timeout=600, capture_output=True, text=True)`; environment came from frozen `round54_c2_entrytruth.py::hermetic_env` using per-row scratch, with `TMPDIR` set there. The environment scrubbed secret-like variables and `GIT_*`, then set scratch `HOME`/`XDG_CONFIG_HOME`, empty counter-owned `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`, and unset `GIT_CONFIG_COUNT`. Script paths existed in clone and the argv passed `entry_mode_ok` (no forbidden selftest/help/dry/version switches). All rows are declared green; there is no declared evidence fragment to match (null).

The exact argv strings below are run with cwd set to the clone root. Observed tails copied from the captured combined stdout/stderr:

## Verdicts

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| order-check | 0 | 0 | N/A (green; no evidence field) | CONFIRMED |
| package-gate | 0 | 0 | N/A (green; no evidence field) | CONFIRMED |
| password-recovery-probe | 0 | 0 | N/A (green; no evidence field) | CONFIRMED |

### order-check

Command: `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt`

Tail:
```text
ORDER claims=plans/round-40-claims.md round=40 freeze=bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER receipt=corpus/evidence/round40/db-wal-probe.txt receipt_commit=055748f78a3335434f2a4070bb3fb1cf8d0eba1f claims_dir=.ufo/waves/round-40/claims/
ORDER scanned commits=1 file_entries=12 distinct_blobs=12
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
```

### package-gate

Command: `python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json --require-clean-tree`

Tail:
```text
P1 ok pinned=3 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
P4 ok checked=22 bad=0 first=0
P5 ok manifest_entries=6 bad=0 first=0
P6 ok rows=3 bad=0 first=0
P7 ok source_lines=3 bad=0 first=0
P8 ok index_rows=57 knowledge_files=57 bad=0 first=0
P9 ok untracked=0 first=0
defects=0
```

### password-recovery-probe

Command: `python3 plans/password_recovery_probe.py --lane .`

Tail (full captured output is retained in `audit.json`):
```text
CASE under-varsea predicted=fail observed=fail tests=F- predicted_tests=F- match=yes regrade=same violates=write-file,one-guess,recover -- the oracle's recovery work done from inside /app/varsea (the solver's cwd elsewhere): the guesses land at /app/varsea/recovered_passwords.txt, never at the graded path
regrade cases=16 differ=0
cases=16 observed_pass=5 observed_fail=11 mismatches=0
```

Registry cross-check: exact rows are `SKILL.md` lines 590 (`order-check`), 574 (`package-gate`), and 615 (`password-recovery-probe`). Ledger values and argv are in `plans/round54-entrytruth.json`. No row mismatch, timeout, execution error, non-entry argv, or absent script observed.
