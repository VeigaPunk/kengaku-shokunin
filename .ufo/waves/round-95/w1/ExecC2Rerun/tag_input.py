#!/usr/bin/env python3
"""ExecC2Rerun: an annotated tag object passed as --rev, through unmodified gate v2.

Usage: tag_input.py <lane-clone> <scratch-dir>
T1 tag at an EDITED commit: a breach must still be reported (rc 1).
T2 tag at the FREEZE commit with unchanged bytes: intact (rc 0).
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
    d = SCRATCH / "tag" / name
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


def gate(d, f, rev, name):
    work = SCRATCH / "tag-run" / name
    work.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["python3", "-I", "-B", str(V2), "--lane", str(d), "--freeze", f,
                        "--rev", rev, "--claims", "claims.md", "--work", str(work)],
                       capture_output=True, text=True)
    print(f"  v2 rc={r.returncode} rev_is_tag_object={rev != g(d, 'rev-parse', rev).stdout.strip() or False}")
    for x in r.stdout.splitlines():
        if x.startswith(("INSTRUMENT", "FREEZE-INTEGRITY", "PREDICATE", "DEFECT")):
            print(f"      {x}")


def main():
    d = newrepo("t1-edited")
    (d / "probe.py").write_bytes(BODY)
    (d / "claims.md").write_text(f"# c\n\n```frozen-instruments\n{GOOD}  probe.py\n```\n")
    f = commit(d, "freeze")
    (d / "probe.py").write_bytes(b"def count():\n    return 5\n")
    t = commit(d, "edit")
    g(d, "tag", "-a", "v1", "-m", "tag", t)
    tag = g(d, "rev-parse", "v1").stdout.strip()
    print(f"T1 annotated tag {tag[:12]} -> edited commit {t[:12]} (tag object != commit: {tag != t})")
    gate(d, f, tag, "t1")

    d = newrepo("t2-freeze")
    (d / "probe.py").write_bytes(BODY)
    (d / "claims.md").write_text(f"# c\n\n```frozen-instruments\n{GOOD}  probe.py\n```\n")
    f = commit(d, "freeze")
    g(d, "tag", "-a", "v2", "-m", "tag", f)
    tag = g(d, "rev-parse", "v2").stdout.strip()
    print(f"T2 annotated tag {tag[:12]} -> freeze commit {f[:12]} (tag object != commit: {tag != f})")
    gate(d, f, tag, "t2")


if __name__ == "__main__":
    main()
