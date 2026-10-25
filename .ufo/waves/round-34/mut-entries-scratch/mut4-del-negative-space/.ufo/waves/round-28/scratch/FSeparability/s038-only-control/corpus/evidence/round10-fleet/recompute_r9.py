#!/usr/bin/env python3
"""Recompute replication.md SUMMARY claims from results-r9.jsonl (read-only)."""
import json, math, collections

P = "/home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round9-replication/results-r9.jsonl"
recs = [json.loads(l) for l in open(P)]

meta = [r for r in recs if r.get("cell") == "meta" and "init" in r]
scored = [r for r in recs if "ok" in r and "nwrong" in r]
fillers = [r for r in recs if "raw" in r and "ok" not in r and "init" not in r]
errors = [r for r in recs if "error" in r]
print(f"total={len(recs)} meta={len(meta)} scored={len(scored)} filler={len(fillers)} error={len(errors)}")

# group scored by (cell, pid); final graded turn = max turn per (cell,pid)
by = collections.defaultdict(dict)
for r in scored:
    by[(r["cell"], r["pid"])][r["turn"]] = r

cells = sorted({c for c, _ in by})
print("cells:", cells, "trajs:", len(by))

summary = {}
for cell in cells:
    passes = 0; nw = []
    for pid in sorted({p for c, p in by if c == cell}):
        final = by[(cell, pid)][max(by[(cell, pid)])]
        if final["ok"]:
            passes += 1
        nw.append(final["nwrong"])
    mean_nw = sum(nw) / len(nw)
    summary[cell] = (passes, len(nw), mean_nw)
    print(f"{cell}: {passes}/{len(nw)}  mean final nwrong {mean_nw:.3f}")

# claimed: A-INC 4/8 0.500; A-CKPT4710 2/8 0.875; A-CKPT710 2/8 1.375; A-MONO 0/8 2.250
claim = {"A-INC": (4, 8, 0.500), "A-CKPT4710": (2, 8, 0.875),
         "A-CKPT710": (2, 8, 1.375), "A-MONO": (0, 8, 2.250)}
for c, (p, n, m) in claim.items():
    got = summary.get(c)
    ok = got == (p, n, m) if got else False
    print(f"CLAIM {c} {p}/{n} {m}: {'MATCH' if ok else 'MISMATCH got=' + repr(got)}")

# sign tests on final pass booleans
def paired(a, b):
    wa = sum(1 for pid in range(101, 109)
             if by[(a, pid)][max(by[(a, pid)])]["ok"] and not by[(b, pid)][max(by[(b, pid)])]["ok"])
    wb = sum(1 for pid in range(101, 109)
             if by[(b, pid)][max(by[(b, pid)])]["ok"] and not by[(a, pid)][max(by[(a, pid)])]["ok"])
    ties = 8 - wa - wb
    n = wa + wb
    if n == 0:
        p = 1.0
    else:
        lo = sum(math.comb(n, k) for k in range(0, min(wa, wb) + 1)) / 2 ** n
        p = 2 * min(lo, 1 - lo + math.comb(n, min(wa, wb)) / 2 ** n) if wa != wb else 1.0
        # exact two-sided: 2*min(P(X<=k),P(X>=k)) with k=min(wa,wb)
        k = min(wa, wb)
        ple = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
        pge = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
        p = min(1.0, 2 * min(ple, pge))
    return wa, wb, ties, p

for a, b in [("A-INC", "A-CKPT4710"), ("A-CKPT4710", "A-CKPT710"),
             ("A-CKPT710", "A-MONO"), ("A-INC", "A-MONO")]:
    wa, wb, ties, p = paired(a, b)
    print(f"SIGN {a} vs {b}: first={wa} second={wb} ties={ties} p={p:.3f}")

# onset for INC: first turn with ok False per pid
onsets = []
for pid in range(101, 109):
    turns = sorted(by[("A-INC", pid)])
    first_bad = next((t for t in turns if not by[("A-INC", pid)][t]["ok"]), None)
    onsets.append(first_bad)
nonperfect = [o for o in onsets if o is not None]
print("INC onsets:", onsets, "mean(non-perfect) =", (sum(nonperfect) / len(nonperfect)) if nonperfect else None,
      f"({len(nonperfect)} non-perfect)")

# finish reasons at final graded turn per cell
for cell in cells:
    fins = collections.Counter()
    for pid in range(101, 109):
        final = by[(cell, pid)][max(by[(cell, pid)])]
        fins[(final["finish"], final.get("parse_ok", final.get("parsed", "n/a")))] += 1
    print(f"final finish {cell}: {dict(fins)}")

# ack compliance: filler records whose raw starts with 'ok'
for cell in ["A-CKPT4710-ack", "A-CKPT710-ack"]:
    acks = [r for r in recs if r.get("cell") == cell]
    ok = sum(1 for r in acks if str(r.get("raw", "")).strip().lower().startswith("ok"))
    print(f"ACK {cell}: {ok}/{len(acks)} = {ok/len(acks)*100:.1f}%")

# r8 vs r9 ladder table cross-check source
print("INC final-turn finish reasons:",
      dict(collections.Counter(by[("A-INC", p)][max(by[("A-INC", p)])]["finish"] for p in range(101, 109))))
