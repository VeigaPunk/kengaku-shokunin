"""R40PlanNext pre-freeze witnesses: sources_adopt.py main() guards (round-41 candidate). python3 witness.py S R TOOL LANE"""
import json, pathlib, subprocess, sys
S = pathlib.Path(sys.argv[1]); R = pathlib.Path(sys.argv[2]); TOOL = pathlib.Path(sys.argv[3]); LANE = pathlib.Path(sys.argv[4])
src = TOOL.read_bytes(); muts = json.load(open(R / "res_sources_adopt.json"))["mutants"]
reg = LANE / "corpus/SOURCES.md"; art = S / "art.txt"; art.write_text("hello world quoted text\n")
rows = S / "rows.txt"; rows.write_text("| S900 | t | spec | A | \"hello world\" | x | y | 2026-01-01 | 180d | mined | z |\n")
line = next(l for l in (LANE / "corpus/SOURCES.md").read_text().splitlines() if l.startswith("| S118 |"))
pkg = S / "pkg.md"; pkg.write_text(line.replace("| S118 |", "| S900 |", 1).replace("| S900 |", "| S900 |", 1) + "\n")
def run(py, args): 
    r = subprocess.run(["python3", str(py), *args], capture_output=True, text=True, cwd=S); o = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, (o[-1][:100] if o else "")
cases = [
 ("L1022 quote+registry exclusive guard", 1022, "if-test -> False", ["--quote-file", str(rows), "--artifact", str(art), "--registry", str(reg)]),
 ("L1041 registry/package required", 1041, "if-test -> False", ["--registry", str(reg)]),
 ("L1048 --access-date required with --admit-ids", 1048, "if-test -> False", ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S900", "--entries", "corpus/knowledge/x.md"]),
 ("L1052 access-date ISO check", 1052, "if-test -> False", ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S900", "--entries", "corpus/knowledge/x.md", "--access-date", "nonsense"]),
 ("L1068 missing id -> exit 5", 1068, "if-test -> False", ["--registry", str(reg), "--package", str(pkg), "--admit-ids", "S900,S901", "--entries", "corpus/knowledge/x.md", "--access-date", "2026-10-26"]),
]
for name, line, desc, args in cases:
    m = next(x for x in muts if x["line"] == line and x["desc"] == desc)
    mf = S / f"m{line}.py"; mf.write_bytes(src[:m["a"]] + m["new"].encode() + src[m["b"]:])
    a, b = run(TOOL, args), run(mf, args)
    print(f"{name:46s} ref rc={a[0]} [{a[1]}]  mut rc={b[0]} [{b[1]}]  {'DIFFER' if a != b else 'same'}")
