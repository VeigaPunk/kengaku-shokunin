#!/usr/bin/env python3
"""Round-8 falsification analysis — offline, read-only, no HTTP. v2 (fixed hang)."""
import json, re, itertools, collections, random

REPO = "/home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round8-horizon"
recs = [json.loads(l) for l in open(f"{REPO}/results.jsonl")]

KEYS = ["nails", "bolts", "screws", "washers", "hinges"]
def sim_apply(state, op):
    s = dict(state); kind = op[0]
    if kind == "SET": s[op[1]] = op[2]
    elif kind == "ADD": s[op[1]] += op[2]
    elif kind == "SUB": s[op[1]] -= op[2]
    elif kind == "MOV": s[op[2]] += s[op[1]]; s[op[1]] = 0
    elif kind == "DEL": del s[op[1]]
    elif kind == "NEW": s[op[1]] = op[2]
    return s
def tail_touched(ops, mid=7):
    t = {o[1] for o in ops[mid:]}
    t |= {o[2] for o in ops[mid:] if o[0] == "MOV"}
    return t

def gen_problem_exact(seed, retries):
    """Exact replica of horizon.py gen_problem; counts +977 retries (depth)."""
    while True:
        rng = random.Random(seed)
        init = {k: rng.randint(3, 30) for k in KEYS}
        extra = ["brackets", "rivets", "gaskets"]
        state, ops = dict(init), []
        while len(ops) < 10:
            live = list(state); roll = rng.random()
            if roll < 0.18: op = ("SET", rng.choice(live), rng.randint(0, 30))
            elif roll < 0.45: op = ("ADD", rng.choice(live), rng.randint(1, 9))
            elif roll < 0.65:
                c = [k for k in live if state[k] > 0]
                if not c: continue
                k = rng.choice(c); op = ("SUB", k, rng.randint(1, min(9, state[k])))
            elif roll < 0.80:
                if len(live) < 2: continue
                a, b = rng.sample(live, 2)
                if state[a] == 0: continue
                op = ("MOV", a, b)
            elif roll < 0.90:
                if len(live) < 4: continue
                op = ("DEL", rng.choice(live))
            else:
                if not extra: continue
                op = ("NEW", extra.pop(0), rng.randint(2, 9))
            if op[0] in ("SET","ADD","SUB","DEL") and op[1] not in state: continue
            if op[0] == "NEW" and op[1] in state: continue
            state = sim_apply(state, op); ops.append(op)
        kinds = {o[0] for o in ops}
        if "DEL" not in kinds or "MOV" not in kinds or len(tail_touched(ops)) < 2:
            seed += 977; retries[0] += 1; continue
        return init, ops

def states_along(init, ops, n=None):
    s, out = dict(init), []
    for op in (ops if n is None else ops[:n]):
        s = sim_apply(s, op); out.append(s)
    return out

print("== counts ==")
cnt = collections.Counter(r["cell"] for r in recs)
print(dict(sorted(cnt.items())), "total", len(recs))
meta = {r["pid"]: r for r in recs if r["cell"] == "meta"}

print("\n== gen_problem replication vs meta; retries; histogram ==")
hist = {}
for pid, m in sorted(meta.items()):
    retries = [0]
    init2, ops2 = gen_problem_exact(700 + pid * 13, retries)
    match = (init2 == m["init"]) and ([list(o) for o in ops2] == m["ops"])
    h = collections.Counter(o[0] for o in m["ops"]); hist[pid] = h
    print(f"pid {pid}: match={match} retries={retries[0]} " +
          " ".join(f"{k}={h.get(k,0)}" for k in ["SET","ADD","SUB","MOV","DEL","NEW"]) +
          "  tail_touched=" + ",".join(m["tail_touched"]))
for k in ["SET","ADD","SUB","MOV","DEL","NEW"]:
    col = [hist[p].get(k, 0) for p in sorted(hist)]
    print(f"  {k}: counts across pids {col}  constant={len(set(col))==1}")

print("\n== truth recompute vs 'want' (off-by-one hunt) ==")
bad = checked = 0
for r in recs:
    if r["cell"] in ("A-INC", "A-CKPT", "A-MONO", "A-CKPT-ack"):
        if r["cell"] == "A-CKPT-ack": continue
        truth = states_along(meta[r["pid"]]["init"], meta[r["pid"]]["ops"])
        want_i = truth[-1] if r["cell"] == "A-MONO" else truth[r["turn"]-1]
        checked += 1
        if r["want"] != want_i: bad += 1; print(f"  MISMATCH {r['cell']} pid={r['pid']} turn={r['turn']}")
    elif r["cell"].startswith("B-"):
        truth = states_along(meta[r["pid"]]["init"], meta[r["pid"]]["ops"])
        checked += 1
        if r["want"] != truth[-1]: bad += 1; print(f"  MISMATCH B pid={r['pid']}")
print(f"checked {checked} want-fields, mismatches {bad}")

print("\n== A-CKPT-ack leaks ==")
acks = [r for r in recs if r["cell"] == "A-CKPT-ack"]
def aclass(raw):
    s = raw.strip().lower()
    if s in ("ok","ok.","'ok'",'"ok"',"ok!"): return "ok"
    if s.startswith("```") or s.startswith("{"): return "json-like"
    if any(k in raw for k in KEYS): return "state-mention"
    return "prose"
print("classes:", dict(collections.Counter(aclass(r["raw"]) for r in acks)))
t1 = [r for r in acks if r["turn"] == 1]
print(f"turn-1 acks (user ASKED full state, harness logged as ack): {len(t1)}")
for r in t1: print(f"  pid {r['pid']}: class={aclass(r['raw'])} ctok={r['usage'].get('completion_tokens')} raw={r['raw'][:60]!r}")
ot = [r for r in acks if r["turn"] != 1 and aclass(r["raw"]) != "ok"]
print(f"non-turn-1 acks not literal 'ok': {len(ot)}")
for r in ot[:10]: print(f"  pid={r['pid']} turn={r['turn']} class={aclass(r['raw'])} ctok={r['usage'].get('completion_tokens')} raw={r['raw'][:60]!r}")
ok_ct = [r["usage"].get("completion_tokens") for r in acks if r["turn"] != 1 and aclass(r["raw"]) == "ok"]
print(f"literal-ok ack completion_tokens: min={min(ok_ct)} max={max(ok_ct)}")

print("\n== CKPT graded turns ==")
for cell in ("A-INC","A-CKPT"):
    print(cell, dict(sorted(collections.Counter(r["turn"] for r in recs if r["cell"]==cell).items())))

inc = {p: {r["turn"]: r for r in recs if r["cell"]=="A-INC" and r["pid"]==p} for p in meta}
ck  = {p: {r["turn"]: r for r in recs if r["cell"]=="A-CKPT" and r["pid"]==p} for p in meta}
mo  = {p: next(r for r in recs if r["cell"]=="A-MONO" and r["pid"]==p) for p in meta}
print("\n== per-pid A table (turn: ok/nwrong) ==")
print("pid | INC t1..t10 | MONO | CKPT t4,t7,t10 | INConset CKPTonset")
onsets_i, onsets_c = {}, {}
for p in sorted(meta):
    irow = " ".join(f"{int(inc[p][t]['ok'])}/{inc[p][t]['nwrong']}" for t in range(1,11))
    crow = " ".join(f"{int(ck[p][t]['ok'])}/{ck[p][t]['nwrong']}" for t in (4,7,10))
    oi = next((t for t in range(1,11) if not inc[p][t]["ok"]), None)
    oc = next((t for t in (4,7,10) if not ck[p][t]["ok"]), None)
    onsets_i[p], onsets_c[p] = oi, oc
    print(f"{p:3d} | {irow} | {int(mo[p]['ok'])}/{mo[p]['nwrong']} | {crow} | {oi} {oc}")
w_im = sum(1 for p in meta if inc[p][10]["ok"] and not mo[p]["ok"])
w_mi = sum(1 for p in meta if mo[p]["ok"] and not inc[p][10]["ok"])
w_ic = sum(1 for p in meta if inc[p][10]["ok"] and not ck[p][10]["ok"])
w_ci = sum(1 for p in meta if ck[p][10]["ok"] and not inc[p][10]["ok"])
print(f"paired@turn10: INC>MONO {w_im} : MONO>INC {w_mi}; INC>CKPT {w_ic} : CKPT>INC {w_ci}")
print("onsets INC:", collections.Counter(onsets_i.values()))
print("onsets CKPT(4/7/10 only):", collections.Counter(onsets_c.values()))

print("\n== finish reasons ==")
fin = collections.defaultdict(collections.Counter)
for r in recs:
    if "finish" in r: fin[r["cell"]][str(r["finish"])] += 1
for k in sorted(fin): print(k, dict(fin[k]))
print("MONO raw tails:")
for r in recs:
    if r["cell"]=="A-MONO": print(f"  pid={r['pid']} fin={r['finish']} nwrong={r['nwrong']} ctok={r['usage'].get('completion_tokens')} tail={r['raw'][-70:]!r}")

print("\n== probe B verification ==")
for r in recs:
    if not r["cell"].startswith("B-"): continue
    m = meta[r["pid"]]; truth = states_along(m["init"], m["ops"])
    correct = states_along(m["init"], m["ops"], 7)
    if r["cell"] in ("B-corrupt-plain","B-corrupt-hint"):
        sm = dict(correct[-1]); sm[r["corrupt_field"]] = r["corrupt_from"]
        simc = states_along(sm, m["ops"][7:])[-1]
        rc = "corrected" if r["got"]==truth[-1] else ("propagated" if r["got"]==simc else "other")
        mm = "" if rc == r["outcome"] else f"  CODING-MISMATCH(log={r['outcome']})"
        hv = any(correct[j].get(r["corrupt_field"])==r["corrupt_from"] and correct[j].get(r["corrupt_field"])!=correct[-1][r["corrupt_field"]] for j in range(5,-1,-1))
        tt = r["corrupt_field"] in tail_touched(m["ops"])
        drift = abs(r["corrupt_from"] - correct[-1][r["corrupt_field"]])
        print(f"  pid={r['pid']} {r['cell']:16s} ok={int(r['ok'])} out={r['outcome']:10s} field={r['corrupt_field']:8s} from={r['corrupt_from']} true={correct[-1][r['corrupt_field']]} drift={drift} histVal={hv} tailTouched={tt}{mm}")
    else:
        print(f"  pid={r['pid']} {r['cell']:16s} ok={int(r['ok'])} out={r['outcome']:10s}")
cp={r["pid"]:r for r in recs if r["cell"]=="B-corrupt-plain"}; ch={r["pid"]:r for r in recs if r["cell"]=="B-corrupt-hint"}
kp={r["pid"]:r for r in recs if r["cell"]=="B-clean-plain"}; kh={r["pid"]:r for r in recs if r["cell"]=="B-clean-hint"}
print("pid | cP cH kP kH (ok) | outcome cP,cH")
for p in sorted(cp): print(f"{p:3d} | {int(cp[p]['ok'])}  {int(ch[p]['ok'])}  {int(kp[p]['ok'])}  {int(kh[p]['ok'])} | {cp[p]['outcome']},{ch[p]['outcome']}")
w_h = sum(1 for p in cp if ch[p]["ok"] and not cp[p]["ok"]); w_ph = sum(1 for p in cp if cp[p]["ok"] and not ch[p]["ok"])
print(f"paired hint-vs-plain on corrupt: hint>{w_h} plain>{w_ph} of 8")

print("\n== probe C ==")
for r in recs:
    if r["cell"].startswith("C-") and r["cell"] != "C-MONO":
        g = r.get("got"); fl = {k: r.get(k) for k in ("viol_ok","square_valid","preserved","over_repair","parse","ok")}
        print(f"  {r['cell']:10s} rep={r['rep']} viol={g.get('violations') if isinstance(g,dict) else None} {fl}")
CONFLICT_ROWS=[["A","B","C","D"],["B","C","D","A"],["A","B","D","C"]]
BENIGN_ROWS=[["A","B","C","D"],["B","A","D","C"],["C","D","A","B"]]
def ccf(rows): return all(len(set(r[c] for r in rows))==len(rows) for c in range(4))
for nm, rows in (("conflict",CONFLICT_ROWS),("benign",BENIGN_ROWS)):
    for sz in range(4):
        keeps=[tuple(i for i in range(3) if i not in c) for c in itertools.combinations(range(3),sz) if ccf([rows[i] for i in range(3) if i not in c])]
        if keeps:
            print(f"  {nm}: minimal_sz={sz} keeps={keeps} -> minimal violation set(s)={ [tuple(sorted(set(range(3))-set(k))) for k in keeps] }"); break

print("\n== parse failures ==")
nf=0
for r in recs:
    if r["cell"].startswith("C-"):
        if r.get("parse") is False: nf+=1; print(f"  C-parse-fail {r['cell']} rep={r['rep']} raw={r['raw'][:90]!r}")
    elif "got" in r and r["got"] is None:
        nf+=1; print(f"  parse-fail {r['cell']} pid={r.get('pid')} turn={r.get('turn')} raw={r['raw'][:90]!r}")
print("total parse failures:", nf)

print("\n== nwrong distributions ==")
for cell in ("A-INC","A-CKPT","A-MONO"):
    print(cell, dict(sorted(collections.Counter(r["nwrong"] for r in recs if r["cell"]==cell).items())))
print("INC turn-1 ok:", sum(r["ok"] for r in recs if r["cell"]=="A-INC" and r["turn"]==1), "/10")
print("INC ckpt-turn ok (4/7/10):", [sum(r["ok"] for r in recs if r["cell"]=="A-INC" and r["turn"]==t) for t in (4,7,10)], "/10 each")
print("MONO nwrong:", [mo[p]["nwrong"] for p in sorted(mo)])
