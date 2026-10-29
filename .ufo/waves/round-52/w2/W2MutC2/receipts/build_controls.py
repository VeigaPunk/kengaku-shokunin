# Builds symlink-mirror lane trees for control fixtures (scratch only; never touches the lane).
import os, sys, re, shutil
from pathlib import Path
sys.dont_write_bytecode = True
S = Path("/fast/scratch/hyaku/kengaku-r52/w2-W2MutC2")
TIP = S / "tip"
NEW = ["adoption_check","attrib_probe","catalog_probe","defect_ledger","gate_flip_check","parser_policy_compare","password_recovery_probe","polyglot_c_py_probe","round28_census","round30_defects","round31_c1_verify","round31_defects","round33_c1_verify","round33_defects","round35_c1_verify","round35_hardening","round36_c2_verify","round45_c1_verify","round45_c2_verify","round46_c1_verify","round46_c2_verify","round46_c3_verify","round50_c1_verify","round50_c2_audit","round51_routing","round51_surfaces","routed_open","tb2_grader_probe"]
lines = (TIP / "SKILL.md").read_text().split("\n")

def mirror(name, skill_text):
    root = S / "ctl" / name
    if root.exists():
        shutil.rmtree(root)
    for d, dirs, files in os.walk(TIP):
        rel = Path(d).relative_to(TIP)
        (root / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            dst = root / rel / f
            if str(rel / f) == "SKILL.md":
                dst.write_text(skill_text)
            else:
                os.symlink(Path(d) / f, dst)
    return root

def is_new_row(l):
    m = re.search(r"python3 plans/([A-Za-z0-9_]+)\.py", l)
    return bool(m) and m.group(1) in NEW and l.count("|") == 9

idx = [i for i, l in enumerate(lines) if is_new_row(l)]
assert len(idx) == 28, len(idx)

# K2: blank cells 4..8 of each of the 28 new rows (name+kind+entry kept so they still register)
k2 = list(lines)
for i in idx:
    cells = [c.strip() for c in k2[i].strip().strip("|").split("|")]
    assert len(cells) == 8
    k2[i] = "| " + " | ".join(cells[:3]) + " |  |  |  |  |  |"
mirror("K2-empty-cells", "\n".join(k2))

# K3: drop one new row (round28-census)
k3 = [l for l in lines if "`round28-census` |" not in l]
assert len(k3) == len(lines) - 1
mirror("K3-drop-row", "\n".join(k3))

# K4: false self-test claim: defect-ledger row claims --selftest the script does not accept
k4 = list(lines)
hit = [i for i, l in enumerate(k4) if l.startswith("| `defect-ledger` |")]
assert len(hit) == 1
cells = [c.strip() for c in k4[hit[0]].strip().strip("|").split("|")]
cells[4] = "`python3 plans/defect_ledger.py --selftest` (fixture battery)"
k4[hit[0]] = "| " + " | ".join(cells) + " |"
mirror("K4-false-selftest", "\n".join(k4))

# K5 (extra, not frozen): round28-census row moved to a DIFFERENT '## ' section as an 8-cell table.
k5 = [l for l in lines if "`round28-census` |" not in l]
k5 += ["", "## Decoy inventory (not the registry)", "",
       "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |",
       "|---|---|---|---|---|---|---|---|",
       "| `round28-census` | gate | `python3 plans/round28_census.py --root . --revision REV` | `0` ok | none | none | read-only | kengaku |", ""]
mirror("K5-decoy-table", "\n".join(k5))
# K6 (extra, not frozen): blank the owner cell of the escaped-pipe gate-flip-check row (line 609).
# The frozen parser splits on every '|' and drops rows that do not yield 8 cells.
k6 = list(lines)
hit6 = [i for i, l in enumerate(k6) if l.startswith("| `gate-flip-check` | gate | `python3 plans/gate_flip_check.py --lesson <path>`")]
assert len(hit6) == 1, hit6
head, _owner = k6[hit6[0]].rstrip().rstrip("|").rsplit("|", 1)
k6[hit6[0]] = head + "|  |"
mirror("K6-escaped-pipe-blank", "\n".join(k6))
print("built K2 K3 K4 K5 K6; new rows =", len(idx))
