# R30 C1 overlap seat — what the card extends, what the lane already holds

Seat: `L1Kengaku30.R30Overlap` (leaf). Access date for lane bytes: 2026-10-25.
Scope: read-only. No production edits. No web fetch was made by this seat — every quote below is
bytes read from the lane repo or from the staged package on this host; sources S081–S086 were not
re-opened by me (that is the S082/S083/S084 seats' work), so nothing here is a re-grounding verdict.

Files read in full: `plans/round-30-claims.md`, `corpus/knowledge/contamination-detection-and-transparency.md`,
`corpus/knowledge/benchmark-task-validity-checklist.md`, `corpus/QUALITY.md` (Q1–Q12 region read,
Q6 quoted), `corpus/README.md` index rows and coverage map, `corpus/lessons/round-29.md` §Gate,
`.ufo/waves/round-29/attempt2/build/R29a2RejectScan.md` §1,
`/home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md`,
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md`
(sha256 `9dee0e0306b9f38a1739b16a0a318e9c76bd3203f2c6656fceeba3f90eaa4dfc`, mtime 2026-10-24 23:33:20 −0300,
7921 bytes, so it is *newer* than the round-29 rejection), and `SOURCES.append.md` rows S081–S086.

## (a) The entry it extends, and the exact lines that hold the gap

**Extending entry: `corpus/knowledge/contamination-detection-and-transparency.md`** (landed round 24,
`verified-at: 2026-10-19`, source line `:1` = S001/S002/S004).

The gap is held in four places, in the lane's own bytes:

| # | Location | Bytes that hold the gap |
|---|---|---|
| G1 | `corpus/README.md:272` | "**Contamination transparency cards**: why — `knowledge/contamination-detection-and-transparency.md` establishes the tier/access vocabulary but the lane has no standard card format recording detector access, tier tested, and what a negative cannot rule out. Next source/instrument: current benchmark-maintainer releases on hidden-test governance and contamination-transparency cards (unopened lead); draft a card template and gate a knowledge entry on Q1–Q8." |
| G2 | `corpus/SOURCES.md:138` (Leads, unopened) | "Benchmark-maintainer releases on hidden-test governance and contamination transparency cards beyond LiveBench (e.g., other monthly-refresh or private-split operations): follow-up needed before turning contamination recommendations into an implementation checklist." |
| G3 | `contamination-detection-and-transparency.md:9-14` (Claim) | "…it bounds only what that detector could see at its access level and contamination tier. … so an evaluation must state the detector, its access and tier scope, and keep a transparency record rather than report \"clean\"." — a *record* is required, never given a field set, an attachment point, or an artefact. |
| G4 | `contamination-detection-and-transparency.md:73` (apply row) | "\| Choosing a benchmark for a claim \| Prefer suites with a documented transparency card or auditable construction \| …" — the card is *named* here and nowhere defined. |

Two adjacent holders that the amendment must not silently absorb:

- `corpus/knowledge/benchmark-task-validity-checklist.md:40` (axis G) — "a per-task canary is embedded in the task files and checked mechanically" — and `:119-127` "**Not contamination measurement.** G reads a maintainer's canary practice *inside its own repository*; it is not a detector…". This is the lane's only canary bytes, and the card's Q2 cites S077 for exactly that canary (see seam R2 below).
- `corpus/knowledge/benchmark-task-validity-checklist.md:43` (axis J) — "the release gate is dated and states its hardware and check set" — the lane's only *dated-artefact* requirement, adjacent to R5/Q8.

Registry fact for (a): **S081–S086 are absent from `corpus/SOURCES.md`.** `grep -n -E '^\| S08[0-9]' corpus/SOURCES.md`
returns nothing; the registry's 82 rows end at S077–S080, S090, S091. So the amendment's six rows are a real
delta, not a re-use — and C1's `used-by` and `opened=2026-10-25` cells must be written this round, because the
card carries `verified-at: 2026-10-23` (card `:8`) and no registry row exists to inherit.

## (b) Field-by-field: new vs already held

Legend: **HELD** = the lane states the same requirement in its own bytes; **PARTIAL** = the slot exists but
the values/definition do not; **NEW** = no lane bytes state it.

| Card field | Card line | Lane status | Lane pointer and bytes |
|---|---|---|---|
| R1 Strata — per-stratum scores for a named stratification | `:32` | **NEW** | No lane entry requires stratified scores of a *benchmark's* contamination claim. The lane *practises* stratification in its own analyses — `grader-perturbation-audit.md:84` "Its format strata are FJ1 639/639…", `extraction-policy-comparison.md:100` "stratify by the format the policy acts on" — but never requires it of a third party's report. Practice ≠ field. |
| R2 Elicitation budget — identified harness + ≥2 of version/budget/attempts/attempt resolution | `:33` | **NEW** (adjacent to axis J) | `grep -rn -i 'elicitation' corpus/knowledge/*.md` → 0 hits. `budget` hits are the lane's own probe/token budgets (`probe-battery-r19.md:64`, `attrib-r21.md:273`), never a reporting field behind a published score. Nearest: `benchmark-task-validity-checklist.md:43` names hardware + check set for a *release gate*, not the model's elicitation budget. |
| R3 Contamination type tested — direct / derivative / temporal / distributional, each with the code observed | `:34` | **PARTIAL** | The slot is asserted, undefined: `contamination-detection-and-transparency.md:70` "contamination tier tested (T1–T4)". `grep -rn 'T1–T4' corpus/ SKILL.md` → one hit, that line; the four labels are never spelled out anywhere in the lane. `grep -rl 'derivative' corpus/knowledge/*.md` → 0. Card values are therefore new vocabulary resolving an existing undefined token. |
| R4 Regeneration status of the instrument used | `:35` | **NEW** | 0 lane hits for a regeneration *status* field (the `regenerat` hits are all round-8/12/14 internal-consistency machinery, e.g. `evidence/round12-fleet/r12-grader-notes.md:80`, not a disclosure field). |
| R5 Instrument currency — date of last substantive update | `:36` | **NEW** (adjacent) | `benchmark-task-validity-checklist.md:43` requires a *dated release gate* (S078 `v2/GATE.md` heading 2026-09-22); `benchmark-saturation-and-lifecycle.md:74` "Retire on reputation age; keep on a \"private split\" claim". Neither asks for "last substantive update" as a disclosable date. |
| S1 Acquired contamination, score-side, with elements in `notes` | `:42` | **NEW** | `contamination-detection-and-transparency.md:13-14` requires "a transparency record rather than report \"clean\"" but gives no attachment point; nothing in the lane distinguishes release-side from run-side records. `:22-26` of the card makes the split — that sentence has no lane counterpart. |
| S2 Card integrity — `controlled`/`not_controlled`/`unknown`, `unknown` valid | `:43` | **NEW** | The "unknown is a valid entry" *principle* is lane-held as a reporting rule (`QUALITY.md:36-42` Q4 "An indeterminate or detector-negative result is reported as such, never laundered into a positive"), but no lane bytes define a card-integrity field or its three values. |
| Q1 Which contamination type is claimed/tested | `:53` | **PARTIAL** | Same as R3 — the question is implicit in `:70`'s "tier", the four named types are new. |
| Q2 What detector access the reporter had | `:54` | **HELD (field), values partly new** | `contamination-detection-and-transparency.md:70` "Name detector family, model access (weights/logits/black-box), contamination tier tested (T1–T4), and what a negative cannot rule out" and `:9-11`. The card's enum adds "the training corpus, a public web index, or a canary" (its S077 clause). |
| Q3 Which tier and which datasets/subsets were tested, and the coverage limit | `:55` | **PARTIAL** | "tier tested" held at `:70`; dataset/subset coverage limit not held — `benchmark-task-validity-checklist.md:57-63` bounds that entry's own counts (1 of 89 task dirs), not a detector's dataset coverage. |
| Q4 What a negative result does **not** rule out | `:56` | **HELD** | `contamination-detection-and-transparency.md:9-11` ("does not establish that a model is uncontaminated…") and `:70` ("what a negative cannot rule out"); also `:49-50` falsifier clause. The card's two source-specific answers (S084, S086) are new *sources*, not a new field. |
| Q5 Is this artefact release-side or score-side? | `:57` | **NEW** | No lane bytes on where a contamination record attaches. `:71` ("require transparency records of training stages") is a *stage* requirement, not an attachment-side one. |
| Q6 Was the elicitation budget stated? | `:58` | **NEW** | Same evidence as R2. |
| Q7 Is the item set protected, and is there a refresh protocol? | `:59` | **PARTIAL** | The "Don't" half is held: `:73` "Treat a private/hidden split as proof of cleanliness" and `benchmark-saturation-and-lifecycle.md:74` same clause; canary practice is held at `benchmark-task-validity-checklist.md:40`. A published *refresh/retirement protocol* as a disclosable artefact is not held. |
| Q8 When was the instrument last regenerated / benchmark last substantively updated | `:60` | **NEW** (adjacent) | Same evidence as R4/R5. |
| Design rule 1 — procedural, not item-revealing (S082) | `:64-69` | **NEW** | `:73` presumes a "documented transparency card" exists; nothing in the lane states the disclosure boundary between procedure and live items. 0 lane hits for the S082 quotes. |
| Design rule 2 — a negative must be stated as a negative | `:71-77` | **HELD (principle)** | `contamination-detection-and-transparency.md:9-14` and `QUALITY.md:36-42` (Q4). The card adds the mechanism (S084/S086 blind-spot disclosure), which is new source material on a held principle. |
| Eastern precedent — S085 "方升" dynamic test bank | `:79-88` | **NEW** | `grep -rl '方升\|OpenCompass\|CAICT\|C-Eval' corpus/knowledge/*.md` → 0 files. No CJK benchmark-governance entry in the lane's 38 entries. |

Counts: **7 NEW fields/sections** (R1, R2, R4, S1, S2, Q5, design rule 1), plus **1 wholly new section**
(Eastern precedent) and **1 NEW-with-adjacent** (R5/Q8); **4 PARTIAL** (R3/Q1, Q3, Q7); **2 HELD as fields**
(Q2, Q4) plus **1 HELD as principle** (design rule 2).

## (c) Q6 verdict

**Verdict: expansion on ground the lane did not hold — not a duplicate — conditional on the amendment
naming `corpus/knowledge/contamination-detection-and-transparency.md` and declaring Q2/Q4 as restatements
of that entry's `:70` row.**

Reason, in the lane's own criterion. `corpus/QUALITY.md:50-53`: "**Q6 — extends, never duplicates or
overwrites.** The entry names the existing entry or coverage row it extends; a weaker entry is superseded by
a new entry that names it…". Two independent tests:

1. **Does the lane already hold card-format bytes?** No. `ls corpus/knowledge | grep -i card` → empty;
   `grep -rn 'transparency card' corpus/*.md corpus/knowledge/*.md` returns exactly `README.md:271`,
   `README.md:272` (the gap statement), `SOURCES.md:138` (the unopened lead) and
   `contamination-detection-and-transparency.md:73` (a preference, not a format). The round-29 rejection's
   competing artefact — "the campaign's own round 6 tabulated three published designs"
   (`corpus/lessons/round-29.md:223-226`, citing `benchmark-card-field-schema-2026-10-23.md:71`) — is
   **campaign-side, not lane-side**: `grep -rn 'card-field-schema\|card-design-arbitration' --include=*.md .`
   hits only `lessons/round-29.md`, `plans/round-30-claims.md` and `.ufo/waves/round-29/**`, i.e. prose about
   the staged file, never a landed lane entry. So within this lane there is no fourth-design rival to
   duplicate: the field set is new corpus bytes and would raise no existing entry's content.
2. **Does the card restate held bytes?** Partly — and this is the residue that keeps Q6 from being a clean
   pass on the card *as staged*. Q2 and Q4 (card `:54`, `:56`) are the `:70` apply row restated; design rule 2
   (`:71-77`) is the Claim at `:9-14` restated; the R3/Q1 slot is the undefined "T1–T4" token given content.
   That is 2 fields + 1 principle of overlap against 7 new fields + 2 new sections. Under Q6 ("extends…
   names the existing entry") this is an amendment, provided the admitted text says so. The card **as staged
   does not**: it has no `## Extends` heading, and its only provenance line is a `ground:` line at `:90` that
   explicitly refuses the job — "The card format and the Q1–Q8 gate are supplied here; the *admission* of the
   card against the lane's existing `knowledge/contamination-detection-and-transparency.md` vocabulary is the
   lane's call, not this entry's." (This is the same finding round 29 recorded at
   `R29a2RejectScan.md:66-69`: "the entry has no `Extends`/`## Extends` section at all … its `ground:` line at
   `:90` explicitly declines the extension".) The flip is therefore closed by the *lane's* admission text, not
   by the staged file.

So: **expansion, and the Q6 burden falls entirely on the admission step** — the amendment section must name
`contamination-detection-and-transparency.md:70` (and `:9-14`) and mark Q2/Q4 as restatements, or it lands as
the duplicate round 29 rejected.

## Adjacency defects the admission step must carry (else C1 lands a seam)

All four were recorded by round 29 (`R29a2RejectScan.md:43-50, 71-76`) and **none is fixed in the staged file**
(sha read today):

- **A1 — S077 cited in the body, absent from the source header.** Card `:54` cites "S077 (canary, per task)";
  the `source:` lines `:2-7` list S081–S086 only. S077 is already `mined` with a single-value
  `used-by` cell reading `corpus/knowledge/benchmark-task-validity-checklist.md` (`SOURCES.md:100`,
  last cell). C1's frozen predicate counts six cited rows for `used-by`, so leaving Q2's S077 clause in
  the admitted body without a seventh header line reproduces round-29's registry seam and will not be caught by
  the counter (`SOURCE_LINE_RE` reads source lines only).
- **A2 — "Q1–Q8" is a live label collision.** The card names its gate "Q1–Q8" (`:45`, `:47`, `:69`, `:90`);
  in this lane that range is the admission bar — `QUALITY.md:15` (Q1) … `:61` (Q8), now Q19, indexed as
  "Admission bar for knowledge entries (Q1–Q8)" at `README.md:115`. If the admitted entry keeps the label,
  `corpus/README.md` will carry two different Q1–Q8. Rename at admission (e.g. `C1–C8`).
- **A3 — `verified-at` is stale for this round.** Card `:8` reads `verified-at: 2026-10-23`, card `:9`
  "re-run the Gate commands for S081–S086 (ran 2026-10-23)". This round's access date is 2026-10-25 and C1
  requires `opened=2026-10-25` on all six rows; the admitted section must carry the new date, not the staged one.
- **A4 — no `Extends` section** (see (c)); plus the amendment must not overwrite the round-24 text —
  `QUALITY.md:51-53` "numbers are corrected by appended errata, never in-place edits", and
  `MERGE-REPORT.md` §Adopt checklist item 5: "**append** its content to the lane's existing
  `corpus/knowledge/<path>` as a dated amendment section. Do not replace the file".

## Remaining unknowns (not resolvable from lane bytes)

1. Whether S081–S086 each survive re-fetch with a ≤25-word byte-substring quote — this seat did not fetch them;
   the kill rule ("fewer than four of the six survive") is decided by the source seats.
2. Whether the staged `benchmark-card-field-schema-2026-10-23.md`'s three-design table is being admitted in a
   *later* round of this campaign. If it lands here, the amendment should cite it; if it stays staged, naming it
   would cite an unlanded working copy, which `QUALITY.md:56-58` (Q7) forbids. The safe lane-internal extension
   target today is `contamination-detection-and-transparency.md` alone.
3. Whether the card's Q2 canary clause (S077) should be dropped instead of sourcing S077 twice. Dropping it
   loses the lane's only per-task canary pointer inside the card; keeping it forces a 7-row `used-by` decision
   the C1 counter does not test. Main's call.
