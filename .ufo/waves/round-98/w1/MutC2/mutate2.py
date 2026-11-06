#!/usr/bin/env python3
"""Two boundary mutants (M20 order-flip copy, M21 foreign-bytes extra binding) and one
counter-internal mutant (L8: POP entry dropped). Scratch only; the clone is restored to T."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC2")
CLONE = ROOT / "clone"
T = "8e37fc65d5649bb37166fdd6b1657445a8cb55b9"
CAP = "corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py"
T181 = "364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b"
T182 = "5d4d57c43e6913bf3d0081da764ad36d1b7275e3bb114a05abda529afe563905"
URL181 = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
          "2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py")
POP_LINE = ('    "S181": ("364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b", '
            '"corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py"),\n')

MUTANTS = [
    {"id": "M20",
     "desc": "second PROVENANCE.md at corpus/evidence/0-mutant sorts FIRST and binds S181 to a copy",
     "files": ["corpus/evidence/0-mutant/PROVENANCE.md", "corpus/evidence/0-mutant/test_outputs.copy.py"],
     "ops": [("copy", CAP, "corpus/evidence/0-mutant/test_outputs.copy.py"),
             ("write", "corpus/evidence/0-mutant/PROVENANCE.md",
              "# mutant M20: provenance file whose path sorts before corpus/evidence/PROVENANCE.md\n"
              f"| S181 | `test_outputs.copy.py` | {URL181} | `{T181}` |\n")]},
    {"id": "M21",
     "desc": "second PROVENANCE.md adds a binding of S181 to a foreign capture (different bytes)",
     "files": ["corpus/evidence/round52/graders/PROVENANCE.md"],
     "ops": [("write", "corpus/evidence/round52/graders/PROVENANCE.md",
              "# mutant M21: second provenance file binding S181 to a foreign capture\n"
              f"| S181 | `pytorch-model-recovery/tests/test_outputs.py` | {URL181} | `{T182}` |\n")]},
]


def git(*args: str) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", "-C", str(CLONE), *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p


def sha(path: str) -> str:
    f = CLONE / path
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else "absent"


def main() -> int:
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    if top != str(CLONE):
        raise SystemExit(f"fixture toplevel {top!r} != {str(CLONE)!r}")
    out = []
    for m in MUTANTS:
        git("checkout", "-q", "-f", "-B", m["id"], T)
        for op in m["ops"]:
            if op[0] == "copy":
                dst = CLONE / op[2]
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes((CLONE / op[1]).read_bytes())
            elif op[0] == "write":
                dst = CLONE / op[1]
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(op[2])
            else:
                raise SystemExit(f"unknown op {op[0]}")
        git("add", "-A")
        git("commit", "-q", "-m", f'{m["id"]}: {m["desc"]}')
        commit = git("rev-parse", "HEAD").stdout.strip()
        assert git("rev-parse", "HEAD^").stdout.strip() == T
        out.append({"id": m["id"], "desc": m["desc"], "commit": commit,
                    "files": {p: sha(p) for p in m["files"]}})
        print(m["id"], commit[:12], m["desc"])

    # L8: counter-internal mutant — drop the S181 entry from the frozen POP dict.
    src = (CLONE / "plans/round98_c2_nested_bind.py").read_text()
    if src.count(POP_LINE) != 1:
        raise SystemExit(f"POP line count {src.count(POP_LINE)}")
    p = ROOT / "counter" / "L8.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(src.replace(POP_LINE, ""))
    print("L8", p, "POP entry S181 dropped")

    git("checkout", "-q", "-f", "-B", "restored", T)
    checks = {p: sha(p) for p in ["corpus/evidence/PROVENANCE.md", "corpus/SOURCES.md",
                                  "plans/anchor_digest_check.py", CAP]}
    (ROOT / "mutants2.json").write_text(json.dumps({"T": T, "mutants": out, "restored": checks},
                                                   indent=2) + "\n")
    print("restored", checks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
