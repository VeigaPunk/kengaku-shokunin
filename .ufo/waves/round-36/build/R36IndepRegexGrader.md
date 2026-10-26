# R36IndepRegexGrader — independent re-implementation of the pinned tb2 `regex-log` grader

Seat: R36IndepRegexGrader (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Wave: round 36, wave 1 (C2 first falsifier). Date 2026-10-25. Frozen claims read in full
(`plans/round-36-claims.md`, freeze `3241b86c`, Amendment 1 `acbda2f3`).

Deliverable: `.ufo/waves/round-36/build/R36IndepRegexGrader/indep.py` — a checker that re-derives
the grader's verdicts from my own reading of the captured source, without importing the grader and
without using the probe's `run_grader`. It imports exactly one symbol, `build_cases`, from
`plans/regex_log_probe.py`.

## Result

`python3 indep.py --lane <lane>` → exit 0, **`agree=24/24 verdict_mismatches=0 class_mismatches=0
assertion_mismatches=0`**. Every one of the 24 frozen cases reproduces the receipt's `observed=`
field, its failing-assertion class, **and its assertion text byte-for-byte** (after the same
`<tmp>` normalisation and 160-char truncation). No disagreement with the probe or the receipt →
no finding against either.

## How independence is held (5 layers)

1. **Hand-copied fixtures.** `SAMPLE_LOGS` (25 strings) and `EXPECTED_DATES` (9 strings) are typed
   out from `corpus/evidence/round36/tb2-regex-log/test_outputs.py:32-56,58-68`; scoring uses only
   those constants. The line→expected mapping (`LINE_OF_EXPECTED = (0,1,3,4,5,8,9,18,19)`) is
   derived from the per-line `# Y`/`# N` comments, not from a program.
2. **Own assertions.** `score()` re-codes the three checks itself: `p.exists()` → `MissingFile`,
   `re.compile(text)` → `InvalidRegex`, `re.findall(text, LOG_TEXT, re.MULTILINE) != EXPECTED_DATES`
   → `WrongMatches`. No `importlib`, no execution of `test_outputs.py`, no `run_grader`.
3. **Instrument pin.** sha256 of the captured grader is compared to the pin before any scoring
   (`REFUSE` + exit 2 on drift), so the read source is the frozen source.
4. **Transcription self-check by AST, not by import.** `ast.parse` + `ast.literal_eval` extracts the
   grader's own `sample_logs` / `expected_dates` literals and compares them to the hand-typed
   constants. This proves the copy without executing the grader and without letting it grade itself.
5. **Receipt comparison is structural.** `observed`, class, and assertion text are all compared;
   class is *re-derived from the receipt text* independently (`klass_of_text`) rather than trusted.

Determinism: two runs are byte-identical — `sha256(run1.txt) = sha256(fresh rerun) =
b16cbeb288ac36984712495d9511417fb21de121ff7425d0cedf5365e6ec1cfe`, both exit 0.

## Evidence

```
$ python3 indep.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
grader=corpus/evidence/round36/tb2-regex-log/test_outputs.py sha256=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 pin_ok=yes
handtyped_log_lines=25 ast_lines=25 handtyped_equals_grader=yes log=yes expected=yes
handtyped_log_sha256=bd72ef92d854ae68662ca2c582dca11919b5703210e0fe790fd5e6a2958edcac
probe_cases=24 receipt_cases=24 receipt_summary='cases=24 observed_pass=8 observed_fail=16 mismatches=0'
… 24 × `case=… verdict_match=yes class_match=yes assertion_match=yes` …
observed_pass=8/24 observed_fail=16/24 perline_concat_equals_wholtext=22/22
agree=24/24 verdict_mismatches=0 class_mismatches=0 assertion_mismatches=0
exit=0
```

Independent counts agree with the receipt's footer: 8 pass / 16 fail / 0 mismatches. The 22/22
concatenation invariant (per-line `findall` concatenation == whole-text `findall`, for every case
whose regex compiles) proves no case regex depends on cross-line context, so the per-line
attribution below is exact, not heuristic.

Environment: python3 3.14.8 (stdlib only). The invalid-regex message reproduced byte-identically
(`missing ), unterminated subpattern at position 0`), i.e. the same interpreter family that produced
the receipt. No tool installs were needed or made.

## Per-case kill table — which sample line each mutant dies on

`L0..L24` index the 25 `sample_logs` entries in file order. `got` is what the mutant produced on
that line, `expected` is what the line's own `# Y`/`# N` comment requires.

| case | class | lines that differ |
|---|---|---|
| first-date-only | wrong-matches | **L1** `2023-12-31` vs `2024-11-01`; **L5** `2018-05-05` vs `2018-06-06` |
| no-ip-condition | wrong-matches | L2, L6, L7, L11, L20, L21, L22, L23, L24 (dates emitted on N lines) |
| ip-octets-unbounded | wrong-matches | **L6, L7, L22, L23, L24** (the five invalid-IP lines only) |
| month-13-allowed | wrong-matches | **L12** `2023-13-05` |
| month-00-allowed | wrong-matches | **L13** `2022-00-15` |
| day-32-allowed | wrong-matches | **L14** `1995-06-32` |
| day-00-allowed | wrong-matches | **L15** `2001-09-00` |
| date-no-left-boundary | wrong-matches | **L17** `2021-08-20` inside `abc2021-08-20` |
| date-no-right-boundary | wrong-matches | **L16** `2020-07-15` inside `2020-07-15abc` |
| ip-no-left-boundary | wrong-matches | **L6** via `56.100.50.25`; **L11** via `192.168.1.1`; **L21** via `10.0.0.5` |
| ip-no-right-boundary | wrong-matches | **L20** via `192.168.1.1`; **L22, L23, L24** via `172.16.0.25` |
| ip-before-date-only | wrong-matches | **L0, L4, L18** (date precedes the IP → missed) |
| empty-pattern | wrong-matches | all 25 lines (39–65 empty matches per line) |
| invalid-regex | invalid-regex | no `findall` (assertion fires at compile) |
| regex-file-absent | missing-file | no `findall` (assertion fires at `exists()`) |
| extra-capture-group | wrong-matches | L0, L1, L3, L4, L5, L8, L9, L18, L19 — tuples; e.g. L3 `('10.0.0.2', '2020-01-01')` (the greedy `.*` in the lookahead makes the **second** IP the captured one) |

The four substring cases above (`56.100.50.25`, `192.168.1.1`, `10.0.0.5`, `172.16.0.25`) were
measured, not inferred: `re.findall` of the boundary-stripped IP alternative on those exact lines.

## Findings against the probe / receipt

**None.** All 24 verdicts, all 24 assertion classes and all 24 assertion strings agree. Specifically
reproduced independently: the exact truncation points of the long `Expected […] but got […]`
messages, the two `<tmp>`-normalised path messages, and the two `no findall` classes.

## Independent confirmations of the entry's headline findings

Each is my own measurement on the captured grader, not a restatement of the receipt:

- **Literal alternation of the nine expected dates passes** (`hardcoded-expected-dates` →
  observed=pass). The graded log is fixed and visible in the test file, so the task is solvable with
  zero pattern logic.
- **Leading-zero IPv4 octets pass** (`ip-leading-zeros-allowed` → pass) although `instruction.md`
  forbids them.
- **Digit-adjacent dates pass** (`date-boundary-letters-only` → pass): the instruction's own example
  `1134-12-1234` is **absent** from the log — `grep -c '1134-12-1234'` → `0` — so only letter
  adjacency is ever exercised.
- **Any year width passes** (`year-any-digit-count`, `\d{2,6}` → pass).
- **Month-length validity is not exercised in the permitting direction**: `Feb 30` / `Apr 31` appear
  only at grader lines 65 and 67, both paired with `172.16.0.256` (an invalid IP), so those lines are
  N for the IP reason; `reference-lenient-days` (day 01-31 in every month) passes.
- **Feb 29 permitting side untested**: `02-29` occurs **0** times in the log — `grep -c '02-29'` →
  `0` — so `feb-29-rejected` (February capped at 28) passes despite the instruction allowing 29.

## Calibration: kill margins are one line wide

The per-line table is also a brittleness measurement. Each of the six single-rule mutants
(`month-13`, `month-00`, `day-32`, `day-00`, `date-no-left`, `date-no-right`) is separated by
**exactly one sample line**, and `first-date-only` by two (L1, L5). The whole date-validity
and boundary surface rests on L12-L17; the whole IPv4-range surface on L6/L7/L22-L24; the "IP anywhere
in the line" surface on L0/L4/L18. Wave-2 mutation of that log (or of a single line) is therefore
high-leverage on the grader's discriminating power, and a regex can pass while violating a rule that
irrelevant lines happen not to pair with. This is a property of the pinned grader, not of the probe.

## Controls run (the checker can disagree)

Scratch mutants live beside `indep.py` (`mt_*.txt`, `logmut.py`); the real receipt is untouched.

| control | mutated | output | exit |
|---|---|---|---|
| receipt verdict flip ×2 (`padded-file` pass→fail, `month-13-allowed` fail→pass) | `mt_verdict.txt` | `agree=22/24 verdict_mismatches=2` | 1 |
| receipt assertion text (drop `missing ), ` from invalid-regex) | `mt_assert.txt` | `agree=23/24 assertion_mismatches=1`; `assertion_match=NO` on `invalid-regex` with both strings printed | 1 |
| hand-typed log line (`2017-03-03` → `2017-03-04`) | `logmut.py` | `handtyped_equals_grader=NO log=NO`, `agree=16/24` | 1 |
| genuine | — | `agree=24/24`, all yes | 0 |

The verdict mutant proves the comparison bites on `observed`; the assertion mutant proves it bites on
text (class stayed `invalid-regex`, so only the string comparison could have caught it); the log mutant
proves the AST self-check would catch a bad transcription before scoring.

## Limits and risks

- The two `no findall` cases cannot be attributed to a log line by construction; their kill point is
  the assertion, reported as such.
- The assertion-text comparison is strong only because both sides normalise the temp path and truncate
  at 160 chars identically; a future probe that changes either would show up as
  `assertion_mismatches>0` with both strings printed (which is what I want).
- My checker reads the probe's `build_cases`, so a defect *inside* a case's regex string is inherited
  and cannot be caught here; conversely a defect in the probe's `run_grader` or its comparison is
  exactly what this seat was built to catch, and none was found.
- The corpus `expected_dates` list is order-sensitive; I verified text order matches list order, so
  no hidden ordering assumption is being papered over.
- Nothing in `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md` or the Git index
  was written. Only `.ufo/waves/round-36/build/R36IndepRegexGrader/` (checker, run logs, mutants) and
  this report.

VERDICT: indep-agree-24/24
