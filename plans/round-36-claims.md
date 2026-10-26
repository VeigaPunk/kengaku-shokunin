# Round 36 — frozen claims (kengaku, hyaku run 7, 2026-10-25)

Baseline lane tip: `b662a5d6dd370491049e4206818373c61be44816`. Frozen before any gate write, any probe
run, any repair and any seat dispatch. A rule changed after a seat has scored is not the claim's rule.

Axis selection: SCORECARD scores coverage 7, novelty 7 (tied lowest non-retired), calibration 8,
depth 9, operability 8, freshness 8, adjacency 8. No stagnation waiver. Tie-break: coverage — a pinned
local source and a runnable instrument exist; round 35's prior-art scout priced the probe pattern as
established (thin-mutant protocol), so a novelty claim would need a new construct this round has no
opened source for. Coverage stays capped at 7 by the open round-25/round-33 L0 question
(`.ufo/l0-questions.md`, kengaku round-33 line); C2 is judged on its counter, not on a score move.
Calibration is the round-35 `Planned (round 36)` row (SCORECARD.md).

## C1 — calibration: a hardened package gate closes the round-35 routed defects R35-D1..D4

Mines `considerthese/2026-10-25.md` proposal 2(c) (tip-receipt validator) and the round-35 non-author
spot-check (`corpus/lessons/round-35-verifier-spotcheck.md:86-89`, routed defects 1-4). The round-35
counters of record accepted junk (a stub probe, one-word quotes, `junk` teaches cells; D1 read the
working tree; D4/D5 checked token co-occurrence). Promote the post-hoc hardening clauses
(`plans/round35_hardening.py` H1-H6) into one gate, `plans/pkg_gate.py`, whose behaviour the frozen
battery below fixes.

- Surface changed: a new gate (`plans/pkg_gate.py`, absent at freeze) plus its ledger
  `corpus/defects-round35.jsonl` and the four repo states the rows measure.
- Frozen instruments: `plans/round36_c1_verify.py` (battery builder, ledger checks, predicate),
  `plans/pkg-spec-r35.json` (the package definition the gate reads), `corpus/defects-round35.jsonl`
  rows (status `open` at freeze).
- Battery (14 fixtures, built in a `mktemp` git repo from committed round-35 bytes): P0 genuine
  package (must accept); P1 one-word quotes, P2 eight copies of one quote, P3 an unparsed quote row,
  P4 `junk` teaches cells, P5 stub probe that prints the receipt, P6 untracked leftover file, P7 the
  cheapest all-junk package (must reject); L1 genuine D4 line and L4 genuine D5 erratum (must accept);
  L2 D4 with its two `file:line` citations swapped, L3 D4 missing its harness token, L5 D5 saying "not
  present", L6 D5 over a quote-injected capture (must reject). `false_green` counts a junk fixture
  accepted, `false_red` a genuine fixture rejected, `unevaluated` a gate crash or absent gate.
- Ledger rows (the four routed items): R35-D1 counters-accept-junk (battery clean and the real
  round-35 package re-runs at the tip through the gate, `--rerun --require-clean-tree`); R35-D2
  working-tree-and-token-cooccurrence (no untracked file anywhere in the lane and the six D4/D5 line
  fixtures behave); R35-D3 narrow-scratch-roots (committed paths matching
  `^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-` at the branch tip: 21 → 0); R35-D4 gate-row-omission
  (the round-36 lesson's `## Gate` carries one line starting `Erratum (round 36):` with `S130`, the
  recount `13 + 23 + 1 = 37` computed from the committed package copy
  `corpus/evidence/round36/toolathlon-package.md` and `denominator 38`).
- **Predicate (frozen):** C1 passes iff `python3 plans/round36_c1_verify.py --lane .` prints
  `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, then
  `rows=4 closed=4 observed_pass=4 mismatches=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean
  clone of the landing tip (no untracked files).
- Before (freeze): gate absent: `FIXTURES total=14 … unevaluated=14`, `rows=4 closed=0 observed_pass=0`,
  exit 1 (`.ufo/waves/round-36/claims/control-c1-nothing.txt`). The round-35 counter of record accepts
  all seven junk packages: `LEGACY accepted=7/7` (`claims/control-c1-legacy.txt`).
- Kill rule: any fixture wrong or unevaluated, any row open, any check failing or any mismatch at the
  landing tip → C1 not admitted. A mutant that survives a wave-2 mutation seat is reported as a
  limit, never repaired into the frozen battery.
- Skip-controls (cannot reach the target): accept-everything gate `false_green=11 false_red=0`
  (`claims/control-c1-accept-all.txt`); reject-everything gate `false_green=0 false_red=3`
  (`claims/control-c1-reject-all.txt`). Every ledger check is red at freeze, which shows each can fail.
- Limit named at freeze: 912 round-28 nested scratch paths under `.ufo/waves/round-28/scratch/` also
  match `/.ufo/waves/` but not the spot-check's `round-3x` pattern; they are cited by round-28 evidence
  pointers and are not touched. R35-D3 claims the 21 round-34 paths only.

## C2 — coverage (lowest, tied): pinned Terminal-Bench 2.0 `regex-log` grader, admitted with an executed probe

Surface moved: frontier → core for one more TB2 task's scoring code (corpus/README.md §Frontier
round-35 clause: "it stays open for the other TB2 tasks"), and a new edge class for the probe: the
graded artefact is an agent-authored *regex pattern file* executed against a fixed log inside the
grader, not a data string. Sources, opened this round (2026-10-25), byte-captured at
`corpus/evidence/round36/tb2-regex-log/` (SHA256SUMS): S108 `tests/test_outputs.py`, S109
`tests/test.sh`, S110 `instruction.md` at
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/`
(plus `task.toml` and the oracle `solution/solve.sh`, captured, not registry rows).

- Entry: `corpus/knowledge/tb2-regex-log-grader.md`; probe `plans/regex_log_probe.py` (24 frozen
  candidate-regex cases, predictions written from a static reading of the grader and the instruction
  before the first run — the reading included the captured oracle, disclosed here); receipt
  `corpus/evidence/round36/regex-log-probe.txt`.
- **Predicate (frozen):** C2 passes iff `python3 plans/round36_c2_verify.py --lane .` prints
  `checks=6 defects=0` and `PREDICATE C2 pass`, exit 0. Checks W1-W6 are defined in the counter's
  docstring (capture manifest at pinned digests; S108-S110 rows with distinct ≥8-word teaches; entry
  triad, falsifier, every quote row parsing, ≥8 distinct 3-25-word quotes at ≥8 distinct located lines;
  index + coverage row and knowledge files == index rows ≥43; frozen probe digest, receipt byte-equal
  to a fresh run, the 24-case summary line and every `match=NO` case named in the entry; census).
- Mismatches between a frozen prediction and the observation are reported in the entry and the
  report, never re-predicted; a mismatch does not fail W5 by itself (the rule is honest reporting,
  the count is calibration data), but an unnamed mismatch does.
- Before (freeze): `checks=6 defects=4`, exit 1 (`claims/control-c2-nothing.txt`; W1 and W6 hold at
  freeze because the capture is committed and the registry is unchanged).
- Kill rule: any W red at the landing tip → C2 not admitted.
- Cheapest skip-control (junk rows, one-word quotes, index row, coverage bullet, hand-typed receipt):
  `checks=6 defects=4`, exit 1 (`claims/control-c2-skip.txt`). It cannot reach the target.

## Separability

C1 touches `plans/pkg_gate.py`, `corpus/defects-round35.jsonl`, the round-34 nested scratch paths, the
round-36 lesson's Gate erratum line and QUALITY. C2 touches `corpus/knowledge/tb2-regex-log-grader.md`,
`corpus/SOURCES.md` rows S108-S110, `corpus/README.md`, `corpus/evidence/round36/`. Neither counter
reads the other's surfaces: C1 builds its battery from round-35 bytes and reads the lane tree only for
untracked files and the nested-path count; C2's index parity is `files == index rows`, not a literal.

## Frozen digests (sha256, at freeze)

```
34ab5dfd6d1c3fb972cb698a1d44db07a1670ee206521d7c3177a9e0f729561b  plans/regex_log_probe.py
d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73  plans/round36_c1_verify.py
f70e6d3a97bc8a755820cb12ab51f22f9eda684d4c2b40ceb8c92e11d48ad150  plans/round36_c2_verify.py
e085b43505c9848c8d19eb52c52fec1a3282dac3c5b436f59320e95e5c299fc4  plans/pkg-spec-r35.json
00132ab0cd660f356bfe94cf2175a9a2df76a7504cd9d9ec4af66634ef62a6f0  corpus/evidence/round36/toolathlon-package.md
```

`corpus/defects-round35.jsonl` is the one file whose rows change in place (`status` open → closed,
`closed_round`), as the ledger convention allows; its check names and ids are frozen.

## Frontier step

Census before: `.ufo/waves/round-36/claims/census-before.txt` (exit 0, 15 W04). Sourced claim: C2
(S108-S110 opened this round). Mistake to mine: the round-35 frozen counters accepted junk (spot-check
§5 item 1; `round35_hardening.py` was post-hoc). Assimilation: `considerthese/2026-10-25.md` proposal
2(c) via C1's tip re-run; `merge/kengaku/` re-screened by wave-1 scouts for one theme fitting C2; no
package row is appended unless an admitted entry cites it.

## Planner seat

The L1 holds the canonical planner seat; the validator rejects `planner` as a swarm role.

## Amendment 1 (pre-scoring instrument repair, disclosed; recorded after freeze `3241b86c`, before any seat dispatch)

The first real probe run (the L1's, after the freeze commit) showed the frozen probe is not
byte-deterministic: two assertion texts (`invalid-regex`, `regex-file-absent`) carried the
`mkdtemp` path (`corpus/evidence/round36/regex-log-probe-first-run.txt`, lines 21-22), so the frozen W5
"fresh run byte-equal to the receipt" could never hold. Repair: `plans/regex_log_probe.py` line 127
replaces the temp directory with `<tmp>` in the printed assertion text. Nothing else changed:
`--dry` output (all 24 cases, regexes and predictions) is byte-identical before and after
(`cmp` of the freeze-commit probe's `--dry` against the amended `--dry`, both equal to
`corpus/evidence/round36/regex-log-dry-cases-freeze.txt`), the first run's 24 predicted/observed
verdicts all matched (`mismatches=0`) before the repair, and two amended runs are byte-equal. The
amended probe digest is `d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc`; the C2
counter's `PROBE_SHA256` constant moves from `34ab5dfd…` to it (one line). Predicate sentence, check
definitions, kill rule and target are unchanged. Whether a pre-scoring mechanical repair of a frozen
instrument is a new revision or voids the claim is the open question already on the L0 queue
(`revenger | round-69`); this round proceeds on the disclosed amendment and reports the verdict either
way.

### Amendment 1 digest correction (appended at round close; the frozen block above is not rewritten)

Digests at the landing tip (`sha256sum`, 2026-10-25): `plans/regex_log_probe.py`
`d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc` (amended; freeze `34ab5dfd…`),
`plans/round36_c1_verify.py` `d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73` (unchanged),
`plans/round36_c2_verify.py` `983ed65c885990f6d783abffbe21b70ab5414431b88a3b27d52fdbda65d67120` (freeze
`f70e6d3a…`; the one-line `PROBE_SHA256` change of Amendment 1), `plans/pkg-spec-r35.json`
`e085b43505c9848c8d19eb52c52fec1a3282dac3c5b436f59320e95e5c299fc4` (unchanged),
`corpus/evidence/round36/toolathlon-package.md` `00132ab0cd660f356bfe94cf2175a9a2df76a7504cd9d9ec4af66634ef62a6f0`
(unchanged). No code reads this table. Two further disclosed limits of the frozen text: the Separability
paragraph is one-way (C1's battery copies C2's README/knowledge/SOURCES bytes, so C1 must be measured after
C2's index row is in place), and `--legacy` is reproducible only at the freeze commit (the round-35 counter
pins 42 knowledge files). Source: `.ufo/waves/round-36/build/R36RevClaims.md` FG3, SEP;
`R36ConnAmendment.md` §7 (recommendation: revision).

### Round close — wave 2 not dispatched

The operator ended the run before the planned falsify wave (`.ufo/waves/round-36/falsify-spec.json`,
34 seats) was taken; the round ran wave 1 only (40 seats). The frozen predicates are unchanged and were
measured on the landing tip; statements elsewhere that a wave-2 pass will attack the gate, entry or
battery record intent, not work done.
