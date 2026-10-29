import importlib.util, io, re, tokenize, json
from pathlib import Path
S = Path("/fast/scratch/hyaku/kengaku-r52/w2-W2CritC1Reach")
B = S / "base"; G = B / "corpus/evidence/round52/graders"
spec = importlib.util.spec_from_file_location("ctr", str(B / "plans/round52_c1_grader_audit.py"))
ctr = importlib.util.module_from_spec(spec); spec.loader.exec_module(ctr)
pop = json.load(open(B / "plans/round52-tasks.json"))
SKIP = (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT)
def strip(src):
    """Blank comments and def-docstrings in place (positions kept, so word boundaries survive)."""
    lines = src.splitlines(keepends=True)
    offs = [0]
    for l in lines: offs.append(offs[-1] + len(l))
    def pos(rc): return offs[rc[0] - 1] + rc[1]
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    blank = []
    sig = []
    for t in toks:
        if t.type == tokenize.COMMENT: blank.append((pos(t.start), pos(t.end)))
        elif t.type not in SKIP: sig.append(t)
    for i, t in enumerate(sig):
        if t.type == tokenize.STRING and i >= 2 and sig[i-1].string == ":" and sig[i-2].string == ")":
            blank.append((pos(t.start), pos(t.end)))
    out = list(src)
    for a, b in blank:
        for k in range(a, b): out[k] = " " if out[k] != "\n" else "\n"
    return "".join(out)
def trunc(body, name):
    m = re.search(r"^def\s+" + name + r"\s*\(", body, re.M)
    rest = body[m.start():]
    nx = re.search(r"^(def|class)\s", rest[1:], re.M)
    return rest[:nx.start() + 1] if nx else rest
def p1(block):
    return ctr.classify_test(block)
for t, n in [("pytorch-model-recovery", "test_model_file_exists"), ("torch-tensor-parallelism", "test_parallel_linear_exists")]:
    body = (G / ctr.primary_grader(pop["tasks"][t])).read_text()
    asis = dict(ctr.split_tests(body))[n]
    print(f"EXEMPLAR {t}::{n} as_is={p1(asis)} stripped_only={p1(strip(asis))} truncated_only={p1(trunc(body,n))} truncated_and_stripped={p1(strip(trunc(body,n)))}")
