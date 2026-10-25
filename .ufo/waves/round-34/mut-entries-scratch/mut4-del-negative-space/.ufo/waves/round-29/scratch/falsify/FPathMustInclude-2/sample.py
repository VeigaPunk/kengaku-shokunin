import json, hashlib
raw_bytes=open('plans/fixtures/r28/webarena/config_files/test.raw.json','rb').read()
raw_text=raw_bytes.decode('utf-8')
raw=json.loads(raw_bytes)
profiles=json.load(open('plans/fixtures/r29/profiles.json'))
proj=json.load(open('.ufo/waves/round-29/scratch/falsify/FPathMustInclude-2/projection.json'))
ORDER=['GITLAB','REDDIT','SHOPPING','SHOPPING_ADMIN','WIKIPEDIA','MAP']
TOKENS=['__GITLAB__','__REDDIT__','__SHOPPING__','__SHOPPING_ADMIN__','__WIKIPEDIA__','__MAP__']

def resolve(obj, ptr):
    cur=obj
    for part in ptr.split('/')[1:]:
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur

# choose 5 leaves across profiles: must_include x3 (incl. the 10-leaf task), program_html url, annotation multi
mi=[]
for i,task in enumerate(raw):
    for j,e in enumerate(task['eval']['program_html']):
        for k,v in enumerate(e.get('required_contents',{}).get('must_include',[])):
            if any(t in v for t in TOKENS):
                mi.append((i,j,k,v))
mi_sorted=sorted(mi,key=lambda r:(r[0],r[1],r[2]))
# task with max must_include token leaves
from collections import Counter
per=Counter(r[0] for r in mi)
maxtask=max(per,key=per.get)
samples=[
 ('mi_first', mi_sorted[0]),
 ('mi_task%d'%maxtask, [r for r in mi_sorted if r[0]==maxtask][3]),
 ('mi_last', mi_sorted[-1]),
]
# program_html url sample: pick task 0 if it has one else first
for i,task in enumerate(raw):
    for j,e in enumerate(task['eval']['program_html']):
        u=e.get('url')
        if isinstance(u,str) and any(t in u for t in TOKENS):
            samples.append(('url_%d_%d'%(i,j),(i,j,None,u))); break
    if len(samples)==4: break
# annotation multi
for i,task in enumerate(raw):
    v=task['eval'].get('reference_answer_raw_annotation','')
    if sum(v.count(t) for t in TOKENS)>1:
        samples.append(('annotation_multi',(i,None,None,v))); break
assert len(samples)==5, len(samples)

for label,(i,j,k,v) in samples:
    if label.startswith('mi_'):
        ptr='/%d/eval/program_html/%d/required_contents/must_include/%d'%(i,j,k)
        tmpl='eval.program_html[].required_contents.must_include[]'
    elif label.startswith('url_'):
        ptr='/%d/eval/program_html/%d/url'%(i,j)
        tmpl='eval.program_html[].url'
    else:
        ptr='/%d/eval/reference_answer_raw_annotation'%i
        tmpl='eval.reference_answer_raw_annotation'
    # raw text provenance: find the JSON-escaped representation occurrence
    esc=json.dumps(v)[1:-1]
    assert esc in raw_text, ('not found verbatim',label)
    pos=raw_text.find(esc)
    print('='*70)
    print('SAMPLE',label,'pointer',ptr,'template',tmpl)
    print('  rawfile char offset',pos,'len',len(esc))
    print('  excerpt',repr(raw_text[max(0,pos-60):pos+len(esc)+20]))
    print('  original raw leaf value:',repr(v))
    print('  raw leaf token occurrences:',{t:v.count(t) for t in TOKENS if t in v})
    print('  raw parse confirms pointer value:', resolve(raw,ptr)==v)
    for pname,p in profiles.items():
        manual=v
        for tok in TOKENS:
            manual=manual.replace(tok,p['values'][tok[2:-2]])
        rec=[r for r in proj['profiles'][pname]['tasks'] if r['task_id']==i][0]
        cl=[c for c in rec['changed_leaves'] if c['json_pointer']==ptr]
        assert len(cl)==1, (label,pname,len(cl))
        c=cl[0]
        # full projected text parse check
        text=raw_text
        for tok in TOKENS: text=text.replace(tok,p['values'][tok[2:-2]])
        parsed=json.loads(text)
        ok = (manual==c['projected']==resolve(parsed,ptr) and c['original']==v
              and c['path_template']==tmpl)
        print('  %-26s manual=%r json=%r parse=%r category=%s match=%s' %
              (pname,manual,c['projected'],resolve(parsed,ptr),c['category'],ok))
