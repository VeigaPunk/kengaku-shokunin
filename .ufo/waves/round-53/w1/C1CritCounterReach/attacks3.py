import json as J, re
exec(open("/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach/attacks.py").read().split("# ---------- T1")[0])
PICK = {}
for tk in ["break-filter-js-from-html", "build-pov-ray", "write-compressor"]:
    x = [v for v in TESTS if v["task"] == tk][0]
    L_ = open(f"{REAL}/corpus/evidence/round52/graders/{x['file']}", encoding="utf-8").read().splitlines()
    span = L_[x["lineno"] - 1:x["end_lineno"]]
    q = next(l.strip() for l in span if len(l.strip()) >= 25 and not l.strip().startswith("def "))
    PICK[tk] = (x["id"], q, x["file"])
def composite(lane, reader="ReaderZ", repdir="ReaderZ"):
    open(f"{lane}/plans/round53_c1_classify.py", "w").write(ALLP1); freeze(lane)
    commit(lane, "A", "plans/round53-c1-freeze.json", "plans/round53_c1_classify.py")
    write_labels(lane); commit(lane, "B", "corpus/evidence/round53/oracle-labels.json")
    os.makedirs(f"{lane}/corpus/evidence/round53/fetched", exist_ok=True)
    open(f"{lane}/corpus/evidence/round53/fetched/fx-a.html", "w").write("fixture archive: presence-only checks of output files are common in graders\n")
    for n in ("fx-s1.html", "fx-s2.html"):
        open(f"{lane}/corpus/evidence/round53/fetched/{n}", "w").write("fixture unrelated page about gardening and soup recipes\n")
def conf(lane, rep, reader):
    return [{"task": t, "test_id": i, "quote": q, "reader": reader, "confirmed": True, "report": rep, "report_sha256": sha(f"{lane}/{rep}")} for t, (i, q, _) in PICK.items()]
def pa(rows_fetch, sweep, verdict, quote, lane):
    out = []
    for i, tk in enumerate(PICK):
        f, qq = rows_fetch(tk)
        r = {"task": tk, "verdict": verdict, "url": f"https://fixture-{'abc'[i]}.invalid/{i}", "fetched": f,
             "fetched_sha256": sha(f"{lane}/{f}") if not f.startswith("/") else None, "quote": qq}
        if sweep is not None: r["sweep"] = [{"file": s, "file_sha256": sha(f"{lane}/{s}")} for s in sweep]
        out.append(r)
    return out
def write(lane, rel, rows):
    open(f"{lane}/{rel}", "w").write(J.dumps(rows))
def sentence(path):
    for l in open(path, encoding="utf-8").read().splitlines():
        w = re.sub(r"\s+", " ", l.strip().strip('"').strip()).split(" ")
        if 8 <= len(w) <= 25 and not l.strip().startswith("assert"):
            return " ".join(w)
    return None

# T5c: reader is a labeler (report path contains the labeler name so the reader-in-path check passes)
L = fresh("T5c-reader-is-labeler")
composite(L)
rep = f"{L}/corpus/evidence/round53/C1LabelA-notes.md"
open(rep, "w").write("FIXTURE report by a labeler seat (critic forgery): break-filter-js-from-html build-pov-ray write-compressor presence.\n")
fx = "corpus/evidence/round53/fetched/fx-a.html"
rows = pa(lambda t: (fx, "presence-only checks of output files are common in graders"), ["corpus/evidence/round53/fetched/fx-s1.html", "corpus/evidence/round53/fetched/fx-s2.html"], "phenomenon-new", None, L)
write(L, "corpus/evidence/round53/prior-art.json", rows)
c = conf(L, "corpus/evidence/round53/C1LabelA-notes.md", "C1LabelA"); write(L, "corpus/evidence/round53/confirmations.json", c)
counter(L, "T5c-reader-is-labeler")

# T6a: prior-art 'fetched' archive is a repo grader reached through a '..' path that passes the prefix test
L = fresh("T6a-archive-traversal")
composite(L)
rep = f"{L}/.ufo/waves/round-53/w2/ReaderZ/report.md"; os.makedirs(os.path.dirname(rep), exist_ok=True)
open(rep, "w").write("FIXTURE reader report (critic forgery): break-filter-js-from-html build-pov-ray write-compressor\n")
write(L, "corpus/evidence/round53/confirmations.json", conf(L, ".ufo/waves/round-53/w2/ReaderZ/report.md", "ReaderZ"))
def trav(tk):
    _, q, f = PICK[tk]
    s = sentence(f"{REAL}/corpus/evidence/round52/graders/{f}")
    return (f"corpus/evidence/round53/fetched/../../round52/graders/{f}", s)
rows = []
for i, tk in enumerate(PICK):
    f, qq = trav(tk)
    rows.append({"task": tk, "verdict": "phenomenon-new", "url": f"https://fixture-{'abc'[i]}.invalid/{i}", "fetched": f,
                 "fetched_sha256": sha(f"{L}/corpus/evidence/round53/fetched/../../round52/graders/{PICK[tk][2]}"),
                 "quote": qq, "sweep": [{"file": "corpus/evidence/round53/fetched/fx-s1.html", "file_sha256": sha(f"{L}/corpus/evidence/round53/fetched/fx-s1.html")},
                                        {"file": "corpus/evidence/round53/fetched/fx-s2.html", "file_sha256": sha(f"{L}/corpus/evidence/round53/fetched/fx-s2.html")}]})
    print("T6a quote", tk, repr(qq), len(qq.split()))
write(L, "corpus/evidence/round53/prior-art.json", rows)
counter(L, "T6a-archive-traversal")

# T6b: 'new' sweep = the same unrelated file listed twice
L = fresh("T6b-sweep-duplicate")
composite(L)
rep = f"{L}/.ufo/waves/round-53/w2/ReaderZ/report.md"; os.makedirs(os.path.dirname(rep), exist_ok=True)
open(rep, "w").write("FIXTURE reader report (critic forgery): break-filter-js-from-html build-pov-ray write-compressor\n")
write(L, "corpus/evidence/round53/confirmations.json", conf(L, ".ufo/waves/round-53/w2/ReaderZ/report.md", "ReaderZ"))
rows = pa(lambda t: ("corpus/evidence/round53/fetched/fx-a.html", "presence-only checks of output files are common in graders"),
          ["corpus/evidence/round53/fetched/fx-s1.html", "corpus/evidence/round53/fetched/fx-s1.html"], "phenomenon-new", None, L)
write(L, "corpus/evidence/round53/prior-art.json", rows)
counter(L, "T6b-sweep-duplicate")

# T6c: 'known' verdict whose archive is a bare link list naming the three task ids once each
L = fresh("T6c-known-link-list")
composite(L)
rep = f"{L}/.ufo/waves/round-53/w2/ReaderZ/report.md"; os.makedirs(os.path.dirname(rep), exist_ok=True)
open(rep, "w").write("FIXTURE reader report (critic forgery): break-filter-js-from-html build-pov-ray write-compressor\n")
write(L, "corpus/evidence/round53/confirmations.json", conf(L, ".ufo/waves/round-53/w2/ReaderZ/report.md", "ReaderZ"))
open(f"{L}/corpus/evidence/round53/fetched/fx-k.html", "w").write("fixture link list of task names: break-filter-js-from-html build-pov-ray write-compressor\n")
rows = pa(lambda t: ("corpus/evidence/round53/fetched/fx-k.html", "fixture link list of task names: break-filter-js-from-html build-pov-ray write-compressor"),
          None, "phenomenon-known", None, L)
write(L, "corpus/evidence/round53/prior-art.json", rows)
counter(L, "T6c-known-link-list")
