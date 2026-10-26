# R36OracleRun — does the pinned TB2 `regex-log` oracle obey its own instruction?

Seat: executor, kengaku round 36 wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen claims read first: `plans/round-36-claims.md` (freeze `3241b86c`, Amendment 1 `acbda2f3`). No lane file
was edited; every artifact below is under `.ufo/waves/round-36/build/R36OracleRun/`.

## 0. Artifacts and how to reproduce

| path (relative to lane) | what |
|---|---|
| `.ufo/waves/round-36/build/R36OracleRun/oracle_probe.py` | the probe (sha256 `cf7b961c3adc8828aa8385c20a92886b2478195926f19a3bb14e49f87c5dfa66`) |
| `.ufo/waves/round-36/build/R36OracleRun/oracle-probe-receipt.txt` | receipt, 107 lines, sha256 `8ebceb5094989e74452ead4fea2fb3aad31ebda2a6a76b2ecbcd5998e4b6467c` |
| `.ufo/waves/round-36/build/R36OracleRun/test_outputs_ip_at_line_start.py` | derived modified grader copy for the fragility probe (§7); **not** a capture |
| `.ufo/waves/round-36/build/R36OracleRun/oracle-probe-run2.txt`, `-run3.txt` | intermediate runs, superseded by the receipt |

```
$ cd .ufo/waves/round-36/build/R36OracleRun && python3 oracle_probe.py > oracle-probe-receipt.txt 2>&1; echo exit=$?
exit=0
$ python3 oracle_probe.py > /tmp/oracle-probe-rerun.txt 2>&1; cmp oracle-probe-receipt.txt /tmp/oracle-probe-rerun.txt && echo DETERMINISTIC
DETERMINISTIC
```

Pinned inputs, hashed by the probe on every run:

```
oracle=corpus/evidence/round36/tb2-regex-log/solve.sh sha256=7e670d4f2b4bccb1e4db38f2a173e085ceda028c38167912b466b0a84fcc0999
grader=corpus/evidence/round36/tb2-regex-log/test_outputs.py sha256=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72
probe=plans/regex_log_probe.py sha256=d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc
```

The grader digest equals `plans/regex_log_probe.py:27 GRADER_SHA256`; the probe digest equals the Amendment-1
digest in the frozen claims. The oracle is extracted by parsing the heredoc, never by copying the string:
marker at `solve.sh:5`, body at `solve.sh:6`, terminator at `solve.sh:7`.

```
oracle_heredoc=solve.sh:5..7 body_line=6 chars=267 whitespace_tokens=1
```

## 1. Instruments used

- `plans/regex_log_probe.py:113 run_grader(mod_path, regex, mode)` — imported as a module (the probe guard at
  `plans/regex_log_probe.py:140` checks the grader digest only in `main()`, so `run_grader` imports the pinned
  file unchanged and monkeypatches `mod.Path`, exactly as C2 does).
- `re.findall(pattern, log, re.MULTILINE)` — the operation named in `instruction.md:10` and used at
  `test_outputs.py:87`.

## 2. (a) The oracle passes the real grader

```
[A] run_grader(oracle) verdict=pass assertion='-'
[A] run_grader(oracle + trailing newline as the heredoc writes it) verdict=pass
[A] fixture_lines=25 expected_count=9 got=['2025-01-09', '2024-11-01', '2020-01-01', '2019-06-15', '2018-06-06', '2017-03-03', '2016-12-31', '2024-11-11', '1999-03-05']
[A] findall_matches_expected=True
```

The second line re-runs with the trailing newline the heredoc actually writes; the grader strips it
(`test_outputs.py:25`). The third line is independent of the grader's own assertion: the 25 fixture strings
were re-parsed out of `test_outputs.py:34-68` and the 9 strings out of `test_outputs.py:71-81`, then
`re.findall` over the joined log reproduced the expected list exactly.

**The task's own oracle is a passing solution.** So the interesting question is what it gets away with.

## 3. (b) 40 hand-built probe lines — 4 violations, 1 ambiguity, 35 conformant

Verdict per row is the oracle's `findall` output on that single line vs the instruction's rule. `Y:date` =
exactly that date matched; `N` = no match. `instr:N` refers to `corpus/evidence/round36/tb2-regex-log/instruction.md`
line N.

| id | probe line | oracle | instruction | note |
|---|---|---|---|---|
| A1 | `from 01.2.3.4 at 2020-01-01` | `Y:2020-01-01` | N | **VIOLATION** — octet `01` has a leading zero (instr:4) |
| A2 | `from 192.168.0.01 at 2020-01-01` | `Y:2020-01-01` | N | **VIOLATION** — 4th octet `01` (instr:4) |
| A3 | `from 192.168.001.1 at 2020-01-01` | N | N | ok, but for the wrong reason: 3-digit `001` is excluded by width, not by the rule |
| A4 | `from 00.0.0.0 at 2020-01-01` | `Y:2020-01-01` | N | **VIOLATION** — octet `00` (instr:4) |
| A5 | `from 010.1.2.3 at 2020-01-01` | N | N | ok, same width artefact as A3 |
| A6 | `from 192.168.01.1 at 2020-01-01` | `Y:2020-01-01` | N | **VIOLATION** — 3rd octet `01` (instr:4) |
| B1 | `8.8.8.8 on 2020-02-29` | `Y:2020-02-29` | Y | Feb 29 permitted (instr:3) |
| B2 | `8.8.8.8 on 2019-02-29` | `Y:2019-02-29` | Y | Feb 29 in a non-leap year, as instr:3 demands |
| B3 | `8.8.8.8 on 2000-02-30` | N | N | Feb capped at 29 (instr:3) |
| B4 | `8.8.8.8 on 2020-04-31` | N | N | Apr has 30 days; instr is silent, grader comment `test_outputs.py:67` says invalid |
| B5 | `8.8.8.8 on 2020-01-31` | `Y:2020-01-31` | Y | 31-day month |
| B6 | `8.8.8.8 on 2020-04-30` | `Y:2020-04-30` | Y | 30-day month |
| B7 | `8.8.8.8 on 2020-02-28` | `Y:2020-02-28` | Y | Feb 28 |
| C1 | `8.8.8.8 on 12345-06-07` | N | N | year is YYYY (instr:1) |
| C2 | `8.8.8.8 on 999-06-07` | N | N | 3-digit year |
| C3 | `8.8.8.8 on 0000-01-01` | `Y:0000-01-01` | Y | 4-digit year; value unconstrained by the instruction |
| D1 | `user 1134-12-1234 8.8.8.8` | N | N | the instruction's own example (instr:6) |
| D2 | `x2020-01-01 8.8.8.8` | N | N | letter before date (instr:7) |
| D3 | `2020-01-012 8.8.8.8` | N | N | digit after date (instr:7) |
| D4 | `_2020-01-01 8.8.8.8` | `Y:2020-01-01` | Y | `_` is not alphanumeric |
| D5 | `2020-01-01. 8.8.8.8` | `Y:2020-01-01` | Y | `.` is not alphanumeric |
| E1 | `::1 on 2020-01-01` | N | N | IPv6, no dotted quad |
| E2 | `2001:db8::1 on 2020-01-01` | N | N | IPv6 |
| E3 | `fe80::1ff:fe23:4567:890a 2020-01-01` | N | N | IPv6 hex groups |
| E4 | `1.2.3.4.5 on 2020-01-01` | `Y:2020-01-01` | Y | 5-octet dotted string: `1.2.3.4` is followed by `.`, so literal instr:7 admits it — shared quirk, not a divergence |
| E5 | `version 1.2.3 on 2020-01-01` | N | N | three octets only |
| E6 | `1.2.3.256 on 2020-01-01` | N | N | octet > 255 |
| E7 | `255.255.255.255 on 2020-01-01` | `Y:2020-01-01` | Y | broadcast |
| E8 | `0.0.0.0 on 2020-01-01` | `Y:2020-01-01` | Y | zero address |
| F1 | `10.0.0.1 10.0.0.2 with 2020-01-01` | `Y:2020-01-01` | Y | two IPs, one date |
| F2 | `2020-01-01 came from 172.16.0.5` | `Y:2020-01-01` | Y | date before IP |
| F3 | `x 2020-01-01 y 2019-06-15 z 8.8.8.8` | `Y:2019-06-15` | Y | last date (instr:2) |
| F4 | `8.8.8.8 2020-01-01 2019-06-15` | `Y:2019-06-15` | Y | last date after IP |
| F5 | `2020-01-01 and 2019-06-15 then 8.8.8.8` | `Y:2019-06-15` | Y | last date, IP last |
| F6 | `8.8.8.8 2020-01-01 then 2021-02-02abc` | `Y:2020-01-01` | AMB | instr:2 ("last date") vs instr:7 (no alnum neighbour) conflict; oracle falls back to the earlier valid date — defensible, unspecified |
| F7 | `no ip 2020-01-01 at all` | N | N | no IPv4 |
| F8 | `8.8.8.8abc 2020-01-01` | N | N | alnum after IP |
| F9 | `abc8.8.8.8 2020-01-01` | N | N | alnum before IP |
| F10 | `8.8.8.8 2020-13-01` | N | N | month 13 |
| F11 | `8.8.8.8 2020-01-32` | N | N | day 32 |

```
[B] rows=40 violations=4 ambiguous=1
```

Whole-match spans prove the `A` rows are matched **through** the bad address, not around it:

```
A1 line='from 01.2.3.4 at 2020-01-01' span=(0, 27) text='from 01.2.3.4 at 2020-01-01' capture=('2020-01-01',)
A2 line='from 192.168.0.01 at 2020-01-01' span=(0, 31) text='from 192.168.0.01 at 2020-01-01' capture=('2020-01-01',)
A4 line='from 00.0.0.0 at 2020-01-01' span=(0, 27) text='from 00.0.0.0 at 2020-01-01' capture=('2020-01-01',)
A6 line='from 192.168.01.1 at 2020-01-01' span=(0, 31) text='from 192.168.01.1 at 2020-01-01' capture=('2020-01-01',)
```

No row is a false negative: every line the instruction says must match, the oracle matches, with the right date.

### 3.1 Exact shape of the leading-zero hole

An exhaustive sweep of 1 110 candidate octet strings (`str(i)` for 0..999, `%02d` 0..99, `%03d` 0..999),
each placed in each of the four octet positions of `<o>.9.9.9`-style addresses on a dated line:

```
[OCT] candidates=1110 instruction-invalid octets accepted by the oracle, by octet position 1..4: [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'], ['00', ..., '09'], ['00', ..., '09'], ['00', ..., '09']]
[OCT] accepted sets identical across positions=True count=10
[OCT] all-four leading-zero case '01.01.01.01' matches=True
[OCT] instruction-valid octets the oracle rejects: []
```

So the oracle accepts exactly ten instruction-illegal octets — `00`..`09` — identically in all four positions, and
rejects no legal one. The mechanism is `1?\d?\d` (`solve.sh:6`): a three-character octet can only be produced by
`1?` + `\d?` + `\d`, so any leading zero forces the two-digit reading, while `0\d\d` can never be consumed as
three characters — hence A3/A5 are rejected by width, not by the leading-zero rule. `rejection/acceptance` is a
property of the alternation, not of a check.

## 4. The bigger defect: the oracle is not line-scoped (new; not in the round-36 probe)

`[^0-9A-Za-z]` matches `\n`, and that class is used twice — inside the IP lookahead and as the date's left
boundary. The oracle therefore joins lines in two directions: the date may land on the line *after* the IP line
(when that next line *starts* with the date), and the IP lookahead may reach an IP that *starts* the next line
(when the current line has no IP). `instruction.md:1` says "dates ... appearing in lines that contain an IPv4
address".

```
[G] multi-line probes (a line's own IP is the instruction's condition, instr:1)
G1-date-at-start-of-IP-less-line log='1.2.3.4\n2020-01-01' instruction=[] oracle=['2020-01-01'] spans=[(0, 18)] VIOLATION
G2-date-on-line-then-IP-starts-next log='2020-01-01\n1.2.3.4' instruction=[] oracle=['2020-01-01'] spans=[(0, 10)] VIOLATION
G3-last-date-crosses-to-IP-less-line log='1.2.3.4 2020-01-01\n2020-01-02' instruction=['2020-01-01'] oracle=['2020-01-02'] spans=[(0, 29)] VIOLATION
G4-both-lines-qualify log='1.2.3.4 2020-01-01\n5.6.7.8 2021-02-03' instruction=['2020-01-01', '2021-02-03'] oracle=['2020-01-01', '2021-02-03'] spans=[(0, 18), (19, 37)] ok
G5-ip-less-line-then-IP-start log='x 2020-01-01\n1.2.3.4 2021-02-03' instruction=['2021-02-03'] oracle=['2020-01-01', '2021-02-03'] spans=[(0, 12), (13, 31)] VIOLATION
G6-date-then-next-line-starts-with-date log='1.2.3.4 2020-01-01\n2021-02-03 more' instruction=['2020-01-01'] oracle=['2021-02-03'] spans=[(0, 29)] VIOLATION
[G] rows=6 violations=5
```

- G1: the match span `(0, 18)` covers `1.2.3.4\n2020-01-01` — the captured date's own line has no address.
- G3/G6 are false negatives *and* false positives at once: the qualifying line's date is dropped and the
  unqualified line's date is returned, because the greedy `.*` treats the pair as one span.
- G4 shows the oracle is correct when each line carries its own IP and a mid-line date, so the leak is a
  boundary artefact, not a general scanning bug.
- The leak survives only when the neighbouring line **starts** with the date or with the IP (the `.*` before the
  class cannot cross a newline; only the single newline character can be consumed).

**Blind spot in the frozen probe:** all 24 C2 cases are built by `plans/regex_log_probe.py:53-57 line_rx`,
which returns `rf"^(?=.*{ipx}){star}{datex}"` — anchored at `^`. An anchored candidate cannot exhibit a
cross-line leak, so no frozen case could have observed this, whatever its prediction. This is a fact about the
probe file, not a change to C2's predicate.

## 5. Which requirements the pinned fixture can actually see (mutant sweep)

Each mutant is a whole-substring splice of the extracted oracle, run through the *pinned* grader by the same
`run_grader`:

```
M0-unmodified-oracle mutated=False verdict=pass requirement=control
M1-strict-octets mutated=True verdict=pass requirement=no leading-zero octets (instr:4)
M2-feb-30 mutated=True verdict=pass requirement=Feb 30 accepted
M3-apr-31 mutated=True verdict=pass requirement=Apr/Jun/Sep/Nov 31 accepted
M4-year-width mutated=True verdict=pass requirement=year width 2..6 (instr:1 YYYY)
M5-left-boundary-letters-only mutated=True verdict=pass requirement=date left boundary blocks letters only
M6-right-boundary-letters-only mutated=True verdict=pass requirement=date right boundary blocks letters only (digit adjacency allowed)
M7-first-date-only mutated=True verdict=fail requirement=positive control: lazy .* must break the battery
```

The fixture separates `M7` (so it is not inert) but it cannot separate any of M1-M6: a pattern that *obeys*
`instr:4` scores exactly like the oracle, and patterns that break `instr:3`'s Feb cap, calendar month lengths,
`instr:1`'s four-digit year, or digit-adjacency score identically too. The oracle's leading-zero violation is
therefore free.

Why the month-length negatives are blind (`test_outputs.py:64-68`) — both lines carry `172.16.0.256`:

```
[F] feb30_line='Login attempt 172.16.0.256 for user 2000-02-30' invalid_ip_present=True
[F] apr31_line='Login attempt 172.16.0.256 for user 2000-04-31' invalid_ip_present=True
[F] feb30 line as-is: oracle=N
[F] feb30 line with 172.16.0.256->172.16.0.25: M2=['2000-02-30']
[F] apr31 line as-is: oracle=N
[F] apr31 line with 172.16.0.256->172.16.0.25: M3=['2000-04-31']
[F] synthetic negative line 'from 01.2.3.4 with 2020-01-01': oracle=['2020-01-01'] M1-strict=N (fixture cannot separate them: it has no such line)
[F] fixture_lines=25 lines_with_a_leading_zero_octet=0 []
```

The Feb-30 / Apr-31 assertions are satisfied by the IP rule alone; correcting the IP to a legal one makes M2/M3
match immediately. And there is no line at all in the 25-line fixture whose only address has a leading zero.

## 6. Fragility of the fixture's negative cases (one-token edit separates oracle from instruction)

Copying the pinned grader into my scratch dir and moving the 4th fixture entry's IP (`test_outputs.py:39`) to the start of its line
(`Multiple IPs 10.0.0.1 ...` → `10.0.0.1 Multiple IPs ...`, everything else byte-identical, `expected_dates`
untouched):

```
[X] run_grader(oracle, modified copy) verdict=fail
[X] modified-copy log findall=['2025-01-09', '2024-11-01', '2022-05-05', '2020-01-01', '2019-06-15', '2018-06-06', '2017-03-03', '2016-12-31', '2024-11-11', '1999-03-05']
[X] extra=['2022-05-05'] missing=[]
[X] fixture line starts with an IP: [1]; line starts with a date: [0, 18]
```

The extra match is `2022-05-05` from `test_outputs.py:38` (`No IP here but 2022-05-05 appears`, expected N) — it
gains an "IP" because the next line now starts with `10.0.0.1`. The pinned ordering happens to hide the leak: the
fixture's only date-bearing N entry (`test_outputs.py:38`) is followed by a line starting with the word `Multiple`. The fixture is
order-lucky, and one token of reordering turns the pinned oracle red. The modified copy is a probe artifact in
my scratch dir; the pinned file is untouched.

## 7. Quoted fragments with `solve.sh` line numbers

The heredoc body (`solve.sh:6`) is one whitespace token of 267 characters, so every regex sub-fragment below is a
1-word quote (limit 25); only the heredoc line itself is a phrase.

| fragment | location | words | role / defect |
|---|---|---|---|
| `cat << 'EOF' > /app/regex.txt` | `solve.sh:5` | 5 | heredoc open, writes `/app/regex.txt` (instr:9) |
| `(?=.*(?:^|[^0-9A-Za-z])` | `solve.sh:6` | 1 | IP lookahead; its `.*` + `[^0-9A-Za-z]` reach one character past the line end (V2) |
| `(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)` | `solve.sh:6` | 1 | the octet alternation repeated for both the counted and the last octet |
| `1?\d?\d` | `solve.sh:6` | 1 | the leading-zero hole: accepts `00`..`09` in every position (V1) |
| `(?=$|[^0-9A-Za-z])` | `solve.sh:6` | 1 | IP right boundary (correct: alnum-adjacency rejected) |
| `.*(?:^|[^0-9A-Za-z])(\d{4}-` | `solve.sh:6` | 1 | date left boundary and the capture group; the newline-as-boundary leak (V2) |
| `(?:01|03|05|07|08|10|12)-(?:0[1-9]|[12]\d|3[01])` | `solve.sh:6` | 1 | 31-day months |
| `(?:04|06|09|11)-(?:0[1-9]|[12]\d|30)` | `solve.sh:6` | 1 | 30-day months (stricter than any rule stated in the instruction) |
| `02-(?:0[1-9]|1\d|2[0-9])` | `solve.sh:6` | 1 | February capped at 29 in all years — matches `instruction.md:3` exactly |
| `(?=$|[^0-9A-Za-z])` | `solve.sh:6` | 1 | date right boundary (correct) |
| `EOF` | `solve.sh:7` | 1 | heredoc close |

## 8. Answer to the key question

**Yes — the task's own oracle violates two instruction requirements, and passes the grader anyway.**

1. **Leading zeros (`instruction.md:4`, "IPv4 addresses use normal decimal notation without leading zeros in
   each octet").** `1?\d?\d` (`solve.sh:6`) accepts `00`..`09` in all four octet positions; demonstrated on four
   hand-built lines (A1, A2, A4, A6) whose whole-match spans contain the illegal address, and characterised
   exhaustively (10 illegal octets accepted, 0 legal octets rejected). The oracle's own `1?\d?\d` is the exact
   cause: the compliant form is `(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)`, which scores identically on the pinned
   fixture (M1 `verdict=pass`).
2. **Line scope (`instruction.md:1`, "dates ... appearing in lines that contain an IPv4 address").** Because
   `[^0-9A-Za-z]` matches `\n` and is used both in the lookahead and as the date's left boundary, the oracle
   matches a date on a line whose own text has no address (G1, G2, G5) and drops a qualifying line's date in
   favour of the next line's (G3, G6): 5 of 6 multi-line probes violate instr:1.

Neither violation costs the oracle a point, because the pinned 25-line fixture contains no leading-zero address
(`[F] lines_with_a_leading_zero_octet=0`), no line that both starts with a date and follows an IP line, and no
N-dated line followed by a line starting with an IP. The instruction's remaining clauses are obeyed: the last
date per span (instr:2), Feb 29 in every year (instr:3), four-digit years, alphanumeric-adjacency rejection
(instr:7), `[^0-9A-Za-z]` boundaries including the instruction's own `1134-12-1234` example, IPv4 range 0-255,
and a single capture group so `findall` returns strings.

The one case the instruction cannot decide is F6 (`8.8.8.8 2020-01-01 then 2021-02-02abc`): `instr:2` wants the
last date, `instr:7` forbids that token. The oracle returns `2020-01-01`. Labelled ambiguous, not counted as a
violation.

## 9. Advisory notes for the L1 (not edits — I wrote no lane file)

- C2's entry text already states that leading-zero octets are unenforced; the receipt above upgrades that from
  a synthetic candidate (`plans/regex_log_probe.py:30 OCT_LZ`, case `ip-leading-zeros-allowed` at line 75) to
  the pinned oracle itself, and pins the accepted set to `00`..`09`.
- The line-scope leak is **not** covered by any of the 24 frozen cases, and cannot be by construction
  (`plans/regex_log_probe.py:53-57` anchors every candidate at `^`). If the L1 wants it in the entry, the honest
  route is a disclosed post-hoc observation in the entry's findings (with these six line pairs), not a new frozen
  case. My verdict does not depend on that decision.
- The `[X]` fragility is a concrete, one-token demonstration for the entry's "the fixture is fixed and visible"
  point: the grader's N cases are order-lucky, not structural.

## 10. Limits and risks

- The TB2 harness (docker, `/app/regex.txt`) was not run; grading was reproduced offline through the pinned
  `test_outputs.py` body with `mod.Path` monkeypatched, exactly as `plans/regex_log_probe.py:113-128` does for
  C2. The application step (`re.findall(pattern, log, re.MULTILINE)`) is the grader's own.
- My 40-line table is single-line by design; per-line semantics are the instruction's ("lines that contain"),
  and the multi-line section is where that assumption is tested.
- `[X]` uses a modified copy of the grader in my scratch dir. It is labelled derived, hashed nowhere, and is not
  a claim about the pinned digest.
- Predictions were not pre-registered for this seat's table; the table was written from the instruction text and
  the oracle's source before running it (the oracle's `1?\d?\d` was read first, so A1-A6 was the expected
  finding; G1-G6 was not).
- Every number above is a line of `oracle-probe-receipt.txt`, reproducible with the command in §0.

VERDICT: oracle-passes-grader-yes-violations-2
