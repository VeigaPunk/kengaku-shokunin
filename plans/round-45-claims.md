# Round 45 — frozen claims (kengaku, hyaku run 9, 2026-10-26)

Baseline lane tip `9d5f9715ebb0343984171be312d44e681f96b9a8` (the round-44 non-author spot-check tip). L1
`KengakuR45` holds the canonical planner seat. Written and frozen before `plans/fixture_fence.py` exists and
before the first recorded (non-dry, non-stage-check) run of `plans/password_recovery_probe.py`. Starting point:
SCORECARD `### Planned (round 45)`, the round-44 data walk `R44PlanNext`, and the round-44 verifier spot-check
§4 routed defects (`R44SentinelFences` V1–V3, `R44LabratLaneInclude`, `R44CritV11` memorizable V11).

**Attempt-1 inheritance.** `.ufo/watchdog.log` line 1618 shows `lane-dead-no-report kengaku round=45` (attempt 1
died on an invalid_prompt policy refusal ~22:27–22:48; never spawned a wave, never committed). Its uncommitted
pre-freeze drafts were re-verified and split: REUSED — the `password-recovery` captures (9/9 files re-fetched at
pin `2fd12b88` 2026-10-26 ~23:0x -03, `cmp`-identical), `plans/password_recovery_probe.py` (docstring repaired),
`plans/round45_c2_verify.py` (digests filled), `plans/refusals45/f7-f9` (re-verified: each LEAKED under the
round-44 fence, `claims/control-c1-fence-r44.txt`); DISCARDED — `plans/round45_c1_verify.py` draft (its C1 asked
`plans/battery45` to re-kill the same five mutants battery44 already kills — a do-nothing copy control; moved to
`.ufo/waves/round-45/attempt1-unclaimed/`), the round-45 C3 novelty draft (census instrument + spec + f1-census
captures, unclaimed this round; moved likewise) and `plans/battery45/` (empty dir, never committed).

**Order of operations (QUALITY Q30; V8 of the C2 counter).** Before this file was committed the C2 probe ran
only as `--dry` and `--stage-check`: `stagecheck cases=16 failed=0` (`claims/c2-stage-check.txt`). No case of
this task was graded on this host before the freeze. The V11 controls ran the CAPTURED grader on 48 generated
states (`claims/control-c2-predictor.txt`); those states come from V11's held-out generator, not the probe's
case table, and are disclosed as the only pre-freeze grader executions.

Axis state carried (SCORECARD round 44): calibration 8, coverage 7 (capped by the open L0 question
`kengaku | round-33`), novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Lowest non-retired:
coverage 7 tied with novelty 7. **Coverage is chosen** for the lowest-axis claim (frozen tie-break; a
memorizable V11 repair is part of C2's counter). No stagnation waiver. C2 stays capped at 7 and is judged on
its counter. Causally separable: C1 changes `plans/fixture_fence.py` + fence evidence only; C2 changes
`corpus/` knowledge/SOURCES/README/PROVINCE + its probe receipt only.

## C1 — calibration: the advertised fixture fence vs the observed one

- **Surface:** `plans/fixture_fence.py` (new), evaluated by `plans/round45_c1_verify.py` over every fixture a
  module can build.
- **Self-assessment vs observed state (the calibration count):** SCORECARD round 44,
  `fenced-fixture-discovery` ("refuse a battery fixture whose git store, discovered repo or argv leaves its
  directory … include/alternates, repo above d") and the round-44 counter's F5 claim "any include.path is
  refused outright, so no file outside `d` is parsed". The frozen count: of the 10 hostile modules in
  `plans/refusals45/` (round-44 f1–f6 byte-copied, plus f7 `.git/commondir`, f8 `.git/config.worktree` include,
  f9 refuse-to-describe, f10 regular-file include), how many the fence contradicts on: admits a fixture
  (`LEAKED`), or refuses it while its own process tree opens/blocks on a path outside the fixture directory
  (`READ`), or never answers (`HUNG`). An outside read is a successful or never-returned open under the
  fixture build scratch but outside `d` (strace `-f -y`).
- **Counter:** `python3 plans/round45_c1_verify.py --lane .` (docstring = the full rule). It builds every
  module in the round-44 counter's own build sandbox (`plans/round44_c1_verify.py` imported, digest-pinned),
  runs the fence read-only under `strace -f -y` inside bwrap, and prints one verdict line per fixture.
- **Frozen predicate:** C1 passes iff it prints `PINS total=33 mismatched=0`, then
  `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, then
  `CALIBRATION advertised=10 contradicted=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of
  the landing tip. HONEST = all 104 fixtures of `plans/battery42`, `plans/battery43`, `plans/battery44` (the
  batteries the round-44 counter admits): a fence that refuses everything fails here.
- **Before (controls, this freeze):** `claims/control-c1-nothing.txt` — no `plans/fixture_fence.py` → every
  refusal module `LEAKED` (the stub raises), `contradicted=10`, `PREDICATE C1 fail`. `claims/control-c1-fence-r44.txt`
  — the round-44 counter's fence as the fence → `REFUSALS total=10 clean=3 leaked=3 read=4`,
  `contradicted=7` (f7/f8/f9 leak; f1/f6/f10/f4 refuse but read outside), `PREDICATE C1 fail` — the
  advertised-vs-observed mismatch before this round's work: **7**. `claims/control-c1-fence-admit_all.txt`
  → `leaked=10`, fail. `claims/control-c1-fence-refuse_all.txt` → `HONEST admitted=0 refused=104`, fail.
  `claims/control-c1-fence-static_only.txt` → f6 leaks (a repo whose toplevel is above d is invisible to a
  `.git`-presence scan) and `HONEST refused=104`, fail: the predicate is not reachable by refusing indiscriminately.
- **Work:** `plans/fixture_fence.py` (a wave executor owns it; contract in the counter docstring). Held-out
  attack: fresh hostile modules authored by wave critic seats against the landed fence, reported, not part of
  the predicate. Intent limit: the predicate binds behaviour on the frozen and held-out fixtures, not source
  intent; non-author review of the fence source rides admission.
- **Kill rule:** any module not `clean`, any honest fixture refused or read, a build error, a pin mismatch →
  C1 not admitted, honest stop.

## C2 — coverage: the pinned TB2 `password-recovery` grader, an eleventh grader class exemplar (F1 exact line-membership of one constant)

- **Surface:** `corpus/knowledge/tb2-password-recovery-grader.md`, `corpus/SOURCES.md` (rows S149–S157, tier A),
  README index row + coverage bullet + §Frontier narrowing (11 of 89), PROVINCE paragraph,
  `corpus/evidence/round45/tb2-password-recovery/` (9 captures + SHA256SUMS, refetched `cmp`-identical at
  `2fd12b88`), `plans/password_recovery_probe.py` (16-case executed probe).
- **Class (worded before data):** the graded artefact is an agent-written guess list
  `/app/recovered_passwords.txt` (`instruction.md:9`), checked by exact line membership of one embedded
  23-char constant after `.strip().split("\n")` (`tests/test_outputs.py:14,18`) — the round-44 exemplar
  checked 100 constants as substrings of one file; this checks one constant as a whole line among guesses
  (format-, case-, order-, count-free).
- **Counter:** `python3 plans/round45_c2_verify.py --lane .` → `checks=11 defects=0`, `PREDICATE C2 pass`,
  exit 0. Same V1–V10 structure as round 44 re-pinned (spec `plans/pkg-spec-r45.json`, dry table
  `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt`, captures, gate `plans/pkg_gate.py`,
  census, order, requirement map, case table, mechanism rows). **V11 hardened** (`R44CritV11`): predictor
  block source-linted (≤4000 B, no table/IO/hash tokens), verdicts printed as a disagreement COUNT only,
  state table `random.Random(45)` over 16 password-shaped kinds.
- **Before (do-nothing control):** `claims/control-c2-nothing.txt` — `checks=11 defects=8`, `PREDICATE C2
  fail`, exit 1 (V1 captures + V5 probe+dry + V6 census already green; package, rows, entry, receipt, map,
  mechanism, predictor absent). `claims/control-c2-predictor.txt` — V11 red-as-required: always-true,
  format-regex, substring, PASSWORD-eq → DEFECT; lookup table → lint DEFECT; the membership reading → ok.
- **Work:** the probe's first recorded run (`corpus/evidence/round45/password-recovery-probe.txt`), the
  knowledge package (entry with `## Predictor`, requirement map, mechanism rows, located quotes), the nine
  SOURCES rows, README/PROVINCE lines — wave scribe/executor seats.
- **Kill rule:** any V defect → C2 not admitted. A probe case whose observed verdict contradicts its frozen
  prediction is a defect in the receipt itself.
- **Limits named now:** host python3 stands in for the image's uvx python (stated in the probe); pytest is
  not run (the harness reproduces its per-test verdict, the only thing `tests/test.sh` rewards); V11's lint
  still cannot refuse an open-coded 48-bit truth table small enough to pass review — non-author review of
  the predictor block rides admission, as for battery intent.
