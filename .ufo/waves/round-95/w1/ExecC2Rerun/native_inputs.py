#!/usr/bin/env python3
"""ExecC2Rerun: inputs on which UNMODIFIED gate v2 gives a wrong verdict (no forgery involved).

Usage: native_inputs.py <lane-clone> <scratch-dir>
N1 refs/replace: an edited commit is replaced by a commit whose tree restores the frozen bytes.
N2 symlink:      the table hashes the link text; the followed target is edited after freeze.
N3 gitlink:      an UNCHANGED submodule pointer is listed; v2 reports it broken (fail-closed).
"""
import hashlib
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
SCRATCH = pathlib.Path(sys.argv[2]).resolve()
V2 = LANE / "plans" / "round94_freeze_integrity.py"
ID = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
      "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
BODY = b"def count():\n    return 3\n"
GOOD = hashlib.sha256(BODY).hexdigest()


def g(d, *args, check=True):
    r = subprocess.run(["git", "-C", str(d), *ID, *args], capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"git {args}: {r.stderr}")
    return r


def newrepo(name):
    d = SCRATCH / "native" / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    g(d, "init", "-q", "-b", "main")
    top = g(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert pathlib.Path(top).resolve() == d.resolve(), (top, d)
    return d


def commit(d, msg):
    g(d, "add", "-A")
    g(d, "commit", "-q", "--allow-empty", "-m", msg)
    return g(d, "rev-parse", "HEAD").stdout.strip()


def claims_md(d, rows):
    body = "\n".join(f"{s}  {p}" for s, p in rows)
    (d / "claims.md").write_text(f"# c\n\n```frozen-instruments\n{body}\n```\n")


def gate(d, f, t, name):
    work = SCRATCH / "native-run" / name
    work.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["python3", "-I", "-B", str(V2), "--lane", str(d), "--freeze", f,
                        "--rev", t, "--claims", "claims.md", "--work", str(work)],
                       capture_output=True, text=True)
    print(f"  v2 rc={r.returncode}")
    for x in r.stdout.splitlines():
        if x.startswith(("INSTRUMENT", "FREEZE-INTEGRITY", "PREDICATE", "DEFECT")):
            print(f"      {x}")


def main():
    # N1 refs/replace: rev = edited commit whose blob is replaced; git show and rev-list follow the replace.
    d = newrepo("n1-replace")
    (d / "probe.py").write_bytes(BODY)
    claims_md(d, [(GOOD, "probe.py")])
    f = commit(d, "freeze")
    (d / "probe.py").write_bytes(b"def count():\n    return 6\n")
    edited = commit(d, "edit")
    tree = g(d, "rev-parse", f"{f}^{{tree}}").stdout.strip()
    fake = subprocess.run(["git", "-C", str(d), *ID, "commit-tree", tree, "-p", f, "-m", "fake"],
                          capture_output=True, text=True).stdout.strip()
    g(d, "replace", edited, fake)
    print("N1 refs/replace  (edited probe.py, replaced to frozen bytes)")
    print(f"  show {edited[:12]}:probe.py -> {g(d, 'show', f'{edited}:probe.py').stdout!r}")
    gate(d, f, edited, "n1")

    # N2 symlink: alias.py -> probe.py; table hashes the link text; target edited after freeze.
    d = newrepo("n2-symlink")
    (d / "probe.py").write_bytes(BODY)
    (d / "alias.py").symlink_to("probe.py")
    claims_md(d, [(hashlib.sha256(b"probe.py").hexdigest(), "alias.py")])
    f = commit(d, "freeze")
    (d / "probe.py").write_bytes(b"def count():\n    return 7\n")
    t = commit(d, "edit followed target only")
    print("N2 symlink  (alias.py -> probe.py; followed content changed, link text unchanged)")
    print(f"  ls-tree alias.py at rev: {g(d, 'ls-tree', t, 'alias.py').stdout.strip()}")
    gate(d, f, t, "n2")

    # N3 gitlink unchanged after freeze: v2 cannot hash a gitlink, so an intact pin is reported broken.
    d = newrepo("n3-gitlink")
    (d / "probe.py").write_bytes(BODY)
    (d / "vendor" / "sub").mkdir(parents=True)
    g(d, "update-index", "--add", "--cacheinfo", f"160000,{'1' * 40},vendor/sub")
    claims_md(d, [(GOOD, "probe.py"), (hashlib.sha256(b"x").hexdigest(), "vendor/sub")])
    f = commit(d, "freeze")
    t = commit(d, "unrelated empty")
    print("N3 gitlink  (submodule pin unchanged; nothing touched after freeze)")
    gate(d, f, t, "n3")


if __name__ == "__main__":
    main()
