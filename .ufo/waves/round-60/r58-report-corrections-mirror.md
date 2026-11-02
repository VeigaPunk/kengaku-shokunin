# kengaku round 60 — byte-mirror of the round-58 report erratum append (fleet working tree)

author: kengaku L1 (round 60, 2026-11-02). The round-59 non-author closure routed defect 1:
the round-59 report's claim that cosmetic corrections were 'mirrored into the round-58
report's `## Corrections (round 59)` section' points at an append that exists ONLY in the
fleet repo's working tree (uncommitted). This lane may not mutate the fleet root (the round
contract makes fleet commits the orchestrator's), so the append is mirrored here byte-for-byte
and the fleet-root landing is ROUTED to the orchestrator in the round-60 report.
Mirror source: `git -C <fleet-root> diff HEAD -- .ufo/reports/round-58/kengaku.md` at the
round-60 working state (fleet HEAD a286489a, 26 inserted lines, verified uncommitted).
Every line below the marker is the working-tree append with the leading `+` stripped.

=== MIRROR (fleet working-tree append, byte-for-byte) ===


## Corrections (round 59, 2026-11-02 â€” appended by the round-59 author per the r58 closure's routed items; the text above stays as written)

1. **The "Sources & frontier" bullet says the round-58 lesson mines "three rows"; the landed
   lesson has FOUR.** The fourth row (the registry-advertisement mistake) was added at wave F2
   after this report's prose was drafted â€” an honest progression, recorded by the r58 closure
   as status-neutral. Counting command: `grep -cE '^\| (freeze|landing|fixture authoring) '
   corpus/lessons/round-58.md` â†’ 4 at the round-59 tip. The LOG close entry's mistakes list
   names three classes for the same table â€” the same undercount, corrected in the round-59
   LOG.
2. **The quality trend below says the repair cascade "broke six tip-counter surfaces"; the
   round-58 LOG close entry says "broke four tip counters".** Both are true under their own
   counting units and the one-evening timeline: the LOG entry (written at wave E) counted the
   four counter legs red BY THEN (round36-c2 W4; round51-routing vocabulary + the two landed
   check fields; r40 a_tok uniqueness; round-close E11); this report counted the six defect
   SURFACES the cascade exposed by the final tip (the four above plus the registry
   advertisement of the repaired checker, which went red only at the wave-F2 final-tip
   capture â€” with the two check fields counted as one surface). One counting unit per claim:
   "counter legs red" vs "defect surfaces caught". Re-derive: `grep -c 'broke four tip
   counters' LOG.md` (lane) â†’ 1; `grep -c 'broke six tip-counter surfaces'` in this file â†’ 1.
3. **The five receipt paths cited above and in the landed round-58 prose were never committed
   (the closure's finding (a))** â€” discharged at kengaku `5420eac9` (round-59 wave R): each
   instrument re-run green at tip `e0cfa97a` and landed at its cited path under a dated
   re-landing header; the finding-(b) exit-label bug is corrected by the dated erratum
   appended to `recon/esc-falsifier-fixed-checker.txt` (kengaku `85ef87e`), with the
   receipt-consistency gate's redâ†’green receipts as the record.

=== END MIRROR ===
