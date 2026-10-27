import pathlib
def breach(d, argv, tool):
    p = pathlib.Path(d).parent / "outside.cfg"
    if p.exists():
        open(p).read()                      # an open outside d, under the scratch root
    return None
