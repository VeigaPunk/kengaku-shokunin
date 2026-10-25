# Round 34 frontier scope: Terminal-Bench narrowing

## Exact source text (corpus/README.md)

(a) `corpus/README.md:276-279`:

> - **Agentic benchmark task-spec audits**: why — S005/S006 show lab self-audits finding task-level validity defects *after* publication; the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately. Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist.
>   - *Partly discharged round 29 attempt 2 (2026-10-25):* `knowledge/benchmark-task-validity-checklist.md` builds the per-benchmark task-validity checklist from the primary maintainer artefacts of Terminal-Bench 2.0, SWE-bench Pro V2 and Toolathlon-Verified. It supersedes the `primary specs` half of the `unopened leads` phrase for those three sources — their scoring code was not read and stays open; contamination-transparency cards, runtime task validity and hosted judges remain open.
>   - *Partly discharged round 31 (2026-10-25):* `knowledge/benchmark-verifier-execution-model.md` reads the harness's own verifier-mode resolver and `Verifier.verify` at Harbor commit `6099b8cf`, so the `their scoring code was not read and stays open` clause above is discharged for **verifier execution** (where grading runs, what is restored first, how SWE-bench Pro V2 derives its PASSED set). The clause stays open for the other benchmarks' scoring code (one SWE-bench Pro V2 task's grader *is* read here, in depth, and that is the only task-level code this round opens), for runtime task validity (which `PROVINCE.md` refuses to this lane) and for Toolathlon; the Terminal-Bench 2.0 axis-E cell is filled by this entry and the SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`.
>   - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads S103's one Toolathlon task (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and S104's LLM-as-judge survey frame (arXiv 2412.05579v2). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).

(b) `corpus/README.md:255` — coverage-map row, **Benchmark grader semantics** (verbatim):

> - **Benchmark grader semantics**: covered at source-code depth (round 33, 2026-10-25, admitted under renumbered ids) — knowledge/benchmark-grader-semantics.md; S093, S103, S104. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, the log-bucket one mixing fail-open exceptions with fail-closed credential absence; the S104 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.

(c) `corpus/README.md:254` — **Benchmark verifier execution model** row (verbatim):

> - **Benchmark verifier execution model**: covered at source-code depth (round 31, 2026-10-25) — knowledge/benchmark-verifier-execution-model.md; S092, S093, S100. Discharges the round-29 frontier clause "their scoring code was not read and stays open" for verifier execution only: the harness's mode resolution, the two restore guarantees that hold in shared mode, SWE-bench Pro V2's own test-space reset, and the log-scan grader behind its PASSED set. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.

(d) Open-gap lines explicitly mentioning Terminal-Bench, `corpus/README.md:358-360`:

> **Partly discharged round28:** the original Frontier task-spec-audit gap is closed only for this WebArena static surface. Terminal-Bench2.0, Toolathlon and SWE-bench Pro primary specifications, generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open.

## C1 narrowing disposition

C1's scope is the pinned `protein-assembly` evaluator (`tests/test.sh` and `tests/test_outputs.py`) compared with that task's `environment/antibody.fasta` and `environment/pdb_ids.txt` (frozen claim, `plans/round-34-claims.md:24-36`). If admitted with its required evidence, narrow **only** the round-33 sub-bullet's parenthetical open scoring-code clause `Terminal-Bench 2.0's` to this one task's scoring code. This is task-level evaluator semantics grounded against expected artifacts, not a claim about all Terminal-Bench scoring code.

Keep open: other Terminal-Bench 2.0 tasks/scoring code; all remaining SWE-bench Pro V2 grading code beyond the one round-31 task; runtime task validity; contamination checks/transparency; generated eval-time configs and hosted judges. C1 does not discharge the general task-spec-audit instrument/coverage claim, verifier execution model, or any open gap outside the named protein-assembly evaluator. The round-29/31/33 qualifications remain intact; no blanket benchmark-level closure follows.

## Evidence and limits

Observed source: `corpus/README.md` lines 254-280 and 358-360; exact long line 255 was fetched with `read` selector `:255:raw`. Frozen scope: `plans/round-34-claims.md:24-36`. This is a scoped text-reconciliation finding, not verification that C1 artifacts have landed or passed.

VERDICT: recon-frontier-done