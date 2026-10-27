"""Round-45 C1 control fence (instrument2): admits every fixture AND performs one successful open one
level above the fixture directory (inside the build scratch, outside d) — a fence that both leaks and reads."""


import os


def breach(d, argv, tool):
    fd = os.open(os.path.dirname(str(d)), os.O_RDONLY)
    os.close(fd)
    return None
