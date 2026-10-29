import sys, json
sys.path.insert(0, sys.argv[1] + "/plans")
import round52_c1_grader_audit as A
from pathlib import Path
lane = Path(sys.argv[1])
pop = A.load_population(lane)
out = {}
for task, files in sorted(pop["tasks"].items()):
    pg = A.primary_grader(files)
    if pg is None:
        out[task] = {"grader": None}; continue
    f = lane / "corpus/evidence/round52/graders" / pg
    if not f.exists():
        out[task] = {"grader": pg, "absent": True}; continue
    body = f.read_text(errors="replace")
    out[task] = {"grader": pg, "file_class": A.classify(body)[0], "tests": A.classify_tests(body), "ntests": len(A.split_tests(body))}
json.dump(out, open(sys.argv[2], "w"), indent=1)
print("tasks", len(out))
# no-test_outputs tasks
print("no_primary", [t for t,v in out.items() if v.get("grader") is None])
print("absent", [t for t,v in out.items() if v.get("absent")])
import collections
c = collections.Counter(tt["class"] for v in out.values() for tt in v.get("tests", []))
print("per-test classes", dict(c))
