"""Scratch text-level consistency check for the connector census.
Uses only pinned bytes + own profile values; does NOT import/execute upstream
generate_test_data.py, and is NOT the round's independent oracle."""
import json
TEXT = open('plans/fixtures/r28/webarena/config_files/test.raw.json', encoding='utf-8').read()
PROFILES = json.load(open('plans/fixtures/r29/profiles.json'))
ORDER = ['GITLAB', 'REDDIT', 'SHOPPING', 'SHOPPING_ADMIN', 'WIKIPEDIA', 'MAP']
TOKENS = ['__GITLAB__', '__REDDIT__', '__SHOPPING_ADMIN__', '__SHOPPING__', '__WIKIPEDIA__', '__MAP__']

def leaves(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, path + [k])
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, path + [i])
    elif isinstance(node, str):
        yield path, node

def at(root, path):
    for seg in path:
        root = root[seg]
    return root

original = json.loads(TEXT)
for name, profile in PROFILES.items():
    projected = TEXT
    for key in ORDER:
        projected = projected.replace('__' + key + '__', profile['values'][key])
    parsed = json.loads(projected)
    changed = sum(1 for a, b in zip(original, parsed) for path, value in leaves(a, []) if at(b, path) != value)
    residual = sum(projected.count(token) for token in TOKENS)
    print(name, 'tasks', len(parsed), 'changed_leaves', changed,
          'len_delta', len(projected) - len(TEXT), 'residual', residual)
