import json, hashlib, sys
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW=LANE+'/plans/fixtures/r28/webarena/config_files/test.raw.json'
PROF=LANE+'/plans/fixtures/r29/profiles.json'
raw_bytes=open(RAW,'rb').read()
raw=raw_bytes.decode('utf-8')
profs=json.load(open(PROF,encoding='utf-8'))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
TOK=lambda n:"__%s__"%n

# original parsed structure + item-311 text span via raw_decode scan
dec=json.JSONDecoder()
i=raw.index('[')+1
spans=[]; vals=[]
while True:
    while i<len(raw) and raw[i] in ' \n\t\r,': i+=1
    if raw[i]==']': break
    v,end=dec.raw_decode(raw,i)
    spans.append((i,end)); vals.append(v); i=end
orig=vals[311]; s,e=spans[311]
print("SPAN311", s, e, "len", e-s)
print("ORIG_TASK_ID", orig['task_id'], "ARRAY_IDX", 311)
# token occurrences inside item span and whole file
span_text=raw[s:e]
for n in ORDER:
    t=TOK(n)
    print("TOKEN_IN_ITEM", n, span_text.count(t), "TOKEN_IN_FILE", raw.count(t))

# independent leaf walk: compare orig vs projected with pointers
def leaves(o, ptr=''):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from leaves(v, ptr+'/'+str(k))
    elif isinstance(o,list):
        for idx,v in enumerate(o):
            yield from leaves(v, ptr+'/'+str(idx))
    else:
        yield ptr,o
def changed(o,p):
    ol=dict(leaves(o)); pl=dict(leaves(p))
    assert set(ol)==set(pl), ("shape mismatch", set(ol)^set(pl))
    out=[]
    for ptr in ol:
        if ol[ptr]!=pl[ptr]:
            out.append((ptr, ol[ptr], pl[ptr]))
    return out

results={}
for pname in ['distinct_origins','path_prefix','trailing_slash_sensitivity']:
    vals_map=profs[pname]['values']
    text=raw
    # sequential global replace in declared order; record per-step replacement counts
    steps=[]
    for n in ORDER:
        t=TOK(n); rep=vals_map[n]
        c=text.count(t)
        steps.append((n,t,c))
        text=text.replace(t,rep)
    proj_arr=json.loads(text)
    assert len(proj_arr)==812
    pitem=proj_arr[311]
    ch=changed(orig,pitem)
    # file hash as upstream would write: json.dump(item, f, indent=2) -- insertion order preserved, ensure_ascii default True, no trailing newline
    body_ordered=json.dumps(pitem, indent=2)
    body_sorted=json.dumps(pitem, indent=2, sort_keys=True)
    h_ordered=hashlib.sha256(body_ordered.encode('utf-8')).hexdigest()
    h_ordered_nl=hashlib.sha256((body_ordered+'\n').encode('utf-8')).hexdigest()
    h_sorted=hashlib.sha256(body_sorted.encode('utf-8')).hexdigest()
    results[pname]=dict(changed=ch, start_url=pitem['start_url'],
        h_ordered=h_ordered, h_nl=h_ordered_nl, h_sorted=h_sorted, steps=steps,
        text_sha=hashlib.sha256(text.encode('utf-8')).hexdigest(),
        item_text=body_ordered)
    print("PROFILE",pname)
    print("  start_url", repr(pitem['start_url']))
    print("  changed", ch)
    print("  h_ordered", h_ordered, "h_nl", h_ordered_nl, "h_sorted", h_sorted)
    print("  projected_text_sha256", results[pname]['text_sha'])
json.dump(results, open('derive311.json','w'), indent=1, ensure_ascii=False)
