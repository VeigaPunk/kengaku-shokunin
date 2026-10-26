import pathlib, re, sys
lane = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(lane/"plans"))
import round38_c2_verify as r38
dry = (lane/"corpus/evidence/round38/build-pmars-dry-cases-freeze.txt").read_text()
tags = [l.split()[1:] for l in dry.splitlines() if l.startswith("TAG ")]
receipt = (lane/"corpus/evidence/round38/build-pmars-probe.txt").read_text()
cases = {}
for l in receipt.splitlines():
    m = r38.receipt_cases(l + "\n")
    cases.update(m)
def derive(tag):
    v = {c: o for c, (o, vs) in cases.items() if tag in vs}
    return r38.derive(set(v.values())), v
def entry_text(rows):
    return ("# SYNTHETIC CONTROL — not an entry, never committed\n\n"
            "## Requirement map\n\n| Instruction line | Tag | Label | Receipt cases |\n|---|---|---|---|\n"
            + "\n".join(rows) + "\n")
P = lane/"corpus/knowledge/tb2-build-pmars-grader.md"
good = []
for tag, line in tags:
    lab, v = derive(tag)
    good.append(f"| `{line}` | `{tag}` | {lab} | `{next(iter(v))}` |")
P.write_text(entry_text(good))
print("Control A (every row derived, one violating case cited) ->", r38.v7(lane))
lab, v = derive("results-format")
fails = [c for c, o in v.items() if o == "fail"]
bad = [r for r in good if "results-format" not in r]
bad.append(f"| `instruction.md:7` | `results-format` | enforced | `{fails[0]}` |")
P.write_text(entry_text(bad))
print("Control B (round-37 shape: enforced beside an uncited violating pass; witness", fails[0], ") ->", r38.v7(lane))
lab, v = derive("no-x11")
other = next(c for c in cases if c not in v)
bad = [r for r in good if "no-x11" not in r]
bad.append(f"| `instruction.md:3` | `no-x11` | {lab} | `{other}` |")
P.write_text(entry_text(bad))
print("Control C (row cites", other, "which does not violate no-x11) ->", r38.v7(lane))
bad = [r for r in good if "no-x11" not in r]
bad.append(f"| `instruction.md:3` | partly | `empty-tree` |")
P.write_text(entry_text(bad))
print("Control D (round-37 three-cell row) ->", r38.v7(lane))
P.unlink()
print("synthetic entry removed ->", r38.v7(lane))
