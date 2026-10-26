# R36RevProbePred — review of the 24 frozen probe cases (C2)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only; no lane file written).
Subject: `plans/regex_log_probe.py` (`build_cases`) sha256 `d58194c8…519bc` (= `PROBE_SHA256`,
`plans/round36_c2_verify.py:41`, Amendment 1) against
`corpus/evidence/round36/tb2-regex-log/instruction.md` and `.../test_outputs.py`
(sha256 `345c3bd0…8f72`, upstream-verified below).
Axis used: (a) label→instruction fidelity, (b) mutant→requirement isolation, (c) uncovered clauses.

## 0. Capture is authentic (positive, verified)

Fetched upstream at the pinned commit and compared bytes:

```
$ for f in tests/test_outputs.py instruction.md tests/test.sh task.toml; do curl -sS <raw>/2fd12b88…/regex-log/$f | sha256sum; done
345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72   (test_outputs.py)
4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c   (instruction.md)
4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334   (test.sh)
6bc98525852755caf1fe34c174c2f10f4328adb4ce6c1968dcafe1c877e4e160   (task.toml)
$ curl <raw>/2fd12b88…/regex-log/solution/solve.sh | sha256sum
7e670d4f2b4bccb1e4db38f2a173e085ceda028c38167912b466b0a84fcc0999   == local solve.sh
```
All five local capture digests are byte-identical to upstream (`regex-log/solution/solve.sh` is the
oracle's real path; `regex-log/solve.sh` is 404 upstream, the capture flattens it). So the oracle I
cite in §4 is authoritative, not an unverified artifact.

## 1. Method

My own copy of the 25 log lines was rebuilt from the grader AST (`sample_logs`, `expected_dates`;
`log_lines = 25 expected = 9 distinct = 9`), then for every `mode="file"` case I re-ran
`re.findall(regex, log_text, re.MULTILINE)` on that copy and attributed each divergent value to the
line that produced it (`/tmp/k36rev/analyze.py`). Harness sanity: the authentic oracle regex fed
through the probe's own `run_grader` → `pass` (`oracle vs grader -> pass`), so the Pin-Patch harness
is not silently passing everything.

Ground truth on the frozen log: must-match lines `[1,2,4,5,6,9,10,19,20]`; must-not `[3,7,8,11,12,
13,14,15,16,17,18,21,22,23,24,25]`.

## 2. Verdict summary

- 24 cases reviewed; all 24 predictions reproduce (`cases=24 observed_pass=8 observed_fail=16 mismatches=0`).
- Isolation: **13 clean**, **1 coarse** (`no-ip-condition` removes a whole clause, 9 lines flip),
  **2 confounded** (`ip-no-right-boundary`, `ip-no-left-boundary` — §3).
- Of the 8 pass cases, **5 are instruction-violating regexes the grader accepts** (§4), 1 is a
  scorer-satisfiability weakness (`hardcoded-expected-dates`), 2 are compliant
  (`reference-month-aware`, `padded-file`).
- **5 instruction clauses have no discriminating case** (§5).

## 3. The confound the assignment asked about — confirmed in the two IP-boundary mutants

Exact spans the mutants match (`/tmp/k36rev/exp3.py`):

```
ip(right=False) on 'User login 192.168.1.1abc on 2021-12-01'        -> ['192.168.1.1']
ip(right=False) on 'Login attempt 172.16.0.256 on 2000-05-10'       -> ['172.16.0.25']
ip(right=False) on 'Login attempt 172.16.0.256 for user 2000-02-30' -> ['172.16.0.25']
ip(right=False) on 'Login attempt 172.16.0.256 for user 2000-04-31' -> ['172.16.0.25']
ip(left=False)  on 'Invalid IP 256.100.50.25 with date 2021-01-01'  -> ['56.100.50.25']
ip(left=False)  on 'Error for user with code abc192.168.1.1 on 2023-01-01' -> ['192.168.1.1']
ip(left=False)  on 'abc10.0.0.5 accessed system on 1999-07-20'      -> ['10.0.0.5']
ip(base)        on 'Login attempt 172.16.0.256 on 2000-05-10'       -> []
```

`ip-no-right-boundary` fails with **4** extras: `2021-12-01` (L21, the labelled alnum-suffix line)
**plus** `2000-05-10`, `2000-02-30`, `2000-04-31` (L23–L25) — because without the trailing guard the
mutant reads the *invalid* octet `256` as the *valid* IP `172.16.0.25`. `ip-no-left-boundary` fails
with **3** extras: `2023-01-01` (L12) and `1999-07-20` (L22) are the labelled alnum-prefix lines, but
`2021-01-01` (L7) comes from reading `256.100.50.25` as `56.100.50.25`.

Reading: the mutated clause *is* the cause (the guard is what forbids both an alnum suffix and a
mid-number start), so neither case is wrong — but neither is isolated. Three consequences:

1. The left/right boundary guard is load-bearing for the **octet-range** requirement too, so these
   two cases overlap `ip-octets-unbounded` (lines 7, 23–25 are the same six lines that case flips).
2. The `assertion=` column for `ip-no-right-boundary` is dominated by the *invalid-IP* lines, and two
   of its extras (`2000-02-30`, `2000-04-31`) are strings the grader's own comments call invalid
   **dates**. A reader of the receipt can plausibly mis-attribute the failure to month-length.
3. No artefact records the per-line attribution that resolves this — see D-RP1.

## 4. Pass cases that are instruction violations the grader accepts

Each was proved on a line the frozen log does not contain (`/tmp/k36rev/exp.py`, `exp2.py`,
`exp4.py`); the log itself cannot see them.

| case | violation of | proof |
|---|---|---|
| `reference-lenient-days` (pass) | `instruction.md:3` "February can have up to 29 days" | `re.findall(ref_lenient, "1.2.3.4 x 2000-02-30") -> ['2000-02-30']`; the month-aware reference returns `[]` |
| `ip-leading-zeros-allowed` (pass) | `instruction.md:4` "without leading zeros in each octet" | `OCT_LZ` on `"1.2.3.04 x 2025-01-09" -> ['2025-01-09']`; base `OCT` -> `[]` |
| `date-boundary-letters-only` (pass) | `instruction.md:6`+`:7` — and the instruction's *own* example | `"… for user 1134-12-1234" -> ['1134-12-12']` (a truncated bogus date); `"1.2.3.4 x 12025-01-09" -> ['2025-01-09']`; `"19999-06-15" -> ['9999-06-15']`; the alnum reference returns `[]` for all three |
| `year-any-digit-count` (pass) | `instruction.md:1` "format YYYY-MM-DD" | `\d{2,6}` on `"1.2.3.4 x 12025-01-09" -> ['12025-01-09']`; `\d{4}` -> `[]` |
| `feb-29-rejected` (pass) | `instruction.md:3` permitting side | Feb-28-capped regex on `"1.2.3.4 x 2024-02-29" -> []`; the month-aware reference -> `['2024-02-29']` |
| `hardcoded-expected-dates` (pass) | not an instruction violation, but satisfiability | `"9.9.9.9 on 2010-02-03" -> []` — the nine-literal alternation generalises to nothing; the log is fixed and in the test file |
| `reference-month-aware` (pass) | compliant | mirrors the oracle: Feb ≤ 29 in any year, 30-day months capped |
| `padded-file` (pass) | compliant | 0 matches if the un-stripped pattern is applied to the log, 9 after `.strip()` → the case isolates `.strip()` exactly |

**Is each of these described correctly?** Yes for `ip-leading-zeros-allowed`,
`date-boundary-letters-only`, `feb-29-rejected`, `hardcoded-expected-dates`. Two need tightening:

- `reference-lenient-days`: the label "all bullets with day 01-31 in every month (no month-length
  check)" is opaque ("bullets"?) and does not name the violation. Only **Feb 30** is an instruction
  violation (`:3`); **Apr 31** is *not* constrained by any instruction sentence, so the label
  conflates a real instruction violation with a grader-comment convention (`test_outputs.py:67`).
  It also omits the mechanism (D-RP3): the grader is not lenient, it is **blind**.
- `year-any-digit-count`: the parenthetical "(other widths are unobserved)" is right, but the
  violation direction (the mutant *accepts* 5- and 6-digit years) is left implicit.

## 5. Instruction clauses with no discriminating case (5)

| # | clause | why no case can see it |
|---|---|---|
| U1 | `instruction.md:1` exact `YYYY-MM-DD` (separator + 4-digit year) | separator-tolerant mutant **passes the frozen log**: `re.findall(sep[-/], log) == expected` is `True`, while on a held-out line it returns `['2025/01/09']`. Year width is covered only by the pass case `year-any-digit-count`. |
| U2 | `instruction.md:2` "only the last date" — last *date* vs last *valid* date | no line holds a valid date followed by an invalid date-like token; both readings score 9/9. Proof: `ref` on `"1.2.3.4 x 2020-01-01 and 2020-13-01" -> ['2020-01-01']` vs `"… 2020-01-01 then 2000-02-30" -> ['2000-02-30']` — the frozen log contains neither shape. |
| U3 | `instruction.md:3` permitting side (Feb 29 must be *accepted*) | no valid-IP line carries `02-29`; only `feb-29-rejected` exists, which passes. |
| U4 | `instruction.md:4` leading-zero octets, enforcing direction | no line contains a leading-zero octet, so no case can require rejection; and the authentic oracle itself violates it (§6, D-RP5). |
| U5 | `instruction.md:5`/`:6` digit-adjacent dates (the instruction's own `1134-12-1234`) | that class is absent from the log (only `1234-56-7890` at `test_outputs.py:48`, invalid by month anyway). A letters-only-boundary regex extracts `1134-12-12` from the instruction's example and still passes. |

Also untested, cheap to note: `instruction.md:10` `re.MULTILINE` is only *transitively* exercised —
with `^`-anchored references the log gives 9 matches with the flag and 1 without it
(`exp4.py`), so a flag drop would be caught, but no case names it.

## 6. Defects, by severity

**D-RP1 (medium, artefact-diagnostic) — the receipt cannot support the claim it is used for.**
`run_grader` truncates every assertion to 160 chars (`plans/regex_log_probe.py`, `run_grader`), and
the `Expected [...]` head is identical for every list mismatch. Measured on the committed receipt:
**11 of the 16 failing cases carry a byte-identical `assertion=` string** (`first-date-only`,
`no-ip-condition`, `ip-octets-unbounded`, `month-13-allowed`, `month-00-allowed`, `day-32-allowed`,
`day-00-allowed`, `date-no-left-boundary`, `date-no-right-boundary`, `ip-no-left-boundary`,
`ip-no-right-boundary`); 7 distinct assertion strings cover all 24 cases. So the one column a wave-2
auditor would use to check "did the case die for its labelled reason" carries no information for
11/16 cases. The probe digest is pinned (Amendment 1), so fixing it needs an Amendment 2 and a
receipt re-freeze. **Cheap in-scope alternative:** carry the per-line attribution table (§7) in
`corpus/knowledge/tb2-regex-log-grader.md`, which W3 does not digest-pin.

**D-RP2 (medium) — two boundary mutants are not diagnostic-clean** (evidence in §3). The cases are
correct mutants; the defect is that their failure set is the union of "alnum adjacent" and "valid
prefix/suffix of a >255 octet", so they overlap `ip-octets-unbounded` and print invalid-date extras
(`2000-02-30`, `2000-04-31`). Recommend the entry state the exact spans (`172.16.0.25`, `56.100.50.25`)
so the overlap cannot be misread as a month-length failure.

**D-RP3 (medium) — month-length validity is unobservable, not merely unenforced.**
The only `2000-02-30` and `2000-04-31` tokens live at `test_outputs.py:65` and `:67`, and **both
lines also carry `172.16.0.256`**, which the IP rule rejects first. The grader comments at `:66`
("`# N: invalid date 30th February`") and `:67` ("`# N: invalid date 31th April`") therefore claim a
discrimination the log cannot make: `reference-lenient-days` and `reference-month-aware` both score
9/9. That is why `reference-lenient-days` passes — blindness, not leniency — and the receipt's
"no month-length check" wording should be replaced by this mechanism.

**D-RP4 (low, label fidelity) — five labels name clauses the instruction never states.**
`month-13-allowed`, `month-00-allowed`, `day-32-allowed`, `day-00-allowed` ("month 01-12", "day
01-31") and `reference-month-aware`'s "30-day months capped at 30" are inferred from "YYYY-MM-DD"
plus the grader's comments (`test_outputs.py:52-55`, `:67`); `instruction.md` has no sentence about
month/day numeric ranges. They are reasonable readings, but the column is `requirement=` and the
labels do not mark the inference. (No case cites an `instruction.md:` line at all — that is a
schema-level gap in the frozen 5-tuples, not fixable without an amendment.)

**D-RP5 (low) — the oracle violates `instruction.md:4`, and the probe's mutant is wider than the
oracle.** Authentic `solution/solve.sh` octet is `1?\d?\d`:
`"1.2.3.04 x 2025-01-09"` and `"01.2.3.4 x 2025-01-09"` both match (`1.2.3.04`, `01.2.3.4`) but
`"1.2.3.010"` does **not**. The probe's `OCT_LZ = (?:25[0-5]|2[0-4]\d|[01]?\d?\d)` admits the
3-digit `010` form the oracle rejects. So the receipt's parenthetical "oracle itself allows them" is
**true only for the 2-digit leading-zero class**, and the stronger, checkable statement — *the task's
own oracle violates its instruction line 4 and the grader cannot detect it* — is left as a
parenthesis.

**D-RP6 (low, hygiene) — the probe writes into the capture directory.** `run_grader` loads
`test_outputs.py` with the default source loader, so every run writes bytecode beside the capture:
`corpus/evidence/round36/tb2-regex-log/__pycache__/` currently holds 6 `.pyc` files
(`cpython-3.11`, `-3.12`, `-3.13`, `-3.13.opt-1`, `-3.14`, `-3.14.opt-1`), i.e. the counter has been
run under at least four interpreters. `__pycache__/` is gitignored (`.gitignore:2`), so
`--require-clean-tree` and W1/W5 are unaffected — but the W5 counter mutates the evidence directory
on every invocation. `python -B` / `PYTHONDONTWRITEBYTECODE=1` stops the *writing*, but it does **not**
stop the *reading*: measured, `-B` executes a stale-but-valid `.pyc` while the source says otherwise —

```
$ printf 'X=1\n' > mod.py; import mod            -> X = 1            (writes __pycache__/mod.cpython-314.pyc)
$ printf 'X=2\n' > mod.py; touch -d <same mtime> -> same size (4), same mtime
$ python3.14 -B -c 'import mod; print(mod.X)'    -> X = 1            <-- pyc wins over source
$ python3.11 -B -c 'import mod; print(mod.X)'    -> X = 2            <-- no cache for that tag
```
So the durable fix is a source-only loader (read bytes → compile → exec), not `-B`; sibling seat
`R36ProbeHarnessMut` reached the same hole from the mutation side (its m6/m7 rows). That is a
counter/harness change, still needing no amendment to the pinned probe.

**D-RP7 (low, methodology) — S7's literal path is unverifiable.** `mod.Path = lambda _arg: real(p)`
replaces the path for *any* argument, so the probe cannot distinguish a grader that reads
`/app/regex.txt` from one that reads any other path; `regex-file-absent` tests only the existence
check. Fine for this grader (the literal is visible in the source and in W3 quotes), but the probe
should not be read as evidence for the path.

## 7. Per-case attribution (hand-off, derived from the frozen log; safe for the entry)

`obs` = observed; `flip` = lines whose match/no-match status differs from ground truth.

| case | obs | flip | isolation / label verdict |
|---|---|---|---|
| reference-lenient-days | pass | — | label imprecise (D-RP3/D-RP4); violation proof in §4 |
| reference-month-aware | pass | — | "30-day months capped at 30" not in the instruction |
| first-date-only | fail | values swapped on L2 (`2024-11-01`→`2023-12-31`), L6 (`2018-06-06`→`2018-05-05`) | clean — last-date rule |
| no-ip-condition | fail | EXTRA L3,7,8,12,21,22,23,24,25 | coarse (whole clause removed), attributable |
| ip-octets-unbounded | fail | EXTRA L7,8,23,24,25 | clean — octet range |
| ip-leading-zeros-allowed | pass | — | correct label (2-digit class), D-RP5 |
| month-13-allowed | fail | EXTRA L13 | clean |
| month-00-allowed | fail | EXTRA L14 | clean |
| day-32-allowed | fail | EXTRA L15 | clean |
| day-00-allowed | fail | EXTRA L16 | clean |
| date-no-left-boundary | fail | EXTRA L18 | clean |
| date-no-right-boundary | fail | EXTRA L17 | clean — both date-boundary cases are the clean pair the IP pair is not |
| date-boundary-letters-only | pass | — | correct label; violation proof in §4 |
| ip-no-left-boundary | fail | EXTRA L7 (`56.100.50.25`), L12, L22 | confounded (D-RP2) |
| ip-no-right-boundary | fail | EXTRA L21 (`192.168.1.1`), L23, L24, L25 (`172.16.0.25`) | confounded (D-RP2) |
| ip-before-date-only | fail | DROP L1, L5, L19 | clean — all three are date-before-IP |
| hardcoded-expected-dates | pass | — | honest label; satisfiability weakness |
| year-any-digit-count | pass | — | label right, violation implicit (§4) |
| empty-pattern | fail | — | clean |
| invalid-regex | fail | — | clean |
| regex-file-absent | fail | — | clean, but path literal unverifiable (D-RP7) |
| extra-capture-group | fail | 9 tuples instead of 9 strings | clean |
| padded-file | pass | — | clean; strip is load-bearing (0 unstripped / 9 stripped) |
| feb-29-rejected | pass | — | correct label; permitting side is U3 |

## 8. Positives verified (so the L1 need not re-derive them)

- Predictions are genuinely frozen: `git diff 3241b86 acbda2f -- plans/regex_log_probe.py` touches
  one line only — `.replace(d, "<tmp>")` in the assertion text — and every `predicted=` line is
  identical between the freeze commit and Amendment 1.
- Receipt reproducibility: `python3.11/3.12/3.13/3.14 -B plans/regex_log_probe.py --lane .` produce
  output **byte-identical** to `corpus/evidence/round36/regex-log-probe.txt` on all four
  interpreters (26 lines each), so W5's `sys.executable` byte-compare is robust.
- The authentic oracle passes the probe's harness, and the oracle generalises (`9.9.9.9 on
  2010-02-03 -> ['2010-02-03']`), which also proves the hardcoded-alternation case is measuring the
  right weakness.
- Working tree for `plans/` and `corpus/evidence/round36/` was clean before and after this review
  (`git status --porcelain` empty for both; `git diff --stat` empty).

Cross-seat reconciliation (peers' reports read as data only): `R36IndepRegexGrader.md` re-derives the
24 regex strings independently and reports `agree=24/24`, so the case *patterns* are faithful
transcriptions — my §3/§4/§5 findings are about label semantics and log coverage, not transcription.
`R36ProbeHarnessMut.md` independently found the `mode=="absent"` blindness (the same bound as my
D-RP7) and the `.pyc`-substitution hole (my D-RP6 measurement agrees and narrows the fix: `-B` is not
enough). No contradiction with either report.

## 9. Residual risk and verification gaps

- `cases=24 mismatches=0` is evidence about **24 hand-built regexes on one 25-line log**, not about
  the task. Five instruction clauses (§5) are invisible to it, and 5 of its 8 passes are held by
  instruction-violating regexes.
- I did not execute the grader inside its container (`alexgshaw/regex-log:20251031`); every claim
  here is about `test_outputs.py` executed offline under CPython 3.11–3.14.
- The mutation `mismatches` metric is a prediction-accuracy measure, not a defect count: a case may
  isolate cleanly and still be labelled imprecisely (D-RP4), which no receipt field can express.
- Fixing D-RP1/D-RP2 inside the receipt requires a claims Amendment 2 (probe + receipt are both
  digest-pinned); D-RP3/D-RP4/D-RP5 can be fixed entirely in the entry text; D-RP6 is counter-side.

VERDICT: probe-review-24-confounded-2-uncovered-5
