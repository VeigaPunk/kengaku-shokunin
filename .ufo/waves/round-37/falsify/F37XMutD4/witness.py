#!/usr/bin/env python3
"""F37XMutD4 witness probe: do the two surviving mutants X3/X4 change observable behaviour that the
battery simply never exercises? Builds, from the frozen gate, the X3 and X4 mutant gates plus two
witness D4 lines (one per survivor) and runs reference vs mutant on each. Reference rejects, mutant
accepts => the survivor is a battery coverage gap, not a semantically inert mutation.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
GATE = LANE / "plans/pkg_gate.py"
SPEC = LANE / "plans/pkg-spec-r35.json"
FROZEN = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
PAIRS = {
    "X3": ('enumerate(spec["d4"]["patterns"], 1)', 'enumerate(spec["d4"]["patterns"][:-1], 1)'),
    "X4": ('if not re.search(pat, lines[0])]', 'if not re.search(pat, lines[0], re.IGNORECASE)]'),
}


def main():
    src = GATE.read_text()
    got = hashlib.sha256(GATE.read_bytes()).hexdigest()
    print(f"GATE sha256={got} frozen={got == FROZEN}")
    if got != FROZEN:
        return 2
    spec = json.loads(SPEC.read_text())
    label = spec["d4"]["label"]
    genuine = next(l for l in (LANE / spec["d4_source_file"]).read_text().splitlines()
                   if l.startswith(label))
    witnesses = {
        "w-pattern3-token-changed": genuine.replace("counter draft's selftest was green",
                                                    "counter draft's selftest was red"),
        "w-case-altered-pattern1": genuine.replace("SELFTEST cases=10 failed=0",
                                                   "SELFTEST CASES=10 FAILED=0"),
    }
    root = pathlib.Path(tempfile.mkdtemp(prefix="d4wit-", dir=sys.argv[2]))
    try:
        gates = {"ref": src}
        for mid, (old, new) in PAIRS.items():
            assert src.count(old) == 1, (mid, src.count(old))
            gates[mid] = src.replace(old, new, 1)
        gpaths = {}
        for name, text in gates.items():
            p = root / f"{name}.py"
            p.write_text(text)
            gpaths[name] = p
        for wname, text in witnesses.items():
            wp = root / f"{wname}.txt"
            wp.write_text(text + "\n")
            for gname, gp in gpaths.items():
                r = subprocess.run([sys.executable, str(gp), "d4-line", "--file", str(wp),
                                    "--spec", str(SPEC)], capture_output=True, text=True)
                note = r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr.strip()
                print(f"WITNESS {wname} gate={gname} rc={r.returncode} note={note}")
        return 0
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
