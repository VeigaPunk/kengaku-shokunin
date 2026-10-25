"""FContractEntry v2 scratch: independent AST derivation over the manifest-pinned bytes.
Hand-written from the claim, NOT imported from plans/benchmark_spec_audit.py. Parses only."""
import ast, hashlib, json
ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/"
man = json.load(open(ROOT + "manifest.json"))
ev_bytes = open(ROOT + "evaluation_harness/evaluators.py", "rb").read()
hf_bytes = open(ROOT + "evaluation_harness/helper_functions.py", "rb").read()
for name, data in (("evaluators.py", ev_bytes), ("helper_functions.py", hf_bytes)):
    key = "evaluation_harness/" + name
    print("sha256 ok", name, hashlib.sha256(data).hexdigest() == man["files"][key]["sha256"])
tree = ast.parse(ev_bytes)
top = {n.name: (n.lineno, n.end_lineno) for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
for want in ("StringEvaluator", "URLEvaluator", "HTMLContentEvaluator", "EvaluatorComb", "evaluator_router"):
    print("anchor", want, top[want])
# statement lines inside EvaluatorComb: score *= ...
comb = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "EvaluatorComb")
print("composite product lines", sorted(n.lineno for n in ast.walk(comb) if isinstance(n, ast.AugAssign) and isinstance(n.op, ast.Mult)))
# N/A override: assignments to `score` whose RHS calls .ua_match
ov = []
for n in ast.walk(tree):
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "score" for t in n.targets):
        if any(isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr == "ua_match" for c in ast.walk(n.value)):
            ov.append(n.lineno)
print("N/A assignment lines", ov)
# dispatch: match-case literal -> constructor names
router = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "evaluator_router")
disp = {}
for m in ast.walk(router):
    if isinstance(m, ast.Match):
        for c in m.cases:
            if isinstance(c.pattern, ast.MatchValue):
                disp[c.pattern.value.value] = [call.func.id for st in c.body for call in ast.walk(st) if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)]
print("dispatch", disp)
ht = ast.parse(hf_bytes)
hf = {n.name: (n.lineno, n.end_lineno) for n in ht.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
for want in ("llm_fuzzy_match", "llm_ua_match", "PseudoPage"):
    print("helper", want, hf[want])
# model-call and keyword lines in the two judges
src = hf_bytes.decode().splitlines()
for i, l in enumerate(src, 1):
    if "gpt-4-1106-preview" in l or "partially correct" in l or '"different" in response' in l or 'assert "same"' in l or 'assert "correct"' in l:
        print("judge line", i, l.strip()[:90])
