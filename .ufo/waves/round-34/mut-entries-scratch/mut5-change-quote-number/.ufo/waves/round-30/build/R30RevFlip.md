# R30RevFlip — what round 29's reject actually demanded, and what an "amendment" discharges

Seat `L1Kengaku30.R30RevFlip` (leaf, revenger — no dispatch, no production edits, no runtime
invoked on the lane). Date 2026-10-25. Contract: reconstruct the round-29 reject's flip condition
from bytes, state which clauses an amendment framing satisfies and which it does not, and give the
smallest statement set the round-30 entry must carry.

Everything below is a quote from bytes I fetched in this seat or a pointer to them. `[INFERENCE]`
marks the two places where I reason past the bytes. Nothing was run against the lane's gates, no
source URL was fetched, and the only file written is this report.

## Evidence base

| # | bytes | what they establish |
|---|---|---|
| E1 | `corpus/lessons/round-29.md:223-227` | the reject's reason sentence and its two evidence pointers |
| E2 | `corpus/lessons/round-29.md:241-243` | the compressed flip sentence C1 quotes |
| E3 | `corpus/lessons/round-29.md:180` | the attempt-2 Gate row: a *second*, differently-worded flip |
| E4 | `.ufo/waves/round-29/attempt2/build/R29a2RejectScan.md` §1 | the property-level receipt: four-part flip (a)-(d), the duplication inventory, the S077 seam, the Q1–Q8 label collision |
| E5 | `lanes/kengaku/round6/DOMAIN.md:43-46` (shokuknow, read-only) | the campaign rule the reject rests on: "amendment to published designs" not "rival invention" |
| E6 | `merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md:71` | the union-of-three-designs table header: `| Lane's proposed field | AI Alliance template | CTC v1.1 form | GEM § 7 Table 3 |` |
| E7 | `merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md` (92 lines) | the staged entry as it stands: 6 `source:` lines, `verified-at: 2026-10-23`, `### The Q1–Q8 gate` at `:45`, body cites S077 at `:54`, `ground:` at `:90` declines the extension |
| E8 | `plans/adoption_check.py:34,79,88,95,122` | what the C1 counter can and cannot see |
| E9 | `corpus/QUALITY.md:50-63` | Q6 "extends, never duplicates or overwrites"; Q7 index+coverage row land together; Q8 rejections kept; Q10 second-seat re-read (`:75-79`) |
| E10 | `corpus/README.md:272` | frontier bullet 2 verbatim, including "draft a card template and gate a knowledge entry on Q1–Q8" |

## (a) What round 29 required for this entry to flip

Round 29 recorded the flip **twice, at different granularities**. Both are operative; they are not
alternatives.

**A1 — the reason + compressed flip (E1, E2), the record C1 quotes.**

> - `contamination-transparency-card.md` — reject on scope (QUALITY Q6): it offers a fourth card
>   design where the campaign's own round 6 tabulated three published designs and ruled this file an
>   amendment, not a rival (`lanes/kengaku/round6/DOMAIN.md:43-46`;
>   `benchmark-card-field-schema-2026-10-23.md:71`). Secondary: all six sources carry the campaign's
>   `2026-10-23` opened date and none was re-opened this round.
>
> Flip conditions: re-open the cited sources in a later round; for the card, land it as an amendment
> to the tabulated designs rather than a new design; …

**A2 — the attempt-2 Gate row (E3), a different axis and a different flip.** Reason: "a second
frontier instrument (contamination cards), not the round's one theme; six sources including two PDF
hosts and one CAICT host that returned HTTP 000 on a first fetch were not re-opened this round".
Flip: "open S081–S086 in a later round **as its own theme** and pass QUALITY Q1–Q8 then".
A2 says nothing about design-vs-amendment; A1 says nothing about one-theme. A discharge needs both.

**A3 — the property-level receipt behind A1 (E4), which A1's one sentence compresses.** Verbatim:

> **Flip condition:** admit only when (a) the file is rewritten as an amendment section naming
> `benchmark-card-field-schema-2026-10-23.md` and `contamination-detection-and-transparency.md` as
> what it extends, keeping the union-of-three-designs table rather than a fourth design; (b) all
> of S081–S086 **and** S077 are re-opened on 2026-10-25 with a ≤25-word located quote each and the
> `source:` header lists every id the body cites; (c) the gate labels move off `Q1–Q8`; and (d) a
> second seat (Q10) re-reads each quote/location.

A3(a) rests on E5, which fixes what "amendment" means:

> So the lane's own `contamination-transparency-card.md` should be rewritten as an
> **amendment to published designs** rather than as a rival invention. The round-6 entry
> `benchmark-card-field-schema-2026-10-23.md` does that and tabulates the union of the
> three field sets.

Note what E5 says about the *object* of the amendment: "an amendment to published designs" whose
carrier "tabulates the union of the three field sets". The thing being amended is the **tabulation**
(the round-6 table, E6), not a fresh reading of S122–S124. That is the hook the round-30 entry must
use, because it is the only hook that fits inside C1's frozen six-id predicate (see (b) item 6 and
(c) D-d).

Seven clauses, therefore, make up the full flip: **theme, re-open, quote, header-completeness,
amendment-not-design, label-move, second-seat re-read** (the last two are (c)-(d) of A3; Q10 is
already in the standing admission bar per E9).

## (b) What an "amendment" framing satisfies — and what it does not

### Satisfies

1. **The design-vs-rival axis, in form.** "Amendment" is the word the reject itself supplies as the
   flip ("land it as an amendment to the tabulated designs rather than a new design", E2). A claim
   that frames the landing as an amendment is aimed at the right property — A1's reason, not A2's
   one-theme reason.
2. **The one-theme clause of A2.** C1 carries the card alone; the judge and grader entries stay
   rejected (E1, first two bullets), so "as its own theme" is structurally met. The freeze's own
   sentence corroborates this is deliberate: "the card's Q1–Q8 gate is admitted as an amendment that
   names the lane entry it extends, not as a rival design" (`plans/round-30-claims.md` §C1).

### Does not satisfy

3. **Two objects must be named; C1's prose names one.** A3(a) requires naming
   `benchmark-card-field-schema-2026-10-23.md` **and** `contamination-detection-and-transparency.md`.
   C1 says "names the lane entry it extends" (singular). Only the second is a lane-corpus entry
   (`corpus/knowledge/` holds `contamination-detection-and-transparency.md` and no
   `benchmark-card-field-schema-*` file — verified by `ls corpus/knowledge`). The tabulation lives in
   the merge package (E6), so naming it is naming a *campaign record*, not a corpus entry. Both names
   are required; the claims sentence covers one.

4. **The framing is not the bytes.** The staged entry (E7) contains **zero** reference to the three
   designs or to the tabulation: `grep -n "S122\|S123\|S124\|field-schema\|card-design-arbitration\|
   benchmark-card-adoption" contamination-transparency-card.md` → no output, exit 1. Its own `ground:`
   line (`:90`) explicitly declines the relation ("the *admission* of the card against the lane's
   existing `knowledge/contamination-detection-and-transparency.md` vocabulary is the lane's call,
   not this entry's"). Landing those bytes with `verified-at` bumped to 2026-10-25 discharges
   **nothing** on A1/A3(a): an amendment label with no `## Extends` and no union table is still the
   fourth design. Q6 (E9) is the standing bar that makes the section load-bearing: "The entry names
   the existing entry or coverage row it extends".

5. **Re-opening is orthogonal to framing.** A1's first clause and A3(b) are source work; the
   amendment framing does not touch them. C1's six re-opens address the header's six ids. They do not
   address the body's seventh id: the staged entry cites **S077** at `:54` ("S077 (canary, per task)")
   and S077 is not in its `source:` header (`:2-7` list S081–S086 only, `verified-at` at `:8`; id census over the staged file
   = S077 ×1, S081 ×13, S082 ×5, S083 ×3, S084 ×7, S085 ×2, S086 ×7). A3(b) says the header "lists
   every id the body cites".

6. **The frozen predicate mechanically forbids the obvious fix for (5).** `adoption_check.py:122`
   requires `len(cited) == required`, where `required = sum(len(sources))` = 6 for
   `.ufo/waves/round-30/adoption-expect.json`. `SOURCE_LINE_RE` (`:34`) is one id per `source:` line.
   Adding S077 to the header → `cited_rows=7`, exit 1; keeping A3(b) unsatisfied → flip open. The only
   way to satisfy both records is to **remove the S077 id from the entry's bytes** and record the
   canary access level as a cross-reference to `knowledge/benchmark-task-validity-checklist.md`
   (which already carries S077 as a `source:` id and as its `used-by`). Re-freezing the expect file to
   seven ids would be a predicate change after seats have scored — by the freeze's own rule
   ("a predicate changed after a seat has scored is not this claim's predicate",
   `plans/round-30-claims.md` preamble), that is a different claim.

7. **The label collision is untouched by the framing.** E4 records it as an operability defect, not a
   style note: the entry's gate is named "Q1–Q8" (`:45`, `:47`, `:69`, `:90`) and so is the lane's
   admission bar (`corpus/QUALITY.md` Q1 through Q8) — "Two different Q1–Q8 in one corpus is an
   operability defect". C1's own text still uses the colliding label ("the card's Q1–Q8 gate"), and
   the frontier bullet it quotes (E10) supplies it ("gate a knowledge entry on Q1–Q8"). A3(c) is
   therefore still open on the claim's own surface as well as the entry's.

8. **The counter cannot see most of the flip.** What `adoption_check.py` actually enforces: entry file
   exists; one anchored `| \`knowledge/<name>.md\` |` row in README (`:77-78`); `verified-at:
   <access_date>` present (gated, unprinted, `:79`); distinct ids on `source:` lines (`:34`);
   `rows_present`; `rows_mined` = registry cell **[7]** == `mined` (`:88`); `usedby_ok` = registry cell
   **[10]** contains the entry path (`:95`); census exit 0. It does **not** read the registry `opened`
   cell (cell 8 — proved by cell mapping on S090: `0 id, 1 source, 2 kind, 3 tier, 4 scope, 5 anchor,
   6 teaches, 7 status, 8 opened, 9 recheck, 10 used-by`), does not read prose, does not require a
   coverage-map row, and knows nothing about Q labels or the union table. So a run printing
   `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` is compatible
   with an entry that fails A3(a), (b)-header, (c) and (d). **The counter is necessary, not
   sufficient.** That is the same target-drift class the lane already logged as M99; here the drift
   is `opened=2026-10-25`, a clause of C1's frozen sentence that `adoption_check.py` cannot evaluate.

9. **Q10 is a seat condition, not an entry property.** A3(d) and E9's Q10 ("a seat other than the
   entry's writer re-opens each cited source and confirms every quote location and every number")
   cannot be discharged by any sentence inside the entry. It needs a committed non-writer receipt, and
   C1's kill rule ("a cited source whose located quote cannot be found in this round's own fetch is
   refused for that row; if fewer than four of the six survive, the entry is not admitted") presumes
   exactly that receipt.

## (c) What would still be a duplicate design, verbatim

From the reject's own sentence (E1, `corpus/lessons/round-29.md:223-225`):

> it offers a fourth card design where the campaign's own round 6 tabulated three published designs
> and ruled this file an amendment, not a rival

and the campaign rule it cites (E5, `lanes/kengaku/round6/DOMAIN.md:43-46`):

> So the lane's own `contamination-transparency-card.md` should be rewritten as an
> **amendment to published designs** rather than as a rival invention. The round-6 entry
> `benchmark-card-field-schema-2026-10-23.md` does that and tabulates the union of the
> three field sets.

Operational reading of that sentence — the round-30 entry is **still the fourth design** if any of
these holds:

- **D-a** it has no amendment section naming the entry/tabulation it extends (Q6's "names the existing
  entry or coverage row it extends"), so the reader cannot tell which published field set each of its
  fields came from;
- **D-b** its release-side/score-side field table (`R1–R5`, `S1–S2`, E7 `:28-43`) is presented as *the*
  card format rather than mapped into the four columns of E6 (`Lane's proposed field | AI Alliance
  template | CTC v1.1 form | GEM § 7 Table 3`) — an un-mapped field list is a design, whatever its
  heading says;
- **D-c** any field that is already a column of E6 is claimed as the amendment's new content
  (release-vs-score, elicitation budget, instrument currency, card integrity all have columns);
- **D-d** the union table is re-derived from the merge package or the three designs are re-tabulated
  here, instead of continuing the round-6 tabulation — E5 says the round-6 entry "does that", so a
  second tabulation is the rival move, and it also collides with C1's six-id predicate (A3(a) attaches
  to the tabulation, not to S122–S124).

What is **not** duplication: mapping every staged field into E6's columns, keeping the table, and
naming the delta honestly. On the recorded table, exactly one staged field has no column — `R1
Strata` ("per-stratum scores for a named stratification", E7 `:32`, attributed to S081 F1). The
answerability gate is an instrument over the fields, not a field. So the honest delta statement is
one field plus one instrument, with the rest mapped. `[INFERENCE]` whether any of the three published
designs carries per-stratum performance internally; the recorded tabulation does not list it, and the
amendment attaches to the recorded tabulation.

## Smallest statement set the round-30 entry must carry

Each item states the statement, the clause it discharges, and the failure that makes it checkable.
Items 1-7 are entry bytes; 8-9 are receipts the round must commit beside it.

| # | statement | discharges | failure that proves it |
|---|---|---|---|
| 1 | `source:` is exactly six lines, one id per line, S081–S086, and **no other S-id appears anywhere in the file** — the `S077 (canary, per task)` cell at `:54` becomes a cross-reference to `knowledge/benchmark-task-validity-checklist.md` | A3(b) header-completeness **and** C1 `cited_rows=6` | adding S077 to the header flips `cited_rows` to 7 → exit 1 (`adoption_check.py:122`); leaving S077 in the body leaves A3(b) open |
| 2 | `verified-at: 2026-10-25` | C1 gating condition | counter prints the same seven fields either way — only the exit code moves, so the receipt must show exit 0 |
| 3 | a `## Extends` section naming **both** `knowledge/contamination-detection-and-transparency.md` (lane entry) and the round-6 tabulation `benchmark-card-field-schema-2026-10-23.md` | A1, A3(a), Q6 | a reader can point at the file each field set came from; the staged `ground:` line's "is the lane's call, not this entry's" is deleted |
| 4 | the union-of-three-designs table reproduced (4 columns, E6's header verbatim) **plus a row mapping each staged field to its column**, and an explicit delta limited to fields with no column (R1 strata), attributed to an in-header id | A3(a) "keeping the union-of-three-designs table rather than a fourth design" | every staged field either has a column or is named as delta; a field that has a column cannot appear as new |
| 5 | the gate is renamed (not `Q1–Q8`), and the frontier bullet's discharged line at `corpus/README.md:272` uses the new label | A3(c) | two Q1–Q8 no longer coexist: `grep -n 'Q1–Q8' corpus/knowledge/contamination-transparency-card.md corpus/README.md` shows only the admission bar and the superseded quote |
| 6 | the body cites **no** S122/S123/S124 and no other out-of-header id; the three designs are referenced only through the round-6 tabulation | C1's six-id equality + E5's "amendment to published designs" | id census over the entry = the six header ids only |
| 7 | one anchored index row `\| \`knowledge/contamination-transparency-card.md\` \|` **and** a coverage-map row **and** the frontier discharge line, all in the same commit | C1 `indexed=1`, Q7 | the counter sees only the index row; Q7's second row is a seat check |
| 8 | a committed receipt of the six registry rows' `opened=2026-10-25` cells (status `mined`, `used-by` exactly `corpus/knowledge/contamination-transparency-card.md`) | C1's `opened=2026-10-25` clause, which the counter cannot read | `adoption_check.py:88` reads cell 7 only; cell 8 must be shown by the receipt or the clause is unproved |
| 9 | a committed non-writer Q10 receipt re-reading each of the six quotes at its located position, with the kill rule applied (<4 survivors → honest stop, registry delta 0) | A3(d), Q10, C1 kill rule | the receipt names a seat id different from the entry's writer and prints quote + location + word count per row |

Items 1-7 are what the entry must **say**; 8-9 are what the round must **show** so the flip is not
re-opened on the two clauses no counter can reach.

## Divergences observed in sibling seats' drafts at filing time

The lane entry itself does not exist yet (`ls corpus/knowledge/contamination-transparency-card.md` →
absent, 04:26). Two sibling drafts are already on record and both intersect this reconstruction. I
diverge from them in three places, with reasons.

1. **`R30Overlap` §Risks A2 proposes renaming the gate "`C1–C8`" — that collides with the round's
   claim ids.** `C1`/`C2`/`C3` are the frozen claim identifiers (`plans/round-30-claims.md` §C1–C3)
   and are printed as such in the closure counter's own label (`defects=…`, C2) and the lesson. A
   gate named `C1–C8` would put a third namespace inside the same round in exactly the way `Q1–Q8`
   already did. Any label outside `Q…` and outside the claim/defect/lesson namespaces works; the
   round should fix one label and use it in three places (entry section, frontier discharge line,
   report).
2. **`R30Overlap` leaves the S077 seam open ("Main's call").** It is not open: the frozen expect file
   pins six ids and `adoption_check.py:122` requires `len(cited) == required`. Keeping the S077 id in
   the body while the header stays six satisfies the counter and leaves A3(b) open; adding a seventh
   header line breaks the frozen predicate. So the id must leave the body. Nothing is lost: the
   canary access level survives as a cross-reference to
   `knowledge/benchmark-task-validity-checklist.md`, which is where the lane's canary bytes actually
   sit (overlap seat's own `:33` quotes axis G there) and which already carries S077 as `source:`
   and `used-by`.
3. **`R30Overlap` risk 2 says naming the tabulation would "cite an unlanded working copy, which
   `QUALITY.md:56-58` (Q7) forbids", leaving `contamination-detection-and-transparency.md` as the
   "safe lane-internal extension target alone".** Q7's bar is on *support*, not on provenance: "no
   support rests on `/tmp`, `local://` or an unlanded working copy". An amendment whose table is
   reproduced in the entry's own bytes, with the round-6 path named as the record it continues, does
   not rest support on the staged file — and A3(a) explicitly requires that name. Naming only the
   lane entry leaves the design-vs-amendment relation to the tabulation unstated, which is the reject
   itself. Land both names (checklist item 3) and let the reproduced table carry the support.

## Confidence, and what would change my answer

- **High** that A1+A3 (not A1 alone) is the operative standard: E1's reason sentence is a paraphrase
  of E4's "Reason (property)" paragraph, E4 is the only property-level receipt in the round, and E4's
  flip is the one the lesson compresses. **High** on the mechanical conflict in (b)(6): it is a read
  of `adoption_check.py:34,122` against the expect file, both frozen.
- **High** on (c): E5's wording plus E6's table are unambiguous about which object is amended.
- **Medium** on one sub-point: whether S081's bytes support a canary access level, which decides
  whether dropping the S077 id costs the Q2 cell or merely re-attributes it. `[INFERENCE]` I did not
  fetch S081; the round's `R30SrcS081` receipt decides. If S081 does not support it, the cell must be
  re-attributed to an in-header id or the access level dropped — not silently kept with a dead id.
- **Not verified by me:** whether any S081–S086 URL still returns bytes today; no fetch was made.
  Whether the six quotes survive is the Src seats' question and C1's kill rule, not mine.

Tool installs/upgrades: none (nothing needed). No pacman transaction attempted.

--- 
