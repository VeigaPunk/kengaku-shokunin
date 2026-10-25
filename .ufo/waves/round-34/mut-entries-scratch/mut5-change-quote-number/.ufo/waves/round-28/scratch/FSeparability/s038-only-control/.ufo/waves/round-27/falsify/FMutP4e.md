# FMutP4e — bounded P4e mutation probe
Identity: KengakuR27.FMutP4e (mutation-tester), not candidate writer KengakuR27; lane-dispatched advisory, not outside closure or a qualifying Q10 reread.
Axes: novelty (legacy → coverage/constructs; no score claim), calibration; detector sensitivity, full-token integrity, exact-byte isolation.
Read the whole draft for proposed `corpus/knowledge/extraction-policy-comparison.md`, claims including Amendment 1, QUALITY Q1–Q15, ExecStateCheckV4 and lesson integration addendum. This report tests P4e only; no parser-policy or Q15 verdict.

## Isolation and exact commands
R=/tmp/kengaku-r27-FMutP4e; E=$R/probe-evidence. All mutations, exports and detector subprocesses ran there, never against the live lane.
Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutP4e && git -C /tmp/kengaku-r27-FMutP4e switch -c r27-FMutP4e b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutP4e rev-parse HEAD` → exit0; observed HEAD=b5f62e5e637b34a1549e3475fc58b4227ed87e5a.
Harness help: `env PYTHONDONTWRITEBYTECODE=1 python3 $R/plans/fixtures/r27/p4_mutate.py --help` → exit0; CLI has no class selector, so used its real P4e recipe/functions only, not all five assigned classes.
D(label,mode): `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-FMutP4e/probe-evidence/tmp python3 /tmp/kengaku-r27-FMutP4e/probe_p4e.py LABEL MODE` (cwd R).
Modes: `selftest` invokes `/usr/bin/python3 $R/plans/state_check.py --selftest`; `json` invokes the same checker `--root $R --json`; 240s subprocess bound.
`target` invokes p4_mutate.export_base(R,b5719440…,base), apply_recipe(P4e), run_checker(checker,base/mutant), judge(P4e,control,mutant); child command is `/usr/bin/python3 $R/plans/state_check.py --root EXPORT --json` (cwd EXPORT).
Implementation anchors: `$R/probe_p4e.py:48–53,63–104`; committed harness `plans/fixtures/r27/p4_mutate.py:104–155`; recipe `plans/fixtures/r27/p4_mutants/P4e.json:2–8`.
Each phase ran independent modes concurrently; mutations/restorations were serialized. No background jobs or delegation.

## Actual phase outputs (exit codes, not inferred passes)
| D label | selftest | json | target |
|---|---:|---:|---:|
| pristine | 0 | 0 | 0 |
| token-mutant | 0 | 1 | 0 |
| token-restored | 0 | 0 | 0 |
| comparison-mutant | 1 | 0 | 1 |
| comparison-restored | 0 | 0 | 0 |
Clean/root JSON: assertions327 MATCH318 MISMATCH0 SUPERSEDED6 offline_unverifiable3 out_of_population24; all six P4e ids present once and MATCH; `P4.population.assertion-inventory` MATCH.
Every target control: exit0, assertions327/MATCH318/MISMATCH0/SUPERSEDED6/offline3/out_of_population20; no stale mismatch can supply a kill. Target exit0 means the seeded P4e source mutant was RED, not that its source was correct.
Full stdout/stderr, commands/exits and input hashes: `$E/LABEL/{selftest,json}/`; target control/changed outputs and attribution: `$E/LABEL/target/target-result.json`.

## M1 — asserted used-by source token: KILLED by JSON
Mutation: `corpus/SOURCES.md:67`, S045 used-by cell, append `, corpus/knowledge/llm-judge-calibration.md` (exact committed P4e recipe). One source line only.
Expected: new `P4e.sources.S045.used-by` MISMATCH, not merely any nonzero exit or an empty assertion population.
Actual D(token-mutant,json): exit1; assertions327/MATCH317/MISMATCH1/SUPERSEDED6/offline3. Sole mismatch id=`P4e.sources.S045.used-by`, source_line67.
Observed used_by contains the two original paths plus the false citer; citing_files remains `[corpus/knowledge/grader-perturbation-audit.md, corpus/lessons/round-26.md]`.
Actual target on pristine, token-mutant and both restored checkers: control exit0 → mutant exit1; named1/new1, exact new id above, RED=true; target wrapper exit0.
All six P4e ids and the full P4 inventory remained present/MATCH as inventories; the named mismatch, not inventory disappearance, kills M1.
SURVIVED selftest-only: D(token-mutant,selftest) exits0, byte-identical to pristine. Its P4e fixture checks S044 (`plans/state_check.py:3684–3698`), not live S045. A green selftest is capability evidence, not a clean-tree measurement.

## M2 — remove production citation comparison: KILLED by selftest and target control
Mutation: `plans/state_check.py:3303`, remove only ` and set(claimed) == set(expected)`; retain row/non-None checks, uniqueness and all emitted assertions.
Expected detector: the existing S044 red fixture must reject this loss of comparison; P4e source-mutant harness must cease producing its required named mismatch.
Actual D(comparison-mutant,selftest): exit1; `selftest FAIL P4e: red mutation survived (P4e.sources.S044.used-by)`; exact output `$E/comparison-mutant/selftest/selftest.stdout:13`.
Actual D(comparison-mutant,target): wrapper exit1; control exit0/mismatch0 → source-mutant exit0/mismatch0; named0/new0, RED=false. It refuses a vacuous kill.
SURVIVED clean-state JSON-only: D(comparison-mutant,json) exit0 and byte-identical pristine JSON, all six P4e assertions still MATCH and P4 inventory MATCH. Thus assertion presence or a clean-state exit alone does not test comparison sensitivity.
Restoring line3303 returns selftest0 and target0 with the same named S045 source MISMATCH. No baseline failure was counted as a kill.

## P4e correction full-token acceptance/refusal
Commands: D(pristine,corrections) and D(comparison-restored,corrections), both exit0; real checker CLI on independent b5719440 exports with the same S045 source mutation, no fake checker.
Each fixture appends at `corpus/SOURCES.md:102`: `- **R27-E901 (2026-10-21)** supersedes \`P4e.sources.S045.used-by\` — now ...`.
Full token=`used-by=S045:corpus/knowledge/grader-perturbation-audit.md|corpus/lessons/round-26.md`.
Full exact token → checker exit0/S045 SUPERSEDED; omit lesson path → exit1/S045 MISMATCH; replace lesson round26 by round25 → exit1/S045 MISMATCH; append a second `extra=1` token → exit1/S045 MISMATCH; change R27-E901 to R29-E901 with full token → exit1/S045 MISMATCH.
Both runs: 5/5 expected controls; exact six-id P4e inventory and P4 inventory MATCH in every fixture. Acceptance is not inferred from correction presence.
Production anchors: `plans/state_check.py:1960–1988,1991–2012,3293–3309`; fixture construction `$R/probe_p4e.py:105–147`; retained outputs `$E/{pristine,comparison-restored}/corrections/`.

## Hashes and exact restoration (SHA-256)
Checker original/restored Hc=29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32.
M2 checker=498598a4be0e47a73d124492eb7e9bbb92de00ae08b89f1331772b716e71b8c9; before Hc → mutant → restored Hc.
Lane-clone SOURCES original/restored Hs=9acb50ec77a7e39f99f7a9f586c75824a691122edc761c14cebf416e6b8be55f.
M1 SOURCES=9c70a6b599cfc335383ca7cc76d36b553809c5f4080519dd6b3a8329be3e2a29; before Hs → mutant → restored Hs.
Frozen-base exported SOURCES He=70127743276e32dbb198ef68ffe2d55c7d881627e57a743dfd075224fdf9936e; target mutant=8e6a9e16753de3c3b849734d1cca8f820906b0986ca6bc39e4488e51877d4fbb; every target restored exact He in finally, including failing detector.
Each of ten correction fixtures also restored exact He in finally; full per-fixture mutant/restored hashes are in correction-results.json. Mutant snapshots remain separate from restored test trees.
Pristine and both restored selftest stdout SHA=7fb4b3f930b229507cae7e449d6d3ffb72ecdab8a1e0057cc9743ec26e0a4973; JSON stdout SHA=b36c203635a6346f1e88bfed3af663e108d7aa7cc02a6d54871416c351633772. All CLI stderr empty.
Retained exact M2/restored checker bytes: `$E/comparison-mutant-state_check.py`, `$E/restored-state_check.py`; restored SOURCES: `$E/restored-SOURCES.md`; seeded source mutant snapshots: `$E/LABEL/target/mutant-SOURCES.md`.
Only live write is this report. Private detector/evidence retained for integration owner; no live source, Git/jj/index, runtime, model or endpoint operations; no admission or shipping decision.
Installs/updates: none.
VERDICT: Scoped PASS for P4e sensitivity/full-token controls: both assigned mutants KILLED by the combined detector, no inconclusive baseline; selftest-only and clean-state-JSON-only survivors explicitly disclosed; 5/5 correction controls pass before/after, and all mutated source trees restored byte-exact.
