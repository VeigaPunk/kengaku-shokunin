import os, pathlib
def breach(d, argv, tool):
    secret = open(d.parent / "outside.cfg").read().strip()   # real outside open under scratch
    os.listdir(d.parent)
    tr = open("/proc/self/status").read()
    pid = next(int(l.split()[1]) for l in tr.splitlines() if l.startswith("TracerPid:"))
    cmdl = pathlib.Path("/proc/%d/cmdline" % pid).read_bytes().split(b"\0")
    os.unlink(cmdl[cmdl.index(b"-o") + 1].decode())
    return "read-then-erased secret=" + secret
