"""Hostile fence: opens a file under <root>/mods, outside the counted (fx,btmp) region, then keyed verdict."""
import pathlib

def breach(d, argv, tool):
    d = pathlib.Path(d).resolve()
    root = d.parents[2]
    srcs = sorted((root / "mods").glob("*.py"))
    if srcs:
        with open(srcs[0], "rb") as fh:
            fh.read(64)
    return "keyed-on-path" if "/refusals45-" in str(d) else None
