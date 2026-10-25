import json, hashlib, collections, sys
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW=LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json'
PROF=LANE+'/plans/fixtures/r29/profiles.json'
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
raw=open(RAW,'rb').read().decode('utf-8')
items=json.loads(raw)
profiles=json.load(open(PROF))

def leaves(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from leaves(v,p+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from leaves(v,p+'/'+str(i))
    elif isinstance(o,str): yield p,o

def projected_item(text, idx):
    proj=json.loads(text)
    return proj[idx]

out={}
for pname in ["distinct_origins","path_prefix","trailing_slash_sensitivity"]:
    vals=profiles[pname]['values']
    text=raw
    for t in ORDER:
        text=text.replace('__%s__'%t, vals[t])
    proj=json.loads(text)
    changed=[]; multi=[]; nonurl=[]; tokcount=collections.Counter()
    for idx,item in enumerate(items):
        if item != proj[idx]:
            # walk both
            def walk(a,b,p):
                if isinstance(a,dict) and isinstance(b,dict):
                    for k in a:
                        walk(a[k],b[k],p+'/'+k)
                elif isinstance(a,list) and isinstance(b,list):
                    for i,(x,y) in enumerate(zip(a,b)):
                        walk(x,y,p+'/'+str(i))
                elif isinstance(a,str) and isinstance(b,str) and a!=b:
                    toks=[]
                    for t in ORDER:
                        tok='__%s__'%t
                        toks += [tok]*a.count(tok)
                    rec=dict(pointer='/%d%s'%(idx,p), template=p, orig=a, proj=b, tokens=toks)
                    changed.append(rec)
                    for tok in toks: tokcount[tok]+=1
                    if len(toks)>1: multi.append(rec)
                    # independent non-URL judgement: not a URL-valued field name and not URL-looking
                    looks_url = a.strip().lower().startswith(('http://','https://'))
                    field_url = p.endswith('/start_url') or p.endswith('/reference_url')
                    if not (looks_url or field_url):
                        nonurl.append(rec)
                else:
                    pass
            walk(item,proj[idx],'')
    bytmpl=collections.Counter(r['template'] for r in changed)
    bypath=collections.Counter()
    for r in changed:
        segs=r['template'].split('/')
        # template path with list indices zeroed
        import re
        tp=re.sub(r'/\d+','/*',r['template'])
        bypath[tp]+=1
    out[pname]=dict(changed_leaf_count=len(changed), by_template=dict(bytmpl),
                    by_path_shape=dict(bypath), by_token=dict(tokcount),
                    multi=multi, nonurl=nonurl,
                    tasks_changed=len({r['pointer'].split('/')[1] for r in changed}),
                    task101=[r for r in changed if r['pointer'].startswith('/101/')])
json.dump(out, open('census.json','w'), indent=1, sort_keys=True)
print('written')
for p,v in out.items():
    print(p, 'leaves',v['changed_leaf_count'],'tasks',v['tasks_changed'],'multi',len(v['multi']),'nonurl',len(v['nonurl']))
    print('  by_token',v['by_token'])
    print('  by_template',v['by_template'])
    print('  task101',v['task101'])
