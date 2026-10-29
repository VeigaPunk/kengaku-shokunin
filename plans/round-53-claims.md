# Round 53 — frozen claims (kengaku, hyaku run 11, 2026-10-28)

L1 `KengakuR53`. Base tip `536925b5320fa64298030b4ee76a58fc4b82723f` (lane branch `master`, `jj-lane.sh state`
`ahead=0 behind=0`). Frozen **before** wave 1 is dispatched. A rule, counter or threshold below is never changed
after a seat has scored; a later change is a dated amendment at the bottom, with the before-state still re-derivable
(PROTOCOL append-only; round-52 lesson `instrument-falsified-after-freeze`).

## Axis choice and the lowest axis

Lane axes (`../MISSION.md`): **novelty + calibration**. Scores at the base tip (`SCORECARD.md`, round-52 section):
novelty 8, calibration 9, depth 9, operability 9, freshness 9, adjacency 9, **coverage 7**.

Coverage is the lowest non-retired axis and **is not claimed**: it is capped at 7 by the open L0 questions
`kengaku | round-25`, `round-33` and `round-51` (`.ufo/l0-questions.md`), none answered; no answer is assumed
(prompt §8: route around). The round works novelty (8→9) and calibration (9→10) exactly as rounds 48–52 worked the 8s
and 9s, and says so. Stagnation nudge: not invoked (coverage 7 < saturation line 8). No exploratory claim.

Both claims answer the round-52 closure's routed defects 1 and 4 and `QUALITY.md` Q42: (a) a forged-but-complete
control is frozen and shown to fail; (b) every input the predicate trusts is pinned by a digest constant or by git
history, not by a file the lane writes; (c) a row-existence counter is claimed as existence only — "truthful" needs an
executed leg per row.

## Claim 1 — R53-C1 (novelty 8 → 9): a sound presence-only grader triage of Terminal-Bench 2.0

**Surface moved.** Round 52 landed the first whole-benchmark triage of the 89 TB2 task graders and was **not admitted**:
its per-test class (a lexical split) disagreed with independent counts (33 / 47 / 54 presence-only tests), its predicate
was reachable without reading a grader (five routes, `.ufo/waves/round-52/w2/W2CritC1Reach/`) and 0 of 16 mutants were
killed (`W2MutC1`). This claim lands the instrument that survives those attacks: an AST classifier scored against an
independent blind-label oracle, pinned inputs, and a prior-art leg that re-reads archived fetches.

**Counting command (frozen).**

```sh
python3 plans/round53_c1_triage.py --lane .      # run on a clean clone of the landing tip
```

**Before (base tip, `.ufo/waves/round-53/claims/c1-before.txt`, exit 1).**

```
PINS population_sha=ok pin_tree_sha=BAD tests_index_sha=BAD captures_blob_match=0 …
FREEZE absent freeze=False classifier=False labels=False
CONFIRM new_confirmed=0      PRIOR-ART rows=0      PREDICATE R53-C1 fail
```

Corroborating before-state: the round-52 classifier's per-test class on the same 305 tests is the control in leg 2.

**Frozen predicate — one sentence, the same in this file, in `plans/round53_c1_triage.py` and in the receipt.**
`PREDICATE R53-C1 pass` iff all five legs hold on a clean clone:

1. **PINS** — `plans/round52-tasks.json` sha256 = `0230b68c…5cfc`; `corpus/evidence/round53/pin-tree-2fd12b88.json`
   sha256 = `96b47248…cbb9` (the GitHub trees API listing of pin `2fd12b88`, 1038 blobs); `tests-index.json` sha256 =
   `579d567f…7897c7330`; each of the 183 captured files' **git blob SHA-1** equals the pin-tree blob for its path
   (`captures_blob_match=183 blob_bad=0 absent=0`); the one operator-excluded capture
   `sanitize-git-repo/tests/test_outputs.py` stays absent and its pin-tree blob is `3269e74e…dacf199dda`
   (`excluded_blob=ok`). The exclusion is therefore part of the frozen population from the start — the round-52
   `183/184` miss cannot recur.
2. **FREEZE + ORACLE** — `plans/round53_c1_classify.py` (`classify_source(src) -> {test key: 'P1'|'P0'}`) has the sha256
   recorded in `plans/round53-c1-freeze.json`, and the commit that first added that freeze file is a strict git ancestor
   of the commit that first added `corpus/evidence/round53/oracle-labels.json` (labels read only after the classifier was
   committed). `oracle-labels.json` gives, for each of the **305** tests, two labels from two distinct labeler seats that
   are not in the freeze file's `author_seats`. A test is *decided* when both labels agree and are `Y`/`N`. The v2 class
   `P1` must equal `Y` on all but **≤ 3 %** of decided tests, **contested** (disagree or `U`) tests must be **≤ 15 %** of
   the 305, `unclassified = 0`, and the **control** must show the leg is not vacuous: the round-52 per-test classifier
   (`plans/round52_c1_grader_audit.py classify_tests`, run by the counter on the same bytes) must disagree with the oracle
   on **≥ max(10, 2 × v2's disagreements)** decided tests (`ORACLE-CONTROL control_ok=yes`). If the control meets the
   target, the leg is vacuous and the claim is not admitted.
3. **CONFIRM** — `corpus/evidence/round53/confirmations.json` holds **≥ 3** distinct tasks, each `confirmed is True`
   (type-checked), each a **never-read** task (its id occurs in none of the base-tip texts `SCORECARD.md`, `LOG.md`,
   `SKILL.md`, `corpus/README.md`, `corpus/knowledge/*.md` except the round-52 triage entry, read with
   `git show 536925b…:<file>`, and not in the round-52 `confirmations.json`), naming a test the v2 classifier puts in `P1`,
   with a `quote` of **≥ 20 characters found inside that test function's own line span** in the capture, a `reader` that is
   neither in `author_seats` nor `KengakuR53*`, and a `report` path under `.ufo/waves/round-53/` whose sha256 equals
   `report_sha256`, whose path contains the reader's name and whose text names the task.
4. **PRIOR-ART** — `corpus/evidence/round53/prior-art.json` has one row per confirmed task and no rejected row; each row
   has a verdict `phenomenon-new` or `phenomenon-known`, a real `url` (not `example.org`), an archived fetch under
   `corpus/evidence/round53/fetched/` whose sha256 matches, and a verbatim 8–25-word `quote` found in that archive;
   a `phenomenon-known` row's archive must itself name the task or one of its test names; a `phenomenon-new` row carries a
   `sweep` of **≥ 2** archived fetches that do **not** name the task or its test names (a negative claim carries its
   sweep). Over all rows: **≥ 3** distinct URLs and **≥ 1** `phenomenon-new` row.
5. Nothing else is a leg. Printed `ORACLE`, `ORACLE-CONTROL` and `CONFIRM` numbers outside the thresholds above are
   evidence, not legs.

**Kill rule.** Any leg failing on the landing tip, or the control leg vacuous, means **novelty stays 8 and the round
reports C1 not admitted** — no narrowing after the fact. The classifier is never edited after the freeze commit; a
disagreement the oracle shows is a result, not a bug to repair.

**Frozen controls (each must make the counter fail on the named leg; receipts in `.ufo/waves/round-53/claims/`).**
`c1-selftest.txt` carries 22 fixture cases (`--selftest`, `cases=22 failures=0`): the forged-complete routes of round 52 —
capture bytes replaced by a stub (`blob_bad=1`), population JSON shrunk (`population_sha=BAD`), `confirmed:"false"`,
reader = author, one-word quote, quote outside the test span, report digest forged, `example.org` URL, archive digest
forged, quote absent from the archive, `phenomenon-new` without a sweep, labeler = classifier author, one labeler
twice, classifier edited after the freeze, plus the null cases. Real-tree controls on the landed evidence are produced
by wave-1 seats on scratch copies and committed (`c1-control-*.txt`): population-of-names-only, every-class-P0
(`all_P0_disagree` ≫ threshold), labels copied from the classifier's own output (order leg), the round-52 classifier
substituted for v2.

## Claim 2 — R53-C2 (calibration 9 → 10): every registry row's tip-state is declared and re-executed

**Surface moved.** `SKILL.md`'s *Gate/probe registry* lists 75 instruments whose cells state what an exit code means
and what the instrument returned **at its own landing tree**. Nothing declares what each returns at the tip, so the
registry's self-assessment can drift from observed state without any counter noticing (round-52 `false-registry-cell`,
Q42 clause c). A manual probe at the base tip (`.ufo/waves/round-53/claims/c2-before-manual-probe.{py,txt}`, a clean
shared clone, one run per row, `60` of `73` parsed rows runnable as written) found **22 rows exiting non-zero and 38
exiting 0, 13 rows with no runnable argv in the cell** — for example `round51-surfaces` exits 1 (`NUMBER-DRIFT SF14 row
claims 171, probe says SOURCES rows=186`) and `state-assertion-check` exits 1 (`VERDICT: FAIL`), while their registry
rows say `0` on a clean tree. This claim makes the registry's tip-state a declared, re-executed fact.

**Counting command (frozen).**

```sh
python3 plans/round53_c2_tipstate.py --lane . --source <clean shared clone of the landing tip> --work <scratch> [--jobs 4]
```

**Before (base tip, `.ufo/waves/round-53/claims/c2-before-head.txt`, exit 1).**
`ROWS registry=75 ledger=0 missing=75 …`, `LEDGER ledger absent: plans/round53-tipstate.json`, `PREDICATE R53-C2 fail`.

**Frozen predicate — one sentence.** `PREDICATE R53-C2 pass` iff, on a clean clone: every registry row has exactly one
entry in `plans/round53-tipstate.json` (`missing=0 extra=0 duplicate_names=0`); each entry's argv names the same script
as its row's entry cell (`entry_mismatch=0`) with a `kind` of `entry`, `selftest` or `help` and a declared exit code
consistent with its `state` (`bad_decl=0`; at most 10 % of rows may be `help`-kind); every `red` row carries a reason of
**≥ 10 words** and a verbatim `evidence` fragment (`bad_reason=0`); and the counter **re-executes every argv** in a
scratch clone and observes **exactly the declared exit code** with **no timeout** (`executed = registry`,
`mismatched=0 timeout=0`) and every red row's `evidence` fragment present in the observed output
(`evidence_missing=0`), the source clone being clean (`clean=yes`).

**Kill rule.** A single row whose observed exit differs from its declared exit, any timeout, any row without an entry, or
a run with `--only` (never a pass) is `fail`; the claim is then not admitted and calibration stays 9. Re-executing is the
counter's job; the ledger is the lane's self-assessment, so a ledger that copies observed output is *truthful*, not a
forgery — the leg being measured is mismatches between declaration and observation.

**Frozen controls (each must fail the counter on the named leg).** `c2-selftest.txt` (`--selftest`, `cases=12 failures=0`):
truthful pass; forged all-green; forged all-red with a plausible fragment; missing row; extra row; ledger pointing at
another row's script; red evidence absent from output; thin reason; state/exit inconsistency; timeout; help-only argv;
partial run. Real-tree controls on 2–3 representative rows (one red, one green) via `--only` on scratch copies, committed
as `c2-control-*.txt`: ledger absent; every row declared green (the "registry says `0`" reading — must `MISMATCH` on every
red row); every row declared red; a red row whose `evidence` fragment was altered.

## Frontier step (inside the 1–3 claim cap)

- **Census** (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`), round start (this
  attempt, before any edit): 15 pre-existing `W04` duplicate-url warnings, `ok`, **exit 0**, 186 rows
  (`grep -c '^| S[0-9]' corpus/SOURCES.md` → 186). Round end: the report pastes the same command and exit code.
- **Sourced claim.** C1's prior-art leg rests on `SOURCES.md` rows opened this round (S194+ — new test-quality or
  benchmark-audit literature; each row's `## Gate` entry carries URL, 2026-10-28 access date and ≤25-word located quote);
  the knowledge entry that lands cites them.
- **Mined mistake.** `corpus/lessons/round-53.md` `## Mistakes`: at minimum the round-52 classes this round repairs
  (`rule-unit-leak`, `counter-reachable-without-the-work`, `false-registry-cell`) with each fix shown able to fail.
- **Carried routed defects (closure of round 52).** (2) the untracked `tb2-paper-full.html` is deleted before landing;
  (3) absolute host paths in round-52 `confirmations.json` are left as landed history (append-only) — the round-53
  evidence files use repo-relative paths only (enforced by the `report` leg of CONFIRM); (4) the C2 `SELFTEST-UNBACKED`
  span fix and K5/K7 controls stay carried, not claimed.
- **Assimilation:** none planned (the frozen claims predate it). `considerthese/`: no proposal taken.

## Round shape

Two v1 waves (policy v1, band 32–64): wave 1 builds (classifier, oracle labels, ledger rows, controls, sources) and
wave 2 falsifies and confirms (readers, prior-art fetchers, attack seats). The canonical §3 planner seat is the L1 (the
validator rejects `planner`). Total 64–128 seats; attack share ≥ 25 %.

## Amendments

Dated entries are appended here, never edited in place. Frozen text above stays as written; where an amendment changes a
rule, the amendment is the rule from its date and the before-state stays re-derivable from commit `a34838f`.

### A1 — 2026-10-28, after wave 1, before any scored run (L1 `KengakuR53`)

**Why.** Wave 1 attacked both frozen counters before data (`C1CritCounterReach`, `C1MutCounter`, `C1SentinelScreen`,
`C2CritLedgerReach`, `C2MutCounter`; reports `.ufo/waves/round-53/w1/<seat>.md`). They landed: C1 passed with an all-`P1`
"classifier" and labels copied from it (the order leg only compared commit order; the planned "labels copied" control could not
fail); a classifier + freeze-digest edit in a later commit passed FREEZE; a contested budget excluded 45 wrong tests from the
disagreement count; report/archive paths escaped by `..` or an absolute path; a sweep of one file listed twice passed; a
`phenomenon-known` row only had to name the task id once; the selftest killed 25 of 81 mutants. C2 passed with zero rows, with a
renamed heading, with 70 of 75 rows, with argv `python3 -c pass <script>` or `sh -c "...; exit 0" <script>`, with a source clone
older than the lane, with a non-git source, and ran every row under the full environment (nine credential-shaped variables).
No seat had scored a claim: no label file had been opened by the L1, no classifier output compared to a label, no ledger measured.

**What changed (both counters rewritten; `--selftest` now `plans/round53_c1_triage.py` 44 cases, `plans/round53_c2_tipstate.py` 50 cases, each
recorded under `.ufo/waves/round-53/claims/` with the forged-complete routes above as named cases).**

*C1.* (1) FREEZE: the classifier and `plans/round53-c1-freeze.json` must be added in **one** commit and never touched by any later
commit (`git log -- path` has exactly one entry each); the freeze file pins by sha256 the classifier, the eight label-seat files and the
eight shard files; the label-seat files are added in **strictly later** commits and never touched again; the tree must be clean.
(2) The oracle is merged by the counter from the eight seats' own files `.ufo/waves/round-53/w1/<seat>/labels.json` over the pinned shards
(each test in exactly two shards, the labeler files must cover exactly their shard), there is no separately authored label file; a
labeler named in `author_seats` voids its rows; `author_seats` may not hold a `C1Label*` seat. (3) The ORACLE leg adds: the classifier agrees with
**≥ 90 %** of the individual non-`U` labels, and decided `Y` and decided `N` each reach **≥ 10** (an all-`Y` copy cannot pass). The 3 % disagreement bound, the 15 %
contested bound, the 305-test total and the control rule stay as frozen. (4) `plans/round52_c1_grader_audit.py` (the control) is pinned by
sha256 `0b1d4213…a7b3`; the classifier module is imported only after FREEZE holds. (5) CONFIRM: `report` must resolve inside
`.ufo/waves/round-53/` (no `..`, no absolute path, no symlink), name the task as a whole token, and the reader may not be a `C1Label*` seat; an
unavailable `BASE_TIP` fails closed. (6) PRIOR-ART: archive and sweep paths resolve inside `corpus/evidence/round53/fetched/` (no `..`, no symlink);
each archive's first line is `SOURCE-URL: <url>` and must equal the row's URL; a `phenomenon-known` row's **quote** must name the task or one of its tests;
a `phenomenon-new` row's archive must not name the task or its tests, and its sweep must be ≥ 2 **distinct** archives with headers that do not
name them. The thresholds (≥ 3 URLs, ≥ 1 `phenomenon-new`, ≥ 3 confirmed) are unchanged.

*C2.* (1) The registry heading is matched line-anchored, exactly once; table lines whose first cell is not a backticked name fail (`BAD-NAME`);
the row set must equal the 75 frozen names (digest `df38a8fc…d0a4` of the sorted names, the file `.ufo/waves/round-53/c2-row-names.json`) plus the two rows this round adds
(`round53-c1`, `round53-c2`). (2) Registry and ledger are read from `--source` (the clean tree under test), not from `--lane`; `--source` must be a clean git work tree whose
HEAD equals the lane's HEAD. (3) argv is `python3 <row script> …` or `uv … python3 <row script> …`; no shell, no `-c`, no wrapper; `kind` must match the argv
(`--help` ⇔ `help`, `--selftest` ⇔ `selftest`, else `entry`); the ledger is rejected on a duplicate JSON key; evidence must be a string. (4) Rows run with credential-shaped
environment variables removed (`TOKEN`, `KEY`, `SECRET`, `PASSWORD`, `OP_*`, `SSH_AUTH_SOCK`, `COOKIE`), and a failed worker reset is an error. The 10 % help-kind cap,
≥ 10-word reasons, verbatim evidence and the exact-exit rule are unchanged.

**Containment (recommended invocation, not a leg).** The C1 counter imports a seat-written classifier: run the scored command as
`bwrap --unshare-net --ro-bind / / --dev /dev --bind <scratch> /tmp --setenv TMPDIR /tmp --chdir <clean clone> python3 plans/round53_c1_triage.py --lane .`
(verified by `C1SentinelScreen` to pass both selftests).

**Not changed (named, not hidden).** "Never-read" still means *not named in the base-tip lane texts and not confirmed in round 52*: the round-52 critic's machine
receipt `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json` records per-test classes for the same tasks and the counter does not consult it
(`C1CritCounterReach` R11); a P1 classifier that is correct cannot be told from a copy of the labels by the counter alone: independence of the label seats
is a protocol property recorded in the seat reports, not something the counter can prove (`C1CritCounterReach` R4). A C2 ledger entry for a gate that cannot fail
(a script that always exits 0) is still truthful; the counter measures declaration against observation, not the strength of the instrument.

### A2 — 2026-10-28, after the freeze commit `d40b705` and the label commit `db90a6b`, before the confirmations, prior art or any C2 full run were scored (L1 `KengakuR53`)

Four mechanical corrections, none of which touches the frozen classifier, the label files, a threshold, or the oracle result printed at `db90a6b`
(`.ufo/waves/round-53/claims/c1-after-oracle.txt`: `disagree=0`, `ORACLE-CONTROL control_ok=yes`):

1. **C1 `names_task` ignores the archive's own `SOURCE-URL:` header line.** A sweep of the tracker for task `X` is an archive whose header URL legitimately carries `X`
   (`…/search/issues?q=…+X`); the A1 rule (a sweep archive must not name the task) was read against the whole file including that header, which made every honest negative sweep
   unusable. The body must still not name the task or its tests (selftest `forged-sweep-body-names-the-task` fails it; `sweep-header-may-carry-the-task-id` passes).
2. **C2 registry heading regex accepts the real suffix.** The registry heading in `SKILL.md` is `## Gate/probe registry (PROTOCOL §Gate standard)`; the A1 regex required the bare heading
   and counted zero rows on the real file (found on the first `--dry` run; the selftest fixtures used the bare heading). The regex is now `^## Gate/probe registry( \(…\))?$`, still line-anchored and
   still required exactly once; a prose mention inside a table cell does not match.
3. **C2 pinned row set gains one name: `stage-scan`.** The wave-1 executor `C1ExecStageScan` delivered the pre-stage credential-pattern scan that the round-52 lesson proposed and did not land
   (`plans/stage_scan.py`, 33-case selftest, `.ufo/waves/round-53/w1/C1ExecStageScan/`). Landing a runnable script requires a registry row (round-52 C2 rule), so the allowed extras are
   `round53-c1`, `round53-c2`, `stage-scan` (registry = the 75 frozen names + these three = 78). The frozen-names digest `df38a8fc…` is unchanged.
4. **Receipts.** `c1-selftest.txt` / `c2-selftest.txt` are regenerated after the A1/A2 edits; the A1 text's case counts (44 / 50) are superseded by the printed
   `SELFTEST cases=<n> failures=0` lines of those receipts.

Still frozen and untouched: every leg threshold, the 305-test population, the control rule, the confirmation and prior-art thresholds, the kill rules.
