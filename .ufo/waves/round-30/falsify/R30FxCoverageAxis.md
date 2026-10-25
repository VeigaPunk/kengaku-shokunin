# R30FxCoverageAxis — is the coverage axis move honest?

Seat: `L1Kengaku30.R30FxCoverageAxis-3` (leaf critic, falsify wave, round 30, 2026-10-25).
Scope: attack C1's axis sentence, the landed round-30 SCORECARD row and the README coverage map.
No lane writes besides this report; no git mutation; no seat spawn; no model.
Scratch: `/tmp/r30fx-coverage-axis-*`.

Candidate: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL at the byte this seat attacked (`f01b7cd2…`, commit `623c1fc`) — the entry's amendment
delta was overstated against its own cited design: R1's CTC v1.1 cell read `(absent)` and `:69` said
"no design tabulates" strata, while the pinned CTC v1.1 template carries a `strata_reported` block, and
S1's "release-side artefact" characterisation was contradicted by that form's own header. C1's counting
command passed at that byte and still passes at the final pin. **Live status: those cells were repaired
and the currency word was adopted; the report's residue at `caf1e2b` / entry `f51951d3…` is §Addendum 2
(the CTC column's provenance), `:41` vs `:160`, M7/M9 and two SCORECARD one-liners.** The number the
whole report turns on — 7 → 7 held, `improved (counts)`, cap open — was correct at every pin.

**Bytes I attacked (they moved under this seat):** `corpus/knowledge/contamination-transparency-card.md`
sha256 `f01b7cd20cf4ebcaf3ee9f7af8b109ace8b86e69002ae53a213c2dc80ad1e6cd`, mtime
`2026-10-25 04:44:02 -0300`, 17,074 bytes, committed at `623c1fc` (tree and working copy identical
at attack time). A sibling seat repaired the earlier "exactly two fields
are new as *fields* (S1, S2)" sentence at that mtime; this report is measured on the repaired bytes,
not on the pre-repair text, and every falsifier below is re-checked against the current file.

## What I re-ran myself (nothing here is accepted from a build report)

| command | printed | exit |
|---|---|---|
| `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` | 0 |
| `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` | `88` | 0 |
| `ls corpus/knowledge/*.md \| wc -l` / `grep -cE '^\| \`knowledge/' corpus/README.md` | `39` / `39` (parity both directions) | 0 |
| `cat .ufo/waves/round-30/claims/control-nothing.txt` | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` / `exit=1` | — |
| `curl -sS -L https://arxiv.org/abs/2608.29463` | 44646 bytes, sha256 `4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a` — **byte-identical to the source seat's recorded `abs.html` sha** (`build/R30SrcS081.md` §2) | 0 |
| `curl -sS -L …/contamination-disclosure-paper/4dba1ed…/templates/disclosure.yaml` | 2181 bytes, sha256 `05131be9f72b333a479046a0df4510d48fd5389192d40c595869e718b5c90d0f` (scratch only; see the durability defect at the end) | 0 |

The round-25 L0 coverage cap is still **unruled**: `.ufo/l0-questions.md` carries
`kengaku | round-25 | Coverage cap (re-filed …) … Until ruled, kengaku coverage stays capped at 7.`
with no answer after it. `PROVINCE.md` has no round-30 paragraph
(`grep -n 'Round30\|Round 30' PROVINCE.md` → 0 hits); its last section is
`## Round29 attempt-2 partial frontier admission`.

## Attack 1 — "real expansion on ground the lane did not hold", or a restatement?

**Claim under attack.** `SCORECARD.md:1022` verdict cell: "**7 → 7 held** — real expansion on
ground the lane did not hold (frontier bullet 2 *unopened lead* → amendment + CG1–CG8 gate) …";
`plans/round-30-claims.md:42-44` ("new corpus bytes on ground the lane did not hold") and `:23`
("moves from *unopened lead* to *core*").

### 1a — the R1 row is contradicted by the design it cites

Live entry `:66` and `:69`:

```
| R1 strata | (absent) | (absent) | (absent) | **delta** — and see §What this does not establish |
…
and **one new value set** (R1's strata, which no design tabulates and whose own source records
this lane's first failure with it)
```

The CTC v1.1 form is the second column of that table (pinned at commit `4dba1ed…` by the
round-6 schema the entry continues). Its `templates/disclosure.yaml` carries:

```
strata_reported:
  reported: true              # false is an answer; make it visible
  strata: []                  # e.g. ["disease_category_A", "..."]
  aggregate_only: false
  definition: ""              # what defines a stratum
  pre_registered: false
  scores: {}                  # optional: {stratum_name: {n: 0, score: 0.0, ci95: [...]}}
```

That is a tabulated stratum field set with its own definition and pre-registration flags. So R1's
CTC cell is wrong and "no design tabulates" is false. S081 pushes the same way from the source
side: its abstract (my capture, sha matches the seat's) calls **"strata reporting"** one of its own
two variables, and `corpus/SOURCES.md:107` already scopes S081 as "the four-field contamination
disclosure protocol (**strata**, elicitation budget, five types, regeneration), its JSON Schema and
validator". [INFERENCE-strong: CTC v1.1 (S123 in the staged table) is S081's released form — the
repo is `contamination-disclosure-paper`, the four blocks match, and the declared-negative header
is the abstract's rule. The R1 cell error does not depend on that identity: the pinned S123 bytes
alone refute it.]

### 1b — S1's "release-side artefact" is contradicted by the form's header

Live entry `:64`:

```
| S1 acquired contamination | (absent) | type 5 recorded per run | (absent) | **delta in placement, not in field** — the run-side half exists only as the CTC form's type-5 row |
```

The repair correctly stopped calling S1 a new field. The placement claim still fails on the same
fetched bytes: the form's top-level keys are `benchmark:`, `system_under_test:`, `evaluation_date:`
— it is filled **per evaluation**, not per benchmark release — and
`contamination_controls.acquired` is followed by `network_access_during_eval`,
`environment_sanitised`, `transcripts_reviewed`, `boundary_integrity_monitored`, `notes`, which is
the entry's S1 definition verbatim ("network access, environment sanitisation, transcript review or
boundary monitoring — with the elements actually stated recorded in `notes`"). The run-side record
is therefore already placed with the reported evaluation by CTC. S1 is a *rename*, not a
relocation.

What survives as a delta of any kind: **S2's single tri-state card-integrity flag** (`:65`) — CTC
distributes `unknown`/`not_controlled` per contamination type rather than exposing one card-level
state. That is a thin, defensible delta and the entry should be allowed to keep it; one field is
not "what an amendment looks like" as a slogan, but it is what this one is.

### 1c — the residual sentence still counts two items it just stopped calling fields

Live `:110-112` (§What this does not establish, second bullet): "The **two fields** this entry adds
are therefore the two its source measured as rare in practice." After the `:64` repair the table
adds one field (S2) and calls S1 a placement. The bullet must follow the table.

### 1d — "core" has no landed referent

Claims `:23` says frontier bullet 2 "moves from *unopened lead* to *core*". The landed README says
otherwise in three places: the coverage-map row is "covered at source-digest depth"
(`corpus/README.md:242`); the frontier note is "*Partly discharged round 30*", supersedes the
`unopened lead` phrase "**for the card format only**", and keeps "Still frontier: benchmark-
maintainer releases on hidden-test governance (no private-split or hidden-test-governance release
was opened this round)" (`:275`). No benchmark-maintainer release on hidden-test governance was
opened — S081/S082 are arXiv, S083 an EACL paper, S084 vendor docs, S085 a sponsoring body's
self-report, S086 a conference paper. "core" exists in this lane only as PROVINCE's round-section
heading format, and no round-30 PROVINCE section exists.

### What is *not* a restatement, and what was already held

`corpus/knowledge/contamination-detection-and-transparency.md` holds none of the card: `:9-14`
requires "a transparency record" and gives no field, `:73` prefers "suites with a documented
transparency card" and defines none; `grep -rn 'transparency card' corpus/*.md corpus/knowledge/*.md`
returns only that preference, the README gap/index rows and the entry itself. On the lane-corpus
denominator the entry is lane-new ground — I agree with `build/R30Overlap.md` §(c). Nor is the
CG gate new this round: round-29's connector catalogued "card field table + Q1–Q8 answerability
gate" as a drafted candidate with line cites
(`.ufo/waves/round-29/attempt2/build/R29a2ConnCapability.md:27-33`), and the round-6 schema already
cross-tabbed the lane's fields against the three designs
(`benchmark-card-field-schema-2026-10-23.md:70-79`).

**Verdict: PASS on "not a restatement of the round-24 entry" and on "the lane did not hold these
bytes"; FAIL on the magnitude.** The field content is one published design's own field list
re-tabulated, plus a crosswalk and a gate; the R1/S1 rows misdescribe that design, and the
scorecard's "real expansion" sells the re-tabulation as expansion.

**Impacts:** coverage (the claim's axis), calibration (false cells about a cited source),
novelty (a restated published protocol must not inherit construct credit).

**Smallest safe correction.** Set R1's CTC cell to `` `strata_reported` (reported / strata /
aggregate_only / definition / pre_registered / scores) `` and drop "which no design tabulates";
rewrite S1's status as "already a column, renamed — CTC's per-evaluation form carries
`contamination_controls.acquired` with its four run-side keys"; change `:110-112` "The two fields"
to "The field this entry adds (S2)". The entry is committed at `623c1fc`, so repair by a follow-up
commit before the Gate's admission record (round-29 practice) or by an appended erratum section
under QUALITY's no-in-place-edit rule once the Gate has admitted it.

## Attack 2 — does the round claim a coverage score it does not move?

**Claim under attack.** Axis cell "**coverage** (lowest non-retired, tie-break)"; verdict
"7 → 7 held … the canonical coverage score stays 7 while the round-25 L0 coverage cap is open. The
claim is the ledger delta, not a raised number."

**What checks out.** No axis is raised anywhere in the round-30 section (C1 7→7, C2 8→8, C3 8→8;
other axes depth 9 / novelty 7 / freshness 8 / adjacency 8 / calibration 8). The cap cited is the
right cap and it is still open (L0 line verified above). The frozen counting command reproduces at
both ends.

**Counterexample — the currency word.** "Real expansion" is not a unit the coverage rubric
measures. Its +1 anchor is two-legged: "every surface the corpus *describes* is indexed **and** every
index row exists on disk (both directions); `PROVINCE.md` enumerates surfaces that resolve"
(`SCORECARD.md:249`). The row exercises only the first leg, and that leg was already satisfied
before the round (38/38). The second leg does not move: `PROVINCE.md` has no round-30 section,
while round 24 — the precedent this row leans on — counted `province_map_sections 0 → 4`
(`:599`) and wrote its verdict as "improved (counts)" (`:616`). Two rounds running (29 attempt 2,
30) have now discharged the lowest-axis obligation on an axis that `plans/round-25-claims.md:12`
says "cannot change its number"; a round-25 critic named that escape hatch forward
(`.ufo/waves/round-25/falsify/CritMappingFresh.md` §3). That is not a defect of this round — it is
why this round's row must not dress a counts delta as expansion.

**Verdict: PASS on the number; FAIL on the currency word.** 7 → 7 held is honest and correctly
capped; "real expansion on ground the lane did not hold" is an unmeasured upgrade of round 24's
"improved (counts)".

**Impacts:** coverage, calibration.

## Attack 3 — is the axis label right (coverage vs depth)?

**Counter-hypothesis.** The artifact ships two decision tables (field mapping; CG1–CG8 with
"answerable from / not answerable when"), which is the shape the depth rubric rewards ("a decision
table/threshold is derived from a read source and a reader can act on `SKILL.md` alone",
`SCORECARD.md:246`).

**Test.** The second depth leg fails on the tree: `SKILL.md` is untouched this round
(`git status --porcelain` lists no `SKILL.md`) and carries no card text at all
(`grep -n 'card\|transparency' SKILL.md` → one hit, `:445` "discards", an unrelated token;
`grep -n 'contamination' SKILL.md` → the pre-existing re-check lines 63-64, 84, 655, 681). A reader
cannot act on `SKILL.md` alone — the CG table lives only in the entry. AXES' own definition also fits coverage: "fraction of
the domain's real surfaces the skill governs (repo paths, tools, **edge classes**)", and "how to
read a benchmark's contamination claim" is an edge class the corpus can now reach.

**Where the label is imprecise — the sub-row is unnamed.** Round 25's mapping of record separates
`coverage/constructs` (where `novelty` is scored) from `coverage/surfaces`, which "keeps its own
row and cap" (`SCORECARD.md:655-663`). The landed row takes its expansion language from the
constructs side ("real expansion … amendment + CG1–CG8 gate") and its hold reason from the surfaces
side (the L0 cap). A row cannot spend one sub-row's currency and cite the other's cap. No numeric
difference today (both sit at 7), but the sentence becomes unauditable: `adoption_check.py` is a
registry/index counter and cannot see a constructs claim — the same predicate gap CritC1 recorded
(`build/R30CritC1.md` §Attack 3).

**Second, smaller mis-cite.** The other-axes paragraph holds depth at 9 because "the entry adds a
field mapping against a published union table, **no new instrument claim**". "Instrument" is a
novelty criterion (`:244`), not a depth leg; the hold should rest on the depth rubric's own legs.

**Verdict: PASS on the axis choice (coverage, not depth); FAIL on precision (sub-row unnamed;
depth hold reasoned from the wrong rubric).**

**Impacts:** coverage, depth, novelty.

## What survived attack (so the round does not over-repair)

1. C1's frozen predicate is mechanically sound and reproduces byte-for-byte; the freeze control
   prints `entries=0 … exit=1`.
2. The entry lands lane-new corpus bytes, names its extension target (§Extends) as QUALITY Q6
   requires, and discloses that its union table is not lane-sourced.
3. No axis number is raised. The round-25 cap is the right cap and remains unruled.
4. C3's scope notes (no URL binding; 25-word cap inert for CJK; PDF text layers) are honest; I
   found nothing to add.

## The exact SCORECARD wording (drop-in replacements)

C1 row, axis cell:

> **coverage (surfaces)** — lowest non-retired, tie-break; held by the open round-25 L0 cap

C1 row, verdict cell:

> **7 → 7 held — improved (counts)**, number held by the open round-25 L0 coverage cap (still
> unruled). Counts it moves: registry 82 → 88 rows (S081–S086; tier A 76→79, B 4→7), knowledge
> files 38 → 39, index rows 38 → 39 with 39/39 parity both directions. Counts it does not move:
> `PROVINCE.md` carries no round-30 section, so the rubric's "PROVINCE enumerates surfaces that
> resolve" leg is unchanged. What the new bytes are: S081's published four-field disclosure
> protocol (strata, elicitation budget, five types, regeneration — its released CTC v1.1 form
> already carries `strata_reported`, the type-5 run-side block inside a per-evaluation form, and
> the declared-negative rule) crosswalked into the round-6 union table's columns, plus the
> CG1–CG8 answerability gate the staged package already drafted (`R29a2ConnCapability.md:27`),
> re-grounded on six rows opened 2026-10-25. The only field this entry adds is S2's tri-state
> card-integrity flag; R1, R2, R4, R5 and S1 are columns CTC v1.1 carries, R3 is the AI Alliance
> template's, and the negative-disclosure row is common to all three. Frontier bullet 2 is
> **partly** discharged: the card-format half lands; the bullet's `unopened lead` —
> benchmark-maintainer releases on hidden-test governance — is still unopened. No construct,
> method or phenomenon credit is taken, and the claim is the ledger delta, not a raised number.

Other-axes sentence, depth clause:

> depth 9 (held on the depth rubric's own legs: `SKILL.md` is unchanged, so "a reader can act on
> `SKILL.md` alone" is not met, and citation resolution is unchanged; instrument criteria belong
> to novelty)

Two phrases the round must not use downstream of this row: **"core"** (no landed referent — README
says "Partly discharged"; PROVINCE has no round-30 section) and **"real expansion on ground the
lane did not hold"** (replaced by "improved (counts)" plus the list above).

## Adjacent defect found while testing the axis (one-line-per-row fix)

The six new rows carry **no byte identity**: `corpus/SOURCES.md:107-112` give URL + quote + line
number, while round 29's S077–S080 rows carry `sha256` and byte counts. The captures live only under
`/tmp/r30-*` (e.g. `/tmp/r30-R30SrcS081/`), which is the `/tmp`-pointer pattern round 14's lesson
rejects at closure, and it means C3's new `--artifact <capture>` mode has **no committed artifact**
to run against for this round's own six rows — the gate validates quotes the round cannot re-supply.
Fix: paste each source seat's §2 sha256 + byte count into its anchor cell, as round 29 did. Impacted
axes: freshness, operability.

## Limits of this report

- I did not re-derive the S082–S086 source verdicts; those are other seats' items
  (`falsify/R30FxSrcS08{1,2,4,6}.md` are landed; I read their verdict lines, not their evidence).
  My S081 fetch is an independent byte-identity cross-check (`4c81bd3c…` matches the seat's), not a
  re-admission.
- `S123` is not in this lane's registry; the union table's **third** design is — the GEM 2026 review
  is `corpus/SOURCES.md:23` row S001, so the entry's "three source rows are not in this lane's
  registry" (`:41`, `:131`) is false and its own `:153` ("two of its three") is right. My CTC read is
  against the commit the entry's own union table pins, fetched today, sha `05131be9…`, retained in
  scratch only.
- The round landed commit `623c1fc` while this seat ran; the attacked entry byte is identical in
  the commit and in the working copy (`git cat-file -p HEAD:… | sha256sum` = `f01b7cd2…`), so every
  falsifier above is against the admitted byte. Counter, registry and index counts were re-run
  after that commit.
- Sources read: S081 abstract (fetched) and S123's pinned template (fetched); S122/S124 not
  re-fetched by this seat.
- No tool installed or upgraded by this seat: `curl` and `python3` stdlib only, both already
  present. PACMAN was not invoked.

## Status on live bytes (appended after three repair commits; supersedes nothing above)

The entry and its row moved while this seat ran. Live state at the time of this append: `HEAD`
`a780c4e` (round-30 repair chain `623c1fc` → `706ed3f` → `d0253c5` → `5cd9229` → `a780c4e`), entry
sha256 `ba0465d1cbcbb0b62529343a7c4fe5c4c26e37db6fd462ac93a8e9d95f106d82` (`git cat-file -p
HEAD:corpus/knowledge/contamination-transparency-card.md | sha256sum` equals the working copy), and
the counter re-run at that state: `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6
usedby_ok=1 census=ok`, exit 0.

| my item | live status | live bytes |
|---|---|---|
| 1a R1 cell + "no design tabulates" | **closed** | `:66` now cells `strata_reported` and reads "already a column in one of three"; the `:70` sentence no longer claims a new value set |
| 1b S1 "release-side artefact" | **closed** | `:64` now reads `contamination_controls.acquired` plus the run-side keys, status "**not a delta** — the CTC form already carries the run-side fact; it is a rename, not a relocation" |
| 1c residual "two fields" bullet | **closed** | `:112-120` now says the two fields S081 measured as rare "are the two this entry marks as already-columned", and that S2 is the one genuinely new field |
| 1d "core" | **closed in the row, open in the frozen prereg** | `SCORECARD.md:1022` now ends "…S2's tri-state flag is the only surviving field delta. **Not core, not real expansion.**" But `plans/round-30-claims.md:22-24` still reads "moves from *unopened lead* to *core*", its §Change record (`:99+`) does not mention the wording, and `grep -n 'core\|partly discharged' corpus/lessons/round-30.md` → 0 hits. One lesson errata line is still owed; frozen claims text stays as landed. |
| 2 currency word + PROVINCE leg | **closed** | row now opens "**7 → 7 held — improved (counts)**; axis *coverage (surfaces)*, held by the open round-25 L0 cap" and adds "Counts it does not move: no `PROVINCE.md` round-30 section, so the coverage/surfaces leg is unchanged" |
| 3 sub-row in the verdict cell | **closed there, not in the axis cell** | the verdict cell names `coverage (surfaces)`; the axis cell is still `**coverage** (lowest non-retired, tie-break)`. Cosmetic, but the two cells now name different things. |
| 3 depth-hold reason | **open** | `SCORECARD.md:1026` still reads "depth 9 (… no new instrument claim)" — an instrument criterion belongs to novelty, not to the depth rubric's legs |

**Defect found on the mid-repair bytes, now fixed.** `corpus/knowledge/contamination-transparency-card.md:120`
rendered as `- **- **Agreement is not established.**` from `706ed3f` through the `ba0465d1…`/`a78eb18a…`
repairs; the marker is single again at the final pin (`f51951d3…`) and what the repair left behind is
a duplicated *sentence* at `:125-126` (see §Addendum).

**Net effect on my verdict.** The `VERDICT: FAIL` at the top of this report is the record of the byte
this seat attacked (`f01b7cd2…`, `623c1fc`); its two field falsifiers and the currency word are
repaired, and the residue — enumerated at the end of §Addendum against the final pin — is
calibration-grade text inside the entry plus two SCORECARD one-liners and one frozen-prereg errata
line. Nothing in it is a reason to refuse C1's admission or to move the coverage number off 7.

## Addendum — items the complete-set seat raised, re-verified on live bytes

**Revision note (2026-10-25, appended in place because this report's own claims must be true of the
byte it describes):** the entry moved five times after this seat wrote. Final pin for this report:
`caf1e2b:corpus/knowledge/contamination-transparency-card.md`, sha256
`f51951d327fa0d4e9ff4157f07b012f70e175b8501c388716746dd4bac8b86eb`. I will not re-pin after this;
later repairs are the owners' to verify. At this byte the counter still prints
`entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0.

The complete-set seat's fetch reproduces mine (same pinned form, same sha). Status of its items and
mine at the final pin:

- **R1 strata — closed.** `:75-77` now reads "strata are carried by the CTC v1.1 form
  (`strata_reported`) and are absent from the other two tabulated designs …" — consistent with the
  `:69` cell. My `05131be9…` fetch of the pinned form is what that sentence now states.
- **S1 — closed** for the third time: `:67` "**not a delta** … it is a rename, not a relocation".
  R4 — closed: `:66` "a dedicated `regeneration:` block".
- **S085 "no measurements" — closed.** `:129` and `:186` now read "no contamination measurement"
  (qualified), matching `:150` and the capture `/tmp/r30-R30SrcS085/caict.txt:1151` (25.8 / 51.8 with
  a score table at `:1178`).
- **`:41` still contradicts `:160`.** `:41` says "three source rows are not in this lane's registry
  (the GEM 2026 review it tabulates is the one exception …)"; `:160` says "two of its three source
  rows are staged". Three minus the one exception is not three. The exception is
  `corpus/SOURCES.md:23` **row S001** (GEM 2026 review, tier A, `mined`, `opened 2026-10-19`, teach
  cell "…the Contamination Transparency Card…", URL `…/2026.gem-main.50`; the staged table's S124 is
  `…/2026.gem-main.50.pdf`, the same document). **This is the residue that touches my axis:** one
  tabulated design was already lane-held, so "ground the lane did not hold" is true of the card
  *format*, not of the designs or the card idea.
- **`:125-126` duplicates a sentence** — "Two coders filling this card need not agree; the card
  records what each stated, not a reconciled truth." twice in a row.
- **`:74` leaves open what the entry's table settles.** "…whether that makes the record score-side is
  a question about *where* it is filed, and this lane cannot settle it without reading that form"
  sits two rows above CTC cells (`contamination_controls.acquired`, `strata_reported`,
  `regeneration:`, `evaluation_date`) that can only come from reading that form, and the form's own
  top-level `system_under_test` / `evaluation_date` answer the placement question. Reading it is what
  the table already did.

**Axis-adjacent integrity item verified here (not the complete-set seat's alone).** At the admitting
commit `623c1fc`, `corpus/lessons/round-30.md` `:31`/`:35` cited `.ufo/waves/round-30/falsify/
R30FxEntryCompleteSet.md` and `…/R30FxRowsCensus.md`, and neither path is in that commit's tree:

```
git cat-file -e 623c1fc:.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md
 → fatal: … exists on disk, but not in '623c1fc'
```

`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit 623c1fc` exits 0
anyway (`PASS line 17 Gate admit … second-seat-reports=28`) because the tool parses Gate rows only,
not the Q10 row. This is the round-26 Q13 class reappearing on a side surface: a coverage claim whose
supporting second-seat set is time-shifted relative to the commit that carries it. The live lesson no
longer cites either path (`grep` → 0 hits at `caf1e2b`), so it is a historical byte fact, not a
present defect; it belongs in the lesson as a Q13 note, not in the SCORECARD row.

**Net effect at the final pin.** The number is right (7 → 7 held, `improved (counts)`, cap open, no
PROVINCE leg) and the row's currency wording is honest. Inside the entry three items remain — `:41`'s
three-vs-two arithmetic, the `:125-126` duplicate, and the `:74`/table tension — all calibration-grade,
none score-moving. This report's `VERDICT: FAIL` therefore remains the accurate reading of the entry's
text (as a calibration finding, not a refusal of the admission); the axis answer is unchanged from
§Attack 1-3: the label and the number are correct, the magnitude of "expansion" was overstated and is
now mostly corrected.

### Addendum 2 — the CTC column's provenance (verified, and the largest axis item left)

The complete-set seat calls this M8; I re-derived it from bytes rather than taking it:

| check | result |
|---|---|
| `grep -cE '^\| *S12[234] *\|' corpus/SOURCES.md` | `0` — no row for the AI Alliance template, the CTC v1.1 form, or the GEM § 7 table beyond S001 |
| `grep -c 'disclosure.yaml\|4dba1ed\|Jangulo7\|raw.githubusercontent' corpus/knowledge/contamination-transparency-card.md` | `0` — the entry names neither the form's path nor its commit |
| `grep -c 'strata_reported\|network_access_during_eval\|regeneration' benchmark-card-field-schema-2026-10-23.md` | `0` — the campaign staging table does not carry any of them (its six CTC cells are `contamination_controls`, `unknown/not_controlled`, "type 5 recorded per run", `elicitation_budget`, `evaluation_date`, —) |

So three cells that are now load-bearing for the entry's delta arithmetic — `strata_reported` (`:69`),
the run-side key names (`:67`), "a dedicated `regeneration:` block" (`:66`) — can only come from
`templates/disclosure.yaml` at `4dba1ed…` (2,181 B, sha256 `05131be9…`), an artefact this lane holds
no registry row for and the entry never cites by path. The `:41-46` shelter covers only the campaign
staging file; `:74` then says the lane "cannot settle it without reading that form, **which it has not
admitted**".

This is the coverage question in its exact form, and it cuts both ways:

- the cells are **factually right** — my own fetch of the pinned form contains every one of them, which
  is why H1/H2's repairs hold;
- their **provenance is unsheltered** — the lane's Q2 discipline says a load-bearing reading names an
  artefact it holds. Right now the entry both depends on the form and says it has not admitted it, so
  a reader cannot tell whether the CTC column is a reading or an inheritance from the campaign table
  (which does not contain those cells, so it cannot be the latter).

Smallest safe fix, in preference order: (a) register the form as a registry row (path + commit
`4dba1ed…` + sha256 `05131be9…` + located field names as the anchor) and add its `used-by` — this
makes the whole mapping lane-sourced and retires the caveat; or (b) if registering is out of round-30
scope, mark the CTC column "read from a staged artefact, not admitted" in the table header and delete
`:74`'s "cannot settle it without reading" clause, which is false given the cells above it. Either way
the axis claim should read "the mapping's CTC column is a reading of an unregistered artefact" rather
than "ground the lane did not hold".

No score moves: 7 → 7 held, cap open, currency `improved (counts)` — the ledger delta is the same
either way. This is a Q2/provenance defect on the entry, and it is the item I would not let past the
Gate.
