import json,hashlib
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
raw=open(LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json',encoding='utf-8').read()
profs=json.load(open(LANE+'/plans/fixtures/r29/profiles.json',encoding='utf-8'))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
TOK=lambda n:"__%s__"%n
dec=json.JSONDecoder(); i=raw.index('[')+1; spans=[]; vals=[]
while True:
    while raw[i] in ' \n\t\r,': i+=1
    if raw[i]==']': break
    v,e=dec.raw_decode(raw,i); vals.append(v); spans.append((i,e)); i=e
orig=vals
def leaves(o, ptr=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from leaves(v, ptr+'/'+str(k))
    elif isinstance(o,list):
        for idx,v in enumerate(o): yield from leaves(v, ptr+'/'+str(idx))
    else: yield ptr,o
out={}
for pname,pm in profs.items():
    text=raw
    for n in ORDER: text=text.replace(TOK(n), pm['values'][n])
    parr=json.loads(text)
    tot=0; bycat={}; bypath={}; bytok={}; multi=[]; pertask={}
    nonurl_tasks=[]; url_tasks=set()
    for idx,(a,b) in enumerate(zip(orig,parr)):
        ol=dict(leaves(a)); pl=dict(leaves(b))
        assert set(ol)==set(pl)
        ch=[(p,ol[p],pl[p]) for p in ol if ol[p]!=pl[p]]
        if ch: pertask[idx]=len(ch); tot+=len(ch)
        for p,ov,pv in ch:
            toks=[t for t in ORDER if TOK(t) in ov]
            nocc=sum(ov.count(TOK(t)) for t in toks)
            tmpl=p.lstrip('/')
            # category: url-ish field
            cat='url_field' if (tmpl=='start_url' or tmpl=='eval.reference_url' or tmpl.endswith('.url')) else 'non_url_field'
            bycat[cat]=bycat.get(cat,0)+1
            if cat=='non_url_field': nonurl_tasks.append((idx,p,ov,pv))
            bypath[tmpl]=bypath.get(tmpl,0)+1
            for t in toks: bytok[TOK(t)]=bytok.get(TOK(t),0)+1
            if nocc>1: multi.append((idx,p,ov,toks,nocc))
    out[pname]=dict(total=tot, bycat=bycat, bypath=bypath, bytok=bytok,
                    multi=multi, changed_tasks=len(pertask),
                    text_sha=hashlib.sha256(text.encode()).hexdigest(), nonurl=nonurl_tasks)
    print('==',pname,'total',tot,'tasks',len(pertask),'text_sha',out[pname]['text_sha'])
    print('  bycat',bycat)
    print('  bypath',json.dumps(bypath))
    print('  bytok',bytok)
    print('  multi_leaves',len(multi),'sum_extra_occ',sum(m[4]-1 for m in multi))
    for m in multi: print('   MULTI',m[0],m[1],repr(m[2]),m[3],m[4])
    print('  nonurl count',len(nonurl_tasks))
    for t in nonurl_tasks[:6]: print('   NONURL',t[0],t[1],repr(t[2])[:60],'->',repr(t[3])[:60])
json.dump(out,open('census.json','w'),indent=1,ensure_ascii=False)
