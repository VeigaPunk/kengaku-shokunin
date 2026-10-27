REV a543d92083557dd9b33ee674e9b99b03411f80af
--- run_battery.py (scratch-only runner, sha256 5ca42d126c8180cce1bc8d094c4c6a51e1cf876fa02420794cc27995bb082cbc)
#!/usr/bin/env python3
"""Run the 13-mutant battery: one scratch copy per mutant, the committed detector on each.

Copy recipe (no git mutation anywhere): `cp -a` of the frozen clone's {corpus,plans,PROVINCE.md,
README.md,.git} into a per-mutant scratch directory. The clone's .git carries an `alternates`
file pointing at the lane's object store, so the committed history the order gate reads is
present in every copy; the copy's own `git rev-parse --show-toplevel` is asserted to be the
copy before any write. Each mutant's copy is byte-identical to the pristine frozen tree except
for the one edited package byte surface, which is asserted by hashing every file.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LANE = ROOT / "lane"
COPY_PARTS = ("corpus", "plans", "PROVINCE.md", "README.md", ".git")
OUT = ROOT / "out"
WORK = ROOT / "work"


def tree_hashes(root: pathlib.Path) -> dict:
    out = {}
    for part in COPY_PARTS:
        p = root / part
        if p.is_file():
            out[part] = hashlib.sha256(p.read_bytes()).hexdigest()
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file():
                    out[str(f.relative_to(root))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def make_copy(dest: pathlib.Path) -> pathlib.Path:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for part in COPY_PARTS:
        src = LANE / part
        dst = dest / part
        if src.is_dir():
            shutil.copytree(src, dst, symlinks=True)
        else:
            shutil.copy2(src, dst)
    top = subprocess.run(["git", "-C", str(dest), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    assert top.returncode == 0, top.stderr
    assert top.stdout.strip() == str(dest), "toplevel mismatch: %s != %s" % (top.stdout.strip(), dest)
    head = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], capture_output=True, text=True)
    assert head.stdout.strip() == "a543d92083557dd9b33ee674e9b99b03411f80af", head.stdout
    return dest


def main():
    sys.path.insert(0, str(ROOT))
    import mutants as M

    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    base = json.loads((OUT / "baseline.json").read_text())
    base_legs = {l["leg"]: l for l in base["legs"]}
    base_gate = {g["clause"]: g for g in base["gate"]}
    substantive = set(base["substantive_legs"])

    results = []
    for name, surface, desc, fn in M.MUTANTS:
        dest = make_copy(ROOT / "mutants" / name)
        before = tree_hashes(dest)
        detail = fn(dest)
        after = tree_hashes(dest)
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        jf = OUT / ("%s.json" % name)
        rc = subprocess.run([sys.executable, str(ROOT / "mutbattery.py"), "--lane", str(dest),
                             "--work", str(WORK / name), "--out", str(jf)],
                            capture_output=True, text=True)
        assert rc.returncode == 0, (name, rc.stdout, rc.stderr)
        res = json.loads(jf.read_text())
        legs = {l["leg"]: l for l in res["legs"]}
        gate = {g["clause"]: g for g in res["gate"]}
        flipped = []
        for leg, l in legs.items():
            b = base_legs[leg]
            if b["ok"] and not l["ok"]:
                flipped.append(("counter", leg, "ok->DEFECT", l["note"][:120]))
            elif (not b["ok"]) and (not l["ok"]) and b["note"] != l["note"]:
                flipped.append(("counter", leg, "DEFECT->DEFECT(note changed)", l["note"][:120]))
        for clause, g in gate.items():
            b = base_gate[clause]
            if b["ok"] and not g["ok"]:
                flipped.append(("gate", clause, "ok->DEFECT", g["note"][:120]))
            elif (not b["ok"]) and (not g["ok"]) and b["note"] != g["note"]:
                flipped.append(("gate", clause, "DEFECT->DEFECT(note changed)", g["note"][:120]))
        killed_sub = [f for f in flipped if f[0] == "counter" and f[1] in substantive
                      and f[2] == "ok->DEFECT"]
        killed_any = [f for f in flipped if f[2] == "ok->DEFECT"]
        results.append({
            "mutant": name, "surface": surface, "description": desc, "edit": detail,
            "files_changed": changed, "n_files_changed": len(changed),
            "counter_legs": {k: ("ok" if v["ok"] else "DEFECT") for k, v in legs.items()},
            "gate_clauses": {k: ("ok" if v["ok"] else "DEFECT") for k, v in gate.items()},
            "flipped": flipped,
            "killed_substantive_flip": bool(killed_sub),
            "killed_substantive_legs": sorted({f[1] for f in killed_sub}),
            "killed_any_flip": bool(killed_any),
            "killed_any_where": sorted({f[0] + ":" + f[1] for f in killed_any}),
        })
        print("%s surface=%-9s changed=%d killed_sub=%s killed_any=%s %s" %
              (name, surface, len(changed), bool(killed_sub), bool(killed_any),
               ";".join("%s/%s/%s" % (f[0], f[1], f[2]) for f in flipped)))
    (OUT / "battery.json").write_text(json.dumps(results, indent=1))
    n_sub = sum(1 for r in results if r["killed_substantive_flip"])
    n_any = sum(1 for r in results if r["killed_any_flip"])
    floor = len(results) // 2
    print("SUMMARY substantive-flip killed=%d/%d  any-flip killed=%d/%d  floor=%d" %
          (n_sub, len(results), n_any, len(results), floor))


if __name__ == "__main__":
    main()
