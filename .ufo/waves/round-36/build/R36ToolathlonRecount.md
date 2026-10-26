# R36ToolathlonRecount — independent recount of the S130 Toolathlon package + D4 erratum line proof

Seat: executor leaf, round 36 wave 1. No lane file written; everything below is scratch under
`.ufo/waves/round-36/build/R36ToolathlonRecount/` plus a `mktemp` fixture. Lane tip at measurement:
`f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd`.

## Axes

1. Is the package's `of 38` denominator re-derivable from its own table? (recount arithmetic)
2. Do the other summing/dividing claims in the package hold?
3. Does the staged S130 row carry the inflated denominator, and what is its locator?
4. Does the drafted `## Gate` erratum line satisfy the frozen `r35_d4` predicate, and can that
   predicate fail (negative controls)?

## 1. Capture identity

```
$ cmp corpus/evidence/round36/toolathlon-package.md \
      /home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/toolathlon-grader-behaviour-probe-2026-10-23.md
IDENTICAL
$ sha256sum <both paths>
00132ab0cd660f356bfe94cf2175a9a2df76a7504cd9d9ec4af66634ef62a6f0  corpus/evidence/round36/toolathlon-package.md
00132ab0cd660f356bfe94cf2175a9a2df76a7504cd9d9ec4af66634ef62a6f0  …/toolathlon-grader-behaviour-probe-2026-10-23.md
$ git -C . show master:corpus/evidence/round36/toolathlon-package.md | sha256sum
00132ab0cd660f356bfe94cf2175a9a2df76a7504cd9d9ec4af66634ef62a6f0  -
```

The committed bytes equal the source knowledge bytes and equal the frozen digest in
`plans/round-36-claims.md` (Frozen digests block).

## 2. Recount (own script, no counter import)

`python3 .ufo/waves/round-36/build/R36ToolathlonRecount/recount.py corpus/evidence/round36/toolathlon-package.md`
(structural markdown parse only — no fixture names, no marker strings). Exit 1.

```
outcome_rows:
   13  of 38  <- isolated and callable
    4  of 38  <- … discriminate (identical accepted, perturbation rejected)
    9  of 38  <- … callable but **not** discriminating under the generic shapes
   23  of 38  <- isolated but not callable with any of the seven shapes
    1  of 38  <- exec failed in isolation

leaf_sum          = 13 + 23 + 1 = 37
stated denominator= 38
shortfall         = 1
discriminate + callable_but_not = 4 + 9 = 13  vs parent 13 -> OK
all rows state 'of 38'          -> True
leaf sum equals stated denominator    -> False
denominator free of contradiction?    -> False

named discriminating functions        = 4 (claim 'four' -> OK)
  k8s-redis-helm-upgrade.values_equal_strict
  live-transactions.validate_log_payload_structure
  nvidia-stock-analysis._compare_names
  student-interview.iso_times_equal
argument shapes listed                = 7 (claim 'seven' -> OK)
graders parsed (claim)                = 108  [not derivable from this file alone]
candidates (claim)                    = 38
'nine callable-but-uninformative'     = OK
steps enumerated in Method            = 2 (claim 'Two')

RECOUNT verdict: INCONSISTENT (13 + 23 + 1 = 37 against a stated denominator of 38)
```

Claim locations in the committed copy: header `| Outcome | Count | of 38 |` at `:30`; rows
`:32-36`; "seven generic argument pairs" at `:23`; "The four that discriminate" at `:38`;
"All 108 graders" at `:17`; "**38** candidates" at `:19`; "Two offline steps" at `:15`.

Per-claim verdicts:

| claim | arithmetic | verdict |
|---|---|---|
| leaf rows vs header | 13 + 23 + 1 = 37 ≠ 38 | **FAIL — one too many in the denominator** (or one row missing; see §2a) |
| callable split | 4 + 9 = 13 | OK |
| discriminating functions named | 4 backticked names | OK |
| argument shapes | string, list, set, dict, dict-of-list, tuple, int = 7 | OK |
| "nine callable-but-uninformative" | sub-row = 9 | OK |
| "23 could not be called … and 1 failed to exec" | 23 + 1 = 24 = 38 − 14, and 13 + 24 = 37 | OK internally, inherits the same 38 |
| Method steps | 2 enumerated | OK |
| "All 108 graders" and "38 candidates" | no second operand in the package (108 → 38 is not a sum or a division) | **not checkable from the committed copy**; no Toolathlon clone exists under `/home/vgpnk/Projects/shokuknow` (`find … -maxdepth 3 -iname "*Toolathlon*"` empty), and the fetch is outside this seat |

Sharper: every `of 38` row states the same denominator, and `23` at `:35` is labelled "of the seven
shapes" (a shape count of 7, consistent), so no *sub-row* is inconsistent — only the population
header is.

### 2a. Corroboration from the source lane document (read-only, outside the lane)

The committed copy is the trimmed knowledge version (68 lines) and carries no per-candidate record.
The source lane document the row points at,
`/home/vgpnk/Projects/shokuknow/lanes/kengaku/round6/toolathlon-grader-behaviour-probe.md`
(sha256 `659ab87def2f29927bfa68f5808c4dd156c633242e1b9883e7574868233560cb`, read-only), *does*
carry one, and its `## Per-candidate record` table enumerates exactly 37 rows:

```
$ awk '/^## Per-candidate record/{f=1;next} f&&/^\| /{print}' … | grep -v '^| task' | grep -v '^|---' | wc -l
37
$ … | awk -F'|' '{gsub(/ /,"",$4); print $4}' | sort | uniq -c
      1 exec-failed
     23 no-callable-shape
     13 ok
```

So the enumerated population is 37; the `38` in the header is the stale number, not a dropped row.
Limit: that table is **not** in the lane's committed bytes, and the locator `lanes/kengaku/round6/…`
is exactly the one the round-35 spot-check ruled unresolvable from this lane — so the erratum line
below rests only on the arithmetic the committed copy supports, and this paragraph is corroboration,
not the lane's evidence.

## 3. Staged S130 row

`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:60` (single table row, 13 columns;
the only `^| S130 |` line — `grep -c` = 1). It is staged: `grep -c S130 corpus/SOURCES.md` → `0` in
the lane. Locator quote (5 words, ≤25):

> Locator: lanes/kengaku/round6/toolathlon-grader-behaviour-probe.md

The row states `"isolated and callable 13 of 38"` and `"discriminate 4 of 38"` (column 7) — both
inherit the inflated denominator, and the row omits the 23 / 1 rows entirely, so a reader of the row
alone cannot see the shortfall. This is exactly the round-35 routed item 4
(`corpus/lessons/round-35-verifier-spotcheck.md:89`, "add the 38 vs 37 denominator reason
(13+23+1)"), whose refusal row at `:69` already recorded the finding
("13 + 23 + 1 = 37 rows — the lesson's Gate row omits this second reason"). My recount independently
reproduces it from the committed copy; the erratum line is the Gate-row fix for that omission.

## 4. Drafted erratum line (paste verbatim, one physical line)

```
Erratum (round 36): S130's Outcome table's three leaf rows are 13 + 23 + 1 = 37 against the stated denominator 38 in the committed copy corpus/evidence/round36/toolathlon-package.md, so the table contradicts its own header and the row's "13 of 38" summary cannot corroborate the count; recorded as an erratum, not repaired.
```

51 words, one line. Integration constraints (both are load-bearing for `r35_d4`):

- it MUST sit between a `## Gate` heading and the next `^## ` heading in `corpus/lessons/round-36.md`;
- it MUST be a bare paragraph line starting with `Erratum (round 36):` — **not** a bullet
  (`- Erratum …` drops `erratum_lines` to 0), and exactly one such line may exist in `## Gate`.

## 5. Proof against the frozen predicate

`python3 .ufo/waves/round-36/build/R36ToolathlonRecount/prove_d4.py` imports
`plans/round36_c1_verify.py` unmodified, builds a `mktemp` lane tree holding the committed package
copy at `corpus/evidence/round36/toolathlon-package.md` plus a fixture `corpus/lessons/round-36.md`
carrying the line under `## Gate`, and calls `r35_d4(lane)`. Exit 0.

```
DRAFTED ERRATUM (51 words, 1 physical line):
… (line above) …

PASS fixture_with_erratum         r35_d4=True  erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS lesson_without_gate_section  r35_d4=False  erratum_lines=0 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS gate_without_erratum         r35_d4=False  erratum_lines=0 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS two_erratum_lines            r35_d4=False  erratum_lines=2 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS denominator_equals_recount   r35_d4=False  erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS no_S130                      r35_d4=False  erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS wrong_arithmetic             r35_d4=False  erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS bullet_prefixed_line         r35_d4=False  erratum_lines=0 recount=13 + 23 + 1 = 37 stated_denominator=38
PASS package_absent               r35_d4=False  toolathlon package capture absent

real lane now: r35_d4=False  round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
```

Eight negative controls flip the predicate (absent Gate, absent line, duplicate line, denominator
equal to the recount, missing `S130`, wrong arithmetic, bullet prefix, absent package), so the green
on the fixture is not a vacuous pass. `corpus/lessons/round-36.md` and `plans/pkg_gate.py` are both
absent at the tip (`ls` → No such file), so `r35_d4` is red until the L1 lands the lesson; the
counter's own message already carries the recount, so the failure is informative by construction.

## Files written (scratch only)

- `.ufo/waves/round-36/build/R36ToolathlonRecount/recount.py` — structural recount, exit 1 on the
  inconsistency.
- `.ufo/waves/round-36/build/R36ToolathlonRecount/prove_d4.py` — `r35_d4` proof + 8 negative controls.
- `.ufo/waves/round-36/build/R36ToolathlonRecount.md` — this report.

No lane file, no git index, no jj state touched. No tool installed.

## Risks / blockers

- The `108` graders / `38` candidates discovery counts cannot be re-derived offline from the pinned
  commit by this seat (no local clone; fetching the pinned repo is outside the seat). My erratum is
  scoped to the table arithmetic, which is what `r35_d4` freezes.
- The drafted line names the committed copy path in prose. A wave-2 attacker could try to make the
  gate accept a lesson whose erratum cites a *different* path; `r35_d4` (frozen) does not check the
  path. Reported as a limit, not repaired — the line's required substrings are the frozen rule.
- Stale-denominator risk if S130 is ever admitted: the row's `13 of 38` / `4 of 38` cells would need
  the same correction; the erratum line already says the summary cannot corroborate the count.
- Clean-tree coupling: my three scratch files are untracked, and `r35_d4`'s sibling predicate
  `r35_d1 --require-clean-tree` reads `git ls-files --others --exclude-standard`. Before the frozen
  C1 predicate is measured at the landing tip the L1 must commit or remove
  `.ufo/waves/round-36/build/`, exactly as for every other wave-1 seat's scratch.

VERDICT: recount-37-vs-38-erratum-line-verified
