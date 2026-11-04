# Round 84 — a second exact-file replay, and an admission the checker could not confirm

2026-11-04, hyaku run 15, attempt 1. L1 KengakuR84. Base `4087b2f8369fb0c317a8460725a607681ff2fd7f`; claims freeze `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`. All times are UTC unless an offset is written. The frozen claims, case table, controls and kill rules are in `plans/round-84-claims.md` and are not edited here. Measured figures are in the round report and `SCORECARD.md`, cited to the receipts and the counters' transcripts in `.ufo/waves/round-84/w1/`.

## Gate

The L1 and the wave's scribe opened the source below on 2026-11-04. One new `corpus/SOURCES.md` row, S271, is admitted. Its scope is member replay only: the pinned grader's acceptance semantics, not a solved-task, model, image or serving-plane claim. No existing row's status, recheck or used-by cell changes.

| id and decision | URL or own-work location | access date | located quote (each under 25 words) | reason / flip |
|---|---|---|---|---|
| S271 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/gcode-to-text/tests/test_outputs.py | 2026-11-04 | :17: `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}", (` (5 words) | The pinned grader supplies the content-leg acceptance rule; :10 supplies the presence leg. The source does not prove an agent solved the task. Flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is made from it as a separate claim (not made here). The fetched bytes are byte-identical to the captured grader (sha256 `6b049dc626aa103b…`). |

### Knowledge entry: `corpus/knowledge/tb2-code-from-image-offline.md` — held, not re-admitted

The round-83 entry was filed without a checkable second-seat re-read (see R83-V1 below). This round tried to re-admit it under a successor Gate. **The re-admission is not made.** The frozen Q13 leg is decided by `plans/gate_timing_check.py`, and that checker cannot accept a second-seat report from this round's single wave:

- `is_second_wave()` resolves a cited report only when its wave directory is `falsify` or `wave2`/`wave-2`/`wave_2`. The round's reviewers wrote under `.ufo/waves/round-84/w1/`, so the checker reports `second-seat-reports=0` and exits 1 for every citation of them (measured by the reviewers and by `AdmitR84`'s probe-gate-contract fixture at `.ufo/waves/round-84/w1/AdmitR84/`).
- A report under `w1/<Seat>/report.md` has six path components; the checker's citation pattern does not parse it.
- The round-83 Gate table has no `candidate | decision | reason` header, so the checker parses zero admit rows at `ddb903a8` and exits 1 (`no admit rows`). The round-83 admission was therefore never checkable by this gate.

Two routes were considered and rejected. (a) Copy this round's reports into a `.ufo/waves/round-84/falsify/` directory with a registry naming the seats. That manufactures a second wave the round never ran, and it would misstate the provenance of the reviews; no such directory is created. (b) Amend `is_second_wave` to accept `w1`. That changes a gate in the middle of a frozen round, owes its own out-of-band run and selftest, and is an operator-visible decision. It is routed as an L0 question instead.

The decision cell in the successor row is therefore **hold**: the entry stays as filed at round 83 with its Q1 and Q21 header defects repaired (below), and its Q13 status is open. Flip: the operator or the gate owner rules that a one-wave round's directory satisfies the checker, or a residual falsify wave of at least eight seats (the policy floor) is dispatched within the round's size cap and re-reads the entry.

| candidate | decision | reason |
|---|---|---|
| `corpus/knowledge/tb2-code-from-image-offline.md` | hold — not re-admitted; Q13 open | Q1 and Q21 header defects repaired at lines 3–4 of the entry (dated correction below). The second-seat re-reads by `ReviewerR84` (`.ufo/waves/round-84/w1/ReviewerR84/report.md`) and `Reviewer2R84` (`.ufo/waves/round-84/w1/Reviewer2R84/report.md`) are committed as evidence and agree with the repaired header, but `plans/gate_timing_check.py` cannot count them under a one-wave directory. Writer field `writer: KengakuR84` added at entry line 4 (the checker's precondition). Flip: see above. |

## Corrections (R83-V1, R83-V2)

These are dated corrections to round-83 filed bytes. The round-83 lesson, its LOG entry, its SCORECARD entry and the outside spot-check remain historical records and are not edited.

- **R83-V1 (2026-11-04) — admission timing.** Defect: the round-83 admission of `corpus/knowledge/tb2-code-from-image-offline.md` named no second-seat re-read. The round-83 Gate table (`corpus/lessons/round-83.md` §Gate) has no `candidate | decision | reason` table at all, so the checker counts zero admits at `ddb903a8`. Repair: none that discharges the admission. The entry is held (above) and the checker shape is routed to the operator. No landing-time review is backdated.
- **R83-V2 (2026-11-04) — freshness.** Defect: the entry's header at `corpus/knowledge/tb2-code-from-image-offline.md:1-3` carried a recheck line with a command and no ISO date or cadence (Q1), and no pin or re-pin cadence although its `source:` line carries the pinned commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (Q21). Repair: line 3 now names the pin, an ISO date, a cadence and the re-check action, and line 4 adds `writer: KengakuR84`. The repaired header is judged against Q1 and Q21 by `plans/round84_c2_admission.py`; its measured figures are in the report. The freshness axis is restored to its held value by this repair; no new freshness gain is claimed.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| admission-bar gap in the lane's own Q1/Q21 check: a knowledge entry with a command-only recheck and an unpinned source was admitted and reported as freshness-held | `corpus/lessons/round-83-verifier-spotcheck.md` §Routed defects R83-V2; `corpus/QUALITY.md` Q1, Q21 | none (Q21's one-liner prints `unpinned` for this file; no round-83 check ran it) | `plans/round84_c2_admission.py` implements Q1/Q21 and calls the Q13 checker; red on the base revision (q1=1 q21=1 q13=1) and on a date-only repair (q21=1, q13=1); its filler control keeps the base bytes red. |
| a one-wave round's second-seat reviews cannot satisfy the Q13 checker, and round 83's Gate had no checkable table | `corpus/lessons/round-83.md` §Gate (no candidate/decision/reason header); `plans/gate_timing_check.py` `is_second_wave` | none: the round-83 checker was not run against its own admit | recorded as an open gate-shape defect; the successor row is `hold`, not an admit; L0 question filed for the operator. |
| the receipt's observation form (`CASE` lines) did not match the ledger's `predicate` verdict, the same vocabulary gap as M83-1; the population gate caught it only after the receipt landed, because the verdict vocabulary had not been priced before minting (the round-83 planned-next note asked for that pricing; this round did not do it) | `plans/round79_c1_population_ledger.py` `VERDICT-MISMATCH gcode-to-text ledger=predicate receipt=cases` at `8a61bce1`; `corpus/lessons/round-83.md` M83-1 | none before landing; the population gate after landing | the M83-1 remedy repeated: a clearly labelled ADMISSION-TRAILER holding the frozen counter's actual stdout at the landing revision, appended after the unchanged observation block; it is evidence of the counter's run, not a probe observation. Debt: price the verdict vocabulary before minting in the next round. |

## Sources and frontier

S271 (above) is the round's only new source row. Existing rows are unchanged. The population ledger moves `gcode-to-text` from `unexecuted/unattempted` to `executed` in round 84; the file-artifact class is restated in `SKILL.md`.

**considerthese.** `considerthese/2026-10-26.md` §Self-improvement suggestions 2 (one standing TB2 admission counter with a filler control) is mined in its per-entry form only. R84-C2's counter reads one entry at a measured revision, keeps the base bytes red as a filler control, and keeps a date-only repair red. The standing, parametrised counter over every admitted TB2 grader, with committed junk packages and digest pinning, is not implemented here and stays open.

**Assimilation: none.** `merge/kengaku/` (175 staged rows, 65 knowledge entries) is not drawn on by these frozen claims and remains unadopted backlog.

## Open questions

- Q13 checker shape for one-wave rounds (routed to `.ufo/l0-questions.md`, kengaku | round-84). `tb2-code-from-image-offline` remains un-readmitted until it is answered.
- R82-F1 (`anchor_line_check.py` quote-shape blind spot) remains open; the lesson makes no claim that it is repaired. The rows that the blind spot may leave unparsed were not counted this round and are a named follow-up.
- The coverage cap `kengaku | round-25/33/51` remains open; nothing is assumed answered.
- `plans/round82_c1_plans_registry.py` is red at BASE `4087b2f8` and stays red: `ROW-SELFTEST-FLAG:--selftest round83-c2-debt`. The round-83 counter builds its flags as `'--' + mode` (no literal `--selftest` in its bytes), so the gate's literal check misses the flag the registry row documents. The row and the counter are historical round-83 artifacts and were not edited; the fix belongs to the round-85 owner, either as a gate-check change under its own out-of-band run or as a round-83 counter spelling change under its own claim.
