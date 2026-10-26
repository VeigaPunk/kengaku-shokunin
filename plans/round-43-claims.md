# Round 43 — frozen claims (kengaku, hyaku run 9, 2026-10-26)

Baseline lane tip `317148c4b918fb2645e46ec0225cac720a8a57e9` (the round-42 non-author spot-check). L1 `KengakuR43`
holds the canonical planner seat. Written and frozen before any `plans/battery43` fixture exists and before the first
recorded run of `plans/feal_probe.py`. Starting point: SCORECARD `### Planned (round 43)` as corrected by
`F42CritPlanNext` D1–D5 and the round-42 closure's routed defects R1–R6
(`corpus/lessons/round-42-verifier-spotcheck.md` §5).

**Order of operations (QUALITY Q30; V8 of the C2 counter).** Before this file was committed the probe ran only as
`--dry` and `--stage-check` (builds each case's end state, runs the recipe, byte-compiles `/app/attack.py` and builds
the `feal_in_c` extension the way `test_outputs.py:20` does; it never imports the grader):
`stagecheck cases=12 failed=0` (`.ufo/waves/round-43/claims/c2-stage-check.txt`). The C2 do-nothing control ran the
gate with `--rerun`; with no receipt on disk its P10 printed `receipt unreadable` and executed nothing
(`claims/control-c2-nothing.txt`). **Disclosed prior observation:** round-42 wave-1 seat `R42PlanNext` graded seven
shapes on this host before this freeze with an unfrozen in-process harness
(`.ufo/waves/round-42/build/R42PlanNext/feal/feal_run1.txt`: nop FAIL, oracle 5/5 PASS, `cheat-import-get_keys` PASS,
`cheat-clock-seed` 5/5 PASS, `slow-oracle-45s` PASS, `wrong-key` FAIL, `sleep-then-cheat` PASS); the cases `nop`,
`oracle-solve-sh`, `wrong-key`, `cheat-import-get_keys`, `cheat-clock-seed` and `slow-oracle-45s` re-observe them.
`oracle-off-by-one`, `return-str`, `cheat-always-equal`, `cheat-sysmodules-shadow`, `cheat-patch-get_keys` and
`cheat-exit-zero` were never graded before this freeze.

Axis state carried (SCORECARD round 42): calibration 8, coverage 7 (capped by the open L0 question `kengaku |
round-33`), novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with
novelty 7. **Coverage is chosen** for the lowest-axis claim (tie-break as in rounds 35–42: a pinned local source and an
offline sandbox exist; no novelty construct with a dated prior-art receipt is ready — `F42CritPlanNext` D4 found
third-party uses of `feal_in_c.get_keys()` scoring, so no novelty is asserted here). Coverage stays capped at 7, so C2
is judged on its counter, not on a score move. No stagnation waiver. Every L1 counter run under
`.ufo/waves/round-43/claims/` carries the round-43 envelope (`claims/envelope.sh`: the round-42 v2 envelope plus a
PATH-dir digest over names, types, link targets and CONTENT bytes, and exit 4 when it changes — closure R6/D5).

## C1 — calibration: nine behaviours `anchor_digest_check.py` and `order_check.py` advertise that no battery demonstrates

- **Surface:** `plans/anchor_digest_check.py` (`11bb2cad…`) and `plans/order_check.py` (`948d5e1d…`), both unedited
  this round, and the nine behaviour-bearing near-variants that survived battery42 in round-42 wave 2
  (`.ufo/waves/round-42/falsify/F42XMutNear.md` §3–§4): anchor NA1 NA5 NA7 NA18 NA20 NA21, order NO5 NO7 NO22 (8
  `direct`, 1 `indirect`: NA18 — the 7-hex commit floor follows from git's abbreviation rule, it is not worded in the
  docstring). NA12 is null (unreachable line, `F42XMutNear` §5) and stays out.
- **Self-assessment vs observed state (the calibration count):** the number of these 9 frozen mutants that no
  `plans/battery43` fixture kills ATTRIBUTABLY in its declared direction. Each `adv` cell quotes the tool's docstring
  with file:line.
- **Directions (Q29/Q33):** carried from a seat's table, so re-derived before freeze: `claims/witness/w_near.py`
  (ported from `F42XMutNear/w2_probe.py`) through the frozen counter in development mode → `claims/witness-run.txt`
  `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`, every kill `value=differs`. Restore
  control (`F42CritPlanNext` D2): NA7 relabelled `rc-silence` → `SURVIVED exhibits=0>1,rc-mirror`
  (`claims/control-c1-direction-mislabel.txt`).
- **Counter:** `python3 plans/round43_c1_verify.py --lane .` (docstring = the full rule) = the round-42 counter with
  the round-42 wave-2 hardened copy's repairs R1–R4 (`F42C1Hardened`: gpg/showSignature/fsmonitor/hooksPath pinned,
  builder by fd with no counter copy in scratch, read-only hides, repo toplevel/`core.worktree` refusal) plus three new
  legs: **g value attribution** (a kill needs the mutant's site record — the next event after each replaced-span line:
  next line + digest of the frame's locals, or the returned value — to differ from the reference's on the killing
  fixture; the reference is traced twice and an unstable record is not evidence), **h symlink escape** refused,
  **i order argv blobs** (`--claims`/`--receipt` that exist at HEAD must be blobs).
- **Frozen predicate:** C1 passes iff `python3 plans/round43_c1_verify.py --lane .` prints `PINS total=2
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=9 killed=9
  survived=0 invalid=0 null_detected=0 unattributed=0`, then `MUTANTS-BY-TOOL anchor=6/6 order=3/3`, then
  `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c1-nothing.txt` — no `plans/battery43`: `BATTERY
  fixtures=0`, `MUTANTS total=9 killed=0 survived=9`, `PREDICATE C1 fail`, exit 1.
- **Other controls (all at this freeze, `claims/c1_controls.sh`):** `control-c1-witness-as-battery.txt` (the freeze
  module copied into a scratch mirror's `plans/battery43` → `PREDICATE C1 pass`: reachable by witnessed work);
  `control-c1-no-mutants.txt` (`MUTANTS = []` → `MUTANTS total=0`, fail); `control-c1-attribution.txt` (span forced to
  line 1 → `unattributed=9`, fail: leg f can fail); `control-c1-value.txt` (site records forced equal →
  `unattributed=9`, fail: leg g can fail); `control-c1-tool-edited.txt` (one appended line in the anchor tool → `PINS
  mismatched=1`, 6 invalid, fail); `control-c1-hostile-escape.txt` (a relative `../` argv → `SETUP … breaks the
  contract`, exit 2); `control-c1-hostile-h1…h6.txt` (each vector open under the round-42 counter and closed under this
  one: h1 gpg program `WRONG` → `ok`; h2 builder `LEAK-35983b` → `CLEAN-3908b`; h3 lane write `WROTE` → `ERR30`; h4
  `core.worktree` accepted → `SETUP … escapes`; h5 symlinked row source accepted → `SETUP … symlink`; h6 receipt that
  is a directory accepted → `SETUP … is a tree at HEAD, not a blob`).
- **Work:** `plans/battery43/*.py` single-purpose fixtures (wave-1 executors), contract in the counter docstring. The
  battery may not import, copy or read `claims/witness/`; non-author review checks that no battery43 module is a
  re-spelling of `w_near.py` (the counter cannot see intent — the witness-as-battery control passes).
- **Kill rule:** any survivor, unattributed or invalid mutant, null detection, `wrong>0`, `tampered>0`,
  `sidechannel>0`, a per-tool count other than 6/6 and 3/3, or a pin mismatch → C1 not admitted, reported as an
  honest stop. A mutant later shown equivalent is reported as a limit, never removed or relabelled. Tools not edited.
- **Limits named now:** a kill is a result difference in the declared direction on a fixture that executes the
  mutated line and changes what follows it, not the fixture's intent; the site record sees locals and control flow,
  not state hidden inside an object whose repr does not show it (false negatives only); the token scan is a
  heuristic; R1 pins four keys, not git's key space; `u = 18` unmutated advertised behaviours (`R42CritEquiv` §3) and
  the `round_close.py` survivors (`F42CritPlanNext` D1: 9 witnessed of 20) stay carried.
- **Correction carried by this counter (closure R4):** the round-42 freeze sentence "these two tools run no fixture
  code" is false for `order_check.py` under a fixture `.git/config` carrying `gpg.program` + `log.showSignature`
  (`R42SentinelCounter` V1, measured again here: `control-c1-hostile-h1.txt` round-42 counter `observed_rc=2 WRONG`).
  The round-42 claims file is not edited; this paragraph is the named correction.

## C2 — coverage: the pinned TB2 `feal-differential-cryptanalysis` grader, a ninth grader class (an agent-authored Python module imported and called inside the grader's interpreter)

- **Surface:** `corpus/knowledge/` (new entry `tb2-feal-differential-cryptanalysis-grader.md`), `corpus/SOURCES.md`
  (S129 `tests/test_outputs.py`, S130 `instruction.md`, S131 `tests/feal_module.c`, S132 `tests/feal.c`, S133
  `tests/test.sh`, S134 `README.md`; terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, fetched by the L1
  2026-10-26 18:40 -03, captures + `SHA256SUMS` in `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`),
  README index row + coverage bullet + §Frontier narrowing (9 of 89), PROVINCE paragraph. Edge class new to the lane
  (worded per `F42CritPlanNext` D4): the graded artefact is a Python module the grader imports into its own
  interpreter (`test_outputs.py:22-24`) beside the reference extension `feal_in_c` whose public `get_keys()` holds the
  answer (`feal_module.c:51`), and the verdict is pytest's exit status (`test.sh:25`). regex-log already executes an
  agent-authored regex in-process; this class is module import + call, not "agent code in-process".
- **Probe (frozen):** `plans/feal_probe.py` (digest in `frozen-digests.txt`), 12 cases, predictions and `violates=`
  tags in `corpus/evidence/round43/feal-dry-cases-freeze.txt` (`cases=12 predicted_pass=8 predicted_fail=4`); every
  case graded twice on one end state by two fresh harness processes (`regrade=`); the verdict is the harness exit
  status (pytest's), so a process that exits 0 before the assert is `P` (`exit=no-verdict-line`). Receipt (first
  recorded run, committed after this file): `corpus/evidence/round43/feal-probe.txt`. `cheat-clock-seed` is a host
  fact (`host=libc-rand`, `F42CritPlanNext` D5).
- **Counter:** `python3 plans/round43_c2_verify.py --lane .` — round-42's V1–V9 re-pointed (spec
  `plans/pkg-spec-r43.json`, gate, probe, dry table, captures pinned; none relaxed) plus **V10 mechanism** (closure R5):
  the entry's `## Mechanism` table names, per receipt case in order, one capture line from the counter's frozen
  DECISIVE map with a ≥2-word verbatim quote of that line.
- **Frozen predicate:** C2 passes iff `python3 plans/round43_c2_verify.py --lane .` prints `checks=10 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c2-nothing.txt` — `checks=10 defects=7` (V2 V3 V4 V7
  V8 V9 V10), `PREDICATE C2 fail`, exit 1. **Informed-filler control:** `claims/control-c2-informed-filler.txt` — the
  filler shape → V9 and V10 DEFECT; the informed filler (case table copied from a synthetic receipt, every mechanism
  row on the assert line) → V9 ok, **V10 DEFECT**; decisive lines → V9 ok, V10 ok (`CONTROL-C2-INFORMED-FILLER
  red-as-required`).
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); never edited out of the table.
- **Limits named now:** host python3 3.14, host gcc and host setuptools stand in for the image's python 3.13 under
  `uvx`, Debian gcc and setuptools 80.9.0; the image is never pulled; pytest is not run (the harness maps the one test
  function onto pytest's exit status — a pytest-parity check is a wave-1 item); recipes run unprivileged. Cases are
  constructed modules, not agents. DECISIVE is the L1's reading of the captures at the freeze; a decisive line it omits
  is a counter limit, never widened after data. The class sentence carries no novelty claim (prior art: wave-1 item).

## Separability

C1 reads only the two tools, `plans/battery43` and fixtures it builds from nothing (no lane clone); C2 reads only its
captures, spec, gate, probe, receipt, entry, SOURCES, README, PROVINCE and the git history of this file and the
receipt. Neither counter reads the other's work product: each passes with the other's work wholly absent.

## Frontier step and routed work (not claims)

- Sourced claim: C2 (S129–S134 opened this round).
- Mined mistake (`corpus/lessons/round-43.md`): round-42 Gate reject of `Dockerfile` carried a flip condition
  ("if the entry keeps the `WORKDIR /app` sentence … admit") that fired at landing and was not executed (closure D3).
  Captured-by: none. Fix: a flip-condition check over a lesson's Gate rejects, shown able to fail on the round-42
  lesson, plus a QUALITY criterion (wave-1 item).
- Closure R1: `## Errata (round 43)` appended to `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (`:297` six graded
  inputs above 2^15, `:311`, `:431`, `:433-434`) and a lesson-pointer correction, never in place. R2: Gate row for
  S128 and the Dockerfile flip executed (tier-B mechanism row for `circuit-fibsqrt/environment/Dockerfile` @ the pin).
  R3: wave-2 routed items written to `corpus/routed-findings.jsonl`. R4: this counter (C1). R5: V10 (C2). R6: the
  envelope content digest (above) and an m_flash-share assertion in the wave-spec generator.
- considerthese: the latest file's unimplemented proposals are re-read in wave 1; at most one lands, cited by file and
  date.
- Assimilation: `merge/kengaku/` re-screened in wave 1 (id-collision check with the 0–3-space pattern, guard proven on
  an indented fixture, quarantine slice); adoption only if an entry fits PROVINCE and passes the scratch census.
