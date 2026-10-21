# ExecPolicyCore — round 27 C1 (WRITER): plans/parser_policy_compare.py

Seat KengakuR27.ExecPolicyCore · base 11a7fc8c64dc (clone HEAD verified) · branch r27-ExecPolicyCore
Clone /tmp/kengaku-r27-ExecPolicyCore · clone writes only · no lane, jj, git or index mutation.

## Files written
- Clone: plans/parser_policy_compare.py, sha256 7dbc592b71654874210064b4a197c62828c227153b1f5a9c363e93501102149d, 580 lines.
- Clone: plans/policy_cases.py, sha256 f3e9b57b80584721437358c7fa1d69146d9cf2588ca483c0bc3f1bf73b47417b, 84 lines, 58 hand-expected cases. No other clone files or bytecode.
- Lane: this report only.

## Exercised verification (clone cwd, PYTHONDONTWRITEBYTECODE=1)
- `--summary` → exit 0; unchanged frozen-population results (TOTAL below).
- `--json | python3 -m json.tool >/dev/null` → pipeline status `0 0`.
- `--selftest` → exit 0: 58/58 hand cases, 9/9 mutants killed, mutated-pin CLI rejection in both modes (`summary_rc=1`, `json_rc=1`, `policy_calls=0`).
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
- Selftest probes are written from the table text, not from the implementation. Each policy has one seeded mutant: E0 no-bare-fallback, E1 last-fence swap, E2 fence leak, E3 order reversed, E4 strip omitted, E5 fallback leak, E6 label restricted, E7 bare-bounded spans, E8 contained-span reuse. All 9 are killed. Alone, `--selftest` runs only the selftest; with `--json` it writes to stderr.
- Added `plans/policy_cases.py` with 58 table-derived expected cases, including E1 first-matched-fence fallback to raw BARE_RE, E2 non-overlapping raw findall, E5 last-fence-only, E6 exact token-label regex, and E8 crossing-span and adjacent-boundary cases. Selftest reports `hand_cases=58 failed=[]`.
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

VERDICT: C1 instrument and pin short-circuit implemented in clone (script sha256 7dbc592b…02149d; cases sha256 f3e9b57b…7417b, n=58); summary exit 0, JSON valid, selftest 9/9 killed and mutated-pin CLI 0 calls, 0 baseline defects on 1964 records.
