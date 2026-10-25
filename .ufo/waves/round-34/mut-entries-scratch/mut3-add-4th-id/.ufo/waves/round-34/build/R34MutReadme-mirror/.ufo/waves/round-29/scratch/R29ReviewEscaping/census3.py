import json, re, collections
RAW="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
t=open(RAW,'rb').read().decode('utf-8')
# all double-underscore placeholder-like patterns
pats=collections.Counter(re.findall(r"__[A-Za-z0-9_]+__", t))
print("ALL __X__ patterns in text:", dict(pats))
# case-insensitive
print("CI:", dict(collections.Counter(m.lower() for m in re.findall(r"__[A-Za-z0-9_]+__",t))))
data=json.loads(t)
print("tasks",len(data))
# start_url value distribution
sv=collections.Counter(d.get("start_url") for d in data)
print("start_url values:", dict(sv))
# sites distribution
print("sites:", dict(collections.Counter(tuple(d.get("sites") or []) for d in data)))
# wikipedia tasks?
w=[d for d in data if "wikipedia" in (d.get("sites") or [])]
print("wikipedia-site tasks:", len(w))
if w: print("sample start_url:", w[0].get("start_url"), "| eval.reference_url:", w[0].get("eval",{}).get("reference_url"))
# 'url' field paths
def walk(o,path,acc):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+[k],acc)
    elif isinstance(o,list):
        for v in o: walk(v,path+["[]"],acc)
    elif isinstance(o,str): acc.append((tuple(path),o))
acc=[];walk(data,[],acc)
urlpaths=collections.Counter(p for p,v in acc if "__" in v)
print("paths of token-bearing leaves:", dict(urlpaths))
# which leaf keys
keyc=collections.Counter(p[-1] for p,v in acc if "__" in v)
print("leaf keys with tokens:", dict(keyc))
