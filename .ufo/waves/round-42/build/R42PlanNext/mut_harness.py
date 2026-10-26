#!/usr/bin/env python3
"""R40PlanNext cheap mutant harness (calibration pricing, NOT a frozen counter).

  python3 mut_harness.py --lane L --tool sources_adopt --sample N --seed S --jobs J --out results.json

AST operators on one plans/<tool>.py (UTF-8 byte-offset splice, single replacement per mutant):
  cmp   Eq<->NotEq, Lt<->LtE, Gt<->GtE, In<->NotIn, Is<->IsNot
  bool  and<->or
  not   `not x` -> `x`
  ret   `return <int>` / `SystemExit(<int>)` constant n -> (0 if n else 1)
  if    `if <test>:` -> `if False:` (clause removed)
  num   int constant inside a Compare, n -> n+1
A mutant is KILLED when (rc, normalised stdout+stderr) of ANY detector command differs from the unmodified
tool's on the same command (result difference, not an attributed kill), or the run times out. Regions of a
tool that are its own self-test fixtures (EXCLUDE) are never mutated. Read-only on the lane.
"""
import argparse, ast, concurrent.futures as cf, hashlib, json, os, pathlib, random, re, shutil, subprocess, sys, time

OPS_CMP = {ast.Eq: "!=", ast.NotEq: "==", ast.Lt: "<=", ast.LtE: "<", ast.Gt: ">=", ast.GtE: ">",
           ast.In: "not in", ast.NotIn: "in", ast.Is: "is not", ast.IsNot: "is"}
EXCLUDE = {"sources_adopt": [(610, 972)], "state_check": [(3583, 4648)],
           "tip_receipts": [], "mutant_direction_check": [], "round39_c1_audit": []}
TMPRE = re.compile(r"/fast/scratch/\S*|/tmp/\S*|\d+\.\d+s|elapsed=\S+")


def offs(src):
    lines = src.split(b"\n"); acc = [0]
    for l in lines: acc.append(acc[-1] + len(l) + 1)
    return acc


def mutants(path, tool):
    src = pathlib.Path(path).read_bytes(); tree = ast.parse(src); ls = offs(src); out = []
    ex = EXCLUDE.get(tool, [])
    def pos(n, end=False):
        return ls[(n.end_lineno if end else n.lineno) - 1] + (n.end_col_offset if end else n.col_offset)
    def ok(n): return not any(a <= n.lineno <= b for a, b in ex)
    def add(kind, n, a, b, new, desc):
        out.append(dict(kind=kind, line=n.lineno, a=a, b=b, new=new, desc=desc))
    for n in ast.walk(tree):
        if not hasattr(n, "lineno") or not ok(n): continue
        if isinstance(n, ast.Compare):
            # operator token location: search between operands
            left_end = pos(n.left, True)
            for i, (op, comp) in enumerate(zip(n.ops, n.comparators)):
                nxt = pos(comp)
                seg = src[left_end:nxt]
                tok = {ast.Eq: b"==", ast.NotEq: b"!=", ast.Lt: b"<", ast.LtE: b"<=", ast.Gt: b">", ast.GtE: b">=",
                       ast.In: b"in", ast.NotIn: b"not in", ast.Is: b"is", ast.IsNot: b"is not"}[type(op)]
                m = re.search(rb"(?<![<>=!])" + re.escape(tok) + (rb"(?![=])" if tok in (b"<", b">") else b""), seg)
                if m and type(op) in OPS_CMP:
                    add("cmp", n, left_end + m.start(), left_end + m.end(), OPS_CMP[type(op)].encode(),
                        f"{tok.decode()} -> {OPS_CMP[type(op)]}")
                left_end = pos(comp, True)
            for c in n.comparators + [n.left]:
                if isinstance(c, ast.Constant) and type(c.value) is int and not isinstance(c.value, bool):
                    add("num", c, pos(c), pos(c, True), str(c.value + 1).encode(), f"{c.value} -> {c.value+1}")
        elif isinstance(n, ast.BoolOp):
            for i, v in enumerate(n.values[:-1]):
                a = pos(v, True); b = pos(n.values[i + 1])
                m = re.search(rb"\b(and|or)\b", src[a:b])
                if m:
                    add("bool", n, a + m.start(), a + m.end(), b"or" if m.group(1) == b"and" else b"and",
                        f"{m.group(1).decode()} -> {'or' if m.group(1)==b'and' else 'and'}")
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            add("not", n, pos(n), pos(n.operand), b"", "not x -> x")
        elif isinstance(n, ast.Return) and isinstance(n.value, ast.Constant) and type(n.value.value) is int:
            v = n.value.value; add("ret", n.value, pos(n.value), pos(n.value, True), str(0 if v else 1).encode(), f"return {v} -> {0 if v else 1}")
        elif isinstance(n, ast.Call) and getattr(n.func, "id", "") == "SystemExit" and n.args \
                and isinstance(n.args[0], ast.Constant) and type(n.args[0].value) is int:
            c = n.args[0]; v = c.value; add("ret", c, pos(c), pos(c, True), str(0 if v else 1).encode(), f"SystemExit({v}) -> {0 if v else 1}")
        elif isinstance(n, ast.If):
            add("if", n.test, pos(n.test), pos(n.test, True), b"False", "if-test -> False")
    # dedupe
    seen = set(); res = []
    for m in out:
        k = (m["a"], m["b"], m["new"])
        if k in seen: continue
        seen.add(k); m["src"] = src[m["a"]:m["b"]].decode(errors="replace"); res.append(m)
    return src, res


def norm(b): return TMPRE.sub("<p>", b.decode(errors="replace"))


def detectors(tool, S, lane):
    w = S + "/w"
    if tool == "sources_adopt": return [["--selftest"]]
    if tool == "state_check": return [["--selftest"], ["--root", "@ROOT@", "--summary"]]
    if tool == "mutant_direction_check": return [["--lane", lane, "--work", w]]
    if tool == "tip_receipts":
        return [["--lane", lane, "--list"], ["--lane", lane, "--only", "round38/build-pmars", "--work", w],
                ["--lane", lane, "--only", "round35", "--work", w], ["--lane", lane, "--only", "round36/regex-log-probe.txt", "--work", w]]
    if tool == "round39_c1_audit": return [["--lane", lane, "--battery", "r38", "--work", w]]


def tree(d, tool, lane, srcbytes):
    """state_check locates its corpus from __file__ (parents[1]): give each mutant a lane-shaped tree of symlinks."""
    os.makedirs(d + "/plans", exist_ok=True)
    for e in os.listdir(lane):
        if e != "plans" and not os.path.lexists(f"{d}/{e}"): os.symlink(f"{lane}/{e}", f"{d}/{e}")
    for e in os.listdir(lane + "/plans"):
        if e != tool + ".py" and not os.path.lexists(f"{d}/plans/{e}"): os.symlink(f"{lane}/plans/{e}", f"{d}/plans/{e}")
    pathlib.Path(f"{d}/plans/{tool}.py").write_bytes(srcbytes)
    return f"{d}/plans/{tool}.py"


def run_one(pyfile, args_list, lane, tmp, timeout):
    res = []
    root = str(pathlib.Path(pyfile).resolve().parents[1])
    for args in args_list:
        args = [root if x == "@ROOT@" else x for x in args]
        env = dict(os.environ, TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")
        try:
            p = subprocess.run(["python3", pyfile, *args], cwd=lane, env=env, capture_output=True, timeout=timeout)
            res.append((p.returncode, norm(p.stdout + p.stderr)))
        except subprocess.TimeoutExpired:
            res.append(("TIMEOUT", "")); break
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True); ap.add_argument("--tool", required=True)
    ap.add_argument("--sample", type=int, default=0); ap.add_argument("--seed", type=int, default=40)
    ap.add_argument("--jobs", type=int, default=6); ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--scratch", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--only-kinds", default="")
    a = ap.parse_args()
    lane = str(pathlib.Path(a.lane).resolve()); tool = a.tool
    path = f"{lane}/plans/{tool}.py"
    src, ms = mutants(path, tool)
    if a.only_kinds: ms = [m for m in ms if m["kind"] in a.only_kinds.split(",")]
    total = len(ms)
    if a.sample and a.sample < total: random.Random(a.seed).shuffle(ms); ms = ms[:a.sample]
    ms.sort(key=lambda m: m["line"])
    S = a.scratch; os.makedirs(S + "/w", exist_ok=True)
    dets = detectors(tool, S, lane)
    use_tree = tool == "state_check"
    if use_tree: path = tree(S + "/base", tool, lane, src)
    t0 = time.time(); base = run_one(path, dets, lane, S, a.timeout)
    print(f"BASE tool={tool} rc={[b[0] for b in base]} t={time.time()-t0:.1f}s population={total} sampled={len(ms)}", flush=True)
    # determinism check of baseline
    base2 = run_one(path, dets, lane, S, a.timeout)
    stable = base == base2
    print(f"BASE-STABLE {stable}", flush=True)

    def job(i):
        m = ms[i]; d = f"{S}/m/{tool}/{i}"; os.makedirs(d, exist_ok=True)
        new = src[:m["a"]] + m["new"] + src[m["b"]:]
        if use_tree: f = tree(d, tool, lane, new)
        else:
            f = f"{d}/{tool}.py"; pathlib.Path(f).write_bytes(new)
        try: compile(pathlib.Path(f).read_text(), f, "exec")
        except SyntaxError as e: shutil.rmtree(d, ignore_errors=True); return i, "invalid", str(e)[:60]
        r = run_one(f, dets, lane, d, a.timeout)
        shutil.rmtree(d, ignore_errors=True)
        if any(x[0] == "TIMEOUT" for x in r): return i, "killed-timeout", ""
        which = [k for k, (x, y) in enumerate(zip(r, base)) if x != y]
        return i, ("killed" if which else "survived"), ",".join(map(str, which))
    d0 = f"{S}/idc"; os.makedirs(d0, exist_ok=True)
    if use_tree: f0 = tree(d0, tool, lane, src)
    else: f0 = f"{d0}/{tool}.py"; pathlib.Path(f0).write_bytes(src)
    ident = run_one(f0, dets, lane, d0, a.timeout) == base
    print(f"IDENTITY-COPY-EQUALS-BASE {ident}", flush=True)
    out = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for i, st, info in ex.map(job, range(len(ms))):
            m = ms[i]; out.append(dict(m, status=st, info=info, src_b=None, new=m["new"].decode()))
            for k in ("a", "b"): pass
    cnt = {}
    for o in out: cnt[o["status"]] = cnt.get(o["status"], 0) + 1
    byk = {}
    for o in out:
        k = byk.setdefault(o["kind"], {"n": 0, "surv": 0}); k["n"] += 1; k["surv"] += o["status"] == "survived"
    print("RESULT", tool, json.dumps(cnt), "by_kind", json.dumps(byk))
    pathlib.Path(a.out).write_text(json.dumps(dict(tool=tool, population=total, sampled=len(ms), counts=cnt, by_kind=byk,
                                                   base_stable=stable, identity_ok=ident, sha=hashlib.sha256(src).hexdigest(), mutants=out), indent=1))
    shutil.rmtree(S + "/m", ignore_errors=True)


if __name__ == "__main__":
    main()
