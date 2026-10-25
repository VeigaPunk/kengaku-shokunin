writer: KengakuR29-2.FCritNoAxisHarm-2

# FCritNoAxisHarm — round 29 post-crash falsify: no-axis-harm attack

- Seat: FCritNoAxisHarm (critic, read-only leaf). Actual writer: `KengakuR29-2.FCritNoAxisHarm-2`.
- Attacks: the C1 statement "calibration8 and other axes unchanged" (`plans/round-29-claims.md:16`) at integrated lane master `56fd949a6478342531e61f4feecb4a685d831640`. The attack covers the coverage/surfaces cap, the gap lines at PROVINCE.md:201 and corpus/README.md:338, freshness (LOG), operability, depth and adjacency, plus a read-only regression run of the four r28 instruments.
- Writes: this report, plus my own scratch `.ufo/waves/round-29/scratch/falsify/FCritNoAxisHarm/` (instrument stdout captures and `quotes.py`). All experiments needing writes ran on copies under `/tmp` (`/tmp/fcnah-base` = `git archive ed26bdf`, `/tmp/fcnah-clone` = local `git clone` of the lane, `/tmp/fcnah-mut` = a copy of that clone at 56fd949). No production, fixture, corpus, SOURCES, SCORECARD or candidate edit. No lane git write, no delegation.
- Production source: **I read parts of `plans/config_projection.py`**: lines 466–547 and grep hits for env, network, write and assert. This is a critic item, not an oracle or re-derivation item, so independence does not apply.
- Tooling: none installed or updated. I used stdlib python3 and coreutils only. No pacman.
- Quotes: every quote below was checked as an exact substring of the stated line by `quotes.py`, which printed `bad 0` with exit 0. Word counts are 4–17 per quote.

## 1. r28 instruments, run read-only at 56fd949 — no regression attributable to round 29

| command (lane root) | exit | compared with | result |
|---|---|---|---|
| `benchmark_spec_audit.py --summary/--selftest/--json` | 0/0/0 | same commands run on `git archive ed26bdf` | all three stdout byte-IDENTICAL (`cmp`); JSON 1900693 bytes |
| `registry_check.py --summary/--selftest/--json` | 0/0/0 | same, baseline archive | all three byte-IDENTICAL; `source_rows_checked=13 … mismatch_sources=0 finding_count=0` |
| `state_check.py --summary/--selftest/--json` | 0/0/0 | `ed26bdf` checked out in `/tmp/fcnah-clone` | 329/318/0/6/5 at both revisions. The only record delta is `NEW P2e.out-of-population.file.evidence/round29-calibration/ OUT_OF_POPULATION` (358→359 records) |
| `round28_census.py --revision 56fd949…` | 0 | r28 receipt `corpus/evidence/round28-calibration/actual-census-corrected.txt` (rev 78e6df8) | deltas only: OOP 29→30, records 358→359, SOURCES rows 69→73, queued 8→12, tier A 63→67; knowledge 36/36, dangling 0, malformed 0 unchanged |

All deltas are the declared round-29 additions: S070–S073 are queued, tier A; `evidence/round29-calibration/` is a new out-of-population file. No MATCH became MISMATCH, no P4 verdict moved (P4 is 48 MATCH, 1 SUPERSEDED, 2 OFFLINE at both revisions), and no frozen verdict class changed.

**Live drift during this wave (observed, not a regression):** at 16:47:54Z an untracked `corpus/lessons/round-29.md` appeared. It is the L1 lesson draft, writer line `KengakuR29-2`. A rerun at 16:48:51Z gave `NEW P2e.out-of-population.file.lessons/round-29.md`, and round28_census then reported OOP 30→31 and records 359→360. The census therefore does not measure revision 56fd949 when it runs in the live lane tree, although its label says so. That is the r28 help text's own caveat ("caller must export or prove byte equality").

**Pre-existing r27/r28 instrument properties (not attributable to round 29; recorded so they are not mistaken for regressions):**
- `P4b.readme.artifact-inventory` counts the gitignored `plans/fixtures/r26/__pycache__/perturb_oracle.cpython-314.pyc` (mtime 2026-10-21 04:51:13 -0300). The lane reads `on_disk_files: 62`; a fresh clone at the same commit reads 61. Both are MATCH. r28 receipts already contain both values: `state-v4-base.json` 61 and `state-final-json.json` 62.
- Running state_check on a `git archive` export with no `.git` turns `P4c.r25.markdown-reports` and `P4c.r25.raw-tree-entries` into OFFLINE_UNVERIFIABLE, giving 316/7 instead of 318/5. Exit is still 0. The "export" route in round28_census's help therefore does not reproduce the r28 receipt numbers.

## 2. Coverage: both-directions index is broken at 56fd949 (fixable defect)

- Counterexample: the coverage cap includes "unindexed files on disk; declared-but-unresolvable surfaces; a gap line contradicted by an artifact already in the repo" (SCORECARD.md:247). At 56fd949 the committed paths `corpus/evidence/round29-calibration/` (6 files), `plans/config_projection.py` and `plans/fixtures/r29/` each have **0** literal hits in corpus/README.md, PROVINCE.md, SKILL.md and SCORECARD.md (`grep -c -F`, all 0). The untracked `corpus/lessons/round-29.md` is also absent from README. My stdlib scan found `lessons not in README: ['round-29.md']`, and `round29-calibration` has 0 README hits.
- No instrument reports this. state_check files it as OUT_OF_POPULATION (disclosed, exit 0), and round28_census checks only `knowledge/`.
- Precedent: r28's pre-admission build commit `18b1922` added a "Round28 supporting artifacts (2026-10-21; knowledge admission deferred)" README table. That table indexed `lessons/round-28.md`, `evidence/round28-calibration/`, both new plans scripts, `fixtures/r28/` and `round28_census.py`. r29's build commit `b98dcf3` and freeze commit `56fd949` touch none of LOG.md, SCORECARD.md, corpus/README.md, PROVINCE.md or SKILL.md (`git show --stat`).
- Impacted axes: coverage, which is held at 7 by the r25 L0 cap. This adds an independent new cap cause, so an L0 ruling alone could no longer lift it. Calibration is also affected: the SCORECARD.md:245 cap includes "any artifact that never reaches `LOG.md`/README".
- Smallest safe correction: append one "Round29 supporting artifacts (knowledge admission deferred)" README table, mirroring 18b1922. It should list `lessons/round-29.md` (once committed), `evidence/round29-calibration/`, `../plans/config_projection.py` and `../plans/fixtures/r29/`, with no frontier-discharge wording. This does not change code or data.

## 3. Gap lines PROVINCE.md:201 and corpus/README.md:338 (tradeoff now; admission-blocking defect if unaddressed)

- Current lines: "generated configs, runtime task validity, hosted judges and contamination remain open." (PROVINCE.md:201) and "generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open." (README.md:338).
- At 56fd949 the projection instrument is committed but the knowledge entry is not admitted. Leaving both lines verbatim before admission follows r28 policy (no frontier discharge before reviewed re-reads), so this is a **tradeoff, not a defect, today**.
- Counterexample at admission: the admission list still reads "index/coverage and source-used-by links." (claims:95). The prereg, candidate draft, `drafts/lesson-and-mistake.md` and `corpus/lessons/round-29.md` all contain **0** hits for `PROVINCE` (`grep -c -i -F`). Admitting `knowledge/webarena-config-projection.md` while PROVINCE.md:201 still says generated configs are wholly open would leave "a gap line contradicted by an artifact already in the repo" (SCORECARD.md:247). r28 avoided this by appending PROVINCE.md:192–202 in its admission commit `df33fc8`, which touched PROVINCE.md.
- Build-wave report `build/R29CritNoAxisHarm.md` §C raised the same omission. The integrated state has not absorbed it: the prereg and candidate are unchanged on this point.
- Location slip in the candidate: line 10 says "Extends corpus/README.md Frontier “generated eval-time configs” left open by round28". That phrase does not appear in README's `## Frontier` section (lines 253–266). Its only occurrence is README.md:338 inside the round28 admitted section, which begins "the original Frontier task-spec-audit gap is closed only for this" (README.md:336). This is a fixable defect: cite README.md:338 and the round28 partial-discharge residual instead of `## Frontier`. It does not change the candidate's facts, but it does change the candidate bytes and therefore the freeze digest.
- Smallest safe correction: add PROVINCE.md to the admitting-commit list. At admission, append (do not edit in place) one dated round-29 paragraph after PROVINCE.md:202 and one after README.md:339. Each should say that an offline source-faithful projection of the dce04686 generator over 812 raw tasks × 3 synthetic `*.invalid` profiles is now held. It should also say that actual env_config/deployment configs, runtime task validity, hosted judges, contamination, and the Terminal-Bench/Toolathlon/SWE-bench Pro specs remain open. Claiming more would be domain bleed into ground C1 disclaims (claims:16–17, 37–40).

## 4. Freshness: no round-29 LOG entry (fixable defect)

- `tail` of LOG.md ends at "### Round28 — corrected measured revision and final evidence". The latest LOG commit is `ed26bdf`, which is the baseline. The three r29 commits (31934e5, b98dcf3, 56fd949) add 0 LOG lines.
- Cadence counterexample: the r26 repair commit 9b0567f, the r27 build commit eeec929 and the r28 build commit 18b1922 each touched LOG.md before admission. The freshness cap is "a round with no re-verification line" (SCORECARD.md:249). Re-verification receipts do exist (`evidence/round29-calibration/sources-before.txt`, `instrument-before.txt`, `build-*.txt`), but no LOG line points to them.
- [INFERENCE] The host-session death at 16:10:51Z is the likely cause; the omission is not intentional scope.
- Impacted axis: freshness 8 is unverified, not lowered, until an entry lands.
- Smallest safe correction: append a "## Round 29" LOG entry. It should name the pins re-verified (manifest f6390b92…, generator 45ddba7b…, raw 7b50386f…), the S070–S073 openings, the build receipts and the crash/seat replacement, with no admission preclaim.

## 5. Operability: wrong-order and wrong-index mutants pass selftest under `python3 -O` (fixable defect)

- The selftest and the production JSON-span invariants rely on bare `assert` statements; `grep -c '^\s*assert '` gives 29 in `plans/config_projection.py`. Python strips these under `-O` and `PYTHONOPTIMIZE`.
- The prereg requires a failing wrong-order witness "before its control counts" (claims:100). The receipt `mutation-witness.txt` shows these mutants killed only by `AssertionError`.
- Measured on `/tmp/fcnah-mut` (a copy at 56fd949):

| mutant (one line edited in the copy) | `--selftest` | `-O --selftest` | `PYTHONOPTIMIZE=1 --selftest` | `--summary` |
|---|---|---|---|---|
| line 143 `for name in reversed(ORDER):` | exit 1 (AssertionError) | **exit 0, `SELFTEST clean cases=20`** | **exit 0** | `TOTAL findings=0 exit=0` |
| line 330 filename from `task_id` instead of index | exit 1 | **exit 0, `SELFTEST clean cases=20`** | not run | `TOTAL findings=0 exit=0` |

- The unmodified control under `-O` also prints `clean cases=20` with exit 0, so the output cannot distinguish the control from a mutant. The production scanner asserts at lines 177, 186, 192 and 196 also disappear under `-O`. Without `-O`, main maps an `AssertionError` from them to exit 2.
- Impacted axes: operability (rubric: "a command in the repo exits 0/1 with a verdict a stranger can run", SCORECARD.md:248) and calibration, through the witness's control-before-count duty.
- Inherited, not new: `benchmark_spec_audit.py` has 19 bare asserts, and its `-O --selftest` also exits 0 with `clean cases=67`. Fixing r28 is outside C1's scope and must not be folded into this round.
- Smallest safe correction: at the top of `selftest()` and `main()`, add `if not __debug__:` that prints a could-not-evaluate finding (for example `assertions_disabled`) and returns 2. Add one CLI selftest case that runs `sys.executable -O … --selftest` and expects exit 2. Replacing all 29 asserts is unnecessary.

## 6. Depth and gate registry (admission-blocking omission; no harm at 56fd949)

- `plans/config_projection.py` is a committed gate (exit 0/1/2 plus `--selftest`). PROTOCOL.md:398 says "a child lane's *registry home* is its own `SKILL.md`." SKILL.md has 0 hits for `config_projection`, and the claims list for admission does not name SKILL.
- r28 added its registry rows (SKILL.md:570–571) and the "Task-spec/scorer observability — round28" section (SKILL.md:674) in admission commit df33fc8, so the pre-admission absence matches precedent.
- Depth stays at 9 only if "a reader can act on `SKILL.md` alone" (SCORECARD.md:246). The candidate's operational decision rule (draft lines 70–75) currently lives only in the draft.
- Smallest safe correction: add "SKILL.md gate registry row (exit map 0/1/2, `--selftest`, pins manifest f6390b92…) plus a round-29 SKILL section carrying the decision rule" to the admitting-commit list. Also add the final SCORECARD row with the explicit `novelty → canonical coverage/constructs` mapping, and restate that coverage 7 is tied and capped with no waiver (build §B, still open: claims has 0 hits for `capped`, `tied` and `waiver`).

## 7. Adjacency and surfaces (no harm found)

- PROVINCE `## Surfaces` and Historical rows have 0 changed lines since ed26bdf (PROVINCE.md is absent from `git diff --stat ed26bdf HEAD`). state_check's P2d/P3b/P3e verdicts are unchanged.
- The instrument does not touch env, network or auth. Grep found no `environ`, `getenv`, `socket`, `urllib` or `importlib`. `subprocess` appears only for selftest self-invocation, and all writes go to a `tempfile.TemporaryDirectory`.
- After `--summary/--json/--selftest`, `find -newer` over the lane showed 0 new lane files.
- `env_config` is parsed only as an AST node (line 65), and the draft keeps the serving plane outside the lane (draft line 80). No foreign scope is absorbed.

## Summary of mismatches

| # | location | value observed | class |
|---|---|---|---|
| 1 | corpus/README.md (whole file) vs committed `corpus/evidence/round29-calibration/`, `plans/config_projection.py`, `plans/fixtures/r29/` | 0 index hits each | fixable defect |
| 2 | `corpus/lessons/round-29.md` (untracked, 16:47:54Z) | not indexed; state_check OOP 30→31 | fixable when committed |
| 3 | PROVINCE.md:201 / README.md:338 vs admission list claims:95 | PROVINCE 0 hits in prereg, draft and lessons | tradeoff now; defect at admission |
| 4 | draft line 10 "Frontier “generated eval-time configs”" | phrase is at README.md:338, not in `## Frontier` (253–266) | fixable defect |
| 5 | LOG.md | 0 round-29 lines across 3 r29 commits | fixable defect |
| 6 | config_projection.py selftest under `-O` | order and index mutants exit 0 `clean cases=20` | fixable defect |
| 7 | SKILL.md registry | 0 `config_projection` hits; not in admission list | admission-blocking omission |
| 8 | r28 instruments | byte-identical or declared-delta only | no regression |

VERDICT: PARTIAL
