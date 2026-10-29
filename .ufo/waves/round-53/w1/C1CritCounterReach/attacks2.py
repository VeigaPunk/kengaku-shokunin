import sys
sys.argv = ["x"]
exec(open("/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach/attacks.py").read().split("# ---------- T1")[0])
import subprocess as sp

# ---------- T2 (proper): freeze+classifier v1 committed, labels committed, THEN classifier v2 + re-hashed freeze ----------
L = fresh("T2-rewrite-after-labels")
open(f"{L}/plans/round53_c1_classify.py", "w").write(ALLP1); freeze(L)
commit(L, "A: freeze + classifier v1", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
write_labels(L); commit(L, "B: labels copied from v1", "corpus/evidence/round53/oracle-labels.json")
open(f"{L}/plans/round53_c1_classify.py", "a").write("\n# v2: changed after labels were committed\n")
freeze(L); commit(L, "C: classifier v2 + re-hashed freeze", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
print(git(L, "log", "--format=%h %s").stdout.strip())
counter(L, "T2")

# ---------- T3: counter reads the working tree, not the committed labels (no clean-tree check) ----------
L = fresh("T3-dirty-tree")
open(f"{L}/plans/round53_c1_classify.py", "w").write(ALLP1); freeze(L)
commit(L, "A", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
write_labels(L); commit(L, "B: honest-looking labels committed (all Y)", "corpus/evidence/round53/oracle-labels.json")
write_labels(L, contested=set(x["id"] for x in TESTS[:45]))   # uncommitted edit
print("dirty:", git(L, "status", "--porcelain").stdout.strip())
counter(L, "T3-working-tree")
print("HEAD labels contested=", sum(1 for v in __import__("json").loads(git(L,"show","HEAD:corpus/evidence/round53/oracle-labels.json").stdout)["labels"].values() if v["labels"][0]!=v["labels"][1]))

# ---------- T5: report path / reader checks (uses the composite-style confirmations) ----------
def composite(lane):
    open(f"{lane}/plans/round53_c1_classify.py", "w").write(ALLP1); freeze(lane)
    commit(lane, "A", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
    write_labels(lane); commit(lane, "B", "corpus/evidence/round53/oracle-labels.json")
    rep = f"{lane}/.ufo/waves/round-53/w2/ReaderZ/report.md"
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    open(rep, "w").write("FIXTURE reader report (critic forgery, not a read): break-filter-js-from-html build-pov-ray write-compressor test presence checks.\n")
    return rep
import json as J
PICK = {}
for tk in ["break-filter-js-from-html", "build-pov-ray", "write-compressor"]:
    x = [v for v in TESTS if v["task"] == tk][0]
    L_ = open(f"{REAL}/corpus/evidence/round52/graders/{x['file']}", encoding="utf-8").read().splitlines()
    span = L_[x["lineno"] - 1:x["end_lineno"]]
    q = next(l.strip() for l in span if len(l.strip()) >= 25 and not l.strip().startswith("def "))
    PICK[tk] = (x["id"], q)
def confirmations(lane, rep, reader):
    return [{"task": t, "test_id": i, "quote": q, "reader": reader, "confirmed": True, "report": rep, "report_sha256": sha(f"{lane}/{rep}") if not rep.startswith("/") else sha(rep)} for t, (i, q) in PICK.items()]
def fx_archives(lane):
    d = f"{lane}/corpus/evidence/round53/fetched"; os.makedirs(d, exist_ok=True)
    open(f"{d}/fx-a.html", "w").write("fixture archive: presence-only checks of output files are common in graders\n")
    open(f"{d}/fx-s1.html", "w").write("fixture unrelated page about gardening and soup recipes\n")
    open(f"{d}/fx-s2.html", "w").write("fixture unrelated page about bread and yeast\n")
def pa_rows(lane, fetched, sweep, verdict="phenomenon-new", quote="presence-only checks of output files are common in graders"):
    rows = []
    for i, tk in enumerate(PICK):
        rows.append({"task": tk, "verdict": verdict, "url": f"https://fixture-{'abc'[i]}.invalid/{i}",
                     "fetched": fetched, "fetched_sha256": sha(f"{lane}/{fetched}") if not fetched.startswith("/") else sha(fetched),
                     "quote": quote, "sweep": [{"file": s, "file_sha256": sha(f"{lane}/{s}")} for s in sweep] if sweep is not None else None})
        if sweep is None: del rows[-1]["sweep"]
    return rows

L = fresh("T5-report-reader")
rep = composite(L); fx_archives(L)
open(f"{L}/corpus/evidence/round53/prior-art.json", "w").write(J.dumps(pa_rows(L, "corpus/evidence/round53/fetched/fx-a.html", ["corpus/evidence/round53/fetched/fx-s1.html", "corpus/evidence/round53/fetched/fx-s2.html"])))
open(f"{L}/corpus/evidence/round53/confirmations.json", "w").write(J.dumps(confirmations(L, ".ufo/waves/round-53/w2/ReaderZ/report.md", "ReaderZ")))
counter(L, "T5a-control-correct-report")
# 5b: report outside .ufo/waves/round-53 (repo path containing the reader name)
os.makedirs(f"{L}/corpus/evidence/round53", exist_ok=True)
open(f"{L}/corpus/evidence/round53/ReaderZ-notes.md", "w").write(open(rep).read())
open(f"{L}/corpus/evidence/round53/confirmations.json", "w").write(J.dumps(confirmations(L, "corpus/evidence/round53/ReaderZ-notes.md", "ReaderZ")))
counter(L, "T5b-report-outside-prefix")
# 5c: reader is a label seat (C1LabelA labels every test; here it also 'reads' and confirms)
open(f"{L}/corpus/evidence/round53/confirmations.json", "w").write(J.dumps(confirmations(L, "corpus/evidence/round53/ReaderZ-notes.md", "C1LabelA")))
counter(L, "T5c-reader-is-labeler")
