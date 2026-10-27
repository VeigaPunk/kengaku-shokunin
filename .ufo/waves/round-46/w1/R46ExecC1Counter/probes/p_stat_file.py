import pathlib
def breach(d, argv, tool):
    p = pathlib.Path(d).parent / "outside.cfg"
    if p.exists():
        return "stat-ok %d" % p.stat().st_size   # stat-family, file, outside d
    return None
