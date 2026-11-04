# C2RowFixR73 — scoped implementation report

Axes: coverage, calibration.

## Delivered

Exact before/after cells, source-line decisions, rejected readings, reproducible input and complete red/green audit transcripts are retained in `corpus/evidence/round73/w1/c2-row-fix.md`.

Draft changes only in the scratch mirror:

- sources-adopt: 0 clean; 1 failed (real selftest return at sources_adopt.py:969); 2 could-not-evaluate; 3–8 failed; 9 could-not-evaluate. Each original description is preserved and each code is individually annotated. Code 9 must not be swept into a blanket “3–9 failed”: sources_adopt.py:423–425 and :958 explicitly distinguish caller-map absence from a bad citation.
- round62-c1-class-survey: exact kind cell `census gate` → `gate`, decided by round62_c1_class_survey.py:264 (`code = 0 if verdict == "pass" else 1`).

No lane SKILL.md, predicate, command, target, kill rule, configuration or script was changed by this seat. Only the two permitted retained files were written outside scratch.

## Exercised evidence

Input: complete archive of freeze revision `255c261db2119906c70195291a2b6f9f46f82a72`, not a landing revision. Command, cwd and exact stdout are in the evidence file:

`python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C2RowFixR73`

- Before edits: rc 1, stderr empty, 106 scripts/106 rows, D2 defects exactly the assigned two, `MISMATCH 2`, `PREDICATE R73-C2 fail`.
- Intermediate annotated draft before adding the real selftest code 1: rc 0, stderr empty, 106 scripts/106 rows, all legs zero.
- Final exact draft: rc 0, stderr empty, `INSTRUMENTS total=106 derived=registry rows=106`, `PARSED scripts=106 failed=0`, D1–D4 each `ok n=0`, `MISMATCH 0`, `PREDICATE R73-C2 pass`.

No third defect was reported by that final mirror audit. No selftest, mutant, build, lint or formatting runs were made; only the assigned audits were executed.

## Findings / limits

An initial archive of moving HEAD already contained 114 rows and the integration's two row changes; its audit was green at 114, not the frozen target count 106. This was discarded and replaced by the explicitly pinned freeze archive. The 114-row observation is not a landing assertion; the L1 must reconcile counts at its own named tip under the unchanged frozen criteria.

The structural audit does not semantically validate each exit-code class: an inaccurate blanket failed range can also pass. The proposed per-code map follows source semantics, not merely the audit's failure-keyword requirement. Classification of code 5 as failed is an explicit interpretation: the requested membership condition was evaluated false on readable package bytes. Alternative caller-error reading is documented and rejected in the evidence.

LSP is not mounted in this seat's tool inventory; symbol locations were obtained through source reads/search. No tools were installed or upgraded, no credentials were read, no fixture git mutation occurred, and no subagents/background jobs were launched. Scratch is removed after retaining these two files; no /tmp files were created by this seat.

## Parent gate

Parent owns final landing-tip audit/selftests/mutants and the coverage gate; this report does not substitute the draft-mirror result for those gates.

## Output self-evaluation

Accuracy 4/5 (real source returns and measured transcripts; code-5 class remains a stated interpretation); completeness 4/5 (all assigned artifacts present; no landing-tip result claimed); clarity 4/5 (exact cells separated from interpretation); actionability 4/5 (direct cell replacement and parent gate named); conciseness 4/5 (source citations intentionally retained). Overall 4.0/5. Highest-impact improvement applied: explicitly pinned the archive after discovering HEAD movement and included the real selftest return 1. Would the user agree? Expected, subject to the openly stated code-5 interpretation.
