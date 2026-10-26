DRAFT — paste-ready append-only section for `corpus/knowledge/tb2-regex-log-grader.md` (seat R37R36Absorb,
round 37 wave 1). Nothing in the lane was edited; this file is the draft for the L1.

---

## Errata (round 37)

Appended 2026-10-26 (round 37, wave 1). This file is append-only: the bytes above stand as filed, and this
section is the correction of record. Every number below was measured on the pinned capture in this lane
(`sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS` → 5/5 `OK`, 2026-10-26) against the frozen
`plans/regex_log_probe.py` case table; the attribution script and its output are filed at
`.ufo/waves/round-37/build/R37R36Absorb/`.

**Erratum (round 37): S110 anchor sha256.** `corpus/SOURCES.md:125` files the digest as
`4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` — **63 hex digits**, the `0` at index 15
dropped. The pinned `instruction.md` is
`4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` (**64 hex**;
`corpus/evidence/round36/tb2-regex-log/SHA256SUMS:3`; `sha256sum instruction.md` today agrees). Wrong:
`…922ea0…` (63). Correct: `…9220ea0…` (64).

**Erratum (round 37): the S110 span disagrees between this file's `source:` line and the SOURCES row, and
neither is the requirement-bullet span.** Measured on the pinned file (19 lines): the requirement sentences
are lines 1–4, 6–7 and 9–10 (5 and 8 blank); line 11 is `Example Python usage:`; 12–19 are the example code
block. This file's `lines 1–11` therefore includes one non-requirement line, and the row's
`instruction.md:1-19` includes eight. Exact bullet anchor: `instruction.md:1-10`.

**Erratum (round 37): the `What decides it` column is not receipt-backed, and two of its rows are not
independent evidence.** The receipt (`corpus/evidence/round36/regex-log-probe.txt`) carries no per-line field
— its fields are `case/predicted/observed/match/assertion/requirement` — and **11 of its 16 failing cases
carry a byte-identical `assertion=` string** (6 distinct assertion strings over the 16 fails, 7 over all 24
cases), so no receipt line can say which fixture line decided a failure. The line numbers in that column were
re-derived by executing the frozen case patterns over the log rebuilt from the capture (23 file-mode cases:
0 `observed=` mismatches against the receipt once the grader's `.strip()` is applied). Corrections:

| entry row | case(s) | cell as filed | measured |
|---|---|---|---|
| `only lines containing an IPv4 address (1)` | `no-ip-condition` | line 37 has a date and no IP | **38** (`No IP here but 2022-05-05 appears`); 37 is a comment. The case flips 9 lines (38, 44, 45, 50, 62, 63, 64, 65, 67) — a superset of the two rows below, so it is coarse, not attributable |
| `last date on a line (2)` | `first-date-only` | line 36 has two dates | 36 ✓, **and 42** (`2018-05-05 8.8.8.8 info 2018-06-06`) |
| `octets 0–255 (4)` | `ip-octets-unbounded` | lines 41–42, 62, 65, 67 carry 256 / 456 | **44, 45, 64, 65, 67**; 41, 42 and 62 carry no out-of-range octet |
| `IPv4 not alnum-adjacent (7)` | `ip-no-left-boundary`, `ip-no-right-boundary` | lines 60, 61 (`abc` before / after the IP) | **63** (`abc10.0.0.5`, before) and **62** (`192.168.1.1abc`, after); 60 is a Y line, 61 a comment |
| `IP may sit after the date (1, implicitly)` | `ip-before-date-only` | line 38 puts the date first | **35, 41, 59**; 38 has a date and no IPv4 at all |
| `month 01–12` (52, 53) / `day 01–31` (54, 55) / `date not alnum-adjacent` (56, 57) | the six rows | as filed | ✓ exact, one flipped line each |
| `month-length validity (implied by 1)` | `reference-lenient-days` | (65, 67) | ✓ exact |

**Not independent evidence — the alnum-adjacency pair and the octet row.** Measured flip sets (sample-line →
file line): `ip-octets-unbounded` = {44, 45, 64, 65, 67}; `ip-no-left-boundary` = {44, 50, 63};
`ip-no-right-boundary` = {62, 64, 65, 67}. So 4 of the pair's 7 flips are lines the octet row owns. For
`ip-no-right-boundary` **only 1 of its 4** flipped lines is the boundary line it is named for: the other three
are the `172.16.0.256` lines, where the missing trailing guard reads the invalid octet `256` as the valid
address `172.16.0.25`. For `ip-no-left-boundary` the invalid-octet line 44 (`256.100.50.25` →
`56.100.50.25`) is likewise not an adjacency line. Read the pair as one case with the octet row, not as
independent evidence for instruction line 7. The clean single-requirement rows are `first-date-only` (36, 42),
the month pair (52, 53), the day pair (54, 55) and the date-boundary pair (56, 57).

**Unchanged and still correct (re-measured, no correction):** the `What the grader checks` line spans
(`34–68, 84`, `71–81`, `87`, `90`) and the four `unobserved` rows — `feb-29` lines `[]`, leading-zero-octet
lines `[]`, `1134` lines `[]`, and the `hardcoded-expected-dates` alternation still equals `expected_dates`.

---

Evidence commands (all read-only, run from the lane root with `python3 -B`, no `__pycache__` written into
`corpus/evidence/`):

```
$ sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS        # 5/5 OK
$ grep -n 'expected_dates = \[\|^    \]' corpus/evidence/round36/tb2-regex-log/test_outputs.py
71:    expected_dates = [
68:    ]
81:    ]
$ python3 -B .ufo/waves/round-37/build/R37R36Absorb/attribution.py     # per-line flips, reproduced receipt
$ python3 -B .ufo/waves/round-37/build/R37R36Absorb/receipt-verdicts.py # 0 mismatches
```
