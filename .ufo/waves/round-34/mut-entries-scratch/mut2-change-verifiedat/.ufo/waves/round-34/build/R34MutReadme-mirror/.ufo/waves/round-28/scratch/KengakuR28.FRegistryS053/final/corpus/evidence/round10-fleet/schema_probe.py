#!/usr/bin/env python3
"""r10-labrat-schema: empirical schema-invariant map of committed probe evidence.

Read-only. Stdlib only. Deterministic (sorted output everywhere, no set iteration
for ordering-sensitive results). Re-runnable: python3 schema_probe.py
Exit 0 always (research probe, not a pass/fail grader).
"""
import json
import os
import sys
from collections import Counter, defaultdict

REPO = "/home/vgpnk/projects/shokunin/kengaku-shokunin"
FILES = [
    ("R8", os.path.join(REPO, "corpus/evidence/round8-horizon/results.jsonl")),
    ("R9", os.path.join(REPO, "corpus/evidence/round9-replication/results-r9.jsonl")),
]

anomalies = []


def flag(msg):
    anomalies.append(msg)
    print(f"  !! ANOMALY: {msg}")


def fmt(v):
    return json.dumps(v, sort_keys=True)


def load(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            recs.append(json.loads(line))  # raises on bad line: loud, not silent
    return recs


def probe(tag, path):
    print("=" * 78)
    print(f"[{tag}] {path}")
    recs = load(path)
    print(f"records: {len(recs)}")
    by_cell = defaultdict(list)
    for r in recs:
        by_cell[r.get("cell")].append(r)
    print("cells: " + ", ".join(f"{c}({len(by_cell[c])})" for c in sorted(by_cell)))
    meta = {r["pid"]: r for r in by_cell.get("meta", [])}

    # ---- meta sanity ----
    print("-- meta sanity --")
    duptruth = []
    for pid in sorted(meta):
        m = meta[pid]
        tlen, oplen = len(m["truth"]), len(m["ops"])
        note = ""
        if tlen != oplen:
            note = "  !! truth_len != ops_len"
            flag(f"{tag} meta pid={pid} truth_len {tlen} != ops_len {oplen}")
        for i in range(tlen - 1):
            if m["truth"][i] == m["truth"][i + 1]:
                duptruth.append((pid, i, i + 1))
        print(f"  pid={pid}: truth_len={tlen} ops_len={oplen} "
              f"init_keys={len(m['init'])} tail_touched={fmt(m.get('tail_touched'))}{note}")
    print(f"  consecutive equal truth states: {duptruth if duptruth else 'none'}")

    # ---- per-cell shape ----
    print("-- per-cell shape --")
    for cell in sorted(by_cell):
        rs = by_cell[cell]
        keysets = Counter(tuple(sorted(r.keys())) for r in rs)
        pids = sorted({r["pid"] for r in rs if "pid" in r})
        turns = sorted({r["turn"] for r in rs if "turn" in r})
        reps = sorted({r["rep"] for r in rs if "rep" in r})
        okc = Counter("ok" in r for r in rs)
        finishes = Counter(r.get("finish", "<absent>") for r in rs)
        reqts = Counter("request_ts" in r for r in rs)
        print(f"  cell={cell}: n={len(rs)} keyset_variants={len(keysets)} "
              f"pids={pids[:12]} turns={turns} reps={reps} "
              f"ok={dict(okc)} finish={dict(finishes)} request_ts={dict(reqts)}")
        if not pids and not reps and cell not in ("filler", "meta"):
            flag(f"{tag} cell={cell} has neither pid nor rep")
        if len(keysets) > 1:
            flag(f"{tag} cell={cell} has {len(keysets)} key-set variants")

    # ---- A-graded invariants (records with ok+pid+turn) ----
    print("-- A-graded (ok+pid+turn) invariants --")
    graded_cells = sorted(c for c, rs in by_cell.items() if c != "meta"
                          and rs and all("ok" in r and "pid" in r and "turn" in r for r in rs))
    graded = [r for c in graded_cells for r in by_cell[c]]
    print(f"  graded cells ({len(graded)} recs): {graded_cells}")

    # want vs truth index (match-set logic; turn-1 must be in matchset)
    want_cells = sorted(c for c in graded_cells
                        if all("want" in r for r in by_cell[c]))
    strict_bad = []
    for cell in want_cells:
        n_ok = 0
        for r in by_cell[cell]:
            tr = meta[r["pid"]]["truth"]
            ms = [k for k, t in enumerate(tr) if r["want"] == t]
            if r["turn"] - 1 < len(tr) and r["want"] == tr[r["turn"] - 1]:
                n_ok += 1
            else:
                strict_bad.append((cell, r["pid"], r["turn"],
                                   [k for k, t in enumerate(tr) if t == r["want"]]))
        n = len(by_cell[cell])
        idxs = sorted({r["turn"] - 1 for r in by_cell[cell]})
        print(f"  {cell}: want==truth[turn-1] {n_ok}/{n} (truth idx used: {idxs})")
    if strict_bad:
        flag(f"{tag} want!=truth[turn-1] violations: {strict_bad[:5]} (n={len(strict_bad)})")
    # which truth index non-A cells actually use
    for cell in want_cells:
        r0 = by_cell[cell][0]
        tr = meta[r0["pid"]]["truth"]
        last = len(tr) - 1
        if all(r["want"] == tr[last] for r in by_cell[cell]) and r0["turn"] - 1 != last:
            print(f"  {cell}: want==truth[{last}] (FINAL state) while turn=1 "
                  f"-> grader must use truth[last] not truth[turn-1]")

    # turn coverage + duplicates
    for cell in graded_cells:
        per = defaultdict(list)
        for r in by_cell[cell]:
            per[r["pid"]].append(r["turn"])
        spans = {p: (min(t), max(t), len(t)) for p, t in per.items()}
        uniform = len(set(spans.values())) == 1
        ex = sorted(spans.items())[0]
        print(f"  {cell}: uniform turn coverage={uniform} e.g. pid={ex[0]} "
              f"turns {ex[1][0]}..{ex[1][1]} n={ex[1][2]}")
        if not uniform:
            flag(f"{tag} cell={cell}: non-uniform turn coverage across pids")
    keyc = Counter((r["cell"], r["pid"], r["turn"]) for r in graded)
    dups = sorted(k for k, n in keyc.items() if n > 1)
    print(f"  duplicate (cell,pid,turn) among graded: {len(dups)}")
    if dups:
        flag(f"{tag} duplicate (cell,pid,turn): {dups[:5]}")
    for cell in sorted(by_cell):
        rs = by_cell[cell]
        if rs and all("rep" in r for r in rs):
            kc = Counter((r["cell"], r.get("pid"), r["turn"], r["rep"]) for r in rs)
            d2 = sorted(k for k, n in kc.items() if n > 1)
            print(f"  cell={cell} rep-keyed: dup(cell,pid,turn,rep)={len(d2)}")
            if d2:
                flag(f"{tag} cell={cell} duplicates incl rep: {d2[:5]}")

    # got / raw / ok / nwrong / finish
    badgot = [(r["cell"], r["pid"], r["turn"], type(r.get("got")).__name__)
              for r in graded if not (r.get("got") is None or isinstance(r.get("got"), dict))]
    print(f"  got not dict-or-None: {len(badgot)}" + (f" {badgot[:3]}" if badgot else ""))
    if badgot:
        flag(f"{tag} got not dict-or-None: n={len(badgot)}")
    noraw = [(r["cell"], r["pid"], r["turn"]) for r in graded
             if not isinstance(r.get("raw"), str) or r.get("raw") == ""]
    print(f"  graded missing/empty raw: {len(noraw)}"
          + (f" by cell {dict(Counter(c for c,_,_ in noraw))}" if noraw else ""))
    if noraw:
        flag(f"{tag} graded cells without usable raw: {sorted({c for c,_,_ in noraw})}")
    allraw = [r for rs in by_cell.values() for r in rs
              if "raw" in r and (not isinstance(r.get("raw"), str) or r.get("raw") == "")]
    print(f"  ALL records missing/empty raw: {len(allraw)}")
    mism_ok, mism_nw = [], []
    for r in graded:
        if "want" in r and isinstance(r.get("got"), dict):
            if r["ok"] != (r["got"] == r["want"]):
                mism_ok.append((r["cell"], r["pid"], r["turn"]))
            if "nwrong" in r:
                diff = [k for k in set(r["got"]) | set(r["want"])
                        if r["got"].get(k) != r["want"].get(k)]
                if r["nwrong"] != len(diff):
                    mism_nw.append((r["cell"], r["pid"], r["turn"], r["nwrong"], len(diff)))
    nw_cells = sorted({r["cell"] for rs in by_cell.values() for r in rs if "nwrong" in r})
    print(f"  ok != (got==want): {len(mism_ok)}; nwrong mismatch (where key exists): {len(mism_nw)}")
    print(f"  nwrong present on cells: {nw_cells}")
    if mism_ok:
        flag(f"{tag} ok inconsistent with got==want: n={len(mism_ok)}")
    if mism_nw:
        flag(f"{tag} nwrong inconsistent with key diff: {mism_nw[:5]}")
    fin_bad = []
    for cell in graded_cells:
        per = defaultdict(list)
        for r in by_cell[cell]:
            per[r["pid"]].append(r)
        for pid, rs in per.items():
            last = max(rs, key=lambda r: r["turn"])
            if last.get("finish") != "stop":
                fin_bad.append((cell, pid, last["turn"], last.get("finish")))
    allfin = Counter(r.get("finish") for r in graded)
    print(f"  graded finish values: {dict(allfin)}; "
          f"final-graded-turn-per-(cell,pid) finish!='stop': {len(fin_bad)} "
          f"{'-> claim HOLDS' if not fin_bad else fin_bad[:5]}")
    if fin_bad:
        flag(f"{tag} final graded turn finish!='stop': {fin_bad[:5]}")

    # ack cells (no ok, carry pid+turn+raw)
    ack_cells = sorted(c for c, rs in by_cell.items() if c != "meta" and rs
                       and all("ok" not in r and "pid" in r and "turn" in r for r in rs))
    for cell in ack_cells:
        graded_fam = [g for g in graded_cells
                      if {r["pid"] for r in by_cell[g]} == {r["pid"] for r in by_cell[cell]}]
        partner = None
        for g in graded_fam:
            gt = {r["turn"] for r in by_cell[g]}
            at = {r["turn"] for r in by_cell[cell]}
            if not (gt & at) and sorted(gt | at) == list(range(1, 11)):
                partner = g
        per = defaultdict(list)
        for r in by_cell[cell]:
            per[r["pid"]].append(r["turn"])
        spans = {p: (min(t), max(t), len(t)) for p, t in per.items()}
        kc = Counter((r["pid"], r["turn"]) for r in by_cell[cell])
        d3 = sorted(k for k, n in kc.items() if n > 1)
        print(f"  ack-cell {cell}: n={len(by_cell[cell])} uniform={len(set(spans.values()))==1} "
              f"dup(pid,turn)={len(d3)} exact-complement-of={partner}")
        if d3:
            flag(f"{tag} ack-cell {cell} duplicates: {d3[:5]}")
        if partner is None:
            flag(f"{tag} ack-cell {cell}: not an exact disjoint complement of a graded cell")

    # ---- B cells ----
    b_cells = sorted(c for c in by_cell if c.startswith("B-"))
    if b_cells:
        print("-- B-cell shape census (corrupt_field, corrupt_from, outcome, healed) --")
        for cell in b_cells:
            shapes = Counter((fmt(r.get("corrupt_field")), fmt(r.get("corrupt_from")),
                              fmt(r.get("outcome")), fmt(r.get("healed")))
                             for r in by_cell[cell])
            print(f"  {cell}: {len(shapes)} distinct shape(s)")
            for s, n in sorted(shapes.items()):
                print(f"      n={n} (corrupt_field,corrupt_from,outcome,healed)=({s[0]},{s[1]},{s[2]},{s[3]})")
        eq_init = eq_got = 0
        tot = 0
        for cell in b_cells:
            for r in by_cell[cell]:
                if r.get("corrupt_field") is None:
                    continue
                tot += 1
                f = r["corrupt_field"]
                if r["corrupt_from"] == meta[r["pid"]]["init"].get(f):
                    eq_init += 1
                if isinstance(r.get("got"), dict) and r["got"].get(f) == r["corrupt_from"]:
                    eq_got += 1
        print(f"  corrupt records n={tot}: corrupt_from==init[field] {eq_init}/{tot}; "
              f"corrupt_from==got[field] {eq_got}/{tot}")

    # ---- C cells ----
    c_cells = sorted(c for c in by_cell if c.startswith("C-"))
    if c_cells:
        print("-- C-cell key-set split --")
        groups = {c: {tuple(sorted(r.keys())) for r in by_cell[c]} for c in c_cells}
        mono_n = len(by_cell.get("C-MONO", []))
        trio_n = sum(len(by_cell[c]) for c in c_cells if c != "C-MONO")
        print(f"  record split: trio={trio_n} vs C-MONO={mono_n} (expected 12 vs 4: "
              f"{(trio_n, mono_n) == (12, 4)})")
        if (trio_n, mono_n) != (12, 4):
            flag(f"{tag} C split {trio_n} vs {mono_n} != 12 vs 4")
        trio_ks = set().union(*[groups[c] for c in c_cells if c != "C-MONO"])
        print(f"  trio share one key-set: {len(trio_ks) == 1}")
        if len(trio_ks) != 1:
            flag(f"{tag} C trio key-sets differ")
        if "C-MONO" in groups and len(groups["C-MONO"]) == 1 and len(trio_ks) == 1:
            mk = next(iter(groups["C-MONO"]))
            tk = next(iter(trio_ks))
            print(f"  C-MONO lacks trio keys: {sorted(set(tk) - set(mk))}")
        gt = Counter(type(r.get("got")).__name__ for c in c_cells for r in by_cell[c])
        print(f"  got value types across C cells: {dict(gt)}")
        if gt.get("list") and gt.get("dict"):
            print("    -> C-MONO got=list-of-lists(4x4 square); trio got=dict{violations,square}: "
                  "grader must branch on cell")
        flags_c = Counter((c, r.get("ok"), r.get("square_valid"), r.get("parse"),
                           r.get("preserved"), r.get("viol_ok"), r.get("over_repair"))
                          for c in c_cells for r in by_cell[c])
        for k, n in sorted(flags_c.items()):
            print(f"    n={n} (cell,ok,square_valid,parse,preserved,viol_ok,over_repair)={k}")

    # ---- filler ----
    if "filler" in by_cell:
        rs = by_cell["filler"]
        print(f"-- filler -- n={len(rs)} raw={dict(Counter(r.get('raw') for r in rs))} "
              f"pid/turn/rep present: 0/0/0 (grader must skip or whitelist)")

    # ---- request_ts / usage / wall_s ----
    ts = sorted({r["request_ts"] for r in recs if "request_ts" in r})
    print(f"-- request_ts on {sum('request_ts' in r for r in recs)} records "
          f"(all str: {all(isinstance(r['request_ts'], str) for r in recs if 'request_ts' in r)})"
          + (f" range {ts[0]}..{ts[-1]}" if ts else ""))
    ut = Counter(tuple(sorted(r["usage"].keys())) for rs in by_cell.values()
                 for r in rs if "usage" in r)
    print(f"-- usage key-tuples: {dict(ut)}")
    ws = Counter(type(r["wall_s"]).__name__ for rs in by_cell.values()
                 for r in rs if "wall_s" in r)
    print(f"-- wall_s types: {dict(ws)}")
    allpids = sorted({r["pid"] for r in recs if "pid" in r})
    print(f"-- pid universe {allpids[0]}..{allpids[-1]} (n={len(allpids)}); "
          f"meta pids match: {allpids == sorted(meta)}")


def main():
    for tag, path in FILES:
        probe(tag, path)
    print("=" * 78)
    print(f"TOTAL ANOMALIES FLAGGED: {len(anomalies)}")
    for i, a in enumerate(anomalies, 1):
        print(f"  {i}. {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
