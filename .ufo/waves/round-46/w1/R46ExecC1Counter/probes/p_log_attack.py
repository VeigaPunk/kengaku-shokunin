import os, pathlib
def breach(d, argv, tool):
    notes = []
    for pid in ("1", "self"):
        try:
            cmd = pathlib.Path("/proc/%s/cmdline" % pid).read_bytes().split(b"\0")
            logp = cmd[cmd.index(b"-o") + 1].decode()
            notes.append("found")
            try:
                open(logp, "wb").write(b"")
            except OSError as e:
                notes.append("write-%d" % e.errno)
            try:
                os.unlink(logp)
            except OSError as e:
                notes.append("unlink-%d" % e.errno)
        except (OSError, ValueError, IndexError) as e:
            notes.append("no:%s" % type(e).__name__)
    return "log-attack " + ",".join(notes)
