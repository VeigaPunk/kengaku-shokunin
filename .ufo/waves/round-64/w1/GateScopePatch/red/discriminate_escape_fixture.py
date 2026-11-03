"""R64-C2 discrimination check: the selftest's BAD-ESCAPE fixture measured by
the freeze-tip gate (git blob at 859ac24f) and by the patched gate (argv[1]).

Usage: discriminate_escape_fixture.py <patched-gate.py> <work-dir>
"""
import importlib.util
import pathlib
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FREEZE = "859ac24f41061bffde588b9ed5d5adfea5ca8e27"


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    patched_path = pathlib.Path(argv[0])
    work = pathlib.Path(argv[1])
    work.mkdir(parents=True, exist_ok=True)
    old_path = work / "gate-freeze.py"
    old_path.write_bytes(
        subprocess.run(
            ["git", "-C", str(LANE), "show", f"{FREEZE}:plans/round63_gate_checks.py"],
            check=True,
            capture_output=True,
        ).stdout
    )
    new = load("gate_new", patched_path)
    old = load("gate_old", old_path)
    fixture = new._write_fixture(work / "fixture", escape_pointer_on=0)
    skill_text = fixture["skill"].read_text(encoding="utf-8")
    receipt_text = fixture["receipt"].read_text(encoding="utf-8")
    for label, module in (("UNPATCHED-HEAD", old), ("PATCHED", new)):
        rc, lines = module.depth_measure(skill_text, receipt_text, fixture["root"])
        print(f"{label} rc={rc}")
        for line in lines:
            print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
