# R37TipSweep — no-harm baseline at lane tip `44b7298` (round 37, wave 1)

Seat: executor (leaf). Scope: **measure only** — no lane file was edited, no plan/corpus/SCORECARD byte was
touched, nothing committed. All numbers below are from one sweep executed before landing, on a clean shared
clone of the lane tip.

## 0. Setup (reproducible)

- Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip `44b7298ae1e03791173097cef0e898285f238870`
  (`round-37: wave-1 spec and validated dispatch (40 seats, policy v1)`), worktree clean except untracked
  `.ufo/` wave files (verified `git -C <lane> status --porcelain` → only `??` paths).
- Clone: `git clone -q --shared <lane> /fast/scratch/hyaku/kengaku-r37/R37TipSweep/fx/lane`;
  `git -C … rev-parse --show-toplevel` equals the clone root (asserted before any run); `git status --porcelain`
  in the clone = **0 lines before and 0 lines after** the whole sweep.
- Scratch: `export TMPDIR=/fast/scratch/hyaku/kengaku-r37/R37TipSweep` (NVMe), per-case `mktemp` dirs land
  there; scratch removed at the end, receipts copied into `build/R37TipSweep/receipts/`.
- Runner: `receipts/run.sh` + `receipts/cmds.tsv`, 4-way parallel, per-command log + `summary.tsv`
  (label, exit, seconds, last non-empty line). **Total wall: 56 s** for all 27 commands.
- Every path in the table is relative to the clone root and was executed with `cwd` = clone root.

## 1. Baseline table (25/25 green)

| # | command | exit | last line (trimmed) | status | known/new |
|---|---|---|---|---|---|
| 1 | `python3 grader.py` | 0 | `VERDICT: PASS — stored evidence fully re-derives offline` | green | known |
| 2 | `python3 grader.py --selftest` | 0 | `[selftest] ALL PASS` | green | known |
| 3 | `python3 corpus/evidence/round13-coverage/coverage_census.py` | 0 | JSON, no `dangling`/`duplicate_rows`; knowledge 43/43 indexed, evidence 23/31, lessons 33/48 | green | known |
| 4 | `python3 plans/attrib_calibration.py --summary` | 0 | `TOTAL files=9 … scored_trials=92 correct=92 incorrect=0 estimates=35 … mismatches=0` | green | known |
| 5 | `python3 plans/attrib_calibration.py --selftest` | 0 | `selftest: 18 checks, 0 failed` | green | known |
| 6 | `python3 plans/state_check.py --summary` | 0 | `VERDICT: PASS — all comparable frozen assertions match` (`assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`) | green | known |
| 7 | `python3 plans/state_check.py --selftest` | 0 | `[selftest] ALL PASS (…)` | green | known |
| 8 | `python3 plans/grader_perturb.py --summary` | 0 | `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9` | green | known |
| 9 | `python3 plans/grader_perturb.py --selftest` | 0 | `SELFTEST TOTAL families=10 branch_cases=10 failed=0` | green | known |
| 10 | `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit b571944` | 0 | `gate_timing_check: commit=b571944 lesson=corpus/lessons/round-26.md admissions=1 passed=1 failed=0 second-seat-reports=53` | green | known |
| 11 | same, `--commit HEAD` | 0 | identical summary with `commit=HEAD` | green | known |
| 12 | `python3 plans/gate_timing_check.py --selftest` | 0 | `[selftest] ALL PASS (five allowed roles; …)` | green | known |
| 13 | `python3 plans/benchmark_spec_audit.py --summary` | 0 | `TOTAL task_count=812 distinct_task_ids=812 … findings=0 exit=0` | green | known |
| 14 | `python3 plans/benchmark_spec_audit.py --selftest` | 0 | `SELFTEST clean cases=67 …` | green | known |
| 15 | `python3 plans/registry_check.py --summary` | 0 | `TOTAL source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0 exit=0` | green | known |
| 16 | `python3 plans/registry_check.py --selftest` | 0 | `SELFTEST clean cases=15 …` | green | known |
| 17 | `python3 plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0` | green | known |
| 18 | `python3 plans/config_projection.py --selftest` | 0 | `SELFTEST clean cases=31 …` | green | known |
| 19 | `python3 plans/sources_adopt.py` (registry entry, no args) | 2 | `error: --registry and --package are required unless --selftest` | green (documented usage exit `2`) | known |
| 20 | `python3 plans/sources_adopt.py --selftest` | 0 | `SELFTEST cases=17 failed=0` | green | known |
| 21 | `python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json --rerun --require-clean-tree` | 0 | `defects=0` (P1–P10 all `ok`; `P10 ok probe_rerun=byte-equal bytes=3399`, `P9 ok untracked=0`) | green | known |
| 22 | `python3 plans/round36_c1_verify.py --lane .` | 0 | `PREDICATE C1 pass` (`FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`) | green | known |
| 23 | `python3 plans/round36_c2_verify.py --lane .` | 0 | `PREDICATE C2 pass` (`W1…W6 ok`, `checks=6 defects=0`) | green | known |
| 24 | `python3 plans/regex_log_probe.py --lane .` + `cmp` vs `corpus/evidence/round36/regex-log-probe.txt` | 0 | `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; cmp **byte-equal**, sha256 `439101fa2eac0e79ebec088ab47d9fc4481df0ec12d0ebc6c3475319d426a2be` | green | known |
| 25 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` | 0 | `file	ok	<clone>/corpus/SOURCES.md` after **15** `W04` duplicate-url warnings (same 15 as `claims/census-before.txt`) | green | known |

Registry coverage: the 13 rows of `SKILL.md` §Gate/probe registry (lines 560–575) are rows 1, 3, 4, 6, 8, 10,
13, 15, 17, 19, 21, 22, 24; each row's declared self-test column is rows 2, 5, 7, 9, 12, 14, 16, 18, 20 (plus
row 23, which is the declared self-test of `regex-log-probe`) and row 11 is the second REV the row's control
names. The only exit `2` in the table is row 19's documented usage error; no gate/probe row returned an
unevaluated verdict.

## 2. Wave-1 falsifier counters at the same tip — red **by design**, exactly as frozen

These are not baseline failures; they are the frozen "before" state and must flip after landing.

| command | exit | output | frozen control it matches |
|---|---|---|---|
| `python3 plans/round37_c1_verify.py --lane .` | 1 | `BATTERY fixtures=14 wrong=0 renamed_disagree=0` / `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0` / `PREDICATE C1 fail` | `claims/control-c1-nothing.txt` (same three lines) |
| `python3 plans/round37_c2_verify.py --lane .` | 1 | `V1 ok listed=6 bad=0 extra=0`; `V2 DEFECT gate_exit=1`; `V3 DEFECT rows=3 bad=['S111:row','S112:row','S113:row']`; `V4 DEFECT receipt or entry absent`; `V5 ok probe=frozen dry_byte_equal=True`; `V6 ok census_exit=0`; `V7 DEFECT receipt or entry absent`; `checks=7 defects=4` / `PREDICATE C2 fail` | `claims/control-c2-nothing.txt` (`checks=7 defects=4`, same V-set) |

Timing: C1 26 s, C2 53 s (the two slowest commands in the sweep; everything else ≤2 s).

## 3. No-harm invariants (the actual deliverable for the L1)

1. **Tree-unchanged after the sweep**: clone `git status --porcelain` = 0 lines immediately before the sweep
   and 0 lines immediately after all 27 commands. `pkg_gate --rerun` re-executed the package probe and left
   no residue in the tree; `--require-clean-tree` was satisfied (`P9 ok untracked=0`).
2. **Lane untouched**: no `git add/commit/stash/checkout/reset/push/pull`, no jj command, no write to the lane
   beyond `build/R37TipSweep/`. The lane's untracked `??` set changed during the wave only through *other*
   seats (`assimilation/`, `make_falsify_spec.py` appeared; this seat created none of them).
3. **Freeze identity confirmed at the measured tree**: `plans/pkg_gate.py` sha256
   `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` — equal to the freeze digest named in
   `plans/round-37-claims.md` §C1; `plans/git_webserver_probe.py` sha256
   `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf` (freeze `63cb75cf…5eedf`).
   `plans/round37_c1_verify.py` `dbc9f719…`, `plans/round37_c2_verify.py` `b8cba11a…`.
4. **Post-landing comparison line**: after wave 1 lands, re-run the same 27 commands; the contract is
   *25/25 stay green*, row 22 becomes `killed=55 survived=0 … PREDICATE C1 pass` and row 23 becomes
   `checks=7 defects=0 … PREDICATE C2 pass`.

## 4. Freshness / operability observations

- **Pending artifacts are genuinely absent at the tip**, which is why C1/C2 are red: `plans/battery37/` does
  not exist and `corpus/knowledge/tb2-git-webserver-grader.md` does not exist (`ls` → `No such file or
  directory`). `corpus/evidence/round37/` *is* present at the freeze commit: the tb2 captures verify
  (`sha256sum -c SHA256SUMS` → `instruction.md/solve.sh/task.toml/test.sh/test_outputs.py/verify.sh: OK`,
  6/6) and the receipt ends `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, matching the frozen claim.
- **Registry addendum is stale, gate is fine**: §Gate/probe registry's paragraph after the table says the
  `coverage-census` script "lands with the census seat's artifact in this wave"; the script is present at the
  tip and exits 0 (row 3). Registry *text* accuracy, not a gate defect — left for the L1, not edited here.
- **`grader-perturb` exit 0 hides a live FAIL by contract**: its verdict map is "`0` audit completed,
  *including* family FAIL findings", and the audit reports `MULTI=31/14@0.452` under `F1`/`F2` (F1/F2
  `verdict=PASS` at composite level, `D1 verdict=NOT_SCORED`). Green here means "the audit ran", not "all
  families pass"; do not read row 8 as evidence that MULTI is invariant.
- **`sources-adopt` cannot be run bare**: its registry entry needs `--registry`/`--package`; exit 2 is the
  documented usage code, so row 19 is green-as-documented but carries no gate verdict — the evaluative path
  is `--selftest` (row 20, 17/17).
- **`gate-timing` needs a real REV**: `REV` is not optional in practice; `b571944` (the round-26 lesson
  commit) and `HEAD` both pass. The registered red control (`--lesson corpus/lessons/round-25.md --commit
  8ea41f9`) was **not** run separately here; only the selftest (row 12) was, so the red direction rests on
  that selftest, not on a re-execution.
- **Disclosure**: my first probe capture appended a `CMP byte-equal` sentinel *after* running `cmp`, which
  made a second `cmp` on that file fail on a trailing byte. The clean rerun
  (`receipts/regex-log-probe-fresh.txt`) is byte-equal to the receipt at sha `439101fa…`; the original
  first-run `cmp -s` also returned success before the append. Only the receipt copy matters.

## 5. Evidence inventory

- `receipts/summary.tsv` — label, exit, seconds, last line for all 27 commands.
- `receipts/*.log` — full stdout/stderr per command (including `package-gate.log` P1–P10 and both
  `round36-*-battery.log` fixture lines).
- `receipts/regex-log-probe-fresh.txt` — fresh probe output, byte-equal to
  `corpus/evidence/round36/regex-log-probe.txt`.
- `receipts/cmds.tsv`, `receipts/run.sh`, `receipts/SHA256SUMS` — the exact command set and runner, so the
  sweep is replayable verbatim.

Not run (out of scope for this seat): the wave-1 battery fixture development, `plans/round37_c1_verify.py
--only …` development mode, and any post-landing verification (parent owns the integration gate).

VERDICT: tip-sweep-25/25
