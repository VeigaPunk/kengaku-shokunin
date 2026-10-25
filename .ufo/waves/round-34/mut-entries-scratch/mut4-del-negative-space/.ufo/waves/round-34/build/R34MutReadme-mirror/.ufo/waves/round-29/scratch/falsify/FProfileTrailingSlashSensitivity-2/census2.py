import json,hashlib
ROOT="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
raw=open(f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json","rb").read().decode()
profs=json.load(open(f"{ROOT}/plans/fixtures/r29/profiles.json"))
vals=profs["trailing_slash_sensitivity"]["values"]
order=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
proj=raw
for t in order:
    proj=proj.replace("__"+t+"__",vals[t])
data=json.loads(proj)
orig=json.loads(raw)
def count_leaves(o):
    n=0
    if isinstance(o,dict):
        for v in o.values(): n+=count_leaves(v)
    elif isinstance(o,list):
        for v in o: n+=count_leaves(v)
    elif isinstance(o,str): n+=1
    return n
print("orig_string_leaf_count",count_leaves(orig))
print("proj_string_leaf_count",count_leaves(data))
print("orig_task_count",len(orig),"proj_task_count",len(data))
print("utf8_len",len(proj.encode()),"chars",len(proj))
# tasks containing a junction: raw token+'/' anywhere in a task
tn=0; per=[]
for i,item in enumerate(orig):
    s=json.dumps(item)
    c=sum(s.count("__"+t+"__/") for t in order)
    if c: tn+=1; per.append((i,c))
print("tasks_with_junction",tn,"junction_occurrences_in_task_json",sum(c for _,c in per))
# junctions by leaf path in projected parsed tree
def walk(a,b,path="",out=None):
    if out is None: out=[]
    if isinstance(a,dict):
        for k in a: walk(a[k],b[k],path+"/"+k,out)
    elif isinstance(a,list):
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,path+"[]",out)
    elif isinstance(a,str) and isinstance(b,str) and a!=b:
        for t in order:
            if "__"+t+"__/" in a: out.append((path,t))
    return out
from collections import Counter
pairs=walk(orig,data)
print("changed_leaves_with_junction_token_occurrence",len(set(p for p,_ in pairs)))
print("by_path",json.dumps(dict(Counter(p for p,_ in pairs)),sort_keys=True))
# which raw chars follow each placeholder (all tokens)
for t in order:
    tok="__"+t+"__"; i=0; c=Counter()
    while True:
        j=raw.find(tok,i)
        if j<0: break
        c[raw[j+len(tok):j+len(tok)+1]]+=1; i=j+1
    print(t,dict(c))
