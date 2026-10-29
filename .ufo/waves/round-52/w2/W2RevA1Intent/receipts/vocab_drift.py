import sys, json, re
sys.path.insert(0, "lane/plans")
import round52_c1_grader_audit as c
from pathlib import Path
pop = json.load(open("lane/plans/round52-tasks.json"))
root = Path("lane/corpus/evidence/round52/graders")
FC = re.compile(r"(read_text|read_bytes|open\(|json\.load|re\.(search|match|findall|finditer)|\.decode\(|\.strip\(\)|\.splitlines\(\))")
FP = re.compile(r"(exists\(|is_file\(|is_dir\(|os\.path\.exists)")
FB = re.compile(r"(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl)")
def fl(b, C, P, B):
    p = bool(P.search(b)); k = bool(C.search(b)); h = bool(B.search(b))
    n = len(re.findall(r"^\s*def\s+test_", b, re.M))
    if p and not k and not h: return "V1"
    if h: return "V2"
    if k: return "V3"
    return "V4" if n <= 2 else "V0"
n = 0
for t, files in sorted(pop["tasks"].items()):
    pg = c.primary_grader(files)
    if not pg or not (root/pg).exists(): continue
    n += 1
    b = (root/pg).read_text(errors="replace")
    a = fl(b, c.CONTENT, c.PRESENCE, c.BEHAVIOUR); f = fl(b, FC, FP, FB)
    if a != f: print("FILE-CLASS DRIFT", t, "frozen-literal=", f, "counter=", a)
print("primary graders compared:", n)
b = (root/"hf-model-inference/tests/test_outputs.py").read_text(errors="replace")
print("P1 false-positive candidate hf-model-inference::test_model_downloaded ->", [d["class"] for d in c.classify_tests(b) if d["test"] == "test_model_downloaded"])
