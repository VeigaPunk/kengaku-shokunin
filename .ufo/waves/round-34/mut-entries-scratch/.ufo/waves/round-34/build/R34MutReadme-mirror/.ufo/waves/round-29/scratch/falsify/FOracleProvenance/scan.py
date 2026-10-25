#!/usr/bin/env python3
"""FOracleProvenance: independent occurrence-provenance oracle (seat KengakuR29-2.FOracleProvenance-2).

Contract source: prereg text (plans/round-29-claims.md), pinned generator bytes, pinned raw JSON.
This script NEVER reads or imports plans/config_projection.py source; it compares its own
structural scan against the instrument's captured --json stdout (data only) and --summary text.
"""
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict

ROOT = '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
RAW = ROOT + '/plans/fixtures/r28/webarena/config_files/test.raw.json'
GEN = ROOT + '/plans/fixtures/r29/generate_test_data.py'
SCRATCH = ROOT + '/.ufo/waves/round-29/scratch/falsify/FOracleProvenance'
INSTR_JSON = SCRATCH + '/instrumentjson'
INSTR_SUM = SCRATCH + '/instrumenttxt'
OUT = SCRATCH + '/oracle_findings.txt'

WS = ' \t\n\r'
LINES = []


def say(s=''):
    print(s)
    LINES.append(str(s))


def esc_ptr(seg):
    return seg.replace('~', '~0').replace('/', '~1')


# ---------------------------------------------------------------- token contract
gen_text = open(GEN, encoding='utf-8').read()
TOKENS = re.findall(r'raw\.replace\(\s*"((?:[^"\\]|\\.)*)"', gen_text)
say('== token contract (ordered raw.replace literals from pinned generator %s) ==' % GEN)
say('tokens_in_order=%r' % (TOKENS,))
assert len(TOKENS) == 6, 'expected six replacement tokens, got %d' % len(TOKENS)

# ---------------------------------------------------------------- raw text facts
raw_bytes = open(RAW, 'rb').read()
text = raw_bytes.decode('utf-8')  # strict decode; raises on invalid UTF-8
n = len(text)
nonascii = sum(1 for c in text if ord(c) > 127)
backslashes = text.count('\\')
say('== pinned raw facts ==')
say('bytes=%d codepoints=%d nonascii_codepoints=%d backslashes=%d' % (len(raw_bytes), n, nonascii, backslashes))
say('raw_sha256=%s' % hashlib.sha256(raw_bytes).hexdigest())

# stdlib sanity check only (validation, not structure mapping)
_ = json.loads(text)
say('stdlib_json_parses=yes')

# ---------------------------------------------------------------- my structural scanner
def scan_text(t):
    """Return (occurrences, strings_seen, dup_keys). occurrence dict:
    token, offset, pointer, role, task_index, template."""
    ln = len(t)
    occurrences = []
    stats = {'strings': 0, 'keys': 0, 'values': 0}
    dup_keys = []

    def skip_ws(i):
        while i < ln and t[i] in WS:
            i += 1
        return i

    def parse_string(i):
        # i at opening quote; returns (open_idx, close_idx+1)
        assert t[i] == '"'
        j = i + 1
        while j < ln:
            c = t[j]
            if c == '\\':
                j += 2
            elif c == '"':
                return i, j + 1
            else:
                j += 1
        raise ValueError('unterminated string at %d' % i)

    def templates_of(ptr, task_index):
        # pointer '/<task_idx>/a/b/0/c' -> two template renderings:
        #   dot style:    eval.program_html.[].url
        #   merged style: eval.program_html[].url
        parts = ptr.split('/')
        rel = parts[2:] if task_index is not None else parts[1:]
        dot = '.'.join('[]' if seg.isdigit() else seg for seg in rel)
        merged = []
        for seg in rel:
            if seg.isdigit() and merged:
                merged[-1] = merged[-1] + '[]'
            else:
                merged.append(seg)
        return dot, '.'.join(merged)

    def emit(tok, off, ptr, role, task_index):
        dot, merged = templates_of(ptr, task_index)
        occurrences.append({
            'token': tok,
            'offset': off,
            'pointer': ptr,
            'role': role,
            'task_index': task_index,
            'template': merged,
            'template_dot': dot,
        })

    def scan_string_for_tokens(s, e, ptr, role, task_index):
        cs, ce = s + 1, e - 1
        for tok in TOKENS:
            pos = cs
            while True:
                k = t.find(tok, pos, ce)
                if k < 0:
                    break
                emit(tok, k, ptr, role, task_index)
                pos = k + 1

    def parse_value(i, ptr, task_index):
        c = t[i]
        if c == '"':
            s, e = parse_string(i)
            stats['strings'] += 1
            stats['values'] += 1
            scan_string_for_tokens(s, e, ptr, 'value', task_index)
            return e
        if c == '{':
            i = skip_ws(i + 1)
            if i < ln and t[i] == '}':
                return i + 1
            seen = {}
            while True:
                i = skip_ws(i)
                ks, ke = parse_string(i)
                key = json.loads(t[ks:ke])
                stats['strings'] += 1
                stats['keys'] += 1
                if key in seen:
                    dup_keys.append((ptr, key, ks))
                seen[key] = ks
                # key-role token occurrences; pointer names the member the key defines
                scan_string_for_tokens(ks, ke, ptr + '/' + esc_ptr(key), 'key', task_index)
                i = skip_ws(ke)
                assert t[i] == ':', 'expected colon at %d' % i
                i = parse_value(skip_ws(i + 1), ptr + '/' + esc_ptr(key), task_index)
                i = skip_ws(i)
                if t[i] == ',':
                    i += 1
                    continue
                assert t[i] == '}', 'expected brace at %d' % i
                return i + 1
        if c == '[':
            i = skip_ws(i + 1)
            if i < ln and t[i] == ']':
                return i + 1
            idx = 0
            while True:
                i = skip_ws(i)
                child_task = idx if ptr == '' else task_index
                i = parse_value(i, ptr + '/' + str(idx), child_task)
                idx += 1
                i = skip_ws(i)
                if t[i] == ',':
                    i += 1
                    continue
                assert t[i] == ']', 'expected bracket at %d' % i
                return i + 1
        # number / true / false / null
        j = i
        while j < ln and t[j] not in ',]}':
            if t[j] in WS:
                break
            j += 1
        return j

    end = parse_value(skip_ws(0), '', None)
    end = skip_ws(end)
    assert end == ln, 'trailing content at %d' % end
    return occurrences, stats, dup_keys


occ, stats, dup_keys = scan_text(text)
say('== my scanner (own structural pass over full text) ==')
say('strings_seen=%d (keys=%d values=%d) duplicate_object_keys=%d' % (
    stats['strings'], stats['keys'], stats['values'], len(dup_keys)))

# flat census independent of structure (whole-text find loop, overlapping stepping)
flat = Counter()
flat_offsets = defaultdict(list)
for tok in TOKENS:
    pos = 0
    while True:
        k = text.find(tok, pos)
        if k < 0:
            break
        flat[tok] += 1
        flat_offsets[tok].append(k)
        pos = k + 1
mine = Counter(o['token'] for o in occ)
say('flat_census_by_token=%r' % ({tok: flat[tok] for tok in TOKENS},))
say('structural_by_token=%r' % ({tok: mine[tok] for tok in TOKENS},))
say('flat_vs_structural_equal=%s' % (all(flat[tok] == mine[tok] for tok in TOKENS),))
struct_off = {tok: sorted(o['offset'] for o in occ if o['token'] == tok) for tok in TOKENS}
say('flat_vs_structural_offsets_equal=%s' % (
    all(struct_off[tok] == sorted(flat_offsets[tok]) for tok in TOKENS),))
say('my_total_occurrences=%d' % len(occ))
say('my_roles=%r' % (dict(Counter(o['role'] for o in occ)),))
my_tasks = {tok: len({o['task_index'] for o in occ if o['token'] == tok}) for tok in TOKENS}
say('my_tasks_with_token=%r' % (my_tasks,))
my_templates = Counter(o['template'] for o in occ)
say('my_templates=%r' % (dict(sorted(my_templates.items())),))

# ---------------------------------------------------------------- codepoint vs byte probe
probe = '{"a":"é__MAP__","é__MAP__":"x"}'
pocc, _, _ = scan_text(probe)
probe_value = [o for o in pocc if o['role'] == 'value'][0]
probe_key = [o for o in pocc if o['role'] == 'key'][0]
say('== codepoint-vs-byte probe (my own synthetic UTF-8 fixture, not a pinned input) ==')
say('probe=%r' % probe)
say('probe_value_offset=%d (codepoint expectation 7; byte offset would be 8) -> cp_based=%s' % (
    probe_value['offset'], probe_value['offset'] == 7))
say('probe_key_offset=%d pointer=%r role=%s' % (probe_key['offset'], probe_key['pointer'], probe_key['role']))

# ---------------------------------------------------------------- instrument outputs
instr = json.load(open(INSTR_JSON, encoding='utf-8'))
say('== instrument captured outputs ==')
say('manifest_sha256_field=%s' % instr.get('manifest_sha256'))
say('raw_text_sha256_field=%s' % instr.get('raw_text_sha256'))
say('raw_text_sha256_matches_pinned_bytes=%s' % (instr.get('raw_text_sha256') == hashlib.sha256(raw_bytes).hexdigest(),))


def find_keys(node, name, path=''):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == name:
                yield path + '/' + k, v
            yield from find_keys(v, name, path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from find_keys(v, name, path + '/%d' % i)


pop_hits = list(find_keys(instr, 'population'))
say('population_paths=%r' % ([p for p, _ in pop_hits],))
pop = pop_hits[0][1] if pop_hits else {}
iot = pop.get('original_occurrences_by_token')
twt = pop.get('tasks_with_token')
roles = pop.get('occurrence_roles')
say('instrument_original_occurrences_by_token=%r' % (iot,))
say('instrument_tasks_with_token=%r' % (twt,))
say('instrument_occurrence_roles=%r' % (roles,))

sum_text = open(INSTR_SUM, encoding='utf-8').read()


def sum_line(name):
    m = re.search(r'^%s (\{.*\})$' % name, sum_text, re.M)
    return json.loads(m.group(1)) if m else None


s_iot, s_twt, s_roles = sum_line('ORIGINAL_OCCURRENCES_BY_TOKEN'), sum_line('TASKS_WITH_TOKEN'), sum_line('OCCURRENCE_ROLES')
say('summary_original_occurrences_by_token=%r' % (s_iot,))
say('summary_tasks_with_token=%r' % (s_twt,))
say('summary_occurrence_roles=%r' % (s_roles,))
say('json_vs_summary_population_agree=%s' % (
    iot == s_iot and twt == s_twt and roles == s_roles,))

# population field verification
iot_ok = iot == {tok: flat[tok] for tok in TOKENS}
twt_ok = twt == my_tasks
roles_ok = roles == dict(Counter(o['role'] for o in occ))
say('== population verification (mine vs instrument --json population) ==')
say('original_occurrences_by_token_match=%s' % iot_ok)
say('tasks_with_token_match=%s' % twt_ok)
say('occurrence_roles_match=%s' % roles_ok)

# path_template convention quantification (pre-normalization observation)
instr_op = instr.get('occurrence_provenance')
mine_by_pair = {}
for o in occ:
    mine_by_pair[(o['token'], o['offset'])] = o
merged_hits = sum(1 for r in instr_op
                  if mine_by_pair[(r['token'], r['original_input_codepoint_offset'])]['template'] == r['path_template'])
dot_hits = sum(1 for r in instr_op
               if mine_by_pair[(r['token'], r['original_input_codepoint_offset'])]['template_dot'] == r['path_template'])
other = len(instr_op) - merged_hits - dot_hits
say('== path_template convention ==')
say('instrument_matches_merged_bracket_style=%d/%d dot_style=%d other=%d' % (merged_hits, len(instr_op), dot_hits, other))

# leaf-level cross-census (occurrences vs distinct changed leaves; units kept distinct)
leaf_occ = defaultdict(list)
for o in occ:
    leaf_occ[o['pointer']].append(o)
leaf_templates = Counter(next(iter(v))['template'] for v in leaf_occ.values())
any_multi = [p for p, v in leaf_occ.items() if len(v) >= 2]
same_multi = [p for p, v in leaf_occ.items()
              if any(c >= 2 for c in Counter(x['token'] for x in v).values())]
say('== leaf census from provenance records (distinct task leaves, not occurrences) ==')
say('my_distinct_leaves_by_template=%r' % (dict(sorted(leaf_templates.items())),))
say('my_distinct_leaves_total=%d my_occurrences_total=%d' % (len(leaf_occ), len(occ)))
say('my_leaves_with_multiple_occurrences_any_token=%d same_token=%d' % (len(any_multi), len(same_multi)))
clt_hits = list(find_keys(instr, 'changed_leaves_by_path_template'))
clm_hits = list(find_keys(instr, 'changed_leaves_with_multiple_occurrences'))
if clt_hits:
    vals = {json.dumps(v, sort_keys=True) for _, v in clt_hits}
    say('instrument_changed_leaves_by_path_template(first_of_%d)=%r profiles_identical=%s' % (
        len(clt_hits), clt_hits[0][1], len(vals) == 1))
if clm_hits:
    vals = {v for _, v in clm_hits}
    say('instrument_changed_leaves_with_multiple_occurrences=%r profiles_identical=%s' % (
        sorted(vals), len(vals) == 1))

# ---------------------------------------------------------------- record comparison
instr_op = instr.get('occurrence_provenance')
say('== occurrence_provenance comparison ==')
say('instrument_record_count=%d my_record_count=%d' % (len(instr_op), len(occ)))


def norm_inst(r):
    return (r['token'], r['original_input_codepoint_offset'], r['json_pointer'],
            r['string_role'], r['task_index'], r['path_template'])


def norm_mine(o):
    return (o['token'], o['offset'], o['pointer'],
            o['role'], o['task_index'], o['template'])


inst_ms = Counter(norm_inst(r) for r in instr_op)
mine_ms = Counter(norm_mine(o) for o in occ)
only_inst = inst_ms - mine_ms
only_mine = mine_ms - inst_ms
say('multiset_exact_match=%s' % (not only_inst and not only_mine,))
say('records_only_in_instrument=%d records_only_in_mine=%d' % (sum(only_inst.values()), sum(only_mine.values())))

mismatches = []
inst_by_pos = defaultdict(list)
for r in inst_ms.elements():
    inst_by_pos[(r[0], r[1])].append(r)
mine_by_pos = defaultdict(list)
for r in mine_ms.elements():
    mine_by_pos[(r[0], r[1])].append(r)
for pos in sorted(set(inst_by_pos) | set(mine_by_pos), key=lambda p: (p[0], p[1])):
    a, b = inst_by_pos.get(pos, []), mine_by_pos.get(pos, [])
    if a and b:
        if a == b:
            continue
        for x, y in zip(a, b):
            for fi, fname in enumerate(('token', 'offset', 'json_pointer', 'string_role', 'task_index', 'path_template')):
                if x[fi] != y[fi]:
                    mismatches.append('FIELD token=%r offset=%d field=%s instrument=%r mine=%r' % (pos[0], pos[1], fname, x[fi], y[fi]))
        if len(a) != len(b):
            mismatches.append('COUNT token=%r offset=%d instrument=%d mine=%d' % (pos[0], pos[1], len(a), len(b)))
    elif a:
        for x in a:
            mismatches.append('ONLY_INSTRUMENT %r' % (x,))
    else:
        for y in b:
            mismatches.append('ONLY_MINE %r' % (y,))

say('field_or_membership_mismatches=%d' % len(mismatches))
for m in mismatches[:80]:
    say(m)
if len(mismatches) > 80:
    say('... %d more mismatch lines written to %s' % (len(mismatches) - 80, OUT))

# codepoint semantics check on every instrument record
bad_off = []
for r in instr_op:
    off, tok = r['original_input_codepoint_offset'], r['token']
    if not (isinstance(off, int) and 0 <= off <= n - len(tok) and text[off:off + len(tok)] == tok):
        bad_off.append((tok, off, r['json_pointer']))
say('instrument_offsets_not_landing_on_token_in_codepoint_space=%d' % len(bad_off))
for b in bad_off[:20]:
    say('BAD_OFFSET %r' % (b,))
say('note: pinned raw is pure ASCII (%d nonascii codepoints), so byte and codepoint offsets coincide '
    'numerically on this input; the cp-vs-byte distinction is exercised on my synthetic probe above '
    'and the instrument labels offsets as codepoints in its LIMIT lines.' % nonascii)

ok = (not mismatches and not bad_off and iot_ok and twt_ok and roles_ok
      and not only_inst and not only_mine and all(flat[tok] == mine[tok] for tok in TOKENS))
say('ORACLE_RESULT=%s' % ('AGREE' if ok else 'MISMATCH'))
open(OUT, 'w').write('\n'.join(LINES) + '\n')
say('written=%s' % OUT)
sys.exit(0 if ok else 3)
