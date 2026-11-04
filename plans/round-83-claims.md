# kengaku round 83 — frozen claims

2026-11-04, hyaku run 15, attempt 1; L1 KengakuR83 holds planner seat.
Base revision: 614f00559c75155ec100e945b3e8257b14fb7496 (master, round-82 outside closure).
Two separable claims. Coverage is lowest non-retired axis (7, L0 cap); calibration is 10 held.
No stagnation waiver. No novelty construct or score increase is claimed.

## R83-C1 — coverage: first offline replay of code-from-image

Predicate R83-C1: the base-unexecuted `code-from-image` member has one located, host-pinned receipt whose eight frozen case vectors reproduce the captured grader's two test functions, with zero mismatches, and the population ledger marks that receipt executed in round 83.

The subject is the tracked `corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py` at BASE, unmodified. Its file-artifact class was held, but this member had never run; this is member coverage, not a new class/method or solving the task. The grader itself must read a real `/app/output.txt` inside bubblewrap: no reimplementation, function patch, mocked Path/open, or host `/app` writes. Each test function runs independently in source definition order. AssertionError or FileNotFoundError is F, normal return is P; any other exception is a setup defect. The staged file is supplied as UTF-8 bytes by plans/round83-cases.json; a null means absent. The frozen table lists eight cases and predictions. Every leg has P and F witnesses; the equality and prefix assert sites have independent red witnesses.

Counter: `python3 plans/round83_c1_replay.py --lane . [--rev REV] --work DIR`.
Target: `TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`, `PREDICATE R83-C1 pass`, exit 0.
Before: located=0 executed=0, fail. Receipt path `corpus/evidence/round83/code-from-image-probe.txt`; replay instrument `plans/round83_code_image_probe.py` accepts `--lane DIR --work DIR`; header `# tb2 code-from-image grader probe`; output `CASE <id> predicted=<P/F vector> observed=<vector>` (slash separated), summary `cases=8 mismatches=0` and `PREDICATE R83-PROBE pass`. Receipt pins MEMBER, SUBJECT_CAPTURE, SUBJECT_SHA, CASE_TABLE_SHA, TOOL, TOOL_SHA, HOST_PYTHON, HOST_OPENSSL, LANE_TIP, WORKTREE clean, COMMAND (exact reconstructed argv modulo work path), EXIT 0, OBSERVATIONS_BEGIN/END. LANE_TIP must resolve and its subject/table/tool digests must equal stamped digests; observation block equals a fresh run's CASE lines and predicate. The gate reads ledger/receipt from the measured tree, not current mutable files in --rev mode. Tool itself must reject a changed subject or table digest.

Controls must lose before real scoring: do-nothing (no receipt), ledger-only (executed flag but absent receipt), fabricated observations (syntactically complete stamp but wrong CASE vectors). Keep stdout/exit evidence. Counter selftest: green plus missing-receipt, wrong-subject, wrong-tool, wrong-table, wrong-vector, missing-case, wrong-ledger (at least eight cases); mutants apply actual data corruptions and require finding-specific nonzero. Fixtures may inject a runner, but the real receipt run cannot. Exit 0 clean, 1 failed, 2 could-not-evaluate. A control reaching target, setup failure, altered frozen input, missing stamp or mismatch kills C1. No after-state narrowed after scoring.

## R83-C2 — calibration: outside spot-check debt versus current record

Predicate R83-C2: the eight R82-V1 through R82-V8 self-assessment/record mismatches named in the round-82 outside spot-check have substantive repairs at the measured tree, each has a closed routed-findings row resolving its source and repair, and each repair check fails against the base tree.

Universe: exactly the eight `- **V<n> ·` routed defects in `corpus/lessons/round-82-verifier-spotcheck.md` section 6 at BASE; no newest-file or moving-id selection. The counter is `plans/round83_c2_debt.py` and checks `plans/round83_c2_checks.py`; reuse prior gate structures but do not edit historical gates. Counter commands: `python3 plans/round83_c2_debt.py --lane . [--rev REV] --work DIR`, `--selftest`, `--mutants`, `--control-presence`, `--sensitivity`. Target `TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0`, `PREDICATE R83-C2 pass`, exit 0; before eight unregistered ids plus missing index, fail. Sensitivity requires `failed_at_base=8` using the CURRENT checks against BASE bytes (instrument copied, repair bytes never copied).

Each row has source `<spotcheck>:<actual line carrying Vn>`, close pointing to tracked `corpus/lessons/round-83.md`, evidence_literal carried by the repair paragraph, status closed and check `python3 plans/round83_c2_checks.py vN`. The lesson states corrections, not edits to filed round82 report/LOG/SCORECARD/lesson. Counter refuses duplicate ids, trivial checks, nontracked repair/source, absent literal, and nonzero repair checks. Every new SOURCE correction uses a supersede row, never edits frozen row cells.

Substantive checks:
- V1: supersede S262 and S263 with anchor quote counts mechanically recomputed (4 and 2), preserving old rows; round83 lesson explicitly corrects round82 Gate/report annotations. Check extracts quoted text/count from the NEW rows, not merely literal corrected numbers. Record the correction rather than rewrite round82 lesson.
- V2: committed `corpus/evidence/round83/r82-census-after.txt` contains COMMAND, REV equal to a44b2f083ee8b4115aea64598646f4bd9e3c1470, EXIT 0 and the observed full historical registry census with W04=27. Round83 correction explicitly supersedes the reported 26 after-count; check counts W04 output lines.
- V3: correction states affected=6, unrecovered=2, recovered=4, distinguishing final statuses from provider-interrupted seats; names all six affected identities from the spot-check. A retained machine-readable receipt derived from round82 results records final terminal/empty counts separately. No invented provider events from final statuses.
- V4: correction names 82fe89d5 as the addition commit for both C2 tools; check `git log --diff-filter=A` or pinned commit file membership re-derives attribution (BASE-mode lacks round83 correction).
- V5: README has valid three-cell rows for round82 lesson and round81 and round82 outside spot-checks; correct missing-cell row; check parses rendered table cells and exact file paths.
- V6: round83 Gate enumerates S265 and S266 URL/access date/located <=25-word quote, explicitly correcting round82 omission; append rejected supersede S264 row with teaches `supersedes S264 — REJECTED: ...; flip: ...` and status rejected. No old SOURCES immutable cell modified.
- V7: correction states seven of ten new registry rows declare selftests and names the three `none declared` exceptions (round37-c1-attribution, round80-c1-remint, round82-c2-checks); check recomputes ten row selftest cells.
- V8: correction states round82's ~07:24 was local -03:00, not Z, hence ~10:24Z; historical report remains byte-identical; check requires this explicit correction and convention UTC for this round's times.

Control presence-only registers eight closed rows but leaves repair bytes unchanged; must fail CHECK-FAIL or substantive defect. Selftest green plus source/literal/trivial/missing-row/index/nonclosed/duplicate/failed-check corruptions; mutants require attributed real data mutations. Exit 0 clean, 1 failed, 2 could-not-evaluate. Any defect or base-insensitive check kills C2. C2 does not read C1 artifacts except shared lesson prose; C1 never depends on C2 records, SOURCES fixes or README.

## Frontier and wave contract

One v1 wave 12 seats, >=25% attack; L1 planner, bounded planner data-walk via scout. Three code executors, two scribes, scout, connector, reviewer, critic, mutation-tester, plus two bounded code/attack seats as spec names. Every seat leaf, no task calls. Only L1 integrates production files and commits. Scratch `/fast/scratch/hyaku/kengaku-r83/<seat>/`, cleaned before yield. One-source C1 opening grounds new S267; C2 corrections reserve S268/S269/S270 (supersede S262/S263/S264). Frontier admits and rejects retain their source locators. Assimilation: none; considerthese proposal1 burn-down already implemented, proposal2 still unimplemented and not widened this round. Planned r82 sweep divergence/anchor blindspot remain named backlog, not secretly declared as claims.
