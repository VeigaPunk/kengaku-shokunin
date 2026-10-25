# Verifies each report quote occurs verbatim on the cited line; counts whitespace-split words.
import json, re, subprocess, urllib.parse

L = '/home/vgpnk/Projects/shokunin/kengaku-shokunin/'
Q = [
    ('plans/round-29-claims.md', 13, 'neutral substitution profiles (2436 task/profile projections)'),
    ('plans/round-29-claims.md', 31, 'own-work profiles.json: distinct origins, path-prefix sensitivity, trailing-slash sensitivity.'),
    ('plans/round-29-claims.md', 40, 'P2/P3 sensitivity profiles are not deployment recommendations or model errors.'),
    ('plans/round-29-claims.md', 53, 'Exit0 = audit completed with expected structural identities; exit1 ='),
    ('plans/round-29-claims.md', 54, 'projection/invariant finding'),
    ('plans/round-29-claims.md', 45, 'No URL normalization, escaping repair or URL-only substitution'),
    ('plans/fixtures/r29/profiles.json', 3, 'controlled synthetic text-substitution profile, not an observed deployment'),
    ('.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md', 87, 'export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"'),
    ('.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md', 89, 'export GITLAB="<your_gitlab_domain>:8023"'),
    ('plans/fixtures/r28/webarena/evaluation_harness/evaluators.py', 189, 'url = url.rstrip("/")'),
    ('plans/fixtures/r28/webarena/evaluation_harness/evaluators.py', 195, 'base_path = parsed_url.netloc + parsed_url.path'),
    ('plans/fixtures/r28/webarena/evaluation_harness/evaluators.py', 223, 'ref_base_path in pred_base_paths'),
    ('plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py', 106, 'if tok_url[1] != "f":'),
    ('plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py', 58, 'order_url = f"{SHOPPING}/sales/order/view/order_id/{order_id}/"'),
]
for f, n, q in Q:
    line = open(L + f, encoding='utf-8').read().split('\n')[n - 1]
    print(f'{"OK " if q in line else "BAD"} {f}:{n} words={len(q.split())} {q!r}')

claims = open(L + 'plans/round-29-claims.md', encoding='utf-8').read()
print('claims "neutral" occurrences', len(re.findall(r'neutral', claims)), 'lines',
      [i + 1 for i, l in enumerate(claims.split('\n')) if 'neutral' in l])
print('claims "sensitivity" occurrences', len(re.findall(r'sensitivity', claims)))
msg = subprocess.run(['git', '-C', L, 'log', '-1', '--format=%s', '31934e5660f1814326c6472eefdfa0c41e642a2f'],
                     capture_output=True, text=True).stdout.strip()
print('prereg commit subject', repr(msg), 'words', len(msg.split()))
rd = open(L + '.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md', encoding='utf-8').read().split('\n')
ex = [l for l in rd[85:92] if l.startswith('export ')]
vals = [re.match(r'export \w+="([^"]*)"', l).group(1) for l in ex]
print('README export lines 86-92', len(ex), 'values ending "/"', sum(v.endswith('/') for v in vals),
      'values with path after port', sum(bool(re.search(r':\d+/', v)) for v in vals))

# Bounded witness: task 374 (url_match, SHOPPING_ADMIN) and task 27-like REDDIT |OR| under each profile.
raw = open(L + 'plans/fixtures/r28/webarena/config_files/test.raw.json', encoding='utf-8').read()
prof = json.load(open(L + 'plans/fixtures/r29/profiles.json'))
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def url_match(ref_field, pred):
    c = lambda u: str(u).rstrip('/')
    bp = lambda u: (lambda p: p.netloc + p.path)(urllib.parse.urlparse(u))
    return float(any(bp(c(r)) in bp(c(pred)) for r in ref_field.split(' |OR| ')))


for name, p in prof.items():
    t = raw
    for k in ORDER:
        t = t.replace(f"__{k}__", p['values'][k])
    data = {d['task_id']: d for d in json.loads(t)}
    for tid in (374, 464):
        d = data[tid]
        ref = d['eval'].get('reference_url') or ''
        ph = [x['url'] for x in d['eval'].get('program_html') or []]
        print(name, tid, 'start_url', d['start_url'], 'ref', ref, 'ph', ph)
    ref = data[374]['eval']['reference_url']
    sp = urllib.parse.urlsplit(ref)
    single = urllib.parse.urlunsplit(sp._replace(path=re.sub('/+', '/', sp.path)))
    print(name, '374 url_match(ref, ref)=', url_match(ref, ref), 'url_match(ref, single-slash pred', single, ')=',
          url_match(ref, single))
