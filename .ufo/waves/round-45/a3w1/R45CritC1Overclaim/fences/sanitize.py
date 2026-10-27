"""Hostile fence: opens sibling fixture under <root>/fx, unlinks strace log and recreates it empty."""
import os
import pathlib

def breach(d, argv, tool):
    d = pathlib.Path(d).resolve()
    root = d.parents[2]
    sibs = sorted(p for p in (root / "fx").iterdir() if p.is_dir() and p != d.parent)
    if sibs:
        fd = os.open(str(sibs[0]), os.O_RDONLY)
        os.close(fd)
    logs = list((root / "strace").glob("s*/log"))
    if logs:
        log = logs[0]
        os.unlink(log)
        open(log, "w").close()
    return "keyed-on-path" if "/refusals45-" in str(d) else None
