# kengaku round 79 — frozen claims (2026-11-04)

L1: `KengakuR79`. Base: the lane tip at round start (`660ec0b9`, round-78 closure spot-check).
This file is frozen **before data**: neither counter below has been run over the after state when it
was written. Amendments land as new `## Amendment` sections; they may only add defects, never move a
target, a control or a kill rule.

Two claims, distinct axes, causally separable: C1 is measured over the census receipt, the ledger,
88 stored grader bodies, the receipts the ledger names and `SKILL.md`'s 16 class rows. C2 is measured
over one spot-check file, `corpus/routed-findings.jsonl`, `corpus/README.md` and the repair artifacts.
Neither counter reads the other's artifact.

## R79-C1 — coverage (lowest non-retired axis, L0-capped at 7)

**Claim.** The **whole 16-class Terminal-Bench 2.0 grader population** (88 members over 230
member-class pairs, derived from `corpus/evidence/round62/class-survey.txt`) becomes a machine-checked
member ledger: every member is accounted exactly once; each `executed` row names a tracked receipt
whose own bytes locate that member in a subject position and carry execution observations; each
`executed-unlocated` row names the round's probe instrument, a receipt under that round and the
`no-subject-stamp` debt; each `unexecuted` row either names a blocker reason whose frozen detector
fires over that task's `tests/test_outputs.py`, or is the honest default `unattempted` when no
detector fires; and all 16 `SKILL.md` class rows carry a derived `executed k of n` plus the ledger
pointer, so `classes-covered` is re-derived for the population instead of quoted from the 2026-10-30
snapshot.

**Why the prior state lacked it.** `SKILL.md` §Decision table states thirteen class rows as a bare
`executed` and three as prose `executed k of n`; `grep -c 'grader-population-ledger' SKILL.md plans/`
→ 0 at base; the ledger it inherits (`plans/grader-selected-members.json`, R78-C1) covers 12 members
over 3 classes. The census publishes `CLASS … members=…` and a single `EXECUTED-COVERAGE
classes-covered=12` line; nothing prices the other 76 members, nothing names which members the lane
replayed after the census, and the five `unexecuted` reasons R78 priced are the only reasons the lane
can state — the rest of the population has no reason at all.

**Frozen predicate (one sentence, same in counter, receipt and report).**
`PREDICATE R79-C1 pass` iff `python3 plans/round79_c1_population_ledger.py --lane .` prints
`DEFECTS n=0` over the universe it derives from the census receipt, and prints the target tuple
`TARGET classes=16 members=88 pairs=230 replayed=<R> located=<E> unlocated=<U> unexecuted=<X>
unaccounted=0 unbacked=0 understated=0 covered=<C>`.

**Counter.** `python3 plans/round79_c1_population_ledger.py --lane .` — modes `--rev REV`,
`--selftest --work DIR`, `--mutants --work DIR`, `--control-namegrep --work DIR`,
`--control-default-reason --work DIR`, `--control-all-blocked --work DIR`. Exit `0` pass, `1` fail,
`2` setup.

**Universe (derived, not listed).** Classes := `CLASS <name> count=<n> members=<csv>` lines of the
census receipt (16, including `container-image count=0`); members := the union of the lists (88);
pairs := the sum (230). The counter refuses if the census is absent.

**Subject shapes (frozen, receipt bytes).** `tb2-header` `^# tb2 <m> grader probe`;
`receipt-header` `^# R<n>-C<m> receipt -- TB2 <m> grader offline`; `grader-path`
`^GRADER .*corpus/evidence/round52/graders/<m>/tests/`; `task-under-test` `^TASK-UNDER-TEST <m>$`;
`capture-tree` `^grader=corpus/evidence/round<n>/tb2-<m>/`. Execution observations:
`^PREDICATE R<n>-C<m> pass` (verdict `predicate`) > any `^VECTOR ` (`vectors`) > any `^CASE `/`^case=`
(`cases`). A replay receipt names at most one population member; a receipt naming two or more is a
population receipt and cannot back an `executed` row.

**Blocker detectors (frozen in the counter, not in the ledger), over
`corpus/evidence/round52/graders/<m>/tests/test_outputs.py` only.** `browser-required`
(`selenium|webdriver.Chrome/Firefox|chromedriver`), `vm-required`
(`qemu-system|qemu-img|/app/isos/|win311`), `external-db-required`
(`GOLDEN_SQL_PATH|/tests/golden.sql|DB_PATH = Path(`), `candidate-library-required`
(`sys.path.append("/app"`). A blocker reason whose detector is silent is `REASON-UNBACKED`; an
`unattempted` row whose detector fires is `REASON-UNDERSTATED` — overclaiming is priced in both
directions, which is why the old "four named blockers" sentence cannot stand.

**Defect classes.** `MEMBER-UNACCOUNTED`, `MEMBER-EXTRA`, `PAIR-MISMATCH`, `STATUS-UNKNOWN`,
`RECEIPT-UNTRACKED`, `RECEIPT-NO-OBS`, `RECEIPT-POPULATION`, `SUBJECT-ABSENT`, `SUBJECT-MISMATCH`,
`VERDICT-MISMATCH`, `INSTRUMENT-UNTRACKED`, `INSTRUMENT-SUBJECT`, `ROUND-MISMATCH`,
`UNLOCATED-RECEIPT-OUTSIDE-ROUND`, `UNLOCATED-SUBJECT-PRESENT`, `DEBT-UNNAMED`, `REASON-UNKNOWN`,
`REASON-UNBACKED`, `REASON-UNDERSTATED`, `EVIDENCE-SHAPE`, `EVIDENCE-MISMATCH`, `CLASS-ROW-ABSENT`,
`CLASS-ROW-UNQUANTIFIED`, `CLASS-K-MISMATCH`, `LINK-ABSENT`, `LEDGER-SHAPE`, `TABLE-ABSENT`.

**Before → after.** Before (`--rev 660ec0b9`): no ledger → `LEDGER rows=0`,
`unaccounted=88`, 13 `CLASS-ROW-UNQUANTIFIED` + 1 `LINK-ABSENT` + class drift,
`DEFECTS n=105`, rc 1 (`corpus/evidence/round79/c1-before.txt`). After: `LEDGER rows=88
executed=18 unlocated=6 unexecuted=64`, `DEFECTS n=0`, `COVERAGE replayed=24 covered=15
uncovered=container-image census_covered=12`, rc 0.

**Controls (each must lose, and does).** `--control-namegrep`: call a member `executed` when any
verdict-bearing receipt mentions it — the census receipt mentions all 88, so the control reaches
`executed=88` and the frozen population rule fires `RECEIPT-POPULATION` on every row;
`--control-default-reason`: mark every `unexecuted` member `unattempted` without the detector sweep →
7 `REASON-UNDERSTATED`; `--control-all-blocked`: mark every `unexecuted` member
`browser-required` → 62 `REASON-UNBACKED`. All three print `target_reached=False`.

**Kill rules.** A red before-run at the base revision and a green after-run at the landing tip are
both required; the mutant matrix (6 mutations) must kill 6/6; a control that reaches the target
invalidates the counter and the claim is withdrawn before data; a `SKILL.md` cell whose `k` does not
equal the ledger's count for that class is `CLASS-K-MISMATCH`, whatever the prose around it says.

**Axis.** coverage — the surface is the 88-member population map (the 76 members no round has ever
priced) and the 16-row class table, not the numbers 18/6/64/15.

## R79-C2 — calibration (held at ceiling 10, exercised)

**Claim.** The round-78 closure's seven routed defects (`R78-D1` … `R78-D7`) are **discharged, not
restated**: each has exactly one row in `corpus/routed-findings.jsonl` with `status=closed`, a
`source` that resolves to the spot-check line carrying its id, a `close` that names a tracked repair
artifact (never the spot-check file itself) whose bytes carry the id, and a `check` command that
exits 0 exactly when the repair holds and is not a command that cannot fail; and
`corpus/README.md` indexes the spot-check file.

**Why the prior state lacked it.** At base `grep -c 'R78-D' corpus/routed-findings.jsonl` → 0 and
`grep -c 'round-78-verifier-spotcheck' corpus/README.md` → 0: the closure routed seven defects to this
round and the lane's own burn-down ledger (`plans/routed_open.py`) cannot see them, so "routed to
round 79" was where they would have died.

**Frozen predicate (one sentence, same in counter, receipt and report).**
`PREDICATE R79-C2 pass` iff `python3 plans/round79_c2_closure_debt.py --lane .` prints `DEFECTS n=0`
and the target tuple `TARGET ids=7 closed=7 checks_passed=7 indexed=yes`.

**Counter.** `python3 plans/round79_c2_closure_debt.py --lane .` — modes `--rev REV` (extracts that
tree with `git archive` and runs every `check` there), `--selftest --work DIR`, `--mutants --work
DIR`, `--control-presence --work DIR`. Exit `0` pass, `1` fail, `2` setup.

**Universe (derived, not listed).** Ids := `^- \*\*(R\d+-D\d+) \([a-z]+\)` lines of
`corpus/lessons/round-78-verifier-spotcheck.md` §6 (7).

**Defect classes.** `DEBT-UNREGISTERED`, `DEBT-DUPLICATE`, `ROW-INVALID`, `STATUS-UNKNOWN`,
`SOURCE-MISMATCH`, `SOURCE-LINE`, `CLOSE-ABSENT`, `CLOSE-NOT-REPAIR`, `CLOSE-NOT-EVIDENCE`,
`CLOSE-COMMIT`, `CLOSE-UNRESOLVED`, `CHECK-TRIVIAL`, `CHECK-FAIL`, `BLOCKER-ABSENT`, `INDEX-MISSING`.

**Before → after.** Before (`--rev 660ec0b9`): 7 `DEBT-UNREGISTERED` + `INDEX-MISSING`,
`DEFECTS n=8`, `TARGET ids=7 closed=0 checks_passed=0 indexed=no`, rc 1
(`corpus/evidence/round79/c2-before.txt`). After: `closed=7 checks_passed=7 indexed=yes`,
`DEFECTS n=0`, rc 0.

**Control (must lose).** `--control-presence`: register all seven ids as closed with the spot-check
file as `close` and `true` as `check` — the cheapest skip of the work. It reaches
`closed=7` and dies on `CLOSE-NOT-REPAIR` ×7 + `CHECK-TRIVIAL` ×7;
`CONTROL presence target_reached=False`.

**Kill rules.** A red before-run at the base revision and a green after-run at the landing tip; the
mutant matrix (4 mutations: drop a row, close naming the spot-check, a trivial check, a reopened
status) must kill 4/4; every `check` must fail at `--rev 660ec0b9` and pass at the landing tip — a
check that passes at base is not a check and is `CHECK-TRIVIAL`'s sibling defect, reported.

**Axis.** calibration — the surface is the lane's self-assessment of its own closure debt
("discharged" vs "restated"), not a new number about the domain.

## Census and frontier (rides inside the cap; not a third claim)

- `corpus/SOURCES.md` curated in-round: one new row opened live for the blocker taxonomy (the
  harness's own container/network model) and one `own-work` row for the population ledger; the
  reason taxonomy's overclaim is the round's mined mistake.
- Census: `scripts/sources-census.sh validate --root … kengaku` at round start and round end.
