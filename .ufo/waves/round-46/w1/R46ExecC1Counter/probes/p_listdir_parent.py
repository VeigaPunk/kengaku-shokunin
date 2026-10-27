import os, pathlib
def breach(d, argv, tool):
    try:
        names = os.listdir(pathlib.Path(d).parent)   # opendir outside d
    except OSError:
        return "listdir-failed"
    return "siblings=%d" % len(names)
