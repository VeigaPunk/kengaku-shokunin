import json, sys
# usage: forge_rows.py <mode> <ledger>   -- appends FABRICATED resolution rows (fixture only)
mode, path = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(path) if l.strip()]
base = {}
for r in rows:
    if "supersedes" not in r and isinstance(r.get("id"), str):
        base.setdefault(r["id"], r)
MALFORMED = {"R82-F1"}  # its source is prose; it is resolved by an explicit row below
pending = [r for r in rows if "supersedes" not in r and r.get("status") in ("open", "blocked")
           and r["id"] not in MALFORMED]
out = []
def res(r, status, **extra):
    d = {"id": f"{r['id']}-fx-{mode}", "class": r["class"], "source": r["source"],
         "opened_round": r["opened_round"], "status": status, "supersedes": r["id"]}
    d.update(extra)
    return d
if mode == "override-two":
    out.append(res(base["R42-R3-02"], "closed", close="fabricated: registry row verified (no commit)", check="true"))
    out.append(res(base["R42-R3-19"], "closed", close="fabricated: criterion re-verified (no commit)"))
elif mode == "refused-two":
    out.append(res(base["R42-R3-02"], "refused", blocker="fabricated standing blocker"))
    out.append(res(base["R45-S5-7e"], "refused", blocker="fabricated standing blocker"))
elif mode in ("full-true", "full-refused"):
    for r in pending:
        if mode == "full-true":
            out.append(res(r, "closed", close="fabricated closure, no work", check="true"))
        else:
            out.append(res(r, "refused", blocker="fabricated standing blocker"))
    if mode == "full-true":
        out.append({"id": "R82-F1-fx-" + mode, "class": "gate-blind-spot", "source": "plans/round90_burndown.py:1",
                    "opened_round": 82, "status": "closed", "close": "fabricated closure, no work",
                    "check": "true", "supersedes": "R82-F1"})
    else:
        out.append({"id": "R82-F1-fx-" + mode, "class": "gate-blind-spot", "source": "plans/round90_burndown.py:1",
                    "opened_round": 82, "status": "refused", "blocker": "fabricated standing blocker",
                    "supersedes": "R82-F1"})
    for sid, src, rnd, cls in (("R42-R2", "corpus/lessons/round-41-verifier-spotcheck.md:110", 42, "historical-close"),
                               ("R82-V8", "corpus/lessons/round-82-verifier-spotcheck.md:195", 82, "timezone-label")):
        if mode == "full-true":
            out.append({"id": sid + "-fx-" + mode, "class": cls, "source": src, "opened_round": rnd,
                        "status": "closed", "close": "fabricated closure, no work", "check": "true", "supersedes": sid})
        else:
            out.append({"id": sid + "-fx-" + mode, "class": cls, "source": src, "opened_round": rnd,
                        "status": "refused", "blocker": "fabricated standing blocker", "supersedes": sid})
print("appended", len(out), "fabricated resolution rows; pending-base(excl. malformed)=", len(pending), file=sys.stderr)
with open(path, "a") as f:
    for d in out:
        f.write(json.dumps(d) + "\n")
