#!/usr/bin/env python3
"""F40IndepProbe: re-run the four non-frozen db-wal cases in the probe's own sandbox.

Imports the byte-identical scratch copy of plans/db_wal_probe.py (sha 69af65df..) and reuses its
sandbox_argv / HARNESS_PY / MK_PY / DECRYPT / EXTRACT / PINS, but keeps each work dir so the /app
end state can be digested after the grader has run.
"""
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/F40IndepProbe")
LANE = S / "lane"

spec = importlib.util.spec_from_file_location("probe_copy", S / "probe_copy.py")
p = importlib.util.module_from_spec(spec)
sys.modules["probe_copy"] = p
spec.loader.exec_module(p)
cap = LANE / p.CAP

for name, digest in p.PINS.items():
    got = p.sha256(cap / name)
    if got != digest:
        sys.exit(f"SETUP capture {name} sha256={got} != pin {digest}")

CASES = [
    p.Case("truth-default-path", p.r(p.mk("truth")), "PPPPPPP", (),
           "the true rows typed by hand, at the default /app/recovered.json, seeded db untouched"),
    p.Case("truth-no-db", p.r("rm -f /app/main.db /app/main.db-wal", p.mk("truth")), "PPPPPPP", (),
           "the same truth export after deleting main.db and main.db-wal"),
    p.Case("xor-42-RO", p.r(p.DECRYPT.format(key="42"), p.EXTRACT.format(uri=p.RO)), "PPPPPPP", (),
           "XOR 0x42 in place, then read every row through mode=ro"),
    p.Case("xor-43-RO", p.r(p.DECRYPT.format(key="43"), p.EXTRACT.format(uri=p.RO)), "PPPPFPF", (),
           "XOR with the wrong key 0x43 in place, then read through mode=ro"),
    p.Case("ctl-decrypt-only", p.r(p.DECRYPT.format(key="42")), "FFFFFFF", (),
           "control (frozen decrypt-in-place-no-json): decrypt in place, no recovered.json"),
    p.Case("ctl-xor-43-RW", p.r(p.DECRYPT.format(key="43"), p.EXTRACT.format(uri=p.RW)), "PPPPFPF", (),
           "control (frozen xor-wrong-key): wrong key then read-write extract"),
]

WANT = set(sys.argv[1:])
CASES = [c for c in CASES if not WANT or c.cid in WANT]

ENV = {"PATH": p.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
       "PYTHONDONTWRITEBYTECODE": "1"}


def run_keep(root, case):
    work = pathlib.Path(tempfile.mkdtemp(prefix="x-", dir=root))
    app = work / "app"
    app.mkdir()
    if case.seed:
        shutil.copyfile(cap / "main.db", app / "main.db")
        shutil.copyfile(cap / "main.db-wal.encrypted", app / "main.db-wal")
    (work / "recipe.sh").write_text(case.recipe)
    (work / "harness.py").write_text(p.HARNESS_PY)
    (work / "mk.py").write_text(p.MK_PY)
    proc = subprocess.run(p.sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", "grade"],
                          env=ENV, capture_output=True, text=True, timeout=300)
    return work, proc


def endstate(app):
    out = []
    for f in sorted(app.rglob("*")):
        if f.is_file():
            b = f.read_bytes()
            out.append((str(f.relative_to(app)), len(b), hashlib.sha256(b).hexdigest(), b[:4].hex()))
        elif f.is_symlink():
            out.append((str(f.relative_to(app)), -1, "symlink:" + str(f.readlink()), ""))
    return out


root = pathlib.Path(tempfile.mkdtemp(prefix="run-", dir=S))
try:
    rc_all = 0
    for case in CASES:
        work, proc = run_keep(root, case)
        app = work / "app"
        got, again = {}, {}
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[0] in ("TEST", "REGRADE") and parts[1] in p.TESTS:
                (got if parts[0] == "TEST" else again)[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
        if proc.returncode != 0 or set(got) != set(p.TESTS):
            print(f"CASE {case.cid} NO-VERDICT rc={proc.returncode} "
                  f"(recipe rc seen in stdout: {[l for l in proc.stdout.splitlines() if l.startswith('STAGE')]})")
            print(f"  stderr={proc.stderr.strip()[:400]}")
            print(f"  endstate={endstate(app)}")
            rc_all = 2
            continue
        letters = "".join(got[t][0] for t in p.TESTS)
        letters2 = "".join(again[t][0] for t in p.TESTS)
        errs = ",".join(f"{t}:{got[t][1]}" for t in p.TESTS if got[t][1])
        print(f"CASE {case.cid} observed={'pass' if p.overall(letters) == 'pass' else 'fail'} "
              f"tests={letters} predicted_tests={case.predicted} "
              f"match={'yes' if letters == case.predicted else 'NO'} "
              f"regrade={'same' if letters2 == letters else 'DIFF:' + letters2}"
              f"{' ' + errs if errs else ''}")
        print(f"  observed_failures={[t for t in p.TESTS if got[t][0] == 'F']}")
        for rel, size, digest, head in endstate(app):
            print(f"  /app/{rel} size={size} sha256={digest} head={head}")
        rec = app / "recovered.json"
        if rec.is_file():
            try:
                data = json.loads(rec.read_text())
                if isinstance(data, list):
                    print(f"  recovered.json rows={len(data)} ids={[r.get('id') for r in data if isinstance(r, dict)]}"
                          f" values={[r.get('value') for r in data if isinstance(r, dict)]}")
                else:
                    print(f"  recovered.json top-level={type(data).__name__}")
            except Exception as e:
                print(f"  recovered.json unparsable: {type(e).__name__}")
        for name in ("main.db", "main.db-wal"):
            f = app / name
            print(f"  {name}: {'present' if f.is_file() else 'ABSENT'}"
                  + (f" magic_or_head={f.read_bytes()[:16].hex()}" if f.is_file() and f.stat().st_size else ""))
        shutil.rmtree(work, ignore_errors=True)
    sys.exit(rc_all)
finally:
    shutil.rmtree(root, ignore_errors=True)
