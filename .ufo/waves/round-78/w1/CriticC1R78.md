# CriticC1R78 — R78-C1 counterexamples

Axes: coverage and calibration. Read-only review of committed source `cd2e25bb80cf618135cc001193df13966ef1c711`; counter SHA-256 `9c4fc23174d65256e3cf6dcc7014e8c79fcac1d3c6d93e229f85dbffae6b212f`. Frozen claims were read in full before commands. No counter imports, lane mutations, installations, or external agent runtimes.

## Reproduction and baseline

The executable driver below reconstructs only committed input bytes in its own initialized Git fixture, verifies its top-level directory before adding/committing, and invokes the unmodified counter as a subprocess. Each case resets ledger, SKILL, and census to the committed baseline before applying its mutation. Receipts are tracked. Command for each case:

```sh
python3 "$S/plans/round78_c1_class_member_ledger.py" --lane "$S" --work "$S/work"
```

Observed baseline: rc=0; `UNIVERSE classes=3 members=12 pairs=13`; `LEDGER rows=12 executed=7 unexecuted=5`; `DEFECTS n=0`; `TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0`; `PREDICATE R78-C1 pass`.

## Findings

### 1. Generic installation presence cannot establish member-specific nonexecution — medium

Item 1; driver case `executed-member-relabeled-unexecuted`. Frozen `network-install-required` detector hits both unexecuted `git-multibranch` and executed `pypi-server`:

```text
DETECTOR-HIT git-multibranch unexecuted corpus/evidence/round52/graders/git-multibranch/tests/test_outputs.py:12 'apt-get update'
DETECTOR-HIT git-multibranch unexecuted corpus/evidence/round52/graders/git-multibranch/tests/test_outputs.py:13 'DEBIAN_FRONTEND=noninteractive apt-get install -y curl expect git openssh-client'
DETECTOR-HIT pypi-server executed corpus/evidence/round52/graders/pypi-server/tests/test.sh:4 'apt-get update'
DETECTOR-HIT pypi-server executed corpus/evidence/round52/graders/pypi-server/tests/test.sh:5 'apt-get install -y curl'
```

Changing pypi-server to unexecuted with that reason and changing network k from 4 to 3 gives rc=0:

```text
CLASS network-service k=3 n=8 census=8 ledger_k=3
LEDGER rows=12 executed=6 unexecuted=6
DEFECTS n=0
TARGET classes=3 members=12 executed=6 unexecuted=6 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

Impact: coverage/calibration. This proves generic syntax presence, not inability to replay or historical nonexecution. Smallest safe correction: keep the frozen detector/claim unchanged this round, but describe it only as syntax-backed categorization; require independent member execution history before interpreting a reason as an execution blocker. The observed hit is not itself a literal frozen-detector violation.

### 2. Same-class swap preserves every target number while attributing execution to the wrong task — high

Item 2; case `wrong-task-same-class-k`: replace git-multibranch's row with pypi-server's executed receipt/predicate/round and demote pypi-server using the shared detector. No SKILL edit. Observed rc=0:

```text
CLASS network-service k=4 n=8 census=8 ledger_k=4
CLASS process-environment k=2 n=3 census=3 ledger_k=2
CLASS db-state k=1 n=2 census=2 ledger_k=1
LEDGER rows=12 executed=7 unexecuted=5
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

Impact: coverage/calibration. Counter checks a pass token but never binds task identity to receipt. Smallest safe correction: validate a member-to-execution-instrument/receipt binding against authoritative committed evidence, not merely a ledger-supplied predicate string. This is a semantic execution-evidence defect, although the weaker literal token-presence gate permits it.

### 3. Fenced shadow rows redefine the class/member universe — high

Item 3; case `fenced-shadow-table-changes-universe`: change actual visible partial cells from `executed` to `replayed`, and append three pipe rows inside a fenced text block under the same section. The third fake partial class is candidate-import, replacing db-state. Uses actual candidate-import census members and tracked census pass receipts. Observed rc=0:

```text
UNIVERSE classes=3 members=13 pairs=17
CLASS network-service k=5 n=8 census=8 ledger_k=5
CLASS process-environment k=2 n=3 census=3 ledger_k=2
CLASS candidate-import k=6 n=6 census=6 ledger_k=6
LEDGER rows=13 executed=10 unexecuted=3
DEFECTS n=0
TARGET classes=3 members=13 executed=10 unexecuted=3 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

Impact: coverage/calibration. `skill_partial_rows` line-scans fenced text; `emit` accepts any nonempty class set rather than enforcing the frozen three-class surface. It even accepts k=n as partial. Smallest safe correction: parse only the actual decision table (exclude fences), reject full execution rows as partial, and explicitly detect disappearance/change of the frozen selected-class surface. Do not silently redefine this round's target to the new universe.

### 4. A census pass from another tool stands in for every execution — high

Item 4; case `foreign-round-tool-all-executions`: point all seven executed ledger rows at the existing tracked round62/class-survey.txt, predicate R62-C1, round 62. No grader execution receipt remains selected. Observed rc=0:

```text
UNIVERSE classes=3 members=12 pairs=13
LEDGER rows=12 executed=7 unexecuted=5
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

Impact: coverage/calibration. `round` only has a numeric range check; no round/member/instrument linkage. This is not an objection to legitimate earlier-round receipts: the substituted receipt is the class census instrument, not any task replay. Smallest safe correction: require execution provenance tying member, predicate, round and actual replay instrument together. Literal frozen pass-token wording is weaker than the claimed execution semantics; report that distinction rather than silently amending the claim.

### 5. Census-plus-ledger rename leaves EXTRA and UNACCOUNTED both zero — medium

Item 5; case `silent-member-rename`: rename pypi-server to not-the-census-task everywhere in the fixture census and the ledger key only. Leave the authentic pypi execution receipt and grader directory unchanged. Observed rc=0:

```text
UNIVERSE classes=3 members=12 pairs=13
LEDGER rows=12 executed=7 unexecuted=5
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

`DEFECTS n=0` means no MEMBER-EXTRA or MEMBER-UNACCOUNTED defect fired. Impact: coverage/calibration. Boundary: requires editing the census as well as the ledger; a ledger-only rename is not demonstrated to bypass the census. Executed members' grader directories are never checked. Smallest safe correction: bind census identity to its committed source capture/roster or immutable baseline digest, and validate receipt task identity. This is a mutable-authority limitation, not evidence the current committed census already contains a rename.

### 6. A single arbitrary VECTOR line is treated as a fully frozen table — high

Additional case `single-vector-no-table`: replace the tracked pypi receipt bytes in the fixture with exactly `VECTOR unrelated frozen=match\n`. No predicate, task identifier, exit, expected table, case count, or leg coverage remains. Observed rc=0:

```text
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

Impact: coverage/calibration. `verdict_token` requires one matching vector line and no `frozen=mismatch`, not a fully frozen vector table. Smallest safe correction: validate the complete frozen case/leg set and its task-specific identity, or require the actual instrument's passing predicate instead of this one-line bypass.

### 7. Duplicate JSON member keys evade exact-once accounting — medium

Additional case `duplicate-json-member`: insert an earlier pypi-server row with status unexecuted and invalid reason, retaining the original later executed key. Python json.loads discards the first occurrence. Observed rc=0:

```text
DEFECTS n=0
TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```

Impact: coverage/calibration. MEMBER-DUPLICATE is named in the frozen defect classes but no duplicate-preserving JSON parse exists. Smallest safe correction: reject duplicate member object keys during JSON decoding before constructing the dictionary.

## Executable reproduction driver

Save this under the seat scratch directory and run `python3 "$HYAKU_SCRATCH/kengaku-r78/CriticC1R78/attack.py"` (default scratch root /fast/scratch/hyaku). Driver subprocess output above was observed directly. The initial fixture attempt used the host default branch and failed with `SETUP unresolved revision 'worktree'`; it supplied no attack evidence. The successful driver below initializes master explicitly. No claim predicates or lane files were changed.

```python
import copy, hashlib, json, os, pathlib, re, subprocess, tempfile
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
seat = pathlib.Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'))/'kengaku-r78/CriticC1R78'
rev = 'cd2e25bb80cf618135cc001193df13966ef1c711'
S = pathlib.Path(tempfile.mkdtemp(dir=seat))
def git(*args):
    return subprocess.check_output(['git','-C',str(lane),*args], text=True)
def put(path, text):
    p = S/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text)
def fg(*args):
    return subprocess.check_output(['git','-C',str(S),*args],text=True)
subprocess.run(['git','-C',str(S),'init','-q','-b','master'],check=True)
assert fg('rev-parse','--show-toplevel').strip() == str(S)
paths = ['SKILL.md','plans/round78_c1_class_member_ledger.py','plans/grader-selected-members.json','corpus/evidence/round62/class-survey.txt']
ledger = json.loads(git('show',rev+':plans/grader-selected-members.json'))
for member,row in ledger['members'].items():
    if row['status']=='executed': paths.append(row['receipt'])
    for name in ('test_outputs.py','test.sh'):
        p=f'corpus/evidence/round52/graders/{member}/tests/{name}'
        if subprocess.run(['git','-C',str(lane),'cat-file','-e',rev+':'+p],capture_output=True).returncode==0: paths.append(p)
original = {p:git('show',rev+':'+p) for p in paths}
for p,text in original.items(): put(p,text)
fg('add','.')
fg('-c','user.name=Critic fixture','-c','user.email=fixture@example.invalid','commit','-qm','isolated committed snapshot')
print('SOURCE_REV',rev)
print('COUNTER_SHA256',hashlib.sha256(original['plans/round78_c1_class_member_ledger.py'].encode()).hexdigest())
base=copy.deepcopy(ledger)
def run(name, data=None, skill=None, census=None):
    put('plans/grader-selected-members.json',json.dumps(data or base))
    put('SKILL.md',skill or original['SKILL.md'])
    put('corpus/evidence/round62/class-survey.txt',census or original['corpus/evidence/round62/class-survey.txt'])
    cmd=['python3',str(S/'plans/round78_c1_class_member_ledger.py'),'--lane',str(S),'--work',str(S/'work')]
    p=subprocess.run(cmd,text=True,capture_output=True)
    print('\nCASE',name,'COMMAND python3 "$S/plans/round78_c1_class_member_ledger.py" --lane "$S" --work "$S/work"','rc='+str(p.returncode))
    for line in p.stdout.splitlines():
        if line.startswith(('UNIVERSE','LEDGER','CLASS ','DEFECT','TARGET','PREDICATE')): print(line)
    if p.stderr: print(p.stderr)
run('baseline')
# Network-install detector copied verbatim from the frozen counter; not imported.
pattern = r'apt-get install|apt-get update|uvx \\\n|-w selenium==|pip install'
for member in ('git-multibranch','pypi-server'):
    for f in ('test_outputs.py','test.sh'):
        path=f'corpus/evidence/round52/graders/{member}/tests/{f}'
        for n,line in enumerate(original.get(path,'').splitlines(),1):
            if re.search(pattern,line): print('DETECTOR-HIT',member,base['members'][member]['status'],path+':'+str(n),repr(line))
data=copy.deepcopy(base)
data['members']['pypi-server']={'status':'unexecuted','classes':['network-service'],'reason':'network-install-required'}
skill=original['SKILL.md'].replace('executed 4 of 8','executed 3 of 8')
run('executed-member-relabeled-unexecuted',data,skill)
# Swap same-class status: unchanged k and totals, but unexecuted member has unrelated task evidence.
data=copy.deepcopy(base)
data['members']['git-multibranch']=copy.deepcopy(base['members']['pypi-server'])
data['members']['pypi-server']={'status':'unexecuted','classes':['network-service'],'reason':'network-install-required'}
run('wrong-task-same-class-k',data)
# All executed members claim the round62 census predicate, not their execution tools.
data=copy.deepcopy(base)
for row in data['members'].values():
    if row['status']=='executed': row.update(receipt='corpus/evidence/round62/class-survey.txt',predicate='R62-C1',round=62)
run('foreign-round-tool-all-executions',data)
# Real table prose excluded, fenced shadow table selected by the line parser.
skill=original['SKILL.md'].replace('executed 4 of 8','replayed 4 of 8').replace('executed 2 of 3','replayed 2 of 3').replace('executed 1 of 2','replayed 1 of 2')
fake='\n```text\n| network-service | 8 | executed 4 of 8 ledger=plans/grader-selected-members.json |\n| process-environment | 3 | executed 2 of 3 ledger=plans/grader-selected-members.json |\n| candidate-import | 6 | executed 6 of 6 ledger=plans/grader-selected-members.json |\n```\n'
skill=skill.replace('\n## Benchmark anti-patterns',fake+'\n## Benchmark anti-patterns')
census=original['corpus/evidence/round62/class-survey.txt']
# Replace third partial class with a different census class using actual member names and an unrelated receipt.
data=copy.deepcopy(base)
for member in ('query-optimize','sqlite-with-gcov'): del data['members'][member]
ids=re.search(r'^CLASS candidate-import count=6 members=(.*)$',census,re.M).group(1).split(',')
for member in ids:
    if member in data['members']:
        data['members'][member]['classes'].append('candidate-import')
        data['members'][member].update(status='executed',round=62,receipt='corpus/evidence/round62/class-survey.txt',predicate='R62-C1')
    else: data['members'][member]={'status':'executed','classes':['candidate-import'],'round':62,'receipt':'corpus/evidence/round62/class-survey.txt','predicate':'R62-C1'}
# headless-terminal status promotion increases network k too.
skill=skill.replace('executed 4 of 8','executed 5 of 8')
run('fenced-shadow-table-changes-universe',data,skill)
# Rename executed member across ledger+census, leaving authentic receipt and grader directory unchanged.
data=copy.deepcopy(base)
data['members']['not-the-census-task']=data['members'].pop('pypi-server')
run('silent-member-rename',data,census=census.replace('pypi-server','not-the-census-task'))
# A frozen vector TABLE is not checked; one arbitrary VECTOR line bypasses predicate absence.
receipt=base['members']['pypi-server']['receipt']
put(receipt,'VECTOR unrelated frozen=match\n')
run('single-vector-no-table')
put(receipt,original[receipt])
# JSON duplicate member key collapses silently.
text=json.dumps(base)
text=text.replace('"members": {','"members": {"pypi-server":{"status":"unexecuted","classes":["network-service"],"reason":"nonsense"},',1)
put('plans/grader-selected-members.json',text)
p=subprocess.run(['python3',str(S/'plans/round78_c1_class_member_ledger.py'),'--lane',str(S),'--work',str(S/'work')],text=True,capture_output=True)
print('\nCASE duplicate-json-member rc='+str(p.returncode))
for line in p.stdout.splitlines():
    if line.startswith(('DEFECT','TARGET','PREDICATE')): print(line)
print('FIXTURE',S)
```

All generated scratch fixtures and the driver were removed before yielding; the report retains the reproducer. No tools installed or upgraded. Source inputs intentionally remain unchanged: this is an assigned critic review, not integration. These are counterexamples for the canonical judge, not an admission/rejection decision by this seat.

Self-review: accuracy 4/5 (exact outputs and source pin; execution-history semantics exceed the literal token gate); completeness 5/5 (all five requested attacks plus two additional); clarity 4/5 (full reproducer increases length); actionability 4/5 (corrections specified, no unauthorized repairs); conciseness 4/5 (long driver retained for reproducibility). Overall 4.2/5. Highest-impact correction is task-specific evidence binding, followed by table/universe parsing and strict vector/duplicate validation.

CRITIC-C1: 7 findings (4 high)
