# R31FxLogErrata — locator audit of the round-31 append-only corrections

Lane: `kengaku-shokunin` @ landed `dbb07364` (round-31 commit). Scope: every locator in the
`## Round 31 — correction` block of `LOG.md` (lines 844–868) and the `## Errata (round 31 …)`
block of `corpus/lessons/round-30.md` (lines 189–208). Each cited range was re-read from current
bytes; the quoted sentence's presence inside the window is stated per locator. No tools were
installed (records: none; python3 stdlib for JSON/counts).

---

## A. `LOG.md` correction block (lines 844–868)

### A1. `LOG.md:792-793` → "declared the delta (two new fields, one new value set)" — RESOLVES, quoted sentence inside
Actual bytes:
```
792: mapped the field list into the round-6 union table's own columns, declared the delta (two new
793: fields, one new value set), renamed the entry's own answerability questions **CG1–CG8** to stop
```
The quoted sentence "declared the delta (two new fields, one new value set)" is present verbatim,
spanning 792–793. The parenthetical "two new fields, one new value set" is exactly what the block
retracts. `python3 plans/round31_defects.py --lane .` → `checks=10 defects=0` exit 0, so check R1
(`LOG.md:792` superseded-delta wording; appended correction quotes it, labels "correction", states
admitted wording; append-only) re-derives as repaired. ✓

### A2. `corpus/knowledge/contamination-transparency-card.md:82-84` → retraction quote — RESOLVES, quoted sentence inside
Actual bytes:
```
82: is the authoritative status. Two earlier readings of this paragraph ("two new fields", then "one field, one
83: placement, one value set") overclaimed; this is the corrected one, and it is why the amendment is a
84: mapping rather than a design.
```
The quoted sentence "Two earlier readings of this paragraph ("two new fields", then "one field, one
placement, one value set") overclaimed; this is the corrected one" is inside 82–84 (line 82–83;
the block's `\"` rendering equals the file's plain `"`). ✓

### A3. `contamination-transparency-card.md:78-81` → strata quote — RESOLVES, quoted sentence inside
Actual bytes:
```
78: it is filed, and this lane cannot settle it without reading that form, which it has not admitted. R1's
79: strata are carried by the CTC v1.1 form (`strata_reported`) and are absent from the other two tabulated
80: designs, while also being present in S081's own four-field protocol (F1, strata) — so strata is a value
81: set this entry inherits from two cited-or-tabulated sources, not a discovery, and the mapping row above
```
The quoted sentence "strata is a value set this entry inherits from two cited-or-tabulated sources,
not a discovery" sits at 80–81, inside 78–81. ✓

### A4. `contamination-transparency-card.md:72-75` → admitted reading — RESOLVES, quoted sentence inside
Actual bytes:
```
72: So the delta is one field, and the rest is not a delta at all. **The only field this entry adds to the
73: union table is S2, and what it adds is the field — a state recorded for the card itself rather than for a
74: contamination type. Its values are not new: the CTC v1.1 form already publishes `controlled` /
75: `not_controlled` / `unknown` / `n/a` per type, and `unknown` / `not_controlled` as valid entries.**
```
The quoted sentence (with `…` standing for the tail after "Its values are not new:") is inside
72–75. ✓

### A5. `:76-78` → the hedge — RESOLVES, quoted content inside
Actual bytes:
```
76: S1 is not a new field: the CTC v1.1 column beside it reads `type 5 recorded per run`,
77: so the run-side fact is carried; whether that makes the record score-side is a question about *where*
78: it is filed, and this lane cannot settle it without reading that form, which it has not admitted. R1's
```
"the hedge" = "whether that makes the record score-side is a question about *where* it is filed, and
this lane cannot settle it without reading that form, which it has not admitted" — inside 76–78. The
block's supporting claims "S1 … is a rename rather than a new field" (line 76) and "this lane has not
admitted that form" (line 78) also match. ✓

### A6. Routing references — RESOLVE
- "Routed by round 30's non-author closure (`corpus/lessons/round-30-verifier-spotcheck.md` §5 item 1)":
  spotcheck §5 item 1 exists and routes exactly this defect: "`LOG.md:792-793` still declares the delta as
  '**two new fields, one new value set**', which the entry retracts…" ✓
- "re-derived by `plans/round31_defects.py` check R1": check_r1 exists, asserts the superseded wording, the
  appended correction quoting it, the "correction" label, the admitted wording and append-only; live run
  `checks=10 defects=0` exit 0. ✓
- "`corpus/lessons/round-30.md` §Errata (Q6 basis)": the Errata block has a Q6 basis entry (see B1). ✓

---

## B. `corpus/lessons/round-30.md` Errata block (lines 189–208)

### B1. `:66-67` (superseded Q6 basis cell) → "one field, one placement, one value set" — RESOLVES, quoted sentence inside
Actual bytes:
```
66: S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass (§Extends names both
67: objects; the delta is stated as one field, one placement, one value set); Q7 pass (entry + index row +
```
"The delta is stated as one field, one placement, one value set" is inside 66–67. ✓
The block's "The Q6 verdict does not change (the entry does name both objects it extends)" also checks
out: entry `## Extends` at `contamination-transparency-card.md:158-166` names both
`contamination-detection-and-transparency.md` (lane entry) and the round-6 staging file
`benchmark-card-field-schema-2026-10-23.md` (union table). ✓

### B2. `contamination-transparency-card.md:78-81` → "the delta is **one field, and the rest is not a delta at all** — S1 is a rename, R1 a value set inherited from two cited-or-tabulated sources, and only the card-level integrity field is new" — **DOES NOT FULLY RESOLVE**
The window's actual bytes are printed in A3. Against the block's attributed paraphrase:
- "the delta is **one field, and the rest is not a delta at all**" — **NOT in 78–81**. That sentence is
  at line **72** ("So the delta is one field, and the rest is not a delta at all."). The Errata misplaces
  the headline clause of its own correction by 6 lines. (The sibling `LOG.md` correction cites the same
  sentence correctly at `:72-75`.)
- "S1 is a rename, R1 a value set inherited from two cited-or-tabulated sources" — partially inside:
  lines 78–81 contain the R1/strata half ("strata is a value set this entry inherits from two
  cited-or-tabulated sources", 80–81); the S1-rename half is at 76–77, just outside the window.
- "only the card-level integrity field is new" — not verbatim anywhere in the entry (grep for
  `integrity field|card-level|only new field`: no matches). It is a compression of lines 69
  ("delta in field — a state for the card itself") and 72–74 ("The only field this entry adds to the
  union table is S2 … a state recorded for the card itself").
Substantively the erratum's admitted wording is correct entry content — just not inside the cited
window. This is the one locator in either block that does not resolve as written.

### B3. `:60-61` (superseded Q2 tier cell) → "`S085 B, S086 A`" — RESOLVES, quoted sentence inside
Actual bytes:
```
60: action, `writer: KengakuR30`); Q2 **pass for the entry's own claims** (S081 B, S082 B, S083 A, S084 A,
61: S085 B, S086 A) and **not load-bearing for the field mapping**, which is labelled as this entry's
```
"`S085 B, S086 A`" is inside 60–61 (line 61). ✓

### B4. `corpus/SOURCES.md`, S086 row, tier cell `B` → "S085 B, S086 B" — RESOLVES
Registry header is `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (SOURCES.md:21). S086 row (worktree and `git show dbb07364:corpus/SOURCES.md` identical for these rows): `| S086 | Code LLM … | paper | B | …` → tier cell = `B`. S085 row tier = `B` likewise. So "S085 B, S086 B" matches the registry. ✓

### B5. `:93` → "tier A 76 → 78, tier B 4 → 8" — RESOLVES, quoted sentence inside
Actual byte at line 93:
```
93: → 82 rows, last ids S077–S080, S090, S091); they enter `mined`, tier A 76 → 78, tier B 4 → 8,
```
"tier A 76 → 78, tier B 4 → 8" is inside line 93. ✓

### B6. `:3` → "36 build, 34 falsify" — RESOLVES, quoted sentence inside
Actual byte at line 3:
```
3: Lane: kengaku (LLM/model research & evaluation). Round shape: two v1 waves (36 build, 34 falsify).
```
"36 build, 34 falsify" is inside line 3. ✓

### B7. `.ufo/waves/round-30/falsify/swarm-registry.json` → `len(members) = 33` — RESOLVES
`python3 -c "import json; d=json.load(open('.ufo/waves/round-30/falsify/swarm-registry.json')); print(len(d['members']))"` → **33**. ✓ (Same measure check_r10 uses.)
"the build registry holds 36" → `.ufo/waves/round-30/build/swarm-registry.json` `len(members)` → **36**. ✓
"the round report says 33" → the round record is `LOG.md` round-30 entry lines 835–837: "Wave 1 build 36 seats (…) Wave 2 falsify 33 seats (12 scout, 8 reviewer, 5 critic, 5 executor, 1 mutation-tester, 1 connector, 1 revenger) — 16/33 attack roles (48%)." → says 33 falsify seats. ✓ (locator implied, resolves)
"16 of the 33 in attack roles" → re-derived from the registry role counts: reviewer 8 + critic 5 + mutation-tester 1 + revenger 1 + connector 1 = **16**, under the reading the lesson itself documents at `round-30.md:162` ("reviewer+critic+mutation-tester+revenger+connector reading"). ✓ with the caveat that the round's own dead-seat report (`R30FxDeadSeats.md:206`) records other counts under other readings (14/33 fleet-with-sentinel; 7/33 critic+mutation-tester+revenger). The Errata repeats the round's own recorded number; it holds under the documented reading.

### B8. Routing references — RESOLVE
- "Round 30's non-author closure routed them (`corpus/lessons/round-30-verifier-spotcheck.md` §5 items 2, 3 and 8)": spotcheck §5 item 2 routes the Q6 basis cell (`:66-67`), item 3 routes the Q2 tier cell (`:60-61`), item 8 routes the round shape (`:3` "34 falsify") — exactly the three cells the Errata corrects. ✓
- "the counter that re-derives them is `plans/round31_defects.py` (checks R2, R3, R10)": check_r2 (proves6-basis), check_r3 (lesson-q2-tier-cell), check_r10 (lesson-round-shape) exist and assert the retracted bytes, the correction of the admitted bytes and append-only; live run `checks=10 defects=0` exit 0. ✓

---

## C. Summary

- Locators verified and resolved (quoted sentence inside cited window): LOG.md:792-793; entry 82-84, 78-81 (strata quote), 72-75, 76-78; lesson 66-67, 60-61, 93, 3; SOURCES.md S086 tier B; swarm-registry.json len=33; build registry len=36; spotcheck §5 items 1/2/3/8; round31_defects.py checks R1/R2/R3/R10 (run: `checks=10 defects=0`, exit 0).
- Locator that does not fully resolve: Errata block's `contamination-transparency-card.md:78-81` attribution of "the delta is **one field, and the rest is not a delta at all**" — that sentence is at `:72`, not inside 78–81; the window contains only the R1/strata half of the paraphrase. The sibling LOG.md correction cites the same sentence correctly at `:72-75`. No other locator fails; no quoted sentence is missing from the entry.
- Corruption/append-only state: LOG.md and round-30.md are unmodified in the worktree (committed at `dbb07364`); the quoted superseded bytes stand as filed. Corrections' claims match the entries' current bytes except for the B2 window placement.

VERDICT: ALL locators in the LOG.md `## Round 31 — correction` block and the round-30.md Errata block resolve and contain their quoted bytes, and the corrections' claims match the entries' current bytes, EXCEPT the Errata's `contamination-transparency-card.md:78-81` citation, which does not contain the attributed headline sentence ("the delta is one field, and the rest is not a delta at all"; actual line 72) and contains only part of the rest of the paraphrase — a window-placement defect in one locator; the substance of every correction is present in the entry and all counters re-derive repaired (`checks=10 defects=0`, exit 0).
