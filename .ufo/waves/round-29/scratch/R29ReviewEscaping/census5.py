import json, re, collections
RAW="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
t=open(RAW,'rb').read().decode('utf-8')
TOK=["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]
data=json.loads(t)
leaves=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+(k,))
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+(f"[{i}]",))
    elif isinstance(o,str): leaves.append((path,o))
walk(data,())
def norm(p):
    # canonical path with list indices collapsed
    return "/".join(("[]" if re.fullmatch(r"\[\d+\]",x) else x) for x in p)
env=collections.Counter(); envocc=collections.Counter()
rt=collections.Counter()
for p,v in leaves:
    n=norm(p)
    for tk in TOK:
        c=v.count(tk)
        if c: env[n]+=1; envocc[n]+=c
    if "__page__" in v or "__last_url__" in v: rt[n]+=1
print("ENV-token-bearing leaf paths (leaves / occurrences):")
for k in sorted(env): print("  ",k, env[k], "/", envocc[k])
print("TOTAL env leaves",sum(env.values()),"occ",sum(envocc.values()))
print("RUNTIME-marker leaf paths:",dict(rt),"total",sum(rt.values()))
# now: per-profile projection over serialized text
PROF=json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"))
print()
for name,prof in PROF.items():
    v=prof["values"]
    p=t
    for tk in TOK:
        p=p.replace(tk, v[tk.strip("_")])
    d=json.loads(p)
    # count changed leaves
    def flat(o,path,acc):
        if isinstance(o,dict):
            for k,val in o.items(): flat(val,path+(k,),acc)
        elif isinstance(o,list):
            for i,val in enumerate(o): flat(val,path+(f"[{i}]",),acc)
        elif isinstance(o,str): acc.append((path,o))
    a=[];b=[]
    flat(data,(),a); flat(d,(),b)
    assert len(a)==len(b)
    ch=[(pa,va,vb) for (pa,va),(_,vb) in zip(a,b) if va!=vb]
    print(name,"tasks",len(d),"changed_leaves",len(ch),"src_digest_len",len(p))
    # remaining placeholders
    rem=collections.Counter()
    for pa,va,vb in ch: pass
    allt=collections.Counter()
    for pa,va,vb in b:
        for tk in TOK:
            if tk in va: allt[tk]+=1
    print("   remaining env tokens in projected text:",dict(allt))
    # paths of changed
    print("   changed by path:",dict(collections.Counter(norm(pa) for pa,_,_ in ch)))
