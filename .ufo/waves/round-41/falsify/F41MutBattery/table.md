| fixture | kind | caught by | observed after mutation |
|---|---|---|---|
| r_ctl-t06-empty-equal-receipt | stub-bytes | WRONG | rc=1 obs=differ:corpus/evidence/round41/r-ctl-probe.txt |
| r_ctl-t06-tamper-on-skipped | trigger-removed | WRONG | rc=0 obs=control:differ,equal:corpus/evidence/round41/r-ctl-probe.txt |
| r_ctl-t08-derived-uv-absent | expect-flip | WRONG | rc=0 obs=control:differ,equal:corpus/evidence/round35/tb2-grader-probe.txt,skip:corpus/ev |
| r_ctl-t08-table-uv-absent | trigger-removed | WRONG | rc=0 obs=control:differ,equal:corpus/evidence/round36/regex-log-probe.txt,equal:corpus/ev |
| r_map-t09-shared-stem-case-fold | trigger-removed | WRONG | rc=0 obs=map:corpus/evidence/r/foo-probe.txt:derived |
| r_map-t09-shared-stem-separators | defects-drop | WRONG | rc=0 obs=skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command |
| r_map-t10-derived-deep-layout | defects-drop | WRONG | rc=0 obs=map:corpus/evidence/round41/scheduling/foo-probe.txt:derived |
| r_map-t10-derived-mapping | trigger-removed | WRONG | rc=0  |
| r_map-t10-derived-with-table-sibling | defects-add | WRONG | rc=0 obs=map:corpus/evidence/r/foo-probe.txt:derived,map:corpus/evidence/round36/regex-lo |
| r_map-t11-table-near-stem-decoy | trigger-removed | **survived** | rc=0 obs=map:corpus/evidence/round35/tb2-grader-probe.txt:table |
| r_map-t11-table-overrides-derived | trigger-removed | **survived** | rc=0 obs=map:corpus/evidence/round35/tb2-grader-probe.txt:table,map:corpus/evidence/round |
| r_map-t12-log-derived | trigger-removed | WRONG | rc=0 obs=skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command |
| r_map-t12-log-population | defects-drop | WRONG | rc=0 obs=skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command |
| r_map-t12-log-with-table-sibling | trigger-removed | **survived** | rc=0 obs=map:corpus/evidence/round36/regex-log-probe.txt:table,skip:corpus/evidence/r/foo |
| r_run-t03-rc-nonzero-mixed | trigger-removed | WRONG | rc=0 obs=control:differ,equal:corpus/evidence/round42/census-probe.txt,equal:corpus/evide |
| r_run-t03-rc-nonzero-single | expect-flip | WRONG | rc=1 obs=differ:corpus/evidence/round43/audit-probe.txt |
| r_run-t04-temp-paths-masked | stub-bytes | WRONG,SURVIVED:T04 | rc=1 obs=differ:corpus/evidence/round36/regex-log-probe-first-run.txt |
| r_run-t13-auto-control-differ | trigger-removed | WRONG | rc=1 obs=control:differ,differ:corpus/evidence/round42/stable-census-probe.txt,equal:corp |
| r_setup-t01-lane-absent | trigger-removed | **survived** | rc=2  |
| r_setup-t01-not-a-repo | trigger-removed | WRONG | rc=0 obs=map:corpus/evidence/r/foo-probe.txt:derived |
| r_setup-t02-evidence-is-file | expect-flip | WRONG | rc=2  |
| r_setup-t02-no-evidence | trigger-removed | WRONG | rc=0 obs=map:corpus/evidence/r/foo-probe.txt:derived |
| r_setup-t05-tamper-absent | trigger-removed | WRONG | rc=0 obs=control:differ,equal:corpus/evidence/r/foo-probe.txt |
| r_setup-t05-tamper-unmapped | trigger-removed | WRONG | rc=1 obs=control:unavailable,equal:corpus/evidence/r/foo-probe.txt,skip:corpus/evidence/r |
| r_setup-t07-lane-subdir | trigger-removed | **survived** | rc=2  |
| r_setup-t07-nested-lane | expect-flip | WRONG | rc=2  |
| s_exit-absent-id | trigger-removed | WRONG | rc=0  |
| s_exit-attest-opened | trigger-removed | WRONG | rc=5  |
| s_exit-collision-admit | trigger-removed | WRONG | rc=0  |
| s_exit-collision-indented | trigger-removed | WRONG | rc=0  |
| s_exit-opened-elsewhere | trigger-removed | WRONG | rc=0  |
| s_exit-queued-admit | trigger-removed | WRONG | rc=0  |
| s_modes-s01-quote-plus-package | trigger-removed | WRONG | rc=0  |
| s_modes-s01-quote-plus-registry-and-package | trigger-removed | WRONG | rc=0  |
| s_modes-s04-url-map-with-adopt | trigger-removed | WRONG | rc=0  |
| s_modes-s04-url-map-with-check-only | expect-flip | WRONG | rc=2  |
| s_modes-s08-artifact-without-quote-file | trigger-removed | WRONG | rc=0  |
| s_modes-s08-quote-file-without-artifact | trigger-removed | WRONG | rc=0  |
| s_modes-s09-url-map-directory | trigger-removed | WRONG | rc=9  |
| s_modes-s09-url-map-nested-shape | trigger-removed | WRONG | rc=0  |
| s_usage-02-package-without-registry | trigger-removed | WRONG | rc=0  |
| s_usage-02-registry-without-package | trigger-removed | WRONG | rc=0  |
| s_usage-03-dotted-access-date | defects-breach | SETUP | rc=-  |
| s_usage-03-single-digit-month-duplicate-request | trigger-removed | WRONG | rc=5  |
| s_usage-05-empty-entries-value | expect-flip | WRONG | rc=2  |
| s_usage-05-two-ids-without-entries | trigger-removed | WRONG | rc=0  |
| s_usage-06-recheck-cadence-word | trigger-removed | WRONG | rc=0  |
| s_usage-06-recheck-prose-scoped-row | trigger-removed | WRONG | rc=0  |
