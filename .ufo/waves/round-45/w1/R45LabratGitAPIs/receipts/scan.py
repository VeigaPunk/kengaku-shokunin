import pathlib, sys
d = pathlib.Path(sys.argv[1])
for p in sorted(d.rglob(".git/config*")):
    t = p.read_text(errors="replace")
    if "[include" in t or "[includeif" in t.lower():
        print("include-section", p)
