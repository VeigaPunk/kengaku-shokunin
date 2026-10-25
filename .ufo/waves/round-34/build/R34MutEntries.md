# R34MutEntries — C1 counter vs entry mutants (end-to-end)

Seat: mutation-tester (leaf). Probe: mutate the C1 knowledge-entry in a scratch mirror of the
lane's post-integration tree; run the C1 counter draft against each mutant; report which
mutants the counter misses.

## Mirror construction

Scratch root (disposable copy; lane untouched):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/mut-entries-scratch/`
(rsync of the lane minus `.git`, `.jj`, `__pycache__`; self-path excluded).

Integration applied to the mirror (from the wave drafts):
- Entry: `.ufo/waves/round-34/build/R34EntryTB2/entry.md` →
  `corpus/knowledge/terminal-bench-task-grader.md` (byte-exact copy).
- Rows: `.ufo/waves/round-34/build/R34RowsTB2/append-rows.md` → S105/S106/S107 appended to
  `corpus/SOURCES.md` as registry-table rows after the S104 row (lines 120–122).
- README patch: `.ufo/waves/round-34/build/R34ReadmePatch/patch.md` blocks (a)(b)(c)(d) applied
  to `corpus/README.md` (index rows before `lessons/round-1.md`; discharge bullet after the
  round-33 grader-semantics bullet; frontier line 279 replaced with the two new lines).
- Counter: `plans/round34_c1_verify.py` = draft copy.

## Baseline (pristine integrated mirror)

Command:
```
cd .../mut-entries-scratch && python3 plans/round34_c1_verify.py --lane .
```
Output:
```
DEFECT V3: source rows mined/opened/used-by
DEFECT V4: exactly one README index row
DEFECT V6: frontier clauses retained and TB clause narrowed
DEFECT V7: freeze control receipt values
checks=8 defects=4
```
exit=1. Baseline is RED: V1/V2/V5/V8 green, V3/V4/V6/V7 red (see "Baseline findings" below).
Entry sha256 (pristine) = `304312ad1c4a996dbd61387c22bd0373b468e920519eff8a20a3a8e04f50b298`.

## Mutants (one behavior-bearing entry change each, fresh copy of integrated mirror)

| # | Mutation | Entry sha256 after | Detector output (diff vs baseline) | Verdict |
|---|---|---|---|---|
| M1 | Drop one `source:` line (S107) | `a3a24604eafe05c1fc5b5572f78d2fe23d11fda8c8c664eaf4a6f84d8d5c40a1` | `DEFECT V1` ADDED (V3/V4/V6/V7 unchanged); `checks=8 defects=5`, exit 1 | **Killed** (V1 catches count≠3) |
| M2 | Change `verified-at: 2026-10-25` → `2026-10-26` | `1680875bb962b2c6e80f9b6255b516dbd82a00cf310c1cbb2243e37a0ec3e914` | `DEFECT V2` ADDED (V3/V4/V6/V7 unchanged); `checks=8 defects=5`, exit 1 | **Killed** (V2 literal) |
| M3 | Add a fourth `source:` id (S092) | `f62fe79d20f13a8b703fbefe6aa87c166c58e497e9074aae4b222506c405efef` | `DEFECT V1` ADDED (V3/V4/V6/V7 unchanged); `checks=8 defects=5`, exit 1 | **Killed** (V1 set/len) |
| M4 | Delete the `## Negative space` section (lines 30–33) | `36ac220071b5f5e26eb1070b5c01a1dd6b0f800d6557cad2781e3fd5e37421fb` | byte-identical to baseline: V3/V4/V6/V7; `checks=8 defects=4`, exit 1 | **SURVIVED (missed)** |
| M5 | Change a number inside a quote: “assert 15 <= gc <= 35” → “assert 15 <= gc <= 36” | `e08c789e91cde8436ff8a6a55d0d545d6a3a34dac64550e6808435a61cf5dbf7` | byte-identical to baseline: V3/V4/V6/V7; `checks=8 defects=4`, exit 1 | **SURVIVED (missed)** |

All five mutants changed the entry hash (before/after recorded above); each run was on a full
copy of the integrated mirror, so the only difference from baseline is the single entry edit.

## Missed mutants (coverage findings)

- **M4 — negative-space deletion**: no V-check reads the entry's `## Negative space` section.
  V1/V2 cover only `source:` lines and the `verified-at:` literal; V3 reads SOURCES rows; V4–V8
  read README/control/captures. Deleting the section leaves every check green.
- **M5 — number inside quote**: no V-check validates quote contents against the captured bytes
  (the Appendix table is not read at all). Changing `35`→`36` within a quote is invisible.

Missed 2/5.

## Baseline findings (counter draft vs integration drafts disagree — calibration note)

The counter as drafted does NOT print `checks=8 defects=0` on the post-integration mirror; it
reports 4 defects. The red checks and their causes:

- **V3**: expects tokens `status=mined`, `opened=2026-10-25`, and the entry name on each S105–S107
  row line. `corpus/SOURCES.md` registry rows (and the drafted append rows) are table rows with
  column values `mined` / `2026-10-25` — the `status=`/`opened=` prefixes never occur (grep
  `status=mined` and `opened=2026-10-25` in the lane's SOURCES.md: 0 hits). V3 is red for every
  row regardless of entry state.
- **V4**: counts README lines containing the substring `terminal-bench-task-grader.md`. After the
  drafted integration this occurs twice — the index row (patch a) AND the coverage discharge bullet
  (patch c, which names `knowledge/terminal-bench-task-grader.md`). `len(index_rows) != 1` → red.
- **V6**: requires the exact clause `SWE-bench Pro V2 graders beyond round-31` in the Frontier
  section; the README (original and patched line 279) writes `any SWE-bench Pro V2 grader beyond
  the round-31 task-level one` — the phrase `graders beyond round-31` does not occur anywhere
  (grep: 0 hits). Also `protein-assembly` + PIN do appear, so only the grammar mismatch bites.
- **V7**: control-c1.txt stores values as `97` and `0` under prose headers (`## registry rows count
  (expect 97)`); the regex requires the literal sequences `registry rows = 97` and
  `rows S105+ = 0`, which don't occur.

None of these four interact with the entry mutations, so the kill/miss verdicts above are
unaffected; but the counter as drafted cannot pass the frozen C1 acceptance on the drafted
integration until V3/V4/V6/V7 are reconciled with the SOURCES/README/control formats.

## Restoration / hygiene

Ext lane files were modified (no writes outside the scratch root; no `jac`/git state touched).
Scratch mirrors retained as evidence under `.ufo/waves/round-34/mut-entries-scratch/`
(`mut1-drop-source` … `mut5-change-quote-number`, plus the integrated pristine tree).

VERDICT: mut-entries (missed 2/5)
