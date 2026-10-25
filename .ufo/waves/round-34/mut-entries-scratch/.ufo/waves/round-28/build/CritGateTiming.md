# CritGateTiming — Q10/Q13–Q16 admission gate for round-28 new knowledge

writer: CritGateTiming (seat; registry agentId `KengakuR28.CritGateTiming-2`, role `critic`, wave `build`)
Scope: author-side critic advice only. This report does not judge, admit or close anything for an outside reviewer. It sits under `build/`, so `gate_timing_check.py` can never count it as second-seat support (`is_second_wave`, lines 241-243).
Axes judged: novelty (C1 knowledge admission), calibration (honesty of structural evidence).
Inputs read (lane tree at HEAD `f0ba09b`, 2026-10-21 10:50:58 -0300; working copy of both files clean against HEAD):
`plans/round-28-claims.md`; `corpus/QUALITY.md:75-144` (Q10–Q16); `plans/gate_timing_check.py` (sha256 `51c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a`, last changed in `6356b0b`, equal to the source SHA FGateQ15 closed on per `corpus/lessons/round-27.md:207`); `corpus/lessons/round-27.md:31`; `.ufo/waves/round-27/falsify/FEntryNumbers.md:60-80`; `.ufo/waves/round-28/build/swarm-registry.json`; `.ufo/waves/round-28/build-spec.json` (DraftKnowledge item).
Commands: read-only `git log`/`git ls-tree`/`git show | sha256sum`/`wc -l`, `rg`, and `python3` JSON reads of registry/spec files. I did not run the checker, its selftest or any build/test. No external source was opened, so no URL quote applies. Installs: none.

## Strongest falsifiable objection

**Q13–Q16 bind a returned re-read to the candidate *path*, not to the *bytes* or *numbers* it re-read. Round 28's own plan creates the window where admitted numbers differ from re-read numbers, and the checker still exits 0 when that happens.**

1. **The checker only tests path and presence.** `audit_admission` (`plans/gate_timing_check.py:335-363`) checks these things about a report: it is in the tree, it is a nonempty regular blob, the seat is registered, the role is allowed, the writer is different, the report text contains the candidate path as a substring (`:358`), and it has at least one anchored `VERDICT:` line (`:360`). It never compares the reviewed content's digest, line count or numbers with the candidate blob in the admitting tree. `VERDICT_RE.findall` accepts any verdict token (`:56`, `:360`), including PARTIAL or FAIL. Q13 says this openly ("Presence is not endorsement", `QUALITY.md:106-107`), and Q15/Q16 call it "structural timing, not source-truth endorsement" (`:128`, `:137-138`). None of Q13–Q16 assigns the reviewed-bytes = admitted-bytes duty to any mechanism. Q10 (`:75-78`) needs "every quote location and every number" confirmed against *the entry*, but no tool checks that.
2. **This round's plan defers the numbers until after drafting.** The DraftKnowledge assignment (`build-spec.json`, item `DraftKnowledge`) says: "Draft can omit unmeasured metrics, which L1 adds after measured run", with `writer: DraftKnowledge`. The prereg (`plans/round-28-claims.md:31`) also expects "resolved findings" before admission. So C1's measured counts (raw population 812, the evaluator-type-set count, the 16-task sample, scorer-contract tallies) enter the candidate *after* the scribe draft. They may also change again after any falsify re-read when L1 resolves findings or reruns after an instrument fix.
3. **Counterexample (falsifiable, no benchmark contact):**
   - Falsify seat `F` (role `reviewer`) re-reads draft bytes D1, which cite 812.
   - Its report names `corpus/knowledge/webarena-task-spec-audit.md` and ends `VERDICT: PASS`.
   - L1 then changes one number in the admitted blob, giving D2 ≠ D1.
   - The Gate row cites `falsify/F.md`, and everything lands in one commit.

   Every branch of `:342-363` passes, so the CLI exits 0 [INFERENCE from static reading of `:322-385`; not executed, because this seat has no assigned probe]. Q10 is violated for exactly the numbers that C1's novelty claim rests on.
4. **Dated precedent (round 27, admission commit `6356b0b`, 2026-10-21 10:34:58 -0300).** The admitted `corpus/knowledge/extraction-policy-comparison.md` and the committed draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` are byte-equal in that tree (both sha256 `b77b7db4ecfcf843ab521631de1b4f31c06253464ff28e9d491c83a3cc794a67`, 114 lines). FEntryNumbers' final PASS (`FEntryNumbers.md:69,77`) identifies what it read only by the label "snapshot `A42E`" and "all 114 lines", with no digest. The "byte-exact from reviewed draft A42E" claim (`corpus/lessons/round-27.md:31`) is therefore prose plus a line count, and it co-landed with the report in a single commit. That holds for draft = admitted, but cannot show draft = what was reviewed. This is a limitation of the evidence, not a finding that round 27 was wrong.

Impacted axes: novelty (the C1 knowledge admission could carry unreviewed counts while showing structural support), calibration (exit 0 would be read as Q10 coverage it does not measure).
Classification: a fixable process defect, not a tradeoff the judge must reject. Q13–Q16 correctly measure what they claim to measure: presence, timing, role and identity.

## Secondary counterexamples (same root, lower severity)

- **Non-falsify citations are dropped silently.** `resolve_citations` adds a path only if `is_second_wave(...)` (`:279-280`). A Gate cell citing `falsify/FEntry.md` plus `build/OpenScorer.md` (for S062) exits 0. The build citation is neither invalid nor unresolved; it is simply ignored. The build-wave `OpenTasks`/`OpenScorer`/`OpenHelpers` scouts opened S061–S063 *before* the draft existed. So per-source Q10 coverage of S061/S062/S063 can look cited while the checker grades only the falsify report. Q10's "re-opens each cited source" is not enumerated per source by any check.
- **The agentId guard can never fire with this round's naming.** `member.agent_id == writer` (`:354`) is an exact string compare. With `writer: DraftKnowledge` and registry agentIds shaped `KengakuR28.<Seat>-2`, it is unreachable. Only the seat-stem check (`:352`) excludes the drafter. All 2026-10-21 round 26/27 registries are spawn-only, so a resumed-drafter self-review has no observed instance. It is a latent gap, not a present one.
- **The writer field can misattribute numbers.** If L1 adds the numbers but `writer:` stays `DraftKnowledge`, the provenance names a seat that did not author the measured cells. This does not enable self-review, because L1 files no falsify report, but the provenance is false for those cells.

## Smallest safe correction (process-only; no production edit by this seat)

1. Freeze the candidate *including* L1's measured numbers before any Q10 re-read. Each cited falsify report must record the sha256 of the exact bytes it re-read.
2. Before landing, L1 compares that digest with `git show <admitting-commit>:corpus/knowledge/<entry>.md | sha256sum`. Any mismatch requires a fresh returned re-read; prose "resolved" or a snapshot label does not count. The Gate cell should state the digest.
3. A Q10 report includes a per-source table for S061, S062 and S063 (location re-opened, quote, every number with exact cell). Gate cells cite only `falsify/`/`wave-2/` reports. Build-wave openings are first-seat inputs, not re-reads.
4. Set `writer:` to the author of the final bytes (e.g. `KengakuR28` with DraftKnowledge credited), or state the split.
5. Optional future QUALITY/checker work, only after failure-capable evidence (prereg `:33`): a digest field compared with the admitted blob, and a warning on cited non-second-wave paths. Not proposed for this round without a red-before receipt.

## Limitations

- At HEAD there is no `corpus/lessons/round-28.md`, no `.ufo/waves/round-28/drafts/`, no falsify wave and no Gate row. Nothing in round 28 is yet admitted or failed by this gate, and this report grades the requirement design against the declared plan.
- The checker's exit on the counterexample is inferred from code, not executed.
- I did not review report truth, S038 or C2 rows, or the C1 implementation.

VERDICT: PARTIAL — scoped to Q10/Q13–Q16 as the round-28 admission gate. Presence, timing, role and identity checks are sound as structural evidence. However, no Q13–Q16 mechanism or written duty binds the re-read bytes and numbers to the admitted blob, and this round's plan adds the measured numbers after drafting. The C1 knowledge admission needs digest-bound, per-source falsify re-reads (corrections 1–3) before exit 0 supports Q10. This is not a round PASS/FAIL or an outside closure.
