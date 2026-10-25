import json,hashlib
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
raw=open(LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json',encoding='utf-8').read()
profs=json.load(open(LANE+'/plans/fixtures/r29/profiles.json',encoding='utf-8'))
inst=json.load(open('instrument.json'))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
TOK=lambda n:"__%s__"%n
dec=json.JSONDecoder(); i=raw.index('[')+1; orig=[]; spans=[]
while True:
    while raw[i] in ' \n\t\r,': i+=1
    if raw[i]==']': break
    v,e=dec.raw_decode(raw,i); orig.append(v); spans.append((i,e)); i=e
def leaves(o, segs=()):
    if isinstance(o,dict):
        for k,v in o.items(): yield from leaves(v, segs+(str(k),))
    elif isinstance(o,list):
        for n,v in enumerate(o): yield from leaves(v, segs+('[]',))
    else: yield segs,o
def segs_from_ptr(p):
    # strip leading /<index>
    parts=p.split('/')[1:]
    assert parts[0].isdigit(), p
    return tuple('[]' if x.isdigit() else x for x in parts[1:])
def segs_from_tmpl(t):
    out=[]
    for part in t.split('.'):
        if part.endswith('[]'):
            base=part[:-2]
            if base: out.append(base)
            out.append('[]')
            out.append('[]')  # must_include[] template has two []: value element after key
        else:
            out.append(part)
    return tuple(out)
# fix: template "eval.program_html[].required_contents.must_include[]" -> segments
def tmpl_segs(t):
    out=[]
    for part in t.split('.'):
        while part.endswith('[]'):
            part=part[:-2]; flag=True
        else:
            flag=False
        if part: out.append(part)
        if flag: out.append('[]')
        # a part could be exactly 'foo[]' -> seg foo then [] ; must_include[] follows key must_include
    return tuple(out)
def cat_of(segs):
    if segs==('start_url',) or segs==('eval','reference_url') or (len(segs)==4 and segs[:2]==('eval','program_html') and segs[2]=='[]' and segs[3]=='url'):
        return 'url_field'
    return 'non_url_field'
fails=[]; checks=0
for pname,pm in profs.items():
    text=raw
    applied={}
    for n in ORDER:
        t=TOK(n); applied[n]=text.count(t); text=text.replace(t,pm['values'][n])
    parr=json.loads(text)
    p=inst['profiles'][pname]
    def chk(c,msg):
        global checks
        checks+=1
        if not c: fails.append((pname,msg))
    chk(p['parsed_task_count']==len(parr)==812, 'parsed_task_count')
    chk(p['projected_text_sha256']==hashlib.sha256(text.encode()).hexdigest(),'projected_text_sha256')
    mine_steps={s['name']:s['applied_replacements'] for s in p['steps']}
    chk(mine_steps==applied,'applied_replacements '+json.dumps(mine_steps)+' mine '+json.dumps(applied))
    chk([s['name'] for s in p['steps']]==ORDER,'step order '+str([s['name'] for s in p['steps']]))
    chk([s['token'] for s in p['steps']]==['__%s__'%n for n in ORDER],'step tokens')
    chk(p['values']==pm['values'],'profile values')
    tot=0; bycat={'url_field':0,'non_url_field':0}; bypath={}; bytok={}; multitask=0; changedtasks=0
    slc=sum(1 for a in orig for _ in leaves(a))
    for idx,(a,b) in enumerate(zip(orig,parr)):
        ol=dict(leaves(a)); pl=dict(leaves(b))
        assert set(ol)==set(pl)
        mine={s:(ol[s],pl[s]) for s in ol if ol[s]!=pl[s]}
        rec=p['tasks'][idx]
        chk(rec['output_index']==idx,'output_index %d'%idx)
        chk(rec['task_id']==a['task_id'],'task_id %d'%idx)
        chk(rec['output_filename']=='config_files/%d.json'%idx,'filename %d'%idx)
        chk(rec['index_equals_task_id']==(a['task_id']==idx),'index_equals_task_id %d'%idx)
        chk(rec['projected_task']==b,'projected_task %d'%idx)
        exp_h=hashlib.sha256(json.dumps(b,indent=2).encode()).hexdigest()
        chk(rec['would_be_file_sha256']==exp_h,'would_be_file_sha256 %d'%idx)
        got={segs_from_ptr(c['json_pointer']):c for c in rec['changed_leaves']}
        chk(len(got)==len(rec['changed_leaves'])==len(mine),'leaf count %d'%idx)
        chk(set(got)==set(mine),'leaf set %d: %s'%(idx,set(got)^set(mine)))
        for s,(ov,pv) in mine.items():
            c=got.get(s)
            if not c: continue
            chk(c['original']==ov and c['projected']==pv,'leaf values %d %s'%(idx,s))
            mytok=[TOK(n) for n in ORDER if TOK(n) in ov]
            chk(c['tokens']==mytok,'leaf tokens %d %s %s vs %s'%(idx,s,c['tokens'],mytok))
            chk(c['category']==cat_of(s),'leaf category %d %s %s'%(idx,s,c['category']))
            tt=tmpl_segs(c['path_template'])
            chk(tt==s,'leaf template %d %s tmpl=%s'%(idx,s,c['path_template']))
            tot+=1; bycat[cat_of(s)]+=1
            bypath[c['path_template']]=bypath.get(c['path_template'],0)+1
            for t in mytok: bytok[t]=bytok.get(t,0)+1
            if sum(ov.count(TOK(n)) for n in ORDER)>1: multitask+=1
        if mine: changedtasks+=1
    chk(p['changed_leaf_count']==tot,'changed_leaf_count %d %d'%(p['changed_leaf_count'],tot))
    chk(p['changed_leaves_by_category']==bycat,'by_category %s %s'%(p['changed_leaves_by_category'],bycat))
    chk(p['changed_leaves_by_path_template']==bypath,'by_path_template '+json.dumps(p['changed_leaves_by_path_template'])+' mine '+json.dumps(bypath))
    chk(p['changed_leaves_by_token']==bytok,'by_token %s %s'%(p['changed_leaves_by_token'],bytok))
    chk(p['changed_leaves_with_multiple_occurrences']==multitask,'multi_occ %d %d'%(p['changed_leaves_with_multiple_occurrences'],multitask))
    chk(p['changed_task_count']==changedtasks,'changed_task_count')
    chk(p['string_leaf_count']==slc,'string_leaf_count %d %d'%(p['string_leaf_count'],slc))
print('checks',checks,'failures',len(fails))
for f in fails[:25]: print('FAIL',f)
