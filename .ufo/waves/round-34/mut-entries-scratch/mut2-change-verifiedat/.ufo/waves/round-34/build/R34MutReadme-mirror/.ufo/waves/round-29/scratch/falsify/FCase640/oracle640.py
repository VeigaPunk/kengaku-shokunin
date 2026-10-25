"""Independent oracle for raw task 640 under 3 frozen profiles.

Derived ONLY from:
  - prereg text plans/round-29-claims.md ("Frozen inputs and semantics", "Required output")
  - pinned generator bytes plans/fixtures/r29/generate_test_data.py
  - pinned data plans/fixtures/r28/webarena/config_files/test.raw.json
  - plans/fixtures/r29/profiles.json
Never reads or imports plans/config_projection.py.
"""
import json, hashlib, sys

ROOT = '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW = ROOT + '/plans/fixtures/r28/webarena/config_files/test.raw.json'
PROF = ROOT + '/plans/fixtures/r29/profiles.json'
ORDER = ['GITLAB', 'REDDIT', 'SHOPPING', 'SHOPPING_ADMIN', 'WIKIPEDIA', 'MAP']
IDX = 640

raw = open(RAW, 'r').read()                      # text mode, universal newlines
profiles = json.load(open(PROF))
raw_obj = json.loads(raw)

def esc(p):
    return p.replace('~', '~0').replace('/', '~1')

def leaves(node, path=''):
    if isinstance(node, dict):
        for k in node:
            yield from leaves(node[k], path + '/' + esc(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, path + '/' + str(i))
    else:
        yield path, node

URL_FIELDS = {'start_url', 'reference_url', 'url'}   # date-agnostic name-based rule

def category(path):
    # last unescaped segment's key name, item-relative
    segs = path.split('/')[1:]
    key = segs[-1]
    return 'url_field' if key in URL_FIELDS else 'non_url_field'

out = {'raw_sha256': hashlib.sha256(open(RAW, 'rb').read()).hexdigest(),
       'index_640_task_id': raw_obj[IDX].get('task_id'),
       'raw_item_sha256_dumps': hashlib.sha256(json.dumps(raw_obj[IDX], indent=2).encode()).hexdigest(),
       'profiles': {}}

# raw text span check: token occurrences attributable to item 640
raw_leaf = dict(leaves(raw_obj[IDX]))

for pname in ['distinct_origins', 'path_prefix', 'trailing_slash_sensitivity']:
    vals = profiles[pname]['values']
    text = raw
    applied = {}
    for tok in ORDER:
        n = text.count('__%s__' % tok)
        applied[tok] = n
        text = text.replace('__%s__' % tok, vals[tok])
    proj = json.loads(text)                     # must parse in one piece
    pobj = proj[IDX]
    proj_leaf = dict(leaves(pobj))
    changed = []
    for path, oval in raw_leaf.items():
        nval = proj_leaf.get(path, '<MISSING>')
        if oval != nval or not isinstance(oval, str):
            if oval != nval:
                toks = [t for t in ORDER if ('__%s__' % t) in str(oval)]
                occ = sum(str(oval).count('__%s__' % t) for t in ORDER)
                changed.append({
                    'json_pointer_item_relative': path,
                    'json_pointer_array_absolute': '/%d%s' % (IDX, path),
                    'category_oracle': category(path),
                    'original': oval, 'projected': nval,
                    'tokens': toks, 'token_occurrences_in_leaf': occ,
                })
    # leaves present only after projection (structural change)?
    only_proj = sorted(set(proj_leaf) - set(raw_leaf))
    file_bytes = json.dumps(pobj, indent=2).encode('utf-8')
    out['profiles'][pname] = {
        'applied_replacements': applied,
        'parsed_task_count': len(proj),
        'projected_text_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
        'projected_task': pobj,
        'projected_task_dumps_sha256': hashlib.sha256(json.dumps(pobj, indent=2).encode()).hexdigest(),
        'would_be_file_sha256': hashlib.sha256(file_bytes).hexdigest(),
        'would_be_file_byte_len': len(file_bytes),
        'changed_leaves': changed,
        'changed_leaf_count': len(changed),
        'leaves_only_in_projection': only_proj,
        'multi_occurrence_leaves': [c for c in changed if c['token_occurrences_in_leaf'] > 1],
        'non_url_changes': [c for c in changed if c['category_oracle'] == 'non_url_field'],
        'remaining_tokens_in_projected_item_text': {t: json.dumps(pobj).count('__%s__' % t) for t in ORDER},
    }

json.dump(out, open(ROOT + '/.ufo/waves/round-29/scratch/falsify/FCase640/oracle640.json', 'w'),
          indent=1, sort_keys=True)
print(json.dumps({p: {k: v for k, v in d.items() if k != 'projected_task'} for p, d in out['profiles'].items()},
                 indent=1, sort_keys=True))
print('raw_sha256', out['raw_sha256'])
print('index640 task_id', out['index_640_task_id'])
