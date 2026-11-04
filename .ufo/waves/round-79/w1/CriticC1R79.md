# CriticR79 — R79-C1 falsification

Axes: **coverage**, **calibration**. Review recommendation: **FAIL as evidence of replay coverage**; this is a recommendation, not canonical admission/judgment. The population-accounting improvement itself is real. No frozen rule, source artifact, or counter was changed.

## Scope and method

Read the complete frozen claims and the counter at `5d6843134017780c045e92eed4e83264188a7d47`. All fixture source bytes were fetched with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show <freeze>:<path>`. Independently parsed census lines, derived member/class membership, and copied the relevant frozen files; did not import the counter. Invoked its frozen CLI as the system under attack. Each fixture had its own verified Git root and fixture-only identity. The appendix is the exact reproducer; it reconstructs fixtures and removes them. No tools installed or upgraded.

Independent derivation: 16 classes, 88 distinct members, 230 pairs; baseline statuses 18 located, 6 unlocated, 64 unexecuted, including 57 `unattempted`. Frozen baseline fixture printed `DEFECTS n=0`, `replayed=24 located=18 unlocated=6 unexecuted=64 covered=15`, rc 0.

## 1. Predicate reach — false replay attribution survives

All attacks below use the complete frozen population and correctly derived class lists. Where statuses change, class cells are recomputed rather than left deliberately inconsistent.

| Construction | Observed result | Meaning |
|---|---|---|
| All 88 `unattempted`, `no-blocker: ... sha256=0` | rc 1; `REASON-UNDERSTATED` ×10 | Detector sweep really constrains reasons. Ten applies to all 88, not the seven among the original 64 unexecuted. |
| All 88 unexecuted, first matching frozen detector or `unattempted`, zero hashes | rc 0, defects 0; replayed 0, covered 0 | Cheapest honest accounting ledger passes. This is **allowed by the frozen variable target**, not independently a broken coverage-map claim: it does no replay and must not be sold as replay progress. |
| Replace the 57 existing no-blocker hash strings by sixteen zeros | rc 0, defects 0; exact original 24/18/6/64/15 tuple | Hash-looking evidence is unverified text, not checked provenance. |
| All 88 unlocated with the existing cancel-task instrument and its receipt | rc 1; `INSTRUMENT-SUBJECT` ×87 | A shared genuine instrument cannot impersonate 88 subjects. |
| All 88 unlocated, each with a **three-line non-probing script** whose second-line docstring names that member and round 62; **one genuine census receipt for all** | rc 0, defects 0; replayed 88, located 0, unlocated 88, unexecuted 0, covered 15 | Strongest false-positive. No task execution is added. The census's population-wide predicate counts as each member's execution observation. |
| All 88 executed, census receipt for all | rc 1; `RECEIPT-POPULATION` ×88 | Located path has the important guard; unlocated path does not. |
| All 88 executed, genuine build-pmars receipt for all | rc 1; `SUBJECT-ABSENT` ×87 | Sharing a single subject-specific real receipt is rejected correctly. |
| Keep baseline statuses/instruments; replace each of the six unlocated receipts by a copy of census bytes under its stated round | rc 0, defects 0; **exact original tuple** | Attack does not depend on a new all-unlocated total or zero replay. Unrelated population observations substitute for every original unlocated receipt. |
| Remove stored grader bodies for the 57 `unattempted` members | rc 0, defects 0; exact original tuple | Missing body becomes empty string and silently means detector-silent; “no blocker” can survive absence of the examined source. |

Relevant counter locations: `check()`'s executed branch checks `distinct_members_named`; unlocated branch checks only instrument line 2, receipt round prefix, any observation, absence of the member's subject stamp, and debt text. It never establishes that the named instrument produced that receipt or checks population breadth there. The `unattempted` branch accepts any evidence beginning `no-blocker:`. `Tree.read()` converts missing text to `""`.

Counterexample script content is deliberately **not** called a real probe: it is only a shebang and a docstring. Counter acceptance of this proves a provenance gap, not that any grader was actually executed.

Smallest safe correction: separately price unlocated evidence as **unverified attribution**, not execution-backed coverage, until a tracked capture binds instrument/member and observations. Reject population receipts in this branch too (necessary, not sufficient). Require grader source existence before a detector-silent default. If hash-looking evidence is retained, verify it or explicitly label it informational. These are proposed additive defects/clarifications for the owner; this seat did not repair the frozen claim.

## 2. Coverage 15 — both sides, verdict

**For:** the frozen contract explicitly permits unlocated rows, exposes six of them separately, requires a member-naming historical instrument and a same-round receipt, and names the debt. This is more honest than silently relabeling all 24 as located. The surface being improved is an 88-member map, not new executions. `covered=15` is reproducible under that declared inclusive convention.

**Against:** absence of a subject stamp is precisely absence of receipt-level attribution. An instrument's existence/docstring does not demonstrate it ran or produced a particular observation. The census substitution above passes without any such causal relationship. Independent class derivation shows **located-only coverage is 13**, not 15: `signal-delivery` has located 0 + unlocated 1 of 1; `numeric-band` has located 0 + unlocated 2 of 10. Thus both entire classes represented by the 15-versus-13 difference rest solely on unlocated attribution. This is not the same comparison as census coverage 12; it does not establish three newly replayed classes.

**Verdict:** honest only as “15 classes with located-or-unverified historical replay claims.” Not honest as machine-checked execution-backed coverage of 15. Smallest safe correction is report both `located_covered=13` and `claimed_covered=15`, withholding proof-strength from the latter. Coverage/calibration are harmed by conflating these identities; accepting an attribution policy is a judge-level tradeoff, not something this critic can silently decide away.

## 3. Reason enum — useful absence, not a proven blocker

`unattempted` for 57/64 is an explicit absence of demonstrated work/blocker, not a causal explanation for failure to replay. A reviewer should accept it as an honest inventory status **because the frozen contract expressly allows it**, but reject “all members have proven blocker reasons” or “57 are impossible offline.” The four detectors are a narrow textual vocabulary, not an exhaustive environment feasibility analysis. The reason labels say “required” but matches alone establish textual dependence, not irreducibility.

Falsification: a frozen detector match in one of those bodies falsifies its permitted default and must produce `REASON-UNDERSTATED`; the all-unattempted attack observed this enforcement. A genuine member execution record falsifies a historical claim of never attempting it (the frozen counter does not search for all such records). A changed body/hash falsifies a claimed exact hash reference, but the zero-hash attack passes. Missing body cannot support detector silence, yet the removal attack also passes. Smallest correction: keep the honest default, distinguish status from blocker reason, and reject absent source; do not invent blockers to improve the enum distribution.

## 4. Class rows — actionable arithmetic, misleading proof strength

They are not just decoration: the reader can identify the backlog and navigate the member ledger; the counter compares each cell to member statuses. Most changed in quantitative meaning: **file-artifact**, formerly bare `executed`, now 16 of 76 inclusive, consisting of **12 located + 4 unlocated**, leaving 60 unexecuted. That is a materially different and actionable reading from class-wide readiness.

Most acute semantic caveat: **signal-delivery** says executed 1 of 1 while the sole member `cancel-async-tasks` is unlocated; no located receipt backs the entire class. `numeric-band` similarly has 0 located + 2 unlocated of 10. Counter-generated exact arithmetic does not turn either into located coverage. Smallest correction: distinguish located and unlocated counts beside each cell while preserving the existing population denominator and pointer. The frozen requirement alone only asks for the inclusive count, so this ambiguity is not a spurious `CLASS-K-MISMATCH` finding.

## 5. Controls — useful, not cheapest sufficient challenge

Read frozen receipt bytes with:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show \
  5d6843134017780c045e92eed4e83264188a7d47:corpus/evidence/round79/c1-control-namegrep.txt \
  5d6843134017780c045e92eed4e83264188a7d47:corpus/evidence/round79/c1-control-default-reason.txt \
  5d6843134017780c045e92eed4e83264188a7d47:corpus/evidence/round79/c1-control-all-blocked.txt
```

Recorded outputs: namegrep defects 102 (`CLASS-K-MISMATCH,RECEIPT-POPULATION`); default-reason defects 7 (`REASON-UNDERSTATED`); all-blocked defects 62 (`REASON-UNBACKED`); each `target_reached=False`. These are read historical control outputs, not fresh reruns. The independent fixtures above freshly exercise the relevant source guards.

They test plausible naive skips, but default-reason/all-blocked are cheap extremes, and the six frozen mutants do not challenge the unlocated evidence seam. Cheaper-than-replay skip: create 88 docstring-only “instruments,” attach the existing census observation to all, regenerate 16 cells. **Score against frozen counter: rc 0, defects 0, replayed 88, covered 15.** Even the weaker six-receipt substitution preserves the exact advertised baseline tuple and passes. A regex sweep plus all-unexecuted rows also passes but is contract-compliant inventory work, not the decisive defect.

Recommendation: do not accept the claim as machine-checked replay provenance merely because its three named controls lose. The additional control reaches the frozen dynamic target and exposes the kill-rule concern. The canonical judge/owner must decide withdrawal under the frozen kill rule; this seat neither changes that rule nor issues an admission.

## Reproduction

Save the following appendix as `$HYAKU_SCRATCH/kengaku-r79/CriticC1R79/attack.py` (default scratch `/fast/scratch/hyaku`; the script assumes that saved directory), then run:

```sh
python3 /fast/scratch/hyaku/kengaku-r79/CriticC1R79/attack.py
```

The script uses frozen Git bytes and fixture-only commits, asserts every fixture root before mutation after initialization, invokes the frozen CLI, prints the observed results above, and deletes its fixture directories. The reviewer should remove the saved script afterward. This seat removed all its scratch before yielding. No suite beyond these assigned attack fixtures was run.

```python
import subprocess, pathlib, tempfile, shutil, json, re, hashlib, concurrent.futures
L=pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin'); R='5d6843134017780c045e92eed4e83264188a7d47'; S=pathlib.Path(__file__).parent

def show(p, rev=R):
 return subprocess.check_output(['git','-C',str(L),'show',f'{rev}:{p}']).decode()
C='corpus/evidence/round62/class-survey.txt'; J='plans/grader-population-ledger.json'; P='plans/round79_c1_population_ledger.py'; G='corpus/evidence/round52/graders'
census=show(C); classes={n:[x for x in csv.split(',') if x and x!='-'] for n,count,csv in re.findall(r'^CLASS (\S+) count=(\d+) members=(.*)$',census,re.M)}; members=sorted(set(sum(classes.values(),[]))); doc=json.loads(show(J)); skill=show('SKILL.md')
paths={C,J,P,'SKILL.md'}|{f'{G}/{m}/tests/test_outputs.py' for m in members}|{r[k] for r in doc['members'].values() for k in ('receipt','instrument') if k in r}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: files=dict(zip(sorted(paths),pool.map(show,sorted(paths))))
patterns={'browser-required':r'selenium|webdriver\.(?:Chrome|Firefox)|chromedriver','vm-required':r'qemu-system|qemu-img|/app/isos/|win311','external-db-required':r'GOLDEN_SQL_PATH|/tests/golden\.sql|DB_PATH\s*=\s*Path\(','candidate-library-required':r'sys\.path\.append\(\s*[\"\']/app'}
print('INDEPENDENT census',len(classes),len(members),sum(map(len,classes.values())))
print('INDEPENDENT baseline statuses', {s:sum(r['status']==s for r in doc['members'].values()) for s in ('executed','executed-unlocated','unexecuted')})
print('INDEPENDENT unattempted',sum(r.get('reason')=='unattempted' for r in doc['members'].values()))
for c,ms in classes.items():
 located=sum(doc['members'][m]['status']=='executed' for m in ms); unloc=sum(doc['members'][m]['status']=='executed-unlocated' for m in ms)
 print('CLASS-INDEPENDENT',c,'located',located,'unlocated',unloc,'n',len(ms))
print('BASE-CLASS-ROWS')
print('\n'.join(x for x in show('SKILL.md','660ec0b9').splitlines() if x.startswith('|') and any(x.startswith('| '+c+' |') for c in classes)))
roots=[]
try:
 for mode in ['baseline','all-unattempted','detector-default','bogus-hashes','shared-existing-instrument','all-unlocated-census','all-executed-census','all-executed-one-real','shared-receipt-six','missing-graders']:
  root=pathlib.Path(tempfile.mkdtemp(prefix=mode+'-',dir=S)); roots.append(root)
  subprocess.run(['git','-C',str(root),'init','-q'],check=True)
  assert subprocess.check_output(['git','-C',str(root),'rev-parse','--show-toplevel']).decode().strip()==str(root)
  f=files.copy(); d=json.loads(json.dumps(doc)); rows=d['members']
  if mode in ('all-unattempted','detector-default'):
   for m in members:
    row={'status':'unexecuted','classes':[c for c,ms in classes.items() if m in ms],'reason':'unattempted','evidence':'no-blocker: tests/test_outputs.py sha256=0'}
    if mode=='detector-default':
     for reason,pattern in patterns.items():
      h=re.search(pattern,f[f'{G}/{m}/tests/test_outputs.py'])
      if h: row.update(reason=reason,evidence=h.group()); break
    rows[m]=row
  if mode=='bogus-hashes':
   for r in rows.values():
    if r.get('reason')=='unattempted': r['evidence']='no-blocker: tests/test_outputs.py sha256=0000000000000000'
  if mode in ('shared-existing-instrument','all-unlocated-census'):
   for m in members:
    instrument='plans/round61_c1_cancel_probe.py'
    if mode=='all-unlocated-census':
     instrument=f'plans/fake-{m}.py'; f[instrument]=f'#!/usr/bin/env python3\n"""Offline probe of the pinned Terminal-Bench 2.0 `{m}` grader (round 62)."""\n'
    rows[m]={'status':'executed-unlocated','classes':[c for c,ms in classes.items() if m in ms],'round':62 if mode=='all-unlocated-census' else 61,'receipt':C if mode=='all-unlocated-census' else 'corpus/evidence/round61/cancel-async-probe.txt','instrument':instrument,'debt':'no-subject-stamp'}
  if mode in ('all-executed-census','all-executed-one-real'):
   for m in members: rows[m]={'status':'executed','classes':[c for c,ms in classes.items() if m in ms],'round':62,'receipt':C if mode=='all-executed-census' else 'corpus/evidence/round38/build-pmars-probe.txt','subject':'tb2-header','verdict':'predicate' if mode=='all-executed-census' else 'cases'}
  if mode=='shared-receipt-six':
   for m,r in rows.items():
    if r['status']=='executed-unlocated':
     target=f"corpus/evidence/round{r['round']}/unrelated-census.txt"; f[target]=census; r['receipt']=target
  if mode=='missing-graders':
   for m,r in rows.items():
    if r.get('reason')=='unattempted': del f[f'{G}/{m}/tests/test_outputs.py']
  if mode not in ('baseline','bogus-hashes','missing-graders','shared-receipt-six'):
   def cell(h):
    c=h.group(1); n=len(classes[c]); k=sum(rows[m]['status'] in ('executed','executed-unlocated') for m in classes[c]); return f'| {c} | {h.group(2)} | executed {k} of {n}'
   f['SKILL.md']=re.sub(r'\| ([\w-]+) \| (\d+) \| executed \d+ of \d+',lambda h:cell(h) if h.group(1) in classes else h.group(),skill)
  f[J]=json.dumps(d)
  for p,t in f.items():
   dest=root/p; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(t)
  subprocess.run(['git','-C',str(root),'add','.'],check=True)
  subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','-qm','fixture'],check=True)
  subprocess.run(['git','-C',str(root),'branch','-f','master','HEAD'],check=True)
  result=subprocess.run(['python3',str(root/P),'--lane',str(root),'--quiet','--work',str(root/'work')],text=True,capture_output=True)
  codes={}
  for code in re.findall(r'^DEFECT (\S+)',result.stdout,re.M):codes[code]=codes.get(code,0)+1
  print('ATTACK',mode,'rc',result.returncode,'codes',codes)
  print('\n'.join(l for l in result.stdout.splitlines() if l.startswith(('LEDGER ','COVERAGE ','DEFECTS ','TARGET ','PREDICATE '))))
  if result.stderr: print(result.stderr)
  shutil.rmtree(root); roots.remove(root)
finally:
 for root in roots: shutil.rmtree(root)

```
