# Round 44 — frozen claims (kengaku, hyaku run 9, 2026-10-26)

Baseline lane tip `0cb2e22598a39b7cd0bf5582d86d62492b57fa12` (the round-43 non-author spot-check). L1 `KengakuR44`
holds the canonical planner seat. Written and frozen before any `plans/battery44` fixture exists and before the first
recorded run of `plans/feal_linear_probe.py`. Starting point: SCORECARD `### Planned (round 44)`, the round-43 data
walk `R43PlanNext` (`.ufo/waves/round-43/build/R43PlanNext.md` §B, §C) and the round-43 closure's routed defects
R1–R5 (`corpus/lessons/round-43-verifier-spotcheck.md` §5).

**Order of operations (QUALITY Q30; V8 of the C2 counter).** Before this file was committed the probe ran only as
`--dry` and `--stage-check` (builds each case's end state — image seed + recipe — and reports whether
`/app/plaintexts.txt` exists; it never imports the grader): `stagecheck cases=14 failed=0`
(`.ufo/waves/round-44/claims/c2-stage-check.txt`). **Disclosed prior observation:** round-43 wave-1 seat
`R43PlanNext` ran the oracle and a substring check (not the grader's test function) on this host before this freeze
(`.ufo/waves/round-43/build/R43PlanNext.md` §C.2: `CONSTANTS 100 ALL_IN_DATA True`); case `oracle-solve-sh`
re-observes it. The other thirteen cases were never graded before this freeze. The V11 controls ran the CAPTURED
grader's `test_attack` on 48 generated end states (`claims/control-c2-predictor.txt`), none of which is a probe case
(they are V11's held-out generator, not receipt rows); that is disclosed here as the one pre-freeze grader
execution.

Axis state carried (SCORECARD round 43): calibration 8, coverage 7 (capped by the open L0 question `kengaku |
round-33`), novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with
novelty 7. **Coverage is chosen** for the lowest-axis claim (tie-break as in rounds 35–43: a pinned local source and an
offline sandbox exist; no novelty construct with a dated prior-art receipt is ready). Coverage stays capped at 7, so
C2 is judged on its counter, not on a score move. No stagnation waiver. Every L1 counter run under
`.ufo/waves/round-44/claims/` carries the round-44 envelope (`claims/envelope.sh`, the round-43 envelope unchanged).

## C1 — calibration: five behaviours `anchor_digest_check.py` and `order_check.py` advertise that no battery demonstrates

- **Surface:** `plans/anchor_digest_check.py` (`11bb2cad…`) and `plans/order_check.py` (`948d5e1d…`), both unedited
  this round, and five of the `u = 18` unmutated advertised behaviours (`R43CritEquiv` §3) that round-43 `R43PlanNext`
  priced with a single-replacement mutant each (§B.1): anchor U5 (`digest-short` label), U6 (`digest-long` label),
  U7 (a token resolving to twin captures is not a defect), U9 (lessons read from the working tree), order U14c
  (unparseable claims name is exit 2). All five `direct`. U3 was priced too and **dropped before freeze**: battery43
  `a_alt-slug-deepest` already kills it (`claims/control-c1-standing-batteries-six-mutant-draft.txt`).
- **Self-assessment vs observed state (the calibration count):** the number of these 5 frozen mutants that no
  `plans/battery44` fixture kills ATTRIBUTABLY in its declared direction. Each `adv` cell quotes the tool's docstring
  with file:line.
- **Directions (Q29/Q33):** carried from a seat's table, so re-derived before freeze: `claims/witness/w_u.py` (ported
  from `R43PlanNext/u_rows.py` + `u_ord.py`) through the frozen counter in development mode → `claims/witness-run.txt`
  `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`, every kill `value=differs`. Restore
  control: U7 relabelled `rc-silence` → `SURVIVED exhibits=0>1,rc-mirror` (`claims/control-c1-direction-mislabel.txt`).
- **Counter:** `python3 plans/round44_c1_verify.py --lane .` (docstring = the full rule) = the round-43 counter (legs
  a–i, R1–R4, value attribution) plus the round-43 wave-1 fence repairs **F1–F6** (`R43SentinelCounter`,
  `R43CritC1Counter` V2′): `.git` FILE refused and `--absolute-git-dir` inside d (F1); no depth cap (F2); exact argv
  shape, no argparse abbreviation (F3); 30 s timeout + no stdin on parent-side git (F4); `--no-includes`, include and
  alternates refused (F5); ceiling + `--lane` discovery inside d (F6).
- **Frozen predicate:** C1 passes iff `python3 plans/round44_c1_verify.py --lane .` prints `PINS total=2
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=5 killed=5
  survived=0 invalid=0 null_detected=0 unattributed=0`, then `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, then
  `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c1-nothing.txt` — no `plans/battery44`: `BATTERY
  fixtures=0`, `MUTANTS total=5 killed=0 survived=5`, `PREDICATE C1 fail`, exit 1. **Standing-battery control:**
  battery42 + battery43 (71 fixtures) copied in as battery44 → `killed=0 survived=5`, `PREDICATE C1 fail`
  (`claims/control-c1-standing-batteries.txt`): the lane's existing batteries do not reach the target.
- **Other controls (`claims/c1_controls.sh`):** witness-as-battery → `PREDICATE C1 pass` (reachable by witnessed
  work); no-mutants → `MUTANTS total=0`, fail; span forced → `unattributed=5`, fail; site records forced equal →
  `unattributed=5`, fail; anchor tool edited → `PINS mismatched=1`, fail; hostile f1–f6 (`claims/hostile/`) each
  admitted or hung under the round-43 counter and refused by SETUP under this one (`control-c1-hostile-f1…f6.txt`;
  f4 under round 43: `exit=124` at the 60 s timeout).
- **Work:** `plans/battery44/*.py` single-purpose fixtures (wave executors), contract in the counter docstring. The
  battery may not import, copy or read `claims/witness/`; non-author review checks that no battery44 module is a
  re-spelling of `w_u.py` (the counter cannot see intent — the witness-as-battery control passes).
- **Kill rule:** any survivor, unattributed or invalid mutant, null detection, `wrong>0`, `tampered>0`,
  `sidechannel>0`, a per-tool count other than 4/4 and 1/1, or a pin mismatch → C1 not admitted, reported as an
  honest stop. A mutant later shown equivalent is reported as a limit, never removed or relabelled. Tools not edited.
- **Limits named now:** as round 43 (intent, hidden object state, token-scan heuristic, R1's four keys); the
  remaining `u = 18` rows are carried (rc-equivalent 2 12 13 17, text-only 4, invariants 1 11 15, doc/code
  contradictions 8 and 10 — `R43PlanNext` §B.1), as are the 17 reachable `round_close.py` survivors (§A.3, a third
  tool the counter does not mutate).

## C2 — coverage: the pinned TB2 `feal-linear-cryptanalysis` grader, a tenth grader class (F1 constant-compare: substring test of embedded constants over an agent-written text file)

- **Surface:** `corpus/knowledge/` (new entry `tb2-feal-linear-cryptanalysis-grader.md`), `corpus/SOURCES.md` (S138
  `tests/test_outputs.py`, S139 `instruction.md`, S140 `environment/task-deps/gen.py`, S141 `environment/Dockerfile`,
  S142 `tests/test.sh`, S143 `README.md`, S144 `solution/solve.sh`, S145 `environment/task-deps/decrypt.c`, S146
  `task.toml`; terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, fetched by the L1 2026-10-26
  20:10:09 -03, captures + `SHA256SUMS` in `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/`), README index
  row + coverage bullet + §Frontier narrowing (10 of 89), PROVINCE paragraph. Class (worded before data): the graded
  artefact is a text file, `/app/plaintexts.txt` (`instruction.md:10`), checked by `assert c in data` for each of
  100 decimal constants written into the test file (`test_outputs.py:4-103`, `:120-122`) — the round-43 histogram's
  F1 class (14 tasks, 0 read).
- **Probe (frozen):** `plans/feal_linear_probe.py` (digest in `frozen-digests.txt`), 14 cases, predictions and
  `violates=` tags in `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt` (`cases=14 predicted_pass=8
  predicted_fail=6`); /app rebuilt per case by replaying `Dockerfile:6-11`; three PUBLIC pin files (`gen.py`,
  `test_outputs.py`, `solve.sh`) readable at /pub; every case graded twice by fresh harness processes (`regrade=`).
  Receipt (first recorded run, committed after this file): `corpus/evidence/round44/feal-linear-probe.txt`.
- **Counter:** `python3 plans/round44_c2_verify.py --lane .` — round-43's V1–V10 re-pointed (spec
  `plans/pkg-spec-r44.json`, gate, probe, dry table, captures pinned; none relaxed) plus **V11 held-out predictor**
  (closure R5 residual, the V10 readable-key limit): the entry's `## Predictor` python block must agree with the
  CAPTURED grader, executed, on 48 generated end states (`random.Random(44)`), with ≥8 passes and ≥8 fails; no
  verdict is stored in the counter.
- **Frozen predicate:** C2 passes iff `python3 plans/round44_c2_verify.py --lane .` prints `checks=11 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c2-nothing.txt` — `PREDICATE C2 fail`, exit 1.
  **Predictor control:** `claims/control-c2-predictor.txt` — always-True → V11 DEFECT (24 disagreements);
  whitespace-token-set reading → DEFECT (12); exact-lines reading → DEFECT (18); substring reading → ok
  (`CONTROL-C2-PREDICTOR red-as-required`).
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); never edited out of the table.
- **Limits named now:** host python3/gcc stand in for the image's python 3.13 (`uvx`) and Debian gcc; the image is
  never pulled; pytest is not run (pytest parity is a wave item); recipes run unprivileged. Cases are constructed end
  states, not agents. DECISIVE (V10) is the L1's reading of the captures at the freeze. V11's 48 states are
  generated from a fixed seed, so a predictor could be tuned to them — but only by running the grader, which is the
  reading V11 asks for. The class sentence carries no novelty claim (prior art: wave item).

## Separability

C1 reads only the two tools, `plans/battery44` and fixtures it builds from nothing (no lane clone); C2 reads only its
captures, spec, gate, probe, receipt, entry, SOURCES, README, PROVINCE and the git history of this file and the
receipt. Neither counter reads the other's work product: each passes with the other's work wholly absent.

## Frontier step and routed work (not claims)

- Sourced claim: C2 (S138–S146 opened this round).
- Mined mistake (`corpus/lessons/round-44.md`): round-43 Gate recorded `Flip check (round 43): task.toml — not fired`
  while the entry cited `task.toml:22` alone (closure §3 disagreement, R1). Captured-by: Q35 / `gate_flip_check.py`
  tests that a flip line exists, not that its verdict is true. Fix (wave item): a `not fired` verdict naming a file is
  red when the cited entry carries a `<file>:<line>` citation of it; red control built from the round-43 lesson.
- Closure R1 (corrected flip lines + entry erratum for finding 11/12), R2 (S134 anchor erratum), R3 (round-43 wave
  control files committed under this round's first commit), R4 (64-seat floor: one v2 wave), R5 (V11 above; fences
  F1–F6 in C1; mutation results of round 43 carried).
- considerthese / assimilation: re-screened in the wave; at most one considerthese proposal lands.
