import json, os, pathlib, sys
sys.dont_write_bytecode = True
S = pathlib.Path(os.environ["S"]); sys.path.insert(0, str(S)); import h
ctr = h.ctr
OUT = S / "report"
res = json.loads((OUT / "res.json").read_text()); meta, RES = res["meta"], res["res"]
T2 = json.loads((OUT / "t2.json").read_text())
fixtures = json.loads((OUT / "fixtures.json").read_text()) if (OUT / "fixtures.json").exists() else None
BY = {}
fxs = [{"fid": k.split("|")[2], "tool": k.split("|")[0]} for k in RES if "|ref|" in k]
for f in fxs:
    BY.setdefault(f["tool"], []).append(f)
plain = lambda t, n, f: (lambda r: (r[0], frozenset(r[1])))(RES["%s|%s|%s" % (t, n, f)]["plain"])
lines = lambda t, n, f: set(T2["%s|%s|%s" % (t, n, f)]["p"]["line_hits"])
print("%-4s %-7s %-13s %-9s %-14s %-13s" % ("id", "span", "changed-span", "hits:region", "hits:changed", "lineset-diff-fx"))
for mid, tool, cls, direction, adv, label, _w, old, new in ctr.MUTANTS:
    m = meta[mid]; span = set(m["span"]); lo = min(span)
    ol, nl = old.split("\n"), new.split("\n")
    changed = {lo + i for i in range(len(nl)) if i >= len(ol) or ol[i] != nl[i]}
    rsh = csh = lsd = 0
    kb = None
    for f in BY[tool]:
        fid = f["fid"]
        if span & lines(tool, mid, fid): rsh += 1
        if changed & lines(tool, mid, fid): csh += 1
        if lines(tool, mid, fid) != lines(tool, "ref", fid): lsd += 1
        e = ctr.exhibits(m["cls"], m["direction"], {"fid": fid, "expect": next(x["expect"] for x in fixtures if x["fid"]==fid) if fixtures else None}, None, None) if False else None
    print("%-4s %-7s %-13s %-9s %-14s %-13s" % (mid, "%d-%d" % (lo, max(span)), sorted(changed),
          "%d/%d" % (rsh, len(BY[tool])), "%d/%d" % (csh, len(BY[tool])), "%d/%d" % (lsd, len(BY[tool]))))
