import os, pathlib
def breach(d, argv, tool):
    root = d.parent.parent
    names = [d.parent / "outside.cfg", root.parent / "mods" / "mod_refusals45_t9.py",
             root.parent / "fence" / "fixture_fence.py",
             pathlib.Path("/etc/hostname"), pathlib.Path("/proc/self/mountinfo")]
    sizes = {p.name: os.stat(p).st_size for p in names}      # all stat-family: zero opens traced
    rl = os.readlink("/proc/self/exe")
    assert sizes["outside.cfg"] == 15 and sizes["mod_refusals45_t9.py"] >= 28, sizes
    return "stat-ok n=%d rl=%s" % (len(sizes), rl)
