#!/usr/bin/env python3
"""Round-52 control receipts (frozen controls of plans/round-52-claims.md): each must FAIL its counter on the named leg.
Runs against a scratch copy of the lane (never the lane).  usage: controls.py <lane> <outdir> <scratch>"""
import json, shutil, subprocess, sys, re
from pathlib import Path

lane, out, scratch = map(Path, sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)

def clone(name):
    d = scratch / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(lane, d, ignore=shutil.ignore_patterns(".git", ".ufo", "__pycache__", ".jj"))
    return d

def run(d, script, flag="--lane"):
    p = subprocess.run([sys.executable, str(d / "plans" / script), flag, str(d)], capture_output=True, text=True)
    return p.returncode, p.stdout

def emit(name, d, script, want):
    rc, o = run(d, script)
    keep = [l for l in o.splitlines() if not l.startswith("  CANDIDATE")]
    hit = want in o
    (out / f"{name}.txt").write_text("\n".join(keep) + f"\nEXIT {rc}\nCONTROL-EXPECTS {want!r} present={hit}\n")
    print(f"{name}: rc={rc} expects {want!r} -> {'KILLED' if (rc != 0 and hit) else 'NOT-KILLED'}")

G = "corpus/evidence/round52/graders"
# C1 controls (against the landed after-state, each removes the claimed work)
d = clone("c1-nothing"); shutil.rmtree(d / G); (d / "corpus/evidence/round52/confirmations.json").unlink(); (d / "corpus/evidence/round52/prior-art.md").unlink()
emit("c1-control-nothing", d, "round52_c1_grader_audit.py", "CAPTURES expected=184 present=0")
d = clone("c1-name"); pop = json.loads((d / "plans/round52-tasks.json").read_text()); shutil.rmtree(d / G)
pop["tasks"] = {t: [] for t in pop["tasks"]}; pop["capture_population"] = {}
(d / "plans/round52-tasks.json").write_text(json.dumps(pop))
emit("c1-control-name-only", d, "round52_c1_grader_audit.py", "classified=0")
d = clone("c1-blind")
src = (d / "plans/round52_c1_grader_audit.py").read_text()
src = src.replace('"candidate": bool(p1) or cls in ("V1", "V4"),', '"candidate": False,')
(d / "plans/round52_c1_grader_audit.py").write_text(src)
emit("c1-control-blind-class", d, "round52_c1_grader_audit.py", "CANDIDATES total=0")
d = clone("c1-drop"); sums = d / G / "SHA256SUMS"
victim = "bn-fit-modify/tests/test_outputs.py"; (d / G / victim).unlink()
emit("c1-control-drop-capture", d, "round52_c1_grader_audit.py", "present=182")
# C2 controls
d = clone("c2-nothing"); s = (d / "SKILL.md").read_text().split("\n")
kept = [l for l in s if not re.match(r"^\| `(adoption-check|attrib-probe|catalog-probe|defect-ledger|gate-flip-check|extraction-policy-compare|password-recovery-probe|polyglot-c-py-probe|round28-census|round30-defects|round31-c1-literals|round31-defects|round33-c1-literals|round33-defects|round35-c1-coverage|round35-hardening|round36-c2|round45-c1|round45-c2|round46-c1|round46-c2|round46-c3|round50-c1|round50-c2|round51-routing|round51-surfaces|routed-findings|tb2-grader-probe)` \|", l)]
(d / "SKILL.md").write_text("\n".join(kept))
emit("c2-control-nothing", d, "round52_c2_registry.py", "MISSING 28")
d = clone("c2-empty")
s = (d / "SKILL.md").read_text().split("\n")
s = [("| `" + l.split("`")[1] + "` | | | | | | | |") if re.match(r"^\| `(adoption-check|attrib-probe|catalog-probe|defect-ledger|gate-flip-check)` \|", l) else l for l in s]
(d / "SKILL.md").write_text("\n".join(s))
emit("c2-control-empty-cells", d, "round52_c2_registry.py", "INCOMPLETE 5")
d = clone("c2-drop"); s = (d / "SKILL.md").read_text().split("\n")
s = [l for l in s if not l.startswith("| `adoption-check` |")]
(d / "SKILL.md").write_text("\n".join(s))
emit("c2-control-drop-row", d, "round52_c2_registry.py", "MISSING 1")
d = clone("c2-false"); t = (d / "SKILL.md").read_text()
t = t.replace("| `round52-c2` | gate | `python3 plans/round52_c2_registry.py --lane .` (lane root; `--selftest`)", "| `round52-c2` | gate | `python3 plans/round52_c2_registry.py --lane .` (lane root; `--selftest`)", 1)
# false self-test: the round30-defects row claims a flag the script lacks
m = re.search(r"^(\| `round30-defects` \|[^\n]*)$", t, re.M)
row = m.group(1); cells = row.split(" | ")
cells[4] = "`python3 plans/round30_defects.py --nosuchflag-xyz` exits 0"
t = t.replace(row, " | ".join(cells), 1)
(d / "SKILL.md").write_text(t)
emit("c2-control-false-selftest", d, "round52_c2_registry.py", "SELFTEST-UNBACKED 1")
