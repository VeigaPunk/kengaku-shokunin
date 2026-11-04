# RestampFeasR78 — coverage / calibration

RESTAMP-FEASIBLE: YES — seven frozen battery tallies reproduce without changing an instrument; a clean-tree stamping recipe was exercised in both output modes. This does NOT mean every rerun passes: R75-C1 is red at the pinned current tip.

## Revisions and method

- Freeze: `2f9eeafb35f3d4c0df2259ec8dc73c48009c96c8`. Battery comparison uses committed receipts at that revision, not the concurrently repaired lane worktree receipts.
- Current tip sampled for reruns: `f20a2f6fcceb6769b48109d57904f52376190e44`; both clone HEAD and master aligned to it before the retained reruns.
- Clone: `/fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone`; work: `/fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work`.
- Original seven battery receipts have no COMMAND field. Exact historical argv cannot be recovered from those stamps alone; the seven explicit assignment invocations were used with the clone as --lane and the required shared --work.
- No counter was imported. No frozen instrument, external substrate, or lane implementation file was edited. No tools installed. LSP was not exposed by this seat’s tool inventory; no symbol refactor was needed.

## Frozen tally comparison

| Receipt / mode | Committed tally = reproduced tally | rc | Comparison |
|---|---|---:|---|
| c1-selftest | `SELFTEST cases=6 red=5 failures=0` | 0 | identical |
| c1-mutants | `MUTANTS real=6 expected_matched=6 wrong_id=0 survived=0` | 0 | identical |
| c1-control-declared | `CONTROL rows=7 declared_verdicts=7 agree=7 live=0 target_reached=False` | 0 | identical |
| c2-selftest | `SELFTEST cases=10 red=9 failures=0` | 0 | identical |
| c2-selftest-git | `GIT-ARMS cases=3 failures=0` | 0 | identical |
| c2-mutants | `MUTANTS real=6 expected_matched=6 wrong_id=0 survived=0` | 0 | identical |
| c2-control-status | `CONTROL rows_claimed_closed=7 trivial_checks=7 failed_legs=0 defects=7 target_reached=False` | 0 | identical |

Exact exercised battery argv (seven lines):

```
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c1_declared_surfaces.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --selftest
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c1_declared_surfaces.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --mutants
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c1_declared_surfaces.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --control-declared
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c2_defect_discharge.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --selftest
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c2_defect_discharge.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --selftest-git
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c2_defect_discharge.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --mutants
/usr/bin/python3 /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone/plans/round77_c2_defect_discharge.py --lane /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/clone --work /fast/scratch/hyaku/kengaku-r78/RestampFeasR78/work --control-status
```

## Current-tip reruns

`/usr/bin/python3 plans/round51_surfaces.py --lane .` — exit 0
```
REV f20a2f6fcceb6769b48109d57904f52376190e44
MANIFEST plans/round51-surfaces.json entries=21 sections=2
ANCHORS total=21 dup=0 missing=0
ROWS section="## Surfaces" rows=11 entries=11 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=21 present=15 absent=6 errors=0
DRIFT 0
STALE 0
UNVERDICTED 0
NUMBER-DRIFT 0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=15 floor=13 verdict=met
PREDICATE R51-C1 pass
```

`/usr/bin/python3 plans/round75_c1_index_parity.py --lane .` — exit 1
```
LANE_TIP f20a2f6fcceb6769b48109d57904f52376190e44
WORKTREE clean
UNIVERSE knowledge files=74 indexed=74 missing=0 orphan=0
UNIVERSE lessons files=128 indexed=127 missing=1 orphan=0
UNIVERSE evidence dirs=68 indexed=68 missing=0 orphan=0
MISSING lessons/round-77-verifier-spotcheck.md
PREDICATE R75-C1 fail
```

`/usr/bin/python3 plans/routed_open.py --lane .` — exit 0
```
ROWS total=93 open=31 blocked=1 closed=59 refused=2
routed_open=32 oldest_round=39
```

## Driver recipe

Self-contained argv; run with cwd at a clean repository whose HEAD equals master. R’s parent exists and is writable; choose an output outside the measured tree for repeated invocations. Default mode uses the tool’s --receipt bytes; --plain uses stdout. The driver preserves tool bytes, carries nonzero exits honestly, and refuses a dirty tree before executing or writing the destination. The braces below denote caller-provided values, not literal arguments.

```sh
/usr/bin/python3 -c 'import argparse, hashlib, pathlib, shlex, subprocess, sys, tempfile
p=argparse.ArgumentParser()
p.add_argument("--receipt", required=True)
p.add_argument("--tool", required=True)
p.add_argument("--plain", action="store_true")
p.add_argument("args", nargs=argparse.REMAINDER)
a=p.parse_args()
def git(*v):
    return subprocess.check_output(["git", *v])
def refuse(message):
    sys.exit("REFUSE "+message)
def clean():
    if git("status", "--porcelain", "--untracked-files=all").strip():
        refuse("dirty tree")
clean()
tip=git("rev-parse", "master").decode().strip()
if git("rev-parse", "HEAD").decode().strip()!=tip:
    refuse("HEAD differs from master")
tool=pathlib.Path(a.tool)
if tool.is_absolute() or ".." in tool.parts:
    refuse("tool must be repository-relative")
blob=subprocess.run(["git", "show", tip+":"+a.tool], capture_output=True)
if blob.returncode or not tool.is_file():
    refuse("tool absent at tip")
if tool.read_bytes()!=blob.stdout:
    refuse("tool bytes differ from tip")
extra=a.args[1:] if a.args[:1]==["--"] else a.args
with tempfile.TemporaryDirectory(dir=pathlib.Path(a.receipt).resolve().parent) as work:
    bodypath=pathlib.Path(work)/"tool.receipt"
    cmd=[sys.executable, a.tool]
    if not a.plain:
        cmd += ["--lane", ".", "--work", work, "--receipt", str(bodypath)]
    cmd+=extra
    run=subprocess.run(cmd, stdout=subprocess.PIPE)
    body=run.stdout if a.plain else bodypath.read_bytes()
    clean()
    if git("rev-parse", "master").decode().strip()!=tip:
        refuse("tip changed")
    head=("LANE_TIP "+tip+"\nTOOL "+a.tool+"\nTOOL_SHA "+hashlib.sha256(blob.stdout).hexdigest()+"\nWORKTREE clean\nCOMMAND "+shlex.join(cmd)+"\nMINTED_BY python-inline-restamp\nEXIT "+str(run.returncode)+"\n")
    pathlib.Path(a.receipt).write_bytes(head.encode()+body)
sys.exit(run.returncode)
' --receipt "$R" --tool "$T" [--plain] -- <args>
```

## Exercised recipe outcomes

| Probe | Exit | Result |
|---|---:|---|
| --plain, round51_surfaces --lane . | 0 | located receipt written |
| receipt mode, round77_c1 --selftest | 0 | located receipt written |
| --plain, round75_c1 --lane . | 1 | honest failing receipt written |
| nonexistent tool | 1 | REFUSE tool absent at tip; no receipt |
| untracked dirty-tree sentinel | 1 | REFUSE dirty tree; no receipt |

## Failure modes / limitations observed

1. Initial parallel use of the mandated shared work directory caused `SELFTEST FAIL clean rc=1 want=0 defects=1` / `SELFTEST cases=10 red=9 failures=1` for C2. The battery implementations reuse fixture names (including case-clean); serialized invocations removed this harness collision. The table retains the serial results, not the contaminated run.
2. Cloning a source with a moving/detached HEAD initially selected cd2e25bb rather than freeze. Explicit freeze checkout was required. Later checking out the new tip alone left clone master at cd2e25bb; tools stamp master rather than HEAD. Aligning the scratch-only master ref produced the retained f20a2f6f stamps. No source refs were modified.
3. R75-C1 has `MISSING lessons/round-77-verifier-spotcheck.md`, so re-minting at f20a2f6f does not yield a pass. R51 passes; routed_open has no PREDICATE line and reports its count with exit 0.
4. Recipe missing-tool and dirty-tree refusals are retained above. A red tool verdict is not suppressed or converted to pass.
5. At initial inventory, the lane worktree round78 evidence directory was absent; it is not used for the frozen battery comparison. The lane advanced while the probe ran, so this report claims only the named tips.
6. Existing plans/round78_restamp.py was inspected, not invoked: its interface is spec-driven, not the requested receipt/tool interface, and its inspected rerun path records dirty status rather than refusing a dirty starting tree. The independent inline argv above supplies the requested refusal behavior without modifying it.
7. Named finite bash calls were returned by the tool as services despite async=false; they exited 0. This tool inconsistency was reported. Subsequent actual probe subprocesses were awaited directly.

## Retained raw frozen battery outputs

### c1-selftest
```
SELFTEST ok clean rc=0 want=0 defects=0
SELFTEST ok hash-drift rc=1 want=1 defects=1
SELFTEST ok drop-marker rc=1 want=1 defects=1
SELFTEST ok stale-prose rc=1 want=1 defects=1
SELFTEST ok unlisted rc=1 want=1 defects=1
SELFTEST ok stale-absent rc=1 want=1 defects=2
SELFTEST cases=6 red=5 failures=0
```

### c1-mutants
```
MUTANT drop-unlisted killed expected=UNLISTED-SURFACE
MUTANT skip-dated killed expected=UNDECLARED-ABSENT
MUTANT skip-hash killed expected=HASH-DRIFT
MUTANT skip-count killed expected=COUNT-DRIFT
MUTANT skip-stale killed expected=STALE-TEXT
MUTANT trust-declared killed expected=UNDECLARED-ABSENT
MUTANTS real=6 expected_matched=6 wrong_id=0 survived=0
```

### c1-control-declared
```
CONTROL-SKIP mode=declared-only
CONTROL rows=7 declared_verdicts=7 agree=7 live=0 target_reached=False
PREDICATE R77-C1-control pass
```

### c2-selftest
```
SELFTEST ok clean rc=0 want=0 defects=0
SELFTEST ok drop-row rc=1 want=1 defects=1
SELFTEST ok open-row rc=1 want=1 defects=1
SELFTEST ok trivial-check rc=1 want=1 defects=7
SELFTEST ok stale-evidence rc=1 want=1 defects=7
SELFTEST ok negated rc=1 want=1 defects=7
SELFTEST ok empty-scope rc=1 want=1 defects=1
SELFTEST ok leg-v2 rc=1 want=1 defects=1
SELFTEST ok leg-v3 rc=1 want=1 defects=2
SELFTEST ok leg-v4 rc=1 want=1 defects=2
SELFTEST cases=10 red=9 failures=0
```

### c2-selftest-git
```
GIT-ARM ancestor got=ancestor want=ancestor ok
GIT-ARM not-ancestor got=not-ancestor want=not-ancestor ok
GIT-ARM unresolved got=unresolved want=unresolved ok
GIT-ARMS cases=3 failures=0
```

### c2-mutants
```
MUTANT skip-ancestry killed expected=CLOSE-NOT-ANCESTOR
MUTANT skip-evidence killed expected=NO-EVIDENCE-FIELD
MUTANT skip-trivial killed expected=CHECK-TRIVIAL
MUTANT skip-negation killed expected=NEGATED-DISCHARGE
MUTANT skip-legs killed expected=LEG-FAIL
MUTANT skip-scope killed expected=EMPTY-SCOPE
MUTANTS real=6 expected_matched=6 wrong_id=0 survived=0
```

### c2-control-status
```
CONTROL-SKIP mode=status-only
CONTROL rows_claimed_closed=7 trivial_checks=7 failed_legs=0 defects=7 target_reached=False
PREDICATE R77-C2-control pass
```

## Scope / handoff

- Changed file: this report only. All scratch clones, work fixtures, and probe receipts are removed before yield; evidence needed for review is embedded above.
- No permanent code change or frozen-counter repair proposed. Parent owns integrated C2 gate; this seat exercised only assigned batteries, reruns, and recipe probes.
- Self-evaluation (1–5): accuracy 4 (moving-tip observations are explicitly pinned); completeness 4 (original receipts lack historical COMMAND, preventing literal historical-argv proof); clarity 4 (retained raw output length); actionability 4 (recipe requires existing output parent); conciseness 4 (raw evidence retained deliberately). Overall 4.0. Improvement priority: maintain a fixed tip across integration, avoid shared-fixture concurrency, retain historical command stamps. Would the user agree: expected yes, because the R75 red is explicit rather than hidden.
