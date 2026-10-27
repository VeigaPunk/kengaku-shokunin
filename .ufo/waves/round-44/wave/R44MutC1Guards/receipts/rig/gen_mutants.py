#!/usr/bin/env python3
"""Round-44 C1 counter mutants: single-line/spans mutations at the same guards as round-43's
M01-M15, translated to the round-44 counter's text (plans/round44_c1_verify.py)."""
import hashlib
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
COUNTER = LANE / "plans" / "round44_c1_verify.py"
OUT = pathlib.Path("/fast/scratch/hyaku/kengaku-r44/R44MutC1Guards/mut")

MUTANTS = {
    # M01 SITE_EQUAL leg g forced equal
    "M01": ("    return tuple(mut_sites) == tuple(ref_sites)",
             "    return True"),
    # M02 reference trace 1 dropped (first record empty)
    "M02": ("                _r_rc, _r_cls, _r_lines, r_sites = runner.run(tool, refs[tool][0], fx, trace=True, span=span)",
             "                r_sites = 0, frozenset(), frozenset(), ()"),
    # M03 reference trace 2 = first (stability check self-comparison)
    "M03": ("                _r_rc, _r_cls, _r_lines, r_sites2 = runner.run(tool, refs[tool][0], fx, trace=True, span=span)",
             "                r_sites2 = r_sites"),
    # M04 newline-count validity off
    "M04": ('                    or old.count("\\n") != new.count("\\n") \\',
             '                    or False \\'),
    # M05 symlink_breach off
    "M05": ("            if p.is_symlink() and not p.resolve().is_relative_to(d):",
             "            if False:"),
    # M06 order_argv_breach blob branch off
    "M06": ('        if got[0] == 0 and got[1] != "blob":',
             '        if False:'),
    # M07 repo_breach toplevel branch vacuous
    "M07": ('                ok = p == repo if what.endswith("toplevel") else p.is_relative_to(d)',
             '                ok = True if what.endswith("toplevel") else p.is_relative_to(d)'),
    # M08 repo_breach worktree branch off
    "M08": ("        if val:",
             "        if False:"),
    # M09 exhibits defects conjunct dropped
    "M09": ('    return cls in ref[1] and cls in set(fx["defects"]) and cls not in mut[1]  # silence',
             '    return cls in ref[1] and cls not in mut[1]  # silence'),
    # M10 floors sum term off
    "M10": ("and sum(FLOORS.values()) == TOTAL",
             "and True"),
    # M11 unattributed counted as survived
    "M11": ("                unattributed += 1",
             "                survived += 1"),
    # M12 fingerprint content term off (paths only)
    "M12": ("                content = file_sha256(p)",
             "                content = \"\""),
    # M13 sidechannel scan off
    "M13": ("        if hits:",
             "        if False:"),
    # M14 PINS-AFTER frozen empty
    "M14": ("        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]",
             "        after = []"),
    # M15 null run check off
    "M15": ('                if res != ref[fx["fid"]]:',
             '                if False:'),
}

def main():
    src = COUNTER.read_text()
    out = {}
    for mid, (old, new) in MUTANTS.items():
        if src.count(old) != 1:
            raise SystemExit(f"{mid}: anchor not unique (count={src.count(old)})")
        mut = src.replace(old, new, 1)
        p = OUT / f"{mid}.py"
        p.write_text(mut)
        out[mid] = hashlib.sha256(mut.encode()).hexdigest()
    base = OUT / "base.py"
    base.write_text(src)
    out["base"] = hashlib.sha256(src.encode()).hexdigest()
    for k, v in out.items():
        print(f"{k} {v}")

if __name__ == "__main__":
    sys.exit(main())
