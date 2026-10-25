#!/usr/bin/env python3
"""Independent read-only census for the __MAP__ placeholder in the pinned r28 raw JSON.

Reads pinned bytes once, parses with an instrumented recursive-descent JSON reader,
and reports raw-serialized vs decoded-leaf occurrences, JSON paths, task ownership,
URL/non-URL context, and replacement span implications for the three frozen profiles.
No imports of plans/config_projection.py or browser_env.env_config; no writes outside
its own JSON/stdout output.
"""
import json, re, hashlib, sys
from collections import Counter, defaultdict
from json.decoder import scanstring

ROOT = '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW = ROOT + '/plans/fixtures/r28/webarena/config_files/test.raw.json'
PROFILES = ROOT + '/plans/fixtures/r29/profiles.json'
MANIFEST = ROOT + '/plans/fixtures/r29/manifest.json'
TOK = '__MAP__'
EXPECT = {
    RAW: '7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652',
    PROFILES: '90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018',
    MANIFEST: 'f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87',
}

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def read_pinned(path, expected):
    b = open(path, 'rb').read()
    got = sha256_bytes(b)
    if got != expected:
        raise SystemExit('snapshot_tampered %s got %s want %s' % (path, got, expected))
    return b

raw_b = read_pinned(RAW, EXPECT[RAW])
prof_b = read_pinned(PROFILES, EXPECT[PROFILES])
man_b = read_pinned(MANIFEST, EXPECT[MANIFEST])
raw = raw_b.decode('utf-8')
assert len(raw.encode('utf-8')) == len(raw_b)
profiles = json.loads(prof_b)

# ---- instrumented parser: records raw string spans + decoded values, keys and values ----
n = len(raw)
WS = ' \t\n\r'
records = []  # dict(kind, path_fields, raw_start, raw_end_excl, decoded)

def skip(i):
    while i < n and raw[i] in WS:
        i += 1
    return i

def parse(i, fields):
    i = skip(i)
    c = raw[i]
    if c == '{':
        i += 1; obj = {}
        i = skip(i)
        if raw[i] == '}':
            return obj, i + 1
        while True:
            i = skip(i)
            assert raw[i] == '"'
            q = i
            k, ni = scanstring(raw, i + 1, True)
            records.append(dict(kind='key', fields=fields + [('key', k)],
                                raw_start=q, raw_end=ni, decoded=k))
            i = skip(ni)
            assert raw[i] == ':'
            v, i = parse(i + 1, fields + [('key', k)])
            obj[k] = v
            i = skip(i)
            if raw[i] == '}':
                return obj, i + 1
            assert raw[i] == ','
            i += 1
    if c == '[':
        i += 1; arr = []; j = 0
        i = skip(i)
        if raw[i] == ']':
            return arr, i + 1
        while True:
            v, i = parse(i, fields + [('idx', j)])
            arr.append(v); j += 1
            i = skip(i)
            if raw[i] == ']':
                return arr, i + 1
            assert raw[i] == ','
            i += 1
    if c == '"':
        q = i
        v, ni = scanstring(raw, i + 1, True)
        records.append(dict(kind='value', fields=fields, raw_start=q, raw_end=ni, decoded=v))
        return v, ni
    if raw.startswith('true', i): return True, i + 4
    if raw.startswith('false', i): return False, i + 5
    if raw.startswith('null', i): return None, i + 4
    m = re.match(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?', raw[i:])
    assert m, (i, raw[i:i+20])
    return json.loads(m.group(0)), i + len(m.group(0))

parsed, end = parse(0, [])
assert not raw[end:].strip(), 'trailing non-whitespace'
assert parsed == json.loads(raw), 'instrumented parse mismatch'
data = parsed

# ---- raw literal occurrences ----
occ = []
start = 0
while True:
    i = raw.find(TOK, start)
    if i < 0:
        break
    occ.append(dict(
        cp_start=i,
        cp_end=i + len(TOK),
        byte_start=len(raw[:i].encode('utf-8')),
        byte_end=len(raw[:i + len(TOK)].encode('utf-8')),
        line=raw.count('\n', 0, i) + 1,
    ))
    start = i + 1
raw_literal = len(occ)

# ---- map every decoded occurrence back to its raw literal span ----
def unescape_map(s):
    """Return decoded string and raw offsets (relative to content start) per decoded char."""
    out = []; rmap = []
    i = 0
    while i < len(s):
        c = s[i]
        if c != '\\':
            out.append(c); rmap.append((i, i + 1)); i += 1
            continue
        e = s[i + 1]
        if e == 'u':
            cp = int(s[i + 2:i + 6], 16)
            out.append(chr(cp)); rmap.append((i, i + 6)); i += 6
        else:
            mapping = {'"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f',
                       'n': '\n', 'r': '\r', 't': '\t'}
            assert e in mapping, (e, s[i:i+8])
            out.append(mapping[e]); rmap.append((i, i + 2)); i += 2
    return ''.join(out), rmap

def format_path(fields):
    out = ''
    for kind, name in fields:
        if kind == 'idx':
            out += '[%d]' % name
        else:
            out += ('.' if out else '') + name
    return out

hits = []
for rec in records:
    val = rec['decoded']
    if TOK not in val:
        continue
    inner = raw[rec['raw_start'] + 1:rec['raw_end'] - 1]
    dec2, rmap = unescape_map(inner)
    assert dec2 == val, (format_path(rec['fields']), dec2[:80], val[:80])
    pos = 0
    while True:
        d = val.find(TOK, pos)
        if d < 0:
            break
        rs, re_ = rmap[d]
        re_ = rmap[d + len(TOK) - 1][1]
        raw_span = raw[rec['raw_start'] + 1 + rs: rec['raw_start'] + 1 + re_]
        hits.append(dict(
            kind=rec['kind'],
            fields=rec['fields'],
            path=format_path(rec['fields']),
            decoded_offset=d,
            raw_inner_span=[rs, re_],
            raw_literal_equal=(raw_span == TOK),
            raw_cp_start=rec['raw_start'] + 1 + rs,
            raw_cp_end=rec['raw_start'] + 1 + re_,
            leaf_value=val,
            leaf_cp_len=len(val),
        ))
        pos = d + 1

decoded_total = sum(r['decoded'].count(TOK) for r in records)
assert decoded_total == sum(r['leaf_value'].count(TOK) for r in hits)
assert all(h['raw_literal_equal'] for h in hits)
assert sorted(h['raw_cp_start'] for h in hits) == [o['cp_start'] for o in occ]
assert len({h['raw_cp_start'] for h in hits}) == raw_literal

# attach line + owning task
for h in hits:
    idx = h['fields'][0][1] if h['fields'] and h['fields'][0][0] == 'idx' else None
    h['task_index'] = idx
    h['task_id'] = data[idx]['task_id'] if idx is not None else None
    h['task_field'] = format_path(h['fields'][1:]) if idx is not None else h['path']
    h['line'] = raw.count('\n', 0, h['raw_cp_start']) + 1
    h['sites'] = data[idx]['sites'] if idx is not None else None

# ---- task/path distributions ----
by_field = Counter(h['task_field'] for h in hits)
by_task = defaultdict(list)
for h in hits:
    by_task[h['task_index']].append(h)
task_counts = Counter(len(v) for v in by_task.values())
task_ids = sorted(by_task)
id_eq_idx = all(data[i]['task_id'] == i for i in task_ids)
site_map_tasks = [i for i, t in enumerate(data) if 'map' in t.get('sites', [])]
site_map_with_tok = [i for i in site_map_tasks if i in by_task]
site_map_without_tok = [i for i in site_map_tasks if i not in by_task]
tok_tasks_not_site_map = [i for i in task_ids if i not in site_map_tasks]

# ---- non-URL classification ----
URL_FIELDS = {'start_url', 'eval.reference_url'}
nonurl = [h for h in hits if h['task_field'] not in URL_FIELDS]
# also check whether any token occurrence is embedded inside a larger non-URL prose value
prose = [h for h in hits if h['task_field'] in ('intent', 'intent_template', 'eval.string_note')]

# ---- profile replacement lengths and spans ----
def cp_len(s): return len(s)
def byte_len(s): return len(s.encode('utf-8'))
map_vals = {}
for pname, obj in profiles.items():
    map_vals[pname] = obj['values']['MAP']
assert all('__MAP__' not in v for v in map_vals.values())
# cascade input: any profile value (any token) containing __MAP__? exact-order relevance for MAP last
cascade_sources = {p: [k for k, v in obj['values'].items() if TOK in v]
                   for p, obj in profiles.items()}
proj = {}
for pname, val in map_vals.items():
    L = cp_len(val)
    d = L - len(TOK)
    proj[pname] = dict(
        replacement=val, replacement_cp_len=L, replacement_byte_len=byte_len(val),
        placeholder_cp_len=len(TOK), delta_cp=L - len(TOK), delta_bytes=byte_len(val) - byte_len(TOK),
        map_only_total_delta_cp=raw_literal * d,
        map_only_projected_raw_cp_len=len(raw) + raw_literal * d,
        map_only_projected_raw_byte_len=len(raw_b) + raw_literal * (byte_len(val) - len(TOK)),
        map_occurrence_count_after=raw.replace(TOK, val).count(TOK),
    )

# per occurrence raw / MAP-only projected spans
for h in hits:
    h['map_only_start'] = {p: h['raw_cp_start'] + i * (cp_len(v) - len(TOK))
                           for i, (p, v) in enumerate(map_vals.items())}
# NOTE: the dict above uses i over profiles, which is wrong; recompute correctly below.
for h in hits:
    h.pop('map_only_start', None)

for pname, val in map_vals.items():
    d = cp_len(val) - len(TOK)
    for j, h in enumerate(sorted(hits, key=lambda x: x['raw_cp_start'])):
        h.setdefault('map_only_projected', {})[pname] = [h['raw_cp_start'] + j * d,
                                                         h['raw_cp_end'] + j * d]

result = dict(
    token=TOK,
    artifacts={
        'raw_path': RAW, 'raw_sha256': sha256_bytes(raw_b),
        'profiles_path': PROFILES, 'profiles_sha256': sha256_bytes(prof_b),
        'manifest_path': MANIFEST, 'manifest_sha256': sha256_bytes(man_b),
        'raw_bytes': len(raw_b), 'raw_unicode_codepoints': len(raw),
        'raw_lines': raw.count('\n') + 1, 'raw_ascii_only': raw_b == raw.encode('utf-8') and all(b < 128 for b in raw_b),
        'items': len(data),
    },
    raw_literal_occurrences=raw_literal,
    decoded_string_occurrences=decoded_total,
    decoded_key_occurrences=sum(r['decoded'].count(TOK) for r in records if r['kind'] == 'key'),
    decoded_value_occurrences=sum(r['decoded'].count(TOK) for r in records if r['kind'] == 'value'),
    escaped_induced_occurrences=decoded_total - raw_literal,
    unicode_escape_sequences_in_raw=len(re.findall(r'\\u[0-9a-fA-F]{4}', raw)),
    escapes_inside_token=len(re.findall(r'\\u005[fF]', raw)) + len(re.findall(r'\\u(?:004d|0041|0050|006d|0061|0070)', raw)),
    occurrences_in_keys=sum(h['kind'] == 'key' for h in hits),
    occurrences_in_values=sum(h['kind'] == 'value' for h in hits),
    distinct_json_paths=len({h['path'] for h in hits}),
    distinct_owning_tasks=len(by_task),
    tasks_by_occurrence_count=dict(sorted(Counter(len(v) for v in by_task.values()).items())),
    task_ids=sorted({h['task_id'] for h in hits}),
    index_equals_task_id=id_eq_idx,
    field_counts=dict(sorted(by_field.items())),
    url_field_occurrences=sum(h['task_field'] in URL_FIELDS for h in hits),
    non_url_field_occurrences=len(nonurl),
    prose_field_occurrences=len(prose),
    leaf_shapes=dict(Counter(h['leaf_value'].replace(TOK, '<TOK>') for h in hits)),
    token_offset_in_leaf=dict(Counter(h['decoded_offset'] for h in hits)),
    site_map_tasks=len(site_map_tasks),
    owning_task_sites=dict(sorted(Counter('+'.join(data[i]['sites']) for i in task_ids).items())),
    site_map_tasks_with_token=len(site_map_with_tok),
    site_map_tasks_without_token=len(site_map_without_tok),
    token_tasks_without_site_map=len(tok_tasks_not_site_map),
    site_map_without_token_task_ids=[data[i]['task_id'] for i in site_map_without_tok],
    token_tasks_without_site_map_ids=[data[i]['task_id'] for i in tok_tasks_not_site_map],
    cascade_sources=cascade_sources,
    profiles=proj,
    occurrence_rows=sorted(hits, key=lambda x: x['raw_cp_start']),
)
json.dump(result, sys.stdout, indent=1, ensure_ascii=False)
