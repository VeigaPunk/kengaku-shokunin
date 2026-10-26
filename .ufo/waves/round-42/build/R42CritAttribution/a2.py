#!/usr/bin/env python3
"""Critic analysis v2: vacuity, trace fidelity, event credit, X6, strengthened-leg draft, value probes."""
import json
import os
import pathlib
import sys

sys.dont_write_bytecode = True
S = pathlib.Path(os.environ["S"])
sys.path.insert(0, str(S))
import h  # scratch harness

ctr = h.ctr
OUT = S / "report"
res = json.loads((OUT / "res.json").read_text())
meta, RES = res["meta"], res["res"]
T2 = json.loads((OUT / "t2.json").read_text())
ROOT3 = S / "run3"
ROOT3.mkdir(parents=True, exist_ok=True)
runner3 = ctr.Runner(ROOT3, 8)
fixtures, side = ctr.build_battery(S / "wb", ROOT3, S / "lane")
BY = {t: [fx for fx in fixtures if fx["tool"] == t] for t in ctr.TOOLS}
FID = {fx["fid"]: fx for fx in fixtures}
L = []


def p(*a):
    L.append(" ".join(str(x) for x in a))


def plain(tool, name, fid):
    r = RES["%s|%s|%s" % (tool, name, fid)]["plain"]
    return (r[0], frozenset(r[1]))


def stock(tool, name, fid):
    r = RES["%s|%s|%s" % (tool, name, fid)]["stock"]
    return (r[0], frozenset(r[1]), frozenset(r[2]))


def t2rc(tool, name, fid):
    r = T2["%s|%s|%s" % (tool, name, fid)]
    return (r["rc"], frozenset(r["cls"]))


def state_diff(tool, mid, fid, span):
    """First common line at/after the span, in a code object holding the span, whose live-frame
    digest differs between mutant and reference. Returns (desc, line) or (None, None)."""
    lo = min(span)
    r = T2["%s|ref|%s" % (tool, fid)]["p"]["locs"]
    q = T2["%s|%s|%s" % (tool, mid, fid)]["p"]["locs"]
    hits = []
    for d in q:
        if d not in r:
            continue
        qd = {int(k): v for k, v in q[d].items()}
        rd = {int(k): v for k, v in r[d].items()}
        if not (set(qd) & span):
            continue
        diffs = sorted(n for n in set(qd) & set(rd) if n >= lo and qd[n] != rd[n])
        if diffs:
            hits.append((min(diffs), d, diffs))
    if not hits:
        return (None, None)
    hits.sort()
    return (hits[0][1], hits[0][2])


p("SETUP fixtures=%d side=%d" % (len(fixtures), side))

p("")
p("== A. frozen span leg vs behaviour ==")
p("%-4s %-6s %-10s %-7s %-4s %-8s %-9s %-12s %-9s %-14s %s" %
  ("id", "tool", "direction", "span", "n_fx", "exhibit", "span_hit", "hit_not_exh", "ref_hit", "state_diff", "killed_by"))
for mid, m in meta.items():
    tool, span = m["tool"], set(m["span"])
    exh = sh = hne = rsh = sd = 0
    kb = "-"
    for fx in BY[tool]:
        fid = fx["fid"]
        e = ctr.exhibits(m["cls"], m["direction"], fx, plain(tool, "ref", fid), plain(tool, mid, fid))
        exh += bool(e)
        if e and kb == "-":
            kb = fid
        sl = stock(tool, mid, fid)[2] & span
        sh += bool(sl)
        hne += bool(sl) and not e
        rsh += bool(stock(tool, "ref", fid)[2] & span)
        sd += state_diff(tool, mid, fid, span)[0] is not None
    p("%-4s %-6s %-10s %-7s %-4d %-8d %-9d %-12d %-9d %-14s %s" %
      (mid, tool, m["direction"], "%d-%d" % (min(span), max(span)), len(BY[tool]),
       exh, sh, hne, rsh, "%d/%d" % (sd, len(BY[tool])), kb))

p("")
p("== B. traced vs untraced ==")
n = d_stock = d_t2 = 0
for key in sorted(RES):
    tool, name, fid = key.split("|")
    a, b, c = plain(tool, name, fid), stock(tool, name, fid), t2rc(tool, name, fid)
    n += 1
    if (a[0], a[1]) != (b[0], b[1]):
        d_stock += 1
        p("DIVERGE-stock", key, a, b[:2])
    if (a[0], a[1]) != (c[0], c[1]):
        d_t2 += 1
        p("DIVERGE-t2", key, a, c)
p("pairs=%d frozen-tracer-diverged=%d instrumented-tracer-diverged=%d" % (n, d_stock, d_t2))

p("")
p("== C. event credit ==")
nonline = set()
calls = set()
for key in sorted(T2):
    tool, name, fid = key.split("|")
    t = T2[key]["p"]
    st = set(t["line_hits"])
    cl = {n for _dd, n in t["calls"]}
    calls |= cl
    nonline |= (cl - st)
    if set(stock(tool, name, fid)[2]) != (st | cl):
        p("MISMATCH", key)
p("line numbers credited only by call events (all runs):", sorted(nonline))
p("distinct call-event line numbers:", len(calls), "includes 0:", 0 in calls)
only_call_spans = []
for mid, m in meta.items():
    for fx in BY[m["tool"]]:
        t = T2["%s|%s|%s" % (m["tool"], mid, fx["fid"])]["p"]
        st, cl = set(t["line_hits"]), {n for _dd, n in t["calls"]}
        sp = set(m["span"])
        if (sp & cl) and not (sp & st):
            only_call_spans.append((mid, fx["fid"]))
p("span credited only by a call event, any run: %d" % len(only_call_spans))
p("span lines that are also call-event lines:", sorted({min(set(m['span']) & calls) for m in meta.values() if set(m['span']) & calls}))

p("")
p("== D. X6 two-line replacement, span %s ==" % meta["X6"]["span"])
for fx in BY["anchor"]:
    fid = fx["fid"]
    lh = set(T2["anchor|X6|%s" % fid]["p"]["line_hits"])
    rlh = set(T2["anchor|ref|%s" % fid]["p"]["line_hits"])
    sd = state_diff("anchor", "X6", fid, set(meta["X6"]["span"]))
    p("  %-28s mut527=%d mut528=%d ref527=%d ref528=%d span_leg=%d state_diff=%s" %
      (fid, 527 in lh, 528 in lh, 527 in rlh, 528 in rlh, bool({527, 528} & lh),
       "%s@L%s" % sd if sd[0] else "-"))

p("")
p("== E. strengthened-leg draft: same-frame live state differs (ref vs mutant) ==")
for mid, m in meta.items():
    tool, span = m["tool"], set(m["span"])
    kb = next((fx["fid"] for fx in BY[tool]
               if ctr.exhibits(m["cls"], m["direction"], fx, plain(tool, "ref", fx["fid"]),
                               plain(tool, mid, fx["fid"]))), None)
    sd = state_diff(tool, mid, kb, span) if kb else (None, None)
    per = [fx["fid"] for fx in BY[tool] if state_diff(tool, mid, fx["fid"], span)[0]]
    p("%-4s killing=%-26s state_diff_on_killing=%-24s fixtures_with_state_diff=%d/%d" %
      (mid, kb, ("%s L%s" % (sd[0], sd[1])) if sd[0] else "NONE", len(per), len(BY[tool])))

p("")
p("== F. value of the mutated expression ==")
V = S / "run1" / "variants"


def load(path_, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, str(path_))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


order = load(V / "ref-order.py", "ref_order2")
xo6 = load(V / "XO6.py", "xo6b")
xo7 = load(V / "XO7.py", "xo7b")
g6, c7 = order.GATE_P10.pattern, order.CASE_LINE.pattern
p("XO6 ref GATE_P10 pattern: %r" % g6)
p("XO6 mut GATE_P10 pattern: %r" % xo6.GATE_P10.pattern)
p("XO7 ref CASE_LINE pattern: %r" % c7)
p("XO7 mut CASE_LINE pattern: %r" % xo7.CASE_LINE.pattern)
l6, l7 = "P10 PASS receipt unreadable", "CASE c1 observed=timeout"
p("XO6 GATE_P10.match(%r) ref=%s mut=%s" % (l6, order.GATE_P10.match(l6), xo6.GATE_P10.match(l6)))
p("XO7 CASE_LINE.match(%r) ref=%s mut=%s" % (l7, order.CASE_LINE.match(l7), xo7.CASE_LINE.match(l7)))
for name in ("ref", "X13"):
    path_ = V / (("ref-anchor.py") if name == "ref" else "X13.py")
    r2 = h.run2(runner3, "anchor", path_, FID["w-x13-staged-index"], "f13-%s" % name, full=(570, 571, 572, 573))
    t = r2[2]["full"].get("573", "")
    mref = [x for x in t.split("|") if "evidence_ref" in x]
    p("X13 %-3s rc=%d frame-state@L573 %s" % (name, r2[0], (mref[0][:120] if mref else "ABSENT")))
for mid, fxid in (("XO6", "w-xo6-p10-pass-line"), ("XO7", "w-xo7-case-timeout")):
    for name in ("ref", mid):
        path_ = V / (("ref-order.py") if name == "ref" else ("%s.py" % mid))
        r2 = h.run2(runner3, "order", path_, FID[fxid], "f-%s-%s" % (mid, name), full=(53, 55, 60))
        t = r2[2]["full"].get("55", "") or r2[2]["full"].get("60", "")
        g = [x for x in t.split("|") if x.startswith("GATE_P10=")]
        c = [x for x in t.split("|") if x.startswith("CASE_LINE=")]
        p("%s %-3s rc=%d module-state GATE_P10=%s CASE_LINE=%s" %
          (mid, name, r2[0], (g[0][len("GATE_P10="):][:110] if g else "-"),
           (c[0][len("CASE_LINE="):][:90] if c else "-")))

p("")
p("== G. control reproduction ==")
ctl = (OUT / "control-repro.txt").read_text()
p("my-run: killed=14 unattributed=0 PREDICATE=pass (see control-repro.txt)")
p("frozen control-c1-attribution.txt: killed=0 unattributed=14 PREDICATE=fail, every span=L1-L1")
(OUT / "analysis.txt").write_text("\n".join(L) + "\n")
print("\n".join(L))
