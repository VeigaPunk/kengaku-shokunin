# FxEntryCoverage — grader-perturbation-audit draft vs Q6/Q7 ground, entries, map

Lane /home/vgpnk/Projects/shokunin/kengaku-shokunin. HEAD `3a2aeb1` (draft retained unadmitted);
`git status --porcelain` = 21 dirty; draft `.ufo/waves/round-26/drafts/grader-perturbation-audit.md`
has +18/−5 uncommitted (`git diff --stat`), so line refs below are to the working-tree draft.
README.md clean at HEAD; anchors valid.

## Verified ground (commands + output)

1. `grep -c "Grader robustness|response-format" corpus/README.md` → 0 matches. The coverage map
   (README.md:218-231) has no row **Grader robustness / response-format invariance**.
2. `git ls-files .ufo/waves/round-26/falsify/` → empty (0 files tracked); `git ls-files
   corpus/knowledge/ | grep -c grader-perturb` → 0, exit 1. Entry `corpus/knowledge/grader-perturbation-audit.md`
   NOT admitted — matches process state.
3. Population recount (`python3` jsonl scan of the four pinned files): round8 188, round9 128,
   round11 320, round12 1328, total 1964; ok-true 125+75+136+685 = 1021 PASS / 943 FAIL. Matches
   draft §Population exactly.
4. Draft §Results arithmetic: Σ family n = 1819+1819+1964+1720+1964+1964+1876+1021+1021 = 15168 ✓
   (audited-verdict total is n-sum, not k-sum); 909 PC separate ✓.
5. Duplication: `knowledge/llm-judge-calibration.md` perturbation text is S009/S010 judge ordering
   (:25-30), 0 hits for grader.py/invariance; `knowledge/attribution-interval-calibration.md` 0 hits
   for perturb/grader.py/invariance. No existing entry holds this ground.
6. Novelty posture: draft states "This is not a new method", holds 7, cites S048/S045 — no global
   method-novelty premise. Compliant with round-26 Amendment 1 item 6.

## Findings

**F1 (major, Q6 uncovered-ground as worded).** Draft Claim-and-scope: "extends `knowledge/llm-judge-calibration.md`
and the coverage-map row **Grader robustness / response-format invariance**". The named row does not
exist (check 1). Q6 (`corpus/QUALITY.md:50-55`) requires naming "the existing entry or coverage row it
extends"; the existing-entry leg is satisfied, the coverage-row leg asserts ground that isn't there.
Repair at admission: either (a) the entry sentence says it *adds* that row (extending the existing
"Judge calibration" row, README.md:227), or (b) names only the existing row/entry. Landing the current
sentence verbatim with a new row satisfies discoverability but misstates the extension relation.

**F2 (major, Q7/Q13 support timing).** Draft cites `.ufo/waves/round-26/falsify/FxFamilyD1.md` as
independent re-derivation of D1 figures; falsify dir has 0 tracked files (check 2). Q7
(`QUALITY.md:56-59`) forbids support resting on an unlanded working copy; Q13 + the prereg require the
admission commit's tree to contain the named second-seat reports and the Gate cell to name them by
path. Other support paths verified tracked: plans/grader_perturb.py, plans/fixtures/r26/{perturb_population.tsv,perturb_oracle.py},
.ufo/waves/round-26/build/ConnTameshi.md, corpus/evidence/round8-horizon/critic-defects.md (git ls-files → 1 each).

**F3 (minor, registry convention).** SOURCES S044/S045/S046/S048 used-by = `corpus/lessons/round-26.md`
only (SOURCES.md:66-70); draft `source:` line makes them load-bearing for the entry. Precedent: S011's
used-by gained `corpus/knowledge/attribution-interval-calibration.md` at that entry's admission
(SOURCES.md:33). At admission, append the entry path to those four rows' used-by. Whether a Q criterion
strictly mandates this is unobserved (rule text names tiers, not used-by); precedent only.

## Exact README.md changes required in the admission commit (Q7 same-commit set)

- **D1 index row**: insert between README.md:61 (`knowledge/attribution-interval-calibration.md`, last
  knowledge row) and :62 (`lessons/round-1.md`): `` `knowledge/grader-perturbation-audit.md` | <covers
  text: byte-pinned 1964-record response-format audit of grader.py; MP/MC/PC split; MULTI 14/31
  counterexample> | S044, S045, S046, S048 — `corpus/SOURCES.md` rows; own-work `plans/grader_perturb.py`, `corpus/evidence/round26-calibration/` ``.
- **D2 coverage-map row**: add with name exactly **Grader robustness / response-format invariance**
  (must match the draft's reference verbatim for Q6/Q7 discoverability). Recommended placement after
  :228 ("Instrument interval calibration") to keep the judge-calibration cluster; phrasing per :228
  precedent: "covered at measured depth (round 26) — knowledge/grader-perturbation-audit.md; sources
  S044–S046, S048; own-work instrument. Extends the Judge calibration row's `grader.py`-outputs half;
  method held at novelty 7 (evalmut S045 prior art)."
- **D3 Frontier**: under "**Judge calibration applied inward**" (README.md:255) append a discharge
  sub-bullet following the :256 append-only precedent, stating the grader.py-outputs + S010-style
  perturbation half is discharged by the new entry, scope and limits included. Must not leave :256's
  "grader.py outputs and an S010-style perturbation audit remain frontier" as the live claim —
  round-25 falsify precedent (build/CritTrends.md:22-25): not left duplicated in both places.
- No change needed to README.md:267 (round-26 artifacts row already lands the instrument) or to
  llm-judge-calibration.md (Q6 needs no edit to the extended entry; r25 appended corrections were
  defect-driven, not Q6-mandated — unobserved as a requirement here).

## Residual risk / gaps

Numbers-vs-oracle equality, Q4 negatives wording, and Gate-cell composition are other seats' scope; I
reconciled arithmetic only (checks 3-4). S045 full used-by field truncated in my read at 512 bytes —
presence verified, tail unobserved. Falsify reports cited by the draft do not exist yet; my PASS legs
assume they land with the admission commit per Q13.

VERDICT: PARTIAL — no duplication and no false novelty premise (population 1964/1021-PASS and 15168
arithmetic verified against committed bytes; exact admission deltas D1–D3 identified), but the draft
as worded extends a coverage-map row that does not exist (F1, Q6 uncovered ground) and rests one
support citation on an unlanded falsify report (F2, Q7/Q13); both are repairable only by the listed
same-commit changes, so the draft is not admission-ready verbatim.
