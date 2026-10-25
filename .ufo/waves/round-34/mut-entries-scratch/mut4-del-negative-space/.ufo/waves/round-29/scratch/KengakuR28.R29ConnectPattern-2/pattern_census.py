"""Read-only occurrence/profile-independent census of pinned r28 raw text.
Does not import/execute upstream code; no production projection used."""
import json, hashlib, collections, sys
RAW = 'plans/fixtures/r28/webarena/config_files/test.raw.json'
TOKENS = ['__GITLAB__','__REDDIT__','__SHOPPING_ADMIN__','__SHOPPING__','__WIKIPEDIA__','__MAP__']
b = open(RAW,'rb').read()
text = b.decode('utf-8')
data = json.loads(text)
assert hashlib.sha256(b).hexdigest() == '7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652'

def leaves(node, path):
    if isinstance(node, dict):
        for k,v in node.items(): yield from leaves(v, path+[('key',k)])
    elif isinstance(node, list):
        for i,v in enumerate(node): yield from leaves(v, path+[('idx',i)])
    elif isinstance(node, str):
        yield path, node

def jp(path):
    out='$'
    for kind,v in path:
        out += f'[{v}]' if kind=='idx' else ('.'+v if v.isidentifier() else f'[{v!r}]')
    return out

occ_by_field = collections.Counter()   # normalized prefix to first eval subkey
occ_by_token_field = collections.Counter()
per_task_occ = collections.Counter()
leaves_with_occ = 0
multi_occ_leaves = []
occ_in_keys = 0
field_class = collections.Counter()
urlmatch_occ = nonurl_occ = 0
field_census = collections.Counter()
for pos,task in enumerate(data):
    ets = task['eval']['eval_types']
    um = 'url_match' in ets
    for path,val in leaves(task, []):
        cnt = sum(val.count(t) for t in TOKENS)
        if not cnt: continue
        leaves_with_occ += 1
        per_task_occ[pos] += cnt
        if um: urlmatch_occ += cnt
        else: nonurl_occ += cnt
        if cnt > 1: multi_occ_leaves.append((pos, jp(path), cnt))
        # classify owning field: first two path components after task
        parts = [v for k,v in path]
        if len(parts)>1 and parts[0]=='eval':
            cat = 'eval.'+parts[1]
            if parts[1]=='program_html':
                cat = 'eval.program_html.'+('.'.join(str(p) for p in parts[2:4]) or '?')
        else:
            cat = parts[0] if parts else '$'
        field_census[cat] += cnt
        for t in TOKENS:
            c = val.count(t)
            if c: occ_by_token_field[(t,cat)] += c
# keys containing tokens?
def keys_with_tokens(node, path=()):
    if isinstance(node, dict):
        for k,v in node.items():
            yield path+(k,), k
            yield from keys_with_tokens(v, path+(k,))
    elif isinstance(node, list):
        for i,v in enumerate(node): yield from keys_with_tokens(v, path+(i,))
occ_in_keys = sum(1 for p,k in keys_with_tokens(data) if any(t in k for t in TOKENS))
print('leaf_strings_with_occurrences', leaves_with_occ)
print('total_occurrences_in_decoded_leaves', sum(per_task_occ.values()), 'serialized_text_occurrences', sum(text.count(t) for t in TOKENS))
print('urlmatch_task_occurrences', urlmatch_occ, 'nonurlmatch_task_occurrences', nonurl_occ)
print('tasks_with_occurrences', len(per_task_occ), 'max_occ_per_task', max(per_task_occ.values()))
print('leaves_with_multiple_occurrences', len(multi_occ_leaves), multi_occ_leaves[:10])
print('token_in_object_keys', occ_in_keys)
print('field_census:')
for k,v in field_census.most_common(): print('  ',k,v)
print('per_token_field_nonzero:')
for (t,f),v in sorted(occ_by_token_field.items()): print('  ',t,f,v)
print('url_note explicit/defaulted', sum(1 for t in data if 'url_match' in t['eval']['eval_types'] and 'url_note' in t['eval']), sum(1 for t in data if 'url_match' in t['eval']['eval_types'] and 'url_note' not in t['eval']))
print('index_eq_taskid', all(t['task_id']==i for i,t in enumerate(data)))
# duplicate identical strings inside same task+field?
dup=0
for pos,task in enumerate(data):
    c=collections.Counter()
    for path,val in leaves(task, []):
        if any(t in val for t in TOKENS): c[jp(path)]+=1
    dup += sum(1 for v in c.values() if v>1)
print('same_jsonpath_duplicate_leaf_witnesses(target-population)', dup)
