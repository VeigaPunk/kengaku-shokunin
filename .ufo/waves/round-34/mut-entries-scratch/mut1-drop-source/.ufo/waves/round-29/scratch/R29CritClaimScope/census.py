import json, re, hashlib, collections, sys
root="/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw_b=open(root+"plans/fixtures/r28/webarena/config_files/test.raw.json","rb").read()
prof_b=open(root+"plans/fixtures/r29/profiles.json","rb").read()
print("raw sha",hashlib.sha256(raw_b).hexdigest(),"bytes",len(raw_b))
raw=raw_b.decode("utf-8"); profs=json.loads(prof_b)
print("codepoints",len(raw),"non-ascii codepoints",sum(1 for c in raw if ord(c)>127))
order=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
data=json.loads(raw); print("tasks",len(data),"distinct ids",len({t["task_id"] for t in data}))
print("index==task_id all:",all(i==t["task_id"] for i,t in enumerate(data)))
for tok in order: print("raw occ",tok,raw.count(f"__{tok}__"))
print("all __X__ patterns:",collections.Counter(re.findall(r"__[A-Za-z_]+?__",raw)).most_common())
# leaves/keys with tokens
toks=[f"__{t}__" for t in order]
leafpaths=collections.Counter(); keyhits=0; taskswith=0; nonurl=collections.Counter()
def walk(o,path,acc):
    global keyhits
    if isinstance(o,dict):
        for k,v in o.items():
            if any(t in k for t in toks): keyhits+=1
            walk(v,path+(k,),acc)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+("[]",),acc)
    elif isinstance(o,str):
        if any(t in o for t in toks): acc.append((path,o))
nleaves=0
for t in data:
    acc=[]; walk(t,(),acc)
    if acc: taskswith+=1
    nleaves+=len(acc)
    for p,v in acc:
        leafpaths["/".join(p)]+=1
print("tasks with token",taskswith,"token-bearing string leaves",nleaves,"keyhits",keyhits)
for p,c in leafpaths.most_common(): print("  path",p,c)
# per-profile projections
for name,pr in profs.items():
    s=raw
    for tok in order: s=s.replace(f"__{tok}__",pr["values"][tok])
    d=json.loads(s)
    changed=0
    def cmp(a,b):
        global changed
        if isinstance(a,dict): [cmp(a[k],b[k]) for k in a]
        elif isinstance(a,list): [cmp(x,y) for x,y in zip(a,b)]
        elif a!=b: changed+=1
    for a,b in zip(data,d): cmp(a,b)
    print(name,"parsed",len(d),"changed leaves",changed,"remaining tokens",sum(s.count(t) for t in toks),
          "'//' after origin count",len(re.findall(r"\.invalid:\d+//",s)),"sha",hashlib.sha256(s.encode()).hexdigest()[:16])
