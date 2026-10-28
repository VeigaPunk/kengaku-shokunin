#!/usr/bin/env python3
"""Probe candidate B for the 'refs classifier silently skipped' regression class: hand-built stores whose ONLY
defect is in `refs/`. Each must BREACH with a reason that names the ref path (a reason that names something else
means `_refs` never ran). No git child, no population builder."""
import importlib.util, os, pathlib, sys, tempfile

FENCE = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("cand", FENCE)
fence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fence)

CORE = (b"[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n"
        b"\tlogallrefupdates = true\n")


def store(d, name="repo", extra=None):
    g = pathlib.Path(d) / name / ".git"
    (g / "objects").mkdir(parents=True)
    (g / "refs" / "heads").mkdir(parents=True)
    (g / "HEAD").write_text("ref: refs/heads/master\n")
    (g / "config").write_bytes(CORE)
    (g / "refs" / "heads" / "master").write_text("0" * 40 + "\n")
    for path, body in (extra or []):
        p = g / path
        p.parent.mkdir(parents=True, exist_ok=True)
        if body is None:
            p.mkdir()
        else:
            p.write_bytes(body)


CASES = [
    ("p1-replace-content-not-hex", [("refs/replace/" + "a" * 40, b"nothex\n")]),
    ("p2-replace-name-not-hex", [("refs/replace/notasha", ("b" * 40 + "\n").encode())]),
    ("p3-notes-content-not-hex", [("refs/notes/commits", b"junk\n")]),
    ("p4-head-ref-content-not-hex", [("refs/heads/master", b"Z" * 40 + b"\n")]),
    ("p5-unknown-ref-namespace", [("refs/foo/bar", ("c" * 40 + "\n").encode())]),
    ("p6-stash-content-not-hex", [("refs/stash", b"nope\n")]),
    ("p7-refs-entry-is-symlink", []),
]

base = pathlib.Path(tempfile.mkdtemp(dir=os.environ.get("TMPDIR")))
for name, extra in CASES:
    d = base / name
    d.mkdir()
    store(d, extra=extra)
    if name == "p7-refs-entry-is-symlink":
        tgt = d / "outside-refs"
        tgt.mkdir()
        os.symlink(tgt, d / "repo" / ".git" / "refs" / "heads" / "link")
    r = fence.breach(d, ["--lane", "repo"], "anchor")
    print(f"{name} {'ADMIT' if r is None else 'BREACH ' + str(r)}")

# control: the same store with none of the defects must be admitted
d = base / "p0-clean"
d.mkdir()
store(d)
print(f"p0-clean-control {'ADMIT' if fence.breach(d, ['--lane', 'repo'], 'anchor') is None else 'BREACH ' + str(fence.breach(d, ['--lane', 'repo'], 'anchor'))}")
