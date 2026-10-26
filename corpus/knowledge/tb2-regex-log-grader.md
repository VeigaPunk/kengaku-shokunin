source: S108 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py — `test_regex_matches_dates`, lines 8–90, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-25
source: S109 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh — pytest exit → reward mapping, lines 1–29, same commit, accessed 2026-10-25
source: S110 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md — requirement bullets, lines 1–11, same commit, accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch the three pinned URLs, `sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS`, and re-run `plans/regex_log_probe.py --lane .`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `regex-log`

At terminal-bench-2 commit `2fd12b88`, the `regex-log` task's whole score is one pytest function,
`test_regex_matches_dates`, mapped by `tests/test.sh` to a binary reward (1 if pytest exits 0, else
0). The graded artefact is not a data string the agent writes: it is a **regex pattern file**
(`/app/regex.txt`) that the grader reads, strips, compiles and runs with `re.findall(..., re.MULTILINE)`
against a **25-line log hard-coded in the test file**, then compares the full match list to nine
literal expected dates. Offline execution of the captured grader *function* on 24 lane-authored
candidate patterns — not a run of Terminal-Bench, of the task image, or of any real submission
(`plans/regex_log_probe.py`; receipt `corpus/evidence/round36/regex-log-probe.txt`) matched every
prediction written from the static reading before the first run:

`cases=24 observed_pass=8 observed_fail=16 mismatches=0`

Six of the eight passing cases are patterns that violate a stated or structural requirement and still
score 1 — the fixed in-test log is the whole test surface, so a literal alternation of the nine
expected strings passes, the instruction's no-leading-zero-octet rule is unobserved, digit-adjacent
dates are unobserved, the year width is unobserved, month-length validity never decides a valid-IP
line, and the permitting side of February 29 is unobserved.

This entry extends `knowledge/benchmark-verifier-execution-model.md` (where a TB2 verifier runs; S100
is the same repository at the same commit), `knowledge/benchmark-grader-semantics.md` (one Toolathlon
grader read) and `knowledge/tb2-protein-assembly-grader.md` (the round-35 TB2 task read the same way),
and discharges, for this one task only, the `corpus/README.md` §Frontier round-35 clause that left
"the other TB2 tasks" open.

## Source labels

S108–S110 are the benchmark maintainers' own task files: primary for *what this grader checks* and
for the requirement text it is mapped against, and a self-report for everything else (the log
comments' `# Y:`/`# N:` labels are the authors' statements about their own fixture; the probe
executes them, it does not audit them). The probe receipt is the lane's own re-runnable gate output
(tier A for its own scope: these 24 patterns against this capture under the host Python). The
captured `solution/solve.sh` oracle is **tier C / own reading** — see the oracle section; it is not a
registry row and nothing below rests on it.

Disclosure: the frozen probe was amended **before any seat scored** (claims file, Amendment 1) so
that two assertion texts print `<tmp>` instead of a `mkdtemp` path; the receipt lines for
`invalid-regex` and `regex-file-absent` carry `<tmp>` for that reason. The `--dry` case list is
byte-identical before and after, and the pre-repair first run already had `mismatches=0`.

## What the grader checks (static reading, `test_outputs.py`)

| Step | Mechanism | Lines |
|---|---|---|
| File | `/app/regex.txt` must exist; `read_text().strip()` — surrounding whitespace is removed | 21–25 |
| Compile | `re.compile(pattern_text)`; an invalid regex raises `AssertionError` from `re.error` | 27–30 |
| Fixture | `sample_logs` is a 25-element list of literal lines in the test file; `"\n".join` ⇒ one 25-line text | 34–68, 84 |
| Execution | `re.findall(pattern_text, log_text, re.MULTILINE)` — `.` does not cross newlines, so the pattern is effectively line-local | 87 |
| Oracle values | `expected_dates` is a 9-element literal list | 71–81 |
| Decision | `assert matches == expected_dates` — full-list equality: count, order and type all matter | 90 |

Structural facts of the executed fixture (AST walk over the capture):

```
sample_logs: 25 expected_dates: 9
feb29 anywhere: 0
leading-zero-octet lines: []
```

The fixture's designed distinctions, read from the `# Y:`/`# N:` comments: IP-before-date and
date-before-IP both qualify (lines 35 and 38), multiple dates on one line must yield the **last**
(line 36), multiple IPs with one date are fine (line 39), `0.0.0.0` and `255.255.255.255` are valid
(lines 46–47), `1234-56-7890` only *resembles* a date (line 48), and the `# N:` group encodes month
13 / month 00 / day 32 / day 00 / alphanumeric-adjacency / octet > 255 rejections (lines 52–67).

## Instruction requirement → enforcing assertion (executed, 24 cases)

The grader has **no requirement-specific assertions**: the only decision is list equality against the
nine literals. "Enforced" below therefore means *the fixed log contains a line that makes a
non-compliant pattern produce a different list*, and "unobserved" means *no line in the log
distinguishes a compliant pattern from the violating one*. Each row is one probe case; observed
verdicts are copied from the receipt.

| Instruction requirement (S110) | Probe case | Observed | What decides it |
|---|---|---|---|
| only lines containing an IPv4 address (1) | `no-ip-condition` | fail | line 37 has a date and no IP |
| last date on a line (2) | `first-date-only` | fail | line 36 has two dates |
| octets 0–255 (4) | `ip-octets-unbounded` | fail | lines 41–42, 62, 65, 67 carry 256 / 456 |
| IPv4 not alnum-adjacent (7) | `ip-no-left-boundary`, `ip-no-right-boundary` | fail, fail | lines 60, 61 (`abc` before / after the IP) |
| IP may sit after the date (1, implicitly) | `ip-before-date-only` | fail | line 38 puts the date first |
| month 01–12 (1) | `month-13-allowed`, `month-00-allowed` | fail, fail | lines 52, 53 |
| day 01–31 (1) | `day-32-allowed`, `day-00-allowed` | fail, fail | lines 54, 55 |
| date not alnum-adjacent (6, 7) | `date-no-left-boundary`, `date-no-right-boundary` | fail, fail | lines 56, 57 |
| the file holds a compilable pattern (9, 10) | `empty-pattern`, `invalid-regex` | fail, fail | the compile step |
| the regex is saved at `/app/regex.txt` (9) | `regex-file-absent` | fail | the existence step |
| `findall` must return date strings, not tuples | `extra-capture-group` | fail | a capture group around the IP lookahead turns matches into tuples |
| a month-aware day range is accepted | `reference-month-aware` | pass | compliant control (Feb ≤ 29, 30-day months capped) |
| a padded file is accepted (10) | `padded-file` | pass | compliant control (`strip()`) |
| **no leading-zero octets (4)** | `ip-leading-zeros-allowed` | **pass** | **unobserved** — no line has a leading-zero octet |
| **digit-adjacent dates (6)** | `date-boundary-letters-only` | **pass** | **unobserved** — letters-only boundaries suffice; `1134-12-1234` is not in the log |
| **four-digit year (1)** | `year-any-digit-count` | **pass** | **unobserved** — `\d{2,6}` passes |
| **month-length validity (implied by 1)** | `reference-lenient-days` | **pass** | **Feb 30 / Apr 31 sit only on invalid-IP lines** (65, 67) |
| **February 29 permitted (3)** | `feb-29-rejected` | **pass** | **unenforced in the permitting direction** — a Feb-28 cap passes; no `02-29` in the log |
| **any pattern logic at all** | `hardcoded-expected-dates` | **pass** | **the nine expected strings, joined by `|`** |

Two controls show the counter is not merely permissive: `reference-month-aware` (a stricter but
compliant pattern) and `padded-file` pass; every over-permissive pattern that the log *can* catch
fails with the expected list in the assertion text.

### The six findings, each bounded to this capture

1. **A hard-coded alternation of the nine expected dates returns without `AssertionError`** (reward 1 under
   S109's mapping). The log and the nine literals are fixed in the test file (whether an agent can read that
   file at solve time is a harness property this entry does not establish), so `2025-01-09|2024-11-01|…|1999-03-05` is a passing "regex". No case of a
   *general* date rule is required, and none is checked.
2. **The no-leading-zero-octet rule (instruction line 4) is unobserved.** A pattern whose octet
   alternation admits `01`-style octets passes, because every IP in the log is written canonically.
   The captured oracle has the same latitude (see below).
3. **Digit-adjacent dates are unobserved.** Forbidding only letters leaves `1134-12-1234` (the
   instruction's own example, line 6) undetected; a letters-only-boundary pattern passes, and the
   string `1134` does not occur in `test_outputs.py` (`grep -n '1134' …` exits 1).
4. **Year width is unobserved.** `\d{2,6}` for the year passes; only the four-digit form appears.
5. **Month-length validity never decides a valid-IP line.** `2000-02-30` and `2000-04-31` occur only
   on lines whose IP is `172.16.0.256`, so a day-01–31-for-every-month pattern passes. The
   distinction "valid IP *and* month-length-invalid date" is never constructed.
6. **The permitting side of February 29 is unobserved.** The instruction allows Feb 29 in all years;
   a pattern capped at Feb 28 also passes, because the log contains no `02-29` at all.

A trajectory or submission analysis that reads a 1 as "the agent implemented the stated date rule"
is therefore reading more than this grader decides. Every finding is a property of *this* fixed
fixture; none says the task is invalid, only that these requirements are untested by it.

## What `test.sh` does with the outcome (S109)

`test.sh` installs `curl` and `uv 0.9.5`, then runs the one test file under `uvx -p 3.13` with
`pytest==8.4.1` and `pytest-json-ctrf==0.3.5`, and writes the reward from the exit status:

```
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
```

So the score is binary and single-bit: one test function, one list comparison, `reward.txt` = 1 or 0,
with the CTRF JSON at `/logs/verifier/ctrf.json` as the only per-test detail. A partial compliance
(23 of 24 style) is indistinguishable from producing nothing. The script also refuses to run when
`PWD` is `/`, and exports `$HOME/.local/bin/env` before `uvx`.

## The oracle (`solution/solve.sh`, captured; tier C, own reading)

`solve.sh` writes one pattern (267 bytes) via a quoted heredoc to `/app/regex.txt`. Located readings of
that pattern, with the executed checks below — **own reading, not a graded result and not a registry
row**:

- IP branch: `(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)`, guarded by a
  lookahead `(?=.*(?:^|[^0-9A-Za-z])…(?=$|[^0-9A-Za-z]))` — octets 0–255, IP anywhere in the line.
- Date branch: `(\d{4}-(?:(?:01|03|05|07|08|10|12)-(?:0[1-9]|[12]\d|3[01])|(?:04|06|09|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|1\d|2[0-9])))`,
  i.e. month-aware day caps with February at most 29 — the instruction's month-length and Feb-29
  rules, in the oracle but untested by the fixture.
- Greedy `.*` before the date group ⇒ the last date on the line.

Executed against the captures (same `mod.Path` redirection the probe uses):

```
findall on the 25-line log: ['2025-01-09', '2024-11-01', '2020-01-01', '2019-06-15', '2018-06-06', '2017-03-03', '2016-12-31', '2024-11-11', '1999-03-05']
captured grader on oracle pattern: pass
'x 10.1.1.1 on 2000-04-31' -> []
'x 10.1.1.1 on 2000-02-30' -> []
'x 10.1.1.1 on 2024-02-29' -> ['2024-02-29']
'x 10.1.1.1 on 2024-02-30' -> []
'x 01.2.3.4 on 2024-05-05' -> ['2024-05-05']
'x 007.2.3.4 on 2024-05-05' -> []
'x 10.1.1.1 on 1134-12-1234' -> []
octet group on 01: True | 007: False
```

Reading of that output: the oracle enforces month length and permits Feb 29 (so the fixture, not the
oracle, is where those requirements go untested); it forbids digit-adjacent dates and a `007` octet;
but it **admits a two-digit leading-zero octet** (`01.`) — the instruction's line-4 rule is not
enforced by the oracle either, and the fixture cannot see the difference.

## Post-hoc observations (outside the frozen 24 cases and outside C2's predicate)

Two wave-1 seats probed beyond the frozen table. Their scripts and run logs are committed under
`.ufo/waves/round-36/build/R36OracleRun/` and `.ufo/waves/round-36/build/R36CritUnenforced/`; their
predictions were written before their runs, but they were **not** frozen before the round, so they
are labelled observations, never claim results.

- **The task's own oracle is not line-scoped.** In `solve.sh` the class `[^0-9A-Za-z]` matches `\n`
  and is used both inside the IP lookahead and as the date's left boundary, so the oracle matches a
  date on a line with no address (`'1.2.3.4\n2020-01-01'` → `['2020-01-01']`) and prefers the next
  line's date over a qualifying line's own (`'1.2.3.4 2020-01-01\n2020-01-02'` → `['2020-01-02']`):
  5 of 6 multi-line probes violate instruction line 1. The fixture has no line pair that exposes it
  (`R36OracleRun.md` §4, §8). No frozen case covers it: every frozen candidate is anchored at `^`.
- **The oracle admits `00`–`09` octets** (ten illegal octets accepted, no legal octet rejected;
  `R36OracleRun.md` §8 item 1), so instruction line 4 is unenforced for the oracle too.
- **Four further requirement faces are free** (`R36CritUnenforced.md`, run v2/v3, `mismatches=0` after
  the seat's own helper defects were corrected): month/day field width (`2025-1-9` passes), the date
  separator set (`2025/01-09`, a space or newline between fields), IPv4 notation (`0255.1.2.3`,
  `1-2-3-4`, a `00` fourth octet) and boundary clauses that are *stricter* than the instruction
  (`.` or whitespace-only adjacency) all pass. Three angles that look free are enforced: scoping
  MULTILINE off, `(?s)`/`[\s\S]` cross-line bridges, and a pattern that requires a trailing newline.
- **Seat calibration datum.** The same seat's first 14 witnesses missed 10 predictions because its
  own helper omitted the date's left boundary and used a range-free date body, not because of the
  grader (`R36CritUnenforced.md` Round 1); predictions made from a static reading of a graded log
  without executing the grader are unreliable at that grain, which is why the frozen table was run
  rather than argued.

## Negative space

This entry does **not** establish: that the task is valid or well-calibrated (no run of the task
image, no model, no trajectory — that is PROVINCE's question, not this lane's); that the grader's nine
literals are the *right* expected values (they are the authors' assertion about their own fixture);
how Harbor executes the verifier (`benchmark-verifier-execution-model.md` covers where it runs);
anything about hidden or additional tests (the capture at this commit contains exactly one test
function, but a run could add files the capture does not show); any agent behaviour, pass rate or
failure mode; whether the `# Y:`/`# N:` comments are accurate beyond the 24 executed patterns; or
anything about the other TB2 tasks. The probe runs the captured function under the host Python, not
inside `alexgshaw/regex-log:20251031`.

**Falsifier:** this entry is falsified if (a) a re-fetch of the three pinned URLs yields bytes whose
SHA-256 differs from `corpus/evidence/round36/tb2-regex-log/SHA256SUMS`; (b) a fresh run of
`plans/regex_log_probe.py --lane .` prints anything other than
`cases=24 observed_pass=8 observed_fail=16 mismatches=0` (for example `hardcoded-expected-dates`
observed `fail`, or `ip-leading-zeros-allowed` observed `fail`); (c) the captured grader applied to a
pattern that is a plain alternation of the nine expected strings raises `AssertionError`; or (d) the
fixture is shown to contain a Feb-29 date, a leading-zero octet, a digit-adjacent valid date, a
non-four-digit year, or a month-length-invalid date on a valid-IP line (the AST walk above prints
`feb29 anywhere: 0` and `leading-zero-octet lines: []`).

## Located quotes

Quotes are byte-exact from the round-36 captures (`corpus/evidence/round36/tb2-regex-log/`, identical
to the pinned raw files at `2fd12b88`), each 3–25 words, verified with `grep -nF`.

| Claim supported | “Quote” | `file:line` |
|---|---|---|
| the graded artefact is an agent-authored regex file | “Test that the agent created a file with a regex, that the regex is valid,” | `test_outputs.py:10` |
| the grader's own statement of the rule | “and that it correctly matches (the last) dates in log lines containing at least one” | `test_outputs.py:11` |
| the log is authored as Y/N labeled literals | “# Sample logs covering various scenarios: Y (should match), N (should not match)” | `test_outputs.py:33` |
| the graded file path is fixed | “regex_file = Path("/app/regex.txt")” | `test_outputs.py:21` |
| a missing file fails | “assert regex_file.exists(), f"Regex file {regex_file} does not exist"” | `test_outputs.py:22` |
| the file is read and stripped | “pattern_text = regex_file.read_text().strip()” | `test_outputs.py:25` |
| the expected list is the authors' literal | “# Expected matches based on "last date after a valid IPv4" rule” | `test_outputs.py:70` |
| multiple dates on one line, last wins | “"192.168.1.100 accessed on 2023-12-31 and 2024-11-01",” | `test_outputs.py:36` |
| multiple IPs, one date, still a match | “"Multiple IPs 10.0.0.1 10.0.0.2 with 2020-01-01",” | `test_outputs.py:39` |
| a date-like non-date is intended to be rejected | “"Broadcast 255.255.255.255 for user 1234-56-7890",” | `test_outputs.py:48` |
| month 13 is a fixture rejection | “"Connection from 192.168.0.10 on 2023-13-05",  # N: month > 12” | `test_outputs.py:52` |
| Feb 30 sits on an invalid-IP line | “"Login attempt 172.16.0.256 for user 2000-02-30",” | `test_outputs.py:65` |
| Apr 31 sits on an invalid-IP line | “"Login attempt 172.16.0.256 for user 2000-04-31",  # N: invalid date 31th April” | `test_outputs.py:67` |
| letters after a date are a fixture rejection | “"User 192.0.2.1 performed action 2020-07-15abc",  # N: alphanumeric after date” | `test_outputs.py:56` |
| fixture lines are joined into one text | “log_text = "\n".join(sample_logs)” | `test_outputs.py:84` |
| the pattern runs through findall with MULTILINE | “matches = re.findall(pattern_text, log_text, re.MULTILINE)” | `test_outputs.py:87` |
| the decision is full-list equality | “assert matches == expected_dates, f"Expected {expected_dates}, but got {matches}"” | `test_outputs.py:90` |
| the test outcome is the pytest exit status | “if [ $? -eq 0 ]; then” | `test.sh:25` |
| pass writes reward 1 | “echo 1 > /logs/verifier/reward.txt” | `test.sh:26` |
| fail writes reward 0 | “echo 0 > /logs/verifier/reward.txt” | `test.sh:28` |
| one file, one run, CTRF report | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” | `test.sh:22` |
| the rule the task states | “Write a regex expression that matches dates in the format YYYY-MM-DD appearing in lines that contain an IPv4 address in a log file.” | `instruction.md:1` |
| last-date rule is stated | “If multiple dates are present in a line, the regex should match only the last date in that line.” | `instruction.md:2` |
| Feb 29 is permitted in all years | “Assume that February can have up to 29 days in all years, without distinguishing leap years from non-leap years.” | `instruction.md:3` |
| no leading-zero octets is stated | “IPv4 addresses use normal decimal notation without leading zeros in each octet.” | `instruction.md:4` |
| the digit-adjacency example is instruction-only | “that looks similar to dates or IPv4 addresses but is not (e.g., user 1134-12-1234).” | `instruction.md:6` |
| alnum adjacency is stated | “To avoid false matches, ensure that valid dates and IPv4 addresses are not immediately preceded or followed by alphanumeric characters.” | `instruction.md:7` |
| the artefact is a file at a fixed path | “Save your regex in /app/regex.txt” | `instruction.md:9` |
| the execution model is disclosed to the agent | “The regex will be read from the file and applied to the log file contents using Python's re.findall with the re.MULTILINE flag.” | `instruction.md:10` |
