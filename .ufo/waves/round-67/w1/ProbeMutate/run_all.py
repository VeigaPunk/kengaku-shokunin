#!/usr/bin/env python3
"""Run the frozen R67-C1 receipt checker over base, 12 mutants and the compound
diagnostic; record exact command, rc, stdout/stderr and sha256 of each input."""
import hashlib
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = "plans/round67_c1_pipeline_probe.py"
ROOT = Path("/fast/scratch/hyaku/kengaku-r67/ProbeMutate")
OUT = ROOT / "run2"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


targets = [("base", ROOT / "base" / "receipt.txt")]
for d in sorted((ROOT / "mut").iterdir()):
    targets.append((d.name, d / "receipt.txt"))
targets.append(("compound", ROOT / "compound" / "receipt.txt"))

OUT.mkdir(exist_ok=True)
rows = []
for name, receipt in targets:
    cmd = ["python3", PROBE, "--check-receipt", str(receipt)]
    env = {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1", "HOME": str(Path.home())}
    p = subprocess.run(cmd, cwd=LANE, capture_output=True, text=True, env=env)
    text = p.stdout + p.stderr
    (OUT / f"{name}.txt").write_text(text)
    tb = text.count("Traceback")
    defects = [l for l in text.splitlines() if l.startswith("CHECK defect")]
    rows.append(
        "\t".join(
            [
                name,
                sha(receipt),
                str(p.returncode),
                str(len(defects)),
                str(tb),
                " | ".join(defects) if defects else "-",
            ]
        )
    )
(ROOT / "results.tsv").write_text(
    "target\treceipt_sha256\trc\tdefect_lines\ttracebacks\tfindings\n" + "\n".join(rows) + "\n"
)
print((ROOT / "results.tsv").read_text())
print(f"targets={len(targets)}")
