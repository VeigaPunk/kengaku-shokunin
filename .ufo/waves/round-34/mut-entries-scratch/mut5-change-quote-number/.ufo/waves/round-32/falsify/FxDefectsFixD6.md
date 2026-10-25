# Round 32 falsify — D6 lesson locator corrections

VERDICT: d6-closable

## Evidence

The frozen C2 predicate routes R6 to two append-only lesson corrections (`plans/round-32-claims.md:69-72`). The current lesson bytes do not yet contain either correction: round-31's Gate source table still gives the precedence docstring as `:35-38` (`corpus/lessons/round-31.md:57`); round-30's round-31 erratum still cites `contamination-transparency-card.md:78-81` (`corpus/lessons/round-30.md:195-200`). The stale strings must remain because the corrections are append-only.

Build draft `R32DraftErrata.md` proposes these exact appended lines:

- Append to `corpus/lessons/round-31.md`:

  `> **Correction (round 32):** The \`verifier_mode.py\` precedence locator in the Gate source table is \`:39-40\`, not \`:35-38\`; the earlier \`:35-38\` reference is superseded.`

- Append to `corpus/lessons/round-30.md`:

  `> **Correction (round 32):** The earlier erratum entry line references \`corpus/knowledge/contamination-transparency-card.md:78-81\` are stale. The relevant entry locations are \`:72\` and \`:82-83\` in that entry; these corrected references supersede \`:78-81\`.`

R6's code (`plans/round32_defects.py:144-173`) explicitly requires the old `:35-38` to remain, the updated `verifier_mode.py` and `:39-40` within 300 characters, and correction/superseded labeling. For round 30, it requires the old `:78-81` to remain, both `:72` and `82-83`, their co-occurrence within 300 characters, and a corrected/superseded label. I ran a predicate simulation by appending only the two draft lines in memory to current lesson texts: **R6 simulation green**. Running the actual check on the unmodified lesson tree reports the expected missing update (`no appended correction updates verifier_mode.py's precedence locator to :39-40`); no lesson was edited.

The draft's exact append lines satisfy these predicates while preserving all superseded bytes. This verdict closes D6 at the planned-correction level only; the corrections are still drafts on disk, not landed append-only lesson edits.
