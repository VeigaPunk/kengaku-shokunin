# ExecPolicyCore — round 27 C1 (WRITER): plans/parser_policy_compare.py

Seat KengakuR27.ExecPolicyCore · base 11a7fc8c64dc (clone HEAD verified) · branch r27-ExecPolicyCore
Clone /tmp/kengaku-r27-ExecPolicyCore · clone writes only · no lane, jj, git or index mutation.

## Files written
- Clone: plans/parser_policy_compare.py, sha256 c4296935ed40f4d12a5d3ad238a2d5b9c7ca98712e61a2caf206476f9b025a27, 595 lines.
- Clone: plans/policy_cases.py, sha256 8484aeaf8a798290e7710032acbd15a7859bddfd54ce37e1dbcea2449246e50c, 85 lines, 59 hand-expected cases. No other clone files or bytecode.
- Lane: this report only.

## Exercised verification (clone cwd, PYTHONDONTWRITEBYTECODE=1)
- `--summary` → exit 0; unchanged frozen-population results (TOTAL below).
- `--json | python3 -m json.tool >/dev/null` → pipeline status `0 0`.
- `--selftest` → restored exit 0: 59/59 hand cases, 10/10 mutants killed, mutated-pin CLI rejection in both modes (`summary_rc=1`, `json_rc=1`, `policy_calls=0`).
- Red/restored control: first-fence E6 mutation sha256 `3f33b6191e49476591bd047f89c4efff2ebe9303e0db2a6da7b6fb42e362f1c4` → selftest exit 1 (`policy=E6` and hand case fail); restored sha256 equals pristine `c4296935…f9b025a27`, selftest exit 0.
- Pin-failure CLI summary and JSON rendering/serialization exercised in selftest. No separate manual `--root` invocation; exit-2 usage, POLICY-RAISE / GRADER-RAISE paths (none occurred), and oracle comparison (other seat) were not run.

## Design
- Population and pins: `gp.build_population(root)` is reused unchanged. Pins and the 1964 / 0-excluded checks come from `gp._LAST`.
- Per-record dispatch: `gp.regrade` runs verbatim. Only its extractor is swapped, via a wrapper on `gp._GRADER` restored in `finally`. `grader_perturb.py` is not edited.
- Immediately after `build_population`, any `gp._LAST["errors"]` returns a structured exit-1 failure before any E-policy call. A blank-line-mutated pinned result file plus poisoned callables produced summary/json rc=1 and `policy_calls=0`; summary has a TOTAL and JSON serializes.
- E0 is a self-contained transcription of the table. Extra check: `E0 == grader.extract_json_block` on all 1964 raws, else exit 1. Result: 0 BASELINE defects.
- Exit 1 also covers grader exceptions. The pre-registration names only policy exceptions; the same defect rule was applied to graders. A defect is never counted as FAIL.
- Grader totality: `grade_c` calls `set(viol)` (grader.py:256) and `valid_latin` calls `set(r)` (grader.py:236). Both can raise TypeError on unhashable list elements. No such case occurred on the population.
- CELLSHIFT is printed for E1..E8; E0 is the reference. Cell label is `<dir>/<file>:<cell>`. Ties go to the first cell in POPULATION_FILES order, then cell name.
- MATRIX lines: one `MATRIX cols ...` header, then nine `MATRIX row <id> ...` lines.
- Selftest probes remain separate from hand cases. E0's duplicate no-bare-fallback mutant now reuses `e5_fence_only`; E6 has a permanent first-vs-last any-label-fence mutant/control. All 10 mutants are killed. Alone, `--selftest` runs only the selftest; with `--json` it writes to stderr.
- `plans/policy_cases.py` has 59 table-derived expected cases, including E1 matched-fence fallback, E2 non-overlapping raw findall, E5 last-fence-only, exact E6 token-label and two-distinct-fence last-selection controls, and E8 crossing/adjacent spans. Selftest: `hand_cases=59 failed=[]`.
- Stratum, per-file and per-cell PASS rates are in `--json` only, so the STRATUM line keeps the pre-registered format.

## Observed (for close-out scoring; predictions are not scored here)
- E0 baseline: agree 1964/1964, pass 1021 (0.5199), none 0, CP95 [0.998124, 1.000000].
- flip_pf / flip_fp: E1 17/0, E2 0/0, E3 17/0, E4 1012/0, E5 26/0, E6 0/0, E7 17/0, E8 0/0.
- E1, E3 and E7 verdicts are identical on all 1964. All 17 flips are in MULTI (agree 14/31).
- E0, E2, E6 and E8 verdicts are identical on all 1964.
- E5 flips: BARE 9 + DANGLE 17. E5 none = 145 = BARE 88 + DANGLE 57.
- E4 none = 1876, pass = 9. All 9 passes are BARE records (BARE agree 88/88).
- TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5.
- Largest per-cell shift: E1, E3, E7 at 75.00 pp (round8-horizon/results.jsonl:B-clean-hint); E4 at 100.00 pp (C-MONO); E5 at 6.67 pp (A-CKPT).
- Prediction observations:
  - Q1 17 disagreements → true.
  - Q2 952/1964 = 48.5% agree → true.
  - Q3 0 → true.
  - Q4 E7 17 vs E3 17 → false.
  - Q5 75 pp at E1 → true.
  - Q6 0 → true.
  - Q7 E0 1021 vs E5 995 = 1.32 pp → false.
  - Q8 26 → true.

## Risks and notes
- E4 keeps `raw.strip()` as pre-registered. Peer RowOpenAIEvalsJson reports (not verified by me) that strip changes nothing on the pinned records. The synthetic `\x0c` probe is what kills the strip-omitted mutant.
- Amendment 1 cost constraint: E7/E8 are kept as frozen pure research functions; no arbitrary-input safety or performance claim. CLI executes them only after the four result-file pins and population checks pass.
- Policies with zero shift print the first cell (A-CKPT) as their cell. That is a tie-break, not a finding.
- CP95 is descriptive only, per the pre-registration.
- No SOURCES rows opened; no quotes used.

Installs: none. Stdlib only; no tool installed or upgraded.

VERDICT: C1 instrument and pin short-circuit implemented in clone (script sha256 c4296935…f9b025a27; cases sha256 8484aeaf…246e50c, n=59); E6 first-fence mutant is red (exit 1), restored source hash is green (exit 0), all 10 mutants killed.
