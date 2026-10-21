import json, hashlib
S = '/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FCase640/'
inst = json.load(open(S + 'instrument.json'))
orc = json.load(open(S + 'oracle640.json'))
ORDER = ['__GITLAB__', '__REDDIT__', '__SHOPPING__', '__SHOPPING_ADMIN__', '__WIKIPEDIA__', '__MAP__']
IDX = 640
problems = []
report = {}

for pname in ['distinct_origins', 'path_prefix', 'trailing_slash_sensitivity']:
    rec = inst['profiles'][pname]['tasks'][IDX]
    o = orc['profiles'][pname]
    checks = {}
    checks['task_id'] = (rec['task_id'], o['projected_task']['task_id'])
    checks['output_index'] = (rec['output_index'], IDX)
    checks['output_filename'] = (rec['output_filename'], 'config_files/%d.json' % IDX)
    checks['index_equals_task_id'] = (rec['index_equals_task_id'], True)
    checks['would_be_file_sha256'] = (rec['would_be_file_sha256'], o['would_be_file_sha256'])
    checks['projected_task_exact'] = (rec['projected_task'] == o['projected_task'],
                                     'rec==oracle' if rec['projected_task'] == o['projected_task'] else 'DIFF')
    # changed leaves normalized
    def norm(leaves, oracle=False):
        out = []
        for l in leaves:
            p = l.get('json_pointer') or l.get('json_pointer_array_absolute')
            toks = l['tokens']
            toks = [t if t.startswith('__') else '__%s__' % t for t in toks]
            out.append((p, l.get('category') or l.get('category_oracle'), tuple(sorted(toks)),
                        l['original'], l['projected']))
        return sorted(out)
    a, b = norm(rec['changed_leaves']), norm(o['changed_leaves'], True)
    checks['changed_leaves_set_equal'] = (a == b, 'rec=%d oracle=%d' % (len(a), len(b)))
    checks['changed_leaves_order'] = ([l['json_pointer'] for l in rec['changed_leaves']],
                                      [l['json_pointer_array_absolute'] for l in o['changed_leaves']])
    checks['path_template'] = [l.get('path_template') for l in rec['changed_leaves']]
    checks['changed_leaf_count_profile'] = (len(rec['changed_leaves']), o['changed_leaf_count'])
    report[pname] = checks
    for k, v in checks.items():
        if k == 'projected_task_exact' and v[0] is False:
            problems.append((pname, k, v))
        if k in ('task_id', 'output_filename', 'index_equals_task_id', 'would_be_file_sha256',
                 'output_index', 'changed_leaf_count_profile') and v[0] != v[1]:
            problems.append((pname, k, v))
        if k == 'changed_leaves_set_equal' and v[0] is False:
            problems.append((pname, k, v))

# global cross-checks against the oracle's whole-text projections
print('== per-profile record 640 ==')
print(json.dumps(report, indent=1))
print('problems:', problems)

print('\n== global text digests ==')
for pname in ['distinct_origins', 'path_prefix', 'trailing_slash_sensitivity']:
    print(pname, 'instrument', inst['profiles'][pname]['projected_text_sha256'],
          'oracle', orc['profiles'][pname]['projected_text_sha256'],
          'EQUAL' if inst['profiles'][pname]['projected_text_sha256'] == orc['profiles'][pname]['projected_text_sha256'] else 'DIFF')

print('\n== top-level input digests / manifest ==')
print('manifest_sha256', inst.get('manifest_sha256'))
print('raw_text_sha256', inst.get('raw_text_sha256'), 'oracle file sha', orc['raw_sha256'])
print('inputs:', json.dumps(inst.get('inputs'), indent=1)[:1500])
print('index_mapping:', json.dumps(inst.get('index_mapping'), indent=1)[:600])
