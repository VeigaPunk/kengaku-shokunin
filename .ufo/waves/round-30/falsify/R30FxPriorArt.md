# R30FxPriorArt — restatement or novelty overclaim in the round-30 card entry

Seat: `L1Kengaku30.R30FxPriorArt-3`, critic. Scope: prior art, the "exactly two fields are
new" claim, the CG1–CG8 gate's instrument status, and the round's non-claim. No lane bytes
written except this file. Nothing installed.

Candidate: `corpus/knowledge/contamination-transparency-card.md`
VERDICT: FAIL — the "exactly two fields are new as *fields* (S1, S2)" sentence is falsified by the entry's own CTC v1.1 cell for S1 and by the round's own wave-1 review (which put the honest delta at one field, R1); CG1–CG8 is an 8/8 relabel of the refused round-29 Q1–Q8, not a new instrument, and S2's card-state mechanism is published in the campaign file this round read and rejected.

Byte basis (read-only): lane HEAD `363a4eb`; the entry is **untracked** (`git ls-files` →
"did not match any file(s) known to git"), so every line anchor below is a working-tree read,
pinned to `contamination-transparency-card.md` sha256
`28f5bbda7dcbad01c8018288b425923ed76007e0c6846e642ff7dc75b37e687e`, mtime 2026-10-25
04:42:01 -0300, 15947 B. The file changed under me mid-review (an earlier working-tree read
still carried the sentence "the field mapping and the delta are the contribution", now gone);
a later peer edit moves line numbers, not the finding. Lane-side companions pinned at
`corpus/README.md` `9392efdb…`, `corpus/SOURCES.md` `ffb4165b…`, `corpus/lessons/round-30.md`
`e63ea920…`. Campaign file at the entry's own path recomputes to the entry's stated sha256
`66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9` — the pin is honest.

## Bottom line

1. **The restatement is mostly honest; the novelty sentence is not.** Seven of eight field rows
   are mapped into the round-6 columns and two are marked new. Of those two, S1 is carried by a
   published design *in the entry's own row*; the one field that is genuinely absent from all
   three designs (R1, per-stratum scores) is demoted out of the field count.
2. **The gate is not new.** CG1–CG8 corresponds 8/8 to the round-29 staged draft's Q1–Q8, which
   round 29 refused; three rows lose content relative to that draft; two rows are re-pointed from
   their sources at the entry's own unadmitted table.
3. **"No novelty credit" does not reach the sentences that take credit.** The frozen non-claim
   (`plans/round-30-claims.md:94-96`) covers "phenomenon or instrument" only. The entry's field
   and value-set novelty assertions sit outside its scope, and no round-30 byte prices them: `grep
   -i 'prior art'` over all 36 build reports returns nothing for C1.

## Prior-art table

Carriers are named from the round-6 tabulation
(`benchmark-card-field-schema-2026-10-23.md:74-79`), the entry's own cells (`:57-66`), and the
entry's registry row (`SOURCES.md:107`).

| # | Entry's field (`:57-66`) | Published design that carries it | Entry's status claim | Verdict |
|---|---|---|---|---|
| 1 | R3 contamination type tested | AI Alliance "Contamination controls"; CTC v1.1 per-type `controlled`/`not_controlled`/`unknown`/`n/a`; GEM Decontamination | **already a column** | AGREE (restatement). Two fidelity losses: round-6's cell named the field `contamination_controls` and the entry's cell does not; round-6's row was "detector access / tier tested", so the access/tier dimension is no longer a field row (it survives only inside CG2/CG3). |
| 2 | "what a negative cannot rule out" (no field id) | AI Alliance "their coverage, and known gaps"; CTC `unknown`/`not_controlled`; GEM Evidence Provided | **already a column** | AGREE. Note the count effect: round-6 describes the AI Alliance carrier as one field — "Checks performed, their coverage, and known gaps" (`:18-20`) — split here into rows 1 and 2, so the 8-row list is not 8 distinct published columns. |
| 3 | R2 elicitation budget | CTC `elicitation_budget`; GEM Reproducibility | **already a column** in two of three | AGREE (round-6 made the same dimension→field inference). |
| 4 | R5 instrument currency | AI Alliance "Release date", "Change log"; CTC `evaluation_date` | **already a column** in two of three | AGREE. |
| 5 | R4 regeneration status | **S081 F4** (the staged draft's own attribution: "S081 F4"); the three designs carry `evaluation_date` / Change log, which row 4 already claims | **already a column**, narrower | MIS-ATTRIBUTED. "Narrower" asserts a regeneration field exists in those designs; they carry the update-date field, i.e. R5's carrier. R4 is not new, but its carrier is a protocol the table's columns exclude. One CTC cell (`evaluation_date`) and one AI Alliance field ("Change log") are now credited to two of the entry's fields each. |
| 6 | S1 acquired contamination | **CTC v1.1 "type 5 recorded per run"** — the entry's own cell — and S081's protocol: `SOURCES.md:107` used-by cell reads "the card's release-side/score-side split and its five types are **this preprint's protocol, not the lane's design**"; round-6 `:76` mapped the same field to the same CTC cell | **delta** — the run-side half | **FALSIFIED.** A published design carries it in the same row the entry wrote. By the entry's own vocabulary ("already a column in two of three", `:61-62`) this is "already a column in one of three", not a delta. The only defensible residual — a per-run record promoted to a *card field* — is narrower than the row claims and is never stated. |
| 7 | S2 card integrity flag | CTC's `unknown`/`not_controlled` enum (the entry cites that enum for row 2); campaign prior art dated 2026-10-24: S165's card verdict `PASS/NEUTRAL/FAIL/INCOMPLETE` failing closed on missing evidence, S166's CI gate that "fails any card publishing a PASS that does not record" required fields (`card-publication-contracts.md:21-31`), S173's computed completeness/repro-gap signal (`card-completeness-and-verification.md:11-15`); the lane's own refused draft already had "S2 Card integrity" | **delta** — a state for the card itself | WEAK PASS against the three tabulated designs only (none has a card-level state flag); **FAIL as a round-level novelty statement**: the value vocabulary is CTC's and the mechanism (a fail-closed state + required-field check) is published in `card-publication-contracts.md`, which `lessons/round-30.md` §Gate records as **read and rejected** — rejected on Q2 tier grounds (`build/R30DraftGate.md:30` tier-scans only S167), with its content never priced as prior art. |
| 8 | R1 strata | **S081 F1** ("strata", `SOURCES.md:107` cell 6); the staged draft attributed R1 to "S081 F1"; the entry's own source line quotes S081's "strata reporting … registered in advance" (`:1`) | **delta** — "one is new as a *value set* (R1's strata, which **no design tabulates** …)" (`:68-69`) | **FALSIFIED as written.** S081 publishes a "four-field contamination disclosure protocol (strata, elicitation budget, five types, regeneration), its JSON schema and validator" (`SOURCES.md:107`). True only as "none of *the three tabulated* designs has a per-stratum scores column" — a scope the sentence never states, while the same page counts GEM's *proposal* as a published design. This is also the one genuinely column-less field, and the count excludes it from "fields". |
| 9 | *(row absent)* grader integrity | AI Alliance "Grader evidence" — round-6 `:27` and `:78`, the field round-6 singles out as already published | not present | **OMISSION against `:45` "The union table is continued, not re-derived".** Four of round-6's six rows are carried (rows 1–4 above, with row 1 relabelled); "detector access / tier tested" is relabelled and "grader integrity" is dropped. Dropping a published column while claiming continuation is a Q6 overwrite by omission, and it raises the apparent new-field fraction (2/8 rather than 2/9). |

## The count sentence, three independent falsifiers

`:68` "So exactly two fields are new as *fields* (S1, S2), one is new as a *value set* …"

1. **Its own cells.** S1's CTC cell is `type 5 recorded per run` (`:64`) — a column. A table whose
   Status vocabulary says "already a column" cannot also say delta for a row whose column is filled.
   3 rows carry `**delta**` (`:64-66`), so a reader counting the table's own labels gets three.
2. **The round's own wave-1 review.** `build/R30RevFlip.md:173-188` (rule D-c) lists
   "release-vs-score, elicitation budget, instrument currency, **card integrity**" as fields that
   "already have columns", and prescribes verbatim: "exactly one staged field has no column — `R1
   Strata` … So the honest delta statement is **one field plus one instrument**, with the rest
   mapped." The landed entry marks exactly those two named-as-column fields as the new ones and
   demotes R1 to a value set. No reason is given for inverting the review; `lessons/round-30.md`
   §Gate then records the inverted count as the admission's basis.
3. **A warrant attached to the wrong pair.** `:102-107`: S081's rare variables are "strata reporting
   and the acquired type", which the entry maps to "R1 (strata) and S1/S2 (acquired / integrity)",
   and concludes "The two fields this entry adds are therefore the two its source measured as
   rare". The warrant covers {R1, S1}; the count's membership is {S1, S2}; S2 is not one of S081's
   two rare variables. The sentence is true only if "two" means {R1, S1} — which contradicts `:68`.
   `SOURCES.md:107` used-by cell repeats the same conflation, so the false statement is now inside
   a registry row later rounds will cite as the source's `used-by`.

Verifiability: the eight "already a column" cells can only be checked against the staged file, and
`:40-42` declares that file unadmitted and "no load-bearing claim here rests on it" — contradicted
by `:117-119` ("The field mapping is not lane-sourced … this entry's reading of that document") and
by the fact that the novelty count is read off it. `R30ConnCorpus.md` D-f (eight cells asserting
positive facts about designs whose tables are not in the lane) was not softened; the entry added a
sha256 and a label, which repairs provenance, not checkability.

## The gate: relabel of a refused draft, not a new instrument

Extracted row-by-row from the entry (`:80-93`) and the staged draft
(`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md:51-60`):

| CG | Same question as refused Q? | "Answerable from" | Verdict |
|---|---|---|---|
| CG1 | Q1, words only | S084/S086 (same) | restatement |
| CG2 | Q2, same four dimensions | S084/S086; the S077 canary pointer dropped (forced by the six-id predicate) | restatement, support narrower |
| CG3 | Q3 **minus a dimension** | S084 | restatement with loss: "Which **tier** and which datasets/subsets" → "Which datasets". The entry's own §Extends says it builds on round 24's *tier/access* vocabulary, so the gate no longer asks the tier question that vocabulary exists for. |
| CG4 | Q4, words only | S084/S086 | restatement |
| CG5 | Q5, identical | S081 | restatement |
| CG6 | Q6, identical | **re-pointed** from "S081 F2" to "the union table's `elicitation_budget` column" | self-referential: the named artefact is the entry's own staged table, so `:77` "Each CG question is answerable from a published artefact" is false as written |
| CG7 | Q7, words only | S083 (+ S085 added) | restatement plus one source |
| CG8 | Q8, identical | **re-pointed** from "S081 F4 and S082" to "the union table's … columns; S085's 2024 programme description" | self-referential **and invalid source**: `:112-114` says S085 has "no document number, no measurements, no data release"; it cannot answer "when was the instrument last regenerated" |

Verdict on instrument status: **not a new instrument, and not a renaming of the three published
designs' questions either.** The question list is the lane's own round-29 synthesis (8/8 identical),
relabelled; the frontier instruction that named "Q1–Q8" predates this round
(`git show 363a4eb:corpus/README.md:272`). The *mechanism* is published twice: CTC v1.1 ships a
validator with `unknown`/`not_controlled` as valid answers (round-6 `:24-29`: "so a card that says
'we did not test this' is a *complete* card") and S166 makes publication "a CI check" that fails on
absent required fields. Nothing in the round prices either as the gate's prior art.

## Does any sentence imply novelty? Yes — three in the entry, one in the index, one in the registry

| Byte | Sentence | Status |
|---|---|---|
| entry `:68-69` | "exactly two fields are new as *fields* (S1, S2), one is new as a *value set* (R1's strata, which no design tabulates …)" | novelty assertion; composition falsified (S1), scope unstated (R1) |
| entry `:71` | "That is what an amendment looks like; a design would have claimed all eight." | comparative novelty framing resting on the falsified count |
| entry `:105-107` | "The two fields this entry adds are therefore the two its source measured as rare in practice." | addition claim with a mis-scoped warrant (see falsifier 3) |
| entry `:120-123` | falsifier tests whether "the two delta fields" are populated | repeats the count; tests rarity, not novelty, so it cannot catch the error it sits beside |
| `README.md:274` | "gate a knowledge entry on Q1–Q8 (**the entry's own answerability questions**, labelled CG1–CG8 …)" | ownership claim for an 8/8 copy of the refused draft's questions |
| `README.md:65`, `:242`, `:275` | "plus the CG1-CG8 answerability gate"; "adds the CG1–CG8 answerability gate"; "supplies the card format and the CG1–CG8 gate" | delivered-instrument claims with no prior-art verdict, in tension with `plans/round-30-claims.md:94-96` ("adds no phenomenon or instrument claim") |
| `SOURCES.md:107` (used-by) | "the two fields the lane adds are the two its own source measured as rare in practice" | the falsified count is laundered into the registry |
| `lessons/round-30.md` §Gate | "declaring the delta (S1, S2 fields; R1's value set)" | closure record repeats an unreproduced count — calibration, not style |

The non-claim is honest as far as it goes but is **narrower than the sentences that take credit**:
it disclaims "phenomenon or instrument" novelty while the entry asserts field- and value-set-level
novelty. `corpus/QUALITY.md` has no novelty or prior-art criterion at all (`grep -ni
'novelt\|prior art' corpus/QUALITY.md` → 0 hits), so nothing in the admission bar can catch this;
the SCORECARD's novelty proxy ("fraction of the round's headline claims carrying a prior-art verdict
with a fetched URL", `SCORECARD.md:47-48`) would score these claims 0/unpriced.

## What does not fail

- The **amendment framing is real**: no fourth design, no rival, no S122–S124 citation, the six-id
  boundary held, and the round-6 file is named as the thing amended.
- **Restatement fidelity** on the four rows it carries is exact (R2, R5, R3's enum, row 2), and the
  borderline GEM dimension→field mappings were inherited from round-6, not invented.
- **S2 is defensible as a weak delta** against the three designs (no card-level state flag there);
  the failure is that the round files it as one of two *new* fields and prices no prior art when the
  mechanism is published in a file it read.
- The **staged-file pin is honest** (sha256 recomputed and matching), and `:102-104`'s new caveat
  that the compiled paper omits the quoted abstract sentence is a correct provenance refinement.

## Impacted axes

- **novelty** (primary): the round's only novelty-shaped assertion is false in composition and
  unpriced; the honest count is one column-less field (R1) plus one composed state (S2), with S1
  priced to CTC v1.1 and S081.
- **coverage**: `SOURCES.md:107` and `README.md:65/242/274-275` carry the claim forward; a coverage
  row that "adds a gate" without a prior-art verdict is a covered surface whose contribution is
  mis-described.
- **depth**: CG6 and CG8 cannot be answered from lane bytes, so a reader following `SKILL.md` alone
  cannot act on two of the eight gate rows.
- **calibration**: `lessons/round-30.md` §Gate records the inverted count as the admission's basis.
- Untouched: operability (C2/C3), adjacency, freshness; the six source quotes are other seats'.

## Smallest safe correction

One sentence replaces the count, then four surfaces follow it:

1. Entry `:68-71` → "Only R1's per-stratum scores column is absent from all three tabulated designs.
   S1's run-side record is CTC v1.1's type-5-per-run column plus S081's filing rule; S2 is a
   card-level state composed from CTC's existing `unknown`/`not_controlled` values, a mechanism
   published in `card-publication-contracts.md` (S165/S166) and scored by S173."
2. Entry `:105-106` → attribute S081's rare-variable warrant to the fields it actually covers (R1's
   strata, S1's acquired type), and drop S2 from that warrant.
3. CG6/CG8 "Answerable from" → S081 F2 / "S081 F4 and S082" (the staged draft's cells), or mark
   "not answerable from lane bytes"; CG3 → restore "tier", since §Extends claims round 24's tier
   vocabulary as its base.
4. `:45` "continued, not re-derived" → "four of six rows carried; grader integrity is dropped here
   and noted as unmapped"; restore it as a row if the union is meant to be complete.
5. Propagate the corrected sentence to `SOURCES.md:107` used-by, `README.md:65/242/274-275`, and
   `lessons/round-30.md` §Gate; add one §What this does not establish bullet naming CTC v1.1's
   validator and S166's CI gate as the published instruments the gate restates.

Cheapest alternative if the writer keeps S2 as a delta: delete "exactly two" and state the three
different statuses (absent from all three / present in one of three / composed from an existing
enum). That alone removes the falsified sentence without touching any mapping cell.
