# ReviewerC2R77 — R77-C2 false-green review

Axes: coverage; calibration. Recommendation: do not treat the seven green legs as semantic proof of discharge. No admission or integration performed.

## Scope and method

Read the frozen claims in full first. `git log -1 --format=%H -- plans/round-77-claims.md` exited 0: `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`. Counter bytes read with `git show <freeze>:plans/round77_c2_defect_discharge.py`; SHA256 `7dde7ab0d1d25bcce5247d321fbf906b7d48415ad818d8659fbb8654160bf67c`.

`git diff 07c97fcd -- plans/round77_c2_defect_discharge.py corpus/routed-findings.jsonl` exited 0: one new 777-line counter, no ledger delta in that observation. LSP discovery `read xd://lsp` returned `No such tool`; semantic references/definition/diagnostics unavailable. Text grep located actual conditions; it is not semantic proof. Read and grep covered the claims, counter and closer's routed-id mentions.

Each attack ran the **unmodified frozen counter CLI**, not monkey-patched functions. Scratch fixture text was synthetic; its `.git` file pointed read-only at the lane's object database. Git operations were read-only throughout. Real git ancestry and committed evidence-byte reads remained active. Fixtures deliberately made unrelated legs green, so each delta tests one assertion. The seven synthetic rows use an existing closer literal rather than claiming to be the eventual production ledger. This tests counter acceptance, not whether production rows actually contain those attacks. Baseline exited 0 with the exact eight-field target and `PREDICATE R77-C2 pass`.

## Findings, severity order

### High — V7 accepts receipts without the REQUIRED TOOL_SHA

`plans/round77_c2_defect_discharge.py:286-293` only compares the digest **if** a stamp is present. Frozen CLI `extra-v7-missing-sha`, rc 0, accepted all three receipts consisting of `LANE_TIP <freeze>`, `PREDICATE unrelated pass`, `EXIT 0`, with **no TOOL_SHA**. Output: `LEG V7 ok V7-routed-open V7-r51-c1 V7-r75-c1`; full target; `PREDICATE R77-C2 pass`. This contradicts claims lines 88-89, not merely the stated live-run honesty limit. Predicate identity is also not bound to the particular rerun.

### High — non-frozen V7 change removes even the passing-predicate requirement

`git diff 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb -- plans/round77_c2_defect_discharge.py`, rc 0, showed frozen lines requiring `PREDICATE` and `pass` replaced by current lines 294-298 requiring `EXIT 0` and rejecting only existing predicate lines without `pass`. It also adds EXIT 0 to fixture receipts. Frozen `extra-v7-no-sha-no-predicate` exited 1, `LEG V7 fail ... carries no passing predicate line`. The **same fixture**, run with the lane worktree counter, exited 0 and printed the full target and `PREDICATE R77-C2 pass`. Observed worktree counter SHA `52419b0bd6865bd433fd6f902a0e6642edd3e62f8063052d4e785007fe648425`. This is both apparatus drift and a false green; it is not used to redefine the frozen result.

### Medium — correction semantics can be exactly backwards

`plans/round77_c2_defect_discharge.py:228-241` requires only both substrings and a date. Attack c replaced all three corrections with `2026-11-04 Correction rejected: <new> is false; <old> remains CURRENT.` Frozen CLI rc 0: `LEG V3 ok LOG.md:1 round-76.md:1 SCORECARD.md:1`, full target, predicate pass. Stated limit: V3 proves lexical co-occurrence, not supersession direction or that the new value is current.

### Medium — tilde fenced correction satisfies the supposedly visible-only leg

`plans/round77_c2_defect_discharge.py:77,135-137` strips only triple-backtick fences. Wrapping the lesson correction in a `~~~` fenced block (`b-tilde`) exited 0 with V3 ok/full target/predicate pass. HTML-comment and triple-backtick versions exited 1. This is a survivor against claims line 113's fence-stripping assurance, not just prose disagreement.

### Medium — V1 never compares receipt tallies with the registry

`plans/round77_c2_defect_discharge.py:177-197` checks stamps and tool bytes, then returns ok. `extra-v1-wrong-tallies` changed both receipt bodies to `SELFTEST cases=1 red=0` and `MUTANTS real=1 expected_matched=0 survived=1`, retaining valid tip/digest. Frozen CLI rc 0: V1 ok, V2 ok, full target, predicate pass. Counter docstring lines 24-25 promises tally agreement; registry-only V2 does not provide that comparison.

## Required attack matrix

Command template actually executed for each frozen case:

`python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC2R77/frozen-counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC2R77/<case> --rev worktree`

The initial driver was invoked as `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC2R77/audit.py` (driver rc 0; each counter rc below is captured separately). Followup cases used the same subprocess argv from the Python tool.

| Attack/case | Counter rc and decisive output | Caught? |
|---|---|---|
| a `a-delete-section6` — delete §6 ids from actual closer | 1; `SCOPE ids=5 ... legs_passed=7 legs_pending=0 wrong=0`; predicate fail | Yes, fixed target prevents green. Other sections still name V1-V5: scope parser scans whole closer, not just §6. |
| a `a-empty-scope` — remove every id | 1; `SCOPE ids=0 ... wrong=1`; `DEFECT EMPTY-SCOPE 0 closer names no routed id` | Yes. |
| b `b-html` | 1; `LEG V3 pending corpus/lessons/round-76.md absent`; `legs_passed=6 legs_pending=1 wrong=0` | Yes, target blocks green. |
| b `b-backtick` | 1; same V3 pending and six passed legs | Yes, target blocks green. |
| b `b-tilde` | 0; V3 ok; full target/predicate pass | **No.** |
| c `c-reversed-correction` | 0; V3 ok; full target/predicate pass | **No.** |
| d `d-evidence-added-later` — new path absent at ancestor base | 1; `EVIDENCE-ABSENT-AT-CLOSE R76-V1`; discharged=6 | Yes. |
| d `d-existing-file-later-literal` — existing tool at ancestor c8c116b4, literal added later | 1; `EVIDENCE-LITERAL-MISSING R76-V1`; discharged=6 | Yes. Literal: `LOOPBACK_HOSTS = ("127.0.0.1", "localhost", "::1")`; present at freeze, absent at c8c116b4. |
| e `e-reused-different-argv` — valid frozen tool stamp, argv changed to selftest | 0; V7 ok; full target/predicate pass | **No; stated provenance limit.** |
| e `e-tip-sha-different-argv` — stamp actual measured tip 6f0c7ad99af0fcf80b3b9fe4f7ba5dfed6288934 and its tool digests; argv selftest with different inputs | 0; V7 ok; full target/predicate pass | **No; stated provenance limit.** |
| f `f-pending-existing-input` — SKILL file exists, registry marker hidden in HTML comment at a revision where inputs exist | 1; `LEG V2 pending round-76 SKILL rows absent`; `legs_passed=6 legs_pending=1 wrong=0`; predicate fail | Yes for target; diagnostics call present-but-hidden input absent and record zero defects. |
| g `g-status-only-faked-v4` — seven closed/trivial/stale rows plus fabricated V4 heading | 1; V4 ok and all 7 legs ok, but seven `CHECK-TRIVIAL+EVIDENCE-LITERAL-MISSING` defects; `discharged=0 ... wrong=7` | Yes. Even faking that leg cannot erase ledger defects. |

All false-green cases above printed:

`SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0`

`DEFECTS n=0`

`PREDICATE R77-C2 pass`

## Residual risks and verification gaps

- Surviving stated limits: argv/receipt reuse is unchecked; V3 direction is lexical; Markdown visibility misses tilde fences; V1 checks stamps but not result tallies; V7 digest is optional. Do not claim these properties from the green metric.
- Canonical rejection for late evidence is in `ledger_report` lines 348-372: real ancestry followed by `reader.at(close, ev_path)` and literal containment in that tree. Both absent-path and missing-literal arms were exercised above.
- No production ledger audit at a final landing revision was performed; integration was changing concurrently. These are frozen-counter adversarial CLI results, not final landing acceptance. Reader worktree stamps moved from 8da90eb7 to 6f0c7ad9 during tests; the frozen script hash stayed pinned.
- The fixture object database was real and read-only; fixture documents/receipts were fabricated intentionally. No new commits, clones, alternate runtimes, installs, production edits, or subagent dispatch occurred.
- Runtime rerouting/resume-continuity contracts are outside this counter's changed behavior; no inference made about them.

## Reproduction driver

The following is the exact initial driver. It only creates files under the seat scratch root and runs read-only git commands. Delete that root after use. Followup constructions are described in the matrix; they use the same `run` function and unchanged frozen bytes.

```python
from pathlib import Path
import subprocess, hashlib, json, shutil, sys
ROOT=Path('/fast/scratch/hyaku/kengaku-r77/ReviewerC2R77')
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
FREEZE='9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb'
BASE='07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59'
def git(*args):
 p=subprocess.run(['git','-C',str(LANE),*args],capture_output=True,text=True); assert p.returncode==0,(args,p.stderr); return p.stdout
src=git('show',FREEZE+':plans/round77_c2_defect_discharge.py')
TOOL=ROOT/'frozen-counter.py'; TOOL.write_text(src)
ns={'__file__':str(TOOL),'__name__':'audit_counter'}; exec(compile(src,str(TOOL),'exec'),ns)
print('FREEZE',FREEZE,'COUNTER_SHA',hashlib.sha256(src.encode()).hexdigest())
closer=git('show',FREEZE+':'+ns['CLOSER'])
base={ns['CLOSER']:closer,
 ns['SKILL']:'round76-c1-surface-resolver cases=12 red=11 9/9 NONLOCAL-ANCHOR ESCAPE-ANCHOR OVERFLOW-ANCHOR MALFORMED-DATE DUPLICATE-SURFACE MANIFEST-DRIFT\nround76-c2-defect-discharge cases=14 red=13 12/12 EMPTY-SCOPE LEG-PENDING NEGATED-DISCHARGE\n',
 ns['LOG']:'Second-reviewer classes\nCorrection 2026-11-04 agree=9 disagree=2 superseded by agree=8 disagree=3\n',
 ns['LESSON76']:'Correction 2026-11-04 agree=9 disagree=2 superseded by agree=8 disagree=3\n',
 ns['SCORECARD']:'Correction 2026-11-04 wrong=12 superseded by wrong=13\nprovince-surface-resolver-table-anchored\n',
 ns['PROVINCE']:'province-surface-resolver-table-anchored\n',
 ns['LESSON77']:'tb2_grader_admit remains open\n'}
rows=[dict(id=f'R76-V{i}',status='closed',close='discharged',close_commit=FREEZE,verified_at='2026-11-04',check="grep 'R76-V1' corpus/lessons/round-76-verifier-spotcheck.md",evidence_path=ns['CLOSER'],evidence_literal='R76-V1') for i in range(1,8)]
base[ns['LEDGER']]='\n'.join(map(json.dumps,rows))+'\n'
def stamp(tool):
 b=subprocess.run(['git','-C',str(LANE),'cat-file','blob',FREEZE+':'+tool],capture_output=True); assert b.returncode==0
 return f'LANE_TIP {FREEZE}\nTOOL_SHA {hashlib.sha256(b.stdout).hexdigest()}\n'
for rel in (ns['R76_C1_SELFTEST'],ns['R76_C1_MUTANTS']): base[rel]=stamp(ns['R76_TOOL'])+'SELFTEST cases=12 red=11\nMUTANTS real=9 expected_matched=9 survived=0\n'
for name,(rel,tool) in ns['RERUNS'].items(): base[rel]=stamp(tool)+f'ARGV python3 {tool} --lane .\nPREDICATE {name} pass\nEXIT 0\n'
def run(name,data):
 d=ROOT/name; d.mkdir()
 # Read-only shared object database; no git mutation, clone, init, or commit.
 (d/'.git').write_text('gitdir: '+git('rev-parse','--absolute-git-dir').strip()+'\n')
 for rel,text in data.items():
  p=d/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text)
 cmd=[sys.executable,str(TOOL),'--lane',str(d),'--rev','worktree']
 p=subprocess.run(cmd,capture_output=True,text=True)
 print('\nATTACK',name,'COMMAND', ' '.join(cmd),'RC',p.returncode)
 print(p.stdout,end=''); print(p.stderr,end='')
 return p
run('baseline',base.copy())
a=base.copy(); a[ns['CLOSER']]=closer.split('## 6.')[0]+'## 6. Routed defects\nnone\n'; run('a-delete-section6',a)
a=base.copy(); a[ns['CLOSER']]='# Closure\n## 6. Routed defects\nnone\n'; run('a-empty-scope',a)
for name,left,right in [('b-html','<!--','-->'),('b-backtick','```\n','\n```'),('b-tilde','~~~\n','\n~~~')]:
 a=base.copy(); a[ns['LESSON76']]=left+a[ns['LESSON76']]+right; run(name,a)
a=base.copy()
for rel,old,new in ns['correction_pairs'](None): a[rel]=f'2026-11-04 Correction rejected: {new} is false; {old} remains CURRENT.\n'+('province-surface-resolver-table-anchored\n' if rel==ns['SCORECARD'] else '')+('Second-reviewer classes\n' if rel==ns['LOG'] else '')
run('c-reversed-correction',a)
a=base.copy(); rr=[dict(r) for r in rows]
# The new frozen counter's literal is absent at BASE; its path was added later.
rr[0].update(close_commit=BASE,evidence_path='plans/round77_c2_defect_discharge.py',evidence_literal='R77-C2 counter')
a[ns['LEDGER']]='\n'.join(map(json.dumps,rr)); run('d-evidence-added-later',a)
a=base.copy()
for rel,tool in ns['RERUNS'].values(): a[rel]=a[rel].replace('ARGV python3 '+tool+' --lane .','ARGV python3 '+tool+' --selftest --work /different-inputs')
run('e-reused-different-argv',a)
a=base.copy(); a[ns['SKILL']]='Registry exists; row hidden\n<!--'+base[ns['SKILL']]+'-->\n'; run('f-pending-existing-input',a)
a=base.copy(); rr=[dict(r,check='ok',evidence_path=ns['LESSON76'],evidence_literal='cases=12') for r in rows]; a[ns['LEDGER']]='\n'.join(map(json.dumps,rr)); a[ns['LOG']]='Second-reviewer classes\n'+base[ns['LOG']]; run('g-status-only-faked-v4',a)
a=base.copy()
for rel,tool in ns['RERUNS'].values(): a[rel]=f'LANE_TIP {FREEZE}\nEXIT 0\n'
run('extra-v7-no-sha-no-predicate',a)
a=base.copy()
for rel in (ns['R76_C1_SELFTEST'],ns['R76_C1_MUTANTS']): a[rel]=stamp(ns['R76_TOOL'])+'SELFTEST cases=1 red=0\nMUTANTS real=1 expected_matched=0 survived=1\n'
run('extra-v1-wrong-tallies',a)
```

## Self-evaluation

Accuracy 4/5: CLI results and frozen hash recorded; final landing was not sampled. Completeness 4/5: all seven required attacks plus fence/digest/tally variants; final production ledger remains outside this fixture audit. Clarity 4/5: frozen versus drifting worktree results separated; fixture command paths are intentionally long. Actionability 4/5: conditions and counterexamples identified; no frozen rule edited. Conciseness 4/5: driver retained for reproducibility despite length. Overall 4.0/5. Highest-impact improvement for integration: explicitly carry survivor limits and reject presenting the changed V7 apparatus as the frozen counter.

Cleanup: scratch root removed before terminal submission (cleanup command and result recorded in the seat tool transcript).
