import importlib.util, json, re, sys
from pathlib import Path
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("c1", LANE / "plans/round52_c1_grader_audit.py")
c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
cap = LANE / "corpus/evidence/round52/graders"
pop = json.loads((LANE / "plans/round52-tasks.json").read_text())
out = {"candidate_lines": [], "p1_checks": [], "ten_first": [], "missed_p1": [], "p1_all": [], "prose_value_hits": []}
recs = {}
for task, files in sorted(pop["tasks"].items()):
    pg = c1.primary_grader(files)
    if pg is None: continue
    if not (cap / pg).exists():
        print("ABSENT (A5 excluded):", task, pg); continue
    body = (cap / pg).read_bytes().decode("utf-8", "replace")
    tests = []
    for name, block in c1.split_tests(body):
        cls = c1.classify_test(block)
        # which VALUE tokens fire on the presence-stripped block
        stripped = c1.PRESENCE.sub(" ", block)
        vhits = sorted({m.group(0) for m in c1.VALUE.finditer(stripped)})
        tests.append({"test": name, "class": cls, "value_hits": vhits, "block": block})
    recs[task] = {"grader": pg, "body": body, "tests": tests, "file_cls": c1.classify(body)[0],
                  "ntestdef_TESTFN": len(c1.TESTFN.findall(body)), "ntestdef_split": len(tests)}
    for t in tests:
        if t["class"] == "P1":
            out["p1_all"].append(f"{task}::{t['test']}")
        # prose-only VALUE hit: presence in block AND a VALUE hit that is only 'in' or '->'
        if c1.PRESENCE.search(t["block"]) and t["class"] == "P3":
            hits = t["value_hits"]
            if hits and set(hits) <= {"in", ">", "<"}:
                out["prose_value_hits"].append({"task": task, "test": t["test"], "hits": hits})
# Candidate lines first ten (mirror counter ordering)
cands = sorted(t for t, r in recs.items() if any(x["class"] == "P1" for x in r["tests"]) or r["file_cls"] in ("V1", "V4"))
out["candidate_count"] = len(cands)
out["candidate_lines"] = cands
out["ten_first"] = cands[:10]
out["p1_all_count"] = len(out["p1_all"])
out["tasks_with_p1"] = sorted({x.split("::")[0] for x in out["p1_all"]})
out["file_v1_without_p1"] = [t for t in cands if not any(x["class"]=="P1" for x in recs[t]["tests"])]
# named A1 tests
for task, name in [("pytorch-model-recovery","test_model_file_exists"),("torch-tensor-parallelism","test_parallel_linear_exists")]:
    blk = [x for x in recs[task]["tests"] if x["test"]==name][0]
    out["missed_p1"].append({"task": task, "test": name, "counter_class": blk["class"], "value_hits": blk["value_hits"], "block": blk["block"]})
# P1 detail for first ten
for t in cands[:10]:
    for x in recs[t]["tests"]:
        if x["class"]=="P1":
            out["p1_checks"].append({"task": t, "test": x["test"], "value_hits_after_presence_strip": x["value_hits"], "block": x["block"]})
# tests-count consistency
out["count_mismatch"] = {t: (r["ntestdef_TESTFN"], r["ntestdef_split"]) for t, r in recs.items() if r["ntestdef_TESTFN"] != r["ntestdef_split"]}
out["prose_value_hits"] = out["prose_value_hits"]
Path("analysis.json").write_text(json.dumps(out, indent=1))
print("cands", len(cands), "p1 tests", len(out["p1_all"]), "tasks_with_p1", len(out["tasks_with_p1"]))
print("file_v1_without_p1", out["file_v1_without_p1"])
print("count_mismatch", out["count_mismatch"])
print("prose_value_hits", len(out["prose_value_hits"]))
for h in out["prose_value_hits"]: print("  ", h)
