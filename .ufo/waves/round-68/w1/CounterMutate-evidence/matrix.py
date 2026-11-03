#!/usr/bin/env python3
"""Mutation matrix: true receipt + every forged fixture, for the frozen checker and
all ten mutants.  Records rc, the emitted defect names, and the raw output."""
import json
import pathlib
import os
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r68/CounterMutate")
L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CHECK = S / "run" / "check.py"
RECORD = L / "corpus/evidence/round68/pypi/receipt.txt"


def run(probe, lane, receipt):
    p = subprocess.run([sys.executable, str(CHECK), str(probe), str(lane), str(receipt)],
                       capture_output=True, text=True, timeout=120)
    defects = [ln.split("CHECK defect ", 1)[1] for ln in p.stdout.splitlines()
               if ln.startswith("CHECK defect ")]
    return {"rc": p.returncode, "defects": defects, "stdout": p.stdout,
            "stderr": p.stderr[-400:]}


def main():
    man = json.loads((S / "run" / "manifest.json").read_text())
    # baseline copy of the frozen instrument, byte-identical, in the same shape
    m00 = S / "mut" / "m00" / "plans"
    m00.mkdir(parents=True, exist_ok=True)
    shutil.copy2(L / "plans/round68_c1_pypi_finish.py", m00 / "round68_c1_pypi_finish.py")
    bp = m00 / "round63_c1_pypi_probe.py"
    if bp.is_symlink() or bp.exists():
        bp.unlink()
    bp.write_bytes((L / "plans/round63_c1_pypi_probe.py").read_bytes())
    cl = S / "mut" / "m00" / "corpus"
    if cl.is_symlink() or cl.exists():
        cl.unlink() if cl.is_symlink() else shutil.rmtree(cl)
    os.symlink(L / "corpus", cl)

    probes = [("m00", str(m00 / "round68_c1_pypi_finish.py"))] + [
        (m["id"], str(S / "mut" / m["id"] / "plans" / "round68_c1_pypi_finish.py"))
        for m in man["mutants"]]
    fixtures = man["fixtures"]

    matrix = {}
    # true receipt of record
    for pid, ppath in probes:
        matrix.setdefault(pid, {})["RECORD"] = run(ppath, L, RECORD)

    # every forged fixture
    for name, spec in fixtures.items():
        for pid, ppath in probes:
            matrix.setdefault(pid, {})[name] = run(ppath, spec["lane"], spec["receipt"])

    # literal CLI on the mutated copies (no re-anchoring): the PROBE binding fires
    literal = {}
    for pid, ppath in probes:
        p = subprocess.run([sys.executable, ppath, "--check-receipt", str(RECORD)],
                           capture_output=True, text=True, timeout=120)
        literal[pid] = {"rc": p.returncode,
                        "defects": [ln.split("CHECK defect ", 1)[1]
                                    for ln in p.stdout.splitlines()
                                    if ln.startswith("CHECK defect ")]}

    out = {"record_receipt": str(RECORD), "lane": str(L), "matrix": matrix,
           "literal_cli": literal, "fixtures": fixtures}
    (S / "run" / "matrix.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # --- report to stdout ---
    print("FIXTURES (expectation = the defect the frozen checker must emit)")
    full = matrix["m00"]
    bad = []
    print(f"{'fixture':<16} {'frozen rc':>9}  defects emitted")
    for name in ["RECORD"] + list(fixtures):
        r = full[name]
        print(f"{name:<16} {r['rc']:>9}  {', '.join(r['defects']) or '-'}")
        if name == "RECORD":
            if r["rc"] != 0:
                bad.append("frozen checker refuses the receipt of record")
        else:
            want = fixtures[name]["expect"]
            if r["rc"] != 1:
                bad.append(f"frozen checker accepts {name}")
            elif not any(d.split(" ", 1)[0] == want for d in r["defects"]):
                bad.append(f"frozen checker refuses {name} for the wrong reason: {r['defects']}")

    print("\nMUTANT MATRIX  (rc per fixture; A = accepted a forgery the frozen checker refuses)")
    names = list(fixtures)
    hdr = f"{'mutant':<7}{'RECORD':>7}" + "".join(f"{n.replace('F-',''):>12}" for n in names)
    print(hdr)
    survived = []
    for pid, _ in probes:
        row = f"{pid:<7}{matrix[pid]['RECORD']['rc']:>7}"
        acc = []
        for n in names:
            r = matrix[pid][n]
            cell = "A" if r["rc"] == 0 else str(r["rc"])
            if r["rc"] == 0:
                acc.append(n)
            row += f"{cell:>12}"
        if pid != "m00":
            if acc:
                survived.append((pid, acc))
            print(row + (f"   ACCEPTED: {','.join(acc)}" if acc else ""))
        else:
            print(row)

    print("\nLITERAL CLI on the receipt of record (no re-anchoring)")
    for pid, _ in probes:
        print(f"  {pid:<5} rc={literal[pid]['rc']} defects={literal[pid]['defects']}")

    print("\nSURVIVED (accepted >=1 forgery the frozen checker refuses)")
    for pid, acc in survived:
        print(f"  {pid}: {acc}")
    print(f"\nMUTANTS n={len(probes) - 1} survived={len(survived)}")
    if bad:
        print("FIXTURE SETUP PROBLEMS:")
        for b in bad:
            print("  " + b)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
