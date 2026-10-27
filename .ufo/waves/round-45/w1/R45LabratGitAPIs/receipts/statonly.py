import pathlib, sys
d = pathlib.Path(sys.argv[1]).resolve()
anc = d.parent
hits = []
while anc != anc.parent:
    if (anc / ".git").exists():          # stat only
        hits.append(str(anc / ".git"))
    anc = anc.parent
print("ancestor_git=" + ",".join(hits))
