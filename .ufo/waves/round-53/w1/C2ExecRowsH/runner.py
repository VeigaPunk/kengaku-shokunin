import json, os, subprocess, sys, time, shutil, re
from concurrent.futures import ThreadPoolExecutor
C="/fast/scratch/hyaku/kengaku-r53/C2ExecRowsH"
SRC="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
CANDS=json.load(open(sys.argv[1]))
def one(item):
    name,spec=item
    d=f"{C}/c-{name}/lane"
    if not os.path.isdir(d):
        os.makedirs(os.path.dirname(d),exist_ok=True)
        subprocess.run(["git","clone","-q","--shared",SRC,d],check=True)
    res=[]
    for k in range(2):
        subprocess.run(["git","-C",d,"reset","-q","--hard"]);subprocess.run(["git","-C",d,"clean","-q","-fdx"])
        tmp=f"{C}/c-{name}/tmp{k}"; os.makedirs(tmp,exist_ok=True)
        env={**os.environ,"TMPDIR":tmp}
        t=time.time()
        try:
            p=subprocess.run(spec,cwd=d,capture_output=True,text=True,timeout=900,env=env); rc=p.returncode; out=p.stdout+p.stderr
        except subprocess.TimeoutExpired: rc="TIMEOUT"; out=""
        res.append((rc,round(time.time()-t,1),out))
        shutil.rmtree(tmp,ignore_errors=True)
        open(f"{C}/c-{name}/out{k}.txt","w").write(out)
    return name,res
with ThreadPoolExecutor(8) as ex:
    for name,res in ex.map(one,CANDS.items()):
        print(name,[(r[0],r[1]) for r in res]); 
        for r in res[:1]: print("  "+"\n  ".join(r[2].splitlines()[-6:]))
