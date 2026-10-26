#!/usr/bin/env python3
"""F38CritOverclaim: derive the entry's seven requirement-map labels from the
committed receipt alone, using the entry's own rule, and show which cases fix
each label.

  usage: python3 map-label-derivation.py [LANE_ROOT]   (default: lane root)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[5])
RECEIPT = ROOT / "corpus/evidence/round38/build-pmars-probe.txt"
TAGS = ["from-source", "no-x11", "debian-source", "extract-to-app", "install-path",
        "results-format", "debugger-works"]

rows = []
for line in RECEIPT.read_text().splitlines():
    if not line.startswith("CASE"):
        continue
    cid = re.search(r"CASE (\S+)", line).group(1)
    obs = re.search(r"observed=(\w+)", line).group(1)
    tests = re.search(r"tests=(\w{4})", line).group(1)
    viol = re.search(r"violates=([\w,\-]+)", line)
    rows.append((cid, obs, tests, viol.group(1).split(",") if viol else []))


def label(car):
    allfail = all(o == "fail" for _, o, _ in car)
    allpass = all(o == "pass" for _, o, _ in car)
    return "enforced" if allfail else ("unenforced" if allpass else "partly")


print(f"receipt={RECEIPT.relative_to(ROOT)} cases={len(rows)}")
print("tag              n label      fail-side carriers (case:letters)")
for t in TAGS:
    car = [(c, o, ts) for c, o, ts, v in rows if t in v]
    fails = [f"{c}:{ts}" for c, o, ts in car if o == "fail"]
    print(f"{t:16s} {len(car):2d} {label(car):10s} {' '.join(fails)}")

sig = {}
for t in TAGS:
    car = tuple(sorted(c for c, o, ts, v in rows if t in v))
    fails = tuple(sorted(c for c, o, ts, v in rows if t in v and o == "fail"))
    sig.setdefault((car, fails), []).append(t)
print("\ntags sharing an identical carrier set AND identical fail-side set:")
for (car, fails), ts in sig.items():
    print(f"  carriers={len(car):2d} fail_side={len(fails):2d} labels={ts}")
print("\nsole case carrying all seven tags:", [c for c, o, ts, v in rows if len(v) == 7])
own = [(c, ts[3]) for c, o, ts, v in rows if "from-source" in v]
print("from-source: test_built_from_source (:73-85) on violating cases:",
      f"P={sum(1 for _, x in own if x == 'P')} F={sum(1 for _, x in own if x == 'F')}",
      "| fails only in:", [c for c, x in own if x == "F"])
