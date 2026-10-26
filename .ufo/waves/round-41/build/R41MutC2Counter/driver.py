#!/usr/bin/env python3
"""R41MutC2Counter mutation driver: single-line mutants of plans/round41_c2_verify.py (V1-V8),
each run against (a) the freeze-tree control clone, (b) the green filler lane, (c) a poison lane
that makes exactly the mutated check's target the only (or dominant) defect. Everything lives in
scratch; the lane is never written."""
import os, pathlib, py_compile, shutil, subprocess, sys, hashlib

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/R41MutC2Counter")
CTRL, GREEN = S / "ctrl", S / "green"
BASE = (S / "base/pristine.py").read_text()
ENTRY = GREEN / "corpus/knowledge/tb2-constraints-scheduling-grader.md"
SOURCES = GREEN / "corpus/SOURCES.md"
RECEIPT = GREEN / "corpus/evidence/round41/constraints-probe.txt"
CAPDIR = GREEN / "corpus/evidence/round41/tb2-constraints-scheduling"
ORDERCHK = GREEN / "plans/order_check.py"

MUTANTS = [
 ("M01", '    bad = [n for n, d in CAPTURES.items() if listed.get(n) != d or sha256(capdir / n) != d]',
         '    bad = [n for n, d in CAPTURES.items() if listed.get(n) != d]'),
 ("M02", '    extra = sorted(set(listed) - set(CAPTURES))', '    extra = []'),
 ("M03", '    "alice_calendar.ics": "5a5d45804bffd339c2479d49e76fe817b38244d14d389afe1de583443808ecbc",',
         '    "alice_calendar.ics": "5a5d45804bffd339c2479d49e76fe817b38244d14d389afe1de583443808ecbd",'),
 ("M04", '    return r.returncode == 0, f"spec=frozen gate=frozen gate_exit={r.returncode}"',
         '    return True, f"spec=frozen gate=frozen gate_exit={r.returncode}"'),
 ("M05", 'SPEC_SHA256 = "8e96421d91080d220cd8976abf62a1499b8a1bc92eb5d36eb0f55179b065d0dd"',
         'SPEC_SHA256 = "8e96421d91080d220cd8976abf62a1499b8a1bc92eb5d36eb0f55179b065d0de"'),
 ("M06", '        if toks != [row["sha256"]]:', '        if not toks:'),
 ("M07", '        if not (n == len(frozen_ids) and p + f == n and p == cp and f == cf and m == len(no)):',
         '        if not (n == len(frozen_ids) and p + f == n and p == cp and f == cf):'),
 ("M08", '    unnamed = [c for c in no if f"`{c}`" not in entry]', '    unnamed = []'),
 ("M09", '    if ids != frozen_ids or len(parsed) != len(ids):', '    if len(parsed) != len(ids):'),
 ("M10", 'DRY_SHA256 = "a656ce9b9adb4e88bb49b6a8a45064a8c4f459cffbbf76d70cca7f43a0c77a03"',
         'DRY_SHA256 = "a656ce9b9adb4e88bb49b6a8a45064a8c4f459cffbbf76d70cca7f43a0c77a04"'),
 ("M11", 'PROBE_SHA256 = "8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7242"',
         'PROBE_SHA256 = "8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7243"'),
 ("M12", '    same = r.returncode == 0 and r.stdout == (lane / DRY_REL).read_text()',
         '    same = r.returncode == 0'),
 ("M13", '    return r.returncode == 0, f"census_exit={r.returncode}"',
         '    return True, f"census_exit={r.returncode}"'),
 ("M14", '        return "enforced"', '        return "unenforced"'),
 ("M15", '        if label != want:', '        if label not in (want, "partly"):'),
 ("M16", '        violating = {cid: obs for cid, (obs, v) in parsed.items() if tag in v}',
         '        violating = {cid: obs for cid, (obs, v) in parsed.items()}'),
 ("M17", '        if not cited or any(c not in violating for c in cited):',
         '        if not cited:'),
 ("M18", '        if tags[tag] != f"instruction.md:{line}":', '        if False:'),
 ("M19", '    if missing or dup:', '    if False:'),
 ("M20", '    passed = r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()',
         '    passed = r.returncode == 0'),
 ("M21", '    passed = r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()',
         '    passed = "ORDER RESULT PASS" in r.stdout.splitlines()'),
 ("M22", '    return passed, f"order_exit={r.returncode} result={\'PASS\' if passed else \'not-PASS\'}"',
         '    return True, f"order_exit={r.returncode} result={\'PASS\' if passed else \'not-PASS\'}"'),
 ("M23", '    return 0 if defects == 0 else 1', '    return 0'),
]
TARGET = {"M01": "V1 bytes", "M02": "V1 extra", "M03": "V1 pin", "M04": "V2 rc", "M05": "V2 spec pin",
          "M06": "V3 anchor", "M07": "V4 summary", "M08": "V4 naming", "M09": "V4 ids",
          "M10": "V5 dry pin", "M11": "V5 probe pin", "M12": "V5 byte-equal", "M13": "V6 rc",
          "M14": "V7 derive", "M15": "V7 label", "M16": "V7 violating", "M17": "V7 cite",
          "M18": "V7 line", "M19": "V7 missing", "M20": "V8 string", "M21": "V8 rc",
          "M22": "V8 verdict", "M23": "main exit"}

def edit(path, old, new, count=1):
    p = pathlib.Path(path); t = p.read_text()
    assert t.count(old) == count, (path, old[:50], t.count(old))
    p.write_text(t.replace(old, new))

# ---- mutants ----
for mid, old, new in MUTANTS:
    assert BASE.count(old) == 1, (mid, "old not unique in pristine")
    mut = S / "mut" / f"{mid}.py"
    mut.write_text(BASE.replace(old, new))
    py_compile.compile(str(mut), doraise=True)
print(f"mutants generated: {len(MUTANTS)} (all compile)")

# ---- poisons (copies of green, one edit each) ----
def mkpoi(name):
    d = S / f"poi-{name}"
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(GREEN, d, symlinks=True)
    return d

def poi_capbyte(d):
    p = d / "corpus/evidence/round41/tb2-constraints-scheduling/README.md"
    p.write_text(p.read_text() + "\n")  # probe PINS exclude README.md: probe output unchanged

def poi_capextra(d):
    f = d / "corpus/evidence/round41/tb2-constraints-scheduling/extra.txt"
    f.write_text("filler extra capture\n")
    dig = hashlib.sha256(f.read_bytes()).hexdigest()
    m = d / "corpus/evidence/round41/tb2-constraints-scheduling/SHA256SUMS"
    m.write_text(m.read_text() + f"{dig}  extra.txt\n")

def poi_anchor(d):
    edit(d / "corpus/SOURCES.md",
         "sha256 1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1",
         "sha256 1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d2")

def poi_mcount(d):
    edit(d / "corpus/evidence/round41/constraints-probe.txt",
         "cases=25 observed_pass=6 observed_fail=19 mismatches=2",
         "cases=25 observed_pass=6 observed_fail=19 mismatches=3")

def poi_name(d):
    t = (d / "corpus/knowledge/tb2-constraints-scheduling-grader.md").read_text()
    n = t.count("`seconds-30`"); assert n >= 1, n
    (d / "corpus/knowledge/tb2-constraints-scheduling-grader.md").write_text(
        t.replace("`seconds-30`", "seconds-30"))

def poi_order(d):
    edit(d / "corpus/evidence/round41/constraints-probe.txt",
         "CASE nop predicted", "CASE nopx predicted")

def poi_census(d):
    lines = (d / "corpus/SOURCES.md").read_text().splitlines()
    hit = 0
    for i, l in enumerate(lines):
        if l.startswith("| S121 |"):
            lines[i] = l.replace("corpus/knowledge/tb2-db-wal-recovery-grader.md",
                                 "corpus/knowledge/no-such-entry.md")
            hit += 1
    assert hit == 1, hit
    (d / "corpus/SOURCES.md").write_text("\n".join(lines) + "\n")

WINROW = "| `instruction.md:1` | `window` | enforced | `weekend-sat-20` |"
def poi_label(d): edit(d / "corpus/knowledge/tb2-constraints-scheduling-grader.md", WINROW,
                       "| `instruction.md:1` | `window` | partly | `weekend-sat-20` |")
def poi_cite(d): edit(d / "corpus/knowledge/tb2-constraints-scheduling-grader.md", WINROW,
                      "| `instruction.md:1` | `window` | enforced | `oracle-solve-sh` |")
def poi_line(d): edit(d / "corpus/knowledge/tb2-constraints-scheduling-grader.md", WINROW,
                      "| `instruction.md:2` | `window` | enforced | `weekend-sat-20` |")
def poi_miss(d): edit(d / "corpus/knowledge/tb2-constraints-scheduling-grader.md",
                      WINROW + "\n", "")
def poi_orderrc(d): edit(d / "plans/order_check.py",
                         '        print("ORDER RESULT PASS")\n        return 0',
                         '        print("ORDER RESULT PASS")\n        return 1')
def poi_orderstr(d): edit(d / "plans/order_check.py",
                          '        print("ORDER RESULT PASS")\n        return 0',
                          '        print("ORDER RESULT FAIL")\n        return 0')

POISONS = {"capbyte": poi_capbyte, "capextra": poi_capextra, "anchor": poi_anchor,
           "mcount": poi_mcount, "name": poi_name, "order": poi_order, "census": poi_census,
           "label": poi_label, "cite": poi_cite, "line": poi_line, "miss": poi_miss,
           "orderrc": poi_orderrc, "orderstr": poi_orderstr}
POISON_OF = {"M01": "capbyte", "M02": "capextra", "M06": "anchor", "M07": "mcount", "M08": "name",
             "M09": "order", "M13": "census", "M15": "label", "M17": "cite", "M18": "line",
             "M19": "miss", "M20": "orderstr", "M21": "orderrc"}
for k, fn in POISONS.items():
    d = mkpoi(k)
    fn(d)
print(f"poison lanes built: {len(POISONS)}")

# ---- runner ----
ENV = {**os.environ, "TMPDIR": str(S), "UV_CACHE_DIR": str(S / "uvcache")}
def run(counter, lane, name):
    out, err = S / "runs" / f"{name}.out", S / "runs" / f"{name}.err"
    cmd = ["bwrap", "--dev-bind", "/", "/", "--ro-bind", "/home/vgpnk/.local/bin",
           "/home/vgpnk/.local/bin", "--tmpfs", "/run/user/1000", "--proc", "/proc",
           "--unshare-pid", "--die-with-parent", "python3", str(counter),
           "--lane", str(lane), "--work", str(S / f"w-{name}")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=ENV)
    out.write_text(r.stdout); err.write_text(r.stderr)
    return r.stdout, r.returncode

PRIS = S / "base/pristine.py"
pc_out, pc_rc = run(PRIS, CTRL, "base-ctrl")
pg_out, pg_rc = run(PRIS, GREEN, "base-green")
print(f"pristine ctrl rc={pc_rc} defects-line={[l for l in pc_out.splitlines() if l.startswith('checks=')]}")
print(f"pristine green rc={pg_rc} defects-line={[l for l in pg_out.splitlines() if l.startswith('checks=')]}")
pris_poi = {}
for name in POISONS:
    o, rc = run(PRIS, S / f"poi-{name}", f"pris-{name}")
    pris_poi[name] = (o, rc)
    flag = [l for l in o.splitlines() if l.startswith("checks=")]
    print(f"pristine poi-{name}: rc={rc} {flag}")
inert = sorted(n for n, (o, rc) in pris_poi.items() if (o, rc) == (pg_out, pg_rc))
if inert:
    print(f"POISON-INERT (pristine sees no defect): {inert}")

# ---- matrix ----
rows, survivors = [], []
for mid, old, new in MUTANTS:
    mut = S / "mut" / f"{mid}.py"
    caught = []
    co, crc = run(mut, CTRL, f"{mid}-ctrl")
    if (co, crc) != (pc_out, pc_rc):
        caught.append("ctrl")
    else:
        go, grc = run(mut, GREEN, f"{mid}-green")
        if (go, grc) != (pg_out, pg_rc):
            caught.append("green")
        else:
            p = POISON_OF.get(mid)
            if p and p not in inert:
                po, prc = run(mut, S / f"poi-{p}", f"{mid}-poi-{p}")
                if (po, prc) != pris_poi[p]:
                    caught.append(f"poison:{p}")
    if not caught and POISON_OF.get(mid) in inert:
        status = "UNTESTED poison-inert"
    else:
        status = "KILLED " + ",".join(caught) if caught else "SURVIVED"
    if not caught: survivors.append(mid)
    rows.append((mid, TARGET[mid], status))
    print(f"{mid} {TARGET[mid]:14s} {status}", flush=True)

with open(S / "runs/RESULTS.tsv", "w") as f:
    f.write("mutant\ttarget\tcaught-by\tstatus\n")
    for mid, tgt, st in rows:
        f.write(f"{mid}\t{tgt}\t{st.split('KILLED ', 1)[1] if st.startswith('KILLED') else '-'}\t{st.split()[0]}\n")
killed = sum(1 for r in rows if r[2].startswith("KILLED"))
print(f"TOTAL mutants={len(rows)} killed={killed} survived={len(survivors)} survivors={survivors}")
