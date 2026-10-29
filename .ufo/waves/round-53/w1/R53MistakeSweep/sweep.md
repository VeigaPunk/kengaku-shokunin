# R53MistakeSweep — mistake-class sweep over rounds 47–52 (kengaku round 53, wave 1, 2026-10-28)

Seat: `R53MistakeSweep` (scout, leaf member, no subagents). Sources read in full: `corpus/lessons/round-52.md`
(`## Mistakes`), `round-52-verifier-spotcheck.md`, `round-51-verifier-spotcheck.md`, `round-50.md`,
`round-50-verifier-spotcheck.md`, `round-51.md`, `round-49.md`, `round-48.md`, `round-48-verifier-spotcheck.md`,
`round-47-verifier-spotcheck.md`, `corpus/QUALITY.md` Q36–Q42, `plans/round-53-claims.md` (frozen, commit a34838f).
All pointers below are relative to the lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin/` and were
existence-checked plus content-grepped in this seat (commands in §4). Round 47 wrote no lesson (`round-47.md` does
not exist — honest-stop round); its evidence lives in the verifier spot-check.

## 1. Mistake classes that RECURRED across rounds 47–52

| # | class | rounds | mechanism | evidence pointers (path:line) |
|---|---|---|---|---|
| R1 | **survivor / stale carried instrument** — a battery, fixture population or counter environment carried from the previous round is not re-validated against the new surface | 48, 49, 50, 51 | r48: the frozen r46 control "`refused=9` minimum" did not reproduce (r46's nine were placeholder-argv refusals; re-authored population yields 8); r49: the r48 120-fixture denominator was incomplete (4 new git states → 124); r50: the carried r49 battery is not a battery for the repaired fence (4/23 change the verdict vector, 7 do not apply); r51: the C2 counter's check environment never exercised (scratch cwd, owner regex matched 0 conf lines: 6 pass vs 43 pass) | `corpus/lessons/round-48.md:28`; `corpus/lessons/round-49.md:10`; `corpus/lessons/round-50.md:15` (receipt `.ufo/waves/round-50/w1/R50C1ExecMutRebase-witness.tsv`); `corpus/lessons/round-51.md:40` |
| R2 | **landing — round work uncommitted or wave unsettled at report time** (uncommitted wave outputs, missing `WAVE-DONE`/`.ready` markers, stray untracked artifacts) | 47, 48, 50, 51, 52 | r47: uncommitted `.ufo/waves/round-47/` artifacts and a `w1.ready` marker the report asserted but the tree does not hold; r48: 7 of 64 settled seats left no report file; r50: `?? .ufo/waves/round-50/w1/` (193 files) + no `WAVE-DONE` (D1/D3); r51: lesson row for exactly r50's D1/D3; r52: untracked >1 MiB `tb2-paper-full.html` + untracked 184-file duplicate of the excluded capture inside a wave-1 report dir | `corpus/lessons/round-47-verifier-spotcheck.md:23`, `:65-66`; `corpus/lessons/round-48.md:5`; `corpus/lessons/round-50-verifier-spotcheck.md:22`, `:149`, `:166`; `corpus/lessons/round-51.md:37`; `corpus/lessons/round-52-verifier-spotcheck.md:19`, `:23`; `corpus/lessons/round-52.md:65` |
| R3 | **counting command names a counter no commit holds / shipped bytes ≠ described bytes** — the verdict instrument is unverifiable at the tip | 48, 49, 50 | r48: `round48_c1_verify.py` absent from the tip (`git ls-tree … grep round48_c1_verify` → absent); r49: "The committed MUTANTS floor and C1 stage-2 counter were not landed"; r50 D2: the described out-of-process counter sat uncommitted (working tree + `refs/jj/keep` only) while the committed counter decided in-process | `corpus/lessons/round-48-verifier-spotcheck.md:31`; `corpus/lessons/round-49.md:18`; `corpus/lessons/round-50.md:14`; `corpus/lessons/round-50-verifier-spotcheck.md:154` |
| R4 | **number-drift — a declared number contradicts the artifact it describes** | 50, 51, 52 | r50 D4: receipt says `TIP f7281bc` for `total=275`, report/SCORECARD attribute it to `71f5f5f` where it re-measures 271; r51: `PROVINCE.md:112` said **25** SOURCES rows, disk held **170**; r52: LOG said "63 of 64 seats wrote a report", `w1-results.json` has 64 entries with output | `corpus/lessons/round-50-verifier-spotcheck.md:169`; `corpus/lessons/round-51.md:35` (red: `.ufo/waves/round-51/claims/c1-before.txt:14-15`); `corpus/lessons/round-52.md:60` (verifier record: `corpus/lessons/round-51-verifier-spotcheck.md:137`) |
| R5 | **frozen-counter leg defective or unsatisfiable before data** — a precondition of a frozen leg was never exercised, or the counter itself has a bug found only when it runs | 48, 49, 52 | r48: frozen tags `both-print`/`toolchain` have no violating case → V7 unsatisfiable whatever the package does; r49: stage-2 receipt pinning cannot satisfy V7's need to inspect post-stage-2 cases (ordering); r52 A2: `CAPTURES present` compared 89 graders to a 184-file target (`present=89 != expected=184`) and `lane_read_tasks()` recovered `{'0','this'}` instead of 12 ids; r52 A3: parser read "no `--selftest`" as a selftest claim | `corpus/lessons/round-48.md:11` (red: `.ufo/waves/round-46/integrate/c3-landing.txt:21`; re-derived `.ufo/waves/round-48/w1/R48C2TagInv.md:16,19`); `corpus/lessons/round-49.md:9` (reds: `.ufo/waves/round-49/w1/R49C2ExecCounter.md:168-170`); `corpus/lessons/round-52.md:57` (red: `.ufo/waves/round-52/w1/C1ExecCounterRun.md:15,134`), `corpus/lessons/round-52.md:58` (red pair: `.ufo/waves/round-52/claims/c2-before.txt:34-35` vs `c2-a3-pre.txt:34`) |
| R6 | **false self-assessment cell / vacuous self-consistency** — a registry/manifest cell states something no instrument ever executed, or a "check" compares the file's own fields to each other | 51, 52 | r51: the `DRIFT` leg compares two manifest fields (`prose` vs `state`) — self-consistency, not truth (SF01); r52: 7 false cells in 28 wave-1 registry rows (`round46-c3` "checks=7 defects=0" really defects=6; `gate-flip-check` "ok=19/19" really 27/27; …) and `W2MutC2` showed `x`-padded rows pass the C2 counter | `corpus/lessons/round-51.md:39`; `corpus/lessons/round-51-verifier-spotcheck.md:145`; `corpus/lessons/round-52.md:64` (reds: `.ufo/waves/round-52/w2/W2ScribeRowsCheck.md:16,20`, `.ufo/waves/round-52/w2/W2RevRowsA.md:47`) |
| R7 | **stale-premise — a declared external/host state is contradicted at run time** | 49, 51 | r49: the ordering premise (receipt can be pinned before the cases it must cite exist); r51: three surfaces described as resolving were absent (`~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`, `:34113`) | `corpus/lessons/round-49.md:9`; `corpus/lessons/round-51.md:36` (reds: `corpus/evidence/round51/c1-before.txt:7-10`; `corpus/evidence/round51/surfaces/paths.txt`, `endpoints.txt`) |
| R8 | **advertised-but-unregistered — a runnable instrument is cited on a surface but has no Gate/probe registry row** | 51, 52 | r51 verifier routed two unregistered verdict instruments (`round51_surfaces.py`, `round51_routing.py`); r52 measured **28** advertised-but-unregistered instruments (`MISSING 28`), spanning 2026-10-16 → 2026-10-28 | `corpus/lessons/round-51-verifier-spotcheck.md:132`; `corpus/lessons/round-52.md:59` (red: `.ufo/waves/round-52/claims/c2-before.txt:3-5`) |

### 1b. Round-52-only classes that round 53 directly inherits (single-round, load-bearing for this round)

| class | evidence pointer | note for round 53 |
|---|---|---|
| `instrument-falsified-after-freeze` | `corpus/lessons/round-52.md:56` (observation receipt `.ufo/waves/round-52/claims/a1-observation.txt`) | freeze-order discipline: probe the rule on the pinned population **before** the freeze commit; `plans/round53-c1-freeze.json` verified still absent from the tree, so the window is open |
| `rule-unit-leak` (open) | `corpus/lessons/round-52.md:61`; independent triangulation `corpus/lessons/round-52-verifier-spotcheck.md:35` (54 vs 33 vs 47 presence-only) | the class this round's AST classifier must not re-create; see §3.1 |
| `unscreened-population` | `corpus/lessons/round-52.md:62`; `corpus/evidence/round52/graders/EXCLUDED.md` | r53-C1 leg 1 pins the exclusion (`excluded_blob=ok`) — repaired by construction in the frozen claims |
| `counter-reachable-without-the-work` | `corpus/lessons/round-52.md:63` (`.ufo/waves/round-52/w2/W2CritC1Reach/`, `W2MutC1/`) | Q42 (`corpus/QUALITY.md:1133`); r53's committed selftests are the first red receipts of the forged-complete class (see §2, R6/R-52 rows) |
| `misrooted-duplicate-of-excluded-bytes` | `corpus/lessons/round-52.md:65` | capture hygiene: copies of pinned bytes must live only where the pins say |

## 2. Is each recurring class's `captured-by` criterion shown able to fail?

"Red-before" = a committed output in which the capturing criterion fires on an instance of the class.

| class | captured-by (as recorded in the lesson) | committed red-before output? | verdict |
|---|---|---|---|
| R1 survivor | r49: claims §C1(a) population freeze; r50: Q38 witness rule; r51: wave seats `C2ExecG/H`, `C2MutLedger`, `CritSurvivor` before the scored after-run | **yes** — `.ufo/waves/round-50/w1/R50C1ExecMutRebase-witness.tsv` (carried battery 4/23, `verdict=unmet`); `.ufo/waves/round-49/w1/R49C1ExecHonest.md` (120 → 124); `.ufo/waves/round-51/w1/CritSurvivor.md`, `C2ExecG.md` exist (numbers recorded at `corpus/lessons/round-51.md:40`) | able to fail, receipts committed |
| R2 landing | closure conformance checklist (`git status --porcelain`, marker existence; hyaku addendum §2) — no lane-owned instrument | **yes, but only as closure records** — `round-50-verifier-spotcheck.md:22` (porcelain lines), `round-47-verifier-spotcheck.md:23` (marker absent). Sweep: no receipt under any `.ufo/waves/*/claims/` records this class firing from a lane instrument | able to fail only at closure; no in-lane detector exists |
| R3 unlanded counter | Q41 (`corpus/QUALITY.md:1112`) + `plans/round50_c2_audit.py` | **yes** — `.ufo/waves/round-50/claims/c2-before.txt:4` `POINTERS total=275 … unresolved=12`; selftest `.ufo/waves/round-50/claims/c2-selftest.txt` | able to fail, receipts committed |
| R4 number-drift | r51: `count_claim` leg of `plans/round51_surfaces.py`; LOG-prose variant: only the verifier's human count | **partial** — manifest numbers: `.ufo/waves/round-51/claims/c1-before.txt:14-15` `NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170`. LOG prose: red exists only as the verifier record (`round-51-verifier-spotcheck.md:137`); `plans/log_appendonly.py` detects rewrites, not falsehoods, and its red demonstration ran on scratch — sweep `grep -rn log_appendonly corpus/evidence/ .ufo/waves/*/claims/` → **0 hits**, so no committed red receipt for the LOG-prose variant | able to fail for declared-count cells; LOG-prose counts still have no committed red |
| R5 unsatisfiable/defective frozen leg | Q40 check (`corpus/QUALITY.md:1091`); wave-1 counter runs before the scored after-run | **yes** — `.ufo/waves/round-46/integrate/c3-landing.txt:21` `V7 DEFECT … tags missing=['both-print','toolchain']`; `.ufo/waves/round-49/w1/R49C2ExecCounter.md:168-170` (`V8 DEFECT` same-commit / early-receipt / no-pin controls); `.ufo/waves/round-52/w1/C1ExecCounterRun.md:134` `CAPTURES expected=184 present=89` | able to fail, receipts committed |
| R6 false cell / vacuous | at r52: human reviewers (`W2ScribeRowsCheck`, `W2RevRowsA/B`), critic `C1CritDeclareAllAbsent` — no standing instrument | **as of r52: no instrument** (Q42 itself says the criterion "is not shown able to fail until a round freezes a forged-complete control and a counter fails it"). **As of this wave: yes** — the committed round-53 receipts `.ufo/waves/round-53/claims/c2-selftest.txt:1-13` (`forged-all-green rc=1`, `red-evidence-absent rc=1`, `state-exit-inconsistent rc=1`, … `cases=12 failures=0`) and `c1-selftest.txt:23` (`cases=22 failures=0`, incl. `forged-confirmed-string rc=1`, `forged-reader-is-author rc=1`) are the first committed reds of the forged-complete class | able to fail as of round-53 wave 1; the r52-era gap is closed by the frozen selftests, not yet by a scored real-tree control (`c1-control-*`/`c2-control-*` on the landed evidence are still to be committed this wave) |
| R7 stale-premise | r51: `UNVERDICTED` leg + dated-`ABSENT` markers | **yes** — `corpus/evidence/round51/c1-before.txt:7-10` `DRIFT 3` with per-row details; `corpus/evidence/round51/surfaces/paths.txt` | able to fail, receipts committed |
| R8 advertised-but-unregistered | `plans/round52_c2_registry.py` (advertised universe vs registry) | **yes** — `.ufo/waves/round-52/claims/c2-before.txt:3-5` `MISSING 28` + per-name lines | able to fail, receipts committed |
| §1b `instrument-falsified-after-freeze` | "none — nothing tested a frozen rule against a sample of its population before the freeze" (r52) | **no instrument red receipt** — the falsification is documented in `.ufo/waves/round-52/claims/a1-observation.txt`, and the r52 fix's own red demo (probe `PROBE graders=88 contradictions=2`, exit 1) is prose in the lesson, with no receipt path named; the proposed leak selftest case is explicitly "not landed" (`round-52.md:61`). Sweep: `grep -rln 'rule-unit-leak' corpus/ plans/ SCORECARD.md LOG.md` → only `corpus/lessons/round-52.md`, `corpus/README.md:534`, `plans/round-53-claims.md:147` — no receipt file | **not yet shown able to fail by a committed instrument output** — open for round 53 |

## 3. The three classes most likely to recur in a round that builds a classifier + an oracle + a ledger

### 3.1 `rule-unit-leak` — the AST classifier's test-span definition (highest risk)

Round 52's open class is exactly this round's new instrument: r52's lexical splitter cut at `^def test_`, so
comments/helpers/docstrings bled into test blocks; 17 of 305 per-test classes change under a comment-stripped
re-split, and the two motivating tests misclassify (`corpus/lessons/round-52.md:61`); three independent counts of
the same 305 tests disagree (33 / 47 / 54, `round-52-verifier-spotcheck.md:35`). An AST classifier removes the
line-split but keeps the unit question (decorators, module-level fixtures, helper calls, `parametrize` loops).
**No committed instrument receipt demonstrates a leak detector firing** (§2, last row) — so nothing would catch a
recurrence before the freeze.

Early-warning command (run **before** the classifier freeze commit `plans/round53-c1-freeze.json` lands; the
`classify_source(src) -> {test key: 'P1'|'P0'}` API is frozen in `plans/round-53-claims.md` leg 2):

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 - <<'PY'
import ast, glob, sys
sys.path.insert(0, "plans")
import round53_c1_classify as C
# (a) the two round-52 leak cases must classify by their own function body only:
for task, fn in [("pytorch-model-recovery", "test_model_file_exists"),
                 ("torch-tensor-parallelism", "test_parallel_linear_exists")]:
    src = open(f"corpus/evidence/round52/graders/{task}/tests/test_outputs.py").read()
    print("LEAK-PROBE", task, fn, C.classify_source(src).get(fn))
    # expected: P1 (the only asserts are existence checks); a P0 here means a
    # comment/helper bled into the test's unit — the r52 leak recurring.
# (b) population-wide unit check: the classifier's key set must equal the AST's
# own test-function names — no helper bleed, no dropped test (unclassified=0):
bad = 0
for p in sorted(glob.glob("corpus/evidence/round52/graders/*/tests/test_outputs.py")):
    src = open(p).read()
    want = {n.name for n in ast.walk(ast.parse(src))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and n.name.startswith("test")}
    got = set(C.classify_source(src))
    if got != want:
        bad += 1
        print("SPAN-MISMATCH", p, sorted(want ^ got)[:4])
print("SPAN files_checked=%d mismatched=%d" % (len(glob.glob('corpus/evidence/round52/graders/*/tests/test_outputs.py')), bad))
PY
```

Any `LEAK-PROBE … P0` line or `mismatched>0` is the early warning: fix (or amend) before the freeze, never after.

### 3.2 Declared tip-state drift (`number-drift` + `false-registry-cell`) — the 75-row ledger vs a moving tip

The C2 ledger freezes 75 declared exit codes; the counter re-executes them and demands exactly the declared code
(`mismatched=0`, `timeout=0`). Rounds 50–52 show declared numbers drifting from the artifact (`PROVINCE` 25 vs
170; receipt 275@f7281bc vs 271@71f5f5f; LOG 63-of-64 vs 64). The base-tip manual probe
(`.ufo/waves/round-53/claims/c2-before-manual-probe.txt`) already shows the flip candidates: rows whose exit
depends on live state (`state-assertion-check exit= 1` at :4 while its registry cell says `0`; `sources-adopt
exit= 2`; the SOURCES-row count moved 171 → 186 between r51 and the r53 freeze, per
`plans/round-53-claims.md` §C2) and rows with long, load-sensitive runtimes (`round37-c1-mutants t= 229`,
`round40-c1-mutants t= 207`, `round38-c1-mutants t= 174`, `git-webserver-probe t= 53`). A row that is green at
ledger-write time and red at counter time (or vice versa) kills C2 on environment, not truth.

Early-warning command (before the ledger is declared final; two fresh clones, two full runs, diff):

```sh
S=/fast/scratch/hyaku/kengaku-r53/R53MistakeSweep && mkdir -p "$S"
git clone -q /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/c1" && \
git clone -q /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/c2"
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round53_c2_tipstate.py --lane . --source "$S/c1" --work "$S/w1" > "$S/run1.txt"; echo "exit1=$?"
python3 plans/round53_c2_tipstate.py --lane . --source "$S/c2" --work "$S/w2" > "$S/run2.txt"; echo "exit2=$?"
diff "$S/run1.txt" "$S/run2.txt"   # every differing row is nondeterministic: declare it red with this diff as evidence
```

### 3.3 `counter-defect-pre-score` / `survivor` — the counters' runtime environment never exercised before the scored run

r51's counter ran 61 lane-relative checks from a scratch cwd and scored 6 vs 43 passes; r48's probe failed 18/18
`--stage-check` under the host's thread load and passed byte-identical at `--nproc=8192`
(`round-48-verifier-spotcheck.md` §2); r52's counter compared 89 to 184 because it had never run against a
complete population before dispatch. Round 53's C2 re-executes **75** argvs with `--jobs 4` and a hard
`timeout=0` kill rule, against rows measured up to 229 s serial — parallel contention alone can produce the
first timeout the predicate ever sees.

Early-warning command (before the scored after-run, on scratch clones):

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
time python3 plans/round53_c2_tipstate.py --lane . --source /fast/scratch/hyaku/kengaku-r53/R53MistakeSweep/c1 --work /fast/scratch/hyaku/kengaku-r53/R53MistakeSweep/w1 --jobs 1 > /tmp/serial.txt
time python3 plans/round53_c2_tipstate.py --lane . --source /fast/scratch/hyaku/kengaku-r53/R53MistakeSweep/c1 --work /fast/scratch/hyaku/kengaku-r53/R53MistakeSweep/w1 --jobs 4 > /tmp/par.txt
diff /tmp/serial.txt /tmp/par.txt   # flips under load = environment-sensitive rows; also read the two wall times against the timeout budget
```

(And the r52 checklist item: run both frozen counters once against their *complete* real populations before
dispatch — `python3 plans/round53_c1_triage.py --selftest` and `--lane` on a clean clone, `--selftest` for C2 —
so a `present=89`-style enumeration bug is a pre-score amendment, not a killed claim. Both selftest reds are
already committed: `.ufo/waves/round-53/claims/c1-selftest.txt:23`, `c2-selftest.txt:13`.)

**Honourable mention — `advertised-but-unregistered` (R8), already live in this wave.** Measured 2026-10-28:
`grep -c round53 SKILL.md` → **0**; the 75 names in `.ufo/waves/round-53/c2-row-names.json` contain **no**
`round53` entry; both `plans/round53_c1_triage.py` and `plans/round53_c2_tipstate.py` exist. The moment
SCORECARD/LOG cite `python3 plans/round53_*.py`, r52's `MISSING 28` class recurs unless both get registry rows.
Early warning before the report lands:

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
grep -no 'python3 plans/round53_[a-z0-9_]*\.py' SCORECARD.md LOG.md SKILL.md corpus/README.md corpus/knowledge/*.md 2>/dev/null | sort -u
grep -c 'round53' SKILL.md   # must be >= 2 (one registry row per cited counter) before the report is filed
```

## 4. Sweep commands used (so every pointer above is reproducible)

```sh
ls corpus/lessons/                                   # inventory; rounds 47-52 files picked from it
grep -n '^## Mistakes' corpus/lessons/round-5{0,1,2}*.md corpus/lessons/round-4{8,9}.md
grep -n 'Q3[6-9]\|Q4[0-2]' corpus/QUALITY.md         # Q36:941 Q37:985 Q38:1027 Q39:1061 Q40:1091 Q41:1112 Q42:1133
for d in .ufo/waves/round-52/claims .ufo/waves/round-51/claims .ufo/waves/round-50/claims .ufo/waves/round-53/claims; do ls "$d"; done
ls .ufo/waves/round-46/integrate/c3-landing.txt .ufo/waves/round-48/w1/R48C2TagInv.md .ufo/waves/round-49/w1/R49C1ExecHonest.md \
   .ufo/waves/round-49/w1/R49C2ExecCounter.md .ufo/waves/round-50/w1/R50C1ExecMutRebase-witness.tsv .ufo/waves/round-52/w1/C1ExecCounterRun.md
ls .ufo/waves/round-52/w2/ | grep -Ei 'reach|mut|rowscheck|revrows|sentinel'
ls .ufo/waves/round-51/w1/ | grep -Ei 'C2ExecG|C2ExecH|MutLedger|Survivor|CritProse|DeclareAllAbsent|C1MutManifest'
grep -n 'NUMBER-DRIFT' .ufo/waves/round-51/claims/c1-before.txt            # :14-15
grep -n 'unresolved'   .ufo/waves/round-50/claims/c2-before.txt            # :4
grep -n 'MISSING'      .ufo/waves/round-52/claims/c2-before.txt            # :3-5
grep -n 'cases='       .ufo/waves/round-53/claims/c1-selftest.txt .ufo/waves/round-53/claims/c2-selftest.txt   # 22 / 12
grep -n 'V7 DEFECT'    .ufo/waves/round-46/integrate/c3-landing.txt        # :21
grep -n 'PINS|classifier=' .ufo/waves/round-53/claims/c1-before.txt        # :1-2
grep -n 'present=89'   .ufo/waves/round-52/w1/C1ExecCounterRun.md          # :15,:134
grep -n 'V8 DEFECT'    .ufo/waves/round-49/w1/R49C2ExecCounter.md          # :168-170
grep -n 'DRIFT|UNVERDICTED' corpus/evidence/round51/c1-before.txt          # :7-10
ls corpus/evidence/round51/surfaces/                                       # paths.txt endpoints.txt pins.txt
ls plans/log_appendonly.py plans/round52_c2_registry.py plans/round51_surfaces.py plans/round50_c2_audit.py \
   plans/round53_c1_triage.py plans/round53_c2_tipstate.py                 # all exist
ls plans/round53-c1-freeze.json                                            # absent (freeze window open)
grep -rln 'rule-unit-leak' corpus/ plans/ SCORECARD.md LOG.md              # 3 prose hits, no receipt
grep -rn 'log_appendonly' corpus/evidence/ .ufo/waves/*/claims/            # 0 hits (no committed red)
grep -c 'round53' SKILL.md                                                 # 0
python3 -c "import json;d=json.load(open('.ufo/waves/round-53/c2-row-names.json'));print(len(d),[n for n in d if 'round53' in n])"
                                                                          # 75, []
ls corpus/evidence/round52/graders/pytorch-model-recovery/tests/test_outputs.py   # probe input exists
```

## 5. Pointer-resolution notes and negative-claim sweeps

- **Pointer drift found in a verifier file:** `corpus/lessons/round-48-verifier-spotcheck.md:40` cites
  `w1/R48C2ExecTagInv.md`; the committed file is `.ufo/waves/round-48/w1/R48C2TagInv.md` (found via `find
  .ufo/waves/round-48 -name '*TagInv*'`). Q41 covers only SCORECARD/SHONEN/PROVINCE, so this drift is unchecked
  by any instrument — same class as R3/R4, one more instance.
- `round-49.md:9`'s pointer "round-48-verifier-spotcheck.md §5 defect 3" resolves at
  `corpus/lessons/round-48-verifier-spotcheck.md:72`.
- Round 47 has no lesson file; `corpus/lessons/round-47-verifier-spotcheck.md` is the round's only committed
  record (verified: no `round-47.md` in the lessons listing).
- Negative: no committed red receipt exists for (a) the `rule-unit-leak` detector (§2 last row), (b) the
  LOG-prose number-drift instrument (`log_appendonly` sweep, §2 R4), (c) any lane-instrument capture of the
  `landing` class (§2 R2). Each sweep command is pasted in §2/§4.
- Blindness: this seat read no `C1Label*` file, no classifier or classifier-seat file
  (`plans/round53_c1_classify.py` contents, `.ufo/waves/round-53/w1/C1ExecClassifier*`), only the frozen counter
  names, the L1's `claims/` receipts and `.ufo/waves/round-53/c2-row-names.json` (name list).
