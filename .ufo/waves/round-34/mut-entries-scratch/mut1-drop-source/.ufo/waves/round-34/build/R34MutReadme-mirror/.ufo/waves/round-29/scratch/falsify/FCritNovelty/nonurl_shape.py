"""Own-work: value shape of token-bearing leaves on paths whose final key is not a URL key. Data only."""
import json, re, collections
RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
d = json.load(open(RAW, encoding="utf-8"))
TOK = re.compile(r"__(GITLAB|REDDIT|SHOPPING_ADMIN|SHOPPING|WIKIPEDIA|MAP)__")
def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, p + "." + k)
    elif isinstance(o, list):
        for v in o: yield from leaves(v, p + "[]")
    elif isinstance(o, str): yield p, o
shape = collections.Counter(); ex = {}
for t in d:
    for p, s in leaves(t):
        if TOK.search(s) and p not in (".start_url", ".eval.reference_url", ".eval.program_html[].url"):
            k = (p, "starts_with_token" if TOK.match(s) else "token_inside", "has_whitespace" if re.search(r"\s", s) else "no_whitespace")
            shape[k] += 1; ex.setdefault(k, (t["task_id"], s[:90]))
for k, c in shape.items(): print(c, k, "example task", ex[k][0], repr(ex[k][1]))
