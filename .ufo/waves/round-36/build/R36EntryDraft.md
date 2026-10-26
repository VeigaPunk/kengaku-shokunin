# R36EntryDraft — C2 knowledge entry draft (`tb2-regex-log-grader.md`)

Seat: R36EntryDraft (scribe, leaf). Round 36 wave 1, 2026-10-25. No product file touched; the draft
is a build artefact for the L1 to integrate.

## Behaviour

Drafted `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36EntryDraft/entry.md`
(237 lines, 18.4 KB) as the exact bytes intended for `corpus/knowledge/tb2-regex-log-grader.md`.

Content, in the order it appears:

1. Five header lines exactly per the frozen W3 contract — `source: S108 … test_outputs.py`,
   `source: S109 … test.sh`, `source: S110 … instruction.md` (bare pinned URLs, no fragment),
   `verified-at: 2026-10-25`, `recheck: 180d — …`.
2. Summary: one test function `test_regex_matches_dates`; the graded artefact is a regex **pattern
   file** at `/app/regex.txt`; the 25-line log is hard-coded in the test file; nine literal expected
   dates; receipt summary `cases=24 observed_pass=8 observed_fail=16 mismatches=0` verbatim on its
   own line; Amendment-1 disclosure (pre-scoring `<tmp>` repair) in the `## Source labels` section.
3. `## What the grader checks (static reading, test_outputs.py)` — 6-row mechanism table with line
   spans, plus the executed fixture structure (`sample_logs: 25 expected_dates: 9`,
   `feb29 anywhere: 0`, `leading-zero-octet lines: []`) and the fixture's designed distinctions read
   from the `# Y:`/`# N:` comments.
4. `## Instruction requirement → enforcing assertion (executed, 24 cases)` — 19-row table covering
   **all 24 probe cases** (16 enforced + 2 compliant controls + 6 unenforced-requirement findings),
   then the six findings as numbered prose.
5. `## What test.sh does with the outcome (S109)` — `uvx -p 3.13`, `pytest==8.4.1`,
   `pytest-json-ctrf==0.3.5`, `/logs/verifier/ctrf.json`, binary `reward.txt`, the `PWD=/` guard,
   `$HOME/.local/bin/env`.
6. `## The oracle (solution/solve.sh, captured; tier C, own reading)` — located readings of the
   267-byte pattern plus an executed own-reading block (the pattern through the captured grader,
   `findall` over the 25-line log, and four synthetic lines showing month length, Feb 29, `01.`
   admittance and `1134-12-1234` rejection). Explicitly marked not-a-registry-row and not a graded
   result.
7. `## Negative space` — what is not established (task validity, hidden tests, agent behaviour, the
   other TB2 tasks, Harbor runtime, comment accuracy, host-Python caveat) and a four-clause
   **Falsifier** ((a) pinned-digest change, (b) probe summary change, (c) alternation-of-literals
   rejection, (d) fixture containing a Feb-29 / leading-zero / digit-adjacent / other-width /
   month-length-invalid-on-valid-IP line).
8. `## Located quotes` — one header row, one separator, **29 quote rows**, 29 distinct quotes, 29
   distinct `(file, line)` locations, 3–23 words each.

## Gates

Real frozen gate run against the draft (not a reimplementation — the module's own `w3` with
`ENTRY` repointed at the draft, because the entry is not yet installed in `corpus/knowledge/`):

```
$ python3 - <<'PY'   # imports plans/round36_c2_verify.py, sets v.ENTRY to the draft, calls v.w3(lane)
real gate w3 on draft: ok
```

W3 clauses exercised by that call: the three `source:` lines with the pinned URLs at lines 1–3,
line 4 `verified-at: 2026-10-25`, line 5 `recheck: 180d …`, `## Negative space` containing
`falsif`, every located-quote row parsing, ≥8 rows / ≥8 distinct quotes / ≥8 distinct locations, and
each quote verbatim inside its cited capture lines.

Entry-side W5 conditions checked separately:

```
$ python3 - <<'PY'  # substring checks over the draft
summary line present: True
PY
```

and `match=NO` case names: **none** — the receipt has `mismatches=0`, every line reads
`match=yes`, so the "entry must name every mismatching case" clause is vacuously satisfied. No
receipt line was cited with a different verdict; no mismatch claim is made anywhere in the entry.

Independent digest re-check of the capture (read-only):

```
$ (cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS)
test_outputs.py: OK
test.sh: OK
instruction.md: OK
task.toml: OK
solve.sh: OK
$ sha256sum plans/regex_log_probe.py
d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc  plans/regex_log_probe.py
```

The three pinned digests equal the counter's `FILES` constants (`345c3bd0…`, `4770437e…`,
`4f7ac05e…`) and the probe digest equals the Amendment-1 constant `d58194c8…`.

Not run by this seat (integration-dependent, L1's to run): the full
`python3 plans/round36_c2_verify.py --lane .` (W1 needs nothing from me, W2 needs SOURCES rows
S108–S110, W4 needs the README index row + coverage bullet and `files == index rows >= 43`, W6 the
census). The entry's own W3/W5 surface is green above.

## Touched surfaces

Writes only under the seat's build area:

- `.ufo/waves/round-36/build/R36EntryDraft/entry.md` — the draft.
- `.ufo/waves/round-36/build/R36EntryDraft.md` — this report.

No `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
`SHONEN.md` edit; no git/jj mutation; no temp fixture repo needed (all work was read-only against the
lane's captures, plus `mktemp`-free inline Python). No package installed.

## Evidence — the 29 quote verifications (`grep -nF`, run in `corpus/evidence/round36/tb2-regex-log`)

```
test_outputs.py :: 10:    Test that the agent created a file with a regex, that the regex is valid,
test_outputs.py :: 11:    and that it correctly matches (the last) dates in log lines containing at least one
test_outputs.py :: 33:    # Sample logs covering various scenarios: Y (should match), N (should not match)
test_outputs.py :: 21:    regex_file = Path("/app/regex.txt")
test_outputs.py :: 22:    assert regex_file.exists(), f"Regex file {regex_file} does not exist"
test_outputs.py :: 25:    pattern_text = regex_file.read_text().strip()
test_outputs.py :: 70:    # Expected matches based on "last date after a valid IPv4" rule
test_outputs.py :: 36:        "192.168.1.100 accessed on 2023-12-31 and 2024-11-01",
test_outputs.py :: 39:        "Multiple IPs 10.0.0.1 10.0.0.2 with 2020-01-01",
test_outputs.py :: 48:        "Broadcast 255.255.255.255 for user 1234-56-7890",
test_outputs.py :: 52:        "Connection from 192.168.0.10 on 2023-13-05",  # N: month > 12
test_outputs.py :: 65:        "Login attempt 172.16.0.256 for user 2000-02-30",
test_outputs.py :: 67:        "Login attempt 172.16.0.256 for user 2000-04-31",  # N: invalid date 31th April
test_outputs.py :: 56:        "User 192.0.2.1 performed action 2020-07-15abc",  # N: alphanumeric after date
test_outputs.py :: 84:    log_text = "\n".join(sample_logs)
test_outputs.py :: 87:    matches = re.findall(pattern_text, log_text, re.MULTILINE)
test_outputs.py :: 90:    assert matches == expected_dates, f"Expected {expected_dates}, but got {matches}"
test.sh :: 25:if [ $? -eq 0 ]; then
test.sh :: 26:  echo 1 > /logs/verifier/reward.txt
test.sh :: 28:  echo 0 > /logs/verifier/reward.txt
test.sh :: 22:  pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
instruction.md :: 1:Write a regex expression that matches dates in the format YYYY-MM-DD appearing in lines that contain an IPv4 address in a log file.
instruction.md :: 2:If multiple dates are present in a line, the regex should match only the last date in that line.
instruction.md :: 3:Assume that February can have up to 29 days in all years, without distinguishing leap years from non-leap years.
instruction.md :: 4:IPv4 addresses use normal decimal notation without leading zeros in each octet.
instruction.md :: 6:Note: Be careful that there might be text in the log that looks similar to dates or IPv4 addresses but is not (e.g., user 1134-12-1234). 
instruction.md :: 7:To avoid false matches, ensure that valid dates and IPv4 addresses are not immediately preceded or followed by alphanumeric characters.
instruction.md :: 9:Save your regex in /app/regex.txt
instruction.md :: 10:The regex will be read from the file and applied to the log file contents using Python's re.findall with the re.MULTILINE flag.
```

29/29 found, no MISS, every line number equal to the location cell in the draft. One quote
(`instruction.md:6`) is cited as the inner clause `that looks similar … 1134-12-1234).` because the
full line is exactly 25 words with a trailing space; the cited substring is byte-verbatim inside it
(shown by the grep hit above).

Structural numbers in the entry come from an AST walk over the capture (read-only):

```
sample_logs: 25 expected_dates: 9
feb29 anywhere: 0
feb30/apr31 lines: ['Login attempt 172.16.0.256 for user 2000-02-30', 'Login attempt 172.16.0.256 for user 2000-04-31']
leading-zero-octet lines: []
```

`grep -n '1134' corpus/evidence/round36/tb2-regex-log/test_outputs.py` → no match, exit 1 (the
instruction's digit-adjacency example does not occur in the fixture).

Oracle own-reading execution (tier C block in the entry):

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

## Findings (all bounded to this capture at `2fd12b88`)

1. **A literal alternation of the nine expected dates passes.** `hardcoded-expected-dates` observed
   `pass`; the fixture log is fixed and visible in the test file, so no general date logic is
   required by the score.
2. **The no-leading-zero-octet rule (instruction:4) is unobserved** — `ip-leading-zeros-allowed`
   passes; no fixture line carries a leading-zero octet (`leading-zero-octet lines: []`). The
   captured oracle also admits a two-digit leading-zero octet (`01.` → match, `007.` → no match),
   so the rule is unenforced on both sides of the capture.
3. **Digit-adjacent dates are unobserved** — `date-boundary-letters-only` passes; line 6's
   `1134-12-1234` example is absent from the fixture (`grep '1134'` exit 1).
4. **Year width is unobserved** — `year-any-digit-count` (`\d{2,6}`) passes.
5. **Month-length validity never decides a valid-IP line** — `reference-lenient-days` (day 01–31 for
   every month) passes; the only `2000-02-30` / `2000-04-31` lines carry `172.16.0.256`.
6. **The permitting side of Feb 29 (instruction:3) is unobserved** — `feb-29-rejected` (Feb capped at
   28) passes; `feb29 anywhere: 0`.
7. Enforced side, for balance: octets 0–255, month 01–12, day 01–31, alnum adjacency (letters),
   last-date-on-line, IP-anywhere-in-line, existence, compilability, and the tuple trap from an
   extra capture group all produce `fail` as predicted (16 cases).
8. Score shape: one test function, full-list equality, binary `reward.txt`, CTRF JSON as the only
   per-test detail (`test.sh:22,25,26,28`).

## Out of scope / limits

- The entry does not claim task validity, hidden tests, agent behaviour, or anything about other TB2
  tasks; it says so in `## Negative space` with per-claim falsifiers.
- The probe (and my oracle check) run the captured functions under the host Python, not inside
  `alexgshaw/regex-log:20251031`; the entry states this.
- `task.toml` and `solve.sh` are captured with digests but are **not** registry rows; the oracle
  section is tier C and the entry says nothing above it depends on the oracle.
- I did not draft the SOURCES rows, README index row, coverage bullet or QUALITY notes — other wave-1
  seats own those; W2/W4 remain the L1's gates.
- No mutation testing of the frozen counter (`plans/round36_c2_verify.py`) was attempted; a wave-2
  mutation seat may attack whether W3's quote gate can be satisfied by an off-topic quote
  (it cannot: the quote must be verbatim at the cited line, but *relevance* of a row's claim cell is
  not machine-checked — that is a named limit of the gate, not of this entry).

## Artifact paths

- Draft entry: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36EntryDraft/entry.md`
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36EntryDraft.md`
- Read-only inputs: `plans/round-36-claims.md`, `plans/round36_c2_verify.py`,
  `plans/regex_log_probe.py`, `corpus/evidence/round36/tb2-regex-log/{test_outputs.py,test.sh,instruction.md,solve.sh,task.toml,SHA256SUMS}`,
  `corpus/evidence/round36/regex-log-probe.txt`, `corpus/knowledge/tb2-protein-assembly-grader.md`
  (style model), `corpus/SOURCES.md` rows S105–S107 (format model), `corpus/README.md:68,257,282`.

VERDICT: entry-drafted-29-quotes
