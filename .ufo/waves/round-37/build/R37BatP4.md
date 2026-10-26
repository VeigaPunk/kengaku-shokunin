# R37BatP4 — battery37 module `p4` (P4 / M09–M12)

Seat: executor, kengaku round 37 wave 1. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(tip `3ea9a1d9…` baseline, frozen claims `plans/round-37-claims.md`). Nothing frozen was edited: the gate at
`sha256=ea638822…` (counter prints `GATE plans/pkg_gate.py sha256=frozen`), the counter, the spec and the
mutant list are read-only inputs here.

## Deliverable

| File | Role |
|---|---|
| `.ufo/waves/round-37/build/R37BatP4/battery/p4.py` | battery37 module, 4 single-defect fixtures, stdlib only, no imports |
| `.ufo/waves/round-37/build/R37BatP4/dev-run.txt` | receipt of the proof run (pasted below) |
| `.ufo/waves/round-37/build/R37BatP4/drop-table.txt` | receipt of the load-bearing table |
| `.ufo/waves/round-37/build/R37BatP4/adjacent.txt` | receipt of the adjacent-mutant probe |

`sha256(p4.py) = 3e506c65098a84d154a37e411f65b32c1bed9439b10e0ea2d8dcff8fa8e7fccf` (4156 bytes).
The L1 integrates it as `plans/battery37/p4.py`; I did not write into the lane.

## Fixtures and the branch each one reaches

Every builder calls `ctx.genuine_package(d)`, rewrites only the data rows of the genuine entry's
`## Located quotes` table through `ctx.r36.rewrite_quotes`, stages with `ctx.git_add(d)` and returns
`["package", "--root", str(d), "--require-clean-tree"]`. The helper `_first_row` locates rows with
`ctx.r36.QUOTE_ROW` and edits exactly one `re` span (`m.span(1|2|3)`), so no fixture depends on a literal
claim text beyond the genuine first row.

| fid | mutant | edit | declared defects | why that set |
|---|---|---|---|---|
| `p4-no-quote-row` | M09 (`return False, "no parsed quote"`) | data rows replaced by `[]`; header + separator kept | `P3,P4` | P4 is the target. P3 fires unavoidably: with zero parsed quotes `len(texts) >= min_quotes(8)` can never hold, and there is no other route to `p.quotes == []` while the section still parses (removing the section is the M04 branch, which this fixture does not exercise). |
| `p4-capture-unreadable` | M10 (`bad.append(f"{q.capture}: unreadable capture")`) | first row's capture name → `no-such-capture-37.py` | `P4,P5` | P4 target. P5 fires through a *different* clause and branch: `quote capture {name} is not pinned in the manifest` (`pkg_gate.py:174-176`). M10 erases only the P4 set member, so the kill is unambiguous. |
| `p4-line-outside` | M11 (`bad.append(... line range outside the capture")`) | first row's start line → `9999` (capture has 73 lines) | `P4` | capture pinned, row parsable, word range untouched → P3/P5 ok. |
| `p4-one-char-off` | M12 (`bad.append(... quote not verbatim there")`) | last alphanumeric char of the first quote's text replaced (`t`→`z` in `…gblock.txt")` → `…gblock.txz")`) | `P4` | same length, same word count (3), same location; only the verbatim branch fires. |

## Proof run (dev mode, read-only on the lane)

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r37/R37BatP4
$ python3 plans/round37_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP4/battery \
    --only M09,M10,M11,M12 --work "$S"
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE p4-no-quote-row expect=reject declared=P3,P4 observed_rc=1 observed_defects=P3,P4 ok
FIXTURE p4-capture-unreadable expect=reject declared=P4,P5 observed_rc=1 observed_defects=P4,P5 ok
FIXTURE p4-line-outside expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4-one-char-off expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
BATTERY fixtures=18 wrong=0 renamed_disagree=0
MUTANT M09 P4 killed by=p4-no-quote-row -- no parsed quote
MUTANT M10 P4 killed by=p4-capture-unreadable -- quote cites an unreadable capture
MUTANT M11 P4 killed by=p4-line-outside -- quote line range outside the capture
MUTANT M12 P4 killed by=p4-one-char-off -- quote not verbatim on its cited line
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
real 0m5.5s
```

All four FIXTURE lines of the module end `ok`, `wrong=0`, `renamed_disagree=0` (every fixture copied under a
hashed directory name `x…q` gives the same result, so the gate keys on no fixture name), `null_detected=0`
(a second unmodified gate copy reproduced every one of the 18 results), `invalid=0`, and each assigned mutant
is `killed by=` its own fixture. Exit code 0 in dev mode.

## Load-bearing check: delete one fixture at a time

Each variant is a scratch copy of `p4.py` with exactly one `FIXTURES` entry removed (asserted `len-1`), run
with only the matching mutant:

```
=== drop p4-no-quote-row -> expect M09 SURVIVED
FIXTURE p4-capture-unreadable … observed_defects=P4,P5 ok
FIXTURE p4-line-outside … observed_defects=P4 ok
FIXTURE p4-one-char-off … observed_defects=P4 ok
BATTERY fixtures=17 wrong=0 renamed_disagree=0
MUTANT M09 P4 SURVIVED -- no parsed quote
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
=== drop p4-capture-unreadable -> expect M10 SURVIVED
BATTERY fixtures=17 wrong=0 renamed_disagree=0
MUTANT M10 P4 SURVIVED -- quote cites an unreadable capture
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
=== drop p4-line-outside -> expect M11 SURVIVED
BATTERY fixtures=17 wrong=0 renamed_disagree=0
MUTANT M11 P4 SURVIVED -- quote line range outside the capture
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
=== drop p4-one-char-off -> expect M12 SURVIVED
BATTERY fixtures=17 wrong=0 renamed_disagree=0
MUTANT M12 P4 SURVIVED -- quote not verbatim on its cited line
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```

(The dropped variant's three survivors each still print `ok` with their declared sets — full text in
`drop-table.txt`.) Diagonal: each fixture is necessary and sufficient for its mutant; no fixture is carried
by a sibling.

| dropped fixture | mutant | before | after |
|---|---|---|---|
| `p4-no-quote-row` | M09 | killed | SURVIVED |
| `p4-capture-unreadable` | M10 | killed | SURVIVED |
| `p4-line-outside` | M11 | killed | SURVIVED |
| `p4-one-char-off` | M12 | killed | SURVIVED |

## Adjacent mutants (not assigned, recorded for integration)

`--only M04,M13,M16,M18,M19` over this module only:

```
MUTANT M04 P3 SURVIVED -- no '## Located quotes' section        (branch not exercised)
MUTANT M13 P5 SURVIVED -- capture manifest absent               (branch not exercised)
MUTANT M16 P5 SURVIVED -- row capture not pinned in the manifest (branch not exercised)
MUTANT M18 P5 killed by=p4-capture-unreadable -- quoted capture not pinned in the manifest
MUTANT M19 P5 SURVIVED -- capture file not covered by the manifest
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0
```

`p4-capture-unreadable` also kills M18, which is expected and harmless: its P5 defect *is* the
`quote capture … is not pinned` branch that M18 silences, and the fixture was built for the P4 branch. No
other adjacent P3/P5 mutant is touched, so the module does not blur neighbouring classes.

## Limits / risks

- A demonstrational kill is observational: it shows the branch is reached and its result is visible, not that
  the check is the right check (limit already named at freeze, `plans/round-37-claims.md` C1).
- `p4-no-quote-row` cannot be reduced to a P4-only fixture (P3 must fire when `min_quotes>0` and no quote
  parses); declared as P3+P4 with the reason inline in the module docstring. M04 keeps its own fixture lane
  (a missing section), so the two mutants stay separable in the set of observable results.
- The module assumes the genuine round-35 entry keeps at least one parsable quote row with an alphanumeric
  character; `_first_row`/`_one_char_off` raise a `RuntimeError` (→ counter SETUP/fixture failure) rather
  than silently degrading if that ever stops holding.

## Tooling and hygiene

- No installs, no upgrades, no pacman; stdlib only (`re` not even needed — `ctx.r36.QUOTE_ROW` is borrowed).
- Scratch `/fast/scratch/hyaku/kengaku-r37/R37BatP4` used for `TMPDIR`/`--work` and the four variants;
  receipts copied into the report dir and the scratch tree deleted (`rm -rf --`, verified gone).
- Lane `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`, `SHONEN.md`,
  the jj/Git state and the Git index were not written. No `git add/commit/stash/checkout/reset/push/pull`,
  no jj command.

VERDICT: battery-p4-killed-4/4-wrong-0
