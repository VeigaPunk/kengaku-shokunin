# Round 40 — frozen claims (kengaku, hyaku run 9, 2026-10-26)

Baseline lane tip `d3a6277f188434458e1d2ce04aff59392c6f0dc6` (the round-39 non-author spot-check). L1 `KengakuR40`
holds the canonical planner seat. Written and frozen before any `plans/battery40` fixture exists and before the
first recorded run of `plans/db_wal_probe.py`.

**Order of operations (QUALITY Q30; checked by `plans/order_check.py` after the first receipt commit).** Before this
file was committed the probe ran only as `--dry` (no sandbox) and `--stage-check` (builds each case's end state in the
sandbox and prints stage exit codes only; the grader module is never imported — `HARNESS_PY` exits before
`spec_from_file_location` in `stage` mode): `stagecheck cases=28 failed=0` (`.ufo/waves/round-40/claims/
c2-stage-check.txt`). The C2 do-nothing control runs the gate with `--rerun`, but with no receipt on disk the gate's
P10 returns `receipt unreadable` before it executes anything, so the probe does not run. Seven of the 28 cases were
graded on this host by the round-39 planning seat (`.ufo/waves/round-39/build/R39PlanNext/dbwal/run1.txt`) before this
round; their predictions copy that pilot and say so in the probe docstring.

Axis state carried (SCORECARD round 39): calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8,
adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. Coverage is chosen (tie-break as in rounds 35–39:
a pinned local source and an offline sandbox exist; the round-39 planning seat priced the novelty candidate — grader
re-run stability — as covered by published TB guidance, `R39PlanNext.md` §4, so it rides C2 as a measured column, not
a claim). Coverage stays capped at 7 by the open L0 question `kengaku | round-33`, so C2 is judged on its counter, not
on a score move. No stagnation waiver. Controls are committed with this file under `.ufo/waves/round-40/claims/`.

## C1 — calibration: what the three tripwire tools advertise and no committed fixture demonstrates

- **Surface:** `plans/anchor_digest_check.py` (`11bb2cad…`), `plans/ledger_tip.py` (`853bcb2a…`),
  `plans/order_check.py` (`948d5e1d…`), all unedited this round, and what each one's docstring advertises (the
  contract the SKILL registry rows and QUALITY Q27/Q30 cite). No round has frozen a mutant list for these tools
  (`considerthese/2026-10-26.md` lesson 3: "a tool that closes a proposal is not a tripwire until it has been
  mutation-tested").
- **Self-assessment vs observed state (the calibration count):** the number of frozen mutants (each one advertised
  behaviour; its `adv` cell quotes the sentence with file:line — the round-39 lesson's forward rule, Mistakes row 4)
  that no committed fixture kills ATTRIBUTABLY in its declared direction. List: the 17 mutants `R39PlanNext` §2.7
  found unkilled by the tip run and the standing fixtures, minus `L08` (a summary-count-only kill; no direction here
  reads summary text), plus one mutant per round-39 R5 clause (`A27` capture-unanchored, `L21` stale pin ref REFUSE)
  plus the order-gate mutants whose witnesses exist (`O04`, `O12`, `O14`). `O13` was withdrawn before freeze: its
  witness showed it EQUIVALENT (`^`-anchored pattern, line-at-a-time, `match` ≡ `search`), recorded in the counter
  docstring. Total **21** (anchor 11, ledger 7, order 3).
- **Directions (QUALITY Q29):** declared per mutant in the counter; witnesses committed before freeze — 14 by
  `R39PlanNext`'s harness runs against these exact tool bytes (`.ufo/waves/round-39/build/R39PlanNext/out_anchor_r5.txt`,
  `out_ledger_r5.txt`; the R5 drafts it ran are byte-identical to the landed tools), 7 by this freeze's witness run
  (`.ufo/waves/round-40/claims/witness-run.txt`, modules in `claims/witness/`: A27, L01, L11, L21, O04, O12, O14 killed
  in their declared directions). Two exit-code directions are new: `error` (reference 2 → mutant 0/1) and `rc-error`
  (reference 0 → mutant 2).
- **Counter:** `python3 plans/round40_c1_verify.py --lane .` (docstring = the full rule). It carries the round-39
  closure R4 soundness repairs inside the frozen rule: build children in a dying pid namespace (A1), no in-process
  battery import (A3), pins re-hashed after the run (A4), counter-owned fixture dirs (A5); plus sandboxed tool runs at
  one fixed variant path, fixture fingerprints (`tampered`) and a git-hook/fsmonitor guard.
- **Frozen predicate:** C1 passes iff `python3 plans/round40_c1_verify.py --lane .` prints `PINS total=3
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=21 killed=21
  survived=0 invalid=0 null_detected=0`, then `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`, exit 0, measured
  on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `.ufo/waves/round-40/claims/control-c1-nothing.txt` — the same
  command with no `plans/battery40`: `BATTERY fixtures=0`, `MUTANTS total=21 killed=0 survived=21`, `PREDICATE C1
  fail`, exit 1. Other controls: `control-c1-tool-edited.txt` (one appended line in the anchor tool → `PINS
  mismatched=1`, its 11 mutants `invalid`); `control-c1-hostile-daemon.txt` (a module whose build leaves a detached
  child that rewrites its fixture 3 s later → the child dies with the build's pid namespace, `tampered=0`, nothing
  killed); `witness-run.txt` doubles as the tip-only control (an anchor tip fixture and a ledger tip fixture kill
  none of the 14 mutants the witnesses do not target).
- **Work:** `plans/battery40/*.py` single-purpose fixtures (wave-1 executors), contract in the counter docstring.
- **Kill rule:** any survivor, invalid mutant, null detection, `wrong>0`, `tampered>0`, `sidechannel>0` or a pin
  mismatch before or after the run → C1 not admitted, reported as an honest stop. A mutant later shown equivalent is
  reported as a limit, never removed or relabelled. The three tools are not edited this round (their mutants' `old`
  strings are the landed bytes).
- **Limits named now:** a kill records a result difference in the declared direction, not the fixture's intent;
  the side-channel scan is a token heuristic and git attribute/filter execution beyond the two disabled hooks is
  caught only by it, so non-author code review of battery40 stays part of admission; tool runs inherit the caller's
  PATH and HOME (the ledger's R35-D1 check needs `uv`).

## C2 — coverage: the pinned TB2 `db-wal-recovery` grader, a sixth grader class (binary database file pair)

- **Surface:** `corpus/knowledge/` (new entry `tb2-db-wal-recovery-grader.md`), `corpus/SOURCES.md` (S119
  `tests/test_outputs.py`, S120 `instruction.md`, terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  opened 2026-10-26 13:05 -03 by the L1), README index row + coverage bullet, PROVINCE paragraph; one §Frontier TB2
  sub-bullet narrowed by one task. Edge class new to the lane: the graded artefact is a JSON export whose source of
  truth is a SQLite main database plus an XOR-encrypted write-ahead log, and the instruction's repair step ("Fix the
  WAL file") is graded only through the export.
- **Probe (frozen):** `plans/db_wal_probe.py` (digest in `frozen-digests.txt`), 28 cases, predictions and `violates=`
  tags in `corpus/evidence/round40/db-wal-dry-cases-freeze.txt` (`cases=28 predicted_pass=8 predicted_fail=20`); every
  case is graded twice on the same end state (`regrade=`; considerthese/2026-10-26.md proposal 3's stability rider).
  Captures `corpus/evidence/round40/tb2-db-wal-recovery/` (8 files + `SHA256SUMS`).
- **Counter:** `python3 plans/round40_c2_verify.py --lane .` — the round-39 counter's V1–V7 re-pointed at this
  package (spec `plans/pkg-spec-r40.json`, gate, probe, dry table and captures pinned); no check added or relaxed.
- **Frozen predicate:** C2 passes iff `python3 plans/round40_c2_verify.py --lane .` prints `checks=7 defects=0`,
  then `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `.ufo/waves/round-40/claims/control-c2-nothing.txt`.
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); they are reported, never edited out of the table.
- **Limits named now:** host sqlite3 3.54.0 / python3 / xxd stand in for the image's Ubuntu 24.04 packages; the
  image is never pulled; recipes run unprivileged. The destructive-read trap (a plain read-write open deletes the
  undecryptable WAL) is published (the oracle's own "read-only to avoid WAL interaction" comment), so the entry
  claims a probed instance only. Known informed-filler limit of V1–V7 carried from rounds 37–39
  (`considerthese/2026-10-26.md` proposal 2, not taken this round).

## Separability

C1 reads only the three tools, `plans/battery40` and a clone of the lane HEAD for its fixtures; C2 reads only its
captures, spec, gate, probe, receipt, entry, SOURCES and README. C1's fixtures copy the live corpus, so a C2 package
landing changes what an anchor tip fixture sees: battery40 fixtures declare their reference result at the landing
tip, and C1 is measured there. Each claim's counter passes with the other's work product wholly absent.

## Frontier step (not a claim)

- Sourced claim: C2 (S119/S120 opened this round).
- Mined mistake (`corpus/lessons/round-40.md`): the planning seat's "reachable with one new fixture" for O13 was
  false — the mutant is equivalent; caught by a pre-freeze witness, the class "reachability asserted, not witnessed".
- considerthese: `2026-10-26.md` proposal 3 (re-run stability rider) lands as the probe's `regrade=` column.
- Routed items carried from `corpus/lessons/round-39-verifier-spotcheck.md` §5: R1 (registry rows for
  `order_check.py`, `round39_c1_audit.py`), R2 (`git_leak_probe.py --work` absent dir), R3 (order class into a ledger —
  blocked this round: `plans/ledger_tip.py` reads two fixed ledgers and is pinned by C1), R4 (C1 counter soundness — this
  counter; the tripwire mutation tests — this C1), R5 (seat scratch hygiene).
