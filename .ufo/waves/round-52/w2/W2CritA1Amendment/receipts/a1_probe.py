#!/usr/bin/env python3
"""Read-only probe of Amendment A1 (per-test P1 rule) against the lane's frozen captures.

Imports the lane's counter as a module (no writes to the lane). Prints every number the
critique cites so the critique can be re-derived with:
    python3 a1_probe.py /home/vgpnk/Projects/shokunin/kengaku-shokunin
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("c1", LANE / "plans/round52_c1_grader_audit.py")
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

pop = json.loads((LANE / "plans/round52-tasks.json").read_text())
cap = LANE / "corpus/evidence/round52/graders"
recs = {}
for t, files in sorted(pop["tasks"].items()):
    pg = c1.primary_grader(files)
    if pg is None or not (cap / pg).exists():
        continue
    body = (cap / pg).read_bytes().decode("utf-8", "replace")
    recs[t] = {"grader": pg, "body": body, "file_cls": c1.classify(body)[0],
               "tests": c1.split_tests(body)}

print("== 1. Amended per-test class of the cited examples")
cited = [("pytorch-model-recovery", "test_model_file_exists"),
         ("torch-tensor-parallelism", "test_parallel_linear_exists"),
         ("bn-fit-modify", "test_bn_sample_exists")]
for t, tn in cited:
    b = dict(recs[t]["tests"])[tn]
    s = c1.PRESENCE.sub(" ", b)
    m_b = c1.BEHAV_T.search(s)
    m_v = c1.VALUE.search(s)
    print(f"{t}/{tn}: class={c1.classify_test(b)} file_cls={recs[t]['file_cls']} "
          f"BEHAV_T={m_b.group(0) if m_b else None!r} VALUE={m_v.group(0) if m_v else None!r}")
    if m_v:
        print("   VALUE context:", repr(s[max(0, m_v.start() - 30): m_v.end() + 15]))
    if m_b:
        print("   BEHAV context:", repr(s[max(0, m_b.start() - 30): m_b.end() + 15]))

print("\n== 2. Candidate pool: frozen (file-level V1/V4) vs amended (>=1 P1 OR V1/V4)")
p1_tasks = sorted(t for t, r in recs.items()
                  if any(c1.classify_test(b) == "P1" for _, b in r["tests"]))
v14 = sorted(t for t, r in recs.items() if r["file_cls"] in ("V1", "V4"))
print("frozen pool (V1/V4):", len(v14), v14)
print("amended P1 tasks:", len(p1_tasks))
print("amended pool (code):", len(set(p1_tasks) | set(v14)))
print("P1 tasks whose file-level class is V2/V3 (grader already has content/behaviour check):",
      sum(1 for t in p1_tasks if recs[t]["file_cls"] in ("V2", "V3")), "of", len(p1_tasks))
print("candidates with zero P1 tests admitted only by the V1/V4 OR-clause:",
      sorted(t for t in v14 if t not in p1_tasks))

print("\n== 3. Sensitivity of the P1 pool to rule variants (same tests, different vocabulary)")
def strip_cd(b):
    b = re.sub(r'"""[\s\S]*?"""', "", b)
    b = re.sub(r"'''[\s\S]*?'''", "", b)
    return re.sub(r"#[^\n]*", "", b)
V_NOIN = re.compile(r"(==|!=|<=|>=|[<>]|allclose|len\(|np\.|torch\.|\.keys\(\))")
V_CMP = re.compile(r"(==|!=|<=|>=|[<>])")
B_ORIG = re.compile(r"(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl )")
def cls(b, value_re, behav_re, strip):
    if "assert" not in b:
        return "P0"
    s = c1.PRESENCE.sub(" ", b)
    if strip:
        s = strip_cd(s)
    if behav_re.search(s):
        return "P2"
    if value_re.search(s):
        return "P3"
    return "P1" if c1.PRESENCE.search(b) else "P0"
variants = {
    "as-coded": (c1.VALUE, c1.BEHAV_T, False),
    "as-coded, comments/docstrings stripped": (c1.VALUE, c1.BEHAV_T, True),
    "as-coded minus bare `in`": (V_NOIN, c1.BEHAV_T, False),
    "comparison-only, original BEHAVIOUR": (V_CMP, B_ORIG, True),
}
for name, (vr, br, st) in variants.items():
    tasks = {t for t, r in recs.items() if any(cls(b, vr, br, st) == "P1" for _, b in r["tests"])}
    n = sum(1 for t, r in recs.items() for _, b in r["tests"] if cls(b, vr, br, st) == "P1")
    print(f"{name:42s} P1 tests={n:3d} tasks={len(tasks):3d}")

print("\n== 4. Helper defs absorbed into a test block (split only at def test_)")
helper = re.compile(r"^def\s+(\w+)\s*\(", re.M)
absorbed = []
for t, r in recs.items():
    for n, b in r["tests"]:
        h = [m.group(1) for m in helper.finditer(b) if not m.group(1).startswith("test_")]
        if h:
            absorbed.append((t, n, h))
print("test blocks containing non-test defs:", len(absorbed))
for a in absorbed:
    print("  ", a)

print("\n== 5. Sole-check heuristic for P1 tests (artefact named by no other P2/P3 test)")
pathre = re.compile(r"""["'](/[^"'\s]+)["']""")
def toks(b):
    out = set()
    for p in pathre.findall(b):
        out.add(p.rstrip("/").split("/")[-1].split(".")[0])
        if p.count("/") >= 2:
            out.add(p.split("/")[-2])
    return {x for x in out if len(x) >= 4 and x != "app"}
gate = sole = nolit = 0
sole_list = []
for t, r in recs.items():
    for n, b in r["tests"]:
        if c1.classify_test(b) != "P1":
            continue
        tk = toks(b)
        if not tk:
            nolit += 1
            continue
        others = [bb for nn, bb in r["tests"] if nn != n and c1.classify_test(bb) in ("P2", "P3")]
        if any(any(k in bb for k in tk) for bb in others):
            gate += 1
        else:
            sole += 1
            sole_list.append((t, n))
print(f"P1 tests: gate-like={gate} sole-check={sole} no-literal={nolit}")
for x in sole_list:
    print("   sole:", x)
