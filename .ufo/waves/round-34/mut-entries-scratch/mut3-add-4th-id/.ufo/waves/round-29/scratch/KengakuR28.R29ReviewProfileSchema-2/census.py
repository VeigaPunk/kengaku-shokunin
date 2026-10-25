import json,collections,hashlib,sys
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
rawp=LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json'
profp=LANE+'/plans/fixtures/r29/profiles.json'
manp=LANE+'/plans/fixtures/r29/manifest.json'
V=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
raw=open(rawp,encoding='utf-8').read()
prof=json.load(open(profp,encoding='utf-8'))
man=json.load(open(manp,encoding='utf-8'))
def cat(path):
    if path[0]=='start_url': return 'start_url'
    if path[0]=='eval' and path[1]=='reference_url': return 'eval.reference_url'
    if path[0]=='eval' and path[1]=='program_html' and path[-1]=='url': return 'eval.program_html[*].url'
    if path[0]=='eval' and path[1]=='program_html' and 'must_include' in path: return 'eval.program_html[*].required_contents.must_include[*]'
    if path[0]=='eval' and path[1]=='reference_answer_raw_annotation': return 'eval.reference_answer_raw_annotation'
    return 'OTHER:'+str(path)
def walk(o,path=()):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,path+(k,))
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,path+(f"[{i}]",))
    elif isinstance(o,str): yield path,o
data=json.loads(raw)
occ_by_tok=collections.Counter(); leaf_by_cat=collections.Counter(); occ_by_cat=collections.Counter()
scheme_less_leaves=0; scheme_leaves=0; leaves_tok=0
for item in data:
    for path,s in walk(item):
        c=sum(s.count("__%s__"%v) for v in V)
        if not c: continue
        leaves_tok+=1
        c2=cat(path); leaf_by_cat[c2]+=1; occ_by_cat[c2]+=c
        for v in V: occ_by_tok[v]+=s.count("__%s__"%v)
        if '://' in s: scheme_leaves+=1
        else: scheme_less_leaves+=1
print("== frozen input census (raw text vs parsed leaves) ==")
print("raw bytes:",len(raw.encode()),"chars:",len(raw))
print("raw occurrences by token:",{v:occ_by_tok[v] for v in V},"total:",sum(occ_by_tok.values()))
print("raw text count by token:",{v:raw.count("__%s__"%v) for v in V})
print("leaves containing >=1 token:",leaves_tok)
print("leaves by category:",dict(leaf_by_cat))
print("occurrences by category:",dict(occ_by_cat))
print("changed leaves that are scheme-less in raw:",scheme_less_leaves," scheme-bearing:",scheme_leaves)
print("tasks:",len(data),"distinct task_id:",len(set(d['task_id'] for d in data)),
      "index==task_id:",sum(1 for i,d in enumerate(data) if i==d['task_id']))
print()
print("== manifest / profiles schema ==")
print("manifest sha256:",hashlib.sha256(open(manp,'rb').read()).hexdigest())
print("manifest replacement_order==source order:",man['replacement_order']==V)
for f,m in man['files'].items():
    h=hashlib.sha256(open(LANE+'/'+f,'rb').read()).hexdigest()
    print("  pin",f,"declared",m['sha256'],"actual",h,"match",h==m['sha256'])
for name,p in prof.items():
    v=p['values']
    print(" profile",name,"| n_keys",len(v),"| keyorder==source",list(v)==V,"| all_str",all(isinstance(x,str) for x in v.values()),
          "| all_.invalid",all('.invalid' in x for x in v.values()),"| no_embedded_placeholder",not any("__%s__"%k in x for k,x in v.items()),
          "| distinct_values",len(set(v.values()))==6,"| purpose_present",bool(p.get('purpose')))
print("profile count:",len(prof))
print()
print("== hand-expected per-profile projections ==")
for name,p in prof.items():
    t=raw
    for v in V: t=t.replace("__%s__"%v,p['values'][v])
    b=t.encode('utf-8'); pd=json.loads(t)
    rem={v:t.count("__%s__"%v) for v in V}
    # changed leaves/occurrences relative to raw
    cl=0; co=0
    for item in pd:
        for path,s in walk(item):
            c=sum(s.count(p['values'][v]) for v in V)
    # exact leaf-level diff
    cl=0; co=0
    for i,(a,bb) in enumerate(zip(data,pd)):
        for (pa,sa),(pb,sb) in zip(walk(a),walk(bb)):
            if sa!=sb:
                cl+=1
                co+=max(sa.count('__%s__'%v) for v in V)
    print(f" {name}: projected_sha256={hashlib.sha256(b).hexdigest()} bytes={len(b)} tasks={len(pd)} changed_leaves={cl}")
    print(f"    remaining placeholders per token: {rem}")
