# R36CritUnenforced — critic, round 36 wave 1

Seat: critic (leaf; no subagents, no background jobs). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: wave-1 falsifier only. Nothing in `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`,
`SKILL.md`, `PROVINCE.md`, `SHONEN.md` was written; no git/jj mutating command was run; no tool was
installed. All artefacts are under `.ufo/waves/round-36/build/R36CritUnenforced/`.

## Hypothesis under test

H: *the pinned `regex-log` grader leaves at least 3 instruction requirements unenforced **beyond** the
probe's frozen 24 cases.*

Canonical sources used (read, not modified):

- `plans/round-36-claims.md` (C2 bullet, Amendment 1).
- `corpus/evidence/round36/tb2-regex-log/{test_outputs.py,instruction.md,test.sh}` — grader sha256
  `345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72` (re-checked by every script below
  before running; pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`).
- `plans/regex_log_probe.py` (amended digest `d58194c8…`), `corpus/evidence/round36/regex-log-probe.txt`.

Everything below is **supplementary**: it is outside the frozen C2 predicate (W1-W6, the 24-case
table, the receipt). It cannot fail C2 and cannot repair it; a surviving mutant is a *limit*
(round-35 convention), not a defect to be patched into the frozen battery.

## Method (reproducible)

Each table imports the probe's own `run_grader` (so the pinned grader, the grader's own `log_text`,
the `.strip()` of the regex file and the `assert matches == expected_dates` comparison are *verbatim*),
re-verifies the grader digest itself, and checks that no witness string is one of the frozen 24
(`duplicates_of_frozen_24=[]` printed by every run). Predictions are in the source file, and each file
was hashed **before** its run.

| round | file | sha256 (pre-run) | run log |
|---|---|---|---|
| v1 (14 cases) | `extra_cases.py` | `c1025e9ade52b2843d198a1159f96f3c481434ab581d2735372fc7bafceac89a` | `extra-cases-run.txt` |
| v2 (17 cases, corrected helper) | `extra_cases_v2.py` | `d1cbd3df6b40dd2d9167ea8bbc4814b2c3802feb9fe42c08208dc05b48d9129a` | `extra-cases-v2-run.txt` |
| v3 (2 cases, corrected V06 + IP separator) | `extra_cases_v3.py` | `07aaf9863928af51b9f68f26086cb033aad7212d33f1a5324959e11e17c84f17` | `extra-cases-v3-run.txt` |
| diagnostic (`got` lists of the grader's own `re.findall`) | `diag.py` | — | stdout quoted below |

Command shape: `python3 .ufo/waves/round-36/build/R36CritUnenforced/extra_cases_v2.py --lane .`

## Round 1 (v1): 10 of 14 predictions wrong — my witnesses, not the grader

`cases=14 observed_pass=0 observed_fail=14 mismatches=10`. Cause found with `diag.py` (which replaces
only the grader module's `re` *name* with a recording proxy around `re.findall`; the grader's log is
untouched):

```
E05-month-day-one-digit  got=[..., '2016-12-31', '2021-08-20', '2024-11-11', '1999-03-05']
E06-year-four-or-five    got=[..., '2016-12-31', '2023-13-05', '2022-00-15', '1995-06-32', '2001-09-00', '2021-08-20', ...]
```

Two construction defects of mine: (a) the `line()` helper put the date's capture group **without** the
reference's left boundary `(?<![A-Za-z0-9])`, so the N line `abc2021-08-20` contributed `2021-08-20`;
(b) three witnesses used a **range-free** date body (`\d{4}-\d{2}-\d{2}`), so the N lines
`2023-13-05`, `2022-00-15`, `1995-06-32`, `2001-09-00` (all on valid-IP lines) were matched. Both are
seat-side defects; they are *evidence that the grader is stricter than my witnesses*, i.e. it does
enforce month/day range and the date left boundary. v1's predictions are not edited.

## Round 2 (v2, corrected): 12 pass / 5 fail, 1 mismatch

Witness shape is the reference shape: `^(?=.*IP).*(?<!\w-class)(BODY)(?!\w-class)`; one feature varied
per case. Full run log: `extra-cases-v2-run.txt`.

| case | predicted | observed | feature varied | verdict |
|---|---|---|---|---|
| V01 feb30-apr31-range | pass | **pass** | Feb capped at 30, 30-day months raised to 31 | frozen-implied ≠ sharp |
| V02 literal-2000-02-30 | pass | **pass** | body + literal `2000-02-30` | frozen-implied ≠ sharp |
| V03 feb-only-30-31 | pass | **pass** | February accepts only 30/31 (every valid Feb day rejected) | frozen-implied |
| V04 leap-only-feb29 | pass | **pass** | real leap rule (the inference the instruction forbids) | frozen-implied |
| V05 month-day-one-digit | pass | **pass** | MM/DD width 1–2 digits | **new face** |
| V06 month-three-digit | pass | fail (`got` = `[..., '2023-13-05', '2022-00-15', ...]`) | width 2–3 digits **and** lost range check | my witness defect |
| V07 year-four-or-five | pass | **pass** | year `\d{4,5}` | frozen-implied |
| V08 ip-fourth-octet-00 | pass | **pass** | last octet `OCT\|00` | frozen-adjacent sharp |
| V09 ip-octet-zero-padded | pass | **pass** | octets `0{1,2}`-padded, range kept | **new face** |
| V10 dot-in-boundary-class | pass | **pass** | `(?![A-Za-z0-9.])` on both boundaries | **new face** |
| V11 whitespace-only-adjacency | pass | **pass** | `(?<!\S)(date)(?=\s\|\Z)` | **new face** |
| V12 slash-separator | pass | **pass** | `[-/]` between YYYY and MM | **new face** |
| V13 newline-as-separator | pass | **pass** | `[\s-]` inside the date body | **new face** |
| V14 inline-dotall-override | fail | **fail** | `(?s)` submitted over the grader's flags | enforced |
| V15 inline-multiline-scoped-off | fail | **fail** (`got=['2025-01-09']`) | `(?-m:^)` | enforced |
| V16 cross-line-bridge | fail | **fail** | `[\s\S]*?` between IP witness and date | enforced |
| V17 newline-required-after-match | fail | **fail** (`got=[..., '2024-11-01', ...]`) | `(?=\n)` after each match | enforced |

Round 3 (`extra_cases_v3.py`, `mismatches=0`) re-ran V06's face with the range check kept and added
the IPv4 separator face:

| case | predicted | observed | feature |
|---|---|---|---|
| V18 month-three-digit-range-kept | pass | **pass** | `\d{4}-(?:0[1-9]\|1[0-2]\|\d{3})-day` |
| V19 ip-dash-separators | pass | **pass** | `(?:OCT[.\-]){3}OCT` |

## Findings — 4 requirement faces unenforced beyond the frozen 24

Minimal witness = the shortest regex observed to be accepted while violating the named bullet (IP
abbreviation: `IP` = the probe's `ip()`, i.e. `(?<![A-Za-z0-9])(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.…)…(?![A-Za-z0-9])`).

**F1 — field widths of MM and DD are free (instruction: "format YYYY-MM-DD").**
Narrow: `^(?=.*IP).*(?<![A-Za-z0-9])(\d{4}-(?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12]\d|3[01]))(?![A-Za-z0-9])`
— accepts `2025-1-9`; observed **pass** (V05). Wide: `…(\d{4}-(?:0[1-9]|1[0-2]|\d{3})-DAY)…` — accepts
`2025-001-09`; observed **pass** (V18). The frozen 24 vary month/day *range* (`13`, `00`, `32`) but
never *width*, so this face is not covered.

**F2 — the date separator character set is free.** `…(\d{4}[-/]MONTH-DAY)…` accepts `2025/01-09`
(pass, V12); `…(\d{4}[\s-]MONTH[\s-]DAY)…` accepts a date whose separators are spaces or a newline
(pass, V13). Every frozen body hard-codes `-`; the frozen set never tests an alternate separator.

**F3 — IPv4 notation is only pinned where the log reaches.** `…(?:(?:0{1,2})?OCT\.){3}(?:0{1,2})?OCT…`
accepts `0255.1.2.3` (pass, V09); `…(?:OCT[.\-]){3}OCT…` accepts `1-2-3-4` as an "IPv4" (pass, V19);
`…(?:OCT\.){3}(?:OCT|00)…` accepts a `00` fourth octet while rejecting `01`–`09` (pass, V08).
`ip-leading-zeros-allowed` (frozen) already shows the padding class is open; V08/V09/V19 show the
*notation* (dots, zero padding, dash separators) cannot be pinned at all.

**F4 — the boundary clause is enforced only in the loosening direction.** `(?!…)` classes that are
*stricter* than "not alphanumeric" pass: `.` counted as alphanumeric (`(?![A-Za-z0-9.])`, pass, V10);
whitespace-only adjacency (`(?<!\S)date(?=\s|\Z)`, pass, V11). Consequence: a submission that would
miss `2023-06-01,` or `(2023-06-01)` on a real log scores 1.0 here. The frozen `date-boundary-letters-only`
shows the opposite (loosening) direction; neither pins the clause.

Frozen-implied confirmations (passes that add witnesses but no new face): V01–V04 (month-length,
February policy, leap rule) and V07 (year width).

### Enforced angles (H's stated guesses that do **not** hold)

- **"ignore the MULTILINE flag"** — no. Disabling it in-band is caught: `(?-m:^)…` yields
  `got=['2025-01-09']` (V15). The flag is load-bearing; a pattern may *use* it (the instruction says so),
  and subverting it fails.
- **"match dates across a line break"** — no. `(?s)` submitted over the call's flags (V14) and a
  `[\s\S]*?` bridge (V16) both fail on extra/cross-line dates.
- **"depend on a trailing newline in the file"** — the fixture *has* no trailing newline
  (`log_text = "\n".join(sample_logs)`, 25 lines, `ends_with_newline: False`), and requiring one is
  caught (V17). The residual fact is a fixture property (patterns requiring true EOF are unrepresentable),
  not an instruction requirement.
- **"Feb 30 on valid-IP lines"** — conditional, and the condition matters for wave 2: the two Feb-30 /
  Apr-31 lines both read `Login attempt 172.16.0.256 for user 2000-02-30` / `… 2000-04-31`, i.e. their
  IPv4 is invalid, so an explicit Feb-30 acceptance only passes **while an IP gate is present** (V02
  pass). Drop the IP gate and the same body fails (`no-ip-condition`, frozen). "Accept Feb 30" is
  therefore true only locally.

## Why these are limits, not defects (the tradeoff the canonical judge must weigh)

The graded log is 25 fixed lines, visible in the graded file, with no trailing newline. Reachability
census over that exact text (extracted with `ast` from the pinned grader, then searched):

```
log_lines: 25 chars: 1112 ends_with_newline: False
three_digit_month: []   slash_separator: []   five_digit_year: []
zero_padded_octet: []   octet_00: []          dash_separated_ip: []
date_then_dot: []       comma_after_date: []  feb29: []
feb30: ['-02-30']       apr31: ['-04-31']     digit_adjacent_date: ['1234-56-789']
```

Every face in F1–F4 is **unreachable in the fixture**: no line can expose it. The frozen 24 already pin
every violation the fixture can *express* (my v1 accident is the demonstration: range-free bodies and a
missing left boundary are caught). So no probe repair can close F1–F4 without changing the task's own
log, which is frozen at pin `2fd12b88`; and any extension that *did* inject new log lines would stop
being a probe of the pinned grader. This is the same shape as the round-35 convention: a surviving
mutant is reported as a limit.

A second, harder limit: `\d` is Unicode-aware in the grader's interpreter (`python 3.14.8`;
`re.findall(r"\d{4}-\d{2}-\d{2}", "２０２５-０１-０９")` → one match, `[0-9]` class → none). Every frozen case
and the reference body use `\d`, so "ASCII digits" is unenforced by construction and is *already*
inside the frozen table rather than beyond it.

## Impacted axes / claim impact

- **C2 predicate: untouched.** W1–W6, the 24-case table, `mismatches=0` and the receipt digest are
  unaffected — verified by not touching them (no lane file written).
- **Coverage (7) and novelty (7):** these are the axes this finding feeds. If the admitted entry
  asserts *"the grader enforces the instruction"* anywhere, it is false for F1–F4 and for the Unicode
  digit class; the entry should say the grader's fixed log pins every *reachable* violation and that
  four requirement faces are unreachable, naming one witness each. That is coverage evidence obtained
  without a new source.
- **Calibration:** 11 supplementary prediction mismatches (v1 10, v2 1, v3 0), all attributed to this
  seat's witness construction and all repaired by construction, none to the grader. Frozen probe's own
  `mismatches=0` is untouched and not contradicted.
- **Cross-claim hazard (C1's `--require-clean-tree`):** `.ufo/waves/round-36/build/` is **not** ignored
  (`git check-ignore -v .ufo/waves/round-36/build/R36CritUnenforced.md` → exit 1, no match), and this
  seat's artefacts are untracked in the live lane (6 files, ~36 KB). C1's predicate is measured "on a
  clean clone of the landing tip", so those are invisible there; but if any seat runs
  `plans/pkg_gate.py --require-clean-tree` against the live tree it will see every build directory of the
  wave, not a defect. Run the gate only against the clone, as the claim words it.

## Smallest safe correction

1. In `corpus/knowledge/tb2-regex-log-grader.md` (C2's entry), add one `## Limits` bullet set naming
   F1/F2/F3/F4 with the four minimal witnesses above, and one line stating the three enforced angles
   (`(?-m:^)`, `(?s)`/`[\s\S]` cross-line, trailing-newline requirement) so wave-2 mutation seats cannot
   re-discover them as defects. No count, digest or predicate sentence changes.
2. Do **not** add cases to `plans/regex_log_probe.py`; its 24 cases and digest are frozen instruments.
   If the L1 wants these preserved as instrument, a *separate* post-freeze harness (this directory) is
   the only admissible home, and it must be labelled outside the C2 predicate.
3. If the entry currently says an explicit `2000-02-30` acceptance passes *unconditionally*, correct it
   to "passes only behind an IP gate" (see the Enforced angles section) — that is the one wording that a
   wave-2 seat can falsify with a two-line regex.

## Files

```
.ufo/waves/round-36/build/R36CritUnenforced/extra_cases.py       (v1, predictions unedited)
.ufo/waves/round-36/build/R36CritUnenforced/extra_cases_v2.py    (v2, corrected helper)
.ufo/waves/round-36/build/R36CritUnenforced/extra_cases_v3.py    (v3, corrected V06 + V19)
.ufo/waves/round-36/build/R36CritUnenforced/diag.py              (got-list diagnostic)
.ufo/waves/round-36/build/R36CritUnenforced/extra-cases-run.txt
.ufo/waves/round-36/build/R36CritUnenforced/extra-cases-v2-run.txt
.ufo/waves/round-36/build/R36CritUnenforced/extra-cases-v3-run.txt
```

VERDICT: unenforced-4-new-mismatches-11
