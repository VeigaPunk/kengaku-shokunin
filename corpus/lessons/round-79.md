# Round 79 — kengaku (2026-11-04 UTC)

Base `660ec0b9` (round-78 closure spot-check). Freeze `5d684313` (two claims, two counters, the
88-member ledger, the 16 derived `SKILL.md` class rows, the before receipts, the three losing
controls). R79-C1 targets coverage (lowest non-retired axis, L0-capped at 7): the whole 16-class
Terminal-Bench 2.0 population becomes an 88-member ledger with a subject-locating receipt per
executed member, a named instrument per unlocated replay, and a detector-backed reason or the honest
`unattempted` default for every member no round has replayed. R79-C2 targets calibration (held at
ceiling 10, exercised): the round-78 closure's seven routed defects are discharged with checks that
fail at the base revision.

## Gate

- **S256 admitted** for the execution surface the blocker taxonomy rests on: a Terminal-Bench 2.0
  run is a *containerized* run, so the grader's `test.sh` installs and starts services inside a
  container, and an in-process offline replay is a different surface. URL opened live by L1
  `KengakuR79` this round:
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md`,
  access date 2026-11-04 UTC. Capture `corpus/evidence/round79/sources/tb2-readme.md`, HTTP 200,
  4 574 bytes, sha256 `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364`. Located
  quote, capture line 24, 22 words: **"Terminal-Bench is a popular benchmark for measuring the
  capabilities of agents and language models to perform valuable work in containerized
  environments."** Kind `docs`, tier A for the harness's own execution model. Registry change:
  absent → S256 `mined`, recheck `on-release`, used-by `corpus/lessons/round-79.md`,
  `plans/round-79-claims.md`.
- **S257 admitted** as an `own-work` row for the population the C1 ledger prices: the round-62 census
  receipt `corpus/evidence/round62/class-survey.txt` (sha256
  `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613`), anchored on its `CLASS …`
  member lists and `EXECUTED-COVERAGE` line, and the round-79 ledger
  `plans/grader-population-ledger.json` (88 rows) it gates. `own-work` is a listed contract kind and
  tier A because the lane can re-run the instruments that produced both
  (`plans/round62_c1_class_survey.py`, `plans/round79_c1_population_ledger.py`). Status `mined`,
  recheck `90d`, used-by as above.
- **Reject candidate:** "the lane's four named blockers (browser, qemu, ssh+nginx, candidate library)
  price the unexecuted population." A four-word sentence names no member, and its `ssh+nginx` is not
  a code: the frozen detectors price 7 members over four codes and leave 57 `unattempted`. Flip: a
  per-member row with a detector that fires over that task's own grader bytes (R79-C1).
- **Reject candidate:** "a `DEFECTS n=0` gate means the ledger is knowledge." The `unattempted`
  default is an absence, not a finding: 57 of 64 unexecuted members are priced as *not yet
  attempted*, which is honest and is not coverage. Flip: a replay receipt per member (round 80's
  work), not a bookkeeping row.
- **Assimilation: none.** `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was not adopted; the mass
  id drift stays open at L0 `kengaku | round-54`. `considerthese/2026-10-26.md`: proposal 1
  (routed-findings burn-down) is implemented and this round uses it for the seven closure ids;
  proposal 2 (`tb2_grader_admit`) stays open (`grep -rn 'tb2_grader_admit' plans corpus SKILL.md`
  hits only `corpus/lessons/round-66.md:332`); proposal 3 (batch sweep + class histogram) is what
  the population ledger now makes possible — the sweep itself is round 80's work.
- Knowledge entries: none admitted (both claims are instrument and ledger work; S256 grounds the
  taxonomy, S257 the population, and no new domain fact is asserted beyond them).

## Census and instrument readings

- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0 at round start
  (245 rows, 25 `W04`, `corpus/evidence/round79/census-before.txt`).
- R79-C1 before (`--rev 660ec0b9`, `corpus/evidence/round79/c1-before.txt`): `UNIVERSE classes=16
  members=88 pairs=230`, `LEDGER rows=0`, 88 `MEMBER-UNACCOUNTED`, 13 `CLASS-ROW-UNQUANTIFIED`,
  `LINK-ABSENT`, `DEFECTS n=105`, rc 1. After (`c1-after.txt`): `LEDGER rows=88 executed=18
  unlocated=6 unexecuted=64`, `COVERAGE replayed=24 covered=15 uncovered=container-image
  census_covered=12`, `DEFECTS n=0`, rc 0. Batteries: `SELFTEST cases=13 red=12 failures=0`,
  `MUTANTS real=6 killed=6 survived=0`, three controls `target_reached=False`.
- R79-C2 before (`--rev 660ec0b9`, `c2-before.txt`): 7 `DEBT-UNREGISTERED` + `INDEX-MISSING`,
  `DEFECTS n=8`, `closed=0 checks_passed=0 indexed=no`, rc 1. After (`c2-after.txt`):
  `closed=7 checks_passed=7 indexed=yes`, `DEFECTS n=0`, rc 0. Batteries: `SELFTEST cases=9 red=8
  failures=0`, `MUTANTS real=4 killed=4 survived=0`, control `target_reached=False`.
- Reason histogram the ledger prices: `unattempted` 57, `candidate-library-required` 3,
  `browser-required` 2, `vm-required` 1, `external-db-required` 1. Coverage derived, not quoted:
  15 of 16 classes carry at least one offline replay; `container-image` has no members.

## Mistakes

- **M79-1 · class `invented-evidence-split` · evidence `corpus/evidence/round78/c2-before.txt` ·
  captured-by `none` · fix `plans/round79_c2_closure_debt.py` + `corpus/routed-findings.jsonl`.**
  Round 78's report, SCORECARD row and lesson printed a per-class defect split
  (`11 TOOL-UNNAMED, 10 COMMAND-ABSENT, 4 PASS-UNLOCATED, 2 WORKTREE-ABSENT, 2 TOOL-UNPINNED`) that
  its own receipt contradicts: `awk '/^DEFECT /{print $2}' corpus/evidence/round78/c2-before.txt |
  sort | uniq -c` → `11 COMMAND-ABSENT, 5 PASS-UNLOCATED, 11 TOOL-UNNAMED, 2 WORKTREE-ABSENT`, and
  `grep -c 'DEFECT TOOL-UNPINNED' corpus/evidence/round78/c2-before.txt` → 0. The prose invented a
  defect class to make a stale reading sum to 29. No criterion caught it: QUALITY Q8 (numbers match
  the receipt they cite) did not exist as a gate. The fix is a gate that re-derives a receipt's
  per-class counts inside its own `check` (R79-C2's D1 row) — it fails at `660ec0b9` and passes only
  once the correction states the receipt's split.
- **M79-2 · class `control-ordering` · evidence `plans/round-79-claims.md` §R79-C1 Controls ·
  captured-by `QUALITY Q28` (freeze before data) · fix: none this round; recorded. The three C1
  controls were first scored after the 88-row ledger and the 16 `SKILL.md` cells were authored, so
  their receipts are not strictly pre-data, even though their skip rules are generic (name-grep,
  default reason, all-blocked) and the frozen predicate was never changed after a control ran. The
  honest reading: the ordering deviation is real and the claim's controls are weaker evidence than
  they look. Fix for round 80: write the control code and its skip rule into the freeze commit
  *before* the ledger exists, and score it against the base revision's absent state.
- **M79-3 · class `overclaim-in-taxonomy` · evidence `SCORECARD.md` round-78 §Planned (round 79) ·
  captured-by `REASON-UNBACKED` / `REASON-UNDERSTATED` (R79-C1) · fix: the frozen detector table.**
  The previous round's planned row named "four blockers (browser, qemu, ssh+nginx and a candidate
  library)" for the whole unexecuted population. Measured: `ssh+nginx` is not a code, `external-db`
  and the 57 `unattempted` members are unnamed, and the old `network-install-required` code fires on
  57 of 64 members because every TB2 `test.sh` carries an `apt-get install` preamble — a detector
  that fires on almost everything prices nothing. The fix prices both directions: a blocker reason
  whose detector is silent is `REASON-UNBACKED`, and an `unattempted` row whose detector fires is
  `REASON-UNDERSTATED`.

## Wave findings that changed the instruments (Amendment A1)

- The C1 counter's `executed-unlocated` branch accepted any receipt under the round with observations and
  no subject stamp: the census receipt (which mentions all 88 members) plus 88 docstring-only instruments
  reached `replayed=88, DEFECTS n=0`. The `unexecuted` branch accepted an absent grader body and any
  `no-blocker:` text. Amendment A1 adds six defect classes and re-measures the after receipt
  (`plans/round-79-claims.md` §Amendment A1). Two survivor mutations (`M02 foreign-blocker-evidence`,
  `M06 duplicate-json-member`) and the "zero-hash" and "drop the bodies" attacks are now killed.
- The C2 gate accepted a tracked recap file plus `test -f` as a repair (`ReviewerC2R79`). It now re-runs
  every check in a tree where the row's evidence file is reverted to `660ec0b9` and requires the check to
  fail there (`CHECK-NOT-REPAIR-SENSITIVE`), and requires the evidence file to carry the row's literal.
  Residual limit, stated: a presence gate cannot prove a semantic repair; the non-author closure is the
  authority for that.
- Host surfaces for the reason codes (`RosterScoutR79`): a browser and matching chromedriver are present
  (so `browser-required` prices a *lane-scope refusal*, not an absent surface), qemu and nginx are absent,
  and `query-optimize`'s `golden.sql`/`oewn.sqlite` are in neither the capture nor the repo. All six
  `executed-unlocated` probes are re-runnable today, but five write only a `REV` header and
  `protein-assembly`'s writer has no `--receipt` option — a subject-stamped re-mint is round 80's work.

## Corrections (round-78 closure routed ids, discharged here)

- **R78-D4** (citation metadata): the S254 quote is **15 words** (not 17) and sits at capture line
  2322 (one sentence), and the S255 row's `anchor` cell says "lines 1–9" while the quoted
  `EXECUTED-COVERAGE` line is line 21. `anchor` is not in SOURCES v1's mutable set, so this dated
  correction re-anchors both rows without editing them: S254 quote = "Show untracked files. The mode
  parameter is used to specify the handling of untracked files." (15 words, capture line 2322);
  S255 quote at line 21, not lines 1–9.
- **R78-D1, R78-D2, R78-D3, R78-D5, R78-D6, R78-D7** are discharged as `corpus/routed-findings.jsonl`
  rows of the same ids, each with a `check` that fails at `660ec0b9`; the gate is
  `plans/round79_c2_closure_debt.py`.
