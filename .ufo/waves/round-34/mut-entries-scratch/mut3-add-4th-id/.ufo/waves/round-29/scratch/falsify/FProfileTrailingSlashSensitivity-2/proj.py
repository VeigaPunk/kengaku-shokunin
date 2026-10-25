import json, hashlib, sys
ROOT="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
raw_path=f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json"
prof_path=f"{ROOT}/plans/fixtures/r29/profiles.json"
raw=open(raw_path,"rb").read().decode("utf-8")
profs=json.load(open(prof_path))
order=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
name="trailing_slash_sensitivity"
vals=profs[name]["values"]
# raw occurrence and junction counts
for t in order:
    tok="__"+t+"__"
    print("TOKEN",t,"occ",raw.count(tok),"slash_after",raw.count(tok+"/"))
proj=raw
applied={}
for t in order:
    tok="__"+t+"__"
    applied[t]=proj.count(tok)
    proj=proj.replace(tok,vals[t])
print("applied",json.dumps(applied,sort_keys=True))
print("proj_text_len_chars",len(proj),"utf8_bytes",len(proj.encode()))
print("proj_text_sha256",hashlib.sha256(proj.encode()).hexdigest())
data=json.loads(proj)
print("parsed_tasks",len(data))
def leaves(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from leaves(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from leaves(v,path+"[]")
    elif isinstance(o,str):
        yield path,o
sl=list(leaves(data))
print("string_leaf_count",len(sl))
# per-task serialization digest
h=hashlib.sha256()
for item in data:
    h.update(json.dumps(item,indent=2).encode())
print("concat_per_task_indent2_sha256",h.hexdigest())
# junctions in projected text: value ending '/' followed by raw '/'
junc=0
for t in order:
    v=vals[t]
    if v.endswith("/"):
        junc+=raw.count("__"+t+"__"+"/")
print("value_slash_then_raw_slash_junctions",junc)
# remaining tokens
rem={t:proj.count("__"+t+"__") for t in order}
print("remaining",json.dumps(rem,sort_keys=True))
# decoded-leaf walk changes vs original for token counts
orig=json.loads(raw)
def collect_pairs(a,b,path=""):
    out=[]
    if isinstance(a,dict) and isinstance(b,dict):
        for k in a:
            out+=collect_pairs(a[k],b[k],path+"/"+k)
    elif isinstance(a,list) and isinstance(b,list):
        for i,(x,y) in enumerate(zip(a,b)):
            out+=collect_pairs(x,y,path+"[]")
    elif isinstance(a,str) and isinstance(b,str):
        if a!=b:
            out.append((path,a,b))
    return out
ch=collect_pairs(orig,data)
print("changed_leaf_count",len(ch))
from collections import Counter
bt=Counter()
for p,a,b in ch:
    for t in order:
        if "__"+t+"__" in a: bt[t]+=1
print("changed_leaves_by_token",json.dumps({t:bt[t] for t in order}))
print("category_url_field",sum(1 for p,a,b in ch if p.endswith("/start_url") or p.endswith("/url") or "reference_url" in p))
