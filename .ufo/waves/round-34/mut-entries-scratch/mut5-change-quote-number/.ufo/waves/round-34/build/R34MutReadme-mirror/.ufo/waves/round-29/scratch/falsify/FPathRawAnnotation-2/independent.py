"""Independent re-derivation for FPathRawAnnotation: text-contract projection only.
Does not read or import plans/config_projection.py."""
import json, hashlib, sys, re

ROOT = '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW = ROOT + '/plans/fixtures/r28/webarena/config_files/test.raw.json'
PROF = ROOT + '/plans/fixtures/r29/profiles.json'
ORDER = ['GITLAB', 'REDDIT', 'SHOPPING', 'SHOPPING_ADMIN', 'WIKIPEDIA', 'MAP']
TOKENS = ['__' + k + '__' for k in ORDER]

def load():
    raw_bytes = open(RAW, 'rb').read()
    assert hashlib.sha256(raw_bytes).hexdigest() == '7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652'
    raw = raw_bytes.decode('utf-8')
    profiles = json.load(open(PROF))
    return raw, profiles

def project_text(raw, values):
    out = raw
    for key in ORDER:
        out = out.replace('__' + key + '__', values[key])
    return out

def leaves(obj, prefix=''):
    """Yield (json_pointer, path_template, value) for every string leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = prefix + '/' + k
            t = prefix + '.' + k if prefix else k
            yield from leaves(v, p) if not isinstance(v, str) else ((p, t, v),)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = prefix + '/' + str(i)
            t = prefix + '[]'
            yield from leaves(v, p) if not isinstance(v, str) else ((p, t, v),)

def all_leaves(obj):
    res = []
    root_list = isinstance(obj, list)
    def walk(o, p, t, parent_key, depth):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + '/' + k, (t + '.' + k if t else k), k, depth + 1)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                # the root task array is not part of the path template
                walk(v, p + '/' + str(i), t if (depth == 0 and root_list) else t + '[]', parent_key, depth + 1)
        elif isinstance(o, str):
            res.append((p, t, o, parent_key))
    walk(obj, '', '', None, 0)
    return res

def category(path_template):
    return 'url_field' if path_template in ('start_url', 'eval.reference_url', 'eval.program_html[].url') else 'non_url_field'

def main():
    raw, profiles = load()
    orig = json.loads(raw)
    base_leaves = all_leaves(orig)
    print('BASE_STRING_LEAVES', len(base_leaves))
    annotation_leaves = [x for x in base_leaves if x[1] == 'eval.reference_answer_raw_annotation']
    print('ANNOTATION_LEAVES', len(annotation_leaves))
    # duplicate json pointers? assert unique
    assert len({x[0] for x in base_leaves}) == len(base_leaves)
    tok_leaves = [x for x in annotation_leaves if any(tk in x[2] for tk in TOKENS)]
    print('ANNOTATION_TOKEN_LEAVES', len(tok_leaves))
    for p, t, v, _ in tok_leaves:
        print('TOKLEAF', p, {tk: v.count(tk) for tk in TOKENS if tk in v})
    # tasks lacking the key
    absent = [i for i, t in enumerate(orig) if not isinstance(t.get('eval'), dict) or 'reference_answer_raw_annotation' not in t['eval']]
    print('TASKS_WITHOUT_ANNOTATION_LEAF', len(absent), 'first', absent[:5])
    # occurrence offsets at this path, independent scan of raw text is global; verify pointer slice offsets by json encoder reconstruction
    # verify instrument provenance offsets by slicing raw
    instr = json.load(open(ROOT + '/.ufo/waves/round-29/scratch/falsify/FPathRawAnnotation-2/proj.json'))
    prov = [o for o in instr['occurrence_provenance'] if o['path_template'] == 'eval.reference_answer_raw_annotation']
    print('PROV_COUNT', len(prov))
    for o in prov:
        off = o['original_input_codepoint_offset']
        print('PROV_SLICE', off, repr(raw[off:off + len(o['token'])]), 'token', o['token'], 'match', raw[off:off + len(o['token'])] == o['token'], 'ptr', o['json_pointer'])
    # verify no annotation token occurrence in raw outside these slices
    all_offsets = []
    start = 0
    while True:
        i = raw.find('__REDDIT__', start)
        if i < 0:
            break
        all_offsets.append(i); start = i + 1
    print('RAW_REDDIT_OFFSETS_TOTAL', len(all_offsets))
    print('EXPECTED_ANNOTATION_OFFSETS', [o['original_input_codepoint_offset'] for o in prov])
    print('ANNOT_IN_OFFSET_LIST', all(o['original_input_codepoint_offset'] in all_offsets for o in prov))
    # position relative to annotation value start: count tokens in raw prefix inside task 66 string
    # full independent projection per profile
    summary = {}
    mism = []
    for name, spec in profiles.items():
        vals = spec['values']
        text = project_text(raw, vals)
        print('PROFILE', name, 'sha256', hashlib.sha256(text.encode('utf-8')).hexdigest())
        proj = json.loads(text)
        assert len(proj) == 812
        pleaves = all_leaves(proj)
        assert len(pleaves) == len(base_leaves)
        assert [x[0] for x in pleaves] == [x[0] for x in base_leaves]
        changed = []
        for (po, pt, vo, _), (pp, ppt, vp, _) in zip(base_leaves, pleaves):
            if vo != vp:
                changed.append((po, pt, vo, vp))
        by_t = {}
        by_c = {'url_field': 0, 'non_url_field': 0}
        ann = []
        for po, pt, vo, vp in changed:
            by_t[pt] = by_t.get(pt, 0) + 1
            by_c[category(pt)] += 1
            if pt == 'eval.reference_answer_raw_annotation':
                ann.append((po, category(pt), vo, vp))
        summary[name] = (len(changed), by_t, by_c, ann)
        print(' INDEP changed_leaf_count', len(changed))
        print(' INDEP by_template', dict(sorted(by_t.items())))
        print(' INDEP by_category', by_c)
        print(' INDEP annotation_changed', len(ann), ann)
        # compare with instrument aggregates
        ip = instr['profiles'][name]
        if ip['changed_leaf_count'] != len(changed):
            mism.append((name, 'changed_leaf_count', ip['changed_leaf_count'], len(changed)))
        if ip['changed_leaves_by_path_template'] != by_t:
            mism.append((name, 'by_template', ip['changed_leaves_by_path_template'], by_t))
        if ip['changed_leaves_by_category'] != by_c:
            mism.append((name, 'by_category', ip['changed_leaves_by_category'], by_c))
        # compare every changed leaf in instrument per-task lists against own walk
        own = {(po, pt): (vo, vp) for po, pt, vo, vp in changed}
        inst = {}
        for task in ip['tasks']:
            for lf in task['changed_leaves']:
                key = (lf['json_pointer'], lf['path_template'])
                if key in inst:
                    mism.append((name, 'dup instrument leaf', key))
                inst[key] = (lf['original'], lf['projected'], lf['category'], tuple(lf['tokens']))
        if set(own) != set(inst):
            mism.append((name, 'leaf key set diff', sorted(set(inst) - set(own))[:5], sorted(set(own) - set(inst))[:5]))
        for key, (vo, vp) in own.items():
            if key in inst:
                io, ipj, icat, itok = inst[key]
                if (io, ipj) != (vo, vp):
                    mism.append((name, 'value diff', key, (io, ipj), (vo, vp)))
                if icat != category(key[1]):
                    mism.append((name, 'category diff', key, icat, category(key[1])))
                expect_tokens = tuple(tk for tk in TOKENS if tk in vo)
                if itok != expect_tokens:
                    mism.append((name, 'tokens diff', key, itok, expect_tokens))
        # task 66 full changed leaf set
        t66 = ip['tasks'][66]
        print(' INDEP task66 changed keys', [k for k in own if k[0].startswith('/66/')])
        print(' INSTR task66 changed', [(lf['json_pointer'], lf['path_template'], lf['category']) for lf in t66['changed_leaves']])
        # verify instrument projected annotation exact
        instr_ann = t66['projected_task']['eval']['reference_answer_raw_annotation']
        own_ann = proj[66]['eval']['reference_answer_raw_annotation']
        if instr_ann != own_ann:
            mism.append((name, 'task66 annotation projected diff', instr_ann, own_ann))
        # structure/key identity
        if list(proj[66]['eval'].keys()) != list(orig[66]['eval'].keys()):
            mism.append((name, 'task66 eval key order diff', None, None))
        # global aggregate consistency
        print(' INDEP total occurrences at annotation path', sum(vo.count(tk) for _, _, vo, _ in ann for tk in TOKENS if tk in vo) if ann else 0)
    print('MISMATCHES', len(mism))
    for m in mism:
        print('MISM', m)
    # text-hash comparison against instrument
    for name in profiles:
        it = instr['profiles'][name]['projected_text_sha256']
        own = hashlib.sha256(project_text(raw, profiles[name]['values']).encode('utf-8')).hexdigest()
        print('TEXTHASH', name, 'instrument', it, 'own', own, 'match', it == own)
    # instrument annotation aggregate equality with independent across profiles
    for name in profiles:
        it = instr['profiles'][name]['changed_leaves_by_path_template'].get('eval.reference_answer_raw_annotation')
        print('ANNOT_AGG', name, 'instrument', it, 'independent', summary[name][1].get('eval.reference_answer_raw_annotation'))
    # instrument task 66 output index mapping and unchanged annotation leaves census sample
    ip = instr['profiles']['distinct_origins']
    print('TASK66 OUTPUT', ip['tasks'][66]['output_index'], ip['tasks'][66]['output_filename'], ip['tasks'][66]['index_equals_task_id'])
    # sample 5 raw annotation leaves with their status (first 5 by task index, including empty)
    for p, t, v, _ in annotation_leaves[:5]:
        print('SAMPLE_LEAF', p, repr(v)[:90])

main()
