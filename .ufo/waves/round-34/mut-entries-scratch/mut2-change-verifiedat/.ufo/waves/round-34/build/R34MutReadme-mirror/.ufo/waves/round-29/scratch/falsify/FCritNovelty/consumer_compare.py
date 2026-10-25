"""Own-work comparison of three published projection rules, re-typed from opened source text.
Never imports or executes upstream or lane production code. Synthetic *.invalid values only."""
import hashlib, json, random, re
RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
b = open(RAW, "rb").read()
assert hashlib.sha256(b).hexdigest() == "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
text = b.decode("utf-8")
ORDER = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
VAL = {t: "http://%s.fcritnovelty.invalid:1" % t.strip("_").lower().replace("_", "-") for t in ORDER}

def text_replace(s):
    for t in ORDER: s = s.replace(t, VAL[t])
    return s

def generator_rule(s):   # webarena generate_test_data.py:11-23 (filename = enumerate index)
    return {str(i): item for i, item in enumerate(json.loads(text_replace(s)))}

def browsergym_rule(s, task_id):   # BrowserGym webarena task.py:58-69,82 (select by task_id)
    return [c for c in json.loads(text_replace(s)) if c["task_id"] == task_id]

def walk(o):
    if isinstance(o, dict):
        return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v) for v in o]
    return o

def prefix_render(o):    # WebArena-Verified config.py:198-207 semantics: replace only when leaf startswith token
    if isinstance(o, dict): return {k: prefix_render(v) for k, v in o.items()}
    if isinstance(o, list): return [prefix_render(v) for v in o]
    if isinstance(o, str):
        for t in ORDER:
            if o.startswith(t): return o.replace(t, VAL[t])
    return o

gen = generator_rule(text)
same = sum(1 for k, v in gen.items() if browsergym_rule(text, v["task_id"]) == [v])
print("frozen order: generator objects equal to BrowserGym task_id selection", same, "of", len(gen))
print("frozen order: generator filename index == task_id", sum(1 for k, v in gen.items() if int(k) == v["task_id"]))

data = json.loads(text); rnd = random.Random(29); rnd.shuffle(data)
shuf = json.dumps(data, ensure_ascii=False, indent=2)
gs = generator_rule(shuf)
print("shuffled order (seed 29): generator index == task_id", sum(1 for k, v in gs.items() if int(k) == v["task_id"]),
      "; BrowserGym selection still equals frozen generator object", sum(1 for v in gen.values() if browsergym_rule(shuf, v["task_id"]) == [v]))

orig = json.loads(text); TOK = re.compile("|".join(ORDER))
def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, p + "." + k)
    elif isinstance(o, list):
        for v in o: yield from leaves(v, p + "[]")
    elif isinstance(o, str): yield p, o
tok_leaves = [(p, s) for t in orig for p, s in leaves(t) if TOK.search(s)]
nonprefix = [(p, s) for p, s in tok_leaves if not any(s.startswith(t) for t in ORDER)]
multi = [(p, s) for p, s in tok_leaves if len(TOK.findall(s)) > 1]
from collections import Counter
print("token-bearing leaves", len(tok_leaves), "; not starting with a token", len(nonprefix), dict(Counter(p for p, _ in nonprefix)))
print("token-bearing leaves with >1 occurrence", len(multi))
pr = [prefix_render(t) for t in orig]; gl = [gen[str(i)] for i in range(len(orig))]
remaining = sum(len(TOK.findall(s)) for t in pr for _, s in leaves(t))
print("hypothetical prefix-render over pinned raw: tasks differing from generator", sum(1 for a, c in zip(pr, gl) if a != c), "; token occurrences left", remaining)
