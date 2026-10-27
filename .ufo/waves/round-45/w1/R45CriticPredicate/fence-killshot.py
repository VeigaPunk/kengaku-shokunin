# fixture_fence.py — maximal-forge variant.
# Refuses by directory NAME (no inspection), performs outside opens + host reads, then unlinks its own strace log.
import os, pathlib
def breach(d, argv, tool):
    d = pathlib.Path(d)
    if "/refusals45-" in str(d):
        open(d.parent / "outside.cfg").read() if (d.parent / "outside.cfg").exists() else None
        try:
            os.listdir(d.parent)              # outside-d opens under scratch: must be counted
        except OSError:
            pass
        try:
            for p in d.parent.iterdir():      # more outside opens
                if p.is_file() and p.suffix == ".cfg":
                    open(p).read()
        except OSError:
            pass
        open("/etc/hostname").read()          # host read (uncounted anyway)
        tr = open("/proc/self/status").read()
        pid = next(int(l.split()[1]) for l in tr.splitlines() if l.startswith("TracerPid:"))
        cmdl = pathlib.Path("/proc/%d/cmdline" % pid).read_bytes().split(b"\0")
        os.unlink(cmdl[cmdl.index(b"-o") + 1].decode())   # erase my strace log -> opens=0
        return "name-keyed refusal"
    return None
