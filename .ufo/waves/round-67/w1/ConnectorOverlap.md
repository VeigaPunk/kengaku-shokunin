# ConnectorOverlap — kengaku round 67, wave 1 (connector seat): findings

Full table, reproduction notes and the 40-file scan list: `.ufo/waves/round-67/w1/ConnectorOverlap/overlap.md`.

## Result

- **Overlaps found: 5** (O1–O5), all at term or quotation level. **0** claim the torch-pipeline grader or the torch-tensor grader.
- **Routing: 0 rows routed to a sibling lane.** O1 and O2 are boundary citations both lanes already state (kumitate owns coordinator topology; kengaku owns agent evaluation). O3 and O4 are term-only collisions (`--tensor-parallel-size` vLLM CLI; "never loads tensors"). O5 is a sibling wave file quoting kengaku's own `corpus/lessons/round-52.md:56`.
- **Frozen claims (R67-C1, R67-C2) touched by any overlap: none.** No text in `plans/round-67-claims.md` needs changing for sibling reasons.

## Question 2 (class-survey row)

`corpus/evidence/round62/class-survey.txt:14`: `CLASS process-environment count=3 members=install-windows-3.11,torch-pipeline-parallelism,torch-tensor-parallelism`.

No sibling lane claims the torch-pipeline grader or the torch-tensor grader. Both are kengaku's:
- torch-tensor-parallelism: R66-C1 (receipt `corpus/evidence/round66/tensor/receipt.txt`; commit `e02c2d90`; `corpus/SOURCES.md:198`, S183).
- torch-pipeline-parallelism: R67-C1 (frozen in `plans/round-67-claims.md`; `corpus/SOURCES.md:253-254`, S238/S239).
- install-windows-3.11: no sibling PROVINCE/SKILL/corpus/plans names it.

## Measured counts (commands in overlap.md §1–3)

- Sibling PROVINCE.md + SKILL.md term hits (40 files): `torch` 0, `gloo` 0, `Terminal-Bench` 0, `process-environment` 0, `tensor` 1 (kama SKILL.md:688, term-only), `pipeline` 30 (generic).
- Kengaku own (same method): `Terminal-Bench` 51, `process-environment` 4, `pipeline` 5, `torch` 0, `gloo` 0.
- Sibling corpus/plans grader-name grep (`torch-pipeline-parallelism|torch-tensor-parallelism|offline-torch|pipeline-parallel|tensor-parallel`): kama artifacts (vLLM CLI flags, at least 20 files) and souji's quote of kengaku's lesson. No sibling file names either grader as a claim.

## Limits

- The grep tool returned `No matches found` for glob path forms (`*-shokunin/PROVINCE.md`) on patterns that do occur in those files. Counts above are from the explicit 40-file list via shell `grep -c`. Reported to xd://report_issue.
- A sibling file that cites a grader is not a claim on the grader. Judgement is by surface ownership, per the table.
- No install. No lane or sibling file edited. No git mutation. No network.
