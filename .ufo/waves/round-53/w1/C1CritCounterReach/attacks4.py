exec(open("/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach/attacks3.py").read().split("# T5c:")[0])
# T6d: two 'known' rows from a bare link list + ONE 'new' row with a 2-file sweep -> predicate
L = fresh("T6d-mixed-known-new")
composite(L)
rep = f"{L}/.ufo/waves/round-53/w2/ReaderZ/report.md"; os.makedirs(os.path.dirname(rep), exist_ok=True)
open(rep, "w").write("FIXTURE reader report (critic forgery): break-filter-js-from-html build-pov-ray write-compressor\n")
write(L, "corpus/evidence/round53/confirmations.json", conf(L, ".ufo/waves/round-53/w2/ReaderZ/report.md", "ReaderZ"))
open(f"{L}/corpus/evidence/round53/fetched/fx-k.html", "w").write("fixture link list of task names: break-filter-js-from-html build-pov-ray write-compressor\n")
kq = "fixture link list of task names: break-filter-js-from-html build-pov-ray write-compressor"
rows = []
for i, tk in enumerate(PICK):
    if i == 0:
        rows.append({"task": tk, "verdict": "phenomenon-new", "url": "https://fixture-a.invalid/0", "fetched": "corpus/evidence/round53/fetched/fx-a.html",
                     "fetched_sha256": sha(f"{L}/corpus/evidence/round53/fetched/fx-a.html"), "quote": "presence-only checks of output files are common in graders",
                     "sweep": [{"file": "corpus/evidence/round53/fetched/fx-s1.html", "file_sha256": sha(f"{L}/corpus/evidence/round53/fetched/fx-s1.html")},
                               {"file": "corpus/evidence/round53/fetched/fx-s2.html", "file_sha256": sha(f"{L}/corpus/evidence/round53/fetched/fx-s2.html")}]})
    else:
        rows.append({"task": tk, "verdict": "phenomenon-known", "url": f"https://fixture-{'bc'[i-1]}.invalid/{i}", "fetched": "corpus/evidence/round53/fetched/fx-k.html",
                     "fetched_sha256": sha(f"{L}/corpus/evidence/round53/fetched/fx-k.html"), "quote": kq})
write(L, "corpus/evidence/round53/prior-art.json", rows)
counter(L, "T6d-mixed-known-new")

# T7: all labels U -> expected: contested budget rejects it (negative control, checks the budget is enforced)
L = fresh("T7-all-U")
composite(L)
lab = {x["id"]: {"labelers": ["C1LabelA", "C1LabelB"], "labels": ["U", "U"]} for x in TESTS}
open(f"{L}/corpus/evidence/round53/oracle-labels.json", "w").write(J.dumps({"labels": lab}))
commit(L, "labels all U", "corpus/evidence/round53/oracle-labels.json")
counter(L, "T7-all-U")
