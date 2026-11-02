
## Corrections (round 59, 2026-11-02 — appended by the round-59 author per the r58 closure's routed items; the text above stays as written)

1. **The "Sources & frontier" bullet says the round-58 lesson mines "three rows"; the landed
   lesson has FOUR.** The fourth row (the registry-advertisement mistake) was added at wave F2
   after this report's prose was drafted — an honest progression, recorded by the r58 closure
   as status-neutral. Counting command: `grep -cE '^\| (freeze|landing|fixture authoring) '
   corpus/lessons/round-58.md` → 4 at the round-59 tip. The LOG close entry's mistakes list
   names three classes for the same table — the same undercount, corrected in the round-59
   LOG.
2. **The quality trend below says the repair cascade "broke six tip-counter surfaces"; the
   round-58 LOG close entry says "broke four tip counters".** Both are true under their own
   counting units and the one-evening timeline: the LOG entry (written at wave E) counted the
   four counter legs red BY THEN (round36-c2 W4; round51-routing vocabulary + the two landed
   check fields; r40 a_tok uniqueness; round-close E11); this report counted the six defect
   SURFACES the cascade exposed by the final tip (the four above plus the registry
   advertisement of the repaired checker, which went red only at the wave-F2 final-tip
   capture — with the two check fields counted as one surface). One counting unit per claim:
   "counter legs red" vs "defect surfaces caught". Re-derive: `grep -c 'broke four tip
   counters' LOG.md` (lane) → 1; `grep -c 'broke six tip-counter surfaces'` in this file → 1.
3. **The five receipt paths cited above and in the landed round-58 prose were never committed
   (the closure's finding (a))** — discharged at kengaku `5420eac9` (round-59 wave R): each
   instrument re-run green at tip `e0cfa97a` and landed at its cited path under a dated
   re-landing header; the finding-(b) exit-label bug is corrected by the dated erratum
   appended to `recon/esc-falsifier-fixed-checker.txt` (kengaku `85ef87e`), with the
   receipt-consistency gate's red→green receipts as the record.
