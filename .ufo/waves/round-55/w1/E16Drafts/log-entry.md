## Round 55 — registry closure under a newly frozen rule; entry-argv structural binding; thirteenth TB2 grader executed (2026-10-30)

L1 KengakuR55. Frozen claims `plans/round-55-claims.md` (freeze commit
`80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`); base tip `798f5e9ef30ef39291295565209b65a17343c00e`
(lane `master`, local==remote, tree clean). Before commands and outputs are committed in
`.ufo/waves/round-55/claims/c1-before.txt`, `c2-before-abbreviated-selftest.txt`,
`c2-before-uv-decoy-script.txt`, `c3-before.txt` — quoted verbatim below.

- C1, operability 8→9 target: registry closure restored under a newly frozen rule after the
  r54 regression (`integrate/round52-c2-regression.txt` in the r54 wave root). Counter (frozen):
  `python3 plans/round52_c2_registry.py --lane <clone>`. Before, at base, observed
  (`.ufo/waves/round-55/claims/c1-before.txt`):

  ```
  BASE 798f5e9ef30ef39291295565209b65a17343c00e
  COMMAND python3 plans/round52_c2_registry.py --lane /fast/scratch/hyaku/kengaku-r55/c1before/clone
  ADVERTISED total=79
  REGISTERED total=77 rows=79
  MISSING 2
    MISSING plans/round54_c1_anchor.py
    MISSING plans/round54_c2_entrytruth.py
  INCOMPLETE 0
  ENTRY-MISSING 0
  SELFTEST-UNBACKED 0
  DUPLICATE 0
  PREDICATE R52-C2 fail
  EXIT=1
  ```

  After predicate (frozen): `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`,
  `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R52-C2 pass`, exit 0; registry rows added
  for `round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`; frozen
  leg 2 (truth spot-leg) executes each named self-test once from a clean clone, receipts under
  `.ufo/waves/round-55/integrate/`.
- C2, calibration 9→10 target: entry-argv structural binding via the NEW instrument
  `plans/round55_c2_entryargv.py` (frozen; four binding legs L1–L4 on top of the unchanged r54
  module's static legs and hermetic execution). Before (red, frozen, base): the two frozen
  laundering fixtures built by `plans/round55_c2_controls.py --case <name>` run against the
  unchanged r54 counter. Observed for `abbreviated-selftest`
  (`.ufo/waves/round-55/claims/c2-before-abbreviated-selftest.txt`):

  ```
  CASE abbreviated-selftest
  ARGV ["python3", "plans/fixture_gate.py", "--selft"]
  ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
  RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0
  TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0
  PREDICATE R54-C2 pass
  COUNTER EXIT 0
  TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
  ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)
  ```

  Observed for `uv-decoy-script`
  (`.ufo/waves/round-55/claims/c2-before-uv-decoy-script.txt`):

  ```
  CASE uv-decoy-script
  ARGV ["uv", "run", "--no-project", "--offline", "python3", "-cprint('wrapper green')", "python3", "plans/fixture_gate.py"]
  ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
  RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0
  TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0
  PREDICATE R54-C2 pass
  COUNTER EXIT 0
  TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
  ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)
  ```

  Fixture kills (frozen): each fixture against the NEW counter at the measured-after revision
  produces its attributed kill line (`ARGV-DEFECT` / `WRAPPER-DEFECT` naming the case),
  `PREDICATE R55-C2 fail`, exit 1, receipt `integrate/c2-fixture-kills.txt`.
- C3, coverage attempt (7→8, L0-capped): thirteenth TB2 task grader `chess-best-move` executed
  offline via the frozen instrument `plans/round55_c3_chess_probe.py` (12 synthetic move.txt
  cases, bubblewrap sandbox, predictions written before the first run, receipt
  `corpus/evidence/round55/chess-best-move-probe.txt`). Before (frozen commands, base), observed
  (`.ufo/waves/round-55/claims/c3-before.txt`):

  ```
  COMMAND test -e corpus/evidence/round55/chess-best-move-probe.txt
  EXIT=1 (1 = absent, expected)
  COMMAND grep -c thirteenth PROVINCE.md
  0
  EXIT=1 (1 = no match, expected)
  COMMAND grep -c chess-best-move corpus/README.md corpus/SOURCES.md
  corpus/README.md:0
  corpus/SOURCES.md:0
  EXIT=1 (1 = no matches, expected)
  ```

  Score stays capped at 7 by open L0 `kengaku | round-25/33/51`; the claim's predicate is its
  counter, never the score number.
- Wave shape: (wave w1: <N> seats, role mix — L1 fills after settle). Dispatch file
  `.ufo/waves/round-55/w1-dispatch.json` records spawn 70 / resume 0 / total 70
  (roles executor 16, scribe 7, scout 7, reviewer 12, critic 10, mutation-tester 6,
  sentinel 4, revenger 3, connector 3, simplifier 2; strict attack share 28/70 = 40%
  reviewer+critic+mutation-tester per the frozen ≥25% rule); settle-derived counts and
  `w1-results.json` verification are PENDING-L1.
- R55-C3 is the round's sourced claim (SOURCES rows S201 grader, S202 instruction opened
  2026-10-30; amendment A1 drops the duplicate verifier-runner row — `tests/test.sh` is
  byte-identical to the S109 regex-log runner, sha256 `4770437e…716e6c334` — and the entry
  cites S109 for runner semantics). Assimilation none (114 mass-ID collisions remain under
  L0 `kengaku | round-54`); the r52 GH013 L0 stays unanswered — no new upstream capture is
  committed. The r52-repair carried defect is reconstructed as evidence (R11/RV3); the
  production r52 counter stays unchanged.

Final measurement revision and verdicts follow in the appended close entry; no score bump is
implied here.

### Round-55 measured close

<!-- L1-FILL: measured-after revision (clean shared clone) -->
Measured revision: <PENDING-L1>.

<!-- L1-FILL: C1 canonical command, observed output, exit -->
- C1 (registry closure): <PENDING-L1>. Receipt: `.ufo/waves/round-55/integrate/c1-after.txt`
  (PENDING-L1).

<!-- L1-FILL: C2 canonical command, observed static legs / RUN / TIPSTATE lines, exit -->
- C2 (entry-argv binding): <PENDING-L1>. Receipts: `.ufo/waves/round-55/integrate/c2-after.txt`,
  `integrate/c2-fixture-kills.txt` (PENDING-L1).

<!-- L1-FILL: C3 probe receipt lines (cases=12 observed_pass=P observed_fail=F mismatches=0) -->
- C3 (chess-best-move probe): <PENDING-L1>. Receipt: `corpus/evidence/round55/chess-best-move-probe.txt`
  (PENDING-L1).

<!-- L1-FILL: verdicts per claim, axis dispositions, kill-rule outcomes, census before/end -->
Verdicts and axis dispositions: <PENDING-L1>.
Census: before receipt `.ufo/waves/round-55/claims/census-before.txt`; end receipt
`integrate/census-end.txt` (PENDING-L1).
Wave settle: `.ufo/waves/round-55/w1-results.json` — <PENDING-L1>.
