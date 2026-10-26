# F42ConnFrontier — frontier & sibling check after landing (kengaku r42 w2, falsify)

Seat: F42ConnFrontier (connector). Evidence below is from read-only greps/reads of the lane
(kengaku-shokunin at `508434ad` per wave cut) and sibling lanes. No battery/counter/fixture ran
inside a bwrap sandbox this seat, so the Q32 envelope (bwrap line, `date +%T` before/after,
`ls -A ~/.local/bin | sha256sum` before/after) does not apply to any run here; no tool installs
were made.

## 1. Routing clause — PROVINCE.md §Round42 (lines 562–566)

Claim under test: "Whether a gate list is a correct digital-logic implementation of
`fib(isqrt(N))`, and the C simulator's own semantics beyond what decides this grader's verdict, are
unowned: a fleet-wide grep of every lane's PROVINCE.md/SKILL.md for digital logic, logic gate,
gate-level, circuit, C simulator or compiler semantics (2026-10-26 17:23, the seat's command)
returned one unrelated sibling hit (`mado-shokunin/SKILL.md:1656`, "short-circuit"), so such
findings route to the orchestrator, not to a sibling."

Reproduction over all 20 sibling lanes (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku,
kake, kama, kasegi, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi,
tsukuroi), PROVINCE.md + SKILL.md each:

- Variant A — `grep -inE "digital[ -]?logic|logic gate|gate-level|circuit|c simulator|compiler semantic|simulator"` → exactly one sibling hit:
  - `mado-shokunin/SKILL.md:1656: short-circuit-vs-silent-tolerance reading stays UNK.` — unrelated: walker `--help` under a broken `config.toml` (rc 0, byte-identical stdout), a config-reload reading; no digital logic/simulator/compiler semantics.
- Variant B — `gate[ -]?level` (space or hyphen) → adds a second, still-unrelated hit:
  - `chousa-shokunin/SKILL.md:432: The falsifying pair at gate level: a copy whose ...` — unrelated: verification/approval-gate terminology in their `--pin/--drift` drift-check tool, not logic gates.
- Extended safety-net vocabulary across the same siblings (verilog|vhdl|\brtl\b|fpga|hardware description|truth table|boolean|instruction set|ISA|interpreter|execution semantics): no lane claims digital-logic, simulator or compiler semantics. The `interpreter` hits are kaidoku's own triage/receipt tools (`tools/round-39/sqfs-triage.py`, `tools/round-40/sqfs-triage-v2.py`), not C simulators or compiler semantics. No PROVINCE.md/SKILL.md exists outside the `-shokunin` directories (`research/` has none; `find` for stray PROVINCE.md/SKILL.md returned nothing).

**Conclusion: routing holds.** No sibling lane owns digital-logic/simulator/compiler semantics; such findings route to the orchestrator. Precision note: the "one unrelated sibling hit" count is pattern-dependent — it reproduces exactly with hyphenated `gate-level` (variant A); a spacing-tolerant pattern also surfaces chousa's "gate level" (line 432), which is equally unrelated. The substance (no sibling owner) is unchanged.

## 2. README §Frontier round-42 sub-bullet — says exactly what changed, "8 of 89"

README `corpus/README.md` §Frontier bullet (lines 362–377) states: eighth TB2 task scoring code
(`circuit-fibsqrt/tests/test_outputs.py` with `tests/sim.c` @ `2fd12b88`; S125/S126/S127), probe
`plans/fibsqrt_probe.py`, receipt `corpus/evidence/round42/fibsqrt-probe.txt`, new graded-state
class ("a program in a data format ... the grader compiles that simulator itself"), the lookup-28
finding, prior art S128 (`R42ScoutPriorArt`), `cases=16 observed_pass=7 observed_fail=9
mismatches=0`, `regrade cases=16 differ=0`, and closes "the remaining TB2 task graders (8 of 89
read)". This matches:

- knowledge entry `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:47-54` ("The edge class it adds ... the graded artefact is not read by the grader at all — it is executed by a C program the grader compiles from its own read-only copy ... 8 of 89 read at 2fd12b88").
- index row (`corpus/README.md:75`) and coverage bullet (`corpus/README.md:271`, "grader-compiled-simulator class").
- PROVINCE.md:537 (core addition) and :562–566 (routing).
- SKILL.md:1160–1204 (§Simulator-executed data-artefact TB2 grader — round 42).
- SCORECARD.md:1741 ("one §Frontier TB2 sub-bullet narrowed by one task (8 of 89)") and LOG.md:1278 ("eighth TB2 grader executed").

Count chain verified monotonic 1→8 (README bullets + knowledge entries): R37 "3 of 89" (README:298), R38 "4 of 89" (:311), R39 "5 of 89" (:326), R40 "6 of 89" (:341), R41 "7 of 89" (:358), R42 "8 of 89" (:374). Denominator anchored: S020 (TB2 paper abstract, "89 tasks") and S079 (SOURCES.md:101: "92 root entries at that commit, of which 89 are task directories carrying a task.toml").

Receipt present and matching: `corpus/evidence/round42/fibsqrt-probe.txt` ends `regrade cases=16 differ=0` / `cases=16 observed_pass=7 observed_fail=9 mismatches=0`; capture sha256 line up with SOURCES S125–S127 anchors (test_outputs.py `6117b8ed…`, instruction.md `a7f50026…`, sim.c `700645ac…`). S128 row present (SOURCES.md:143, tier B, OpenAgents #9645, quote "The official grader exercises 28 values, none above 48,401."). `plans/fibsqrt_probe.py` exists; `corpus/routed-findings.jsonl` carries the claimed +6 round-42 rows (R42-R1..R5 open, R40-R1.1 closed).

## 3. Is 'grader-compiled simulator over a data artefact' new vs the seven earlier graders?

Yes — new. The seven prior executed TB2 graders, cited:

1. **R35 protein-assembly** — `corpus/knowledge/tb2-protein-assembly-grader.md:9-21,36-46`: graded state `/app/gblock.txt` (DNA/protein string); whole score is one pytest function asserting literals (translate, `find` order, GC windows); the artefact is read, never executed as a program.
2. **R36 regex-log** — `corpus/knowledge/tb2-regex-log-grader.md:12-14,50-57`: graded artefact `/app/regex.txt` is read, `re.compile`d and run via `re.findall` over a hard-coded 25-line log — the closest relative (a data artefact executed in-process), but by Python's library regex engine; nothing is compiled by the grader, and a pattern is not a program with step semantics.
3. **R37 configure-git-webserver** — `corpus/knowledge/tb2-git-webserver-grader.md:12-19`: graded state is two HTTP responses; substring check over a helper script's stdout; no compile, no interpreter.
4. **R38 build-pmars** — `corpus/knowledge/tb2-build-pmars-grader.md` (summary) + README bullet: graded state is an installed binary + source tree; the grader executes `pmars` and scans `ldd`/tree, but "no rebuild anywhere" — the grader never compiles, and the artefact is already an executable, not data interpreted by a simulator.
5. **R39 git-leak-recovery** — `corpus/knowledge/tb2-git-leak-recovery-grader.md` (summary): repo object store/refs/flag file scored via `git` commands; no compile; the artefact is not a program.
6. **R40 db-wal-recovery** — `corpus/knowledge/tb2-db-wal-recovery-grader.md` (summary): JSON export over a binary db pair; `json.load` + field checks; no execution of a program.
7. **R41 constraints-scheduling** — `corpus/knowledge/tb2-constraints-scheduling-grader.md` (summary) + README bullet: verdict computed by an embedded scheduling model inside the test file over three sha256-pinned calendars; the graded ICS is read with regexes, not executed; no compile.

R42 (`corpus/knowledge/tb2-circuit-fibsqrt-grader.md:47-54`; SKILL.md:1171-1180) adds: "the graded artefact is not read by the grader at all — it is executed by a C program the grader compiles from its own read-only copy, so the semantics that decide the verdict are a 353-line simulator (sim.c) plus a 28-row table". None of the seven compiles an interpreter at grading time and runs the graded data artefact under it. Nearest adjacencies are R36 (artefact executed in-process by a library engine, no compile) and R38 (graded artefact executed, but agent-built, grader never compiles); R41 is the nearest along the "grader computes rather than asserts" axis but executes nothing.

## Verdict

`VERDICT: frontier-new-routing-holds`
