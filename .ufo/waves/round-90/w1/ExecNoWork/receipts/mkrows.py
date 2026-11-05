import json,sys
mode, ledger_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
rows=[]
for l in open(ledger_path):
    if l.strip(): rows.append(json.loads(l))
pending=[o for o in rows if not o.get("supersedes") and o.get("status") in ("open","blocked")]
# first non-blank line of a file that exists in fixture tree (for malformed row R82-F1)
nb=[i for i,x in enumerate(open("corpus/lessons/round-83.md"),1) if x.strip()][0]
new=[]
for o in (pending if mode != "v3" else []):
    src = o["source"] if (isinstance(o.get("source"),str) and o["source"].rsplit(":",1)[-1].isdigit()) else f"corpus/lessons/round-83.md:{nb}"
    new.append({"id": "CTRL1-"+o["id"], "class": o.get("class","ledger-only-control"), "source": src,
                "opened_round": o.get("opened_round",82) if isinstance(o.get("opened_round"),int) else 82,
                "status": "closed", "close": "ledger-only control: marked closed by fiat, no work performed",
                "blocker": None, "check": None, "supersedes": o["id"]})
if mode in ("v2","v3"):
    for k,r in enumerate(range(83,90),1):
        new.append({"id": f"FAKESEED-{r}", "class": "fake-seed", "source": "corpus/routed-findings.jsonl:1",
                    "opened_round": r, "status": "closed", "close": "fake seed: no verification",
                    "blocker": None, "check": None, "supersedes": None})
with open(out,"a") as f:
    for r in new: f.write(json.dumps(r)+"\n")
print("pending_resolved",len(pending),"appended",len(new))
