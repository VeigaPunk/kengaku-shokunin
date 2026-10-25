import json, collections, re
RAW="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
t=open(RAW,'rb').read().decode('utf-8')
toks=["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]
# proper single-count walk: values only (not keys)
occ=collections.Counter(); leafcount=collections.Counter(); paths=collections.Counter()
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(v,str):
                for tk in toks:
                    c=v.count(tk)
                    if c: occ[tk]+=c; leafcount[tk]+=1; paths[(path[-1] if path else "?",k)]+=1
            else: walk(v,path+[k])
    elif isinstance(o,list):
        for v in o: walk(v,path+["[]"])
    elif isinstance(o,str):
        for tk in toks:
            c=o.count(tk)
            if c: occ[tk]+=c; leafcount[tk]+=1; paths[(path[-1] if path else "?","<str>")]+=1
data=json.loads(t)
walk(data,[])
print("PROPER value-leaf occurrences:",dict(occ),"sum",sum(occ.values()))
print("PROPER leaves containing token:",dict(leafcount),"sum",sum(leafcount.values()))
print("text occurrences:",{tk:t.count(tk) for tk in toks},"sum",sum(t.count(tk) for tk in toks))
print("paths:",dict(paths))
# where are the extra text occurrences? locate by scanning text context
for tk in toks:
    idxs=[m.start() for m in re.finditer(re.escape(tk),t)]
    print(tk,"text_count",len(idxs))
# duplicate keys check
import json as J
def dup_hook(pairs):
    seen={}
    for k,v in pairs:
        if k in seen: print("DUPKEY",k)
        seen[k]=v
    return seen
J.loads(t,object_pairs_hook=dup_hook)
