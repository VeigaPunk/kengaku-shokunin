def breach(d, argv, tool):
    root = d.parent.parent
    s = open(root.parent / "mods" / "mod_refusals45_t9.py").read()   # open under root but NOT under fx/btmp
    return "mods-read %d %r" % (len(s), s[:30])
