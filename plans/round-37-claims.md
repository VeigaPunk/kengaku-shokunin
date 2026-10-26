# Round 37 — frozen claims (kengaku, hyaku run 8, 2026-10-26)

Baseline lane tip: `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd`. Frozen before any battery fixture beyond the
one-fixture API example, before any recorded grader probe run and before any seat dispatch. The probe smoke
test (`--smoke`) exercised the sandbox plumbing only: it serves a non-grader body and curls it; the grader
was not imported. Disclosure: the C2 skip-control's P10 clause (`gate --rerun`) executed the frozen probe
once inside a scratch clone at control time; the gate compared its output with the hand-typed receipt and
discarded it (`control-c2-skip.txt` shows only `P10 DEFECT … not byte-equal`); no verdict was printed or
read, and the probe file was already at its frozen digest `63cb75cf…` before that run. A rule changed after
a seat has scored is not the claim's rule.

Axis selection: SCORECARD scores coverage 7, novelty 7 (tied lowest non-retired), calibration 8, depth 9,
operability 8, freshness 8, adjacency 8. No stagnation waiver. Tie-break: coverage — a pinned local source
and an offline sandbox exist; the round-36 planning seat priced the novelty candidate (a requirement-class
census) as covered by published work (`.ufo/waves/round-36/build/R36PlanNext.md` §1.4). Coverage stays
capped at 7 by the open L0 question (`.ufo/l0-questions.md`, `kengaku | round-33` line); C2 is judged on its
counter, not on a score move. Calibration is the round-36 `### Planned (round 37)` row (SCORECARD.md).

## C1 — calibration: advertised package-gate clauses that no fixture demonstrates, 50 → 0

The round-36 gate `plans/pkg_gate.py` advertises defect classes in its docstring, in `corpus/QUALITY.md`
Q24 and in the SCORECARD capability row `package-gate`. That is the lane's self-assessment of what the
gate does. The round-36 non-author spot-check (`corpus/lessons/round-36-verifier-spotcheck.md` §5 item 2)
routed that the frozen battery is gameable and leaves clauses without a fixture, and asked for a mutant
harness that covers them and a renamed-fixture run.

- Counter (frozen): `plans/round37_c1_verify.py`. It silences one gate branch at a time with 55 frozen
  `old → new` replacements (M01–M55, listed in the counter with clause and advertised class), against the
  gate at its freeze digest `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`. The gate
  is not edited this round. A class counts as demonstrated only when its mutant changes the gate's result
  — (exit code, set of clauses printing `DEFECT`) — on at least one battery fixture. Survivors are
  advertised-but-undemonstrated clauses: the count of mismatches between what the lane says its gate
  rejects and what its tests show.
- Battery: the frozen round-36 battery (14 fixtures, unchanged) plus `plans/battery37/*.py` (absent at
  freeze — this is the work). Every battery37 fixture declares `expect` and its exact `DEFECT` clause set,
  and the unmodified gate must match each declaration. A null mutant (an unmodified copy) must change
  nothing, and a renamed run (every fixture copied under another directory name) must agree.
- **Predicate (frozen):** C1 passes iff `python3 plans/round37_c1_verify.py --lane .` prints
  `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`, then
  `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`, exit 0,
  measured on a clean clone of the landing tip, with `plans/pkg_gate.py` at its freeze digest.
- Before (freeze, `.ufo/waves/round-37/claims/control-c1-nothing.txt`): `BATTERY fixtures=14 wrong=0
  renamed_disagree=0`, `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`,
  `PREDICATE C1 fail`, exit 1. The five demonstrated classes: M01 (P1 instrument pin), M05 (P3 unparsed
  row), M40 (P9 untracked), M47 (D4 pattern), M54 (D5 manifest digest). The mismatch count is 50.
- Kill rule: any survivor, invalid mutant, null detection, wrong declaration or renamed disagreement at the
  landing tip → C1 not admitted. The mutant list, the kill criterion and the gate are not changed after
  freeze; an equivalent mutant found later is reported as a limit of this freeze, never removed.
- Skip-controls (cannot reach the target): editing the gate so mutants stop applying gives `invalid=55`
  (`control-c1-gate-edited.txt`); a battery that labels the genuine package a reject gives `wrong=1`
  (`control-c1-mislabel.txt`); the example single-defect fixture written to prove the API kills one more
  mutant only (`control-c1-example.txt`, M08) — a battery must be built clause by clause.
- Excluded branches, named at freeze (not counted in the 55, never claimed demonstrated): the empty
  `frozen_instruments` branch of P1 and every `spec not found` / `root not a directory` setup path (the
  battery cannot vary the fixed spec); the `OSError`/`SubprocessError` branch of P10 (needs uv missing or a
  600 s probe); the `run_checks` clause-crash handler and `main`'s crash → exit 2 handler (no clause crash is
  known to be reachable with the fixed spec); the `--require-clean-tree`/`--rerun` option gating (plumbing,
  not a defect class).
- Limit named at freeze: demonstration is observational (a fixture shows the branch is reached and its
  result is visible), not proof that each check is the right check.

## C2 — coverage (lowest, tied): pinned TB2 `configure-git-webserver` grader admitted with an executed probe

Surface moved: frontier → core for a third Terminal-Bench 2.0 task's scoring code, and a new grader class
for the lane: the verdict is a stdout substring over a helper shell script that probes a live HTTP service
(the first service/state grader the lane reads; rounds 35 and 36 read a data-string grader and an
agent-authored regex grader). Sources, opened this round (2026-10-26) and byte-captured at
`corpus/evidence/round37/tb2-git-webserver/` (SHA256SUMS): S111 `tests/test_outputs.py`, S112
`tests/verify.sh`, S113 `instruction.md` at
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/`
(plus `tests/test.sh`, `task.toml` and the oracle `solution/solve.sh`, captured, not registry rows).

- Probe (frozen): `plans/git_webserver_probe.py`, sha256 `63cb75cf…5eedf`; 22 cases, predictions written
  from a static reading of verify.sh, test_outputs.py and instruction.md before the first run (the reading
  included the captured oracle); case table `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt`
  (`cases=22 predicted_pass=9 predicted_fail=13`). Each case runs the captured grader in a bubblewrap
  sandbox (private network namespace, HOME and /tmp in scratch, /tests bound read-only to the captures).
  Receipt: `corpus/evidence/round37/git-webserver-probe.txt`. Entry:
  `corpus/knowledge/tb2-git-webserver-grader.md`.
- Counter (frozen): `plans/round37_c2_verify.py`, V1–V7 (docstring): capture manifest; the package gate
  `plans/pkg_gate.py --rerun --require-clean-tree` over `plans/pkg-spec-r37.json` (quote support: every
  quote verbatim on its cited line — round-36 routed item 3); anchor digests equal the pins (routed item 1);
  receipt consistency; frozen probe and dry table; census; a requirement map whose labels agree with the
  executed verdicts.
- **Predicate (frozen):** C2 passes iff `python3 plans/round37_c2_verify.py --lane .` prints
  `checks=7 defects=0`, then `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- Mismatches between a frozen prediction and an observation are reported in the entry and the report and
  never re-predicted; a mismatch does not fail V4 by itself, an unnamed one does.
- Before (freeze, `control-c2-nothing.txt`): `checks=7 defects=4` (V2, V3, V4, V7 red: no entry, rows or
  receipt), exit 1.
- Cheapest skip-control (`control-c2-skip.txt`, built by `claims/make_c2_skip.py`): junk rows whose anchors
  carry the right digests, eight one-word quotes, an index row and coverage bullet, a requirement map, and a
  hand-typed receipt copying the frozen case table → V2 red (quote shape, teaches, fresh re-run not
  byte-equal), exit 1. It cannot reach the target.
- Kill rule: any V red at the landing tip → C2 not admitted.
- Limit named at freeze: the probe shows what the grader's verdict depends on with `apt-get` and `expect`
  absent; it never runs the oracle or a real git push, so it does not show that the intended path passes.

## Separability

C1 reads `plans/pkg_gate.py`, `plans/pkg-spec-r35.json`, round-35 package bytes and `plans/battery37/`.
C2 reads `corpus/evidence/round37/`, `plans/git_webserver_probe.py`, `plans/pkg-spec-r37.json`, the entry,
S111–S113 and README. C1's genuine fixture copies all `corpus/knowledge/*.md` and the README from the
lane, and the gate's P8 compares knowledge files with index rows, so C1 must be measured on a tree where
C2's entry and index row are both present or both absent (either state is consistent; a half-landed C2
would show up as a wrong declaration in C1, not as a kill). Neither counter reads the other's work product.

## Frontier step

Census before: `.ufo/waves/round-37/claims/census-before.txt` (exit 0, 15 W04). Sourced claim: C2
(S111–S113 opened this round). Mistake to mine: the S110 anchor digest that lost one hex digit
(round-36 spot-check §5 item 1); its fix must be shown able to fail. Assimilation candidate:
`considerthese/2026-10-25.md` proposal 2(a) (re-run every closed defect's check at the tip).

## Planner seat

The L1 holds the canonical planner seat; the validator rejects `planner` as a swarm role.

## Frozen digests (sha256, at freeze)

Recorded in `.ufo/waves/round-37/claims/frozen-digests.txt`, written by `sha256sum` in the freeze commit.
