# RevM19Critic — kaika-W3 dispute of lesson row M19 (round-25 kengaku, read-only)

Axes: calibration (assigned) + landing/append-only integrity of the disputed row. Scope: M19 only; no lane-tree writes; base `6180e4fb92e9` (note unchanged since base; `git diff base -- <note>` empty).

## Dispute
`.ufo/waves/kaika-w3/kengaku-critic.md:11`: M19's "left unmarked" is false because the r23 note self-dates to 13:33Z mid-flight (`2026-10-16-round23-stream-surface.md:9-14,149-157`) and says receipts supersede it (`:22-23`) — a time-bounded observation, not an unmarked current premise.

## Evidence (commands + output)
1. All three kaika anchors are verbatim-true: note `:9` "written at 13:33Z with the wave **mid-flight**: no round-23 artifact has landed"; `:22-23` "Where the round's landed receipts disagree, they supersede this note"; `:149-154` "The r23 premise is unconfirmed at this note's write time … the round's landed receipts supersede it."
2. Receipts overtook the note: `corpus/evidence/attrib-r23-stream.log:233-239` (GT counts; `ACCURACY: 30/30 = 1.000 … -> PASS`; `STREAM TARGET opencode-go … -> FAIL`); first GT read stamped `:194` = 2026-10-16T13:49:42Z.
3. Timeline: `git log -1 --format=%cI 3358c4d` → 2026-10-16T11:23:19-03:00 (=14:23:19Z, receipts commit `f9337d5` 14:22:45Z); M19's "14:23:19Z, after the 13:49:42Z score block" reproduces.
4. M19 as landed, `corpus/lessons/round-24.md:29` (identical at base): "left unmarked after the receipts landed … the file was committed `3358c4d` at 14:23:19Z"; captured-by none; fix = dated erratum in the same file. Class row `:41` (LAND, uncaptured 5); totals `:46` (20/3/3/2/12 — per-class lists sum to 21 vs 20: adjacent count slip, context only).
5. The row's rule is round-24-fresh and on point: `corpus/QUALITY.md:90` **R5** — superseded premise gets a dated erratum naming the receipt; check = stale sentence present AND `erratum|superseded` line citing the receipt. The r23 note has only a generic receipt-less supersede clause; the erratum is still unpaid, and the receipt it must cite is in-repo (`attrib-r23-stream.log:233-239`).
6. Adjudication history: kaika kengaku-review verified only the count (`kengaku-review.md:42` `C2.lesson_mistake_rows absent→20`), no M19 diagnosis check; dispute first raised by the W3 critic.

## Adjudication — PARTLY
- **Kaika critic right (this half):** "left **unmarked**" is false as written — self-date + supersede clause + named leftover bound the premise to 13:33Z; no reader at commit time (14:23:19Z) mistakes it for a current claim.
- **M19 survives, narrowed:** the R5 erratum obligation is real and unpaid — the generic supersede line does not name the receipt, so R5's receipt-citing erratum is absent; the R5 closure criterion is open at base.
- **Defect in the row, not the finding:** M19's evidence cell proves only that the note was committed after the receipts were in-repo (commit time ≠ author knowledge at the 13:33Z write). What stands: the receipt-naming erratum was owed after landing and was not written. Fix the evidence cell, not the row.

## Proposed append-only correction (round-25 lesson `## Mistakes` / corrections; old rows byte-identical per R1)
```
## Correction to round-24 M19 (append-only, 2026-10-20)
M19 (corpus/lessons/round-24.md:29) is narrowed, not withdrawn. The kaika-W3 dispute
(.ufo/waves/kaika-w3/kengaku-critic.md:11) is right that "left unmarked" overstates: the r23 note
self-dates its mid-flight write at 13:33Z (2026-10-16-round23-stream-surface.md:9), bounds the absence
to that time (:9-14, 149-154), and says landed receipts supersede it (:22-23). What stands is the R5
obligation (corpus/QUALITY.md:90): a dated erratum naming the overtaking receipt; the note carries only
a generic receipt-less supersede clause (grep -nE 'erratum|superseded' <note> hits no receipt-naming
erratum; checked 2026-10-20 at base 6180e4f). M19's evidence cell is corrected: commit `3358c4d`
14:23:19Z (after the 13:49:42Z score block, attrib-r23-stream.log:194) proves the note was committed
after the receipts existed without the R5 erratum — not that the author knew at the 13:33Z write.
Recompute: git log -1 --format=%cI 3358c4d; grep -n '13:33Z' <note> -> :9,:151; grep -nE
'erratum|superseded' <note>. The R5 erratum on the r23 note itself remains open (a writer seat appends
one dated line naming attrib-r23-stream.log:233-239; never rewrite :9-14/:149-157). Class row (:41) and
totals (:46) unchanged; adjacent count slip (lists sum 21 vs 20 at :41,:44,:45,:46) noted, not reclassified.
```

## Residual risks
- R5's grep is satisfiable by the note's existing generic "supersede" word; require the receipt path inside the erratum line (prose already demands it).
- The R5 erratum on the r23 note is a writer-seat write, outside this read-only seat's scope; supplied as placement note above.
- Per-class total mismatch (21 vs 20) needs its own M-row treatment by the round-25 tally seat.

VERDICT: M19 is PARTLY a real mistake — R5 erratum stands unpaid, "unmarked" overstated; append-only correction proposed; no installs (git/coreutils only).
