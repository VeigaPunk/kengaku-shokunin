# GateMutate71 — R71-C2 gate: semantic mutation matrix, shipped-`--mutants` comparison, and the `DEFECTS n=0` load-bearing verdict

## Item attacked

R71-C2's kill rule: *"the gate [is] killed 4/4 under single-check deletion"*, and its predicate
`DEFECTS n=0` as the closure proof for R70-D1/R70-D2. This seat builds mutants **beyond** the
shipped `--mutants` by rewriting the gate source (no flags), runs them against the red fixtures
the gate's own selftest builds, and scores whether each neutered assertion still detects its
defect. No predicate, case table, vector, digest, kill rule or target was edited; two
gate-vs-docstring gaps and two false-red formatting cases are reported, not fixed.

## Pinned bytes read and tested

Lane `master` = `d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0`. The working tree also carries two
uncommitted sibling edits (`corpus/README.md` gained the round-71 C1 knowledge row; the nginx
entry gained the `E-D2a` amendment). Everything below is pinned to these exact bytes:

| file | sha256 |
|---|---|
| `plans/round71_c2_routed_defects.py` | `d472312ac8ea2c25413e34e275af883879a0c9c354261b35625b4679096d95ff` |
| `LOG.md` | `8979933b7420e7501da57a033199f5d119fb3ad610bbb9b10e56da3b603afaf0` |
| `corpus/README.md` | `97e754718c761ad404da992640206212a836042cf50092d81b3deeaad49387c7` |
| `corpus/lessons/round-70.md` | `5ce57b957015a4d13e54370d048d1cbdca75578c4a1210d8953abbbdc89677c3` |
| `corpus/knowledge/tb2-nginx-request-logging-offline.md` | `2d4e92afae74e64b1cd7fdcf2a430a27700ad61b84f01924e710f335623d4dc8` |

**Drift note.** A sibling appended the round-71 index row and supporting block while this report
was being written: `corpus/README.md` moved `97e7547…` → `cf2eec3…`. The two round-70 E1c sites
(`README.md:566` index row, `README.md:798/801` support block) are byte-identical between the two
revisions, the new `round-71` lines are skipped by E1c's round-70 context test, and the gate at
`cf2eec3…` still prints `DEFECTS n=0 / PREDICATE R71-C2 pass`. The battery was run on `97e7547…`;
nothing else moved.

Python 3.14.8, stdlib only. No tools installed; no mutating `git`/`jj`; no lane write other than
this file. Mutants and fixtures were built in `/fast/scratch/hyaku/kengaku-r71/GateMutate71`
and removed after the run (seat bounds); every mutant is a one-line rewrite specified in §2, and
every fixture is either built by the gate's own `--selftest` or derived by the one-token edit
named in §2/§4, so the whole battery is reproducible from this report. Lane hashes for `LOG.md`,
the lesson, the entry and the gate were re-read after the battery and are identical to the table
above; `README.md` moved by a sibling per the drift note.

## What was run (commands, rc)

| # | command | rc | output |
|---|---|---|---|
| 1 | `python3 plans/round71_c2_routed_defects.py --lane .` at L | 0 | `E1a ok` `E1b ok` `E1c ok` `E2a ok` `DEFECTS n=0` `PREDICATE R71-C2 pass` |
| 2 | `… --selftest --work S/st-base` | 0 | `DEFECTS-RED n=14 codes=E1a,E1b,E1c,E2a want=E1a,E1b,E1c,E2a` / `SELFTEST defects-in-fake=4 want=4 all-fail=True append-only-arm=True ok=True` |
| 3 | `… --mutants --work S/mu-base` | 0 | 4× `MUTANT <code> defect_absent=True killed=True rc=1` / `MUTANTS total=4 killed=4 survived=0` |
| 4 | six semantic mutants (below), each on its red fixture | see matrix | see matrix |
| 5 | each semantic mutant's own `--mutants` | 0 (all six) | `MUTANTS total=4 killed=4 survived=0` |
| 6 | each semantic mutant's own `--selftest` | 0/1 | see matrix |
| 7 | base-tip reproduction: gate over `git show 1cb49cac:<rel>` bytes | 1 | `DEFECTS n=6`, **byte-identical** to `.ufo/waves/round-71/c2-red-before.txt` |
| 8 | tip-shaped injections T1–T11 on a copy of the pinned live bytes | see §4 | see §4 |

Command 7 is a provenance check worth recording: the pre-fix bytes (`1cb49cac`) plus the
committed gate reproduce the committed `c2-red-before.txt` exactly (`n=6`, same seven lines).
The red-before is therefore re-derivable, not a stored tally.

Label note: the selftest's `defects-in-fake=4` is `len(codes_red)` — the number of distinct
check codes that fired (`plans/round71_c2_routed_defects.py:312`, `:322-324`), not four defect
lines; on the red+stale pair there are 14 defect lines. The printed string is the frozen one,
but the label counts codes.

## 1. The shipped `--mutants` is a wiring test; its 4/4 is invariant under semantic weakening

The four shipped mutants are built at `plans/round71_c2_routed_defects.py:331-347`:

```python
red = build_fixture(work / "mutant-red", green=False, rows=7)
src = Path(__file__).resolve().read_text()
...
mutant_src = src.replace(f'    ("{code}", ', f'    # ({code} deleted) ("{code}"_x, ', 1)
mutant_src = re.sub(rf'\s+\("{code}", (check_\w+)\),', "", mutant_src, count=1)
...
absent = f"DEFECT {code} " not in out.stdout
killed += 1 if absent else 0
```

The regex is dead code: after the first `replace`, the line no longer matches
`\s+\("E1c", (check_\w+)\),`. The mutation is exactly the comment-out of one `CHECKS` row.
Verified by diff (`diff -u gate mutant-E1c.py`):

```diff
-    ("E1c", check_e1_readme),
+    # (E1c deleted) ("E1c"_x, check_e1_readme),
```

That is a **wiring** test: it removes the call, not an assertion inside the check. All six
semantic mutants below still print `MUTANTS total=4 killed=4 survived=0`, including the two that
fully neuter an arm (`M3b`, `M4b`). So the 4/4 is literally reproducible but carries no
arm-level information.

## 2. Semantic mutants (source rewrites, no flags) and the matrix

Six mutants from the four briefed shapes; M3b/M4b are the "fully accept the defect" variants of
M3a/M4a and expose the double coverage.

| id | rewrite (gate lines) | neutered property |
|---|---|---|
| M1 | `:153` `if n != WANT_ROWS:` → `if n not in (WANT_ROWS, 6):` | E1c accepts a six-row count |
| M2 | `:183-184` deleted | E2a accepts an erratum without `instruction.md:6-11,15-18` |
| M3a | `:176-177` deleted | E2a stops requiring the original sentence to stay (`flat` arm) |
| M3b | `:176-177` + `:187-188` deleted | E2a fully accepts a rewritten superseded sentence |
| M4a | `:97` `if len(rows) != WANT_ROWS:` → `if len(rows) not in (WANT_ROWS, 7):` | E1a accepts a seven-row count |
| M4b | M4a + `:99` `for key in ROW_KEYS:` → `for key in ROW_KEYS[:-1]:` | E1a fully accepts seven rows |

Every replacement was asserted to occur exactly once in the source. Two columns of kill are
reported because the brief's wording ("stops detecting the defect it neutered") is
sub-assertion-level, while the shipped runner's actual test (`:343`) is check-level:

- **sub-assertion**: the exact defect line the mutant targets disappears;
- **check-level** (= `run_mutants` convention): `DEFECT <code> ` disappears from stdout entirely.

| id | fixture | baseline target line(s) | mutant emits | sub-assertion | check-level | mutant `--selftest` |
|---|---|---|---|---|---|---|
| M1 | `fake-red` (selftest) | `DEFECT E1c index-row:count=6`, `support-block:count=6` | only the two `…:missing=…` lines (`DEFECTS n=4`) | lost | **survived** | `ok=True` (n=10) |
| M1 | `red-count-only` (derived) | both count lines (`DEFECTS n=2`) | none (`DEFECTS n=0 PREDICATE pass`) | lost | killed | — |
| M2 | `fake-red` (selftest) | `DEFECT E2a no-errata-section` (early return `:178-179`) | unchanged (`n=6`) | — | **survived** | `ok=True` (n=14) |
| M2 | `red-no-range` (derived) | `DEFECT E2a no-corrected-range` | none (`n=0 pass`) | lost | killed | — |
| M3a | `fake-rewritten` (selftest) | `superseded-sentence-missing` + `erratum-does-not-quote-superseded-sentence` | only the errata line (`n=1`) | lost (one line) | **survived** | `ok=True` (n=14) |
| M3b | `fake-rewritten` (selftest) | both E2a lines | none (`n=0 pass`) | lost | killed | **`ok=False`** (`append-only-arm=False`, rc 1) |
| M4a | `fake-stale-lesson` (selftest) | `row-count=7 want=8` + `missing-row-class:unre-derived landing prose` | only the key line (`n=7`) | lost (one line) | **survived** | `ok=True` (n=13) |
| M4b | `fake-stale-lesson` (selftest) | both E1a lines | none (`n=0 pass`) | lost | killed | **`ok=False`** (`defects-in-fake=3 want=4`, rc 1) |

**Result: 6/6 sub-assertion kills (by construction), 2/6 check-level kills.** The four
check-level survivors and the exact code each should have produced:

- **M1** should have produced `DEFECT E1c index-row:count=6` and
  `DEFECT E1c support-block:count=6`. On `fake-red` they are masked because the same README line
  is also six-names (`FIXTURE_README_ROW_RED`, `:251-253`; `FIXTURE_README_SUPPORT_RED`,
  `:257-258`): the `missing=` arm (`:155-157`) keeps E1c red. On the isolating fixture (green
  README with both `eight Mistakes rows` → `six Mistakes rows`, all eight names kept) the baseline
  gate prints exactly those two lines and M1 prints `DEFECTS n=0 / PREDICATE R71-C2 pass`.
- **M2** should have produced `DEFECT E2a no-corrected-range`. **No shipped fixture ever reaches
  that assertion on red bytes**: `fake-red` has no `## Errata` at all, so `:178-179` returns
  before `:183`; `fake-rewritten` has the range. The isolating fixture `red-no-range` (derived
  from `fake-green` by deleting `,15-18` from the erratum, the same one-token derivation the
  selftest uses at `:316-318`) is detected by the baseline and passes under M2.
- **M3a** should have produced `DEFECT E2a superseded-sentence-missing`. It is masked by the
  second copy of the same assertion, `:187-188` (`erratum-does-not-quote-superseded-sentence`),
  because the selftest's rewrite (`.replace(...)` without count, `:318`) rewrites both copies.
  With the flat arm gone but the errata arm present, E2a stays red (`n=1`).
- **M4a** should have produced `DEFECT E1a row-count=7 want=8`. It is masked by the key arm
  (`:99-101`): `build_fixture(rows=7)` drops the eighth row and therefore the eighth key from the
  same table (`:288-291`), so `missing-row-class:unre-derived landing prose` keeps E1a red
  (`n=7`).

**The pair that matters:** M1 and M2 pass the **entire frozen predicate** on defective bytes —
`--lane` prints `DEFECTS n=0 / PREDICATE pass`, `--selftest` prints `ok=True`, and `--mutants`
prints 4/4 (verified: §4 `T1_M1`, `T3_M2`). M3b/M4b also produce a false `n=0` but are caught by
the selftest line (`append-only-arm=False`; `defects-in-fake=3 want=4`), so the composite
predicate still fails for them. The only full-predicate false passes are the two whose assertion
the shipped fixture set cannot isolate.

## 3. Why the survivors survive: fixture coupling and one genuine redundancy

- M1: **fixture coupling** — count and class-names are wrong on the same fixture line; the
  shipped fixture never observes the count arm alone.
- M2: **fixture gap** — the range assertion is unreachable on every shipped red fixture
  (`no-errata-section` short-circuits `:178-179`); the selftest never exercises
  `no-corrected-range` at all.
- M3a: **redundancy** — two assertions test the same property (whole-text presence and
  errata-region presence); deleting one leaves the other.
- M4a: **coupling + redundancy** — `rows=7` couples count and key, and the key arm alone keeps
  the check red.

## 4. Tip-shaped injections: is `DEFECTS n=0` at the tip load-bearing?

Each probe is a one-shape edit on a fresh copy of the pinned live bytes; the unmutated gate is
run first, then a weakened gate where a mutant is named. `rc` and the decisive lines:

| probe | injected shape | unmutated gate | verdict |
|---|---|---|---|
| T1 | both README sites say `six Mistakes rows`, all eight names kept | `DEFECT E1c index-row:count=6` + `support-block:count=6`, `n=2` | caught |
| T1_M1 | same bytes, gate M1 | `DEFECTS n=0 / PREDICATE pass`, rc 0 | **false pass** |
| T2 | index + support say `eight`, name only six | `missing=dead check clause,unre-derived landing prose` ×2, `n=2` | caught |
| T3 | all three `instruction.md:6-11,15-18` occurrences removed | `DEFECT E2a no-corrected-range`, `n=1` | caught |
| T3_M2 | same bytes, gate M2 | `n=0 / pass`, rc 0 | **false pass** |
| T3b | range removed from the **E-D2 bullet only** (E-D3/E-D2a keep it) | `E2a ok`, `n=0 / pass`, rc 0 | **residual** |
| T4 | the two erratum quotes rewritten, original intact | `DEFECT E2a erratum-does-not-quote-superseded-sentence`, `n=1` | caught |
| T4c | **original sentence** rewritten, both erratum quotes intact | `E2a ok`, `n=0 / pass`, rc 0 | **residual (append-only shape)** |
| T4d | original + E-D2 quote rewritten, E-D2a quote intact | `E2a ok`, `n=0 / pass`, rc 0 | **residual (append-only shape)** |
| T5 | one `## Mistakes` data row removed (seven rows) | `row-count=7 want=8` + `missing-row-class:unre-derived landing prose`, `n=2` | caught |
| T5_M4a | seven rows, gate M4a | only the key line, `n=1`, rc 1 | caught (redundancy holds) |
| T5_M4b | seven rows, gate M4b | `n=0 / pass`, rc 0 | **false pass** (selftest catches M4b) |
| T6b | LOG count sentence `**eight**` → `**six**`, same entry later says "say eight" | `E1b ok`, `n=0 / pass`, rc 0 | **residual (check-vs-docstring)** |
| T7a | extra `- Round-70 note: six Mistakes rows were carried.` | `E1c ok`, `n=0 / pass`, rc 0 | **residual (check-vs-docstring)** |
| T7b | same line with lowercase `round-70` | `DEFECT E1c line806:count=6`, `n=1` | caught |
| T8 | one table row class renamed, key text kept in appended prose | `E1a ok`, `n=0 / pass`, rc 0 | residual (within frozen E1a wording) |
| T9 | correct count written as `8 Mistakes rows` | `DEFECT E1c index-row:count=8` + `support-block:count=8`, `n=2` | **false red** |
| T10 | correct count written as `` `eight` Mistakes rows `` | `DEFECT E1c index-row:count=None` + `support-block:count=None`, `n=2` | **false red** |
| T11 | the appended `## Errata` heading removed, E-D2 bullets kept | `E2a ok`, `n=0 / pass`, rc 0 | residual (shape-level) |

Details that matter:

- **T3b / T4c / T4d are direct consequences of the checks' scoping.** `check_e2_entry` splits on
  the **first** `## Errata` (`:180`), so its region is everything from line 53's
  `## Errata (round 70)` to EOF. The range and `supersede` arms are therefore satisfied by the
  round-70 `E-D3` block; at the base tip those arms were already green (command 7 shows only
  `no-E-D2` and `erratum-does-not-quote…`). T4c is the sharpest: **the D2 fix itself duplicates
  the superseded phrase**, so rewriting the original sentence is invisible to
  `SUPERSEDED_SENTENCE not in flat` (`:176`). The selftest's append-only arm cannot see this
  because its fixture has exactly one copy (`FIXTURE_ENTRY_BASE` + `FIXTURE_ENTRY_ERRATA`) and
  `.replace` (`:318`) rewrites all copies. On the live entry the phrase has three flattened
  copies (`:14-15`, `:93-94`, `:98`); T4d still passes with one left.
- **T6b** is a check-vs-docstring gap: E1b's docstring (`:17-18`) says the entry "stating eight",
  but the implementation greps a −2/+24-line window (`lines[i-2:i+24]`) for `\beight\b`
  (`:112-117`). A correction entry
  whose count sentence says six while a later sentence says "now say eight and name all eight
  classes" is accepted.
- **T7a** is the same class for E1c: the docstring (`:19-20`) says "every `corpus/README.md`
  mention of round-70 Mistakes rows says eight … no unsuperseded wrong count remains", but the
  tail scan (`:158-166`) requires the line itself to contain lowercase `round-70`/`round 70`.
  Capitalised `Round-70` (as in the README's own heading style) is skipped; lowercase is caught
  (T7b). A second bullet inside the round-70 support block without the context token would also
  be skipped.
- **T8** is inside the frozen E1a wording ("the eight class keys are present"): presence is
  whole-text (`:99-101`), so a mislabelled row passes if the key survives in prose. Report as
  scope, not a violation.
- **T9/T10 are detector bugs, not rule issues.** `parse_count` (`:85-91`) returns the **string**
  `"8"` for a digit (the map holds word keys only), so `n != WANT_ROWS` is `"8" != 8` → defect
  `count=8`; a backticked/wrapped token yields `None` → defect `count=None`. Both are correct
  renderings of "eight". This makes `n=0` brittle to formatting, not lax.

## 5. Verdict

**Does `DEFECTS n=0` at the tip hold, and is it load-bearing?**

1. **The frozen predicate is met at the pinned tip.** `--lane .` → `E1a ok`, `E1b ok`, `E1c ok`,
   `E2a ok`, `DEFECTS n=0`, `PREDICATE R71-C2 pass`, rc 0; `--selftest` → `defects-in-fake=4
   want=4 all-fail=True` with `append-only-arm=True`; `--mutants` → `total=4 killed=4
   survived=0`. Command 7 reproduces `c2-red-before.txt` byte-for-byte at the base tip (`n=6`).
   Nothing here refutes R71-C2 as written.
2. **`n=0` is load-bearing for the two routed defects in the shapes they actually took.** Each
   historical shape injected into the live bytes turns the gate red with the expected code:
   six-count-with-eight-names (T1), eight-says/six-named (T2), no corrected range anywhere (T3),
   rewritten errata quote (T4), seven rows (T5).
3. **It is not a universal certificate.** Five measured content shapes pass the unmutated gate:
   T3b (range only in the older errata), T4c/T4d (original sentence rewritten; the fix's own
   quote hides it), T6b (entry's count sentence says six, later sentence says eight), T7a
   (capitalised `Round-70` mention says six), T11 (appended heading removed, bullets kept). T8 is
   a scope note within E1a's wording. Of these, **T6b and T7a contradict the gate's own
   docstrings** ("stating eight"; "every README mention … says eight"); the rest are scope/shape
   limits of `E2a`'s region-wide scan and `E1a`'s whole-text key test. Two correct renderings
   (digit `8`, backticked `` `eight` ``) are **false reds**. These are report-only: the frozen
   rules were not edited.
4. **The `4/4` must not be cited as arm-level evidence.** It is invariant under all six semantic
   mutants (`MUTANTS total=4 killed=4 survived=0` in every case); it only proves the four
   `CHECKS` rows are wired. At check level my matrix is **2/6 killed, 4/6 survived**, and the two
   survivors that pass the entire frozen predicate on defective bytes (M1, M2) are exactly the
   arms whose shipped fixtures cannot isolate them (coupling; unreachable red arm).
5. **The append-only property named in the claim's fix shape ("the original sentence stays as
   written") is not enforced on the post-fix entry.** E2a checks phrase presence anywhere in the
   file; the erratum's own verbatim quote satisfies it. The selftest's append-only arm proves the
   property only for a single-copy fixture. If a future round wants that property to be
   load-bearing, it needs a positional check (the phrase above the first `## Errata`) or a
   per-block check — that is a rule change for the L1 to freeze, not for a seat.

## 6. Non-mutation evidence

- No `git`/`jj` mutating command was run; the only reads were `rev-parse`, `show`, `diff`,
  `status`, `log`, `cat-file`-style `git show`.
- Lane file hashes before and after the battery are identical to §"Pinned bytes" for
  `LOG.md 8979933…`, lesson `5ce57b9…`, entry `2d4e92af…` and gate `d472312a…`. `README.md` was
  `97e7547…` during the battery and `cf2eec3…` at the final read — the sibling's round-71 landing,
  not a write by this seat; the round-70 E1c sites are byte-identical and the gate is `n=0` at
  both revisions.
- The only lane write is this report. The scratch tree `/fast/scratch/hyaku/kengaku-r71/GateMutate71/`
  (`mutants/`, `st-base/`, `live-*`, `tip-suite.log`, `matrix.json`, `tip-suite.json`,
  `manifest.json`) was removed after the run; every output quoted above came from that tree.
