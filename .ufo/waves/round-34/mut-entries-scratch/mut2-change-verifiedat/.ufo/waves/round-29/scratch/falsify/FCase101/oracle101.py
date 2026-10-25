import json, hashlib, sys

LANE = '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW = LANE + '/plans/fixtures/r28/webarena/config_files/test.raw.json'
PROF = LANE + '/plans/fixtures/r29/profiles.json'
ORDER = ["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
IDX = int(sys.argv[1]) if len(sys.argv) > 1 else 101

raw_bytes = open(RAW,'rb').read()
raw_text = raw_bytes.decode('utf-8')
print('raw_sha256', hashlib.sha256(raw_bytes).hexdigest(), file=sys.stderr)
print('raw codepoints', len(raw_text), 'bytes', len(raw_bytes), file=sys.stderr)
print('raw tail', repr(raw_text[-40:]), file=sys.stderr)

# independent JSON decode only (no execution of upstream code)
raw_items = json.loads(raw_text)
profiles = json.load(open(PROF))
tok_fields = {t: [] for t in ORDER}

def leaves(obj, ptr=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, ptr+'/'+k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, ptr+'/'+str(i))
    elif isinstance(obj, str):
        yield ptr, obj

def occ(s, tok):
    n=0; out=[]
    i=s.find(tok)
    while i != -1:
        out.append(i); n+=1; i=s.find(tok, i+1)
    return out

result = {}
for pname in ["distinct_origins","path_prefix","trailing_slash_sensitivity"]:
    values = profiles[pname]['values']
    text = raw_text
    per_token_counts = {}
    for t in ORDER:
        c = text.count('__%s__' % t)
        per_token_counts['__%s__' % t] = c
        text = text.replace('__%s__' % t, values[t])
    proj_sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
    items = json.loads(text)
    orig_item = raw_items[IDX]; proj_item = items[IDX]
    changed = []
    for ptr, oval in leaves(orig_item):
        # find corresponding projected leaf
        cur = proj_item
        parts = ptr.split('/')[1:]
        for p in parts:
            cur = cur[int(p)] if isinstance(cur, list) else cur[p]
        if not isinstance(cur, str):
            print('TYPE DRIFT at', ptr, type(cur), file=sys.stderr); continue
        if cur != oval:
            toks = []
            for t in ORDER:
                tok='__%s__'%t
                if tok in oval:
                    toks.extend([tok]*oval.count(tok))
            changed.append({
                'json_pointer': '/%d%s' % (IDX, ptr),
                'path_template': ptr,
                'original': oval,
                'projected': cur,
                'tokens': toks,
                'category': 'url_field' if oval.strip().lower().startswith(('http://','https://')) or ptr.endswith('start_url') or ptr.endswith('reference_url') else 'other_string_field',
            })
    # generator per-task file: json.dump(item, f, indent=2) -> ensure_ascii default True, no newline
    per_task = json.dumps(proj_item, indent=2)  # matches json.dump defaults
    per_task_nl = per_task + '\n'
    result[pname] = dict(
        per_token_counts=per_token_counts,
        projected_text_sha256=proj_sha,
        parsed_count=len(items),
        changed=changed,
        file_sha256=hashlib.sha256(per_task.encode()).hexdigest(),
        file_sha256_nl=hashlib.sha256(per_task_nl.encode()).hexdigest(),
        projected_task=proj_item,
        filename='config_files/%d.json' % IDX,
        index_equals_task_id=(len(items[IDX]['task_id'].__str__())>0 and items[IDX]['task_id']==IDX)
    )
print(json.dumps(result, indent=1, sort_keys=True))
