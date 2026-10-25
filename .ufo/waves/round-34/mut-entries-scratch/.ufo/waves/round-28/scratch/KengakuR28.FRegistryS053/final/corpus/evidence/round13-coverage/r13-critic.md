# R13Critic — bounded coverage claim under adversarial review

Steered round 13 re-dispatch, 2026-10-15; advisory L2 only. Read-only review apart from this artifact. Baseline: `3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf`. This is not a canonical Rust judgment, admission, promotion review, or outside non-author learning spot-check. No builds, tests, smoke runs, endpoint requests, or repeated absence checks were run.

## Scoped conclusion

The strongest defensible claim is **better source-status coverage and corpus discovery over a fixed, bounded population**, not more available research sources or a higher coverage score. Explicit historical-unavailable annotations can remove an ambiguity a reader previously faced, and indexing the already-existing round-16 lesson removes a real discovery defect. The existing rubric makes these relevant to coverage: `SCORECARD.md:243` names bidirectional indexing and contradictory gaps, while `AXES.md` defines coverage as governed surfaces. They also touch freshness/calibration, but documenting that relationship does not justify extra axis-moves or double-counted gains.

**Unmarked 12→0 plus equal index counts alone does not prove the claim.** It supports the claim only if the same twelve paths remain in scope, annotations accurately distinguish retained digest text from missing original bytes, and exact file/index membership—not just totals—closes on a named delivered revision. Even then it proves annotation/discovery improvement, not expanded domain knowledge. The declared-but-unresolvable-source cap remains; the legacy coverage anchor stays **7**. Novelty also remains 7; no new model result or source-restoration claim follows.

Coverage is a defensible tie choice because this particular defect can be corrected and measured without the missing services. It is not justified by claiming novelty is impossible in all hermetic work: `SCORECARD.md:250-259` already describes a future novelty instrument, and the old round-13 ack audit used retained responses. Those stronger scientific legs are outside this continuation. The narrower rationale is that this selected coverage defect has an inspectable baseline and a falsifiable, source-independent correction now.

## Evidence and counterexamples

### 1. Frozen denominator versus convenient rescanning

**Evidence:** `surface-receipt.json:45-59` fixes twelve named candidate files using a first-twelve-lines source regex. `baseline-initial.json:2-25` independently records the baseline revision, twelve unmarked files, knowledge 23/23, and lessons 18/17 with `round-16-recensus.md` missing. The earlier round-16 lesson's `:34` instead reports 61 live citations and 17 knowledge source lines under a wider audit.

**Concrete disconfirmation [INFERENCE, not an executed mutation]:** prepend enough metadata to move a wiki citation below line twelve, rescan the edited files, and the candidate disappears. A purported 12→0 unmarked result could then be a denominator shrink rather than twelve corrected files. Likewise, counting only entries that now have a `source:` key excludes `eval-design-digest-3.md`, whose original source list is at `:6-11`.

**Impacted axes:** coverage, calibration.

**Smallest safe correction:** load the receipt's literal twelve paths for both revisions; report missing candidates separately, never remove them from the denominator. Record zero unmarked **of the same twelve**. Keep the broader 61/17 audit as motivating carried debt, not a denominator allegedly closed by this census. The first-line regex is a selection rule, not a census of every source-bearing entry.

### 2. Equal counts can conceal an undiscoverable artifact

**Evidence:** `baseline-initial.json:5-7` identifies exact missing membership, not merely a one-row deficit. The receipt's initial lesson population is 18/17; the inherited `round-13-coverage.md` is another existing working-tree lesson describing this continuation. `corpus/README.md:35-51` was the seventeen-row lesson index when read.

**Concrete disconfirmation [INFERENCE]:** eighteen lesson files and eighteen rows can still hide the round-16 lesson if another row is duplicated or points to a nonexistent lesson. Knowledge 23/23 can similarly conceal one missing file plus one dangling row. New advisory artifacts also increase the evidence inventory after an early census.

**Impacted axes:** coverage, calibration, durability-related operability.

**Smallest safe correction:** require exact set differences in both directions and identify duplicate rows; disclose whether evidence is indexed per-directory or per-file. Capture final membership after all advisory artifacts exist. Count the new lesson as new output, not as a second pre-existing missing lesson; close the pre-existing `round-16-recensus.md` gap explicitly. Directory indexing does not prove every nested artifact has been individually reviewed.

### 3. Source-status tokens are not source availability or provenance

**Evidence:** the surface receipt observes eight exact paths absent and `/health` ECONNREFUSED at its stated timestamp, with limits at `:74-78`; it does not search the entire host or refetch public URLs. `eval-theory-notes.md:3-6` is a retained digest of wiki pages, not the pages themselves. `r14-scout-surfaces.md:209-218` retains six MD5 strings of then-present external files; those strings are not the external files. `round-16-recensus.md:38` explicitly says no missing-file content hash of the unit/jinja was found.

**Concrete disconfirmation [INFERENCE]:** a marker-only checker could accept `source-status: historical-unavailable` alongside `verified-at: 2026-10-15` and an unqualified `original bytes retained` assertion. The token count improves while the reader receives false freshness or provenance. Replacing an unavailable wiki citation with this corpus's own digest also makes a pointer resolve without restoring independent authority.

**Impacted axes:** coverage, freshness, calibration, depth.

**Smallest safe correction:** distinguish the historical content-read date from the current availability-check date; retain original paths and identify the actual in-repo evidence type. Say `digest text retained; original source bytes unavailable at the checked path`, or `historical digest string retained; original bytes not recovered`, as applicable. Never invent unit/template hashes, infer a live model identity from pid 1299, or equate connection refusal with a global absence of serving processes. A manual semantic review must complement a marker count.

### 4. Baseline revision versus inherited, later-created artifacts

**Evidence:** the review ran only this baseline-membership inquiry:

`git ls-tree -r --name-only 3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf -- corpus/evidence/round13-coverage corpus/lessons/round-13-coverage.md corpus/lessons/round-16-recensus.md`

Its sole output was `corpus/lessons/round-16-recensus.md`. The surface receipt and inherited coverage lesson were readable in the working tree but are not blobs at the named baseline. This does not by itself determine their current tracked/untracked status. The independent `baseline-initial.json` correctly describes a retrospective census using `git ls-tree`/`git show` against that revision.

**Concrete disconfirmation [INFERENCE]:** describing all currently present inherited artifacts as committed baseline evidence falsely makes the new lesson or surface receipt look recoverable from `git show BASE:path`. Ignoring inherited artifacts at final close produces another uncommitted-evidence hole.

**Impacted axes:** calibration, coverage, evidence durability.

**Smallest safe correction:** distinguish **baseline tree census**, **later host observation**, and **delivered revision**. Record the host receipt as a timestamped observation associated with the work, not as a file present at baseline. Land inherited/new round artifacts under the parent's ownership policy before claiming durable closure.

### 5. Self-referential revision citations

**Evidence:** the baseline is immutable and independently named. Parent's integration message proposes an implementation+LOG commit followed by a record-only commit citing the measured implementation SHA. That addresses the design risk; it is not yet evidence of landed commits in this review.

**Concrete disconfirmation [INFERENCE]:** a document inside commit X claims it was measured at X, but inserting X's final hash changes the document and therefore X. Substituting `HEAD` later silently changes which tree was actually measured. Measuring a working tree while reporting the preceding clean commit is another false baseline.

**Impacted axes:** calibration, operability/reproducibility, coverage evidence.

**Smallest safe correction:** retain the parent's two-commit approach. Name the implementation revision in post-measurements and make the later receipt/scorecard record-only revision explicit. If later edits change source annotations, the README index, or census logic, they invalidate measurements of the earlier implementation for those changed claims. Separate report durability from the tree measured by the census.

### 6. Repeated round 13 is not permission to erase rounds 13–16

**Evidence:** `round-13-coverage.md:3-4` expressly identifies a re-dispatch, while `LOG.md:20` records historical ack-state work and `LOG.md:24-29` identifies round 16. The existing fleet `.ufo/reports/round-13/kengaku.md:1-25` is the historical novelty/ack-audit plan; `.ufo/reports/round-16/kengaku.md:47-55` carries absent-source debt and serving-plane routing. Both files were read, not edited. The parent reports preservation of the prior round-13 report SHA and append-only continuation intent.

**Concrete disconfirmation [INFERENCE]:** replacing the old report with a better-shaped current report makes an earlier incomplete record disappear and can make an old citation mean new work. Calling this round 17 instead would also change the explicit steered identity. Editing frozen probe defaults just to drive down the old broad audit count trades apparent coverage against byte/provenance integrity.

**Impacted axes:** calibration, coverage, operability, adjacency.

**Smallest safe correction:** append a dated `round 13 re-dispatch / source-availability coverage continuation` section, preserve filed report/LOG/lesson prefixes and later-round records, and cite the actual new work commit only after it exists. Keep archived probe bytes intact and explain current replay entry points in living documentation. Route serving-plane restoration to the current owner/operator, not kengaku. This seat edits no report outside the lane.

## Fixable defects versus impermissible trades

The denominator, duplicate-row, provenance-label, revision-citation, and continuation-label issues above are fixable without expanding this task. None requires source recovery or new traffic. If they remain, the proposed numerical deltas cannot establish the claimed bounded improvement.

Deleting absent surfaces to evade the cap, dropping candidates, laundering digests as originals, changing archived experiment bytes, overwriting a filed report, or replacing outside review with nine lane-dispatched opinions are not harmless presentation choices. They sacrifice another authority or evidence obligation for a cleaner metric; such a trade must be exposed to the canonical judgment, not waved through by this advisory critique. The actual canonical Rust judge is not invoked by this seat.

## Precise report wording

Use the following only after the parent obtains the stated delivered-revision measurements; this review does not supply an after-run result:

> This is the 2026-10-15 steered round-13 source-availability coverage continuation; earlier round-13 ack-state work and rounds 14–16 remain historical records. A retrospective tree census of baseline `3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf` found 12 unmarked entries in the receipt-fixed twelve-file source population, knowledge index membership 23/23, and lessons 18/17 with `round-16-recensus.md` missing. At the separately named measured implementation revision, the same twelve entries have zero unmarked source-availability headers, and the census records exact bidirectional index membership, duplicates, and added output separately. This is a bounded correction to historical-source labeling and discovery, not evidence of recovered original bytes, live source availability, new model results, novelty, or closure of round 16's wider 61-citation audit. The unavailable-surface cap continues to hold the legacy coverage anchor at 7; no score increase or axis retirement is claimed. Receipt creation time, measured revision, and later record-only commit are distinct. No outside non-author learning or promotion review occurred.

Fair limit: a zero marker count and complete index can coexist with incomplete domain coverage, unresolved wider historical citations, and unavailable external sources. That is not a reason to deny the narrow corrective value; it is a reason to state exactly what improved and leave the remaining caps and debt visible.
