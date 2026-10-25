import json, collections
raw_text=open('plans/fixtures/r28/webarena/config_files/test.raw.json','rb').read().decode('utf-8')
raw=json.loads(raw_text)
proj=json.load(open('.ufo/waves/round-29/scratch/falsify/FPathMustInclude-2/projection.json'))
TOKENS=['__GITLAB__','__REDDIT__','__SHOPPING__','__SHOPPING_ADMIN__','__WIKIPEDIA__','__MAP__']
T='eval.program_html[].required_contents.must_include[]'

# container type checks
cont=collections.Counter(); mi_types=collections.Counter(); url_types=collections.Counter()
for task in raw:
    ev=task.get('eval',{})
    ph=ev.get('program_html')
    cont['program_html:'+type(ph).__name__]+=1
    for e in ph:
        rc=e.get('required_contents')
        if rc is None: cont['required_contents:missing']+=1; continue
        cont['required_contents:'+type(rc).__name__]+=1
        mi=rc.get('must_include')
        if mi is None: cont['must_include:missing']+=1
        else:
            cont['must_include:'+type(mi).__name__]+=1
            mi_types[(type(mi).__name__, len(mi) if hasattr(mi,'__len__') else -1)]+=0
        u=e.get('url')
        url_types[type(u).__name__]+=1
print('containers',dict(cont))
print('program_html url types',dict(url_types))
print('must_include lengths dist',dict(collections.Counter(len(rc.get('must_include',[])) for t in raw for e in t['eval']['program_html'] for rc in [e.get('required_contents',{})])))
# provenance: all occurrences
prov=proj['occurrence_provenance']
print('provenance entries',len(prov))
bad=[]; per_t=collections.Counter()
for o in prov:
    per_t[o['path_template']]+=1
    off=o['original_input_codepoint_offset']; tok=o['token']
    if raw_text[off:off+len(tok)]!=tok: bad.append(('slice',o))
    if o['string_role']!='value': bad.append(('role',o))
print('prov per template',dict(per_t))
print('prov slice/role mismatches',len(bad), bad[:3])
# all text occurrence positions
pos=[]
for tok in TOKENS:
    start=0
    while True:
        p=raw_text.find(tok,start)
        if p<0: break
        pos.append((p,tok)); start=p+len(tok)
print('raw text occurrences',len(pos),'provenance',len(prov),'same position multiset',
      sorted(pos)==sorted((o['original_input_codepoint_offset'],o['token']) for o in prov))
# must_include provenance entries subset equals our 60 pointers
mi_prov=[o for o in prov if o['path_template']==T]
print('must_include provenance',len(mi_prov),
      'tokens',dict(collections.Counter(o['token'] for o in mi_prov)),
      'tasks',len({o['task_index'] for o in mi_prov}))
# pointer->raw leaf consistency for those
def resolve(obj,ptr):
    cur=obj
    for part in ptr.split('/')[1:]:
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur
ok=all(o['token'] in resolve(raw,o['json_pointer']) for o in mi_prov)
print('all must_include prov pointers resolve and contain token',ok)
# token count at this template by token
print('per-token leaf/occ at template from raw:',
      {tok:sum(1 for o in mi_prov if o['token']==tok) for tok in TOKENS})
# tasks with token overall vs instrument
tasks_by_tok={tok:{o['task_index'] for o in prov if o['token']==tok} for tok in TOKENS}
print('tasks_with_token indep',{k:len(v) for k,v in tasks_by_tok.items()},
      'instrument',proj['population']['tasks_with_token'])
