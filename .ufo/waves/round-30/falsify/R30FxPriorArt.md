# R30FxPriorArt — restatement or novelty overclaim in the round-30 card entry

Seat: `L1Kengaku30.R30FxPriorArt-3`, critic. Scope: prior art, the "two fields are new" claim,
the CG1–CG8 gate's instrument status, and the round's non-claim. No lane bytes written except
this file. Nothing installed. Scratch: `/tmp/r30fx-priorart/` (frozen copies, hashes below).

Candidate: `corpus/knowledge/contamination-transparency-card.md`
VERDICT: FAIL — the assigned claim ("exactly two fields are new") was **withdrawn by the writer while I reviewed it** and replaced at `:70-77` by a three-part delta; of its parts S1's "new placement" is unsupported by the cell it cites, R1's "no design tabulates" is false against S081's own protocol row in this lane's registry, and S2's "new field" is unpriced against campaign prior art the round read and rejected; the withdrawn count survives in four landed surfaces. CG1–CG8 is an 8/8 relabel of the refused round-29 Q1–Q8, not a new instrument, and the index still calls those questions "the entry's own".

Byte basis. The entry is untracked at lane HEAD `363a4eb` (`git ls-files` → "did not match any
file(s) known to git"), so it moved three times during this review:
`28f5bbd…` (still carried "exactly two fields are new … (S1, S2)" at `:68`), `df0b6d41…` (one delta
label left, table rewritten), `f01b7cd2…` (current, frozen). All line anchors below are the
**`f01b7cd2…` snapshot** at `/tmp/r30fx-priorart/entry-snapshot.md`; sibling snapshots
`readme 9392efdb…`, `sources cf58f52b…`, `lesson ab0cbc1c…`. Re-check a later revision with
`grep -n 'new field\|new placement\|new value set\|two fields this entry adds\|two delta fields'`.
The campaign file at the entry's own path recomputes to the entry's stated sha256
`666510079…3533b9`; its anchors are `:73` detector access, `:75` release-side vs score-side,
`:78` grader integrity.

## Bottom line

1. **Restatement: mostly honest.** Seven of nine rows map cleanly to the round-6 columns; the
   grader-integrity column dropped in `28f5bbd` is restored and declared at `:61` — that omission
   finding is closed by declaration, not by silence.
2. **Novelty: still overclaimed, more narrowly.** The count sentence was corrected; its
   replacement keeps one falsified part (R1's universal), one part contradicted by the cell printed
   beside it (S1's "placement"), and one part that is defensible against the three tabulated designs
   but not against the campaign prior art this round read and rejected on tier grounds (S2).
3. **Gate: not a new instrument.** CG1–CG8 is an 8/8 relabel of the round-29 staged draft's Q1–Q8
   (which round 29 refused), with CG3 losing a dimension and CG6/CG8 re-pointed at the entry's own
   unadmitted table. The mechanism is published twice (CTC v1.1's validator; S166's CI gate) and
   priced nowhere in this round.

## Prior-art table (field / carrier / entry's status / verdict)

Carriers: round-6 tabulation (`benchmark-card-field-schema-2026-10-23.md:73-78`), the entry's own
cells (`:58-68`), and `SOURCES.md:107` (S081's row).

| # | Entry's field | Published design that carries it | Entry's status claim | Verdict |
|---|---|---|---|---|
| 1 | R3 contamination type tested (`:60`) | AI Alliance "Contamination controls"; CTC `contamination_controls` per-type `controlled`/`not_controlled`/`unknown`/`n/a`; GEM Decontamination | **already a column** | AGREE (restatement). Two fidelity losses: round-6's cell names the field `contamination_controls`, the entry's does not; round-6's row was "detector access / tier tested" (`:73`), so the access/tier dimension is no longer a field row (it survives only inside CG2/CG3). |
| 2 | grader integrity (`:61`) | AI Alliance "Grader evidence" (round-6 `:27`, `:78`) | **already a column**, and dropped from this entry | AGREE, and the drop is now **declared** with a lane pointer (`grader-perturbation-audit.md`). Earlier revision omitted the row silently; closed. Residual: `:45`'s "continued, not re-derived" now covers a table that is 6 of round-6's 6 rows plus 3 the round-6 table never had, with one row marked not-carried — a mapping, not a continuation. |
| 3 | "what a negative cannot rule out" (`:62`) | AI Alliance "their coverage, and known gaps"; CTC `unknown`/`not_controlled`; GEM Evidence Provided | **already a column** | AGREE. Count effect: round-6 describes the AI Alliance carrier as one field — "Checks performed, their coverage, and known gaps" — split here into rows 1 and 3, so the nine rows are not nine distinct published columns. |
| 4 | R2 elicitation budget (`:63`) | CTC `elicitation_budget`; GEM Reproducibility | **already a column** in two of three | AGREE (round-6 made the same dimension→field inference). |
| 5 | R5 instrument currency (`:64`) | AI Alliance "Release date", "Change log"; CTC `evaluation_date` | **already a column** in two of three | AGREE. |
| 6 | R4 regeneration status (`:65`) | S081 F4 (the staged draft's own attribution: "S081 F4"); the three designs carry `evaluation_date` / "Change log", already claimed by row 5 | **already a column**, narrower | MIS-ATTRIBUTED. "Narrower" asserts a regeneration field in those designs; they carry R5's date field. One CTC cell and one AI Alliance field are credited to two of the entry's fields each. Not new, wrong carrier. |
| 7 | S1 acquired contamination (`:66`) | **CTC v1.1 "type 5 recorded per run"** — the cell printed in this row; round-6 `:75` read that same cell as the carrier of the release-side-vs-score-side field; `SOURCES.md:107` used-by: "the card's release-side/score-side split and its five types are **this preprint's protocol, not the lane's design**" | **delta in placement, not in field** — "the run-side half exists only as the CTC form's type-5 row … not as a score-side record" (`:70-73`) | **UNSUPPORTED.** The reclassification needs S123's schema bytes; the cell it cites says "recorded per run", and round-6 read it as the split's carrier. "Per-type value inside the release-side form" and "not a score-side record" cannot both be read off "recorded per run". Honest status: **indeterminate pending S123**, not a delta. |
| 8 | S2 card integrity flag (`:67`) | CTC's `unknown`/`not_controlled` values (the entry cites that enum for row 3) — none of the three designs has a card-level state flag. Campaign prior art dated 2026-10-24: S165 verdict `PASS/NEUTRAL/FAIL/INCOMPLETE` failing closed on missing evidence; S166 CI gate failing any PASS without required provenance fields (`card-publication-contracts.md:21-31`); S173 computed completeness/repro gap (`card-completeness-and-verification.md:11-15`) | **delta in field** — a state for the card itself | **WEAK PASS against the three designs; FAIL as a round-level novelty statement.** The value vocabulary is CTC's; the mechanism is published in a file `lessons/round-30.md` §Gate records as **read and rejected** — rejected for tier (`build/R30DraftGate.md:30` tier-scans S167 only), content never priced. |
| 9 | R1 strata (`:68`) | **S081's four-field disclosure protocol** — "strata, elicitation budget, five types, regeneration … its JSON schema and validator" (`SOURCES.md:107` cell 6); the staged draft attributed R1 to "S081 F1"; the entry's own `:1` quotes S081's "strata reporting … registered in advance" | **delta** + "one new value set (R1's strata, which **no design tabulates** …)" (`:73-74`) | **FALSIFIED as written.** Two published protocols tabulate strata (S081's, which this entry's own source line quotes). True only as "no *one of the three tabulated* designs has a per-stratum scores column" — a scope the sentence never states, on a page that counts GEM's *proposal* as a published design. This is also the entry's one genuinely column-less field. |

Arithmetic of the current statement (`:70-77`): "one new field (S2), one new placement (S1), one new
value set (R1)". Membership is now defensible for S2 alone; S1 is a reinterpretation, R1 is a real
absence mis-stated as universal. So the count is not wrong any more — the *descriptions* are.

## Does the gate restate published answerability questions?

Extracted row-by-row from the entry (`:86-95`) and the round-29 staged draft
(`…/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md:53-60`; its
identical "S2 Card integrity" field at `:43`):

| CG | Same question as refused Q? | "Answerable from" | Verdict |
|---|---|---|---|
| CG1 | Q1, words only | S084/S086 (same) | restatement |
| CG2 | Q2, same four dimensions | S084/S086; the S077 canary pointer dropped (forced by the six-id predicate) | restatement, support narrower |
| CG3 | Q3 **minus a dimension** | S084 | loss: "Which **tier** and which datasets/subsets" → "Which datasets". §Extends claims round 24's *tier/access* vocabulary as its base, so the gate no longer asks the tier question that vocabulary exists for. |
| CG4 | Q4, words only | S084/S086 | restatement |
| CG5 | Q5, identical | S081 | restatement |
| CG6 | Q6, identical | **re-pointed** from "S081 F2" to "the union table's `elicitation_budget` column" | self-referential: the named artefact is the entry's own unadmitted table, so `:83` "Each CG question is answerable from a published artefact" is false as written |
| CG7 | Q7, words only | S083 (+ S085 added) | restatement plus one source |
| CG8 | Q8, identical | **re-pointed** from "S081 F4 and S082" to "the union table's … columns; S085's 2024 programme description" | self-referential **and invalid source**: `:118-120` says S085 has "no document number, no measurements, no data release"; it cannot answer "when was the instrument last regenerated" |

Instrument verdict: **neither a new instrument nor a renaming of the three designs' questions.** The
question list is the lane's own round-29 synthesis (8/8 identical, three rows reworded, no row
added), relabelled; the frontier instruction that already said "Q1–Q8" predates the round
(`git show 363a4eb:corpus/README.md:272`). The *mechanism* — required fields, an explicit
"unknown" answer, and a fail-closed state — is published in CTC v1.1's validator ("`unknown` is a
valid entry. So is `not_controlled`. Declare what you don't know", round-6 `:24-29`) and in S166's
publication gate. The round prices neither.

## Novelty-sentence inventory (does any sentence imply one? yes)

| Byte (f01b7cd2 snapshot) | Sentence | Status |
|---|---|---|
| entry `:70-77` | "one new field (S2's tri-state integrity flag), one new placement (S1 …), one new value set (R1's strata, which no design tabulates …)" | novelty assertion; two of three parts do not survive the table above |
| entry `:76-77` | "the earlier 'two new fields' reading counted a placement as a field" | good-faith self-correction — but it did not propagate (next two rows) |
| entry `:112-113` | "The two fields this entry adds are therefore the two its source measured as rare in practice" | **now internally inconsistent**: the file states three parts at `:70-77`; S081's two rare variables (strata, acquired) also cover {R1, S1}, not any pair that includes S2 |
| entry `:126-128` | falsifier: "the two delta fields are not rare in practice" | same stale count; and it tests rarity, not novelty, so it cannot catch the error beside it |
| entry `:41` vs `:54` | "its three source rows are not in this lane's registry" vs "the review this lane already registers at tier A" | **contradiction inside one section, and `:41` is false for GEM**: the lane holds the GEM 2026 review as **S001**, tier A, claim cell "…the Contamination Transparency Card" (`SOURCES.md:23`, same `2026.gem-main.50` paper). Consequence: the GEM column of the mapping *is* lane-checkable; only the AI Alliance and CTC columns rest on unadmitted bytes. |
| `README.md:274` | "gate a knowledge entry on Q1–Q8 (**the entry's own answerability questions**, labelled CG1–CG8 …)" | ownership claim for an 8/8 copy of the refused draft's questions; the entry itself never claims they are new |
| `README.md:65`, `:242`, `:275` | "plus the CG1-CG8 answerability gate"; "adds the CG1–CG8 answerability gate"; "supplies the card format and the CG1–CG8 gate" | delivered-instrument claims with no prior-art verdict, in tension with `plans/round-30-claims.md:94-96` ("adds no phenomenon or instrument claim") |
| `SOURCES.md:107` (used-by) | "the two fields the lane adds are the two its own source measured as rare in practice" | **stale against its own entry** (which now states three parts): the registry row now contradicts the file it names as its user |
| `lessons/round-30.md:46` vs `:49` | "six bullets including the two-delta-field concession" vs "the delta is stated as one field, one placement, one value set" | the closure record carries both the old and the new count |

Why nothing catches it: `corpus/QUALITY.md` has **no novelty or prior-art criterion**
(`grep -ni 'novelt\|prior art' corpus/QUALITY.md` → 0 hits), and the frozen non-claim covers
"phenomenon or instrument" only, so field- and value-set-level novelty is outside the scope of the
round's disclaimer. The SCORECARD proxy ("fraction of the round's headline claims carrying a
prior-art verdict with a fetched URL", `SCORECARD.md:47-48`) would score these claims unpriced. Across
the 35 build reports on disk, the only "prior art" hits are about S091 in
`benchmark-task-validity-checklist.md` (`R30DefectFix.md:208`, `R30RevDefects.md:186`) — nothing
prices prior art for this entry.

## What does not fail

- The **amendment framing is real**: no fourth design, no rival, no S122–S124 citation, six-id
  boundary held, round-6 named as the thing amended.
- **Restatement fidelity** on the carried rows is exact (R3's enum, row 3, R2, R5), the two GEM
  dimension→field inferences were inherited from round-6, and the grader-integrity drop is now
  declared with a reason.
- **S2 is a defensible weak delta** against the three tabulated designs.
- The **staged-file pin is honest** (sha256 recomputed, matches) and `:108-111`'s note that the
  compiled paper omits the quoted abstract sentence is a correct provenance refinement.

## Impacted axes

- **novelty** (primary): the round's novelty-shaped assertions are two-thirds unsupported and wholly
  unpriced; the honest statement is one column-less field (R1, per-stratum scores), one
  indeterminate placement question (S1) that CTC's own cell already records, and one composed state
  (S2) whose mechanism is published in `card-publication-contracts.md`.
- **coverage**: `SOURCES.md:107` used-by contradicts the entry's current text; `README.md:65/242/274-275`
  describe a delivered gate without a prior-art verdict and call the refused draft's questions the
  entry's own.
- **depth**: CG6/CG8 are unanswerable from lane bytes (`:83` false for them); a reader following
  `SKILL.md` alone cannot act on two of eight gate rows.
- **calibration**: `lessons/round-30.md:46` and `:49` record two different delta shapes for the same
  admission.
- Untouched: operability (C2/C3), adjacency, freshness; the six source quotes are other seats'.

## Smallest safe correction

1. Entry `:70-77` → keep the three-part shape but fix two descriptions: **S1** → "not new; CTC v1.1's
   type-5 row records it per run, and whether that record is score-side is unresolved without
   S123's schema (not opened)"; **R1** → "absent from all three *tabulated* designs; S081's protocol
   tabulates it (F1), so this is a column this lane's card adds, not a new value set".
2. Entry `:112-113` and `:126-128` → replace "the two fields this entry adds / the two delta fields"
   with the three-part wording, and attach S081's rare-variable warrant to R1 and S1 only.
3. Entry `:41` → "two of the three source rows are not in this lane's registry; the GEM review is
   held here as S001 (tier A)".
4. CG6/CG8 → S081 F2 / "S081 F4 and S082", or mark "not answerable from lane bytes"; CG3 → restore
   "tier" (its own §Extends claim depends on it).
5. Propagate to `SOURCES.md:107` used-by, `README.md:65/242/274-275`, `lessons/round-30.md:46,:49`;
   add one §What this does not establish bullet pricing CTC v1.1's validator and S166's CI gate as the
   instruments the gate restates, and name S165/S166/S173 as the prior art for S2's card-state flag.
