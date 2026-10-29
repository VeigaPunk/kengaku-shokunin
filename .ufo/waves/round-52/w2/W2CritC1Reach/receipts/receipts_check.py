import importlib.util, json, hashlib, io, re, tokenize
from pathlib import Path
S = Path("/fast/scratch/hyaku/kengaku-r52/w2-W2CritC1Reach")
B = S / "base"; G = B / "corpus/evidence/round52/graders"
spec = importlib.util.spec_from_file_location("ctr", str(B / "plans/round52_c1_grader_audit.py"))
ctr = importlib.util.module_from_spec(spec); spec.loader.exec_module(ctr)
pop = json.load(open(B / "plans/round52-tasks.json"))
# blob check against the pin tree (GitHub git/trees at pin, recursive)
tree = json.load(open(S / "pin-tree.json"))
up = {e["path"]: e["sha"] for e in tree["tree"] if e["type"] == "blob"}
pop_files = sorted({p for v in pop["capture_population"].values() for p in v})
ok = bad = absent = notup = 0
for p in pop_files:
    f = G / p
    if not f.exists(): absent += 1; continue
    data = f.read_bytes()
    sha = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if p not in up: notup += 1
    elif up[p] == sha: ok += 1
    else: bad += 1; print("BLOB MISMATCH", p)
print(f"BLOB pin_tree_blobs={len(up)} population_files={len(pop_files)} match={ok} mismatch={bad} not_in_tree={notup} absent={absent}")
# exemplar re-classification: as-is vs stripped (comments + docstrings) + truncated at next top-level def/class
def strip(block):
    toks = list(tokenize.generate_tokens(io.StringIO(block).readline))
    out = []; prev = None
    for t in toks:
        if t.type == tokenize.COMMENT: continue
        if t.type == tokenize.STRING and prev is not None and prev.type == tokenize.OP and prev.string == ":" :
            out.append('""'); prev = t; continue
        out.append(t.string); prev = t
    return "".join(out)
def trunc(body, name):
    m = re.search(r"^def\s+" + name + r"\s*\(", body, re.M)
    rest = body[m.start():]
    nx = re.search(r"^(def|class)\s", rest[1:], re.M)
    return rest[:nx.start() + 1] if nx else rest
for t, n in [("pytorch-model-recovery", "test_model_file_exists"), ("torch-tensor-parallelism", "test_parallel_linear_exists")]:
    body = (G / ctr.primary_grader(pop["tasks"][t])).read_text()
    asis = dict(ctr.split_tests(body))[n]
    both = strip(trunc(body, n))
    print(f"EXEMPLAR {t}::{n} as_is={ctr.classify_test(asis)} comment_docstring_stripped={ctr.classify_test(strip(asis))} "
          f"truncated_only={ctr.classify_test(trunc(body, n))} truncated_and_stripped_P1_check={'P1' if ('assert' in both and ctr.PRESENCE.search(both) and not ctr.VALUE.search(ctr.PRESENCE.sub(' ', both)) and not ctr.BEHAV_T.search(ctr.PRESENCE.sub(' ', both))) else 'not-P1'}")
