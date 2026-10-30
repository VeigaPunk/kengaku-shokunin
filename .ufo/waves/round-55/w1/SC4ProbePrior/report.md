# SC4ProbePrior — seat report

**Role:** scout (read-only). **Task:** extract the established probe pattern from
`plans/password_recovery_probe.py`, `plans/polyglot_c_py_probe.py`, `plans/build_pmars_probe.py`
so E5's R55-C3 instrument implementation can be checked against it.

**Deliverable:** `.ufo/waves/round-55/w1/SC4ProbePrior/pattern.md` — the five items with
file:line quotes (bwrap flag pattern; frozen case table + predictions; observed-vs-predicted and
mismatch printing; CLI conventions; exit-code contract), plus a deviation list for the current
draft `plans/round55_c3_chess_probe.py` and the commands I ran with their exit codes.
Scoped findings also at `.ufo/waves/round-55/w1/SC4ProbePrior.md` (the Report-trailer path).

**What I ran** (all read-only against the lane; writes only to my scratch and my wave dir):

| command | result | exit |
|---|---|---|
| `python3 plans/password_recovery_probe.py --lane . --dry` \| `cmp - corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` | byte-equal | 0 |
| `python3 plans/polyglot_c_py_probe.py --lane . --dry` \| `cmp - corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` | byte-equal | 0 |
| `python3 plans/round55_c3_chess_probe.py --lane . --work <scr>/chess --selftest` | `SELFTEST cases=2 failures=0` | 0 |
| `python3 plans/round55_c3_chess_probe.py --lane . --work <scr>/chess` | `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass` | 0 |
| copy of the draft with one prediction flipped | `mismatches=1`, `PREDICATE R55-C3 fail` | 1 |
| copy of the draft with one case forced to SETUP | `cases=12 observed_pass=4 observed_fail=7 mismatches=0` + `SETUP cases=…` | 2 |
| draft with `--work` pre-populated (`precious/data.txt`) | `--work` directory deleted by the tool | 0 |
| draft `--receipt <f>` vs stdout | byte-equal | 0 |
| `python3 plans/build_pmars_probe.py --lane . --work <absent> --smoke` | `FileNotFoundError` (pmars does not create `--work`) | 1 |
| `python3 plans/password_recovery_probe.py --lane . --work <pre-populated>` | caller's `--work` contents preserved | 0 |
| bwrap (draft flags) with `/app/move.txt` a directory | `IsADirectoryError`, no `AssertionError` → draft scores SETUP, pattern scores `F error=IsADirectoryError` | 1 |
| `git cat-file -e 80afa613:plans/round55_c3_chess_probe.py` | absent at the freeze commit | 128 |

**Files written:** `.ufo/waves/round-55/w1/SC4ProbePrior/pattern.md`,
`.ufo/waves/round-55/w1/SC4ProbePrior/report.md`, `.ufo/waves/round-55/w1/SC4ProbePrior.md`.
No lane file edited; no sibling's file touched; no mutating git/jj command.

**Defects found (in the draft instrument, reported not fixed — E5/L1 own it):** D1 non-AssertionError
grader failure scored SETUP instead of a case verdict; D2 summary line can print `mismatches=0`
while a case went unevaluated (`p+f != n`, the shape `round46_c3_verify.py:331-335` detects);
D3 `--work` deleted wholesale; D4 receipt `CASE` lines do not parse under the lane's own receipt
parser (`round46_c3_verify.py:307`) and the exit-code contract differs from every other probe row
in `SKILL.md`; D5 the case table lacks the instruction-requirement mapping the claims require;
D6 bwrap flags differ in form (functional, measured).

**Not run (honest):** the R55-C2 laundering fixtures, `plans/round52_c2_registry.py`, any
network/benchmark call. `plans/round55_c2_entryargv.py` did not exist when I read the tree early in
this seat; a sibling seat created it untracked at 12:38 during the wave, so it is out of my read
set. I re-read only its CLI surface (`plans/round55_c2_entryargv.py:410-416`: `--lane` default `.`,
`--source`, `--work`, `--jobs`, `--timeout`, `--dry`, `--selftest` — matching the lane's counter
CLI convention of pattern.md §4) and did not run it.

**Dead ends:** searching for a pre-existing "probe pattern" note in the lane found only
`plans/round-36-claims.md:8-10` (the pattern described as "established") and
`.ufo/waves/round-37/build/R37ConnSibling.md:127-129` (the "pinned-grader-probe" capability
uniqueness claim) — neither enumerates the mechanics, so the pattern had to be re-derived from
the three sources. `plans/round55_c2_entryargv.py` was absent from the tree when I read it early in
this seat, so the C2 instrument's CLI could not be cross-read at that point.

**Installs:** none. **Scratch:** `/fast/scratch/hyaku/kengaku-r55/SC4ProbePrior/` deleted.
