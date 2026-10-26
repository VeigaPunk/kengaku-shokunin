# Round 42 — frozen claims (kengaku, hyaku run 9, 2026-10-26)

Baseline lane tip `d69452cfa4ea8f95a43caf3727a7c797ba390b6c` (the round-41 non-author spot-check). L1 `KengakuR42`
holds the canonical planner seat. Written and frozen before any `plans/battery42` fixture exists and before the first
recorded run of `plans/fibsqrt_probe.py`. Starting point: SCORECARD `### Planned (round 42) — corrected`.

**Order of operations (QUALITY Q30; V8 of the C2 counter).** Before this file was committed the probe ran only as
`--dry` (no sandbox) and `--stage-check` (builds each case's end state, runs the oracle recipe, never imports the
grader): `stagecheck cases=16 failed=0` (`.ufo/waves/round-42/claims/c2-stage-check.txt`). The C2 do-nothing control
ran the gate with `--rerun`; with no receipt on disk its P10 printed `receipt unreadable` and executed nothing.
**Disclosed prior observation:** round-41 wave-1 seat `R41PlanNext` graded three shapes on this host before this freeze
(`.ufo/waves/round-41/build/R41PlanNext.md` §3.1–§3.2: nop 2/3 tests, oracle 3/3, a 1195-line 28-value lookup 3/3);
cases `nop`, `oracle-solve-sh` and `lookup-28` re-observe them. The other 13 cases were never graded before this freeze.

Axis state carried (SCORECARD round 41): calibration 8, coverage 7 (capped by the open L0 question `kengaku |
round-33`), novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with
novelty 7. **Coverage is chosen** for the lowest-axis claim (tie-break as in rounds 35–41: a pinned local source and an
offline sandbox exist; no novelty construct with a dated prior-art receipt is ready). Coverage stays capped at 7, so C2
is judged on its counter, not on a score move. No stagnation waiver. Controls are committed with this file under
`.ufo/waves/round-42/claims/`; every L1 counter run there carries the Q32 envelope (`claims/envelope.sh`: `bwrap`
line, start/end `date +%T`, `~/.local/bin` listing digest before/after).

## C1 — calibration: what `anchor_digest_check.py` and `order_check.py` advertise and battery40 does not demonstrate

- **Surface:** `plans/anchor_digest_check.py` (`11bb2cad…`) and `plans/order_check.py` (`948d5e1d…`), both unedited
  this round, and the 14 directional round-40 wave-2 near-variants that survived battery40 (anchor X1 X3 X6 X7 X9 X12
  X13 X14 X15; order XO1 XO3 XO5 XO6 XO7). Before-state at round 41 (`R41PlanNext/near40_survivors_only.txt`, the
  unedited round-40 counter): the 20 battery40 survivors `MUTANTS total=20 killed=0 survived=20`.
- **Self-assessment vs observed state (the calibration count):** the number of these 14 frozen mutants that no
  `plans/battery42` fixture kills ATTRIBUTABLY in its declared direction. Every `adv` cell quotes the tool's
  docstring (13 `direct`, 1 `indirect`: XO6 — a `P10 PASS` line is not a gate verdict the gate prints).
- **Directions (Q29):** witnessed before freeze: `claims/witness/w_anchor.py` + `w_order.py` (built from nothing,
  ported from the round-40 builders) through the frozen counter in development mode → `claims/witness-run.txt`
  `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`. XO5 and XO6 are `rc-mirror`
  (the mutants are stricter), not the round-40 table's `rc-silence`; `claims/control-c1-direction-mislabel.txt` shows
  the round-40 labels fail (`XO5/XO6 SURVIVED exhibits=0>1,rc-mirror`).
- **Counter:** `python3 plans/round42_c1_verify.py --lane .` (docstring = the full rule) = the round-41 counter plus
  the five `F41C1Hardened` repairs (a variant bound by fd with the store hidden, b `--unshare-ipc`, c `--tmpfs /run`,
  d relative-token `path_ok`, e streaming digests) and **f attribution**: a direction hit counts only when a traced
  re-run on the killing fixture reproduces the result and executes a line of the replaced span.
- **Frozen predicate:** C1 passes iff `python3 plans/round42_c1_verify.py --lane .` prints `PINS total=2
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=14 killed=14
  survived=0 invalid=0 null_detected=0 unattributed=0`, then `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, then
  `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c1-nothing.txt` — no `plans/battery42`: `BATTERY
  fixtures=0`, `MUTANTS total=14 killed=0 survived=14`, `MUTANTS-BY-TOOL anchor=0/9 order=0/5`, `PREDICATE C1 fail`, exit 1.
- **Other controls (all at this freeze):** `control-c1-witness-as-battery.txt` (the two freeze modules copied into a
  scratch mirror's `plans/battery42` → `PREDICATE C1 pass`: reachable by witnessed work); `control-c1-no-mutants.txt`
  (`MUTANTS = []`, patch committed → `MUTANTS total=0`, `PREDICATE C1 fail`); `control-c1-attribution.txt` (the
  attributed span forced to line 1 → `killed=0 unattributed=14`, fail: leg f can fail); `control-c1-tool-edited.txt`
  (one appended line in the anchor tool → `PINS mismatched=1`, 9 invalid, fail); `control-c1-hostile-escape.txt`
  (a fixture argv `../../../../..` → `SETUP … breaks the contract`, exit 2: repair d). Repairs a–c guard vectors that
  need fixture code to run inside a tool run; these two tools run none (git plumbing only), so no hostile module can
  reach them here — named as a limit, attacked in wave 1, not claimed.
- **Work:** `plans/battery42/*.py` single-purpose fixtures (wave-1 executors), contract in the counter docstring. The
  battery may not import, copy or read the freeze modules (`claims/witness/`); the token scan flags `witness`.
- **Kill rule:** any survivor, unattributed or invalid mutant, null detection, `wrong>0`, `tampered>0`,
  `sidechannel>0`, a per-tool count other than 9/9 and 5/5, or a pin mismatch → C1 not admitted, reported as an honest
  stop. A mutant later shown equivalent is reported as a limit, never removed or relabelled. Tools not edited.
- **Limits named now:** a kill is a result difference in the declared direction on a fixture that executes the
  mutated line, not the fixture's intent; the token scan is a heuristic; non-author review of battery42 stays part of
  admission. XL1–XL6 (text-only), `state_check.py`/`round_close.py` survivors and the 34 unpriced advertised rows of
  `tip_receipts.py`/`sources_adopt.py` stay out (named as carried).

## C2 — coverage: the pinned TB2 `circuit-fibsqrt` grader, an eighth grader class (a data artefact run by a grader-owned simulator)

- **Surface:** `corpus/knowledge/` (new entry `tb2-circuit-fibsqrt-grader.md`), `corpus/SOURCES.md` (S125
  `tests/test_outputs.py`, S126 `instruction.md`, S127 `tests/sim.c`, terminal-bench-2 @
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, opened 2026-10-26 17:08 -03 by the L1: raw sha256 equal to the
  captures), README index row + coverage bullet + §Frontier narrowing (8 of 89), PROVINCE paragraph. Edge class new
  to the lane: the graded artefact is a gate list executed by `sim.c`, which the grader compiles at grading time
  (`gcc -O3 /tests/sim.c -o sim` in the cwd) and runs as `/app/sim N` on a fixed 28-value table (max 48401).
- **Probe (frozen):** `plans/fibsqrt_probe.py` (digest in `frozen-digests.txt`), 16 cases, predictions and
  `violates=` tags in `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt` (`cases=16 predicted_pass=7
  predicted_fail=9`); every case graded twice on one end state (`regrade=`). Captures
  `corpus/evidence/round42/tb2-circuit-fibsqrt/` (9 files + `SHA256SUMS`). Receipt (first recorded run, committed
  after this file): `corpus/evidence/round42/fibsqrt-probe.txt`.
- **Counter:** `python3 plans/round42_c2_verify.py --lane .` — round-41's V1–V8 re-pointed (spec
  `plans/pkg-spec-r42.json`, gate, probe, dry table, captures pinned; none relaxed) plus **V9 content** (round-41
  closure R3; `considerthese/2026-10-26.md` proposal 2, filler-control half): the entry's `## Case table` equals the
  receipt row by row, every row id occurs outside its `source:` line, PROVINCE names the task and the entry, README
  §Frontier names the task.
- **Frozen predicate:** C2 passes iff `python3 plans/round42_c2_verify.py --lane .` prints `checks=9 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c2-nothing.txt` — `checks=9 defects=6` (V2 V3 V4 V7
  V8 V9), `PREDICATE C2 fail`, exit 1; the gate's P10 reads `receipt unreadable`. **Filler control:**
  `claims/control-c2-filler.txt` — the round-41 filler shape → `V9 DEFECT`; the same mirror with the measured content →
  `V9 ok` (`CONTROL-C2-FILLER red-as-required`).
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); never edited out of the table.
- **Limits named now:** host python3 and host gcc 16 stand in for the image's python 3.13 and Debian gcc; the image
  is never pulled; recipes run unprivileged. The lookup circuit is a constructed end state, not an agent; the coverage
  gap it shows is measured, not novel-claimed (prior-art search is a wave-1 item; the only public statement found at
  round 41 asserts the opposite, `R41PlanNext` §3.2).

## Separability

C1 reads only the two tools, `plans/battery42` and fixtures it builds from nothing (no lane clone); C2 reads only its
captures, spec, gate, probe, receipt, entry, SOURCES, README, PROVINCE and the git history of this file and the
receipt. Neither counter reads the other's work product: each passes with the other's work wholly absent.

## Frontier step (not a claim)

- Sourced claim: C2 (S125/S126/S127 opened this round).
- Mined mistake (`corpus/lessons/round-42.md`): the round-40 near-variant table labelled XO5/XO6 `rc-silence` although
  its own witness text recorded `reference … rc=0, mutant … rc=1`; the round-41 plan carried the list without
  re-deriving directions. Captured-by: Q29 (directions witnessed) — not applied because that table was never frozen.
  Fix: the round-42 directions are witnessed through the frozen counter; shown able to fail by
  `control-c1-direction-mislabel.txt`.
- considerthese: `2026-10-26.md` proposal 2 (filler control half) → V9 + `control-c2-filler.txt`.
- Routed from `corpus/lessons/round-41-verifier-spotcheck.md` §5: R1 (counter soundness: repairs a–e + attribution, this
  counter); R2 (scratch hygiene: round root carries `.ROUND-ROOT-SENTINEL`, checked by the L1 before each measurement;
  guard sentence in every wave context); R3 (V9); R4 (SOURCES rule 2: corrections only by a new `supersedes` row — wave
  rule); R5 (carried, one item via a wave-1 seat with a check command).
