import sys, re, json, ast
sys.path.insert(0, "lane/plans")
import round52_c1_grader_audit as c
from pathlib import Path
from collections import Counter
lane = Path("lane")
pop = json.loads((lane/"plans/round52-tasks.json").read_text())
root = lane/"corpus/evidence/round52/graders"
PRES_NAMES = {"exists","is_file","is_dir","isfile","isdir"}
def is_pres(e):
    if isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.Not):
        return is_pres(e.operand)
    if isinstance(e, ast.BoolOp):
        return all(is_pres(v) for v in e.values)
    if isinstance(e, ast.Call):
        f = e.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        return name in PRES_NAMES
    return False
def msg_text(a):
    return ast.get_source_segment(SRC, a.msg) if a.msg is not None else ""
out = []
for task, files in sorted(pop["tasks"].items()):
    pg = c.primary_grader(files)
    if not pg or not (root/pg).exists(): continue
    SRC = (root/pg).read_text(errors="replace")
    try:
        tree = ast.parse(SRC)
    except SyntaxError as e:
        out.append(dict(task=task, test="<parse-error>", oracle="ERR", counter=None, note=str(e))); continue
    tests = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_")]
    counter = {d["test"]: d["class"] for d in c.classify_tests(SRC)}
    for fn in tests:
        asserts = [n for n in ast.walk(fn) if isinstance(n, ast.Assert)]
        n_pres = sum(1 for a in asserts if is_pres(a.test))
        if asserts and n_pres == len(asserts):
            oracle = "PRES"
        elif n_pres and n_pres < len(asserts):
            oracle = "MIXED"
        else:
            oracle = "OTHER"
        seg = ast.get_source_segment(SRC, fn) or ""
        out.append(dict(task=task, grader=pg, test=fn.name, n_assert=len(asserts), n_pres=n_pres,
                        oracle=oracle, counter=counter.get(fn.name), in_msg=any(re.search(r"\bin\b", msg_text(a)) for a in asserts),
                        toplevel=fn.col_offset==0, lines=seg.count("\n")+1))
json.dump(out, open("oracle.json","w"), indent=1)
print("tests", len(out))
print("oracle x counter:")
cnt = Counter((r["oracle"], r.get("counter")) for r in out)
for k,v in sorted(cnt.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))): print("  ", k, v)
print("non-toplevel test defs:", sum(1 for r in out if not r.get("toplevel")), "tasks:", sorted({r["task"] for r in out if not r.get("toplevel")})[:40])
