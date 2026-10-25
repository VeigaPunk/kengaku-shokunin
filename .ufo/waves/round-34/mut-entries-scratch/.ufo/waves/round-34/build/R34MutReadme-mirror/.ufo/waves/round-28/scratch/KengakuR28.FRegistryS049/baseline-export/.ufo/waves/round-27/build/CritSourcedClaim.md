# CritSourcedClaim — round 27

## Counterexample and evidence

- **No round-27 source support is present in the observed lane tree.** `corpus/SOURCES.md` ends at S048 (lines 65–70); S044/S045 have `opened=2026-10-21` but their `used-by` is the round-26 lesson/audit (lines 66–67). The C1 entry `corpus/knowledge/extraction-policy-comparison.md` and `corpus/evidence/round27-sources/gate.md` both returned “not found.” Therefore, an entry citing only S044/S045 would rely on round-26 rows, not rows opened for C1 this round.
- The frozen requirement is explicit: the C1 entry cites rows opened this round **for each harness policy it names**, with URL, access date, and a located ≤25-word quote in `corpus/evidence/round27-sources/gate.md` (`plans/round-27-claims.md:73–83`). The named examples are lm-evaluation-harness `regex`/`group_select`, inspect_ai `match`/`pattern`, and OpenAI simple-evals answer regexes (`:73–76`).
- S044 is scoped to xFinder’s regex-extraction motivation/learned extraction, not the named harnesses’ implemented selection semantics (`corpus/SOURCES.md:66`). S045 is scoped to evalmut’s equivalent/defect mutations, not those extraction policies (`:67`). The older entry uses them accordingly for adjacent extraction research and grader mutation testing (`corpus/knowledge/grader-perturbation-audit.md:18–22`). Re-citing or merely re-opening them cannot establish the three specific harness behaviors.
- The tier rule is substantive: a load-bearing claim needs ≥1 A/B row scoped to that claim; C cannot stand alone (`corpus/SOURCES.md:11–17`; `corpus/QUALITY.md:24–33`).

## Minimum safe source set

- **External implementation/prior-art claim:** add at least **three new rows**, one per named harness/policy claimed. Prefer **Tier A** official documentation or version-pinned upstream source code, with each row narrowly scoped to the exact behavior (e.g. first/last match or fence/whole-output behavior actually evidenced). A strong, reproducible **Tier B** source can meet the floor where primary material is unavailable; Tier C alone cannot. Record each opening and exact quote/location in the round-27 `gate.md` as preregistered. Do not claim semantics broader than the source shows.
- **C1’s measured lane result:** add **one new Tier A own-work row** for the committed, re-runnable parser-policy instrument/output and its pinned population. External harness docs cannot substantiate the 1964-response result; S044/S045 cannot either. This follows the registry’s Tier-A scope for the lane’s own re-runnable gate output (`corpus/SOURCES.md:11–17`).
- Thus, for the currently preregistered three-harness comparison and a result-bearing knowledge entry, the minimum is **four new rows: three external A rows + one own-work A row** (or three scoped B rows in place of the external A rows, plus the own-work A row). The next available ID is S049. The external rows make prior-art claims real; the own-work row sources the measurement. S044/S045 may remain as earlier, adjacent context, not substitutes.

**Impacted axis:** novelty only. This sourcing correction supports the scoped construct and prior-art account; it does not justify novelty credit by itself.

**Smallest safe correction:** before admitting C1, open and register one direct source per named harness plus the lane’s result-bearing gate output; cite those new rows in the entry, preserve S044/S045 only for their actual scopes, and retain the required round-27 opening evidence. No installs.

VERDICT: C1 is not yet sourced by this-round rows; S044/S045 alone are insufficient. Four scoped new rows (3 external A/B + 1 own-work A) are the minimum for the preregistered three-harness, result-bearing claim.