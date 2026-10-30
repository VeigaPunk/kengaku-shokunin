# Round 55 claims — frozen before data (2026-10-30, L1 KengakuR55)

Base tip `798f5e9ef30ef39291295565209b65a17343c00e` (lane `master`, local==remote, tree clean).
Axis state carried from round 54: calibration 9, coverage 7 (L0-capped), novelty 8, depth 9,
operability 8 (harmed 9→8 in r54 by the registry regression), freshness 9, adjacency 9.
Lowest non-retired axis: **coverage 7**. The stagnation nudge is not invoked (axes sit below the
saturation line 8). A coverage claim is declared (R55-C3); its score stays capped by the open L0
questions `kengaku | round-25`, `round-33`, `round-51` (unanswered), so the claim's predicate is
its counter, never the score number.

Rules: no predicate, counter, kill rule or target below changes after any seat has scored.
Corrections land as data (ledger declarations, receipt bytes) or as dated amendment rows here,
never as in-place rule edits. Every after-run is taken on a clean clone at the recorded
measured-after revision. Scratch lives under `/fast/scratch/hyaku/kengaku-r55/` only.

## R55-C1 — operability 8→9 — registry closure restored under a newly frozen rule

- **Surface:** the round-52-C2 advertised-vs-registered gate regress in round 54 when the two
  round-54 counters were advertised in `LOG.md` without registry rows
  (`integrate/round52-c2-regression.txt`: ADVERTISED 79, REGISTERED 77, MISSING 2, exit 1).
- **Before (frozen command, base `798f5e9e…`, clean shared clone):**
  `python3 plans/round52_c2_registry.py --lane <clone>` → `MISSING 2`
  (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`), `PREDICATE R52-C2 fail`,
  exit 1. Receipt `.ufo/waves/round-55/claims/c1-before.txt`.
- **After predicate (frozen):** the same command at the measured-after revision prints
  `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`,
  `PREDICATE R52-C2 pass`, exit 0, over the full advertised set at that revision — which
  includes every script this round's LOG/SCORECARD/SKILL/README/knowledge text advertises
  (`plans/round55_c2_entryargv.py`, `plans/round55_c2_controls.py`,
  `plans/round55_c3_chess_probe.py` included). Registry rows added in round 55:
  `round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`.
- **Frozen leg 2 (truth spot-leg):** every registry row added in round 55 names a self-test;
  at landing each named self-test command is executed once from a clean clone and its observed
  verdict matches the row's verdict-map cell. Receipts under `.ufo/waves/round-55/integrate/`.
- **Do-nothing control:** the base run is the control — the counter enumerates the full
  advertised set over closed files, so a round that adds no registry rows cannot pass.
- **Kill rule:** if an attack seat demonstrates, at the landing revision, a round-55-added
  registry row whose verdict-map cell is false (the claimed self-test command exits otherwise
  than the cell claims), operability holds at 8 and the claim is not admitted. Cell fixes are
  data only if made before the after-run, each with a dated amendment line here.

## R55-C2 — calibration 9→10 — entry-argv structural binding, truthful entry-ledger remeasure

- **Surface:** the r54 entry-truth counter executes each ledger row's declared `entry_argv`
  without binding it to the SKILL registry's declared entry (`entry_mode_ok` computed but
  unwired; `w1/R2C2Counter/laundering-probes.txt`): a ledger row whose entry argv is an
  argparse-prefix abbreviation (`--selft`) or a `uv` wrapper around an inline `-c` program
  passes while the registry-declared entry truly fails.
- **Instrument (new, frozen):** `plans/round55_c2_entryargv.py` (`--lane/--source/--work/
  --jobs/--timeout/--dry/--selftest`), reusing the unchanged r54 module's static legs and
  hermetic execution and adding four binding legs:
  - **L1 ledger↔registry argv identity** — every ledger row's `entry_argv` must token-equal
    the SKILL registry row's declared entry command; a mismatch is an `ARGV-DEFECT` and fails.
  - **L2 interpreter identity, no wrappers** — `argv[0]` must resolve to a real interpreter
    binary (`python3`/`python`); `uv`/`pipx`/`poetry`-style wrappers as `argv[0]` and any
    inline `-c…` program token are `WRAPPER-DEFECT`s.
  - **L3 no flag prefix abbreviation** — any flag token that is a strict prefix of a longer
    flag accepted by that script's own argparse is an `ABBREV-DEFECT` (defense in depth
    behind L1; checked without executing).
  - **L4 per-row ground truth** — each row is executed hermetically: green rows must exit 0;
    red rows must exit nonzero and print their declared evidence fragment.
- **Before (red, frozen, base):** the two frozen laundering fixtures, built by
  `plans/round55_c2_controls.py --case <name>` (case names frozen: `abbreviated-selftest`,
  `uv-decoy-script`), run against the unchanged r54 counter: `PREDICATE R54-C2 pass`,
  counter exit 0, while the registry-declared entry exits 1. Receipts
  `.ufo/waves/round-55/claims/c2-before-abbreviated-selftest.txt` and
  `c2-before-uv-decoy-script.txt` (prior evidence: r54 `w1/R2C2Counter/laundering-probes.txt`).
- **Fixture kills (frozen):** the same two fixtures against the NEW counter at the
  measured-after revision each produce their attributed kill line (`ARGV-DEFECT` /
  `WRAPPER-DEFECT` naming the case), `PREDICATE R55-C2 fail`, exit 1. Receipt
  `.ufo/waves/round-55/integrate/c2-fixture-kills.txt`.
- **Ledger truth corrections (data, before the after-run):** (a) `round35-c1-coverage`'s
  declared evidence fragment is re-derived from the entry's actual output at the landing
  revision and corrected with the observed output committed; (b) `round52-c2` stays declared
  green — R55-C1's repair restores its true exit 0; (c) ledger rows are added for the registry
  rows added in round 55 so the ledger set equals the registry set, each declared from its
  measured true behavior. The ledger is the lane's self-assessment; corrections carry evidence.
- **After predicate (frozen):** `python3 plans/round55_c2_entryargv.py --lane <clone>
  --source <clean clone> --work <scratch> --jobs N` at the measured-after revision prints
  clean static legs (`missing=0 extra=0 argv_defect=0 wrapper_defect=0 abbrev_defect=0
  bad_decl=0 duplicate_names=0 headings=1`), `RUN executed=<ledger rows> timeout=0
  mismatched=0 evidence_missing=0 laundered=0`, `TIPSTATE` declared green/red equal to
  observed green/red, `PREDICATE R55-C2 pass`, exit 0.
- **Do-nothing control:** at base the new counter does not exist and the r54 counter passes
  the laundering fixtures (committed before receipts) — a round that skips the binding work
  cannot meet the predicate.
- **Kill rule (frozen):** calibration HELD at 9 and the claim not admitted if any attack seat
  constructs a runnable fixture with ALL static legs clean that passes
  `plans/round55_c2_entryargv.py` at the measured-after revision while the row's
  registry-declared entry truly exits otherwise — i.e., a soundness break, not a documentation
  rewrite. (Rewriting the reviewed SKILL registry cell by hand is a documentation attack
  already carried by the r52 row-audit legs and reviewer cell audits; it does not fire this
  rule. LEDGER-side tampering that the binding legs fail to flag does.)

## R55-C3 — coverage 7→8 attempt (L0-capped) — a thirteenth TB2 task grader executed offline

- **Target axis:** coverage — frontier ground (the 77 not-yet-read TB2 graders) moves one
  task into the instrumented set. Score capped at 7 by open L0 `kengaku | round-25/33/51`;
  the claim's predicate is the counter, the score stays 7 unless the cap is lifted.
- **Task (frozen):** `chess-best-move` at TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
  Capture `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` sha256
  `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`, byte-identical to
  upstream at the pin (verified 2026-10-30 pre-freeze). Graded artefact class new to this
  lane: an agent-written token file judged by **order-insensitive full-multiset equality over
  whitespace-split tokens** (`assert sorted(move) == sorted(["g2g4", "e2e4"])`) — r45's
  password-recovery was line-split *membership*; here partial answers fail, order is free,
  and no normalization of case or digit width exists.
- **Instrument (frozen):** `plans/round55_c3_chess_probe.py` — a frozen case table of 12
  synthetic `move.txt` artefacts, each mapped to one instruction requirement with a prediction
  written before the first run; per case a bubblewrap sandbox (private namespaces, case-owned
  `/app`, `/tests` bound read-only) executes the captured `test_move_correct` and records the
  observed verdict; prints `cases=12 observed_pass=P observed_fail=F mismatches=0` where a
  mismatch is observed ≠ predicted. Receipt `corpus/evidence/round55/chess-best-move-probe.txt`.
- **Before (frozen commands, base):** `test -e corpus/evidence/round55/chess-best-move-probe.txt`
  → absent; `grep -c "thirteenth" PROVINCE.md` → 0; `grep -c "chess-best-move" corpus/README.md
  corpus/SOURCES.md` → 0 0. Receipt `.ufo/waves/round-55/claims/c3-before.txt`.
- **After:** the probe receipt commits with `mismatches=0`;
  `corpus/knowledge/tb2-chess-best-move-grader.md` admitted under QUALITY Q1–Q17 with the
  Q13/Q14 second-seat re-read on record; SOURCES rows S201 (grader, code A) and S202
  (instruction, docs A) opened this round (2026-10-30) land as mined with used-by the entry.
  Amendment A1 (2026-10-30, pre-dispatch, no seat has scored): the third planned row (verifier
  runner) is DROPPED — the chess-best-move `tests/test.sh` is byte-identical to the regex-log
  runner already held as S109 (both sha256 `4770437e…716e6c334`), so a new row would duplicate
  held ground; the entry cites S109 for runner semantics instead.
  `PROVINCE.md` gains a round-55 partial-frontier paragraph narrowing "12 of 89 read" →
  "13 of 89"; `corpus/README.md` gains the entry/evidence index rows and a Frontier narrowing
  note. No capability row is claimed (an instrument probe is not a capability; r52 ruling).
- **Do-nothing control:** base lacks the receipt, the entry and the index rows (commands above).
- **Kill rule:** any attack seat shows (a) a probe run where an observed≠predicted case is not
  counted as a mismatch, or (b) the oracle derives from anything but the captured grader's own
  assertions, or (c) the upstream identity check fails at the pin → claim not admitted.

## Round shape (frozen before dispatch)

One v2 wave (`w1`) under `ufo-wave-policy-v2.json`, band 64–128, ≥25 % strict attack share
(reviewer + critic + mutation-tester; sentinels do not count). Target 70 seats; final count and
role mix are recorded in the dispatch file and re-derived from `w1-results.json` after settle.
Wave-1 attacks hit the frozen claims, the before-state and the instruments under construction;
post-landing re-verification is the L1's integration duty plus the outside closure.

## Sourced claim, assimilation, L0 routing

- R55-C3 is the round's sourced claim (S201 grader + S202 instruction opened 2026-10-30,
  quotes and sha256 pins in the round lesson's Gate block; runner semantics cite held S109).
- Assimilation: **none** — the merge/kengaku package mass id drift (114 collisions) is under
  the unanswered L0 `kengaku | round-54`; nothing is adopted and no staged row is appended.
- The r52 GH013 push-protection L0 (`kengaku | round-52`) stays unanswered: no new upstream
  capture is committed this round — R55-C3 executes the already-pinned in-repo capture, whose
  bytes are verified against upstream at the pin (receipt), so no push-protection surface is
  touched. The r52-repair carried defect (order-check regression + masked K7 control) is
  reconstructed as evidence this round (R11/RV3); the production r52 counter stays unchanged.
