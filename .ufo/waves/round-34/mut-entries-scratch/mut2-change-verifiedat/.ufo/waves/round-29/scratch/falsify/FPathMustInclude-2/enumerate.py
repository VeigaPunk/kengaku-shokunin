import json, collections, hashlib
raw_path='plans/fixtures/r28/webarena/config_files/test.raw.json'
b=open(raw_path,'rb').read()
d=json.loads(b)
TOKENS=['__GITLAB__','__REDDIT__','__SHOPPING__','__SHOPPING_ADMIN__','__WIKIPEDIA__','__MAP__']
# order-sensitive: emulate source order but non-overlapping semantics of str.replace
ORDER=['__GITLAB__','__REDDIT__','__SHOPPING__','__SHOPPING_ADMIN__','__WIKIPEDIA__','__MAP__']

def walk(node, path, out):
    if isinstance(node, dict):
        for k,v in node.items():
            walk(v, path+[k], out)
    elif isinstance(node, list):
        for i,v in enumerate(node):
            walk(v, path+[('[]',i)], out)
    else:
        out.append((tuple(path), node))

leaves=[]
for i,task in enumerate(d):
    walk(task, [('[]',i)] if False else [], leaves)

def tmpl(path):
    parts=[]
    for c in path:
        if isinstance(c, tuple):
            parts.append('[]')
        else:
            parts.append(c)
    # merge: list marker appended directly to preceding component
    s=''
    for p in parts:
        if p=='[]':
            s+='[]'
        else:
            s = s + ('.' if s and not s.endswith('[]') else ('.' if s else '')) + p
    # simpler: join non-bracket components with dots, keep brackets attached
    out=[]; buf=''
    for p in parts:
        if p=='[]':
            buf+='[]'
        else:
            if buf: out.append(buf)
            buf=p
    if buf: out.append(buf)
    return '.'.join(out)

cnt_leaf=collections.Counter()
cnt_occ=collections.Counter()
tok_leaf=collections.Counter()
tok_occ=collections.Counter()
multi=[]
url_paths={'start_url','eval.reference_url','eval.program_html[].url'}
cat=collections.Counter()
multi_tmpl=collections.Counter()
per_task_paths=collections.defaultdict(set)
for path,val in leaves:
    if not isinstance(val,str): continue
    t=tmpl(path)
    n=0
    per_tokens={}
    for tok in TOKENS:
        c=val.count(tok)
        if c:
            per_tokens[tok]=c
            tok_occ[tok]+=c
            tok_leaf[tok]+=1
            n+=c
    if n:
        cnt_leaf[t]+=1
        cnt_occ[t]+=n
        cat['url_field' if t in url_paths else 'non_url_field']+=1
        if n>1:
            multi.append((t,path,val[:160],per_tokens))
            multi_tmpl[t]+=1
        task_index = path[0][1] if path and isinstance(path[0],tuple) else None
        per_task_paths[task_index].add(t)

print('LEAVES total string leaves:',sum(1 for p,v in leaves if isinstance(v,str)))
print('CHANGED_LEAVES total:',sum(cnt_leaf.values()))
print('CHANGED_OCCURRENCES total:',sum(cnt_occ.values()))
print('BY_TEMPLATE leaves:',dict(sorted(cnt_leaf.items())))
print('BY_TEMPLATE occurrences:',dict(sorted(cnt_occ.items())))
print('BY_CATEGORY leaves:',dict(cat))
print('BY_TOKEN leaves:',{k:tok_leaf[k] for k in TOKENS})
print('BY_TOKEN occurrences:',{k:tok_occ[k] for k in TOKENS})
print('MULTI leaf count:',len(multi),'by template',dict(multi_tmpl))
for m in multi: print('MULTI',m)
