# RevQ9Q10 — r24 spot-check disagreements → grounded Q9/Q10, able-to-fail test

Read-only; tree = 3f371d2 (HEAD; clean except untracked `.ufo/waves/`). No installs. Axis: calibration.

## Grounding — PASS
1. `corpus/QUALITY.md:67-74` Q9 ("a rejection's reason follows from its evidence"; "a correct
   verdict with a wrong reason is a gate failure") cites `corpus/lessons/round-24.md` M21 with the
   S023/S006 non-sequitur content; `QUALITY.md:75-80` Q10 ("locations and numbers are re-read by a
   second seat"; bans "an approximation such as \"~45–48%\"") cites M22 with the five-slips+one-range
   content. Both match the lesson rows in substance.
2. `round-24.md:31` (M21) and `:32` (M22) exist with exactly those contents; their fix columns name
   QUALITY Q9 / Q10 — grounding is bidirectional.
3. Fixing commit: `git log -S'Q10 — locations' -- corpus/QUALITY.md` → `e21f9ea` ("round-24:
   post-review fixes"); disagreement record `round-24.md:113` §Post-review corrections, `:121-126`
   (both spot-check disagreements → §Corrections/S026, M22→Q10, M21→Q9), `:136-139` (S026 receipt);
   matches `corpus/lessons/round-24-verifier-spotcheck.md:13` ("became Q9/Q10 … in e21f9ea").

## Q9 able-to-fail on the r24 original — PASS
4. `git show 94da19e:corpus/SOURCES.md | grep '| S023'` → `:45`: "REJECTED: vendor marketing claims
   contamination-resistance that a later OpenAI audit (S006 …) reports as ~30% broken tasks".
   Claim's property = contamination-resistance; cited evidence's property = task validity → Q9's
   property-match rule fires → gate failure. Q9 catches the original defect.
5. Discrimination: current `corpus/SOURCES.md:47` keeps the defective S023 reason byte-identical
   (diff of `grep '| S023'`, 94da19e vs 3f371d2 → identical); S026 (`:48`) supersedes with a
   property-matched reason ("…unreviewed self-description…; S006 does not bear on it — S006 reports
   Pro task validity …, a separate property"). Q9 fails S023@94da19e, passes S026; remedy is Q9's
   own "rewritten as a superseding row".
6. Registry diff 94da19e..3f371d2 = +22/−21 (21 in-place recheck-cell normalizations, contract
   rule 2, + appended S026); the three knowledge entries are +15/+16/+17 with 0 deletions — pure
   appends; drifted lines still sit above the blocks (see #8).

## Q10 able-to-fail on the r24 originals — PASS
7. Blocks: three entry-level `## Corrections (round 24 post-review, 2026-10-19)` —
   `llm-judge-calibration.md:84`, `contamination-detection-and-transparency.md:85`,
   `agent-time-horizon-and-task-validity.md:48` — plus the lesson's `round-24.md:113` section = 4
   only if that one is counted. Together they cover exactly M22's four sources (S002, S005, S009,
   S012), six findings.
8. Q10's re-open-and-confirm applied to the 94da19e bytes mismatches on every M22 item:
   llm-judge `94da19e:27` "~45–48%" (Q10's text bans this exact string form; true: Table 3 §4.2
   cells 35.40–45.54 / 40.53–48.58, correction `:89ff`) and `:36-38` 'repetitive list' under
   Abstract (true §3.3); contamination `94da19e:1` anchor "§3.1 Table 2, §4 Table 5", `:29` "Table 2
   shows" (true Figure 2, §3.1), `:31` "S002, §4" (true §1 Introduction); agent-time-horizon
   `94da19e:17` 59.4% quote under "Too narrow and too wide tests" (true opening-summary item 1),
   `:18` "Contamination" quote (true opening-summary item 2). 5 location slips + 1 unreproduced
   range = the full M22 set → Q10 fails the originals.
9. Append-only intact at tip: drifted lines still present above the blocks —
   `llm-judge-calibration.md:27`, `contamination-detection-and-transparency.md:29,:31`,
   `agent-time-horizon-and-task-validity.md:17`.

## S026 row checks
10. `corpus/SOURCES.md:48`: reason addresses the asserted property (contamination) and names the
    non-sequitur explicitly → Q9-clean. Receipt `corpus/evidence/round24-sources/gate.md:34`: 22-word
    quote ≤25, exact location "Data Contamination → The Solution" → meets Q10's format bar.
11. Observation, no action: S026 sha256 `171087c5…` vs S023's `ee510e84…`, same URL + date, both
    128,773 bytes — consistent with the dynamic-content caveat (`round-24-verifier-spotcheck.md:12`
    marks S005/S006/S023 dynamic); equal byte counts are a coincidence, not a defect.

## Findings
- LOW (wording scope): Q9/Q10 sit under "## Admission bar — knowledge entries"
  (`QUALITY.md:22-24` preamble binds entries), but the M21 defect lived in a `corpus/SOURCES.md`
  registry row's reason cell. Substance is covered (Q8 routes rejections to "a `rejected`
  `SOURCES.md` row or a … `## Gate` line"; Q9's remedy is the superseding row S026 is), yet no
  sentence extends Q9/Q10 to Q8-recorded rejections wherever recorded. One future new-row sentence
  (Q-rows are superseded, never edited) would close it.
- INFO: Q9/Q10 are gate prose, not mechanically enforced; the r24 firing path was the non-author
  spot-check. No overlap with C2's frozen P2a–P2e populations (no Q-row assertions there), so no
  conflict with `plans/state_check.py`.

## Verification gaps
- Offline contract: I did not re-open the four web sources; the able-to-fail pairs rest on the
  committed corrections' re-open statements, the M21/M22 rows, and the 94da19e bytes. No live fetch.
- The second-seat mandate (who re-reads) is process, not bytes; only the location/number comparison
  is demonstrable from repo state.

VERDICT: Grounded and able to fail — Q9/Q10 at QUALITY.md:67-80 cite M21/M22 (round-24.md:31-32, landed e21f9ea); Q9 fails 94da19e S023 and passes S026; Q10 flags all six M22 drifts from 94da19e bytes; one LOW wording-scope note.
