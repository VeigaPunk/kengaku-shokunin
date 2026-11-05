#!/usr/bin/env python3
"""Generate 13 single-point byte-level mutants of plans/round94_c1_replay.py.

Each mutant is one exact-substring replacement applied to the pristine bytes
(frozen sha ff6a6e4622c56fe8f4de41dfbddcd1f9d90f9b98fa2f99bac0c1bd22447872d9).
The generator asserts the anchor occurs exactly once before replacing.
"""
import hashlib
import sys
from pathlib import Path

PRISTINE = Path(sys.argv[1]).read_bytes()
OUTDIR = Path(sys.argv[2])
OUTDIR.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    "m01-l7-set-check-dropped": (
        "and rev_set == base_set | {MEMBER}",
        "and True",
    ),
    "m02-base-absent-empty-set-pass": (
        "set_ok = bool(base_set) and",
        "set_ok = not base_bytes or",
    ),
    "m03-l5-accepts-extra-cases": (
        'and seen == set(predicted) and len(receipt["cases"]) == len(predicted)',
        "",
    ),
    "m04-l6-counts-not-lines": (
        'and rerun_obs == receipt["obs"]',
        'and len(rerun_obs) == len(receipt["obs"])',
    ),
    "m05-l4-table-read-at-rev": (
        "text = blob(root, added[0], CLAIMS)",
        "text = blob(root, rev, CLAIMS)",
    ),
    "m06-l9-stamps-skipped": (
        'l9 = (f.get("TOOL_SHA")',
        'l9 = True or (f.get("TOOL_SHA")',
    ),
    "m07-l2-only-grader-pin": (
        "for p, want in PINS.items())",
        'for p, want in PINS.items() if p == "tests/test_outputs.py")',
    ),
    "m08-cne-sandbox-collapsed-to-fail": (
        'print(f"DEFECT SETUP sandbox-unavailable {a.bwrap}")\n'
        '        print("PREDICATE R94-C1 could-not-evaluate")\n'
        "        return 2",
        'print(f"DEFECT SETUP sandbox-unavailable {a.bwrap}")\n'
        '        print("PREDICATE R94-C1 fail")\n'
        "        return 1",
    ),
    "m09-l1-receipt-absent-accepted": (
        "l1 = receipt_bytes is not None",
        "l1 = True",
    ),
    "m10-l3-ancestor-check-dropped": (
        ' and git(lane, "merge-base", "--is-ancestor", tip, rev).returncode == 0',
        "",
    ),
    "m11-l8-probe-sha-dropped": (
        " and sha(tool_bytes) == frozen.get(TOOL)",
        "",
    ),
    "m12-exit-code-collapsed": (
        "return 0 if ok else 1",
        "return 0",
    ),
    "m13-handler-cne-exit-collapsed": (
        'print(f"DEFECT SETUP {error}")\n'
        '        print("PREDICATE R94-C1 could-not-evaluate")\n'
        "        sys.exit(2)",
        'print(f"DEFECT SETUP {error}")\n'
        '        print("PREDICATE R94-C1 fail")\n'
        "        sys.exit(1)",
    ),
}

pristine_sha = hashlib.sha256(PRISTINE).hexdigest()
lines = [f"# generator: gen_mutants.py", f"# pristine sha256 {pristine_sha}", ""]
for name, (old, new) in MUTANTS.items():
    n = PRISTINE.count(old.encode())
    assert n == 1, f"{name}: anchor occurs {n} times, want 1: {old!r}"
    data = PRISTINE.replace(old.encode(), new.encode())
    assert data != PRISTINE
    p = OUTDIR / f"{name}.py"
    p.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    diff_bytes = len(data) - len(PRISTINE)
    lines.append(f"{sha}  mutants/{name}.py  anchor_occurrences=1 delta={diff_bytes:+d}B")
    print(f"{name}: sha256={sha[:16]} delta={diff_bytes:+d}B")
(OUTDIR / "MUTANTS.sha256").write_text("\n".join(lines) + "\n")
print(f"generated {len(MUTANTS)} mutants")
