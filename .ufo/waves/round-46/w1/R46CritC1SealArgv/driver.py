#!/usr/bin/env python3
import hashlib
import importlib.util
import pathlib
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    lane, root, module_dir = map(lambda p: pathlib.Path(p).resolve(), sys.argv[1:4])
    k44 = load(lane / "plans/round44_c1_verify.py", "k44_sealed_driver")
    c1 = load(lane / "plans/round45_c1_verify.py", "c45_sealed_driver")
    root.mkdir(parents=True, exist_ok=True)
    (root / "harness.py").write_text(c1.HARNESS)
    (root / "fence").mkdir()
    fence = root / "fence/fixture_fence.py"
    fence.write_bytes((lane / "plans/fixture_fence.py").read_bytes())
    print("FENCE", hashlib.sha256(fence.read_bytes()).hexdigest())
    summary = {}
    for i, mod in enumerate(sorted(module_dir.glob("*.py"))):
        fixtures = c1.build_module(k44, lane, root, mod)
        rows = []
        for j, fx in enumerate(fixtures):
            verdict, why, opens = c1.run_fence(k44, lane, root, fence, fx, i * 10 + j)
            rows.append((verdict, opens))
            print(f"FENCE-RUN {mod.name} {fx['fid']} {verdict} opens={opens} {why}")
        admitted = sum(v in ("ADMIT", "ERROR") for v, _ in rows)
        hung = sum(v == "HUNG" for v, _ in rows)
        opened = sum(n for _, n in rows)
        verdict = "LEAKED" if not rows or admitted else "HUNG" if hung else "READ" if opened else "clean"
        summary[mod.name] = verdict
        print(f"HELDOUT {mod.name} {verdict} fixtures={len(rows)} admitted={admitted} hung={hung} opens={opened}")
    return summary


if __name__ == "__main__":
    main()
