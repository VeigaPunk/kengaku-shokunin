import json, sys, collections, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import alt_classify as A
ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence')
idx = json.load(open(ROOT/'round53/tests-index.json'))['tests']
cache = {}
res = {}
missing = []
for t in idx:
    f = t['file']
    if f not in cache:
        src = (ROOT/'round52/graders'/f).read_text()
        cache[f] = A.classify_detail(src)
    key = (t['class']+'.' if t['class'] else '') + t['name']
    d = cache[f].get(key)
    if d is None:
        missing.append(t['id']); continue
    res[t['id']] = d
out = {'missing': missing, 'results': res}
json.dump(out, open('alt_results.json','w'), indent=1, sort_keys=True)
print('n', len(res), 'missing', missing)
print(collections.Counter(d['cls'] for d in res.values()))
print(collections.Counter(d['why'].split(':')[0] if d['why'].startswith('effect') else d['why'] for d in res.values()))
fl = collections.Counter(f for d in res.values() for f in d['flags'])
print(fl)
print("P1:")
for k,d in res.items():
    if d['cls']=='P1': print(' ',k,d['asserts'],d['flags'])
