# Lessons — round 14 (an unlanded round is not a round)

Source: round-14 pre-landing state at child HEAD `e171cdf`; verification under
`corpus/evidence/round14-fleet/`; `LOG.md` rounds 12–14.

Rounds 12 and 13 completed substantial work but left it uncommitted. At the
start of round 14, `LOG.md`, `SCORECARD.md`, and `corpus/README.md` still ended
at round 11; the r12 ladder/fleet and r13 audit directories were untracked.

Consequences:

1. **Uncommitted evidence is not durable evidence.** The r12 verdicts existed
   only in one checkout. A fresh clone could neither discover nor replay them.
2. **A cold agent follows the index.** With no README rows or knowledge/lesson
   entries, two rounds were invisible to the exact consumer the corpus serves.
3. **Unlanded artifacts rot.** `analysis_r12.md` was regenerated after drafts
   recorded its hash. The drafts carried `ddfe60d2…`; the landed bytes are
   `029c3bcd…`. The generator also embeds an absolute path, preventing byte
   identity across path casing while leaving statistics unchanged.
4. **Debt compounds.** Round 12 needed shadow report/log/doc-delta artifacts;
   round 13 then stacked another unlanded directory on top.

Round closure checklist:

1. Commit the round's evidence; no round-owned `??` paths remain.
2. Append one evidence-first LOG entry with re-measured counts.
3. Record the before→after axis move in SCORECARD.md.
4. Keep README rows equal to files/directories in both directions.
5. Land knowledge and lesson entries for the result.
6. Re-pin hashes from the bytes being committed, never from a draft.
7. Run the changed gate against the landing tree; commit its replay layer in
   the same round as the evidence it governs.

Round 14 also closes a concrete gate gap: `grader.py` now md5-pins
`analysis_r12.md`, taking the replay from 732 to 733 checks.
