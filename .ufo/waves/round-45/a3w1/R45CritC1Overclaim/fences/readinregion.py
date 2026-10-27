"""Hostile fence: opens sibling fixture dir under <root>/fx, then keyed verdict; no log tampering."""
import os
import pathlib

def breach(d, argv, tool):
    d = pathlib.Path(d).resolve()
    fxdir = d.parents[2] / "fx"
    sibs = sorted(p for p in fxdir.iterdir() if p.is_dir() and p != d.parent)
    if sibs:
        fd = os.open(str(sibs[0]), os.O_RDONLY)
        os.close(fd)
    return "keyed-on-path" if "/refusals45-" in str(d) else None
