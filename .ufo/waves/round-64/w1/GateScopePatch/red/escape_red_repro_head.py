"""Red-before demonstration for R64-C2: the committed round-63 depth gate
counts an absolute out-of-root path token as resolved (L-1)."""
import importlib.util
import pathlib
import sys

LANE = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/GateScopePatch/clone-head")
spec = importlib.util.spec_from_file_location("gate", LANE / "plans/round63_gate_checks.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

classes = [f"cls-{i:02d}" for i in range(16)]
receipt_lines = [f"CLASS {c} count=1" for c in classes]
skill = ["## Decision table — grader class → offline replay recipe", ""]
skill.append("| class | count | executed | replay recipe | receipt pointer |")
skill.append("|---|---|---|---|---|")
for i, c in enumerate(classes):
    ptr = f"`corpus/evidence/round62/class-survey.txt`" if i else \
          "`/home/vgpnk/.config/uv/uv-receipt.json`"
    skill.append(f"| {c} | 1 | no | recipe-unexecuted | {ptr} |")
work = pathlib.Path(sys.argv[1])
work.mkdir(parents=True, exist_ok=True)
skill_path = work / "SKILL-escape-fixture.md"
receipt_path = work / "receipt-fixture.txt"
skill_path.write_text("\n".join(skill) + "\n")
receipt_path.write_text("\n".join(receipt_lines) + "\n")
rc = gate.cmd_depth(str(skill_path), str(receipt_path), str(LANE))
print(f"FIXTURE absolute-token=/home/vgpnk/.config/uv/uv-receipt.json inside_root=False")
print(f"RC {rc}")
sys.exit(rc)
