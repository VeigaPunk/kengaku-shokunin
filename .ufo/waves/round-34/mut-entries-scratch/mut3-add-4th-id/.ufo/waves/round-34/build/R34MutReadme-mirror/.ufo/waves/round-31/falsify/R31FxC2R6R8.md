# R31FxC2R6R8 — attack on the R6 count regex and the R8 row-cell guard

Round 31, wave 2, FALSIFY. Seat `L1Kengaku31.R31FxC2R6R8` (leaf: no dispatch, no background
jobs). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `dbb07364`.
No tool installs or upgrades (nothing needed; pacman paused host-wide).
Scratch: `/tmp/r31fx-R31FxC2R6R8/` (420 KB, well under 60 MB). No production edits —
the only file written under the lane is this report.

Target: `plans/round31_defects.py` — `check_r6` (`:191-232`) and `check_r8` (`:253-262`),
against the six assigned fixtures under `/tmp`. Every result below is from commands I ran this
seat; the fixture battery is `/tmp/r31fx-R31FxC2R6R8/drive.py` (reproducible verbatim).

## 0. Ground truth (real lane)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/round31_defects.py --lane .
checks=10 defects=0
EXIT=0
```

The landed C2 counter is green. `check_r6` on a copy of the real entry returns `''` (pass),
re-deriving `unregistered = 2`:

- staged file `…/benchmark-card-field-schema-2026-10-23.md:2-4` names exactly 3 URLs
  (S122 AI Alliance template, S123 CTC `disclosure.yaml`, S124 GEM 2026 PDF);
- registry keys (`SOURCES.md`, 91 rows) contain the S124 document key only:
  `https://aclanthology.org/2026.gem-main.50.pdf` → `…/2026.gem-main.50` (S001 at
  `SOURCES.md:23`); S122/S123 are unregistered → **2**.

The entry carries both target shapes:
`corpus/knowledge/contamination-transparency-card.md:40-41` — the counted form
("two of its three source rows are not in this lane's registry") and `:163` — the
§Extends form ("two of its three source rows are staged and not in this lane's registry").
R8's repair is visible in the diff `git diff 0883e72 dbb07364 -- corpus/knowledge/contamination-transparency-card.md`:
the `@@ -135,8 +137,8 @@` hunk deletes "the CC0 card"; both `grep -c "CC0"` on the entry
and on `SOURCES.md` are `0` today, so `check_r8` is vacuous on the landed bytes.
`git diff` `@@ -37,11 +37,12 @@` shows the R6 repair (bare "its three source rows are
not …" → "two of its three source rows are not …"; "adopting those three rows" →
"those two rows").

## 1. R6 battery (`check_r6`, `round31_defects.py:219-231`)

The regex is `(?:([a-z]+) of )?its three source rows are not in this lane's registry`,
searched over the flattened entry; every fixture uses the real registry copy (so
`unregistered = 2`), varying only the entry text.

| fixture | entry text (fake) | check_r6 returns | caught? |
|---|---|---|---|
| 1 wrong number word | `one of its three source rows are not in this lane's registry.` | `'the entry states 1 unregistered staged sources, the registry gives 2'` | **yes** |
| 2 bare, mid-sentence | `the card notes its three source rows are not in this lane's registry.` | `'the entry asserts all three staged source rows are unregistered; 2 are'` | **yes** |
| 3 both forms | `one of its three source rows are not in this lane's registry, and its three source rows are not in this lane's registry.` | `'the entry states 1 unregistered staged sources, the registry gives 2'` | **yes** |
| 4 §Extends form | `two of its three source rows are staged and not in this lane's registry.` | `'the entry states no staged-source count; the re-derived count is 2'` | **false positive** |

Trace (same battery, `re.finditer`): fixture 1 captures group `('one')`; fixture 2
matches bare with group `None`; fixture 3 yields both matches; fixture 4 yields **zero**
matches — `finditer` = `[]`.

Findings:

- **F1 (R6) — fixtures 1–3 are caught.** The wrong count word, a bare assertion embedded
  mid-sentence, and the coexistence of both forms each make the check red with a correct
  diagnostic. The `[…]${ of ` optional-group parsing does handle the nested-substring
  ambiguity it was written for (a counted form is not double-counted as bare: one match).
- **F2 (R6) — fixture 4 is a false positive: the honest §Extends form fails the check.**
  `"two of its three source rows are staged and not in this lane's registry"` is the true
  statement (matches the re-derived `2`) and is *exactly* the real entry's own sentence at
  `contamination-transparency-card.md:163`. The regex requires the byte sequence
  `it three source rows are not in this lane's registry`; `"are staged and not in"` breaks it,
  so the check reports a defect against a correct sentence. The check is a single-template
  lexer, not a count verifier: any honest paraphrase ("are staged and not in", "are missing
  from", "are absent from", "the three source rows it names are not in" — the latter is the
  minimal repair wording R31DefR6's own F-e proposed) trips it. C2's green therefore depends
  on the entry keeping the byte-exact landed sentence, not on the claim being true.
- The check does not flag the bare form when `unregistered == 3` (then the bare assertion is
  correct); with the current two-unregistered registry any bare occurrence is correctly red.

## 2. R8 battery (`check_r8`, `round31_defects.py:253-262`)

`check_r8` returns clean if the entry does not contain `"CC0"`; otherwise it scans `registry_rows(lane)`
(`:119-129`, rows matched by `ROW_RE` `:63`, exactly 11 `|`-cells) for any cell containing
`"CC0"`. Both fixtures use the same entry (`"a decision rule the CC0 card cannot supply on its own."`).

| fixture | registry | check_r8 returns | caught? |
|---|---|---|---|
| 5 row scope cell mentions CC0, licence differs | one 11-cell row (S900) whose **scope** cell reads `CC0-licensed metadata only; the release itself is CC BY 4.0` (rows parsed: `['S900']`, `any-cell-CC0: True`) | `''` — **greens** | **no** |
| 6 CC0 in non-row line only | `# Registry\n\n<!-- CC0 -->\n\nProse: all cards are released under CC0, but this is not a row.\n` (rows parsed: `[]`) | `'the entry names a CC0 licence no registry row records'` | **yes** |

Findings:

- **F3 (R8) — fixture 6 is caught.** A CC0 mention outside the row table (comment or prose)
  no longer greens the guard; the original C2-critic comment-greening vector is closed.
- **F4 (R8) — fixture 5 is a false green.** The guard is an unanchored `"CC0"` substring
  scan over *any* cell of *any* row. A row whose scope cell merely mentions CC0 — while the
  row's own licence grant is `CC BY 4.0` — satisfies the guard, even though no row records a
  CC0 licence for the design the entry names. The R8 defect ("no registry row records a CC0
  licence for that design") is therefore not verifiable by this check: it proves "some row
  cell contains the string CC0", not "the named design's licence is grounded".
- The check is also vacuous whenever the entry omits the exact string `"CC0"` (the current
  state), or if a future edit writes a different ungrounded licence word (e.g. "MIT",
  "Apache-2.0") — the residual `check_r8` is lexical was already conceded in
  `.ufo/waves/round-31/build/R31DefR8.md:142-146`; fixture 5 adds a concrete satisfiable
  false-green input whenever the guard *is* armed.

## 3. Commands (verbatim, output that carries each finding)

```
python3 plans/round31_defects.py --lane .          # checks=10 defects=0, EXIT=0
python3 /tmp/r31fx-R31FxC2R6R8/drive.py            # full battery output, incl. grounds:
                                                   #   urls=3; registered: S122 False, S123 False, S124 True; unregistered=2
                                                   #   f1..f4/f5/f6 results as in the tables above
grep -c "CC0" corpus/knowledge/contamination-transparency-card.md corpus/SOURCES.md   # 0 / 0
git diff 0883e72 dbb07364 -- corpus/knowledge/contamination-transparency-card.md     # R6 hunk @@ -37,11 +37,12 @@; R8 hunk @@ -135,8 +137,8 @@
```

## VERDICT

R6's check survived the wrong-number-word, bare-embedded and both-forms fixtures (1–3, all
red) but fell on fixture 4: the honest §Extends form — the real entry's own sentence at
`:163` — is reported as "no staged-source count", a false positive; the regex verifies one
byte-exact sentence, not the count claim. R8's check survived fixture 6 (non-row CC0 mention
stays red) but fell on fixture 5: a row whose scope cell merely mentions CC0 greens the guard,
so the check verifies "some row cell contains CC0", not "the named design's licence is
grounded"; it is vacuous on the landed bytes (no CC0 anywhere) and on any other licence word.
