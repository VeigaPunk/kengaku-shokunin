import os, json, pathlib, shutil, subprocess, re
S=pathlib.Path('/fast/scratch/hyaku/kengaku-r41/R41PlanNext'); lane=S/'lane'
src=(lane/'plans/state_check.py').read_bytes()
res=json.load(open(S/'res_state_main.json'))
surv=[m for m in res['mutants'] if m['status']=='survived']
def tree(d, drop_fixture=False, edit_fixture=False, toolbytes=src):
    d=pathlib.Path(d); shutil.rmtree(d, ignore_errors=True); (d/'plans').mkdir(parents=True)
    for e in os.listdir(lane):
        if e not in ('plans','.git'): os.symlink(lane/e, d/e)
    for e in os.listdir(lane/'plans'):
        if e in ('fixtures','state_check.py'): continue
        os.symlink(lane/'plans'/e, d/'plans'/e)
    if not drop_fixture:
        shutil.copytree(lane/'plans/fixtures', d/'plans/fixtures')
        if edit_fixture:
            p=d/'plans/fixtures/r25/shonen-seed.txt'; p.write_text(p.read_text()+"x")
    (d/'plans/state_check.py').write_bytes(toolbytes)
    return d
def run(d, *a):
    p=subprocess.run(['python3', str(d/'plans/state_check.py'), *a], capture_output=True, text=True, env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    out=(p.stdout+p.stderr).strip().split('\n'); return (p.returncode, out[-1][:70])
shapes={'A-protocol-none':dict(drop_fixture=True),'B-seed-pin-broken':dict(edit_fixture=True)}
ref={k:run(tree(S/'wit_ref',**v),'--root',str(S/'wit_ref'),'--summary') for k,v in shapes.items()}
print('REF',ref)
for m in surv:
    new=src[:m['a']]+m['new'].encode()+src[m['b']:]
    row=[]
    for k,v in shapes.items():
        d=S/'wit_m'; t=tree(d,toolbytes=new,**v); r=run(t,'--root',str(d),'--summary')
        row.append(f"{k[:1]}:{'DIFF' if r!=ref[k] else 'same'}{'' if r==ref[k] else r}")
    print(m['line'],m['desc'],row)
