# Read-only census; never imports/executes upstream code. Evaluator/helper logic below is a
# hand-transcription of evaluators.py:187-224 and helper_functions.py:98-113 applied to synthetic strings only.
import json, re, hashlib, collections, urllib.parse

ROOT = '/home/vgpnk/Projects/shokunin/kengaku-shokunin/'
raw_b = open(ROOT + 'plans/fixtures/r28/webarena/config_files/test.raw.json', 'rb').read()
prof_b = open(ROOT + 'plans/fixtures/r29/profiles.json', 'rb').read()
print('raw_sha', hashlib.sha256(raw_b).hexdigest())
print('prof_sha', hashlib.sha256(prof_b).hexdigest())
raw = raw_b.decode('utf-8')
profiles = json.loads(prof_b)
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

seg = collections.Counter(m.group(1) for m in re.finditer(r'__SHOPPING_ADMIN__/([^/"?\s]*)', raw))
print('SHOPPING_ADMIN first segment top', seg.most_common(8), 'total', sum(seg.values()), 'admin-seg', seg.get('admin', 0))
print('distinct purpose strings', len({p['purpose'] for p in profiles.values()}), 'of', len(profiles))


def proj(vals):
    t = raw
    for k in ORDER:
        t = t.replace(f"__{k}__", vals[k])
    return t


def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, path + ('[]',))
    elif isinstance(o, str):
        yield '.'.join(path), o


def clean_url(u):
    return str(u).rstrip('/')


def parse_url(u):
    p = urllib.parse.urlparse(u)
    return p.netloc + p.path, urllib.parse.parse_qs(p.query)


def url_match(ref_field, pred):
    refs = [clean_url(u) for u in ref_field.split(' |OR| ')]
    pb, _ = parse_url(clean_url(pred))
    return float(any(parse_url(r)[0] in pb for r in refs))


for name, p in profiles.items():
    t = proj(p['values'])
    data = json.loads(t)
    dbl = collections.Counter()
    tasks_dbl = set()
    for d in data:
        for path, s in walk(d, ()):
            n = len(re.findall(r'(?<!:)//', s))
            if n:
                dbl[path] += n
                tasks_dbl.add(d['task_id'])
    fail = tot = 0
    for d in data:
        ref = d['eval'].get('reference_url')
        if not ref:
            continue
        first = ref.split(' |OR| ')[0]
        sp = urllib.parse.urlsplit(first)
        pred = urllib.parse.urlunsplit(sp._replace(path=re.sub('/+', '/', sp.path)))
        tot += 1
        fail += url_match(ref, pred) == 0.0
    print(f'{name}: tasks={len(data)} codepoints={len(t)} nonscheme_double_slash={sum(dbl.values())} '
          f'tasks_with_double_slash={len(tasks_dbl)} by_field={dict(dbl)} '
          f'url_match_zero_vs_slash_collapsed_first_ref={fail}/{tot}')


def reddit_get_post_url(url):
    tok = urllib.parse.urlparse(url).path.split('/')
    if len(tok) < 4 or tok[1] != 'f':
        return 'UNCHANGED'
    return 'NORMALIZED'


for name, p in profiles.items():
    u = p['values']['REDDIT'] + '/f/space/134164/x/-/comment/1'
    print('reddit_get_post_url', name, repr(u), reddit_get_post_url(u))
print('raw tasks mentioning reddit_get_post_url', sum('reddit_get_post_url' in json.dumps(d) for d in json.loads(raw)))
