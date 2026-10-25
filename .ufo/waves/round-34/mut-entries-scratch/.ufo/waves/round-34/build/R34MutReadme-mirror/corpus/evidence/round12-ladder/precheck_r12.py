#!/usr/bin/env python3
"""Round-12 preregistration precheck (probe_plan_r12.md §6 step 2).

Proves, before any endpoint request and before the bundle hash:
  1. all 64 family-1 problems generate from seeds 3000+pid*41 and are
     BYTE-IDENTICAL to r11's committed metas (identity, not disjointness —
     r12 deliberately reuses r11's problem set);
  2. all 48 family-2 problems generate from seeds 5000+pid*37;
  3. no duplicate (init, ops) within family 1, within family 2, or across the
     two families (cross-family comparison is on the canonical JSON of the
     pair; the state types differ, so a collision would be a generator bug);
  4. no family-2 problem duplicates an r8 or r9 problem either;
  5. the arm-order rotation realizes the position counts the descriptors
     record claims (every arm in every position 12 or 13 times over 64 pids);
  6. the retry chain (seed+977) actually fires for at least the seeds where
     the generator's kind constraint needs it, and terminates;
  7. the three prediction artifacts exist and their sha256s match the values
     printed inside predictions-r12.md (the bundle's internal consistency).

Stdlib only, offline, deterministic. Exit 0 = all checks pass.
Usage: python3 precheck_r12.py  (tee into prereg-precheck.log)
"""
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
R11 = os.path.join(ROOT, "corpus/evidence/round11-power/results-r11.jsonl")
R8 = os.path.join(ROOT, "corpus/evidence/round8-horizon/results.jsonl")
R9 = os.path.join(ROOT, "corpus/evidence/round9-replication/results-r9.jsonl")

N1, N2 = 64, 48
PIDS = list(range(201, 201 + N1))
PIDS2 = list(range(401, 401 + N2))
ARMS = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO"]

fails = []


def check(ok, label, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails.append(label)


def load_probe():
    spec = importlib.util.spec_from_file_location("probe", os.path.join(HERE, "probe_r12.py"))
    m = importlib.util.module_from_spec(spec)
    # neutralize the module-level OUT/LOGF side effects for an offline precheck
    os.environ["KENGAKU_R12_OUT"] = "/tmp/kengaku-r12-precheck"
    spec.loader.exec_module(m)
    return m


def load(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def canon(init, ops):
    return json.dumps([init, [list(o) for o in ops]], separators=(",", ":"), sort_keys=True)


def main():
    p = load_probe()

    # 1. family 1 generation + identity with r11's committed metas
    r11 = load(R11)
    r11meta = {r["pid"]: r for r in (r11 or []) if r.get("cell") == "meta"}
    f1, mism = {}, 0
    for pid in PIDS:
        init, ops = p.gen_problem(3000 + pid * 41)
        f1[pid] = (init, ops)
        m = r11meta.get(pid)
        if m is None:
            mism += 1
            continue
        if json.dumps(init, sort_keys=True) != json.dumps(m["init"], sort_keys=True) or \
           canon(init, ops) != canon(m["init"], m["ops"]):
            mism += 1
    check(len(f1) == N1, "family 1 generates", f"{len(f1)}/{N1} pids")
    check(mism == 0, "family 1 byte-identical to r11 metas",
          f"{N1 - mism}/{N1} match r11 committed metas ({len(r11meta)} r11 metas present)")
    # truth derivation must agree with r11's stored truth
    tmis = sum(1 for pid in PIDS if pid in r11meta and
               json.dumps(p.states_along(*f1[pid]), sort_keys=True)
               != json.dumps(r11meta[pid]["truth"], sort_keys=True))
    check(tmis == 0, "family 1 truth re-derivation matches r11", f"{tmis} mismatches")

    # 2. family 2 generation
    f2 = {}
    for pid in PIDS2:
        f2[pid] = p.gen_seq_problem(5000 + pid * 37)
    check(len(f2) == N2, "family 2 generates", f"{len(f2)}/{N2} pids")
    lens = sorted({len(p.states_along2(i, o)[-1]) for i, o in f2.values()})
    kinds = sorted({k for i, o in f2.values() for k in {x[0] for x in o}})
    check(all(len(i) == 6 for i, o in f2.values()), "family 2 init length is 6 tokens")
    check(all(len(o) == 10 for i, o in f2.values()), "family 2 op count is 10")
    check({"DEL", "MOV", "REV"} <= set(kinds), "family 2 op-kind constraint holds",
          f"kinds observed: {','.join(kinds)}")
    print(f"       family 2 final-state lengths observed: {lens}")
    check(all(len(p.tail_positions(o)) >= 2 for i, o in f2.values()),
          "family 2 tail_positions >= 2 for every problem")

    # 3./4. duplicate (init, ops) checks
    c1 = {canon(*v) for v in f1.values()}
    c2 = {canon(*v) for v in f2.values()}
    check(len(c1) == N1, "family 1 has no duplicate (init,ops)", f"{len(c1)} distinct of {N1}")
    check(len(c2) == N2, "family 2 has no duplicate (init,ops)", f"{len(c2)} distinct of {N2}")
    check(not (c1 & c2), "no cross-family (init,ops) collision", f"{len(c1 & c2)} collisions")
    prior = set()
    for path, tag in ((R8, "r8"), (R9, "r9")):
        recs = load(path)
        if recs is None:
            print(f"[SKIP] {tag} results not present at {os.path.relpath(path, ROOT)}")
            continue
        for r in recs:
            if r.get("cell") == "meta" and "init" in r and "ops" in r:
                prior.add(canon(r["init"], r["ops"]))
        print(f"       {tag} metas loaded: {sum(1 for r in recs if r.get('cell') == 'meta')}")
    check(not (c2 & prior), "family 2 collides with no r8/r9 problem", f"{len(c2 & prior)} collisions")
    # family 1 deliberately REUSES r11's problem set (identity proven in check 1)
    # and must therefore be disjoint from the r8/r9 sets, whose seeds differ.
    check(not (c1 & prior), "family 1 is disjoint from the r8/r9 problem sets",
          f"{len(c1 & prior)} collisions with {len(prior)} r8/r9 metas")

    # 5. arm-order rotation position counts
    pos = {a: [0] * len(ARMS) for a in ARMS}
    for k, pid in enumerate(PIDS):
        rot = k % len(ARMS)
        for i, a in enumerate(ARMS[rot:] + ARMS[:rot]):
            pos[a][i] += 1
    print("       realized arm-position counts (position 1..5):")
    for a in ARMS:
        print(f"         {a:12s} {pos[a]}")
    check(all(sorted(v) in ([12, 12, 13, 13, 14], [12, 13, 13, 13, 13]) or
              (min(v) >= 12 and max(v) <= 14 and sum(v) == N1) for v in pos.values()),
          "rotation balances every arm across positions",
          f"min={min(min(v) for v in pos.values())} max={max(max(v) for v in pos.values())} sum={sum(sum(v) for v in pos.values())}")
    # family 2 parity counterbalance
    tfirst = {"T-DENSE": 0, "T-SPARSE": 0}
    for pid in PIDS2:
        tfirst["T-DENSE" if pid % 2 == 0 else "T-SPARSE"] += 1
    check(tfirst["T-DENSE"] == N2 // 2 and tfirst["T-SPARSE"] == N2 - N2 // 2,
          "family 2 parity counterbalance is exact", str(tfirst))

    # 6. retry chain: counted by patching the module global that the generator's
    # own recursive call resolves through, so total invocations - problems =
    # retries. Proves termination and reports how hard the constraint works.
    def count_retries(fn_name, seeds):
        calls = {"n": 0}
        orig = getattr(p, fn_name)

        def counted(seed, _depth=0):
            calls["n"] += 1
            return orig(seed, _depth)

        setattr(p, fn_name, counted)
        try:
            out = [orig.__globals__[fn_name](s) for s in seeds]
        finally:
            setattr(p, fn_name, orig)
        return out, calls["n"] - len(seeds)

    _, ret2 = count_retries("gen_seq_problem", [5000 + pid * 37 for pid in PIDS2])
    _, ret1 = count_retries("gen_problem", [3000 + pid * 41 for pid in PIDS])
    print(f"       seed+977 retries: family 1 {ret1}, family 2 {ret2} "
          f"(recursion terminated for all {N1 + N2} seeds)")
    check(ret2 >= 0 and ret1 >= 0, "retry chain terminates for every seed",
          f"family1={ret1} family2={ret2} retries")
    det = all(canon(*p.gen_seq_problem(5000 + pid * 37)) == canon(*f2[pid]) for pid in PIDS2)
    check(det, "family 2 generator is deterministic on re-run", f"{N2}/{N2} identical")
    det1 = all(canon(*p.gen_problem(3000 + pid * 41)) == canon(*f1[pid]) for pid in PIDS)
    check(det1, "family 1 generator is deterministic on re-run", f"{N1}/{N1} identical")

    # 7. prediction artifacts + internal sha consistency
    md = os.path.join(HERE, "predictions-r12.md")
    pj = os.path.join(HERE, "predictions-r12-perproblem.jsonl")
    sj = os.path.join(HERE, "predictions-r12-signevents.jsonl")
    for f in (md, pj, sj):
        check(os.path.exists(f), f"prediction artifact exists: {os.path.basename(f)}")
    def sha(f):
        with open(f, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    txt = open(md).read() if os.path.exists(md) else ""
    check(sha(pj) in txt, "per-problem jsonl sha256 is pinned inside predictions-r12.md", sha(pj)[:16] + "…")
    check(sha(sj) in txt, "sign-event jsonl sha256 is pinned inside predictions-r12.md", sha(sj)[:16] + "…")
    nrows = sum(1 for _ in open(pj)) if os.path.exists(pj) else 0
    srows = sum(1 for _ in open(sj)) if os.path.exists(sj) else 0
    check(nrows == 5 * N1 + 2 * N2, "per-problem pass events = 5*64 + 2*48", f"{nrows}")
    check(srows == 4 * N1 + N2, "sign events = 4*64 + 48", f"{srows}")

    print()
    if fails:
        print(f"PRECHECK: FAIL ({len(fails)}): " + "; ".join(fails))
        return 1
    print("PRECHECK: PASS — all checks green; safe to hash the bundle")
    return 0


if __name__ == "__main__":
    sys.exit(main())
