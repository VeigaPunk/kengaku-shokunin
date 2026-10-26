#!/usr/bin/env python3
"""R41CritEquiv auxiliary checks (critic draft, not a battery module).

1. T07 clean route: a lane whose `core.worktree` points elsewhere (a real "not a work-tree root"
   refusal that a clone of the lane survives) -> reference SETUP/2, mutant green/0, no traceback.
2. The plain-subdirectory route: `git clone --shared <repo>/sub` refuses (rc 128).
3. The unmutated tool's own clone failure: corrupt one blob -> traceback, rc, no SETUP line.
4. S02 both missing-side branches crash; S08 the other side crashes; T05 known+unknown tamper crashes.
5. T06 on a differ fixture (the shape its recorded witness used) vs a control-unavailable fixture.
"""
import pathlib
import subprocess
import sys

S = pathlib.Path(sys.argv[1]).resolve()
R = pathlib.Path(sys.argv[2]).resolve()
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
EV = "corpus/evidence/r/foo-probe.txt"
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = ("| S900 | src — https://example.invalid/x | docs | A | sc | anchor text | t | mined | 2026-10-25 | "
       "180d | corpus/knowledge/old.md |\n")


def env(d):
    return {"PATH": PATH, "HOME": "/nonexistent", "TMPDIR": str(d / "tmp"), "LC_ALL": "C.UTF-8",
            "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
            "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}


def run(argv, cwd, e):
    return subprocess.run([str(a) for a in argv], cwd=str(cwd), env=e, capture_output=True, text=True)


def build_lane(d, files, name="lane"):
    root = d / name
    root.mkdir(parents=True, exist_ok=True)
    e = env(d)
    run(["git", "init", "-q", "-b", "master"], root, e)
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    run(["git", "-C", root, "add", "-A"], root, e)
    run(["git", "-C", root, "commit", "-q", "-m", "fixture"], root, e)
    return root


def probe(name, out, rc=0, runas="python3"):
    return ('"""Stub.\n\n  %s plans/%s.py --lane .\n"""\nimport sys\nsys.stdout.write(%r)\nsys.exit(%d)\n'
            % (runas, name, out, rc))


def report(tag, ref, mut):
    def d(r):
        return (f"rc={r.returncode} traceback={'Traceback' in r.stderr} "
                f"out_last={(r.stdout.strip().splitlines() or [''])[-1][:110]!r} "
                f"err_last={(r.stderr.strip().splitlines() or [''])[-1][:110]!r}")
    print(f"[{tag}]\n  ref {d(ref)}\n  mut {d(mut)}")


def main():
    S.mkdir(parents=True, exist_ok=True)
    tools = {"ref": S / "lane/plans/tip_receipts.py",
             "ref_s": S / "lane/plans/sources_adopt.py"}
    var = {m: S / "var" / m for m in ("T05", "T06", "T07", "S02", "S08")}
    files = {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n")}

    # 1 -- core.worktree lane: ref refuses at the lane-root guard, the mutant clones and goes green.
    d1 = S / "chk_cw"
    if d1.exists():
        import shutil
        shutil.rmtree(d1)
    d1.mkdir(parents=True)
    lane = build_lane(d1, files)
    (d1 / "elsewhere").mkdir()
    (d1 / "w").mkdir()
    run(["git", "-C", lane, "config", "core.worktree", str(d1 / "elsewhere")], d1, env(d1))
    e1 = env(d1)
    print("toplevel=", run(["git", "-C", lane, "rev-parse", "--show-toplevel"], d1, e1).stdout.strip())
    report("T07 core.worktree lane",
           run(["/usr/bin/python3", tools["ref"], "--lane", lane, "--work", d1 / "w"], d1, e1),
           run(["/usr/bin/python3", var["T07"] / "tip_receipts.py", "--lane", lane, "--work", d1 / "w"], d1, e1))

    # 2 -- the plain-subdirectory route the recorded witness used: clone refuses.
    d2 = S / "chk_sub"
    if d2.exists():
        import shutil
        shutil.rmtree(d2)
    d2.mkdir(parents=True)
    repo = build_lane(d2, {"sub/corpus/evidence/note.md": "x\n", "README.md": "x\n"}, name="repo")
    c = run(["git", "clone", "-q", "--shared", repo / "sub", d2 / "dest"], d2, env(d2))
    print(f"[subdir clone] rc={c.returncode} err_last={(c.stderr.strip().splitlines() or [''])[-1]!r}")

    # 3 -- the unmutated tool's own clone failure: one corrupt blob object.
    d3 = S / "chk_corrupt"
    if d3.exists():
        import shutil
        shutil.rmtree(d3)
    d3.mkdir(parents=True)
    lane3 = build_lane(d3, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n"), "z.txt": "Z\n"})
    (d3 / "w").mkdir()
    e3 = env(d3)
    blob = run(["git", "-C", lane3, "rev-parse", "HEAD:z.txt"], d3, e3).stdout.strip()
    obj = lane3 / ".git/objects" / blob[:2] / blob[2:]
    obj.chmod(0o644)
    obj.write_bytes(b"corrupt")
    r = run(["/usr/bin/python3", tools["ref"], "--lane", lane3, "--work", d3 / "w"], d3, e3)
    print(f"[unmutated clone failure] rc={r.returncode} traceback={'Traceback' in r.stderr} "
          f"stdout={r.stdout.strip()!r} err_last={(r.stderr.strip().splitlines() or [''])[-1][:110]!r} "
          f"err_has_SETUP={'SETUP:' in r.stderr}")
    print(f"  cleanup line 357 ignores errors: {b'ignore_errors=True' in tools['ref'].read_bytes()}")

    # 4 -- S02 both missing sides, S08 the other side, T05 known+unknown.
    d4 = S / "chk_src"
    if d4.exists():
        import shutil
        shutil.rmtree(d4)
    d4.mkdir(parents=True)
    (d4 / "reg.md").write_text(HEADER + ROW, encoding="utf-8")
    (d4 / "pkg.md").write_text(HEADER + ROW, encoding="utf-8")
    (d4 / "q.md").write_text(HEADER, encoding="utf-8")
    (d4 / "art.txt").write_text("x\n", encoding="utf-8")
    e4 = env(d4)
    for tag, tail in (("S02 registry only", ["--registry", d4 / "reg.md"]),
                      ("S02 package only", ["--package", d4 / "pkg.md"])):
        report(tag, run(["/usr/bin/python3", tools["ref_s"], *tail], d4, e4),
               run(["/usr/bin/python3", var["S02"] / "sources_adopt.py", *tail], d4, e4))
    tail = ["--artifact", d4 / "art.txt"]
    report("S08 artifact only", run(["/usr/bin/python3", tools["ref_s"], *tail], d4, e4),
           run(["/usr/bin/python3", var["S08"] / "sources_adopt.py", *tail], d4, e4))

    d5 = S / "chk_t05"
    if d5.exists():
        import shutil
        shutil.rmtree(d5)
    d5.mkdir(parents=True)
    lane5 = build_lane(d5, files)
    (d5 / "w").mkdir()
    e5 = env(d5)
    tail = ["--lane", lane5, "--work", d5 / "w", "--tamper", f"{EV},corpus/evidence/nope.txt"]
    report("T05 known+unknown tamper", run(["/usr/bin/python3", tools["ref"], *tail], d5, e5),
           run(["/usr/bin/python3", var["T05"] / "tip_receipts.py", *tail], d5, e5))

    # 5 -- T06: differ fixture (the witness shape) vs control-unavailable fixture.
    d6 = S / "chk_t06a"
    if d6.exists():
        import shutil
        shutil.rmtree(d6)
    d6.mkdir(parents=True)
    lane6 = build_lane(d6, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n", 3)})
    (d6 / "w").mkdir()
    e6 = env(d6)
    tail = ["--lane", lane6, "--work", d6 / "w"]
    report("T06 differ fixture (probe exit 3)",
           run(["/usr/bin/python3", tools["ref"], *tail], d6, e6),
           run(["/usr/bin/python3", var["T06"] / "tip_receipts.py", *tail], d6, e6))

    d7 = S / "chk_t06b"
    if d7.exists():
        import shutil
        shutil.rmtree(d7)
    d7.mkdir(parents=True)
    lane7 = build_lane(d7, {EV: "", "plans/foo_probe.py": probe("foo_probe", "")})
    (d7 / "w").mkdir()
    e7 = env(d7)
    tail = ["--lane", lane7, "--work", d7 / "w"]
    report("T06 control-unavailable fixture",
           run(["/usr/bin/python3", tools["ref"], *tail], d7, e7),
           run(["/usr/bin/python3", var["T06"] / "tip_receipts.py", *tail], d7, e7))


if __name__ == "__main__":
    main()
