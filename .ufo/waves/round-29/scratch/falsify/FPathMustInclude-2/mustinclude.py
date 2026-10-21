import json, hashlib, collections
raw_bytes=open('plans/fixtures/r28/webarena/config_files/test.raw.json','rb').read()
raw=json.loads(raw_bytes)
profiles=json.load(open('plans/fixtures/r29/profiles.json'))
proj=json.load(open('.ufo/waves/round-29/scratch/falsify/FPathMustInclude-2/projection.json'))
TOKENS=['__GITLAB__','__REDDIT__','__SHOPPING__','__SHOPPING_ADMIN__','__WIKIPEDIA__','__MAP__']
ORDER=['GITLAB','REDDIT','SHOPPING','SHOPPING_ADMIN','WIKIPEDIA','MAP']
T='eval.program_html[].required_contents.must_include[]'

# every must_include leaf, with type and token occurrence
rows=[]
types=collections.Counter()
for i,task in enumerate(raw):
    ph=task.get('eval',{}).get('program_html',[])
    for j,entry in enumerate(ph):
        mi=entry.get('required_contents',{}).get('must_include',[])
        for k,val in enumerate(mi):
            types[type(val).__name__]+=1
            occ={tok:val.count(tok) for tok in TOKENS if isinstance(val,str) and tok in val}
            if occ: rows.append((i,j,k,val,occ))
print('TOTAL must_include leaves',sum(types.values()),'types',dict(types))
print('must_include leaves with any token',len(rows))
print('tasks containing them',len({r[0] for r in rows}))
per_task=collections.Counter(r[0] for r in rows)
print('per-task count dist',dict(collections.Counter(per_task.values())))
tokleaf=collections.Counter(); tokocc=collections.Counter(); mult=[]
for i,j,k,val,occ in rows:
    for t,c in occ.items(): tokleaf[t]+=1; tokocc[t]+=c
    if sum(occ.values())>1: mult.append((i,j,k,val,occ))
print('by token leaves',dict(tokleaf),'occurrences',dict(tokocc))
print('multi leaves',len(mult))
# leaves with >=2 distinct tokens
distinct=[r for r in rows if len(r[4])>1]
print('leaves with >=2 distinct tokens',len(distinct))
# check instrument records at this template vs rows
for pname,p in profiles.items():
    recs=[]
    for rec in proj['profiles'][pname]['tasks']:
        for c in rec['changed_leaves']:
            if c['path_template']==T:
                recs.append((rec['task_id'],c['json_pointer'],c['original'],c['projected'],tuple(c['tokens'])))
    expected=[]
    for i,j,k,val,occ in rows:
        t=raw_bytes.decode('utf-8')  # placeholder
        expected.append((i,'/%d/eval/program_html/%d/required_contents/must_include/%d'%(i,j,k),val,None,tuple(sorted(occ))))
    print('PROFILE',pname,'instrument must_include records',len(recs),
          'unique tasks',len({r[0] for r in recs}),
          'pointers equal',[r[1] for r in recs]==[e[1] for e in expected],
          'originals equal',[r[2] for r in recs]==[e[2] for e in expected])
    # projected values by manual replacement per profile
    bad=0
    for (tid,ptr,orig,projv,toks),e in zip(recs,expected):
        val=orig
        for tok in TOKENS:
            val=val.replace(tok,p['values'][tok[2:-2]])
        if val!=projv or not projv.startswith(tuple(p['values'].values())):
            # note: projected value might have prefix text before the token URL
            pass
        if val!=projv: bad+=1; print('BAD',pname,tid,ptr,val,projv)
    print('  projected recompute mismatches',bad)
# count leaves whose projected value contains no replacement? ensure each changed
# check URL-looking must_include values and category treatment
url_like=sum(1 for r in rows if '://' in r[3] or r[3].startswith('__'))
print('must_include token leaves that are URL-shaped (contain ://)',url_like)
# all path templates containing 'url'
allt=collections.Counter()
for task in raw:
    def wk(n,path):
        if isinstance(n,dict):
            for kk,v in n.items(): wk(v,path+[kk])
        elif isinstance(n,list):
            for v in n: wk(v,path+['[]'])
        elif isinstance(n,str):
            s='.'.join(path)
            if any(tok in n for tok in TOKENS): allt[s]+=1
    wk(task,[])
print('ALL TEMPLATES with token leaves:',dict(sorted(allt.items())))
