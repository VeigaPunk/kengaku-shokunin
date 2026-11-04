# Round 84 — a second exact-file replay and the admission bar the lane's own gate missed

2026-11-04, hyaku run 15, attempt 1. L1 KengakuR84. Base `4087b2f8369fb0c317a8460725a607681ff2fd7f`; freeze `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`. All timestamps in this round are UTC unless an explicit offset is written.

The two frozen claims are R84-C1 (coverage: the second offline replay of the base-unexecuted `gcode-to-text` grader) and R84-C2 (calibration: the round-83 admission-bar debt in the admitted knowledge entry `corpus/knowledge/tb2-code-from-image-offline.md`). The frozen claim sentences, the case table, the control set and the kill rule live in `plans/round-84-claims.md` and are not edited here. This lesson records decisions, corrections and mined mistakes; the measured figures are transcribed by the L1 from the committed receipts, and none are asserted below.

## Gate

The L1 opened the source below on 2026-11-04. One new `corpus/SOURCES.md` row is proposed, S271; no existing row's status, recheck or used-by cell changes. The S271 row supports member replay only: it is not a solved-task, model or image claim, and no task image, oracle or serving plane is touched by it.

| id and decision | URL or own-work location | access date | located quote (each under 25 words) | reason / flip |
|---|---|---|---|---|
| S271 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/gcode-to-text/tests/test_outputs.py | 2026-11-04 | :17: `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}", (` (5 words) | The pinned grader itself supplies the acceptance rule for the content leg and :10 supplies the presence leg; it does not prove an agent solved the task. flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is attempted from this source — a separate claim, not made here. |

The second row below is the round's only knowledge-entry decision: the round-83 entry is re-admitted under this round's successor Gate on the strength of the two named second-seat re-read reports. The reports are committed in the admitting tree, and no landing-time review is backdated: the round-83 Gate row for S267 and the round-83 filed bytes stay exactly as filed, and no report is presented as if it had existed at the round-83 landing.

| candidate | decision | reason |
|---|---|---|
| `corpus/knowledge/tb2-code-from-image-offline.md` | admitted — re-admit under successor Gate (round 84) | The round-83 outside closure routed R83-V1 (admission timing) and R83-V2 (freshness) against this entry, and this row is the successor admission that discharges them. The second-seat re-read reports are `.ufo/waves/round-84/w1/ReviewerR84/report.md` and `.ufo/waves/round-84/w1/Reviewer2R84/report.md`; both are committed in the admitting tree, and neither is a backdated landing-time review. The candidate's writer is KengakuR84, distinct from both re-read seats; this round's repair adds the `writer: KengakuR84` field at entry line 4 so that the seat-versus-writer distinction is checkable from the entry bytes alone. The Q1 triad repair (line 3 recheck with an ISO date or cadence plus a named re-check action, and the historical pin or a re-pin cadence named on the same line) is carried by the same dated correction below. |

Gate-timing note for the integrator: the frozen Q13 leg is decided by `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit REV` on the admitting tree. That checker admits only an `admit`-initial decision cell and only resolves a second-seat report by a repo-relative `.md` path that exists in the committing tree; the decision cell above is written `admitted — re-admit under successor Gate (round 84)` for that reason, and the two cited paths are the ones the reviewer seats write. If the checker as committed does not resolve those two paths under this wave's directory layout, the installer must place the two reports where the checker resolves them before the admitting commit; the prose above is unchanged either way, and no substitute, stub or placeholder report is written.

## Corrections (R83-V1, R83-V2)

These are dated corrections to round-83 filed bytes. The round-83 lesson, its LOG entry, its SCORECARD entry and the round-83 outside spot-check remain historical records, unchanged; the correction is a new dated paragraph here, per the lane's append-only rule.

- **R83-V1 (2026-11-04) — admission timing.** Defect: the round-83 admission of `corpus/knowledge/tb2-code-from-image-offline.md` had no second-seat re-read on record, contrary to Q13/Q14. The line that carries it is the round-83 lesson's Gate row for S267 (`corpus/lessons/round-83.md`, the S271-precursor row that admits the pinned `code-from-image` grader and points at the new knowledge entry): that row and its successor admit the entry's source without naming any returned re-read report. Repair: this lesson's Gate row above is the successor admission, and it names the two second-seat re-read reports by repo-relative path, each committed in the admitting tree, with the candidate writer distinct from the re-read seats. No landing-time review is retrofitted and no filed round-83 byte is rewritten to make the historical admission look reviewed.

- **R83-V2 (2026-11-04) — freshness.** Defect: the admitted entry's header triad, `corpus/knowledge/tb2-code-from-image-offline.md:1-3`, does not meet Q1/Q21. Line 1 carries the `source:` row id, URL and anchor and the pinned commit; line 2 carries `verified-at:`; line 3 carries only a re-run command, with no ISO date or cadence and no name of the pinned historical source or a re-pin cadence. Repair: this round's repair rewrites the header's first three lines so that the recheck line names an ISO date or a cadence together with a named re-check action, and names the pinned commit or an explicit re-pin cadence on the same line, and adds the entry's `writer:` field at line 4. The repair is a dated change to the entry's header, not a rewrite of the entry's body claims, and the round-83 lesson's Gate row stays as filed. The outside closure's own statements that the round-83 report's freshness-held and unconditional expansion-improved assertions are superseded by R83-V1/R83-V2 are carried forward as routed findings; this round's lesson does not restate them as its own verdicts.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| admission-bar gap in the lane's own Q1/Q13/Q21 gate | `corpus/lessons/round-83-verifier-spotcheck.md` §Routed defects (R83-V1 admission timing, R83-V2 freshness) | none | R84-C2 counter, red on BASE and on a date-only repair: the frozen R84-C2 claim requires `plans/round84_c2_admission.py` to report the base revision's entry as defective on all three criteria and to keep the Q21 and Q13 defects alive when only the recheck date is repaired, with a filler control that runs the base bytes and must stay red |

## Sources and frontier

S271 is the round's only new source row and is an admit for member replay only; it supports neither a solved-task nor a model claim, and its scope is the pinned grader's acceptance semantics. No existing `corpus/SOURCES.md` row's status, recheck or used-by cell changes in this round, and no row is edited in place.

The considerthese proposal used this round is `considerthese/2026-10-26.md` §Self-improvement suggestions 2, the standing TB2 admission counter with a built-in filler control. It is mined here in its per-entry form: the frozen R84-C2 claim carries a filler control whose base bytes must stay red and a date-only control that must keep the Q21 and Q13 defects alive, and the counter reads the entry and the lesson at a measured revision rather than at the working tree.

Assimilation: none. `merge/kengaku/` (staged rows and knowledge entries) is not drawn on by these frozen claims and remains unadopted backlog; no merged row, entry or frontier item is adopted, adapted or retired in this round.

## Frontier mining

`considerthese/2026-10-26.md` §Self-improvement suggestions 2 proposed one standing, parametrised TB2 admission counter — a single `tb2_grader_admit.py` that digest-pins the spec, dry table and probe it reads, ships a committed filler package that must stay red, and is re-run at every tip for all admitted graders — because the per-round copies of `plans/round3{6,7,8,9}_c2_verify.py` share one before state and several of them admitted a junk or informed-filler package.

What this round implements is only the per-entry form of that idea, and only inside the frozen R84-C2 claim: one counter over one admitted entry, run at a measured revision, whose filler control runs the base bytes and must stay red and whose date-only control must keep the Q21 and Q13 defects alive. What this round does not implement is the standing counter the proposal actually asked for: no single parametrised instrument spans the admitted TB2 graders, no committed junk or informed-filler package exists as a shipped artefact, no spec/dry-table/probe digest pinning is done by that counter, and no re-run-at-every-tip sweep over the admitted set is claimed. The general proposal therefore remains open; the per-entry filler control is not evidence that the standing counter is closed.
