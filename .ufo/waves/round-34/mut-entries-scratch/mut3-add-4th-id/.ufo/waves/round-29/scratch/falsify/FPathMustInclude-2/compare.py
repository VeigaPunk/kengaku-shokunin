import json, hashlib, collections
raw_bytes=open('plans/fixtures/r28/webarena/config_files/test.raw.json','rb').read()
raw=json.loads(raw_bytes)
profiles=json.load(open('plans/fixtures/r29/profiles.json'))
proj=json.load(open('.ufo/waves/round-29/scratch/falsify/FPathMustInclude-2/projection.json'))
ORDER=['GITLAB','REDDIT','SHOPPING','SHOPPING_ADMIN','WIKIPEDIA','MAP']
url_paths={'start_url','eval.reference_url','eval.program_html[].url'}

def walk(node, path, out):
    if isinstance(node, dict):
        for k,v in node.items(): walk(v, path+[('k',k)], out)
    elif isinstance(node, list):
        for i2,v in enumerate(node): walk(v, path+[('i',i2)], out)
    else: out.append((path, node))

def tmpl(path):
    out=[]; buf=''
    for kind,c in path:
        if kind=='i': buf+='[]'
        else:
            if buf: out.append(buf); 
            buf=c
    if buf: out.append(buf)
    return '.'.join(out)

def ptr(path):
    return ''.join('/'+str(c) for kind,c in path)

def leaves_of(obj):
    out=[]; walk(obj, [], out); return out

mismatches=[]
for pname,p in profiles.items():
    t=raw_bytes.decode('utf-8')
    for tok in ORDER:
        t=t.replace('__%s__'%tok, p['values'][tok])
    sha=hashlib.sha256(t.encode('utf-8')).hexdigest()
    parsed=json.loads(t)
    if sha!=proj['profiles'][pname]['projected_text_sha256']:
        mismatches.append(('text_sha',pname,sha,proj['profiles'][pname]['projected_text_sha256']))
    cnt=collections.Counter(); cat=collections.Counter(); total=0
    tk=proj['profiles'][pname]['tasks']
    inst_by_index={rec['output_index']:rec for rec in tk}
    for i in range(812):
        want=[]
        for (rp,rv),(pp,pv) in zip(leaves_of(raw[i]), leaves_of(parsed[i])):
            if ptr(rp)!=ptr(pp): mismatches.append(('ptr',pname,i,ptr(rp),ptr(pp))); break
            if rv!=pv:
                tp=tmpl(rp); want.append(('/%d'%i+ptr(rp),tp,rv,pv))
                cnt[tp]+=1; cat['url_field' if tp in url_paths else 'non_url_field']+=1; total+=1
        rec=inst_by_index.get(i)
        if rec is None: mismatches.append(('missing_rec',pname,i)); continue
        if rec['projected_task']!=parsed[i]: mismatches.append(('projected_task',pname,i))
        got=[(c['json_pointer'],c['path_template'],c['original'],c['projected']) for c in rec['changed_leaves']]
        if got!=want:
            mismatches.append(('changed_leaves',pname,i,rec['task_id'],'ptr-order' if [g[0] for g in got]!=[w[0] for w in want] else 'value',
                               [g for g in got if g not in want][:2],[w for w in want if w not in got][:2]))
        for c in rec['changed_leaves']:
            exp='url_field' if c['path_template'] in url_paths else 'non_url_field'
            if c['category']!=exp:
                mismatches.append(('record_category',pname,i,c['json_pointer'],c['category'],exp))
    print('INDEP',pname,'changed',total,'by_template',dict(sorted(cnt.items())),'by_category',dict(cat),'sha',sha)
    if dict(cnt)!=proj['profiles'][pname]['changed_leaves_by_path_template']:
        mismatches.append(('template_totals',pname,dict(cnt),proj['profiles'][pname]['changed_leaves_by_path_template']))
    if dict(cat)!=proj['profiles'][pname]['changed_leaves_by_category']:
        mismatches.append(('category_totals',pname,dict(cat),proj['profiles'][pname]['changed_leaves_by_category']))
    if len(tk)!=812: mismatches.append(('tasks_len',pname,len(tk)))
    # uniqueness of pointer within task
    for rec in tk:
        ps=[c['json_pointer'] for c in rec['changed_leaves']]
        if len(ps)!=len(set(ps)): mismatches.append(('dup_ptr',pname,rec['task_id']))
print('MISMATCHES',len(mismatches))
for m in mismatches[:20]: print('MM',m)
