# RoundStateScoutR73 — planning data-walk

Captured 2026-11-04T02:52:31.523826+00:00. Axes: coverage; calibration.

## Scope and method

Observed source snapshot: HEAD `255c261db2119906c70195291a2b6f9f46f82a72` (freeze commit, not a landing-tip claim); SKILL.md was concurrently modified. Plans documents are enumerated lexically using the frozen gate’s exact `CMD` regex at `plans/round52_c2_registry.py:36`; `collect` at lines 105–125 filters nonexistent paths. File counts retain zero-command files. Command forms below are literal command-to-line/backtick excerpts, not shell-parsed invocations. A multiline continuation is not invented.

LSP unavailable: `read xd://lsp` returned “No such tool”; source references below are lexical evidence, not semantic LSP proof. No tools installed.

## Table 1 — plans advertisements per file

| File | Command occurrences | Distinct scripts | Distinct line forms | Paths and command forms |
|---|---:|---:|---:|---|
| plans/attrib-r21-frozen.md | 1 | 1 | 1 | `python3 plans/attrib_probe.py block-sha` |
| plans/attrib-r22-frozen.md | 1 | 1 | 1 | `python3 plans/attrib_probe.py block-sha --frozen` |
| plans/attrib-r23-frozen.md | 0 | 0 | 0 | — |
| plans/probe-battery-TEMPLATE.md | 0 | 0 | 0 | — |
| plans/probe-battery-r19.md | 0 | 0 | 0 | — |
| plans/round-24-claims.md | 2 | 1 | 1 | `python3 grader.py` |
| plans/round-25-claims.md | 2 | 2 | 2 | `python3 plans/attrib_calibration.py --summary`<br>`python3 plans/state_check.py --summary` |
| plans/round-26-claims.md | 4 | 3 | 4 | `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-<N>.md --commit <landing>`<br>`python3 plans/grader_perturb.py [--root DIR] [--summary\|--json] [--selftest]`<br>`python3 plans/grader_perturb.py --summary`<br>`python3 plans/state_check.py --summary` |
| plans/round-27-claims.md | 3 | 2 | 3 | `python3 plans/parser_policy_compare.py [--root DIR] [--summary\|--json] [--selftest]`<br>`python3 plans/parser_policy_compare.py --summary`<br>`python3 plans/state_check.py --summary` |
| plans/round-28-claims.md | 2 | 2 | 2 | `python3 plans/benchmark_spec_audit.py --summary`<br>`python3 plans/registry_check.py --summary` |
| plans/round-29-attempt2-claims.md | 3 | 2 | 3 | `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census`<br>`python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json`<br>`python3 plans/sources_adopt.py --selftest` |
| plans/round-29-claims.md | 1 | 1 | 1 | `python3 plans/config_projection.py --summary` |
| plans/round-30-claims.md | 5 | 3 | 3 | `python3 plans/adoption_check.py --expect`<br>`python3 plans/round30_defects.py --lane .`<br>`python3 plans/sources_adopt.py --selftest` |
| plans/round-31-claims.md | 5 | 3 | 3 | `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census`<br>`python3 plans/round31_defects.py --lane .`<br>`python3 plans/sources_adopt.py --selftest` |
| plans/round-32-claims.md | 6 | 4 | 4 | `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census`<br>`python3 plans/round32_c1_verify.py --lane .`<br>`python3 plans/round32_defects.py --lane .`<br>`python3 plans/catalog_probe.py --diff --lane .` |
| plans/round-33-claims.md | 6 | 4 | 4 | `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census`<br>`python3 plans/round33_c1_verify.py --lane .`<br>`python3 plans/round33_defects.py --lane .`<br>`python3 plans/catalog_probe.py --verify --lane .` |
| plans/round-34-claims.md | 5 | 3 | 4 | `python3 plans/round34_c1_verify.py --lane .`<br>`python3 plans/round34_mutate.py`<br>`python3 plans/round34_defects.py --lane .`<br>`python3 plans/round34_defects.py --selftest` |
| plans/round-35-claims.md | 2 | 2 | 2 | `python3 plans/round35_c1_verify.py --lane .`<br>`python3 plans/defect_ledger.py --lane .` |
| plans/round-36-claims.md | 2 | 2 | 2 | `python3 plans/round36_c1_verify.py --lane .`<br>`python3 plans/round36_c2_verify.py --lane .` |
| plans/round-37-claims.md | 2 | 2 | 2 | `python3 plans/round37_c1_verify.py --lane .`<br>`python3 plans/round37_c2_verify.py --lane .` |
| plans/round-38-claims.md | 4 | 2 | 2 | `python3 plans/round38_c1_verify.py --lane .`<br>`python3 plans/round38_c2_verify.py --lane .` |
| plans/round-39-claims.md | 4 | 2 | 2 | `python3 plans/round39_c1_verify.py --lane .`<br>`python3 plans/round39_c2_verify.py --lane .` |
| plans/round-40-claims.md | 4 | 2 | 2 | `python3 plans/round40_c1_verify.py --lane .`<br>`python3 plans/round40_c2_verify.py --lane .` |
| plans/round-41-claims.md | 4 | 2 | 2 | `python3 plans/round41_c1_verify.py --lane .`<br>`python3 plans/round41_c2_verify.py --lane .` |
| plans/round-42-claims.md | 4 | 2 | 2 | `python3 plans/round42_c1_verify.py --lane .`<br>`python3 plans/round42_c2_verify.py --lane .` |
| plans/round-43-claims.md | 4 | 2 | 2 | `python3 plans/round43_c1_verify.py --lane .`<br>`python3 plans/round43_c2_verify.py --lane .` |
| plans/round-44-claims.md | 4 | 2 | 2 | `python3 plans/round44_c1_verify.py --lane .`<br>`python3 plans/round44_c2_verify.py --lane .` |
| plans/round-45-claims.md | 2 | 2 | 2 | `python3 plans/round45_c1_verify.py --lane .`<br>`python3 plans/round45_c2_verify.py --lane .` |
| plans/round-46-claims.md | 3 | 3 | 3 | `python3 plans/round46_c1_verify.py --lane .`<br>`python3 plans/round46_c2_verify.py --lane .`<br>`python3 plans/round46_c3_verify.py --lane .` |
| plans/round-48-claims.md | 2 | 2 | 2 | `python3 plans/round48_c1_verify.py --lane .`<br>`python3 plans/round48_c2_verify.py --lane .` |
| plans/round-49-claims.md | 2 | 2 | 2 | `python3 plans/round49_c1_verify.py --lane .`<br>`python3 plans/round49_c2_verify.py --lane .` |
| plans/round-50-claims.md | 2 | 2 | 2 | `python3 plans/round50_c1_verify.py --lane .`<br>`python3 plans/round50_c2_audit.py --lane .` |
| plans/round-51-claims.md | 2 | 2 | 2 | `python3 plans/round51_surfaces.py --lane .`<br>`python3 plans/round51_routing.py --lane . --run-checks` |
| plans/round-52-claims.md | 2 | 2 | 2 | `python3 plans/round52_c1_grader_audit.py --lane .`<br>`python3 plans/round52_c2_registry.py --lane .` |
| plans/round-53-claims.md | 3 | 2 | 3 | `python3 plans/round53_c1_triage.py --lane .      # run on a clean clone of the landing tip`<br>`python3 plans/round53_c2_tipstate.py --lane . --source <clean shared clone of the landing tip> --work <scratch> [--jobs 4]`<br>`python3 plans/round53_c1_triage.py --lane .` |
| plans/round-54-claims.md | 3 | 2 | 3 | `python3 plans/round54_c1_anchor.py verify \`<br>`python3 plans/round54_c2_entrytruth.py --lane . --source CLEAN_CLONE --work SCRATCH \`<br>`python3 plans/round54_c2_entrytruth.py --lane . --dry` |
| plans/round-55-claims.md | 2 | 2 | 2 | `python3 plans/round52_c2_registry.py --lane <clone>`<br>`python3 plans/round55_c2_entryargv.py --lane <clone>` |
| plans/round-56-claims.md | 10 | 7 | 10 | `python3 plans/round52_c2_registry.py --lane <clone>`<br>`python3 plans/round55_c3_chess_probe.py --lane <clone>`<br>`python3 plans/round55_c2_entryargv.py --selftest`<br>`python3 grader.py`<br>`python3 grader.py --selftest`<br>`python3 plans/round56_landcheck.py --lane <clone>`<br>`python3 plans/tb2_grader_probe.py --lane .`<br>`python3 plans/round55_c2_entryargv.py --lane`<br>`python3 plans/round55_c2_controls.py --case abbreviated-selftest`<br>`python3 plans/round55_c2_entryargv.py --lane <clone>` |
| plans/round-57-claims.md | 2 | 2 | 2 | `python3 plans/round52_c2_registry.py --lane <clone>`<br>`python3 plans/round55_c2_entryargv.py --lane <clone>` |
| plans/round-58-claims.md | 5 | 4 | 5 | `python3 plans/anchor_line_check.py --lane .`<br>`python3 plans/round46_c2_verify.py --lane . --work <scratch>`<br>`python3 plans/anchor_line_check.py --selftest`<br>`python3 plans/round50_c1_verify.py`<br>`python3 plans/round58_c2_kl_probe.py --lane . --work <scratch> --receipt` |
| plans/round-59-claims.md | 2 | 1 | 1 | `python3 plans/round59_c1_openssl_probe.py --lane .` |
| plans/round-60-claims.md | 1 | 1 | 1 | `python3 plans/round59_c1_openssl_probe.py --lane . --work <scratch>` |
| plans/round-61-claims.md | 0 | 0 | 0 | — |
| plans/round-62-claims.md | 0 | 0 | 0 | — |
| plans/round-63-claims.md | 3 | 2 | 3 | `python3 plans/round63_c1_pypi_probe.py --check-receipt corpus/evidence/round63/pypi-probe.txt; echo $?`<br>`python3 plans/round63_c1_pypi_probe.py --check-receipt corpus/evidence/round63/pypi-probe.txt`<br>`python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt; echo $?` |
| plans/round-64-claims.md | 6 | 3 | 6 | `python3 plans/round64_c1_kvstore_probe.py --check-receipt corpus/evidence/round64/kvstore-probe.txt; echo $?`<br>`python3 plans/round64_c1_kvstore_probe.py --check-receipt`<br>`python3 plans/round63_gate_checks.py --selftest --work <scratch>; echo $?`<br>`python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .; echo $?`<br>`python3 plans/round63_gate_checks.py trio <file>`<br>`python3 plans/round64_trio_sweep.py --sweep --lane . ; echo $?` |
| plans/round-65-claims.md | 2 | 1 | 2 | `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt; echo $?`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt` |
| plans/round-66-claims.md | 7 | 2 | 7 | `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt; echo $?`<br>`python3 plans/round66_c1_tensor_probe.py --run --work <scratch> --receipt corpus/evidence/round66/tensor/receipt.txt`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt; echo $?`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict; echo $?`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt --strict; echo $?`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt; echo $?`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` |
| plans/round-67-claims.md | 3 | 2 | 3 | `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt <R> --strict`<br>`python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` |
| plans/round-68-claims.md | 7 | 4 | 5 | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt`<br>`python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt; echo $?`<br>`python3 plans/round68_c2_correction_gate.py`<br>`python3 plans/round68_report_contract.py <report> --shonen SHONEN.md`<br>`python3 plans/round68_capability_table.py --lane .` |
| plans/round-69-claims.md | 3 | 2 | 3 | `python3 plans/round69_c1_nginx_probe.py --lane . --work <scratch> --receipt corpus/evidence/round69/nginx/receipt.txt --evidence-dir corpus/evidence/round69/nginx/sandbox`<br>`python3 plans/round69_c1_nginx_probe.py --check-receipt corpus/evidence/round69/nginx/receipt.txt`<br>`python3 plans/round69_c2_routed_defects.py` |
| plans/round-70-claims.md | 4 | 2 | 4 | `python3 plans/round70_c1_nginx_probe.py --render-table`<br>`python3 plans/round70_c1_nginx_probe.py --lane . --work <scratch> --receipt corpus/evidence/round70/nginx/receipt.txt --evidence-dir corpus/evidence/round70/nginx/sandbox`<br>`python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt`<br>`python3 plans/round70_c2_routed_defects.py` |
| plans/round-71-claims.md | 3 | 2 | 3 | `python3 plans/round71_c1_hf_probe.py --lane . --work <scratch>`<br>`python3 plans/round71_c1_hf_probe.py --lane . --check-receipt`<br>`python3 plans/round71_c2_routed_defects.py --lane .` |
| plans/round-72-claims.md | 5 | 2 | 5 | `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/receipt.txt`<br>`python3 plans/round72_c1_hf_probe.py --lane . --work <scratch>/battery --receipt`<br>`python3 plans/round72_c1_hf_probe.py --lane . --check-receipt`<br>`python3 plans/round72_c1_hf_probe.py --lane . --work`<br>`python3 plans/round72_c2_routed_defects.py --lane .` |
| plans/round-73-claims.md | 6 | 3 | 6 | `python3 plans/round52_c2_registry.py --lane .`<br>`python3 plans/round52_c2_registry.py --selftest`<br>`python3 plans/round52_c2_registry.py --lane . ; echo "rc=$?"`<br>`python3 plans/round73_c2_registry_audit.py`<br>`python3 plans/round73_c2_registry_audit.py --lane . ; echo "rc=$?"`<br>`python3 plans/round72_c2_routed_defects.py --lane <fixture>` |
| plans/wwkd-round-16-recensus.md | 0 | 0 | 0 | — |
| plans/wwkd-round-17-coverage.md | 2 | 1 | 2 | `python3 grader.py`<br>`python3 grader.py --selftest` |

Union: **89** script paths; **82** exist; **7** absent. **86** union paths also occur in at least one of SCORECARD.md, SKILL.md, LOG.md, corpus/README.md in the captured scan (includes absent historical advertisements). Existing overlap: **82**.

## Table 2 — seven frozen missing-path entry probes

Command cwd: lane root. Commands: `python3 <path> --help` and `python3 <path> --lane .`. All seven help commands ran. No required imports prevented startup. The last three no-`--lane` interfaces were probed too, to distinguish a usage refusal from an unrun assumption.

| Script | Help rc | First usage line | Bare lane rc | Observed result |
|---|---:|---|---:|---|
| `plans/round32_c1_verify.py` | 0 | `usage: round32_c1_verify.py [-h] [--lane LANE] [--selftest]` | 1 | `DEFECT V2 cited-row-identity: the S094 registry row cites no URL checks=6 defects=1` |
| `plans/round32_defects.py` | 0 | `usage: round32_defects.py [-h] [--lane LANE] [--selftest]` | 1 | `DEFECT R2 round32-report-order-tip: the round-32 report does not cite the final lane tip ea41880fa7 checks=7 defects=1` |
| `plans/round66_c1_tensor_probe.py` | 0 | `usage: round66_c1_tensor_probe.py [-h] (--run \|` | 2 | `round66_c1_tensor_probe.py: error: one of the arguments --run --check-receipt --selftest is required` |
| `plans/round69_c1_nginx_probe.py` | 0 | `usage: round69_c1_nginx_probe.py [-h] [--lane LANE] [--work WORK]` | 2 | `SETUP work-dir-required` |
| `plans/round69_c2_routed_defects.py` | 0 | `usage: round69_c2_routed_defects.py [-h] [--root ROOT] [--selftest]` | 2 | `round69_c2_routed_defects.py: error: unrecognized arguments: --lane .` |
| `plans/round70_c1_nginx_probe.py` | 0 | `usage: round70_c1_nginx_probe.py [-h] [--lane LANE] [--work WORK]` | 2 | `SETUP work-dir-required` |
| `plans/round70_c2_routed_defects.py` | 0 | `usage: round70_c2_routed_defects.py [-h] [--root ROOT] [--selftest]` | 2 | `round70_c2_routed_defects.py: error: unrecognized arguments: --lane .` |

Both nginx entries return `SETUP work-dir-required`, not argparse usage errors. Their `main` dispatches (`round69_c1_nginx_probe.py:694–725`, `round70_c1_nginx_probe.py:879–911`) require `--work` before the battery and do not acquire the host lock on these bare runs. The round-32 counters run but return live historical defects (not startup failures).

## Table 3 — nonexistent plans-advertised paths

| Path | Advertising plans documents | Gate treatment |
|---|---|---|
| `plans/round34_c1_verify.py` | plans/round-34-claims.md | Filtered before coverage comparison |
| `plans/round34_defects.py` | plans/round-34-claims.md | Filtered before coverage comparison |
| `plans/round34_mutate.py` | plans/round-34-claims.md | Filtered before coverage comparison |
| `plans/round48_c1_verify.py` | plans/round-48-claims.md | Filtered before coverage comparison |
| `plans/round48_c2_verify.py` | plans/round-48-claims.md | Filtered before coverage comparison |
| `plans/round49_c1_verify.py` | plans/round-49-claims.md | Filtered before coverage comparison |
| `plans/round49_c2_verify.py` | plans/round-49-claims.md | Filtered before coverage comparison |

Non-gate concrete Python command tokens additionally seen in plans prose/fixtures: `main.py.c` (polyglot fixture), `/ctl/driver.py` (sandbox fixture). They are not lane instrument paths and are outside the frozen regex. Placeholder paths, interpreter versions and prose after “python3” are not counted as instruments.

## Table 4 — advertised instruments rejecting bare `--lane .`

Universe: all 113 existing instruments advertised by the full frozen gate surfaces, not just the plans subset. Every row below was actually invoked with `python3 <path> --lane .`, rc 2, and stderr containing `usage:`. Only candidate parser refusals and the seven required scripts were executed; other instrument bodies were not exercised. This is not a claim that every registry entry is bare `--lane .`: many correctly document `--root`, required modes or subcommands.

| Instrument | Advertised in plans | rc | Final usage error |
|---|---|---:|---|
| `grader.py` | yes | 2 | `grader.py: error: unrecognized arguments: --lane .` |
| `plans/attrib_calibration.py` | yes | 2 | `attrib_calibration.py: error: unrecognized arguments: --lane .` |
| `plans/attrib_probe.py` | yes | 2 | `attrib_probe.py: error: argument cmd: invalid choice: '.' (choose from 'block-sha', 'freeze-check', 'trials', 'force-trials', 'stream-trials', 'score')` |
| `plans/benchmark_spec_audit.py` | yes | 2 | `benchmark_spec_audit.py: error: unrecognized arguments: --lane .` |
| `plans/config_projection.py` | yes | 2 | `config_projection.py: error: unrecognized arguments: --lane .` |
| `plans/gate_flip_check.py` | no | 2 | `gate_flip_check.py: error: unrecognized arguments: --lane .` |
| `plans/gate_timing_check.py` | yes | 2 | `gate_timing_check.py: error: unrecognized arguments: --lane .` |
| `plans/grader_perturb.py` | yes | 2 | `grader_perturb.py: error: unrecognized arguments: --lane .` |
| `plans/parser_policy_compare.py` | yes | 2 | `parser_policy_compare.py: error: unrecognized arguments: --lane .` |
| `plans/pkg_gate.py` | no | 2 | `pkg_gate.py: error: argument cmd: invalid choice: '.' (choose from 'package', 'd4-line', 'd5-line')` |
| `plans/registry_check.py` | yes | 2 | `registry_check.py: error: unrecognized arguments: --lane .` |
| `plans/round28_census.py` | no | 2 | `round28_census.py: error: the following arguments are required: --revision` |
| `plans/round54_c1_anchor.py` | yes | 2 | `round54_c1_anchor.py: error: argument cmd: invalid choice: '.' (choose from 'stamp', 'upgrade', 'verify', 'selftest')` |
| `plans/round55_c2_controls.py` | yes | 2 | `round55_c2_controls.py: error: one of the arguments --case --selftest is required` |
| `plans/round63_gate_checks.py` | yes | 2 | `round63_gate_checks.py: error: argument cmd: invalid choice: '.' (choose from 'trio', 'depth', 'selftest')` |
| `plans/round66_c1_tensor_probe.py` | yes | 2 | `round66_c1_tensor_probe.py: error: one of the arguments --run --check-receipt --selftest is required` |
| `plans/round67_c1_pipeline_probe.py` | yes | 2 | `round67_c1_pipeline_probe.py: error: unrecognized arguments: --lane .` |
| `plans/round68_c2_correction_gate.py` | yes | 2 | `round68_c2_correction_gate.py: error: unrecognized arguments: --lane .` |
| `plans/round69_c2_routed_defects.py` | yes | 2 | `round69_c2_routed_defects.py: error: unrecognized arguments: --lane .` |
| `plans/round70_c2_routed_defects.py` | yes | 2 | `round70_c2_routed_defects.py: error: unrecognized arguments: --lane .` |
| `plans/scratch_guard.py` | no | 2 | `scratch_guard.py: error: argument command: invalid choice: '.' (choose from 'check', 'safe-rm', 'safe_rm')` |
| `plans/sources_adopt.py` | yes | 2 | `sources_adopt.py: error: unrecognized arguments: --lane .` |
| `plans/state_check.py` | yes | 2 | `state_check.py: error: unrecognized arguments: --lane .` |
| `plans/adoption_check.py` | yes | 2 | `adoption_check.py: error: the following arguments are required: --expect` |
| `plans/order_check.py` | no | 2 | `order_check.py: error: the following arguments are required: --claims, --receipt` |

Usage-error count: **25** across the full 113-script universe; **20** are plans-advertised. Additional manual parser refusal: `plans/stage_scan.py --lane .`, rc 2, stderr `ERROR unknown option --lane` (no usage banner); its `--help` also exits 2, `ERROR unknown option --help`. No startup/import failure observed in the other 112 help probes.

## Initial gate receipt and target arithmetic

Executed once: `python3 plans/round52_c2_registry.py --lane . ; echo "rc=$?"` (lane cwd). Exact output:

```text
UNIVERSE mode=full files=133 plans_only=3
ADVERTISED total=113
REGISTERED total=105 rows=107
MISSING 8
  MISSING plans/round32_c1_verify.py
  MISSING plans/round32_defects.py
  MISSING plans/round66_c1_tensor_probe.py
  MISSING plans/round69_c1_nginx_probe.py
  MISSING plans/round69_c2_routed_defects.py
  MISSING plans/round70_c1_nginx_probe.py
  MISSING plans/round70_c2_routed_defects.py
  MISSING plans/round73_c2_registry_audit.py
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 fail
PREDICATE R73-C1 fail
rc=1
```

Observed: the frozen Work paragraph names seven old missing instruments plus the new audit instrument, while the actual first gate names eight missing paths. The initial plans-only delta is the two round-32 instruments plus `round73_c2_registry_audit.py` advertised by the new round-73 claims document. `git diff --stat d96c3e62..HEAD -- plans/` showed only round-73 claims, amended gate, and new audit changed. [INFERENCE] The target 112 counts 110 legacy + two historical plans additions but omits the audit’s own advertisement; the observed freeze-tree count is 113. Do not edit a predicate/target to hide this discrepancy. Later SKILL registry-row advertisements can change `plans_only`, so this is a timestamped initial observation, not a landing verdict.

## PLAN-DATA

```text
plans_md_files=57
plans_command_occurrences=174
plans_script_union=89
plans_script_existing=82
plans_script_absent=7
plans_also_four_self_surfaces=86
plans_existing_also_four_self_surfaces=82
initial_full_advertised=113
initial_full_missing=8
initial_gate_rc=1
frozen_old_missing_requested=7
old_missing_help_run=7
old_missing_help_rc0=7
old_missing_lane_run=7
old_missing_lane_rc1=2
old_missing_lane_rc2_usage=3
old_missing_lane_rc2_setup=2
full_help_run=113
full_help_rc0=112
full_help_rc2_manual=1
full_bare_lane_usage_rc2=25
plans_bare_lane_usage_rc2=20
full_bare_lane_manual_rc2=1
reported_target_advertised=112
observed_target_delta=1
```

## Evidence limits and process notes

Enumeration/probe driver commands: `python3 <scratch>/scan.py <scratch>/scan.json` rc 0; Python subprocess driver ran each captured command with timeout 25 seconds, PYTHONDONTWRITEBYTECODE=1 and TMPDIR in this seat scratch. No probe timed out. Help rc/output and tested-entry rc/error lines are reproduced above. No build, linter, test suite, mutation test, selftest or landing check was run.

Unresolved: the L1 must reconcile the frozen 112 target against the initial 113 observation; no target or counting code was edited. The other supported `--lane` bodies were not run and are not asserted green. Confidence: high on captured literal advertisements, missing paths, and executed subprocess results; no semantic LSP coverage claimed.

Process defects: an initial shell command created scratch before the frozen claims read completed; early exploration used shell listing/search/paging rather than specialized tools, and an early help loop used a small `/tmp/h.<pid>` file which it removed. These are instruction deviations, not evidence that checks passed. Scratch is removed after both scoped reports are persisted. No installs or PATH-directory writes.
