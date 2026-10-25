# R31DefR1 — R1: the round-30 delta declaration vs the entry's retraction

Seat: reviewer, round 31 (hyaku run 6, 2026-10-25). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Routed defect: `LOG.md:792-793` declares the round-30 delta as "two new fields, one new value set";
R1's frozen text (`plans/round31_defects.py:11-13`) says the entry retracts that reading and that the
repair is an appended named correction.
No production edit was made. Scratch: `/tmp/r31-r1/` (420 KB). No tool installed, no pacman transaction.

Receipts (all commands run from the lane root):

| what | command | result |
|---|---|---|
| original bytes at baseline | `git show 0883e72:LOG.md` | 842 lines; `:791-794` quoted below |
| entry at baseline | `git show 0883e72:corpus/knowledge/contamination-transparency-card.md` | 194 lines |
| live counter | `python3 plans/round31_defects.py --lane .` | `checks=10 defects=1`, exit 1 — only `R9` red |
| frozen control | `.ufo/waves/round-31/claims/defects-before.txt` | `checks=10 defects=10` |
| worktree state | `git status --porcelain` | `LOG.md`, the entry, the lesson, `plans/sources_adopt.py`, five round-30 seat reports modified; `.ufo/waves/round-31/`, `corpus/evidence/round31/` untracked |

`LOG.md` was clean when this seat started and carried a sibling's appended block by the time the review
reached the mechanical stage. Both states are recorded below; every quote is pinned to the tree it came
from.

---

## 1. Do the two disagree? — CONFIRMED

**The LOG.md clause, at baseline `0883e72` (raw bytes, two lines):**

```
791|   the ANLP 2025 paper), replaced every anchor with a located quote from this round's own fetch,
792|   mapped the field list into the round-6 union table's own columns, declared the delta (two new
793|   fields, one new value set), renamed the entry's own answerability questions **CG1–CG8** to stop
```

Flattened (whitespace collapsed, the way `plans/round31_defects.py:71-73` reads it) the declaration is
`declared the delta (two new fields, one new value set)`.

**The entry, at the same commit `0883e72`:**

```
71|So the delta is one field, and the rest is not a delta at all. **S2's tri-state integrity flag is the
72|only new field.** S1 is not a new field: the CTC v1.1 column beside it reads `type 5 recorded per run`,
...
76|designs, while also being present in S081's own four-field protocol (F1, strata) — so strata is a value
77|set this entry inherits from two cited-or-tabulated sources, not a discovery, and the mapping row above
78|is the authoritative status. Two earlier readings of this paragraph ("two new fields", then "one field, one
79|placement, one value set") overclaimed; this is the corrected one, and it is why the amendment is a
80|mapping rather than a design.
```

The two disagree, on **both** halves of the LOG's parenthetical, and they disagree **in the same commit**:

1. Field count. LOG says two new fields; the entry says `one field` (`:71`) and names `two new fields` as
   the **first** of the two readings it retracts (`:78`).
2. Value set. LOG says one **new** value set; the entry says strata is `a value set this entry inherits
   from two cited-or-tabulated sources, not a discovery` (`:76-77`). Inherited is not new.

Precision worth keeping: the LOG's string matches **neither** reading the entry names. The entry's
retracted readings are `"two new fields"` and `"one field, one placement, one value set"` (`:78-79`). The
LOG's is a hybrid — the first reading's field count plus a fragment of the second's value-set claim, with
"one placement" dropped. A correction that says the LOG repeated the second reading would itself be
wrong; it must quote the LOG's own string.

Byte-level detail that matters for any correction: the string `two new fields` **does not occur
contiguously in `LOG.md`** — it is split by the line break at `:792/:793`
(`grep -c "two new fields" LOG.md` → `0`; `grep -c "one new value set" LOG.md` → `1`). It exists only
after whitespace flattening. So the correction cannot rely on a raw byte grep to demonstrate the original
is intact; it must use the same flattening the counter uses, or grep the fragment `two new`.

## 2. The routed window `card.md:74-81` — what it does and does not contain

The assignment points at `contamination-transparency-card.md:74-81` as "the entry's retraction". At
`0883e72` that window is:

- `:74-75` — the S1 filing question ("whether that makes the record score-side … which it has not admitted");
- `:76-77` — the value-set ruling (`… not a discovery`);
- `:78-80` — **the retraction sentence**;
- `:81` — blank.

So the window **does** contain the retraction and the value-set ruling, and it is enough to confirm the
disagreement. It **does not** contain `:71-72`, i.e. the admitted delta sentence
(`one field, and the rest is not a delta at all`) or the superseded-in-entry wording
(`S2's tri-state integrity flag is the only new field`). A seat that read only the routed window would
have to invent the admitted wording — which is precisely the requirement (ii)/(iii) content. The
correction must therefore cite `:71` **and** `:78-80`, not the routed window.

The window has also already drifted, twice, inside this round:

| tree | delta sentence | retraction sentence | file length |
|---|---|---|---|
| `0883e72` | `:71` | `:78-80` | 194 |
| live worktree (R6 repair landed at `:41`) | `:72` | `:82-84` | 196 |

The `+1` at `:41` is visible in `git diff -- corpus/knowledge/contamination-transparency-card.md`
(`three source rows` → `two of its three source rows`, plus a re-wrap), and the `+3` before the
retraction is the R7 repair at `:72-74` (`The card-level integrity field is the only new one; its
tri-state vocabulary is not`). Consequence: **no bare line number for this entry is stable across this
round.** Any locator must be section-relative (`§Field mapping into the union table`) and/or pinned to a
commit.

## 3. Four different strings are in play — the conflation hazard

| # | string | where | status |
|---|---|---|---|
| A | `two new fields, one new value set` | `LOG.md:792-793` (`0883e72`) | superseded; `SUPERSEDED_DELTA` |
| B | `one field, one placement, one value set` | entry `:79` (`0883e72`), lesson `:66-67` | retracted reading; `RETRACTED_Q6` |
| C | `one field, and the rest is not a delta at all` | entry `:71` (`0883e72`), `:72` (worktree) | admitted; `ADMITTED_DELTA` |
| D | `S2's tri-state integrity flag is the only new field` | entry `:71-72` (`0883e72`) | superseded **by R7**; the repaired entry reads `card-level … the only new one` |

A is not B. C is not D. A correction that quotes B as the thing LOG said, or quotes D as the thing the
entry says now, is wrong in this round's own terms.

## 4. What an append-only correction must contain — four testable conditions

**(i) The original stays byte-identical.** Not provable by the counter (§7, C-4), so it needs its own
command. The file's existing idiom is `git diff --numstat` (lesson `:95`: "6 insertions, 0 deletions"):

```
git diff --numstat 0883e72 -- LOG.md      # must be "<N>\t0\tLOG.md" — 0 deletions
```

and the substantive half: `:791-794` must still read as quoted in §1, including the line break inside
`two new | fields`, because that break is what a rewrite would silently normalise.

**(ii) It names the superseded wording.** Three parts, all required: the quoted string (A, verbatim,
comma form), its location (`LOG.md:792-793`), and an explicit status word (`superseded`). Quoting the
string without the location makes the reader hunt; naming it without quoting it lets the string drift.

**(iii) A reader can tell which reading is current.** Two sentences, one per direction: one saying the
paragraph is the current reading, one saying the round-30 text stands as filed and is not the entry's
position. The second is not decoration — the file's own precedent is a defect mined from exactly this
(round 9, `LOG.md:15`: "round 7's amendment rewrote `LOG.md:9` in place … **Major 2** (append-only
violation, rule 9)").

**(iv) A checker can verify it mechanically.** Four assertions, which are exactly `check_r1`'s
(`plans/round31_defects.py:104-115`): A present at all; A present **twice** after its first occurrence
(original + quote); the literal token `correction` in that tail; C present in that tail. Plus the
numstat assertion from (i), which the counter does not make.

Mechanical traps inside (iv), each measured (§6): the admitted string must keep its **comma** — the
lane's house style would write `one field — and the rest is not a delta at all`, which turns the check
red; the superseded string may be bolded or re-wrapped (flattening tolerates both) but not hyphenated;
and the label must be the token `correction`, not `corrected` (unlike R2, which accepts `errata`/`erratum`
— so a single block reused in both files needs both tokens, or two blocks).

## 5. Proposed correction block — exact heading and required sentences

Heading (recommended form; rationale in §6.4):

```
### Round30 — C1 delta wording: appended correction (appended 2026-10-25, round-30 text not rewritten)
```

Required sentences, in order, each mapped to a condition:

1. *(ii)* The round-30 C1 item declares the delta at `LOG.md:792-793` as "declared the delta (two new
   fields, one new value set)".
2. *(iii)* That wording is superseded, and this paragraph is the current reading of it.
3. *(ii)+(iii)* The admitted entry states the delta as "one field, and the rest is not a delta at all"
   and retracts the LOG's reading in its own bytes — "Two earlier readings of this paragraph ("two new
   fields", then "one field, one placement, one value set") overclaimed; this is the corrected one" —
   both in `corpus/knowledge/contamination-transparency-card.md` §Field mapping into the union table, at
   `:71` and `:78-80` of `0883e72` (`:72` and `:82-84` in the repaired entry).
4. *(iii)* The one new object is the card-level integrity field, not the tri-state vocabulary; S1 is a
   rename of a fact the CTC v1.1 form already carries, with the entry leaving open whether that makes the
   record score-side; and strata is a value set the entry "inherits from two cited-or-tabulated sources,
   not a discovery", so "one new value set" is not a delta either.
5. *(i)* Correction, not a rewrite: the round-30 text above stands as filed, and
   `git diff --numstat 0883e72 -- LOG.md` reports 0 deletions.
6. *(iv)* Routed by round 30's non-author closure (`corpus/lessons/round-30-verifier-spotcheck.md` §5
   item 1) and re-derived by `plans/round31_defects.py` check R1; the same locator is corrected in
   `corpus/lessons/round-30.md` §Errata.

Exact bytes, appended after `LOG.md:842` (end of file at `0883e72`) and before any `## Round 31` section:

```markdown

### Round30 — C1 delta wording: appended correction (appended 2026-10-25, round-30 text not rewritten)

The round-30 C1 item declares the delta at `LOG.md:792-793` as "declared the delta (two new fields, one
new value set)". That wording is superseded, and this paragraph is the current reading of it. The
admitted entry states the delta as "one field, and the rest is not a delta at all" and retracts the LOG's
reading in its own bytes — "Two earlier readings of this paragraph ("two new fields", then "one field,
one placement, one value set") overclaimed; this is the corrected one" — both in
`corpus/knowledge/contamination-transparency-card.md` §Field mapping into the union table, at `:71` and
`:78-80` of `0883e72` (`:72` and `:82-84` in the repaired entry). The one new object is the card-level
integrity field, not the tri-state vocabulary; S1 is a rename of a fact the CTC v1.1 form already
carries, with the entry leaving open whether that makes the record score-side; and strata is a value set
the entry "inherits from two cited-or-tabulated sources, not a discovery", so "one new value set" is not
a delta either. Correction, not a rewrite: the round-30 text above stands as filed, and
`git diff --numstat 0883e72 -- LOG.md` reports 0 deletions. Routed by round 30's non-author closure
(`corpus/lessons/round-30-verifier-spotcheck.md` §5 item 1) and re-derived by `plans/round31_defects.py`
check R1; the same locator is corrected in `corpus/lessons/round-30.md` §Errata.
```

16 lines, 1,494 bytes, max column 105 — inside the round-30 entry's own range (`:780-842` max column
106, mean 84). Style basis: the five appended blocks in the immediately preceding round
(`LOG.md:675`, `:705`, `:731`, `:748`, `:765`) are bold lead-ins inside the round entry; the H3 form is
the one used at `:298` and `:613`, where the corrected round's entry already carries H3s. Round 30's
entry has none, and this block *is* an H3 subsection of it, so H3 is the consistent choice — see §6.4.

## 6. Mechanical proof of the proposal

### 6.1 The block passes R1

`check_r1` on a `/tmp` lane holding `0883e72:LOG.md` + the block: reason `''` (green), superseded
occurrences `2`, admitted string present. Baseline, same lane without the block:
`no appended correction quotes the superseded delta wording (only the original occurrence exists)` —
byte-identical to the live `DEFECT R1` line in `.ufo/waves/round-31/claims/defects-before.txt`.

### 6.2 Mutation matrix — what turns R1 red

| mutation of the proposed block | `check_r1` |
|---|---|
| as proposed | GREEN |
| admitted wording as `one field — and the rest is not a delta at all` | `the appended correction does not state the admitted wording 'one field, and the rest is not a delta at all'` |
| superseded string hyphenated (`two new-fields`) | `no appended correction quotes the superseded delta wording (only the original occurrence exists)` |
| original clause rewritten to `(one field, one value set)` | red, **wrong message** (see C-2) |
| block quotes only the admitted string | `no appended correction quotes the superseded delta wording …` |
| superseded string bolded `**two new fields, one new value set**` | GREEN (emphasis outside the span is harmless) |
| superseded string re-wrapped across a line break | GREEN (flattening) |
| typographic outer quotes on the retraction | GREEN |
| H3 heading instead of bold lead-in | GREEN |

### 6.3 What the proposal proves and what it does not

It proves the four `check_r1` assertions are satisfiable by one block that also carries (i), (ii)'s
location, and (iii)'s two-directional marker. It does **not** prove append-only placement (C-4) or the
correctness of any locator (C-1) — neither is something `check_r1` measures.

### 6.4 Heading choice against the file's own convention

`LOG.md:298` — `### Round 25 falsify-wave revision (appended 2026-10-20 ~23:25 -03; the entry above stays
as landed in `8ea41f9`)`; `LOG.md:613` — `### Round29 — current-tree source-copy containment correction
(2026-10-21)`. Both are appended subsections named for the round they **correct**. The proposal follows
that. It also keeps the literal token `correction` in the heading, so the label requirement is satisfied
by the heading and not incidentally by the checker's own name (§7, C-3).

## 7. Review of the block already landed in the worktree

A sibling appended a correction while this seat was reading. Bytes reviewed:
`LOG.md:844-854`, sha256 `522ef2e5fb9c402f181fdb44ab76c57837e65af8913e219922aef1e9b98fced9`
(whole file sha256 `8450b490101a161b1dddd2f0c234206f42b2147d7cca2bf26044bc42400fa5c3`, 854 lines);
`git diff --numstat -- LOG.md` → `12 0 LOG.md`.

```
844|### Round 31 — correction to the round-30 C1 entry above (appended 2026-10-25, not rewritten)
846|The round-30 entry declares the card's delta as "declared the delta (two new fields, one new value set)".
847|That wording is superseded. The admitted entry retracts it in its own bytes
848|(`corpus/knowledge/contamination-transparency-card.md:78-81`): the delta is **one field, and the rest is
849|not a delta at all** — S1 is a rename of a fact the CTC v1.1 form already carries, R1's strata are a value
850|set inherited from two cited-or-tabulated sources, and only the card-level integrity field is new.
851|Correction, not a rewrite: the round-30 text above stands as filed, per the append-only rule. Routed by
852|round 30's non-author closure (`corpus/lessons/round-30-verifier-spotcheck.md` §5 item 1); re-derived by
853|`plans/round31_defects.py` check R1. The same reading is corrected in `corpus/lessons/round-30.md` §Errata
854|(Q6 basis) in this round.
```

It is green on R1 (`defects=1`, R9 only), 0 deletions, and it satisfies (ii)'s quote, (iii)'s
"superseded" marker and (iv) exactly. It fails on three points.

### MAJOR-1 — the only locator into the entry does not locate either quoted sentence

`:78-81` is cited for the whole sentence set. Measured:

| tree | `:78-81` contains the admitted sentence C? | contains the retraction? | where C actually is | where the retraction actually is |
|---|---|---|---|---|
| `0883e72` | **no** (`grep -c` → 0) | yes (`:78-80`, one line over) | `:71` | `:78-80` |
| live worktree | **no** (`grep -c` → 0) | **no** (`overclaimed` absent from `:78-81`) | `:72` | `:82-84` |

So in the tree the block will be committed with, `:78-81` reaches neither the admitted sentence nor the
end of the retraction — it stops one line short of `Two earlier readings …` at `:82` and one line before
`placement, one value set") overclaimed`. `check_r1` returns `''` regardless, because it never looks at
the locator (C-1). This is the same class as round 29's `### Round29 — locator corrections and scratch
safety` (`LOG.md:597-603`) and round 30's D1. The same wrong locator is duplicated at
`corpus/lessons/round-30.md:197`, so one edit fixes both or neither.

### MAJOR-2 — one clause is true only because an uncommitted sibling repair is true

`only the card-level integrity field is new` (`:850`) is correct against the repaired entry (`:72-74`)
and **false against the commit the block cites** — at `0883e72` the entry reads `S2's tri-state integrity
flag is the only new field` (`:71-72`), with no `card-level` token anywhere. The retraction half of the
same sentence is true at `0883e72`; the card-level half is not. So the block mixes a claim verified at
the cited commit with a claim verified only in the worktree, and no committed state currently holds both.

That is acceptable only as a **commit-coupling requirement**: R7's repair and this block must land in one
commit, and the commit must be the one a reader can verify. Nothing currently asserts it. The check that
would:

```
git show <landing-commit>:corpus/knowledge/contamination-transparency-card.md | grep -c 'card-level'   # 1
git show <landing-commit>:LOG.md | grep -c 'card-level'                                                 # 1
```

If R7 were dropped, the block would be citing a reading the entry does not hold — the exact
"recorded the mismatch instead of answering it" pattern round 30 mined (`LOG.md` item 5, `:826-830`).

### MINOR-1 — heading hierarchy contradicts the file's convention

`### Round 31 — …` is an H3 nested under `## Round 30 — …`. Precedent (`:298`, `:613`) names appended
subsections for the round they correct. As written, a reader scanning headings sees a Round-31 subsection
inside Round 30, and when round 31 appends its own `## Round 31` entry this block will sit *above* it and
read as round-30 content titled Round 31. Fix: `### Round30 — C1 delta wording: appended correction
(appended 2026-10-25, round-30 text not rewritten)`.

### MINOR-2 — the superseded clause has no location

`:846` quotes A but never gives `LOG.md:792-793`. Requirement (ii) is met by the quote alone, but the
clause is already 54 lines above the correction and will move as rounds append. Add the line span.

### MINOR-3 — a hedged claim is presented as settled

`:849` — "S1 is a rename of a fact the CTC v1.1 form already carries". Grounded in the table row
(`:68`, `it is a rename, not a relocation`), but the prose the block summarises (`:75-77`) explicitly
refuses to settle it: "whether that makes the record score-side is a question about *where* it is filed,
and this lane cannot settle it without reading that form, which it has not admitted". The block drops the
hedge. Round 29's fourth correction batch killed exactly this shape of widening (`LOG.md:708-715`,
"Entry widenings removed"). Add: "with the entry leaving open whether that makes the record score-side".

### Verified as accurate

The closing cross-reference is true: `corpus/lessons/round-30.md:189` is
`## Errata (round 31, appended 2026-10-25 — …)`, and its Q6 item is present at `:195-200`.

## 8. Findings about the counter itself (advisory — `plans/round31_defects.py` is frozen for round 31)

**C-1 (MAJOR for calibration).** `check_r1` has no locator assertion, so it cannot see MAJOR-1: it
returns `''` on a block whose only citation is wrong. R1's frozen predicate is therefore satisfied by
"two strings and a word", not by a correction a reader can follow. Hardening for round 32: assert the
quoted admitted string is a substring of the cited range in the cited commit, the way R6 re-derives its
count from the staged file.

**C-2 (MINOR).** Diagnostics invert when the original is destroyed. Repro: rewrite `:792-793` to
`(one field, one value set)` while keeping the block. Result: red, but with
`no appended correction quotes the superseded delta wording (only the original occurrence exists)` — the
message says the *correction* is missing when in fact the *original* was deleted, which sends the repair
in the wrong direction. The first branch (`the superseded wording … is gone from LOG.md`) is unreachable
in that state because the block's own quote satisfies `SUPERSEDED_DELTA in text`.

**C-3 (MINOR).** "Labelled as a correction" is satisfied by any `correction` substring after the
original — including the checker's own name. Measured: a block with the label removed but
`(`log-delta-correction`)` kept → GREEN; label kept, check name removed → GREEN; both removed → red.

**C-4 (MINOR).** Placement is not measured. A block inserted immediately after the round-30 item, not at
EOF, → GREEN. So R1 does not test append-only; the `--numstat` 0-deletion assertion is the only
append-only proof, and it must be part of the receipt.

**C-5 (NOTE).** The frozen docstring says `LOG.md:792`; the string spans `:792-793`, and a raw grep for
the docstring's phrase returns `0`. Cosmetic, but it is the reason a scribe may believe a byte grep
proves the original intact.

**C-6 (NOTE, C2-level).** The C2 predicate's first clause — "prints `defects=10` and exits 1 on the
pre-repair tree" — is no longer reproducible on the live tree: this seat measured `checks=10 defects=7`
mid-round (R4/R5/R8 already repaired) and `checks=10 defects=1` at the end (R9 only). The committed
control `.ufo/waves/round-31/claims/defects-before.txt` is the only receipt of the `10`; any seat that
reruns expecting `10` will record a false mismatch.

## 9. Residual risk and verification gaps

- I did not run the counter against a tree where R7's repair is reverted, so MAJOR-2's dependency is
  established by text comparison at `0883e72` (`grep -c 'card-level'` → 0 there) and not by a red/green
  pair. A two-state receipt would close it.
- The worktree moved three times during this review (R6, then R7, then the LOG block). Every quote above
  is pinned to `0883e72` or to a sha256 of the file I read; line numbers in the live tree are stated as
  observed, not as stable.
- `R9` is still red at the time of writing (`checks=10 defects=1`, exit 1), so C2's `defects=0` is not yet
  reachable; that is outside R1's scope and belongs to the R9 owner.
- No census, gate or selftest was run by this seat: not in R1's scope, and other seats own them.

VERDICT: CONFIRMED — `LOG.md:792-793` and the entry do disagree, on both halves of the LOG's parenthetical, in the same commit; the entry is the current reading; the landed correction at `LOG.md:844-854` satisfies R1 mechanically but its only entry locator (`:78-81`) locates neither quoted sentence in either tree (MAJOR-1) and its "card-level" clause is true only under an uncommitted sibling repair (MAJOR-2) — both must be fixed before the landing commit.
