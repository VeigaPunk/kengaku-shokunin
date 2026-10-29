import subprocess, json, os, sys, time, shutil
from concurrent.futures import ThreadPoolExecutor
B="/fast/scratch/hyaku/kengaku-r53/C2ExecRowsB.bTXB"
SRC="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
rows={
"anchor-digest-check":["python3","plans/anchor_digest_check.py","--lane","."],
"defect-ledger":["python3","plans/defect_ledger.py","--lane","."],
"grader-perturb":["python3","plans/grader_perturb.py","--summary"],
"regex-log-probe":["python3","plans/regex_log_probe.py","--lane","."],
"round35-c1-coverage":["python3","plans/round35_c1_verify.py","--lane","."],
"round39-c1-mutants":["python3","plans/round39_c1_verify.py","--lane","."],
"round43-c2":["python3","plans/round43_c2_verify.py","--lane","."],
"round50-c2":["python3","plans/round50_c2_audit.py","--lane","."],
"tb2-grader-probe":["uv","run","--no-project","--with","biopython==1.85","python3","plans/tb2_grader_probe.py","--lane","."],
}
if len(sys.argv)>2: rows={k:v for k,v in rows.items() if k in sys.argv[2:]}
run=sys.argv[1] if len(sys.argv)>1 else "1"
def go(n):
    d=f"{B}/r{run}-{n}"; subprocess.run(["git","clone","-q","--shared",SRC,d+"/lane"] if False else ["git","clone","-q","--shared",SRC,d],check=True)
    assert subprocess.run(["git","-C",d,"rev-parse","--show-toplevel"],capture_output=True,text=True).stdout.strip()==d
    tmp=f"{B}/tmp-r{run}-{n}"; os.makedirs(tmp,exist_ok=True)
    env={**os.environ,"TMPDIR":tmp}
    t=time.time()
    try:
        p=subprocess.run(rows[n],cwd=d,capture_output=True,text=True,timeout=900,env=env); rc=p.returncode; out=p.stdout+p.stderr
    except subprocess.TimeoutExpired: rc="TIMEOUT"; out=""
    s=round(time.time()-t,1)
    st=subprocess.run(["git","-C",d,"status","--porcelain"],capture_output=True,text=True).stdout
    open(f"{B}/drv/out-r{run}-{n}.txt","w").write(out)
    return n,rc,s,len(out),st.strip()[:100]
with ThreadPoolExecutor(9) as ex:
    for r in ex.map(go,list(rows)): print(run,*r)
