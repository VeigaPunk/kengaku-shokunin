import json,hashlib
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
raw=open(LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json',encoding='utf-8').read()
profs=json.load(open(LANE+'/plans/fixtures/r29/profiles.json',encoding='utf-8'))
inst=json.load(open('instrument.json'))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
TOK=lambda n:"__%s__"%n
dec=json.JSONDecoder(); i=raw.index('[')+1; orig=[]
while True:
    while raw[i] in ' \n\t\r,': i+=1
    if raw[i]==']': break
    v,e=dec.raw_decode(raw,i); orig.append(v); i=e
def leaves(o, segs=()):
    if isinstance(o,dict):
        for k,v in o.items(): yield from leaves(v, segs+(str(k),))
    elif isinstance(o,list):
        for n,v in enumerate(o): yield from leaves(v, segs+('/%d'%n,))
    else: yield segs,o
def canon(segs):
    return tuple('[]' if s.startswith('/') else s for s in segs)
def ptr_segs(p):
    parts=p.split('/')[1:]
    assert parts[0].isdigit(), p
    out=[]
    for x in parts[1:]:
        out.append(x if not x.isdigit() else '/'+x)
    return tuple(out)
def tmpl_segs(t):
    out=[]
    for part in t.split('.'):
        while part.endswith('[]'):
            part=part[:-2]
            if part: out.append(part)
            out.append('[]'); part=''
        if part: out.append(part)
    return tuple(out)
def tmpl_segs_exact(t):
    return tuple(('[]' if s=='[]' else s) for s in tmpl_segs(t))
def cat_of(segs):
    c=canon(segs)
    if c==('start_url',) or c==('eval','reference_url') or c==('eval','program_html','[]','url'): return 'url_field'
    return 'non_url_field'
fails=[]; checks=0
def chk(c,msg):
    global checks
    checks+=1
    if not c: fails.append(msg)
for pname,pm in profs.items():
    text=raw; applied={}
    for n in ORDER:
        t=TOK(n); applied[n]=text.count(t); text=text.replace(t,pm['values'][n])
    parr=json.loads(text); p=inst['profiles'][pname]
    chk(p['parsed_task_count']==len(parr)==812,'%s parsed_task_count'%pname)
    chk(p['projected_text_sha256']==hashlib.sha256(text.encode()).hexdigest(),'%s text_sha'%pname)
    chk({s['name']:s['applied_replacements'] for s in p['steps']}==applied,'%s applied'%pname)
    chk([s['name'] for s in p['steps']]==ORDER,'%s step order'%pname)
    chk(p['values']==pm['values'],'%s values'%pname)
    tot=0; bycat={'url_field':0,'non_url_field':0}; bypath={}; bytok={}; multi=0; ctasks=0
    slc=sum(1 for a in orig for _,v in leaves(a) if isinstance(v,str))
    for idx,(a,b) in enumerate(zip(orig,parr)):
        ol=dict(leaves(a)); pl=dict(leaves(b)); assert set(ol)==set(pl)
        mine={s:(ol[s],pl[s]) for s in ol if ol[s]!=pl[s]}
        rec=p['tasks'][idx]
        chk(rec['output_index']==idx,'%s output_index %d'%(pname,idx))
        chk(rec['task_id']==a['task_id'],'%s task_id %d'%(pname,idx))
        chk(rec['output_filename']=='config_files/%d.json'%idx,'%s filename %d'%(pname,idx))
        chk(rec['index_equals_task_id']==(a['task_id']==idx),'%s index_eq %d'%(pname,idx))
        chk(rec['projected_task']==b,'%s projected_task %d'%(pname,idx))
        chk(rec['would_be_file_sha256']==hashlib.sha256(json.dumps(b,indent=2).encode()).hexdigest(),'%s file_sha %d'%(pname,idx))
        def resolve(ptr):
            cur=parr
            for raw_tok in ptr.split('/')[1:]:
                tok=raw_tok.replace('~1','/').replace('~0','~')
                cur = cur[int(tok)] if isinstance(cur,list) else cur[tok]
            return cur
        got={ptr_segs(c['json_pointer']):c for c in rec['changed_leaves']}
        for c in rec['changed_leaves']:
            chk(resolve(c['json_pointer'])==c['projected'],'%s pointer resolves %d %s'%(pname,idx,c['json_pointer']))
        ok = len(got)==len(rec['changed_leaves'])==len(mine) and set(got)==set(mine)
        chk(ok,'%s leaf set %d got=%d rec=%d mine=%d'%(pname,idx,len(got),len(rec['changed_leaves']),len(mine)))
        for s,(ov,pv) in mine.items():
            c=got.get(s)
            if not c: continue
            chk(c['original']==ov and c['projected']==pv,'%s leaf values %d %s'%(pname,idx,s))
            mytok=[TOK(n) for n in ORDER if TOK(n) in ov]
            chk(c['tokens']==mytok,'%s leaf tokens %d %s %s vs %s'%(pname,idx,s,c['tokens'],mytok))
            chk(c['category']==cat_of(s),'%s leaf cat %d %s %s'%(pname,idx,s,c['category']))
            chk(tmpl_segs(c['path_template'])==canon(s),'%s leaf tmpl %d %s %s'%(pname,idx,canon(s),c['path_template']))
            tot+=1; bycat[cat_of(s)]+=1
            bypath[c['path_template']]=bypath.get(c['path_template'],0)+1
            for t in mytok: bytok[t]=bytok.get(t,0)+1
            if sum(ov.count(TOK(n)) for n in ORDER)>1: multi+=1
        if mine: ctasks+=1
    chk(p['changed_leaf_count']==tot,'%s changed_leaf_count'%pname)
    chk(p['changed_leaves_by_category']==bycat,'%s by_cat %s vs %s'%(pname,p['changed_leaves_by_category'],bycat))
    chk(p['changed_leaves_by_path_template']==bypath,'%s by_tmpl %s vs %s'%(pname,p['changed_leaves_by_path_template'],bypath))
    norm={n:bytok.get(n,0) for n in ['__GITLAB__','__MAP__','__REDDIT__','__SHOPPING_ADMIN__','__SHOPPING__','__WIKIPEDIA__']}
    chk(p['changed_leaves_by_token']==norm,'%s by_tok %s vs %s'%(pname,p['changed_leaves_by_token'],norm))
    chk(p['changed_leaves_with_multiple_occurrences']==multi,'%s multi %d vs %d'%(pname,p['changed_leaves_with_multiple_occurrences'],multi))
    chk(p['changed_task_count']==ctasks,'%s changed_task_count'%pname)
    chk(p['string_leaf_count']==slc,'%s string_leaf_count %d vs %d'%(pname,p['string_leaf_count'],slc))
print('checks',checks,'failures',len(fails))
for f in fails[:20]: print('FAIL',f)
