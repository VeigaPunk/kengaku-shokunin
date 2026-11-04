# ReviewerC2R78 — R78-C2 false-green review

Axes: coverage and calibration. Recommendation only; no admission, integration, or claim repair performed.

REVIEW-C2: 4 findings (2 high)

## Scope and evidence identity

Read the complete frozen claims before fixture execution. Reviewed the freeze addition at `2f9eeafb:plans/round78_c2_stamp_location.py` and the available working-file snapshot. Counter SHA-256: frozen `e79fe3fdee1348baa518a9327e19c6865ada4159a925f2efab24ac9fc4913a0b`; working `543fc7b057fe2eba2b36532175e900b56f7f44f97833dae5186523cb8df7382e`. These are different snapshots, not interchangeable evidence. Every outcome below reproduced on both. Line citations refer to the inspected working snapshot. The frozen counter was obtained with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 2f9eeafb:plans/round78_c2_stamp_location.py`, never imported. All counter invocations were separate Python processes against independent fixture repositories.

LSP was unavailable: reading `xd://lsp` returned `No such tool: xd://lsp`; semantic references/definitions/diagnostics could not be obtained. Source inspection and executable fixtures are the evidence, not semantic grep claims. No tools installed or upgraded. No domain runtime, unrelated lane, or subagent invoked. Fixtures were confined to the assigned scratch directory and removed after recording this report.

## Findings, by severity

### 1. HIGH — tool bytes are checked at the audit revision, not the receipt's stamp

Item: own-revision invariant / false green. `Ctx.__init__` sets `self.tip` to master for a working-tree audit (lines 64–66); `exists_at` and `tool_digest` read `self.tip` (91–100). `audit` parses each receipt's `tip` but never changes the context used for those lookups (150–183). Therefore ancestry is checked against the receipt stamp but tool bytes come from another tree.

Fixture: commit tool version A at ancestor T1; advance master to T2 with tool version B; leave receipt stamped T1. With A's full digest, `historic-correct-digest` prints `DEFECT TOOL-DRIFT`, `DEFECT PASS-UNLOCATED`, `DEFECTS n=2`, `TARGET receipts=1 located=0 unlocated=1`, rc 1. Replace only its pin with B's full digest: `historic-wrong-current-digest` prints `DEFECTS n=0`, `TARGET receipts=1 located=1 unlocated=0`, `PREDICATE R78-C2 pass`, rc 0. This directly defeats the frozen own-stamped-revision predicate; it is not a truncation artifact.

Command: the case-labelled invocations in the transcript below (`python3 <snapshot>_counter.py --lane <fixture> --work <scratch>/counter-work`). Action: route the failed invariant to the lane owner; lookup must use the resolved per-receipt revision. Do not restamp away the counter defect.

### 2. HIGH — prefix digest acceptance violates the explicit full-digest kill rule

Item 4. `TOOL_SHA` admits 8–64 hex characters (49), and `digest_matches` explicitly accepts `actual.startswith(pin)` for shorter pins (103–104).

Observed: `pin-8` → `DEFECTS n=0`, `TARGET receipts=1 located=1 unlocated=0`, pass, rc 0. `pin-64-same-prefix-wrong-tail` retains those same first eight characters but deliberately changes every trailing character → `TOOL-DRIFT,PASS-UNLOCATED`, `DEFECTS n=2`, fail, rc 1. `pin-64-correct` → pass, rc 0. Thus only the 64-character input exercises the differing suffix. No real SHA-256 collision was generated or claimed; the demonstrated flaw is acceptance of an under-specified pin. [INFERENCE] An eight-hex pin constrains only 32 bits, unlike a full SHA-256 digest.

Commands: case-labelled transcript and complete independent driver below. The frozen kill rule explicitly requires full comparison; prefix acceptance must not be reported as satisfying it.

### 3. MEDIUM — TOOL-SUPPLIED can locate fabricated numbers without any recoverable producer

Item 1. Lines 170–190 let the supplied marker bypass absent historical bytes. When the tool is absent from the audit tree, neither supplied-tool existence nor its actual bytes are checked. This is more than inability to prove causality: even a nonexistent producer is accepted.

Observed: `supplied-wrong-producer` names an untracked tool containing exactly `print('WRONG OUTPUT')`, stamps that file's full current digest, but claims `SELFTEST cases=999 failures=0` and `PREDICATE R78-C2 pass`. Counter prints `tool=plans/supplied.py sha=yes legs=ok`, `DEFECTS n=0`, target 1/1/0, rc 0. Executing the producer is unnecessary to establish the mismatch: its complete stored bytes are one unconditional print with different output. `supplied-nonexistent` names `plans/never-existed.py`, supplies no digest, and still prints `tool=plans/never-existed.py sha=- legs=ok`, target 1/1/0, pass, rc 0.

Commands: corresponding transcript cases. These receipts demonstrate a provenance/calibration limit, not proof that existing lane receipts were fabricated. The frozen exception intentionally permits supplied tools, so do not silently redefine it into mandatory replay. The closure lesson must distinguish marker acceptance from producer recovery or reproduction of stamped results. A claim that the counter establishes the supplied numbers' origin is unsupported.

### 4. MEDIUM — last-stamp-wins silently suppresses frozen STAMP-CONFLICT and prior failures

Item 2. `stamp_block` (107–116) discards everything before the final matching LANE_TIP; there is no emitted `STAMP-CONFLICT` despite that leg being frozen. A correction does not need to be dated, identify what it supersedes, or even label itself as a correction.

Observed: `earlier-bad-block` produces two defects and rc 1. Append a complete valid stamp block: `append-valid-block` produces zero defects and rc 0 while the original false block remains byte-for-byte. Stronger case `append-distinct-conflicting-tip-no-correction-label` starts with an unresolved `ffffffffffffffffffffffffffffffffffffffff` tip and appends a valid, distinct master-tip block without a correction label: zero defects, pass, rc 0 on both snapshots. No `STAMP-CONFLICT` or earlier `TIP-UNRESOLVED` appears.

Commands: transcript cases below. Append-only supersession can be acceptable for a clearly dated correction while preserving history, but appending alone does not make the earlier assertions true. Record that distinction in the round-78 closure lesson's calibration/append-only corrections section and reference it beside any re-stamped round-77 receipts; the existing round-77 closure §6 is the relevant routed-defect context. No round-78 lesson file was found by the targeted filename discovery at review time. Most importantly, the frozen two-tip conflict leg cannot be silently waived by a code comment: this is a target/counter mismatch for owner judgment, not permission to amend a frozen claim.

## Requested controls and declared residual risk

### Item 3 — unresolved and non-ancestor tips are detected

`unresolved`: stamp forty `f` characters which do not resolve in the independent fixture. Observed `DEFECT TIP-UNRESOLVED .../a.txt`, `DEFECTS n=1`, target 1/0/1, rc 1.

`not-ancestor`: use `git -C <fixture> ... commit-tree <master-tree> -m unrelated` without a parent. The resulting valid commit exists but is not an ancestor of master. Observed `DEFECT TIP-NOT-ANCESTOR .../a.txt`, `DEFECTS n=1`, target 1/0/1, rc 1. Tool bytes were identical, isolating the ancestry leg. Both controls work; findings above do not imply those checks are absent.

### Item 5 — moving receipts escapes the dynamic universe (declared boundary, not a fifth defect)

Start with a good `keep.txt` plus bad `a.txt`: `UNIVERSE dirs=2 receipts=2`, two defects, target 2/1/1, rc 1. Move only the bad receipt to `corpus/evidence/round79/a.txt`: `UNIVERSE dirs=2 receipts=1`, `DEFECTS n=0`, target 1/1/0, pass, rc 0. Moving it instead to `corpus/evidence/round77/sources/a.txt` gives exactly the same green summary. There is no relocation, lost-member, or denominator-regression diagnostic.

This follows the frozen two-directory/sources-excluded universe, so it is not grounds to reopen that universe. It is an observable saturation limit: located=R means every CURRENT selected member, not every historical receipt, and not preserved coverage after movement. Keep at least one valid receipt in these attacks; with zero receipts `emit` requires `receipts > 0` and would fail. The lesson should disclose that reduction can create a green result.

Additional observed scope discrepancy: `signature-after-line40` prepends forty newlines to a valid receipt and still counts it (`receipts=1`, rc 0), because `universe` scans the entire file (136–137), whereas the frozen text specifies first forty lines. This over-inclusion is not a false green and is not counted among the four findings.

## Verification gaps

The report establishes counter behavior on controlled fixtures, not honesty of the lane's actual historical outputs or completion of D1–D5 repairs. No actual supplied-tool provenance or canonical result replay was established. No digest collision was searched. No final-owner acceptance/admission decision is made. A working snapshot may change after its recorded hash; results bind only to the two identified byte snapshots.

## Reproduction driver

Run the following only in the seat's allowed scratch directory; it obtains the frozen committed bytes, snapshots the working bytes, creates repositories with `mktemp -d` under that directory, verifies their roots before mutation, and invokes counters without importing them. The fixture setup uses no lane git mutation. The recorded command was `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/attack.py`.

```python
import hashlib, json, os, pathlib, subprocess, tempfile
S=pathlib.Path(__file__).resolve().parent
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
def run(args,cwd=None):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True); return p
committed=run(['git','-C',LANE,'show','2f9eeafb:plans/round78_c2_stamp_location.py']).stdout
live=pathlib.Path(LANE+'/plans/round78_c2_stamp_location.py').read_text()
results=[]
for version,code in [('frozen',committed),('working',live)]:
 counter=S/(version+'_counter.py'); counter.write_text(code)
 d=pathlib.Path(run(['mktemp','-d',str(S/(version+'-XXXXXX'))]).stdout.strip())
 def git(*args,mutation=False):
  if mutation:
   assert run(['git','-C',str(d),'rev-parse','--show-toplevel']).stdout.strip()==str(d)
  p=run(['git','-C',str(d),*args]); assert p.returncode==0,(args,p.stderr); return p.stdout.strip()
 p=run(['git','-C',str(d),'init','-q','-b','master']); assert p.returncode==0
 tool=d/'plans/tool.py'; tool.parent.mkdir(); tool.write_text("print('NOT THE STAMPED NUMBERS')\n")
 git('add','plans/tool.py',mutation=True)
 git('-c','user.name=fixture','-c','user.email=fixture@fixture','commit','-qm','tool',mutation=True)
 tip=git('rev-parse','master'); digest=hashlib.sha256(tool.read_bytes()).hexdigest()
 receipt=d/'corpus/evidence/round77/a.txt'; receipt.parent.mkdir(parents=True)
 good=f'LANE_TIP {tip}\nWORKTREE clean\nTOOL plans/tool.py\nTOOL_SHA {digest}\nCOMMAND python3 plans/tool.py\nPREDICATE R78-C2 pass\n'
 def test(name,text):
  receipt.write_text(text)
  cmd=['python3',str(counter),'--lane',str(d),'--work',str(S/'counter-work')]
  p=run(cmd); results.append({'version':version,'case':name,'command':' '.join(cmd),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 test('baseline',good)
 supplied=d/'plans/supplied.py'; supplied.write_text("print('WRONG OUTPUT')\n"); sh=hashlib.sha256(supplied.read_bytes()).hexdigest()
 test('supplied-wrong-producer',f'LANE_TIP {tip}\nWORKTREE dirty\nTOOL plans/supplied.py\nTOOL_SHA {sh}\nTOOL-SUPPLIED plans/supplied.py absent at stamp\nCOMMAND python3 plans/supplied.py\nSELFTEST cases=999 failures=0\nPREDICATE R78-C2 pass\n')
 test('supplied-nonexistent',f'LANE_TIP {tip}\nWORKTREE dirty\nTOOL-SUPPLIED plans/never-existed.py absent at stamp\nCOMMAND python3 plans/never-existed.py\nPREDICATE R78-C2 pass\n')
 bad=good.replace(digest,'0'*64)
 test('earlier-bad-block',bad)
 test('append-valid-block',bad+'\nCORRECTION supersedes prior stamp\n'+good)
 test('unresolved',good.replace(tip,'f'*40))
 tree=git('rev-parse','master^{tree}')
 orphan=git('-c','user.name=fixture','-c','user.email=fixture@fixture','commit-tree',tree,'-m','unrelated',mutation=True)
 test('not-ancestor',good.replace(tip,orphan))
 test('pin-8',good.replace(digest,digest[:8]))
 wrongfull=digest[:8]+''.join('0' if c!='0' else '1' for c in digest[8:])
 test('pin-64-same-prefix-wrong-tail',good.replace(digest,wrongfull))
 test('pin-64-correct',good)
 keep=receipt.parent/'keep.txt'; keep.write_text(good)
 test('universe-before-move',bad)
 for destname in ['corpus/evidence/round79/a.txt','corpus/evidence/round77/sources/a.txt']:
  dest=d/destname; dest.parent.mkdir(parents=True,exist_ok=True)
  receipt.replace(dest)
  cmd=['python3',str(counter),'--lane',str(d),'--work',str(S/'counter-work')]
  p=run(cmd); results.append({'version':version,'case':'move-'+destname,'command':' '.join(cmd),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
  dest.replace(receipt)
 keep.unlink()
 test('signature-after-line40','\n'*40+good)
 tool.write_text("print('NEW TOOL')\n"); newdigest=hashlib.sha256(tool.read_bytes()).hexdigest()
 git('add','plans/tool.py',mutation=True)
 git('-c','user.name=fixture','-c','user.email=fixture@fixture','commit','-qm','new tool',mutation=True)
 test('historic-correct-digest',good)
 test('historic-wrong-current-digest',good.replace(digest,newdigest))
results_path=S/'results.json'; results_path.write_text(json.dumps(results,indent=2))
print('COUNTER_HASHES frozen='+hashlib.sha256(committed.encode()).hexdigest()+' working='+hashlib.sha256(live.encode()).hexdigest())
for r in results:
 print('\nCASE',r['version'],r['case'],'rc='+str(r['rc'])); print(r['stdout'],end=''); print(r['stderr'],end='')

```

The distinct-tip append extension used the existing fixture after its second commit: construct a fully pinned current-master good block, write `good.replace(tip, "f" * 40) + good` to `a.txt`, then invoke the same counter command. This preserves two different LANE_TIP lines with no intervening correction label.

## Observed command/output transcript

### frozen / baseline

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / supplied-wrong-producer

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=dirty tool=plans/supplied.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / supplied-nonexistent

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=dirty tool=plans/never-existed.py sha=- legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / earlier-bad-block

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### frozen / append-valid-block

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / unresolved

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=ffffffff worktree=clean tool=plans/tool.py sha=yes legs=TIP-UNRESOLVED
DEFECT TIP-UNRESOLVED corpus/evidence/round77/a.txt
DEFECTS n=1
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### frozen / not-ancestor

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=23ddbf31 worktree=clean tool=plans/tool.py sha=yes legs=TIP-NOT-ANCESTOR
DEFECT TIP-NOT-ANCESTOR corpus/evidence/round77/a.txt
DEFECTS n=1
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### frozen / pin-8

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / pin-64-same-prefix-wrong-tail

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### frozen / pin-64-correct

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / universe-before-move

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=2
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/keep.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=2 located=1 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### frozen / move-corpus/evidence/round79/a.txt

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/keep.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / move-corpus/evidence/round77/sources/a.txt

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/keep.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / signature-after-line40

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 4e0d041f8605ea7ed9ec7d7aa9a8321ed3242c2a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / historic-correct-digest

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 1fb98f85ab8be488a2a4abc6e95fc516562978b2
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### frozen / historic-wrong-current-digest

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 1fb98f85ab8be488a2a4abc6e95fc516562978b2
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=4e0d041f worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / baseline

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / supplied-wrong-producer

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=dirty tool=plans/supplied.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / supplied-nonexistent

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=dirty tool=plans/never-existed.py sha=- legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / earlier-bad-block

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### working / append-valid-block

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / unresolved

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=ffffffff worktree=clean tool=plans/tool.py sha=yes legs=TIP-UNRESOLVED
DEFECT TIP-UNRESOLVED corpus/evidence/round77/a.txt
DEFECTS n=1
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### working / not-ancestor

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=24b58a1c worktree=clean tool=plans/tool.py sha=yes legs=TIP-NOT-ANCESTOR
DEFECT TIP-NOT-ANCESTOR corpus/evidence/round77/a.txt
DEFECTS n=1
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### working / pin-8

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / pin-64-same-prefix-wrong-tail

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### working / pin-64-correct

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / universe-before-move

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=2
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
RECEIPT corpus/evidence/round77/keep.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=2 located=1 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### working / move-corpus/evidence/round79/a.txt

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/keep.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / move-corpus/evidence/round77/sources/a.txt

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/keep.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / signature-after-line40

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP a61978c0f3e80a1cca9a1e68f61a56604f93822f
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / historic-correct-digest

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP f67701eaa8bbd13293c3d8e40f0077991cec935a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=TOOL-DRIFT,PASS-UNLOCATED
DEFECT TOOL-DRIFT corpus/evidence/round77/a.txt
DEFECT PASS-UNLOCATED corpus/evidence/round77/a.txt
DEFECTS n=2
TARGET receipts=1 located=0 unlocated=1
PREDICATE R78-C2 fail
exit 1
```

### working / historic-wrong-current-digest

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP f67701eaa8bbd13293c3d8e40f0077991cec935a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=a61978c0 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### frozen / append-distinct-conflicting-tip-no-correction-label

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/frozen-9LINfv --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP 1fb98f85ab8be488a2a4abc6e95fc516562978b2
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=1fb98f85 worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

### working / append-distinct-conflicting-tip-no-correction-label

Command: `python3 /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working_counter.py --lane /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/working-qum9pS --work /fast/scratch/hyaku/kengaku-r78/ReviewerC2R78/counter-work`

```text
LANE_TIP f67701eaa8bbd13293c3d8e40f0077991cec935a
WORKTREE dirty
UNIVERSE dirs=2 receipts=1
RECEIPT corpus/evidence/round77/a.txt tip=f67701ea worktree=clean tool=plans/tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=1 located=1 unlocated=0
PREDICATE R78-C2 pass
exit 0
```

Self-evaluation: accuracy 4/5 (no actual digest collision or lane replay claimed); completeness 5/5 (all five requested attacks plus own-revision invariant exercised on two snapshots); clarity 4/5 (full transcript is lengthy but preserves provenance); actionability 4/5 (counter/claim mismatches isolated, owner decision remains); conciseness 4/5 (duplicate snapshot output retained for evidence). Overall 4.2/5. Highest-impact improvement: owner review of findings 1 and 2 before treating a green as calibration evidence.
