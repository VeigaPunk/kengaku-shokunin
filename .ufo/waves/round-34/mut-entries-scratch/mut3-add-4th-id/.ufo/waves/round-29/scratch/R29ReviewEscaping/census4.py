import json, re, collections
RAW="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
b=open(RAW,'rb').read()
t=b.decode('utf-8')
TOK=["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]
data=json.loads(t)
leaves=[]  # (path_tuple, value)
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+(k,))
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+(f"[{i}]",))
    elif isinstance(o,str): leaves.append((path,o))
walk(data,())
print("total string leaves:",len(leaves))
tok_leaves=[(p,v) for p,v in leaves if any(tk in v for tk in TOK)]
print("leaves containing >=1 env token:",len(tok_leaves))
multi=[(p,v) for p,v in tok_leaves if sum(v.count(tk) for tk in TOK)>1]
print("leaves with >1 occurrence:",len(multi))
print("  total occurrences in those:",sum(sum(v.count(tk) for tk in TOK) for p,v in multi))
for p,v in multi[:6]: print("   ",p,repr(v[:120]))
# runtime markers
rt=[(p,v) for p,v in leaves if "__page__" in v or "__last_url__" in v]
print("runtime-marker leaves:",len(rt), "paths:", dict(collections.Counter(p[-1] for p,v in rt)))
# leaves with __ but not env tokens
other=[(p,v) for p,v in leaves if "__" in v and not any(tk in v for tk in TOK)]
print("leaves with __ but no env token:",len(other), dict(collections.Counter(p[-1] for p,v in other)))
# exact vs suffixed
exact=sum(1 for p,v in tok_leaves if any(v==tk for tk in TOK))
print("exact-token-equal leaves:",exact," non-exact:",len(tok_leaves)-exact)
# shape of start_url
su=[v for p,v in leaves if p[-1]=="start_url"]
c=collections.Counter()
for v in su:
    tk=[x for x in TOK if v.startswith(x)][0]
    rest=v[len(tk):]
    c["suffix_empty" if rest=="" else "suffix_path"]+=1
print("start_url shapes:",dict(c))
# path detail for start_url with suffix
sfx=collections.Counter()
for v in su:
    tk=[x for x in TOK if v.startswith(x)][0]; rest=v[len(tk):]
    sfx[rest[:1]]+=1
print("start_url suffix first-char:",dict(sfx))
# program_html url field shape
uh=[v for p,v in leaves if p[-1]=="url"]
cu=collections.Counter()
for v in uh:
    tk=[x for x in TOK if v.startswith(x)]
    cu[("prefix_"+tk[0]) if tk else "no_prefix"]+=1
print("url leaf shapes:",dict(cu))
# per-token: distinct leaf count & exact counts
per=collections.defaultdict(lambda: [0,0,0])
for p,v in leaves:
    for tk in TOK:
        c=v.count(tk)
        if c: per[tk][0]+=c; per[tk][1]+=1; per[tk][2]+= (1 if v==tk else 0)
for tk in TOK: print(tk,"occ/leaves/exact:",per[tk])
# escaped-slash check
print("escaped_solidus_count:", t.count("\\/"))
print("json_escape_kinds:", dict(collections.Counter(re.findall(r"\\(.)", t))))
