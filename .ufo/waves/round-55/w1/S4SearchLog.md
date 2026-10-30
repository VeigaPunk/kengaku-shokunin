# S4SearchLog — scoped findings (round 55 w1)

Deliverable: `.ufo/waves/round-55/w1/S4SearchLog/search-log.md` — one PRISMA-style bounded-search
note, splice-ready for `corpus/SOURCES.md` `## Search log` (house one-bullet dated format).

Grounding (all read-only against the live lane; every number in the note was measured, not assumed):

- identified 89 — `find corpus/evidence/round52/graders -mindepth 1 -maxdepth 1 -type d | wc -l` → 89;
  pin `2fd12b88…766d6` per frozen R55-C3.
- excluded 12 already-read — the 12 `corpus/knowledge/tb2-*-grader.md` entries (protein-assembly r35
  … polyglot-c-py r46, one per round r35–r46 per README Coverage map bullets).
- excluded 1 push-protection-blocked — sanitize-git-repo: only capture dir without
  `tests/test_outputs.py`; `graders/EXCLUDED.md` records GH013 (HF token pattern, sha256
  `57e49041…b59e`, operator decision 2026-10-28).
- screened 5, with measured reasons: chess-best-move 25 lines stdlib-only multiset-equality verdict
  (INCLUDE; sha256 `a540714e…f286` = frozen byte identity); extract-elf 392 lines; cancel-async-tasks
  172 lines with `time.sleep`/3–10 s timeout runtime dependence; dna-insert shells out to external
  `oligotm` (`tests/test_outputs.py:17-20`); count-dataset-tokens 13 lines but dataset-derived
  constant `"79586"`.
- counts reconcile: 89 = 12 + 1 + 5 screened + 71 unreached; excluded 17; included 1. Stop rationale:
  one grader per round (r35–r46 cadence), frontier narrows 12→13 of 89.

Defects: none in scope. Observation (pre-landing, expected): `corpus/evidence/round55/` receipt dir
absent at read time — E6ChessReceipt owns it. Dead ends and full command log:
`.ufo/waves/round-55/w1/S4SearchLog/report.md`. No installs; no scratch dir (all work read-only on
the live lane); no mutating git command run.
