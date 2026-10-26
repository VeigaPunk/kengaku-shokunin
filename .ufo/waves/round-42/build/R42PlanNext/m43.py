"""R42PlanNext cheap row-priced mutant harness (calibration pricing, NOT a frozen counter).
  python3 m43.py --lane L --scratch S --out res.json [--jobs N] [--only ROW,ROW]
For each advertised-but-unpriced row of tip_receipts.py / sources_adopt.py: AST mutants inside the row's implementing
lines (+ hand mutants where the AST operators reach nothing). Kill = (rc, normalised output [, post-state]) of ANY fixture
differs from the unmodified tool's on the same fixture. Detector sets: 'bat' = lane's battery41 (+ --selftest for sources),
'wit' = wit43.py. A mutant survives when neither kills it."""
import argparse, concurrent.futures as cf, importlib.util, json, os, pathlib, re, shutil, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mut_harness as mh
import wit43

PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
TOOLS = {"tr": "tip_receipts", "sa": "sources_adopt"}

WIN = {  # row -> (tool, [(a,b)...], note)
    "TR01": ("tr", [(253, 261)], "--list classifies and runs nothing"),
    "TR02": ("tr", [(249, 251)], "--only SUBSTR restricts the population"),
    "TR03": ("tr", [(297, 305)], "--jobs N runs probes in parallel"),
    "TR04": ("tr", [(263, 266)], "scratch parent = --work, else TMPDIR, else platform temp"),
    "TR05": ("tr", [(138, 157)], "command resolved from the script's own Run as: line"),
    "TR06": ("tr", [(160, 184)], "doc= provenance of SKILL/README"),
    "TR07": ("tr", [(271, 276)], "toplevel/HEAD equality guards are 2"),
    "TR08": ("tr", [(201, 211)], "every probe re-run inside the clone"),
    "TR09": ("tr", [(186, 194), (326, 330)], "stdout byte-compared; first_diff"),
    "TR10": ("tr", [(245, 248)], "a table-mapped file enters the comparison"),
    "TR11": ("tr", [(97, 102)], "derived mapping is kind=byte origin=derived"),
    "TR12": ("tr", [(287, 294)], "script gone -> skip probe-script-absent"),
    "TR13": ("tr", [(318, 325)], "temp-paths receipt re-run, masked; other diff is differ"),
    "TR14": ("tr", [(333, 338)], "--tamper repeatable and comma-splittable"),
    "TR15": ("tr", [(214, 226), (344, 355)], "one byte flipped, same fresh output re-compared"),
    "TR16": ("tr", [(339, 341)], "no --tamper -> one control on the cheapest byte-equal receipt"),
    "TR17": ("tr", [(270, 270)], "clone failure exits 2"),
    "TR18": ("tr", [(356, 357)], "cleanup / work dir removed on exit"),
    "TR20": ("tr", [(203, 204)], "probe TMPDIR/TEMP/TMP inside the work dir"),
    "SA01": ("sa", [(143, 182), (1071, 1079)], "0 gates an append and prints the append block"),
    "SA02": ("sa", [(304, 348), (463, 488)], "2 unreadable quote artifact"),
    "SA03": ("sa", [(559, 560)], "4 malformed staged row (quote mode)"),
    "SA04": ("sa", [(561, 562)], "6 quote over the 25-word cap"),
    "SA05": ("sa", [(563, 564)], "7 quote absent from artifact bytes"),
    "SA06": ("sa", [(565, 566)], "8 quote bound to mismatched URL"),
    "SA07": ("sa", [(567, 568)], "9 quote has no url-map entry"),
    "SA08": ("sa", [(1048, 1053)], "--access-date required/ISO with --admit-ids"),
    "SA09": ("sa", [(1065, 1067)], "--attest-opened prints attested:"),
    "SA10": ("sa", [(1074, 1076)], "--out writes the block"),
    "SA11": ("sa", [(192, 242)], "--scope-to-admit narrows refusals"),
    "SA12": ("sa", [(621, 627), (968, 972)], "--selftest case accounting"),
}
HAND = [  # (row, tool, old, new) single-occurrence text mutants where AST operators reach nothing
    ("TR20", "tr", "TMPDIR=str(tmpdir), TEMP=str(tmpdir), TMP=str(tmpdir), ", "TEMP=str(tmpdir), TMP=str(tmpdir), "),
    ("TR20", "tr", "TMPDIR=str(tmpdir), TEMP=str(tmpdir), TMP=str(tmpdir), ", "TMPDIR=str(tmpdir), TMP=str(tmpdir), "),
    ("TR20", "tr", "TMPDIR=str(tmpdir), TEMP=str(tmpdir), TMP=str(tmpdir), ", "TMPDIR=str(tmpdir), TEMP=str(tmpdir), "),
    ("TR18", "tr", "        shutil.rmtree(ws, ignore_errors=True)", "        pass"),
    ("TR17", "tr", '"--shared", str(lane), str(clone)], check=True)', '"--shared", str(lane), str(clone)], check=False)'),
    ("TR04", "tr", 'dir=str(work_parent) if work_parent else None', 'dir=None'),
    ("TR03", "tr", "max_workers=jobs", "max_workers=1"),
    ("TR16", "tr", "min(equal, key=lambda r: len(results[r][\"blob\"]))", "max(equal, key=lambda r: len(results[r][\"blob\"]))"),
    ("TR15", "tr", "nb = b ^ 0x01\n            return", "nb = b ^ 0x02\n            return"),
    ("TR15", "tr", "start = len(data) // 2", "start = 0"),
    ("TR08", "tr", "cwd=str(clone), env=env", "cwd=str(clone.parent), env=env"),
    ("TR19", "tr", "        shutil.rmtree(ws, ignore_errors=True)", "        (lane / 'leak.txt').write_text('x'); shutil.rmtree(ws, ignore_errors=True)"),
    ("TR07", "tr", "        top = git(clone, \"rev-parse\", \"--show-toplevel\")", "        top = git(clone, \"rev-parse\", \"--show-toplevel\")  # same"),
    ("SA10", "sa", "args.out.write_text(text, encoding=\"utf-8\")", "pass"),
    ("SA09", "sa", 'print("  attested: the caller asserts every requested source was opened on "', 'print("  attested: the caller asserts every requested source was opened on x"'),
]
HAND = [h for h in HAND if h[0] != "TR07"]  # no-op text mutant, dropped
WIN["TR19"] = ("tr", [(356, 357)], "the lane is read only")


class Ctx:
    def __init__(self, root):
        self.root = pathlib.Path(root).resolve()
        self.ENV = {"PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
                    "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
                    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
                    "GIT_CEILING_DIRECTORIES": str(self.root.parent)}

    def sh(self, *argv, cwd=None, check=True):
        r = subprocess.run([str(a) for a in argv], cwd=cwd, env=self.ENV, capture_output=True, text=True)
        if check and r.returncode: raise RuntimeError(f"{argv[:3]} rc={r.returncode} {r.stderr[-200:]}")
        return r

    def write(self, path, text):
        p = pathlib.Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        (p.write_bytes if isinstance(text, bytes) else p.write_text)(text); return p

    def init(self, dest):
        dest = pathlib.Path(dest); dest.mkdir(parents=True, exist_ok=True)
        self.sh("git", "-C", str(dest), "init", "-q", "-b", "master"); return dest

    def git(self, repo, *args, check=True):
        return self.sh("git", "-C", str(repo), *args, check=check)


def loadmod(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def build_fixtures(lane, S):
    """-> list of dict(set, tool, fid, dir, argv, env, post, cwd_rel)"""
    fx = []
    ctx = Ctx(S + "/fx")
    for f in sorted(pathlib.Path(lane, "plans/battery41").glob("*.py")):
        m = loadmod(f, "b41_" + f.stem)
        for k, e in enumerate(m.FIXTURES):
            d = pathlib.Path(S + f"/fx/bat/{f.stem}/f{k:03d}"); d.mkdir(parents=True)
            argv = e["build"](ctx, d)
            tool = {"receipts": "tr", "sources": "sa"}[e["tool"]]
            fx.append(dict(set="bat", tool=tool, fid=e["fid"], dir=d, argv=argv, env={}, post=None))
    for tool, lst in (("tr", wit43.FIXTURES_TR), ("sa", wit43.FIXTURES_SA)):
        for k, e in enumerate(lst):
            d = pathlib.Path(S + f"/fx/wit/{tool}/f{k:03d}"); d.mkdir(parents=True)
            argv = e["build"](ctx, d)
            fx.append(dict(set="wit", tool=tool, fid=e["fid"], dir=d, argv=argv, env=e.get("env", {}), post=e.get("post")))
    fx.append(dict(set="bat", tool="sa", fid="sa-standing-selftest", dir=None, argv=["--selftest"], env={}, post=None))
    return fx


TMPRE = re.compile(r"tip-receipts-[A-Za-z0-9_]{8}")


def run_fx(toolpath, fx, runroot, timeout=60):
    rr = pathlib.Path(runroot); rr.mkdir(parents=True, exist_ok=True)
    if fx["dir"] is not None:
        rd = rr / "d"; shutil.copytree(fx["dir"], rd, symlinks=True)
    else:
        rd = rr / "d"; rd.mkdir()
    wrk = rr / "wrk"; wrk.mkdir()
    base = str(fx["dir"]) if fx["dir"] is not None else None

    def sub(t):
        if base: t = t.replace(base, str(rd))
        t = t.replace("@D@", str(rd))
        t = re.sub(r"\{WORK:([a-z]+)\}", lambda m: str(rr / "wd" / m.group(1)), t)
        t = t.replace("{WORK}", str(wrk))
        return t
    argv = [sub(t) for t in fx["argv"]]
    for t in argv:
        for m in re.finditer(re.escape(str(rr)) + r"/wd/[a-z]+", t): pathlib.Path(m.group(0)).mkdir(parents=True, exist_ok=True)
    env = {"PATH": PATH, "HOME": str(rr / "home"), "TMPDIR": str(rr / "tmp"), "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
           "GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@x.invalid", "GIT_COMMITTER_NAME": "f", "GIT_COMMITTER_EMAIL": "f@x.invalid"}
    (rr / "home").mkdir(); (rr / "tmp").mkdir()
    for k, v in fx["env"].items():
        env[k] = sub(v)
        pathlib.Path(env[k]).mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run(["python3", toolpath, *argv], cwd=str(rd), env=env, capture_output=True, timeout=timeout)
        o = p.stdout + p.stderr; rc = p.returncode
    except subprocess.TimeoutExpired:
        o = b"TIMEOUT"; rc = "TIMEOUT"
    txt = o.decode(errors="replace").replace(str(rr), "<R>")
    txt = TMPRE.sub("tip-receipts-<x>", txt)
    txt = re.sub(r'File "[^"]*(tip_receipts|sources_adopt)\.py"', 'File "<tool>"', txt)
    txt = re.sub(r"line \d+, in", "line N, in", txt)   # tracebacks of mutated copies shift
    post = ""
    if fx["tool"] == "tr" and fx.get("post"):
        lst = sorted(str(q.relative_to(rr)) for q in rr.rglob("*") if q.parts[len(rr.parts)] in ("wrk", "wd"))
        lane = pathlib.Path(rd / "lane")
        st = subprocess.run(["git", "-C", str(lane), "status", "--porcelain", "--ignored"], capture_output=True, text=True).stdout if lane.is_dir() else ""
        post = f"|WORK {lst}|STATUS {st!r}"
    elif fx["tool"] == "sa" and fx.get("post"):
        q = rd / fx["post"]; post = "|OUT " + (q.read_text() if q.exists() else "absent")
    shutil.rmtree(rr, ignore_errors=True)
    return (rc, txt + post)


def mutate_candidates(lane, tool_key):
    name = TOOLS[tool_key]; mh.EXCLUDE[name] = []
    src, ms = mh.mutants(f"{lane}/plans/{name}.py", name)
    return src, ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True); ap.add_argument("--scratch", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8); ap.add_argument("--only", default="")
    ap.add_argument("--build-only", action="store_true")
    a = ap.parse_args()
    lane = str(pathlib.Path(a.lane).resolve()); S = a.scratch
    shutil.rmtree(S + "/fx", ignore_errors=True); shutil.rmtree(S + "/runs", ignore_errors=True)
    fx = build_fixtures(lane, S)
    print(f"FIXTURES bat={sum(1 for f in fx if f['set']=='bat')} (tr={sum(1 for f in fx if f['set']=='bat' and f['tool']=='tr')} sa={sum(1 for f in fx if f['set']=='bat' and f['tool']=='sa')}) "
          f"wit={sum(1 for f in fx if f['set']=='wit')} (tr={sum(1 for f in fx if f['set']=='wit' and f['tool']=='tr')} sa={sum(1 for f in fx if f['set']=='wit' and f['tool']=='sa')})", flush=True)
    if a.build_only: return
    srcs = {}; refs = {}
    for tk, name in TOOLS.items():
        pth = f"{lane}/plans/{name}.py"; srcs[tk] = pathlib.Path(pth).read_bytes()
    # reference results, twice (stability)
    t0 = time.time()
    def ref(tk, f, rep):
        return run_fx(f"{lane}/plans/{TOOLS[tk]}.py", f, f"{S}/runs/ref{rep}/{tk}/{f['set']}/{f['fid']}")
    unstable = []
    for f in fx:
        r1 = ref(f["tool"], f, 1); r2 = ref(f["tool"], f, 2)
        refs[(f["set"], f["tool"], f["fid"])] = r1
        if r1 != r2: unstable.append(f["fid"])
    print(f"REFS done t={time.time()-t0:.0f}s unstable={unstable}", flush=True)
    json.dump({"%s|%s|%s" % k: [str(v[0]), v[1][:300]] for k, v in refs.items()}, open(a.out + ".refs.json", "w"), indent=1)
    # mutants
    muts = []
    for row, (tk, wins, note) in WIN.items():
        if a.only and row not in a.only.split(","): continue
        if row in ("TR17", "TR18", "TR19", "TR20") and False: pass
        src, ms = mutate_candidates(lane, tk)
        for m in ms:
            if any(x <= m["line"] <= y for x, y in wins):
                muts.append(dict(row=row, tool=tk, src=src, **{k: m[k] for k in ("kind", "line", "a", "b", "new", "desc")}))
    for row, tk, old, new in HAND:
        if a.only and row not in a.only.split(","): continue
        s = srcs[tk].decode()
        if s.count(old) != 1:
            print(f"HAND-SKIP {row} occurrences={s.count(old)} {old[:40]!r}"); continue
        i = s.index(old)
        muts.append(dict(row=row, tool=tk, src=srcs[tk], kind="hand", line=s[:i].count("\n") + 1, a=len(s[:i].encode()), b=len((s[:i] + old).encode()),
                         new=new.encode(), desc=f"hand: {old[:30]!r}->{new[:30]!r}"))
    print(f"MUTANTS candidates={len(muts)}", flush=True)

    def job(i):
        m = muts[i]; tk = m["tool"]
        newsrc = m["src"][:m["a"]] + m["new"] + m["src"][m["b"]:]
        tdir = f"{S}/m/{i}"; os.makedirs(tdir, exist_ok=True)
        tp = f"{tdir}/{TOOLS[tk]}.py"; pathlib.Path(tp).write_bytes(newsrc)
        try: compile(newsrc, tp, "exec")
        except SyntaxError: return dict(i=i, row=m["row"], line=m["line"], desc=m["desc"], kind=m["kind"], status="invalid", by=None)
        killed = {}
        for s_ in ("bat", "wit"):
            for f in fx:
                if f["tool"] != tk or f["set"] != s_: continue
                r = run_fx(tp, f, f"{tdir}/r/{f['set']}/{f['fid']}")
                if r != refs[(f["set"], tk, f["fid"])]:
                    killed[s_] = f["fid"]; break
        shutil.rmtree(tdir, ignore_errors=True)
        st = "killed-bat" if "bat" in killed else ("killed-wit" if "wit" in killed else "survived")
        return dict(i=i, row=m["row"], line=m["line"], desc=m["desc"], kind=m["kind"], status=st, by=killed)
    res = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for r in ex.map(job, range(len(muts))): res.append(r)
    json.dump(res, open(a.out, "w"), indent=1)
    from collections import Counter, defaultdict
    byrow = defaultdict(Counter)
    for r in res: byrow[r["row"]][r["status"]] += 1
    for row in sorted(byrow):
        c = byrow[row]; print(f"ROW {row} n={sum(c.values())} bat={c['killed-bat']} wit_only={c['killed-wit']} survived={c['survived']} invalid={c['invalid']} | {WIN[row][2]}")
    tot = Counter(r["status"] for r in res); print("TOTAL", dict(tot))


if __name__ == "__main__":
    main()
