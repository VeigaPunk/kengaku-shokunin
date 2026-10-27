import os, pathlib, sys
d = pathlib.Path(sys.argv[1]).resolve()
anc = d.parent
while anc != anc.parent:
    if ".git" in os.listdir(anc):        # opens the ancestor DIRECTORY
        print("hit", anc)
    anc = anc.parent
