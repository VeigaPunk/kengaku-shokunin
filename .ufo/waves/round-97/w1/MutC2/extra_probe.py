#!/usr/bin/env python3
"""MutC2 extras: --base override, added probe row, hidden gate row, and diff capture."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r97/MutC2")
import driver as D

def main():
    base_sha = D.build_base()
    ev = D.ROOT / "ev"
    out = {}

    # A: --base override to the measured revision itself
    rc, txt = D.run_census(D.T, D.T)
    out["base_override_self"] = dict(rc=rc, out=txt)
    print("A --base T rc=", rc, txt.splitlines()[-1])

    # B: add a parsed probe row (new script, no spelling) -> no finding, rev=172
    def add_probe(r):
        p = r / "SKILL.md"; lines, idxs = D.rows_of(p.read_text())
        (r / "plans/extra_probe.py").write_text("import sys\nsys.exit(0)\n")
        new = ("| `extra-probe` | probe | `python3 plans/extra_probe.py` | `0` clean · `1` failed | "
               "none | pins | read-only | kengaku |")
        lines.insert(idxs[-1] + 1, new)
        p.write_text("\n".join(lines))
    rev = D.build_mutant(base_sha, "extra-probe-row", add_probe)
    rc, txt = D.run_census(rev, base_sha)
    out["added_probe_row"] = dict(rc=rc, out=txt)
    print("B added probe row rc=", rc, [l for l in txt.splitlines() if l.startswith(("ROWS", "PREDICATE"))])

    # C: hidden gate row (no backticked name) -> rev stays 171, pass
    def add_hidden(r):
        p = r / "SKILL.md"; lines, idxs = D.rows_of(p.read_text())
        new = ("| hidden-gate | gate | `python3 plans/round37_c2_verify.py` | `0` clean · `1` failed | "
               "none | pins | read-only | kengaku |")
        lines.insert(idxs[-1] + 1, new)
        p.write_text("\n".join(lines))
    rev = D.build_mutant(base_sha, "extra-hidden-row", add_hidden)
    rc, txt = D.run_census(rev, base_sha)
    out["hidden_gate_row"] = dict(rc=rc, out=txt)
    print("C hidden gate row rc=", rc, [l for l in txt.splitlines() if l.startswith(("ROWS", "PREDICATE"))])

    # D: capture the minimal SKILL.md diffs of the headline survivors
    diffs = {}
    for name in ("mut-45th-kind", "mut-gate-to-Gate", "mut-strip-selftest",
                 "mut-launder-comment", "mut-dead-def", "mut-hidden-row", "mut-decoy-entry"):
        rev = D.git("rev-list", "-1", "--grep", f"^{name}$", "HEAD")
        if not rev:
            continue
        p = subprocess.run(["git", "-C", str(D.REPO), "diff", base_sha, rev, "--", "SKILL.md"],
                           capture_output=True, text=True)
        diffs[name] = p.stdout
    out["diffs"] = diffs
    (ev / "extras.json").write_text(json.dumps(out, indent=1))
    for n, d in diffs.items():
        print(f"\n--- {n}\n{d}")

if __name__ == "__main__":
    main()
