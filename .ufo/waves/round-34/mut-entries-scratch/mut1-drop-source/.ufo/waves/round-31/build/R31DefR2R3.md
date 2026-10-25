# R31 — routed defects R2 and R3: the Q6 basis and the Q2 tier cell

Seat: reviewer (`R31DefR2R3`). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD
`0883e72` (`round-30 verifier spot-check …`). No production edit was made; the lesson was not touched.
Scratch: `/tmp/r31-R2R3/` (<1 MB). No tool installed or upgraded this seat.

## Snapshot the quotes below are pinned to

| file | sha256 (worktree, this seat's run) | state |
|---|---|---|
| `corpus/lessons/round-30.md` | `c7733b08b858940beb8ed5f3dcafd0dc745f34bee7c9ab1b9b5060e455d75762` | 208 lines; `git diff --numstat` → `21 0` (errata appended during this run) |
| `corpus/knowledge/contamination-transparency-card.md` | `eb8dacfd…` (first read) → `666f90faa079d34e7910fef01ae64e781f19ac7fe6611136ac19a1a6b483d965` (write time) | 196 → 197 lines; `12 10` → `13 10` vs HEAD (R4/R7/R8 repairs landing concurrently) |
| `corpus/SOURCES.md` | `dec033bf982cce1fb8852703647ad38165c128b06fdab0ee2a56036162fcb5c3` | 88 rows, A 78 / B 8 / C 2 |
| `plans/round31_defects.py` | `370913781baf…` (first read) → `2c320d58dab609d7041318980354d0369cde437eef5ddf8a75012a0a7d4f3234` (write time) | **untracked** (`?? plans/round31_defects.py`); `check_r2` body unchanged between the two hashes |

The entry moved twice under this review (`eb8dacfd…` → `666f90f…`): the admitted wording stayed at
`:72`, the retraction moved `:81-83` → `:82-83`, and the S086 peer-review sentence moved `:152-154` →
`:153`. Both counter hashes agree on `check_r2`/`check_r3`/`check_r10` and both print `R2=''`, `R3=''`,
`R10=''` on the lesson bytes at `c7733b08…`.

Two files moved under this review: the errata section appeared at `:189-208` while I was reading, and
`check_r2`'s body changed from a raw-substring test to `flat(...)` between two of my own reads. Every
claim below is pinned to the hashes above; a re-run against other bytes is a different measurement.

## (a) The exact text to be corrected

`corpus/lessons/round-30.md:60-61` (raw, R3 target):

```
60:   action, `writer: KengakuR30`); Q2 **pass for the entry's own claims** (S081 B, S082 B, S083 A, S084 A,
61:   S085 B, S086 A) and **not load-bearing for the field mapping**, which is labelled as this entry's
```

Wrong token: **`S086 A`** on `:61`. The other five cells (`S081 B`, `S082 B`, `S083 A`, `S084 A`,
`S085 B`) re-derive correctly.

`corpus/lessons/round-30.md:66-67` (raw, R2 target):

```
66:   S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass (§Extends names both
67:   objects; the delta is stated as one field, one placement, one value set); Q7 pass (entry + index row +
```

Wrong clause: **"the delta is stated as one field, one placement, one value set"** on `:67`.

Both strings survive verbatim in the worktree: `one field, one placement, one value set` occurs once raw
(on `:67`), and `S085 B, S086 A` occurs twice raw — on `:61` and again inside the new errata's quote at
`:201`. Append-only therefore holds, and the repair is an append, not a rewrite.

## (b) Is "S086 A" wrong? The registry's own tier cell

**Yes.** Re-derived, not quoted from the counter:

- `corpus/SOURCES.md:110` is the S086 row. Its fourth cell, under the header
  `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
  at `corpus/SOURCES.md:21`, reads **`B`**. The row splits into exactly 11 cells, so the column is
  unambiguous.
- The same row's `scope` cell: "the paper's own contamination-detection method and its false-positive
  caveat for code benchmarks, in Japanese; the society publishes these proceedings **without peer
  review**".
- Independent arithmetic from the lesson's own transition line. `:93` says "tier A 76 → 78, tier B 4 →
  8". A census over the pre-round blob (`git show 363a4ebf:corpus/SOURCES.md`) gives 82 rows, A 76 / B 4
  / C 2; the worktree gives 88 rows, A 78 / B 8 / C 2, i.e. ΔA = +2 and ΔB = +4. The six rows added by
  round 30 are `S081 B, S082 B, S083 A, S084 A, S085 B, S086 B` — 2 A + 4 B. The `:61` set (3 A + 3 B)
  contradicts `:93` by one row in each column, and S086 is exactly the row that differs.

So the registry says `S086 B`, the lesson's own cell-transition arithmetic says `S086 B`, and the
enumerated set on `:61` says `S086 A`. The cell is wrong; the tier of every other row in it is right.

## (c) Does the verdict change, or only the stated basis?

**Only the basis, for both.** Each is re-derived against the bar row's own text:

- **Q2** (`corpus/QUALITY.md:24-27`): "Each load-bearing claim rests on ≥1 `SOURCES.md` row of tier A or
  B *for that claim's scope*". B clears an A-or-B floor, and S086's scope cell matches the use the entry
  makes of it (CG1/CG2 at `:91-92`, CG4 at `:94` — the code-corpus detector and its false-positive
  caveat). The verdict "pass for the entry's own claims" survives; what was wrong is the enumerated tier
  set printed beside it.
- **Q6** (`corpus/QUALITY.md:50-54`): the test is that the entry names the existing entry or coverage row
  it extends and does not duplicate it. `§Extends` (`entry :157-164`) names
  `contamination-detection-and-transparency.md` and the coverage-map row
  (*Contamination transparency card format*). The retracted three-part delta is **larger** than the
  admitted one, so the correction shrinks a claim; it does not convert the entry into a duplicate,
  because the surviving delta is non-zero — the card-level integrity state (`entry :69`, `:72-73`). The
  pass stands on the corrected basis.

One consequence worth stating in the erratum itself: the delta sentence is **not** "one field, one
placement, one value set" narrowed to "one field" with the placement/value-set legs intact. The entry
retracts all three legs (`entry :82-83` in the current worktree, `:78-79` at `0883e72`: "Two earlier readings of this paragraph ("two new fields", then
"one field, one placement, one value set") overclaimed; this is the corrected one"), and states the
admitted wording at `:72-73`: "So the delta is one field, and the rest is not a delta at all."

Interaction with R7: the sentence at HEAD `:71-72` ("**S2's tri-state integrity flag is the only new
field**") is itself being repaired in this round, and the worktree now reads "**The card-level integrity
field is the only new one; its tri-state vocabulary is not**". An erratum that quoted the HEAD sentence
would quote bytes the same round deletes. The landed errata correctly does not quote it.

## (d) The append-only form, and a review of the errata that landed

### Form, and what append-only requires here

Append-only is satisfied: `git diff --numstat -- corpus/lessons/round-30.md` → `21 0`, zero deletions,
one new section after the previous last line `:187` ("and resent unchanged once a slot settled."). The
cells at `:3`, `:60-61` and `:66-67` are untouched.

The erratum must carry, at minimum, these four things — one per corrected cell, plus the frame:

1. **Frame**: the section label ("Errata"/"Erratum"), the round and date, and the statement that the
   cells above stand as written because the file is append-only.
2. **Q6**: the superseded basis (quoted or located by line), the admitted wording verbatim —
   *one field, and the rest is not a delta at all* — and the explicit statement that the **verdict** does
   not change, with the reason: `§Extends` names the round-24 entry and the coverage row, and the
   surviving delta is non-zero.
3. **Q2**: the superseded cell (quoted), the registry tier `B` **with a locator**, the lesson's own `:93`
   arithmetic, and the statement that the verdict stands because Q2's floor is A-or-B.
4. **Round shape** (R10, same append): `34 falsify` → 33, from the committed registry.

### What landed (`:189-208`) and what is right in it

Three bullets — Q6 basis (`:195-200`), Q2 tier cell (`:201-204`), round shape (`:205-208`) — under the
heading "## Errata (round 31, appended 2026-10-25 …)". Verified accurate:

- the citation "`round-30-verifier-spotcheck.md` §5 items 2, 3 and 8" matches §5's own numbering (item 2
  = the `:66-67` Q6 basis, item 3 = the `:60-61` tier cell, item 8 = the `:3` round shape);
- "this lesson's own `:93` already counts "tier A 76 → 78, tier B 4 → 8"" — exact quote of `:93`;
- the round-shape bullet's "33 members" and "36" re-derive: `len(members)` of
  `.ufo/waves/round-30/falsify/swarm-registry.json` = 33 (scout 12, reviewer 8, critic 5, executor 5,
  mutation-tester 1, revenger 1, connector 1 → 16 in the attack reading), build registry = 36;
- both verdict-unchanged claims are correct as argued in (c).

### Three defects in the landed errata

**D1 (medium) — the Q6 bullet's locator does not contain the sentence it quotes.** `:196-197` cites
`corpus/knowledge/contamination-transparency-card.md:78-81` for the retraction *and* for the quoted
admitted wording. The admitted wording is at `:72-73` in the worktree (`:71` at `0883e72`); the
retraction sentence starts at `:82` in the current worktree (`:78` at `0883e72`) and runs to `:83`
(`:79`). At HEAD the span `:78-81` catches the retraction's first two lines but not the quoted admitted
sentence; in the worktree it begins mid-R1-strata sentence. Three observations of the entry across this
run (`eb8dacfd…` 196 lines, `666f90f…` 197 lines, HEAD 194 lines) put the retraction at `:81-83`,
`:82-83` and `:78-79` respectively, so the cited `:78-81` matched the retraction start only once, at
HEAD, and never covered the quoted wording. A closure that follows the citation to re-derive
the quote gets no match — the class round-30's own §Mistakes names ("an adjacent repair that records the
mismatch instead of answering it"). Because the entry is still being edited (`13 10` vs HEAD), the fix
should cite both spans *and* quote the sentences, or pin the blob sha.

**D2 (low) — the Q2 bullet cites the registry row without a line number.** `:202` says "(`corpus/SOURCES.md`,
S086 row, tier cell `B`)". The row is `:110` and the `tier` header is `:21`; a locator costs one token
and makes the re-derivation mechanical.

**D3 (low) — the Q6 reason is one-sided.** `:199-200` gives "the entry does name both objects it
extends" as the reason the verdict holds. That answers Q6's naming clause only; the non-duplication
clause is carried implicitly by "only the card-level integrity field is new". Also, one of the "both
objects" is the round-6 union table inside a **staged, non-lane-admitted** file (`entry :40-45` says so
itself), so the naming basis that is unambiguously lane-side is the round-24 entry plus the coverage row.
Both are one clause away from being exact.

### Mechanical constraints the text must keep satisfying (mutant-verified)

Against the pinned counter (`sha256 370913781baf…`), in `/tmp/r31-R2R3/lane` (lesson + registry +
falsify registry copied; the proposed text written there, never in the lane):

- `check_r2` flattens the tail after the **raw** `rfind` of `one field, one placement, one value set`, so
  (i) the admitted wording must appear after the *last raw* occurrence and (ii) the word
  `errata`/`erratum` must also appear after it. Mutants: re-quoting the retracted string on one raw line
  with the label only in the heading → red, "the block correcting the Q6 basis is not labelled as an
  erratum"; dropping the admitted wording → red, "no appended erratum states the admitted Q6 basis after
  the retracted one".
- `check_r3` needs the literal `S086 B` **after** the last raw occurrence of `S085 B, S086 A`. Mutants:
  correction moved before the quote → red; correction removed → red; `S086 tier B` → red.
- Both predicates are substring tests, not semantic ones. The landed text is green on all three
  (`R2=''`, `R3=''`, `R10=''`), which is why D1 — invisible to the counter — has to be caught here.

### Proposed replacement for the section (fixes D1-D3, stays green)

Verified in `/tmp/r31-R2R3/lane` against the pinned predicates: `R2=''`, `R3=''`, `R10=''`; zero
deletions versus HEAD's lesson.

```markdown
## Errata (round 31, appended 2026-10-25 — this file is append-only, so the cells above stand as written)

Three counted cells are corrected here rather than rewritten. Round 30's non-author closure routed them
(`corpus/lessons/round-30-verifier-spotcheck.md` §5 items 2, 3 and 8); the counter that re-derives them is
`plans/round31_defects.py` (checks R2, R3, R10).

- **Q6 basis (supersedes the `:66-67` cell).** The cell states the delta as "one field, one placement,
  one value set". The admitted entry retracts that reading by name and states the admitted one
  (`corpus/knowledge/contamination-transparency-card.md:82-83` and `:72-73` in the round-31 worktree;
  `:78-79` and `:71` at `0883e72`): "Two earlier readings of this paragraph … overclaimed; this is the
  corrected one", and the admitted wording is **one field, and the rest is not a delta at all** — S1 is a
  rename, R1 a value set inherited from two cited-or-tabulated sources, and only the card-level integrity
  field is new. The Q6 **verdict** does not change: §Extends names the round-24 entry
  (`contamination-detection-and-transparency.md`) and the coverage-map row, and the surviving delta is
  non-zero, so the entry extends the round-6 union table rather than duplicating it. The basis the cell
  quoted, not the verdict, was wrong.
- **Q2 tier cell (supersedes the `:60-61` cell).** The cell lists the Q2 tier set as "S085 B, S086 A".
  The registry records S086 at tier `B` (`corpus/SOURCES.md:110`, fourth cell; the `tier` column header
  is `corpus/SOURCES.md:21`), so the set is S085 B, S086 B. This lesson's own `:93` agrees: "tier A 76 →
  78, tier B 4 → 8" from a pre-round census of A 76 / B 4 / C 2 (`git show 363a4ebf:corpus/SOURCES.md`)
  admits four new B rows, and the six new rows are B, B, A, A, B, B. The Q2 verdict stands — Q2's floor is
  a tier A or B row for the claim's scope (`corpus/QUALITY.md:24-27`) and a B clears it — so the cell,
  not the verdict, was wrong.
- **Round shape (supersedes `:3`).** The header says "36 build, 34 falsify". The committed falsify
  registry holds **33** members (`.ufo/waves/round-30/falsify/swarm-registry.json` → `len(members) = 33`),
  the build registry holds 36, and the round report says 33; 33 falsify seats of 69 is the shape, with
  16 of the 33 in attack roles (reviewer 8 + critic 5 + mutation-tester 1 + revenger 1 + connector 1).
  The `34` was a transcription slip, not a dispatch difference.

Both superseded strings above are quoted, never rewritten; this section is appended errata and the
round-30 bytes at `:60-61` and `:66-67` stand as written.
```

Note the elision `"Two earlier readings of this paragraph … overclaimed"`: it keeps the retracted
three-part string out of a single raw line, so the counter's anchor stays at `:67`. The landed version
achieves the same by line-wrapping the quote; either is fine, but the closing sentence carrying the word
"errata" is what makes the label survive the `rfind` — do not drop it.

## Finding outside the frozen ten (report it; do not score it)

`corpus/lessons/round-30.md:66` also states "S081/S082 preprints vs **S083/S086 peer-reviewed**". The same
registry row contradicts it: `corpus/SOURCES.md:110` scope cell — "the society publishes these
proceedings **without peer review**" — and the admitted entry says the same at `:153-154` in the worktree (`:152-154` at `0883e72`) ("S086 is a
言語処理学会 2025 paper that the society publishes **without peer review** … so it is labelled a
non-peer-reviewed proceedings paper, not a peer-reviewed result").

So after R3's erratum the lesson will say S086 is tier `B` on `:61` and still call it peer-reviewed on
`:66`, seven lines apart, two labels for one row. This is **not** one of R1-R10: C2's predicate fixes the
count at 10, and adding an R11 after seats have scored would move a frozen predicate. Two honest
options: (i) carry it as a fourth bullet explicitly marked *uncounted*, in which case the heading's
"Three cells" must read "Three counted cells … plus one uncounted correction", and the round must say in
its receipt that `defects=0` does not cover it; or (ii) record it as open debt for round 32 in the report
and `SCORECARD`. What is not available is leaving it silently uncorrected while the errata's own opening
sentence claims the lesson's wrong cells have been dealt with.

## Residual risk and verification gaps

- The counter is **untracked** (`?? plans/round31_defects.py`) and its body changed during this review
  (`check_r2`: raw → `flat`). The errata's claim that it "re-derives" the cells is true only of the bytes
  at `sha256 370913781baf…`. C2's predicate needs those bytes at HEAD; R9 already enforces committed
  artifacts for the seat reports, and the counter deserves the same.
- Entry line numbers are unstable this round (`13 10` vs HEAD, repairs still landing), so D1's locator
  will drift again before the round commits. A locator that survives is the sentence text plus the blob
  sha, not a line span.
- Measured, once, as a snapshot and not as a landing measurement: `python3 plans/round31_defects.py
  --lane .` at lesson `c7733b08…` → `DEFECT R9 … R30DraftGate.md still differs from HEAD`, `checks=10
  defects=1`, exit 1. R2, R3 and R10 are green in that snapshot; R9 is the only red.
- Not verified by me: whether Q6's "extends" survives a strict reading in which `§Extends`' second named
  object is a staged document. I judged Q6 satisfied by the round-24 entry plus the coverage row and said
  so; the staged union table is not lane-admitted and the entry says so at `:40-45`.
- No file outside this report was written in the lane; no `git` command beyond read-only `show`, `diff`,
  `status`, `log`, `cat-file`.

VERDICT: R2 and R3 are correctly diagnosed and correctly repaired in append-only form — both superseded strings still stand at HEAD (`:60-61`, `:66-67`), the tier correction is right (S086 = `B`, re-derived from `corpus/SOURCES.md:110` and from the lesson's own `:93` arithmetic: ΔA +2 / ΔB +4 against A 76 / B 4 / C 2 at `363a4ebf`), both verdicts survive while only their bases change (Q2's floor is A-or-B; Q6 needs naming plus a non-zero delta, and the surviving delta is the card-level integrity field) — but the Q6 bullet's locator `:78-81` does not contain the sentence it quotes, so the erratum is not yet re-derivable by a closure, and the same registry row's "without peer review" still contradicts the lesson's Q5 clause at `:66`, uncorrected and outside the frozen ten.
