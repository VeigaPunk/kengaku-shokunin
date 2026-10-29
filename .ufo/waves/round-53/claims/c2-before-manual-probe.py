import json,subprocess,sys,time,os,re
from concurrent.futures import ThreadPoolExecutor
rows=json.load(open('rows.json'))
lane=os.path.abspath('lane')
def run(r):
    name,cmd,codes,_=r
    if not cmd or re.search(r'<[^>]+>|\bDIR\b|\bREV\b|\bN\b|\[',cmd): 
        return name,'SKIP-placeholder',None,0,cmd
    t=time.time()
    w=f'/fast/scratch/hyaku/kengaku-r53/L1/w/{name}'; os.makedirs(w,exist_ok=True)
    try:
        p=subprocess.run(cmd,shell=True,cwd=lane,capture_output=True,text=True,timeout=240,env={**os.environ,'TMPDIR':w})
        return name,p.returncode,(p.stdout+p.stderr)[-300:],round(time.time()-t),cmd
    except subprocess.TimeoutExpired:
        return name,'TIMEOUT',None,240,cmd
with ThreadPoolExecutor(6) as ex:
    res=list(ex.map(run,rows))
json.dump(res,open('rowruns.json','w'))
for r,x in zip(rows,res): print(x[0],'exit=',x[1],'listed=',r[2],'t=',x[3])
