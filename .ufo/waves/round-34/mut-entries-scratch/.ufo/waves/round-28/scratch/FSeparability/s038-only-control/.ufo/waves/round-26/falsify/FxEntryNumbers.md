# FxEntryNumbers — scoped numerical audit

Scope: numerical and date assertions in the unadmitted draft `corpus/knowledge/grader-perturbation-audit.md` (source: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/drafts/grader-perturbation-audit.md`). No production prose was edited.

## Findings

No surviving numerical or date mismatch found in the current draft. The recorded F1/F2 MULTI counterexample is a real scoped failure, accurately stated; it is not a discrepancy in its reported counts.

## Independent counts / commands

Commands ran against `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (exit codes printed):

- Command, cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`: `python3 plans/grader_perturb.py --summary; rc=$?; printf 'EXIT=%s\n' "$rc"`; observed `EXIT=0`. Parsed `FAMILY` n/k: F1 1819/1802; F2 1819/1802; F3 1964/1964; F4 1720/1720; F5 1964/1964; F6 1964/1964; F7 1876/1876; D1 909/909; G1 1021/1021; G2 1021/1021. Exact summary lines: `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`; `FORMATS FJ1=1296 FJM=492 MULTI=31 DANGLE=57 BARE=88`; `DEDUP raw+want+grader unique_raw_want_grader=1451 duplicate_groups=294 records_in_duplicate_groups=807 excess_duplicate_records=513`.
- `python3 plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin; rc=$?; printf 'EXIT=%s\n' "$rc"` → `EXIT=0`: `POPULATION candidates=1964 included=1964 excluded=0`; `EXCLUDED baseline=0 missing_want=0 meta_truth=0`. Its all-family n/k pairs exactly match those listed above.
- Exact manifest count command, cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`: `awk -F '\t' 'NR>1 {key=$1 FS $6; total[key]++; if ($7=="true") pass[key]++; else if ($7=="false") fail[key]++; else invalid[key]++} END {for (key in total) printf "%s total=%d pass=%d fail=%d invalid=%d\n", key, total[key], pass[key], fail[key], invalid[key]}' plans/fixtures/r26/perturb_population.tsv | sort; rc=$?; printf 'EXIT=%s\n' "$rc"` → `EXIT=0`.
- Awk output: `corpus/evidence/round11-power/results-r11.jsonl state total=320 pass=136 fail=184 invalid=0`; `corpus/evidence/round12-ladder/results-r12.jsonl seq total=240 pass=17 fail=223 invalid=0`; `corpus/evidence/round12-ladder/results-r12.jsonl state total=1088 pass=668 fail=420 invalid=0`; `corpus/evidence/round8-horizon/results.jsonl c total=16 pass=13 fail=3 invalid=0`; `corpus/evidence/round8-horizon/results.jsonl state total=172 pass=112 fail=60 invalid=0`; `corpus/evidence/round9-replication/results-r9.jsonl state total=128 pass=75 fail=53 invalid=0`; `EXIT=0`.
- Manifest generator check, cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`: `python3 -B /tmp/kengaku-r26-ExecPopulationManifest-scratch/gen_perturb_population.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --check; rc=$?; printf 'EXIT=%s\n' "$rc"` → `EXIT=0`: `TOTAL n=1964 include=1964 exclude=0 pass=1021 fail=943 graders={'state': 1708, 'c': 16, 'seq': 240}`; `META grader.py truth builders: checks=54 mismatches=0`; `SECONDARY stored-field replay diffs: 0`; `CHECK ok`.
- `sha256sum -c plans/fixtures/r26/perturb_population.sha256; rc=$?; printf 'EXIT=%s\n' "$rc"` → `EXIT=0`: `corpus/evidence/round8-horizon/results.jsonl: OK`; `corpus/evidence/round9-replication/results-r9.jsonl: OK`; `corpus/evidence/round11-power/results-r11.jsonl: OK`; `corpus/evidence/round12-ladder/results-r12.jsonl: OK`.

Core output also confirms the table strata: F1/F2 `MULTI=31/14@[17/0;14/14]`, i.e. 17/17 baseline-PASS flips and 14/14 baseline-FAIL unchanged. Build evidence `ExecFamilyEdges.md:11,17-18` independently identifies the 31 as r8 B multi-fence records and the operation-9 extraction effect. The CP95 family bounds in core output are F1/F2 `[0.985079,0.994547]`, F3/F5/F6 `[0.998124,1]`, F4 `[0.997858,1]`, F7 `[0.998036,1]`, G1/G2 `[0.996394,1]`; all nine MP/MC lower bounds exceed the configured 0.95 bar. `attrib_calibration.py:144-152` defines exact two-sided CP; `grader_perturb.py:17,469-476` uses lower≥bar for PASS. F1/F2 composite `187/194`, `[0.927072,0.985372]`, INDETERMINATE is also exact.

Current draft lines 81-85 already show D1's separate PC interval `[0.995950,1.000000]`, file+pid `129/129` interval `[0.971809,1.000000]`, all five format strata, and the 26 DANGLE/BARE cases. Thus the earlier FxFamilyD1 omission note does not describe this current draft copy.

## Dates and sources

Draft `verified-at: 2026-10-21` matches the assigned review date; `date -u -d '2026-10-21 +90 days' '+%F'` printed `2027-01-19` (exit 0), consistent with its 90-day recheck. Reopened S048 supports §2.2, PDF p.3 / proceedings p.4904. S044 identifies v3 dated 25 Feb 2025; PyPI metadata gives evalmut 0.1.0 upload date 2026-08-10; Python 3.15.0 docs line 523 support the quoted `\s` whitespace set. No date conflict found.

LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no status/references/definition/diagnostics endpoint was mounted. No grep result is used as semantic proof. No tools installed; no build, lint, or additional test run.

VERDICT: PASS — scoped numeric/date assertions for `corpus/knowledge/grader-perturbation-audit.md` match the independent oracle, manifest, pinned population, and source checks; this does not decide novelty, Q13, or admission.