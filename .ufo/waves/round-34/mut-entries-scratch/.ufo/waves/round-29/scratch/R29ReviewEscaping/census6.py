import json, re, collections, hashlib
RAW="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
rb=open(RAW,'rb').read(); t=rb.decode('utf-8')
TOK=["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]
data=json.loads(t)
def flat(o,path,acc):
    if isinstance(o,dict):
        for k,v in o.items(): flat(v,path+(k,),acc)
    elif isinstance(o,list):
        for i,v in enumerate(o): flat(v,path+(f"[{i}]",),acc)
    elif isinstance(o,str): acc.append((path,o))
def norm(p): return "/".join(("[]" if re.fullmatch(r"\[\d+\]",x) else x) for x in p)
PROF=json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"))
a=[];flat(data,(),a)
for name,prof in PROF.items():
    v=prof["values"]; p=t
    for tk in TOK: p=p.replace(tk, v[tk.strip("_")])
    d=json.loads(p); b=[]; flat(d,(),b)
    ch=[(pa,va,vb) for (pa,va),(_,vb) in zip(a,b) if va!=vb]
    print("PROFILE",name)
    print("  tasks",len(d),"changed_leaves",len(ch))
    print("  changed_by_path:",dict(collections.Counter(norm(pa) for pa,_,_ in ch)))
    # remaining env tokens after projection
    rem=collections.Counter(); rmo=collections.Counter()
    for pa,va in b:
        for tk in TOK:
            c=va.count(tk)
            if c: rem[tk]+=1; rmo[tk]+=c
    print("  remaining_env_token_leaves:",dict(rem),"occ:",dict(rmo))
    # remaining runtime markers
    rmc=collections.Counter()
    for pa,va in b:
        if "__page__" in va or "__last_url__" in va: rmc[norm(pa)]+=1
    print("  runtime_marker_leaves_after:",dict(rmc))
    print("  projected_text_sha256:",hashlib.sha256(p.encode()).hexdigest())
    print("  projected_bytes:",len(p.encode()))
    # non-URL field changes
    nonurl=[(pa,va,vb) for pa,va,vb in ch if norm(pa)!="[]/start_url"]
    print("  non_start_url_changed_leaves:",len(nonurl))
    for pa,va,vb in nonurl[:3]: print("    ",norm(pa),repr(va[:80]),"->",repr(vb[:80]))
print()
# WIKIPEDIA: 23 wikipedia-site tasks but 0 __WIKIPEDIA__ tokens
w=[d for d in data if "wikipedia" in (d.get("sites") or [])]
print("wikipedia tasks:",len(w),"their start_url values:",dict(collections.Counter(x["start_url"] for x in w)))
print("=> __WIKIPEDIA__ token count 0; wikipedia tasks use __MAP__ start_url")
