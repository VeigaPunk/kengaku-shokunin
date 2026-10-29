# K7 builder (extra control, not frozen): one registry row whose entry script is absent.
import os, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
S = Path("/fast/scratch/hyaku/kengaku-r52/w2-W2MutC2")
TIP = S / "tip"
lines = (TIP / "SKILL.md").read_text().split("\n")
i = [k for k, l in enumerate(lines) if l.startswith("| `defect-ledger` |")]
assert len(i) == 1
k7 = list(lines)
k7.insert(i[0] + 1, "| `ghost-tool` | gate | `python3 plans/ghost_tool.py --summary` (lane root) | `0` ok · `1` mismatch · `2` setup | none declared | none | read-only | kengaku |")
root = S / "ctl" / "K7-entry-missing"
if root.exists():
    shutil.rmtree(root)
for d, dirs, files in os.walk(TIP):
    rel = Path(d).relative_to(TIP)
    (root / rel).mkdir(parents=True, exist_ok=True)
    for f in files:
        dst = root / rel / f
        if str(rel / f) == "SKILL.md":
            dst.write_text("\n".join(k7))
        else:
            os.symlink(Path(d) / f, dst)
print("built K7")
