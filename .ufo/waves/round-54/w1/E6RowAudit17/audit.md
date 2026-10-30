# R54-C2 independent ledger-row execution audit

Audit clone tip: `62e9bba5e4a0bed376890299aa6a09039db7e68e`.
Each invocation used the committed row's `entry_argv`, `cwd` at that clone, `mod.hermetic_env(tmp)` imported from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c2_entrytruth.py`, and a 600-second subprocess timeout. The helper-owned temporary roots were under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit17/`. All rows are entry mode (no forbidden selftest/help/dry/version flags) and their script paths exist in the clone.

| name | entry command | declared exit/state | observed exit | evidence fragment | verdict |
|---|---|---:|---:|---|---|
| round40-c1-mutants | `python3 plans/round40_c1_verify.py --lane .` | 1 / red | 1 | `PINS total=3 mismatched=0` — matched | CONFIRMED |
| round40-c2 | `python3 plans/round40_c2_verify.py --lane .` | 0 / green | 0 | none declared (not applicable) | CONFIRMED |
| round41-c1-mutants | `python3 plans/round41_c1_verify.py --lane .` | 0 / green | 0 | none declared (not applicable) | CONFIRMED |

## Observed output tails

`round40-c1-mutants` (execution 331.3 s; output tail as emitted):
```text
en-in-teaches tool=anchor expect=reject declared=token-outside-anchor observed_rc=1 observed=anchor-unbound,token-outside-anchor WRONG
FIXTURE a_row-12-cells tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=anchor-unbound,row-malformed WRONG
FIXTURE a_tok-upper-anchor tool=anchor expect=reject declared=digest-uppercase observed_rc=1 observed=digest-uppercase,anchor-unbound WRONG
FIXTURE a_tok-abbrev-7hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved,anchor-unbound WRONG
FIXTURE a_tok-abbrev-64hex tool=anchor expect=reject declared=abbrev-unresolved observed_rc=1 observed=abbrev-unresolved,anchor-unbound WRONG
FIXTURE l_refuse-source-not-a-repo tool=ledger expect=e…
```

`round40-c2` (execution 3.1 s; output tail as emitted):
```text
V1 ok listed=8 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=16 distinct_quotes=16 distinct_lines=16 out_of_word_range=0
    gate: P4 ok checked=16 bad=0 first=0
    gate: P5 ok manifest_entries=8 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=57 knowledge_files=57 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=6 tags=6 bad=0
checks=7 defec…
```

`round41-c1-mutants` (execution 6.3 s; output tail as emitted):
```text
 s_modes-s08-artifact-without-quote-file tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s09-url-map-nested-shape tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s09-url-map-directory tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-02-registry-without-package tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-02-package-without-registry tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-03-dotted-access-date tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-03-single-digit-month-duplicate-request tool=sources expect=error declared_r…
```

The latter two output excerpts are limited by tool-output display truncation; observed exit codes and the red-row evidence fragment match (the green rows declare no fragment). No mismatch or unrun row.
