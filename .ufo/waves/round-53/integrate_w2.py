#!/usr/bin/env python3
"""L1 integration of wave-2 evidence into corpus/evidence/round53/ (run from the lane root, working tree only; nothing is committed here).

  confirmations.json  <- C1ConfRead*/confirmations-part.json (confirmed:true only, one per task, report path + digest added)
  prior-art.json      <- C1PriorArt*/prior-art-part.json restricted to confirmed tasks, archives copied to
                         corpus/evidence/round53/fetched/<seat>-<name> with their digests recomputed
Usage: integrate_w2.py [--tasks t1,t2]   (restrict to a subset of tasks, for experiments)
"""
import glob
import hashlib
import json
import shutil
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]
W2 = LANE / ".ufo/waves/round-53/w2"
OUT = LANE / "corpus/evidence/round53"
FETCHED = OUT / "fetched"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


only = None
if "--tasks" in sys.argv:
    only = set(sys.argv[sys.argv.index("--tasks") + 1].split(","))

conf, seen = [], set()
for f in sorted(glob.glob(str(W2 / "C1ConfRead*/confirmations-part.json"))):
    for r in json.loads(Path(f).read_text()):
        if r.get("confirmed") is not True or r["task"] in seen or (only and r["task"] not in only):
            continue
        rep = W2 / f"{r['reader']}.md"
        if not rep.is_file():
            print("no report for", r["reader"])
            continue
        rel = str(rep.relative_to(LANE))
        conf.append({"task": r["task"], "test_id": r["test_id"], "quote": r["quote"], "reader": r["reader"], "confirmed": True,
                     "report": rel, "report_sha256": sha(rep)})
        seen.add(r["task"])
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "confirmations.json").write_text(json.dumps(conf, indent=1) + "\n")
print("confirmations", len(conf), sorted(seen))

FETCHED.mkdir(parents=True, exist_ok=True)


def ingest(seat: str, path: str) -> Path | None:
    src = Path(path)
    if not src.is_absolute():
        src = LANE / path
    if not src.is_file():
        return None
    dst = FETCHED / f"{seat}-{src.name}"
    shutil.copyfile(src, dst)
    return dst


rows, taken = [], set()
for f in sorted(glob.glob(str(W2 / "C1PriorArt*/prior-art-part.json"))):
    seat = Path(f).parent.name
    for r in json.loads(Path(f).read_text()):
        t = r["task"]
        if t not in seen or t in taken:
            continue
        main = ingest(seat, r["fetched"])
        if main is None:
            print("missing archive", seat, t, r["fetched"])
            continue
        row = {"task": t, "verdict": r["verdict"], "url": r["url"], "fetched": str(main.relative_to(LANE)),
               "fetched_sha256": sha(main), "quote": r["quote"]}
        if r["verdict"] == "phenomenon-new":
            sw = []
            for s in r.get("sweep", []):
                d = ingest(seat, s["file"])
                if d is not None:
                    sw.append({"file": str(d.relative_to(LANE)), "file_sha256": sha(d)})
            row["sweep"] = sw
        rows.append(row)
        taken.add(t)
(OUT / "prior-art.json").write_text(json.dumps(rows, indent=1) + "\n")
print("prior-art rows", len(rows), "tasks", sorted(taken), "missing", sorted(seen - taken))
