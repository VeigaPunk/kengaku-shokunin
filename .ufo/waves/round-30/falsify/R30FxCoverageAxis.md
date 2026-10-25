# R30FxCoverageAxis — is the coverage axis move honest?

Seat: `L1Kengaku30.R30FxCoverageAxis-3` (leaf critic, falsify wave, round 30, 2026-10-25).
Scope: attack C1's axis sentence, the landed round-30 SCORECARD row and the README coverage map.
No lane writes besides this report; no git mutation; no seat spawn; no model.
Scratch: `/tmp/r30fx-coverage-axis-*`.

Candidate: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL — the entry's amendment delta is still overstated against its own cited design: R1's
CTC v1.1 cell reads `(absent)` and `:69` says "no design tabulates" strata, while the pinned CTC
v1.1 template carries a `strata_reported` block, and S1's "release-side artefact" characterisation
is contradicted by that form's own header. C1's counting command passes (re-run below) and the
score 7 → 7 held is the honest number. Repair is two cells, one clause, and the SCORECARD wording
in §"The exact SCORECARD wording".

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
- `S123` is not in this lane's registry (the entry says so and cites it by document); my CTC read is
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
