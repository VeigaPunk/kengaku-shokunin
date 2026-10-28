# R49C2ScribeEntry — requirement-map repair drafts for the TB2 `polyglot-c-py` entry (R49-C2, coverage)

role: scribe · claim served: R49-C2 (coverage) · lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
date: 2026-10-28 · author seat: R49C2ScribeEntry · write scope: this file only

REV 9d2900af41e4d1fc6022eff99010436fde6dbd93

(The measured revision. The entry blob read here is `413d48282ee809a4dafc40d27db6065ec88798dd` and is identical
at `9d2900af…`, at the current lane tip `af88aab193e6034cb9b386472064e3c18fa90128`, and in the worktree — verified
with `git rev-parse <rev>:corpus/knowledge/tb2-polyglot-c-py-grader.md` and `git hash-object` on the worktree file.
This report is not a receipt: no counter and no probe was executed by this seat.)

VERDICT: DRAFTED, NOT MEASURED — the two `not exercised` rows are replaced by seven canonical four-cell rows citing
`both-print-c-silent` and `toolchain-c23-bool`, and the entry paragraphs naming the round-49 receipt are drafted.
The drafted rows pass the counter's `MAP_ROW`/citation/`derive` rules on a synthetic receipt (below). No R49-C2
admission and no pass assertion is made: the two label cells are receipt-derived and unobserved.

## Axes named

- **coverage (primary).** The requirement map is the artifact `V7` reads; two of its seven rows cannot be parsed by
  the counter at all, and two frozen tags carry no violating case, so the package's own coverage statement is
  unmeasurable. The repair drafted here makes the map's shape and its coverage claim checkable.
- **operability (secondary).** The repair is written as line-anchored old→new blocks plus one whole-section
  replacement, so the integration owner can apply it without re-deriving the counter's parsing rules.
- **quality (non-harm).** No production byte was edited; every statement about the grader is grounded in the pinned
  capture at `corpus/evidence/round46/tb2-polyglot-c-py/`.

## 1. Prerequisites checked before any work

Stage-1 freeze exists in the committed lane tree and predates this work:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
```

Lane tip at read time `af88aab193e6034cb9b386472064e3c18fa90128` (wave spec + dispatch, 09:18:20). Working tree
touched nothing tracked:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain
?? .ufo/waves/round-49/w1.ready.dispatched
?? .ufo/waves/round-49/w1/
```

No scored counter or probe was run (`plans/round46_c3_verify.py` and `plans/polyglot_c_py_probe.py` were read, never
executed). Scratch `TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2ScribeEntry` was created for the validators and the
two fetches and is removed before this seat yields.

## 2. The defect, measured (not inherited)

The counter's `V7` parses the map with `MAP_ROW` (`plans/round46_c3_verify.py:135`) and derives each label from the
receipt's `observed=` column (`:361-371`, `:392-410`). Two rows do not match that pattern:

```
$ python3 <inline section parser>   # MAP_ROW copied verbatim from plans/round46_c3_verify.py:135; loop over the '## Requirement map' section
  81 UNPARSED :: | Instruction line | Tag | Label | Receipt cases cited (violating) |
  82 UNPARSED :: |---|---|---|---|
  83 PARSE ('1', 'single-file', 'partly') :: | `instruction.md:1` | `single-file` | partly | `nop`, `extra-file`, `leftover-cmain`, `regrade-same-state` |
  84 PARSE ('3', 'python-run', 'enforced') :: | `instruction.md:3` | `python-run` | enforced | `c-only` |
  85 PARSE ('5', 'c-build', 'enforced') :: | `instruction.md:5` | `c-build` | enforced | `python-only`, `dir-in-place` |
  86 UNPARSED :: | instruction.md:7 | both-print | not exercised | no frozen case violates it |
  87 PARSE ('7', 'fib-kth', 'partly') :: | `instruction.md:7` | `fib-kth` | partly | `lookup-table`, `wrong-value`, `n-parsed-differently`, `empty-file` |
  88 PARSE ('7', 'stdout-only', 'enforced') :: | `instruction.md:7` | `stdout-only` | enforced | `value-plus-line` |
  89 UNPARSED :: | instruction.md:9 | toolchain | not exercised | no frozen case violates it |
```

Two independent defects sit in those two lines, and the routed round-46 lesson names only the second: (i) **shape** —
no backticked `instruction.md:N`, no backticked tag, and a label (`not exercised`) outside `{enforced, unenforced,
partly}`, so `V7` records `unparsed row …` and cannot even reach the "no receipt case violates it" branch; (ii)
**coverage** — no frozen case carries `violates=both-print` or `violates=toolchain` (`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, 18 `CASE` lines). Repairing only (ii) leaves `V7` red on (i); the draft below
repairs both in the same section.

## 3. Deliverable A — `## Requirement map` body (entry lines 75-106), replacement text

Apply verbatim; it replaces the intro paragraph (75-79), the table (81-89) and the bullet list (91-106). Seven rows,
four cells each, every cited id carried by that tag's `violates=` set.

```
Labels are **derived** from the receipt by the counter's `V7` rule: `enforced` iff every case whose `violates=` set
carries the tag is observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise. The
probe freezes seven tags on five instruction lines; the round-49 case amendment
(`corpus/evidence/round49/polyglot-c-py-dry-cases.txt`, `cases=20`) freezes at least one violating case for every
tag, so every row below is a canonical row with a label and its citing cases. A label is the value the `CASE …
observed=` lines of `corpus/evidence/round49/polyglot-c-py-probe.txt` derive: a cell filled before that receipt
exists, a tag with no cited violating case, or a cited case that does not carry `violates=<tag>` is a defect of
this map, not a measurement.

| Instruction line | Tag | Label | Receipt cases cited (violating) |
|---|---|---|---|
| `instruction.md:1` | `single-file` | partly | `nop`, `extra-file`, `leftover-cmain`, `regrade-same-state` |
| `instruction.md:3` | `python-run` | enforced | `c-only` |
| `instruction.md:5` | `c-build` | enforced | `python-only`, `dir-in-place` |
| `instruction.md:7` | `both-print` | enforced | `both-print-c-silent` |
| `instruction.md:7` | `fib-kth` | partly | `lookup-table`, `wrong-value`, `n-parsed-differently`, `empty-file` |
| `instruction.md:7` | `stdout-only` | enforced | `value-plus-line` |
| `instruction.md:9` | `toolchain` | unenforced | `toolchain-c23-bool` |

- **1 (`single-file`, partly).** The listing at `test_outputs.py:17-18` is exact and taken once, before the build:
  a missing directory (`nop`), a second file (`extra-file`) or the binary `instruction.md:5` itself tells the agent to
  build (`leftover-cmain`) fail. `regrade-same-state` is the pass that makes the label `partly`: it is the oracle's
  state after one grading, so it violates the single-file rule only on its *second* grading, and its first grading
  passes (`regrade=DIFF:F`).
- **3 (`python-run`, enforced) and 5 (`c-build`, enforced).** Every `subprocess.run` carries `check=True`; a file
  valid in one language only dies at the other leg (`c-only` at the interpreter, `python-only` at gcc), and a
  directory named `main.py.c` passes the listing but not gcc (`dir-in-place`).
- **7 (`fib-kth`, partly).** "The kth Fibonacci number" is graded at exactly N in {42, 10, 0} (`:27`):
  `lookup-table`, which hardcodes the three literals, passes; `wrong-value`, `n-parsed-differently` and
  `empty-file` fail.
- **7 (`stdout-only`, enforced).** Only `stdout.strip()` is compared (`:36`, `:43`), so a second output line fails
  (`value-plus-line`) while symmetric padding (`trailing-ws`) and stderr (`stderr-noise`) pass — those two cases
  violate no tag and are recorded as the requirement's tolerances, not violations.
- **7 (`both-print`, enforced).** `both-print-c-silent` is a polyglot whose `python3` leg prints the right value
  while the C leg builds, exits 0 and leaves stdout empty: `:44` compares both stripped stdouts with the same
  literal, so the C leg fails the assertion and `instruction.md:7`'s "both of these should print to stdout" is
  enforced. Its `violates=` tuple carries `both-print` alone, so it adds no citation to `fib-kth` or `stdout-only`.
- **9 (`toolchain`, unenforced).** `toolchain-c23-bool` writes a C side that uses C23 `bool` as a keyword without
  `<stdbool.h>`: the probe host's gcc builds it at its default C dialect (`gnu23`) and the grader passes it, while
  the documented gcc 13.2.0 default dialect (`gnu17`, gcc 13.2 manual, C dialect options: "This is the default for
  C code") rejects it with `unknown type name 'bool'`. The grader never reads a toolchain version — `:24` is its
  only gcc interaction — so the case passes and the label records that `instruction.md:9` is not enforced, not that
  a toolchain was verified.
```

Provenance of the two case ids and of `cases=20`: peer `R49C2ExecCases` reported them on 2026-10-28 (`both-print-c-silent` predicted=fail `violates=("both-print",)`; `toolchain-c23-bool` predicted=pass `violates=("toolchain",)`; amended dry table 20 cases, both stage-checked `match=yes`). **This seat did not measure either case** and did not see the amended dry table — `corpus/evidence/round49/` did not exist at read time. At stage 2 the L1 must re-read the ids and the count from the committed dry table; the draft's only invariant is that each cited id carries `violates=<tag>` and that its row's label equals the receipt derivation.

## 4. Deliverable B — entry paragraphs naming the round-49 receipt move

Each block is line-anchored against the frozen blob and splices cleanly (the fences delimit the replacement exactly).

### B1. `recheck:` (line 9)

OLD
```
recheck: 180d — from the lane root run `(cd corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)` (eight files), re-fetch the seven pinned URLs above and compare with the pin table in `plans/pkg-spec-r46.json`, then re-run `python3 plans/polyglot_c_py_probe.py --lane .`; any capture digest, probe output or receipt change supersedes this entry
```
NEW
```
recheck: 180d — from the lane root run `(cd corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)` (eight files), re-fetch the seven pinned URLs above and compare with the pin table in `plans/pkg-spec-r49.json`, then re-run `python3 plans/polyglot_c_py_probe.py --lane .` and diff its receipt against `corpus/evidence/round49/polyglot-c-py-probe.txt` (frozen case table `corpus/evidence/round49/polyglot-c-py-dry-cases.txt`); any capture digest, probe output or receipt change supersedes this entry
```

### B2. Summary receipt sentence (lines 36-40)

Lines 34-35 stay byte-identical so `Errata` 1's `Summary (':35')` pointer does not drift.

OLD
```
changes the graded directory in the middle of its own test. Every measured end state is recorded in the
receipt named by `plans/pkg-spec-r46.json` (`corpus/evidence/round46/polyglot-c-py-probe.txt`: `cases=18
observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`), first recorded after the stage-2
freeze `4fdeebaa` (QUALITY Q30); the sections below were drafted from the sources before that run and their
verdict cells filled from the receipt.
```
NEW
```
changes the graded directory in the middle of its own test. Every measured end state is now recorded in the
receipt named by `plans/pkg-spec-r49.json`, `corpus/evidence/round49/polyglot-c-py-probe.txt`, whose first-commit
is the round-49 stage-3 commit (a descendant of the stage-2 amendment commit) and whose frozen case table is
`corpus/evidence/round49/polyglot-c-py-dry-cases.txt` (`cases=20`); the round-46 receipt
`corpus/evidence/round46/polyglot-c-py-probe.txt` (`cases=18 observed_pass=7 observed_fail=11 mismatches=0`,
`regrade cases=18 differ=7`), recorded after the round-46 stage-2 freeze `4fdeebaa`, is the prior measurement this
one supersedes (QUALITY Q30/Q40: no full probe runs before the receipt names itself; only `--dry` and
`--stage-check` run pre-receipt). The current receipt's counts and verdicts are not restated here — the case and
mechanism tables below carry them, filled from that receipt.
```

### B3. `## Case table` intro (line 110)

OLD
```
The probe's 18 frozen cases, verdicts from the receipt. `Tests` is the single test function's letter
```
NEW
```
The probe's 20 frozen cases (the eighteen of round 46 plus `both-print-c-silent` and `toolchain-c23-bool`), in the
receipt's `CASE` order, verdicts from `corpus/evidence/round49/polyglot-c-py-probe.txt`. `Tests` is the single test function's letter
```

`V9` compares the table's `(case, tests, observed)` triples to the receipt's `CASE` lines as an **ordered list**
(`plans/round46_c3_verify.py:432-440`), so the two new rows must sit where the amended `CASES` list puts them.

### B4. Falsifier (b) (lines 211-213)

OLD
```
`plans/polyglot_c_py_probe.py --lane .` prints a verdict other than the receipt's for any of the 18 cases, or a
`regrade` column other than the receipt's; (c) `test_outputs.py` is shown to list the directory after the gcc call,
to compare anything but stripped stdout, or to test any N other than 42, 10 and 0.
```
NEW
```
`plans/polyglot_c_py_probe.py --lane .` prints a verdict other than `corpus/evidence/round49/polyglot-c-py-probe.txt`
for any case of the frozen table, a `violates=` token set other than the dry table's for any case, or a `regrade`
column other than the receipt's; (c) `test_outputs.py` is shown to list the directory after the gcc call,
to compare anything but stripped stdout, or to test any N other than 42, 10 and 0.
```

### B5. Limits bullet (lines 307-308)

OLD
```
- Two frozen requirement tags (`both-print`, `toolchain`) are exercised by no case (see Requirement map), so the
  map's coverage of `instruction.md:7,9` is partial and the counter's `V7` reports it.
```
NEW
```
- `instruction.md:9`'s toolchain statement is not checked by the grader: `toolchain-c23-bool` passes on the host
  toolchain and would not translate under the documented gcc 13.2.0 default dialect, so its row records
  non-enforcement, not a verified toolchain — the image's gcc/python versions stay unmeasured (no image was
  pulled). `both-print` is exercised on this host only, and `f(1)` is still named by `instruction.md:7` while no
  graded N and no frozen case exercises it (Errata 2).
```

### B6. Count in Negative space (line 205)

`**prevalence** — one task, eighteen cases, no tracker sweep by this seat;` → `**prevalence** — one task, twenty cases, no tracker sweep by this seat;`

### B7. Deliberately not changed

`verified-at: 2026-10-27` (line 8 — captures unchanged; re-dating is the L1's call), `## Located quotes`,
`## Findings`, `## Predictor`, `## Errata`, the seven `source:` lines, the dry table's seven `TAG` lines (claims
C2(a): tag names are never re-worded), and `## Negative space` other than B6. No drafted sentence asserts that C2
passes or that any label was observed.

## 5. Dependent rows the map alone cannot satisfy (same commit, outside this seat's item)

Drafted here as advisories so the integration owner does not ship a map that `V7` accepts while `V9`/`V10` fail:

1. `## Case table`: 20 rows in receipt order; new rows `| \`both-print-c-silent\` | F | fail | … |` and
   `| \`toolchain-c23-bool\` | P | pass | … |` (`Tests` = frozen predicted letters, `Observed` = receipt verdict).
2. `## Mechanism`: 20 rows in receipt order. Recommended `DECISIVE` lines (the L1 must confirm quote-on-line;
   `V10` substring-checks the normalized quote against the pinned capture):
   - `both-print-c-silent` → `test_outputs.py:44` — `assert python_out == expected and c_out == expected,`
   - `toolchain-c23-bool` → `test_outputs.py:24` — `["gcc", "/app/polyglot/main.py.c", "-o", "/app/polyglot/cmain"], check=True`
3. `DECISIVE` in `plans/round46_c3_verify.py` must gain both ids: `V10` fails outright when its keys differ from
   the frozen table (`:506-508`), so the amended probe table and that map move together.
4. Receipt `CASE` lines must carry `violates=both-print` / `violates=toolchain`: `V7` reads `violates=` from the
   **receipt** (`:361-366`), not from the dry table, so a correct dry table with a receipt that omits the token still
   leaves each row citing a non-violating case.

## 6. Validation of the drafted shape (synthetic, no lane execution)

`validate_rows.py` (scratch) reimplements `MAP_ROW`, the citation regex `` `([a-z0-9_-]+)` `` and `derive()`
verbatim from `plans/round46_c3_verify.py:135, 361-371, 392-410`, scopes itself to the `## Requirement map` section
as `v7` does, and checks cell count, frozen-line match, citation membership and label derivation (its per-row output
carries one trailing space, trimmed in the transcription below):

```
$ python3 validate_rows.py corpus/knowledge/tb2-polyglot-c-py-grader.md drafted-map.md
== current entry (unchanged rows 83-89)
  OK   single-file  row_label=partly     derived=partly cells=4 cited=['nop', 'extra-file', 'leftover-cmain', 'regrade-same-state']
  OK   python-run   row_label=enforced   derived=enforced cells=4 cited=['c-only']
  OK   c-build      row_label=enforced   derived=enforced cells=4 cited=['python-only', 'dir-in-place']
  UNPARSED -> V7 bad entry :: | instruction.md:7 | both-print | not exercised | no frozen case violates it |
  OK   fib-kth      row_label=partly     derived=partly cells=4 cited=['lookup-table', 'wrong-value', 'n-parsed-differently', 'empty-file']
  OK   stdout-only  row_label=enforced   derived=enforced cells=4 cited=['value-plus-line']
  UNPARSED -> V7 bad entry :: | instruction.md:9 | toolchain | not exercised | no frozen case violates it |
  RESULT current entry (unchanged rows 83-89): DEFECT
== drafted map
  OK   single-file  row_label=partly     derived=partly cells=4 cited=['nop', 'extra-file', 'leftover-cmain', 'regrade-same-state']
  OK   python-run   row_label=enforced   derived=enforced cells=4 cited=['c-only']
  OK   c-build      row_label=enforced   derived=enforced cells=4 cited=['python-only', 'dir-in-place']
  OK   both-print   row_label=enforced   derived=enforced cells=4 cited=['both-print-c-silent']
  OK   fib-kth      row_label=partly     derived=partly cells=4 cited=['lookup-table', 'wrong-value', 'n-parsed-differently', 'empty-file']
  OK   stdout-only  row_label=enforced   derived=enforced cells=4 cited=['value-plus-line']
  OK   toolchain    row_label=unenforced derived=unenforced cells=4 cited=['toolchain-c23-bool']
  RESULT drafted map: all rows canonical + labels derive
== drafted map under a receipt that contradicts the frozen prediction
  OK   single-file  row_label=partly     derived=partly cells=4 cited=['nop', 'extra-file', 'leftover-cmain', 'regrade-same-state']
  OK   python-run   row_label=enforced   derived=enforced cells=4 cited=['c-only']
  OK   c-build      row_label=enforced   derived=enforced cells=4 cited=['python-only', 'dir-in-place']
  BAD  both-print   row_label=enforced   derived=unenforced cells=4 cited=['both-print-c-silent'] label enforced != derived unenforced
  OK   fib-kth      row_label=partly     derived=partly cells=4 cited=['lookup-table', 'wrong-value', 'n-parsed-differently', 'empty-file']
  OK   stdout-only  row_label=enforced   derived=enforced cells=4 cited=['value-plus-line']
  BAD  toolchain    row_label=unenforced derived=enforced cells=4 cited=['toolchain-c23-bool'] label unenforced != derived enforced
  RESULT drafted map under a receipt that contradicts the frozen prediction: DEFECT
```

The third case is the point: when the receipt's `observed=` values contradict the frozen predictions, the drafted
labels are **wrong**, not merely stale — which is why the two cells are marked receipt-derived and why the intro
paragraph makes a pre-receipt label a defect of the map.

## 7. The `toolchain` label's factual basis (measured here, and its limit)

`toolchain-c23-bool` passes only if the host gcc accepts C23 `bool` without `<stdbool.h>`. Measured in scratch:

```
$ gcc --version | head -1
gcc (GCC) 16.2.1 20260810
$ python3 --version
Python 3.14.8
$ printf 'int main(void){bool b=1;return b?0:1;}\n' > b23.c
$ gcc b23.c -o b23_default; echo exit=$?
exit=0
$ gcc -std=gnu17 b23.c -o b23_gnu17; echo exit=$?
b23.c: In function ‘main’:
b23.c:1:16: error: unknown type name ‘bool’
    1 | int main(void){bool b=1;return b?0:1;}
      |                ^~~~
b23.c:1:1: note: ‘bool’ is defined in header ‘<stdbool.h>’; this is probably fixable by adding ‘#include <stdbool.h>’
exit=1
```

So the version gate the case rests on is real on this host: default dialect accepts the construct, `gnu17` rejects
it. That the documented **gcc 13.2.0** default is `gnu17` is a source fact, re-opened this round:

| source | URL | accessed | located quote (≤25 words) |
|---|---|---|---|
| GCC 13.2 manual, C dialect options | `https://gcc.gnu.org/onlinedocs/gcc-13.2.0/gcc/C-Dialect-Options.html` | 2026-10-28 | under `gnu17`/`gnu18`: "GNU dialect of ISO C17. This is the default for C code." (12 words) |
| S168 `instruction.md` (the toolchain line the tag cites) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/instruction.md` | 2026-10-28 | `:9` "I'm using python3 3.12.3 and gcc 13.2.0." (7 words) |

The S168 fetch is byte-equal to the committed capture — `sha256 a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` for both the downloaded file and
`corpus/evidence/round46/tb2-polyglot-c-py/instruction.md`, which is the digest in that directory's `SHA256SUMS`.

The limit this imposes on the draft: the case violates `instruction.md:9` **because the documented default dialect is
`gnu17`**, not because the host prints a version string. A case that merely relied on "the host is newer" would not
violate the tag and its citation would be unsupportable — the map repair inherits that dependency, so the toolchain
row is only as good as that documented gate. `-std=gnu17` on gcc 16 is an approximation of gcc 13.2.0's default, not
gcc 13.2.0 itself (the image is never pulled; entry Limits already say so).

## 8. Findings

1. **The `not exercised` rows are a shape defect as well as a coverage defect.** `MAP_ROW` rejects them before any
   case table is consulted (`unparsed row …`), so the round-48 route item 3 ("a frozen tag with no violating case")
   is only half the repair; the canonical four-cell shape is the other half. Drafted both.
2. **The derived `toolchain` label is `unenforced`, and that is the honest value.** The violating case passes because
   the grader never reads a version; writing `enforced` (or omitting the row) would overstate coverage. This is a
   statement about the grader's reach, not an admission of the package.
3. **Tag-minimality is load-bearing.** Both new cases carry exactly one tag. A case that also carried `fib-kth` or
   `stdout-only` would silently change those rows' derived labels and citations; the validator above shows the
   single-tag draft derives the same labels for the five untouched rows as the current entry does.
4. **`V7` reads `violates=` from the receipt, not the dry table.** A frozen dry table plus a receipt that drops the
   token still fails the citation check — recorded in §5.4 so it is checked at stage 3, not discovered then.
5. **`cases=20` and the two ids are peer-reported, not measured here.** `corpus/evidence/round49/` did not exist at
   read time; the stage-2 dry table is the only authority. Flagged in §3.
6. **Internal cross-reference preserved.** `Errata` 1 cites `Summary (':35')`; the draft edits only lines 36-40, so
   that pointer keeps meaning what it meant.
7. **No pass assertion and no production edit.** Every sentence added to the entry is either a shape statement, a
   derivation rule, or a citation of a capture line; the two label cells are explicitly receipt-derived.

## 9. Limits

- No counter or probe was executed; the validation in §6 is a reimplementation of the counter's parsing rules on a
  synthetic receipt, not the counter itself. A `V7`/`V9`/`V10` result remains unmeasured.
- The two case ids, their predicted letters and `cases=20` come from peer `R49C2ExecCases` and were not observed by
  this seat; the amended dry table was not on disk.
- The gcc gate was measured on gcc 16.2.1 with `-std=gnu17` as a stand-in for gcc 13.2.0's default; no image was
  pulled and gcc 13.2.0 itself was not run.
- This report drafts one entry file's text; it says nothing about C1, about the v4 counter, about the mutation
  battery, or about whether any label will survive the stage-3 receipt.

## 10. Tooling

No tool was installed, upgraded or invoked outside the listed commands; no pacman transaction was attempted. Scratch
`/fast/scratch/hyaku/kengaku-r49/R49C2ScribeEntry` held `s168_instruction.md`, `gcc13-dialect.html`, `b23.c`,
`b23_default`, `b23_gnu17`, `drafted-map.md`, `entry-paragraphs.md`, `validate_rows.py`, `validator.out`; it is
removed before this seat yields, and every artifact worth keeping is transcribed above.
