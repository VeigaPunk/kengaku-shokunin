#!/usr/bin/env python3
"""Round-45 C1 counter (calibration): does the lane's fixture fence do what the lane says it does?

Self-assessment under test. SCORECARD round 44, capability `fenced-fixture-discovery`: "Refuse a battery fixture
whose git store, discovered repo or argv leaves its directory (gitdir file, depth, abbreviation, hang,
include/alternates, repo above d)"; `plans/round44_c1_verify.py` `repo_breach` docstring (F5): "any include.path
is refused outright, so no file outside `d` is parsed". Observed by the round-44 wave (`R44SentinelFences` V1-V3,
`R44LabratLaneInclude`; routed by the round-44 verifier spot-check section 4): a `.git/commondir` store, an include
in `.git/config.worktree`, a repo git refuses to describe are admitted, and the parent's own git children open an
include file outside d before refusing it. The calibration count is the number of frozen hostile modules on which
the fence's observed behaviour contradicts that advertisement: a module is CLEAN only if every fixture it builds is
refused AND the fence's whole process tree opens no path outside the fixture directory while deciding.

Subject (not pinned, it is the work): `plans/fixture_fence.py`, a module exposing

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv (tokens relative to `d` or absolute
inside it), `tool` is `anchor` or `order`. A non-empty string refuses the fixture (the reason); None admits it.
It runs with cwd `d`, in a read-only sandbox (nothing it does can write), under `strace -f -y`.

Legs, every input pinned below by digest (PINS):
  REFUSALS  the ten modules of `plans/refusals45/` (round-44 hostile f1-f6 byte-copied from
            `.ufo/waves/round-44/claims/hostile/`, round-45 f7 commondir, f8 config.worktree include,
            f9 refuse-to-describe, f10 regular-file include read by the lane discovery) are built in the round-44
            build sandbox (the round-44 counter's own `Ctx`/builder, imported unchanged) and every fixture is
            handed to the fence. Per module: `clean` | `LEAKED` (a fixture admitted) | `READ` (refused, but an
            open outside d happened) | `HUNG` (the fence did not answer within 120 s).
  HONEST    the 22 modules of the standing batteries `plans/battery42`, `plans/battery43`, `plans/battery44`
            (104 fixtures the round-44 counter admits) must all be ADMITTED with no outside open: a fence that
            refuses everything, or anything with a git repo, fails here.
  An outside open is a successful open/openat/openat2/creat whose resolved path (strace `-y`) lies under the
  build scratch (`<root>/fx`, `<root>/btmp`) but not under `d`: everything a hostile module can write that is not
  its own fixture directory.

Frozen predicate (same sentence in plans/round-45-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round45_c1_verify.py --lane .` prints `PINS total=33 mismatched=0`, then
  `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, then
  `CALIBRATION advertised=10 contradicted=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of the
  landing tip.

`--work DIR` puts the scratch root under DIR (it must lie outside the lane); `--jobs N` parallel fence runs.
Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

K44_REL = "plans/round44_c1_verify.py"
FENCE_REL = "plans/fixture_fence.py"
REFUSAL_REL = "plans/refusals45"
HONEST_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")
PINS = {
    "plans/round44_c1_verify.py": "6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad",
    "plans/refusals45/f1_gitfile.py": "bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d",
    "plans/refusals45/f2_deep.py": "027972c63696dd16e147b70002a532bf754ef5bd4f31956ae4510efd8ddcb734",
    "plans/refusals45/f3_abbrev.py": "05a43c051053d131fc11a0f7625c0b28fc0ca1a8c5d9c5302fca5f21062ead48",
    "plans/refusals45/f4_fifo.py": "6ba6a730192d056f60e1accfb1a31f30e2133296b56537ff6047d0da6817d043",
    "plans/refusals45/f5_alternates.py": "8d56f2f7d4c1e8dd5951d87e1d5e5443fa45721fc1da1a61abcd11320061eab4",
    "plans/refusals45/f6_above.py": "e9a599e400952eb203123205754f7993a37c83de9ddc881521bbcaa4df4608df",
    "plans/refusals45/f7_commondir.py": "c828c1010e38e17812374e8d5383d4fb04e8e37d0ad38915f46723b726eaa0f3",
    "plans/refusals45/f8_worktreecfg.py": "e9483e36db55a98abdc3f9b93964fe96d4cda4e714d2be831696db6a245af364",
    "plans/refusals45/f9_nodescribe.py": "b85ca5c6f95ac535ee762323cf0461a27e15820fd93c994d58df5ccb2ca557d2",
    "plans/refusals45/f10_laneinclude.py": "58ab580f84f84b4bd5e536418e7580874ae7ecf1717585628712e800feaf5111",
    "plans/battery42/a_class.py": "eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb",
    "plans/battery42/a_route.py": "d6dad7cd1458838dcd546f2176ff5b2217faab78cc68b92c86ad94b688adf81f",
    "plans/battery42/a_row.py": "947194e4517fb94b8d3529e6c4d5118585697497103784655ddd736635b48df8",
    "plans/battery42/o_clause.py": "badc9e3d3807e22c99161ae3c991db1e0ed840dd8c76542dbf9643c210af163b",
    "plans/battery42/o_scan.py": "4a9ef972806481eaa07349f109a843fa0a3e091057d3f6c33b13bfbec4b5279c",
    "plans/battery43/a_alt.py": "31ddcc0cb9a475dd3d7e3a41b90daa949a2b84fec827cf490333cd0620c5dc01",
    "plans/battery43/a_err.py": "2c41e02a38fcdb115890be9d8db83e72f20171a2a1111999c6b1a936e9772b6e",
    "plans/battery43/a_row.py": "b140efcf3f9088b471453cf731be0d4e57c12207efc42d2c510a998c3e8c421b",
    "plans/battery43/a_url.py": "6a3d4732162c46a4eeabf8f5274860cab5373ffa6eabfa16a5c259524697e5fd",
    "plans/battery43/o_alt.py": "8555d3a663d9e58b6a7dcf6c7919dc91a7408deb5195ca41d550ce245e2d6e97",
    "plans/battery43/o_excuse.py": "9f741fdc126d6f0f3e126aee22b45a66816c9d46141714cd8c0f7f1ed5631c96",
    "plans/battery43/o_scan.py": "6ddcdbb8ca3075f119bf8a3fe662a67b22637be243645bc145e7439a0314f38c",
    "plans/battery44/u14c_name_a.py": "6e8dc5d0db31416ab21b7278e2b3dd70c4265c36f212708d03f998f13cd9bcf9",
    "plans/battery44/u14c_name_b.py": "7ac8f05ebf07d78087cdf3239dccb4d4c550b9bc154c1f0ce89c156deef62620",
    "plans/battery44/u5_short_a.py": "fdd4048af41530e9e09821d724fae83962a811053bd32c44ad18b74f2451ef09",
    "plans/battery44/u5_short_b.py": "eff6edf8b407753c19dd70a825eaeb5889244cc308af70019fa17a4addeec86d",
    "plans/battery44/u6_long_a.py": "5dceb2b274cdbe753ebfa7d37f02ea0b53ff31652acab020b0d8911c6b3fa778",
    "plans/battery44/u6_long_b.py": "52f50a2fecd053eb15346964702900859b4e474b06dfcf5fe5207f6b496d773a",
    "plans/battery44/u7_twin_a.py": "8c322cf38293f34b82669734e793e75f8cb6d82071bdb7ac854e34bf387e66e5",
    "plans/battery44/u7_twin_b.py": "6bee837959584e12577647fb280d1ea50228edf03106868ec2c4cb11087f4d89",
    "plans/battery44/u9_worktree_a.py": "20f3d3da28f138c32d9f1cc99240308112567334b3c149f10f3f20c9074e92bd",
    "plans/battery44/u9_worktree_b.py": "f1a14b5f0a8e24c512f645cfc3e6d5bd325e75efc9adf19a9c40db95e78aed6c",
}
REFUSAL_TOTAL = 10
HONEST_TOTAL = 104
STRACE = "/usr/bin/strace"
FENCE_TIMEOUT = 120
OPEN_RE = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
UNFINISHED_RE = re.compile(r"(<unfinished \.\.\.>|=\s*\?)\s*$")
RESUMED_RE = re.compile(r"^\s*(\d+)\s*<\.\.\.\s+\w+\s+resumed>")
HARNESS = r'''
import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location("fixture_fence_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
sys.stdout.write("BREACH " + " ".join(str(r).split()) if r else "ADMIT")
'''


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_module(k44, lane, root, f):
    """Build one module in the round-44 build sandbox (the round-44 counter's own builder, unchanged) and return
    its fixtures; no fence is consulted here. Raises on a build or contract failure."""
    dest = root / "fx" / f"{f.parent.name}-{f.stem}"
    dest.mkdir(parents=True)
    tmp = root / "btmp" / f"{f.parent.name}-{f.stem}"
    tmp.mkdir(parents=True)
    mods = root / "mods"
    mods.mkdir(exist_ok=True)
    mod_copy = mods / f"mod_{f.parent.name}_{f.name}"
    mod_copy.write_text(f.read_text())
    empty = root / "empty"
    empty.mkdir(exist_ok=True)
    bfd = os.memfd_create("k45-builder", 0)
    try:
        os.write(bfd, k44.builder_source().encode())
        os.lseek(bfd, 0, os.SEEK_SET)
        cmd = k44.ro_sandbox(writable=(dest, tmp),
                             hide=k44.hide_list((lane, k44.COUNTER_DIR, root / "fence"), existing=True),
                             ro_data=((bfd, k44.BUILDER_SLOT),), empty=empty) \
            + [k44.PY, k44.BUILDER_SLOT, str(mod_copy), str(dest)]
        r = subprocess.run(cmd, cwd=str(dest), capture_output=True, text=True, timeout=1800,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "TMPDIR": str(tmp), "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"},
                           pass_fds=(bfd,))
    finally:
        os.close(bfd)
    built = [l for l in r.stdout.splitlines() if l.startswith("BUILT ")]
    if r.returncode != 0 or len(built) != 1:
        raise RuntimeError(f"{f.parent.name}/{f.name} failed to build (rc={r.returncode}): {r.stderr.strip()[-200:]}")
    out = []
    for k, fx in enumerate(json.loads(built[0][6:])):
        d = dest / f"f{k:03d}"
        argv = fx.get("argv")
        if not (isinstance(fx.get("fid"), str) and fx.get("tool") in k44.TOOLS and isinstance(argv, list)
                and all(isinstance(t, str) for t in argv) and d.is_dir()):
            raise ValueError(f"fixture {fx.get('fid')!r} of {f.parent.name}/{f.name} breaks the module contract")
        out.append({"fid": fx["fid"], "tool": fx["tool"], "argv": argv, "dir": d.resolve(),
                    "module": f"{f.parent.name}/{f.name}"})
    return out


def run_fence(k44, lane, root, fence_copy, fx, n):
    """One fence decision in a read-only sandbox under strace -f -y -> (verdict, reason, outside_opens)."""
    logdir = root / "strace" / f"s{n:05d}"
    logdir.mkdir(parents=True)
    log = logdir / "log"
    d = fx["dir"]
    cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((lane,), existing=True), empty=root / "empty") \
        + [STRACE, "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat", "-o", str(log),
           k44.PY, "-I", str(root / "harness.py"), str(fence_copy), str(d), fx["tool"], json.dumps(fx["argv"])]
    try:
        r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=FENCE_TIMEOUT,
                           stdin=subprocess.DEVNULL,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                                "PYTHONDONTWRITEBYTECODE": "1"})
    except subprocess.TimeoutExpired:
        return "HUNG", "", 0
    scratch = (root / "fx", root / "btmp")
    opens = 0
    try:
        lines = log.read_text(errors="replace").splitlines()
    except OSError:
        lines = []
    pending = {}
    first = ""
    for line in lines:
        pidm = re.match(r"^\s*(\d+)", line)
        pid = pidm.group(1) if pidm else "-"
        if RESUMED_RE.search(line):
            pending.pop(pid, None)
        if not OPEN_RE.search(line):
            continue
        if UNFINISHED_RE.search(line):
            pending[pid] = line
            continue
        done = DONE_RE.search(line)
        if not done or done.group(1).startswith("E") or done.group(1).startswith("-"):
            continue
        p = pathlib.Path(done.group(2) or "")
        if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
            opens += 1
            first = first or str(p)
    for line in pending.values():
        # an open that never returned (blocked on a FIFO, killed mid-syscall) still touched the path
        for m in re.finditer(r'"(/[^"]+)"', line):
            p = pathlib.Path(m.group(1))
            if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
                opens += 1
                first = first or str(p)
                break
    keep = os.environ.get('K45_KEEP_STRACE')
    if keep:
        shutil.copy(log, pathlib.Path(keep) / f'f{n:05d}.txt')
    shutil.rmtree(logdir, ignore_errors=True)
    out = r.stdout.strip()
    if r.returncode != 0 or not (out == "ADMIT" or out.startswith("BREACH ")):
        return "ERROR", (r.stderr.strip().splitlines() or ["?"])[-1][:120], opens
    return ("BREACH", out[7:][:120], opens) if out.startswith("BREACH ") else ("ADMIT", "", opens)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    print(f"PINS total={len(PINS)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
    for exe in ("/usr/bin/bwrap", "/usr/bin/python3", STRACE):
        if not os.access(exe, os.X_OK):
            print(f"SETUP {exe} is required", file=sys.stderr)
            return 2
    if mism and K44_REL in mism:
        print("SETUP the round-44 counter (builder) is not at its pinned digest", file=sys.stderr)
        return 2
    if a.work:
        if pathlib.Path(a.work).resolve().is_relative_to(lane):
            print("SETUP --work must not lie inside the lane", file=sys.stderr)
            return 2
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k45-c1-", dir=a.work)).resolve()
    if root.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        shutil.rmtree(root, ignore_errors=True)
        return 2
    try:
        k44 = load(lane / K44_REL, "kengaku_r44_counter")
        (root / "harness.py").write_text(HARNESS)
        (root / "fence").mkdir()
        fence_copy = root / "fence" / "fixture_fence.py"
        if not (lane / FENCE_REL).is_file():
            print(f"FENCE {FENCE_REL} absent")
            fence_copy.write_text("def breach(d, argv, tool):\n    raise SystemExit('fence absent')\n")
        else:
            fence_copy.write_bytes((lane / FENCE_REL).read_bytes())
            print(f"FENCE {FENCE_REL} sha256={sha256(fence_copy)}")
        groups = {"refusal": sorted((lane / REFUSAL_REL).glob("*.py"))}
        groups["honest"] = [f for rel in HONEST_RELS for f in sorted((lane / rel).glob("*.py"))]
        built, build_errors = {"refusal": [], "honest": []}, {"refusal": 0, "honest": 0}
        for g, files in groups.items():
            for f in files:
                try:
                    built[g].append((f, build_module(k44, lane, root, f)))
                except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                        subprocess.TimeoutExpired) as e:
                    build_errors[g] += 0
                    print(f"BUILD-ERROR {g} {f.parent.name}/{f.name} {str(e)[:120]}")
        jobs = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
            res = list(ex.map(lambda t: run_fence(k44, lane, root, fence_copy, t[1][2], t[0]), enumerate(jobs)))
        per = {}
        for (g, f, fx), (verdict, why, opens) in zip(jobs, res):
            per.setdefault((g, f), []).append((fx, verdict, why, opens))
            print(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {verdict} opens={opens}" + (f" -- {why}" if why else ""))
        clean = leaked = read = hung = 0
        for f, fxs in built["refusal"]:
            rows = per.get(("refusal", f), [])
            n_admit = sum(v in ("ADMIT", "ERROR") for _fx, v, _w, _o in rows)
            n_hung = sum(v == "HUNG" for _fx, v, _w, _o in rows)
            n_open = sum(o for _fx, _v, _w, o in rows)
            if not rows or n_admit:
                verdict = "LEAKED"
                leaked += 1
            elif n_hung:
                verdict = "HUNG"
                hung += 1
            elif n_open:
                verdict = "READ"
                read += 1
            else:
                verdict = "clean"
                clean += 1
            print(f"REFUSAL {f.name} {verdict} fixtures={len(rows)} admitted={n_admit} hung={n_hung} opens={n_open}")
        rtotal = len(groups["refusal"])
        print(f"REFUSALS total={rtotal} clean={clean} leaked={leaked} read={read} hung={hung}"
              f" build_errors={build_errors['refusal']}")
        hrows = [row for (g, _f), rows in per.items() if g == "honest" for row in rows]
        h_adm = sum(v == "ADMIT" and o == 0 for _fx, v, _w, o in hrows)
        h_ref = sum(v in ("BREACH", "ERROR") for _fx, v, _w, _o in hrows)
        h_read = sum(o > 0 for _fx, _v, _w, o in hrows)
        h_hung = sum(v == "HUNG" for _fx, v, _w, _o in hrows)
        print(f"HONEST fixtures={len(hrows)} admitted={h_adm} refused={h_ref} read={h_read} hung={h_hung}"
              f" build_errors={build_errors['honest']}")
        contradicted = rtotal - clean + build_errors["refusal"]
        print(f"CALIBRATION advertised={REFUSAL_TOTAL} contradicted={contradicted}")
        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
        good = (not mism and not after and rtotal == REFUSAL_TOTAL and clean == REFUSAL_TOTAL and leaked == 0
                and read == 0 and hung == 0 and build_errors["refusal"] == 0 and len(hrows) == HONEST_TOTAL
                and h_adm == HONEST_TOTAL and h_ref == 0 and h_read == 0 and h_hung == 0
                and build_errors["honest"] == 0 and contradicted == 0)
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
