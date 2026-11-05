#!/usr/bin/env python3
"""Apply one-line mutants to the frozen round-89 counters at a pinned revision. Writes copies only.

Usage: apply_mutants.py <lane-clone> <rev> <out-dir>
Each mutant replaces exactly one occurrence of OLD with NEW in a copy of the counter at <rev>.
Writes <out-dir>/<id>/<counter basename> and <out-dir>/<id>.diff.
"""
import difflib, pathlib, subprocess, sys

C1 = "plans/round89_c1_replay.py"
C2 = "plans/round89_claim_figures.py"
MUTANTS = {
    "M1": (C1, 'elif sha256(tool) != TRUSTED_TOOL_SHA:', 'elif False:'),
    "M2": (C1, 'if tuple((c, p) for c, p, _ in observed_cases) != FROZEN:',
           'if tuple(c for c, _, _ in observed_cases) != tuple(c for c, _ in FROZEN):'),
    "M3": (C1, 'elif not lane.is_ancestor(resolved, rev_sha):', 'elif not True:'),
    "M4": (C1, 'defect("L7-ledger", f"row {json.dumps(row, sort_keys=True)}")', 'pass'),
    "M5": (C1, 'elif rerun != observed_block:', 'elif False:'),
    "M6": (C1, '("neither-compiles", "F"))', '("neither-compiles", "P"))'),
    "M7": (C1, 'if stamp.get("EXIT") != "0":', 'if False:'),
    "N1": (C2, 'status = "KNOWN" if (cid, key, claimed, measured) in KNOWN else "UNEXPECTED"',
           'status = "KNOWN" if (cid, key, measured) in {(k[0], k[1], k[3]) for k in KNOWN} else "UNEXPECTED"'),
    "N2": (C2, 'for row in sorted(set(pinned) - set(current)):', 'for row in []:'),
    "N3": (C2, 'st = selftest_fn(lane, rev, work) if selftest_fn else selftest_defects(lane, rev, work)', 'st = []'),
    "N4": (C2, 'if text == original:', 'if False:'),
    "N5": (C2, '"Before (BASE" in line', '"**Before" in line'),
    "N6": (C2, '    work.mkdir(parents=True, exist_ok=True)\n    st = selftest_fn', '    pass\n    st = selftest_fn'),
}

def main(lane, rev, out):
    out = pathlib.Path(out)
    for mid, (path, old, new) in MUTANTS.items():
        if mid == "N6":
            old = "    work.mkdir(parents=True, exist_ok=True)\n    st = selftest_fn"
            new = "    pass\n    st = selftest_fn"
        text = subprocess.run(["git", "-C", lane, "show", f"{rev}:{path}"], capture_output=True, check=True).stdout.decode()
        assert text.count(old) == 1, (mid, text.count(old))
        mutated = text.replace(old, new)
        d = out / mid
        d.mkdir(parents=True, exist_ok=True)
        (d / pathlib.Path(path).name).write_text(mutated)
        diff = "".join(difflib.unified_diff(text.splitlines(True), mutated.splitlines(True),
                                            f"a/{path}", f"b/{path}"))
        (out / f"{mid}.diff").write_text(diff)
        print(mid, path, "ok")

if __name__ == "__main__":
    main(*sys.argv[1:4])
