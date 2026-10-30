<!--
Draft for the corpus/README.md additions of round 53. L1 owns the landed text; this file is the seat's proposal.
The index row is the row for the round's new knowledge entry; the bullets are the round-53 evidence block.
`[pending: ...]` marks anything the L1 has not measured or assigned yet.
-->

## Index row (for the "What's here" table of `corpus/README.md`)

Insert in the `knowledge/` block, after the `knowledge/tb2-grader-vacuity-triage.md` row (round 52) and next to the
round-53 `knowledge/fixture-honest-geometry.md` row:

```
| `knowledge/tb2-presence-only-triage.md` | Sound presence-only triage of the Terminal-Bench 2.0 graders: 305 test functions over 88 tasks at pin `2fd12b88` (183 of 184 captures committed, the operator-excluded `sanitize-git-repo/tests/test_outputs.py` absent by design), a frozen AST classifier (sha256 `935db122…`) scoring 52 `P1` / 253 `P0` against an eight-seat blind-label oracle that decides all 305 with `disagree=0` (limit 9.2 %), `contested=0` and a non-vacuous control (the round-52 classifier disagrees on 23 decided tests), 28 never-read candidate tasks and 20 confirmed presence-only tasks with a quote inside the test's own line span; the round's verdict is not admitted because the PRIOR-ART leg holds no rows at the measured revision (`PREDICATE R53-C1 fail`), and the prior-art pricing is the open leg | [pending: the SOURCES ids the L1 assigns from S194 for the rows this round opens] + the pinned TB2 tree at `2fd12b88` (`corpus/evidence/round53/pin-tree-2fd12b88.json`, `tests-index.json`) and the round-53 receipts `.ufo/waves/round-53/claims/c1-after-oracle.txt`, `c1-candidates.txt`, `corpus/evidence/round53/confirmations.json` |
```

(Shape check against the round-52 row it follows: `| \`knowledge/tb2-grader-vacuity-triage.md\` | <covers> | <primary source> |`.)

## Bullets (new `### Round-53 evidence` block, appended after `### Round-52 evidence`)

```
### Round-53 evidence (2026-10-28 → 2026-10-30)

- `corpus/evidence/round53/pin-tree-2fd12b88.json`, `tests-index.json` — the pinned inputs of the C1 predicate: the GitHub trees-API listing of pin `2fd12b88` (1038 blobs, sha256 `96b47248…cbb9`) and the 305-test index (sha256 `579d567f…7897c7330`); `plans/round52-tasks.json` (sha256 `0230b68c…5cfc`) carries the population.
- `corpus/evidence/round53/confirmations.json` — the CONFIRM leg's 20 rows, one per never-read presence-only task (five wave-2 readers × 4 tasks, all `confirmed: true`), each with the test id, a quote inside the test function's own line span, the reader and the report path + sha256; the readers' own reports are `.ufo/waves/round-53/w2/C1ConfRead{A,B,C,D,G}.md` with their parts under `.ufo/waves/round-53/w2/C1ConfRead*/`.
- `.ufo/waves/round-53/labels/shard-{A..H}.json` and `.ufo/waves/round-53/w1/C1Label*/labels.json` — the eight blind label shards and the eight seat label files (four scout, four reviewer seats; each test labelled by exactly two seats of different role); the merged oracle is computed by the counter, not authored.
- `.ufo/waves/round-53/claims/` — the frozen counting receipts: `c1-before.txt` (base tip: `PINS … pin_tree_sha=BAD`, `FREEZE absent`, `PREDICATE R53-C1 fail`), `c1-after-oracle.txt` (the oracle at `db90a6b`: `ORACLE tests=305 decided=305 oracle_Y=52 oracle_N=253 disagree=0 limit=9.2 per_label_agree=1.000`, `ORACLE-CONTROL control_ok=yes`), `c1-candidates.txt` (28 never-read candidates), `c1-selftest.txt` (`cases=47 failures=0`), `c2-before-head.txt` (`ROWS registry=75 ledger=0 missing=75`), `c2-before-manual-probe.{py,txt}` (73 rows parsed, 60 runnable as written: 38 exit 0, 22 exit non-zero, 13 with a placeholder in the entry cell), `c2-run1.txt` (`RUN executed=77 timeout=0 mismatched=18 evidence_missing=1`, `PREDICATE R53-C2 fail`, exit 1), `c2-selftest.txt` (`cases=52 failures=0`), `c2-a3-redbefore.txt` (the A3 worker-reset fix shown able to fail).
- `../plans/round53_c1_triage.py`, `../plans/round53_c1_classify.py`, `../plans/round53-c1-freeze.json` — the C1 counter, the frozen AST classifier (sha256 `935db122…`, `P1=52 P0=253` over the 305 ids) and the freeze file that pins the classifier, the eight label files and the eight shards.
- `../plans/round53_c2_tipstate.py`, `../plans/round53-tipstate.json`, `../plans/stage_scan.py` — the C2 counter, the 78-row tip-state ledger (74 `entry` + 4 `selftest`; 66 green, 12 red) and the pre-stage credential-pattern scan landed with its registry row `stage-scan`.
- `.ufo/waves/round-53/w1/`, `.ufo/waves/round-53/w2/`, `.ufo/waves/round-53/w3/` — the three waves' seat evidence (35 build seats, 42 falsify/confirm seats of which five confirmation readers completed, 32 wave-3 seats); `../corpus/lessons/round-53.md` holds the mined mistakes.
- Sources for this round's knowledge entry: [pending: the L1 assigns the SOURCES ids from S194; the round-start census is 186 rows with 15 pre-existing W04 duplicate-url warnings, exit 0 (`grep -c '^| S[0-9]' corpus/SOURCES.md` → 186)].
```

## Index-row and bullet cross-checks run by this seat

- `grep -c '^| \`knowledge/' corpus/README.md` → 56; `ls corpus/knowledge | wc -l` → 56 (the two agree, so the new
  `knowledge/tb2-presence-only-triage.md` must add one row and one file together — the round-50 index defect this lane
  already paid for once, in `corpus/knowledge/fixture-honest-geometry.md`).
- `grep -c '^| S[0-9]' corpus/SOURCES.md` → 186.
- `grep -n '^| \`round53\|^| \`stage-scan' SKILL.md` → three registry rows (`round53-c1`, `round53-c2`, `stage-scan`),
  i.e. the C2 counter's pinned row set is 75 frozen names + 3 = 78, matching
  `ROWS registry=78 ledger=78 … row_set_pinned=ok` at `9ead4476`.
