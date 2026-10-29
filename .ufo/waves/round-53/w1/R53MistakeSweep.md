# R53MistakeSweep — report (kengaku round 53, wave 1, 2026-10-28)

Scout seat, mistake-mining sweep over the lane's own rounds 47–52 for the round-53 `## Mistakes` section and the
L1's routed list. No tools installed or upgraded; no pacman transaction attempted; no lane tree edited outside my
seat directory.

## Deliverable

**`.ufo/waves/round-53/w1/R53MistakeSweep/sweep.md`** — the full findings: (1) eight mistake classes that recurred
across rounds 47–52 with path:line evidence; (2) per class, whether its `captured-by` criterion has a committed
red-before output (or the negative sweep saying none exists); (3) the three classes most likely to recur in this
classifier + oracle + ledger round, each with a concrete early-warning command for the L1, plus one honourable
mention that is already live. Every pointer was existence-checked and content-grepped this seat; §4 of the
deliverable pastes the exact `ls`/`grep`/`python3` commands.

## Headline findings

1. **Eight recurring classes** (rounds in parentheses): survivor / stale carried instrument (48,49,50,51);
   landing — uncommitted or unsettled round work (47,48,50,51,52); counting command naming a counter no commit
   holds (48,49,50); number-drift (50,51,52); frozen-counter leg unsatisfiable/defective before data (48,49,52);
   false self-assessment cell / vacuous self-consistency (51,52); stale-premise (49,51);
   advertised-but-unregistered (51,52). Round-52-only classes that round 53 inherits directly
   (`instrument-falsified-after-freeze`, `rule-unit-leak`, `unscreened-population`,
   `counter-reachable-without-the-work`, `misrooted-duplicate-of-excluded-bytes`) are tabulated separately.
2. **Captured-by able-to-fail:** six of eight recurring classes have committed red-before receipts (e.g.
   `.ufo/waves/round-51/claims/c1-before.txt:14` `NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170`;
   `.ufo/waves/round-50/claims/c2-before.txt:4` `unresolved=12`; `.ufo/waves/round-52/claims/c2-before.txt:3`
   `MISSING 28`; `.ufo/waves/round-46/integrate/c3-landing.txt:21` `V7 DEFECT … tags missing`). Three negatives
   carry their sweeps: (a) no committed instrument receipt captures the `landing` class (closure records only);
   (b) no committed red receipt for the LOG-prose number-drift instrument (`grep -rn log_appendonly
   corpus/evidence/ .ufo/waves/*/claims/` → 0 hits); (c) **no committed red output exists for any
   `rule-unit-leak` detector** — the round-52 fix is explicitly "not landed" (`corpus/lessons/round-52.md:61`),
   which is why §3.1 of the deliverable is the top risk. The round-53 frozen selftests already committed under
   `.ufo/waves/round-53/claims/` (`c1-selftest.txt:23` cases=22, `c2-selftest.txt:13` cases=12, all forged-complete
   cases rc=1) are the first committed reds of Q42's forged-but-complete class.
3. **Top-3 recurrence risks for this round, with early-warning commands** (full command blocks in the deliverable):
   - **`rule-unit-leak` in the AST classifier's test-span unit** — probe `classify_source` (frozen API) on the two
     round-52 leak cases (`pytorch-model-recovery::test_model_file_exists`,
     `torch-tensor-parallelism::test_parallel_linear_exists`) and assert its key set equals the AST's own
     test-function names over all 183 captures; run **before** `plans/round53-c1-freeze.json` lands (verified
     still absent from the tree, so the window is open).
   - **Declared tip-state drift** (number-drift/false-registry-cell): two fresh clones, two full
     `round53_c2_tipstate.py` runs, diff — any differing row is nondeterministic and must be declared red with
     that diff. The base-tip manual probe already shows flip candidates (`state-assertion-check exit= 1`,
     `sources-adopt exit= 2`, live-count rows; runtimes up to t=229 s).
   - **Counter environment never exercised pre-score** (counter-defect-pre-score/survivor): run the C2 counter
     once with `--jobs 1` and once with `--jobs 4` on a scratch clone and diff; r51 (6 vs 43 passes from a wrong
     cwd) and r48 (probe 18/18 fail under host thread load, pass at `--nproc=8192`) are the precedents; the C2
     kill rule makes any timeout an automatic fail.
   - Honourable mention, **already live**: `advertised-but-unregistered` — measured 2026-10-28:
     `grep -c round53 SKILL.md` → 0; the 75 names in `.ufo/waves/round-53/c2-row-names.json` contain no `round53`
     entry; both `plans/round53_c1_triage.py` and `plans/round53_c2_tipstate.py` exist. Registry rows are needed
     before the report cites the counters, or r52's `MISSING 28` recurs.

## Incidental pointer defect found

`corpus/lessons/round-48-verifier-spotcheck.md:40` cites `w1/R48C2ExecTagInv.md`; the committed file is
`.ufo/waves/round-48/w1/R48C2TagInv.md` (`find .ufo/waves/round-48 -name '*TagInv*'`). Q41 covers only
SCORECARD/SHONEN/PROVINCE, so this drift is instrument-invisible — one more instance of the R3/R4 class for the
round-53 `## Mistakes` mining.

## Blindness compliance

This seat read no `C1Label*` file, no other label seat's file, and no classifier artifact (no
`plans/round53_c1_classify.py` contents, no `.ufo/waves/round-53/w1/C1ExecClassifier*` paths). It read only the
frozen claims, lesson/verifier files, L1 receipts under `.ufo/waves/round-53/claims/`, the counter filenames, and
the name list `.ufo/waves/round-53/c2-row-names.json`.

## Scratch

`/fast/scratch/hyaku/kengaku-r53/R53MistakeSweep/` created and removed (empty; the §3 clone/diff commands are
proposals for the L1, not runs by this seat). ENOSPC: none seen.
