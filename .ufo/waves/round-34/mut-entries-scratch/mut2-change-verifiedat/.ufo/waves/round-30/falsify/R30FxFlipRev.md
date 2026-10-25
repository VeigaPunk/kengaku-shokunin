# R30FxFlipRev — did the landed entry actually discharge round 29's two flip loci?

Seat `L1Kengaku30.R30FxFlipRev-3` (leaf, revenger, falsify wave). Read at **2026-10-25T07:41Z**.
Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No lane byte written except this report; no
task spawned, no background job, no runtime invoked against the lane's gates. Tool installs/upgrades:
**none** (python3, git, curl were already present; no pacman transaction was attempted, host guard
respected).

Method disclosure: **no `lsp` device is mounted in this session** — `read xd://lsp` returns
"No such tool: xd://lsp". Every locator below is therefore a literal read, a `git` object read, a
recomputed count or a fetch whose command and output appear here. Nothing below is presented as
semantic (call-graph) proof; where I reason past the bytes it is marked `[INFERENCE]`.

What I actually ran, so a re-runner can red-anything I claim:

| # | command | result |
|---|---|---|
| R1 | `git rev-parse HEAD` | `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db` = the baseline `plans/round-30-claims.md` names |
| R2 | `git status --porcelain` | every round-30 byte is untracked or modified: `?? corpus/knowledge/contamination-transparency-card.md`, `?? corpus/lessons/round-30.md`, `?? .ufo/waves/round-30/`, `M corpus/README.md`, `M corpus/SOURCES.md`, `M corpus/QUALITY.md` |
| R3 | `git show 363a4eb:corpus/README.md \| sed -n '274p'` | frontier bullet ends "…draft a card template and gate a knowledge entry on **Q1–Q8**." with no disambiguation |
| R4 | `curl …caict.ac.cn…/P020240711534708580017.pdf` | **HTTP 200, 1949572 bytes** — the size the round-30 lesson records |
| R5 | count recomputation (`len(span.split())`, codepoints) over the landed entry and the round-30 Sources table | see §3 table; two lesson cells and one entry cell do not reproduce |
| R6 | `ls .ufo/waves/round-30/falsify/` | `R30FxDeadSeats.md`, `R30FxSrcS082.md`, `swarm-registry.json` — **no `FxEntryCompleteSet.md`** |
| R7 | `grep -o "S0[0-9][0-9]" corpus/knowledge/contamination-transparency-card.md \| sort \| uniq -c` | S081×9 S082×5 S083×3 S084×6 S085×8 S086×7 — exactly six distinct ids, no seventh |

---

## 1. The two loci, reconstructed from round-29 bytes

Round 29 recorded the card's refusal **twice, on different axes**. Both are operative; the entry
must meet both, and the round-30 lesson claims it met both in one commit.

**Locus 1 — the amendment-vs-rival flip** (`corpus/lessons/round-29.md:241-243`), decided by the
refusal at `:223-227`:

> `contamination-transparency-card.md` — reject on scope (QUALITY Q6): it offers a fourth card
> design where the campaign's own round 6 tabulated three published designs and ruled this file an
> amendment, not a rival (…). Secondary: all six sources carry the campaign's `2026-10-23` opened
> date and none was re-opened this round.
>
> Flip conditions: re-open the cited sources in a later round; **for the card, land it as an
> amendment to the tabulated designs rather than a new design**; for the grader entry, cite the
> corrected 16/108 tabulation and a well-formed row.

**Locus 2 — the one-theme / Q1–Q8 flip** (`corpus/lessons/round-29.md:180`, attempt-2 Gate):

> | `contamination-transparency-card.md` (S081–S086) | reject this round | a second frontier
> instrument (contamination cards), not the round's one theme; six sources including two PDF hosts
> and one CAICT host that returned HTTP 000 on a first fetch were not re-opened this round |
> **open S081–S086 in a later round as its own theme and pass QUALITY Q1–Q8 then** |

Two properties of that second sentence matter and are easy to lose: the flip names the file
`QUALITY` and the range `Q1–Q8` (`corpus/QUALITY.md:15-63`, under the heading at `:10`, the lane's
*admission bar*), and it
bundles a second conjunct that has nothing to do with the amendment relation.

**What round 30 claims.** `corpus/lessons/round-30.md` §Gate:

> Both flip loci in `corpus/lessons/round-29.md` are discharged in one commit: the `:227`/`:241-243`
> flip (amendment, not a rival design) and the `:180` attempt-2 Gate flip (open S081–S086 as this
> round's one theme and pass the admission bar).

and, in the same table's reason cell for the admitted package:

> the design-vs-rival flip is met by mapping every field into the round-6 union table's own columns
> and declaring the delta (S1, S2 fields; R1's value set) instead of presenting a format; all six
> cited sources re-opened 2026-10-25 with ≤25-word located quotes; Q1 triad rebuilt

Note two edits the lesson's gloss performs, before any evidence is weighed: `:227` (the
2026-10-23 *opened-date* clause) is folded into "the amendment, not a rival design" flip, and
`:180`'s named "QUALITY Q1–Q8" becomes "the admission bar". Neither edit is stated as an edit.

---

## 2. Locus 1 — is "amendment" carried by the field mapping, or by the label?

The test is not the heading. `corpus/knowledge/contamination-transparency-card.md` carries the
staging campaign's union table (`benchmark-card-field-schema-2026-10-23.md:71-78`, read-only in
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/`):

```
| Lane's proposed field | AI Alliance template | CTC v1.1 form | GEM § 7 Table 3 |
| detector access / tier tested | "Contamination controls" | `contamination_controls` (per-type …) | Decontamination |
| what a negative cannot rule out | "their coverage, and known gaps" | `unknown` / `not_controlled` are valid entries | Evidence Provided |
| release-side vs score-side | (not present) | type 5 recorded per run | — |
| elicitation budget | (not present) | `elicitation_budget` | Reproducibility |
| instrument currency | "Release date", "Change log" | `evaluation_date` | — |
| grader integrity | "Grader evidence" | — | — |
```

and that file's own conclusion, three lines later (`:80-83`):

> Two fields the lane's own card proposal had as first-class — **grader evidence** and
> **elicitation budget** — appear in *different* published designs, and the union of the three is
> strictly larger than any one of them. The lane's card should now be written as an amendment to
> these three, not as a rival.

### 2a. The relation is genuinely in the cells — this is not a label

I compared the landed table cell by cell against that table rather than taking the Status column:

| landed row | staging row it reproduces | cells | verdict |
|---|---|---|---|
| R3 contamination type tested | row 1 (detector access / tier tested) | "Contamination controls" ✓, per-type value set ✓, Decontamination ✓ | faithful (the left-hand field is renamed; see 2d) |
| "what a negative cannot rule out" | row 2 | "their coverage, and known gaps" ✓, `unknown`/`not_controlled` ✓, Evidence Provided ✓ | faithful |
| R2 elicitation budget | row 4 | (absent) ✓, `elicitation_budget` ✓, Reproducibility ✓ | faithful |
| R5 instrument currency | row 5 | "Release date", "Change log" ✓, `evaluation_date` ✓, (absent) ✓ | faithful |
| S1 acquired contamination | **row 3** (release-side vs score-side) | (absent) ✓, **`type 5 recorded per run`** ✓, (absent) ✓ | **cells faithful, Status flipped to `delta`** |
| R4 regeneration status | none | Change log / `evaluation_date` / Reproducibility | new row, labelled "already a column, narrower" |
| S2 card integrity flag | none | (absent) / `unknown`,`not_controlled` / (absent) | new row; its CTC cell is row 2's own value set |
| R1 strata | none | (absent) / (absent) / (absent) | the only row absent from all three designs |

Four of the five shared rows are cell-for-cell what the staging table says, and §Extends names both
objects the flip required (the round-24 lane entry and the round-6 tabulation). So the amendment
relation **is** carried by the mapping: a reader can point at the design each field came from. On
that half, locus 1 is met.

### 2b. The delta arithmetic is contradicted by the table it maps into

The entry's decisive contribution sentence:

> So **exactly two fields are new as *fields* (S1, S2)**, one is new as a *value set* (R1's strata,
> which no design tabulates and whose own source records the lane's first failure with it), and the
> rest are this entry's names for columns those designs already carry. **That is what an amendment
> looks like; a design would have claimed all eight.**

S1's row reproduces the staging table's `release-side vs score-side` row, whose CTC column is
`type 5 recorded per run`. Under the entry's **own** Status semantics that row cannot be a delta:
the entry labels R2 "already a column **in two of three**" and R5 "already a column in two of
three", i.e. presence in two designs is still "already a column"; S1 is present in one (CTC) and is
called a delta. Run the same rule consistently and S1 is "already a column in one of three". S2 is
weaker still: its only populated cell is `unknown`/`not_controlled`, which is row 2's own value set,
so it is a *state* of columns the table already lists, not a field absent from all three.

This is not a hostile reading invented after the fact. The build wave filed the criterion before
the entry existed — `build/R30RevFlip.md` §(c), item **D-c**:

> **D-c** any field that is already a column of E6 is claimed as the amendment's new content
> (release-vs-score, elicitation budget, instrument currency, card integrity all have columns);

with the operational consequence stated in the same report:

> So the honest delta statement is one field plus one instrument, with the rest mapped.

The landed entry does the opposite: it declares **two** new fields (S1, S2) and demotes the one row
that has no column (R1) to "a value set". Under the round's own pre-filed D-c, "release-vs-score …
claimed as the amendment's new content" is one of the enumerated conditions under which the entry
is *still the fourth design*. The entry does not merely overstate; it overstates in the exact
direction the flip was written against.

The overstatement also breaks the entry's internal consistency. §What this does not establish
says of S081's below-threshold pair:

> that is R1 (strata) and S1/S2 (acquired / integrity) in this entry's own naming. **The two fields
> this entry adds are therefore the two its source measured as rare in practice.**

There, the two added fields are R1 **and** S1 (with S2 fudged in by the slash); in the mapping
table they are S1 **and** S2, with R1 demoted. S081's quoted sentence names exactly two rare
variables — "strata reporting and the acquired type" — i.e. R1 and S1. The entry cannot be right on
both surfaces: either R1 is a field (then the mapping table undercounts) or it is a value set (then
§What this does not establish overcounts). `[INFERENCE]` the writer wanted "two" in both places and
let the composition of the pair drift.

### 2c. One union-table row is dropped without a word

`grader integrity → "Grader evidence"` (staging row 6) appears nowhere in the landed table, although
the staging file names it one of the two fields that made the union "strictly larger than any one"
of the designs. §Extends says the union table is "continued, not re-derived"; a continuation that
drops a row is a re-partition. It may well be the right call for a card about contamination — but
the entry owes the sentence that says so, because the dropped row is the staging file's own headline
evidence.

### 2d. The mapping's cells have no lane-side evidence, and one of them could

The entry says of the three designs: they are "**not** in this lane's `corpus/knowledge/`, and its
three source rows are not in this lane's registry." True for the campaign ids (S122/S123/S124). But
S124 in the staging file is `https://aclanthology.org/2026.gem-main.50.pdf` — the same paper the
lane registers at **tier A as S001** (`corpus/SOURCES.md:23`, claim cell: "…the Contamination
Transparency Card"). So one of the three columns (GEM § 7 Table 3) has a lane-registered,
tier-A row that the entry does not cite, while the claim "its three source rows are not in this
lane's registry" reads as though none of them is. Two consequences: the GEM column's Q2 scope
("for that claim's scope") was satisfiable and was not taken; and the sentence as written is true of
the ids and misleading about the sources.

For the AI Alliance template and the CTC v1.1 YAML there is no in-lane row, and the entry's own
words make the mapping table — "the field mapping and the delta are the contribution" — the one
load-bearing claim in the entry whose evidence is outside the registry. That is the headline of the
build wave's connector report as well (`build/R30ConnCorpus.md` D-a, D-f), and it is the fact that
makes locus 2's Q2 verdict fail (below).

### Locus 1 verdict

**Relation: discharged. Arithmetic: not discharged.** The entry is no longer the fourth design in
form — the mapping is real, cell-faithful and named in both directions. But the one sentence that
states what the amendment *adds* claims two new fields where its own source table supports at most
one, which is the condition the round's pre-filed criterion treats as "still the fourth design".
The distance is one Status cell and one sentence, not a rewrite; but as landed, the claim
"both flip loci are discharged" is not true of these bytes.

---

## 3. Locus 2 — one theme, and the Q1–Q8 collision

### 3a. Clauses that are genuinely discharged

| clause of `:180` | evidence I re-derived | verdict |
|---|---|---|
| "as its own theme" | the card is the round's only admitted knowledge theme; the other staged entries are rejected on theme/scope in the same Gate, and Q20 is a criteria edit, not a knowledge admission | **met** |
| "open S081–S086 … re-opened" | all six registry rows read `mined \| 2026-10-25 \| 180d \| corpus/knowledge/contamination-transparency-card.md` (R7-adjacent read of `corpus/SOURCES.md`). The named blocker — CAICT HTTP 000 — is cleared: my own fetch returned **200 / 1949572 B**, byte-count identical to the lesson's figure | **met, re-run by me** |
| ≤25-word located quotes | re-counted: S081 22/6/18, S082 11/17, S083 14/19, S084 3/7/1 tokens, S086 3/1 — all ≤25 whitespace tokens (CJK caveat below) | **met** |
| header completeness (the staged text's seventh id) | id census: six distinct ids, no S077 and no other id anywhere (R7) | **met** |
| label move off `Q1–Q8` | entry gate is CG1–CG8; `corpus/README.md:274` gained "(the entry's own answerability questions, labelled **CG1–CG8** … so they cannot be confused with `QUALITY.md` Q1–Q8)" — absent at baseline (R3) | **met** |

### 3b. The clause that is not: "pass QUALITY Q1–Q8"

The collision is not resolved; it is renamed and then declared resolved.

- Round 29 demanded a pass on `QUALITY.md` Q1–Q8 — the *admission bar* (triad, tier floor, quote
  containment, negative space, source labelling, extends, same-commit landing, rejections kept).
- The landed entry supplies CG1–CG8, and its own opening line says what they are: "The eight
  questions are labelled **CG1–CG8** here so they cannot be confused with `QUALITY.md` Q1–Q8, which
  are this lane's *admission* criteria." That is a correct diagnosis of the collision — and an
  admission that CG1–CG8 are a *different* set of questions ("Which contamination type is claimed?",
  "What access did the reporter have?") from the admission criteria ("Does the triad open the
  entry?", "Does each load-bearing claim rest on a tiered row?").
- Answering the card's eight questions therefore says nothing about the admission bar. The lesson's
  paraphrase — "pass the admission bar" — replaces the named clause without showing it, and no
  seat in the build wave re-scored the landed entry against `QUALITY.md` Q1–Q8: `R30RevEntryQ1Q6.md`
  grades the **staged** object (`verified-at: 2026-10-23`, `extends`→0 hits, no negative-space
  section) and explicitly does not transfer; `R30RevEntryQ7Q9.md` and `R30RevGate.md` contain no
  Q1–Q8 verdict for the landed entry (`grep` for `flip|locus|loci|amendment` in `R30RevGate.md` →
  no match).

`corpus/QUALITY.md:12-13` is not a style preference: "An entry is admitted only when every row below
passes; **the round lesson's `## Gate` records the pass/fail per entry** and every rejected
candidate." Round 29's final Gate did exactly that ("Q1–Q6 and Q10 confirmed … Q7/Q8 through
same-tree index/coverage"). Round 30's Gate records three clauses of one Q and nothing else. So even
if every Q passed, the flip's second conjunct would be *unrecorded*.

I ran the missing score myself against the landed bytes, so the next seat does not have to:

| Q | basis (landed bytes) | my verdict |
|---|---|---|
| Q1 triad | six `source:` lines then `verified-at: 2026-10-25`, `recheck: 180d` + action + `2027-04-23` (=+180d, checked), `writer:`; multi-source-line shape is the lane's admitted precedent | **pass** |
| Q2 tier floor | S081 B, S082 B, S083 A, S084 A, S085 B, S086 A — no tier C, no `community`, every source-scoped claim has a B-or-better row. **But** the mapping claim ("already a column", the entry's own "the field mapping and the delta are the contribution") rests on S122–S124, which are not in `SOURCES.md`; the GEM column *is* in-lane as S001 and is uncited | **fail for that claim's scope** |
| Q3 quote containment | the six sources are anchored ≤25 tokens; the mapping's ~14 status cells are unquoted assertions about three designs; §What this does not establish relies on S081's κ/0.84 behaviour with no anchored quote for the numbers | **pass for the six; owed for the mapping cells and the κ caveat** |
| Q4 negative space | §What this does not establish, six bullets, explicit **Falsifier:**, and it does *not* launder S081's below-threshold pair | **pass** |
| Q5 labelling | §Attribution labels S081/S082 preprints, S083 and S086 peer-reviewed, S084 vendor self-description, S085 a self-report "about its own benchmark programme" | **pass** |
| Q6 extends | §Extends names the round-24 entry and the tabulation; README index `:65` and coverage `:242` rows name it as an amendment | **pass** |
| Q7 same-commit landing | **nothing is committed**: HEAD is the round-30 baseline and every entry/README/SOURCES/wave byte is untracked or modified (R1, R2) | **pending, not passed** |
| Q8 rejections kept | entry §Rejected (three items with flips) + the Gate's six reject rows | **pass** |

So the admission bar would pass 6 of 8 on these bytes, fail one (Q2, mapping), and await one (Q7).
That is a materially different record from "both flip loci are discharged", and it is the record
`QUALITY.md` asks the lesson to carry.

### 3c. Two receipt defects inside the same claim

1. **The cited Q10 second seat does not exist.** The lesson's §Round 30 admission says: "Q10 second
   seat: `.ufo/waves/round-30/falsify/FxEntryCompleteSet.md` (a `reviewer` seat that did not write
   the entry re-opened all six sources and re-derived every number)". At 07:41Z that file is absent;
   `falsify/` holds only `R30FxDeadSeats.md`, `R30FxSrcS082.md` and `swarm-registry.json` (R6). A
   peer seat is live on that file, so this may close during the wave — the defect is that the
   lesson asserts a returned report in the past tense before it returned. `gate_timing_check.py`
   fails exactly this case (red variant "absent from commit tree", exit 1, per
   `build/R30Q13Check.md` §4).
2. **The Q13 line stores an unrun command.** `Q13 check: python3 plans/gate_timing_check.py
   --lesson corpus/lessons/round-30.md --commit <admitting sha>` — the placeholder is a command no
   one can run, recorded in the past tense of a check. Q13 is unproven by the lesson's own text.

### 3d. CG2 lost the source it needs (a regression from the staged text)

The staged Q2 cited "S084 …, S086 …, S077 (canary, per task)". The landed CG2 asks "What access did
the reporter have — parameters only, the training corpus, a public index, **a canary**?" and answers
from S084 and S086 only. S077 was removed from the body to satisfy C1's six-id equality (the build
wave's own recommendation, `R30RevFlip.md` item 1), but the removal took the *cross-reference* with
it: two of the four access levels CG2 names are now unanswerable from any source in the entry, and
CG2 itself says "Each CG question is answerable from a published artefact". This is a small, fully
mechanical debt — one clause pointing at `knowledge/benchmark-task-validity-checklist.md`, which
holds the lane's canary bytes — and it was named in the build wave (`R30ConnCorpus.md` D-e).

### Locus 2 verdict

**Theme, re-open, quote, header-completeness and the label move: discharged** — and I verified the
one clause round 29 was blocked on by re-fetching the CAICT PDF myself (200 / 1949572 B).
**"Pass QUALITY Q1–Q8": not discharged** — not recorded anywhere, not re-scored by any seat against
the landed bytes, and not fully passable as written (Q2 fails for the mapping claim; Q7 awaits a
commit). The collision is disambiguated, which is a real improvement and the right first move; it is
not resolved, because the admission bar was never run against the object that landed.

---

## 4. What the entry still owes (each with the observation that proves it fixed)

| # | owed item | proves it |
|---|---|---|
| 1 | Correct the delta arithmetic: S1's Status cell becomes "already a column in one of three" (staging row 3, CTC `type 5 recorded per run`), and the contribution sentence stops claiming "exactly two fields are new" — the honest forms are "one field (R1) plus one value set / one instrument" (the build wave's pre-filed reading) or "one new field (S2), one new value set (R1)" with S1 mapped | no row labelled `delta` has any non-`(absent)` cell in the three design columns; the D-c test returns empty |
| 2 | Reconcile §What this does not establish with the table: S081's rare pair is strata (R1) + acquired (S1); state which is a field and which a value set **once**, or the same composition twice | one composition of the pair, used in both places |
| 3 | Declare the dropped union-table row `grader integrity → "Grader evidence"` — mapped, or excluded with a reason — since §Extends claims continuation, not re-derivation | every row of the staging table appears in §Extends or in the mapping, or is named as dropped |
| 4 | Cite S001 (tier A) for the GEM § 7 Table 3 column, and stop saying "its three source rows are not in this lane's registry" without that qualification; for AI Alliance and CTC v1.1 either land the rows or restate the mapping as "this entry's reading of a package file, not a re-derivation" (Q2/Q3 for the load-bearing table) | Q2 can be answered for the mapping claim's scope from `corpus/SOURCES.md`; the sentence no longer contradicts `SOURCES.md:23` |
| 5 | Anchor the κ / ceiling-0.84 / class-skew caveat to S081's abstract quote (the entry uses the behaviour but quotes only the two-variable sentence) | Q3's sentence→quote map has no unanchored load-bearing sentence |
| 6 | Fix the count cells to one named counter. Measured today: S084 `目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集` = **7** whitespace tokens (lesson `:54` says 13; entry says 7); S084 `但如今开源社区…训练数据集` = **1** (lesson 3; entry 1); S086 `一致したものを一律に混入とみなして除去することには疑問が残る` = **30** codepoints, no punctuation (entry **and** lesson say 23; the registry row says 30 and is the only right one) | `len(span.split())` / codepoint count recomputed from the landed strings equals every printed annotation, and the lesson's table equals the entry's |
| 7 | Record `QUALITY.md` Q1–Q8 pass/fail per entry in the round-30 `## Gate`, as the admission bar's preamble requires and round-29's final Gate did — including the Q2 failure and the Q7 pending state, or an explicit statement that the flip's clause is being redefined (which is a predicate change and must be logged as one) | the Gate contains eight rows or lines naming Q1…Q8 and a verdict each |
| 8 | Add CG2's canary cross-reference (or drop the "canary" option from the question) | every access level CG2 names is answerable from a cited artefact |
| 9 | Land the Q10 receipt (`.ufo/waves/round-30/falsify/FxEntryCompleteSet.md` or its successor) and replace `--commit <admitting sha>` with a real sha after the admitting commit; re-run `gate_timing_check.py` | the cited report exists in the commit tree, is registry-registered with a non-writer identity, carries a `VERDICT:` line; the Q13 command exits 0 |
| 10 | Commit entry + index row + coverage row + frontier discharge + SOURCES rows **together** (currently HEAD = baseline; all of it is untracked) | `git ls-tree <admitting sha> -- corpus/knowledge/contamination-transparency-card.md corpus/README.md` shows all of them; `adoption_check.py` exit 0 on that commit's tree |

---

## 5. Why the counters cannot close either locus, and what that means for the claim

- **C1's frozen predicate contains neither flip.** It names the entry, six ids, `verified-at`, six
  registry cells, one index row and one counter line. A rival presenting the field list as *the*
  format would print the same seven fields and exit 0 — the build wave proved this by landing the
  staged text byte-identical except one date (`build/R30CritC1.md`, probe A). The amendment's status
  therefore rests on §Extends/§Rejected prose and the mapping table, none of which `adoption_check.py`
  reads.
- The counter also cannot read the registry `opened` cell (cell 8) — verified by the cell mapping in
  `R30FxFlipRev`'s read of `SOURCES.md` and independently by `R30RevFlip.md` §(b)(8). I checked
  `opened=2026-10-25` by hand; no counter will re-check it on the next run.
- Net: "both flip loci are discharged" is a prose claim about prose, sitting inside a round whose
  counters are green for reasons unrelated to it. That is the same target-drift class the lane
  logged as M99; here the drift is that a *disposition* was recorded in the lesson but no
  falsifiable surface was created for it.

## 6. Confidence, and what would change my verdicts

- **High** on the arithmetic divergence (§2b): it is a cell-for-cell read of two files, both quoted,
  plus the round's own pre-filed D-c criterion. **High** on the commit state and the absent Q10
  receipt (R1/R2/R6 are `git`/`ls` outputs, not readings). **High** on the counts (R5 recomputed),
  and **high** that the S086 figure is 30 — the string has no punctuation to exclude.
- **Medium** on S2: if "card integrity" is intended as a *new field reusing existing values*, one
  new field is arguable; the two-new-fields sentence still fails on S1 alone, so my locus-1 verdict
  does not depend on this one.
- **Budget on Q2**: I did not attempt to tier the AI Alliance template or the CTC v1.1 YAML myself
  (they are not in this lane's registry and I did not open them); my verdict is that the *claim* has
  no lane-side row, not that the sources are weak. `[INFERENCE]` both would clear tier A/B on their
  own merits; that is an admission decision for the round, not a re-read I performed.
- **Not fetched**: S081–S084, S086 (peers `R30FxSrcS082-3` and `R30FxEntryCompleteSet-3` own those
  re-reads; I read their claims, not their evidence). My only fetch was the CAICT PDF (R4), chosen
  because round-29's reject named it as the standing blocker.
- **What would flip locus 1 to discharged**: item 1 alone, corrected in the entry's bytes. Nothing
  else in my list is load-bearing for it.
- **What would flip locus 2 to discharged**: items 7 and 9 — a recorded Q1–Q8 (or an explicit
  predicate-change log), and a real Q10 receipt behind a real sha. The theme/re-open half is already
  done and I could not break it.
