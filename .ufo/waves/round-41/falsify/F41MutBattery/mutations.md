# Round-41 F41MutBattery — fixture-mutant change receipts

One mutant per battery41 fixture; applied to a scratch copy of the whole battery
(`bat/<fid>/`), never to the lane. `old → new` is the exact byte replacement in the
module named by the receipt file `runs/mut-<fid>.txt`.

- **r_ctl-t06-empty-equal-receipt** [stub-bytes]: `run="python3 plans/r_ctl_probe.py", out="", rc=0)` → `run="python3 plans/r_ctl_probe.py", out="X", rc=0)`
- **r_ctl-t06-tamper-on-skipped** [trigger-removed]: `run="uv run --no-project python3 plans/r_ctl_probe.py",⏎            out="a receipt whose …` → `run="python3 plans/r_ctl_probe.py",⏎            out="a receipt whose probe needs uv`
- **r_ctl-t08-derived-uv-absent** [expect-flip]: `"fid": "r_ctl-t08-derived-uv-absent", "tool": "receipts", "expect": "accept"` → `"fid": "r_ctl-t08-derived-uv-absent", "tool": "receipts", "expect": "reject"`
- **r_ctl-t08-table-uv-absent** [trigger-removed]: `run="uv run --no-project python3 plans/build_pmars_probe.py"` → `run="python3 plans/build_pmars_probe.py"`
- **r_map-t09-shared-stem-case-fold** [trigger-removed]: `"plans/FooProbe.py": stub("FooProbe"), ` → ``
- **r_map-t09-shared-stem-separators** [defects-drop]: `f"skip:{EV_R}:no-committed-re-run-command"], "build": b_shared_stem_separators}` → `[], "build": b_shared_stem_separators}`
- **r_map-t10-derived-deep-layout** [defects-drop]: `"defects": ["map:corpus/evidence/round41/scheduling/foo-probe.txt:derived"]` → `"defects": []`
- **r_map-t10-derived-mapping** [trigger-removed]: `{EV_R: "X\n", "plans/foo_probe.py": stub("foo_probe"), "plans/bar_probe.py": stub("bar_pr…` → `{"plans/foo_probe.py": stub("foo_probe"), "plans/bar_probe.py": stub("bar_probe"),`
- **r_map-t10-derived-with-table-sibling** [defects-add]: `"map:corpus/evidence/round36/regex-log-probe.txt:table"], "build": b_derived_with_table_s…` → `"map:corpus/evidence/round36/regex-log-probe.txt:table", "equal:corpus/evidence/r/foo-pro…`
- **r_map-t11-table-near-stem-decoy** [trigger-removed]: `"plans/tb2_grader_probe_v2.py": stub("tb2_grader_probe_v2")}` → `}`
- **r_map-t11-table-overrides-derived** [trigger-removed]: `TB2: "tb2\n", "plans/tb2_grader_probe.py": stub("tb2_grader_probe"),⏎                  PM…` → `TB2: "tb2\n",⏎                  PMARS:`
- **r_map-t12-log-derived** [trigger-removed]: `"plans/foo_probe.py": stub("foo_probe"), "plans/unrelated.py": stub("unrelated")})` → `"plans/unrelated.py": stub("unrelated")})`
- **r_map-t12-log-population** [defects-drop]: `f"skip:{EV_LOG}:no-committed-re-run-command"], "build": b_log_population}` → `[], "build": b_log_population}`
- **r_map-t12-log-with-table-sibling** [trigger-removed]: `"plans/foo_probe_v2.py": stub("foo_probe_v2"), ` → ``
- **r_run-t03-rc-nonzero-mixed** [trigger-removed]: `probe("rc_ledger_probe", bad, rc=7)` → `probe("rc_ledger_probe", bad)`
- **r_run-t03-rc-nonzero-single** [expect-flip]: `"fid": "r_run-t03-rc-nonzero-single", "tool": "receipts", "expect": "reject"` → `"fid": "r_run-t03-rc-nonzero-single", "tool": "receipts", "expect": "accept"`
- **r_run-t04-temp-paths-masked** [stub-bytes]: `print("rows=3")` → `print("rows=4")`
- **r_run-t13-auto-control-differ** [trigger-removed]: `probe("stable_census_probe", a)` → `probe("stable_census_probe", a, rc=3)`
- **r_setup-t01-lane-absent** [trigger-removed]: `return listing(d / "absent")` → `return listing(d)`
- **r_setup-t01-not-a-repo** [trigger-removed]: `return listing(d / "plain")` → `return listing(tree(ctx, d / "plain", {RECEIPT: "X", "plans/foo_probe.py": PROBE}))`
- **r_setup-t02-evidence-is-file** [expect-flip]: `"fid": "r_setup-t02-evidence-is-file", "tool": "receipts", "expect": "error"` → `"fid": "r_setup-t02-evidence-is-file", "tool": "receipts", "expect": "accept"`
- **r_setup-t02-no-evidence** [trigger-removed]: `"plans/foo_probe.py": PROBE})` → `"plans/foo_probe.py": PROBE,⏎                                  EV + "/r/foo-probe.txt": "…`
- **r_setup-t05-tamper-absent** [trigger-removed]: `"--tamper", "corpus/evidence/nope.txt"` → `"--tamper", RECEIPT`
- **r_setup-t05-tamper-unmapped** [trigger-removed]: `"corpus/evidence/r/bar-probe.log": "X\n"})` → `"corpus/evidence/r/bar-probe.log": "X\n", "plans/bar_probe.py": PROBE})`
- **r_setup-t07-lane-subdir** [trigger-removed]: `return listing(root / "sub")` → `return listing(root)`
- **r_setup-t07-nested-lane** [expect-flip]: `"fid": "r_setup-t07-nested-lane", "tool": "receipts", "expect": "error"` → `"fid": "r_setup-t07-nested-lane", "tool": "receipts", "expect": "reject"`
- **s_exit-absent-id** [trigger-removed]: `return argv + admit("S199")` → `return argv + admit("S170")`
- **s_exit-attest-opened** [trigger-removed]: `return argv + admit("S161", extra=("--attest-opened",))` → `return argv + admit("S161")`
- **s_exit-collision-admit** [trigger-removed]: `[row("S121"), row("S122", opened="2026-10-25"), row("S123")]` → `[row("S121"), row("S142", opened="2026-10-25"), row("S123")]`
- **s_exit-collision-indented** [trigger-removed]: `[row("S130"), row("S131", opened="2026-10-24")]` → `[row("S130"), row("S141", opened="2026-10-24")]`
- **s_exit-opened-elsewhere** [trigger-removed]: `[row("S160", opened="2026-09-30")]` → `[row("S160")]`
- **s_exit-queued-admit** [trigger-removed]: `[row("S150", status="queued")]` → `[row("S150")]`
- **s_modes-s01-quote-plus-package** [trigger-removed]: `return ["--quote-file", quote_file(ctx, d), "--artifact", art,⏎            "--package", s…` → `return ["--quote-file", quote_file(ctx, d), "--artifact", art]`
- **s_modes-s01-quote-plus-registry-and-package** [trigger-removed]: `"--registry", str(d / "corpus" / "SOURCES.md"),⏎            "--package", str(d / "corpus"…` → `"--url-map", str(d / "corpus" / "evidence" / "r41-url-map.json")]`
- **s_modes-s04-url-map-with-adopt** [trigger-removed]: `"--access-date", "2026-10-26", "--url-map", str(d / "plans" / "url-map-r41.json")]` → `"--access-date", "2026-10-26"]`
- **s_modes-s04-url-map-with-check-only** [expect-flip]: `fx("s_modes-s04-url-map-with-check-only", "error", b_s04_check)` → `fx("s_modes-s04-url-map-with-check-only", "accept", b_s04_check)`
- **s_modes-s08-artifact-without-quote-file** [trigger-removed]: `return ["--artifact", art]` → `return ["--quote-file", quote_file(ctx, d), "--artifact", art]`
- **s_modes-s08-quote-file-without-artifact** [trigger-removed]: `lane_tree(ctx, d)⏎    ctx.write` → `art = lane_tree(ctx, d)⏎    ctx.write` ; `return ["--quote-file", quote_file(ctx, d, rid="S903"),` → `return ["--quote-file", quote_file(ctx, d, rid="S903"), "--artifact", art,`
- **s_modes-s09-url-map-directory** [trigger-removed]: `"--url-map", str(d / "corpus" / "evidence" / "r41-url-maps")]` → `"--url-map", str(d / "corpus" / "evidence" / "r41-url-maps" / "inner.json")]`
- **s_modes-s09-url-map-nested-shape** [trigger-removed]: `'{"b-capture.txt": {"url": "' + CITED + '"}}\n'` → `'{"b-capture.txt": "' + CITED + '"}\n'`
- **s_usage-02-package-without-registry** [trigger-removed]: `return ["--package", str(pkg), "--admit-ids", "S131", "--entries", ENTRY,` → `return ["--registry", str(_reg), "--package", str(pkg), "--admit-ids", "S131", "--entries…`
- **s_usage-02-registry-without-package** [trigger-removed]: `return ["--registry", str(reg), "--admit-ids", "S131", "--entries", ENTRY,` → `return ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S131", "--entries"…`
- **s_usage-03-dotted-access-date** [defects-breach]: `fx("s_usage-03-dotted-access-date", "error", b03a)` → `{"fid": "s_usage-03-dotted-access-date", "tool": "sources", "expect": "error", "defects":…`
- **s_usage-03-single-digit-month-duplicate-request** [trigger-removed]: `"--access-date", "2026-1-5"]` → `"--access-date", "2026-10-26"]`
- **s_usage-05-empty-entries-value** [expect-flip]: `fx("s_usage-05-empty-entries-value", "error", b05b)` → `fx("s_usage-05-empty-entries-value", "accept", b05b)`
- **s_usage-05-two-ids-without-entries** [trigger-removed]: `"--admit-ids", "S131,S132",⏎            "--access-date", "2026-10-26"]` → `"--admit-ids", "S131,S132", "--entries", ENTRY,⏎            "--access-date", "2026-10-26"]`
- **s_usage-06-recheck-cadence-word** [trigger-removed]: `"--recheck", "monthly"]` → `"--recheck", "180d"]`
- **s_usage-06-recheck-prose-scoped-row** [trigger-removed]: `"--recheck", "every 30 days", "--scope-to-admit"]` → `"--recheck", "180d", "--scope-to-admit"]`
