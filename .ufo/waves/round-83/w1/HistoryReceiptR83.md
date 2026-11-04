# HistoryReceiptR83

Axes: coverage; calibration. Full report and install-ready receipts: `.ufo/waves/round-83/w1/HistoryReceiptR83/` (`report.txt`). No production edits or tools installed.

- V2: private historical clone at `a44b2f083ee8b4115aea64598646f4bd9e3c1470`; deployed `sources-census.sh validate --file` exited0 with exactly27 tab-separated W04 rows. Complete COMMAND/REV/EXIT/stdout/stderr in `r82-census-after.txt`, ready for `corpus/evidence/round83/r82-census-after.txt`. Separate registry census retained; no live registry relabeled.
- V3: `w1-results.json` actually has12 rows and no outer status fields:10 JSON-object outputs,1 nonterminal transcript (`RegistryCounterR82`),1 empty (`SweepGateR82`). Roles executor5/scribe2/scout1/connector1/reviewer1/critic1/mutation-tester1. `r82-seat-census.json` retains actual schema, per-seat classifications and source hashes; identical `r82-seat-counts.json` matches the check's requested install filename. Compatibility `final_terminal=10` means JSON-object outputs, NOT explicit terminal statuses.
- Historical affected=6, unrecovered=2, recovered=4 comes from pinned outside spotcheck lines173–177, separately from final-output classifications. Affected: SweepGateR82, SweepHarvestR82, ReviewerR82, CriticR82, MutationR82, RegistryCounterR82. Recovered: SweepHarvestR82, ReviewerR82, CriticR82, MutationR82. No provider events inferred from final statuses.
- V4: both C2 scripts added at `82fe89d5dd29fa4c1bb8d85399d9e43442d1b862`; independent log and show receipts retained. File-filtered show at alleged `c804dd41` is empty, exit0.
- Peer-requested preservation digest retained in `r82-report-preservation.json` and receipt: fleet report at `c839b658102dbcc401c78bbb7ea3bb47f11a333d`, SHA256 `5a83443dc6544a76633ee42b90394cb1028a1abab18ee69ff54a4857758b0480`.

Only authorized historical probes/derivations ran; no general tests. Scratch cleaned after capture. L1 owns installation and C2 integration/sensitivity gates. No blockers; preserve classification caveat in lesson wording.
