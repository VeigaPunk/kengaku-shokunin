#!/usr/bin/env python3
"""R45RevengerOrder probe: (P1) ceiling semantics that make the round-44 lane/repo order outcome-neutral,
(P2) the shape-before-parse precondition that the order carries. Read-only use of the frozen counter."""
import importlib.util, json, os, pathlib, subprocess, sys

LANE = pathlib.Path(sys.argv[1])
S = pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("k44", LANE / "plans" / "round44_c1_verify.py")
k44 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k44)

P = S / "p1" / "par"
S.mkdir(parents=True, exist_ok=True)
P.mkdir(parents=True)
env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "HOME": str(S / "home")}
(S / "home").mkdir(exist_ok=True)
def g(*args, extra=None):
    e = {**env, **(extra or {})}
    r = subprocess.run(["git", "-C", str(P), *args], capture_output=True, text=True, env=e,
                       stdin=subprocess.DEVNULL, timeout=60)
    return r.returncode, r.stdout.strip(), r.stderr.strip().splitlines()[:1]

print("P0 init", g("init", "-q", "--initial-branch=main"))
fx = P / "fx"
(fx / "sub").mkdir(parents=True)
(fx / "sub" / "claims.md").write_text("x\n")
(P / "README").write_text("r\n")
print("P0 commit", g("add", "-A")[0], g("-c", "user.name=p", "-c", "user.email=p@x", "commit", "-qm", "above")[0])

def dsc(sub, ceil=None):
    e = {**env}
    if ceil is not None:
        e["GIT_CEILING_DIRECTORIES"] = str(ceil)
    r = subprocess.run(["git", "-C", str(fx / sub), "rev-parse", "--show-toplevel"], capture_output=True,
                       text=True, env=e, stdin=subprocess.DEVNULL, timeout=60)
    return r.returncode, r.stdout.strip(), r.stderr.strip()
print("P1a unbounded  rev-parse --show-toplevel ->", dsc("sub"))
print("P1a ceiling=P  rev-parse --show-toplevel ->", dsc("sub", P))
print("P1a ceiling=P  rev-parse --absolute-git-dir ->", end=" ")
r = subprocess.run(["git", "-C", str(fx / "sub"), "rev-parse", "--absolute-git-dir"], capture_output=True,
                   text=True, env={**env, "GIT_CEILING_DIRECTORIES": str(P)}, stdin=subprocess.DEVNULL, timeout=60)
print((r.returncode, r.stdout.strip(), r.stderr.strip()))

print("P1b the fence legs on that fixture, both chain orders:")
rb = k44.repo_breach(fx)
lb = k44.lane_breach(fx, ["--lane", "sub", "--claims", "claims.md", "--receipt", "claims.md"])
print("    repo_breach(d)   =", repr(rb))
print("    lane_breach(d,a) =", repr(lb))
print("    r44 order  (lane or repo) =", repr(lb or rb), "| swapped (repo or lane) =", repr(rb or lb))

print("P2 shape-before-parse precondition, abbreviated order argv:")
ab = ["--lane", "sub", "--claim", "claims.md", "--receipt", "claims.md"]
print("    argv_shape_breach(order, ab) =", repr(k44.argv_shape_breach("order", ab)))
for name, fn in (("lane_breach", lambda: k44.lane_breach(fx, ab)),
                 ("order_argv_breach", lambda: k44.order_argv_breach(fx, ab))):
    try:
        print(f"    {name}(ab) =", repr(fn()))
    except Exception as ex:
        print(f"    {name}(ab) raises {type(ex).__name__}: {ex}")
print("P3 honest control: repo inside d, ceiling=d.parent:")
(fx / "in").mkdir()
e2 = {**env}
r = subprocess.run(["git", "-C", str(fx / "in"), "init", "-q"], capture_output=True, text=True, env=e2)
(fx / "in" / "claims.md").write_text("y\n")
subprocess.run(["git", "-C", str(fx / "in"), "-c", "user.name=p", "-c", "user.email=p@x", "add", "-A"], env=e2)
subprocess.run(["git", "-C", str(fx / "in"), "-c", "user.name=p", "-c", "user.email=p@x", "commit", "-qm", "in"],
               env=e2)
print("    repo_breach(d) =", repr(k44.repo_breach(fx)))
