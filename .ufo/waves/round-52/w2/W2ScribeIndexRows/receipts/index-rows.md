# Round-52 corpus index rows — W2ScribeIndexRows draft (2026-10-28)

Measured at lane HEAD `87301bacca90c03fa915716fbe6d7023762c5ab3` (`git rev-parse --show-toplevel` = lane root).
Target file: `corpus/README.md`. Rows are written in that file's existing table style. Nothing here is pasted into the lane tree by this seat; the L1 integrates.

Counter state the rows rely on (re-run read-only by this seat, `TMPDIR` in scratch):

```
R52-C1 literal : TASKS total=89 records=89 classified=88 | CAPTURES expected=184 present=183 mismatched=0
                 CLASS V1=2 V4=0 V2=53 V3=31 V0=3 | TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
                 CANDIDATES total=29 | CONFIRMED new=0 | PRIOR-ART ok=False urls=0 | LABELS agree=0 of 0
                 PREDICATE R52-C1 fail (exit 1)
R52-C1 A5      : A5 CAPTURES present+pinned_excluded=184 of 184 | A5 TASKS classified+excluded=89 of 89
                 PREDICATE R52-C1-A5 fail
R52-C2         : ADVERTISED total=72 | REGISTERED total=72 rows=74 | MISSING 0 | INCOMPLETE 0
                 ENTRY-MISSING 0 | SELFTEST-UNBACKED 0 | PREDICATE R52-C2 pass (exit 0)
selftests      : R52-C1 cases=6 failures=0 (exit 0) | R52-C2 cases=3 failures=0 (exit 0)
```

Status of each artefact, measured now:

| artefact | on disk now | row status |
|---|---|---|
| `plans/round52-tasks.json` | yes | paste |
| `plans/round52_c1_grader_audit.py` | yes | paste |
| `plans/round52_c2_registry.py` | yes | paste |
| `plans/round-52-claims.md` | yes | paste |
| `corpus/evidence/round52/graders/` | yes (183 captures + SHA256SUMS + EXCLUDED.md) | paste |
| `corpus/evidence/round52/confirmations.json`, `prior-art.md`, `labels.json` | **no** | paste only after they land and the after-run is recorded |
| `corpus/knowledge/tb2-grader-vacuity-triage.md` | **no** (planned name, from the wave-2 spec) | paste only after it lands; fill the Covers cell from the landed file, not from this draft |
| `corpus/lessons/round-52.md` | **no** | paste only after it lands; fill the Covers cell from the landed file |

Verdict dependence: the knowledge row, the lesson row, the coverage bullet and the frontier bullet state a capability that is **admitted only if the literal R52-C1 predicate passes**. At this measurement it does not (`PREDICATE R52-C1 fail`, `CONFIRMED new=0`). The integrator uses exactly one of the two frontier variants below.

---

## 1. `### plans/` table — append after the last row (`plans/wwkd-round-17-coverage.md`)

| File | Covers |
|---|---|
| `plans/round-52-claims.md` | Round-52 frozen claims: R52-C1 (grader-vacuity triage, novelty 8→9) and R52-C2 (gate-registry closure, operability 8→9); before/after targets, kill rules, controls, frontier step, amendments A1–A5 (A1 per-test rule; A2 counter fixes; A3 C2 parser; A4 P1 count correction; A5 operator exclusion of one capture, additive report) |
| `plans/round52-tasks.json` | Frozen R52-C1 population: Terminal-Bench 2.0 at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, 89 tasks, `capture_file_count=184` (94 `test_outputs.py`, 89 `test.sh`, 1 `verify.sh`), per-task grader files; `sha256 0230b68c…` |
| `plans/round52_c1_grader_audit.py` | R52-C1 counter: TASKS, CAPTURES (every capture digest-checked against `corpus/evidence/round52/graders/SHA256SUMS`), file-level CLASS V1–V0, per-test TESTCLASS (P1 presence-only), CANDIDATES, CONFIRMED, PRIOR-ART, LABELS, and the additive `R52-C1-A5` line; `--lane .` (exit 0 pass, 1 fail, 2 setup), `--selftest` (`cases=6 failures=0`); `sha256 0b1d4213…` |
| `plans/round52_c2_registry.py` | R52-C2 counter: ADVERTISED (`plans/<name>.py`, `corpus/evidence/<dir>/<name>.py` or `grader.py`) against the SKILL.md *Gate/probe registry* — MISSING, INCOMPLETE, ENTRY-MISSING, SELFTEST-UNBACKED; `--lane .`, `--selftest` (`cases=3 failures=0`); `sha256 b9ce9439…` |

## 2. `## What's here` knowledge table — insert after the `knowledge/tb2-polyglot-c-py-grader.md` row (CONDITIONAL on landing)

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/tb2-grader-vacuity-triage.md` | Whole-population triage of the 89 Terminal-Bench 2.0 graders at pin `2fd12b88`: 184 digest-pinned captures; file-level classes V1 2 · V4 0 · V2 53 · V3 31 · V0 3; per-test presence-only tests P1 33 across 27 tasks; 29 vacuity candidates (≥1 P1 test); the confirmed findings and their prior-art pricing as the after-run receipt records them (at this measurement `CONFIRMED new=0`, `PRIOR-ART ok=False`). A bytes-level triage, not a hand reading: hand-read TB2 graders stay at 12 of 89 until confirmations land | S179 (TB2 grader-file population at the pin), S115 re-opened for `build-pmars`; `corpus/evidence/round52/`; `plans/round52_c1_grader_audit.py`; `plans/round52-tasks.json` |

## 3. `## What's here` lessons table — insert after the `lessons/round-51.md` row (CONDITIONAL on landing)

| Entry | Covers | Evidence |
|---|---|---|
| `lessons/round-52.md` | Grader-vacuity triage over a benchmark population (per-test vs file-level classification, A1–A4 counter corrections, A5 operator exclusion of one digest-pinned capture) and the 28-row gate-registry closure (72/72, `order-check` self-test claim fixed); one mined Mistakes row with its Gate; fill the Covers cell from the landed file | `plans/round-52-claims.md`; `.ufo/waves/round-52/`; `corpus/evidence/round52/` |

## 4. `### evidence/` round sections — append at end of file (after `### Round-51 evidence`)

### Round-52 evidence (2026-10-28)

- `corpus/evidence/round52/graders/` — 89 task directories holding **183 of the 184** digest-pinned Terminal-Bench 2.0 grader captures at pin `2fd12b88` (`find … -type f` = 185 = 183 captures + `SHA256SUMS` + `EXCLUDED.md`); `SHA256SUMS` lists all 184 pinned paths, unedited; `EXCLUDED.md` records the one absent file, `sanitize-git-repo/tests/test_outputs.py` (sha256 `57e49041…b59e`, excluded because GitHub push protection GH013 flags a token pattern in the public fixture; operator decision 2026-10-28; Amendment A5). The absent file is not a defect of any other leg and must not be re-fetched into the tree.
- `corpus/evidence/round52/confirmations.json`, `prior-art.md`, `labels.json` — **not on disk at this measurement**; listed here only when they land.
- `.ufo/waves/round-52/claims/c1-after.txt`, `c2-after.txt` — **stale snapshots**: they show `CAPTURES present=89` and `MISSING 28`; the counters at lane HEAD `87301ba` give `present=183` and `MISSING 0`. The after-run receipt must be regenerated at the landing revision before it is cited.

## 5. `## Coverage map` — insert after the twelfth-task Terminal-Bench 2.0 bullet, before `## Open gaps` (CONDITIONAL on admission)

- **Terminal-Bench 2.0 grader population triage**: covered at bytes level (round 52, 2026-10-28) — knowledge/tb2-grader-vacuity-triage.md; S179; instrument `plans/round52_c1_grader_audit.py`; population `plans/round52-tasks.json`; captures `corpus/evidence/round52/graders/`. All 89 graders are classified and 29 are vacuity candidates; the 77 graders that were not hand-read keep their scoring code unread beyond the triage queue. Not task validity, not contamination measurement, not model or agent performance.

## 6. `## Frontier` — the clause this round advances, and the two drafted variants

The clause (`corpus/README.md:329`, bullet **Agentic benchmark task-spec audits**): "the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately … turned into a per-benchmark task-validity checklist." Its open part for this round is the **graders** leg for Terminal-Bench 2.0 (`… stays open for the remaining TB2 task graders (N of 89 read)`). Contamination and runtime task validity are not advanced.

Variant A — use only if the literal R52-C1 predicate passes at the landing revision (`PREDICATE R52-C1 pass`, `CONFIRMED ≥ 2` with located quotes, `PRIOR-ART ok=True`):

  - *Partly discharged round 52 (2026-10-28):* `knowledge/tb2-grader-vacuity-triage.md` audits all 89 Terminal-Bench 2.0 graders at pin `2fd12b88` as a population (184-file capture set, digest-pinned in `corpus/evidence/round52/graders/SHA256SUMS`; `plans/round52_c1_grader_audit.py`, receipt `<landing receipt path>`). The per-test presence-only triage (P1) flags N vacuity candidates; the confirmed findings are `<confirmed task ids>`, each read by a second reader from its captured bytes. The "Terminal-Bench 2.0's" clause is **narrowed for the grader population**, not for scoring code: hand-read TB2 graders stand at `<12 + confirmed-new>` of 89; it stays open for the remaining graders' scoring code, for SWE-bench Pro V2 and Toolathlon, for runtime task validity (which `PROVINCE.md` refuses to this lane), and for contamination. Not the task image, the oracle or a harness run; not model or agent behaviour.

Variant B — use at the measured state (`PREDICATE R52-C1 fail`, `CONFIRMED new=0`): the frontier advance is **not** claimed; the bullet records the instrument as landed and not admitted, so no discharge reads as admitted:

  - *Round 52 (2026-10-28), instrument landed, not admitted:* `plans/round52_c1_grader_audit.py` triages all 89 Terminal-Bench 2.0 graders at pin `2fd12b88` at bytes level (`TASKS classified=88 of 89` literal, `CAPTURES present=183 of 184`, `PREDICATE R52-C1 fail`); the A5 line reports `R52-C1-A5 fail` because no confirmation or prior-art leg landed. The clause stays open exactly as before round 52 (hand-read TB2 graders 12 of 89). Honest stop recorded in `lessons/round-52.md` and the SCORECARD row; novelty held at 8.

---

## Notes for the integrator

1. Insertion anchors are by content, not line number (the lane tree moves): the plans table ends at `plans/wwkd-round-17-coverage.md`; the knowledge table ends at `knowledge/tb2-polyglot-c-py-grader.md` then `lessons/round-1.md`; the lessons table row `lessons/round-51.md` is followed by the `round29`-section rows; the coverage map's last TB2 bullet precedes `## Open gaps`; the Frontier bullet's last TB2 line is the round-46 `Partly discharged` bullet.
2. Keep S-ids in the rows equal to what `corpus/SOURCES.md` holds at landing. At `87301ba` the highest registry id is S178; S179 (TB2 population) is drafted by the wave-1 scribe and is not in the registry yet.
3. Do not paste the knowledge, lesson, coverage or frontier-Variant-A rows if `PREDICATE R52-C1` is not `pass`.
