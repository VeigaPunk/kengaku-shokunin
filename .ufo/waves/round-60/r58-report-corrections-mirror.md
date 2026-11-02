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

## ERRATUM (round 61, 2026-11-02 — the byte-fidelity correction; everything above this line stays as written)

The round-60 claim that this file mirrors the fleet working-tree append "byte-for-byte" is
FALSE at the byte level. Caught by the round-60 non-author closure (defect D1), re-measured
this round by byte comparison against the authoritative bytes (the append is still
uncommitted in the fleet working tree at the measurement; fleet HEAD and both sha256s are in
the receipt `.ufo/waves/round-61/mirror-fidelity-receipt.txt`):

1. ENCODING DEFECT — the append's 9 non-ASCII characters (5 em-dashes U+2014, 4 arrows
   U+2192) are cp1252-double-encoded here: each UTF-8 triple was mis-decoded as
   windows-1252 and re-encoded, producing 27 mojibake characters — the em-dash class as
   byte triple `C3 A2 E2 82 AC E2 80 9D` (a-circumflex + euro + right-double-quote) and the
   arrow class as `C3 A2 E2 80 A0 E2 80 99` (a-circumflex + dagger + right-single-quote);
   5 em-dash-class and 4 arrow-class sequences in this file. Grounding: the WHATWG
   windows-1252 index (S225, capture
   `corpus/evidence/round61/whatwg-windows1252/index-windows-1252.txt`) maps cp1252 byte
   0x80 to U+20AC (:7), byte 0x86 to U+2020 (:13), byte 0x92 to U+2019 (:25), byte 0x94 to
   U+201D (:27), and byte 0xE2 to U+00E2 (:105) — exactly the mis-decode that produced
   these triples. First differing byte against the authoritative append: byte 39, line 2.
2. LINE-COUNT DEFECT — the block between the MIRROR markers measures 27 newline-terminated
   lines against the append's 26: one surplus trailing blank line.
3. THE CORRECTION — the byte-true mirror of record is
   `.ufo/waves/round-61/r58-report-corrections-append-byte-true.md`: byte-identical to the
   authoritative append (26 lines, 2141 bytes, sha256
   `2a2f952ca9809c426d91ec22feb3713fb485e0d7e393dea0fd3cecf939af2a21`; the fidelity
   receipt's cmp leg prices it). It carries no header: the file IS the append, so byte
   verification needs no marker-stripping step — the step whose absence hid this defect.
4. STATUS DOWNGRADE — this round-60 file is the CONTENT-mirror of record (every line
   present; the encoding defect and surplus blank stay uncorrected above by the
   append-only rule); the BYTE-mirror of record is the round-61 file. A future byte-fidelity
   claim cites a byte-compare receipt, never prose.
