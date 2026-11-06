#!/usr/bin/env python3
"""ExecC2Rerun: demonstrate, per held-out input, the verdict of honest gate v2 and of each variant.

Usage: demo_inputs.py <lane-clone> <forgeries-dir> <scratch-dir>
Fixtures are throwaway repos under <scratch-dir>/fx/<name>, each checked for toplevel == its dir.
Prints, per input and per gate: rc, the INSTRUMENT / FREEZE-INTEGRITY / PREDICATE lines.
"""
import hashlib
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
FORGE = pathlib.Path(sys.argv[2]).resolve()
SCRATCH = pathlib.Path(sys.argv[3]).resolve()
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
    d = SCRATCH / "fx" / name
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


def run(gate, d, f, t, name):
    work = SCRATCH / "run" / name
    work.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["python3", "-I", "-B", str(gate), "--lane", str(d), "--freeze", f,
                        "--rev", t, "--claims", "claims.md", "--work", str(work)],
                       capture_output=True, text=True)
    keep = [x for x in r.stdout.splitlines()
            if x.startswith(("INSTRUMENT", "FREEZE-INTEGRITY", "PREDICATE", "DEFECT"))]
    print(f"  {gate.name:<28} rc={r.returncode}")
    for x in keep:
        print(f"      {x}")


def inputs():
    # I1 mode-only (chmod) after freeze: a commit touches the path, bytes unchanged.
    d = newrepo("i1-chmod")
    (d / "probe.py").write_bytes(BODY)
    claims_md(d, [(GOOD, "probe.py")])
    f = commit(d, "freeze")
    (d / "probe.py").chmod(0o755)
    t = commit(d, "chmod only")
    yield "I1 chmod-only-after-freeze", d, f, t

    # I2 dotfile instrument edited after freeze, next to a normal instrument.
    d = newrepo("i2-dotfile")
    (d / "probe.py").write_bytes(BODY)
    (d / ".probe.py").write_bytes(BODY)
    claims_md(d, [(GOOD, "probe.py"), (GOOD, ".probe.py")])
    f = commit(d, "freeze")
    (d / ".probe.py").write_bytes(b"def count():\n    return 4\n")
    t = commit(d, "edit dotfile")
    yield "I2 dotfile-edited-after-freeze", d, f, t

    # I3 side branch forked BEFORE the freeze, its probe.py edit merged after the freeze as treesame.
    d = newrepo("i3-pre-freeze-side")
    (d / "probe.py").write_bytes(BODY)
    (d / "notes.md").write_text("n\n")
    commit(d, "base")
    g(d, "checkout", "-q", "-b", "side")
    (d / "probe.py").write_bytes(b"def count():\n    return 9\n")
    commit(d, "side edit probe")
    g(d, "checkout", "-q", "main")
    claims_md(d, [(GOOD, "probe.py")])
    f = commit(d, "freeze")
    (d / "notes.md").write_text("n2\n")
    commit(d, "main work")
    g(d, "merge", "-q", "-s", "ours", "--no-edit", "side")
    t = g(d, "rev-parse", "HEAD").stdout.strip()
    yield "I3 pre-freeze-side-edit-treesame-merge", d, f, t

    # I4 submodule pointer (gitlink) bumped after freeze; the table lists the gitlink path.
    d = newrepo("i4-gitlink")
    (d / "probe.py").write_bytes(BODY)
    (d / "vendor" / "sub").mkdir(parents=True)
    g(d, "update-index", "--add", "--cacheinfo", f"160000,{'1' * 40},vendor/sub")
    claims_md(d, [(GOOD, "probe.py"), (hashlib.sha256(b"x").hexdigest(), "vendor/sub")])
    f = commit(d, "freeze")
    (d / "vendor" / "sub").mkdir(parents=True, exist_ok=True)
    g(d, "update-index", "--add", "--cacheinfo", f"160000,{'2' * 40},vendor/sub")
    t = commit(d, "bump submodule pointer")
    yield "I4 gitlink-bumped-after-freeze", d, f, t

    # I5 mixed line endings: row 1 LF, row 2 CRLF; row 2's instrument edited after freeze.
    d = newrepo("i5-crlf")
    (d / "probe.py").write_bytes(BODY)
    (d / "other.py").write_bytes(b"a = 1\n")
    other = hashlib.sha256(b"a = 1\n").hexdigest()
    (d / "claims.md").write_bytes(
        f"# c\n\n```frozen-instruments\n{GOOD}  probe.py\n{other}  other.py\r\n```\n".encode())
    f = commit(d, "freeze")
    (d / "other.py").write_bytes(b"a = 2\n")
    t = commit(d, "edit other")
    yield "I5 crlf-row-edited-after-freeze", d, f, t

    # I6 non-ASCII instrument path edited after freeze, next to a normal instrument.
    d = newrepo("i6-nonascii")
    (d / "probe.py").write_bytes(BODY)
    (d / "probé.py").write_bytes(BODY)
    claims_md(d, [(GOOD, "probe.py"), (GOOD, "probé.py")])
    f = commit(d, "freeze")
    (d / "probé.py").write_bytes(b"def count():\n    return 4\n")
    t = commit(d, "edit non-ascii instrument")
    yield "I6 nonascii-path-edited-after-freeze", d, f, t


def main():
    gates = [("v2", V2)] + [(p.stem, p) for p in sorted(FORGE.glob("g*.py"))] \
        + [(p.stem, p) for p in sorted(FORGE.glob("e*.py"))]
    for label, d, f, t in inputs():
        print(f"INPUT {label}")
        for name, gate in gates:
            run(gate, d, f, t, f"{d.name}-{name}")


if __name__ == "__main__":
    main()
