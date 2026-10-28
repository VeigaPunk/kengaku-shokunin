# C2ExecRowRuns — stranger-run measurements

## Method and evidence

- Read `plans/round-52-claims.md` in full before acting. Its frozen C2 baseline is `ADVERTISED 72`, `REGISTERED 44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (`order-check`).
- Read `/home/vgpnk/.omp/agent/RULES.md`; pacman transactions were paused, and no tools were installed or updated.
- Commands run:
  - `git clone --shared -b master /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/lane`
  - `git -C /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/lane rev-parse HEAD` → `1315234bdc8024499d943f0483dcb51fb5e4a618`.
  - `python3 plans/round52_c2_registry.py --lane .` in that clone → `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1`, `PREDICATE R52-C2 fail`, exit 1. The listed 28 are the instruments in the table below.
  - `git worktree add --detach /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/base 30801b479e3418c11089b8586178b6960216f364` (scratch clone only; frozen base tree).
  - `git diff --name-only 30801b479e3418c11089b8586178b6960216f364 HEAD` showed only `.ufo/waves/round-52/{build_spec_w1.py,claims/c1-before.txt,claims/c2-before.txt,claims/c2_before_probe.py,w1-dispatch.json,w1-run.err,w1-run.out,w1-spec.json,w1/swarm-registry.json}` and `plans/{round-52-claims.md,round52-tasks.json,round52_c1_grader_audit.py,round52_c2_registry.py}`. The instrument executions below use master HEAD, as directed by the clone command.
  - `df -h /fast/scratch` before runs: 540 GB available; later observation: 525 GB available.
  - Network checks: `curl` to Hugging Face and OpenRouter returned HTTP 200. `uv run --no-project --with biopython==1.85 python3 -c 'import Bio; print(Bio.__version__)'` returned `BIO_OK 1.85`.
- The complete runner is `/fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/run.py`; its per-instrument captured stdout, stderr, and result JSON are under `/fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/<instrument>/`. Each run used an isolated `cp -a --reflink=always` copy of the master clone (XFS reflink test succeeded), set `TMPDIR` to its own scratch `tmp/`, and supplied a separate `--work` or `--scratch` directory where supported. No instrument ran inside the real lane tree. Wall times are elapsed seconds measured individually; runs were sequential.
- Write detection: per-run `find ... -newer marker` over the isolated copy, excluding `.git`, plus `git status --porcelain --untracked-files=all`. `git status` was clean in all runs because the observed `__pycache__` files are ignored. A `writes` result below means files were nevertheless newly written into that run's clone copy.
- The real lane already had 39 porcelain-status entries at inspection; I did not alter or clean them. No tool installs/updates.

## Measurements

`writes` lists paths newly touched in that run's clone; `—` means none observed. Output is the instrument's final verdict/summary line(s), not a guessed interpretation. Exit codes and durations are measured.

| Instrument | Command run | Exit | Wall s | Verdict / final output | Wrote into clone? |
|---|---|---:|---:|---|---|
| adoption_check | `python3 plans/adoption_check.py --lane . --expect .ufo/waves/round-33/claims/adoption-expect.json --census` | 1 | 0.037 | `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail` | — |
| attrib_probe | `python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` | 0 | 0.045 | `FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK` | — |
| catalog_probe | `python3 plans/catalog_probe.py --verify --lane .` | 0 | 0.043 | `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok`; `HF missing fields: author, sha, lastModified, gated` | — |
| defect_ledger | `python3 plans/defect_ledger.py --lane .` | 0 | 0.045 | `rows=5 closed=5 observed_pass=5 mismatches=0`; `PREDICATE C2 pass` | — |
| gate_flip_check | `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42.md` | 0 | 0.033 | `FLIPS total=2 unresolved=0`; final citation line `FLIP-CITE entries=- missing=instruction.md,README.md,R42PkgRows.md not_fired=1 red=0` | — |
| parser_policy_compare | `python3 plans/parser_policy_compare.py --summary` | 0 | 0.268 | `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` | — |
| password_recovery_probe | `python3 plans/password_recovery_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/password_recovery_probe/work` | 0 | 1.450 | `regrade cases=16 differ=0`; `cases=16 observed_pass=5 observed_fail=11 mismatches=0` | — |
| polyglot_c_py_probe | `python3 plans/polyglot_c_py_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/polyglot_c_py_probe/work` | 0 | 1.624 | `regrade cases=18 differ=7`; `cases=18 observed_pass=7 observed_fail=11 mismatches=0` | — |
| round28_census | `python3 plans/round28_census.py --revision 1315234bdc8024499d943f0483dcb51fb5e4a618` | 1 | 1.323 | JSON reports `c1.exit=0`, `c2.exit=0`, `historical_state.exit=1` (`mismatch=1`), `sources.rows=171`, `knowledge.files=55`, `index_rows=54`, and `unindexed=["knowledge/fixture-honest-geometry.md"]` | — |
| round30_defects | `python3 plans/round30_defects.py --lane .` | 0 | 0.048 | `checks=5 defects=0` | — |
| round31_c1_verify | `python3 plans/round31_c1_verify.py --lane .` | 0 | 0.031 | `checks=6 defects=0` | — |
| round31_defects | `python3 plans/round31_defects.py --lane .` | 0 | 0.090 | `checks=10 defects=0` | — |
| round33_c1_verify | `python3 plans/round33_c1_verify.py --lane .` | 0 | 0.036 | `checks=8 defects=0` | — |
| round33_defects | `python3 plans/round33_defects.py --lane .` | 0 | 0.040 | `checks=6 defects=0` | — |
| round35_c1_verify | `python3 plans/round35_c1_verify.py --lane .` | 1 | 17.833 | `V4 DEFECT knowledge files=55 index rows=54 (want 42/42)`; `checks=6 defects=1`; `PREDICATE C1 fail` | — |
| round35_hardening | `python3 plans/round35_hardening.py --lane .` | 0 | 0.055 | `hardening run=6 failed=0` | — |
| round36_c2_verify | `python3 plans/round36_c2_verify.py --lane .` | 1 | 0.451 | `W4 DEFECT knowledge files=55 index rows=54 (want equal and >=43)`; `checks=6 defects=1`; `PREDICATE C2 fail` | `corpus/evidence/round36/tb2-regex-log/__pycache__/test_outputs.cpython-314.pyc` |
| round45_c1_verify | `python3 plans/round45_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round45_c1_verify/work` | 0 | 3.756 | `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=10 contradicted=0`; `PREDICATE C1 pass` | `plans/__pycache__/round44_c1_verify.cpython-314.pyc` |
| round45_c2_verify | `python3 plans/round45_c2_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round45_c2_verify/work` | 1 | 2.204 | `V2 DEFECT spec=frozen gate=frozen gate_exit=1`; `checks=11 defects=1`; `PREDICATE C2 fail` | — |
| round46_c1_verify | `python3 plans/round46_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round46_c1_verify/work` | 0 | 5.389 | `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=32 contradicted=0`; `PREDICATE C1 pass` | `plans/__pycache__/round44_c1_verify.cpython-314.pyc` |
| round46_c2_verify | `python3 plans/round46_c2_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round46_c2_verify/work` | 0 | 0.175 | `checks=4 defects=0`; `PREDICATE C2 pass` | `plans/__pycache__/anchor_line_check.cpython-314.pyc`, `plans/__pycache__/round45_c2_verify.cpython-314.pyc` |
| round46_c3_verify | `python3 plans/round46_c3_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round46_c3_verify/work` | 1 | 4.116 | `V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12`; `checks=13 defects=3`; `PREDICATE C3 fail` | — |
| round50_c1_verify | `python3 plans/round50_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round50_c1_verify/work` | 0 | 54.656 | `REFUSALS total=20 clean=20 leaked=0 build_errors=0`; `SEALED total=20 clean=20 leaked=0 build_errors=0`; `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met`; `PREDICATE R50-C1 pass` | Python bytecode caches under `plans/__pycache__/`, `plans/battery42/__pycache__/`, `plans/battery43/__pycache__/`, `plans/battery44/__pycache__/`, `plans/honest50/**/__pycache__/`, `plans/refusals46/__pycache__/`, `plans/sealed46/__pycache__/`, and `plans/sealed50/__pycache__/` (full list in `runs/round50_c1_verify/result.json`) |
| round50_c2_audit | `python3 plans/round50_c2_audit.py --lane .` | 0 | 0.275 | `TIP 1315234bdc8024499d943f0483dcb51fb5e4a618 branch=master`; `POINTERS total=292 paths=228 hashes=64 resolved=292 exists=216 superseded=3 never-landed=9 unresolved=0` | — |
| round51_routing | `python3 plans/round51_routing.py --lane . --run-checks --scratch /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/runs/round51_routing/scratch` | 0 | 0.620 | `CHECKS present=75 absent=0`; `VERIFIED ran=41 passed=41 failed=0`; `PREDICATE R51-C2 pass` | — |
| round51_surfaces | `python3 plans/round51_surfaces.py --lane .` | 0 | 0.064 | `PROBES run=20 present=14 absent=6 errors=0`; `UNVERDICTED 0`; `PREDICATE R51-C1 pass` | — |
| routed_open | `python3 plans/routed_open.py --lane .` | 0 | 0.035 | `ROWS total=75 open=31 blocked=1 closed=41 refused=2`; `routed_open=32 oldest_round=39` | — |
| tb2_grader_probe | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` | 0 | 0.139 | `cases=18 observed_pass=5 observed_fail=13 mismatches=0` | — |

## Findings / limits

- **All 28 commands completed; no run timed out and none printed a traceback.** There are no crash tracebacks to paste. Exit 1 on adoption_check, round28_census, round35_c1_verify, round36_c2_verify, round45_c2_verify, and round46_c3_verify was a reported predicate/counter failure, not a Python crash.
- **Visible-row accounting issue:** the `gate-flip-check` row is present at `SKILL.md:609`, but parsing the registry block by the frozen counter's eight-cell rule yields 9 cells. The extra split is the literal `|` in `fired\|not fired`. The row is skipped, and `gate_flip_check.py` appears in `MISSING 28` despite the visible row. It should be repaired in place, not duplicated. Evidence command/output: the counter above; exact row printed by `grep -n 'gate-flip-check' SKILL.md`; an independent parser split reported `BADCELLS 9` and entry cell ``python3 plans/gate_flip_check.py --lesson <path> ...``.
- **Hidden worktree writes:** default Python execution generated ignored `.pyc` caches for round36_c2_verify, round45_c1_verify, round46_c1_verify, round46_c2_verify, and especially round50_c1_verify (many fixture modules). Git status remained clean, so registry write-scope cells must not be inferred from porcelain status alone. Evidence is each `runs/<instrument>/result.json` `writes` field; no tracked source/receipt file changed.
- **Clone-bound census behavior:** adoption_check produced `census=fail`, exit 1, in the standalone clone placement. Its code derives census root from `lane.parent` and lane id from lane directory name while invoking the fixed fleet census script; this measured result is layout-dependent. This report does not claim the same invocation fails in the canonical fleet layout.
- `round28_census` returned exit 1 because its embedded historical-state and index counts did not meet its clean predicate (`historical_state.mismatch=1`; 55 knowledge files vs 54 index rows, one unindexed file). The command did produce JSON, not a traceback.
- No package/tool install occurred. No check/build/lint/test/formatter was run. No lane/fleet commit, push, deploy, or remediation was performed.

## Artifacts and cleanup

- Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ExecRowRuns/report.md`
- Run artifacts (temporary, to be removed before return): `/fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/`
