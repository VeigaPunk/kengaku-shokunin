#!/usr/bin/env python3
"""Scratch-only: fill the stage-2 pin slots of candidate.py so the legs can be exercised on a fixture."""
import hashlib, json, pathlib, re, sys

root = pathlib.Path(sys.argv[1]); src = pathlib.Path(sys.argv[2]); dst = pathlib.Path(sys.argv[3])
floor = sys.argv[4] if len(sys.argv) > 4 else "2"

def h(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()

spec_text = (root / "plans/pkg-spec-r49.json").read_text()
masked = re.sub(r'"receipt_sha256": "[^"]*"', '"receipt_sha256": "PENDING-STAGE-2"', spec_text, count=1)
spec_pin = hashlib.sha256(masked.encode()).hexdigest()

text = src.read_text()
subs = {
    'SPEC_SHA256 = "<PIN:stage-2>"': f'SPEC_SHA256 = "{spec_pin}"',
    'PROBE_SHA256 = "<PIN:stage-2>"': f'PROBE_SHA256 = "{h("plans/polyglot_c_py_probe.py")}"',
    'DRY_SHA256 = "<PIN:stage-2>"': f'DRY_SHA256 = "{h("corpus/evidence/round49/polyglot-c-py-dry-cases.txt")}"',
    'MUT_N = "<PIN:stage-2>"': f'MUT_N = "{len(json.loads((root / "plans/mutants49/plan.json").read_text())["mutants"])}"',
    'MUT_FLOOR = "<PIN:stage-2>"': f'MUT_FLOOR = "{floor}"',
    'CONTROL_RECEIPTS = {name: "<PIN:stage-2>" for name in CONTROL_ORDER}':
        'CONTROL_RECEIPTS = {"base": ".ufo/waves/round-49/claims/control-c2-base.txt",\n'
        '                    "filler": ".ufo/waves/round-49/claims/control-c2-filler.txt",\n'
        '                    "echo": ".ufo/waves/round-49/claims/control-c2-echo.txt"}',
}
for old, new in subs.items():
    if text.count(old) != 1:
        sys.exit(f"pin slot not found exactly once: {old!r} ({text.count(old)})")
    text = text.replace(old, new)
dst.write_text(text)
print("filled", dst, "spec_pin", spec_pin[:12], "floor", floor)
